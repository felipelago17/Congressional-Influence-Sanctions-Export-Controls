# Congressional Influence on Sanctions and Export Controls

Evidence-based framework mapping **public congressional signals** (bills, riders, letters, hearing questions, holds, mandatory reports) to **public administration actions** on sanctions, export controls, OFAC guidance, BIS rules, and related financial-crime/regulatory compliance matters.

Elections and party control are inputs, not the subject of the repository.

**This repository is for informational and academic purposes only. It does not constitute legal advice.** Always consult qualified export-control and sanctions counsel before taking any compliance decision.

---

## Core Principles

- **Signals and actions, not “influence.”**  
  The unit of analysis is a documented *signal* and a documented *action*. Any connection appears only in a graded `linkage` field:

  | Grade | Meaning |
  |-------|---------|
  | `statutory-mandate` | Statute or binding requirement (e.g., CAATSA, ECRA, specific NDAA provision) |
  | `documented-request` | Agency cites Congress, member letter, GAO/CRS report, or hearing record |
  | `proximity-only` | Temporal or topical proximity with no direct evidence; **no inference is drawn** |

- **Public scope only.**  
  OFAC general licenses, FAQs, enforcement releases, and interpretive guidance. BIS annual aggregates and public actions. No unpublished specific licenses.

- **Aggregation, not scorecards.**  
  Party and committee totals only. Roll calls are linked. No per-member rankings or scorecards.

- **Status is multi-field.**  
  Every regulatory item carries separate `scheduled` / `announced` / `published` / `in-force` fields. An announcement is not a Federal Register notice.

- **No duplication.**  
  This repository owns Congress.gov, the Congressional Record, LDA filings, committee pages, GAO/CRS/OIG reports, and nominee holds. It consumes (does not re-scrape) OFAC, BIS, and Federal Register outputs from the companion repositories.

---

## Open source collaboration

This repository is open for contributions.

Fork it, make your changes, and open a pull request. Tracker rows are added only via pull request after review.

[Fork the repository](https://github.com/felipelago17/Congressional-Influence-Sanctions-Export-Controls/fork)

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## What This Repository Contains

- `docs/` — MkDocs source (methodology, influence pages)
- `trackers/` — YAML trackers for signals, regulations under discussion, and linkages
- `news/digest.md` — Daily digest (automated updates only)
- `.github/workflows/` — Deploy and daily digest workflows

Public site: https://felipelago17.github.io/Congressional-Influence-Sanctions-Export-Controls/
