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


def numbers_block(r):
    flags = []
    if r["comparable"] != "True":
        flags.append("not directly comparable (non-operating, service commission, or special services district)")
    if r["benefits_line_incomplete"] == "True":
        flags.append("audited health exceeds the budget benefits line, so some benefits are charged elsewhere and the line understates them")
    st0, st1 = r["students_per_teacher_2021_22"] or "n/a", r["students_per_teacher_2024_25"] or "n/a"
    lines = [
        "## Our numbers",
        "_Auto-generated from `data/processed/district_panel.csv` by `analysis/district_profiles.py`. Baseline is the 2025-26 "
        "**revised** budget; state aid is NJDOE K-12 formula aid (FY26 → FY27)._",
        f"- Benefits budget 2025-26 (revised) → 2026-27: {m(r['benefits_budget_2526'], False)} → {m(r['benefits_budget_2627'], False)} "
        f"({p(r['benefits_change_pct'], True)}); formula aid change: {m(r['state_aid_change_dollars'])}; "
        f"aid change minus benefit increase: {m(r['aid_change_minus_benefit_change'])}",
        f"- Benefits share of operating budget 2026-27: {p(r['benefits_share_of_gce_2627'])}; health share of district-paid "
        f"benefits (FY25 audit): {p(r['acfr_health_share_of_benefits_2025'])}; audited health growth FY23→FY25: "
        f"{p(r['acfr_health_growth_23_25_pct'], True)}",
        f"- Tax levy change: {p(r['levy_change_pct'], True)}; budgeted fund balance used 2025-26 → 2026-27: "
        f"{m(r['fund_balance_used_2526'], False)} → {m(r['fund_balance_used_2627'], False)}",
        f"- Students per teacher 2021-22 → 2024-25: {st0} → {st1}; state-paid TPAF pension/retiree medical FY25 (not in district budget): "
        f"{m(r['tpaf_onbehalf_total_2025'], False)}",
    ]
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
        index.append((path.parent.name.title(), title, did, cls, summary, path.relative_to(DIR)))

    order = {c: i for i, c in enumerate(CLASSES)}
    counts = Counter(c for *_, c, _, _ in [(x[0], x[1], x[2], x[3], x[4], x[5]) for x in index])
    out = ["# District profiles: Burlington, Camden & Gloucester",
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
    out += ["", "_Coverage caveat: the session's web-search quota ran out partway through most batches; districts researched "
            "after that point relied on district websites and state budget PDFs only (noted in each profile)._", ""]
    for county in sorted({x[0] for x in index}):
        out += [f"## {county}", "", "| District | Classification | Summary |", "|---|---|---|"]
        for _, title, did, cls, summary, rel in sorted((x for x in index if x[0] == county), key=lambda x: (order.get(x[3], 9), x[1])):
            out.append(f"| [{title}]({rel}) | {cls} | {summary.replace('|', '/')} |")
        out.append("")
    (DIR / "README.md").write_text("\n".join(out))
    print("updated", len(index), "profiles;", dict(counts))


if __name__ == "__main__":
    main()
