#!/usr/bin/env python3
"""Write a markdown findings page from data/processed/district_panel.csv.

    .venv/bin/python analysis/report_counties.py --counties 05,07,15 --out docs/findings/south-jersey-benefits.md
    .venv/bin/python analysis/report_counties.py --counties all --out docs/findings/statewide-benefits.md
"""
import argparse
import csv
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PANEL = ROOT / "data" / "processed" / "district_panel.csv"


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def money(x):
    x = f(x)
    if x is None:
        return "–"
    return f"{'-' if x < 0 else '+'}${abs(x)/1e6:.1f}M"


def med(vals):
    vals = [v for v in vals if v is not None]
    return statistics.median(vals) if vals else None


def fmt(v, suffix="%", nd=1):
    return "–" if v is None else f"{v:.{nd}f}{suffix}"


def summary_row(label, rs):
    b26 = sum(f(r["benefits_budget_2526"]) for r in rs)
    b27 = sum(f(r["benefits_budget_2627"]) for r in rs)
    aid = sum(f(r["state_aid_change_dollars"]) for r in rs)
    squeezed = sum(1 for r in rs if f(r["aid_change_minus_benefit_change"]) < 0)
    hs = med(f(r["acfr_health_share_of_benefits_2025"]) for r in rs)
    hg = med(f(r["acfr_health_growth_23_25_pct"]) for r in rs)
    n_hs = sum(1 for r in rs if f(r["acfr_health_share_of_benefits_2025"]) is not None)
    n_hg = sum(1 for r in rs if f(r["acfr_health_growth_23_25_pct"]) is not None)
    st = [(f(r["students_per_teacher_2021_22"]), f(r["students_per_teacher_2024_25"])) for r in rs]
    st = [(a, b) for a, b in st if a and b]
    up = sum(1 for a, b in st if b > a + 0.2)
    return (f"| {label} | {len(rs)} | {sum(r['in_sehbp'] == 'True' for r in rs)} | ${b26/1e6:,.0f}M → ${b27/1e6:,.0f}M "
            f"({(b27/b26-1)*100:+.1f}%) | {money(b27-b26)} | {money(aid)} | {squeezed} of {len(rs)} | {fmt(hs, '%', 0)} (n={n_hs}) | "
            f"{'–' if hg is None else f'{hg:+.0f}%'} (n={n_hg}) | {up} of {len(st)} |")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counties", default="05,07,15")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(PANEL)))
    sel = rows if a.counties == "all" else [r for r in rows if r["county_id"] in a.counties.split(",")]
    counties = sorted({(r["county_id"], r["county"]) for r in sel})

    L = []
    L.append("| Area | Districts | In SEHBP | Benefits budget 2025-26 → 2026-27 | Benefit increase | State aid change | Benefit increase > aid increase | Health share of district benefits (FY25 audits, median) | Health cost growth FY23→FY25 (median) | Districts with more students per teacher, 2021-22 → 2024-25 |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    L.append(summary_row("**Statewide**", rows))
    if a.counties != "all":
        L.append(summary_row("**Selected counties**", sel))
    for cid, cname in counties:
        L.append(summary_row(cname, [r for r in sel if r["county_id"] == cid]))

    L.append("\n### SEHBP vs. other health plans (median budgeted benefit growth, 2025-26 → 2026-27)\n")
    L.append("| Area | SEHBP districts | Other plans |")
    L.append("|---|---|---|")
    for label, rs in [("Statewide", rows)] + ([("Selected counties", sel)] if a.counties != "all" else []):
        s = med(f(r["benefits_change_pct"]) for r in rs if r["in_sehbp"] == "True")
        o = med(f(r["benefits_change_pct"]) for r in rs if r["in_sehbp"] != "True")
        L.append(f"| {label} | {fmt(s)} (n={sum(r['in_sehbp']=='True' for r in rs)}) | {fmt(o)} (n={sum(r['in_sehbp']!='True' for r in rs)}) |")

    for cid, cname in counties:
        rs = sorted((r for r in sel if r["county_id"] == cid), key=lambda r: f(r["aid_change_minus_benefit_change"]))
        L.append(f"\n### {cname} County\n")
        L.append("Sorted by how far the benefit increase outran the state aid change (most squeezed first).\n")
        L.append("| District | SEHBP | Benefits 25-26 → 26-27 | Benefit increase | State aid change | Aid change − benefit increase | Benefits % of operating budget | Health % of benefits (FY25) | Health growth FY23→25 | Students per teacher 21-22 → 24-25 | Surplus used 25-26 → 26-27 |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in rs:
            st0, st1 = f(r["students_per_teacher_2021_22"]), f(r["students_per_teacher_2024_25"])
            hg = f(r["acfr_health_growth_23_25_pct"])
            L.append(
                f"| {r['district_name']} | {'✓' if r['in_sehbp'] == 'True' else ''} | {fmt(f(r['benefits_change_pct']))} | "
                f"{money(r['benefits_change_dollars'])} | {money(r['state_aid_change_dollars'])} | {money(r['aid_change_minus_benefit_change'])} | "
                f"{fmt(f(r['benefits_share_of_gce_2627']))} | {fmt(f(r['acfr_health_share_of_benefits_2025']), '%', 0)} | "
                f"{'–' if hg is None else f'{hg:+.0f}%'} | {fmt(st0, '', 1)} → {fmt(st1, '', 1)} | "
                f"{money(r['fund_balance_used_2526'])[1:] if f(r['fund_balance_used_2526']) else '–'} → {money(r['fund_balance_used_2627'])[1:] if f(r['fund_balance_used_2627']) else '–'} |")
    out = ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    marker = "<!-- generated tables below -->"
    head = out.read_text().split(marker)[0] if out.exists() and marker in out.read_text() else f"# Benefits squeeze by district\n\n_Generated by `analysis/report_counties.py`. Add commentary above the marker; tables below are regenerated._\n\n"
    out.write_text(head + marker + "\n\n" + "\n".join(L) + "\n")
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
