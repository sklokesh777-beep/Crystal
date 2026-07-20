"""
Universe screener.

Pipeline for each ticker:
  1. Pull validated history (data layer rejects bad data automatically).
  2. Enrich with indicators.
  3. Evaluate the entry signal on the latest bar.
  4. Apply the earnings blackout (no trade that straddles earnings in the
     holding window).
  5. Build an exact trade plan (shares, stop-loss, best take-profit).

Survivors are ranked by confidence score, then a diversification pass caps how
many positions come from any single sector so the final list is not one
correlated bet.
"""
from __future__ import annotations

import csv
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

try:
    import yfinance as yf
except ImportError as exc:  # pragma: no cover
    raise ImportError("yfinance is required") from exc

import config
from . import data as datamod
from . import indicators as ind
from . import signals as sig
from . import risk as riskmod

log = logging.getLogger("crystal.screener")


@dataclass
class Candidate:
    signal: sig.Signal
    plan: riskmod.TradePlan
    sector: str = "Unknown"
    next_earnings: Optional[str] = None
    days_to_earnings: Optional[int] = None

    def as_row(self) -> dict:
        s = self.signal.as_dict()
        p = self.plan.as_dict()
        return {
            "ticker": self.signal.ticker,
            "sector": self.sector,
            "score": s["score"],
            "close": s["close"],
            "rsi2": s["rsi2"],
            "entry": p["entry"],
            "stop_loss": p["stop_loss"],
            "stop_pct": p["stop_pct"],
            "shares": p["shares"],
            "notional": p["notional"],
            "dollar_risk": p["dollar_risk"],
            "capital_pct": p["capital_pct"],
            "best_take_profit": p["best_take_profit"],
            "reward_risk": p["reward_risk"],
            "days_to_earnings": self.days_to_earnings,
            "reasons": s["reasons"],
            "warnings": p["warnings"],
        }


def load_universe(path: str = None) -> list:
    """Read tickers from a CSV (first column, or a 'ticker'/'symbol' column)."""
    path = path or config.UNIVERSE_FILE
    if not os.path.exists(path):
        raise FileNotFoundError(f"universe file not found: {path}")
    tickers = []
    with open(path, newline="") as fh:
        reader = csv.reader(fh)
        rows = list(reader)
    if not rows:
        return []
    header = [c.strip().lower() for c in rows[0]]
    col = 0
    if "ticker" in header:
        col = header.index("ticker")
    elif "symbol" in header:
        col = header.index("symbol")
        rows = rows[1:]
    start = 1 if header[col] in ("ticker", "symbol") else 0
    for r in rows[start:]:
        if r and r[col].strip():
            t = r[col].strip().upper()
            if t and not t.startswith("#"):
                tickers.append(t)
    # de-dup, keep order
    seen, out = set(), []
    for t in tickers:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def _earnings_guard(ticker: str, cfg) -> tuple:
    """Return (blocked, next_date_iso, days_to). Blocks if earnings in window."""
    try:
        ed = yf.Ticker(ticker).get_earnings_dates(limit=8)
        if ed is None or ed.empty:
            return False, None, None
        now = pd.Timestamp.now(tz=ed.index.tz) if ed.index.tz else pd.Timestamp.now()
        future = ed[ed.index >= now].sort_index()
        if future.empty:
            return False, None, None
        nxt = future.index[0]
        days = int((nxt - now).days)
        blocked = 0 <= days <= cfg.EARNINGS_BLACKOUT_DAYS
        return blocked, nxt.date().isoformat(), days
    except Exception as exc:
        log.debug("earnings guard failed for %s: %s", ticker, exc)
        return False, None, None


def scan(
    tickers=None,
    cfg=None,
    check_regime: bool = True,
    check_earnings: bool = True,
    diversify: bool = True,
    progress: bool = True,
) -> dict:
    """
    Run the full screen. Returns:
        {"regime": {...}, "candidates": [Candidate,...], "scanned": n, "rejected": {...}}
    """
    cfg = cfg or config
    tickers = tickers or load_universe(cfg.UNIVERSE_FILE)

    regime = sig.market_regime(cfg) if check_regime else {"risk_on": True, "regime": "ignored"}
    risk_on = regime.get("risk_on", True)

    candidates = []
    rejected = {"data": 0, "no_signal": 0, "earnings": 0, "unsizable": 0}
    scanned = 0

    for i, t in enumerate(tickers):
        if progress and i % 25 == 0:
            log.info("scanning %d/%d ...", i, len(tickers))
        df = datamod.get_history(t, period=cfg.HISTORY_PERIOD)
        if df is None or len(df) < 60:
            rejected["data"] += 1
            continue
        scanned += 1

        enriched = ind.enrich(df, cfg)
        signal = sig.entry_signal(t, enriched, cfg, regime_ok=risk_on)
        if signal is None:
            rejected["no_signal"] += 1
            continue

        blocked, nxt, days = (False, None, None)
        if check_earnings:
            blocked, nxt, days = _earnings_guard(t, cfg)
            if blocked:
                rejected["earnings"] += 1
                continue

        # Entry is next session's open in practice; we plan off the last close.
        plan = riskmod.build_plan(t, entry=signal.close, atr=signal.atr, cfg=cfg)
        if plan is None or plan.shares < 1:
            rejected["unsizable"] += 1
            continue

        sector = _safe_sector(t)
        candidates.append(Candidate(
            signal=signal, plan=plan, sector=sector,
            next_earnings=nxt, days_to_earnings=days,
        ))
        time.sleep(cfg.REQUEST_PAUSE_SEC if not _cache_hit(t, cfg) else 0)

    # rank by conviction
    candidates.sort(key=lambda c: c.signal.score, reverse=True)

    if diversify:
        candidates = _diversify(candidates, cfg)

    return {
        "regime": regime,
        "candidates": candidates,
        "scanned": scanned,
        "rejected": rejected,
        "universe_size": len(tickers),
    }


_SECTOR_CACHE = {}


def _safe_sector(ticker: str) -> str:
    if ticker in _SECTOR_CACHE:
        return _SECTOR_CACHE[ticker]
    sector = "Unknown"
    try:
        info = yf.Ticker(ticker).info
        sector = info.get("sector") or "Unknown"
    except Exception:
        pass
    _SECTOR_CACHE[ticker] = sector
    return sector


def _cache_hit(ticker: str, cfg) -> bool:
    path = datamod._cache_path(ticker, cfg.HISTORY_PERIOD, "1d")
    return datamod._read_cache(path, cfg.CACHE_TTL_MINUTES) is not None


def _diversify(candidates, cfg) -> list:
    """Keep the best N per sector and cap total concurrent positions."""
    per_sector = {}
    kept = []
    for c in candidates:
        n = per_sector.get(c.sector, 0)
        if n >= cfg.MAX_SECTOR_POSITIONS:
            continue
        per_sector[c.sector] = n + 1
        kept.append(c)
        if len(kept) >= cfg.MAX_CONCURRENT_POSITIONS:
            break
    return kept
