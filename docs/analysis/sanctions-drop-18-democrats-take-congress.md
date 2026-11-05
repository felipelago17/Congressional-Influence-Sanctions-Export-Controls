# Reading note — "Democrats Take Congress. What's Next for US Sanctions and Export Controls?"

**Source:** Nick Turner, *The Sanctions Drop*, Issue #18, 4 November 2026 — [sanctionsdrop.substack.com](https://sanctionsdrop.substack.com/p/democrats-take-congress-whats-next)

**Source tier:** Tier 3 (labeled secondary commentary). This note summarises the author's analysis in this repository's own words; it is not a basis for any linkage grade on its own. Each item below lists the primary source that would be needed before it is promoted to a tracker entry.

**Not legal advice.** The views summarised are the author's.

---

## Headline argument

The piece reads the 2026 midterm result (Democratic control of both chambers) as a shift in *oversight capacity* rather than *legislative capacity* on sanctions and export controls. Most bills still need Republican votes to clear a Senate filibuster, and reversing an executive action by statute needs a two-thirds veto override in both chambers. Where Democrats do gain real room is in hearings, letters, confirmations and the annual NDAA.

This maps cleanly onto the levers in [Administration Levers](../influence/administration-levers.md): the expected effect is concentrated in **oversight** and **statutory mandates via NDAA**, not in stand-alone sanctions legislation.

## Four threads the author flags

### 1. Lame-duck session of the 119th Congress — NDAA and RASA

- The House passed its FY2027 NDAA on 22 July 2026; a Senate procedural vote failed on 14 July 2026, so the Senate has not taken up its own version.
- Neither chamber's text fundamentally reshapes sanctions or export controls. Both extend the DoD Section 1260H "Chinese military companies" list mandate by five years (2030 → 2035) and add procurement restrictions.
- The Remote Access Security Act (H.R. 2683, already on the [watchlist](../trackers/congress-signals.md)) could ride on the NDAA via a proposed Senate amendment. If that fails, it dies sine die on 3 January 2027 and must be reintroduced in the 120th Congress.

*Repository relevance:* confirms the sine-die risk already recorded for `rasa-hr2683-119`. An NDAA amendment, if adopted, would be a new signal and a candidate `statutory-mandate` linkage to any later BIS remote-access rule.

*Primary sources needed:* Congress.gov record for the FY2027 NDAA (House-passed text, Senate cloture vote of 14 July 2026, and any Senate amendment text attaching RASA).

### 2. Russia — Graham Act waiver and the diesel deal

- The Lindsey O. Graham Sanctioning Russia and Iran Act of 2026 was signed on 18 September 2026 (House 262-159; Senate 86-11). It mandated new Russia sanctions and steep tariffs on Russian goods and on major buyers/facilitators of Russian oil.
- On 16 October 2026 the President waived most of those sanctions and tariffs under Section 115, following a 9 October deal allowing Russian diesel imports and sales until April 2027, implemented through OFAC General License 135.
- The Act contains no mechanism for Congress to terminate a waiver. Two House proposals would bar OFAC from authorising Russian energy transactions and nullify GL 135. The author expects hearings and letters, not enacted legislation, absent a broader deal.

*Repository relevance:* a textbook case for the methodology — a `statutory-mandate` (the Act) followed by an executive waiver the statute itself permits. Any congressional response should be logged as **oversight** signals, with linkage to OFAC action graded only if OFAC documents cite Congress.

*Primary sources needed:* Public Law citation and Congress.gov roll calls; the 16 October 2026 executive order (Federal Register); OFAC GL 135 and accompanying FAQ; Congress.gov entries for the two House proposals.

### 3. China Select Committee — reauthorisation

- The House Select Committee on the CCP (created January 2023, reauthorised January 2025) must be renewed each Congress. It cannot legislate but shapes attention and bill drafting on advanced computing, AI and supply-chain controls.
- Renewal under a Democratic House is not confirmed. The presumptive chair, Rep. Ro Khanna, has not committed. The author thinks its bipartisan record makes renewal likely, but notes Democrats could instead fold its remit into broader oversight of China sanctions and export-control implementation.

*Repository relevance:* committee existence and chair changes are tracked as contextual inputs in [Election Cycles](../influence/election-cycles.md). No inference is drawn from a chair change alone.

*Primary sources needed:* House rules package / resolution for the 120th Congress (January 2027).

### 4. FinCEN and the Corporate Transparency Act

- FinCEN suspended CTA enforcement in March 2025, then on 14 August 2026 issued a final rule exempting US companies and US persons from beneficial-ownership reporting — removing, per GAO, more than 99 percent of expected filers. Senators Grassley and Whitehouse objected that the rule undercuts the statute's intent.
- On 27 October 2026, attorneys general from 20 states and DC sued FinCEN in federal court in Oregon to block the exemptions and halt the purge of more than 16 million records.
- The author doubts Congress will overturn the rule (House Financial Services advanced a CTA *repeal* bill earlier in 2026), but expects hearings to press FinCEN on consistency with congressional intent.

*Repository relevance:* candidate entry for `trackers/regulations-under-discussion.yaml` using the multi-status fields (published 14 August 2026; in force; litigation pending). The Grassley–Whitehouse statement is a documented congressional signal; whether FinCEN's rule cites Congress is what determines any grade above `proximity-only`.

*Primary sources needed:* Federal Register citation for the 14 August 2026 final rule; the state AG complaint (D. Or.); GAO figure source; Congress.gov entry for the repeal bill.

## What this changes for the repository's "current baseline"

| Item | Before this note | After this note |
|------|------------------|-----------------|
| Chamber control, 120th Congress | Not recorded | Democratic House and Senate from 3 January 2027 (per secondary source; to be confirmed against official certified results) |
| RASA sine-die risk | Recorded | Unchanged; NDAA-rider path noted |
| Graham Act / GL 135 | Not recorded | Follow-up items opened (see below) |
| CTA exemption rule | Not recorded | Follow-up items opened (see below) |

## Follow-up items (to be added to trackers only with Tier 1 sources)

- [ ] `signals.yaml`: FY2027 NDAA (House-passed; Senate cloture failed 14 July 2026) and any RASA amendment.
- [ ] `signals.yaml`: Graham Act (enacted 18 September 2026) with roll calls and party aggregates.
- [ ] `signals.yaml`: the two House proposals targeting OFAC Russian-energy authorisations / GL 135.
- [ ] `regulations-under-discussion.yaml`: FinCEN CTA exemption final rule (14 August 2026) with litigation status.
- [ ] `linkages.yaml`: Graham Act → 16 October 2026 waiver EO, grade `statutory-mandate` (the statute authorises the waiver under s.115).
- [ ] `election-cycles.md`: confirm chamber control and committee chairs from official sources once the 120th Congress organises.
