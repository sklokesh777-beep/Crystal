# Crystal Trader (v10)

A compact, robust **swing-trading analysis model** you run on your own PC.
It scans a universe of US stocks for short-hold (**1-8 trading day**) mean-reversion
setups, sizes each trade for a **$100,000** account, and gives you an **exact
stop-loss** and a **recommended (best) take-profit** for every idea. It also
produces a deep **research dossier** for any single stock (fundamentals,
technicals, earnings calendar, analyst targets, ownership, and news).

> This is a research/paper-trading tool for a finance assignment. It does **not**
> place orders and it is **not** investment advice. Past/backtested behaviour does
> not guarantee future results. You make every trading decision yourself.

---

## What it does

- **Scan** a universe and return ranked, filtered candidates with exact sizing.
- **Plan** any ticker: shares, stop-loss, and a 1R/1.5R/2R take-profit ladder.
- **Profile** a stock: everything Yahoo Finance knows about it, in one screen.
- **Exit** check: tells you if an open position should be closed today.
- **Regime**: risk-on / risk-off switch based on SPY vs its 200-day average.

### Built-in discipline (the "no mistakes" part)
- **Robust data layer** - retries with backoff, on-disk caching, and strict
  validation that **rejects bad rows** (split glitches, NaNs, non-positive
  prices, stale feeds) before they can reach a signal.
- **Earnings blackout** - never proposes a trade that would straddle an earnings
  report inside your 1-8 day window (gap risk blows through stops).
- **Window-aware exits** - a hard time-stop at 8 days plus mean-reversion exits.
- **Fixed-fractional risk** - every trade risks 1% of capital, capped at 10% of
  capital per position.
- **Diversification** - caps how many positions come from one sector.

---

## Install

Requires **Python 3.9+**.

```bash
cd crystal_trader
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
# 1) Market regime (are we risk-on?)
python run.py regime

# 2) Scan the default universe (data/universe.csv) for today's setups
python run.py scan

# 3) Scan a custom list and save CSV + markdown to output/
python run.py scan --tickers AAPL,MSFT,NVDA,JPM,XOM,CAT --save

# 4) Exact trade plan for one idea (stop-loss + best take-profit)
python run.py plan AAPL --entry 326.60
python run.py plan CAT                 # uses last close if --entry omitted
python run.py plan NVDA --stop 195     # manual stop override

# 5) Full research dossier for one stock (add --json to save it)
python run.py profile NVDA --json

# 6) Should I exit an open position?
python run.py exit AAPL --entry-date 2026-07-14
```

### Example: a trade plan

```
TRADE PLAN - AAPL   (capital $100,000, risk 1.0%)
  Entry (ref)      : 326.6
  STOP-LOSS        : 310.40   (4.96% away)
  Shares           : 30
  Notional         : $9,798.00  (9.8% of capital)
  Dollar risk      : $486.00
  Take-profit ladder:
      1R : 342.80
      1.5R : 350.90  <== BEST
      2R : 359.00
  BEST TAKE-PROFIT : 350.90  (reward:risk 1.5:1)
```

---

## How it works

### The edge
The primary sleeve is **RSI(2) mean-reversion inside an uptrend** (buy a short,
sharp pullback in a stock trading above its 200-day average). This setup
statistically resolves in **1-8 trading days**, which is exactly your holding
window. A 0-100 **confidence score** blends corroborating signals (Bollinger
%B, trend, ADX, EMA structure) and is used to *rank* candidates - not as a hard
gate. (Honest caveat: more indicators help you prioritise when you can only take
a few trades; they do not, by themselves, raise the win rate.)

### Stop-loss (exact)
`stop = entry - 2 x ATR(14)`, clamped so it is never wider than 12% or tighter
than 1.5% of price. Setups whose natural stop is wider than 12% are rejected as
too risky/illiquid.

### Position size
```
shares = floor( (capital x 1%) / (entry - stop) )      # fixed 1% risk
```
then capped so no single position exceeds 10% of capital.

### Take-profit (best)
Targets are expressed as **R-multiples** of the risk distance. Because the
mean-reversion sleeve wins *often but small*, the recommended target is a modest
**1.5R** rather than a greedy 2R+ (which tends to turn winners into losers on
this style). All of 1R / 1.5R / 2R are printed so you can choose.

### Exit logic
A position is closed on the first of:
1. RSI(2) recovers above 65 (reversion complete),
2. price closes back above the fast SMA (snapped back), or
3. the 8-day time-stop is hit.

---

## Configuration

Every knob lives in **`config.py`** - capital, risk %, hold window, ATR
multiplier, thresholds, liquidity gates, earnings blackout, and the universe
file path. Change values there; no logic code needs editing.

## Project layout

```
crystal_trader/
├── run.py                # CLI entry point
├── config.py             # all tunable settings
├── requirements.txt
├── data/universe.csv     # tickers to scan (edit freely)
└── crystal/
    ├── data.py           # robust Yahoo Finance loader (retry/cache/validate)
    ├── indicators.py     # RSI, ATR, Bollinger, MACD, ADX, Stochastic, RVOL...
    ├── signals.py        # entry/exit logic + confidence score + regime
    ├── risk.py           # sizing, exact stop-loss, best take-profit
    ├── screener.py       # universe scan + earnings/sector filters
    ├── profile.py        # deep single-stock research dossier
    └── report.py         # console tables + CSV/markdown/JSON output
```

## Notes & limitations
- Data comes from Yahoo Finance via `yfinance`; it can rate-limit or change
  schemas. The data layer retries and caches to soften this, and skips any
  ticker it cannot trust.
- `.info` fundamental fields are occasionally missing for some tickers; the
  profile degrades gracefully (shows what is available).
- A 10-day / 60-trade sprint is statistically noisy - the tool's value is
  disciplined, repeatable risk management, not a guaranteed profit.
