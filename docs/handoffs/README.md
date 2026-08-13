# The open chain — dependency order

`ls docs/handoffs/` is the inventory of open work; this file carries only the
thing a directory listing cannot — **what depends on what**, and what is waiting
on a ruling. Delete a handoff in the commit that ships its work, and prune its
line here in the same commit.

**Reset 2026-08-05.** This file had accumulated ~450 lines of shipped-work
archaeology, which its own contract says to prune. Every shipped entry named the
record it landed as; those records are the permanent account, and `git log` is
the permanent history. Both are better sources than a summary here, so the
summaries are gone. Parked work is in [`__archive/`](__archive/).

---

## Open work

**Swept 2026-08-11 (evening, post-meeting).** The chain-of-five is retired: (1),
the axis-metrics brief, closed on Marc's ruling — every axis it owned now reads
DEMONSTRATED, DESIGNED or future work, and the criterion's per-axis M8b fields
are the permanent account; (2), (3) and (5) had already shipped or been
replaced, their files deleted in the commits that shipped them. The axis context
trio is retired with it (axis 6 on `dea3d4d`; axes 4 and 7 in this sweep), as is
the disengagement retire-note, whose own retirement condition — delete when
`feat/axis7-disengagement-clean` lands in `dev` — was met by `07a3459`. `git
log` is the record for all of it; the shipped-work summaries this section
carried went with them, per this file's own contract.

What is open:

- [`2026-08-11_jin_meeting/`](2026-08-11_jin_meeting/) — **the V-trail
  executors** from the 11-Aug supervisor meeting with Jin (register §V1–V7,
  [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)):
  the predictability rework (V2), which feeds the instrument validation pass
  (V1 + V4), which **gates quoting any instrument figure** in methodology or
  results prose; and the experiment/chapter restructure onto the sub-question
  spine (V5–V7), independent of the other two. V3 commissions nothing (use
  Tay's pretrained agent as-is). The folder's README carries the trail.

- [`2026-08-11_movement_objectives.md`](2026-08-11_movement_objectives.md) —
  **a strategic-objective layer for the movement attacker** (`movement_general`
  frontier discipline / `movement_targeted` located objective), curing the
  out-of-order-FSM churn independently of the tactic net. Opened by the
  exploit-learning diagnosis: the movement attacker wastes nine-tenths of its
  actions re-compromising hosts it already owns because Brown's FSM succession
  governed host-selection and the movement layer removed it without replacement.

- [`2026-08-11_learning_scale_dependence.md`](2026-08-11_learning_scale_dependence.md)
  — **is attacker-learning advantage scale-dependent?** Sweeps the existing
  axis-7 routing-belief learner across host-count scale; if the advantage is
  absent, diagnoses mechanism versus implementation. (Its `related:` sibling,
  the probability-shaped exploit-learning brief, no longer exists in this
  directory — read its header note with that in mind.)

- **The exploit-learning-null discriminators.** Both take the compound-exploit
  learner's measured negative
  ([`../implementation/pipeline/ogasp/exploit_learning_findings.md`](../implementation/pipeline/ogasp/exploit_learning_findings.md))
  and turn it from an inferred diagnosis into a demonstration; neither moves
  axis 7's badge; neither introduces a named attacker. **The primary, on-host
  exhibit shipped 2026-08-13** — the yield ledger, as
  [`../implementation/pipeline/ogasp/exploit_learning_yield_findings.md`](../implementation/pipeline/ogasp/exploit_learning_yield_findings.md)
  (prereg + read-only instrument alongside): the committed null branch fired, the
  learner operationalises and its gains are absorbed on the movement attacker's own
  terrain by exploit-insensitivity (X), with no cross-attacker comparison. What is
  still open:
  - [`2026-08-11_fsm_hosted_learning_control_arm.md`](2026-08-11_fsm_hosted_learning_control_arm.md)
    — **the backup discriminator**, for the narrower global-deflationary residual
    the on-host ledger cannot reach ("does exploit capability convert on *any*
    attacker?"). Hosts the same frozen mechanism on the native FSM as a
    pre-registered positive control. Gated by its own step-0 kill-cheap ceiling
    pilot; retires by evidence if that pilot shows no headroom.

- [`2026-08-13_validation_triage.md`](2026-08-13_validation_triage.md) — **the
  validation map**: every contribution enumerated on the capture/model/evaluate
  spine with its existing verification artefacts, and the manual-review queue
  (declared-value families first) ordered by claim-bearing weight. Off every
  chain; consumed by Marc directly.

- [`2026-08-13_axis8_timing_channel_reexamination.md`](2026-08-13_axis8_timing_channel_reexamination.md)
  — **the axis-8 timing-channel inversion**: the substrate's "exponential"
  clocks verified as loc-shifted (quasi-periodic trigger), falsifying the
  planned memorylessness closure and surfacing a candidate timing-distribution
  divergence (documented nowhere; suggested D-39). **Waits on a Marc
  disposition**; blocks any axis-8 timing-intractability prose and the
  criterion amendment either way.

- [`2026-08-06_research_record_from_prompt_corpus.md`](2026-08-06_research_record_from_prompt_corpus.md)
  — **the research record**, mined from Marc's own prompts across the session
  transcripts. Off every chain: it touches no code, gates nothing, and is gated
  by nothing. Splits deliberately: the annal is `implementation/` material — the
  notes rubric bans session logs and decision registers outright — and only what
  the mining *earns* becomes a note. Two outputs beyond the annal: the
  **abandonments and reversals** no shipped record owns, and a **`record-drifted`
  flag list** where the thinking moved on and the document did not (flagged for
  Marc, never actioned). **Stage 0 shipped 2026-08-08; Stages 1–3 remain
  deferred** while the instruments and records they would be measured against are
  still moving — the corpus is backed up (`~/mtdsim-corpus-snapshot/2026-08-08/`,
  checksummed, untracked), the extractor is committed as
  `tools/prompt_corpus.py` with a self-checking gate, and a second extraction
  pass is owed once the axis metrics and the Tay decision settle, so **it does
  not retire at Stage 3**.

---

## Decisions waiting on Marc

Nothing below blocks a handoff except where noted; all of it blocks *closing*
one. The full rows, with costed options, are in the disposition list of
[`../implementation/intent_conformance_audit.md`](../implementation/intent_conformance_audit.md).

| # | What | Blocks |
|---|---|---|
| **D-09** | Zhang's unimplemented MTD-interruption give-up threshold (IS-INT-06) — wanted, and in which form? | no handoff — the measure that generalises it **shipped**; the ruling now bears on whether that generalisation is ratified ([`../implementation/pipeline/ogasp/attacker_disengagement.md`](../implementation/pipeline/ogasp/attacker_disengagement.md) §8, alongside the axis-6 ratification) |
| **D-16** | Eq 2's `V_exploited` half is not charged into phase-2 duration | — |
| **D-17** | The OSDA MIP formulation is decoupled; ranked recommendation is withdraw ≥ replace ≫ repair | — |
| **D-18** | OS Diversity's compatibility guard is inert, so it always replaces every service. **New evidence 2026-08-05:** a repaired guard would replace 13.9 % against Service Diversity's 100 % — a sevenfold separation, so repair settles the family's cardinality by construction | the diversity pair's separability |
| **D-19** | The commented-out OS success gate. Recommendation: leave commented and record | — |
| **D-26** | `Host.total_users` is the index of the first password-reusing account, not the account count. **Same two-line loop as D-32** — rule together | — |
| **D-27** | The credential channel carries 10–23 % of compromises and no mechanism in the reported family moves it | family scope |
| **D-29** | Mechanisms and attacker share one RNG stream, so seed-matched arms are **independent, not paired** — record-grade. **Widened 2026-08-08 by the `mtd_ai` determinism gate:** it is **two** shared streams, not one. Python `random` carries the forced-deploy draw, the exploration action choice and the detection-sensitivity draw against the attacker's host-ordering tie-break; **numpy/scipy** carries every `exponential_variates` call, which is both the defender's trigger and execution times *and* the attacker's action durations and confusion penalty. Measured: one extra draw shifts everything downstream by one position | seed budgeting |
| **D-30/31/32** | NAV feed degeneracy; HostTopologyShuffle compromise-model desync; UserShuffle's ratchet — the latter two latent, gating those mechanisms' activation | latent-pool use |
| **D-35** | EXPLOIT_VULN is uninterruptible in the movement arm, so the diversity family loses **89-97 %** of its exploit-blocking windows in the headline arm. Mapping policy (an S3-R consequence); the recommendation is to state the boundary rather than repair | the diversity family's cross-arm comparison |
| **D-36** | A network-class mutation arriving during an application-class penalty **loses its cursor clear** — the gate fires, the counter increments, the documented position destruction does not happen. The one candidate *bug* of the disruption brief; repair recommended, bounded re-baseline (1.0/run at `simultaneous`, 0 elsewhere) | — |
| **D-37** | The confusion penalty (8.0-17.7 % of the clock) is charged to no `attack_record` row on either arm; only the movement arm can reconstruct it — record-grade | cross-arm time budgets |
| **D-38** | The priority queue gives the higher-priority member of each class pair a systematic extra firing — measured **identically in both arms**, so it is not an arm asymmetry and cannot explain the inversion, but it spuriously separates each pair. Report per firing — record-grade | within-pair claims |
| **D-33** | SCAN_NEIGHBOR is dispatched from uncompromised hosts (48 % of calls in the movement arm, 0 natively). **Measured to move a ranking** — gating it moves `simultaneous` from third to first | boundary review 1's gate |
| **D-34** | `HostTopologyShuffle` writes attacker state directly (`swap_hosts_in_compromised_hosts`) — the latent seventh channel, per-mechanism in a boundary otherwise priced per class. Rule before any promotion into a reported family. *(Renumbered on merge: opened as review 3's D-27, which collided with review 1's)* | latent-pool use |

**Two more, attached to no handoff:**

- **Axis-7 framing** — the shipped axis-7 records report the axis in *performance*
  terms and thereby under-report the finding. Whether they are re-framed, and
  whether the badge is re-pre-registered under a *property* criterion, are
  dispositions rather than housekeeping.
- **The retrace re-take** — the retrace-arm cells of the three sink-bearing
  profiles ran under the since-superseded sink implementation. Whether they are
  re-taken is open; Row B of the criterion re-scores against it if they are.
- **Tempo claims: within-arm only?** The duty-cycle study's kill criterion fired —
  which attacker returns to the floor **reverses** with how the inherited
  attacker's exploit attempts are counted, because S3-R took the
  per-vulnerability clock off the movement arm
  ([`../implementation/pipeline/ogasp/stealth_dutycycle.md`](../implementation/pipeline/ogasp/stealth_dutycycle.md)
  §8). The recommendation is to confine tempo claims to **within-arm**
  comparisons, where the instrument works, rather than re-pricing the movement
  arm (which would move every movement-arm timing figure on record). The
  knowledge-gated brief is designed to need only within-arm comparisons, so this
  ruling does not block it — but it does bound what any cross-arm stealth
  sentence may say.
- **The per-vulnerability row count.** `baseline_ledger` and everything built on
  it count attack-record *rows*, which inflate **3.75×** against per-action
  counts because `_do_exploit_vuln` writes one row per vulnerability tried. This
  is no longer only a bookkeeping question: it is the axis the duty-cycle verdict
  turned on. Whether the suite's cross-arm event definition is corrected — and
  whether experiment 1's and experiment 2's affected figures are restated — is
  open. `baseline_action_rows` is the correction; the restatement is the cost.

---

## One finding with no owner

**Internal MTTC ranks the mechanisms perversely, and no brief in the programme
owns the metrics layer.** `evaluation.py:110` computes attack-action time over
the **number of attack actions** — a mean action duration, not a time to
compromise. Read from the committed goldens at a common compromise depth, **IP
Shuffle scores best** (the mechanism verified to change nothing the attacker
reads) and **OS Diversity worst, below no defence at all**; the four-mechanism
arm carries the highest attack success rate of any scenario.

The code matches `metrics_semantics.md` §(a), so this is not a code/doc
divergence, and it does **not** carry experiment 2's headline. But
[`../workflows/project_context.md`](../workflows/project_context.md) names
internal MTTC the project's **primary metric**, and §(d) asserts that
within-substrate cross-configuration deltas are "Valid — informative".

**Recommendation: its own brief, before any ch5 prose leans on internal MTTC.**
Evidence in
[`../implementation/attacker_read_surface.md`](../implementation/attacker_read_surface.md)
§(m1).

---

## The boundary programme — closed 2026-08-05

Marc's three-brief programme (2026-08-02) asked whether the comparative
evaluation compares *defence ideas* or *integration depths*. All three briefs are
retired; two durable records survive them and are the reference for anything
touching the attacker/defender/network seams:

- [`../implementation/attacker_read_surface.md`](../implementation/attacker_read_surface.md)
  — the read side: what the attacker perceives, censused by instrumented run over
  both driving arms. Its headline: the attacker consults topology, the host's
  pooled vulnerability stack, ports and credentials, and **no host label at all**.
- [`../implementation/mtd_write_surfaces.md`](../implementation/mtd_write_surfaces.md)
  — the write side: every mechanism's write set, live-verified, with the
  purview/fairness table.

Two results from that programme bear on how the family is described. **IP
Shuffle's invisibility to the attacker is documented behaviour, not an
integration artefact** — no lineage paper gives the attacker an IP-addressing
model, and Zhang's IS-INT-04 recasts network-layer MTD as class-based immediate
failure, which is what the code does. **The OS/Service half is different**: that
one is a broken documented wire (D-18). The reported family therefore carries
**two attacker-facing effects across four mechanisms**, and the ρ = −0.893
inversion should be read as a 2 × 2 family contrast.

Boundary review 1's confidence gate did **not** pass — D-33 remains open and is
measured to move a ranking. Marc closed the programme regardless; the open
dispositions live on in the audit's list above, which is their permanent home.

---

## Parked

A sensitivity study over `VULN_PERCENT_CROSS_PLATFORM` — sweeping the service
catalogue's cross-platform share and reporting the diversity pair across it, so
"the two diversity mechanisms are one mechanism at the lineage's own default"
becomes a finding rather than a confound. **Parked by Marc 2026-08-05**, pending
the metrics question above; the measurements supporting it are in
[`../implementation/attacker_read_surface.md`](../implementation/attacker_read_surface.md)
§(g). Note that it needs a joint move — lowering the cross-platform share alone
restructures sharing rather than reducing it, because the per-OS catalogue
shrinks with it.

Older parked or superseded work is in [`__archive/`](__archive/).
