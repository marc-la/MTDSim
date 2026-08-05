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

## Open work — five handoffs

**(1) is unblocked; start there.**

> **Reconciled on merge, 2026-08-05.** This chain was written on the boundary
> branch, before the session branches were merged into `dev`. Three corrections
> the merge forced, recorded here rather than silently applied:
>
> - **(4) has largely shipped.** `dev` built and ran the disengagement measure
>   (`35f772e`) and the iterated cost model this brief declares retired. The
>   handoff is kept, because its 2026-08-05 rescope — the promotion to axis 6's
>   metric — is not in the shipped record; it now opens with a banner pointing
>   at the artefacts. Read that before starting.
> - **(6) was invisible to this chain**, having been created on `dev` after the
>   fork. It is open, with five of its scope items unruled. Added rather than
>   dropped.
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


1. [`2026-08-04_stealth_exposure_metric_reader.md`](2026-08-04_stealth_exposure_metric_reader.md)
   — **axis 5's metric, buildable now.** A post-hoc detectability curve over an
   unmodified run's own action stream: no attacker state, no S2 question, no
   ruling gate. Now the **single** stealth handoff — the mtd_ai-consequential
   route (1b) is absorbed into it as the follow-on, with its four prerequisites
   and its cheap falsifying run recorded. **No ruling needed** for the reader;
   1(b) still needs the supervisor ruling on sanctioning the reactive defender.

2. [`2026-08-05_apt_axis_measurement_metrics.md`](2026-08-05_apt_axis_measurement_metrics.md)
   — **a metric per axis**, so the APT criterion is scored by evidence rather
   than argument. Owns axes 1, 2, 4, 8 and the lettered rows; consumes (2) and
   (4) rather than duplicating them; and states plainly that **axis 7 cannot be
   moved by measurement** at all. Also owns the one instrumentation decision
   three handoffs are waiting on: whether `MovementRecord` gains **host
   identity**. Settle that early — (4) needs it too, and (1) needs an adjacent
   widening, so both should land in one schema change and one re-capture.

3. [`2026-08-01_attacker_disengagement_measure.md`](2026-08-01_attacker_disengagement_measure.md)
   — **axis 6's metric** as of 2026-08-05: the attack-cost measure that answers
   *where would the APT eventually give up*. A projected-effort reading over
   existing runs, reported as a frontier over patience, so MTD's own economic
   claim becomes scorable. Absorbs the retired iterated-cost-model brief on a
   measurement-first ruling: MTD does not raise the attacker's *cost*, it
   destroys its *productive capacity*, so the route to axis 6 is measuring
   disengagement rather than building a better decision rule. **Blocked on
   D-09** — and, since the merge, **mostly built**: what is left is whether the
   shipped measure is ratified as axis 6's metric and the badge re-scored, which
   is a ruling rather than a build. Read its merge banner first.

4. [`2026-08-04_vulnerability_memory_and_swift_mode.md`](2026-08-04_vulnerability_memory_and_swift_mode.md)
   — **the axis-8 proof of concept**, rescoped 2026-08-05 to the stronger form:
   host configurations held in memory, so a previously-seen image confers
   success. **This reverses a ruled exclusion**, and the handoff argues the
   reversal properly rather than overriding it — the exclusion was justified on
   needing ML/RL inference, which a *memoisation* PoC does not engage. Three
   records carry that exclusion and each needs a dated amendment before any
   build. **Blocked on Marc's disposition**, and gated behind (3)'s
   `repeat_configuration_compromise_rate` reader, which tells you whether
   configurations ever recur on this substrate — if they do not, the PoC has
   nothing to memoise and that is a cheap, legitimate result.

5. [`2026-08-02_axis67_scope_finalisation.md`](2026-08-02_axis67_scope_finalisation.md)
   — **the scope decisions the freeze released**, for axes 6 and 7. Item 5 was
   ruled 2026-08-02 (static weights stay the default, the learner is kept as a
   tested negative) and items 7–9 retired by evidence; the rest are open. What it
   ships is a set of dated rulings and the closure amendment that re-adopts both
   rows into the freeze — **not a build**. It overlaps (4) at the axis-6 end, so
   rule the two together.

**Suggested order for the rest of the week:** (1), which is unblocked. Then (2),
which settles the schema question and serves the rest — and note that the
A6 widening has already landed one half of the `MovementRecord` change it owns,
so the host-identity decision is now the only part left. (3), (4) and (5) when
their rulings land — and (3) and (5) should be ruled in one sitting.

---

## Decisions waiting on Marc

Nothing below blocks a handoff except where noted; all of it blocks *closing*
one. The full rows, with costed options, are in the disposition list of
[`../implementation/intent_conformance_audit.md`](../implementation/intent_conformance_audit.md).

| # | What | Blocks |
|---|---|---|
| **D-09** | Zhang's unimplemented MTD-interruption give-up threshold (IS-INT-06) — wanted, and in which form? | **(3) entirely** |
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
