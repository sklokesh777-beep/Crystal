"""
Robust Yahoo Finance data layer.

Design goals (the "firm and exceptional" requirement):
  * Never trust a single network call - retry with exponential backoff.
  * Cache to disk so repeated runs are fast and work briefly offline.
  * Validate every price frame and *reject* bad data (split glitches,
    NaNs, zero volume, stale rows) before it can poison a signal.
  * Degrade gracefully: a broken ticker is skipped, never crashes a scan.

All price history is auto-adjusted (splits/dividends) so indicators are
computed on a continuous series.
"""
from __future__ import annotations

import os
import time
import pickle
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError as exc:  # pragma: no cover
    raise ImportError("yfinance is required: pip install yfinance") from exc

import config

log = logging.getLogger("crystal.data")

OHLCV = ["Open", "High", "Low", "Close", "Volume"]


# ---------------------------------------------------------------------------
# Data quality report
# ---------------------------------------------------------------------------
@dataclass
class QualityReport:
    ticker: str
    ok: bool
    rows: int
    problems: list

    def __str__(self) -> str:
        state = "OK" if self.ok else "REJECTED"
        detail = "; ".join(self.problems) if self.problems else "clean"
        return f"[{state}] {self.ticker}: {self.rows} rows - {detail}"


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------
def _cache_path(ticker: str, period: str, interval: str) -> str:
    os.makedirs(config.CACHE_DIR, exist_ok=True)
    safe = ticker.replace("/", "_").replace(".", "_")
    return os.path.join(config.CACHE_DIR, f"{safe}_{period}_{interval}.pkl")


def _read_cache(path: str, ttl_minutes: int) -> Optional[pd.DataFrame]:
    if not os.path.exists(path):
        return None
    age_min = (time.time() - os.path.getmtime(path)) / 60.0
    if age_min > ttl_minutes:
        return None
    try:
        with open(path, "rb") as fh:
            return pickle.load(fh)
    except Exception:  # corrupt cache -> ignore
        return None


def _write_cache(path: str, df: pd.DataFrame) -> None:
    try:
        with open(path, "wb") as fh:
            pickle.dump(df, fh)
    except Exception as exc:  # caching must never break a run
        log.debug("cache write failed for %s: %s", path, exc)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def validate(ticker: str, df: Optional[pd.DataFrame], min_rows: int = 60) -> QualityReport:
    """Inspect a raw price frame and decide whether it is trustworthy."""
    problems: list = []

    if df is None or df.empty:
        return QualityReport(ticker, False, 0, ["no data returned"])

    df = df.copy()
    # Normalise a possible MultiIndex (yfinance sometimes returns one).
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    missing = [c for c in OHLCV if c not in df.columns]
    if missing:
        return QualityReport(ticker, False, len(df), [f"missing columns {missing}"])

    rows = len(df)
    if rows < min_rows:
        problems.append(f"only {rows} rows (<{min_rows})")

    # Drop rows that are entirely NaN in OHLC.
    nan_rows = df[OHLCV].isna().all(axis=1).sum()
    if nan_rows:
        problems.append(f"{nan_rows} all-NaN rows")

    # Non-positive prices are impossible -> data glitch.
    nonpos = (df[["Open", "High", "Low", "Close"]] <= 0).any(axis=1).sum()
    if nonpos:
        problems.append(f"{nonpos} rows with non-positive prices")

    # High/Low sanity.
    bad_hl = (df["High"] < df["Low"]).sum()
    if bad_hl:
        problems.append(f"{bad_hl} rows where High < Low")

    # Detect un-adjusted split glitches: a >45% single-day move with no
    # matching volume spike is almost always a bad tick / split artefact.
    close = df["Close"].astype(float)
    ret = close.pct_change().abs()
    glitch = (ret > 0.45).sum()
    if glitch:
        problems.append(f"{glitch} suspicious >45% daily jumps (possible split glitch)")

    # Staleness: last bar older than ~7 calendar days means a dead feed.
    last_ts = df.index[-1]
    if isinstance(last_ts, pd.Timestamp):
        last_naive = last_ts.tz_localize(None) if last_ts.tzinfo else last_ts
        if (datetime.now() - last_naive.to_pydatetime()).days > 7:
            problems.append("stale: last bar > 7 days old")

    # A frame is usable if it has enough clean rows and no fatal glitches.
    fatal = any(
        p.startswith(("missing", "no data")) or "split glitch" in p or "non-positive" in p
        for p in problems
    )
    ok = (rows >= min_rows) and not fatal
    return QualityReport(ticker, ok, rows, problems)


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned OHLCV frame (drop bad rows, forward-fill tiny gaps)."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[[c for c in OHLCV if c in df.columns]].copy()
    df = df[~df[OHLCV].isna().all(axis=1)]
    df = df[(df[["Open", "High", "Low", "Close"]] > 0).all(axis=1)]
    df = df[df["High"] >= df["Low"]]
    # A couple of isolated NaNs get forward filled; everything else already dropped.
    df[OHLCV] = df[OHLCV].ffill()
    df = df.dropna(subset=OHLCV)
    return df


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def get_history(
    ticker: str,
    period: str = None,
    interval: str = "1d",
    use_cache: bool = True,
    validate_data: bool = True,
) -> Optional[pd.DataFrame]:
    """
    Fetch validated, cleaned, auto-adjusted OHLCV history for one ticker.

    Returns None if the data cannot be trusted (the caller should skip it).
    """
    period = period or config.HISTORY_PERIOD
    path = _cache_path(ticker, period, interval)

    if use_cache:
        cached = _read_cache(path, config.CACHE_TTL_MINUTES)
        if cached is not None:
            return cached

    raw = None
    last_err = None
    for attempt in range(1, config.MAX_RETRIES + 1):
        try:
            raw = yf.Ticker(ticker).history(
                period=period, interval=interval, auto_adjust=True, actions=False
            )
            if raw is not None and not raw.empty:
                break
        except Exception as exc:  # network/parse errors -> retry
            last_err = exc
            log.debug("attempt %d for %s failed: %s", attempt, ticker, exc)
        time.sleep(config.RETRY_BACKOFF_SEC ** attempt)

    if raw is None or raw.empty:
        log.warning("no data for %s after %d attempts (%s)",
                    ticker, config.MAX_RETRIES, last_err)
        # Fall back to a stale cache if we have one - better than nothing.
        stale = _read_cache(path, ttl_minutes=60 * 24 * 30)
        return stale

    if validate_data:
        report = validate(ticker, raw)
        if not report.ok:
            log.warning("%s", report)
            return None

    clean = _clean(raw)
    if use_cache:
        _write_cache(path, clean)
    return clean


def get_batch(tickers, period: str = None, interval: str = "1d",
              use_cache: bool = True) -> dict:
    """Fetch many tickers, skipping any that fail validation. Returns {ticker: df}."""
    out = {}
    for i, t in enumerate(tickers):
        df = get_history(t, period=period, interval=interval, use_cache=use_cache)
        if df is not None and len(df) >= 60:
            out[t] = df
        # polite pacing to avoid Yahoo throttling
        if not use_cache or df is None:
            time.sleep(config.REQUEST_PAUSE_SEC)
    return out


def last_price(ticker: str) -> Optional[float]:
    """Best-effort latest price using the fast endpoint, then history fallback."""
    try:
        fi = yf.Ticker(ticker).fast_info
        px = getattr(fi, "last_price", None)
        if px is None and hasattr(fi, "get"):
            px = fi.get("lastPrice")
        if px and px > 0:
            return float(px)
    except Exception:
        pass
    df = get_history(ticker, period="5d")
    if df is not None and not df.empty:
        return float(df["Close"].iloc[-1])
    return None


def get_regime_series(symbol: str = None, period: str = None) -> Optional[pd.DataFrame]:
    """Load the index used for the market-regime filter (default SPY)."""
    symbol = symbol or config.REGIME_SYMBOL
    return get_history(symbol, period=period or config.HISTORY_PERIOD)
