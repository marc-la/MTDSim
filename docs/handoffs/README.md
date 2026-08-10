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

## Open work — the chain of five, plus the 2026-08-09 additions below it

**(2) is the live one — start there.** Its rulings all landed 2026-08-07 and its
prerequisite checks and both approved measurements have run; what remains before a
build is **one cheap measurement** (the exploit-failure decomposition re-taken on
the *movement* arm, where D-35 says EXPLOIT_VULN is uninterruptible, so the
memory's headroom should be far larger than the native arm showed) and **one owed
record** (the dated axis-6 reversal, since R-A reopened a closed row). (1) is
unblocked and settles the schema question. **(5)'s dependency is discharged in
substance:** it wanted a reactive defender that responds to what it measures, and
one now exists and runs — the rebuild shipped 2026-08-08 — so what is left of the
`mtd_ai` sanction is Marc's ruling on *using* it in a reported experiment, not a
question about whether there is anything to sanction. (3) is now the
scaled-training proposal that rebuild opened, and it gates nothing. (4) is
independent of the axis chain and can run alongside any of it.

> **Reconciled on merge, 2026-08-05.** This chain was written on the boundary
> branch, before the session branches were merged into `dev`. Three corrections
> the merge forced, recorded here rather than silently applied:
>
> - **The disengagement brief has shipped and is now deleted.** `dev` built and
>   ran the measure (`35f772e`) and the iterated cost model that brief declared
>   retired. It was briefly kept because its 2026-08-05 rescope — the promotion
>   to axis 6's metric — was not in the shipped record; that rescope, the
>   measure's ratified vocabulary and its two open rulings were folded into
>   [`../implementation/pipeline/ogasp/attacker_disengagement.md`](../implementation/pipeline/ogasp/attacker_disengagement.md)
>   (§1.2–1.3, §8) on 2026-08-05 and the handoff deleted, which is where the
>   lifecycle wanted it. Its alternatives-considered argument lives in `git log`.
> - **The axis-6/7 scope brief is deleted.** It was created on `dev` after the
>   fork, so this chain never saw it — but it had already been overtaken there:
>   Marc's axis-6 closure (`681cdf2`, the day after the brief was last updated)
>   retires the iterated cost model outright and discharges all five of its
>   remaining items, and it simply was not deleted in the commit that shipped
>   that ruling. Its four dated rulings survive in `git log`; the axis-6
>   disposition's permanent home is the criterion's axis-6 row. **It was briefly
>   restored during this merge on the strength of its own `status: open` and its
>   "items 1-4 and 6 remain open" line — a reminder that a handoff's self-report
>   is evidence about the day it was written, not about today.**
> - The **OS/Service indistinguishability brief is deleted**, as the audit and
>   the write/read-surface records already say it is. Its content lives on as
>   D-18/D-19 in the disposition list.

*(Shipped 2026-08-05: the **disruption-wiring brief**. A6 was the instrument
and is repaired — the movement record now names the mechanism that interrupted
it, so 0 of 1 061 interrupts are unattributed where previously none could be
attributed at all. With it, the class-level pricing model is **verified rather
than assumed**: the gate rows are identical within a class and the penalty draw
is bit-identical across the four real mechanisms. The model is faithfully wired
at the gate and does **not** arrive equally at the two arms — a network-class
firing delivers 0.92-1.00 of its native disruption to the movement attacker, an
application-class firing 0.67-0.83, in every scheme at every seed. A1 and A4 do
not cancel: A4 turns out to be load-bearing rather than offsetting, carrying
four-fifths of the diversity pair's measured effect, which is much stronger
evidence for D-21's ruling than that ruling had. Every one of A1-A7 and both
scheduler effects carries a verdict; D-35..D-38 opened, A6 repaired, A2/A3/A4
confirmed as already-ruled. Record:
[`../implementation/disruption_wiring.md`](../implementation/disruption_wiring.md).)*


*(Shipped 2026-08-06: the **axis-5 exposure reader**. The measure is sound — it
discriminates between profiles, and its kill criterion held decisively (Spearman
−0.529, against 0.90) — and it inverted the prediction it was built to test. The
inherited attacker reads **quieter** than every profile in ten cells of ten,
because the tempo premise was an accounting artefact: the substrate writes one
attack-record row **per vulnerability tried**, inflating that arm's event count
3.75×, and counted as *actions* it takes 371 steps per run against the profiles'
463–674. The separation that remains is mix-borne rather than tempo-borne, and
four of five profiles draw 56–62 % of their exposure from tactics that dispatch
no substrate verb at all. **No badge move** — a reader is not a mechanism, on the
same reasoning the disengagement measure declined one. The CVSS half the meeting
proposed was built, swept both ways and is **measured inert**. The 1(b)
mtd_ai-consequential route the handoff carried is rehomed to
[`../implementation/pipeline/ogasp/stealth_conceptualisation.md`](../implementation/pipeline/ogasp/stealth_conceptualisation.md)
§17, with its premise restated on the new evidence — it is a low-*yield* claim,
not a tempo one. Record:
[`../implementation/pipeline/ogasp/stealth_exposure_metric.md`](../implementation/pipeline/ogasp/stealth_exposure_metric.md).)*


*(Shipped 2026-08-06: the **GASP class rename**. The four classes are now
`objective_exfiltration` / `objective_impact` / `objective_exfiltration_impact` /
`objective_none_c2`, named against the declared `OBJECTIVE_TACTICS` mapping and
**never** against a selection filter — the brief corrected the premise it was
commissioned under, and `gasp_schema.md` §(c) now carries the permanent
three-vocabulary crosswalk (frozen CSV label → retired spec label → tactic
label). Membership, weights and walk semantics are untouched: the divergence
report is bit-identical modulo keys, the 19:8:6:5 split and 98/62/57/39 node
counts hold, and the suite is green at the **same 1 031 tests**. Two things did
move, both diagnosed rather than absorbed. The **timeline library re-seeded** —
seeds are content-addressed on a `run_id` that embeds the profile name, so
renaming a profile re-draws its runs; `aggregate` reproducing bit-for-bit is the
proof. That flipped `ordering_stable_across_sweep_extremes` false→true, which
turns out to expose a **2.7 % near-tie at 100 runs/cell** rather than a
structural property — neither value should be quoted as a finding
(`data/ogasp/timeline/timeline_schema.md` § *Re-seeded by the 2026-08-06
rename*, ruled by Marc). And the **15 retrace goldens were re-captured
label-only** — byte-identical once the profile string is substituted, every
behavioural manifest field unchanged (`baseline/CHANGELOG.md`). 30 investigation
records were bannered rather than rewritten; the audit CSV's `stated_objective`
column stays frozen. **Flagged:** 16 gitignored `data/results/` workspaces now
have patched runners whose committed numbers were taken under the old labels.)*


1. [`2026-08-05_apt_axis_measurement_metrics.md`](2026-08-05_apt_axis_measurement_metrics.md)
   — **a metric per axis**, so the APT criterion is scored by evidence rather
   than argument. Owns axes 1, 2, 4, 8 and the lettered rows; consumes the two
   shipped readers — disengagement and stealth exposure — rather than duplicating
   them; and states
   plainly that **axis 7 cannot be moved by measurement** at all. Also owns the
   one remaining instrumentation decision: whether `MovementRecord` gains **host
   identity**. **Its §4 was corrected 2026-08-05** — two of the three consumers
   that justified the widening are discharged (the disengagement measure by a
   *count*, `n_compromised`; the disruption brief by `interrupted_by_name`), so
   the case now rests on axis 1's foothold retention and axis 8's
   repeat-configuration reader alone.

2. [`2026-08-06_knowledge_gated_apt_attacker.md`](2026-08-06_knowledge_gated_apt_attacker.md)
   — **a learning mechanism (axis 7) with an incentive-shaped decision rule on top
   (axis 6)**; stealth is a measurement that emerges, not a claim.
   **Re-scoped and retitled 2026-08-07** — it read "one mechanism across axes 5, 7
   and 8 (i)", which the code does not support: the capability never references the
   defender (it behaves identically with MTD off), so it is **not** scheme
   awareness, and the axis-8 half is now handoff (5). §0 carries the honest axis
   map and wins over the body. **Two corrections landed with it.** The decision is
   coded on **`EXPLOIT_VULN` itself**, taking the attacker model's memory as an
   input, with the verdict returning through the controller to the net — *not* as a
   routing modulator on the attacker-state seam, which was an impedance mismatch
   (memory is host/vulnerability-keyed, the seam is tactic-keyed) and which
   dissolves the hard-vs-soft gate question entirely. And the target is now known to
   be real: `Vulnerability.network()` succeeds iff `random() < complexity`, drawn
   once at catalogue generation and preserved by every per-host copy, so there is a
   genuine per-id constant to learn. **Two measurements precede any build**
   (approved): decompose exploit failures into roll-failure vs MTD interrupt vs
   no-vulnerabilities, since the brief's 49–99 % *blocked* fraction conflates them
   and only the first is reachable by memory; and sweep the complexity range across
   the lineage's own disagreement — `VULN_MIN_COMPLEXITY = 0.4` is faithful to Brown
   Table I while Zhang §4.4.3 specifies [0, 1], which makes widening it a
   lineage-grounded sensitivity rather than a convenience. The attacker recons
   quietly, remembers which vulnerabilities it has beaten, and
   spends `EXPLOIT_VULN` only when that knowledge says it will pay. **Absorbs and
   replaces the vulnerability-memory / swift-mode brief** (deleted 2026-08-06):
   that memory is its arm 1, and the axis-8 scope decision, reversal argument and
   composition hazard are carried forward in full. **"Swift mode" is retired as a
   mechanism** — it is the *latter half of the campaign*, not a state the attacker
   flips into, so it gets no arm, loses its declared idle-threshold, and is
   **measured** as an emergent accumulate-then-strike arc instead (§4.1). That may
   also remove the seam change, which was the design's largest engineering item,
   and it reaches **axis 1**, whose gap is staged advance in outcome terms.
   **Its prerequisite check has run** — two-thirds of live vulnerability ids sit on
   more than one host, so cross-host memory has traction; a mutation destroys ~80 %
   of a *host's* vulnerability set, so the key must be identity and never
   (host, vulnerability); and exact whole-host recurrence is **zero** (the apparent
   9.87 % is precisely the five never-mutated endpoints), so axis-8 primitive (i)
   in its exact-image form is dead on this substrate and must key coarser.
   **Its three remaining checks have now run too (2026-08-07), all read-only, and
   two change the design.** The **pool combinatorics falsify** the conjecture that
   narrowing the service pool revives primitive (i)'s exact-image form: the binding
   term is 16 versions per service name (`SERVICE_VERSIONS` ÷ `OS_VERSION_DICT`,
   fixed), not `services_per_os`, and exact-image collisions measure **zero at
   every setting down to the floor** over 20 000 host draws — so the form is
   unreachable by construction rather than merely absent at the default, and the
   sweep survives only as a sensitivity study over arm 1–2's effect size. The
   **objective-conditioned half is recommended dropped**: the targeted-attacker
   feasibility study already answers it, and its B4 blocker is deeper than the
   flagged one — no profile's objective connects to what the simulator scores, for
   either arm, so there is nothing to strike at without substrate work under S2.
   The **seam check holds** — the arc in routing terms needs nothing built, keeping
   the seam change off the cost — but surfaced an uncosted fork: a *hard* gate trips
   the seam's `may_zero` rule and owes a licensing rule plus a no-stall re-run,
   where a *soft* gate owes neither. Now a pre-registration item.
   The design's load-bearing move is to build the **efficiency** claim and
   *measure* stealth as an emergent consequence — optimising the metric you score
   on would make the result definitional. It also inherits the shipped exposure
   reader as its instrument, and sidesteps that reader's own kill criterion,
   because its comparison is movement-versus-movement rather than cross-arm.
   **Blocked on four rulings** (§2), of which reopening axis 6 and sanctioning
   `mtd_ai` are the two that matter. Two scope corrections were folded in
   2026-08-06: **mutation avoidance does not tick axis 8** (§5.1 — it is either
   the excluded beacon primitive or it is signal-starvation, which is not scheme
   awareness), and the sharper measurable form is **shifting the defender's
   mutation mix** rather than avoiding mutations, which §17 of the stealth record
   already wants run as a cheap falsifying test. §6.1 carries the `ch6_discussion`
   framing — *move better, not move more* — with the four results that evidence it
   and the one clause the project's own data refuses.

3. [`2026-08-08_mtd_ai_scaled_training_proposal.md`](2026-08-08_mtd_ai_scaled_training_proposal.md)
   — **what a scaled `mtd_ai` training run would have to specify, costed against
   a measured CPU baseline.** Opened 2026-08-08 by the rebuild it replaces, which
   shipped; it is the proposal only and runs nothing. Its prerequisites come from
   what the calibration measured rather than from general caution: per-worker RNG
   ownership and a declared reproducibility status (the determinism gate found an
   added defender-side draw shifts the shared streams — both of them, Python
   `random` *and* numpy/scipy, which is wider than D-29's wording), policy entropy
   as a first-class outcome (MTDAI-16), the static-degrade factor swept or
   separated out (MTDAI-17), and MTDAI-14/15 repaired first. Cost baseline:
   **692 s per agent** at Tay's own geometry, against ~22 hours for the same agent
   under the inherited per-sample replay loop.

4. [`2026-08-06_research_record_from_prompt_corpus.md`](2026-08-06_research_record_from_prompt_corpus.md)
   — **the research record**, mined from Marc's own prompts across the 110
   session transcripts. Off the axis chain entirely: it touches no code, gates
   nothing, and is gated by nothing. Scoped by measurement rather than estimate —
   **73 human prompts at ≥ 150 words, 63 900 words**, carrying most of the
   argument mass. (May and June 2026 have no transcripts at all against 92
   commits on `dev`; that window was intro/lit-review work, so the blackout is a
   one-line boundary in the record and explicitly **not** a reconstruction job.)
   Splits deliberately: the annal is `implementation/` material — the notes
   rubric bans session logs and decision registers outright — and only what the
   mining *earns* becomes a note, under the writing guide and template. Two
   outputs beyond the annal: the **abandonments and reversals** no shipped record
   owns, and a **`record-drifted` flag list** where the thinking moved on and the
   document did not (flagged for Marc, never actioned).
   **Stage 0 shipped 2026-08-08; Stages 1–3 remain deferred.** The corpus is
   backed up (`~/mtdsim-corpus-snapshot/2026-08-08/`, checksummed, untracked) and
   the extractor is committed as `tools/prompt_corpus.py` with a self-checking
   gate. Re-measured: **77 prompts / 61 164 words** at ≥ 150 words across 112
   transcripts and 25 branches. **The pinned figure was re-pinned, and why is a
   finding:** the survey's 63 900 words included two *compaction continuation
   summaries* — 3 625 words the assistant wrote about its own execution, admitted
   into the record of Marc's intent, which is the failure the brief was written to
   prevent. Reproducing the number would have meant reproducing the defect.
   **It also no longer retires at Stage 3** (Marc, 2026-08-08): the axis-5/7/8
   metrics and the Tay retrain are still being finalised, so a second pass over the
   prompts written this week is owed, and `record-drifted` cannot be measured
   against records that are still moving.


5. [`2026-08-09_mtd_ai_mechanism_selection.md`](2026-08-09_mtd_ai_mechanism_selection.md)
   — **what the reactive defender spends its budget on**, and the substrate
   blocker in front of any study of it. Replaces `2026-08-07_axis8_defender_metric_reasoning.md`,
   deleted 2026-08-09 when **axis 8 was closed on evidence**. That brief asked
   whether an attacker could manoeuvre the defender's own security metrics into
   suppressing mutation; the answer is no, for two independent reasons now
   recorded in
   [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
   axis 8 (amendment 2026-08-09). **Structurally**, triggering is clocked in every
   arm — metrics select *what* is decided at an epoch, never *when* an epoch
   occurs. **Empirically**, the one defence that reads attacker-derived metrics
   converges to constant-action policies that ignore their state (17 of 18 agents
   at one of two attractors), with the static-degrade timer supplying 29 of 31
   mutations in the quiet regime. Keep the two apart: "the substrate is time-based
   MTD, therefore metric manipulation is impossible" is an **overclaim** the
   eleven-feature state head contradicts. One cause also subsumes the axis-6
   collapse and the no-referent finding at λ = 0. **What survives** is
   defender-side and needs no attacker capability: the unmodified-reward agent
   fires **IPShuffle on 100 % of 367 mutations** — the one mechanism verified dead
   to the attacker's readable projection — and compromises about what the
   barely-moving agent does. That is a shape, **not** a result: C5 does not
   separate at three seeds. Blocked meanwhile by a measured `ZeroDivisionError`
   that kills two profiles in three at the first decision, unrepaired and awaiting
   disposition.

### Added 2026-08-09, after the chain above was written

Off the numbered chain; none of it blocks or is blocked by (1)–(5).

- **The axis context trio — restored to three, 2026-08-10** —
  [axis 4](2026-08-10_axis4_adaptivity_context.md),
  [axis 6](2026-08-09_axis6_incentive_rationality_context.md),
  [axis 7](2026-08-09_axis7_learning_context.md). Context only, commissioning
  nothing: each records what is built, measured and bounded on its axis so a
  proposal lands against the real bar. The axis-4 member and the recovery brief
  that arrived against it were superseded 2026-08-10 by the predictability brief
  and deleted in the commit that shipped it. That supersession was half right:
  the recovery brief *was* plurality-shaped and correctly landed as axis 3's
  per-verdict decomposition — but the predictability instrument is axis 3's, not
  axis 4's (`predictability.md`: "axis 4 stays DESIGNED … stationary policy,
  never adaptivity"), so deleting the axis-4 *context* left the one DESIGNED
  axis with no orientation file and no instrument commissioned. Restated
  2026-08-10 ahead of the adaptivity-instrument work, with the verdict-slice
  positive (composition splits 4/5) folded in as §3b.
- **The predictability instrument shipped 2026-08-10** as
  [`../implementation/pipeline/ogasp/predictability.md`](../implementation/pipeline/ogasp/predictability.md):
  one trace-level scalar (P, with Hill-family companions N, D, E) applied to both
  attack models over each model's own decision state, the scripted FSM pinned at
  P = 1 *by construction* and the movement attacker measured at P = 0.33–0.57 in
  the preferred-mixture regime; the verdict splits the composition in four of five
  profiles, and the experiment-2 outcome negative travels unmoved. The handoff is
  deleted; the record is the permanent account.

**Suggested order for the rest of the week:** (1), which is unblocked and which
settles the schema question and serves the rest — and note that the adjacent
`MovementRecord` widenings it was told to bundle have now all landed
(`interrupted_by_name` from the A6 repair, `n_compromised` from the disengagement
measure, `exploitability` from the exposure reader), so **host identity is the
only part left**. (2) when its ruling lands. (3) runs alongside either.

**(3) shipped, 2026-08-08, and what it returned changes (5)'s footing.** It was a
wiring job, the forensics pass turned it into a rebuild, and the rebuild now
exists: the no-op costs simulated time and stores a transition, moving is charged
against a downtime metric readable under any scheme, and the replay update is
batched. The `λ` ladder **passed its pre-registered criterion** — greedy no-op
share **+0.732** between the bottom and top halves, same sign in all three seeds,
against a bar of 0.15, with the instrument's own kill criterion intact (the λ = 0
agent declines to deploy on 2.1 % of decisions, bar 10 %). Record:
[`../implementation/pipeline/ogasp/mtd_ai_cost_calibration.md`](../implementation/pipeline/ogasp/mtd_ai_cost_calibration.md).

**Read that verdict narrowly, because two of its findings are load-bearing
elsewhere.** The response is a **step, not a gradient** — seventeen of eighteen
agents are near-constant policies and `λ` selects which constant, which is the
same degeneracy the forensics pass measured in Tay's own checkpoints, reappearing
under a *repaired* reward (MTDAI-16). And the **static-degrade guard supplied 29
of the 31 mutations** that fired at the top of the ladder, so the guard rather
than the policy is doing the defending in exactly the region the study reports as
success (MTDAI-17). Anything leaning on this defender — (5) most of all, whose
premise is that the attacker steers what the defender measures — has to reckon
with an agent that currently answers with one of two constants. The mutation-mix
half is worse off still: the ladder's C3 is **recorded not held**, because at the
top of the ladder the mix is the guard's uniform draw and at the bottom it is a
single pinned mechanism.

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
