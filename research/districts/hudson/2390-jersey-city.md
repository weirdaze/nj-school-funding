# Jersey City (Hudson County) — district 2390
_Researched 2026-10-24; revised after adversarial review 2026-10-24. In SEHBP: no (per Oct 2026 list). Sample: county median._

## Our numbers
_Auto-generated from `data/processed/district_panel.csv` by `analysis/district_profiles.py`; every figure links to its public source. Baseline is the 2025-26 **revised** budget; state aid is NJDOE K-12 formula aid (FY26 → FY27)._
- **Benefits budget** 2025-26 (revised) → 2026-27: $73.37M → $75.48M (+2.9%). Source: [2026-27 User-Friendly Budget](https://www.nj.gov/education/budget/ufb/2627/reports/17/UFB27_2390.pdf), Appropriations, line "Total Personal Services – Employee Benefits" (columns 2025-26 revised / 2026-27 budget); also [UFB data files](https://www.nj.gov/education/budget/ufb/2627/index.shtml) `approp27.csv` line 71260.
- **Formula aid change** FY26 → FY27: -$3.89M. Source: [NJDOE FY27 K-12 aid, district details](https://www.nj.gov/education/stateaid/2627/FY27_GBM_District_Details.xlsx) (row for district 2390, "FY26–FY27 K–12 Aid Difference"). Aid change minus benefit increase: -$5.99M (computed).
- **Benefits share of operating budget** 2026-27: 21.9% (computed from [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/17/UFB27_2390.pdf): employee benefits ÷ Total General Current Expense).
- **Health share of district-paid benefits** FY25: n/a; **audited health growth** FY23→FY25: n/a. Source: audited ACFR Exhibit C-1, "Health Benefits" actual, [FY2023 report](https://www.nj.gov/education/finance/fp/acfr/search/23/2390.pdf#page=98).
- **Tax levy change**: +17.0%; **budgeted fund balance used** 2025-26 → 2026-27: $148.85M → $98.25M. Source: [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/17/UFB27_2390.pdf), Revenues, lines "Total Tax Levy" and "Budgeted Fund Balance-Operating Budget".
- **Students per teacher (TGES ratio)** 2021-22 → 2024-25: 11.8 → 11.3. Source: [Taxpayers' Guide to Education Spending](https://www.nj.gov/education/guide/2025tges.shtml) Indicator 16, file `CSG16.CSV` column `STRAT` (2025 edition for 2024-25; [2023 edition](https://www.nj.gov/education/guide/) for 2021-22). This divides students by all teaching staff, so it is roughly half of typical class size and is **not a class-size measure**; the 2024-25 value is the latest edition's newer column, which later editions usually confirm but which is not yet final.
- **State-paid teacher pension/retiree medical** FY25 (not in the district budget): $108.76M. Source: [Treasury TPAF on-behalf allocations FY2025](https://www.nj.gov/education/fpp/audit/2425/docs/NJ_TPAF_Allocations_LEAs_FY2025.xlsx).
- **In SEHBP**: no per the [October 2026 participating-employer list](https://www.nj.gov/treasury/pensions/documents/pdf/sehbpemp.pdf) (name-matched).
- ⚠️ former Abbott district: may budget by school, so the general-fund benefits line can be partial

## What the district / local reporting says
- [primary] Preliminary 2026-27 general fund budget of $1,096,541,152 adopted Mar. 26, 2026; tax support of $625,304,688 = local tax levy $545,175,855 + **banked cap $80,128,833**; public hearing and final adoption scheduled Apr. 30, 2026. [Jersey City Public Schools, School Funding and District Budget page](https://www.jcboe.org/apps/pages/index.jsp?uREC_ID=1537228&type=d&pREC_ID=1667727), accessed Oct. 24, 2026. The $545.2M base equals the 2025-26 levy ($534,486,132) + 2.0%, so the whole increase above 2% comes from banked cap.
- [primary] UFB: total tax levy $534,486,132 (2025-26 revised) → $625,304,688 (2026-27), +17.0%; general fund state revenue $132,632,193 → $128,974,263; budgeted fund balance $148,847,199 → $98,245,713; employee benefits (11-XXX-XXX-2XX) $73,370,353 → $75,476,516; enrollment on roll 30,507 (Oct. 2025) → 31,784 est. (+4.2%) [NJDOE UFB 2026-27, Jersey City](https://www.nj.gov/education/budget/ufb/2627/reports/17/UFB27_2390.pdf), pp. 1, 2, 4 (generated July 14, 2026). The district's 9-page advertised budget notice (scanned; public hearing Apr. 30, 2026) shows the same enrollment table. [2026-2027 Advertised Budget](https://4.files.edl.io/53a9/04/27/26/185511-b416b739-e2b9-4e1a-b61f-613e7d7aa093.pdf), pp. 1-2.
- [primary] The budget page lists what the budget "specifically supports," starting with "Enrollment growth and student achievement" and "Competitive salaries and benefits for our staff"; it gives no staffing or health-plan figures. [JCPS budget page](https://www.jcboe.org/apps/pages/index.jsp?uREC_ID=1537228&type=d&pREC_ID=1667727).
- [news] Background (2025-26, not 2026-27): the preliminary 2025-26 budget of $1,027,273,122 had "health and employee benefits" of $168.9M, up 15% (this likely uses a broader definition than our UFB benefits line), about a 20% tax increase, and a state aid loss of ~$98M per Superintendent Norma Fernandez, who said "My goal is to keep the classrooms intact." [Hudson County View](https://hudsoncountyview.com/jersey-city-boe-approves-preliminary-1b-budget-with-20-percent-tax-increase/), Mar. 20, 2025.
- No public reporting found on 2026-27 layoffs, RIFs, position cuts, class sizes or program cuts; searches returned only 2018 and 2025 coverage. No public reporting found on the district's health plan, its 2026-27 health premium increase, or any health care cost cap adjustment.

## Verification of our numbers
- Benefits: our $73.37M (2025-26 revised) → $75.48M (2026-27) matches UFB p. 4 exactly, but that line is **partial**: Jersey City uses school-based budgeting (school-based appropriations $381.5M → $394.1M, UFB data file `schapp27.csv`), and benefits charged inside school budgets (about $365M → $378M per independent review; not re-verified) are not in it. A match on the undistributed line is therefore not a meaningful benefits comparison (recorded as unknown).
- Levy: our +17.0% matches UFB p. 2 ($534.49M → $625.30M) and the district's page (base + banked cap = $625.30M).
- State aid: our figure is NJDOE formula aid (-$3.89M); UFB total general fund state revenue falls -$3.66M ($132.63M → $128.97M, p. 2). No district statement of the aid change was found to compare against.
- Fund balance: our $148.85M → $98.25M matches UFB p. 2.
- **Data problem:** our `acfr_health_2025` = 66 (giving -100% growth and a 0% health share) is clearly a parsing error and should be fixed; FY23 = $58.30M looks plausible.

## Assessment
**Insufficient evidence.** Jersey City's undistributed benefits line rose only 2.9% (it excludes benefits inside school-based budgets), while the levy rose 17% using $80.1M of banked cap and fund balance use fell by ~$50.6M ($148.85M → $98.25M). That points to replacing a smaller planned fund-balance draw and a modest state revenue drop (-$3.66M total state revenue; formula aid -$3.89M) while funding projected enrollment growth (+4.2% on roll, which the district names first among what the budget supports), not to a benefit-driven squeeze. No reported 2026-27 layoffs, class-size increases or statements tying cuts to health costs were found.

## Confidence
**Medium**: the levy, banked cap and UFB figures come from district/NJDOE primary documents that reconcile with ours, but staffing and health-plan facts are missing, not disproven.

## Open questions
- Did the adopted (Apr. 30, 2026) budget include staffing reductions? Board minutes are on BoardDocs (go.boarddocs.com/nj/jcps), not checked.
- Which health plan does JCPS use (self-insured or a private carrier)? What was the 2026-27 premium change?
- Fix the ACFR FY2025 health value (66) in our panel.

<!-- facts: confidence=medium; plan=unknown; health_increase_pct=unknown; health_cap_adjustment=unknown; banked_cap_used=80128833; positions_cut=unknown; teacher_positions_cut=unknown; class_size_increase=unknown; our_benefits_match=unknown; our_aid_match=unknown -->
