---
status: durable
created: 2026-08-19
updated: 2026-08-19
topic: "L3/L4 — the failure tactic-to-tactic weight set presented as a decomposition: (declared failure kernel) × (lifecycle-distance kernel) → the committed matrix; the two-pair walkthrough; the kernel-discrepancy ruling (open); the §4.2.4.2 scaffold and the appendix wiring"
---

# The failure weight set, decomposed then aggregated — provenance on the page

**Status:** durable. Executes the presentation half of the 2026-08-19 provenance
brief (`handoffs/2026-08-19_failure_weight_provenance.md`): the failure
tactic-to-tactic weight set was already rule-generated and reproducible
([`success_failure_overlay_design.md`](success_failure_overlay_design.md) §2–§3,
[`weight_sensitivity_study.md`](weight_sensitivity_study.md) §1), but nothing on
the page *showed* that — a reader of `failure.json` saw 210 numbers. Marc's
framing (2026-08-19): the values "are somewhat random, but they need to be in a
defensible manner", so present the matrix as **failure kernel × distance kernel
→ aggregated matrix**, decomposed then aggregated, "so it is very clear how they
got their results". This record is where that presentation lives, together
with the one ruling the brief left open (§4).

**Nothing about the values changed.** No rule value, no kernel parameter, no
registry version. `python -m mtdsim.l3_simulation.controller.rules --check`
still reproduces every committed view (0 of 420 differing cells per version).
The generator below *reads* the compiler's own per-cell output
(`rule`, `d`, `delta`, `v`) and draws it; it derives nothing of its own.

**Reproduce**

```
PYTHONPATH=src python tools/failure_weight_decomposition_figure.py \
    [--version v3_persistent_backward] [--verdict failure] \
    [--walk a->b ...] [--dry-run-adjacent] [--no-compile] [--no-tables]
```

writes `docs/thesis/figures/failure_weight_decomposition.{tex,pdf}` (the
three-panel figure, TikZ at 12 pt) and `docs/thesis/tables/outcome_overlay_weights.tex`
(the appendix tables: both rule ledgers, the kernel parameters, the complete
success and failure sets for the version), and prints every number quoted
below. `--verdict success` produces the sibling decomposition of the success
set on demand; it is not committed, because the sibling feasibility study
([`success_null_overlay_feasibility.md`](success_null_overlay_feasibility.md))
may retire the success set — its ruling slot is open. The failure decomposition
is invariant to that ruling either way.

---

## 1. The two kernels, and why the product is the whole story

Every one of the 210 failure values (15 sources × 14 destinations, no
self-loops) is

```
    failure(a→b)  =  rule_value_failure(a→b)  ×  d(a,b)
```

and each factor is small enough to print on one line.

**(a) The failure kernel — nine declared semantics rules, first match wins.**
The rule order is the rules file's (`outcome_rules.json`, `failure_rules`), and
the compiler's `_failure_rule` applies it: two dependency gates, then two
dampers, then the relationship ladder. Key letters are the figure's.

| key | rule | value | fires on | pairs |
|---|---|--:|---|--:|
| A | `ia_gate_foothold` | 0.02 | `initial-access` failed → any foothold-dependent destination | 12 |
| B | `recon_gate_initial_access` | 0.4 | `reconnaissance` failed → `initial-access` | 1 |
| C | `recon_gate_deep` | 0.05 | `reconnaissance` failed → any foothold-dependent destination | 12 |
| D | `preintrusion_damper` | 0.25 | a post-intrusion source falling backward to a pre-foothold destination | 35 |
| E | `execution_damper` | 0.35 | any backward move whose destination is `execution` | 11 |
| F | `backward` | 0.9 | else backward | 26 |
| G | `lateral` | 0.7 | else within-stage | 65 |
| H | `forward_from_foothold` | 0.35 | else forward, source post-intrusion | 35 |
| I | `forward_from_prep` | 0.3 | else forward, source pre-foothold | 13 |

Eight distinct values (E and H coincide at 0.35 by separate arguments — the
ledger keeps them as two rules because their rationales differ). The
relationship term (forward / lateral / backward) is read from the four
consensus stages, not the retired five-band prior
([`weight_sensitivity_study.md`](weight_sensitivity_study.md) §1.1). Each rule's
one-sentence rationale, tier, status and confidence live in the rules file and
are reproduced in the appendix table; the adversarial-scrutiny history is the
ledger ([`../../declared_value_provenance.md`](../../declared_value_provenance.md)).

**(b) The distance kernel — a pure function of the stage offset.** With
`Δ = s(b) − s(a)` over the consensus stages (preparation 0, intrusion 1,
post-intrusion operations 2, objective 3;
[`lifecycle_consensus.md`](lifecycle_consensus.md) §4) and the declared
parameters `γ = δ = 0.25`, `z = 0.1` (§6 there; `v3_persistent_backward`):

| Δ | d | pairs | reading |
|--:|--:|--:|---|
| 0, ±1 | **1** | 154 | within a stage, or to the adjacent stage — untouched |
| ±2 | **0.25** | 44 | a two-stage skip or a deep fallback — quartered |
| ±3 | 0.0625 → **0** | 12 | under the floor: the preparation ↔ objective corners read as exactly zero |

The kernel is block-structured (panel (b) of the figure is four stage blocks
on each axis), so the distance term touches exactly 56 of the 210 pairs and
leaves 154 alone.

**(c) The product.** Fourteen distinct values; 12 exact zeros; and because
(a) and (b) are each printed in full, any cell of (c) resolves by eye to one
rule letter and one distance factor. That is the defensibility claim in a
sentence: *the failure matrix has nine declared numbers and three declared
parameters in it, and nothing else.*

What the decomposition does **not** claim: that any magnitude is attested.
The failure side is the `declared-judgement` tier by construction
([`success_failure_overlay_design.md`](success_failure_overlay_design.md) §4 —
incident reports record what worked, not what an attacker did after a step
failed), and the distance kernel's magnitudes are declared with only the decay
*pattern* attested. The sweep is what defends where the magnitudes sit (§6);
it did not produce them.

---

## 2. Two pairs walked end to end

Printed by `--walk`; the figure's cells carry the same three numbers.

**`initial-access → discovery`** (stage 1 → 2, Δ = +1).
The source is `initial-access` and the destination is foothold-dependent, so
the first rule in match order fires: **A `ia_gate_foothold` = 0.02** (a failed
intrusion leaves no foothold to discover from — the declared ~45:1 soft floor,
not a hard zero, so the regression bridge can dominate the out-set). Adjacent
forward travel is not penalised: **d = 1**. Committed value **0.02 × 1 = 0.02**.
Composed on a net, this cell is why the failure mass out of `initial-access`
collapses onto the synthetic `initial-access → reconnaissance` bridge
(83 % on the sparse profiles; design record §2.3).

**`exfiltration → execution`** (stage 3 → 1, Δ = −2).
Neither gate applies (the source is not `initial-access` or
`reconnaissance`); the pre-intrusion damper does not apply (`execution` is
not pre-foothold); the move is backward and its destination is `execution`,
so **E `execution_damper` = 0.35** fires (re-running code against a held
foothold is a forward-level retry, not a 0.9 "back to the drawing board"
regress). It is a two-stage fallback: **d = δ^(2−1) = 0.25**. Committed value
**0.35 × 0.25 = 0.0875**. Before the 2026-07-28 persistence ruling (`δ = 0.5`)
this cell was 0.175 — the one-parameter change that produced `v3` is visible
here as a halving, with the rule value untouched.

Two boundary cells, for completeness: **`initial-access → reconnaissance`**
(Δ = −1) is **F `backward` = 0.9 × d = 1 = 0.9** — the regression bridge,
exempt from the pre-intrusion damper because its source is itself pre-foothold,
and untouched by distance because it is adjacent; and
**`reconnaissance → impact`** (Δ = +3) is **C `recon_gate_deep` = 0.05 × d = 0
= 0** — the canonical long jump S1 named, zero by the floor rather than by a
per-pair edit (and, on this corpus, an edge no profile net carries;
[`weight_sensitivity_study.md`](weight_sensitivity_study.md) §2).

---

## 3. Presentation decisions

- **Three aligned 15 × 14 views on one stage-grouped axis**, one 0–1 grey
  scale across all three panels, every cell printed — the diagnostic register
  the brief asked for: no arrows, no highlights, no circles. The rule letter
  rides in each (a) cell and the signed offset as a subscript in each (b)
  cell, so the reader never has to look anything up to take a (c) cell apart.
- **Axis order.** Consensus stage, then the ATT&CK reading order within a
  stage — the order `fig:l1-graph` uses, with one move: `command-and-control`
  sits in the post-intrusion block rather than between `collection` and
  `exfiltration`, because the consensus seats it at stage 2. Within-block
  order asserts nothing (the consensus declares the middle unordered).
- **Rendered as a TikZ standalone at the document's 12 pt base** under the
  same conventions as `tools/l1_attack_graph_figure.py` (greys carry the
  value on one ramp; no colour carries a category; document font), so the
  two figures read as one system. The figure is 464 pt × 535 pt and takes a
  float page on its own; the appendix tables compile with no overfull boxes
  (checked in a scratch copy of the thesis, 2026-08-19).
- **No hard-coded numbers.** The tool reads the rules, the consensus and the
  registry manifest, and prints every number a caption quotes. If a rule
  value or a kernel parameter is ever re-declared, re-running it regenerates
  the figure and tables and re-prints the caption numbers to re-check.

---

## 4. The kernel discrepancy — ruling open, recommendation recorded

**The discrepancy.** Marc's dictated §4.2.4.2 narrative: "if the transition
was within the same phase, it would be weighted a high value; if it was one
away, it would be weighted a lower value; if it was two away, an even lower
value; and the maximum distance is weighted zero." The declared kernel
penalises nothing at one stage: `d = 1` for Δ = ±1, `0.25` at ±2, `0` at ±3.
Marc's "and if not, that's how it should be done" is a candidate
re-declaration. Flagged in the tex (`[WRONG]` at the overlay paragraph); the
brief asks for one question with a recommendation.

**The candidate, costed (`--dry-run-adjacent`).** The nearest kernel that
penalises one stage away is the exponent shift `γ^Δ` forward, `δ^|Δ|`
backward (Δ = ±1 → 0.25, ±2 → 0.0625 → 0 under the floor, ±3 → 0), all else
unchanged. On the failure set:

| | as declared | re-declared |
|---|--:|--:|
| cells changed | — | **132 of 210** (every Δ = ±1 and ±2 pair) |
| newly exact-zero cells | — | **44** (all 22 Δ = +2 and all 22 Δ = −2 pairs) |
| `initial-access → reconnaissance` (the regression bridge) | 0.9 | **0.225** |
| `reconnaissance → initial-access` (the pair S1 said must not be suppressed) | 0.4 | **0.1** |
| `initial-access → discovery` | 0.02 | 0.005 |
| `exfiltration → execution` | 0.0875 | **0** |

And on this corpus the Δ = ±2 edges are the *only* edges the distance term
currently moves mass on — 16 forward and 12 backward base edges across the
five nets ([`weight_sensitivity_study.md`](weight_sensitivity_study.md) §2
census) — so the re-declaration would hard-suppress 28 edges the corpus
actually carries, where `v3` hard-suppresses none (study §3b: "0 base edges
hard-suppressed"). The success set moves the same way (the kernel multiplies
both verdicts).

**Recommendation: keep the kernel as declared, and repair the sentence.**
Four reasons, in order of weight:

1. *It is what S1 asked for.* The supervisor's defect was that a
   lifecycle-length leap weighed the same as an adjacent step; the fix was to
   suppress far jumps while leaving `reconnaissance → initial-access`
   "untouched, as required" (study §2). Penalising adjacency reverses the
   half of the ruling that protected the adjacent step.
2. *Adjacency is the attested pattern.* The lifecycle models chain each
   phase to its successor; that is the one thing the literature does say
   about distance ([`lifecycle_consensus.md`](lifecycle_consensus.md) §6,
   "why this family"). A kernel that penalises the successor move penalises
   the attested transition and keeps the declared one.
3. *Direction at one stage already lives in the rule tier.* On failure the
   one-step fallback is 0.9 against a forward 0.35 — that is where "one away,
   lower" is actually encoded, by semantics rather than by distance (rules
   artefact, `kernel_symmetry_note`). The dictated sentence describes the
   *combined* matrix's behaviour at the same time as it misdescribes the
   kernel.
4. *Blast radius.* A re-declaration is a new registry version (`v4`, with
   `v3` frozen as every published figure is keyed on it), a fold-in
   recompile, a re-sweep (the 2 600-run S1 design, or its successor under
   the current timing regime — §6), and the Δ = ±2 hard-suppression above,
   which the stall check and the base-edge check would both need re-running.

The repaired sentence is Marc's to dictate; what it has to say is: *within a
stage or to the adjacent stage, the full value; two stages away, a quarter;
the maximum distance, zero.* Content points for it are in §5.

**Ruling:** *open — Marc's.* `[ ] keep as declared (recommended)  [ ] re-declare
(names the form; opens v4 + re-sweep)`. Record the ruling here and in the tex
comment when taken; if re-declared, this record's figure and tables regenerate
from the new version with one flag.

---

## 5. Chapter inputs

### 5.1 Content-point scaffold — the owed §4.2.4.2 failure-encoding paragraph

Marc dictates; no prose here. Each point names the document that grounds it.
The slot is the `[pending, your ask 2026-08-19]` comment after the overlay
paragraph in `subsubsec:mechanics-join`.

1. **Why a failure matrix has to be declared at all** — the corpus encodes
   success (survivorship), so the failure side is judgement by construction;
   this is the evidence-tier asymmetry, stated as a finding rather than an
   apology. (`success_failure_overlay_design.md` §4;
   `notes/ch4_methods/outcome_overlay_directionality.md`.) Already half-said
   in the paragraph above the slot ("failures are not encoded") — this point
   closes it rather than repeating it.
2. **The values are not 210 numbers; they are nine rules and three
   parameters.** The decomposition: first-matching semantics rule × lifecycle
   distance, multiplied, then multiplied onto the base proportion and
   renormalised (the composition rule is already in the paragraph above).
   Point at `fig:failure-weight-decomposition` and the appendix. (This record
   §1.)
3. **What the nine rules say, in one breath** — two foothold gates (no
   foothold, no post-intrusion move), two dampers (a full collapse to
   preparation is minor; re-running code on a held foothold is a retry, not
   a regress), and a ladder: fall back 0.9, sidestep 0.7, push on 0.35. One
   rationale each, kept once per rule. (Rules file; appendix
   `tab:overlay-failure-rules`.)
4. **What distance adds, correctly stated** — the four consensus phases are
   already in the paragraph; the kernel sentence needs the repair in §4:
   *same phase or adjacent, full; two away, a quarter; maximum distance,
   zero.* The recon → impact example already in the paragraph is the Δ = +3
   case and survives as is. (`lifecycle_consensus.md` §6; this record §4.)
5. **Declared, not fitted; swept, not produced** — the values were fixed
   before any net was walked and never tuned to make a profile traverse;
   the sweep (pointer to `sec:sensitivity`, V6) tests whether the
   conclusions move with them. The dictated "how did you come up with the
   values? we swept them" line must not land in that form (it inverts
   declare-then-sweep); this is where it goes instead, the right way round.
   (`declared_value_provenance.md` §1, §5; `weight_sensitivity_study.md` §8.)
6. **The honest ceiling, one clause** — magnitudes are a declared-plausibility
   envelope, CTI-unvalidated by construction; only within-source ratios are
   claimed, and the reasoning plus the scrutiny it survived is the defence.
   (`success_failure_overlay_design.md` §2.5 last caveat.)
7. **Hold for the sibling ruling:** if the failure-only overlay is adopted,
   point 1 simplifies to one declared object and the success half of the
   sentence above the slot is re-dictated; if not, nothing here changes.
   ([`success_null_overlay_feasibility.md`](success_null_overlay_feasibility.md)
   §8 — recommendation: keep `v3`, carry the study as the ablation.)

### 5.2 The appendix wiring — for Marc to verify, then paste

Not applied to `dissertation.tex` (Marc, 2026-08-19: "don't wire into my
thesis before I verify"). Compile-checked in a scratch copy: builds clean,
figure on its own float page, five tables, no overfull boxes. The skeleton
already routes "the ~200-value success/failure overlay matrix declaration" to
`app:sensitivity`; this block goes directly under its `\label`. The section
lead and the caption are session-drafted and owed Marc's voice pass; the
numbers in the caption are the tool's printed numbers.

```latex
% ---- the outcome-overlay weight sets (the appendix subsec:mechanics-join
%      points at: "the full set of tactic-to-tactic weight sets") -------
% GENERATED (2026-08-19): figure + tables by
% tools/failure_weight_decomposition_figure.py from
% data/ogasp/controller/outcome_rules.json + lifecycle_consensus.json through
% the tracked compiler (overlay version v3_persistent_backward). Regenerate,
% never hand-edit the PDF or tables/outcome_overlay_weights.tex; the numbers
% the caption quotes are printed by the tool --- re-check them if the rule
% set or the kernel is re-declared. Caption and section lead are
% SESSION-DRAFTED and owed Marc's voice pass. Record:
% docs/implementation/pipeline/ogasp/failure_weight_decomposition.md.
\section{The outcome-overlay weight sets}
\label{app:overlay-weights}

% [session-drafted lead, owed Marc's voice pass] The two tactic-to-tactic
% weight sets Section~\ref{subsubsec:mechanics-join} multiplies onto the
% token's out-transitions are not authored cell by cell. Each of the 210
% values (15 tactics by 14 destinations, no self-loops) is the product of
% two declared kernels: the value of the first-matching semantics rule
% (Tables~\ref{tab:overlay-failure-rules} and
% \ref{tab:overlay-success-rules}) and the lifecycle-distance factor over
% the four consensus stages (Table~\ref{tab:overlay-distance-kernel}).
% Figure~\ref{fig:failure-weight-decomposition} shows the failure set
% decomposed then aggregated; Tables~\ref{tab:overlay-failure-set} and
% \ref{tab:overlay-success-set} are the complete sets as committed.

\begin{figure}[p]
  \centering
  \includegraphics[width=\textwidth]{failure_weight_decomposition}
  \caption{How the failure tactic-to-tactic weight set is produced:
  decomposed, then aggregated. All three panels share one axis (rows are
  the source tactic $a$ whose action returned the failure verdict,
  columns the candidate next tactic $b$), grouped into the four
  consensus stages of the APT lifecycle (preparation, intrusion,
  post-intrusion operations, objective) with the ATT\&CK reading order
  inside a stage, and one grey scale from 0 to 1.
  (a)~The failure kernel: for each pair, the value of the first of the
  nine declared failure rules that matches it (key below the panels;
  Table~\ref{tab:overlay-failure-rules} gives each rule's rationale).
  The two foothold gates (A, C) fill the initial-access and
  reconnaissance rows, the pre-intrusion damper (D) fills the two
  preparation columns below the intrusion block, the execution damper
  (E) the execution column, and the backward\,/\,lateral\,/\,forward
  ladder (F, G, H\,/\,I) everything else --- eight distinct values
  across 210 pairs.
  (b)~The lifecycle-distance kernel $d(a,b)$, a pure function of how
  many consensus stages the transition crosses (the subscript is the
  signed offset $\Delta = s(b) - s(a)$): within a stage or to the
  adjacent stage $d = 1$; two stages away $d = \gamma = \delta = 0.25$;
  three stages away $0.0625$, which falls under the floor $z = 0.1$ and
  reads as exactly $0$. The kernel is block-structured, so the twelve
  corner cells are zero and the 44 cells two stages from the diagonal
  block carry 0.25; the remaining 154 are untouched.
  (c)~The failure weight set as committed: every cell is (a) multiplied
  by (b). Fourteen distinct values, twelve exact zeros (the preparation
  to objective and objective to preparation corners), and every
  non-zero cell traceable by eye to one rule letter and one distance
  factor. The values are declared and rule-generated; the sensitivity
  sweep defends where they sit, it did not produce them.}
  \label{fig:failure-weight-decomposition}
\end{figure}

\input{tables/outcome_overlay_weights}
```

And, at the `[pending …]` slot in `subsubsec:mechanics-join`, a one-line
pointer comment to §5.1 of this record is all the tex needs until Marc
dictates the paragraph.

---

## 6. The sensitivity study as ch5's backing — status, stated honestly

Marc's working assumption (2026-08-19): "I will back up with a sensitivity
study in ch5, I assume it has already run." It has, with two qualifications
the chapter must carry or the study must close before it is cited for `v3`:

- **It ran** — 2 600 runs over the declared bands of `γ`, `δ`, `z`, one-at-a-time
  then the influential corners, on both controller mappings, with the verdict
  recorded as mixed (C2/C4 held; C1 held on `v2_partial`, moved on
  `v1_ckc_total` for the intermediate profile; C3 moved for a power reason;
  `z` inert on this corpus). ([`weight_sensitivity_study.md`](weight_sensitivity_study.md) §5–§6.)
- **Qualification 1 — regime.** The 2 600 runs were executed under the
  *fixed-dwell* regime at commit `e84bd2a`; the S3-R stochastic-timing regime
  landed mid-study. The numbers are the right comparator for experiment 1's
  findings and not a prediction for the reported arms. (Study preamble.)
- **Qualification 2 — band.** `δ`'s band was re-cut to 0.1–0.5 with the
  persistence ruling; `δ = 0.1` is **unswept** and C1's verdict is
  *suspended* for the new band rather than resolved. The study's own
  recommendation is a wholesale re-sweep under the current regime.
  (Study §3b; `lifecycle_consensus.json` `band_note`.)

So: a sensitivity study exists and can be described in ch5 exactly as the
study record states it; what cannot yet be said is that `v3`'s declared point
was swept within its *current* band under the *reported* timing regime. That
is a re-run, not a re-argument — and it is the same re-run a kernel
re-declaration (§4) would force, which is one more reason to take the kernel
ruling before scheduling it. Flagged here; not actioned (out of this brief's
scope).

---

## 7. Where this connects, and when to update

- **Consumes:** [`success_failure_overlay_design.md`](success_failure_overlay_design.md)
  §2–§4 (the rules, their tiers, the asymmetry);
  [`lifecycle_consensus.md`](lifecycle_consensus.md) §4, §6 (stages, kernel);
  [`weight_sensitivity_study.md`](weight_sensitivity_study.md) §1–§3b, §8 (fold-in,
  census, persistence ruling, CTI-independence);
  [`../../declared_value_provenance.md`](../../declared_value_provenance.md) §1, §5;
  `data/ogasp/controller/{outcome_rules,lifecycle_consensus}.json` and
  `overlays/manifest.json`; `src/mtdsim/l3_simulation/controller/rules.py`.
- **Feeds:** `subsubsec:mechanics-join`'s owed failure-encoding paragraph
  (§5.1) and `app:sensitivity`'s weight-set section (§5.2); the sibling
  feasibility verdict ([`success_null_overlay_feasibility.md`](success_null_overlay_feasibility.md),
  which keeps the failure set whichever way it rules, and whose §5.8 rules
  the kernel-only alternative out on expressiveness).
- **Artefacts:** `tools/failure_weight_decomposition_figure.py`;
  `docs/thesis/figures/failure_weight_decomposition.{tex,pdf}`;
  `docs/thesis/tables/outcome_overlay_weights.tex`.
- **When to update:** if Marc rules on §4 (record it; regenerate if
  re-declared); if any failure rule value or kernel parameter is re-declared
  (regenerate, re-check the caption numbers); if the failure-only overlay is
  adopted (the success appendix table and the success rules table drop or
  re-caption; the failure decomposition stands); if a new registry version
  becomes the reported one (`--version`).
