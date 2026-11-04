# Contributing

This repository is open for contributions. All changes to tracker data must go through a pull request.

## How to contribute

1. Fork the repository.
2. Create a branch for your change.
3. Add or update entries in `trackers/*.yaml` following the existing schema and linkage-grade rules.
4. Include at least one primary-source URL for every new signal or action.
5. Open a pull request against `main`.

## Rules

- Aggregate by party and committee only. Do not add per-member scorecards.
- Linkage grades must be one of: `statutory-mandate`, `documented-request`, `proximity-only`.
- Proximity-only entries must explicitly state that no inference is drawn.
- Regulatory items must use the multi-status fields (`scheduled` / `announced` / `published` / `in-force`).
- Do not commit unpublished specific license data.

## Daily digest

`news/digest.md` may receive automated updates. Do not manually edit it unless correcting an error; open a PR instead.

Thank you for helping keep the record accurate and source-backed.
