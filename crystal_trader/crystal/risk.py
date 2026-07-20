"""
Risk, position sizing, stop-loss and take-profit.

The anchor rule: risk a fixed fraction of capital per trade. Position size is
derived from the *distance to the stop*, so every trade risks the same dollar
amount regardless of price or volatility.

    shares = floor( (capital * risk_pct) / (entry - stop) )

The stop is an ATR-based level (exact price). Take-profit levels are expressed
as R-multiples of that risk, and a single "best" target is recommended based on
the mean-reversion sleeve's statistical profile (wins are frequent but small,
so a modest target - not a greedy one - maximises expectancy).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

import config


@dataclass
class TradePlan:
    ticker: str
    entry: float
    stop: float
    risk_per_share: float
    stop_pct: float
    shares: int
    notional: float
    dollar_risk: float
    capital_pct: float
    targets: dict = field(default_factory=dict)     # {"1.0R": price, ...}
    best_target: float = 0.0
    best_target_r: float = 0.0
    best_reward_risk: float = 0.0
    capped_by: str = ""                              # "" | "position_cap"
    warnings: list = field(default_factory=list)

    def as_dict(self) -> dict:
        d = {
            "ticker": self.ticker,
            "entry": round(self.entry, 2),
            "stop_loss": round(self.stop, 2),
            "stop_pct": round(self.stop_pct * 100, 2),
            "risk_per_share": round(self.risk_per_share, 2),
            "shares": self.shares,
            "notional": round(self.notional, 2),
            "dollar_risk": round(self.dollar_risk, 2),
            "capital_pct": round(self.capital_pct * 100, 2),
            "best_take_profit": round(self.best_target, 2),
            "best_target_r": self.best_target_r,
            "reward_risk": round(self.best_reward_risk, 2),
            "capped_by": self.capped_by,
            "warnings": "; ".join(self.warnings),
        }
        for k, v in self.targets.items():
            d[f"tp_{k}"] = round(v, 2)
        return d


def compute_stop(entry: float, atr: float, cfg=None) -> float:
    """Exact ATR stop with a percentage floor so tiny ATRs don't oversize."""
    cfg = cfg or config
    atr_stop = entry - cfg.ATR_STOP_MULT * atr
    min_stop = entry * (1.0 - cfg.MAX_STOP_PCT)   # widest allowed
    floor_stop = entry * (1.0 - cfg.MIN_STOP_PCT) # tightest allowed
    # Keep the stop inside [min_stop, floor_stop].
    stop = max(atr_stop, min_stop)
    stop = min(stop, floor_stop)
    return round(stop, 2)


def build_plan(
    ticker: str,
    entry: float,
    atr: float,
    cfg=None,
    capital: float = None,
    stop_override: float = None,
) -> Optional[TradePlan]:
    """
    Produce a full, exact trade plan: shares, stop-loss, and take-profit ladder.
    Returns None if the setup is un-sizable (e.g. zero risk distance).
    """
    cfg = cfg or config
    capital = capital if capital is not None else cfg.CAPITAL

    stop = stop_override if stop_override is not None else compute_stop(entry, atr, cfg)
    risk_per_share = entry - stop
    if risk_per_share <= 0:
        return None

    stop_pct = risk_per_share / entry
    warnings = []

    # --- size by risk -----------------------------------------------------
    dollar_risk_budget = capital * cfg.RISK_PER_TRADE
    raw_shares = dollar_risk_budget / risk_per_share
    shares = int(math.floor(raw_shares))

    capped_by = ""
    # --- enforce max position size ---------------------------------------
    max_shares_by_notional = int(math.floor((capital * cfg.MAX_POSITION_PCT) / entry))
    if shares > max_shares_by_notional:
        shares = max_shares_by_notional
        capped_by = "position_cap"
        warnings.append(
            f"trimmed to {cfg.MAX_POSITION_PCT*100:.0f}% capital cap "
            f"(risk now < {cfg.RISK_PER_TRADE*100:.1f}%)"
        )

    if shares < 1:
        warnings.append("stop too wide to size even 1 share within risk budget")
        shares = 0

    notional = shares * entry
    dollar_risk = shares * risk_per_share
    capital_pct = notional / capital if capital else 0.0

    # --- take-profit ladder (R-multiples) --------------------------------
    targets = {}
    for r in cfg.TARGET_R_MULTIPLES:
        targets[f"{r:g}R"] = round(entry + r * risk_per_share, 2)

    best_r = cfg.PREFERRED_TARGET_R
    best_target = round(entry + best_r * risk_per_share, 2)
    best_reward_risk = best_r  # by construction reward:risk == R multiple

    if stop_pct > cfg.MAX_STOP_PCT:
        warnings.append(f"stop {stop_pct*100:.1f}% exceeds max {cfg.MAX_STOP_PCT*100:.0f}%")

    return TradePlan(
        ticker=ticker,
        entry=round(entry, 2),
        stop=stop,
        risk_per_share=round(risk_per_share, 4),
        stop_pct=stop_pct,
        shares=shares,
        notional=notional,
        dollar_risk=dollar_risk,
        capital_pct=capital_pct,
        targets=targets,
        best_target=best_target,
        best_target_r=best_r,
        best_reward_risk=best_reward_risk,
        warnings=warnings,
        capped_by=capped_by,
    )


def portfolio_risk_check(plans, cfg=None) -> dict:
    """Aggregate risk across a set of plans and flag over-exposure."""
    cfg = cfg or config
    plans = [p for p in plans if p and p.shares > 0]
    total_notional = sum(p.notional for p in plans)
    total_risk = sum(p.dollar_risk for p in plans)
    warnings = []
    if len(plans) > cfg.MAX_CONCURRENT_POSITIONS:
        warnings.append(
            f"{len(plans)} positions > max {cfg.MAX_CONCURRENT_POSITIONS} concurrent"
        )
    if total_notional > cfg.CAPITAL:
        warnings.append("total notional exceeds capital (leverage)")
    return {
        "positions": len(plans),
        "total_notional": round(total_notional, 2),
        "capital_deployed_pct": round(100 * total_notional / cfg.CAPITAL, 2),
        "total_dollar_risk": round(total_risk, 2),
        "portfolio_risk_pct": round(100 * total_risk / cfg.CAPITAL, 2),
        "warnings": warnings,
    }
