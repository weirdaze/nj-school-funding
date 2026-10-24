# Garfield City (Bergen County) — district 1700
_Researched 2026-10-24. In SEHBP: yes (per Oct 2026 list). Sample: county least-squeezed._

## Our numbers
(filled automatically)

## What the district / local reporting says
- [primary] State aid: $82,951,498 (2025-26) → $87,924,588 (2026-27), +$4,973,090 (6%). [Garfield Public Schools, 2026-2027 Budget Presentation, Mar. 30, 2026, slide 15](https://www.gboe.org/UserFiles/Servers/Server_66689/Image/Board%20of%20Education/Budgets/GBOE%20-3%2030%2026%20Budget%20Presentation-FY26-27.pdf).
- [primary] "Where does the $4.9 million go?": "Premium Increases in Health Benefits Total 26-27 Increase: $3,580,960"; charter schools +$1,214,655; energy +$850,354. Same presentation, slide 16. Slide 20 repeats the $3,580,960 health increase and adds substitutes (+$851,000) and special education tuition (+$1,287,623).
- [primary] Cost control: "Position Control Adjustment: Estimated 60 less positions resulting in nearly $7 Million Saved in Salary and Benefit Appropriations"; in-house pre-K special ed ABA saving $498,198; $3,500,000 budgeted fund balance. Same presentation, slide 21. Roles and layoffs vs. attrition are not given.
- [primary] Levy $37,306,500 → $39,173,640 (+$1,867,140, +5.0%); average home +$245/yr. Slide 22. A 0% levy would mean "Additional 22-25 positions will be eliminated" and "Overcrowded Classrooms," slide 25 (a hypothetical, not the adopted plan).
- [primary] General fund "Employee Benefits" $7,368,174 → $8,260,750; "General Fund Contribution to schools" $62,247,772 → $63,701,909. Slide 17. The district is $17,768,723 below adequacy, slide 26.
- [snippet] Aggregator summaries of March 2026 board meetings describe ~60 positions cut to address an $18M shortfall under adequacy, attributed to rising healthcare and energy costs (per search snippet; auto-generated text, not relied on).
- No public reporting found on actual class sizes, the health care cap adjustment amount, or banked cap.

## Verification of our numbers
- Benefits line $7,368,174 → $8,260,750 (+$892,576, +12.1%): **match** district slide 17 and [UFB p. 4](https://www.nj.gov/education/budget/ufb/2627/reports/03/UFB27_1700.pdf), but **mismatch** with the district's total health premium increase of $3,580,960 (slide 16). Garfield uses school-based budgeting (school-based appropriations $62.9M → $64.1M per NJDOE `schapp27.csv`), so most benefits sit in school budgets, not line 71260. Audited FY25 health costs ($13.4M) far exceed the whole benefits line, which confirms it. Our benefit change understates the real increase by roughly $2.7M.
- Formula aid +$4,923,090 vs district +$4,973,090: the $50,000 difference is extraordinary aid ($900,000 → $950,000, UFB p. 2). **Match.**
- Levy +5.0%: **match** slide 22.
- Fund balance $3,300,000 → $3,500,000: **match** UFB p. 2 / slide 21.

## Assessment
**Consistent.** The district's own presentation says a $3.58M health premium increase absorbs most of the $4.97M state aid increase, and it cuts an estimated 60 positions (~$7M in salaries and benefits). Health is the largest single cost driver listed, but charter, energy, substitute and special-ed tuition increases are also cited, and the deck does not say the cuts were made specifically because of health costs.

## Confidence
**Medium**: from the district's own presentation, which we opened, and aid, levy and fund balance reconcile; but our benefits line ($0.89M) is known to be incomplete versus the district's $3.58M, and the position count is an "estimate" with no breakdown.

## Open questions
- How many of the ~60 positions were teachers, and were they layoffs or attrition? Did class sizes rise?
- Did Garfield use the health care cap adjustment? A 5.0% levy suggests some cap adjustment.
- Fix our benefits measure for school-based-budget districts (add school-level benefit lines).

<!-- facts: confidence=medium; plan=SEHBP; health_increase_pct=unknown; health_cap_adjustment=unknown; banked_cap_used=unknown; positions_cut=60; teacher_positions_cut=unknown; class_size_increase=unknown; our_benefits_match=no; our_aid_match=yes -->
