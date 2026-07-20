"""
Output helpers: pretty console tables + markdown/CSV files.
"""
from __future__ import annotations

import csv
import json
import os
from datetime import datetime

import config

try:
    from tabulate import tabulate
    _HAS_TAB = True
except ImportError:  # graceful fallback
    _HAS_TAB = False


def _table(rows, headers):
    if not rows:
        return "(none)"
    if _HAS_TAB:
        return tabulate(rows, headers=headers, tablefmt="github", floatfmt=".2f")
    # minimal fallback
    line = " | ".join(str(h) for h in headers)
    out = [line, "-" * len(line)]
    for r in rows:
        out.append(" | ".join(str(x) for x in r))
    return "\n".join(out)


def scan_console(result) -> str:
    regime = result["regime"]
    cands = result["candidates"]
    lines = []
    lines.append("=" * 78)
    lines.append(f"CRYSTAL TRADER - watchlist  ({datetime.now():%Y-%m-%d %H:%M})")
    lines.append(f"Capital ${config.CAPITAL:,.0f} | risk {config.RISK_PER_TRADE*100:.1f}%/trade "
                 f"| hold {config.MIN_HOLD_DAYS}-{config.MAX_HOLD_DAYS}d")
    lines.append(f"Market regime: {regime.get('regime')} ({regime.get('detail','')})")
    lines.append(f"Scanned {result['scanned']}/{result['universe_size']} | "
                 f"rejected: {result['rejected']}")
    lines.append("=" * 78)

    headers = ["Ticker", "Sector", "Score", "Entry", "Stop", "Stop%",
               "Shares", "Notional", "$Risk", "Cap%", "BestTP", "R:R", "ToEarn"]
    rows = []
    for c in cands:
        r = c.as_row()
        rows.append([
            r["ticker"], (r["sector"] or "")[:12], r["score"], r["entry"],
            r["stop_loss"], r["stop_pct"], r["shares"], r["notional"],
            r["dollar_risk"], r["capital_pct"], r["best_take_profit"],
            r["reward_risk"], r["days_to_earnings"],
        ])
    lines.append(_table(rows, headers))

    # portfolio-level risk summary
    from . import risk as riskmod
    pr = riskmod.portfolio_risk_check([c.plan for c in cands])
    lines.append("")
    lines.append(f"If all taken: {pr['positions']} positions | "
                 f"deployed {pr['capital_deployed_pct']}% | "
                 f"portfolio risk {pr['portfolio_risk_pct']}%")
    if pr["warnings"]:
        lines.append("WARN: " + "; ".join(pr["warnings"]))
    if not cands:
        lines.append("\nNo qualifying setups today. Cash is a position.")
    return "\n".join(lines)


def scan_save(result, out_dir: str = None) -> dict:
    out_dir = out_dir or config.OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d")
    csv_path = os.path.join(out_dir, f"watchlist_{stamp}.csv")
    md_path = os.path.join(out_dir, f"watchlist_{stamp}.md")

    rows = [c.as_row() for c in result["candidates"]]
    if rows:
        with open(csv_path, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    with open(md_path, "w") as fh:
        fh.write("# Crystal Trader watchlist\n\n")
        fh.write(f"_{datetime.now():%Y-%m-%d %H:%M}_\n\n")
        fh.write(f"- Capital: ${config.CAPITAL:,.0f}\n")
        fh.write(f"- Risk per trade: {config.RISK_PER_TRADE*100:.1f}%\n")
        fh.write(f"- Hold window: {config.MIN_HOLD_DAYS}-{config.MAX_HOLD_DAYS} trading days\n")
        fh.write(f"- Regime: {result['regime'].get('regime')} "
                 f"({result['regime'].get('detail','')})\n\n")
        fh.write("```\n")
        fh.write(scan_console(result))
        fh.write("\n```\n")
    return {"csv": csv_path if rows else None, "md": md_path}


def profile_console(dossier: dict) -> str:
    d = dossier
    L = []
    c = d["company"]
    L.append("=" * 78)
    L.append(f"{d['ticker']} - {c.get('name') or ''}")
    L.append(f"{c.get('sector') or '?'} / {c.get('industry') or '?'} | "
             f"{c.get('country') or '?'} | {c.get('employees') or '?'} employees")
    L.append("=" * 78)
    if c.get("summary"):
        L.append(c["summary"])
        L.append("")

    v = d["valuation"]
    L.append("-- VALUATION & FUNDAMENTALS " + "-" * 49)
    L.append(_kv([
        ("Market cap", v.get("market_cap")), ("Enterprise val", v.get("enterprise_value")),
        ("Trailing P/E", v.get("trailing_pe")), ("Forward P/E", v.get("forward_pe")),
        ("PEG", v.get("peg_ratio")), ("P/B", v.get("price_to_book")),
        ("P/S", v.get("price_to_sales")), ("Profit margin", v.get("profit_margin")),
        ("ROE", v.get("roe")), ("Rev growth", v.get("revenue_growth")),
        ("Debt/Equity", v.get("debt_to_equity")), ("Beta", v.get("beta")),
        ("Div yield", v.get("dividend_yield")), ("52w high", v.get("52w_high")),
        ("52w low", v.get("52w_low")), ("Avg vol", v.get("avg_volume")),
    ]))

    t = d["technical"]
    if t:
        L.append("")
        L.append("-- TECHNICAL SNAPSHOT " + "-" * 55)
        L.append(_kv([
            ("Last close", t.get("last_close")), ("Trend", t.get("trend")),
            ("RSI(2)", t.get("rsi2")), ("RSI(14)", t.get("rsi14")),
            ("ATR", t.get("atr")), ("ATR %", t.get("atr_pct")),
            ("SMA20", t.get("sma20")), ("SMA200", t.get("sma200")),
            ("%B", t.get("pct_b")), ("ADX", t.get("adx")),
            ("Stoch %K", t.get("stoch_k")), ("RVOL", t.get("rvol")),
            ("Off 52w high %", t.get("pct_off_52w_high")),
            ("Above 52w low %", t.get("pct_above_52w_low")),
        ]))

    e = d["earnings"]
    L.append("")
    L.append("-- EARNINGS " + "-" * 65)
    L.append(f"Next: {e.get('next_earnings')} (in {e.get('days_to_earnings')} days) | "
             f"holding-window blackout: {'YES - AVOID' if e.get('in_holding_blackout') else 'no'}")
    for r in e.get("recent", [])[:4]:
        L.append(f"  {r['date']}: est {r['eps_est']} / actual {r['eps_actual']} "
                 f"(surprise {r['surprise_pct']}%)")

    a = d["analysts"]
    L.append("")
    L.append("-- ANALYSTS " + "-" * 65)
    L.append(f"Consensus: {a.get('recommendation')} | analysts: {a.get('num_analysts')} | "
             f"target mean {a.get('target_mean')} (low {a.get('target_low')} / "
             f"high {a.get('target_high')})")
    if a.get("breakdown"):
        L.append("  " + " ".join(f"{k}:{v}" for k, v in a["breakdown"].items()))

    h = d["holders"]
    if h.get("institutional_pct") is not None or h.get("top_institutions"):
        L.append("")
        L.append("-- OWNERSHIP " + "-" * 64)
        L.append(f"Institutional: {h.get('institutional_pct')} | insider: {h.get('insider_pct')}")
        for inst in h.get("top_institutions", [])[:5]:
            L.append(f"  {inst['holder']}: {inst['shares']} shares")

    if d.get("news"):
        L.append("")
        L.append("-- LATEST NEWS " + "-" * 62)
        for n in d["news"]:
            L.append(f"  * {n['title']}  ({n.get('publisher') or '?'}, {n.get('published') or ''})")

    L.append("")
    L.append(f"Data quality: {d.get('data_quality')}")
    return "\n".join(L)


def _kv(pairs) -> str:
    parts = []
    for k, v in pairs:
        if v is None:
            continue
        parts.append(f"{k}: {v}")
    return "  |  ".join(parts) if parts else "(no data)"


def save_json(obj: dict, path: str) -> str:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=2, default=str)
    return path
