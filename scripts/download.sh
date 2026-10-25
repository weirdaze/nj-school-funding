#!/usr/bin/env bash
# Download the core NJ school funding datasets into data/raw/.
# Re-runnable: skips files that already exist (pass -f to force).
set -euo pipefail

FORCE=0
[[ "${1:-}" == "-f" ]] && FORCE=1

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RAW="$ROOT/data/raw"
UA="Mozilla/5.0 (nj-school-funding research)"

fetch() { # fetch <subdir> <url>
  local dir="$RAW/$1" url="$2"
  local name; name="$(basename "${url%%\?*}")"; name="${name//%20/_}"
  mkdir -p "$dir"
  if [[ -f "$dir/$name" && $FORCE -eq 0 ]]; then echo "skip  $1/$name"; return; fi
  if curl -fsSL -A "$UA" --retry 2 --max-time 300 "$url" -o "$dir/$name.part"; then
    mv "$dir/$name.part" "$dir/$name"; echo "ok    $1/$name"
  else
    rm -f "$dir/$name.part"; echo "FAIL  $url" >&2
  fi
}

NJ=https://www.nj.gov

# Stage 3: state aid to districts (SFRA)
for f in FY27_GBM_District_Details.xlsx FY27_GBM_County_Summary.xlsx FY27_GBM_Preschool_Aid.xlsx; do
  fetch stateaid/2627 "$NJ/education/stateaid/2627/$f"
done
fetch stateaid/zips "$NJ/education/stateaid/zippedfiles/2526.zip"
fetch stateaid/zips "$NJ/education/stateaid/zippedfiles/2425.zip"
fetch stateaid/ear  "$NJ/education/stateaid/docs/ear/EAR_FY2026_AppendixB.xlsx"

# Stage 4: district budgets (User-Friendly Budget)
for yy in 21 22 23 24 25 26 27; do
  prev=$(printf '%02d' $((10#$yy - 1)))
  for f in rev approp esttax recap pupcst enroll employees schapp; do
    # 2024-25 files carry an odd "_minus_1" suffix on the NJDOE site
    sfx=""; [[ $yy == 25 ]] && sfx="_minus_1"
    fetch "ufb/$prev$yy" "$NJ/education/budget/ufb/$prev$yy/download/$f$yy$sfx.csv"
  done
done
fetch ufb "$NJ/education/budget/ufb/2627/download/userfr_layout.xlsx"

# Stage 5: actual spending (Taxpayers' Guide to Education Spending)
fetch tges/2023 "$NJ/education/guide/docs/2023_TGES.zip"
fetch tges/2024 "$NJ/education/guide/docs/2024/TGES24_Zipped.zip"
fetch tges/2025 "$NJ/education/guide/docs/2025/TGES2025_Zipped.zip"
for z in "$RAW"/tges/*/*.zip; do  # analysis reads tges/<edition>/x/*/CSG*.CSV
  [[ -d "$(dirname "$z")/x" && $FORCE -eq 0 ]] || unzip -oq "$z" -d "$(dirname "$z")/x"
done

# State-paid teacher pension / retiree medical on behalf of districts (TPAF allocations)
fetch audit "$NJ/education/fpp/audit/2223/docs/NJ_TPAF_Allocations_LEAs_FY2023.xlsx"
fetch audit "$NJ/education/fpp/audit/2324/docs/NJ_TPAF_Allocations_LEAs_FY2024.xlsx"
fetch audit "$NJ/education/fpp/audit/2425/docs/NJ_TPAF_Allocations_LEAs_FY2025.xlsx"

# SEHBP participating employers (current list; Treasury replaces it in place, so keep a dated copy when it matters)
fetch sehbp "$NJ/treasury/pensions/documents/pdf/sehbpemp.pdf"
# Earlier list (Sep 2025, archived by the Wayback Machine) for the membership-history comparison; the
# 2021-2025 lists cut names at 30 characters, which district_panel.untruncate() handles
fetch sehbp/2025-09 "https://web.archive.org/web/20250904173748id_/https://www.nj.gov/treasury/pensions/documents/pdf/sehbpemp.pdf"
fetch sehbp/2021-11 "https://web.archive.org/web/20211111000412id_/https://www.nj.gov/treasury/pensions/documents/pdf/sehbpemp.pdf"

# Outcomes: School Performance Reports (district/state detail ~120MB; school detail is larger)
SPR="$NJ/education/sprreports/download/DataFiles/2024-2025"
for f in Database_DistrictLayout.xlsx Database_DistrictStateDetail.xlsx Database_SchoolLayout.xlsx; do
  fetch spr/2024-2025 "$SPR/$f"
done
# fetch spr/2024-2025 "$SPR/Database_SchoolDetail.xlsx"   # uncomment if needed

# Stage 1: local property tax (DLGS abstract of ratables, Taxation rate tables)
for yy in 22 23 24 25; do
  fetch "dlgs/20$yy" "$NJ/dca/dlgs/resources/Property_Tax/${yy}_data/${yy}abstract.xls"
  fetch "dlgs/20$yy" "$NJ/dca/dlgs/resources/Property_Tax/${yy}_data/${yy}taxes.xls"
done
fetch taxation "$NJ/treasury/taxation/pdf/lpt/gtr/2025taxrates.pdf"
fetch taxation "$NJ/treasury/taxation/pdf/lpt/2026StateEq.pdf"

# Stage 1–2: state budget
fetch omb/fy27 "$NJ/treasury/omb/publications/27budget/RevCert-FY27.pdf"
fetch omb/fy27 "$NJ/treasury/omb/publications/27bib/BIB.pdf"
fetch omb/fy27 "$NJ/treasury/omb/publications/27approp/FY2027AppropriationsHandbook-Full.pdf"

echo "done → $RAW"
