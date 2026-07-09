---
status: durable
created: 2026-07-07
topic: "cross-sectional review of the 15 tactic profiles — black/grey/white-box + adversarial-examiner, scored against the thesis-backbone rubric, with a prioritised action list"
---

# Cross-sectional review of the tactic profiles — four lenses, one convergent finding

## Why this is worth recording

Before Step E, the 15 `docs/tactic_profiles/` were reviewed against the rubric in
[`./2026-07-07_thesis_backbone_rubric.md`](./2026-07-07_thesis_backbone_rubric.md)
through four independent lenses — a black-box characterisation (profiles vs their
own template), a grey-box literature-adequacy audit (are the mined sources right
for the *behavioural* question), a white-box five-theme cross-product (can each
profile sustain tactic × APT × modelling × dynamic-networks × substrate × MTD),
and an adversarial examiner (what fails a viva). The four agree to a degree that is
itself the headline. This note records the convergent finding, the per-tactic
disposition, the prioritised action list, and the live examiner vulnerabilities, so
Step E is executed against evidence rather than the handoff's summary.

## The convergent finding — three reviewers, one crown jewel

Independently, all three deep reviewers named the **same** thing as the strongest,
most defensible, most genuinely-novel content in the work — and it is currently
buried in §4 tables, unwritten as argument:

> **The reset verdict splits by *what kind of gain* the tactic produces:
> capability/credential state *survives* a network mutation; network-position
> state is *invalidated* by it.** And several tactics are *modality-split* inside
> themselves (lateral-movement: scan-hop resets, credential-hop survives).

- Examiner: the per-modality reset split is "mechanism-grounded, APT-relevant, and
  falsifiable — the closest thing to a real finding; promote it from the §4 tables
  into the argument."
- White-box: the survivor/vulnerable axis "is the actual discriminator the
  cross-product surfaces, and it is well-enough evidenced to write today."
- Grey-box: Evans 2011's per-attack-class taxonomy (the mechanism behind the split)
  is "under-exploited — used in only 1 of 15 profiles" when it should underpin the
  reset verdict of every tactic that reuses stolen material vs runs a fresh exploit.

This is the spine Step E should be written around. It is not a gap to fill — it is
a finding to foreground.

## The shared diagnosis (where the worry is right, and where it isn't)

- **The corpus is not adrift.** §2 (behaviour, spined on Alshamrani/Cho/Selmanaj)
  and the MTD-mechanism bundles (Evans, FlipIt, the scan-disruption family) are
  well-targeted for the behavioural and reset questions respectively. The worry
  "splayed all over the place" is **not** borne out at the source level.
- **The real problem is sequencing + lop-sidedness.** Effort over-invested in
  **macro durations the profiles' own §4 rows concede are "whole-chain, not
  per-tactic"**, to feed a duration catalogue the rubric demotes to a *distillation
  of §3* — while **§3, the novel object, is empty in all 15**, with some of its
  best source material already extracted and unused (Alshamrani §IV-C-2-B "renders
  the exploratory knowledge of the attacker useless"; Evans' taxonomy; xiong's
  privilege-escalation gating-state).
- **The lit effort inverted the rubric's priority exactly where it matters.** The
  tactics where the macro-number hunt ran hottest (objective-execution +
  ambiguous-group) are the same tactics where the mechanism/reset question ran
  coldest.

## Per-tactic disposition (white-box matrix, condensed)

Cross-product columns: (a) APT behaviour · (b) adversarial modelling · (c) dynamic
networks/reset · (d) substrate · (e) MTD mechanism. (a) is STRONG everywhere;
(d)=THIN on Tier-3 tactics is *structural* (no native verb → declared dwell via
L3b), not a content gap.

- **Cross-product-complete, write §3 now (7):** `01 reconnaissance`,
  `09 credential-access`, `10 discovery`, `11 lateral-movement` (all 5×STRONG);
  `05 persistence`, `07 stealth`, `13 command-and-control` (complete modulo the
  structural Tier-3 (d)). Four already carry `(→§3)`-tagged reset rows in §4.
- **Thin but writable from mechanism (5):** `03 initial-access`, `04 execution`,
  `06 privilege-escalation`, `14 exfiltration` (rides C2), `15 impact` (Barach
  gives it a real MTD row).
- **Real holes — need more source, not just writing (3):**
  - `08 defense-impairment` — (c) & (e) both HOLE; group-uncertain; nothing grounds
    *which* MTD action bites (a disabled control is host-local state a network
    mutation likely does not restore — a survivor verdict worth grounding).
  - `12 collection` — (c) & (e) both HOLE; host-local read survives, remote-share
    read might reset — neither developed.
  - `02 resource-development` — (e) HOLE because the interaction is genuinely
    **null** (off-network, pre-clock, reset-immune). Flag **inert** per rubric
    crit. 7; the verdict is owned, but it contributes nothing to the novel object.

## The genuinely-ambiguous reset verdicts (research questions, not gaps)

Foreground these as *open contests*, do not resolve them mechanically:

- **`05 persistence` (standout)** — FlipIt frames foothold survival as a rate
  contest (defender move-rate ÷ attacker re-compromise-rate) with an explicit
  "higher-move-cost player → benefit 0" result. Whether a periodic shuffle evicts
  an entrenched foothold *has no fixed answer* — it flips on the ratio, and this is
  the dwell that most directly drives the MTD comparison (cho2020). Foreground it.
- **`13 command-and-control` (secondary)** — the channel is *architected* to survive
  connection loss (fallback/proxy/CDN-fronting); an IP shuffle degrades but may not
  sever it. Outcome depends on beacon-cadence vs move-interval and whether fallback
  infra is modelled.
- **`04 execution` (minor)** — diversity-MTD bites only if APT-preferred fileless
  execution is a *circumvention* attack (Evans → immune) vs *incremental probing*
  (disruptable). A modelling choice the profile leaves open — keep it open, wide
  sweep.

## The prioritised action list

**P0 — Promote, don't mine (free wins, material already held).**
1. Write the **survivor-vs-vulnerable reset axis** as the organising spine of §3
   across the set (crown jewel above).
2. Wire the three under-exploited-but-extracted sources into §3: Alshamrani
   §IV-C-2-B (recon/discovery reset seed), Evans' per-modality taxonomy (every
   reuse-vs-fresh-exploit tactic), xiong2021 gating-state (privesc/binding).
3. Demote §4's macro-duration rows to a labelled "operational-validation outer
   envelope" block; keep only rows that resolve dwell-character or reset-verdict in
   the body. (Keep ransomware *encryption-speed* rows — a real per-act floor.)

**P1 — Write §3 for the 7 complete tactics** (01, 05, 07, 09, 10, 11, 13) as thesis
prose: attacker-knowledge-held → what a mutation does to it → reset verdict +
sweep-width. These are Step E's high-confidence core.

**P2 — Mine-deeper for the 3 holes + the thin objective-execution group**
(08, 12, 14, 15; and firm up 03, 04, 06). Source-*types*, not titles:
- Named-actor IR case studies read for **behaviour-under-network-change** (what the
  actor did when a host was rebuilt / credential rotated / segment changed) — not
  for duration.
- Adversary-emulation plans (CALDERA/ART/emulation libraries) for **executable
  per-tactic procedure** (crit. 1 + crit. 5).
- **MTD-effect-under-a-live-foothold** literature — the genuine unknown: what a
  shuffle does to an attacker who already *holds* credentials/C2 (survivor tactics).
- Defence-disabling behavioural studies (BYOVD / EDR-kill) → `08`.
- Data-staging / exfil-channel-under-MTD → `12`, `14`.
- Attacker-*knowledge*/observability modelling → the "what a recon-successful
  attacker knows" dimension (crit. 3).
- Objective-conditioned behaviour-variation (chemat2024 / al-sada2024 tables,
  under-tapped) → crit. 7 discrimination.

**P3 — Reframe (claims, not just notes) — pre-empt the examiner.**
- State the **detection-regime mismatch** openly: macro dwell/breakout targets are
  *defined by when detection caught the intrusion*, and IDS is culled — so they are
  a *shape/plausibility* envelope, never an absolute-timing target. (Currently no
  doc answers this; it is a clean examiner hit.)
- Restate "APT" as **the source-genre of the CTI corpus**, not a full-fidelity
  claim — Adaptive/detection-evasion are explicitly out of scope (envelope-not-actor
  + CTI-note §8 table already support this; the *claims* must make the retreat).
- Reframe the executed profile as a **worst-case-within-objective stress
  envelope**, not an emulation of any actor (over-generation is disclosed, not
  fixed — say so in the claim).

## The examiner vulnerabilities that outrank the writing

The writing above is necessary but it **defends a result not yet produced**. Two
objections can fail a viva and share one cure:

- **V1** — the novel object rests on two invented parameter families (per-tactic
  dwell × reset fraction). Strip them and nothing separates the APT from the
  generic attacker. Defence exists (declare-and-sweep is the field norm; the sweep
  *width/direction* is mechanism-bounded; the per-modality split is real) but is
  **unrealised** until §3 is written and the sweep is run.
- **V2** — "fidelity changes the answer" is parameter noise unless the
  ranking-change **survives its own sweep band and is distinct from the generic
  attacker's (also stable) ranking**. The correct test (discrimination probe +
  sweep) is *identified* (CTI-note §10) but **unrun**.

**One cure for both:** run the discrimination probe + full sweep; show the
profiled-attacker ranking is stable across its uncertainty band and distinct from
the generic attacker's. Until then the central finding is "declared, not evidenced"
— by the project's own admission. This ranks above prose polish.

Lesser but live: V3 detection-mismatch + tactic-level unfalsifiability (SERIOUS,
partly reframable via P3); V4 envelope over-generation + altitude-on-feasibility
(SERIOUS/MANAGEABLE, reframe via P3); V5 "APT" over-claim (reframe via P3).

## How it connects

- Scores against [`./2026-07-07_thesis_backbone_rubric.md`](./2026-07-07_thesis_backbone_rubric.md).
- Executed into Step E/F of the state-duration work (shipped 2026-07-09 as
  [`../../data/ogasp/tactic_durations.json`](../../data/ogasp/tactic_durations.json))
  (P0/P1/P2 = §3; P3 = the framing the methodology chapter must carry).
- The V1/V2 cure depends on the timeline runner
  ([`../handoffs/2026-07-03_l3_timeline_runner.md`](../handoffs/2026-07-03_l3_timeline_runner.md))
  and the discrimination probe (CTI-note §10) — both downstream, both unbuilt.

## When this would need updating

- After Step E lands §3 — the "holes" and "thin" dispositions are re-scored.
- If P2 mining changes a reset verdict (esp. `08`/`12`) — the per-tactic table moves.
- If the discrimination probe/sweep runs — V1/V2 downgrade from FATAL to SERIOUS or
  the negative-result disposition applies.
