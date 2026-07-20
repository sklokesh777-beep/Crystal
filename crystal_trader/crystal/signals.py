"""
Swing-trading signal engine.

Primary sleeve: RSI(2) mean-reversion in an uptrend - the classic short-hold
edge (Connors-style). It naturally resolves in 1-8 trading days, which matches
the required holding window. A confidence score (0-100) blends corroborating
indicators; it is used for *ranking*, not as a hard gate (the honest finding
from prior research is that more indicators do not raise win rate, but they do
help prioritise when you can only take a handful of trades).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd

import config
from . import indicators as ind


@dataclass
class Signal:
    ticker: str
    date: pd.Timestamp
    close: float
    direction: str = "long"
    rsi2: float = np.nan
    rsi14: float = np.nan
    pct_b: float = np.nan
    adx: float = np.nan
    atr: float = np.nan
    atr_pct: float = np.nan
    dollar_vol: float = np.nan
    above_trend: bool = False
    score: float = 0.0
    reasons: list = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "ticker": self.ticker,
            "date": self.date.date().isoformat() if hasattr(self.date, "date") else str(self.date),
            "close": round(self.close, 2),
            "rsi2": round(self.rsi2, 1) if not np.isnan(self.rsi2) else None,
            "rsi14": round(self.rsi14, 1) if not np.isnan(self.rsi14) else None,
            "pct_b": round(self.pct_b, 2) if not np.isnan(self.pct_b) else None,
            "adx": round(self.adx, 1) if not np.isnan(self.adx) else None,
            "atr": round(self.atr, 2) if not np.isnan(self.atr) else None,
            "atr_pct": round(self.atr_pct * 100, 2) if not np.isnan(self.atr_pct) else None,
            "score": round(self.score, 1),
            "reasons": "; ".join(self.reasons),
        }


def _confidence_score(row: pd.Series, cfg) -> tuple:
    """Blend corroborating signals into a 0-100 conviction score + reasons."""
    score = 0.0
    reasons = []

    # Deeper oversold on RSI(2) -> stronger snap-back tendency (max 35).
    rsi2 = row["rsi2"]
    if rsi2 <= cfg.RSI2_OVERSOLD:
        pts = 35.0 * (cfg.RSI2_OVERSOLD - min(rsi2, cfg.RSI2_OVERSOLD)) / cfg.RSI2_OVERSOLD
        score += 15.0 + pts * 20.0 / 35.0  # base 15 for triggering + depth bonus
        reasons.append(f"RSI2={rsi2:.1f} oversold")

    # Below lower Bollinger band (max 20).
    pct_b = row.get("pct_b", np.nan)
    if not np.isnan(pct_b) and pct_b < 0.2:
        score += 20.0 * (0.2 - max(pct_b, 0.0)) / 0.2
        reasons.append(f"%B={pct_b:.2f} at band")

    # Trend alignment - dips in uptrends mean-revert more reliably (20).
    if row.get("above_trend", False):
        score += 20.0
        reasons.append("above 200-SMA")

    # Not a runaway downtrend: mild ADX preferred (10).
    adx = row.get("adx", np.nan)
    if not np.isnan(adx) and adx < 35:
        score += 10.0
        reasons.append(f"ADX={adx:.0f} not trending down hard")

    # Pullback still near a rising short EMA (15).
    if not np.isnan(row.get("ema20", np.nan)) and row["Close"] > row["ema50"]:
        score += 15.0
        reasons.append("above 50-EMA")

    return min(score, 100.0), reasons


def entry_signal(ticker: str, df_enriched: pd.DataFrame, cfg=None,
                 regime_ok: bool = True) -> Optional[Signal]:
    """
    Evaluate the *latest* bar for a fresh long entry.

    Returns a Signal if the setup triggers and passes liquidity/quality
    gates, else None. No look-ahead: only the last completed bar is used.
    """
    cfg = cfg or config
    if df_enriched is None or len(df_enriched) < cfg.TREND_SMA // 2:
        return None

    row = df_enriched.iloc[-1]
    close = float(row["Close"])

    # --- hard quality / liquidity gates ---------------------------------
    if close < cfg.MIN_PRICE:
        return None
    if np.isnan(row.get("dollar_vol", np.nan)) or row["dollar_vol"] < cfg.MIN_AVG_DOLLAR_VOLUME:
        return None
    if np.isnan(row.get("atr", np.nan)) or row["atr"] <= 0:
        return None

    # --- core trigger: RSI(2) mean reversion in an uptrend ---------------
    rsi2 = float(row["rsi2"])
    triggered = (rsi2 <= cfg.RSI2_OVERSOLD) and bool(row.get("above_trend", False))
    if not triggered:
        return None

    # Skip if the market regime is risk-off (unless caller overrides).
    if not regime_ok:
        return None

    # Reject setups whose ATR stop would be absurdly wide (data/vol risk).
    stop_dist_pct = (cfg.ATR_STOP_MULT * row["atr"]) / close
    if stop_dist_pct > cfg.MAX_STOP_PCT:
        return None

    score, reasons = _confidence_score(row, cfg)
    sig = Signal(
        ticker=ticker,
        date=df_enriched.index[-1],
        close=close,
        rsi2=rsi2,
        rsi14=float(row.get("rsi14", np.nan)),
        pct_b=float(row.get("pct_b", np.nan)),
        adx=float(row.get("adx", np.nan)),
        atr=float(row["atr"]),
        atr_pct=float(row.get("atr_pct", np.nan)),
        dollar_vol=float(row.get("dollar_vol", np.nan)),
        above_trend=bool(row.get("above_trend", False)),
        score=score,
        reasons=reasons,
    )
    return sig


def exit_signal(df_enriched: pd.DataFrame, entry_date, cfg=None) -> Optional[dict]:
    """
    Decide whether an open position should be closed on the latest bar.

    Exit rules (first that fires wins):
      1. RSI(2) recovered above RSI2_EXIT  -> mean reversion complete.
      2. Close back above the fast SMA     -> snapped back.
      3. Time stop: held >= MAX_HOLD_DAYS.
    (Stop-loss / take-profit price levels are handled by risk.py + the broker.)
    """
    cfg = cfg or config
    if df_enriched is None or df_enriched.empty:
        return None
    row = df_enriched.iloc[-1]
    last_date = df_enriched.index[-1]

    held_days = None
    try:
        ed = pd.Timestamp(entry_date)
        if ed.tzinfo and last_date.tzinfo is None:
            ed = ed.tz_localize(None)
        held_days = (last_date.tz_localize(None) if last_date.tzinfo else last_date) - \
                    (ed.tz_localize(None) if getattr(ed, "tzinfo", None) else ed)
        held_days = held_days.days
    except Exception:
        held_days = None

    if float(row.get("rsi2", 0)) >= cfg.RSI2_EXIT:
        return {"exit": True, "reason": f"RSI2 recovered to {row['rsi2']:.1f}", "held_days": held_days}
    if not np.isnan(row.get("sma_fast", np.nan)) and row["Close"] > row["sma_fast"]:
        return {"exit": True, "reason": "closed above fast SMA (snap-back)", "held_days": held_days}
    if held_days is not None and held_days >= cfg.MAX_HOLD_DAYS:
        return {"exit": True, "reason": f"time stop ({held_days}d >= {cfg.MAX_HOLD_DAYS}d)", "held_days": held_days}
    return {"exit": False, "reason": "hold", "held_days": held_days}


def market_regime(cfg=None) -> dict:
    """Risk-on/off switch based on the index vs its long SMA."""
    from . import data as datamod
    cfg = cfg or config
    idx = datamod.get_regime_series(cfg.REGIME_SYMBOL)
    if idx is None or len(idx) < cfg.REGIME_SMA:
        return {"regime": "unknown", "risk_on": True, "detail": "insufficient index data"}
    sma_ = ind.sma(idx["Close"], cfg.REGIME_SMA).iloc[-1]
    px = float(idx["Close"].iloc[-1])
    risk_on = px > sma_
    return {
        "regime": "risk-on" if risk_on else "risk-off",
        "risk_on": bool(risk_on),
        "index": cfg.REGIME_SYMBOL,
        "price": round(px, 2),
        "sma": round(float(sma_), 2),
        "detail": f"{cfg.REGIME_SYMBOL} {'>' if risk_on else '<'} {cfg.REGIME_SMA}-SMA",
    }
