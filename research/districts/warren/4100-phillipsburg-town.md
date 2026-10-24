# Phillipsburg Town (Warren County) — district 4100
_Researched 2026-10-24. In SEHBP: no (per Oct 2026 list). Sample: county least-squeezed._

## Our numbers
_Auto-generated from `data/processed/district_panel.csv` by `analysis/district_profiles.py`; every figure links to its public source. Baseline is the 2025-26 **revised** budget; state aid is NJDOE K-12 formula aid (FY26 → FY27)._
- **Benefits budget** 2025-26 (revised) → 2026-27: $6.23M → $7.06M (+13.2%). Source: [2026-27 User-Friendly Budget](https://www.nj.gov/education/budget/ufb/2627/reports/41/UFB27_4100.pdf), Appropriations, line "Total Personal Services – Employee Benefits" (columns 2025-26 revised / 2026-27 budget); also [UFB data files](https://www.nj.gov/education/budget/ufb/2627/index.shtml) `approp27.csv` line 71260.
- **Formula aid change** FY26 → FY27: +$3.27M. Source: [NJDOE FY27 K-12 aid, district details](https://www.nj.gov/education/stateaid/2627/FY27_GBM_District_Details.xlsx) (row for district 4100, "FY26–FY27 K–12 Aid Difference"). Aid change minus benefit increase: +$2.44M (computed).
- **Benefits share of operating budget** 2026-27: 18.7% (computed from [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/41/UFB27_4100.pdf): employee benefits ÷ Total General Current Expense).
- **Health share of district-paid benefits** FY25: 79.9%; **audited health growth** FY23→FY25: +12.8%. Source: audited ACFR Exhibit C-1, "Health Benefits" actual: [FY2025 report](https://www.nj.gov/education/finance/fp/acfr/search/25/4100.pdf#page=79), [FY2023 report](https://www.nj.gov/education/finance/fp/acfr/search/23/4100.pdf#page=81).
- **Tax levy change**: +3.0%; **budgeted fund balance used** 2025-26 → 2026-27: $0.43M → $0.28M. Source: [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/41/UFB27_4100.pdf), Revenues, lines "Total Tax Levy" and "Budgeted Fund Balance-Operating Budget".
- **Students per teacher** 2021-22 → 2024-25: 11.4 → 10.6. Source: [Taxpayers' Guide to Education Spending](https://www.nj.gov/education/guide/2025tges.shtml) Indicator 16 (2025 edition for 2024-25; [2023 edition](https://www.nj.gov/education/guide/) for 2021-22).
- **State-paid teacher pension/retiree medical** FY25 (not in the district budget): $16.18M. Source: [Treasury TPAF on-behalf allocations FY2025](https://www.nj.gov/education/fpp/audit/2425/docs/NJ_TPAF_Allocations_LEAs_FY2025.xlsx).
- **In SEHBP**: no per the [October 2026 participating-employer list](https://www.nj.gov/treasury/pensions/documents/pdf/sehbpemp.pdf) (name-matched).
- ⚠️ former Abbott district: may budget by school, so the general-fund benefits line can be partial

## What the district / local reporting says
- [primary] Employee benefits (11-XXX-XXX-2XX): $4,763,247 actual 2024-25, $6,232,864 revised 2025-26, $7,058,328 proposed 2026-27. [NJDOE 2026-27 UFB, Phillipsburg Town](https://www.nj.gov/education/budget/ufb/2627/reports/41/UFB27_4100.pdf), p. 5 (generated July 14, 2026). The district posts the same UFB on its [Budget page](https://www.pburgsd.net/apps/pages/index.jsp?uREC_ID=1201822&type=d&pREC_ID=1441374).
- [primary] **School-based budgeting**: the general fund contribution to school-based budgets is $51,584,262 (2025-26 revised) and $52,375,839 (2026-27), larger than the entire $37.65M general current expense shown outside it. [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/41/UFB27_4100.pdf), Appropriations. Salaries and benefits of school-based staff are budgeted there, so the 11-XXX-XXX-2XX line covers only part of the district's benefits. Benefits are reported as 36.45% of salaries for 2026-27 (UFB per-pupil page).
- [primary] Revenue: levy $13,491,989 to $13,896,749; equalization aid $48,376,596 to $51,234,463; total general fund state sources $54,542,317 to $57,810,850; tuition from other districts $15,911,453 to $16,631,424; capital reserve withdrawal $5,200,000 to $2,100,000; budgeted fund balance $425,680 to $280,916. [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/41/UFB27_4100.pdf), pp. 2-3.
- [primary] Federal special revenue: Title I $1,468,432 to $1,101,324 and IDEA $1,098,534 to $691,500, so total federal projects fall by $1,038,289. [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/41/UFB27_4100.pdf), p. 3.
- [primary] Enrollment: on-roll 3,795 (Oct 2025) to 3,928 (Oct 2026 est.). [UFB](https://www.nj.gov/education/budget/ufb/2627/reports/41/UFB27_4100.pdf), p. 1.
- The board's agendas and minutes are on BoardDocs, which returned 403 to automated access. No budget presentation was posted on the district budget page. Searches returned no news coverage. Results for "PHS" budget cuts referred to Princeton High School, not Phillipsburg.
- No public reporting found on staff reductions, class sizes, health cost increases, health plan or cap adjustments for 2026-27.

## Verification of our numbers
- Benefits: the UFB line's $6,232,864 to $7,058,328 matches ours (+$825,464, +13.2%). **This line is incomplete for Phillipsburg** (our benefits_line_incomplete flag) because school-based staff are budgeted in the $52.4M school-based-budget contribution. Audited FY25 health benefits ($11.95M in our ACFR data) are almost double the 2025-26 UFB benefits line. Neither the benefits share of budget nor the benefits growth rate should be used for this district. The 2025-26 revised figure is also $548,662 below the original ($6,781,526), which further distorts the percentage change.
- State aid: the UFB shows general fund state sources up $3,268,533, which matches our formula aid and UFB state revenue change.
- Levy: +3.0%, which matches.
- Fund balance: $425,680 and $280,916 match.

## Assessment
**Insufficient evidence.** Phillipsburg received about $3.27M more state aid, and its levy rose 3.0%. No district statement or news coverage of cuts or health costs was found. Because of school-based budgeting, our benefits figures understate the district's true benefit costs. Calling it "least-squeezed" rests on an incomplete benefits line, although the large aid increase probably holds regardless.

## Confidence
**Low**: only the UFB was opened, district minutes were inaccessible, and our benefits measure is structurally incomplete for this district.

## Open questions
- What are total district-wide health benefits for 2026-27, including the school-based budgets? The ACFR suggests about $12M or more.
- Did the federal aid cuts (-$1.04M Title I and IDEA) lead to staffing changes?
- What is the health plan?

<!-- facts: confidence=low; plan=unknown; health_increase_pct=unknown; health_cap_adjustment=unknown; banked_cap_used=unknown; positions_cut=unknown; teacher_positions_cut=unknown; class_size_increase=unknown; our_benefits_match=no; our_aid_match=yes -->
