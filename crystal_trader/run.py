#!/usr/bin/env python3
"""
Crystal Trader - command line entry point.

Examples
--------
    # Scan the default universe for today's swing setups
    python run.py scan

    # Scan a custom list, save CSV + markdown
    python run.py scan --tickers AAPL,MSFT,NVDA,JPM --save

    # Full research dossier for one stock
    python run.py profile NVDA

    # Exact trade plan (stop-loss + best take-profit) for a manual idea
    python run.py plan AAPL --entry 326.60

    # Check whether an open position should be exited
    python run.py exit NVDA --entry-date 2026-07-15

    # Market regime (risk-on / risk-off)
    python run.py regime
"""
from __future__ import annotations

import argparse
import logging
import os
import sys

# Make top-level modules (config) and the package importable regardless of CWD.
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import config
from crystal import data as datamod
from crystal import indicators as ind
from crystal import signals as sig
from crystal import risk as riskmod
from crystal import screener
from crystal import profile as profmod
from crystal import report


def _setup_logging(verbose: bool):
    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def cmd_scan(args):
    tickers = None
    if args.tickers:
        tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    result = screener.scan(
        tickers=tickers,
        check_regime=not args.ignore_regime,
        check_earnings=not args.ignore_earnings,
        diversify=not args.no_diversify,
    )
    print(report.scan_console(result))
    if args.save:
        paths = report.scan_save(result)
        print(f"\nSaved: {paths}")


def cmd_profile(args):
    dossier = profmod.build_profile(args.ticker, with_news=not args.no_news)
    print(report.profile_console(dossier))
    if args.json:
        path = os.path.join(config.OUTPUT_DIR, f"{args.ticker.upper()}_profile.json")
        report.save_json(dossier, path)
        print(f"\nSaved JSON: {path}")


def cmd_plan(args):
    ticker = args.ticker.upper()
    df = datamod.get_history(ticker)
    if df is None:
        print(f"Could not load trustworthy data for {ticker}.")
        return
    enriched = ind.enrich(df)
    atr = float(enriched["atr"].iloc[-1])
    entry = args.entry if args.entry else float(enriched["Close"].iloc[-1])
    plan = riskmod.build_plan(ticker, entry=entry, atr=atr,
                              stop_override=args.stop)
    if plan is None:
        print("Could not build a plan (risk distance is zero/invalid).")
        return
    d = plan.as_dict()
    print("=" * 60)
    print(f"TRADE PLAN - {ticker}   (capital ${config.CAPITAL:,.0f}, "
          f"risk {config.RISK_PER_TRADE*100:.1f}%)")
    print("=" * 60)
    print(f"  Entry (ref)      : {d['entry']}")
    print(f"  STOP-LOSS        : {d['stop_loss']}   ({d['stop_pct']}% away)")
    print(f"  Risk / share     : {d['risk_per_share']}")
    print(f"  Shares           : {d['shares']}")
    print(f"  Notional         : ${d['notional']:,.2f}  ({d['capital_pct']}% of capital)")
    print(f"  Dollar risk      : ${d['dollar_risk']:,.2f}")
    print(f"  Take-profit ladder:")
    for r in config.TARGET_R_MULTIPLES:
        key = f"tp_{r:g}R"
        star = "  <== BEST" if abs(r - config.PREFERRED_TARGET_R) < 1e-9 else ""
        print(f"      {r:g}R : {d.get(key)}{star}")
    print(f"  BEST TAKE-PROFIT : {d['best_take_profit']}  "
          f"(reward:risk {d['reward_risk']}:1)")
    if d["warnings"]:
        print(f"  WARNINGS         : {d['warnings']}")


def cmd_exit(args):
    ticker = args.ticker.upper()
    df = datamod.get_history(ticker)
    if df is None:
        print(f"Could not load data for {ticker}.")
        return
    enriched = ind.enrich(df)
    decision = sig.exit_signal(enriched, args.entry_date)
    print(f"{ticker}: {'EXIT' if decision['exit'] else 'HOLD'} - {decision['reason']} "
          f"(held ~{decision.get('held_days')} days)")


def cmd_regime(args):
    r = sig.market_regime()
    print(f"Market regime: {r.get('regime').upper()} - {r.get('detail')}")
    print(f"  {r.get('index')} price {r.get('price')} vs {config.REGIME_SMA}-SMA {r.get('sma')}")
    print(f"  Risk-on: {r.get('risk_on')}")


def build_parser():
    p = argparse.ArgumentParser(prog="crystal", description="Crystal Trader swing model")
    p.add_argument("-v", "--verbose", action="store_true", help="verbose logging")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("scan", help="scan universe for swing setups")
    s.add_argument("--tickers", help="comma-separated tickers (override universe)")
    s.add_argument("--save", action="store_true", help="save CSV + markdown")
    s.add_argument("--ignore-regime", action="store_true")
    s.add_argument("--ignore-earnings", action="store_true")
    s.add_argument("--no-diversify", action="store_true")
    s.set_defaults(func=cmd_scan)

    pr = sub.add_parser("profile", help="deep research dossier for one stock")
    pr.add_argument("ticker")
    pr.add_argument("--json", action="store_true", help="also save JSON")
    pr.add_argument("--no-news", action="store_true")
    pr.set_defaults(func=cmd_profile)

    pl = sub.add_parser("plan", help="exact stop-loss + best take-profit plan")
    pl.add_argument("ticker")
    pl.add_argument("--entry", type=float, help="entry price (default: last close)")
    pl.add_argument("--stop", type=float, help="manual stop override")
    pl.set_defaults(func=cmd_plan)

    ex = sub.add_parser("exit", help="should an open position be closed?")
    ex.add_argument("ticker")
    ex.add_argument("--entry-date", required=True, help="YYYY-MM-DD")
    ex.set_defaults(func=cmd_exit)

    rg = sub.add_parser("regime", help="market risk-on/off state")
    rg.set_defaults(func=cmd_regime)
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    _setup_logging(getattr(args, "verbose", False))
    args.func(args)


if __name__ == "__main__":
    main()
