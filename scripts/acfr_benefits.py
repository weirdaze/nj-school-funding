#!/usr/bin/env python3
"""Pull the employee-benefit breakdown out of district ACFRs (audited financial reports).

NJDOE hosts every district's ACFR at
    https://www.nj.gov/education/finance/fp/acfr/search/{YY}/{district_id}.pdf
Exhibit C-1 (General Fund budgetary comparison) itemizes "Unallocated Benefits"
(health, PERS, social security, ...) and the state's on-behalf TPAF payments.

Each PDF (~5 MB) is downloaded to a temp file, only the benefit pages are kept as
text under data/raw/acfr_text/, and the PDF is deleted, so statewide runs stay small.

    .venv/bin/python scripts/acfr_benefits.py fetch --counties 05,07,15 --years 23,24,25
    .venv/bin/python scripts/acfr_benefits.py parse
"""
import argparse
import csv
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "data" / "raw" / "acfr_text"
OUT = ROOT / "data" / "processed" / "acfr_benefits.csv"
UFB = ROOT / "data" / "raw" / "ufb" / "2627" / "approp27.csv"
URL = "https://www.nj.gov/education/finance/fp/acfr/search/{yy}/{dist}.pdf"
UA = "Mozilla/5.0 (nj-school-funding research)"

# (column, label regex). Order matters: first match wins for a line.
FIELDS = [
    ("total_unallocated", r"^Total (Undistributed Expenditures\s*-\s*)?(Unallocated (Employee )?Benefits|Personal Services\s*-\s*Employee Benefits)"),
    ("social_security", r"^Social Security Contrib"),
    ("pers", r"^Other Retirement Contrib\w*\.?\s*-+\s*PERS"),
    ("other_retirement", r"^Other Retirement Contrib\w*\.?\s*-+\s*(Regular|ERIP|DCRP|Other)"),
    ("unemployment", r"^Unemployment Comp"),
    ("workers_comp", r"^Work\w*'?s'? Comp"),
    ("health", r"^Health Benefits\b"),
    ("tuition_reimb", r"^Tu\w*ion Reimb"),
    ("other_benefits", r"^Other Employee Benefits"),
    ("unused_sick", r"^Unused (Sick|Vacation)"),
    ("tpaf_prm", r"(TPAF|Teachers'? Pension).*Post[- ]?Ret"),
    ("tpaf_ncgi", r"(TPAF|Teachers'? Pension).*(Non-?contributory|NCGI)"),
    ("tpaf_ltd", r"(TPAF|Teachers'? Pension).*(Long[- ]Term Disab|LTDI)"),
    ("reimbursed_ss", r"Reimbursed (T\.?P\.?A\.?F\.? )?Social Security"),
    ("tpaf_pension", r"(TPAF|Teachers'? Pension and Annuity Fund)(?!.*(Social|Medical|Ret|Disab|LTDI|NCGI|Non-?contrib))"),
]
COLS = [c for c, _ in FIELDS]
# Uniform Minimum Chart of Accounts: 11-000-291-xxx = unallocated employee benefits
CODES = {"220": "social_security", "241": "pers", "249": "other_retirement", "250": "unemployment",
         "260": "workers_comp", "270": "health", "280": "tuition_reimb", "290": "other_benefits", "299": "unused_sick"}
NUM = re.compile(r"^\(?-?[\d,]+(\.\d+)?\)?$|^-$")


def page_text(page):
    """Page text in reading order, rebuilding rows when the table is printed sideways."""
    lines = [l for b in page.get_text("dict")["blocks"] for l in b.get("lines", [])]
    vertical = sum(1 for l in lines if abs(l["dir"][1]) > abs(l["dir"][0]))
    if not lines or vertical < len(lines) / 2:
        return page.get_text(sort=True)
    items = []
    for l in lines:
        txt = "".join(s["text"] for s in l["spans"]).strip()
        if not txt:
            continue
        x0, y0, x1, y1 = l["bbox"]
        dx, dy = l["dir"]
        if abs(dy) > abs(dx):
            row, along = (x0 + x1) / 2, (-(y0 + y1) / 2 if dy < 0 else (y0 + y1) / 2)
        else:
            row, along = (y0 + y1) / 2, (x0 + x1) / 2
        items.append((row, along, txt))
    items.sort()
    rows, cur, last = [], [], None
    for row, along, txt in items:
        if last is not None and abs(row - last) > 4:
            rows.append(cur)
            cur = []
        cur.append((along, txt))
        last = row
    rows.append(cur)
    return "\n".join("   ".join(t for _, t in sorted(r)) for r in rows)


def districts(counties):
    seen = {}
    with open(UFB, encoding="latin-1") as f:
        for r in csv.DictReader(f):
            if not counties or r["county_id"] in counties:
                seen[r["district_id"]] = (r["county_id"], r["county_name"], r["district_name"].strip())
    return seen


def fetch(args):
    counties = set(args.counties.split(",")) if args.counties else None
    todo = districts(counties)
    print(f"{len(todo)} districts × {len(args.years)} years")
    for yy in args.years:
        (TEXT / yy).mkdir(parents=True, exist_ok=True)
        for dist, (_, cname, name) in sorted(todo.items()):
            dest = TEXT / yy / f"{dist}.txt"
            miss = TEXT / yy / f"{dist}.missing"
            if dest.exists() or miss.exists():
                continue
            with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
                try:
                    req = urllib.request.Request(URL.format(yy=yy, dist=dist), headers={"User-Agent": UA})
                    with urllib.request.urlopen(req, timeout=120) as r:
                        tmp.write(r.read())
                    tmp.flush()
                except urllib.error.HTTPError as e:
                    miss.write_text(f"HTTP {e.code}\n")
                    print(f"miss  {yy} {dist} {name} ({e.code})")
                    time.sleep(args.delay)
                    continue
                except Exception as e:  # network hiccup: leave for next run
                    print(f"err   {yy} {dist} {name}: {e}")
                    time.sleep(args.delay * 5)
                    continue
                try:
                    doc = pymupdf.open(tmp.name)
                    # cheap prefilter first; rebuild reading order only on candidate pages
                    pages = [page_text(p) if re.search(r"Benefit|TPAF|Social\s+Sec", p.get_text(), re.I) else "" for p in doc]
                except Exception as e:
                    miss.write_text(f"unreadable: {e}\n")
                    print(f"bad   {yy} {dist} {name}")
                    continue
            keep = [f"=== page {i+1}\n{t}" for i, t in enumerate(pages)
                    if re.search(r"Unallocated (Employee )?Benefits|11-000-291|Health Benefits|On[- ]behalf T\.?P\.?A\.?F|Reimbursed (T\.?P\.?A\.?F\.? )?Social Security", re.sub(r"\s+", " ", t), re.I)]
            dest.write_text(f"# {dist} {name} ({cname}) FY20{yy}\n" + "\n".join(keep))
            print(f"ok    {yy} {dist} {name} ({len(keep)} pages)")
            time.sleep(args.delay)


def to_num(tok):
    if tok == "-":
        return 0.0
    neg = tok.startswith("(")
    v = float(tok.strip("()").replace(",", ""))
    return -v if neg else v


def actual_of(nums):
    """Pick the 'actual' column from a row's trailing numbers.

    Full rows: original, transfers, final, actual, variance (final - actual = variance).
    Some auditors leave zero columns blank, so check the arithmetic before trusting position.
    """
    v = [to_num(t) for t in nums]
    if len(v) == 3 and abs(v[0] + v[1] - v[2]) <= 1 and v[1] != 0:  # original, transfers, final; rest blank
        return v[2] if v[2] == 0 else 0.0
    if len(v) >= 3 and abs((v[-3] - v[-2]) - v[-1]) <= 1:
        return v[-2]
    if len(v) >= 2 and abs(v[-2] + v[-1]) <= 1 and v[-2] != 0:  # nonbudgeted: actual, (actual)
        return v[-2]
    if len(v) >= 2 and abs(v[-1] - v[-2]) <= 1:  # final == actual, variance left blank
        return v[-1]
    return v[-2] if len(v) >= 2 else v[-1]


def _parse_c1_main(text):
    """Return {field: actual} from the Exhibit C-1 benefit block."""
    pages = [re.sub(r"[ \t\xa0]+", " ", p) for p in text.split("=== page ")]

    def score(p):
        return (3 * bool(re.search(r"11-000-291-2[27]0", p))
                + 2 * bool(re.search(r"Total (Undistributed Expenditures\s*-\s*)?Unallocated (Employee )?Benefits", p, re.I))
                + 2 * bool(re.search(r"^\s*Health Benefits\s+(11-000-291-270\s+)?[\d(]", p, re.I | re.M))
                + bool(re.search(r"Final\s+Budget|Variance|Final to Actual", p, re.I)))
    scored = [(score(p), -i) for i, p in enumerate(pages)]
    best = max(scored) if scored else (0, 0)
    if best[0] < 2:
        return {}
    idx = -best[1]
    lines = "\n".join(pages[idx: idx + 2]).splitlines()
    start = next((i - 1 for i, l in enumerate(lines) if "11-000-291-" in l), None)
    if start is None:
        start = next((i for i, l in enumerate(lines) if re.search(r"Unallocated Benefits", l, re.I)
                      and not re.search(r"Total", l, re.I)), None)
    if start is None:
        start = next((i for i, l in enumerate(lines) if re.search(r"^\s*(Social Security|Health Benefits)\s+[\d(]", l, re.I)), 16) - 2
    out, pending = {}, ""
    for raw in lines[max(start, 0): max(start, 0) + 60]:
        line = re.sub(r"(\d) ,(\d)", r"\1,\2", re.sub(r"\s+", " ", raw)).strip()
        line = re.sub(r"(?<=[\s(,\d])[Iil](?=[\d,])|(?<=\d)[Iil](?=[\d,\s)]|$)", "1", line)
        if re.match(r"^Total (Undistributed|General Current|Expenditures)", line, re.I) and not re.search(r"Benefits", line, re.I):
            break
        if not line:
            continue
        code = re.search(r"11-000-291-(\d{3})", line)
        toks = [t for t in line.split(" ") if t != "$"]
        nums = []
        while toks and NUM.match(toks[-1]):
            nums.insert(0, toks.pop())
        label = " ".join(t for t in toks if not re.match(r"^\d{2}-\d{3}-\d{3}-\d{3}$", t)).strip()
        if not nums:
            pending = (pending + " " + label).strip() if label else pending
            continue
        if not label or re.fullmatch(r"\(?non-?budgeted\)?", label, re.I):
            label = pending
        elif pending and not any(re.search(p, label, re.I) for _, p in FIELDS):
            label = pending + " " + label
        pending = ""
        if len(nums) < 2 and "-" not in nums:
            continue
        if code and code.group(1) in CODES:
            col = CODES[code.group(1)]
            if col == "other_retirement":
                out[col] = out.get(col, 0) + actual_of(nums)
            elif col not in out:
                out[col] = actual_of(nums)
            continue
        for col, pat in FIELDS:
            if re.search(pat, label, re.I):
                if col == "other_retirement":  # Regular, ERIP, DCRP... can each have a row
                    out[col] = out.get(col, 0) + actual_of(nums)
                elif col not in out:
                    out[col] = actual_of(nums)
                break
    return out


def parse_c1(text):
    """Unallocated-benefits block if it has health; otherwise try benefits allocated by function."""
    main = _parse_c1_main(text)
    if main.get("health"):
        return main
    alloc = parse_allocated([re.sub(r"[ \t\xa0]+", " ", p) for p in text.split("=== page ")])
    if alloc:
        alloc.update({k: v for k, v in main.items() if k.startswith(("tpaf", "reimbursed"))})
        return alloc
    return main


def parse_allocated(pages):
    """Districts that charge benefits to each function (11-xxx-xxx-270 etc.) instead of 11-000-291.

    Sum the actual column of every coded benefit line across the C-1 pages, by object code.
    """
    out = {}
    seen = set()
    for p in pages:
        for raw in p.splitlines():
            line = re.sub(r"(\d) ,(\d)", r"\1,\2", re.sub(r"\s+", " ", raw)).strip()
            m = re.search(r"\b11-[\dX]{3}-[\dX]{3}-2(\d\d)\b", line)  # general fund only
            if not m or ("2" + m.group(1)) not in CODES or m.group(0) in seen:
                continue
            seen.add(m.group(0))
            toks = [t for t in line[m.end():].split(" ") if t and t != "$"]
            nums = [t for t in toks if NUM.match(t)]
            if len(nums) >= 2:
                col = CODES["2" + m.group(1)]
                out[col] = out.get(col, 0) + actual_of(nums)
    if out.get("health"):
        out["total_unallocated"] = sum(v for k, v in out.items() if k in CODES.values())
        out["method"] = "allocated"
        return out
    return {}


def parse(args):
    rows = []
    for f in sorted(TEXT.glob("*/*.txt")):
        head = f.read_text().splitlines()[0]
        m = re.match(r"# (\d+) (.*) \((.*)\) FY(\d+)", head)
        dist, name, cname, fy = m.groups()
        vals = parse_c1(f.read_text())
        comp = sum(vals.get(c, 0) for c in COLS[1:10])
        tot = vals.get("total_unallocated")
        ok = bool(tot) and abs(comp - tot) <= max(1000, 0.01 * tot)
        rows.append({"fiscal_year": fy, "county": cname, "district_id": dist, "district_name": name,
                     **{c: vals.get(c, "") for c in COLS}, "components_match_total": ok,
                     "method": vals.get("method", "unallocated" if vals else "")})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    good = sum(r["components_match_total"] for r in rows)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} district-years, {good} reconcile to total")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("--counties", default="", help="comma-separated county ids, e.g. 05,07,15 (default: all)")
    f.add_argument("--years", default="23,24,25", type=lambda s: s.split(","))
    f.add_argument("--delay", default=1.5, type=float, help="seconds between requests")
    sub.add_parser("parse")
    a = ap.parse_args()
    {"fetch": fetch, "parse": parse}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
