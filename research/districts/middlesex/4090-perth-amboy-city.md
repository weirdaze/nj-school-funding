# Perth Amboy City (Middlesex County) — district 4090
_Researched 2026-10-24; revised after adversarial review 2026-10-24. In SEHBP: yes (per Oct 2026 list). Sample: county least-squeezed._

## Our numbers
_Auto-generated from `data/processed/district_panel.csv` by `analysis/district_profiles.py`; every figure links to its public source. Baseline is the 2025-26 **revised** budget; state aid is NJDOE K-12 formula aid (FY26 → FY27)._
- **Benefits budget** 2025-26 (revised) → 2026-27: $24.39M → $22.54M (-7.6%). Source: [2026-27 User-Friendly Budget](https://www.nj.gov/education/budget/ufb/2627/reports/23/UFB27_4090.pdf), Appropriations, line "Total Personal Services – Employee Benefits" (columns 2025-26 revised / 2026-27 budget); also [UFB data files](https://www.nj.gov/education/budget/ufb/2627/index.shtml) `approp27.csv` line 71260.
- **Formula aid change** FY26 → FY27: +$6.27M. Source: [NJDOE FY27 K-12 aid, district details](https://www.nj.gov/education/stateaid/2627/FY27_GBM_District_Details.xlsx) (row for district 4090, "FY26–FY27 K–12 Aid Difference"). Aid change minus benefit increase: +$8.11M (computed).
- **Benefits share of operating budget** 2026-27: 23.1% (computed from [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/23/UFB27_4090.pdf): employee benefits ÷ Total General Current Expense).
- **Health share of district-paid benefits** FY25: 80.3%; **audited health growth** FY23→FY25: +18.3%. Source: audited ACFR Exhibit C-1, "Health Benefits" actual: [FY2025 report](https://www.nj.gov/education/finance/fp/acfr/search/25/4090.pdf#page=90), [FY2023 report](https://www.nj.gov/education/finance/fp/acfr/search/23/4090.pdf#page=88).
- **Tax levy change**: +4.0%; **budgeted fund balance used** 2025-26 → 2026-27: $3.00M → $7.00M. Source: [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/23/UFB27_4090.pdf), Revenues, lines "Total Tax Levy" and "Budgeted Fund Balance-Operating Budget".
- **Students per teacher (TGES ratio)** 2021-22 → 2024-25: 11.9 → 13.3. Source: [Taxpayers' Guide to Education Spending](https://www.nj.gov/education/guide/2025tges.shtml) Indicator 16, file `CSG16.CSV` column `STRAT` (2025 edition for 2024-25; [2023 edition](https://www.nj.gov/education/guide/) for 2021-22). This divides students by all teaching staff, so it is roughly half of typical class size and is **not a class-size measure**; the 2024-25 value is the latest edition's newer column, which later editions usually confirm but which is not yet final.
- **State-paid teacher pension/retiree medical** FY25 (not in the district budget): $38.52M. Source: [Treasury TPAF on-behalf allocations FY2025](https://www.nj.gov/education/fpp/audit/2425/docs/NJ_TPAF_Allocations_LEAs_FY2025.xlsx).
- **In SEHBP**: yes per the [October 2026 participating-employer list](https://www.nj.gov/treasury/pensions/documents/pdf/sehbpemp.pdf) (name-matched).
- ⚠️ former Abbott district: may budget by school, so the general-fund benefits line can be partial

## What the district / local reporting says
- [primary] State UFB (generated July 14, 2026), p. 2. The state funds most of the budget: state revenue is $228,444,666 (2025-26) → $234,780,955 (2026-27), +$6.34M, including equalization aid $196.97M → $202.13M. The base levy rises from $30,049,204 to $31,251,172 (+4.0%). Budgeted fund balance rises from $3,000,000 to $7,000,000. The total general fund operating budget goes from $262.85M to $274.60M. [UFB27 4090](https://www.nj.gov/education/budget/ufb/2627/reports/23/UFB27_4090.pdf)
- [primary] UFB p. 4: the "Personal Services-Employee Benefits" line falls from $24,387,344 to $22,541,959. However, this line covers only the district's ~$97.6M general current expense, not its full ~$275M operating budget. As in other former Abbott districts, most spending (and the related benefits) sits in school-based budgets outside this line. Regular-programs instruction in the same section falls from $11.89M to $8.22M. UFB p. 8: employee benefits as a share of salaries rise from 53.94% (2025-26) to 62.10% (2026-27), up from 45.57% in 2023-24. That points to a substantial benefit increase district-wide despite the falling 71260 line. [UFB27 4090](https://www.nj.gov/education/budget/ufb/2627/reports/23/UFB27_4090.pdf)
- [primary] UFB p. 7: the row labelled "Legal Reserve" goes from $931,003 (6/30/2026) to $0 (est. 6/30/2027), a planned drawdown appropriated in the budget. This is separate from, and much smaller than, the $7.0M budgeted fund balance on p. 2. [UFB27 4090](https://www.nj.gov/education/budget/ufb/2627/reports/23/UFB27_4090.pdf)
- [primary] The district's budget page posts only the 2025-26 and 2026-27 UFBs, with no budget presentation. [PAPS District Budget page](https://www.paps.net/departments/business-office/district-budget) (accessed Oct. 24, 2026)
- No public reporting found on 2026-27 layoffs, class sizes, program cuts, health-care cap adjustment or banked cap. A Google Slides deck citing a 26.1% health increase appeared in searches for this district, but it is Highland Park's deck and was not used.

## Verification of our numbers
- Benefits: the UFB 71260 line is $24,387,344 → $22,541,959, which matches ours (-7.6%). Our panel already flags this district `benefits_line_incomplete=True`. The UFB confirms that the line covers only a fraction of operating spending, and the rising benefits-to-salaries ratio (53.94% → 62.10%) contradicts a real decline. Our ACFR health spending (FY23 $44.99M → FY25 $53.23M, +18.3%) is more than double the 71260 line, which confirms the line understates district benefits.
- Aid: our figure is NJDOE formula aid (+$6.27M); the UFB total state revenue change is +$6,336,289, a different definition, so the two do not match exactly (~$66K apart).
- Levy: +4.0%, which matches ours.
- Fund balance: $3.0M → $7.0M, which matches ours.

## Assessment
**Insufficient evidence.** Perth Amboy is labeled "least-squeezed" only because its 71260 benefits line is incomplete. The district-wide benefits-to-salaries ratio jumps about 8 points, and audited health costs have been growing about 9% a year (+18.3% over FY23→FY25). A $6.3M formula aid increase (total state revenue +$6.34M), a 4% levy increase and a larger budgeted fund balance ($3.0M → $7.0M, which includes appropriating the $0.93M legal reserve) appear to cover the gap. No public statements or reporting on cuts or health costs were found.

## Confidence
**Low**: only state UFB data was available. The key benefits figure in our data is known to be incomplete for this district.

## Open questions
- What is the true district-wide 2025-26 → 2026-27 benefits change, including school-based budgets (fund 15)? This needs the full budget statement.
- Why does the regular-instruction line fall $3.7M? Is this a recoding between central and school-based budgets?
- Why do UFB p. 1 enrollment estimates jump (on-roll regular full-time 9,056 → 10,579)?

<!-- facts: confidence=low; plan=SEHBP; health_increase_pct=unknown; health_cap_adjustment=unknown; banked_cap_used=unknown; positions_cut=unknown; teacher_positions_cut=unknown; class_size_increase=unknown; our_benefits_match=no; our_aid_match=no -->
