#!/usr/bin/env python3
"""Check that quoted text in profile source bullets appears word for word in the cited document; write docs/quote-check.md.

Every quoted string in a profile (all sections except the auto-generated "Our numbers" block and the facts comment) is
checked if it has 3+ words or contains a digit. It is searched for in the URLs on the same line, or, for a line with
no URL (Assessment, "same presentation" bullets), in the documents the profile cites elsewhere (audits and
spreadsheets excluded). Documents are cached under data/raw/quote_cache; matching ignores case, punctuation and
markdown bold, and "…" splits a quote into pieces that must appear in order, each within 60 words of the last.
The README tables repeat Assessment text, so they are covered through the profiles. Status classes:
  verbatim     found in a document cited on the same line (or, for a line with no URL, in the profile's sources)
  other source not in the line's own source(s) but found in a document the profile cites elsewhere: the wording is
               real, but the attribution on that line may be wrong; check which document it comes from
  not found    every document the profile cites was read and has real text, but the quote isn't in any of them: a
               paraphrase, or a slide image inside a text document; check by hand
  image-only?  not found, but a cited document could not be read as text (under 1,000 words, .pptx, Google
               Drive/Slides, or a failed fetch), so the quote may be in it; unverified
  unfetchable  no cited document could be fetched (paywall, bot wall, dead link)
  no source    neither the line nor the rest of the profile cites a readable document

    .venv/bin/python scripts/check_quotes.py
"""
import hashlib
import html
import re
import subprocess
import unicodedata
from collections import Counter
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "raw" / "quote_cache"
QUOTE = re.compile(r'["“]([^"”]{3,400})["”]')
WINDOW = 60  # the longest real elision in the profiles spans about 40 words
_docs = {}
LINK = re.compile(r"\]\((https?://[^)\s]+)\)")


def toks(s):
    s = unicodedata.normalize("NFKC", html.unescape(s)).replace("**", "").lower()
    s = re.sub(r"\[[^\]]*\]", " ", s)  # editorial insertions
    s = re.sub(r"(?<=\d)[, ](?=\d{3}\b)", "", s)  # thousands separators, incl. PDF-split "694 496" -> one token
    s = re.sub(r"(?<=\d)\.(?=\d)", "p", s)  # keep decimal points: "6.93" -> "6p93", never equal to "69.3"
    return re.sub(r"[^a-z0-9$%]+", " ", re.sub(r"([$%])", r" \1 ", s)).split()


def fetch(url):
    url = url.split("#")[0]
    if url not in _docs:
        _docs[url] = _fetch(url)
    return _docs[url]


def _fetch(url):
    f = CACHE / hashlib.sha1(url.encode()).hexdigest()
    code = CACHE / (f.name + ".code")
    if not code.exists():
        r = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "40", "-A", "Mozilla/5.0 (Macintosh) Safari/605",
                            "-o", str(f), "-w", "%{http_code}", url], capture_output=True, text=True)
        code.write_text(r.stdout or "000")
    if not code.read_text().startswith("2") or not f.exists():
        return None
    b = f.read_bytes()
    if b[:4] == b"%PDF":
        try:
            t = " ".join(p.get_text() for p in pymupdf.open(stream=b, filetype="pdf"))
        except Exception:
            return None
    else:
        t = re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", b.decode("utf-8", "ignore")))
    return toks(t)


def found(doc, parts):
    """Each piece occurs in doc, in order, starting within WINDOW tokens after the previous piece ends."""
    def at(piece, lo, hi):
        n, first = len(piece), piece[0]
        for i in range(lo, min(hi, len(doc) - n + 1)):
            if doc[i] == first and doc[i:i + n] == piece:
                yield i + n
    def rest(k, lo, hi):
        return k == len(parts) or any(rest(k + 1, e, e + WINDOW) for e in at(parts[k], lo, hi))
    return bool(parts) and rest(0, 0, len(doc))


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in sorted((ROOT / "research" / "districts").glob("*/*.md")):
        if p.name == "README.md":
            continue
        body = re.sub(r"(?s)^## Our numbers.*?(?=^## )", "", p.read_text(), flags=re.M)
        body = re.sub(r"(?s)<!--.*?-->", "", body)
        pool = [u for u in dict.fromkeys(LINK.findall(body)) if not re.search(r"/acfr/|\.xlsx?\b|\.csv\b", u)]
        for line in body.splitlines():
            if "✘" in line:
                continue  # Fact-check lines marked ✘ quote our own earlier, wrong text on purpose
            urls = LINK.findall(line) or pool
            for q in QUOTE.findall(line):
                if q != q.strip() or not (len(q.split()) >= 3 or re.search(r"\d", q)):
                    continue  # a fragment between two quotations, or a short label
                parts = [toks(x) for x in re.split(r"\s*(?:…|\.\.\.)\s*", q)]
                parts = [x for x in parts if x]
                docs = [d for d in map(fetch, urls) if d]
                hit = any(found(d, parts) for d in docs)
                elsewhere = not hit and any(found(d, parts) for d in map(fetch, pool) if d)
                unreadable = len(docs) < len(urls) or (docs and min(map(len, docs)) < 1000) or any(
                    re.search(r"\.pptx?\b|docs\.google|drive\.google", u) for u in urls)
                status = ("verbatim" if hit else "other source" if elsewhere else "no source" if not urls else "unfetchable" if not docs
                          else "image-only?" if unreadable else "not found")
                rows.append((p.relative_to(ROOT / "research" / "districts"), status, q))
    c = Counter(r[1] for r in rows)
    out = ["# Quote check", "",
           "_Generated by `scripts/check_quotes.py`; see its docstring for the status classes. Only **verbatim** quotes "
           "are verified. Everything listed below is **unverified** by this script._", "",
           "_Hand triage, 2026-10-25: ten quotations that did not match their source were corrected "
           "(Cherry Hill ×4, Collingswood, Piscataway, Galloway, Hillsborough, Morris Hills, Monroe Twp) and a headline fixed "
           "(Pleasantville). The remaining \"not found\" rows were judged, not confirmed, to be one of: fact-check "
           "lines quoting our own earlier figures; table rows whose cells the PDF splits apart; slide images inside "
           "text documents; search snippets the profile already labels unused or unverified; or document titles. "
           "The 15 \"other source\" rows were read: each is a line citing the UFB that quotes a figure from a "
           "district document it names in the text, or a news quote also found in another copy the profile cites; "
           "none was judged a misattribution. \"image-only?\" and \"unfetchable\" rows were not examined._", "",
           ", ".join(f"{k}: {c[k]}" for k in ("verbatim", "other source", "not found", "image-only?", "unfetchable", "no source")), "",
           "| Profile | Status | Quote |", "|---|---|---|"]
    out += [f"| [{r}](../research/districts/{r}) | {s} | {q[:160].replace('|', '/')} |" for r, s, q in rows if s != "verbatim"]
    (ROOT / "docs" / "quote-check.md").write_text("\n".join(out) + "\n")
    print(f"wrote docs/quote-check.md: {dict(c)}")


if __name__ == "__main__":
    main()
