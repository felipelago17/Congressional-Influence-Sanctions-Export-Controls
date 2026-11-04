#!/usr/bin/env python3
"""Pull congressional signals from the official Congress.gov API (v3).

Two passes:
1. Watchlist — bills listed in trackers/bill-watchlist.yaml: latest action,
   sponsor party, cosponsor party counts (aggregates only, no member names).
2. Scan — bills updated in the last N days whose title matches any keyword in
   the watchlist file's `keywords` list.

Requires CONGRESS_API_KEY (free key: https://api.congress.gov/sign-up/).
Without a key the script writes nothing and exits 0 with a warning so the
scheduled job does not fail before the secret is configured.

Outputs:
  data/congress-signals.json
  docs/trackers/congress-signals.md
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WATCHLIST = ROOT / "trackers" / "bill-watchlist.yaml"
DATA_OUT = ROOT / "data" / "congress-signals.json"
PAGE_OUT = ROOT / "docs" / "trackers" / "congress-signals.md"

API = "https://api.congress.gov/v3"
KEY = os.environ.get("CONGRESS_API_KEY", "").strip()
SCAN_DAYS = int(os.environ.get("CONGRESS_SCAN_DAYS", "7"))
TIMEOUT = 30


def _get(path: str, **params) -> dict:
    params = {"api_key": KEY, "format": "json", **params}
    url = f"{API}/{path.lstrip('/')}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "congressional-influence-tracker/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise
    return {}


def _party_counts(members: list[dict]) -> dict:
    return dict(sorted(Counter((m.get("party") or "?") for m in members).items()))


def _bill_url(congress: int, btype: str, number: int) -> str:
    names = {
        "hr": "house-bill", "s": "senate-bill", "hjres": "house-joint-resolution",
        "sjres": "senate-joint-resolution", "hres": "house-resolution", "sres": "senate-resolution",
        "hconres": "house-concurrent-resolution", "sconres": "senate-concurrent-resolution",
    }
    return f"https://www.congress.gov/bill/{congress}th-congress/{names.get(btype, btype)}/{number}"


def fetch_watch_bill(entry: dict) -> dict:
    c, t, n = int(entry["congress"]), str(entry["type"]).lower(), int(entry["number"])
    bill = _get(f"bill/{c}/{t}/{n}").get("bill", {})
    cos: list[dict] = []
    offset = 0
    while True:
        page = _get(f"bill/{c}/{t}/{n}/cosponsors", limit=250, offset=offset)
        cos.extend(page.get("cosponsors", []))
        if len(page.get("cosponsors", [])) < 250:
            break
        offset += 250
    la = bill.get("latestAction") or {}
    return {
        "id": entry.get("id") or f"{t}{n}-{c}",
        "label": entry.get("label") or bill.get("title"),
        "congress": c,
        "number": f"{t.upper()}.{n}" if t in ("hr", "s") else f"{t.upper()} {n}",
        "title": bill.get("title"),
        "introduced": bill.get("introducedDate"),
        "latest_action_date": la.get("actionDate"),
        "latest_action": la.get("text"),
        "sponsor_party_counts": _party_counts(bill.get("sponsors", [])),
        "cosponsor_party_counts": _party_counts(cos),
        "cosponsor_total": len(cos),
        "policy_area": (bill.get("policyArea") or {}).get("name"),
        "committees_url": (bill.get("committees") or {}).get("url"),
        "url": _bill_url(c, t, n),
    }


def scan_recent(keywords: list[str], days: int) -> list[dict]:
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")
    kws = [k.lower() for k in keywords]
    hits: list[dict] = []
    offset = 0
    while offset < 1000:  # hard cap: 4 pages
        page = _get("bill", fromDateTime=since, sort="updateDate+desc", limit=250, offset=offset)
        bills = page.get("bills", [])
        for b in bills:
            title = (b.get("title") or "")
            tl = title.lower()
            matched = [k for k in kws if k in tl]
            if not matched:
                continue
            la = b.get("latestAction") or {}
            hits.append({
                "congress": b.get("congress"),
                "number": f"{b.get('type')}.{b.get('number')}",
                "title": title,
                "latest_action_date": la.get("actionDate"),
                "latest_action": la.get("text"),
                "matched_keywords": matched,
                "url": _bill_url(int(b.get("congress", 0)), str(b.get("type", "")).lower(), int(b.get("number", 0))),
            })
        if len(bills) < 250:
            break
        offset += 250
    return hits


def render_page(payload: dict) -> str:
    gen = payload["generated_at"][:16].replace("T", " ") + " UTC"
    out = [
        "# Congressional signals (Congress.gov API)",
        "",
        f"*Auto-generated {gen} from the official [Congress.gov API](https://api.congress.gov/). "
        "Aggregate party counts only — no per-member scorecards. Not legal advice.*",
        "",
        "## Watchlist",
        "",
        "| Bill | Title | Latest action | Sponsor | Cosponsors by party | Total |",
        "|---|---|---|---|---|---|",
    ]
    for b in payload["watchlist"]:
        sp = ", ".join(f"{k} {v}" for k, v in b["sponsor_party_counts"].items()) or "—"
        cp = ", ".join(f"{k} {v}" for k, v in b["cosponsor_party_counts"].items()) or "—"
        la = f"{b.get('latest_action_date') or ''} — {b.get('latest_action') or ''}".strip(" —")
        out.append(f"| [{b['number']}]({b['url']}) ({b['congress']}th) | {b.get('title') or ''} | {la} | {sp} | {cp} | {b['cosponsor_total']} |")
    out += [
        "",
        f"## Keyword scan — bills updated in the last {payload['scan_days']} days",
        "",
        f"Keywords: {', '.join('`' + k + '`' for k in payload['keywords'])}",
        "",
    ]
    if payload["scan"]:
        out += ["| Bill | Title | Latest action | Matched |", "|---|---|---|---|"]
        for b in payload["scan"]:
            la = f"{b.get('latest_action_date') or ''} — {b.get('latest_action') or ''}".strip(" —")
            out.append(f"| [{b['number']}]({b['url']}) | {b['title']} | {la} | {', '.join(b['matched_keywords'])} |")
    else:
        out.append("_No title matches in this window._")
    out += [
        "",
        "---",
        "Signals are facts about congressional activity. Any connection to an administration action is "
        "recorded separately in `trackers/linkages.yaml` with a [linkage grade](../methodology/linkage-grades.md).",
        "",
    ]
    return "\n".join(out)


def main() -> int:
    if not KEY:
        print("::warning::CONGRESS_API_KEY is not set – skipping Congress.gov fetch. "
              "Add it under Settings → Secrets and variables → Actions.")
        return 0
    wl = yaml.safe_load(WATCHLIST.read_text(encoding="utf-8")) or {}
    bills = wl.get("bills", [])
    keywords = wl.get("keywords", [])

    watch_out = []
    for e in bills:
        try:
            watch_out.append(fetch_watch_bill(e))
            print(f"  ✓ {e.get('label') or e}")
        except Exception as exc:  # noqa: BLE001
            print(f"  ⚠ {e.get('label') or e}: {exc}")
    try:
        scan = scan_recent(keywords, SCAN_DAYS)
        print(f"  ✓ keyword scan: {len(scan)} hit(s)")
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ keyword scan failed: {exc}")
        scan = []

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "https://api.congress.gov/v3",
        "scan_days": SCAN_DAYS,
        "keywords": keywords,
        "watchlist": watch_out,
        "scan": scan,
    }
    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    DATA_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    PAGE_OUT.parent.mkdir(parents=True, exist_ok=True)
    PAGE_OUT.write_text(render_page(payload), encoding="utf-8")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(f"### Congress.gov: {len(watch_out)} watchlist bills refreshed, {len(scan)} keyword hits\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
