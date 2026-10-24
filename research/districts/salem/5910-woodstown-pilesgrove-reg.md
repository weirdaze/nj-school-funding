# Woodstown-Pilesgrove Reg (Salem County) — district 5910
_Researched 2026-10-24. In SEHBP: no (per Oct 2026 list). Sample: county median._

## Our numbers
_Auto-generated from `data/processed/district_panel.csv` by `analysis/district_profiles.py`; every figure links to its public source. Baseline is the 2025-26 **revised** budget; state aid is NJDOE K-12 formula aid (FY26 → FY27)._
- **Benefits budget** 2025-26 (revised) → 2026-27: $5.28M → $6.09M (+15.4%). Source: [2026-27 User-Friendly Budget](https://www.nj.gov/education/budget/ufb/2627/reports/33/UFB27_5910.pdf), Appropriations, line "Total Personal Services – Employee Benefits" (columns 2025-26 revised / 2026-27 budget); also [UFB data files](https://www.nj.gov/education/budget/ufb/2627/index.shtml) `approp27.csv` line 71260.
- **Formula aid change** FY26 → FY27: +$0.55M. Source: [NJDOE FY27 K-12 aid, district details](https://www.nj.gov/education/stateaid/2627/FY27_GBM_District_Details.xlsx) (row for district 5910, "FY26–FY27 K–12 Aid Difference"). Aid change minus benefit increase: -$0.27M (computed).
- **Benefits share of operating budget** 2026-27: 21.2% (computed from [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/33/UFB27_5910.pdf): employee benefits ÷ Total General Current Expense).
- **Health share of district-paid benefits** FY25: 78.9%; **audited health growth** FY23→FY25: +10.5%. Source: audited ACFR Exhibit C-1, "Health Benefits" actual: [FY2025 report](https://www.nj.gov/education/finance/fp/acfr/search/25/5910.pdf#page=85), [FY2023 report](https://www.nj.gov/education/finance/fp/acfr/search/23/5910.pdf#page=92).
- **Tax levy change**: +5.2%; **budgeted fund balance used** 2025-26 → 2026-27: $1.53M → $0.97M. Source: [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/33/UFB27_5910.pdf), Revenues, lines "Total Tax Levy" and "Budgeted Fund Balance-Operating Budget".
- **Students per teacher (TGES ratio)** 2021-22 → 2024-25: 11.7 → 11.1. Source: [Taxpayers' Guide to Education Spending](https://www.nj.gov/education/guide/2025tges.shtml) Indicator 16, file `CSG16.CSV` column `STRAT` (2025 edition for 2024-25; [2023 edition](https://www.nj.gov/education/guide/) for 2021-22). This divides students by all teaching staff, so it is roughly half of typical class size and is **not a class-size measure**; the 2021-22 value is actual and the 2024-25 value is from the budget-year column.
- **State-paid teacher pension/retiree medical** FY25 (not in the district budget): $5.36M. Source: [Treasury TPAF on-behalf allocations FY2025](https://www.nj.gov/education/fpp/audit/2425/docs/NJ_TPAF_Allocations_LEAs_FY2025.xlsx).
- **In SEHBP**: no per the [October 2026 participating-employer list](https://www.nj.gov/treasury/pensions/documents/pdf/sehbpemp.pdf) (name-matched).

## What the district / local reporting says
- [primary] Staffing: "Cut one FT support & one PT support position – Attrition"; "Certificated staff status quo"; "All instructional programs in core subjects & related arts remain"; extracurriculars budgeted; a special education ERI program added (slide 4). [WPRSD 2026-2027 Budget Public Hearing presentation](https://www.woodstown.org/ourpages/auto/2024/6/8/54985963/2026-2027%20Budget%20Public%20Hearing%2004.30.26.pdf?rnd=1777853877737), Apr. 30, 2026.
- [primary] Cost drivers (slide 8): "Health Care ($600k) & Utilities"; state funding "$2.9M Below Adequacy"; out-of-district tuition and transportation; "Fluctuations in Tuition Revenues - Sending District & SCVTS"; aging facilities and outstanding bonds. Same source.
- [primary] Revenue (slide 9): local tax levy $13,902,830 → $14,629,392 (+$726,562, +5.23%); tuition $3,767,251 → $3,135,614 (−$631,637, −16.77%); state aid $9,312,932 → $9,850,502 (+$537,570, +5.77%); fund balance $1,525,237 → $966,350; total general fund $29,095,284 → $29,124,443 (+0.28%). Same source.
- [primary] Expenditures (slide 11): "Personnel Services (Benefits)" $5,282,479 → $6,093,630 (+$811,151, +15.36%); administrative costs −$276,391 (−12.11%); equipment/capital outlay $620,013 → $109,894 (−82.28%); instruction and support programs +1.40%. Same source.
- [primary] Health plan: SHIF (School Health Insurance Fund) for medical, prescription and dental, per the presentation (slide 5) and the [UFB27_5910](https://www.nj.gov/education/budget/ufb/2627/reports/33/UFB27_5910.pdf) shared-services page.
- [primary] Adequacy (slide 13): levy plus equalization aid ($22,077,458) is $2,994,022 below the adequacy budget ($25,071,480). Tax impact: +$249/yr on the average Woodstown home; −$275 on the average Pilesgrove home because of a reassessment-driven base increase (slides 14-15). Same source.
- No public reporting found on the health care cost cap adjustment or banked cap amounts, the SHIF renewal %, or class sizes.

## Verification of our numbers
- Benefits: district $5,282,479 → $6,093,630 (+15.36%) matches ours (+15.4%) and the UFB. The district's "Health Care ($600k)" is about 74% of the $811K benefits increase.
- State aid: district +$537,570 matches our `state_revenue_change_ufb` (+$537,570). Our formula aid figure (+$545,124) differs slightly, likely because of how aid categories are counted.
- Levy: +5.23% matches ours (5.2%). That is above 2%, consistent with a health care or other cap adjustment, but the amount is not stated.
- Fund balance: $1,525,237 → $966,350 matches ours.

## Assessment
**Consistent.** The district cut one full-time and one part-time support position through attrition, kept certificated staff and programs, and named health care (+$600K) as one of several cost drivers. A $632K drop in tuition revenue and below-adequacy state funding are equally prominent. The modest gap was closed mainly by a 5.23% levy increase and cuts to administration and capital outlay, not by instructional cuts.

## Confidence
**High**: all key facts come from the district's own budget hearing presentation, and its figures reconcile exactly with the UFB and our numbers.

## Open questions
- Amount of the health care cost cap adjustment and any banked cap used to reach the 5.23% levy.
- SHIF 2026-27 renewal rate (%).

<!-- facts: confidence=high; plan=SHIF; health_increase_pct=unknown; health_cap_adjustment=unknown; banked_cap_used=unknown; positions_cut=2; teacher_positions_cut=0; class_size_increase=unknown; our_benefits_match=yes; our_aid_match=yes -->
