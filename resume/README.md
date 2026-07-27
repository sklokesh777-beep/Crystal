# S K Lokesh — Resume (JPMorganChase 2027 CIB Research & Analytics, Securities Services)

Target: **2027 Commercial & Investment Bank Research & Analytics, Securities Services — Full-Time
Senior Team Member, India (Bengaluru)** · Job ID 210772851 · Alternative Fund Services.

## Files

| File | Use |
|---|---|
| `S-K-Lokesh-Resume.pdf` | **Upload this** to the JPMorganChase application (Oracle Recruiting Cloud) |
| `S-K-Lokesh-Resume.docx` | Editable Word master — identical text, Times New Roman, one page |
| `S-K-Lokesh-Resume.txt` | Plain text for pasting into web forms and for ATS keyword checks |
| `S-K-Lokesh-Cover-Letter.pdf` | Attach alongside the resume where the form allows it |
| `S-K-Lokesh-Cover-Letter.docx` / `.txt` | Editable Word master and plain text (for pasting into a form or email body) |
| `preview.png` / `cover_preview.png` | Page images |
| `resume_content.py` / `build_resume.py` | Resume content source + generator (`python3 build_resume.py`) |
| `cover_letter_content.py` / `build_cover_letter.py` | Cover letter content + generator (`python3 build_cover_letter.py`) |

Both documents share one typographic system (Liberation Serif / Times New Roman, same header block and
rule), so they read as a matched set rather than two unrelated files.

## Cover letter

One page, 494 words, four substantive paragraphs. Structure: why this team; the 360 ONE fund-servicing
evidence; the platform audit as the proof of a control mindset; AI-tool habit and NISM Series-VII; close.

- Quotes the role title and **Job ID 210772851** exactly as posted, since it is read next to an Oracle
  Recruiting Cloud application record.
- Addressed to the campus recruiting team — no invented recipient name, which is correct for a
  programme reviewed on a rolling basis.
- States "simulated paper portfolio" explicitly and carries **no realised P&L or win-rate claim**, for
  the same reasons as the resume.
- Verified one page in both PDF and Word rendering; PDF and DOCX text identical (1.0000).

## Verified build checks

- One page in **both** the PDF and the Word rendering (Word/LibreOffice pagination tested, not assumed).
- PDF and DOCX extract to **identical text** (similarity 1.0000); bullets extract as real `•`, not
  control characters, so nothing garbles in the parser.
- Single column, standard section headings, no images, no text boxes, no tables carrying content —
  JPMorganChase applications are parsed by Oracle Recruiting Cloud before a human reads them.
- All 25 checked job-description terms appear in the text (fund accounting, portfolio accounting,
  NAV, financial reporting, investor reporting, reconciliations, control, compliance, analytics, AI,
  Python, Excel, Bloomberg, quantitative, attention to detail, collaboration, curiosity, risk, …).
- Every number is traceable to a source: the two prior resumes, or measurements taken directly from
  `trading_suite_v9.zip` in this repository.

## The trading project: what went on the page, and what deliberately did not

Four bullets, ordered by what a Research & Analytics screener actually values:

1. **Engineering** — modular platform, validated/cached ingestion, 12 indicators, backtest engine,
   ATR stops, 1%-risk sizing, Sharpe/Sortino/profit factor/expectancy/R-multiples, automated
   Markdown/PDF/Excel reporting.
2. **Validation** — 7 long/short strategies, 16.5 years (2010–2026), 504- and 1,001-symbol universes,
   8,600+ simulated trades, signals at close filled at next open (no look-ahead), costs on every
   fill, walk-forward 3y/1y, Monte-Carlo over 250 ten-day windows.
3. **Findings, negative results included** — confluence scoring flat at 60–62% across buckets;
   universe 504→1,001 cut CAGR 5.3%→1.2%; regime filter cut max drawdown −34.5%→−28.8%; edge gone at
   2–3× costs; survivorship-bias and regime caveats stated.
4. **Risk-control audit & remediation** — reward:risk found inverted at ~0.1:1 against the suite's own
   2.0 minimum; stops tightened 3×→2× ATR; fixed-fractional 1% sizing with a 10% position cap and
   explicit 1.5R targets; data-validation layer rejecting corrupt prices (>60% one-day jumps,
   High < Low); silent exception handling that had disabled the earnings filter repaired; 7 defects
   closed, including 3 mis-set stops that left ~USD 107k of notional unprotected.

Live operation sits in the entry descriptor: run daily against a **USD 1,000,000 simulated paper
portfolio**, 14 closed trades over 6 sessions, ~1% risk each, zero stop-outs — followed on the page
by *"a favourable-regime sample, not presented as a repeatable edge."*

### What was deliberately left off

| Left off | Why |
|---|---|
| `+$8,119.90` realised, `100% win rate`, `+0.81%` on the account | Real broker-reconciled numbers, but from a **simulated** TradingView account over **6 sessions** with ~1% targets in a RISK-ON regime. A 14/14 record invites the reader to discount the whole section, and your own report says it is not repeatable. The sample size, risk-per-trade and zero stop-outs are stated instead — those are the defensible facts. |
| Crystal Trader v10 (PR #1, 14 files) | You chose to stay on v9.1; claiming a superseded parallel build adds words without adding signal. |
| Excel journal dashboard, environment fixes (`tabulate`, `lxml`) | Real work, but too granular for one page. Good interview material. |
| India ₹50k NSE model | Scoped, not built. Nothing unbuilt goes on a resume. |
| The 60-trade assignment target (14 of 60 closed) | A resume states what was done, not a quota. Be ready to explain the quality-over-quota choice if asked — it is a good answer. |

Earlier drafts of this resume cited a synthetic demo dataset as the source of `output/report.md`. That
is still true of `data/sample_trades.csv`, but your real record is the 14 broker-reconciled closed
trades, and the page now reflects that instead.

## Confirm or correct these before you submit

1. **B.Com CGPA / percentage is still missing.** Indian screeners expect marks for degree, Class XII
   and Class X. Send it and it goes on the education line.
2. **Which NISM module, and when?** The resume currently says *NISM Series-VII: Securities Operations
   & Risk Management — in preparation*, chosen because Series-VII covers clearing, settlement and
   operational risk, which maps directly onto Securities Services work. If you intended a different
   module (Series-XV Research Analyst, Series-VIII Equity Derivatives, Series-V-A Mutual Funds), say
   so. Also send the target exam month so the line can read "exam scheduled <month> 2026" — a booked
   date reads far stronger than "in preparation".
3. **Do you want the P&L on the page at all?** My recommendation is no, for the reasons above. If you
   disagree, the honest version is: "+USD 8.1k realised on a USD 1M simulated account over 6 sessions
   (14/14 closed, favourable regime, small sample)" — say the word and I will add exactly that.
4. **Native language conflict.** Older resume said Kannada (native); newer says Tamil (native),
   Kannada and Hindi (conversational). The newer version is used.
5. **University name.** Official current name is **Bengaluru City University** (per SJCC's own
   publications), used here in place of "Bangalore City/Central University".
6. **Class XII stream.** Older resume: "Science / Commerce"; newer: "Commerce". Commerce is used.
7. **NSS Treasurer tenure.** No dates in either resume, so that line shows location instead of a date
   range. Send the term (e.g. "2025 – Present").
8. **360 ONE scale figure.** "INR 6 lakh crore+ client assets" is stated conservatively against press
   reporting of assets above INR 6.6 lakh crore. Say the word and it comes off.
9. **Equity investing tenure** carried over as "2+ years" — update if longer.
10. The older `.docx` resume you uploaded could not be decoded. If it holds anything the two PDF
    resumes don't (awards, competitions, scholarships, other roles), send it.

## Interview preparation notes

- **Own the paper-trading distinction before you're asked.** "The P&L in my tooling is a simulated
  paper account and a synthetic demo dataset; what's real is the engine, the validation design, and
  the findings" is a strong, senior answer. Getting caught the other way round is fatal.
- **Lead with the negative results.** That you tested whether stacking indicators improved win rate,
  found it didn't, and published that finding is exactly the instinct a Research & Analytics team
  screens for. Same for the 1,000-name universe test and the transaction-cost stress test.
- **Be ready on the fund-services side.** The posting names NAV production, capital calls,
  distributions, transfer agency and expense accruals. Your evidence today is adjacent (rolling
  returns from NAV histories, cost-basis reconciliation, PMS/AIF fee modelling), so read up on the
  mechanics before an interview.
