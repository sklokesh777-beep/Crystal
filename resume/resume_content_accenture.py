"""
Accenture variant of S K Lokesh's resume.

Target: Accenture campus drive at St. Joseph's College of Commerce -
        **Analyst, Career Level 11** (CTC INR 6,65,500: fixed 5,50,000 + 21% variable)
        Eligibility: final-year undergraduate graduating 2027, no active backlogs
        Registration deadline 1 Aug 2026 16:00 IST; hiring date 17 Aug 2026
        Location not stated in the notification (to be clarified at the PPT)

Same content system and layout engine as the JPMorganChase version; only the
positioning changes. Every factual claim is identical to the verified JPMC
resume, so both documents stay consistent under background verification - which
the placement notification explicitly warns will happen.

Positioning rationale (the detailed JD had not decoded when this was written):
Accenture hires B.Com/BBA/B.Sc/BA finalists into Analyst (CL11) roles that are
predominantly Finance Operations and Financial Services delivery - Record to
Report, Order to Cash, Intercompany, and FS analytics. Accenture's own published
analyst postings describe reconciliations, month-end close support, reporting,
SLA and KPI delivery, transaction review, documentation, adherence to process
guidelines, and identifying areas of improvement. The bullets below are therefore
led with process automation, reconciliation, cost analysis, data management,
controls and defect remediation - all of which are things the candidate has
genuinely done, simply framed in the vocabulary of the work.

If the attached JD turns out to be a technology or consulting track, the ordering
should change: the analytics/automation platform moves above the internship.

EDITORIAL RULE (applied deliberately): nothing on this page restates the drive's
eligibility criteria as if it were a selling point. No "applying for the Analyst
role", no "no active backlogs", and the graduation year appears once, in the
education block where a reader structurally expects it. Eligibility is proved by
the registration form and the transcript, not by resume copy. The summary opens
on quantified outcomes and only then identifies the candidate.
"""

OUT_NAME = "S-K-Lokesh-Resume-Accenture"
PDF_SUBJECT = "Accenture - Analyst (Career Level 11) - Campus Drive 2026, Graduating 2027"
PDF_KEYWORDS = ("analyst, finance operations, reconciliations, financial reporting, month-end close, "
                "process improvement, automation, controls, documentation, data analytics, Python, "
                "advanced Excel, Power BI, AI-enabled tools, CFA Level I, NISM, stakeholder management")

NAME = "S K LOKESH"

CONTACT = [
    ("Bengaluru, Karnataka, India", None),
    ("+91 99865 78113", "tel:+919986578113"),
    ("sklokesh777@gmail.com", "mailto:sklokesh777@gmail.com"),
    ("linkedin.com/in/s-k-lokesh-a09160313",
     "https://www.linkedin.com/in/s-k-lokesh-a09160313"),
]

PROFILE = (
    "Automated a recurring returns pack covering 120+ funds in Python (~90% less manual effort), reconciled 5+ years of "
    "transaction history for cost-basis accuracy, and modelled fee structures that surfaced INR 4.2 lakh of annual "
    "savings for a client \u2013 delivered during a finance internship at India's largest listed wealth manager. "
    "Independently built, audited and remediated a 6,500-line Python analytics platform, closing seven defects "
    "including an inverted risk structure in its own logic. Final-year B.Com student at St. Joseph's College of "
    "Commerce, Bengaluru, with an automation-first instinct, a controls mindset around reporting accuracy, and daily "
    "hands-on use of AI-enabled tools."
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
                "sub": "Affiliated to Bengaluru City University  &#183;  NAAC A++ accredited  &#183;  Final year, graduating 2027",
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
                    "<b>Process automation:</b> Engineered a Python framework (pandas, openpyxl) that computed 6M/1Y/3Y/5Y rolling "
                    "returns from NAV histories for 120+ funds across four market-cap categories, cutting manual data processing time "
                    "by ~90% and standardising a recurring reporting deliverable.",

                    "<b>Reconciliation &amp; tax computation:</b> Reconstructed 5+ years of transaction history from Script Cashflow "
                    "reports to reconcile cost basis and compute LTCG/STCG liability on 6 equity instruments held by an HNI family "
                    "portfolio, applying post-Budget 2024 rates.",

                    "<b>Cost &amp; fee analysis:</b> Modelled PMS/AIF fee structures across 9 holdings (1.94% weighted-average fixed "
                    "fee) and quantified an INR 4.2 lakh annual saving by moving a 10-fund portfolio from regular to direct plans.",

                    "<b>Data management &amp; client reporting:</b> Maintained a 4,000+ security BSE/NSE dataset with Bloomberg BDH/BDP "
                    "formulas, mapping holdings against model portfolios to generate Buy/Sell/Hold calls; co-authored a 30+ slide "
                    "institutional deck on fund performance used by advisory teams with clients.",
                ],
            },
            {
                "type": "entry",
                "left": "<b>Guanella Preethi Nivas (Preethi Nivas Trust)</b>  |  Social Intern",
                "right": "<b>May 2025 (60 hours)</b>",
                "bullets": [
                    "Charitable home for 50+ destitute elderly residents (The Guanellian Society): rebuilt resident records, activity "
                    "logs and medical-room inventory, and ran facility safety audits to support compliance, preparing the reporting "
                    "decks used by staff.",
                ],
            },
        ],
    },
    # --------------------------------------------------------- PROJECT (analytics)
    {
        "heading": "ANALYTICS & AUTOMATION PROJECT",
        "blocks": [
            {
                "type": "entry",
                "left": "<b>Equity Analytics &amp; Automation Platform</b>  |  Independent Python build, AI-assisted",
                "right": "<b>2026</b>",
                "sub": "6,500-line stack across 10 build iterations  &#183;  run daily against a USD 1,000,000 simulated paper portfolio "
                       "(14 closed trades over 6 sessions, ~1% risk each \u2013 a favourable-regime sample, not a proven edge)",
                "bullets": [
                    "<b>Engineering &amp; automation:</b> Built a modular platform (pandas, NumPy, yfinance, Matplotlib) covering "
                    "validated and cached data ingestion, 12 indicators, a backtest engine, risk-based position sizing, performance "
                    "analytics and automated Markdown, PDF and Excel reporting.",

                    "<b>Controls &amp; defect remediation:</b> Audited the system against its own risk policy and found reward:risk "
                    "inverted at ~0.1:1 versus a 2.0 minimum; corrected the stop and target geometry, enforced 1%-risk sizing with a "
                    "position cap, added a validation layer rejecting corrupt input data (>60% one-day jumps, High &lt; Low) and repaired "
                    "silent exception handling that had disabled a key filter \u2013 closing 7 defects, 3 of which left ~USD 107k of "
                    "notional unprotected.",

                    "<b>Validation &amp; findings:</b> Tested 7 strategies over 16.5 years (2010\u20132026) across 504- and 1,001-symbol "
                    "universes and 8,600+ simulated trades with no look-ahead, walk-forward windows and Monte-Carlo sampling; reported "
                    "that a multi-indicator confluence score did not lift win rate (flat 60\u201362%) and that a wider universe cut CAGR "
                    "5.3%\u21921.2%, with survivorship-bias caveats rather than optimised results.",
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
                    ("Automation &amp; Analytics",
                     "Python (pandas, NumPy, openpyxl, Matplotlib), Advanced Excel (PivotTables, VLOOKUP, macros), Power BI, data "
                     "validation and quality checks, reporting automation, process documentation"),
                    ("Finance &amp; Operations",
                     "Reconciliations, cost-basis analysis, fee and expense modelling, capital gains tax (LTCG/STCG), financial "
                     "statement analysis, NAV-based performance reporting, Bloomberg Terminal (BDH/BDP)"),
                    ("AI-Enabled Workflow",
                     "ChatGPT and Claude for code generation and review, research synthesis and document drafting  &#183;  "
                     "<b>Strengths:</b> attention to detail, deadline delivery, quality review, stakeholder communication, teamwork"),
                    ("Languages",
                     "English (professional)  &#183;  Tamil (native)  &#183;  Kannada and Hindi (conversational)  &#183;  open to "
                     "Accenture locations across India"),
                ],
            },
        ],
    },
]
