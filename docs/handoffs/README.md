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

**Swept 2026-08-13 (session close, on Marc's direction).** The 2026-08-11 set —
the jin-meeting V-trail folder (whose last open item was the V1 + V4 instrument
validation pass; V2 and the V5–V7 restructure had already landed and V3
commissions nothing), the movement-objectives brief, the
learning-scale-dependence brief, and the FSM-hosted learning control arm (the
exploit-learning-null discriminators' last open item) — is removed on Marc's
instruction rather than retired by evidence; the supervisor decision register
and the shipped findings records remain the permanent account of what each
carried, and `git log` the record of the briefs themselves. The axis-8
timing-channel re-examination retired the same day in the commits that shipped
its work (the D-08 regime ruling and the criterion's dated amendment).

- [`2026-08-16_drafting_movement_attacker_section.md`](2026-08-16_drafting_movement_attacker_section.md)
  — **the §4.2 drafting context** (standing; retires with the section). Two
  validation handoffs spun out of the §4.2.2 passes on 2026-08-17, both
  gating numbers the chapter will cite and both to run in fresh sessions:
  [`2026-08-17_l2_classification_confidence_validation.md`](2026-08-17_l2_classification_confidence_validation.md)
  (one structural baseline for the 13→19→15 number trail; can the composite
  terminal-tactic + CTI approach reach 38/38 high confidence) and
  the tactic-resolution validation (independent re-derivation of the
  profile numbers; the null ruling) — **retired 2026-08-17** in the commits
  that shipped
  [`tactic_profile_statistics.md`](../implementation/pipeline/gasp/tactic_profile_statistics.md):
  size-matched null and tactic-to-tactic resolution ruled, gate pinned, the
  partition's warrant reconciled with the structural null. The
  classification-confidence one **retired 2026-08-17 too** (`83a6d0b`,
  `3c35870`, `f309c07`): baseline pinned, 38 / 38 high, Marc's three
  membership rulings applied (19 / 7 / 7 / 5), L2–L3 rebuilt — record
  [`structural_baseline.md`](../implementation/pipeline/gasp/structural_baseline.md).
  What it leaves is prose, not numbers:
  [`2026-08-17_post_ruling_chapter_numbers.md`](2026-08-17_post_ruling_chapter_numbers.md)
  — carry 19 / 7 / 7 / 5, the pinned baseline and the 38 / 38 column into
  §4.2.2 and the ch4 findings note. Depends on the drafting context above;
  blocks nothing else.

- [`2026-08-20_section42_figures_tables_appendix.md`](2026-08-20_section42_figures_tables_appendix.md)
  — **the §4.2 figure / table / appendix build**: Marc's 2026-08-20 ruled
  inventory (three in-prose figures, one table, the consolidated appendix
  ledger) plus the open CONFIRMs (fig:l1-graph stays; audit-table columns;
  threat-model framing; the maybe-appendix renders). Depends on the drafting
  context above for the ruling trail; its failure-figure wiring is gated on the
  v4 re-key ruling in the table below.

- [`2026-08-13_validation_triage.md`](2026-08-13_validation_triage.md) — **the
  validation map**: every contribution enumerated on the capture/model/evaluate
  spine with its existing verification artefacts, and the manual-review queue
  (declared-value families first) ordered by claim-bearing weight. Off every
  chain; consumed by Marc directly.

*(The research-record brief retired 2026-08-20 with Stages 1–3 complete — the
annal is the permanent account
([`../implementation/research_record/`](../implementation/research_record/),
whose living README carries the re-run instructions); the post-metrics delta
pass it stayed open for rides that README now, not a handoff. `git log` holds
the brief.)*

---

## Decisions waiting on Marc

Nothing below blocks a handoff except where noted; all of it blocks *closing*
one. The full rows, with costed options, are in the disposition list of
[`../implementation/intent_conformance_audit.md`](../implementation/intent_conformance_audit.md).

| # | What | Blocks |
|---|---|---|
| **Overlay: re-key experiment 2 under `v4`?** | The failure-only ruling is **taken and applied** (2026-08-19, Marc: "having a success matrix makes no sense logically"): `v4_failure_only` is the go-forward overlay, registered and compile-checked; `v3` frozen ([`success_null_overlay_feasibility.md`](../implementation/pipeline/ogasp/success_null_overlay_feasibility.md) §8). What remains is whether the published records — experiment 2 first, the chapter's headline source — are re-run under `v4` before ch5 is drafted, or stand on `v3` with the feasibility study as the bridge (the retired success table's effect is a profile-signed 1–3 hosts, no headline moved; ≈ 27 000 rows for the full set, 2 760 for experiment 2 alone, §6). The sibling kernel-discrepancy ruling **closed 2026-08-19** (keep as declared; [`failure_weight_decomposition.md`](../implementation/pipeline/ogasp/failure_weight_decomposition.md) §4), whose figure set regenerates under `--version v4_failure_only` at the tex wiring pass | the ch5 numbers; the owed §4.2.4 failure-encoding paragraph is unblocked |
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
