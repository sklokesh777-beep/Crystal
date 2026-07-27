"""
Single source of truth for S K Lokesh's resume content.

Every line below is traceable to one of the candidate's source resumes, to the
trading-suite codebase in this repository (`trading_suite_v9.zip`), or to a
publicly verifiable fact about an institution named here:

  * SJCC affiliation / NAAC grade -> sjcc.edu.in official syllabus & brochure PDFs
    ("An Autonomous Institution affiliated to Bengaluru City University",
     "Accredited with A++ Grade by NAAC in 4th Cycle (CGPA of 3.75/4)")
  * 360 ONE listing status         -> listed on NSE & BSE since 19 Sep 2019
  * 360 ONE scale                  -> reported assets above INR 6.6 lakh crore (Aug 2025 press),
                                      stated conservatively as "INR 6 lakh crore+"
  * Trading platform figures       -> measured from the repository itself:
      ~6,528 lines of Python across 72 files; universes of 504 and 1,001 symbols;
      backtest window 2010-01-05 to 2026-07-15 (16.5y); 8,665 RSI-2 trades;
      confluence-score win rates flat at 59.5-62.2% across score buckets;
      500-name CAGR +5.32% vs 1,000-name +1.16%; graduated regime filter
      max drawdown -34.5% -> -28.8%; cost stress 2x -> +1.2% CAGR, 3x -> -2.9%;
      Monte Carlo over 250 ten-day windows; walk-forward 3y train / 1y test.

  NOTE ON P&L: no profit or return figure from the paper-trading tool appears on
  this resume. `data/my_trades.csv` is empty and the +10.09% report in
  `output/report.md` was generated from `data/sample_trades.csv`, a synthetic
  60-trade demo whose exits are back-solved from intended R-multiples, on a
  $100,000 SIMULATED TradingView account. Presenting that as realised profit
  would be indefensible in interview. The resume claims engineering, validation
  methodology and research findings only - all of which are real and checkable.

Target role: JPMorganChase - 2027 Commercial & Investment Bank, Research &
Analytics, Securities Services (Alternative Fund Services) - Full-Time Senior
Team Member, Bengaluru (Job ID 210772851).

Currency is written as "INR" rather than the rupee glyph so that every ATS
parser and every PDF font renders it identically.
"""

NAME = "S K LOKESH"

CONTACT = [
    ("Bengaluru, Karnataka, India", None),
    ("+91 99865 78113", "tel:+919986578113"),
    ("sklokesh777@gmail.com", "mailto:sklokesh777@gmail.com"),
    ("linkedin.com/in/s-k-lokesh-a09160313",
     "https://www.linkedin.com/in/s-k-lokesh-a09160313"),
]

PROFILE = (
    "Final-year B.Com student (Class of 2027) and CFA Level I candidate applying to Commercial &amp; Investment Bank "
    "Research &amp; Analytics \u2013 Securities Services (Alternative Fund Services), Bengaluru, with the aim of building a career "
    "in fund accounting, portfolio accounting, NAV production, financial reporting and investor reporting. Delivered "
    "portfolio analytics at India's largest listed wealth manager \u2013 rolling returns for 120+ funds automated in Python "
    "(~90% less manual effort) and PMS/AIF fee modelling worth INR 4.2 lakh a year to a client \u2013 and independently built a "
    "6,500-line Python backtesting platform validated across 16.5 years of market data."
)

SECTIONS = [
    # ------------------------------------------------------------------ EDUCATION
    {
        "heading": "EDUCATION",
        "blocks": [
            {
                "type": "entry",
                "left": "<b>Bachelor of Commerce (B.Com)</b>  |  St. Joseph's College of Commerce (Autonomous), Bengaluru",
                "right": "<b>2024 \u2013 2027</b>",
                "sub": "Affiliated to Bengaluru City University  &#183;  NAAC A++ accredited  &#183;  Final year, expected graduation 2027",
                "lines": [
                    "<b>Relevant coursework:</b> Financial Accounting, Corporate Finance, Investment Management, Business Statistics, "
                    "Taxation, Economics",
                ],
            },
            {
                "type": "entry",
                "left": "<b>Class XII \u2013 Pre-University (Commerce)</b>  |  Seshadripuram Independent PU College  "
                        "&#183;  Karnataka State Board",
                "right": "<b>93%  &#183;  2024</b>",
            },
            {
                "type": "entry",
                "left": "<b>Class X \u2013 Secondary School Certificate (SSLC)</b>  |  St. Anthony's Boys' High School  "
                        "&#183;  Karnataka State Board",
                "right": "<b>80%  &#183;  2022</b>",
            },
        ],
    },
    # --------------------------------------------------------------- EXPERIENCE
    {
        "heading": "PROFESSIONAL EXPERIENCE",
        "blocks": [
            {
                "type": "entry",
                "left": "<b>360 ONE Portfolio Managers Limited</b>  |  Finance Intern \u2013 Wealth Management",
                "right": "<b>May \u2013 Jun 2026</b>",
                "sub": "India's largest listed wealth manager (NSE/BSE listed; INR 6 lakh crore+ client assets)  &#183;  Bengaluru, India",
                "bullets": [
                    "<b>Portfolio analytics &amp; automation:</b> Engineered a Python framework (pandas, openpyxl) that computed "
                    "6M/1Y/3Y/5Y rolling returns from NAV histories for 120+ mutual funds across Large, Mid, Small and Flexi Cap "
                    "categories, cutting manual data processing time by ~90%.",

                    "<b>Reconciliation &amp; cost basis:</b> Reconstructed 5+ years of transaction history from Script Cashflow reports to "
                    "reconcile cost basis and compute LTCG/STCG liability on 6 equity instruments in an HNI family portfolio at "
                    "post-Budget 2024 rates.",

                    "<b>Fee &amp; expense modelling:</b> Modelled PMS/AIF fee structures across 9 holdings (1.94% weighted-average "
                    "fixed fee) and quantified an INR 4.2 lakh annual saving by moving a 10-fund mutual fund portfolio from regular "
                    "to direct plans.",

                    "<b>Reference data &amp; Bloomberg:</b> Maintained a 4,000+ security BSE/NSE dataset with Bloomberg BDH/BDP formulas and "
                    "mapped client holdings against model portfolios to generate Buy/Sell/Hold calls for Investment Counsellors.",

                    "<b>Client reporting:</b> Co-authored a 30+ slide institutional deck on active vs. passive fund performance (rolling "
                    "alpha, hit rates, alpha dispersion by market-cap segment) used by advisory teams with clients.",
                ],
            },
            {
                "type": "entry",
                "left": "<b>Guanella Preethi Nivas (Preethi Nivas Trust)</b>  |  Social Intern",
                "right": "<b>May 2025 (60 hours)</b>",
                "sub": "Charitable home for 50+ destitute elderly residents, run by The Guanellian Society  &#183;  Bengaluru, India",
                "bullets": [
                    "Rebuilt resident records, activity logs and medical-room inventory, and ran safety audits (extinguisher expiry, hazard "
                    "documentation, signage) to support compliance, preparing the reporting decks used by staff.",
                ],
            },
        ],
    },
    # ------------------------------------------------------- QUANTITATIVE PROJECT
    {
        "heading": "QUANTITATIVE RESEARCH PROJECT",
        "blocks": [
            {
                "type": "entry",
                "left": "<b>Equity Backtesting &amp; Screening Platform</b>  |  Independent Python project, AI-assisted build",
                "right": "<b>2026</b>",
                "sub": "6,500-line research stack, 10 build iterations; run daily to screen a 500-name US universe for a USD 100,000 "
                       "simulated paper-trading portfolio  &#183;  also a 2+ year retail investor in Indian equities",
                "bullets": [
                    "<b>Engineering:</b> Built a modular platform (pandas, NumPy, yfinance, Matplotlib) spanning data ingestion, 12 technical "
                    "indicators, a backtest engine, ATR stops, 1%-risk sizing, performance analytics (Sharpe, Sortino, profit factor, "
                    "expectancy, R-multiples) and automated reporting.",

                    "<b>Validation methodology:</b> Tested 7 long and short strategies over 16.5 years (2010\u20132026) across 504- and "
                    "1,001-symbol universes and 8,600+ simulated trades: signals read at the close and filled at the next open to "
                    "remove look-ahead, commission and slippage on every fill, walk-forward 3y-train/1y-test windows, and Monte-Carlo "
                    "sampling of 250 ten-day windows.",

                    "<b>Findings, negative results included:</b> Showed a multi-indicator confluence score did not lift win rate "
                    "(flat 60\u201362% across score buckets) and that widening the universe from 504 to 1,001 names cut CAGR 5.3% to "
                    "1.2%; a graduated regime filter cut max drawdown \u221234.5% to \u221228.8%, and the edge disappeared at 2\u20133x assumed costs \u2013 "
                    "reported with survivorship-bias and regime caveats rather than optimised results.",
                ],
            },
        ],
    },
    # --------------------------------------------------------------- LEADERSHIP
    {
        "heading": "LEADERSHIP & EXTRACURRICULAR",
        "blocks": [
            {
                "type": "entry",
                "left": "<b>National Service Scheme (NSS), St. Joseph's College of Commerce</b>  |  Treasurer (elected)",
                "right": "<b>Bengaluru, India</b>",
                "bullets": [
                    "Elected treasurer of a 100+ member unit; own the annual budget, fund allocation and expense records. Completed "
                    "2 rural exposure camps (8 days each) running community development surveys and field projects.",
                ],
            },
        ],
    },
    # ----------------------------------------------- CERTIFICATIONS AND SKILLS
    {
        "heading": "CERTIFICATIONS & TECHNICAL SKILLS",
        "blocks": [
            {
                "type": "kvlines",
                "lines": [
                    ("Certifications",
                     "CFA Level I candidate \u2013 Feb 2027 window (CFA Institute)  &#183;  NISM Series-VII: Securities Operations &amp; "
                     "Risk Management \u2013 in preparation  &#183;  Excel Skills for Business \u2013 Macquarie University (Coursera)  &#183;  "
                     "Soft Skills Development \u2013 NPTEL / SWAYAM (IIT)"),
                    ("Fund &amp; Portfolio Analytics",
                     "Rolling returns from NAV histories, portfolio mapping vs. model portfolios, performance analysis (alpha, hit "
                     "rate, dispersion), fee &amp; expense modelling (PMS/AIF), reconciliations, cost basis, capital gains tax, "
                     "financial statement analysis"),
                    ("Technical",
                     "Python (pandas, NumPy, openpyxl, Matplotlib), Advanced Excel (PivotTables, VLOOKUP, macros), Power BI, "
                     "PowerPoint, Bloomberg Terminal (BDH/BDP), Screener.in, Chartink, TradingView"),
                    ("AI-Enabled Workflow",
                     "ChatGPT and Claude for code generation and review, research synthesis, data clean-up and document drafting"),
                    ("Strengths",
                     "Attention to detail and data accuracy  &#183;  quality review and control discipline  &#183;  clear "
                     "communication  &#183;  collaboration  &#183;  intellectual curiosity"),
                    ("Languages",
                     "English (professional)  &#183;  Tamil (native)  &#183;  Kannada and Hindi (conversational)  &#183;  interests: "
                     "fine arts, home gardening"),
                ],
            },
        ],
    },
]
