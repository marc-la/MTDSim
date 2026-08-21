---
status: open — design; becomes the experimental structure of §4.3 and the pre-registration skeleton for the final campaign once Marc rules the open items in §8
created: 2026-08-21
updated: 2026-08-21
topic: "The hypothesis tree — the RQ and its evaluation sub-question decomposed, hypothesis-first, into an AND/OR-gated claim tree whose leaf nodes are the experiments. Root: MTD disrupts the four CTI-grounded attack profiles (Marc's headline) AND the answer is attacker-dependent (the burden's divergence half). Typed nodes (scope ruling / gated claim / characterisation obligation), typed leaves (superiority / equivalence / characterisation), per-leaf epistemic status (observed / pre-registered / unrun), fixed-sequence α-spending, and the leaf→experiment mapping onto E3–E6. Inverts the parameter-sweep-first framing: every run exists as the test of a named sub-hypothesis, and the sweeps are demoted to validity leaves."
---

# The hypothesis tree — from the headline down to the experiments

**Commissioned by Marc, 2026-08-21**, after the critique of the raw form was
returned and accepted (recorded in
[`evaluation_predesign.md`](evaluation_predesign.md), whose §4 statistical
instrument and §5 budgets this design consumes). Two directives shape it:

1. **Hypothesis-first, by supervisor signal.** Marc reports feedback from Dr
   Hong that the working direction of the experimental setup — run the
   simulator under varied parameters and inspect the results — is not strong,
   because it is not *relevant*: a sweep answers no named question.
   *(Provenance: Marc's paraphrase in session, 2026-08-21; no transcript —
   conservative wording, not a numbered register ruling.)* This tree is the
   inversion: the hypothesis is stated first, decomposed by reasoning alone,
   and **an experiment exists only as the test of a leaf**. The V6 sweeps are
   not discarded — they are *demoted* from experiments to validity leaves
   (limb V below), which is where a sensitivity analysis earns its relevance:
   it defends a claim rather than generating one.
2. **The corrected logical form.** Per the accepted critique: no
   "deterministic" null-ruling — the tree carries a fixed-sequence
   α-spending discipline so the root inherits a *stated* family-wise error
   rate; the bare existential ("MTD can disrupt") is too weak to need a tree,
   so the root is the **quantified** headline; scope choices are typed as
   rulings, not hypotheses; and every leaf carries its epistemic status so
   the anchor/frontier pre-registration partition survives.

## 1. The root, its null, and its scope

**Root claim R (the RQ, V5, in its testable form):**

> **R = H1 ∧ H2.**
> **H1 (the headline):** MTD disrupts the four CTI-grounded,
> objective-conditioned attack profiles this pipeline produces — denying,
> delaying, containing and taxing them — at the operating mutation tempo, on
> this simulator.
> **H2 (the relevance/divergence half):** the disruption profile is
> **attacker-dependent** — the evaluation's answer against these profiles
> differs from its answer against the inherited baseline attacker, at a
> stated grade (magnitude / ordering / recommendation).

H1 is Marc's headline sentence made precise. H2 is the burden of proof's
divergence half ([`../../../notes/ch4_methods/evaluation_burden.md`](../../../notes/ch4_methods/evaluation_burden.md))
and the reason H1 is a contribution rather than a rerun: without H2, "MTD
disrupts the profiles" is a fact about this simulator that the inherited
evaluation would have reported anyway. With H2, the evaluation itself is
shown to depend on the threat model — which is also the direct answer to the
relevance objection above.

**The corner null the tree refutes** (the interesting form of "MTD cannot
disrupt APT attackers"):

> **N:** No mechanism in the inherited defence pool moves any disruption
> channel against any of the four profiles beyond seed-draw noise, at any
> swept mutation tempo — and the answer is the same whichever attacker the
> evaluation carries.

**Scope rulings (context nodes — ruled and cited, never tested):**

| id | ruling | source |
|---|---|---|
| S1 | The profiles are behavioural envelopes derived from CTI, one instantiation per run — never named actors, never "real attackers". No leaf can lift this. | criterion §(b), architecture §(j) |
| S2 | "Disrupt" is operationalised as four channels (§2). The success-rate channel is excluded at the operating tempo by the degenerate-region rule. | [`operating_point_discrimination.md`](../../../notes/ch4_methods/operating_point_discrimination.md) |
| S3 | All claims are within-substrate; no cross-paper magnitude comparison. | [`../../metrics_semantics.md`](../../metrics_semantics.md) |
| S4 | Emulation/testbed validation is the successor programme, not a branch. | [`../../../notes/ch7_future_work/emulation_rung.md`](../../../notes/ch7_future_work/emulation_rung.md) |
| S5 | Every unrun leaf executes on the post-gate configuration (`v4_failure_only`, landed sink, D-33 ruled, corrected event counts). | predesign §7 |
| S6 | Cross-arm comparisons are event-wise or defender-side only; unpaired tests only (D-29). | [`measurement_suite.md`](measurement_suite.md) §(d), predesign §4d |

## 2. The disruption channels — the operationalisation layer

Four channels, each with its measure already in the suite
([`measurement_suite.md`](measurement_suite.md)) and its control built in
(the `none` condition at the same operating point — attribution is a
property of every leaf, not a separate branch):

| channel | claim shape | measure | test type |
|---|---|---|---|
| D-deny | MTD reduces the fraction of runs in which the attacker compromises *any* host | first-compromise indicator per run | superiority (two-proportion / Mann–Whitney on indicator) |
| D-delay | MTD postpones first compromise | time-to-first-compromise, **censored** at horizon | superiority (Kaplan–Meier / log-rank; RMST delta as effect size) |
| D-contain | MTD reduces compromise breadth | distinct hosts compromised | superiority (Mann–Whitney, Cliff's δ) |
| D-tax | MTD forces re-work and friction | interrupt-destroyed event time, confusion penalty share, blocked-action re-work (`cost_ledger`) | superiority, movement-arm-only (time fields are arm-local) |

Deliberately **excluded** channels, with reasons on record: objective denial
(the profiled attacker reaches the objective 0/400 *without* MTD at the
relaxed interval — the zero belongs to the attacker on this substrate, not
to the defence; findings §17); belief destruction (the learning arm is
exploratory by pre-registration — it reports under C, never gates).

## 3. The tree

```
R  "How does MTD perform against the APT attack profiles?"   [AND: H1 ∧ H2; V gates interpretation]
│
├── H1  MTD disrupts the four profiles                        [AND over the four profiles]
│   ├── H1.P1  objective_exfiltration is disrupted            [OR over channels]
│   │   ├── L-P1-deny     D-deny    vs none @ 200 s           [OR over 7 MTD conditions, Holm-corrected]
│   │   ├── L-P1-delay    D-delay   vs none @ 200 s
│   │   ├── L-P1-contain  D-contain vs none @ 200 s
│   │   └── L-P1-tax      D-tax     vs none @ 200 s
│   ├── H1.P2  objective_impact               … same four leaves
│   ├── H1.P3  objective_exfiltration_impact  … same four leaves
│   └── H1.P4  objective_none_c2              … same four leaves
│
├── H2  the answer is attacker-dependent                      [graded, not binary]
│   ├── L-H2-rank   the defence ordering differs between arms (permutation test on
│   │               rank correlation; observed ρ = −0.893 @ 10 seeds)     [ordering grade]
│   ├── L-H2-rec    the top-ranked mechanism differs                      [recommendation grade]
│   └── L-H2-prior  each lineage headline (Zhang / Brown / Ho), re-run under
│                   both arms, holds or falls per arm                     [characterisation, graded]
│
├── V  validity — gates the *interpretation* of H1 ∧ H2       [AND]
│   ├── V-tempo    the disruption attenuates as the interval relaxes, and each
│   │              metric is reported only where it can vary  [characterisation with
│   │              a directional test; doubles as the attribution instrument]
│   ├── V-stab-w   verdicts stable across routing-weight bands      [equivalence: OBSERVED, held]
│   ├── V-stab-d   verdicts stable across duration bands            [equivalence: OBSERVED, held]
│   ├── V-stab-r   verdicts stable across reset-fraction bands      [equivalence: UNRUN]
│   ├── V-map      verdicts survive the tactic→verb mapping choice  [UNRUN — the largest
│   │              open risk on record (findings §20); bounds every claim until run]
│   └── V-gen      H1/H2 survive network scale and density          [pre-registered frontier: UNRUN]
│
└── C  characterisation obligations                           [ungated; mandatory reporting]
    ├── C-cost     the disruption is priced: suppression vs occupancy frontier
    │              (free lunch vs steep trade — OBSERVED, frontier record)
    ├── C-family   per-mechanism resolution as the 2 × 2 family contrast
    │              (position-destroying vs diversity; within-family ranks reported as ties)
    ├── C-agg      the aggregate envelope beside the four objective profiles
    └── C-supp     supplementary channels (spacing/stealth contrast, learner-belief
                   destruction, disengagement frontier) — reported where they stand
```

**Gate semantics.** An AND node holds when every child holds; an OR node
when at least one child survives its multiplicity correction. A leaf that
fails to reject is **not** evidence for N at that leaf — each gated node
carries a failure disposition (§6). V does not gate whether H1/H2 *hold*;
it gates what holding *means*: an H1 verdict with V-map unrun is stated as
bounded by the mapping caveat, exactly as Row B is today.

## 4. The leaf contract

Every leaf is well-formed only as the full tuple — this is the
pre-registration row it becomes:

> **id · claim sentence · type** (superiority / equivalence /
> characterisation) **· measure** (suite function) **· operating point ·
> control · test · minimum effect size** (Marc's to set; mandatory — at
> 0.2 s/run, significance without an effect floor is vacuous) **· seed
> budget** (from predesign §5) **· status** (observed / pre-registered /
> unrun) **· failure disposition · experiment cell.**

Current status census, so hindsight is not laundered into prediction: the
sixteen H1 leaves and L-H2-rank/rec are **observed at ten seeds**
(experiment 2 and the probes over its recorded runs) — their re-take at
powered seeds under S5 is what gets pre-registered, and they are reported
as anchor-motivated, per the grading note's anchor/frontier partition.
V-stab-w and V-stab-d are **observed and held** (the two instalments).
C-cost is **observed** (the frontier). L-H2-prior, V-stab-r, V-map and
V-gen are **unrun**, and they are the only leaves for which a genuine
prediction can be claimed.

## 5. The α-spending discipline

Fixed-sequence gatekeeping, committed here so the root inherits a stated
family-wise error rate rather than a rhetorical one:

1. **H1 first, α = 0.05.** Within each profile branch, Holm across that
   branch's channel × condition leaves; the branch holds if any corrected
   leaf rejects. The AND over four profiles needs no further correction
   (an AND is conservative — it can only lose power, which the seed budget
   buys back; predesign §5 prices the compounding).
2. **H2 second**, at full α once H1 has resolved (fixed-sequence
   procedures pass α forward): the permutation test on the cross-arm rank
   correlation, then the recommendation contrast.
3. **V-tempo, V-gen, V-map** are characterisation/equivalence shaped and
   spend no α from the chain; equivalence leaves use TOST at their own
   declared margins.

Power compounds down the AND: four branches at 90 % power each give ~66 %
for H1 entire, which is why the re-take runs at 100 seeds per cell rather
than ten (predesign §5 — the bootstrap already shows the observed effects
are far from marginal, so the real risk is per-profile denial/delay leaves
in the weaker diversity conditions, which the OR structure absorbs).

Two execution risks this discipline does not cover by itself, named here so
they are built for rather than discovered (they are the substance of the
generic caution that a design this wide needs careful gate execution and
power management):

- **Power does not transfer to new scales.** The §5 budgets are derived
  from variance measured on the 50-host network; nothing licenses assuming
  either the wall-cost *or the variance* at E4's larger scales. E4's
  pre-registration therefore opens with a **pilot that sizes both** — the
  wall-cost curve already required, plus a small-seed variance estimate per
  scale from which E4's own seed budget is computed before its grid is
  fixed. A frontier cell run at a seed count inherited from a different
  geometry is the power failure this tree exists to prevent.
- **The verdict bookkeeping is mechanical or it is wrong.** Sixteen H1
  leaves × conditions under Holm, a fixed-sequence chain, TOST margins on
  the equivalence leaves — done by hand across analysis sessions, this
  *will* drift. The leaf table (§4 tuples) is therefore maintained
  machine-readable, and the campaign's analysis computes every gate verdict
  from it programmatically, so the tree's logic is executed by code that
  can be reviewed once rather than by discipline that must hold every
  time. The equivalence margins are declared in the same table (they ride
  §8 ruling 1, beside the effect floors), because a TOST margin chosen
  after seeing a sweep is not an equivalence test.

## 6. Failure dispositions, per gated node — stated before anything runs

- **An H1 profile branch fails** → the headline narrows honestly: "MTD
  disrupts *n* of the four profiles", with the failing profile's channels
  reported — a finding about which behavioural envelope the defence pool
  cannot touch, not a suppressed row.
- **H1 fails entirely** → the burden note's negative disposition applies
  verbatim: the contribution retreats to the construction method and the
  negative demonstration, stated in advance so it cannot be reframed.
- **H2 fails (orderings agree)** → H1 stands but the fidelity claim
  retreats to the magnitude grade or below; the thesis's central claim is
  re-worded per the burden note. The inversion's disappearance under the
  post-gate configuration would itself be a reportable reversal.
- **V-map moves a verdict** → the affected claims re-scope to "under the
  reported mapping", and the mapping study's cells become the boundary of
  every H1/H2 sentence — this is the one leaf that can demote the whole
  tree, which is why it is in it.
- **An equivalence leaf fails (a band extreme flips a verdict)** → the
  claim is stated at the declared value with the sensitivity disclosed in
  the V6 preamble table — the sweep's purpose, now attached to a named
  claim.

## 7. Leaves → experiments

The tree generates the campaign; each experiment is now the test of named
leaves rather than a parameter excursion:

| experiment | leaves it discharges | shape (predesign §5 budgets) |
|---|---|---|
| **E3** — consolidated re-take + tempo frontier | all 16 H1 leaves; L-H2-rank, L-H2-rec; V-tempo; C-cost (re-priced at E3 config); C-family; C-agg | full matrix @ 100 seeds + ~7 intervals @ 30 seeds |
| **E4** — generality frontier | V-gen | scale × density grid, pre-registered after E3 freezes configuration; wall-cost curve first |
| **E5** — prior-model comparison | L-H2-prior | three lineage configurations × both arms |
| **E6** — mapping sensitivity | V-map | candidate mappings × the H1/H2 core cells |
| (V6 sweeps, standing) | V-stab-r; V-stab-w/d already held | per V6 selectivity |
| (no experiment) | C-supp | reported from existing records |

The §4.3 skeleton's two families are preserved, reorganised: the
prior-model family is the L-H2-prior branch; the fresh-evaluation family is
E3 + E4. What changes is the presentation order the chapter can now use —
hypothesis, then its leaves, then the factor table as the leaves'
realisation — which is the structure the supervisor's signal asks for.

## 8. What Marc must rule before this becomes the pre-registration

1. **Minimum effect sizes per channel** (D-deny/delay/contain/tax) — the
   floors that stop cheap-run significance (§4). Recommendation: set them
   from operational meaning (e.g. delay ≥ 1.5× RMST, containment ≥ 20
   percentage points), not from the observed values.
2. **Is E6 (mapping sensitivity) in scope for the honours timeline?** It is
   the largest open risk and the only leaf that can demote the tree; if it
   cannot run, V-map is carried as a standing bound in every claim sentence
   instead, as today.
3. **V-stab-r** (reset fractions) — sweep, or own as undischarged in the V6
   table.
4. **The §7 gates** from the predesign (overlay, D-33, retrace, event
   counts) — unchanged, and they precede every unrun leaf.
5. **Whether H1's AND is over four profiles or five** (the aggregate
   envelope currently rides as characterisation, C-agg).

## 9. Evidence and anchors

- The commissioning chain and the statistical instrument this tree consumes:
  [`evaluation_predesign.md`](evaluation_predesign.md) §§1b, 4, 5, 7.
- The burden and grading instruments the limbs implement:
  [`../../../notes/ch4_methods/evaluation_burden.md`](../../../notes/ch4_methods/evaluation_burden.md),
  [`../../../notes/ch4_methods/evaluation_grading.md`](../../../notes/ch4_methods/evaluation_grading.md).
- The observed leaves: [`experiment_02_findings.md`](experiment_02_findings.md)
  (§9–§13, §17, §20), [`mtd_disruption_frontier.md`](mtd_disruption_frontier.md),
  [`weight_sensitivity_study.md`](weight_sensitivity_study.md),
  [`rate_feasibility_study.md`](rate_feasibility_study.md).
- The measures every leaf names: [`measurement_suite.md`](measurement_suite.md).
- The dissertation slots this structure feeds: `sec:experimental-setup`
  (`subsec:burden`, `subsec:metrics`, `subsec:families`) and the results
  chapter's V6 preamble ([`../../../thesis/dissertation.tex`](../../../thesis/dissertation.tex)).

## 10. Revisit conditions

- Marc's §8 rulings convert this design into the E3 pre-registration; the
  tree is then frozen there and this record points at it.
- If the supervisor's next review changes the RQ decomposition (V5), the
  limb structure re-derives from the new spine; the leaves survive, the
  gating may not.
- If any observed leaf inverts under the post-gate configuration, its
  branch re-scores and §6's dispositions apply — the tree is the structure
  for reporting that honestly, not a promise that it will not happen.
