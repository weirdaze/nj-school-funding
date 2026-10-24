#!/usr/bin/env python3
"""Extract the datasets embedded in the NJ Report Card site (reportcard.nj.gov).

The site is a single-page app behind Incapsula; its budget/revenue data ships as
CSV template literals inside the JS bundle. This renders the page through the
Playwright scraper (to learn the current bundle name), fetches the bundle, and
writes each embedded CSV to data/processed/reportcard/.

    SCRAPER_API_KEY=... python3 scripts/fetch_reportcard.py
"""
import base64
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

SITE = "https://reportcard.nj.gov"
SCRAPER_URL = os.environ.get("SCRAPER_URL", "http://localhost:8765")
OUT = Path(__file__).resolve().parent.parent / "data" / "processed" / "reportcard"

# header (first column set) -> output filename
NAMES = {
    "program_area,fiscal_year,amount,status,yoy_pct_change": "appropriations_by_program_area.csv",
    "dept_code,dept_name,budget_category,fund,fiscal_year,amount,status": "appropriations_by_department.csv",
    "dept_code,dept_name,proposed_amount,enacted_amount,dollar_change,pct_change": "fy27_proposed_vs_enacted_by_department.csv",
    "rev_id,approp_id,rev_title,type,fund,fiscal_year,amount,status": "revenues",  # two tables share this header
}


def scraper(endpoint, payload, timeout):
    req = urllib.request.Request(
        f"{SCRAPER_URL}/{endpoint}",
        data=json.dumps(payload).encode(),
        headers={"X-API-Key": os.environ["SCRAPER_API_KEY"], "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def main():
    if "SCRAPER_API_KEY" not in os.environ:
        sys.exit("set SCRAPER_API_KEY")
    html = scraper("fetch-html", {"url": SITE + "/", "timeout_ms": 30000, "wait_for_selector": None}, 75)["html"]
    bundle = re.search(r'src="(/assets/index-[\w-]+\.js)"', html)
    if not bundle:
        sys.exit("could not find JS bundle in rendered page")
    time.sleep(3)  # be gentle
    raw = scraper("fetch-raw", {"url": SITE + bundle.group(1), "timeout_ms": 45000}, 100)
    if raw.get("status") != 200:
        sys.exit(f"bundle fetch failed: {raw.get('status')}")
    js = (base64.b64decode(raw["body_base64"]) if raw.get("body_base64") else raw["body"].encode()).decode("utf-8")

    OUT.mkdir(parents=True, exist_ok=True)
    revenue_tables = []
    for m in re.finditer(r"`([a-z_]+(?:,[a-z_]+){2,})\n(.*?)`", js, re.S):
        header, body = m.group(1), m.group(2).rstrip()
        name = NAMES.get(header)
        if name == "revenues":
            revenue_tables.append(header + "\n" + body + "\n")
            continue
        if name:
            (OUT / name).write_text(header + "\n" + body + "\n")
            print(f"wrote {name} ({body.count(chr(10)) + 1} rows)")
    # Larger table is revenue by fund (all line items); smaller is the top-10 major line items.
    revenue_tables.sort(key=len, reverse=True)
    for name, text in zip(["revenues_by_fund.csv", "revenues_major_line_items.csv"], revenue_tables):
        (OUT / name).write_text(text)
        print(f"wrote {name} ({text.count(chr(10)) - 1} rows)")
    (OUT / "SOURCE.txt").write_text(
        f"Extracted from {SITE}{bundle.group(1)} on {time.strftime('%Y-%m-%d')}.\n"
        "Units: by-program-area in dollars; by-department and revenues in THOUSANDS of dollars.\n"
        "status: final/actual = audited; adjusted/estimate = current-year; enacted = FY27 appropriation.\n"
    )


if __name__ == "__main__":
    main()
