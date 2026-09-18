---
status: open — structural question, Marc's ruling owed
created: 2026-09-08
topic: "Where the two evaluation limbs live: ch5 experimental setup vs ch6 results. Corrects a misread (ch5 = evaluate only, not capture/model), tests Marc's proposed three-section results chapter against the record, and names the one asymmetry that breaks it."
---

# Ch5 / ch6 — finding a home for the two limbs

## The correction

Ch4 (APT attacker model) answers **capture** and **model**. Ch5 is the
methodological home of **evaluate** only (`ch5_experimental_setup/README.md`).
That is unchanged and was never in doubt.

## The real question

"Evaluate" has **two experiment-bearing limbs**
([`../implementation/pipeline/ogasp/hypothesis_tree.md`](../implementation/pipeline/ogasp/hypothesis_tree.md) §8c):

- **Limb A — fidelity.** Does the model hit the fidelity claimed? Instrument:
  the eight-axis criterion and its badges. Not answered by MTD runs.
- **Limb B — disruption.** H1 (MTD disrupts the four profiles) ∧ H2 (the answer
  is attacker-dependent), with **V** (sensitivity = validity) and **C**
  (characterisation) hanging under it.

The current ch5 skeleton (`sec:burden`, `sec:metrics`, `sec:families`) carries
Limb B's furniture only. Limb A is *scored* nowhere and *verdicted* in ch7.
Sensitivity has no stated home at all. That is the gap Marc is feeling.

## Marc's proposed structure, tested

Proposal: ch5 sets up all of it; ch6 results in three sections — capture,
model, evaluate — with evaluate carrying the comparison plus a look at the
model's own implemented parts.

**Verdict: sound in shape, with one asymmetry that has to be resolved.**

- It is right that ch5 is the setup for *everything that gets reported*, and
  right that the model's self-assessment needs a results home. Both are
  improvements on the current skeleton.
- **The asymmetry: capture has no experiments.** SQ1 is construction, not a
  hypothesis (hypothesis_tree §8c). Its evidence — corpus extraction, the
  objective partition, the technique graph — is reported in ch4 as
  construction. A symmetric three-section results chapter invents a section
  with nothing to report in it.
- **Second conflation:** "evaluate looks at itself" bundles two different
  things — Limb A (fidelity badges, incl. the measured negatives) and the V
  limb (does the disruption verdict survive the declared parameters). They
  answer different sub-questions and should not share a section.

## Recommendation

Two limbs, carried consistently through both chapters:

- **ch5 setup** — (1) what must be shown: the burden (stability ∧ divergence),
  the grading instrument, the failure dispositions, the scope rulings;
  (2) how "disrupt" is measured: four channels, the discrimination gate, the
  comparability boundary; (3) what runs: leaves → experiments (E2-R, E3–E7),
  with the sensitivity sweeps stated as *validity leaves*, not experiments.
- **ch6 results** — two parts, not three: **fidelity** (Limb A: axis-by-axis
  evidence, the measured negatives) and **MTD evaluation** (Limb B: H1, H2,
  with V reported inside it as the sensitivity preamble, and C as
  characterisation). Capture stays in ch4 as construction.
- **ch7** keeps the fidelity *verdict* and the scoring discipline.

## Open ruling

Whether Limb A gets a full ch6 section or stays a ch7 verdict fed by ch4's
evidence. The three-unit ch5 budget assumes the latter; a ch6 fidelity section
costs units the ledger has to find.

## The placement map (2026-09-08, second pass)

### The rule that resolves it

"Results = numbers only, no defence" is one notch too strict and is what makes
everything look like it belongs in the discussion. The workable rule:

> **ch5 commits the criterion. ch6 reads it. ch7 says what it means.**

A verdict stated in ch6 ("H2 holds at the ordering grade, at 200 s, 100 seeds")
is not a defence — it is the pre-registered instrument being applied. That is
exactly what the grading instrument and the failure dispositions were committed
in advance *for*. Anything not licensed by a ch5-committed criterion is ch7.

### Where each thing lives

| Thing | ch5 setup | ch6 results | ch7 discussion |
|---|---|---|---|
| Burden of proof (stability ∧ divergence) | states it | reports both halves met/unmet | what it means if unmet |
| Grading instrument (magnitude/ordering/recommendation) | commits it | applies it per comparison | — |
| Failure dispositions | states them in advance | applies the one that fired | — |
| Discrimination gate (operating point) | states the rule the design obeys | reports which metrics could vary at which tempo | the transferable methodological finding |
| Sensitivity runs (V-stab-w/d/r, V-map, V-gen) | declares them as **validity leaves**, with bands | the V6 preamble table: parameters, ranges, observed effects | — |
| Sensitivity *interpretation* | — | "the verdict did/did not move" beside the claim it defends | the identifiability finding, the shape-at-the-corner, the declared-parameter honesty |
| Fidelity (Limb A, eight axes) | states the criterion + scoring discipline | the measured axis evidence (2, 3 positive; 6, 7 negatives) | the fidelity verdict and the badge ceiling |
| Comparability boundary | states it | every cross-arm number stated inside it | the limits it imposes on the contribution |

### The three comparisons — name them separately

They are one word in conversation and three different experiments:

1. **Cross-arm** — movement vs inherited attacker. This is **H2**, the thesis
   claim. ch6 states the grade; ch7 states what a threat-model-dependent
   evaluation means for practice.
2. **Cross-mechanism** — which MTD wins against a given attacker. This is
   **H1** and the 2x2 family contrast (severance vs surface re-roll).
3. **Cross-lineage** — Zhang / Brown / Ho headlines re-run on one simulator
   under both arms (**E5 / L-H2-prior**). Makes published claims testable
   rather than cited; the lineage's internal disagreement is the phenomenon,
   not something to reconcile.

### Does the fidelity defence need results?

**Yes, in part — it cannot be qualitative-only.** Axes 2 and 3 are badged
DEMONSTRATED, and those badges rest on measurement (execution-level profile
divergence against its split-half null; strategic plurality). Axes 6 and 7
carry *measured negatives* (the disengagement frontier's censoring half; the
pool-invariant exploit-learning null). Dropping the numbers forces four badges
down. Two honest ways to carry it:

- **(a) A short ch6 fidelity section** — an axis-evidence table plus the two
  negatives. Cleanest, costs units the ledger must find.
- **(b) Evidence rides in ch4 as construction/validation**, ch7 scores it.
  Cheaper; risks the fidelity claim reading as asserted because its numbers sit
  three chapters from its verdict.

Recommendation: **(a)**, small — the measured negatives are among the most
credible things the work owns, and burying them in ch4 wastes them.
