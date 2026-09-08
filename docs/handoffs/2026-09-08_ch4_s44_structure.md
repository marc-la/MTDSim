---
status: open — structural critique; Marc's rulings owed before any tex change
created: 2026-09-08
topic: "§4.4 after the §4.3 formalism: the title does not say what the section does, the two subsections do not cut at a joint, the units have no internal shape, the floats' captions carry argument, and the prose has not adopted the symbols §4.3 declared. Critique and a proposed shape; no tex touched."
---

# §4.4 — what it is now that §4.3 is a formalism

## The ask (Marc, 2026-09-08)

§4.3 now defines the profile net $\mathcal{N}_c$ and its extension
$(\mathcal{N}_c, F)$. From here the chapter is "in the stage of formalism":
§4.4 has to be written *with* it, intentionally, not re-keyed at the margin.
Marc's own reading of §4.4: it is not a trace of the token; it is the set of
assumptions that join the formalism to MTDSim so that MTD evaluation can run.
Three of those assumptions are the ones ch5/ch6 sweep (the dwell means, the
tactic-to-verb mapping, the failure matrix); the rest are held fixed. His
critique, verbatim in substance: the title does not convey this; the two
subsections both read as "more assumptions"; the section reads as paragraphs
stacked with no rhyme or reason; Table 4.2 has two panels for no reason and
(a) plus the multiplier belong in the appendix; the captions do not just say
what is in the float. This file is the session's assessment. Nothing below
is applied.

## 1. What §4.4 is, stated in the formalism's terms

§4.3 leaves exactly four things undefined, and every one of them is a
symbol the notation table (`tab:gspn-notation`) already promises §4.4 will
declare:

| Left open by §4.3 | Symbol | What §4.4 owes | Which subsection today |
|---|---|---|---|
| the rate of every timed transition | $\mu_p$ (in $W_c(\tau_p) = 1/\mu_p$) | fifteen declared means and the distribution family of the draw | 4.4.1, block 1 |
| which action a tactic dispatches to earn a verdict | $\varphi : P \to A \cup \{\bot\}$ | the mapping, its constraints, dwell-only as $\bot$ | 4.4.1, block 2 |
| the failure factor | $F_{\text{failure}} = R \cdot d(\Delta)$ | the matrix, its two kernels, the declared magnitudes | 4.4.1, block 3 |
| how the simulator produces $v \in V$ | $\nu$ (no symbol yet) | the three ways to fail, none at $\bot$, pre-emption by a mutation | 4.4.2 |

Plus two policies that are neither values nor the verdict: the sink retrace
(a history-dependent restriction of the enabled set at $\hat p$, §4.3
handoff §4.5) and the confusion penalty (substrate-side, not a net element).
And the clock: $\tau_p$'s drawn firing time *is* the dispatched action's
duration (S3-R), and a mutation can pre-empt it.

That is the whole content of §4.4. The section currently carries all of it,
so nothing is missing; what is missing is the *organisation* that says so.

**Which are swept.** Of the four, $\varphi$ is swapped (v2_partial against
v1_ckc_total), $\mu_p$ is swept over anchor bands and its family checked
(Erlang-4 same mean), $F_{\text{failure}}$ is swept through $\gamma, \delta,
z$ (the rule kernel $R$ is argued, not swept, by rule). $\nu$, the retrace,
the penalty and the synthetic share $s$ are held fixed. The section should
say this once, at the end, and point at ch5 — not restate the sweep
discipline (skeleton comment: "sweep discipline points at sec:sensitivity
rather than restating it"; ch5/ch6 handoff: sweeps are *validity leaves*
declared in ch5, reported as the V6 preamble table in ch6).

## 2. The title

`L4: The attacker-agent traversal in MTDSim` names the *run* (the pipeline
figure's fifth rung). The section's content is the interface and the
declared values that make a run possible. Marc is right that it misleads:
an examiner opening it expects a walk of the token and finds a parameter
register.

Candidates, in the ruled heading form (sentence case; L-prefix kept; MTDSim
is a name):

1. **`L4: Joining the profile net to MTDSim`** — recommended. Names the
   act, covers both the interface and the values (you cannot join without
   valuing), reaches back to §4.3 by the object's name ("profile net"), and
   sits beside the sibling titles as a product-of-the-layer name.
2. `L4: Declared parameters and the join to MTDSim` — the 2026-08-18
   framing word for word. Honest but a list, and "parameters" repeats
   inside the section as a heading.
3. `L4: The profile net in MTDSim` — shortest; under-describes the
   declarations.

Whichever is chosen, the ch4 preamble's sentence "to an attacker-agent
traversal in MTDSim (L4)" in the `fig:pipeline` caption is unaffected: the
*rung* is still the traversal; the *section* is the join.

## 3. The subsection split — where the joint actually is

### 3.1 Why the current split reads as "two lots of assumptions"

4.4.1 "The controller layer" = the three declared inputs. 4.4.2 "Mechanics
and the join to MTDSim" = the runtime loop, the verdict rule, the retrace,
the penalty. Both headings name *architecture* (a layer; mechanics), neither
names what its unit contributes to the formalism, and the second unit's
opening paragraph restates Eq.~4.4 in prose — so a reader meets the
conditioning rule twice (§4.3 as a display, 4.4.2 as a paragraph) and the
verdict it depends on once, after the matrix that consumes it. That is the
"no rhyme or reason" feeling: the split is by *where the code lives*, not by
what the formalism needs.

### 3.2 The joint

The formalism draws one line through §4.4's content:

- **The interface** — the symbols the *simulator* owns and the net merely
  names: the action set $A$, the dispatch $\varphi$, the verdict $\nu$, the
  shared clock and pre-emption, the penalty, the retrace, termination.
  These are inherited or structural. $\varphi$ is the one choice in here,
  and it is *swapped*, not swept.
- **The declared values** — the symbols the *net* owns and the formalism
  left as free parameters: $\mu_p$ (and the exponential family) and
  $F_{\text{failure}}$ (and its two kernels). These are numbers we wrote
  down, and they are *swept over bands*.

The assumption register (§4.3 handoff §7.2) partitions the same way:
interface assumptions (A5 binary verdict, A6 dwell-only opacity, A10
retrace, A11 substrate invariants) against value assumptions (A1
exponential, A3/A4 survivorship and success pass-through, A8 consensus
staging). And ch5's story becomes one sentence: one interface swap, two
band sweeps.

### 3.3 Two shapes, one recommended

**Shape B — interface first, then values (recommended).**

```
4.4  L4: Joining the profile net to MTDSim
     preamble  — why a two-way join (the dead-end timeline; this is what
                 Eq. 4.4 conditions on v FOR); the three layers named
                 (movement / controller / action, fig:pipeline); the
                 contract: §4.3 left A, φ, ν, μ_p, F_failure open, this
                 section declares them
4.4.1 The interface: mapping and verdict
     A (the six verbs, ch2) → φ: constraints (≤ 1 verb, ⊥ = dwell-only),
     the figure + Table, alternatives tried (total mapping → App. B.7;
     Caldera, one sentence) → ν: the three ways to fail (precondition,
     mutation, the state-delta rows), none at ⊥ → the clock: τ_p's draw
     is the action's duration; a mutation pre-empts it and the penalty is
     the simulator's → the retrace as a restriction of the enabled set →
     the ceiling paragraph closes the unit (the interface is inherited;
     the model is as good as what it adopts) — the standing must-carry
4.4.2 The declared values: dwell means and the failure matrix
     μ_p: no value exists anywhere (the three citations) → derived from
     MTDSim's own costs, four anchors not fifteen → the table (per-tactic
     μ_p only) → exponential as tractability, mean is the claim → the
     caveat sentence (model parameter, not measurement)
     F_failure: the verdict is what the corpus cannot give (survivorship;
     w_c is a proportion of flows, not a probability of success) → R, the
     nine argued rules → d(Δ) over the four consensus stages, γ, δ, z →
     the figure → the not-reverse-engineered defence → the caveat sentence
     close  — which of these ch5 swaps or sweeps, and which are held
```

Costs, stated: Marc's "three big assumptions" straddle the two units
($\varphi$ in 4.4.1, $\mu_p$ and $F$ in 4.4.2); and §4.3's closing ceiling
paragraph currently lists "parameters ... and mechanics" in the other
order, so it takes a one-clause re-key (which it needs anyway — see §6).
Gains: every symbol is defined before it is used (ν before F_failure; A
before φ); the two units are different *kinds* of thing, so the headings
can say what they are; the ch5 sentence writes itself.

**Shape A — values first, then the join (conservative).** Keep the two
units as they stand, rename them "The declared parameters" ($\mu_p$,
$\varphi$, $F_{\text{failure}}$, in that order) and "The join to MTDSim"
($\nu$, clock, pre-emption, retrace, penalty), give the three declarations
the uniform shape of §4 below, and cut 4.4.2's restatement of Eq.~4.4.
Matches the 2026-08-18 framing one-to-one and keeps the three swept inputs
together. Cost: the failure matrix is declared before the reader has been
told how a verdict arises (§4.3's abstract $V$ covers it, thinly).

Either shape is two subsections, which is the 2026-08-18 ruling (exactly
two; a three-way split declined). The 2026-08-19 rename ("Parameterisation"
→ "The controller layer") was made when there was no formalism to
parameterise; now that $\mu_p$, $\varphi$ and $F$ are declared symbols,
"parameters" has a referent again, which is why both shapes drop "the
controller layer" from the heading and keep the controller as the
preamble's name for the layer that carries them.

## 4. The rhyme: one shape for every declaration

Whatever the split, the stacked-paragraphs feeling goes away only if the
three declarations share a visible shape. Proposed five beats, in order,
for $\mu_p$, $\varphi$ and $F_{\text{failure}}$ alike:

1. **What the symbol is in the net** (one clause: "$\mu_p$, the mean of
   $\tau_p$'s firing time in Eq.~4.1").
2. **Why no value exists to take** (the literature / CTI gap; "no real
   mapping here"; "the blind spot of the CTI").
3. **How it was declared** (derivation from MTDSim's costs; the
   constraints; the two kernels).
4. **The float**, with a decode-only caption, and a pointer to the
   appendix that carries the derivation.
5. **The caveat and the sweep pointer** (a model parameter anchored to
   this simulator, not a measurement; swept / swapped in ch5, or held).

Today's blocks against that shape:

| Beat | $\mu_p$ | $\varphi$ | $F_{\text{failure}}$ |
|---|---|---|---|
| 1 net symbol | absent | absent | absent |
| 2 no value | ✓ (3 cites) | ✓ ("no real mapping") | ✓ (survivorship) — but it sits in a stray paragraph keyed to "recurrence values" |
| 3 declaration | ✓ | ✓ + Caldera + total-mapping + the ceiling paragraph interleaved | ✓ but the "overfit" defence *precedes* the definition |
| 4 float | ✓ (two panels, argument in caption) | ✓ | ✓ |
| 5 caveat + sweep | flagged prose slot, unwritten | absent (the ceiling paragraph does the job, out of place) | flagged prose slot, unwritten; the "plausible, literature-bounded, sensitivity-swept" close covers all three at once |

Strays to relocate, not delete:

- **"The base transition weights are recurrence values ... survivorship
  bias"** — beat 2 of the failure-matrix block. Re-key: $w_c$ is a
  proportion of flows (Eq.~4.2), not a probability of success. The
  closed-world clause in it (A2) is about $w_c$, which §4.3 owns; candidate
  to move beside Eq.~4.2 (Marc's call; the §4.3 handoff §3 already says
  "stated once with $W$").
- **"One concern was trying to overfit ..."** — beat 5 of the failure
  matrix (the defence after the definition), or folded into the caveat.
- **"We tried other mappings ... Caldera"** — beat 3 of $\varphi$,
  compressed to two sentences; the total-mapping experiment already has
  App.~B.7.
- **"The ceiling of this thesis lies in the action layer"** — the close of
  the interface unit under Shape B (it is a statement about the inherited
  interface), or the close of the whole section under Shape A.
- **4.4.2's "This is verdict-conditioned re-weighting ... encodes
  direction"** — becomes one sentence pointing at Eq.~4.4; the display
  already says it. The one thing worth keeping from it is "this is what
  encodes direction", which is the *purpose* of $F_{\text{failure}}$ and
  belongs in that block's beat 2.
- **The preamble's dead-end-timeline argument** — stays as the section's
  opening, but it now has a named consequence: it is why Eq.~4.4
  conditions on $v$. One clause.

## 5. The floats

### 5.1 Table 4.2 (`tab:dwell-catalogue`)

Marc: panel (a) and the multiplier to the appendix; (b) is the focus. Agreed,
with one thing the chapter must not lose: the **four-anchors-not-fifteen**
argument is what makes the dwell sweep tractable (ch6 sweeps anchors, and
the low-and-slow anchor is the only one that moves an outcome, §4.3 handoff
§7.1). If (a) leaves, one prose sentence carries it: "the fifteen means
resolve to four declared anchors and a multiplier (Appendix~B.4); the
anchors are what Chapter~6 sweeps".

Proposed chapter table: `Tactic | μ_p (s) | Evidence`, one panel, the
evidence badge moved from the family to the tactic (it is what tells the
reader which rows are swept). Family and multiplier columns and panel (a)
go to `app:dwell-derivation`. This is a change to
`tools/dwell_catalogue_tables.py` (generated; never hand-edit), so it is a
tool edit plus a regenerate.

### 5.2 Captions

The rule already exists (`figure_table_conventions.md` §b2: the caption
decodes every encoding; a reader who sees only the float can read it) and
was applied to `fig:controller-mapping` and `fig:failure-weight-matrix` on
2026-09-05 (Marc: "the decode only"). The offenders are the ones that also
*argue*:

- **`tab:dwell-catalogue`** (~170 words): carries the 4-not-15 argument,
  the replaces-not-adds rule, the resource-development exception, the
  evidence decode and a pointer to the mapping figure. Keep: the column
  decode and the badge key and the version pin. Move to prose: 4-not-15
  (beat 3), replaces-not-adds (the clock, 4.4.1 under Shape B), the
  exception (beat 3).
- **`fig:gspn-gadget`** (§4.3, adjacent, flagged not actioned): the last
  sentence ("Under a success verdict the base weights stand; under failure
  the mass moves ... which is the foothold-gate rule ... acting on the
  net") is argument. It belongs in §4.3's prose beside Eq.~4.4, or in the
  failure-matrix block as the worked example.
- **`fig:failure-weight-matrix`** and **`fig:controller-mapping`**: within
  the rule.

Proposed caption rule for the chapter, in one line: *the caption names what
the float shows, the encodings, and the pin; every "because", "so" and
"which is" goes to the prose.*

## 6. Terminology: the §4.4 re-key list

Counts are non-comment lines of §4.4 as it stands (2026-09-08).

| §4.4 today (count) | Formalism term | Note |
|---|---|---|
| "the Petri net(s)" (9) | the profile net $\mathcal{N}_c$ | §4.3's name for the object; "Petri net" survives only as the genus |
| "dwell time(s)" (10), "the stochastic dwell times" | the drawn dwell = $\tau_p$'s firing time; the parameter = the mean dwell $\mu_p$ | the two are conflated throughout; the table head is "mean dwell" and the prose never says it |
| "tactic-to-verb mapping" | $\varphi$, the tactic-to-verb mapping | keep the prose name; introduce the symbol once with its type $P \to A \cup \{\bot\}$ (the notation table's [3b] says it has no symbol anywhere yet) |
| "verbs", "the action layer" (16, 9) | $A$, the action set; its six elements are the simulator's verbs | say once, then "verb" is fine |
| "dwell-only" (6) | $\varphi(p) = \bot$; verdict none; $F_{\text{none}}$ the identity | keep the word, bind it to the symbol once |
| "success or failure signal" (1), "success or failure" | the verdict $v \in V$ | "signal" → "verdict" |
| "failure matrix" (6), "failure weight matrix", "failure weight set", "15-by-14 tactic-to-tactic failure weight matrix", "the declared failure matrix", "overlay" | $F_{\text{failure}}$, the failure matrix | one prose name; the figure caption's "failure weight set" and the appendix's "overlay" are the same object |
| "failure rules A to I" | $R$, the rule kernel | |
| "distance", "four broad phases", "a quarter", "floor of 0.1" | $d(\Delta)$ over the stages $s(\cdot)$; $\gamma = \delta = 0.25$; $z = 0.1$ | the appendix already uses $\gamma, \delta, z$ |
| "base proportion(s)" (2), "base transition weights", "recurrence values" (2) | $w_c(p,q)$, the base weight | "recurrence" is the L1 count; the net weight is a proportion — the blur the §4.3 comment already flags |
| "re-weights", "re-weighting" (7) | the conditioning factor $F_v$; Eq.~4.4 | "conditioning" is the notation table's noun; "re-weight" can stay as the verb |
| "the token selects the next tactic" | $t_{pq}$ fires | |
| "sinks" (2) | a place with no out-transition (no $t_{pq}$ from $\hat p$) | §4.3 does not define "sink"; §4.4 must, once |
| "MTD interrupts the attacker" | a mutation pre-empts $\tau_p$; $v = $ failure | |
| "the movement layer supplies all the tactic timing" | $\tau_p$'s firing time is the duration of the dispatched action | S3-R in formalism words |

**One collision to rule on.** "Phase" is doing two jobs: the inherited
attacker's *six phases* (ch2, ch4 preamble, ch6) and the lifecycle
consensus's *four phases* (§4.4.1 prose: "four broad phases of an attack";
`fig:failure-weight-matrix` caption: "four lifecycle phases"). The §4.3
handoff, the appendix and one line of ch2 say *stages*. Recommendation:
**stage** for the lifecycle ($s(\cdot)$, $\Delta$), **phase** reserved for
the baseline attacker's six. Two prose edits and one caption.

**A symbol still missing.** The verdict function has none; the §4.3
handoff uses $\nu$. Whether §4.4 needs it or "the verdict the simulator
returns" carries it in prose is Marc's call; the notation table would gain
one row either way ($v \in V$ is "Declared in §4.4.2" there, so the
declaration has to land somewhere).

## 7. Adjacent flags — §4.3, not actioned

- The ceiling paragraph closing §4.3 lists "parameters ($\mu_p$; the
  exponential) and mechanics ($F_v$; sink retrace)". After the formalism,
  $F_{\text{failure}}$ is a declared *value* and the mechanic is Eq.~4.4,
  which §4.3 now owns. Re-key: "parameters ($\mu_p$, $\varphi$,
  $F_{\text{failure}}$) and the join ($v$, the clock, the retrace)". Its
  order should match whichever shape §4.4 takes.
- `fig:gspn-gadget` caption, last sentence (§5.2 above).
- The closed-world clause (A2), candidate move beside Eq.~4.2 (§4 above).

## 8. Rulings owed

- R1 the title (§2; recommended 1).
- R2 the shape (§3.3; recommended B).
- R3 the five-beat shape for each declaration (§4) — yes / no.
- R4 Table 4.2: one panel, per-tactic $\mu_p$ with the evidence badge;
  (a) and the multiplier to the appendix (§5.1).
- R5 the caption rule (§5.2) and its application to `tab:dwell-catalogue`
  and, adjacently, `fig:gspn-gadget`.
- R6 stage / phase (§6).
- R7 $\nu$ as a symbol, or prose (§6).

## What happens next, on the rulings

A pass-5-style restructure of §4.4: Marc's sentences reassigned to the
beats, the strays moved, the re-key applied clause by clause, the two
caveat slots left as Marc's prose slots, the table tool edited and
regenerated, build clean. No new argument is drafted; every sentence in
the result is one already in the tex or a one-clause symbol binding.

## Reading list

- `docs/thesis/dissertation.tex` §4.3 (`sec:petri-formalism`) — the
  symbols and the notation table §4.4 is bound to.
- `docs/thesis/dissertation.tex` §4.4 (`sec:execution`) — the text this
  critiques, with its skeleton comments (the 2026-08-18/19 rulings).
- `docs/handoffs/2026-09-08_ch4_s43_gspn_formalism.md` §4.2–4.5, §7 —
  the interface elements, the parameter and assumption registers.
- `docs/handoffs/2026-09-08_ch5_ch6_structure.md` — where the sweeps are
  declared and reported; §4.4 points, it does not restate.
- `docs/workflows/figure_table_conventions.md` §b — the caption rule.
- `tools/dwell_catalogue_tables.py` — the generator Table 4.2 comes from.

## Out of scope

Drafting prose; touching §4.3 beyond the flags in §7; the appendix
tables; ch5's sensitivity section.

## 9. Pass 5 merge outcome and the front-loading ruling (2026-09-08, later)

Two streams ran (white box with session context; black box cold), ledgers in
the session scratchpad `p5/WB_ledger.md`, `p5/BB_ledger.md`, merged in
`p5/MERGED_ledger.md`. Convergent block, ruled ACCEPTED by Marc: the title
(§2 candidate 1); join material before the declared values; "The controller
layer" retired as a heading; the spine sentence bound to $\mu_p$, $\varphi$,
$F_{\text{failure}}$; the shared cuts (the loop paragraph, the Eq.~4.4
restatement, the mutation example, the flourishes); twelve symbol bindings.
Rejected at merge and confirmed: the black box's re-opening of the
2026-08-20 rulings (constraint sentence, worked examples, three-citation
sentence) and its kernel/floor "tension" (verified false: the floor is what
zeroes the $\Delta = 3$ cell). The $\varphi$-placement divergence is moot
under the ruling below.

**Marc's ruling — front-load, point forward.** §4.4 states what the model
runs with; the *why this shape* and *what bounds* detail belongs to the
appendix and the sensitivity analysis, which §4.4 forward-references. So:
the dwell table shows the committed means only (badges, families,
multipliers to the appendix); the failure-matrix block drops the kernel
detail (values, floor, example) and the defence sentences, keeping the two
kernels named, the figure, and the close; each declared input ends on a
pointer to its appendix section and the sweep.

**Structure, recommended to Marc (ruling owed):** preamble (two-way join,
the layers, the contract) + four units — 4.4.1 The runtime mechanics
(verdict, clock, retrace, penalty, ceiling); 4.4.2 The dwell times; 4.4.3
The tactic-to-verb mapping; 4.4.4 The failure matrix. ≈ 990 words; one unit
of overdraft on the writing-guide ledger beyond the two units plus slack.
Funded fallback: mechanics folded into the preamble, three headings. One
prose slot for Marc: the sentence that says the three declared inputs are
what Chapter 5 sweeps (no sentence of his says it yet).
