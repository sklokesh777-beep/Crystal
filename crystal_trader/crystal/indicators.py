"""
Vectorised technical indicators.

Every function takes a price DataFrame (Open/High/Low/Close/Volume) or a
Series and returns pandas objects aligned to the input index. No look-ahead:
each value uses only data up to and including that bar.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(period, min_periods=period).mean()


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False, min_periods=period).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Wilder's RSI. period=2 gives the fast mean-reversion trigger."""
    delta = series.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0.0, np.nan)
    out = 100.0 - (100.0 / (1.0 + rs))
    return out.fillna(100.0)  # zero loss -> maximally strong


def true_range(df: pd.DataFrame) -> pd.Series:
    high, low, close = df["High"], df["Low"], df["Close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range (Wilder smoothing)."""
    tr = true_range(df)
    return tr.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()


def bollinger(series: pd.Series, period: int = 20, num_std: float = 2.0):
    mid = sma(series, period)
    std = series.rolling(period, min_periods=period).std(ddof=0)
    upper = mid + num_std * std
    lower = mid - num_std * std
    # %B: 0 at lower band, 1 at upper band
    width = (upper - lower).replace(0.0, np.nan)
    pct_b = (series - lower) / width
    return mid, upper, lower, pct_b


def macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    macd_line = ema(series, fast) - ema(series, slow)
    signal_line = ema(macd_line, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist


def adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average Directional Index - trend strength (0-100)."""
    up_move = df["High"].diff()
    down_move = -df["Low"].diff()
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    tr = true_range(df)
    atr_ = tr.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    plus_di = 100.0 * pd.Series(plus_dm, index=df.index).ewm(
        alpha=1.0 / period, adjust=False, min_periods=period).mean() / atr_
    minus_di = 100.0 * pd.Series(minus_dm, index=df.index).ewm(
        alpha=1.0 / period, adjust=False, min_periods=period).mean() / atr_
    dx = 100.0 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0.0, np.nan)
    return dx.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()


def stochastic(df: pd.DataFrame, k_period: int = 14, d_period: int = 3):
    low_k = df["Low"].rolling(k_period, min_periods=k_period).min()
    high_k = df["High"].rolling(k_period, min_periods=k_period).max()
    denom = (high_k - low_k).replace(0.0, np.nan)
    k = 100.0 * (df["Close"] - low_k) / denom
    d = k.rolling(d_period, min_periods=d_period).mean()
    return k, d


def rvol(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """Relative volume: today's volume vs its rolling average."""
    avg = df["Volume"].rolling(period, min_periods=period).mean()
    return df["Volume"] / avg.replace(0.0, np.nan)


def dollar_volume(df: pd.DataFrame, period: int = 20) -> pd.Series:
    return (df["Close"] * df["Volume"]).rolling(period, min_periods=period).mean()


def roc(series: pd.Series, period: int = 10) -> pd.Series:
    return series.pct_change(period) * 100.0


def enrich(df: pd.DataFrame, cfg=None) -> pd.DataFrame:
    """
    Attach the full indicator set used by the strategy and profile modules.
    Returns a new DataFrame; original is untouched.
    """
    import config as _cfg
    cfg = cfg or _cfg
    out = df.copy()
    close = out["Close"]

    out["rsi2"] = rsi(close, cfg.RSI2_PERIOD)
    out["rsi14"] = rsi(close, 14)
    out["atr"] = atr(out, cfg.ATR_PERIOD)
    out["atr_pct"] = out["atr"] / close
    out["sma_fast"] = sma(close, cfg.FAST_SMA)
    out["sma_trend"] = sma(close, cfg.TREND_SMA)
    out["ema20"] = ema(close, 20)
    out["ema50"] = ema(close, 50)

    mid, up, low, pctb = bollinger(close, cfg.BB_PERIOD, cfg.BB_STD)
    out["bb_mid"], out["bb_up"], out["bb_low"], out["pct_b"] = mid, up, low, pctb

    macd_line, sig, hist = macd(close)
    out["macd"], out["macd_signal"], out["macd_hist"] = macd_line, sig, hist

    out["adx"] = adx(out)
    k, d = stochastic(out)
    out["stoch_k"], out["stoch_d"] = k, d
    out["rvol"] = rvol(out)
    out["dollar_vol"] = dollar_volume(out)
    out["roc10"] = roc(close, 10)
    out["above_trend"] = close > out["sma_trend"]
    return out
