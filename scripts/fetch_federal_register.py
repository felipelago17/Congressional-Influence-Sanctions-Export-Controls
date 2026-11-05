#!/usr/bin/env python3
"""Pull presidential documents (executive orders, proclamations, memoranda) on
sanctions, tariffs and export controls from the Federal Register API.

The API is public and keyless: https://www.federalregister.gov/developers/documentation/api/v1
Content is public domain.

Two passes:
1. Targets — specific documents listed in trackers/presidential-documents.yaml
   that the repository needs citations for (matched by signing date + title
   keyword). Resolves "Federal Register citation to be added" gaps.
2. Scan — all presidential documents since SCAN_FROM whose title matches any
   keyword in the same file.

Outputs:
  data/presidential-documents.json
  docs/trackers/presidential-documents.md
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "trackers" / "presidential-documents.yaml"
DATA_OUT = ROOT / "data" / "presidential-documents.json"
PAGE_OUT = ROOT / "docs" / "trackers" / "presidential-documents.md"

API = "https://www.federalregister.gov/api/v1/documents.json"
TIMEOUT = 30
FIELDS = [
    "document_number", "title", "type", "subtype", "executive_order_number",
    "signing_date", "publication_date", "citation", "html_url", "pdf_url",
]


def _get(params: dict) -> dict:
    q = []
    for k, v in params.items():
        if isinstance(v, list):
            q += [(k, x) for x in v]
        else:
            q.append((k, v))
    url = f"{API}?{urllib.parse.urlencode(q)}"
    req = urllib.request.Request(url, headers={"User-Agent": "congressional-influence-tracker/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 503) and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise RuntimeError(f"HTTP {exc.code} from Federal Register: {exc.reason}") from None
    return {}


def _slim(d: dict) -> dict:
    return {k: d.get(k) for k in FIELDS}


def search(term: str | None, date_from: str, date_to: str | None = None, per_page: int = 100) -> list[dict]:
    params = {
        "conditions[type][]": "PRESDOCU",
        "conditions[publication_date][gte]": date_from,
        "per_page": per_page,
        "order": "newest",
        "fields[]": FIELDS,
    }
    if date_to:
        params["conditions[publication_date][lte]"] = date_to
    if term:
        params["conditions[term]"] = term
    out: list[dict] = []
    page = 1
    while page <= 10:
        params["page"] = page
        data = _get(params)
        results = data.get("results", [])
        out += [_slim(r) for r in results]
        if page >= int(data.get("total_pages") or 1):
            break
        page += 1
    return out


def resolve_target(t: dict) -> dict | None:
    """Find a specific document by signing date window and title keywords."""
    sd = t["signing_date"]
    # Publication follows signing by a few days; search from the signing date onward
    # and filter on exact signing_date plus title keywords.
    cands = search(t.get("term"), sd)
    kws = [k.lower() for k in t.get("title_keywords", [])]
    for c in cands:
        if c.get("signing_date") != sd:
            continue
        title = (c.get("title") or "").lower()
        if all(k in title for k in kws):
            return c
    # fallback: any doc signed on that date whose title has at least one keyword
    for c in cands:
        if c.get("signing_date") == sd and any(k in (c.get("title") or "").lower() for k in kws):
            return c
    return None


def render_page(payload: dict) -> str:
    gen = payload["generated_at"][:16].replace("T", " ") + " UTC"
    out = [
        "# Presidential documents (Federal Register API)",
        "",
        f"*Auto-generated {gen} from the [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1). "
        "Executive orders, proclamations and memoranda on sanctions, tariffs and export controls. Public-domain content. Not legal advice.*",
        "",
        "## Resolved citations (targets)",
        "",
        "Documents the repository's trackers and case studies refer to. Once resolved here, the citation is authoritative.",
        "",
        "| Target | Signed | EO No. | FR citation | Published | Title | Links |",
        "|---|---|---|---|---|---|---|",
    ]
    for t in payload["targets"]:
        d = t.get("resolved")
        if d:
            eo = d.get("executive_order_number") or "—"
            links = f"[FR]({d['html_url']})" + (f" · [PDF]({d['pdf_url']})" if d.get("pdf_url") else "")
            out.append(f"| {t['id']} | {d.get('signing_date') or ''} | {eo} | {d.get('citation') or '—'} | {d.get('publication_date') or ''} | {d.get('title') or ''} | {links} |")
        else:
            out.append(f"| {t['id']} | {t['signing_date']} | — | _not yet found_ | — | {t.get('label','')} | — |")
    out += [
        "",
        f"## Keyword scan — presidential documents published since {payload['scan_from']}",
        "",
        f"Keywords: {', '.join('`' + k + '`' for k in payload['keywords'])}",
        "",
    ]
    if payload["scan"]:
        out += ["| Signed | Type | EO No. | FR citation | Title | Matched |", "|---|---|---|---|---|---|"]
        for d in payload["scan"]:
            typ = d.get("subtype") or d.get("type") or ""
            out.append(f"| {d.get('signing_date') or d.get('publication_date') or ''} | {typ} | {d.get('executive_order_number') or '—'} | "
                       f"[{d.get('citation') or d.get('document_number')}]({d.get('html_url')}) | {d.get('title') or ''} | {', '.join(d.get('matched_keywords', []))} |")
    else:
        out.append("_No title matches._")
    out += [
        "",
        "---",
        "Presidential documents are administration actions. Any connection to a congressional signal is recorded in "
        "`trackers/linkages.yaml` with a [linkage grade](../methodology/linkage-grades.md).",
        "",
    ]
    return "\n".join(out)


def main() -> int:
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8")) or {}
    targets = cfg.get("targets", [])
    keywords = [k.lower() for k in cfg.get("keywords", [])]
    scan_from = cfg.get("scan_from", "2025-01-20")

    resolved = []
    for t in targets:
        try:
            d = resolve_target(t)
            print(f"  {'✓' if d else '○'} {t['id']}: {d.get('citation') if d else 'not found'}")
            resolved.append({**t, "resolved": d})
        except Exception as exc:  # noqa: BLE001
            print(f"  ⚠ {t['id']}: {exc}")
            resolved.append({**t, "resolved": None})

    scan: list[dict] = []
    try:
        allpd = search(None, scan_from)
        for d in allpd:
            tl = (d.get("title") or "").lower()
            m = [k for k in keywords if k in tl]
            if m:
                scan.append({**d, "matched_keywords": m})
        print(f"  ✓ scan: {len(scan)} of {len(allpd)} presidential documents matched")
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ scan failed: {exc}")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": API,
        "scan_from": scan_from,
        "keywords": keywords,
        "targets": resolved,
        "scan": scan,
    }
    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    DATA_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    PAGE_OUT.parent.mkdir(parents=True, exist_ok=True)
    PAGE_OUT.write_text(render_page(payload), encoding="utf-8")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        found = sum(1 for t in resolved if t.get("resolved"))
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(f"### Federal Register: {found}/{len(resolved)} targets resolved, {len(scan)} scan hits\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
