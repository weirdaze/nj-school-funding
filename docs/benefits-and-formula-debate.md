# Benefits squeeze and the school funding formula debate

_Notes as of 2026-10-24. Figures come from `analysis/benefits_trend.py` unless a source is cited._

## The claim
"Employee benefit costs are rising sharply, so districts are cutting staff and increasing class sizes."

## What the district budget data shows (User-Friendly Budgets, all ~577 districts)

Statewide general current expense budgets, comparing each year's budget to the prior year's budget:

| Budget year | Benefits | Everything else | Benefits' share of the year's growth |
|---|---|---|---|
| 2022-23 | $4.42B (+2.8%) | $20.51B (+4.6%) | 12% |
| 2023-24 | $4.77B (+7.9%) | $21.43B (+4.5%) | 27% |
| 2024-25 | $5.07B (+6.3%) | $22.69B (+5.9%) | 19% |
| 2025-26 | $5.50B (+8.5%) | $23.63B (+4.1%) | 31% |
| **2026-27** | **$6.40B (+16.3%)** | **$23.82B (+0.8%)** | **83%** |

- In 2026-27, benefits took **83 cents of every new operating dollar**. Everything else, including salaries, instruction, special ed, transportation, and buildings, grew 0.8%, which is a real-dollar cut after inflation.
- The median district budgeted **+17.8%** for benefits. Benefits now make up a median **20.9%** of the operating budget, and 26%+ for the top tenth of districts.
- **Cherry Hill:** benefits rose from $54.5M to $61.4M (+$6.9M) while the operating budget rose only $6.2M, so spending on everything else went *down*. Benefits are 24.3% of its budget.
- **It is likely to get worse.** On 2026-09-28 the SEHBP commission approved a **~34% premium increase for plan year 2027**, starting January 2027 ([Sun Papers](https://thesunpapers.com/2026/09/28/nj-school-health-plan-commission-approves-34-premium-hike-for-2027/)). The 2026-27 budgets were adopted in spring 2026, before that vote, so the second half of this school year and all of 2027-28 will feel it.

### Why premiums are rising ([Treasury, 2026-03-24](https://www.nj.gov/treasury/news/2026/03242026.shtml); [NJ Globe](https://newjerseyglobe.com/state-government/school-employees-face-34-health-premium-hike-as-state-delays-vote/))
- The SEHBP lost $126M in plan year 2024 and $207M in plan year 2025, $333M in total, which now has to be repaid.
- Active-member claims rose 12% for medical and 24% for prescriptions. GLP-1 drug spending per member is up about 95%.
- Healthier districts are leaving for private plans, which leaves a sicker and costlier pool. Treasury calls this a "death spiral" risk.
- Chapter 44 (2020) locks benefit design until January 2028. It also moved costs toward employers, meaning districts and taxpayers.

## Where the money goes: what we can and can't see

| Question | Granularity we have | Source in repo |
|---|---|---|
| Total benefits per district, per year | ✅ district × year, 2018-19 → 2026-27 | UFB `approp*.csv` line 71260 |
| Spending by function (regular ed, special ed, tuition, transport, plant, admin) | ✅ district × year | UFB `approp*.csv` |
| Per-pupil costs vs. peer districts | ✅ district × year, about 21 indicators | TGES `CSG*.CSV` |
| Admin salaries and benefits (superintendent, business administrator, and non-union staff over $75k) | ✅ per person | UFB `employees*.csv` |
| Revenue mix (levy, state aid, federal) | ✅ district × year | UFB `rev*.csv` |
| **Benefits split into health, pension (PERS), FICA, and other** | ❌ UFB only gives the total | District **ACFRs** (audits): budgetary comparison schedule C-1 |
| **Teacher pension and retiree health paid by the state "on behalf"** | ⚠️ statewide only | ACFRs list it per district; Report Card has the state total |
| **Which districts are in SEHBP vs. private plans** | ❌ | Treasury/SEHBP participation lists (TBD) |
| **Staff counts, layoffs, class size over time** | ⚠️ 2024-25 only | SPR database files for earlier years (to download) |
| Teacher salary guides | ❌ | District contracts (PERC) |

**Bottom line:** we can already show *that* benefits are eating the growth, and *which* districts are hit hardest. To show *which kind* of benefit is driving it (health vs. pension vs. FICA) and *how it shows up* in staffing and class size, we need two additions: (1) district ACFRs, starting with Camden County, and (2) SPR staffing and class-size data for several years.

## The formula debate

### How the formula connects to benefits
SFRA's adequacy budget is a per-pupil base cost, set every three years by the Educational Adequacy Report, plus weights for at-risk, LEP, and special ed students. Between reports it is inflated by CPI, which was **3.6% for FY27**. Benefits are buried inside that base cost. When benefits grow 16% and the formula grows about 3.6%, districts have to cover the gap with the local levy, but the levy is capped at **2%**. Something else gets cut.

### What changed for FY27 (budget language; [ELC](https://edlawcenter.org/breaking-down-school-funding-in-governor-sherrills-proposed-fy27-budget/))
- Aid increases are capped at **+6%** and cuts at **−3%** per year.
- Local Fair Share now uses **3-year averages** of property value and income instead of a single year.
- Special ed aid is based on each district's **projected classified enrollment**.
- K-12 formula aid is $12.43B, up $372M (+3.1%). 400 districts gain and 167 lose.
- These are one-year budget-language changes, not changes to the statute.

### What's next
The Sherrill administration has a steering committee, led by Commissioner Laux with the Hunt Institute, reviewing the formula this fall. The goals are "predictable, transparent, accountable." Changes require legislation, and Speaker Coughlin backs the review ([NJ Globe](https://newjerseyglobe.com/education/coughlin-backs-sherrill-administration-push-to-overhaul-school-funding/), [NJ Monitor](https://newjerseymonitor.com/2026/04/15/nj-school-funding-formula/)).

### The positions

| Who | Argues | Wants |
|---|---|---|
| **Education Law Center** (equity advocates) | The core structure is sound. The state's share of adequacy fell from **38% (2008-09) to 31% (2025-26)**, shifting cost onto property taxpayers. About half of districts don't raise their Local Fair Share. | Make the FY27 fixes permanent, eventually remove the caps and fully fund the formula, restore the state share, allow 2%-cap waivers for districts under their Local Fair Share, and add more extraordinary special ed aid |
| **Garden State Initiative** (fiscal conservatives; [report](https://www.gardenstateinitiative.org/research/garden-state-initiative-report-how-to-achieve-a-fairer-more-transparent-school-funding-formula-in-new-jersey/)) | "More spending alone is not the solution." NJ is #3 in per-pupil spending and #1 in property tax. Cost assumptions are opaque. 192 districts get $396M more than the formula says and 284 get $383M less. Local Fair Share expectations exceed the 2% cap and hit middle-income towns. | Audit the cost assumptions, slow formula cost growth, keep the 2% cap, align Local Fair Share with the cap, limit caps on aid changes, give 60 days' notice of aid |
| **"Fair Funding" district campaigns** (e.g. [Kingsway Regional](https://www.krsd.org/our-district/fair-funding-campaign/what-is-sfra)) | Growing or underfunded districts lost out for years to caps and hold-harmless aid. They want aid that follows students. | Run the formula as written (S2-style), predictable and transparent, and track it with a "Fair Funding Index" |
| **Districts losing aid** | Aid cuts on top of benefit spikes and a 2% levy cap force layoffs. | Tighter loss caps, stabilization aid, health-cost relief |
| **NJEA / unions** | The 34% premium increase means job and program cuts. They oppose shifting costs onto members. | State relief for SEHBP, PBM (pharmacy benefit manager) reform; the governor has pledged PBM reform |

### Questions for the report
1. In each district, how much of the 2026-27 aid change was cancelled out by the benefit increase?
2. Does the formula's CPI inflator undercount benefit growth? Compare benefit growth with the formula's inflation adjustment over time.
3. Do SEHBP districts look different from districts on private plans?
4. Districts below their Local Fair Share: is it because they won't tax or because they can't (2% cap)?
