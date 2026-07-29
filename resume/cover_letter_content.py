"""
Cover letter content for S K Lokesh -> JPMorganChase 2027 CIB Research &
Analytics, Securities Services (Alternative Fund Services), Bengaluru.

Same accuracy rules as the resume: every factual claim here is traceable to the
candidate's source resumes or to measurements of `trading_suite_v9.zip`.

Deliberate choices:
  * No realised P&L figure. The trading account is a SIMULATED TradingView paper
    portfolio and the 14/14 record spans 6 sessions in a favourable regime;
    the letter cites the audit and the fix instead, which is the stronger and
    fully defensible claim.
  * No invented recipient name. Addressed to the campus recruiting team, which
    is standard for a programme application reviewed on a rolling basis.
  * The role title and job ID are quoted exactly as posted, because the letter
    is read alongside an Oracle Recruiting Cloud application record.
"""

DATE = "27 July 2026"

RECIPIENT = [
    "Campus Recruiting Team",
    "Commercial &amp; Investment Bank \u2013 Research &amp; Analytics",
    "JPMorganChase, Bengaluru, India",
]

SUBJECT = ("Application \u2013 2027 Commercial &amp; Investment Bank Research &amp; Analytics, Securities Services, "
           "Full-Time Senior Team Member, India (Job ID 210772851)")

SALUTATION = "Dear Campus Recruiting Team,"

PARAGRAPHS = [
    "I am applying to the 2027 Research &amp; Analytics, Securities Services programme in Bengaluru. I am a final-year "
    "B.Com student at St. Joseph's College of Commerce, graduating in 2027, and a CFA Level I candidate for the "
    "February 2027 window. What draws me to Alternative Fund Services is that the work rewards the two things I have "
    "spent the last year practising: getting a number exactly right, and being able to prove how I got it.",

    "During a wealth management internship at 360 ONE Portfolio Managers, India's largest listed wealth manager, I "
    "automated 6M/1Y/3Y/5Y rolling-return computation from NAV histories for over 120 mutual funds in Python, cutting "
    "manual processing time by roughly 90%. I reconstructed more than five years of transaction history from Script "
    "Cashflow reports to reconcile cost basis and compute LTCG/STCG liability across six equity instruments in an HNI "
    "family portfolio, and modelled PMS/AIF fee structures across nine holdings to quantify an INR 4.2 lakh annual "
    "saving available to one client. Reconciliations, fee and expense accuracy, and reporting a client can rely on are "
    "why fund and portfolio accounting, NAV production and investor reporting are where I want to build a career.",

    "Alongside my coursework I built a 6,500-line Python trading-research platform, which I run daily against a "
    "simulated paper portfolio. Its most useful "
    "output was not a return; it was an audit. Testing the system against its own risk policy, I found the "
    "reward-to-risk geometry inverted at roughly 0.1:1 against a stated 2.0 minimum \u2013 wide stops paired with very "
    "small targets, a structure that looks successful right up until the first loss. I tightened the stops, enforced "
    "fixed-fractional 1% sizing with explicit 1.5R targets, added a validation layer that rejects corrupt price data, "
    "and repaired silent exception handling that had quietly disabled the earnings filter, closing seven defects in "
    "all. That platform also taught me to report findings I did not want: my multi-indicator confluence score did not "
    "improve the win rate at all, and widening the universe from 504 to 1,001 names cut annualised returns from 5.3% "
    "to 1.2%. I documented both rather than tuning them away.",

    "I built it with AI tools as a collaborator rather than a shortcut \u2013 generating code and then reviewing it \u2013 "
    "which is the habit your posting asks for. I am also preparing for NISM Series-VII, Securities Operations and Risk "
    "Management, because clearing, settlement and operational risk are the mechanics behind this role's deliverables.",

    "I would welcome the chance to discuss how I can contribute to the Alternative Fund Services team in Bengaluru. "
    "Thank you for your time and consideration.",
]

CLOSING = "Sincerely,"
SIGNOFF = "S K Lokesh"
ENCLOSURE = "Enclosure: Curriculum vitae"
