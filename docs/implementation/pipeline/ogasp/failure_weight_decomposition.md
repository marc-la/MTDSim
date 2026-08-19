---
status: durable
created: 2026-08-19
updated: 2026-08-19
topic: "L3/L4 — the failure tactic-to-tactic weight set presented as a decomposition: (declared failure kernel) × (lifecycle-distance kernel) → the committed matrix; three figures with three homes (ch4 matrix / appendix decomposition + declared-point-in-bands); the two-pair walkthrough; where every number lives; the kernel-discrepancy ruling (resolved: keep as declared)"
---

# The failure weight set, decomposed then aggregated — provenance on the page

**Status:** durable. Executes the presentation half of the 2026-08-19 provenance
brief (`handoffs/2026-08-19_failure_weight_provenance.md`, retired in the
commit that shipped this): the failure tactic-to-tactic weight set was already
rule-generated and reproducible
([`success_failure_overlay_design.md`](success_failure_overlay_design.md) §2–§3,
[`weight_sensitivity_study.md`](weight_sensitivity_study.md) §1), but nothing on
the page *showed* that — a reader of `failure.json` saw 210 numbers. Marc's
framing (2026-08-19): the values "are somewhat random, but they need to be in a
defensible manner", so present the matrix as **failure kernel × distance kernel
→ aggregated matrix**, decomposed then aggregated, "so it is very clear how they
got their results".

**Marc's split (2026-08-19, scrutinised and adopted as variant B).** The
chapter gets *the matrix*; the sensitivity study gets *the decomposition and
how the declared point was landed on*. Three figures, three homes (§3). The
one guard the split needs — stated here because the split invites the
opposite reading — is that **the nine rule values were never swept**: the
sensitivity study covers only the three kernel parameters, and the rules are
defended by argument and adversarial review, not by a sweep. Every number
therefore has a home that says which kind of number it is (§5.3).

**Nothing about the values changed.** No rule value, no kernel parameter, no
registry version. `python -m mtdsim.l3_simulation.controller.rules --check`
still reproduces every committed view (0 of 420 differing cells per version).
The generator below *reads* the compiler's own per-cell output
(`rule`, `d`, `delta`, `v`) and the tracked net loader's base edges, and draws
them; it derives nothing of its own.

**Reproduce**

```
PYTHONPATH=src python tools/failure_weight_decomposition_figure.py \
    [--layout all|matrix|decomposition|bands] [--version v3_persistent_backward] \
    [--verdict failure|success] [--walk a->b ...] [--dry-run-adjacent] \
    [--no-compile] [--no-tables]
```

writes `docs/thesis/figures/{failure_weight_matrix, failure_weight_decomposition,
distance_kernel_bands}.{tex,pdf}` (TikZ at 12 pt; `--verdict success` gives
`success_weight_matrix`, also committed, for the case the pair is kept), and
`docs/thesis/tables/outcome_overlay_weights.tex` (the appendix tables: both rule
ledgers, the kernel parameters, the complete success and failure sets for the
version). Every number quoted below is printed on a run. The failure
decomposition is invariant to the failure-only ruling
([`success_null_overlay_feasibility.md`](success_null_overlay_feasibility.md)
§8, recommendation keep `v3`): if `v4` were adopted the success matrix becomes
a constant and drops out of ch4; the failure figures stand as they are.

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
dampers, then the relationship ladder. Key letters are the figures'.

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
are reproduced in the appendix table; the adversarial-scrutiny history (R0–R4,
~90 agents, certified 82 %) is the ledger
([`../../declared_value_provenance.md`](../../declared_value_provenance.md) §6.1).
**These nine values are not a sweep dimension and never were** — the
declared-value precedent's rule is argument for single magnitudes, sweep for
parameterised terms (ledger §4, last paragraph).

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

The floor acts on the **distance factor at fold-in** (`d < z` reads as 0
*before* composition), never on a finished, renormalised edge weight — the
fact the fresh-pass `[WRONG — M3]` flag in the tex asks the sentence to carry;
the bands figure (§3) draws exactly this. The kernel is block-structured, so
the distance term touches exactly 56 of the 210 pairs and leaves 154 alone.
**These three parameters are the sweep set** (`γ` 0.1–0.5, `δ` 0.1–0.5, `z`
{0, 0.05, 0.1}; `lifecycle_consensus.json`).

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
*pattern* attested. The sweep is what defends where the kernel magnitudes sit
(§6); it did not produce them, and it does not reach the rules.

---

## 2. Two pairs walked end to end

Printed by `--walk`; the figures' cells carry the same three numbers.

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
per-pair edit (and, on this corpus, an edge no profile net carries — §3,
bands figure).

---

## 3. The three figures and their homes

| figure | file | home | what it shows | what it must *not* be read as |
|---|---|---|---|---|
| **the matrix** | `failure_weight_matrix` (and `success_weight_matrix` if the pair is kept) | **ch4 §4.2.4.2**, at the overlay paragraph | the committed set alone: every cell its value **and the letter of the rule that produced it**, stage-grouped axis, one grey scale; the nine-line key (letter, rule id, declared value) in-figure | a typed table — the letters are there precisely so it reads as generated; rationale and tier are not here (they are in the appendix ledger table) |
| **the decomposition** | `failure_weight_decomposition` | **appendix `app:sensitivity`** (Marc's "sweep pointer ruled to appendix", `bdf3de7`), opening the overlay's sensitivity entry | (a) failure kernel, (b) distance kernel with Δ as subscript, (c) = (a) × (b) — three aligned 15 × 14 panels, one 0–1 scale, every cell printed | the sweep's output — it is **the declared point**: (b) is what the sweep's three parameters move, (a) is what the sweep holds fixed |
| **the declared point in its bands** | `distance_kernel_bands` | **appendix `app:sensitivity`**, beside the decomposition | d(Δ) at the declared `γ = δ = 0.25` (accent) and at the band edges 0.1 / 0.5 (greys); the floor strip {0, 0.05, 0.1} with `d < z → 0`; under the axis: declared pairs per Δ (6/22/44/66/44/22/6) and **base edges with mass per Δ on the five current routing nets** (0/12/66/146/84/15/0 of 323) | a results figure — it shows *where the point sits and what the corpus can exercise*; the sweep's *results* panel is owed to the v3 re-sweep (§6) |

The bands figure carries the two facts the sweep narrative turns on, both
read fresh from the artefacts on every run rather than quoted from the study:
**no profile net carries a three-stage transition in either direction**, so
`z` is inert by corpus structure (the study's §6.1 finding, re-confirmed on
the post-rebuild nets), and the only Δ classes the kernel moves mass on are
±2 (15 forward, 12 backward base edges).

**Conventions, all three.** Consensus stage, then the ATT&CK reading order
within a stage — the order `fig:l1-graph` uses, with one move:
`command-and-control` sits in the post-intrusion block, where the consensus
seats it. TikZ standalone at the document's 12 pt base, greys carry the value
on one ramp, the single accent marks the declared point, document font; the
same conventions as `tools/l1_attack_graph_figure.py`. Sizes: matrix
≈ 470 × 215 pt (a normal float), decomposition ≈ 464 × 535 pt (a float page),
bands ≈ 353 × 155 pt. All three, plus the five appendix tables, compile with
no overfull boxes in a scratch copy of the thesis (2026-08-19). No number is
hard-coded; if a rule value or parameter is re-declared, one run regenerates
everything and re-prints the caption numbers.

---

## 4. The kernel discrepancy — **resolved: keep as declared** (Marc, 2026-08-19)

**What it was.** Marc's dictated §4.2.4.2 narrative had "one away, a lower
value"; the declared kernel penalises nothing at one stage (`d = 1` for
Δ = ±1, 0.25 at ±2, 0 at ±3). The brief asked for one question with a
recommendation; the recommendation was keep-as-declared, on four grounds (S1
protected the adjacent step; adjacency is the attested pattern; direction at
one stage already lives in the rule tier, 0.9 vs 0.35; blast radius).

**How it resolved.** Marc's L4 flag walk (`bdf3de7`, "kernel narrative fixed
to record values") rewrote the sentence to the declared kernel — *"a
transition within the same phase, or one phase away, is not penalised; two
phases away keeps a quarter of its weight; and the maximum distance is
weighted zero"* — which is the keep-as-declared ruling taken on the page. No
version, no re-sweep. The `[WRONG]` that remains on that paragraph is the
separate **M3 floor-semantics** fact (the floor zeroes the *distance factor*,
not a renormalised edge), which §1(b) states and the bands figure draws.

**The costed alternative, kept for the record** (`--dry-run-adjacent`, the
exponent shift `γ^Δ` / `δ^|Δ|`): 132 of 210 failure cells move, 44 go to exact
zero (every Δ = ±2 pair), the regression bridge 0.9 → 0.225,
`reconnaissance → initial-access` 0.4 → 0.1, `exfiltration → execution` → 0, and
all 27 Δ = ±2 base edges the corpus carries are hard-suppressed where `v3`
hard-suppresses none. The sibling feasibility study reached the same place
from the other side: its "adjacent form" of a kernel-only overlay **stalls a
profile** ([`success_null_overlay_feasibility.md`](success_null_overlay_feasibility.md)
§5.8). If the asymmetric-decay idea (separate `γ` ≠ `δ`) is ever taken up,
the sentence changes and this figure set regenerates from the new version.

---

## 5. Chapter inputs

### 5.1 Content-point scaffold — the owed §4.2.4.2 failure-encoding paragraph

Marc dictates; no prose here. Points 1 and 5–7 are shared with, and should be
read together with, the fresh-pass `[INSERT — M2]` points already at the slot
and the feasibility study's §9; they are not repeated where those own them.

1. **Why a failure matrix is declared at all** — the corpus encodes success
   (survivorship); failure is judgement by construction; the tier asymmetry is
   a finding, not an apology. (Design record §4; the paragraph above the slot
   already says "failures are not encoded" — close it, do not repeat it.)
2. **The values are nine rules and three parameters, not 210 numbers** —
   first-matching semantics rule × lifecycle distance, multiplied, then onto
   the base proportion and renormalised (the composition sentence is already
   above the slot). Point at the ch4 matrix figure: *every cell carries the
   letter of the rule that produced it*. (§1; `fig:failure-weight-matrix`.)
3. **What the nine rules say, in one breath** — two foothold gates (no
   foothold, no post-intrusion move), two dampers (a full collapse to
   preparation is minor; re-running code on a held foothold is a retry, not a
   regress), and a ladder: fall back 0.9, sidestep 0.7, push on 0.35. One
   rationale each, kept once per rule, in the appendix ledger.
   (`tab:overlay-failure-rules`.)
4. **The floor, correctly** — it zeroes the *distance factor* below 0.1 at
   fold-in; it is not a threshold on the finished edge weight (M3). The
   two-phase quarter and the far-jump zero are the only things distance does.
   (§1(b); `lifecycle_consensus.md` §6.)
5. **Declared, not fitted; swept, not produced** — values fixed before any net
   was walked, never tuned for traversal (the anti-fitting boundary + the
   adversarial-review defence, as the M2 insert has them); the sweep in the
   appendix tests whether *conclusions* move with the three kernel parameters
   — and, said plainly, **the rules are not swept; they are argued.**
   (`declared_value_provenance.md` §1, §4–§5; `weight_sensitivity_study.md` §8.)
6. **The honest ceiling, one clause** — a declared-plausibility envelope,
   CTI-unvalidated by construction; within-source ratios are what is claimed.
   (Design record §2.5.)
7. **The success half** — on the feasibility verdict's premise: the base
   carries the corpus's success routing, the failure matrix what the corpus
   cannot record, the success table a declared sharpening priced by ablation
   (one to three hosts, profile-signed, no headline moved). (Feasibility
   study §9 — sequence the dictation after Marc's §8 ruling.)

### 5.2 Wiring blocks — for Marc to verify, then paste (NOT applied to the tex)

Compile-checked together in a scratch copy (clean; no overfull boxes). Captions
and the appendix lead are session-drafted and owed the voice pass; caption
numbers are the tool's printed numbers.

**(i) ch4 §4.2.4.2 — after the overlay paragraph, at the `[figure slot ---
four-phase overlay]` comment.** One figure if `v4` is adopted; add the second
`\includegraphics` (or a sibling figure) for `success_weight_matrix` if the
pair stays (the recommendation).

```latex
% FIGURE (2026-08-19): the committed failure weight set, every cell with the
% letter of the declared rule that produced it --- generated by
% tools/failure_weight_decomposition_figure.py --layout matrix from the
% outcome rules + lifecycle consensus through the tracked compiler (overlay
% version v3_persistent_backward). Regenerate, never hand-edit. Caption is
% SESSION-DRAFTED and owed Marc's voice pass. Decomposition + the declared
% point in its sweep bands live in app:sensitivity; the rule ledger (rationale,
% tier) is tab:overlay-failure-rules there.
\begin{figure}[tbp]
  \centering
  \includegraphics[width=\textwidth]{failure_weight_matrix}
  \caption{The failure tactic-to-tactic weight set (\texttt{v3\_persistent\_backward}).
  Rows are the source tactic $a$ whose action returned the failure verdict,
  columns the candidate next tactic $b$, grouped into the four consensus
  phases of the APT lifecycle (preparation, intrusion, post-intrusion
  operations, objective) with the ATT\&CK reading order inside a phase; one
  grey scale from 0 to 1. Each cell is the value the token's base
  out-transition is multiplied by on a failure verdict, and the letter is the
  declared rule that produced it (key below the matrix; each rule's rationale
  and evidence tier are in Table~\ref{tab:overlay-failure-rules}): two
  foothold gates (A, C) fill the initial-access and reconnaissance rows, a
  pre-intrusion damper (D) the two preparation columns below the intrusion
  block, an execution damper (E) the execution column, and the
  backward\,/\,lateral\,/\,forward ladder (F, G, H\,/\,I) everything else.
  The rule's value is then multiplied by the lifecycle-distance factor
  (unchanged within a phase or one phase away, a quarter two phases away,
  zero at the maximum distance), which is why the far corners are zero and
  the two-phase bands carry a quarter of their rule's value; the
  decomposition is Figure~\ref{fig:failure-weight-decomposition}. The set is
  declared and rule-generated; none of its values was produced by, or tuned
  on, a simulation run.}
  \label{fig:failure-weight-matrix}
\end{figure}
```

**(ii) appendix `app:sensitivity` — the overlay's entry: the decomposition, the
declared point in its bands, the tables.** Directly under `\label{app:sensitivity}`.

```latex
% ---- the outcome overlay: the declared point, decomposed, and its sweep ----
% GENERATED (2026-08-19): three figures + the tables by
% tools/failure_weight_decomposition_figure.py from
% data/ogasp/controller/outcome_rules.json + lifecycle_consensus.json through
% the tracked compiler and the routing-net loader (overlay version
% v3_persistent_backward). Regenerate, never hand-edit; re-check the caption
% numbers if a rule or parameter is re-declared. Lead + captions are
% SESSION-DRAFTED and owed Marc's voice pass. Record:
% docs/implementation/pipeline/ogasp/failure_weight_decomposition.md.
% The sweep RESULTS paragraph/figure is owed to the v3 re-sweep under the
% current timing regime (record section 6) --- the 2026-07-28 study is
% fixed-dwell and delta = 0.1 is unswept; describe it as recorded until then.
\section{The outcome-overlay weight sets and their sensitivity}
\label{app:overlay-weights}

% [session-drafted lead, owed Marc's voice pass] The failure weight set of
% Section~\ref{subsubsec:mechanics-join} (Figure~\ref{fig:failure-weight-matrix})
% is the product of two declared kernels: the value of the first-matching
% semantics rule (Table~\ref{tab:overlay-failure-rules}; the success rules in
% Table~\ref{tab:overlay-success-rules}) and a lifecycle-distance factor over
% the four consensus stages (Table~\ref{tab:overlay-distance-kernel}).
% Figure~\ref{fig:failure-weight-decomposition} shows the set decomposed then
% aggregated. The nine rule values are declared and defended by argument and
% adversarial review; they are not swept. The three kernel parameters are the
% swept set: Figure~\ref{fig:distance-kernel-bands} shows the declared point
% inside its declared bands, and which stage offsets this corpus can exercise.
% Tables~\ref{tab:overlay-failure-set} and \ref{tab:overlay-success-set} are
% the complete sets as committed.

\begin{figure}[p]
  \centering
  \includegraphics[width=\textwidth]{failure_weight_decomposition}
  \caption{The failure weight set decomposed, then aggregated --- the declared
  point the sensitivity sweep is taken around. All three panels share one
  axis (rows the source tactic $a$ on a failure verdict, columns the candidate
  next tactic $b$), grouped into the four consensus stages with the ATT\&CK
  reading order inside a stage, and one grey scale from 0 to 1.
  (a)~The failure kernel: for each pair, the value of the first of the nine
  declared failure rules that matches it (key below the panels;
  Table~\ref{tab:overlay-failure-rules}) --- eight distinct values across 210
  pairs. These values are not a sweep dimension.
  (b)~The lifecycle-distance kernel $d(a,b)$, a pure function of how many
  consensus stages the transition crosses (the subscript is the signed offset
  $\Delta = s(b) - s(a)$): within a stage or to the adjacent stage $d = 1$;
  two stages away $d = \gamma = \delta = 0.25$; three stages away $0.0625$,
  which falls under the floor $z = 0.1$ and reads as exactly $0$ --- the
  floor acts on this factor, not on a finished edge weight. The kernel is
  block-structured: the twelve corner cells are zero, the 44 cells two
  stages from the diagonal block carry 0.25, and the remaining 154 are
  untouched. $\gamma$, $\delta$ and $z$ are the swept parameters.
  (c)~The committed set: every cell is (a) multiplied by (b) --- fourteen
  distinct values, twelve exact zeros, every non-zero cell traceable by eye
  to one rule letter and one distance factor.}
  \label{fig:failure-weight-decomposition}
\end{figure}

\begin{figure}[tbp]
  \centering
  \includegraphics[width=0.82\textwidth]{distance_kernel_bands}
  \caption{The declared distance-kernel point inside its declared sweep bands.
  The distance factor $d$ against the signed stage offset $\Delta$ at the
  declared parameters ($\gamma = \delta = 0.25$, the tinted curve) and at the
  band edges ($0.1$ and $0.5$, grey); the shaded strip is the floor's swept
  set $\{0, 0.05, 0.1\}$, with the declared $z = 0.1$ dashed --- a factor
  below it reads as exactly zero, which is what zeroes the three-stage
  corners. Beneath the axis: how many of the 210 declared pairs sit at each
  offset, how many base edges with mass the five routing nets carry at each
  offset (323 in all), and $d$ at the declared point. No net carries a
  three-stage transition in either direction, so the floor has nothing to act
  on in this corpus and its sensitivity is zero by structure rather than by
  measurement; the offsets the kernel actually moves mass on are $\pm 2$ (15
  forward and 12 backward edges). The point was declared from the lifecycle
  consensus and the persistence ruling before any run; the sweep defends it,
  it did not choose it.}
  \label{fig:distance-kernel-bands}
\end{figure}

\input{tables/outcome_overlay_weights}
```

**(iii) ch5 `sec:sensitivity` — the V6 parameter table.** No figure; one row
per swept family. The overlay's row: *lifecycle-distance kernel — `γ`, `δ`
(0.1–0.5), `z` ({0, 0.05, 0.1}) — declared `0.25 / 0.25 / 0.1` — effects:
`δ` largest (fallback distance), `γ` second, `z` inert by corpus structure —
appendix §\ref{app:overlay-weights}.* The nine rule values do **not** get a
row; their provenance row is the ledger table in the appendix.

### 5.3 Where every number lives

Marc's concern (2026-08-19): the A–I categorisation and its values "come from
somewhere, and will live somewhere in the dissertation" — they must not be
mistaken for outputs of a sensitivity study. The homes:

| number | kind | produced by | lives at |
|---|---|---|---|
| the nine failure rule values (A–I) and the five success rule values | **declared** magnitudes | R2 authoring + four adversarial rounds, finalised 2026-07-23 (ledger) | the rule ledger tables in the appendix (`tab:overlay-failure-rules`, `tab:overlay-success-rules`: key, id, value, tier, rationale); letters in the ch4 matrix cells; rationale narrative in ch4 (point 3 of §5.1) |
| the rule *order* (first match wins) and the firing sets | declared structure | the rules file | the ch4 matrix (which letter where); design record §2.3 |
| `γ`, `δ`, `z` and their bands | **declared parameters (the swept set)** | the lifecycle consensus + the persistence ruling (2026-07-27/28) | `tab:overlay-distance-kernel` (appendix); the bands figure; the V6 row in ch5 §5.1 |
| the four stages and the per-tactic seats | sourced / rule-resolved / declared, per tactic | the lifecycle consensus overlay | ch4 overlay paragraph (already); `tab:overlay-distance-kernel` |
| the 210 compiled cells per verdict | **derived** (rule × d) | the tracked compiler | the ch4 matrix; the appendix set tables; the decomposition figure |
| pairs per Δ (6/22/44/66/44/22/6) | derived from the stages | the compiler | the bands figure |
| base edges per Δ (0/12/66/146/84/15/0 of 323) | **corpus** (L2 nets, current) | the routing-net loader | the bands figure; the inert-`z` sentence |
| the sweep's results (C1–C4; influence ranking) | **measured** | `weight_sensitivity_study.md` (fixed-dwell; to be re-run) | appendix, the sweep paragraph/figure — owed (§6) |

---

## 6. The sensitivity study as the appendix's backing — status, stated honestly

Marc's working assumption (2026-08-19): "I will back up with a sensitivity
study, I assume it has already run." It has, with two qualifications the
appendix must carry or the study must close before it is cited for `v3`:

- **It ran** — 2 600 runs over the declared bands of `γ`, `δ`, `z`, one-at-a-time
  then the influential corners, on both controller mappings, with the verdict
  recorded as mixed (C2/C4 held; C1 held on `v2_partial`, moved on
  `v1_ckc_total` for the intermediate profile; C3 moved for a power reason;
  `z` inert on this corpus). ([`weight_sensitivity_study.md`](weight_sensitivity_study.md) §5–§6.)
- **Qualification 1 — regime.** The runs were executed under the
  *fixed-dwell* regime at commit `e84bd2a`; S3-R landed mid-study. They are
  the right comparator for experiment 1's findings and not a prediction for
  the reported arms.
- **Qualification 2 — band.** `δ`'s band was re-cut to 0.1–0.5 with the
  persistence ruling; `δ = 0.1` is **unswept** and C1's verdict is suspended
  for the new band. The study's own recommendation is a wholesale re-sweep
  under the current regime. (Study §3b; `lifecycle_consensus.json` `band_note`.)

So: the appendix can describe the study exactly as recorded, and the bands
figure already shows the declared point and the bands; what cannot yet be
said is that `v3`'s point was swept within its *current* band under the
*reported* timing regime. That is a re-run, not a re-argument. With the kernel
ruling now closed (§4) nothing else gates it. Flagged here; not actioned
(out of this brief's scope).

---

## 7. Where this connects, and when to update

- **Consumes:** [`success_failure_overlay_design.md`](success_failure_overlay_design.md)
  §2–§4; [`lifecycle_consensus.md`](lifecycle_consensus.md) §4, §6;
  [`weight_sensitivity_study.md`](weight_sensitivity_study.md) §1–§3b, §6, §8;
  [`../../declared_value_provenance.md`](../../declared_value_provenance.md) §1, §4–§5;
  [`success_null_overlay_feasibility.md`](success_null_overlay_feasibility.md) §8–§9;
  `data/ogasp/controller/{outcome_rules,lifecycle_consensus}.json`,
  `overlays/manifest.json`, `data/ogasp/petri/*_structural.json` +
  `synthetic_overlay.json`; `src/mtdsim/l3_simulation/controller/rules.py`,
  `movement/net.py`.
- **Feeds:** ch4 §4.2.4.2 (the matrix figure; the owed failure paragraph,
  §5.1); `app:sensitivity` (decomposition, bands, tables, §5.2); ch5 §5.1's
  V6 table row.
- **Artefacts:** `tools/failure_weight_decomposition_figure.py`;
  `docs/thesis/figures/{failure_weight_matrix, success_weight_matrix,
  failure_weight_decomposition, distance_kernel_bands}.{tex,pdf}`;
  `docs/thesis/tables/outcome_overlay_weights.tex`.
- **When to update:** if any rule value or kernel parameter is re-declared
  (regenerate; re-check captions); if the failure-only overlay is adopted as
  `v4` (drop `success_weight_matrix` from ch4; the success tables re-caption;
  `--version v4_…`); if the asymmetric-decay idea lands (the bands figure
  gains a second curve family; the ch4 sentence changes); when the v3
  re-sweep runs (the appendix gains its results figure beside the bands).
