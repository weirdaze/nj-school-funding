# Union City (Hudson County) — district 5240
_Researched 2026-10-24. In SEHBP: no (per Oct 2026 list). Sample: county least-squeezed._

## Our numbers
_Auto-generated from `data/processed/district_panel.csv` by `analysis/district_profiles.py`; every figure links to its public source. Baseline is the 2025-26 **revised** budget; state aid is NJDOE K-12 formula aid (FY26 → FY27)._
- **Benefits budget** 2025-26 (revised) → 2026-27: $25.86M → $19.06M (-26.3%). Source: [2026-27 User-Friendly Budget](https://www.nj.gov/education/budget/ufb/2627/reports/17/UFB27_5240.pdf), Appropriations, line "Total Personal Services – Employee Benefits" (columns 2025-26 revised / 2026-27 budget); also [UFB data files](https://www.nj.gov/education/budget/ufb/2627/index.shtml) `approp27.csv` line 71260.
- **Formula aid change** FY26 → FY27: +$1.11M. Source: [NJDOE FY27 K-12 aid, district details](https://www.nj.gov/education/stateaid/2627/FY27_GBM_District_Details.xlsx) (row for district 5240, "FY26–FY27 K–12 Aid Difference"). Aid change minus benefit increase: +$7.92M (computed).
- **Benefits share of operating budget** 2026-27: 15.8% (computed from [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/17/UFB27_5240.pdf): employee benefits ÷ Total General Current Expense).
- **Health share of district-paid benefits** FY25: 77.4%; **audited health growth** FY23→FY25: +30.6%. Source: audited ACFR Exhibit C-1, "Health Benefits" actual: [FY2025 report](https://www.nj.gov/education/finance/fp/acfr/search/25/5240.pdf#page=92), [FY2023 report](https://www.nj.gov/education/finance/fp/acfr/search/23/5240.pdf#page=91).
- **Tax levy change**: +0.0%; **budgeted fund balance used** 2025-26 → 2026-27: $18.19M → $0.26M. Source: [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/17/UFB27_5240.pdf), Revenues, lines "Total Tax Levy" and "Budgeted Fund Balance-Operating Budget".
- **Students per teacher (TGES ratio)** 2021-22 → 2024-25: 12.9 → 13.1. Source: [Taxpayers' Guide to Education Spending](https://www.nj.gov/education/guide/2025tges.shtml) Indicator 16, file `CSG16.CSV` column `STRAT` (2025 edition for 2024-25; [2023 edition](https://www.nj.gov/education/guide/) for 2021-22). This divides students by all teaching staff, so it is roughly half of typical class size and is **not a class-size measure**; the 2021-22 value is actual and the 2024-25 value is from the budget-year column.
- **State-paid teacher pension/retiree medical** FY25 (not in the district budget): $46.59M. Source: [Treasury TPAF on-behalf allocations FY2025](https://www.nj.gov/education/fpp/audit/2425/docs/NJ_TPAF_Allocations_LEAs_FY2025.xlsx).
- **In SEHBP**: no per the [October 2026 participating-employer list](https://www.nj.gov/treasury/pensions/documents/pdf/sehbpemp.pdf) (name-matched).
- ⚠️ the 2025-26 benefits budget was revised +21% mid-year ($21.30M original → $25.86M revised); measured from the original budget the 2026-27 change is -10.5%; former Abbott district: may budget by school, so the general-fund benefits line can be partial

## What the district / local reporting says
- [primary] UFB: employee benefits line (11-XXX-XXX-2XX) $29,613,968 (2024-25 actual) → $25,864,200 (2025-26 revised) → $19,056,442 (2026-27). But most of the general fund goes out as "General Fund Contribution to School Based Budgeting" (10-000-520-930): $151,248,603 → $145,326,184. Benefits for school-based staff are budgeted there, not in the 2XX line. [NJDOE UFB 2026-27, Union City](https://www.nj.gov/education/budget/ufb/2627/reports/17/UFB27_5240.pdf), pp. 4-5 (generated July 14, 2026).
- [primary] UFB: general fund total $300,750,907 (2025-26 revised) → $268,796,813 (2026-27), down $32.0M; budgeted fund balance $18,192,773 → $257,064; tax levy flat at $15,418,637 for three years; general fund state revenue $246,248,198 → $247,583,260; on-roll enrollment 11,089.5 → 11,086 est. Same source, pp. 1-2, 5. Some lines shrink: operation and maintenance of plant $42.87M → $36.92M, regular programs instruction $8.10M → $4.26M, general administration $6.64M → $5.33M, administrative IT $1.91M → $0.80M (p. 4). The UFB does not say whether these are staffing cuts or one-time 2025-26 spending, such as revised appropriations funded by fund balance.
- [primary] The district's Business Department page posts the 2025-26 user-friendly budget but no 2026-27 budget presentation or narrative. [Union City BOE Business Department](https://www.ucboe.us/apps/pages/index.jsp?uREC_ID=416102&type=d), accessed Oct. 24, 2026.
- No public reporting found on 2026-27 layoffs, position cuts, class sizes, the district's health plan or premium increase, cap adjustments or banked cap (the levy is flat, so neither appears to have been used).

## Verification of our numbers
- Benefits: our figures ($25.86M → $19.06M, -26.3%) match UFB p. 4, but **the line does not represent district benefits** (our flag `benefits_line_incomplete=True` is correct). The audited FY2025 health cost ($54.59M in our ACFR column) is nearly 3x the FY2025 UFB 2XX line ($29.6M), because school-based budget benefits sit in the $145M transfer. The -26.3% should not be read as a benefit decrease.
- State revenue: our UFB state revenue change (+$1.34M) matches UFB p. 2 ($246.25M → $247.58M). Formula aid +$1.11M: no district statement to compare.
- Levy 0.0% and fund balance $18.19M → $0.26M match UFB p. 2.

## Assessment
**Insufficient evidence.** Union City's general fund budget fell about $32M (‑10.6%) as budgeted fund balance dropped from $18.2M to near zero with a flat levy and flat aid, which suggests real spending reductions. But no district or press account describes layoffs or attributes anything to health costs. Our benefits figures for this district are structurally incomplete and should be excluded from benefit-growth comparisons.

## Confidence
**Low**: the only source is the UFB, with no district narrative or news coverage, and our benefits line is known to be incomplete.

## Open questions
- What is in the $145.3M school-based budget transfer (fund 15), and how much of it is health benefits? The FY2025 ACFR shows $54.6M health.
- Did the ~$32M general fund reduction involve staff cuts, or was it removal of one-time 2025-26 fund-balance spending?
- Health plan (SEHBP not used) and the 2026-27 premium change.

<!-- facts: confidence=low; plan=unknown; health_increase_pct=unknown; health_cap_adjustment=none; banked_cap_used=none; positions_cut=unknown; teacher_positions_cut=unknown; class_size_increase=unknown; our_benefits_match=no; our_aid_match=unknown -->
