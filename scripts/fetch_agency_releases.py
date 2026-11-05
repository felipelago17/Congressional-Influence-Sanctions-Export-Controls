#!/usr/bin/env python3
"""Collect enforcement-related releases from DOJ, BIS and OFAC official sites.

Sources (all public; no API keys):
  DOJ  — RSS feed of Office of Public Affairs press releases, plus the press-release
         search page for resolving named targets older than the feed window.
  BIS  — HTML listing at /news-updates (no RSS).
  OFAC — HTML listing at /recent-actions (RSS retired January 2025).

Two passes, mirroring the Federal Register script:
1. Targets — named cases in trackers/agency-releases.yaml the repository needs an
   official URL for; matched by keywords in the title.
2. Scan — recent releases whose title matches any keyword.

Parsing is regex-based and deliberately tolerant; each source is isolated so one
failure does not block the others. Outputs:
  data/agency-releases.json
  docs/trackers/agency-releases.md
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "trackers" / "agency-releases.yaml"
DATA_OUT = ROOT / "data" / "agency-releases.json"
PAGE_OUT = ROOT / "docs" / "trackers" / "agency-releases.md"
TIMEOUT = 30
UA = {"User-Agent": "Mozilla/5.0 (compatible; congressional-influence-tracker/1.0; +https://github.com/felipelago17)"}

DOJ_RSS = "https://www.justice.gov/feeds/opa/justice-news.xml"
DOJ_SEARCH = "https://www.justice.gov/news/press-releases?search_api_fulltext={q}"
BIS_NEWS = "https://www.bis.gov/news-updates"
BIS_ENF = "https://www.bis.gov/enforcement"
OFAC_RECENT = "https://ofac.treasury.gov/recent-actions"
OFAC_PENALTIES = "https://ofac.treasury.gov/civil-penalties-and-enforcement-information"


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 503) and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise RuntimeError(f"HTTP {exc.code} {url}") from None
        except urllib.error.URLError as exc:
            if attempt < 2:
                time.sleep(3)
                continue
            raise RuntimeError(f"URL error {url}: {exc.reason}") from None
    return ""


def _clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def _abs(base: str, href: str) -> str:
    return urllib.parse.urljoin(base, href)


# ---------------------------------------------------------------- DOJ
def doj_rss() -> list[dict]:
    raw = _fetch(DOJ_RSS)
    root = ET.fromstring(raw)
    out = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        date = ""
        for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z"):
            try:
                date = datetime.strptime(pub, fmt).strftime("%Y-%m-%d")
                break
            except ValueError:
                continue
        out.append({"agency": "DOJ", "title": title, "url": link, "date": date})
    return out


def doj_search(query: str) -> list[dict]:
    raw = _fetch(DOJ_SEARCH.format(q=urllib.parse.quote_plus(query)))
    out = []
    # Anchors to press releases: /opa/pr/..., /usao-.../pr/..., /nsd/pr/...
    for m in re.finditer(r'<a[^>]+href="(/(?:opa|usao-[a-z-]+|nsd|criminal)/pr/[^"]+)"[^>]*>(.*?)</a>', raw, re.S | re.I):
        title = _clean(m.group(2))
        if not title:
            continue
        out.append({"agency": "DOJ", "title": title, "url": _abs("https://www.justice.gov", m.group(1)), "date": ""})
    # de-dupe by url
    seen, uniq = set(), []
    for r in out:
        if r["url"] in seen:
            continue
        seen.add(r["url"]); uniq.append(r)
    return uniq


# ---------------------------------------------------------------- BIS
_MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"


def _bis_parse(raw: str, base: str) -> list[dict]:
    out = []
    # Generic: anchor + nearby date text. Capture (href, anchor text) then look back/forward for a date.
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', raw, re.S | re.I):
        href, text = m.group(1), _clean(m.group(2))
        if not text or len(text) < 15:
            continue
        if not re.search(r"/(press-release|news|enforcement|media/documents)/", href):
            continue
        window = raw[max(0, m.start() - 400): m.end() + 400]
        dm = re.search(rf"({_MONTHS})\s+(\d{{1,2}}),\s+(\d{{4}})", _clean(window))
        date = ""
        if dm:
            try:
                date = datetime.strptime(f"{dm.group(1)} {dm.group(2)} {dm.group(3)}", "%B %d %Y").strftime("%Y-%m-%d")
            except ValueError:
                pass
        out.append({"agency": "BIS", "title": text, "url": _abs(base, href), "date": date})
    seen, uniq = set(), []
    for r in out:
        if r["url"] in seen:
            continue
        seen.add(r["url"]); uniq.append(r)
    return uniq


def bis_listing() -> list[dict]:
    rows = []
    for url in (BIS_NEWS, BIS_ENF):
        try:
            rows += _bis_parse(_fetch(url), url)
        except Exception as exc:  # noqa: BLE001
            print(f"  ⚠ BIS {url}: {exc}")
    return rows


# ---------------------------------------------------------------- OFAC
def ofac_listing() -> list[dict]:
    out = []
    for url in (OFAC_RECENT, OFAC_PENALTIES):
        try:
            raw = _fetch(url)
        except Exception as exc:  # noqa: BLE001
            print(f"  ⚠ OFAC {url}: {exc}")
            continue
        for m in re.finditer(r'<a[^>]+href="(/recent-actions/(\d{8})(?:_\d+)?)"[^>]*>(.*?)</a>', raw, re.S | re.I):
            title = _clean(m.group(3))
            if not title:
                continue
            d = m.group(2)
            out.append({"agency": "OFAC", "title": title, "url": _abs(OFAC_RECENT, m.group(1)),
                        "date": f"{d[:4]}-{d[4:6]}-{d[6:]}"})
        # Enforcement release PDFs on the penalties chart
        for m in re.finditer(r'<a[^>]+href="(/media/\d+/download[^"]*)"[^>]*>(.*?)</a>', raw, re.S | re.I):
            title = _clean(m.group(2))
            if title:
                out.append({"agency": "OFAC", "title": title, "url": _abs(OFAC_RECENT, m.group(1)), "date": ""})
    seen, uniq = set(), []
    for r in out:
        if r["url"] in seen:
            continue
        seen.add(r["url"]); uniq.append(r)
    return uniq


# ---------------------------------------------------------------- matching
def _match_target(t: dict, rows: list[dict]) -> dict | None:
    kws = [k.lower() for k in t.get("title_keywords", [])]
    any_kws = [k.lower() for k in t.get("title_any", [])]
    for r in rows:
        tl = r["title"].lower()
        if kws and not all(k in tl for k in kws):
            continue
        if any_kws and not any(k in tl for k in any_kws):
            continue
        if t.get("agency") and r["agency"] != t["agency"]:
            continue
        return r
    return None


def render_page(payload: dict) -> str:
    gen = payload["generated_at"][:16].replace("T", " ") + " UTC"
    out = [
        "# Agency enforcement releases (DOJ · BIS · OFAC)",
        "",
        f"*Auto-generated {gen} from official DOJ, BIS and OFAC web pages (DOJ via RSS; BIS and OFAC via their HTML listings — OFAC retired its RSS feed in January 2025). "
        "Keyword-filtered. Public-domain content. Not legal advice.*",
        "",
        f"Sources reachable this run: {', '.join(payload['sources_ok']) or 'none'}"
        + (f"; failed: {', '.join(payload['sources_failed'])}" if payload["sources_failed"] else ""),
        "",
        "## Resolved targets",
        "",
        "Official URLs for cases referenced in `trackers/enforcement-actions.yaml`.",
        "",
        "| Target | Agency | Date | Title | Link |",
        "|---|---|---|---|---|",
    ]
    for t in payload["targets"]:
        r = t.get("resolved")
        if r:
            out.append(f"| {t['id']} | {r['agency']} | {r.get('date') or ''} | {r['title']} | [link]({r['url']}) |")
        else:
            out.append(f"| {t['id']} | {t.get('agency') or '—'} | — | _not yet found_ — {t.get('label','')} | — |")
    out += ["", "## Keyword scan — recent releases", "",
            f"Keywords: {', '.join('`' + k + '`' for k in payload['keywords'])}", ""]
    if payload["scan"]:
        out += ["| Date | Agency | Title | Matched |", "|---|---|---|---|"]
        for r in sorted(payload["scan"], key=lambda x: x.get("date") or "", reverse=True):
            out.append(f"| {r.get('date') or ''} | {r['agency']} | [{r['title']}]({r['url']}) | {', '.join(r['matched_keywords'])} |")
    else:
        out.append("_No title matches._")
    out += ["", "---",
            "Releases are administration actions. Curated entries with amounts, conduct and sources live in "
            "[Enforcement Actions](enforcement-actions.md); congressional connections only in `trackers/linkages.yaml`.", ""]
    return "\n".join(out)


def main() -> int:
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8")) or {}
    targets = cfg.get("targets", [])
    keywords = [k.lower() for k in cfg.get("keywords", [])]

    rows: list[dict] = []
    ok, failed = [], []
    for name, fn in (("DOJ RSS", doj_rss), ("BIS", bis_listing), ("OFAC", ofac_listing)):
        try:
            got = fn()
            rows += got
            ok.append(f"{name} ({len(got)})")
            print(f"  ✓ {name}: {len(got)} rows")
        except Exception as exc:  # noqa: BLE001
            failed.append(name)
            print(f"  ⚠ {name}: {exc}")

    resolved = []
    for t in targets:
        r = _match_target(t, rows)
        if not r and t.get("agency") == "DOJ" and t.get("search"):
            try:
                r = _match_target(t, doj_search(t["search"]))
            except Exception as exc:  # noqa: BLE001
                print(f"  ⚠ DOJ search '{t['search']}': {exc}")
        print(f"  {'✓' if r else '○'} {t['id']}: {r['url'] if r else 'not found'}")
        resolved.append({**t, "resolved": r})

    scan = []
    for r in rows:
        tl = r["title"].lower()
        m = [k for k in keywords if k in tl]
        if m:
            scan.append({**r, "matched_keywords": m})
    print(f"  ✓ scan: {len(scan)} of {len(rows)} releases matched")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sources_ok": ok, "sources_failed": failed,
        "keywords": keywords, "targets": resolved, "scan": scan,
    }
    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    DATA_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    PAGE_OUT.parent.mkdir(parents=True, exist_ok=True)
    PAGE_OUT.write_text(render_page(payload), encoding="utf-8")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        found = sum(1 for t in resolved if t.get("resolved"))
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(f"### Agency releases: {found}/{len(resolved)} targets resolved, {len(scan)} scan hits; sources ok: {', '.join(ok)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
