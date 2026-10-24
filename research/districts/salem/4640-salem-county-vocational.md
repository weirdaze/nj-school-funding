# Salem County Vocational (Salem County) — district 4640
_Researched 2026-10-24. In SEHBP: no (per Oct 2026 list). Sample: county most-squeezed (% of budget)._

## Our numbers
_Auto-generated from `data/processed/district_panel.csv` by `analysis/district_profiles.py`; every figure links to its public source. Baseline is the 2025-26 **revised** budget; state aid is NJDOE K-12 formula aid (FY26 → FY27)._
- **Benefits budget** 2025-26 (revised) → 2026-27: $2.87M → $3.71M (+29.0%). Source: [2026-27 User-Friendly Budget](https://www.nj.gov/education/budget/ufb/2627/reports/33/UFB27_4640.pdf), Appropriations, line "Total Personal Services – Employee Benefits" (columns 2025-26 revised / 2026-27 budget); also [UFB data files](https://www.nj.gov/education/budget/ufb/2627/index.shtml) `approp27.csv` line 71260.
- **Formula aid change** FY26 → FY27: +$0.23M. Source: [NJDOE FY27 K-12 aid, district details](https://www.nj.gov/education/stateaid/2627/FY27_GBM_District_Details.xlsx) (row for district 4640, "FY26–FY27 K–12 Aid Difference"). Aid change minus benefit increase: -$0.61M (computed).
- **Benefits share of operating budget** 2026-27: 20.8% (computed from [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/33/UFB27_4640.pdf): employee benefits ÷ Total General Current Expense).
- **Health share of district-paid benefits** FY25: 74.5%; **audited health growth** FY23→FY25: +13.5%. Source: audited ACFR Exhibit C-1, "Health Benefits" actual: [FY2025 report](https://www.nj.gov/education/finance/fp/acfr/search/25/4640.pdf#page=83), [FY2023 report](https://www.nj.gov/education/finance/fp/acfr/search/23/4640.pdf#page=82).
- **Tax levy change**: +2.0%; **budgeted fund balance used** 2025-26 → 2026-27: $0.04M → $1.18M. Source: [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/33/UFB27_4640.pdf), Revenues, lines "Total Tax Levy" and "Budgeted Fund Balance-Operating Budget".
- **Students per teacher (TGES ratio)** 2021-22 → 2024-25: 16.0 → n/a. Source: [Taxpayers' Guide to Education Spending](https://www.nj.gov/education/guide/2025tges.shtml) Indicator 16, file `CSG16.CSV` column `STRAT` (2025 edition for 2024-25; [2023 edition](https://www.nj.gov/education/guide/) for 2021-22). This divides students by all teaching staff, so it is roughly half of typical class size and is **not a class-size measure**; the 2024-25 value is the latest edition's newer column, which later editions usually confirm but which is not yet final.
- **State-paid teacher pension/retiree medical** FY25 (not in the district budget): $1.76M. Source: [Treasury TPAF on-behalf allocations FY2025](https://www.nj.gov/education/fpp/audit/2425/docs/NJ_TPAF_Allocations_LEAs_FY2025.xlsx).
- **In SEHBP**: no per the [October 2026 participating-employer list](https://www.nj.gov/treasury/pensions/documents/pdf/sehbpemp.pdf) (name-matched).

## What the district / local reporting says
- [primary] State UFB 2026-27: county tax levy $1,865,280 (2025-26 revised) → $1,902,528 (2026-27); state sources revenue $11,494,485 → $11,721,409 (equalization aid $10,410,279 → $10,675,669); tuition from sending districts $3,450,669 → $2,989,840; budgeted fund balance $41,885 → $1,177,798; employee benefits $2,313,604 (2024-25 actual) → $2,873,030 (2025-26 revised) → $3,706,760 (2026-27); benefits as a share of salaries 45.80% (2025-26 revised) → 58.57% (2026-27); on-roll enrollment 835 → 723 (estimate, which shows shared-time and post-secondary at 0). Pages 1, 2, 4 and 7. [NJDOE UFB27_4640](https://www.nj.gov/education/budget/ufb/2627/reports/33/UFB27_4640.pdf), generated July 14, 2026. The district posts the same UFB on its site, dated May 8, 2026. [SCVTS 2026-27 Budget Summary](https://scvts.org/wp-content/uploads/2026/05/SCVTS-2026-27-Budget-Summary.pdf).
- [primary] March 18, 2026 budget meeting agenda: preliminary 2026-27 budget listed as general fund $16,852,819, local tax levy $1,865,280, special revenue $1,380,970, total base budget $18,233,789 (p. 3). The "board presentation" was attached in BoardDocs but not in the posted PDF. The district shares its board, superintendent and business office with Salem County Special Services (district 4635). [Budget Meeting Agenda 3/18/2026](https://scvts.org/wp-content/uploads/2026/03/Budget-Meeting-Agenda-03-18-2026.pdf); shared roles per [UFB27_4640](https://www.nj.gov/education/budget/ufb/2627/reports/33/UFB27_4640.pdf) pp. 8-10.
- No public reporting found on staff reductions, class sizes, health plan or premium increases, a health care cost cap adjustment, banked cap, or program cuts.

## Verification of our numbers
- Benefits: UFB $2,873,030 → $3,706,760 (+29.0%) matches ours. The 2025-26 original budget ($3,173,030) was higher than revised.
- State aid: UFB state revenue +$226,924 matches ours.
- Levy: +2.0% per UFB, matching ours.
- Fund balance: $41,885 → $1,177,798, matching ours.
- Data issue: our `acfr_health_2023` = 1518.061 is clearly a units error (likely $1,518,061 entered in thousands), which is why `acfr_health_growth_23_25_pct` is blank.

## Assessment
**Insufficient evidence.** Budgeted benefits rise 29% (+$834K: $2,873,030 → $3,706,760) against a $227K aid increase, closed mainly by a $1.18M fund balance draw and a 2% levy increase. Tuition revenue falls with lower projected enrollment. We found no district narrative or news coverage of cuts or of health costs.

## Confidence
**Low**: district and state budget documents reconcile with our numbers, but they contain no narrative about cuts or health costs, and no local reporting exists.

## Open questions
- Health plan (SHIF or other) and renewal rate for the vo-tech and special services districts.
- Whether the projected enrollment drop (835 → 723) reflects real program changes or only the estimate's zeroed shared-time and post-secondary rows.

<!-- facts: confidence=low; plan=unknown; health_increase_pct=unknown; health_cap_adjustment=unknown; banked_cap_used=unknown; positions_cut=unknown; teacher_positions_cut=unknown; class_size_increase=unknown; our_benefits_match=yes; our_aid_match=yes -->
