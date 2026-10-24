#!/usr/bin/env python3
"""Build a per-district panel joining every source we have on benefits and budgets.

Inputs (all under data/):
  raw/ufb/*/approp*.csv, rev*.csv     district budgets (benefits, operating budget, aid, levy, fund balance)
  raw/audit/NJ_TPAF_Allocations_*     state-paid teacher pension / retiree medical (on-behalf)
  processed/acfr_benefits.csv         audited benefit breakdown (health, PERS, FICA...) from ACFRs
  raw/sehbp/sehbpemp.pdf              districts in the State School Employees' Health Benefits Program
  raw/tges/*/CSG16.CSV, CSG14.CSV     students per teacher, median teacher salary, benefits % of salaries

Output: data/processed/district_panel.csv, plus a summary printed for chosen counties.

    .venv/bin/python analysis/district_panel.py --counties 05,07,15
"""
import argparse
import csv
import difflib
import glob
import re
import statistics
from pathlib import Path

import openpyxl
import pymupdf

ROOT = Path(__file__).resolve().parent.parent
RAW, PROC = ROOT / "data" / "raw", ROOT / "data" / "processed"


def num(x):
    try:
        return float(x or 0)
    except ValueError:
        return 0.0


def ufb_lines(kind, lines):
    """{district_id: {budget_year_file: {line: (a1, a2, a3)}}} for selected line numbers."""
    out, meta = {}, {}
    for f in sorted(glob.glob(str(RAW / "ufb" / "*" / f"{kind}*.csv"))):
        yr = Path(f).parent.name  # e.g. 2627 = budget year 2026-27
        with open(f, encoding="latin-1") as fh:
            for r in csv.DictReader(fh):
                ln = r["line_no"].strip()
                if ln in lines:
                    d = r["district_id"]
                    meta[d] = (r["county_id"], r["county_name"], r["district_name"].strip())
                    out.setdefault(d, {}).setdefault(yr, {})[ln] = tuple(num(r[c]) for c in ("amount_1", "amount_2", "amount_3"))
    return out, meta


def formula_aid():
    """{district_id: (fy26_k12_aid, fy27_k12_aid)} from NJDOE FY27 district details (formula aid, excl. debt service)."""
    out = {}
    ws = openpyxl.load_workbook(RAW / "stateaid" / "2627" / "FY27_GBM_District_Details.xlsx", read_only=True, data_only=True).worksheets[0]
    for row in ws.iter_rows(min_row=6, values_only=True):
        if row and isinstance(row[1], (int, float)):
            out[str(int(row[1])).zfill(4)] = (num(row[3]), num(row[12]))
    return out


def tpaf():
    """{district_id: {fy: (pension, prm, total)}} from Treasury on-behalf allocation workbooks."""
    out = {}
    for f in sorted((RAW / "audit").glob("NJ_TPAF_Allocations_LEAs_FY*.xlsx")):
        fy = re.search(r"FY(\d{4})", f.name).group(1)
        ws = openpyxl.load_workbook(f, read_only=True, data_only=True).worksheets[0]
        for row in ws.iter_rows(min_row=8, values_only=True):
            if row and row[1] and str(row[1]).strip().isdigit():
                out.setdefault(str(row[1]).zfill(4), {})[fy] = (num(row[8]), num(row[9]), num(row[11]))
    return out


def norm(name):
    n = name.upper()
    n = re.sub(r"\b(BD OF ED|BOARD OF EDUCATION|BOE|SCHOOL DISTRICT|SCH DIST|PUBLIC SCHOOLS)\b", "", n)
    for a, b in [("TOWNSHIP", "TWP"), ("BOROUGH", "BORO"), ("REGIONAL", "REG"), ("VOCATIONAL", "VOC"),
                 ("COUNTY", "CO"), ("SPECIAL SERVICES", "SPEC SERV"), ("CITY OF ", ""), ("TOWN OF ", "")]:
        n = re.sub(rf"\b{a}\b", b, n)
    return re.sub(r"[^A-Z0-9 ]", "", re.sub(r"\s+", " ", n)).strip()


# SEHBP list names that don't normalize to the UFB district name
OVERRIDES = {"TRENTON CITY": "5210", "SOUTHERN REG H S DISTRICT": "4950", "SUSSEX WANTAGE REG SCHOOL DIST": "5100"}


def sehbp(meta):
    """District ids whose board of education appears on the SEHBP participating-employer list."""
    text = "\n".join(p.get_text(sort=True) for p in pymupdf.open(RAW / "sehbp" / "sehbpemp.pdf"))
    entries = []
    for line in text.splitlines():
        m = re.match(r"^\s*(.+?)\s{2,}([A-Z ]+) COUNTY\s*$", line)
        if m and re.search(r"BD OF ED|BOARD OF EDUCATION|SCHOOL|VOC|SPEC|REGIONAL", m.group(1)) \
                and not re.search(r"CHARTER|COLLEGE|UNIVERSITY|JOINTURE|COMMISSION", m.group(1)):
            entries.append((norm(m.group(1)), m.group(2).strip().title()))
    by_county = {}
    for d, (_, cname, name) in meta.items():
        by_county.setdefault(cname.title(), {})[norm(name)] = d
    hits, unmatched = set(), []
    generic = {"TWP", "BORO", "CITY", "TOWN", "VILLAGE", "CO", "REG", "DIST", "H", "S", "SCHOOL", "SCHOOLS"}
    for n, county in entries:
        if re.search(r"CUSTODIAN|ADMINISTRAT", n):  # a single bargaining unit, not the whole district
            continue
        pool = by_county.get(county, {})
        match = OVERRIDES.get(n) or pool.get(n)
        if not match and re.search(r"\bVOC|TECHNICAL", n):
            c = [k for k in pool if re.search(r"\bVOC|TECH", k)]
            match = pool[c[0]] if len(c) == 1 else None  # ambiguous if a county has more than one
        if not match and "SPEC" in n:
            c = [k for k in pool if "SPEC" in k]
            match = pool[c[0]] if len(c) == 1 else None
        if not match:
            core = set(n.split()) - generic
            cands = [d for k, d in pool.items() if core and core == (set(k.split()) - generic)]
            match = cands[0] if len(cands) == 1 else None
        if not match:
            best = difflib.get_close_matches(n, pool.keys(), n=1, cutoff=0.8)
            match = pool[best[0]] if best else None
        if match:
            hits.add(match)
        else:
            unmatched.append(f"{n} ({county})")
    return hits, unmatched


def tges():
    """{district_id: {year: (students_per_teacher, median_teacher_salary)}}; benefits % of salaries."""
    ratios, benpct = {}, {}
    # each edition reports two years: STRAT00 = older, STRAT01 = newer
    editions = {"2023": ("2021-22", "2022-23"), "2024": ("2022-23", "2023-24"), "2025": ("2023-24", "2024-25")}
    for ed, (y0, y1) in editions.items():
        f = next(iter(glob.glob(str(RAW / "tges" / ed / "x" / "*" / "CSG16.CSV"))), None)
        if not f:
            continue
        with open(f, encoding="latin-1") as fh:
            for r in csv.DictReader(fh):
                if not r["DIST"].isdigit():
                    continue
                d = r["DIST"].zfill(4)
                for y, s, t in ((y0, "STRAT0016", "SALT0016"), (y1, "STRAT0116", "SALT0116")):
                    if num(r[s]):
                        ratios.setdefault(d, {})[y] = (num(r[s]), num(r[t]))
    f = next(iter(glob.glob(str(RAW / "tges" / "2025" / "x" / "*" / "CSG14.CSV"))), None)
    if f:
        with open(f, encoding="latin-1") as fh:
            for r in csv.DictReader(fh):
                if r["DIST"].isdigit():
                    benpct[r["DIST"].zfill(4)] = (num(r["PP114"]), num(r["PP214"]), num(r["PP314"]))
    return ratios, benpct


def acfr():
    out = {}
    p = PROC / "acfr_benefits.csv"
    if p.exists():
        with open(p) as fh:
            for r in csv.DictReader(fh):
                out.setdefault(r["district_id"], {})[r["fiscal_year"]] = r
    return out


def src(r):
    """Link to the audited report page the figure was read from (Exhibit C-1)."""
    if not r or not r.get("health"):
        return ""
    return r["source_url"] + (f"#page={r['source_page']}" if r.get("source_page") else "")


def pct(a, b):
    return (a / b - 1) * 100 if b else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counties", default="05,07,15")
    args = ap.parse_args()
    focus = set(args.counties.split(","))

    appr, meta = ufb_lines("approp", {"71260", "72260"})
    rev, _ = ufb_lines("rev", {"114", "520", "580"})
    tp = tpaf()
    faid = formula_aid()
    in_sehbp, unmatched = sehbp(meta)
    ratios, benpct = tges()
    audits = acfr()

    rows = []
    for d, (cid, cname, name) in sorted(meta.items(), key=lambda kv: kv[1]):
        a = appr.get(d, {})
        b26, b27 = a.get("2526", {}), a.get("2627", {})
        if "71260" not in b27 or "71260" not in b26 or not b26["71260"][2]:
            continue
        # Baseline = 2025-26 *revised* budget as reported in the 2026-27 UFB (amount_2), which is what
        # districts compare against; the original 2025-26 budget is kept for reference.
        ben26_orig = b26["71260"][2]
        baseline_source = "revised" if b27["71260"][1] else "original (revised missing)"
        ben26, ben27 = b27["71260"][1] or ben26_orig, b27["71260"][2]
        gce26, gce27 = b27.get("72260", (0, 0, 0))[1] or b26.get("72260", (0, 0, 0))[2], b27.get("72260", (0, 0, 0))[2]
        r27 = rev.get(d, {}).get("2627", {})
        rev_aid26, rev_aid27 = r27.get("520", (0, 0, 0))[1:]
        aid_source = "formula" if d in faid else "UFB state revenue (not in aid file)"
        aid26, aid27 = faid.get(d, (rev_aid26, rev_aid27))
        levy26, levy27 = r27.get("114", (0, 0, 0))[1:]
        fb26, fb27 = r27.get("580", (0, 0, 0))[1:]
        ratio = ratios.get(d, {})
        au = audits.get(d, {})
        def usable(r):
            """Use an audit row only if its components reconcile to the total, or health is a sane share of it."""
            if not r or not num(r.get("health")):
                return False
            if r.get("quality") == "reconciled":
                return True
            h, t = num(r.get("health")), num(r.get("total_unallocated"))
            return r.get("quality") == "unreconciled" and t > 0 and 0.2 <= h / t <= 1.0
        a23, a25 = au.get("2023"), au.get("2025")
        h23 = num(a23.get("health")) if usable(a23) else 0
        h25 = num(a25.get("health")) if usable(a25) else 0
        t25 = num(a25.get("total_unallocated")) if usable(a25) else 0
        tpaf25 = tp.get(d, {}).get("2025", (0, 0, 0))
        rows.append({
            "county_id": cid, "county": cname, "district_id": d, "district_name": name,
            "in_sehbp": d in in_sehbp,
            "baseline_source": baseline_source, "aid_source": aid_source,
            "comparable": baseline_source == "revised" and aid_source == "formula" and not (ben27 < 1e5 or re.search(r"Ed(uc)?\.? Serv|Spec(ial)?\.? Serv|Jointure|Commission|Regional Day", name, re.I)),
            "benefits_budget_2526": ben26, "benefits_budget_2627": ben27, "benefits_budget_2526_original": ben26_orig,
            "benefits_change_pct": round(pct(ben27, ben26), 1),
            "benefits_change_dollars": ben27 - ben26,
            "other_gce_change_pct": round(pct(gce27 - ben27, gce26 - ben26), 1) if gce26 else "",
            "benefits_share_of_gce_2627": round(ben27 / gce27 * 100, 1) if gce27 else "",
            "other_gce_budget_2526": gce26 - ben26, "other_gce_budget_2627": gce27 - ben27,
            "state_aid_change_dollars": aid27 - aid26,  # NJDOE K-12 formula aid FY26 -> FY27
            "state_revenue_change_ufb": rev_aid27 - rev_aid26,
            "levy_change_pct": round(pct(levy27, levy26), 1) if levy26 else "",
            "fund_balance_used_2526": fb26, "fund_balance_used_2627": fb27,
            "aid_change_minus_benefit_change": (aid27 - aid26) - (ben27 - ben26),
            "acfr_health_2023": h23 or "", "acfr_health_2025": h25 or "",
            "acfr_2023_source": src(a23) if h23 else "", "acfr_2025_source": src(a25) if h25 else "",
            # guard against a mis-parsed year: health can't plausibly move >150% in two years
            "acfr_health_growth_23_25_pct": round(pct(h25, h23), 1) if h23 > 1e4 and h25 and abs(pct(h25, h23)) <= 150 else "",
            "acfr_health_share_of_benefits_2025": round(h25 / t25 * 100, 1) if h25 and t25 and 0.2 <= h25 / t25 <= 1.0 else "",
            "acfr_quality_2023": (a23 or {}).get("quality", ""), "acfr_quality_2025": (a25 or {}).get("quality", ""),
            "tpaf_onbehalf_total_2025": tpaf25[2] or "",
            "benefits_line_incomplete": bool(h25 and h25 > 1.05 * ben27),
            "students_per_teacher_2021_22": ratio.get("2021-22", ("",))[0],
            "students_per_teacher_2024_25": ratio.get("2024-25", ("",))[0],
            "median_teacher_salary_2024_25": ratio.get("2024-25", ("", ""))[1],
            "benefits_pct_of_salaries_fy23_fy24_fy25b": "/".join(str(x) for x in benpct.get(d, ())),
        })

    out = PROC / "district_panel.csv"
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out.relative_to(ROOT)} ({len(rows)} districts); SEHBP matched {len(in_sehbp)}, unmatched {len(unmatched)}")
    if unmatched:
        print("  unmatched SEHBP entries:", "; ".join(unmatched[:40]))

    def summarize(label, rs):
        if not rs:
            return
        b26 = sum(r["benefits_budget_2526"] for r in rs)
        b27 = sum(r["benefits_budget_2627"] for r in rs)
        aid = sum(r["state_aid_change_dollars"] for r in rs)
        hs = [r["acfr_health_share_of_benefits_2025"] for r in rs if r["acfr_health_share_of_benefits_2025"] != ""]
        hg = [r["acfr_health_growth_23_25_pct"] for r in rs if r["acfr_health_growth_23_25_pct"] != ""]
        neg = sum(1 for r in rs if r["aid_change_minus_benefit_change"] < 0)
        print(f"\n{label}: {len(rs)} districts ({sum(r['in_sehbp'] for r in rs)} in SEHBP)")
        print(f"  benefits budget  {b26/1e6:8.1f}M -> {b27/1e6:8.1f}M  (+{(b27-b26)/1e6:.1f}M, {pct(b27,b26):+.1f}%)")
        print(f"  state aid change {aid/1e6:+8.1f}M   -> benefit increase exceeds aid increase in {neg} of {len(rs)} districts")
        print(f"  median benefits share of operating budget: {statistics.median(r['benefits_share_of_gce_2627'] for r in rs if r['benefits_share_of_gce_2627'] != ''):.1f}%")
        if hs:
            print(f"  audited FY25: health = median {statistics.median(hs):.0f}% of district-paid benefits (n={len(hs)})")
        if hg:
            print(f"  audited health cost growth FY23->FY25: median {statistics.median(hg):+.1f}% (n={len(hg)})")
        for grp, flag in (("SEHBP", True), ("private/other plans", False)):
            g = [r["benefits_change_pct"] for r in rs if r["in_sehbp"] == flag]
            if g:
                print(f"    {grp:20} benefits budget growth median {statistics.median(g):+.1f}% (n={len(g)})")

    summarize("STATEWIDE", rows)
    for c in sorted(focus):
        summarize(next((r["county"] for r in rows if r["county_id"] == c), c), [r for r in rows if r["county_id"] == c])


if __name__ == "__main__":
    main()
