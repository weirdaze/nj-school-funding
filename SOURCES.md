# Data Sources: NJ School Funding, Tax Dollar to District

Each source is listed under the stage of the money flow where it applies. Every URL was checked on **2026-10-24**. NJ state sites move pages often, so re-check them before citing.

Legend: 📊 machine-readable (CSV/XLSX), 📄 PDF only, 🔗 index page

---

## Stage 1: Taxes are collected

### State taxes (mainly the Gross Income Tax)
| Source | What it gives you | Link |
|---|---|---|
| NJ Constitution, Art. VIII §1 ¶7 | Dedicates **all income tax revenue** to the **Property Tax Relief Fund (PTRF)**, which must be spent on reducing or offsetting property taxes. School aid is the largest use. | (cite text; see Budget Detail glossary) |
| OMB: Budget publications hub 🔗 | Index of every budget document, including archives back to the 1980s | https://www.nj.gov/treasury/omb/ |
| FY2027 Revenue Certification 📄 | Certified revenue estimates, including GIT and Sales Tax | https://www.nj.gov/treasury/omb/publications/27budget/RevCert-FY27.pdf |
| FY2027 Budget in Brief 📄 | Plain-language summary of the proposed budget | https://www.nj.gov/treasury/omb/publications/27bib/BIB.pdf |

### Local property taxes
| Source | What it gives you | Link |
|---|---|---|
| Div. of Taxation: Local Property Tax statistics 🔗 | State Equalization Tables, General Tax Rates, average residential tax, MOD-IV assessment files | https://www.nj.gov/treasury/taxation/lpt/statdata.shtml |
| General Tax Rates by municipality 📄 | Tax rate per $100 of assessed value, one file per year (2015–2025) | https://www.nj.gov/treasury/taxation/pdf/lpt/gtr/2025taxrates.pdf |
| State Equalization Table 📄 | Equalized (true market) valuation per municipality, which feeds the SFRA "local fair share" calculation | https://www.nj.gov/treasury/taxation/pdf/lpt/2026StateEq.pdf |
| Average residential tax 📄 | Average Class 2 assessment and tax by town | https://www.nj.gov/treasury/taxation/pdf/lpt/class4/2026AvgResStat.pdf |
| DCA / DLGS: Property Tax Information 📊 | **Abstract of Ratables** (`YYabstract.xls`) splits each town's levy into **school, municipal, and county** portions. Also `YYtaxes.xls` and `YYlirateables.xls`. Years 2012–2025. | https://www.nj.gov/dca/dlgs/resources/Property_Tax_info.shtml |
| e.g. 2025 Abstract of Ratables 📊 | | https://www.nj.gov/dca/dlgs/resources/Property_Tax/25_data/25abstract.xls |

---

## Stage 2: The state budgets for and appropriates school aid
| Source | What it gives you | Link |
|---|---|---|
| FY2027 Budget Detail (full) 📄 | Line-item appropriations, including the Dept. of Education's PTRF school aid lines | https://www.nj.gov/treasury/omb/publications/27budget/FY%202027%20Budget%20Detail%20-%20Full.pdf |
| FY2027 Appropriations Handbook (enacted) 📄 | The **enacted** appropriations act, which is what actually passed | https://www.nj.gov/treasury/omb/publications/27approp/FY2027AppropriationsHandbook-Full.pdf |
| OLS: Analysis of DOE budget FY2027 📄 | Office of Legislative Services analysis of the DOE budget. Explains the aid formula changes, including the FY26+ caps (increases capped at 6%, decreases at 3%) | https://pub.njleg.state.nj.us/publications/budget/governors-budget/2027/doe_analysis_2027.pdf |
| NJ Comprehensive Annual Financial Report (ACFR) 📄 | Actual (audited) state spending, which may differ from what was appropriated | https://www.nj.gov/treasury/omb/publications/25fr/NJFY2025Complete.pdf |
| YourMoney.NJ.gov 📊 | State transparency portal with actual spending and payments | https://www.yourmoney.nj.gov/ |

---

## Stage 3: The state formula allocates aid to districts (SFRA)
The School Funding Reform Act of 2008 (P.L.2007, c.260, N.J.S.A. 18A:7F-43 et seq.) works like this: **Adequacy Budget − Local Fair Share = Equalization Aid**. Categorical aid (special ed, transportation, security, etc.) is added on top. S2 (P.L.2018, c.67) phased out adjustment aid.

| Source | What it gives you | Link |
|---|---|---|
| NJDOE: State Aid Summaries 🔗 | Hub page with per-district aid for every year since 1997-98 | https://www.nj.gov/education/stateaid/ |
| FY27 District Details 📊 | Aid by category for every district, with the change from FY26 | https://www.nj.gov/education/stateaid/2627/FY27_GBM_District_Details.xlsx |
| FY27 County Summary 📊 | | https://www.nj.gov/education/stateaid/2627/FY27_GBM_County_Summary.xlsx |
| FY27 Preschool Aid 📊 | | https://www.nj.gov/education/stateaid/2627/FY27_GBM_Preschool_Aid.xlsx |
| Historical aid (zipped, 1997-98 → 2025-26) 📊 | One zip per year, e.g. `2526.zip` | https://www.nj.gov/education/stateaid/zippedfiles/2526.zip |
| Educational Adequacy Report (EAR) FY2026 📄📊 | The triennial report that sets SFRA cost parameters (base per-pupil amount, weights) | https://www.nj.gov/education/stateaid/docs/ear/EAR2026.pdf · [Appendix B xlsx](https://www.nj.gov/education/stateaid/docs/ear/EAR_FY2026_AppendixB.xlsx) |
| FY2026 School Funding Report (Res. 1378) 📄 | | https://www.nj.gov/education/stateaid/docs/FY2026%20Resolution%201378_School%20Funding%20Report_Final_12.1.2025_AE.pdf |
| District Factor Groups 🔗 | Socioeconomic groupings of districts, useful for comparisons | https://www.nj.gov/education/stateaid/dfg.shtml |
| NJDOE School Funding Modernization Project 📄 | The current formula review and its learning series | https://www.nj.gov/education/schoolfinance/schoolfunding/ |

---

## Stage 4: The district budgets (revenue = state aid + local levy + federal + other)
| Source | What it gives you | Link |
|---|---|---|
| **User-Friendly Budget (UFB) data** 📊 | **The key file.** CSVs for every district: `rev27.csv` (revenues, **including the local tax levy**), `approp27.csv` (appropriations), `esttax27.csv` (estimated tax rate impact), `recap27.csv`, `pupcst27.csv`, `enroll27.csv`, `employees27.csv`, `shared27.csv`, `unusual27.csv`. Field layout is in `userfr_layout.xlsx`. Years 2020-21 → 2026-27 (the 2024-25 files are named `*25_minus_1.csv`). | https://www.nj.gov/education/budget/ufb/2627/index.shtml |
| District budget hub 🔗 | Budget guidance and per-pupil costs | https://www.nj.gov/education/budget/ |

---

## Stage 5: What districts actually spent
| Source | What it gives you | Link |
|---|---|---|
| **Taxpayers' Guide to Education Spending (TGES) 2025** 📊 | Per-pupil spending broken into 21 indicators (CSG1–CSG21), compared within peer groups. Covers actual FY24 and budgeted FY25. Full zip available. | https://www.nj.gov/education/guide/2025tges.shtml |
| TGES archive (2011–2023 zips) 📊 | | https://www.nj.gov/education/guide/ |
| District audits / ACFRs 🔗 | Audited financial statements for each district | https://www.nj.gov/education/fpp/audit/index.shtml · https://www.nj.gov/education/fpp/acfr/ |
| Audit summary data 📊 | Statewide audit summary data | https://www.nj.gov/education/fpp/audit/audsum/index.shtml |
| NJ School Performance Reports 🔗 | Outcomes, enrollment, and per-pupil figures for each school and district. Probably behind a bot wall, so download by hand. | https://rc.doe.state.nj.us/ |

---

## Cross-checks and federal context
| Source | What it gives you | Link |
|---|---|---|
| Census Annual Survey of School System Finances (F-33) 📊 | A nationally comparable revenue source split (federal/state/local) for every NJ district. FY2024 was released May 2026. | https://www.census.gov/programs-surveys/school-finances.html |
| NJSBA: Understanding NJ State Aid 📄 | Readable explainer of the SFRA mechanics | https://www.njsba.org/school-leader/school-leader-summer-2024/understanding-new-jersey-school-state-aid-funding/ |
| Education Law Center: NJ School Funding 🔗 | Advocacy analysis of adequacy gaps. Cite it as analysis, not official data. | https://edlawcenter.org/ |

---

## Known gaps / TODO
- [ ] Find the FY27 **enacted** aid file. The `GBM` files are the Governor's Budget Message (proposed) numbers. Compare them against the 2627 zip once NJDOE posts it.
- [ ] Find a machine-readable GIT and PTRF revenue time series. OMB only publishes it in PDFs, so it may have to be extracted from the Budget Detail.
- [ ] Map **municipality → school district**, which is many-to-many for regional districts. The DLGS abstract lists school levy per *town*, while UFB is per *district*.
- [ ] Track property tax relief programs (ANCHOR, Stay NJ, Senior Freeze), which are paid from the PTRF but not to schools.
