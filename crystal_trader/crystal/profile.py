"""
Deep single-stock research dossier.

Pulls "everything about a stock" from Yahoo Finance and packages it into one
structured object: company facts, valuation & fundamentals, price/technical
snapshot, earnings calendar (with a holding-window blackout check), analyst
recommendations & price targets, dividends, institutional holders, and the
latest news headlines.

Every remote call is wrapped so a missing field never crashes the dossier -
Yahoo's schema is inconsistent across tickers.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError as exc:  # pragma: no cover
    raise ImportError("yfinance is required: pip install yfinance") from exc

import config
from . import data as datamod
from . import indicators as ind

log = logging.getLogger("crystal.profile")


def _safe(fn, default=None):
    try:
        return fn()
    except Exception as exc:
        log.debug("profile field failed: %s", exc)
        return default


def _fmt_big(n) -> Optional[str]:
    if n is None or (isinstance(n, float) and np.isnan(n)):
        return None
    try:
        n = float(n)
    except (TypeError, ValueError):
        return None
    for unit, div in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(n) >= div:
            return f"{n/div:.2f}{unit}"
    return f"{n:.2f}"


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------
def _company(info: dict) -> dict:
    return {
        "name": info.get("longName") or info.get("shortName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "country": info.get("country"),
        "employees": info.get("fullTimeEmployees"),
        "website": info.get("website"),
        "summary": (info.get("longBusinessSummary") or "")[:600],
    }


def _valuation(info: dict) -> dict:
    return {
        "market_cap": _fmt_big(info.get("marketCap")),
        "enterprise_value": _fmt_big(info.get("enterpriseValue")),
        "trailing_pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "peg_ratio": info.get("pegRatio"),
        "price_to_book": info.get("priceToBook"),
        "price_to_sales": info.get("priceToSalesTrailing12Months"),
        "profit_margin": info.get("profitMargins"),
        "operating_margin": info.get("operatingMargins"),
        "roe": info.get("returnOnEquity"),
        "revenue_growth": info.get("revenueGrowth"),
        "earnings_growth": info.get("earningsGrowth"),
        "debt_to_equity": info.get("debtToEquity"),
        "beta": info.get("beta"),
        "dividend_yield": info.get("dividendYield"),
        "52w_high": info.get("fiftyTwoWeekHigh"),
        "52w_low": info.get("fiftyTwoWeekLow"),
        "avg_volume": _fmt_big(info.get("averageVolume")),
    }


def _technical(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {}
    e = ind.enrich(df)
    row = e.iloc[-1]

    def g(k):
        v = row.get(k, np.nan)
        return None if (v is None or (isinstance(v, float) and np.isnan(v))) else round(float(v), 2)

    close = float(row["Close"])
    hi52 = e["Close"].tail(252).max()
    lo52 = e["Close"].tail(252).min()
    return {
        "last_close": round(close, 2),
        "rsi2": g("rsi2"),
        "rsi14": g("rsi14"),
        "atr": g("atr"),
        "atr_pct": round(float(row["atr_pct"]) * 100, 2) if not np.isnan(row.get("atr_pct", np.nan)) else None,
        "sma20": g("bb_mid"),
        "sma200": g("sma_trend"),
        "above_200sma": bool(row.get("above_trend", False)),
        "ema50": g("ema50"),
        "pct_b": g("pct_b"),
        "adx": g("adx"),
        "macd_hist": g("macd_hist"),
        "stoch_k": g("stoch_k"),
        "rvol": g("rvol"),
        "roc10": g("roc10"),
        "pct_off_52w_high": round(100 * (close - hi52) / hi52, 2) if hi52 else None,
        "pct_above_52w_low": round(100 * (close - lo52) / lo52, 2) if lo52 else None,
        "trend": "uptrend" if row.get("above_trend", False) else "downtrend",
    }


def _earnings(tk, cfg) -> dict:
    ed = _safe(lambda: tk.get_earnings_dates(limit=8))
    out = {"next_earnings": None, "days_to_earnings": None,
           "in_holding_blackout": False, "recent": []}
    if ed is None or ed.empty:
        return out
    now = pd.Timestamp.now(tz=ed.index.tz) if ed.index.tz else pd.Timestamp.now()
    future = ed[ed.index >= now].sort_index()
    if not future.empty:
        nxt = future.index[0]
        days = (nxt - now).days
        out["next_earnings"] = nxt.date().isoformat()
        out["days_to_earnings"] = int(days)
        out["in_holding_blackout"] = bool(0 <= days <= cfg.EARNINGS_BLACKOUT_DAYS)
    past = ed[ed.index < now].sort_index(ascending=False).head(4)
    for idx, r in past.iterrows():
        out["recent"].append({
            "date": idx.date().isoformat(),
            "eps_est": None if pd.isna(r.get("EPS Estimate")) else float(r["EPS Estimate"]),
            "eps_actual": None if pd.isna(r.get("Reported EPS")) else float(r["Reported EPS"]),
            "surprise_pct": None if pd.isna(r.get("Surprise(%)")) else float(r["Surprise(%)"]),
        })
    return out


def _analysts(tk, info: dict) -> dict:
    out = {
        "recommendation": info.get("recommendationKey"),
        "num_analysts": info.get("numberOfAnalystOpinions"),
        "target_mean": info.get("targetMeanPrice"),
        "target_high": info.get("targetHighPrice"),
        "target_low": info.get("targetLowPrice"),
        "breakdown": None,
    }
    rec = _safe(lambda: tk.recommendations)
    if rec is not None and not rec.empty:
        latest = rec.iloc[0].to_dict()
        out["breakdown"] = {k: int(v) for k, v in latest.items()
                            if k in ("strongBuy", "buy", "hold", "sell", "strongSell")}
    return out


def _holders(tk) -> dict:
    out = {"institutional_pct": None, "insider_pct": None, "top_institutions": []}
    mh = _safe(lambda: tk.major_holders)
    if mh is not None and not getattr(mh, "empty", True):
        try:
            d = mh.to_dict().get(mh.columns[0], {}) if hasattr(mh, "columns") else {}
            out["institutional_pct"] = d.get("institutionsPercentHeld")
            out["insider_pct"] = d.get("insidersPercentHeld")
        except Exception:
            pass
    inst = _safe(lambda: tk.institutional_holders)
    if inst is not None and not getattr(inst, "empty", True):
        for _, r in inst.head(5).iterrows():
            out["top_institutions"].append({
                "holder": r.get("Holder"),
                "shares": _fmt_big(r.get("Shares")),
                "pct_out": r.get("pctHeld"),
            })
    return out


def _news(tk, limit: int = 6) -> list:
    items = _safe(lambda: tk.news, default=[]) or []
    out = []
    for it in items[:limit]:
        c = it.get("content", it) if isinstance(it, dict) else {}
        provider = (c.get("provider") or {}).get("displayName") if isinstance(c.get("provider"), dict) else None
        url = None
        for key in ("canonicalUrl", "clickThroughUrl"):
            v = c.get(key)
            if isinstance(v, dict) and v.get("url"):
                url = v["url"]
                break
        out.append({
            "title": c.get("title"),
            "publisher": provider,
            "published": c.get("pubDate"),
            "summary": (c.get("summary") or c.get("description") or "")[:240],
            "url": url,
        })
    return out


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
def build_profile(ticker: str, cfg=None, with_news: bool = True) -> dict:
    """Assemble the complete research dossier for one ticker."""
    cfg = cfg or config
    ticker = ticker.upper().strip()
    tk = yf.Ticker(ticker)
    info = _safe(lambda: tk.info, default={}) or {}
    df = datamod.get_history(ticker, period=cfg.HISTORY_PERIOD)

    dossier = {
        "ticker": ticker,
        "generated": datetime.now().isoformat(timespec="seconds"),
        "company": _company(info),
        "valuation": _valuation(info),
        "technical": _technical(df),
        "earnings": _earnings(tk, cfg),
        "analysts": _analysts(tk, info),
        "holders": _holders(tk),
        "news": _news(tk) if with_news else [],
        "data_quality": None,
    }
    if df is not None:
        rep = datamod.validate(ticker, df)
        dossier["data_quality"] = str(rep)
    else:
        dossier["data_quality"] = f"[REJECTED] {ticker}: no trustworthy data"
    return dossier
