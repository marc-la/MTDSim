---
status: durable
created: 2026-05-28
topic: CTI as data — what ages, what doesn't, what "always updating" actually means
---

# CTI ages — but the methodologically-useful frame is *taxonomy drift*, not "staleness"

## Why this is worth recording

The trigger for this note is concrete and slightly absurd: an audit
handoff was opened to *"reconcile legacy MITRE labels (`stealth`,
`defense-impairment`) against modern Enterprise"* — except those labels
are *current*. TA0005 was renamed from `defense-evasion` to `stealth` on
2026-05-12; TA0112 `defense-impairment` was created 2026-04-14, six
weeks before this note. The GAP's `attack_source: enterprise-attack-19.1`
pin already tracks them, and the build's bundle-derived `tactic_id →
shortname` map remaps the CTID source's `TA0005` to `stealth` at parse
time. There is nothing legacy about the labels and nothing to reconcile;
the handoff was retired by evidence in the same commit as this note.

But Marc's framing of *why* this kind of question arises — "CTI ages,
becomes stale, always needs updating/revising" — is the substantive
thing to sharpen, and the incident's actual shape sharpens it in a way
the original framing didn't. The high-level claim is *partially* true
and *partially* misleading: the version-pin mitigation it implies is
correct; the *implied direction of drift* (artefact lags upstream) is
only half the picture. When an artefact pins to a *moving* upstream
taxonomy, freshness questions invert from "is the data out of date?" to
"is the reader out of date?" — and that is the polarity this handoff
demonstrates, 14-tactic mental model running into a correctly-pinned
15-tactic artefact whose pin had updated three weeks earlier.

## The substance

### The claim, restated

"CTI ages and becomes stale, so the corpus is always needing
updating / revising."

This claim packages four distinct things together. They have different
half-lives, different mitigations, and the right response differs for
each. Conflating them produces either over-engineering ("we must rebuild
the GAP every six months") or under-engineering ("the GAP is fine as-is
forever"). Neither is right.

### What actually ages (and what doesn't)

**1. Taxonomy drift — real, addressable by version pinning *on both
sides*.**
The encoding language of CTI evolves. MITRE ATT&CK adds tactics
(Reconnaissance / Resource Development were added in v8, April 2020),
renames tactics (TA0005 was renamed from `defense-evasion` to `stealth`
on 2026-05-12 in v19 and *split*: the new TA0112 `defense-impairment`
was carved out as a separate semantic — concealment that leaves controls
intact vs. degradation / disabling of controls), and deprecates /
merges techniques. The GAP picked this up automatically because the
build derives its `tactic_id → shortname` map from the pinned ATT&CK
STIX bundle rather than a hard-coded table; the classic-14 table in
`schema.py` survives only as a standalone fallback. The drift is **two-
sided**: the *artefact* can lag behind upstream (mitigation: re-pin,
rebuild) *and* the *reader* can lag behind the artefact's pin
(mitigation: read the version field — the GAP's `attack_source` here —
before assuming what the labels mean). The audit handoff this note
retired is an instance of the second polarity, not the first: 14-tactic
mental model, 15-tactic artefact correctly pinned to a 15-tactic
taxonomy released three weeks earlier. The "anomaly" was on the
reading side. **Half-life:** months to a couple of years on either
side. **Mitigation:** version-pin the artefact; surface the pin's field
name and value at a glance so readers notice when they've drifted.

**2. Incident historicity — does NOT age.**
The fact that "in 2017, NotPetya disrupted Maersk via EternalBlue and
M.E.Doc supply-chain compromise" is permanent historical truth. A 2025
reader using a 2017 incident report learns *the same thing* the 2017
reader learned: how that operation actually unfolded. The CTI isn't
"stale" in the sense that the report has become wrong — it's just
*about an older event*. **Half-life:** infinite (modulo retractions
based on new evidence). **Mitigation:** none needed; treat historical
incident corpora as archival data, not as forecasts.

**3. Operational relevance — degrades, but this is a different
question than "is the data correct".**
What worked for attackers in 2017 may not work today (defender controls
caught up; OS vendors patched; the attacker's tooling evolved). A 2017
breach report is *correct* about 2017 but may *not predict* 2025
attacker behaviour. This is the only sense in which the corpus is
"stale" — its predictive value for current-day operations decays.
**Half-life:** 1–5 years for technique-level operational details;
decades for high-level patterns (data exfiltration as a goal is not
going away). **Mitigation:** scope claims explicitly — "this analysis
characterises 2017–2025 documented incident patterns", not "this
predicts 2026 attacker behaviour".

**4. Coverage — does NOT degrade, but does NOT grow without active
extension either.**
A corpus snapshotted at time T covers the incidents reported up to T.
At time T+k, the corpus's *coverage* of the world is smaller (because
new incidents have occurred that aren't in it), but the corpus itself
hasn't degraded. This is the most-frequently-misunderstood case:
people say "the corpus is stale" when they mean "the corpus's *fraction
of relevant incidents* has shrunk". **Half-life:** depends on rate of
new public incident reports vs. corpus refresh cadence. **Mitigation:**
periodic extension (add new flows) — but only if the dissertation's
claims require current-day coverage.

### What "always needing updating" gets wrong

The phrasing implies a continuous-maintenance frame: the corpus is a
*living* artefact that must be kept current. This is the wrong default
for at least three reasons:

1. **A snapshot is a legitimate research artefact.** Pinned at a
   specific time, with a specific taxonomy version, against a specific
   source corpus, it's reproducible and defensible. Continually
   rebuilding it sacrifices reproducibility for the illusion of
   currency.
2. **"Stale" is the wrong metaphor.** CTI isn't milk; it doesn't go
   off. It's more like a topographic map — useful until the terrain
   has changed enough that someone using the map would walk off a
   cliff that wasn't there. The right question isn't "how old is the
   map?" but "have the cliffs moved enough to mislead?". For the GAP
   built from CTID flows authored 2017–2024, the only *moved cliff*
   that matters here is MITRE's tactic vocabulary — which is a
   taxonomy issue (#1 above), not an incident-historicity issue (#2
   above).
3. **Continuous updating creates a Sisyphean maintenance burden** that
   competes with the dissertation's actual contribution (the MTDSim
   architecture and the L2/GASP / L4 evaluation). Time spent
   refreshing the corpus is time not spent on the simulator.

### What to do instead

Treat the GAP as **a snapshot with three labelled axes** — which the GAP
already records, just under field names worth surfacing more explicitly:

1. **`corpus_ref`** (currently
   `attack-flow@v3.1.1 (pkg 3.2.0); STIX 2.0.0 extension; CTID published
   export`) — which CTID Attack Flow Builder dataset it was distilled
   from.
2. **`attack_source`** (currently `enterprise-attack-19.1`) — which
   Enterprise ATT&CK version the tactic / technique vocabulary aligns
   with. This is the field that decides whether the GAP renders 14 or 15
   tactic states, what TA0005 means, whether TA0112 exists at all. The
   retired handoff demonstrated this field is *discoverable-by-search
   but not-discoverable-at-a-glance*: the spec describes the v19.1 pin
   in prose (Decision 5), the JSON carries the pin under a non-canonical
   field name, and a reader looking for `mitre_attack_version` finds
   nothing.
3. **`build_date`** (currently `2026-05-28`) — when the GAP itself was
   assembled.

When dissertation claims are made:

- Pure *historical* claims ("the incidents in this corpus exhibit X
  pattern") don't need refresh — they're about the snapshot.
- *Generalisation* claims ("attacker behaviour in current Enterprise
  environments exhibits X") need to scope explicitly to the corpus's
  temporal window, and disclaim beyond it.
- *Methodological* claims ("the MTDSim architecture can ingest CTI
  via the GAP seam") don't depend on freshness at all — they're about
  the architecture's properties.

### Critique of the high-level point

The claim "CTI ages and always needs revising" is **directionally
correct but operationally misleading** for this project. The real
mitigations are version pinning and provenance, not continuous
rebuilding. The taxonomy-drift case (the only one that's actively
biting right now) is fixable once, by pinning. The historical-content
case doesn't need fixing. The operational-relevance case is a
scoping-of-claims question, not a corpus-refresh question. The
coverage case only matters if the dissertation needs current-day
coverage, which it likely doesn't — MTDSim's contribution is
*architectural* (the seam, the L1→L4 pipeline) and the GASP
verification is *methodological* (does the partition discriminate?),
neither of which requires the corpus to reflect 2026 operations.

A weaker version of the claim that survives the critique: **"CTI
encoded in a versioned taxonomy needs its taxonomy version pinned, or
downstream comparisons against newer taxonomy versions will produce
spurious anomalies"**. That's the actionable, version-pinning
implication. Everything else in "CTI ages" is either already
addressed (the historical content is fine) or out of scope (the
operational-relevance / coverage questions are scoping concerns,
not data-maintenance concerns).

## How it connects

- To the immediate trigger: the audit handoff this note retired
  (`docs/handoffs/2026-05-28_gap_mitre_version_audit.md`, deleted in
  the same commit) was resolved by evidence, not by the audit it
  proposed — v19.1's release shipped the split, the GAP's
  `attack_source` already tracked it, the drift was reader-side. A
  technique-ID drift audit ran as part of the retirement and confirms
  clean alignment with v19.1: **124/124 parent technique IDs active**
  (0 deprecated, 0 not-found), **118/121 sub-technique IDs active**;
  three sub-techniques are revoked (`T1070.001` *Clear Windows Event
  Logs*, `T1070.002` *Clear Linux or Mac System Logs*, `T1574.002`
  *DLL Side-Loading*) but all collapse to active parents
  (`T1070`, `T1574`), so the aggregate GAP is unaffected.
- To the GAP schema:
  [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) §(d) records
  `attack_source` and `corpus_ref` as GAP-level metadata fields, but
  doesn't surface them as the load-bearing version pins they are.
  Worth a one-liner header making the discoverability explicit (folded
  into the same commit as this note).
- To the architecture:
  [`../specs/architecture.md`](../specs/architecture.md) discusses
  load-bearing assumptions; the assumption "the GAP is a snapshot, not
  a stream" should be made explicit there. Affects how L4 results are
  scoped (claims are about the corpus's temporal window, not current
  operations).
- To the dissertation's scoping language: the introduction's "we
  study attacker behaviour" should be tightened to "we study the
  documented attacker behaviour in the CTID Attack Flow corpus
  (2017–2024), encoded against MITRE ATT&CK Enterprise vX.Y" — both
  for accuracy and to head off "your data is stale" reviewer objections
  *by scoping rather than refreshing*.

## When this would need updating

- If MITRE ATT&CK introduces a fundamentally restructured taxonomy
  (not a tactic rename, but a paradigm shift — e.g. a switch from
  tactic-based to outcome-based categorisation), the "pin and
  document" mitigation becomes insufficient — would need to re-derive
  the analysis under the new structure.
- If the dissertation's claims expand to include *predictive* statements
  about post-corpus-cutoff attacker behaviour, the operational-relevance
  case stops being scope-able-away and starts requiring actual corpus
  extension.
- If the CTID Attack Flow Builder project itself is deprecated /
  forked / rebuilt under a different schema, the `corpus_ref` pinning
  becomes a backwards-compatibility burden rather than a clean snapshot
  reference.
