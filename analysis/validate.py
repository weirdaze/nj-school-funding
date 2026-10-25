#!/usr/bin/env python3
"""Validate the assumptions behind district_panel.csv and write docs/validation.md.

Checks
  V1  Provenance: our UFB numbers appear verbatim in the state's per-district UFB PDF (random sample).
  V2  Audit vs budget: ACFR FY25 "Total Unallocated Benefits" vs UFB FY25 actual (line 71260, 2024-25 actual).
  V3  Baseline: revised vs original 2025-26 benefits budget.
  V4  Outliers: implausible benefit changes.
  V5  Aid definition: formula aid change vs UFB total state revenue change.
  V6  SEHBP membership: Oct 2026 list vs what each district's own FY25 audit says about its health plan.
  V7  Levy: is the above-2% levy growth consistent with a health-care cap adjustment (≤ benefit increase)?

    .venv/bin/python analysis/validate.py [--sample 25]
"""
import argparse
import csv
import random
import re
import statistics
import tempfile
import time
import urllib.request
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
PANEL = ROOT / "data" / "processed" / "district_panel.csv"
ACFR = ROOT / "data" / "processed" / "acfr_benefits.csv"
TEXT = ROOT / "data" / "raw" / "acfr_text"
# V6: auditor template sentence (FY25 audits containing it), and manual review of the remaining conflicts
TEMPLATE = {"0460", "0510", "1465", "1800", "1990", "2090", "2140", "3100", "4490", "4530"}
SEHBP_SERIES = {  # Wayback captures of sehbpemp.pdf: (matched, of which comparable); Oct 2026 is the live list
    "2021-11": (243, 229), "2022-09": (258, 243), "2022-12": (249, 235), "2023-06": (243, 229), "2023-12": (238, 224),
    "2024-07": (227, 213), "2024-09": (225, 211), "2024-12": (214, 201), "2025-03": (212, 199), "2025-09": (210, 197),
    "2026-10": (157, 144)}
V6_NOTES = {
    "2900": "resolved for the list; note 14: \"Effective January 1, 2025, the District has health benefits coverage for its employees "
            "under Horizon Blue Cross Blue Shield of New Jersey. Prior to that … State of New Jersey\" (on the archived 2021-2024 lists, off from Mar 2025)",
    "5110": "resolved for the list; the self-insured plan ended December 31, 2023 and the SHIF hit is property/casualty JIF text",
    "3100": "resolved for the list; UFB 2026-27 shared-services page: \"a member of the School Health Insurance Fund (SHIF)\"; audit has the template sentence",
    "1990": "resolved for the list; UFB 2026-27 shared-services page: \"Medical insurance with School Health Insurance Fund\"; audit has the template sentence",
    "4490": "only the template sentence; on the archived 2021-22 lists, not on 2025-26",
    "2770": "unresolved; the audit says the District transitioned to the State Health Benefits program (no date given) and, during FY25, "
            "dissolved its self-insurance fund; it is on the archived lists Sep 2022 – Dec 2023 and off every list from Jul 2024, "
            "(not a matcher miss: the name is absent from the raw text). Either the audit describes the earlier membership and a late "
            "fund wind-down, or the district is still a member and the lists omit it; nothing here tells which",
    "2180": "consistent with the Sep 2025 list (on it), so likely left after FY25",
    "5030": "consistent with the Sep 2025 list (on it), so likely left after FY25",
    "3670": "unresolved; audit says \"through the State Health Benefits Plan\"; on none of the archived 2021-2026 lists",
}
UFB = ROOT / "data" / "raw" / "ufb" / "2627" / "approp27.csv"
UFB_PDF = "https://www.nj.gov/education/budget/ufb/2627/reports/{cc}/UFB27_{d}.pdf"


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def fmt_int(x):
    return f"{int(round(x)):,}"


def v1_provenance(rows, n):
    random.seed(20261024)
    sample = random.sample([r for r in rows if r["comparable"] == "True"], n)
    ok, results = 0, []
    for r in sample:
        url = UFB_PDF.format(cc=r["county_id"], d=r["district_id"])
        try:
            with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (nj-school-funding research)"})
                tmp.write(urllib.request.urlopen(req, timeout=60).read())
                tmp.flush()
                text = re.sub(r"\s+", " ", " ".join(p.get_text() for p in pymupdf.open(tmp.name)))
        except Exception as e:
            results.append((r, url, f"fetch failed: {e}"))
            continue
        want = {"benefits 2025-26 revised": f(r["benefits_budget_2526"]), "benefits 2026-27": f(r["benefits_budget_2627"])}
        missing = [k for k, v in want.items() if v and fmt_int(v) not in text]
        ok += not missing
        results.append((r, url, "all found" if not missing else "not found: " + ", ".join(missing)))
        time.sleep(1)
    return ok, results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=25)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(PANEL)))
    comp = [r for r in rows if r["comparable"] == "True"]
    acfr25 = {r["district_id"]: r for r in csv.DictReader(open(ACFR)) if r["fiscal_year"] == "2025"}
    ufb_actual = {}
    with open(UFB, encoding="latin-1") as fh:
        for r in csv.DictReader(fh):
            if r["line_no"].strip() == "71260":
                ufb_actual[r["district_id"]] = f(r["amount_1"])
    L = ["# Validation of the district data",
         "",
         "_Generated by `analysis/validate.py`. Each check tests an assumption the findings rely on; the confidence notes "
         "say what that means for using the numbers publicly._",
         ""]

    # V1
    ok, res = v1_provenance(rows, a.sample) if a.sample else (0, [])
    L += [f"## V1. Provenance: do our numbers appear in the state's published PDFs?",
          f"Random sample of {len(res)} comparable districts; for each, the 2025-26 revised and 2026-27 benefits figures we "
          f"use were searched for verbatim in the district's [2026-27 User-Friendly Budget PDF](https://www.nj.gov/education/budget/ufb/2627/index.shtml).",
          f"",
          f"**Result: {ok} of {len(res)} matched exactly.**", "",
          "| District | PDF | Result |", "|---|---|---|"]
    L += [f"| {r['district_name']} ({r['county']}) | [UFB27_{r['district_id']}]({u}) | {msg} |" for r, u, msg in res]

    # V2
    pairs = []
    for r in comp:
        a25, u = acfr25.get(r["district_id"]), ufb_actual.get(r["district_id"])
        if a25 and f(a25["total_unallocated"]) and u:
            pairs.append((r, f(a25["total_unallocated"]) / u - 1, a25))
    within = sum(1 for _, d, _ in pairs if abs(d) <= 0.02)
    off = sorted(pairs, key=lambda x: -abs(x[1]))
    L += ["", "## V2. Audited benefits vs. budget-file actuals (FY2024-25)",
          "The UFB's \"2024-25 actual\" employee-benefits line should equal the audited ACFR \"Total Unallocated Benefits\" "
          "for the same year (when a district budgets benefits in that line).", "",
          f"**Result: {within} of {len(pairs)} districts agree within 2%** "
          f"(median absolute difference {statistics.median(abs(d) for _, d, _ in pairs)*100:.2f}%). "
          f"Differences mean either a parsing problem or that the district charges benefits outside the unallocated line "
          f"(flagged `benefits_line_incomplete`).", "",
          "Largest differences (check before quoting these districts):", "",
          "| District | ACFR FY25 total | UFB FY25 actual | Difference | Source |", "|---|---|---|---|---|"]
    for r, d, a25 in off[:20]:
        L.append(f"| {r['district_name']} ({r['county']}) | ${f(a25['total_unallocated'])/1e6:.2f}M | "
                 f"${ufb_actual[r['district_id']]/1e6:.2f}M | {d*100:+.0f}% | [ACFR p.{a25['source_page']}]({a25['source_url']}#page={a25['source_page']}) |")

    # V3
    gaps = [(r, f(r["benefits_budget_2526"]) / f(r["benefits_budget_2526_original"]) - 1) for r in comp
            if f(r["benefits_budget_2526_original"])]
    big = sorted([g for g in gaps if abs(g[1]) > 0.10], key=lambda x: -abs(x[1]))
    L += ["", "## V3. Baseline: revised vs. original 2025-26 budget",
          "Districts revise budgets during the year. We now measure growth from the **revised** 2025-26 figure (what the "
          "2026-27 budget is compared against). The first draft used the original and was wrong for some districts.", "",
          f"**Result: median revision {statistics.median(g for _, g in gaps)*100:+.1f}%; {len(big)} of {len(gaps)} districts "
          f"revised their 2025-26 benefits by more than 10%.** For these, growth rates differ a lot depending on the baseline.", ""]
    L += ["| District | Original | Revised | Revision |", "|---|---|---|---|"]
    for r, g in big[:15]:
        L.append(f"| {r['district_name']} ({r['county']}) | ${f(r['benefits_budget_2526_original'])/1e6:.2f}M | "
                 f"${f(r['benefits_budget_2526'])/1e6:.2f}M | {g*100:+.0f}% |")

    # V4
    out = sorted([r for r in comp if f(r["benefits_change_pct"]) is not None and
                  (f(r["benefits_change_pct"]) > 40 or f(r["benefits_change_pct"]) < -10)],
                 key=lambda r: -abs(f(r["benefits_change_pct"])))
    L += ["", "## V4. Outliers: benefit changes above +40% or below −10%",
          f"**{len(out)} of {len(comp)} comparable districts.** These usually reflect accounting moves (benefits shifted "
          f"between grant and general funds), plan switches, or staffing changes, not premiums. They are included in totals "
          f"but should not be quoted individually without checking the district's documents.", "",
          "| District | Change | 2025-26 rev. | 2026-27 | Audited health FY23→25 |", "|---|---|---|---|---|"]
    for r in out[:30]:
        L.append(f"| {r['district_name']} ({r['county']}) | {f(r['benefits_change_pct']):+.0f}% | "
                 f"${f(r['benefits_budget_2526'])/1e6:.2f}M | ${f(r['benefits_budget_2627'])/1e6:.2f}M | "
                 f"{r['acfr_health_growth_23_25_pct'] or 'n/a'}{'%' if r['acfr_health_growth_23_25_pct'] else ''} |")

    # V5
    diffs = [f(r["state_aid_change_dollars"]) - f(r["state_revenue_change_ufb"]) for r in comp
             if f(r["state_revenue_change_ufb"]) is not None]
    L += ["", "## V5. Which \"state aid\"?",
          "We use NJDOE **K-12 formula aid** (the figure districts are notified of and quote). The UFB's \"Total Revenues from "
          "State Sources\" also includes extraordinary special-ed aid estimates and other items.", "",
          f"**Result: the two measures differ by more than $250K for {sum(abs(d) > 2.5e5 for d in diffs)} of {len(diffs)} "
          f"districts; statewide totals: formula aid {sum(f(r['state_aid_change_dollars']) for r in comp)/1e6:+.0f}M vs UFB state "
          f"revenue {sum(f(r['state_revenue_change_ufb']) or 0 for r in comp)/1e6:+.0f}M.** District documents checked in the "
          f"South Jersey research matched the formula-aid figure (e.g. Cherry Hill −$857,788; Gateway +$694,496)."]

    # V6
    plan = {}
    for d in acfr25:
        p = TEXT / "25" / f"{d}.txt"
        if not p.exists():
            continue
        t = re.sub(r"\s+", " ", p.read_text())
        t = re.sub(r"State Health Benefits Local Education Retired Employees Plan", "", t, flags=re.I)
        # only statements about where *employees'* health coverage comes from; skip OPEB "SEHBP Act" boilerplate
        # and workers'-compensation JIF membership
        cover = r"(health (benefits|insurance|coverage|care)[^.]{0,100}(provided|through|participat|member|enrolled|purchased|obtain))"
        # sentence-level, ignoring retiree coverage; carrier names (Horizon, Aetna) also administer SEHBP, so they are not evidence
        sents = [x for x in re.split(r"(?<=\.)\s", t) if re.search(cover, x, re.I) and not re.search(r"retire", x, re.I)]
        sehbp = any(re.search(r"State of New Jersey|School Employees'? Health|State Health Benefits (Program|Plan)|SEHBP", x, re.I) for x in sents)
        shif = any(re.search(r"School Health Insurance Fund|\bSHIF\b|Health Insurance Fund|Public Employer Trust|self[- ]insured", x, re.I) for x in sents)
        plan[d] = (sehbp, shif)
    agree = disagree = unknown = 0
    conflicts = []
    for r in comp:
        sp = plan.get(r["district_id"])
        if not sp or sp == (False, False) or sp == (True, True):
            unknown += 1
            continue
        audit_says = sp[0]
        if audit_says == (r["in_sehbp"] == "True"):
            agree += 1
        else:
            disagree += 1
            conflicts.append((r, "audit mentions SEHBP" if audit_says else "audit mentions SHIF/JIF/trust"))
    L += ["", "## V6. SEHBP membership: state list vs. the district's own audit",
          "We flag SEHBP districts by matching names on Treasury's [October 2026 participating-employer list]"
          "(https://www.nj.gov/treasury/pensions/documents/pdf/sehbpemp.pdf). As a cross-check, the FY25 audit pages we "
          "extracted were searched for the district's own description of its plan (SEHBP vs. SHIF/JIF/trust). Only "
          "benefit-related pages were kept, so many audits say nothing either way.", "",
          f"**Result: {agree} agree, {disagree} conflict, {unknown} undetermined.** Manual review of the full audit notes "
          f"(and, where needed, the UFB shared-services page) settles 6 conflicts in favour of the list; 7 others rest only on an auditor template sentence and lean toward the list; 2 (Long Branch, North Plainfield) are unresolved. The sentence "
          f"\"Health Benefits are provided to the employees through the State of New Jersey Health Benefits Plan\" is an "
          f"auditor template: it appears word for word in {len(TEMPLATE)} FY25 audits, only one of which (Haworth) is on either "
          f"list, and two of those districts' own budgets name the School Health Insurance Fund. Districts whose only evidence "
          f"is that sentence are probably not in SEHBP, but this isn't confirmed. The [September 2025 list](https://web.archive.org/web/20250904173748/https://www.nj.gov/treasury/pensions/documents/pdf/sehbpemp.pdf) "
          f"(Wayback copy) is shown alongside. **Treat SEHBP membership, and the SEHBP-vs-other comparison, as Medium "
          f"confidence until confirmed with the Division of Pensions & Benefits.** Conflicts:", ""]
    for r, why in conflicts[:30]:
        prev = {"True": "on", "False": "not on"}.get(r.get("in_sehbp_2025_09"), "?")
        note = V6_NOTES.get(r["district_id"]) or ("only the template sentence; no carrier named" if r["district_id"] in TEMPLATE else "")
        L.append(f"- {r['district_name']} ({r['county']}): Oct 2026 list says {'SEHBP' if r['in_sehbp'] == 'True' else 'not SEHBP'} "
                 f"({prev} the Sep 2025 list); {why}" + (f". **Review:** {note}" if note else ""))
    L += ["", "**Membership over time.** Districts matched (all panel districts / comparable) on each Wayback capture of the list and on the current (Oct 2026) "
          "list, counted with `district_panel.sehbp()`: " + "; ".join(f"{k} {a}/{c}" for k, (a, c) in SEHBP_SERIES.items()) +
          ". Membership was already falling, by about 8 comparable districts a year from Nov 2021 to Sep 2025 (about 15 a year "
          "from the Sep 2022 peak), so exits are not a single event; the Sep 2025 → Oct 2026 step (−53 comparable) is three "
          "to six times that pace and coincides with the retitled list, which fits either an exit wave for plan year 2026 or "
          "a narrower list; these data can't tell which. The 2 added in Oct 2026 (Belleville, Holmdel) are rejoiners that "
          "were on the lists until late 2024. Some districts left and returned between lists (Denville, Jefferson Twp, "
          "Lacey, Sussex Voc). Over the longer window the gap holds: districts on the Nov 2021, Sep 2025 and Oct 2026 lists "
          "budgeted a median +24.1% vs +15.5% for districts on none of the three ([numbers](findings/numbers.md)).", "",
          "**Unmatched entry (sensitivity).** \"PASSAIC COUNTY REGIONAL HS BD\" appears on every archived list from Oct 2020 "
          "to Sep 2025 (with a separate \"…BOE NON\" unit line) and not on the Oct 2026 list. It matches no district name; "
          "by elimination it is probably Passaic Valley Regional (3990), but no list, audit or budget confirms that, so we "
          "add no override. If it is 3990, the Sep 2025 count rises by one and the \"left\" group becomes 56; the group "
          "medians do not change (left +14.5%, neither +16.1%)."]

    # V7
    rows7 = []
    for r in comp:
        lv = f(r["levy_change_pct"])
        if lv is None or lv <= 2.05:
            continue
        rows7.append(r)
    L += ["", "## V7. Levy increases above 2%",
          f"{len(rows7)} of {sum(1 for r in comp if f(r['levy_change_pct']) is not None)} comparable districts raised the general-fund "
          "levy more than 2%. The cap law allows this through adjustments (health-care costs, enrollment, banked cap) or a "
          "voter-approved question. The state files do not break the adjustments out, so **we cannot attribute any "
          "district's above-cap increase to health costs from the data alone**; the district research reads it from "
          "adopted budget resolutions (e.g. Winslow $4.22M, Willingboro $2.34M, Swedesboro-Woolwich $1.01M health "
          "adjustments)."]

    # Confidence summary
    L += ["", "## What this means for confidence",
          "| Claim type | Confidence | Why |", "|---|---|---|",
          "| Statewide / county totals of budgeted benefits and formula aid | **High** | Straight sums of the state's own "
          "published files; V1 shows the inputs match the PDFs. |",
          "| \"Benefit increase exceeded aid increase in N districts\" | **High** for the count, **Medium** for any single "
          "district | Robust in aggregate; individual districts can be distorted by accounting moves (V2, V4). |",
          "| Health ≈ 78% of district-paid benefits; audited health growth ~17–18% FY23→FY25 | **Medium-High** | Medians from "
          "audited reports; ~91% parse coverage; V2 shows the audit and budget files agree for most districts. |",
          "| SEHBP vs. non-SEHBP growth gap | **Medium** | Membership is name-matched to Treasury lists. The gap holds on both "
          "the Sep 2025 and Oct 2026 lists and within counties; of 15 audit conflicts, 6 resolve in the lists' favour, 7 are unconfirmed "
          "(auditor template sentence only) and 2 are unresolved (V6), and the 2026 list's scope may differ. Quote the direction and approximate size; confirm membership with "
          "DPB before quoting exact figures for individual districts. |",
          "| Any single district's growth rate | **Medium** unless its profile is rated High | Baseline revisions (V3) "
          "and outliers (V4) can move it a lot. |",
          "| \"Layoffs / larger classes were caused by benefits\" | **Only where a profile says Confirmed with High "
          "confidence**, and even then as \"the district names health costs as a cause\" | Causation comes from district statements, "
          "not from our data, and districts usually name several causes (aid, enrollment, salaries) alongside health. |",
          "| Budgeted fund balance totals | **High** as figures; they are *planned* drawdowns (UFB line 580) | They do not show "
          "remaining reserves, so they cannot support \"reserves are running out\". |",
          "| Students per teacher (TGES Indicator 16) | **Low** for any class-size claim | It counts all teaching staff "
          "(about half of typical class size); the 2024-25 value is not yet confirmed by a later edition; the CSG16 label is "
          "inferred from its columns. Roughly as many districts went down as up. |"]
    (ROOT / "docs" / "validation.md").write_text("\n".join(L) + "\n")
    print("wrote docs/validation.md;", f"V1 {ok}/{len(res)}, V2 {within}/{len(pairs)}, V3 {len(big)}, V4 {len(out)}, "
          f"V6 agree {agree} conflict {disagree}")


if __name__ == "__main__":
    main()
