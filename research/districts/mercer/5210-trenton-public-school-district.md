# Trenton Public School District (Mercer County) — district 5210
_Researched 2026-10-24. In SEHBP: yes (per Oct 2026 list). Sample: county least-squeezed._

## Our numbers
_Auto-generated from `data/processed/district_panel.csv` by `analysis/district_profiles.py`; every figure links to its public source. Baseline is the 2025-26 **revised** budget; state aid is NJDOE K-12 formula aid (FY26 → FY27)._
- **Benefits budget** 2025-26 (revised) → 2026-27: $19.72M → $23.02M (+16.7%). Source: [2026-27 User-Friendly Budget](https://www.nj.gov/education/budget/ufb/2627/reports/21/UFB27_5210.pdf), Appropriations, line "Total Personal Services – Employee Benefits" (columns 2025-26 revised / 2026-27 budget); also [UFB data files](https://www.nj.gov/education/budget/ufb/2627/index.shtml) `approp27.csv` line 71260.
- **Formula aid change** FY26 → FY27: +$23.98M. Source: [NJDOE FY27 K-12 aid, district details](https://www.nj.gov/education/stateaid/2627/FY27_GBM_District_Details.xlsx) (row for district 5210, "FY26–FY27 K–12 Aid Difference"). Aid change minus benefit increase: +$20.69M (computed).
- **Benefits share of operating budget** 2026-27: 10.9% (computed from [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/21/UFB27_5210.pdf): employee benefits ÷ Total General Current Expense).
- **Health share of district-paid benefits** FY25: 100.0%; **audited health growth** FY23→FY25: +13.0%. Source: audited ACFR Exhibit C-1, "Health Benefits" actual: [FY2025 report](https://www.nj.gov/education/finance/fp/acfr/search/25/5210.pdf#page=100), [FY2023 report](https://www.nj.gov/education/finance/fp/acfr/search/23/5210.pdf#page=100).
- **Tax levy change**: +2.0%; **budgeted fund balance used** 2025-26 → 2026-27: $15.04M → $26.18M. Source: [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/21/UFB27_5210.pdf), Revenues, lines "Total Tax Levy" and "Budgeted Fund Balance-Operating Budget".
- **Students per teacher** 2021-22 → 2024-25: 12.6 → 13.5. Source: [Taxpayers' Guide to Education Spending](https://www.nj.gov/education/guide/2025tges.shtml) Indicator 16 (2025 edition for 2024-25; [2023 edition](https://www.nj.gov/education/guide/) for 2021-22).
- **State-paid teacher pension/retiree medical** FY25 (not in the district budget): $44.84M. Source: [Treasury TPAF on-behalf allocations FY2025](https://www.nj.gov/education/fpp/audit/2425/docs/NJ_TPAF_Allocations_LEAs_FY2025.xlsx).
- **In SEHBP**: yes per the [October 2026 participating-employer list](https://www.nj.gov/treasury/pensions/documents/pdf/sehbpemp.pdf) (name-matched).
- ⚠️ former Abbott district: may budget by school, so the general-fund benefits line can be partial

## What the district / local reporting says
- [primary] UFB: general fund state revenue $403,656,121 (2025-26 revised) → $427,640,852 (2026-27), +$23.98M (equalization aid $370,033,663 → $391,886,403). Tax levy $25,739,874 → $26,254,671 (+2.0%). Budgeted fund balance $15,044,467 → **$26,182,973**. General fund total $478,729,084 → $481,459,736. Transfers to charter schools $68,072,280 → $76,512,681 (+$8.44M). "General Fund Contribution to School Based Budgeting" $177,044,610 → $191,835,997. Employee benefits line (11-XXX-XXX-2XX) $19,720,948 → $23,019,017. On-roll enrollment 16,619.5 → 16,872 est. [NJDOE UFB 2026-27, Trenton](https://www.nj.gov/education/budget/ufb/2627/reports/21/UFB27_5210.pdf), pp. 1-2, 5.
- [primary] Board meeting calendar: public hearing on the budget Apr. 27, 2026; a special meeting May 13, 2026 for "Non-Renewals" (routine annual action; counts not published on the page). [Trenton BOE Board Meetings](https://www.trentonk12.org/about_us/board_of_education/board_meetings), accessed Oct. 24, 2026. District news lists hiring events on Mar. 27 and Apr. 25, 2026 ([Mar. 27 Hiring Event](https://www.trentonk12.org/news/archived_news/march_27_hiring_event); [Apr. 25 Hiring Event](https://www.trentonk12.org/news/archived_news/april_25_hiring_event)).
- [snippet] An aggregator summary of the Apr. 27, 2026 meeting says the budget exceeds half a billion dollars with "55 cents of every dollar" going to classroom instruction, about $53M in grants and capital work, and a $12.95M capital reserve draw (per search snippet; [govly listing](https://app.govly.com/public/meetings/36796), AI-generated summary, not verified).
- No public reporting found on 2026-27 layoffs, position cuts, class sizes, health premium increases or cap adjustments (levy rose exactly 2%, so no adjustment appears to have been used).

## Verification of our numbers
- Aid: our formula aid change (+$23,984,731) equals the UFB general fund state revenue change exactly (p. 2).
- Levy: our +2.0% matches UFB p. 2.
- Fund balance: our $15.04M → $26.18M matches UFB p. 2.
- Benefits: our $19.72M → $23.02M (+16.7%) matches the UFB 2XX line, but **the line is incomplete** (flag `benefits_line_incomplete=True` is correct). Benefits for school-based staff sit inside the $191.8M school-based budgeting transfer (fund 15). Audited FY2025 health cost ($26.28M) is about double the FY2025 UFB 2XX line ($13.31M). Our `acfr_health_share_of_benefits_2025` = 100% is likely an artifact of comparing against the incomplete line and should be reviewed.

## Assessment
**Insufficient evidence.** Trenton received a ~$24M formula aid increase, about 7x the increase in its (incomplete) benefits line, and the district was hiring in spring 2026. No reporting ties cuts, layoffs or class-size increases to health costs, and no cuts were found. The sharply higher fund balance use ($26.2M) and +$8.4M charter transfers are the notable pressures.

## Confidence
**Low**: no district budget presentation, resolution or local news was accessible; the benefits line is structurally incomplete; meeting details come from an AI-summarized aggregator snippet.

## Open questions
- Total district health/benefit cost including fund 15 (school-based budgets) for 2025-26 and 2026-27.
- Content of the Apr. 27, 2026 budget presentation and May 13 non-renewal list (counts, roles).
- Why fund balance use rises to $26.2M despite a $24M aid increase (charter transfers? capital?).

<!-- facts: confidence=low; plan=SEHBP; health_increase_pct=unknown; health_cap_adjustment=none; banked_cap_used=none; positions_cut=unknown; teacher_positions_cut=unknown; class_size_increase=unknown; our_benefits_match=no; our_aid_match=yes -->
