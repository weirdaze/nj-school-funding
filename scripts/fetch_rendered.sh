#!/usr/bin/env bash
# Render a JS-heavy page through the Playwright scraper service and print its HTML.
#   SCRAPER_API_KEY=... ./scripts/fetch_rendered.sh <url> [wait_for_selector]
# SCRAPER_URL defaults to a local instance. Be gentle: a few seconds between calls.
set -euo pipefail

: "${SCRAPER_API_KEY:?set SCRAPER_API_KEY (e.g. via op run / op read)}"
SCRAPER_URL="${SCRAPER_URL:-http://localhost:8765}"
URL="${1:?usage: $0 <url> [wait_for_selector]}"
SEL="${2:-}"

payload=$(python3 -c 'import json,sys; print(json.dumps({"url":sys.argv[1],"timeout_ms":30000,"wait_for_selector":sys.argv[2] or None}))' "$URL" "$SEL")

# The scraper applies timeout_ms to the page load and again to the selector wait.
curl -sS --max-time 75 -X POST "$SCRAPER_URL/fetch-html" \
  -H "X-API-Key: $SCRAPER_API_KEY" -H 'Content-Type: application/json' -d "$payload" \
| python3 -c 'import json,sys; d=json.load(sys.stdin); sys.stdout.write(d["html"]) if "html" in d else sys.exit("scraper error: %s" % d.get("detail", d))'
