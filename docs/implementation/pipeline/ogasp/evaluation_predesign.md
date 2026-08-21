---
status: open — pre-design investigation; becomes the source for the final campaign's pre-registrations once Marc rules on §7's gates
created: 2026-08-21
updated: 2026-08-21 — §1b re-aim added same day (the disruption headline; the overhead tiers)
topic: "Pre-design feasibility study for the final experimental campaign — working backwards from the headline the dissertation wants to the experiments that would license it. Audits the workshopped 'MTD thwarted 4 APT profiles' headline against the record (not licensable; the licensable headline is stronger), answers the null-hypothesis/p-value question for a seeded discrete-event substrate, prices every claim upgrade in seeds and wall-clock from the recorded experiment-2 variance (a fresh probe over expo02's runs.jsonl, reproducing the published cell means), and orders the ruling gates a consolidated re-take would discharge. Analysis-only: no run, no ruling, no parameter change."
---

# The evaluation pre-design — what a successful experimental setup looks like, priced backwards from the headline

**Commissioned by Marc, 2026-08-21**, with an externally-workshopped framing
(pasted into the session) proposing (1) a headline of the form *"the MTD
mechanism successfully thwarted four distinct APT profiles"*, (2) a
"negative runtime performance" concession blamed on the inherited action
sets, and (3) open scope/limitations and future-work sections. This record
audits that framing against the evidence on file, then works backwards from
the headline the record *can* carry to the experiments, statistics, seed
budgets and rulings that a successful setup needs. It also answers the
question asked with the commission: **whether null-hypothesis testing and
p-values are usable for the headline claims and the baseline-versus-movement
comparison** (§4).

Nothing here runs, rules, or changes a parameter. One analysis probe was
taken over the recorded experiment-2 outputs
(`data/results/expo02_ashen_lynx/runs.jsonl`, 2 760 rows, fresh — the probe
reproduces the published cell means exactly: 5.88 / 0.60–3.70 hosts on the
movement arm, 38.40 on the baseline) to ground the seed-budget arithmetic in
measured variance rather than convention; the probe script is
session-scratch, its numbers are quoted in §5 and reproducible from the
`runs.jsonl` by the formulas stated there.

Profile labels below are the current `objective_*` set; the experiment-2
record uses the pre-2026-08-06 labels (crosswalk:
[`../gasp/gasp_schema.md`](../gasp/gasp_schema.md) §(c)).

## 1. The workshopped headline, audited — and the headline the record licenses

**"MTD successfully thwarted / neutralised four APT attack paths" is not
licensable, at any sample size.** Two independent facts on record kill it:

- **The attribution fails.** At the operating interval the movement attacker
  reaches the substrate objective in 0 of 1 200 runs — *including every
  no-MTD cell* — and its zero survives the relaxation to 2 000 s that lifts
  the baseline's off the floor
  ([`experiment_02_findings.md`](experiment_02_findings.md) §9, §17). What
  stops the movement attacker completing is the substrate and the regime,
  not the defence; "MTD thwarted it" claims for MTD an outcome MTD is not
  shown to cause. This is the measurement-versus-attribution rule in its
  plainest instance.
- **The success-shaped vocabulary is degenerate where the claim would be
  made.** Inside the degenerate region (interval ≲ 1 600 s) every
  success-rate-shaped measurement is pinned at zero and discriminates
  nothing ([`rate_feasibility_study.md`](rate_feasibility_study.md) §7;
  [`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(b)).
  "Neutralised the attack paths" is an ASR-shaped sentence uttered at an
  operating point where ASR cannot vary.

**The "negative runtime performance" concession defends against a problem
that does not exist.** A movement run costs ~0.2 s wall; the 1 728-run rate
grid took 5.1 minutes on six workers
([`rate_feasibility_study.md`](rate_feasibility_study.md) §6). There is no
runtime overhead to apologise for, and no "upstream action-set constraint"
on compute. What the workshop framing has garbled is the **action-layer
ceiling**, which is real, already owned, and not a performance concession:
the movement attacker can only be as good as the verbs it adopts, seven of
fifteen tactics are dwell-only under `v2_partial`, and §4.2.4 of the
dissertation already carries this as a scoped commitment with the mapping
declared a chosen input parameter. Writing it as a runtime problem would
replace an owned design boundary with a fictitious engineering failure.

**The headline the record licenses is stronger than the one proposed.** It
is on file, graded, and instrumented:

> Substituting a CTI-grounded attacker for the inherited scripted one
> **inverts the MTD evaluation's answer**: the defence ranking reverses
> (ρ = −0.893 at the operating interval) and the *recommended mechanism
> changes* — Service Diversity best suppresses the inherited attacker
> (90.4 %), the position-destroying family best suppresses the movement
> attacker (87.8–89.8 %). An evaluator would buy a different defence
> depending solely on which attacker the evaluation carried.

That is Row B of the criterion at its top (recommendation) grade
([`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(d2)), the
three-grade instrument's designed use
([`../../../notes/ch4_methods/evaluation_grading.md`](../../../notes/ch4_methods/evaluation_grading.md)),
and the modest-claim ceiling's sharpest permitted form: *behavioural
fidelity changes the answer* — never "the model is true", never "MTD
works". The closest honest neighbour of the wowie sentence also exists and
is defensible as a **conditional** effectiveness claim: at the operating
tempo, the right *family* of MTD suppresses the movement attacker's
compromise breadth by ~88–90 % — and it is the opposite family from the one
the baseline evaluation recommends, and the effect largely evaporates at
2 000 s ("whatever MTD buys against this attacker, it buys at tempo",
findings §10). Breadth suppression, never objective blockage, is the
quantity; the interval rides in the sentence.

**What survives from the workshopped advice** is its structural counsel,
and the repo already implements it systematically: limitations owned first
(the badge vocabulary, two NOT ADDRESSED axes visible, caveats travelling
in the row), a scope-and-assumptions discipline (envelope-not-actor, the
mapping caveat, the comparability boundary), and a named future-work
roadmap (the successor programme rows throughout the criterion). No new
mechanism is needed to satisfy it.

## 1b. Re-aim, same day — the disruption headline, and the overhead question

**Marc's correction to §1 (2026-08-21, same session): the wanted headline is
not the inversion but the direct question — *does MTD still disrupt APT
attackers?* — with the workshopped follow-on that reviewers will ask for the
system overhead (CPU, latency, bandwidth) of the shuffling.** Two findings,
one per half.

### The disruption headline is claimable — it is the ratified RQ, and the data already carries it

"Does MTD still disrupt APT attackers" **is** V5's research question ("How
does MTD perform against APT attackers?"), so the re-aim is not a new claim
but the RQ answered in disruption-denominated vocabulary — which is exactly
the vocabulary the degenerate region leaves open (breadth, time, effort;
never ASR at the operating interval). A probe over the same recorded
`runs.jsonl` (movement arm, pooled five profiles × ten seeds, within-arm
only, so no cross-clock caveat applies) shows the record already carries
**three disruption channels**:

| condition (200 s) | runs achieving any compromise | median first-compromise (s), where achieved | mean interrupts |
|---|--:|--:|--:|
| none | 100 % | 1 509 | 0.0 |
| complete_topology | 52 % | 4 198 | 75.0 |
| ip_shuffle | 56 % | 3 602 | 75.0 |
| simultaneous_multi | 48 % | 3 692 | 127.0 |
| os_diversity | 98 % | 2 140 | 52.7 |
| service_diversity | 96 % | 2 188 | 52.4 |

- **Denial** — at the operating tempo the position-destroying family denies
  the movement attacker *any* compromise in roughly half of runs (48–56 %
  vs 100 % under no MTD).
- **Delay** — where compromise happens at all, first compromise lands
  2.4–2.8× later (median 1 509 s → 3 602–4 198 s).
- **Containment** — breadth suppressed 87.8–89.8 % (E1, CI-disjoint), plus
  the friction ledger (blocked fractions, ~75–127 interrupts/run, the ~9 %
  dwell surcharge, learner-belief destruction).

At 2 000 s all three channels largely close (94–100 % achieve compromise;
median delay shrinks to ≤ 1.3×) — so the headline is honest only with its
two conditions attached: **yes, MTD still disrupts the APT-shaped attacker
— at tempo, and through the *opposite* mechanism family from the one the
inherited evaluation recommends.** The inversion is not a rival headline;
it is this headline's second clause. Wording discipline stands: *APT-shaped
behavioural envelopes derived from CTI*, never "real attackers" (no
simulation study can claim a real attacker — the workshopped "does this MTD
actually slow down a real attacker" is unclaimable by anyone at the
simulation rung, ours included); *disrupts/delays/denies/contains*, never
*thwarts/neutralises* (§1).

**Instrument consequence for §4.** First-compromise time is **censored**
data — half the runs under the strong family never compromise — so
conditional means are survivor-biased and the correct instrument is
survival analysis: Kaplan–Meier curves per condition, log-rank tests, and
restricted-mean-survival-time deltas as the effect size. This is a standard,
examiner-legible instrument, it upgrades the delay claim from a median
comparison to the field's proper form, and it slots into E3 with no new
runs. It needs a V1 hand-validation like every other statistic.

### The overhead half — why CPU/latency/bandwidth is not possible here, and what would be needed

**Not possible with what we have, structurally.** MTDSim is a discrete-event
abstraction: a mutation is a timed event seizing a resource-layer token, not
a resource consumer. There is no CPU model, no packet, no link, no queue of
traffic anywhere in the substrate — nothing for a latency or bandwidth
number to be measured *on*. The workshopped advice presupposes an
emulation/testbed evaluation; this study sits on the simulation rung of the
evaluation ladder, where the lineage sits too (none of Brown/Zhang/Ho/Tay
reports system overhead), and the methods conventions already require the
rung to be positioned explicitly. Three tiers of response, in ascending
cost:

- **Tier 0 — in scope now, analysis-only: the availability frontier.** The
  substrate *does* carry a defender-cost half: `MTD_DURATION` per mechanism
  (Zhang 2023 Table 3, badged faithful in
  [`../../provenance.md`](../../provenance.md)) and `downtime_ratio`
  ([`mtd_statistics.py`](../../../../mtdnetwork/statistic/mtd_statistics.py))
  — cumulative availability loss over the mutation execution records, this
  project's own definition, currently consumed only by the `mtd_ai` path.
  Promoting it into the reported suite prices disruption in the simulator's
  own vocabulary: **disruption bought per unit availability lost**, as a
  frontier over the interval sweep and the schemes (the 127-vs-75
  interrupt confound already shows the scheme dimension is cost-relevant).
  The honest sentence it buys: *disruption is bought with tempo, and tempo
  costs availability* — at 200 s the strong family denies and delays, and
  charges ~75–127 mutations/run at 70–110 s execution each; at 2 000 s both
  the disruption and the cost largely vanish. Needs: a metrics-suite entry,
  a V1 hand-trace, no substrate change (derived-only, so the defender
  freeze is untouched). Caveat travels in the sentence: this is
  *availability* cost, not CPU/latency/bandwidth, and is said so.
- **Tier 1 — possible, recommended against: declared resource prices.**
  Attach declared per-mutation CPU/bandwidth prices from literature and
  multiply through the execution records. Rejected on Row A grounds: it is
  a new declared family with no external anchor and no validation target
  (three-fifths of the ledger is already declared judgement), and it would
  manufacture exactly the overhead numbers a reviewer would then treat as
  measured. The Tier-0 proxy is more honest and answers the same reviewer.
- **Tier 2 — the real thing, and it is the successor programme:** an
  emulation/testbed rung — SDN (e.g. Mininet) or a container/VM testbed in
  which IP shuffling is an actual controller reconfiguration and OS/service
  diversity an actual redeploy, measuring added RTT, packet loss during
  reconvergence, controller CPU, and rule-install traffic. A different
  instrument class and at least a semester of work on its own; the
  movement layer's portability contract (the mapping as a declared seam) is
  what makes the swap-in describable as future work rather than a rebuild.
  This is the "3-year PhD roadmap" item the workshopped framing asked for,
  stated at the rung where it is true.

**What this adds to the campaign (§6):** E3 gains a *disruption panel* —
denial fraction, first-compromise survival curves with log-rank/RMST,
breadth, friction — and the Tier-0 disruption-per-downtime frontier joins
the tempo frontier (C2) as one figure family. No new runs beyond §5's
budgets; one new metric promotion and its V1 pass.

### Amendment, same session — Tier 0 is already built and already run; both rulings taken

**Correction, on a deeper look at the code and records: the Tier-0
description above under-credits the repo.** The availability measure is not
"currently consumed only by the `mtd_ai` path": a **derived disruption
ledger already exists** (`DisruptionLedger` in
`src/mtdsim/l3_simulation/movement/measures.py` — occupancy, reconfiguration
time by layer and mechanism, executions per ksec, computed entirely from the
substrate's own per-mutation execution records, snapshotted per run on
`MovementRunResult.mtd_executions`, cross-arm safe on defender-side time),
**and the frontier has already been run and reported**, pre-registered, as
[`mtd_disruption_frontier.md`](mtd_disruption_frontier.md) (2026-08-01). Its
headline strengthens the §1b disruption story rather than merely pricing it:
**whether MTD involves a trade-off at all depends on the attacker** — against
the inherited attacker the Pareto set is a singleton (Service Diversity:
best suppression at lowest occupancy, a free lunch), against the movement
attacker six of seven conditions are Pareto-efficient and the ~90 %
suppression of the position-destroying family costs occupancy 0.50–0.70. The
Tier-0 work remaining is therefore **integration, not construction**: carry
the ledger's frontier into E3's reporting beside the tempo frontier, at E3's
configuration and seed budget, with its V1 pass if any new statistic is
added.

**Rulings taken (Marc, 2026-08-21, this session):** (1) **Tier 0 is
ratified** — the availability-denominated cost frontier is the overhead
answer this work reports, with its currency caveat in the sentence. (2)
**Tier 2 is the named future work**, with the portability claim made
explicit: the model's knowledge and semantics — corpus-derived campaign
structure, objective-conditioned profiles, the Petri-net execution
semantics, the controller pattern — carry to a future emulation, because the
join is two declared inputs (mapping, parameter catalogue) authored per
environment. Documented as the future-work chapter's third programme:
[`../../../notes/ch7_future_work/emulation_rung.md`](../../../notes/ch7_future_work/emulation_rung.md).
Tier 1 stays rejected.

## 2. Working backwards — the claim ladder

Each row: the claim as the dissertation would state it → where it stands →
what upgrades it → what gates it. Grades are the grading instrument's
(magnitude / ordering / recommendation).

| # | Claim | Stands today | Upgrade needed | Gated by |
|---|---|---|---|---|
| C1 | The recommendation inverts at the operating interval (Row B, grade 3) | OBSERVED, directional at ten seeds | seed count supporting formal inference (§4–§5); re-take under `v4_failure_only` + landed sink | overlay re-key ruling; retrace re-take ruling; D-33 |
| C2 | The inversion is a property of the high-pressure regime (ρ = +0.286 at 2 000 s) | observed at two intervals only | a **tempo frontier**: ρ(interval) with CIs across ~6–8 intervals spanning the degenerate boundary — turns the caveat into a result figure | same re-take gates |
| C3 | The inversion survives scale and density (the genuinely pre-registered frontier) | UNSEEN — the pre-registration claim attaches here | the fresh-family crossing at powered seeds; wall-cost curve vs network size measured first (§5) | C1's gates, then pre-registration commit |
| C4 | The lineage's own headlines (Zhang shuffle-dominates; Brown best-single ≈ best-combo; Ho diversity-dominates) become testable and are explained by attacker dependence | designed, not run | the prior-model comparison family under both arms | none beyond C1's gates |
| C5 | Stability: conclusions do not hinge on where declared values sit in their bands | two of four families swept and held | remaining families per V6 selectivity; **equivalence framing, not failed significance** (§4d) | V6 selectivity (Marc picks the swept set) |
| C6 | Per-profile ordering by progress | BARRED at ten seeds (two independent sweeps) | ~330 seeds/cell separates every adjacent pair (§5, measured variance) — or the claim is dropped, as currently worded | none; pure power |
| C7 | Supplementary-measure findings (coverage, stealth spacing, disengagement frontier) | on record, within-arm | V4 steady-state re-take at the few-thousand-runs standard for any figure promoted to ch5 | V1 hand-validation per new statistic |

The negative-result disposition stays as pre-stated in
[`evaluation_burden.md`](../../../notes/ch4_methods/evaluation_burden.md):
if C3 breaks the inversion somewhere on the frontier, the frontier location
is the finding, and the claim narrows to the surveyed region rather than
softening.

## 3. What "successful" means, concretely

The campaign succeeds if it delivers, with every number below replaced by a
measured one:

1. **C1 at formal strength** — the inversion reported with a confidence
   interval on the rank correlation and a permutation p-value, at a seed
   count chosen by the §5 arithmetic, under the go-forward configuration
   (one overlay version, one sink implementation, D-33 ruled), so ch5
   quotes one experiment rather than experiment 2 plus four caveats.
2. **C2 as a figure** — suppression per mechanism family versus mutation
   interval, both arms, degenerate boundary marked; the interval caveat
   becomes the tempo result.
3. **C3 answered either way** — the pre-registered frontier verdict.
4. **C4's three lineage rows scored** on the grading instrument.
5. **The V6 sensitivity preamble table** filled for the swept set.
6. Every reported statistic V1-hand-validated once, at four-to-five nodes.

## 4. The statistics question — are null hypotheses and p-values usable here?

**Yes, and the field accepts them — but they answer a narrower question
than the headline, and the design must say which question each number
answers.** This section is the recommended instrument, stated so the
pre-registration can adopt it verbatim.

**(a) What a p-value can and cannot license on this substrate.** Every run
is a pure function of (config, seed) (SIM-05). The only randomness a test
can address is therefore **seed-draw variation on this simulator**. A small
p-value licenses exactly: *the difference between arms/conditions is not an
artefact of which seeds were drawn*. It licenses nothing about real
networks, real APT campaigns, or MTD outside this substrate — external
validity is carried by the modelling argument (ch4) and the envelope
discipline, not by inference. Written that way, hypothesis tests
*strengthen* the within-substrate claims (the comparability boundary in
[`../../metrics_semantics.md`](../../metrics_semantics.md) is untouched);
written as "statistically proven that MTD stops APTs", they overclaim in
precisely the way §1 bars. The lineage itself (Zhang, Ho, Tay) reports
means over repeated runs without formal inference, so formal inference here
*exceeds* lineage practice rather than merely matching it.

**(b) Estimation first, tests second.** Primary reporting: effect sizes
with confidence intervals (suppression percentages, breadth deltas, rank
correlations, each with a bootstrap CI). Tests attach to pre-registered
hypotheses only. This matches both the project's existing CI-separation
discipline and current methodological consensus, and it defuses the cheap-run
pathology: at ~0.2 s a run, *any* nonzero difference can be made
"significant" by adding seeds, so **a hypothesis is only registered with a
minimum effect size of interest attached** (e.g. a suppression difference
< 10 percentage points is not a reportable mechanism separation even if
p < 0.05; margins are Marc's to set per claim). Significance without a
declared effect floor is vacuous under these run costs.

**(c) The specific instruments, per claim.**

- **C1 (the inversion).** H₀: the two arms' defence orderings are
  exchangeable (no arm effect on ordering). Test: permutation — permute the
  arm labels over seed-level replicates within each condition, recompute
  the rank correlation between arm-wise orderings each time; p = fraction
  of permutations at least as negative as observed. Report Kendall's τ (or
  Spearman's ρ, matching the record) with a seed-level bootstrap CI beside
  it. Per-mechanism contrasts: **Mann–Whitney U** with **Cliff's δ** and
  BCa bootstrap CIs — the cell distributions are non-normal by inspection
  (floor-pinned cells: mean 0.60, sd 0.73 hosts; a t-test's assumptions
  fail exactly where MTD works best) — with **Holm–Bonferroni** across the
  seven MTD conditions per family of comparisons.
- **C2/C3 (frontiers).** Same instruments per frontier cell; the reportable
  object is the effect-versus-dimension curve with CIs, not a grid of
  p-values. Any success-rate-shaped hypothesis is registered **only for
  cells at ≥ 1 600 s** — inside the degenerate region ASR cannot vary, so a
  test on it is undefined by design, and pre-registering one there would be
  an instrument error ([`operating_point_discrimination.md`](../../../notes/ch4_methods/operating_point_discrimination.md)).
- **C5 (stability).** NHST is the *wrong shape* here: failing to find a
  difference at some n is not evidence of stability. Use **equivalence
  testing (TOST)**: declare a margin within which "the conclusion does not
  move", show the CI of the sweep-extreme difference sits inside it. The
  burden's stability half becomes falsifiable instead of an absence.
- **C6 (profile ordering).** Kruskal–Wallis omnibus, then pairwise
  Mann–Whitney with Holm, at the §5 seed budget; or the claim stays
  dropped. Jonckheere–Terpstra is available if an ordering is predicted in
  advance, which is stronger pre-registration.

**(d) Two design constraints already on record bind the statistics.**

- **D-29: seed-matched arms are independent, not paired.** The attacker and
  the mechanisms share two RNG streams, so identical seeds do not give
  matched randomness across arms. All cross-arm tests are **unpaired**;
  no Wilcoxon signed-rank, no paired-t, anywhere. (Splitting the streams
  would be a substrate change moving every golden — not recommended; the
  unpaired penalty is purchasable with seeds at 0.2 s each.)
- **V4: steady state at the few-thousand-runs standard.** Any plotted point
  promoted to ch5 reports the post-transient region, raw data kept,
  batches appended and averaged per point. The seed budgets in §5 clear
  this standard for every headline cell without strain.

**(e) Cross-arm scope.** Only event-wise quantities are cross-arm safe
(S3-R; the two arms price time differently), the per-vulnerability row
inflation (3.75×) must be resolved to `baseline_action_rows` before any
cross-arm event count is tested, and internal MTTC enters no hypothesis
until its open metrics brief is ruled (it ranks mechanisms perversely;
handoffs README, "one finding with no owner").

## 5. Feasibility — the arithmetic, from measured variance and measured wall-cost

**Wall-cost facts on record:** movement run ≈ 0.2 s (15 000 s horizon,
50-host network, six workers); experiment 2's 2 760 runs are minutes, not
hours. The one unmeasured cost is the **scale dimension** — a larger
network raises per-run cost by an unknown factor — so the C3 frontier's
first step is a ~20-run wall-cost curve over the candidate scales before
its grid is fixed (the rate study's "no silent caps" convention).

**The probe over `expo02`'s recorded runs** (this study's one analysis
act):

- **C1 is already far more robust than "directional" implies.** Resampling
  the ten seeds with replacement 2 000 times and recomputing the
  arm-versus-arm rank correlation: 95 % of resamples fall in
  [−1.000, −0.679], median −0.893, and **no resample of 2 000 produced a
  non-negative ρ**. This is an indicative bootstrap at n = 10, not the
  reported statistic — but it prices the upgrade: the inversion is not
  fragile, and a re-take at **50–100 seeds per cell** will support the §4c
  permutation test with headroom. Cost: the full experiment-2 matrix at
  100 seeds ≈ 27 600 runs ≈ **1.5–2 h** on six workers.
- **C6 is purchasable.** Movement-arm no-MTD breadth at 200 s, per profile
  (mean ± sd at ten seeds): 4.10 ± 2.33, 4.70 ± 1.77, 6.10 ± 1.52,
  6.40 ± 1.17, 8.10 ± 2.23. Normal-approximation power (α = 0.05, 80 %,
  n ≈ 16 (σ/Δ)²) for the adjacent pairs: ≈ 18, 22, 190 and 329 seeds per
  cell — the two tight pairs (Δ = 0.3–0.6 hosts) drive the budget. **~350
  seeds × 5 profiles ≈ 1 750 runs ≈ 6 min** settles the whole ordering at
  one condition; the two prior "power failure" verdicts convert to a
  measured design at trivial cost. Whether the ordering is *worth*
  claiming remains Marc's call — the record currently words it as dropped.
- **The recommendation contrast needs almost nothing.** The family-level
  2 × 2 (position-destroying vs diversity, by arm) is separated by factors
  of 2.4–5 with sds under half the gaps; it is the *within-family,
  within-arm* adjacent ranks (e.g. movement arm 0.60 vs 0.64 vs 0.72
  hosts) that no realistic seed count separates — and the honest report is
  that they are **ties within a family**, per D-38's within-pair caution,
  not a strained total order. The 2 × 2 family reading is also the
  boundary programme's own recommendation (two attacker-facing effects
  across four mechanisms).

**Budget table** (movement-arm runs at recorded cost; scale cells pending
the cost curve):

| campaign piece | shape | runs | wall (6 workers) |
|---|---|--:|--:|
| E3 consolidated re-take (C1) | exp-2 matrix, 100 seeds, `v4` + landed sink | ~27 600 | ~1.5–2 h |
| E3 tempo frontier (C2) | 2 arms × 8 defences × 5 profiles × ~7 intervals × 30 seeds | ~35 000 | ~2 h |
| C6 power run (if wanted) | 5 profiles × ~350 seeds × 1–2 conditions | ~3 500 | ~12 min |
| E4 scale/density frontier (C3) | e.g. 3 scales × 3 densities × 4 conditions × 2 arms × 5 profiles × 30 seeds | ~10 800 × cost-factor | measure first |
| E5 prior-model family (C4) | three lineage configurations × 2 arms × powered seeds | ~5–10 000 | ~1 h |
| V6 sweeps (C5) | per Marc's selectivity ruling | — | historically minutes–hours each |

**The binding resource is not compute.** Everything above fits in
overnight-or-less batches. The binding resources are (1) the §7 rulings,
(2) analysis and write-up time per campaign piece, and (3) the V1
hand-validation pass per new statistic. The feasibility verdict is
therefore: **the experimental programme the headline needs is cheap; the
programme's gates are decisions, not resources.**

> **Superstructure added 2026-08-21, same session:** the campaign below is now
> generated by the hypothesis tree
> ([`hypothesis_tree.md`](hypothesis_tree.md)) — the RQ decomposed
> hypothesis-first into AND/OR-gated claims whose leaves are these
> experiments, replacing the parameter-sweep-first framing per the
> supervisor signal recorded there. The steps and budgets below stand; the
> tree supplies the claims each step tests and the α-spending order.

## 6. The campaign, in dependency order

1. **Rulings first** (§7) — a single consolidated ruling session unblocks
   everything below.
2. **E3 — the consolidated re-take** (supersedes experiment 2 as ch5's
   source): the full matrix under `v4_failure_only`, the landed
   `retrace_sinks`, the D-33 disposition applied, corrected event counts,
   100 seeds, with C1's permutation/bootstrap instrument and C2's tempo
   frontier folded in. One experiment discharges four open dispositions
   (overlay re-key, retrace re-take, D-33's gate, the 3.75× restatement)
   and removes the "directional at ten seeds" qualifier — Row B's own
   listed re-score triggers.
3. **E4 — the robustness frontier** (C3), pre-registered *after* E3's
   configuration is frozen and *before* any frontier cell runs; wall-cost
   curve first.
4. **E5 — the prior-model comparison family** (C4).
5. **V6 sweeps** as time permits, results-preamble table filled.
6. **V1 validation** interleaved: each statistic hand-traced once before
   its first reported use.

Sequencing note: E3 before any §4.3 prose is drafted if possible — the
experimental-setup section then describes the design actually run, and the
anchor/frontier pre-registration partition
([`evaluation_grading.md`](../../../notes/ch4_methods/evaluation_grading.md))
stays clean.

## 7. The gates — open rulings this campaign is blocked behind

All are already inventoried (handoffs README; the intent audit's
disposition list); this section only orders them by what they block here.

| gate | blocks | note |
|---|---|---|
| Overlay: re-key under `v4_failure_only`? | E3's configuration | already half-forced: the chapter's Figure 4.2 caption states `v4`, so standing on `v3` numbers costs a reconciliation sentence |
| Retrace re-take | E3 | free if E3 runs — the landed implementation is the code that would execute |
| D-33 (SCAN_NEIGHBOR from uncompromised hosts) | E3 | **measured to move a ranking** (simultaneous third → first); must be ruled before the headline matrix, either way |
| Internal-MTTC brief | the metric suite E3 reports | perverse ranking on record; drop from the reported suite or own it before ch5 leans on it |
| Per-vulnerability row inflation (3.75×) | any cross-arm event hypothesis | `baseline_action_rows` is the correction; E3 adopts it and restates nothing retroactively |
| D-29 statistical treatment | §4's instrument | needs no code change — the ruling is "unpaired tests, recorded" |
| C6: is the profile ordering wanted at all? | the C6 power run | currently worded as dropped; §5 prices reinstating it |
| V6 selectivity | which C5 sweeps run | timing and target durations already named by the ruling |

## 8. Evidence anchors

- The headline result and its caveats: [`experiment_02_findings.md`](experiment_02_findings.md) §9–§10, §17; Row B in [`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(d2).
- The burden and the grading instrument: [`evaluation_burden.md`](../../../notes/ch4_methods/evaluation_burden.md), [`evaluation_grading.md`](../../../notes/ch4_methods/evaluation_grading.md).
- The degenerate region: [`rate_feasibility_study.md`](rate_feasibility_study.md) §7; [`operating_point_discrimination.md`](../../../notes/ch4_methods/operating_point_discrimination.md).
- The V-trail (V1 validation, V4 run standard, V5 spine, V6 sensitivity regime): [`supervisor_decision_register.md`](supervisor_decision_register.md).
- Open dispositions and the unowned metrics finding: [`../../../handoffs/README.md`](../../../handoffs/README.md); [`../../intent_conformance_audit.md`](../../intent_conformance_audit.md).
- The probe's data: `data/results/expo02_ashen_lynx/runs.jsonl` (untracked, present and fresh as of 2026-08-21).

## 9. Revisit conditions

- When Marc rules the §7 gates, this record's §6 sequence is either adopted
  into E3's pre-registration or amended there; the pre-registration, not
  this record, then carries the campaign's authority.
- If E3's re-take moves the inversion materially, §1's licensed headline is
  re-audited against the new Row B score before any abstract sentence uses
  it.
- If the wall-cost curve at scale breaks the §5 budgets (cost factor ≫ 10),
  the C3 grid shrinks by pre-registered priority (scale before density),
  recorded there.
- If minimum effect sizes are set (§4b), they are recorded per hypothesis
  in the pre-registration and this section gains the pointer.
