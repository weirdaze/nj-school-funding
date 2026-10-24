#!/usr/bin/env python3
"""Refresh the "## Our numbers" block in each research/districts/*/*.md from district_panel.csv,
and write research/districts/README.md: an index of every profile with its classification.

    .venv/bin/python analysis/district_profiles.py
"""
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "research" / "districts"
CLASSES = ["Confirmed", "Consistent", "No cuts reported", "Insufficient evidence"]


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def m(x, sign=True):
    x = f(x)
    if x is None:
        return "n/a"
    return f"{('+' if x >= 0 else '-') if sign else ''}${abs(x)/1e6:.2f}M"


def p(x, sign=False):
    x = f(x)
    return "n/a" if x is None else (f"{x:+.1f}%" if sign else f"{x:.1f}%")


UFB_PDF = "https://www.nj.gov/education/budget/ufb/2627/reports/{cc}/UFB27_{d}.pdf"
UFB_CSV = "https://www.nj.gov/education/budget/ufb/2627/index.shtml"
AID = "https://www.nj.gov/education/stateaid/2627/FY27_GBM_District_Details.xlsx"
TPAF = "https://www.nj.gov/education/fpp/audit/2425/docs/NJ_TPAF_Allocations_LEAs_FY2025.xlsx"
TGES = "https://www.nj.gov/education/guide/2025tges.shtml"
TGES23 = "https://www.nj.gov/education/guide/"
SEHBP = "https://www.nj.gov/treasury/pensions/documents/pdf/sehbpemp.pdf"


def numbers_block(r):
    flags = []
    if r["comparable"] != "True":
        flags.append("not directly comparable (non-operating, service commission, or special services district)")
    if r["benefits_line_incomplete"] == "True" and r.get("former_abbott") != "True":
        flags.append("audited health exceeds the budget benefits line, so some benefits are charged elsewhere and the line understates them")
    ufb = UFB_PDF.format(cc=r["county_id"], d=r["district_id"])
    a23, a25 = r.get("acfr_2023_source", ""), r.get("acfr_2025_source", "")
    st0, st1 = r["students_per_teacher_2021_22"] or "n/a", r["students_per_teacher_2024_25"] or "n/a"
    lines = [
        "## Our numbers",
        "_Auto-generated from `data/processed/district_panel.csv` by `analysis/district_profiles.py`; every figure links to "
        "its public source. Baseline is the 2025-26 **revised** budget; state aid is NJDOE K-12 formula aid (FY26 → FY27)._",
        f"- **Benefits budget** 2025-26 (revised) → 2026-27: {m(r['benefits_budget_2526'], False)} → {m(r['benefits_budget_2627'], False)} "
        f"({p(r['benefits_change_pct'], True)}). Source: [2026-27 User-Friendly Budget]({ufb}), Appropriations, line "
        f"\"Total Personal Services – Employee Benefits\" (columns 2025-26 revised / 2026-27 budget); also [UFB data files]({UFB_CSV}) `approp27.csv` line 71260.",
        f"- **Formula aid change** FY26 → FY27: {m(r['state_aid_change_dollars'])}. Source: [NJDOE FY27 K-12 aid, district details]({AID}) "
        f"(row for district {r['district_id']}, \"FY26–FY27 K–12 Aid Difference\"). Aid change minus benefit increase: {m(r['aid_change_minus_benefit_change'])} (computed).",
        f"- **Benefits share of operating budget** 2026-27: {p(r['benefits_share_of_gce_2627'])} (computed from [UFB]({ufb}): employee benefits ÷ Total General Current Expense).",
        f"- **Health share of district-paid benefits** FY25: {p(r['acfr_health_share_of_benefits_2025'])}; **audited health growth** FY23→FY25: "
        f"{p(r['acfr_health_growth_23_25_pct'], True)}. Source: audited ACFR Exhibit C-1, \"Health Benefits\" actual"
        + (f": [FY2025 report]({a25})" if a25 else "") + (f", [FY2023 report]({a23})" if a23 else "")
        + ("" if (a23 or a25) else " (not extracted for this district)") + ".",
        f"- **Tax levy change**: {p(r['levy_change_pct'], True)}; **budgeted fund balance used** 2025-26 → 2026-27: "
        f"{m(r['fund_balance_used_2526'], False)} → {m(r['fund_balance_used_2627'], False)}. Source: [UFB]({ufb}), Revenues, "
        f"lines \"Total Tax Levy\" and \"Budgeted Fund Balance-Operating Budget\".",
        f"- **Students per teacher (TGES ratio)** 2021-22 → 2024-25: {st0} → {st1}. Source: [Taxpayers' Guide to Education Spending]({TGES}) "
        f"Indicator 16, file `CSG16.CSV` column `STRAT` (2025 edition for 2024-25; [2023 edition]({TGES23}) for 2021-22). "
        f"This divides students by all teaching staff, so it is roughly half of typical class size and is **not a class-size measure**; "
        f"the 2024-25 value is the latest edition's newer column, which later editions usually confirm but which is not yet final.",
        f"- **State-paid teacher pension/retiree medical** FY25 (not in the district budget): {m(r['tpaf_onbehalf_total_2025'], False)}. "
        f"Source: [Treasury TPAF on-behalf allocations FY2025]({TPAF}).",
        f"- **In SEHBP**: {'yes' if r['in_sehbp'] == 'True' else 'no'} per the [October 2026 participating-employer list]({SEHBP}) (name-matched).",
    ]
    o, rv, b27 = f(r.get("benefits_budget_2526_original")), f(r["benefits_budget_2526"]), f(r["benefits_budget_2627"])
    if o and rv and abs(rv / o - 1) > 0.10:
        flags.append(f"the 2025-26 benefits budget was revised {(rv / o - 1) * 100:+.0f}% mid-year (${o/1e6:.2f}M original → "
                     f"${rv/1e6:.2f}M revised); measured from the original budget the 2026-27 change is {(b27 / o - 1) * 100:+.1f}%")
    if r.get("former_abbott") == "True":
        flags.append("former Abbott district: may budget by school, so the general-fund benefits line can be partial")
    if flags:
        lines.append("- ⚠️ " + "; ".join(flags))
    return "\n".join(lines) + "\n\n"


def main():
    panel = {r["district_id"]: r for r in csv.DictReader(open(ROOT / "data" / "processed" / "district_panel.csv"))}
    index = []
    for path in sorted(DIR.glob("*/*.md")):
        text = path.read_text()
        did = path.name.split("-")[0]
        r = panel.get(did)
        if r:
            text = re.sub(r"## Our numbers\n.*?(?=\n## )", numbers_block(r).rstrip("\n") + "\n", text, flags=re.S)
            path.write_text(text)
        assess = text.split("## Assessment", 1)[1] if "## Assessment" in text else ""
        cls = next((c for c in CLASSES if f"**{c}" in assess), "Unclassified")
        summary = re.sub(r"\s+", " ", re.sub(r"\*\*[^*]+\*\*[.:]?", "", assess.split("## ")[0])).strip()
        summary = re.sub(r"^(\([^)]*\)[.:]?\s*)+", "", summary)
        summary = re.split(r"(?<=[.!?])\s(?=[A-Z])", summary)[0][:240]
        title = text.splitlines()[0].lstrip("# ").split(" (")[0]
        conf_m = re.search(r"## Confidence\s*\n\s*\**(High|Medium|Low)", text, re.I) or re.search(r"confidence=(high|medium|low)", text, re.I)
        conf = conf_m.group(1).title() if conf_m else "Not yet rated"
        index.append((path.parent.name.replace("-", " ").title(), title, did, cls, summary, path.relative_to(DIR), conf))

    order = {c: i for i, c in enumerate(CLASSES)}
    counts = Counter(x[3] for x in index)
    confs = Counter(x[6] for x in index)
    out = ["# District profiles",
           "",
           "Each profile tests the claim *\"rising benefit costs are forcing cuts, layoffs and larger class sizes\"* against "
           "district budget presentations, board minutes and local news (researched 2026-10-24), alongside our computed numbers.",
           "",
           "**Classification key:** **Confirmed**: the district explicitly ties cuts to benefit/health costs. "
           "**Consistent**: cuts happened and benefits are one stated factor. **No cuts reported**: the district absorbed "
           "the increase (usually via the levy cap's health-care adjustment, state aid, or reserves). **Insufficient "
           "evidence**: no usable public documents found.",
           "",
           "| | " + " | ".join(CLASSES) + " |", "|---|" + "---|" * len(CLASSES)]
    for county in sorted({x[0] for x in index}):
        c = Counter(x[3] for x in index if x[0] == county)
        out.append(f"| {county} | " + " | ".join(str(c[k]) for k in CLASSES) + " |")
    out.append("| **Total** | " + " | ".join(f"**{counts[k]}**" for k in CLASSES) + " |")
    out += ["", "**Confidence** (is the profile's evidence solid enough to quote publicly?): " + ", ".join(f"{k}: {v}" for k, v in sorted(confs.items())) + ". "
            "High = key claims verified in the district's own documents and our numbers reconcile; Medium = credible news or "
            "partial documents; Low = snippets/unverified. Only quote High-confidence profiles as fact.", ""]
    out += ["", "_Coverage caveat: the session's web-search quota ran out partway through most batches; districts researched "
            "after that point relied on district websites and state budget PDFs only (noted in each profile)._", ""]
    for county in sorted({x[0] for x in index}):
        out += [f"## {county}", "", "| District | Classification | Confidence | Summary |", "|---|---|---|---|"]
        for _, title, did, cls, summary, rel, conf in sorted((x for x in index if x[0] == county), key=lambda x: (order.get(x[3], 9), x[1])):
            out.append(f"| [{title}]({rel}) | {cls} | {conf} | {summary.replace('|', '/')} |")
        out.append("")
    # Evidence summary from the machine-readable facts lines
    facts = {}
    for x in index:
        t = (DIR / x[5]).read_text()
        m_ = re.search(r"<!-- facts: (.*?) -->", t, re.S)
        if m_:
            facts[x[2]] = dict(kv.split("=", 1) for kv in [k.strip() for k in m_.group(1).split(";")] if "=" in kv)
    def num_(v):
        try:
            return float(str(v).replace(",", "").replace("$", ""))
        except ValueError:
            return None
    strong = [x for x in index if x[3] in ("Confirmed", "Consistent") and x[6] in ("High", "Medium")]
    adj = [(x, num_(facts.get(x[2], {}).get("health_cap_adjustment"))) for x in index]
    adj = [(x, v) for x, v in adj if v]
    out += ["## Evidence summary (High/Medium-confidence profiles only)", "",
            "Districts that cut positions or programs with benefits/health costs as a stated cause. **Only these should be cited as examples.**", "",
            "| District | County | Classification | Confidence | Positions cut | Teacher positions cut | Larger classes |", "|---|---|---|---|---|---|---|"]
    for x in sorted(strong, key=lambda x: (order[x[3]], {"High": 0, "Medium": 1}[x[6]], x[0], x[1])):
        fx = facts.get(x[2], {})
        out.append(f"| [{x[1]}]({x[5]}) | {x[0]} | {x[3]} | {x[6]} | {fx.get('positions_cut', 'unknown')} | "
                   f"{fx.get('teacher_positions_cut', 'unknown')} | {fx.get('class_size_increase', 'unknown')} |")
    determined = sum(1 for x in index if facts.get(x[2], {}).get("health_cap_adjustment", "unknown") not in ("unknown", ""))
    out += ["", f"**Health-care cost cap adjustments documented**: {len(adj)} of the {determined} profiled districts where it could be "
            f"determined used one (the other {len(index) - determined} profiles have no public document that says either way; "
            f"\"unknown\" means not found, not \"not used\"). The documented amounts sum to ${sum(v for _, v in adj)/1e6:,.1f}M. "
            "This is a sum of figures from different stages, not an audited total: some come from adopted resolutions or hearing decks, some "
            "from tentative or preliminary presentations, and some are rounded figures from news reports; each profile says which. "
            "The adjustment lets a district raise the levy above 2% for health costs. Because the profiled districts over-sample large "
            "benefit increases, this does not show how districts statewide absorbed the increase.", ""]
    (DIR / "README.md").write_text("\n".join(out))
    print("updated", len(index), "profiles;", dict(counts))


if __name__ == "__main__":
    main()
