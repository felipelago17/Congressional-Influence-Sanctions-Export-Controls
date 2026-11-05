# Congressional Influence on Sanctions and Export Controls

**Status as of 4 November 2026**

Evidence-based framework mapping **public congressional signals** (bills, riders, letters, hearing questions, holds, mandatory reports) to **public administration actions** on sanctions, export controls, OFAC guidance, BIS rules, and related financial-crime/regulatory compliance matters.

Elections and party control are inputs, not the subject of this site.

**Not legal advice.** This site is for informational and academic purposes only. Always consult qualified export-control and sanctions counsel before taking any compliance decision.

---

## Purpose

This repository documents publicly available congressional signals and administration actions for research and academic reference.

It is not affiliated with any political party, candidate, government, or agency.

Every entry includes:
- At least one primary-source link (Congress.gov, Federal Register, official statement, etc.)
- A graded linkage only where documentary evidence supports it

## Contents

- [Linkage Grades](methodology/linkage-grades.md) — How connections are graded (`statutory-mandate` / `documented-request` / `proximity-only`)
- [Source Hierarchy](methodology/source-hierarchy.md)
- [Administration Levers](influence/administration-levers.md)
- [Party and Committee Aggregates](influence/party-committee-aggregates.md)
- [Election Cycles](influence/election-cycles.md)
- [OFAC and Tariffs](ofac-tariffs/index.md) — where sanctions and trade remedies meet: legal framework, [case studies](ofac-tariffs/case-studies.md) (EO 14245, India, *Learning Resources*, Graham Act and waiver), [research list](ofac-tariffs/research.md)
- [Congressional Signals](trackers/congress-signals.md) — auto-refreshed daily from the Congress.gov API (watchlist + keyword scan)
- [Sanctions Lists](trackers/sanctions-data.md) — OFAC/BIS list statistics and new listings, daily via OpenSanctions
- [Enforcement Actions](trackers/enforcement-actions.md) — DOJ NSD / OFAC / BIS resolutions and AI-chip diversion prosecutions, 2025–26 (22 entries; hand-curated, primary sources)
- Trackers (YAML): `trackers/signals.yaml`, `trackers/enforcement-actions.yaml`, `trackers/regulations-under-discussion.yaml`, `trackers/linkages.yaml`, `trackers/bill-watchlist.yaml`
- Analysis — reading notes on labeled secondary commentary (Tier 3), with the primary sources each item still needs: [Sanctions Drop #18](analysis/sanctions-drop-18-democrats-take-congress.md) · [Dow Jones Risk Journal, 4 Nov 2026](analysis/dj-risk-journal-tweaks-not-major-change.md) · [Al Jazeera, 4 Nov 2026](analysis/aljazeera-democrats-win-congress.md)
- [Daily digest](news/digest.md)

## Current baseline (November 2026)

| Item | Status |
|------|--------|
| BIS Affiliates Rule | Formal reimposition still scheduled for 10 November 2026. Extension to 10 January 2027 announced; no implementing Federal Register notice yet. |
| Remote Access Security Act (H.R. 2683) | Passed House 369-22 on 12 January 2026. Referred to Senate Banking. 119th Congress ends 3 January 2027. |
| Graham Act (Pub. L. 119-111) | Enacted 18 September 2026. Tariffs and new sanctions set by EO of 16 October 2026 and waived the same day under §115 (EO 14436, 91 FR 66627); waivers open-ended. `statutory-mandate` linkage recorded. |
| IEEPA tariffs | Foreclosed by *Learning Resources v. Trump* (20 February 2026). Sanctions powers under IEEPA unaffected. |

## Methodology

- **Signals and actions, not “influence.”** Connections appear only in a graded `linkage` field. Temporal proximity alone is never sufficient.
- **Public scope only.** No unpublished specific licenses.
- **Aggregation, not scorecards.** Party and committee totals only. No per-member rankings.
- **Multi-status fields.** Every regulatory item carries separate `scheduled` / `announced` / `published` / `in-force` fields.

See [Linkage Grades](methodology/linkage-grades.md) for definitions and examples.

## Open source collaboration

This repository is open for contributions.

Fork it, make your changes, and open a pull request. Tracker rows are added only via pull request after review.

[Fork the repository](https://github.com/felipelago17/Congressional-Influence-Sanctions-Export-Controls/fork)

See [CONTRIBUTING.md](https://github.com/felipelago17/Congressional-Influence-Sanctions-Export-Controls/blob/main/CONTRIBUTING.md) for guidelines.

## Disclaimer

This repository is for educational and informational purposes only. Always verify against primary sources. It does not constitute legal advice.
