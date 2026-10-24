#!/usr/bin/env python3
"""Employee benefits vs. everything else in NJ district general-fund budgets.

Uses User-Friendly Budget appropriations (data/raw/ufb/*/approp*.csv):
  line 71260 = Total Personal Services - Employee Benefits
  line 72260 = Total General Current Expense (operating budget, excl. capital/debt/grants)
Each file has amount_1 (actual, 2 yrs prior), amount_2 (revised, prior yr), amount_3 (budget yr).

    python3 analysis/benefits_trend.py [district name prefix]
"""
import csv
import glob
import statistics
import sys
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw" / "ufb"
BENEFITS, GCE = "71260", "72260"
COLS = ("amount_1", "amount_2", "amount_3")


def load(path):
    """{(county_id, district_id, name): {line: [a1, a2, a3]}} for the two lines we need."""
    out = {}
    with open(path, encoding="latin-1") as f:
        for r in csv.DictReader(f):
            ln = r["line_no"].strip()
            if ln not in (BENEFITS, GCE):
                continue
            vals = []
            for c in COLS:
                try:
                    vals.append(float(r[c] or 0))
                except ValueError:
                    vals.append(0.0)
            out.setdefault((r["county_id"], r["district_id"], r["district_name"].strip()), {})[ln] = vals
    return out


def main():
    prefix = sys.argv[1] if len(sys.argv) > 1 else None
    files = sorted(glob.glob(str(RAW / "*" / "approp*.csv")))
    print("Statewide, budget-to-budget ($B)")
    print(f"{'budget year':12} {'benefits':>9} {'other GCE':>10} {'benefit %':>10}")
    prev = None
    for f in files:
        data = load(f)
        b = sum(v.get(BENEFITS, [0, 0, 0])[2] for v in data.values())
        g = sum(v.get(GCE, [0, 0, 0])[2] for v in data.values())
        year = Path(f).parent.name
        line = f"{year:12} {b/1e9:9.2f} {(g-b)/1e9:10.2f} {b/g*100:9.1f}%"
        if prev:
            db, dg = b - prev[0], g - prev[1]
            line += f"   Δbenefits {db/prev[0]*100:+5.1f}%  Δother {((g-b)/(prev[1]-prev[0])-1)*100:+5.1f}%  benefits = {db/dg*100:4.0f}% of GCE growth"
        print(line)
        prev = (b, g)

    data = load(files[-1])
    rows = []
    for k, v in data.items():
        if BENEFITS in v and GCE in v and v[BENEFITS][1] > 1e5:
            b2, b3 = v[BENEFITS][1], v[BENEFITS][2]
            g3 = v[GCE][2]
            rows.append((k, (b3 / b2 - 1) * 100, b3 / g3 * 100))
    growth = sorted(r[1] for r in rows)
    share = sorted(r[2] for r in rows)
    q = lambda xs, p: xs[int(p * (len(xs) - 1))]
    print(f"\nLatest file, per district (n={len(rows)}), revised prior year -> budget year:")
    print(f"  benefit growth   median {statistics.median(growth):5.1f}%  p25 {q(growth,.25):5.1f}%  p75 {q(growth,.75):5.1f}%")
    print(f"  benefits % of GCE median {statistics.median(share):5.1f}%  p10 {q(share,.1):5.1f}%  p90 {q(share,.9):5.1f}%")

    if prefix:
        for f in files:
            for k, v in load(f).items():
                if k[2].lower().startswith(prefix.lower()) and BENEFITS in v:
                    b, g = v[BENEFITS], v[GCE]
                    print(f"  {Path(f).parent.name} {k[2]}: benefits actual/revised/budget "
                          + " / ".join(f"{x/1e6:.1f}M" for x in b)
                          + f"   GCE budget {g[2]/1e6:.1f}M ({b[2]/g[2]*100:.1f}% benefits)")


if __name__ == "__main__":
    main()
