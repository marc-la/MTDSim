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

## Open work — four handoffs

**(1) is unblocked; start there.** (2) and (3) are a pair — (3) supplies the
defender arm (2)'s consequential half needs. (4) is independent of the axis chain
and can run alongside any of it.

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
   — **one mechanism across axes 5, 7 and 8 (i)**, with axis 6 contested.
   The attacker recons quietly, remembers which vulnerabilities it has beaten, and
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

3. [`2026-08-07_mtd_ai_cost_calibrated_rebuild.md`](2026-08-07_mtd_ai_cost_calibrated_rebuild.md)
   — **rebuild `mtd_ai` into an agent that trades cost against risk, and prove it
   does before any Kaya time is spent.** Supersedes and absorbs the reintegration
   brief (2026-08-06), which is kept, bannered and `status: superseded` because
   its defect list, determinism gate and wiring seam all survive. Both of that
   brief's load-bearing premises did not, per
   [`../implementation/pipeline/ogasp/mtd_ai_forensics.md`](../implementation/pipeline/ogasp/mtd_ai_forensics.md):
   **every figure in Tay's paper was produced by a uniform random selector** —
   `epsilon` defaults to 1.0 in `execute_ai_model` and the harness never overrides
   it, so `predict` was never called (verified at five commits) — which dissolves
   the reuse-vs-retrain question rather than answering it, since the project's
   existing random-scheme arm already *is* the faithful replication of those
   results. And **the do-nothing action advances no simulated time**: the
   `yield` sits inside `if action > 0:`, so a no-op is rejection sampling under
   ε-greedy and a livelock under a greedy policy. The root cause is upstream of
   both — `calculate_reward` weights `mtd_freq` and `time_since_last_mtd` at
   **zero**, so **"always deploy" is optimal** and action 0's Q-value is never a
   TD target. The checkpoints are separately unusable: an `8/3 → 5` signature the
   live head cannot produce, `moving_variance` collapsed to exactly 0 by
   batch-size-1 `fit`, and 34 of 55 with a policy entropy under 0.5 bits (one
   never trained at all). **The build is therefore Tay's own unimplemented
   T-TS-02** — downtime / operational impact, as a *network metric only* (Marc,
   2026-08-07) — plus a reward charge against it. Its kill criterion is a CPU-scale
   `λ` ladder: if the no-op share does not move with the cost weight, the agent is
   trading nothing off and Kaya cannot fix it. **Ends at a go/no-go, not a trained
   model.**

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
   **Timing: Stage 0 now, Stages 1–3 in about a week** — the extractor and a
   snapshot of an unbacked corpus should not wait, but the analysis wants the
   implementation settled and first results in hand.


**Suggested order for the rest of the week:** (1), which is unblocked and which
settles the schema question and serves the rest — and note that the adjacent
`MovementRecord` widenings it was told to bundle have now all landed
(`interrupted_by_name` from the A6 repair, `n_compromised` from the disengagement
measure, `exploitability` from the exposure reader), so **host identity is the
only part left**. (2) when its ruling lands. (3) runs alongside either.

**(3) grew, 2026-08-07.** It was a wiring job; the forensics pass turned it into a
rebuild. That does not block (2) — (2)'s arms 1 and 2 need no reactive defender —
but it does mean **(2)'s consequential half now waits on a build rather than on a
ruling**, and the R-B ruling it was blocked on ("sanction Tay's agent") is a
narrower question than it was: what would be sanctioned is no longer Tay's
trained agent, because there isn't one.

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
| **D-29** | Mechanisms and attacker share one RNG stream, so seed-matched arms are **independent, not paired** — record-grade | seed budgeting |
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
