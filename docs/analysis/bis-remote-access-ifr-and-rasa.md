# Reading note — BIS remote-access interim final rule while the Remote Access Security Act is pending (16–18 Nov 2026)

**Sources (all paraphrased; no article text reproduced):**

- Paul Hastings LLP, "US Department of Commerce Issues Regulations to Restrict Remote Cloud Access", client alert, 17 Nov 2026 — https://www.paulhastings.com/thought-leadership/us-department-of-commerce-issues-regulations — **Tier 3** (law-firm alert; read via a fetch summary, not line by line)
- BIS press release and display copy of the interim final rule (RIN 0694-AK50), 16 Nov 2026, as summarised in the sibling repository's case note — **Tier 1/2 in the original; not re-read for this note** (the IFR is a pre-publication draft; Federal Register publication was expected 19 Nov per Paul Hastings)
- Congress.gov entries for H.R. 2683 and S. 3519, as recorded in [Congressional Signals](../trackers/congress-signals.md) — **Tier 1** (not re-queried today)

**Not legal advice.** Rule detail is provisional until the Federal Register text is published.

---

## Why this note exists

The [FY2027 NDAA note](fy27-ndaa-ai-chip-export-bills.md) said that if the Remote Access Security Act (RASA) were dropped, a BIS remote-access rule would have to be graded against a bill that had not become law. BIS has now released that rule, **while RASA is still pending** (House-passed 369–22 on 12 Jan 2026; referred to Senate Banking). This note records the administrative action and what it does and does not change for the congressional record.

## 1. What the rule does (per Paul Hastings; Tier 3)

- Creates a licence requirement under 15 C.F.R. § 744.24 for exports, reexports or in-country transfers of advanced computing items to data centres that give Macau- or Country Group D:5-headquartered companies access above **12,000,000 aggregate TPP** (the firm estimates about 98 GB300 GPUs). Because it hangs on an export, it reaches overseas data centres, not US ones.
- Adds licence requirements for advanced semiconductors going to **Indonesia, Malaysia, Singapore, Thailand and Brazil**, with an exemption for US-headquartered end users that file monthly reports.
- Adds KYC expectations: refusal or inability to give ownership information presumptively establishes knowledge.
- Gives BIS "is-informed" authority and lets the State Department and the National Security Advisor flag high-risk destinations.
- Repeals the Biden-era AI Diffusion Rule's worldwide restrictions, replacing them with country-specific licensing.
- Takes effect on Federal Register publication (expected 19 Nov); comments due 60 days later; existing operators serving covered customers need a licence within 90 days.

## 2. Congressional signals it sits beside (aggregated by party and committee)

| Signal | Status | Source tier |
|---|---|---|
| RASA (H.R. 2683 / S. 3519) | House-passed 369–22 (12 Jan 2026); in Senate Banking; 119th Congress ends 3 Jan 2027 | Tier 1 (via tracker) |
| NDAA candidate vehicle | Remote-access language still a candidate Senate amendment, not in the House-passed NDAA | Earlier note |
| Bipartisan push on Megaspeed and chip diversion | Letters and statements recorded in the [Nvidia note](nvidia-ceo-resignation-export-controls.md) | Tier 3 |
| Agency statement | [Commerce–DOJ joint statement on Megaspeed](commerce-doj-megaspeed-joint-statement.md), 16–17 Nov | Tier 2 |

## 3. Assessment against the repository's framework

1. **Linkage grade: `proximity-only`.** The rule is topically and temporally close to RASA and to the Megaspeed oversight cycle. Paul Hastings says it rests on **existing EAR authorities**, not on RASA, and the sibling note records the BIS press release saying it was drafted at the direction of Treasury and the National Security Council. No document read cites Congress. **No inference of causation is drawn.** Whether the preamble cites congressional letters or bills has **not been checked**.
2. **It is not a `statutory-mandate`.** RASA is not enacted. The rule is an executive instrument and can be amended or reversed without Congress, unlike statutory text.
3. **It narrows the case for RASA without ending it.** The administrative rule covers the core fact pattern (compute rented to Chinese-headquartered customers). Open questions the firm flags (the meaning of "running" a model; API and token services) are the kind of gap legislation could address, but that is an observation, not a sourced congressional position.
4. **Executive-branch lever.** This is a clear instance of the executive closing a legislative gap by rule; see [Administration Levers](../influence/administration-levers.md). The involvement of State and the National Security Advisor in "is-informed" designations widens the set of agencies able to trigger licensing.
5. **Oversight window.** The rule's comment period (60 days after publication) runs into the new Congress. The Democratic House majority arrives 3 Jan 2027; that is a forward-looking observation, not a finding.

## 4. What would change the assessment

| Development | Where to look | Likely grade |
|---|---|---|
| Federal Register publication and preamble | Federal Register; BIS | `documented-request` only if the preamble cites a congressional letter or bill |
| RASA included in the final NDAA | Conference report | `statutory-mandate` anchor for later rules |
| Member letters on the rule's scope ("running", API services) | Member and committee pages | Signal only; no linkage without an agency reply |
| Is-informed notices naming parties | Federal Register; BIS | `proximity-only` unless a cited request |

## 5. Tracker entry (candidate)

- `bis-remote-access-ifr-2026-11` — executive action; add on Federal Register publication with the citation and date; grade `proximity-only` to `rasa-hr2683-119`; hold until the primary text is read.
