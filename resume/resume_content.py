"""
Single source of truth for S K Lokesh's resume content.

Every line below is traceable to one of the two source resumes supplied by the
candidate (the 2nd-year version and the final-year version) or to a publicly
verifiable fact about an institution named in them:

  * SJCC affiliation / NAAC grade -> sjcc.edu.in official syllabus & brochure PDFs
    ("An Autonomous Institution affiliated to Bengaluru City University",
     "Accredited with A++ Grade by NAAC in 4th Cycle (CGPA of 3.75/4)")
  * 360 ONE listing status         -> listed on NSE & BSE since 19 Sep 2019
  * 360 ONE scale                  -> reported assets above INR 6.6 lakh crore (Aug 2025 press)
                                      stated conservatively as "INR 6 lakh crore+"

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
    "Research &amp; Analytics \u2013 Securities Services (Alternative Fund Services) in Bengaluru, with the aim of building a "
    "career in fund accounting, portfolio accounting, NAV production, financial reporting and investor reporting. "
    "Delivered portfolio analytics at "
    "India's largest listed wealth manager: automated rolling-return computation across 120+ funds in Python (~90% less "
    "manual effort), reconstructed and reconciled 5+ years of transaction history for cost-basis accuracy, and modelled "
    "PMS/AIF fee structures that surfaced INR 4.2 lakh of annual client savings. Brings quantitative rigour, a "
    "controls-first approach to reporting accuracy, and daily hands-on use of AI-enabled research tools."
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
                "sub": "Affiliated to Bengaluru City University  &#183;  NAAC A++ accredited (4th cycle)  &#183;  Final year; expected graduation 2027",
                "lines": [
                    "<b>Relevant coursework:</b> Financial Accounting, Corporate Finance, Investment Management, "
                    "Business Statistics, Taxation, Economics",
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
                "sub": "India's largest listed wealth manager (NSE/BSE listed; INR 6 lakh crore+ client assets); PMS, AIF and "
                       "mutual fund solutions for HNI and family-office clients  &#183;  Bengaluru, India",
                "bullets": [
                    "<b>Portfolio analytics &amp; automation:</b> Engineered a Python framework (pandas, openpyxl) that computed "
                    "6M/1Y/3Y/5Y rolling returns from NAV histories for 120+ mutual funds across Large, Mid, Small and Flexi Cap "
                    "categories, cutting manual data processing time by ~90% and standardising output for advisory review.",

                    "<b>Reconciliation &amp; cost-basis analysis:</b> Reconstructed 5+ years of transaction history from Script "
                    "Cashflow reports to reconcile cost basis and compute LTCG/STCG liability on 6 equity instruments held by an "
                    "HNI family portfolio, applying post-Budget 2024 tax rates.",

                    "<b>Fee &amp; expense modelling:</b> Modelled PMS/AIF fee structures across 9 holdings (1.94% weighted-average "
                    "fixed fee) and quantified an INR 4.2 lakh annual saving by moving a 10-fund mutual fund portfolio from regular "
                    "to direct plans.",

                    "<b>Reference data &amp; Bloomberg:</b> Maintained a 4,000+ security BSE/NSE dataset using Bloomberg BDH/BDP "
                    "formulas and mapped client holdings against internal model portfolios to generate Buy/Sell/Hold "
                    "recommendations for Investment Counsellors.",

                    "<b>Client reporting &amp; presentation:</b> Co-authored a 30+ slide institutional deck on active vs. passive "
                    "fund performance – rolling alpha, hit rates and alpha dispersion by market-cap segment \u2013 used by advisory "
                    "teams in client discussions.",
                ],
            },
            {
                "type": "entry",
                "left": "<b>Guanella Preethi Nivas (Preethi Nivas Trust)</b>  |  Social Intern",
                "right": "<b>May 2025 (60 hours)</b>",
                "sub": "Charitable home for destitute elderly men run by The Guanellian Society; 50+ residents  &#183;  Bengaluru, India",
                "bullets": [
                    "<b>Records &amp; documentation:</b> Rebuilt resident records, daily activity logs and medical-room inventory for a "
                    "50+ resident facility – categorising and labelling pharmaceutical supplies – improving retrieval speed during "
                    "medication rounds and emergency response.",

                    "<b>Controls, compliance &amp; safety review:</b> Ran facility safety audits \u2013 fire-extinguisher expiry checks, hazard "
                    "documentation and disaster-awareness signage \u2013 to support safety compliance, and prepared the PowerPoint "
                    "decks and structured reports used by staff.",
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
                    "Elected treasurer of a 100+ member unit; own the annual budget, fund allocation and expense records across unit "
                    "programmes.",

                    "Completed 2 rural exposure camps (8 days each), running community development surveys and field projects "
                    "alongside volunteer teams.",
                ],
            },
            {
                "type": "entry",
                "left": "<b>Independent Equity Markets Research</b>  |  Self-directed",
                "right": "<b>Ongoing (2+ years)</b>",
                "bullets": [
                    "Active retail investor applying a multi-factor screening framework (valuation, momentum, quality) across Indian "
                    "equities using Screener.in, Chartink and TradingView; maintain a personal watchlist and trade log.",
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
                     "CFA Program \u2013 Level I candidate, February 2027 exam window (CFA Institute)  &#183;  Excel Skills for Business \u2013 "
                     "Macquarie University (Coursera)  &#183;  Soft Skills Development \u2013 NPTEL / SWAYAM (IIT)"),
                    ("Fund &amp; Portfolio Analytics",
                     "Rolling returns from NAV histories, portfolio mapping vs. model portfolios, active vs. passive performance "
                     "analysis (alpha, hit rate, dispersion), fee &amp; expense modelling (PMS/AIF), reconciliations, cost-basis "
                     "analysis, capital gains taxation (LTCG/STCG), financial statement analysis"),
                    ("Technical",
                     "Python (pandas, openpyxl), Advanced Excel (PivotTables, VLOOKUP, macros), Power BI, PowerPoint, Word"),
                    ("Platforms &amp; Data",
                     "Bloomberg Terminal (BDH/BDP), Screener.in, Chartink, TradingView"),
                    ("AI-Enabled Workflow",
                     "ChatGPT and Claude for research synthesis, data clean-up, document drafting and workflow automation"),
                ],
            },
        ],
    },
    # -------------------------------------------------------------- ADDITIONAL
    {
        "heading": "ADDITIONAL INFORMATION",
        "blocks": [
            {
                "type": "kvlines",
                "lines": [
                    ("Strengths",
                     "Attention to detail and data accuracy  &#183;  quality review discipline  &#183;  deadline delivery"),
                    ("Working style",
                     "Clear written and verbal communication  &#183;  collaboration across diverse teams  &#183;  initiative and "
                     "intellectual curiosity"),
                    ("Languages",
                     "English (professional)  &#183;  Tamil (native)  &#183;  Kannada (conversational)  &#183;  Hindi (conversational)"),
                    ("Additional",
                     "Expected graduation 2027  &#183;  open to full-time roles in Bengaluru  &#183;  interests: fine arts, home gardening"),
                ],
            },
        ],
    },
]
