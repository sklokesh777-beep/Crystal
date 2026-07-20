"""
Crystal Trader - central configuration.

Every tunable knob lives here so you can adjust the model without touching
logic code. Values are chosen for a short (1-8 trading day) swing horizon on a
$100,000 account.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Account / capital
# ---------------------------------------------------------------------------
CAPITAL: float = 100_000.0          # total account size in USD
RISK_PER_TRADE: float = 0.01        # fraction of capital risked per trade (1%)
MAX_POSITION_PCT: float = 0.10      # hard cap: no single position > 10% of capital
MAX_CONCURRENT_POSITIONS: int = 8   # cap on simultaneous open trades
MAX_SECTOR_POSITIONS: int = 2       # avoid piling into one sector

# ---------------------------------------------------------------------------
# Holding horizon (trading days)
# ---------------------------------------------------------------------------
MIN_HOLD_DAYS: int = 1
MAX_HOLD_DAYS: int = 8              # hard time-stop; nothing is held longer

# ---------------------------------------------------------------------------
# Costs (per side unless noted) - keep the model honest
# ---------------------------------------------------------------------------
COMMISSION_PER_SHARE: float = 0.005
SLIPPAGE_BPS: float = 5.0           # 5 basis points of slippage per fill

# ---------------------------------------------------------------------------
# Stop-loss / take-profit
# ---------------------------------------------------------------------------
ATR_PERIOD: int = 14
ATR_STOP_MULT: float = 2.0          # stop = entry - ATR_STOP_MULT * ATR
MAX_STOP_PCT: float = 0.12          # reject setups whose stop is wider than 12%
MIN_STOP_PCT: float = 0.015         # floor so tiny stops don't oversize
TARGET_R_MULTIPLES = (1.0, 1.5, 2.0)   # take-profit levels reported (R = risk)
PREFERRED_TARGET_R: float = 1.5     # the "best" TP for a mean-reversion sleeve

# ---------------------------------------------------------------------------
# Entry signal thresholds (mean-reversion sleeve, fits 1-8 day holds)
# ---------------------------------------------------------------------------
RSI2_PERIOD: int = 2
RSI2_OVERSOLD: float = 10.0         # enter when RSI(2) below this
RSI2_EXIT: float = 65.0            # exit when RSI(2) recovers above this
TREND_SMA: int = 200               # only buy dips above the long-term trend
FAST_SMA: int = 5                  # short mean to snap back to
BB_PERIOD: int = 20
BB_STD: float = 2.0

# Liquidity / quality gates
MIN_PRICE: float = 5.0
MIN_AVG_DOLLAR_VOLUME: float = 20_000_000.0   # $20M/day average
MIN_MARKET_CAP: float = 2_000_000_000.0       # $2B

# ---------------------------------------------------------------------------
# Regime filter (index-level risk switch)
# ---------------------------------------------------------------------------
REGIME_SYMBOL: str = "SPY"
REGIME_SMA: int = 200              # risk-on only when SPY > its 200-day SMA

# ---------------------------------------------------------------------------
# Data layer
# ---------------------------------------------------------------------------
HISTORY_PERIOD: str = "2y"         # how much daily history to pull for indicators
CACHE_DIR: str = ".cache"          # on-disk price cache (relative to project root)
CACHE_TTL_MINUTES: int = 30        # re-use cached prices for this long
MAX_RETRIES: int = 4               # network retry attempts
RETRY_BACKOFF_SEC: float = 1.5     # exponential backoff base
REQUEST_PAUSE_SEC: float = 0.4     # polite pause between ticker requests

# ---------------------------------------------------------------------------
# Earnings guard - never enter a trade that would straddle an earnings report
# inside the holding window (gap risk blows through the stop).
# ---------------------------------------------------------------------------
EARNINGS_BLACKOUT_DAYS: int = MAX_HOLD_DAYS + 1

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
OUTPUT_DIR: str = "output"
UNIVERSE_FILE: str = "data/universe.csv"
