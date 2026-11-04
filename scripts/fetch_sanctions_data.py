#!/usr/bin/env python3
"""Pull sanctions / export-control list statistics from OpenSanctions bulk data.

For each dataset: entity count, last change, and the targets first seen in the
last N days (new designations / listings). Uses the public bulk exports —
no API key required. Data © OpenSanctions (CC BY-NC 4.0); attribution kept on
the generated page.

Outputs:
  data/sanctions-summary.json
  docs/trackers/sanctions-data.md
"""
from __future__ import annotations

import csv
import io
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_OUT = ROOT / "data" / "sanctions-summary.json"
PAGE_OUT = ROOT / "docs" / "trackers" / "sanctions-data.md"

BASE = "https://data.opensanctions.org/datasets/latest"
DATASETS = [
    ("us_ofac_sdn", "OFAC Specially Designated Nationals (SDN)"),
    ("us_ofac_cons", "OFAC Consolidated (non-SDN) List"),
    ("us_bis_denied", "BIS Denied Persons List"),
    ("us_trade_csl", "Consolidated Screening List (Commerce/State/Treasury)"),
]
NEW_DAYS = int(os.environ.get("SANCTIONS_NEW_DAYS", "7"))
MAX_ROWS = 60
TIMEOUT = 60


def _fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "congressional-influence-tracker/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def _find_resource(index: dict, name: str) -> str | None:
    for r in index.get("resources", []):
        if r.get("name") == name:
            return r.get("url")
    return None


def fetch_dataset(slug: str) -> dict:
    index = json.loads(_fetch(f"{BASE}/{slug}/index.json"))
    out = {
        "slug": slug,
        "entity_count": index.get("entity_count") or index.get("target_count"),
        "target_count": index.get("target_count"),
        "last_change": index.get("last_change"),
        "last_export": index.get("last_export"),
        "publisher_url": (index.get("publisher") or {}).get("url"),
        "new_targets": [],
    }
    csv_url = _find_resource(index, "targets.simple.csv")
    if not csv_url:
        return out
    cutoff = (datetime.now(timezone.utc) - timedelta(days=NEW_DAYS)).strftime("%Y-%m-%d")
    text = _fetch(csv_url).decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    new = []
    for row in reader:
        fs = (row.get("first_seen") or "")[:10]
        if fs and fs >= cutoff:
            new.append({
                "name": row.get("name"),
                "schema": row.get("schema"),
                "countries": row.get("countries"),
                "first_seen": fs,
                "programs": (row.get("sanctions") or "")[:120],
                "id": row.get("id"),
            })
    new.sort(key=lambda r: (r["first_seen"], r["name"] or ""), reverse=True)
    out["new_target_count"] = len(new)
    out["new_targets"] = new[:MAX_ROWS]
    return out


def render_page(payload: dict) -> str:
    gen = payload["generated_at"][:16].replace("T", " ") + " UTC"
    out = [
        "# Sanctions and export-control lists (OpenSanctions)",
        "",
        f"*Auto-generated {gen}. Statistics and new listings from "
        "[OpenSanctions](https://www.opensanctions.org/) bulk data (CC BY-NC 4.0), which mirrors the "
        "official OFAC and BIS publications. Always verify against the issuing agency before acting. Not legal advice.*",
        "",
        "## List statistics",
        "",
        "| List | Entities | Last change | New in last %d days |" % payload["new_days"],
        "|---|---|---|---|",
    ]
    for d in payload["datasets"]:
        if d.get("error"):
            out.append(f"| {d['label']} | — | — | ⚠ {d['error']} |")
            continue
        out.append(f"| [{d['label']}](https://www.opensanctions.org/datasets/{d['slug']}/) | "
                   f"{d.get('entity_count') or '—'} | {(d.get('last_change') or '')[:10] or '—'} | "
                   f"{d.get('new_target_count', 0)} |")
    for d in payload["datasets"]:
        if not d.get("new_targets"):
            continue
        out += ["", f"## New in {d['label']} (last {payload['new_days']} days)", "",
                "| First seen | Name | Type | Countries | Programs |", "|---|---|---|---|---|"]
        for r in d["new_targets"]:
            out.append(f"| {r['first_seen']} | [{r['name']}](https://www.opensanctions.org/entities/{r['id']}/) | "
                       f"{r['schema']} | {r['countries'] or ''} | {r['programs']} |")
        if d.get("new_target_count", 0) > MAX_ROWS:
            out.append(f"\n_Showing {MAX_ROWS} of {d['new_target_count']}._")
    out += ["", "---",
            "Designation volume is an **action** metric. It is never read as evidence of congressional influence "
            "unless a [graded linkage](../methodology/linkage-grades.md) is documented.", ""]
    return "\n".join(out)


def main() -> int:
    results = []
    for slug, label in DATASETS:
        try:
            d = fetch_dataset(slug)
            d["label"] = label
            print(f"  ✓ {slug}: {d.get('entity_count')} entities, {d.get('new_target_count', 0)} new")
        except Exception as exc:  # noqa: BLE001
            d = {"slug": slug, "label": label, "error": str(exc)[:120]}
            print(f"  ⚠ {slug}: {exc}")
        results.append(d)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "new_days": NEW_DAYS,
        "datasets": results,
    }
    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    DATA_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    PAGE_OUT.parent.mkdir(parents=True, exist_ok=True)
    PAGE_OUT.write_text(render_page(payload), encoding="utf-8")
    ok = sum(1 for d in results if not d.get("error"))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(f"### OpenSanctions: {ok}/{len(results)} datasets refreshed\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
