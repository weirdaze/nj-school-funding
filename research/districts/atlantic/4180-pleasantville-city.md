# Pleasantville City (Atlantic County) — district 4180
_Researched 2026-10-24; revised after adversarial review 2026-10-24. In SEHBP: yes (per Oct 2026 list). Sample: county least-squeezed._

## Our numbers
_Auto-generated from `data/processed/district_panel.csv` by `analysis/district_profiles.py`; every figure links to its public source. Baseline is the 2025-26 **revised** budget; state aid is NJDOE K-12 formula aid (FY26 → FY27)._
- **Benefits budget** 2025-26 (revised) → 2026-27: $6.78M → $7.41M (+9.3%). Source: [2026-27 User-Friendly Budget](https://www.nj.gov/education/budget/ufb/2627/reports/01/UFB27_4180.pdf), Appropriations, line "Total Personal Services – Employee Benefits" (columns 2025-26 revised / 2026-27 budget); also [UFB data files](https://www.nj.gov/education/budget/ufb/2627/index.shtml) `approp27.csv` line 71260.
- **Formula aid change** FY26 → FY27: +$3.46M. Source: [NJDOE FY27 K-12 aid, district details](https://www.nj.gov/education/stateaid/2627/FY27_GBM_District_Details.xlsx) (row for district 4180, "FY26–FY27 K–12 Aid Difference"). Aid change minus benefit increase: +$2.83M (computed).
- **Benefits share of operating budget** 2026-27: 15.7% (computed from [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/01/UFB27_4180.pdf): employee benefits ÷ Total General Current Expense).
- **Health share of district-paid benefits** FY25: 70.8%; **audited health growth** FY23→FY25: +28.6%. Source: audited ACFR Exhibit C-1, "Health Benefits" actual: [FY2025 report](https://www.nj.gov/education/finance/fp/acfr/search/25/4180.pdf#page=90), [FY2023 report](https://www.nj.gov/education/finance/fp/acfr/search/23/4180.pdf#page=94).
- **Tax levy change**: +13.7%; **budgeted fund balance used** 2025-26 → 2026-27: $14.86M → $7.42M. Source: [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/01/UFB27_4180.pdf), Revenues, lines "Total Tax Levy" and "Budgeted Fund Balance-Operating Budget".
- **Students per teacher (TGES ratio)** 2021-22 → 2024-25: 10.9 → 11.5. Source: [Taxpayers' Guide to Education Spending](https://www.nj.gov/education/guide/2025tges.shtml) Indicator 16, file `CSG16.CSV` column `STRAT` (2025 edition for 2024-25; [2023 edition](https://www.nj.gov/education/guide/) for 2021-22). This divides students by all teaching staff, so it is roughly half of typical class size and is **not a class-size measure**; the 2024-25 value is the latest edition's newer column, which later editions usually confirm but which is not yet final.
- **State-paid teacher pension/retiree medical** FY25 (not in the district budget): $14.95M. Source: [Treasury TPAF on-behalf allocations FY2025](https://www.nj.gov/education/fpp/audit/2425/docs/NJ_TPAF_Allocations_LEAs_FY2025.xlsx).
- **In SEHBP**: yes per the [October 2026 participating-employer list](https://www.nj.gov/treasury/pensions/documents/pdf/sehbpemp.pdf) (name-matched).
- ⚠️ former Abbott district: may budget by school, so the general-fund benefits line can be partial

## What the district / local reporting says
- [primary] State UFB: employee benefits (line 11-XXX-XXX-2XX) $5,035,592 (2024-25 actual) → $6,782,317 (2025-26 revised) → $7,409,883 (2026-27 proposed), p. 4; benefits as % of salaries 37.05% → 44.35%, p. 8; levy $10,374,405 → $11,800,559, p. 2; equalization aid $78,865,063 → $82,488,314, total state revenue $87,657,528 → $91,119,105, p. 2; budgeted fund balance $14,857,021 → $7,421,695, p. 2; enrollment on roll 3,831 → 3,782 (est.), p. 1. [NJDOE UFB 2026-27, Pleasantville City](https://www.nj.gov/education/budget/ufb/2627/reports/01/UFB27_4180.pdf), generated July 14, 2026.
- [primary] Pleasantville budgets by school (school-based budgeting): appropriations in school-based budgets total $56,685,650 (2025-26) → $52,877,833 (2026-27). [NJDOE UFB data file schapp27.csv](https://www.nj.gov/education/budget/ufb/2627/index.shtml) (repo copy `data/raw/ufb/2627/schapp27.csv`). Benefits for school-based staff are likely charged within those budgets rather than the line we use; see verification.
- [snippet] A Press of Atlantic City article, "Pleasantville school budget will raise taxes, eliminate 11 positions," lists two principals on special assignment, two deans of students and the director of curriculum among cuts ("eliminate 11 positions"); it is dated May 8, 2019 (page metadata checked 2026-10-25), so it concerns the 2019-20 budget, not 2026-27. [Press of Atlantic City](https://pressofatlanticcity.com/education/pleasantville-school-budget-will-raise-taxes-eliminate-positions/article_15393d14-92d3-5f4a-8d43-a1451785f12b.html) (headline and date read 2026-10-25; article body is behind the paywall).
- No public reporting found on 2026-27 staff reductions, class sizes, health-cost commentary or the health-care cap adjustment. The district website (pps-nj.us) did not expose budget documents to a non-JavaScript fetch. Note: "Pleasantville" searches mostly return Pleasantville UFSD in New York, which is a different district.

## Verification of our numbers
- Benefits $6,782,317 → $7,409,883 (+$627,566, +9.3%): **match** UFB p. 4, but the line is **incomplete** for this district: audited benefits (FY25 ACFR total $11.8M; C-1 health benefits $9,305,220, per independent review) exceed the whole UFB benefits line ($5.0M actual 2024-25), consistent with benefits being budgeted inside school-based budgets. Our benefit growth figure therefore understates the true change.
- Formula aid +$3,461,577: **match** UFB total state revenue change p. 2 ($87,657,528 → $91,119,105, +$3,461,577); here formula aid and total state revenue change by the same amount.
- Levy +13.7%: **match** UFB p. 2 (+$1,426,154). This is far above the 2% cap; the adjustments used were not found.
- Fund balance used $14,857,021 → $7,421,695: **match** UFB p. 2 (a $7.4M drop in budgeted surplus).

## Assessment
**Insufficient evidence.** Formula aid rose $3.5M and the measured benefits line only $0.6M, but that line misses school-based benefits, and the district cut its fund-balance draw in half while raising the levy 13.7%. No 2026-27 district or news source on cuts or health costs was found.

## Confidence
**Low**: only the state UFB was verified; the one news item on cuts is from 2019; our benefits line is known to be incomplete.

## Open questions
- What is Pleasantville's total (district-wide) health benefit cost change for 2026-27 including school-based budgets?
- What cap adjustments justified a 13.7% levy increase (health care, banked cap, other)?
- Did the falling school-based appropriations (-$3.8M) involve staff reductions?

<!-- facts: confidence=low; plan=SEHBP; health_increase_pct=unknown; health_cap_adjustment=unknown; banked_cap_used=unknown; positions_cut=unknown; teacher_positions_cut=unknown; class_size_increase=unknown; our_benefits_match=no; our_aid_match=yes -->
