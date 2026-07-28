---
status: durable
created: 2026-07-27
updated: 2026-07-27
topic: "L3 S1 (literature half) — the APT-lifecycle consensus overlay: five published lifecycle models overlaid onto the fifteen ATT&CK tactics, their consensus ordering extracted, and a declared tactic-to-tactic distance model derived from it, ready to ground the outcome-overlay transition weights"
---

# The lifecycle consensus overlay — a tactic-to-tactic distance model grounded in the published APT lifecycles

**Status:** durable. Executes the literature half of **S1**
([`supervisor_decision_register.md`](supervisor_decision_register.md) §S1): the
tactic-pair routing weights grade transitions by *direction* but not by *how
far* they travel, so `reconnaissance → impact` carries mass comparable to
`reconnaissance → initial-access`. The directed fix is a literature-based
distance dependency, and the supervisor's method is specific: **overlay the
published lifecycle models, take their consensus, and only then fold that
consensus into the weights.** This record is the consensus artefact. **No
weight value changes here** — the fold-in and the sensitivity sweep are the
next handoff's job (`2026-07-27_tactic_weight_sensitivity_study.md`), and the
machine-readable model is
[`../../../../data/ogasp/controller/lifecycle_consensus.json`](../../../../data/ogasp/controller/lifecycle_consensus.json).

**The standing assumption (M3), stated where the ordering is used.** ATT&CK
deliberately encodes no tactic ordering — the matrix's left-to-right layout
reflects "typical attack progression" but "does not itself encode the sequence
of malicious activities" ([`al-sada2024`](../../../sources/extractions/al-sada2024.md)
§2, p. 12:3). Every ordering below is therefore **imported** from the lifecycle
literature, as an assumption of this work (register §M3). There is precedent
for exactly this import: Ferraz's pipeline orders each campaign's techniques by
"the canonical ATT&CK kill-chain progression (Reconnaissance → Impact)" and is
explicit that this is "an organisational behaviour, not a recovered temporal
sequence" ([`ferraz2024`](../../../sources/extractions/ferraz2024.md)).

---

## 1. The target representation — an ordering, from which distance is derived

The artefact produces a **consensus ordering** (a stage rank per tactic), not a
directly-authored 210-cell distance table. Chosen because it is what lifecycle
models actually publish (phases, not pairwise distances), because it degrades
gracefully where models disagree (a tactic's rank can be marked weak without
poisoning every pair it touches), and because distance falls out of it.

For a directed pair `a → b`, the **signed stage offset** is

```
    Δ(a, b) = s(b) − s(a)
```

where `s(·)` is the consensus stage index (§4). The sign convention is fixed:
`Δ > 0` is forward travel, `Δ < 0` backward, `Δ = 0` within-stage. Forward and
backward distance are **different quantities** with different kernels (§6);
they are never collapsed into `|Δ|`.

---

## 2. The models overlaid

Five models, each recorded verbatim with a locator. One extraction pass per
paper (guardrails); secondary channels are named as such.

| # | Model | Phases (verbatim, in published order) | Cited via |
|---|---|---|---|
| **L1** | Lockheed Martin Cyber Kill Chain (Hutchins, Cloppert & Amin 2011) — the primary overlay S1 names | Reconnaissance → Weaponization → Delivery → Exploitation → Installation → Command and Control → Actions on Objectives | [`hutchins2011`](../../../sources/extractions/hutchins2011.md) §3.2, pp. 4–5 (primary, acquired 2026-07-27) |
| **L2** | Alshamrani 2019 five-phase APT lifecycle | Reconnaissance → Establish Foothold → Lateral Movement/Stay Undetected → Exfiltration/Impediment → Post-Exfiltration/Post-Impediment | [`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §II-C, p. 1854 |
| **L3** | Mandiant APT1 attack lifecycle (2013) | Initial Compromise → Establish Foothold → Escalate Privileges → Internal Reconnaissance → Move Laterally → Maintain Presence → Complete Mission (the prose's seven stages; Figure 14 additionally prefixes **Initial Recon** — eight by figure, seven by prose). The middle four "do not have to occur in this order every time" and, once established, the group "continually repeat[s] the cycle … until they are removed entirely" | [`mandiant2013`](../../../sources/extractions/mandiant2013.md) Fig. 14 p. 27, Appendix B pp. 63–65 (**primary, verified 2026-07-27** — supplied by Marc); channel record [`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §II-C, p. 1854, whose seven-stage listing the primary's prose confirms |
| **L4** | Ussath 2016 three-stage model | Initial Compromise → Lateral Movement → Command & Control Activity | [`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §II-C, p. 1854 (secondary channel) |
| **L5** | The CKC-derivative family skeleton (Che Mat 2024, Table 4: CKC + SDAPT, Dell SecureWorks, LogRhythm, Mandiant, Lancaster, BSI) | three parts: gain foothold (first 2–3 phases) → gain remote access / expansion → ultimate goals ("often occurs in the final two phases") | [`chemat2024`](../../../sources/extractions/chemat2024.md) §Discussion Table 4 prose |

L5 is a published *overlay of overlays* — a peer-reviewed SLR performing the
same consolidate-and-take-consensus operation this artefact performs, which is
why its three-part skeleton is treated as consensus evidence rather than as a
sixth independent phase enumeration. Candidate further lifecycles checked and
found to carry none: `al-sada2024`, `sadlek2022`, `buechel2025`, `bianco2013`,
`adversary_emulation_frameworks`. Deliberately not chased (fresh extractions,
diminishing returns for an ordering already quadruply attested): the Unified
Kill Chain and the remaining L5 derivatives' primaries (Dell SecureWorks,
LogRhythm, Lancaster, BSI) — on Marc's to-download list if examiner pressure
ever warrants them. The Mandiant primary *was* chased (supplied by Marc,
2026-07-27) and verified — see L3.

---

## 3. Per-model mapping onto the fifteen tactics

The mapping is the interpretive step, done once per model, visibly. Cell
markers: **[def]** justified from the model's own phase *definition*;
**[conv]** the pre-v19.1 academic ATT&CK→CKC convention already in use
([`controller.md`](controller.md) §1, `data/misc/_viz/ckc_lifecycle/ckc_layer_viz.py`);
**[name]** inferred from the phase name alone; **[verify]** the channel
under-determines the cell — recorded, not relied on. Tactics a model does not
reach are listed as unmapped — no silent cells.

### L1 — Cyber Kill Chain (seven phases)

| CKC phase | Tactics | Basis |
|---|---|---|
| Reconnaissance | reconnaissance | [def] external target research |
| Weaponization | resource-development | [def] payload/tooling preparation, off-network |
| Delivery | initial-access | [def] transmission of the weapon to the target |
| Exploitation | execution | [def] "exploitation triggers intruders' code" — code execution on the victim; privilege-escalation, stealth, defense-impairment also sit here **[conv]** only (Hutchins does not individuate them) |
| Installation | persistence | [def] the backdoor "allows the adversary to maintain persistence" — primary-grounded |
| Command and Control | command-and-control | [def] beacon out, "hands on the keyboard" |
| Actions on Objectives | collection, exfiltration, impact [def] ("collecting, encrypting and extracting"; integrity/availability violations); lateral-movement [def] (the "hop point … move laterally" sentence); credential-access, discovery **[conv]** only | catch-all — asserts membership, not internal order |

### L2 — Alshamrani five-phase

| Stage | Tactics | Basis |
|---|---|---|
| 1 Reconnaissance | reconnaissance [def]; resource-development [def] (off-network tooling/planning before the foothold, §I/§II-C Stage 1) | |
| 2 Establish Foothold | initial-access [def] (spear-phish / watering-hole / vuln exploitation); execution [def] (user-triggered execution of the delivered malware) | |
| 3 Lateral Movement / Stay Undetected | credential-access [def] (credential dumping, pass-the-hash); privilege-escalation [def]; lateral-movement [def]; discovery [def] (internal search; "position for future" extends this stage indefinitely); stealth [def] (the stage's second name); persistence [def] (durable implants, §II-C Stage 3) | |
| 4 Exfiltration / Impediment | collection [def] ("actions comprising retrieving … this data"); exfiltration [def]; impact [def] (disabling/destroying components) | |
| 5 Post-Exfiltration / Post-Impediment | no dedicated tactic among the fifteen (log-scrubbing/clean-exit is nearest `stealth`, already seated at stage 3) — unmapped, recorded | |
| — | command-and-control: **not a phase** — §II-D treats C&C as a continuous long-term activity (beaconing "at given intervals"), and stage 4 names the C&C server as exfiltration's *destination* | the disagreement datum, §5 |
| — | defense-impairment: unmapped — the paper "barely addresses" impairment (extraction, Step B block) | |

### L3 — Mandiant APT1 lifecycle (primary-verified; middle unordered *and cyclic*)

All cells now [def] from Appendix B's stage definitions (pp. 63–65) — the
`verify` flags the name-level channel forced are resolved.

| Stage | Tactics | Basis |
|---|---|---|
| (fig. only) Initial Recon | reconnaissance | [def]-weak — Figure 14 depicts the stage; the prose gives it no section. Counted as figure-level support for the preparation stage, not as a prose-attested seat |
| 1 Initial Compromise | initial-access, execution | [def] spear-phish / strategic web compromise / webshells; user-triggered payload |
| 2 Establish Foothold | persistence, command-and-control | [def] backdoors that "establish an outbound connection … to a computer controlled by the attackers" — both cells primary-grounded (was [verify]) |
| 3 Escalate Privileges | privilege-escalation, credential-access | [def] "Most often this consists of obtaining usernames and passwords" — hash dumping, cracking, pass-the-hash (was [verify]) |
| 4 Internal Reconnaissance | discovery | [def] OS commands, share listings, data-of-interest searches — TA0007 (internal), not TA0043 |
| 5 Move Laterally | lateral-movement | [def] compromised credentials / pass-the-hash via PsExec, Task Scheduler |
| 6 Maintain Presence | persistence, command-and-control (second appearance of **both** — neither is uniquely seated in this model) | [def] new backdoor families + "a variety of command and control addresses" |
| 7 Complete Mission | collection, exfiltration | [def] archive (RAR/ZIP) then transfer out. **impact is *not* attested** — APT1's mission is data theft; impact's stage-3 seat rests on L1/L2 |
| — | unmapped: resource-development; stealth; defense-impairment | |

### L4 — Ussath three-stage (name-level channel)

| Stage | Tactics | Basis |
|---|---|---|
| 1 Initial Compromise | initial-access, execution | [name] |
| 2 Lateral Movement | lateral-movement [name]; credential-access [def] (Ussath's own finding, via the channel: "dumping credentials is the most common chosen method for lateral movement") | |
| 3 Command & Control Activity | command-and-control [name]; exfiltration **[verify]** (whether "C2 activity" includes exfiltration is not recoverable from the name) | |
| — | unmapped: the remaining nine tactics (a deliberately minimal model) | |

### L5 — the family skeleton (three parts)

Foothold-gaining part ← {reconnaissance, resource-development, initial-access,
execution} · expansion/remote-access part ← the post-intrusion middle ·
final-goals part ← {collection, exfiltration, impact}. Part-level only, [def]
from the Table 4 prose; carries no per-tactic cells.

---

## 4. The consensus ordering — four super-stages, with a weakly-ordered middle

Where the models agree on relative order, the agreement is strong and
consistent; where they disagree, the disagreement is confined to the
post-intrusion middle. The consensus is therefore a **banded partial order**
over four super-stages:

| `s` | Stage | Tactics | Internal order |
|---|---|---|---|
| 0 | **preparation** | reconnaissance, resource-development | prep precedes intrusion in every model that reaches it (L1 phases 1–2; L2 stage 1; L5 part 1; L3's Figure 14 prefixes Initial Recon before Initial Compromise); L4 starts later, consistently |
| 1 | **intrusion** | initial-access, execution | unanimous: L1 3–4, L2 stage 2, L3 stage 1, L4 stage 1 |
| 2 | **post-intrusion operations** | persistence, privilege-escalation, stealth, defense-impairment, credential-access, discovery, lateral-movement, command-and-control | **explicitly weakly ordered**: L3's primary states the stages between Establish Foothold and Complete Mission "do not have to occur in this order every time" and that the group "continually repeat[s] the cycle" until evicted (Appendix B, p. 63) — the middle is not merely permutable but *cyclic*; L2 holds them in a single stage; L1 compresses them into phases 5–7 and is structurally silent on their internal sequence |
| 3 | **objective** | collection, exfiltration, impact | unanimous terminal: L1 AoO, L2 stage 4, L3 stage 7 (*after* the any-order block), L5 "final two phases" |

Two corollaries the models state directly: the **invariant prefix** —
Alshamrani's structural claim that stages 1–2 are invariant across APT
operations while 3–5 are objective-conditioned — makes `s0 ≺ s1 ≺ rest` the
strongest-sourced part of the ordering; and L1's chain framing ("only now,
after progressing through the first six phases…") is the strongest *forward*
sequentiality claim, read at stage granularity, not within-stage.

One boundary nuance, recorded rather than hidden: L3's cyclic caveat has
"completing mission" *recurring* inside the repeated middle cycle, which
blurs the stage-2/stage-3 boundary within a long campaign. The consensus
keeps the objective stage terminal because every model — including L3's own
stage listing — still places mission completion as the campaign's end-state;
the cyclic re-entry is behaviour the *overlay's* verdict routing already
models (retry/fallback), not a stage-ordering claim.

### The disagreements, and the rules that resolve them

No model is asserted wrong; both poles of each disagreement are recorded, and
each is resolved by a stated rule.

**Rule R-1 — ambiguity collapses into the unordered middle.** Where models
genuinely disagree about a tactic's position, or one treats it as a continuous
activity rather than a positioned phase, the tactic is seated in stage 2 — the
stage that asserts no internal order — rather than adjudicating between
models. Rationale: seating an order-ambiguous tactic in the unordered stage
never manufactures a distance the literature does not support; seating it at
either disputed pole would.

**Rule R-2 — individuation beats the catch-all.** Where a tactic's CKC seat
comes only from the coarse Actions-on-Objectives catch-all or from a
convention cell with no primary definition, and an APT-specific model
individuates the same tactic at a finer position, the finer placement wins. A
catch-all asserts membership, not position.

| Disagreement | Poles | Rule | Resolution |
|---|---|---|---|
| **Where command-and-control sits** — the flagship case | L1: a discrete phase between Installation and AoO. L2: not a phase — a continuous supporting activity (§II-D), corroborated by Che Mat's Stuxnet caveat (C&C is optional). L4: the *terminal* stage. L3: seated **twice** [def] — Establish Foothold's outbound backdoor channel *and* Maintain Presence's redundant C2 addresses — which is the continuous reading in phase clothing | R-1 | stage 2, flagged order-weak |
| **Where persistence sits** | L1: Installation, a discrete mid-chain phase. L3: stages 2 *and* 6 (appears twice, primary-confirmed). L2: stage 3 | R-1 | stage 2 |
| **Whether credential-access, discovery, lateral-movement are late or mid-campaign** | CKC convention: AoO (late). L2 stage 3, L3 stages 3–5, L4 stage 2: mid-campaign | R-2 | stage 2 |
| **Where privilege-escalation sits** | CKC convention: Exploitation (intrusion band). L2 stage 3, L3 stage 3: post-intrusion | R-2 | stage 2 |
| **Whether exfiltration is objective or C2-activity** | L1/L2/L3: terminal objective. L4: inside "C&C Activity" [verify] | majority + the L4 cell being [verify]-grade | stage 3 |

### Per-tactic evidence status

`sourced` — seated by model agreement; `rule` — seated by R-1/R-2 (inputs
sourced, rule declared); `declared` — no model reaches it.

| Tactic | `s` | Status |
|---|---|---|
| reconnaissance | 0 | sourced |
| resource-development | 0 | sourced |
| initial-access | 1 | sourced |
| execution | 1 | sourced |
| persistence | 2 | rule (R-1) |
| privilege-escalation | 2 | rule (R-2) |
| stealth | 2 | sourced-thin (one model, L2's "Stay Undetected"; no disagreement, but single-source) |
| defense-impairment | 2 | **declared** — no lifecycle model addresses TA0112 (a post-v19.1 tactic); seated as stealth's ATT&CK sibling |
| credential-access | 2 | rule (R-2) |
| discovery | 2 | rule (R-2) |
| lateral-movement | 2 | rule (R-2) |
| command-and-control | 2 | rule (R-1) |
| collection | 3 | sourced |
| exfiltration | 3 | sourced |
| impact | 3 | sourced |

---

## 5. Verdict on the five-band prior

The five-band prior (0 prep, 1 intrusion, 2 consolidate, 3 expand, 4
objective — [`success_failure_overlay_design.md`](success_failure_overlay_design.md)
§2.1, declared-not-sourced) was one of the things this overlay had to settle:
survive, re-cut, or replace. Verdict: **partially survives, re-cut**.

- **Bands 0, 1 and the objective band's {collection, exfiltration, impact}
  survive intact** — they are exactly consensus stages 0, 1, 3, now sourced
  rather than declared.
- **The band-2/band-3 split (consolidate ≺ expand) does not survive.** The
  overlay finds no model that orders consolidation before expansion: L3's
  nominal numbering (escalate ≺ internal recon ≺ lateral movement) is exactly
  the ordering its own any-order caveat withdraws, and L2 holds the whole
  middle in one stage. The split collapses into the single weakly-ordered
  stage 2.
- **Command-and-control's band-4 seat does not survive.** No lifecycle model
  places C2 *with* the objectives except L4's terminal stage, which is
  outweighed under R-1 by L1 (discrete mid-chain phase) and L2 (continuous
  activity). C2 moves to stage 2.

**Named consequence for the fold-in (not actioned here):** the overlay rules'
`relationship` term (forward/lateral/backward) is currently computed from the
five bands. Under the consensus stages, relationship classes change for pairs
involving command-and-control, discovery, lateral-movement and
credential-access (e.g. `command-and-control → execution`, backward under the
bands, becomes backward-within-consensus-stage-2's terms a *lateral* move).
Whether the fold-in recomputes relationships from `s(·)` or keeps the bands
for relationship and adds distance separately is the re-derivation's decision
to make — visibly, in the ledger.

---

## 6. The distance model

**Functional form (declared).** A geometric decay per stage crossed, separate
for each direction, with a zero floor:

```
              ⎧ 1                    Δ = 0        (within-stage)
    d(a,b) =  ⎨ γ^(Δ−1)              Δ ≥ 1        (forward kernel)
              ⎩ δ^(|Δ|−1)            Δ ≤ −1       (backward kernel)

    floor:    values with d < z are read as exactly 0 at fold-in
```

**Named parameters (all declared; the sweep set):**

| Param | Value | Sweep band | Role |
|---|---|---|---|
| `γ` (gamma) | **0.25** | 0.1 – 0.5 | forward decay per extra stage crossed — adjacent forward is never penalised (`f(1) = 1`), a two-stage skip keeps a quarter of its mass, a three-stage leap 1/16 |
| `δ` (delta) | **0.5** | 0.25 – 0.75 | backward decay per extra stage — deliberately gentler than `γ`: falling back after failure is ordinary campaign behaviour ("back to the drawing board"), leaping far forward is the thing being suppressed |
| `z` (floor) | **0.1** | {0, 0.05, 0.1} | the supervisor's "close to, or exactly, zero": with `z = 0.1` the three-stage forward leap (0.0625) reads as exactly 0; with `z = 0` it stays merely near-zero. Both poles of the ruling are representable |

**Why this family:** the models publish *sequenced stages*, which attests that
transition plausibility concentrates on adjacency (every model's phases chain
to their successor; none draws a recon-to-objective edge) — a monotone decay
in stage distance is the attested *pattern*; the specific magnitudes are
declared judgement, defended by the sensitivity sweep, not by citation. The
kernel is deliberately parameter-light (two ratios and a floor) so the sweep
is identifiable — the same group-anchors-not-free-fit discipline as the
duration catalogue.

**Worked pairs — the behaviour the ruling asks for:**

| Pair | Δ | d | Reading |
|---|--:|--:|---|
| reconnaissance → initial-access | +1 | **1.0** | adjacent forward — stays high (the pair S1 says must not be suppressed) |
| reconnaissance → impact | +3 | **0.0625 → 0** (under `z`) | the canonical large jump — falls to near/exactly zero |
| initial-access → discovery | +1 | 1.0 | adjacent forward |
| initial-access → exfiltration | +2 | 0.25 | a skip: suppressed, not banned |
| persistence → lateral-movement | 0 | 1.0 | within the middle — distance is silent there, *by consensus* (the literature declares no order to violate) |
| initial-access → reconnaissance | −1 | **1.0** | the failure-side regression bridge — untouched by distance |
| exfiltration → initial-access | −2 | 0.5 | a deep fallback — reduced |
| impact → reconnaissance | −3 | **0.25** | full-campaign collapse — clearly distinguishable from the adjacent backward move (1.0), which is what "a plausible backward move must not be indistinguishable from an implausible one" requires |

**What distance is not.** It is not the whole weight: it carries no verdict
conditioning, no `enables` semantics, no foothold gating — those stay with the
overlay rules it will multiply
([`success_failure_overlay_design.md`](success_failure_overlay_design.md) §1–2).
And it is not fitted: no parameter was chosen by looking at how any profile's
net traverses (the CTI-independence boundary, §1 of the same record — the
worked pairs above are semantic checks, not traversal outcomes).

---

## 7. Sourced vs declared — the separability statement

A reader (and the sensitivity study) must be able to split this artefact into
what the literature fixes and what this project declares. The split:

**Sourced (not swept):** the four-stage spine `s0 ≺ s1 ≺ s2 ≺ s3`; the
per-tactic seats marked `sourced`; the weak ordering of stage 2 (L3's
any-order caveat, L2's single stage); the invariant prefix.

**Rule-resolved (rules declared, inputs sourced; re-arguable but not swept):**
the R-1/R-2 seats — command-and-control, persistence, privilege-escalation,
credential-access, discovery, lateral-movement.

**Declared (the sweep set, plus two seats):** the kernel family and `γ`, `δ`,
`z` (tier: the decay *pattern* is `attested-pattern/declared-magnitude`; the
floor is `declared-judgement` — [`../../declared_value_provenance.md`](../../declared_value_provenance.md)
§2); the `defense-impairment` seat; the `stealth` seat's single-source
thinness. The sensitivity study sweeps **only** `γ`, `δ`, `z`; a challenge to
a rule-resolved seat is a re-argument of R-1/R-2, not a sweep dimension.

---

## 8. Where this connects, and when to update

- **Consumes:** [`supervisor_decision_register.md`](supervisor_decision_register.md)
  §S1/§M3; the extractions named in §2; [`controller.md`](controller.md) §1
  (the crosswalk this checks and cites);
  [`success_failure_overlay_design.md`](success_failure_overlay_design.md)
  §2.1/§2.6 (the band prior this re-cuts, the value model the distance term
  will enter).
- **Feeds:** the weight re-derivation + sensitivity study
  (`2026-07-27_tactic_weight_sensitivity_study.md`), which folds `d(a,b)` into
  the outcome rules and sweeps `γ`, `δ`, `z`.
- **Artefact:** [`../../../../data/ogasp/controller/lifecycle_consensus.json`](../../../../data/ogasp/controller/lifecycle_consensus.json)
  (stages, per-tactic seats + status, kernel + parameters + sweep bands).
  Provenance row: [`../../provenance.md`](../../provenance.md).
- **Ratification:** the consensus (stages, rules, kernel and parameters) was
  reviewed and **greenlit by Marc on 2026-07-27**, after the Mandiant primary
  was acquired and verified against the channel (no seat changed; the two
  `verify` cells resolved, and the any-order caveat strengthened to cyclic).
- **When to update:** ~~if the Mandiant primary contradicts its channel~~ —
  discharged 2026-07-27: the primary was acquired and *confirms* the channel
  (prose = seven stages; Figure 14 adds Initial Recon — see
  [`mandiant2013`](../../../sources/extractions/mandiant2013.md)). Still
  live: if a new lifecycle model is overlaid (add a §2 row and re-run §4); if
  the sensitivity study shows a conclusion turning on `γ`, `δ` or `z` (the
  declared magnitudes then need re-argument, per the ledger's maintenance
  protocol); if Marc re-cuts a rule-resolved seat (R-1/R-2 re-argument).
