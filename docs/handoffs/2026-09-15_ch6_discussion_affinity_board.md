---
status: open — design; macrostructure RULED 2026-09-28 (§10: Discussion → Conclusion with future work; supersedes §2 and §3); ch6/ch7 microstructure proposed (§11), Marc's rulings owed on its four open items (§11.6) and the disposition of every board item marked FOUNDATION (§6). Feeds ch6 drafting; nothing here is prose.
created: 2026-09-15
updated: 2026-09-28
topic: "The discussion chapter's affinity board: every discussion-shaped idea on disk (six inventories over the notes, the criterion, the L3 investigation records, the ch5 design pass, the ratified ch1/ch3/ch4 prose, the lineage extractions and the field's discussion-section conventions), affinity-grouped into themes, stated as mini-hypotheses, forward-joined to the ch5 measurement that earns each one, and flagged where the foundation may move. Marc's three reads of §6.1–§6.3 tested against the record. Session-proposed compositions kept apart from the inventory."
---

# Ch6 discussion — the affinity board

**Goal.** Give the discussion chapter a complete, evidence-joined inventory of
what it may say, so that its nine units are assembled from a census of the
record rather than from whatever a drafting session happens to remember — and
so that every discussion point is soft-joined to a ch5 measurement in advance
without the join being fitted to a wanted outcome.

**How to read it.** §1 answers Marc's question (are the three reads right).
§2–§3 are the structural and heading consequences. §4 is the board proper:
themes, each a cluster of numbered mini-hypotheses (MH) with the claim in one
line, the evidence status the record itself assigns, the ch5 float or label
that feeds it, and the note or record that carries it. §5 is the forward-join
map in both directions (discussion points with no measurement; measurements
with no consumer). §6 is the foundation-risk register — the items whose
evidence has moved under them since their note was written. §7 is the short
list of session-proposed compositions, kept apart so Marc can judge them
without their being mistaken for the record. §8 is housekeeping the sweep
surfaced. Locators are repo paths; `sec:` / `subsec:` / `tab:` / `fig:` names
are the live labels in `docs/thesis/dissertation.tex`.

**Provenance.** Six read-only inventory passes on 2026-09-14: (i) the 33
notes under `docs/notes/` plus the READMEs and writing guide; (ii)
`apt_model_criterion.md` in full, `architecture.md`, `fidelity_implications.md`,
`hypothesis_tree.md`; (iii) all 80 records under
`docs/implementation/pipeline/ogasp/`; (iv) the Evaluation chapter's tex
(L4895–6535) and the 2026-09-09 experiments-design handoff; (v) the ratified
ch1/ch3/ch4 prose and comments; (vi) the lineage and yardstick extractions, the
25 evaluation anatomies, the research-record threads, and the two conventions
files. Nothing in §4 is invented; where an idea is a composition of on-disk
material it sits in §7 and says so.

---

## 1. Marc's three reads, tested

The ratified spine matrix (`docs/notes/_writing_guide.md`) assigns the
discussion column as: **capture → what the capture licenses; model → fidelity
verdict; evaluate → what changes for MTD evaluation.** All three reads are
right in substance. Two need a correction of emphasis and one a correction of
placement.

**§6.1 = discussion.capture — right, with one nuance.** The matrix cell is
"what the capture *licenses*", which is two things at once: the behaviours the
CTI capture put into the model that prior attackers lack (the positive half —
the S6 answer in `apt_model_criterion.md` §(g) para 1: campaign structure,
objective conditioning, branching plurality reaching the defence dimension,
the minimal adaptive loop; plus the stealth-shaped spacing and the directedness
the records added since) **and** the ceiling the capture imposes on what those
behaviours may be called (Row A: "CTI-grounded structure with declared, tiered,
swept magnitudes" — the binary sentence "a CTI-derived attacker model" is
unavailable in either direction; envelope not actor; the observability
boundary). The post-intrusion blind spot is the *framing* of this section, and
the record carries it in two halves that have never been composed: the field's
attacker holds no post-foothold campaign (ch3 §3.3.5, verbatim at L3601–3607),
and the CTI corpus is thin pre-intrusion (ch4 L3996–4005; reconnaissance in
10 of 38 flows) — see §7 N1. Note the current tex comment under `sec:captured`
puts the *scoring discipline and the structural limitations* there, which is
§6.2's job by the fidelity-verdict comment two lines later; the two comment
blocks drifted apart across the 2026-09-04/09-07 passes.

**§6.2 = discussion.model, the fidelity verdict — right, and it must be
formalised before ch5 is drafted.** The instrument is the eight properties
read against evidence, and the record already supplies the discipline (badges;
axes fixed before scoring; scores move on evidence only; census not scale;
measured negative distinguished from absence). What ch5 must supply is one
measurement per property, and the current wiring points properties 6 and 7 at
a retired label (`subsec:aio-capabilities`, removed with the ablation
subsection on `be53d621`) — so as things stand two of the seven ticks in
`tab:fidelity-verdict` have no ch5 antecedent and no ch4 antecedent either
(the tex flags both). The per-property join is §4 theme B and §5.

**§6.3 = discussion.evaluate — right on the matrix; wrong as a lineage
comparison, and not future work.** Three things on disk settle this:

- The record distinguishes three comparisons and places only one in the
  discussion (`2026-09-08_ch5_ch6_structure.md`): *cross-arm* (H2 — ch5 states
  the grade, ch6 says what a threat-model-dependent evaluation means);
  *cross-mechanism* (H1, ch5); *cross-lineage* (E5 / L-H2-prior — a **ch5**
  table, `subsec:eff-lineage` / `tab:eff-lineage`, "inside the strand they
  instrument rather than in a section of their own"). The lineage comparison
  reaches §6.3 as one interpretive point — "the lineage's internal
  disagreement is the phenomenon, not something to reconcile" — and reaches
  §6.2 as the three prior-work rows of the fidelity table. It is not the
  section.
- The origin of the lineage-in-discussion reading is Marc's own prompt #86
  (2026-08-11, "lineage headlines become discussion comparison points"); the
  later rulings moved the numbers to ch5 and left the interpretation in ch6.
  The reading has a paper trail; the record has since refined it.
- Future work is ch7, its own three units, on the "earned by measurement" rule
  (`ch8_future_work/README.md`). §6.3 hands ch7 its exclusions by pointer; it
  does not carry them. What makes §6.3 *read* like future work is its
  verb-shaped heading ("What changes…"), not its content — the content on disk
  is the evaluation-method findings (theme D below), which are the cheapest
  and most transferable results the project owns.

**The one gap the reads do not name.** The discussion chapter's charter
(`ch7_discussion/README.md`) has *two* movements — impact, and *limitations
owned in one place* — and the tex has no unit for the second. Four notes are
written for it (corpus thinness, operator concentration, declared parameters,
the detection-regime boundary) and have nowhere to land. §2 recommends a unit.

---

## 2. Section shape — recommendation

Nine units. The current tex has three sections with no subsection structure.
Recommended split, each unit named by its matrix cell:

| Unit | Section | Job | Board themes |
|---|---|---|---|
| 1–2 | 6.1 capture | the behaviours captured, against the post-intrusion blind spot; what the capture licenses (Row A ceiling, envelope not actor) | A, B(positive half) |
| 3 | 6.2 model | the scoring discipline (badges; fixed before scoring; census not scale; negative ≠ absence) | C1–C3 |
| 4–5 | 6.2 model | the walk: properties 2, 3 (shown to change an outcome); properties 1, 4, 6, 7 (built, operate, no advantage); 5, 8 blank by ruling | C4–C14 |
| 6 | 6.2 model | limitations owned in one place | C9 |
| 7–9 | 6.3 evaluate | the threat-model dependence and its mechanism; the operating-point / instrument / tempo findings; the lineage read | D, E |

Unit 6 is the one the charter owes and the tex lacks; it is funded from the
nine, not added. If Marc keeps three sections, the limitations unit closes 6.2.

Corpus precedent for the shape: Tay's three-chapter split (numbers → a
Discussion that mirrors the results subsection-for-subsection → Future work) is
"the ruled shape of this dissertation's ch5/ch6/ch7"
(`evaluation_conventions.md` §h). Brown's §V is the exact model for a
discussion that opens on attacker realism and closes on what the evaluation
needs (§V.A "Attacker capabilities and realism" … §V.D "Need for multiple MTD
techniques").

---

## 3. Headings — audit and shortlist

Marc's own rules (memory, 2026-08-09 / 2026-09-04): sentence case; no acronyms
except the ratified visible ones (APT, MTD); headings are *labels*, the claim
goes in the first sentence; "movement attacker" lives in prose, never in a
heading; keep APT visible; no repeated rhetorical scaffold across siblings. The
corpus (25 anatomies) uses plain topic nouns for discussion sections — Brown's
"Attacker capabilities and realism", "Attacker limitations"; Hong's "Comparing
MTD techniques", "MTD techniques and threats"; Zhang's "Adversary profile";
Masud's "Comparison with the present study" — and **no paper uses an
interrogative or descriptive-clause heading**.

Against that, the three current headings fail as follows:

| Current | Fault |
|---|---|
| What the movement attacker has captured | a clause, not a label; "movement attacker" in a heading (2026-09-04 reversal); a claim ("has captured") |
| Fidelity verdict | passes as a label; "verdict" reads as a claim word, tolerable |
| What changes for MTD evaluation | a clause; verb-shaped, which is why it reads as future work |

Shortlist (one per section; Marc chooses; the claim moves to each section's
first sentence):

- **6.1** *Captured APT behaviour* — or *APT behaviour captured*. Keeps APT;
  label form; the post-intrusion framing is the first sentence.
- **6.2** *Attacker model fidelity* — or keep *Fidelity verdict*. "APT attacker
  model fidelity" echoes ch4's title as signage if the echo is wanted.
- **6.3** *Implications for MTD evaluation* — the corpus's own word for the
  section that says what an evaluation should now do differently (Cho §XI
  "insights and lessons learned"; Jalowski §5 guidelines).
- **Limitations** — corpus-attested as its own heading (Alavizadeh, Kim, He),
  if unit 6 gets a heading.

Trap check: no title case; no triplet or antithesis tail; four different
grammatical shapes across the siblings, so no scaffold repeats.

---

## 4. The board

Format per item: **MH-x.y** claim (one line, as the record states it) ·
*status* as the record assigns it · **feed**: the ch5 label / float that earns
it, or UNFED · **carried by**: the note or record · flags.

Status vocabulary is the record's: DEMONSTRATED / measured-positive /
measured-negative / DESIGNED / NOT ADDRESSED / ruled / declared / concession /
conjecture. FOUNDATION marks an item whose evidence has moved since its note
(register in §6).

### Theme A — The post-intrusion blind spot (6.1 framing)

- **MH-A.1** The evaluations of Table 3.3 leave MTD's performance against an
  attacker *with a foothold* unmeasured: without properties 1, 2 and 4 "an
  attacker with no multi-stage knowledge to lose cannot register the value MTD
  claims" · ratified ch3 prose (L3601–3607) · **feed**: none needed (it is the
  gap statement the chapter closes) · carried by ch3 §3.3.5,
  `post_ingress_mtd_gap.md`.
- **MH-A.2** Capability and credential state survives a network mutation;
  network-position state is invalidated by it — so surface-shifting MTD
  structurally under-defends the post-ingress phase "as a consequence of what
  the mechanism is *good at*" · argued, three review passes converged ·
  **feed**: `subsec:aio-disruption` (blocked fraction by layer),
  `subsec:eff-cross-arm` · carried by `post_ingress_mtd_gap.md`, tactic
  profile 11 §3 (the scan-hop vs credential-hop showcase).
- **MH-A.3** Automation changes MTD's responsiveness, not its phase reach: "a
  field that automates incomplete coverage is faster at the same thing" ·
  argued · **feed**: none (literature claim) · carried by
  `post_ingress_mtd_gap.md`; the note's own Position says "the discussion
  should close on the mechanism".
- **MH-A.4** The inherited attacker carries exactly two pieces of state a
  defence can reach; the movement attacker "is the first attacker on this
  simulator that has a campaign to be set back in", so it is the first against
  which MTD's stated mechanism is expressible at all · DESIGNED (the regression
  is a declared policy, not an emergent consequence — the strength and the
  limitation are the same fact) · **feed**: `subsec:aio-disruption` ·
  carried by `state_bounds_measurable_disruption.md`.
- **MH-A.5** The simulator's objective is a non-APT objective (mass compromise
  of 40 hosts): the APT-shaped attacker reaches it 0 times in 400 runs with no
  defence, and "cannot satisfy it however it is tuned"; nine post-ingress
  tactics have no verb to map onto, so the objective band is dwell-only ·
  measured / design-fact · **feed**: `subsec:aio-unopposed` "how runs ended"
  column, `tab:factors-varied` objective row · carried by `hypothesis_tree.md`
  §8b, `action_layer_anatomy.md` §5.2, `controller_mapping_v2.md` §2 — **no
  note**.
- **MH-A.6** The corpus is bounded by defender observability *by construction*
  (analysts draw up to detection; recon in 10/38 flows; 88 % of technique
  edges single-observation) — "the right bound for the object being modelled"
  · design-fact · **feed**: none (construction) · carried by
  `technique_graph_construction.md`, `objective_partition_findings.md` F3/F4.
- **MH-A.7** Weakest-link symmetry: ch3 names the attacker the weakest link of
  MTD evaluation; the action layer is the weakest link of this model ("can
  only be as good as what we adopt", ch4 L4648) — the ch3 comment asks the ch6
  sentence to point back · declared · **feed**: ch4 §4.4.1 ceiling sentence ·
  carried by ch3 comment L3573–3577.

### Theme B — What the model captures (6.1 positive half)

- **MH-B.1** Objective conditioning reaches runtime behaviour: every pair of
  profiles diverges at execution by 40–110× the seed-noise ceiling, the
  divergence is MTD-invariant, and it concentrates in the objective band with
  the lifecycle's invariant prefix contributing least — "profiles agree on how
  campaigns start and diverge on what they are for" (Alshamrani's shape,
  echoed at execution) · DEMONSTRATED · **feed**: `fig:aio-divergence` ·
  carried by `profile_divergence_findings.md` §3–§6 (no note carries the
  runtime echo) · **FOUNDATION**: attribution to objective vs corpus size is
  open (19/8/6/5 flows; the size-matched label-blind arm has never run); the
  L2 size-matched null failed (p = 0.49 / 0.71) so the discrimination claim
  is L3-scoped by Marc's 2026-08-17 ruling.
- **MH-B.2** Objective conditioning reaches the defence dimension: which
  mechanism suppresses best differs by profile in four of five cells at the
  operating interval · measured-positive (pre-restoration) · **feed**:
  `subsec:eff-under-defence`, `fig:eff-suppression-profiles` · carried by
  `experiment_02_findings.md` §12 — **no note** · **FOUNDATION**: the E3(b)
  statistic cannot fail on noise (`demonstration_arms_cross_examination.md`
  §3); the crossover form is the statistic a claim needs.
- **MH-B.3** Strategic plurality is variety, not strategy: 2–10 distinct
  five-tactic openings and 1.45–2.71 bits per profile against a baseline that
  is a structural zero; "the mechanisms *spend* the variety rather than
  steering it" · DEMONSTRATED with the honest limit riding · **feed**:
  `fig:aio-coverage` panel (b) (distinct openings; the entropy fan is killed
  as a hub-occupancy chart) · carried by `plurality_reporting.md` §2, §5, §6
  (§6 is written as a discussion subsection) — **no note**.
- **MH-B.4** The inherited attacker is a deterministic policy (one effective
  behaviour, by theorem over its transition table); the movement attacker runs
  2.7–5.9 effective next-moves per decision — "the cleanest cross-arm
  statement the project owns", and the one instrument hand-validated (V1) ·
  measured-positive · **feed**: `subsec:aio-unopposed` — **"nowhere in this
  chapter" as scaffolded** · carried by `predictability.md` — **no note**;
  the word "predictability" is retired (V2), say "a deterministic policy
  against a stochastic one".
- **MH-B.5** The corpus-weighted policy tracks the field-success prior and is
  substrate-success *anti*-aligned — "a corpus-derived stationary policy, not a
  substrate-gaming one" · measured-positive (reader study) · **feed**: UNFED ·
  carried by `plural_preference.md` — **no note**.
- **MH-B.6** Four of five profiles space substrate-visible actions 1.5–1.8×
  further apart and run 45 % quieter; the whole margin is the dwell-only
  tactics, a class of behaviour the baseline cannot represent (it "has no
  pauses at all"); the fifth profile inverts, "which is the mechanism working"
  · measured-positive, **fenced**: the badge stays NOT ADDRESSED because there
  is no detector for spacing to matter against — "the fence is on the badge,
  not on the measurement" · **feed**: a `tab:unopposed-summary` column, "not
  added", awaiting ruling C11 · carried by `stealth_spacing_diagnostic.md` —
  **no note** · caveats travel: cross-clock; contrast largely pre-decay; the
  earlier "loud baseline" premise was an accounting artefact (per-vulnerability
  rows inflate the baseline count 3.75×).
- **MH-B.7** Given navigation, the movement attacker reaches a located target
  with less than half the collateral the inherited attacker needs (footprint
  5.8 vs 13.1, CIs disjoint) — directedness is a captured behaviour; but the
  four objective-conditioned profiles fail the reachability gate at every
  depth, so "the movement attacker models APT tactical *behaviour* without APT
  *target-seeking*" · measured-positive + measured-negative · **feed**:
  `tab:factors-varied` objective row (E7 awaits ruling) · carried by
  `targeted_attacker_findings.md` §4, `targeted_objective_probe.md` §5–§7 —
  **no note**.
- **MH-B.8** The persistence structure runs end to end and outcome does not
  follow: effort does not convert to breadth; per-foothold retention 0.0–1.6 %
  against the defences that contest position; duration is granted by the
  episode structure for both arms · DESIGNED, defended as "duration
  unmeasurable by design, pursuit measured and negative" · **feed**:
  `fig:aio-coverage` (a), `tab:unopposed-summary` · carried by
  `persistence_duration_premise.md` (ratified 2026-08-09).
- **MH-B.9** The adaptive loop operates — the verdict splits the composition
  into two distinct static mixtures, CI-separated in four of five profiles —
  and confers no advantage against a verdict-blind control; the model
  "*responds distinctly* to defender resistance and the framework *measures*
  whether that response confers advantage — statements the baseline attacker
  cannot make" · DESIGNED (measured negative, matched control) · **feed**:
  `subsec:aio-disruption`, `fig:aio-adaptivity` · carried by criterion axis 4
  disposition 2026-08-11, `predictability.md` §4 · **FOUNDATION**: the
  verdict-blind arm is between-arm, not matched; the placebo-timestamp null
  (C26) is owed, and the contrast regenerated on the rebuilt nets differs in
  shape from experiment 2 §11.
- **MH-B.10** Direction is a property of how the attacker responds to its
  world, not an imposed stage machine: the corpus is the success policy; the
  failure overlay is "the one layer no corpus could supply" (survivorship) ·
  declared, red-team challenged · **feed**: `sec:sensitivity` γ/δ rows ·
  carried by `outcome_overlay_directionality.md`.
- **MH-B.11** Envelope, not actor: a token walking the union of 5–19 flows
  "can stitch one campaign's technique onto another campaign's next step and
  produce a chain no real actor ever ran" — the strength and the limitation
  are the same fact · ceiling · **feed**: none · carried by
  `structure_to_behaviour_binding.md`; **the phrase does not appear in ch4
  prose** (cut as repo vocabulary) — if 6.1 uses it, 6.1 introduces it.
- **MH-B.12** Cho's asymmetry — defender learning everywhere, attacker learning
  nowhere — "is no longer simply reproduced here" · interpretive · **feed**:
  none needed · carried by criterion §(g).
- **MH-B.13** The objective is a host-selection property, not a
  tactic-ordering one: Brown's FSM conflates the two; the movement layer freed
  the operational axis and dropped the strategic one; restoring only the
  strategic axis leaves the model "strictly more expressive than the baseline
  — not a retreat toward it" · design-fact · **feed**: `tab:factors-fixed`
  fresh-host contract row · carried by `movement_objectives_design.md` §1–§8 —
  **no note**.

### Theme C — The fidelity verdict (6.2)

C1–C3 are the discipline; C4–C14 the walk; C9 the limitations unit.

- **MH-C.1** The eight properties were fixed from the literature before the
  model was scored; scores move on evidence only ("never change the model,
  weights, mapping, or metrics to improve a row") · method · carried by
  criterion §(a), §(h).
- **MH-C.2** The rows are a census, not a scale: every declared dial (utility
  λ, learner κ, alignment α, succession α) narrows plurality from its own null
  at steep dose-response, so raising axis 6 or 7 lowers axis 3; the one
  measured exception (benefit-through-the-net) is deleted code · measured ·
  carried by criterion §(b), `plurality_reporting.md` §3,
  `modulator_composition.md` §4.
- **MH-C.3** A measured negative is not an absence: axis 1 records an absence;
  axes 4, 6, 7 record built, swept, ablatable mechanisms shown to operate
  without advantage — "a stronger statement about the field's gap than silence
  was, and one only a model carrying the capability can make"; the badge
  vocabulary flattens the two and a fifth badge is reserved to Marc · ruled ·
  carried by criterion §(b), §(c); `model_scope_freeze.md` §2 ("every DESIGNED
  row carries a *measured negative* rather than an absence").
- **MH-C.4** Property 2 is the one property shown to change an outcome; the
  walk's whole job is to separate it from the five ticks that are "built and
  operate without advantage on this terrain" (Marc's 2026-09-07 charitable
  ruling; the caption decode differs from Table 3.3's and must say so) ·
  ruled · **feed**: per property, §5.
- **MH-C.5** Axis 6 is closed at DESIGNED because "the attacker has something
  to be rational *about* but nothing to be rational *toward*" — no payoff is
  reachable or bankable; the cost/benefit rule was built twice, the tax is
  levied in near-proportion to dwell (~9 % surcharge, ratio-invariant), and the
  iterated model's criterion was passed by a negative control · ruled
  2026-08-02 · **feed**: UNFED (the §5.3.3 that carried the disengagement
  frontier is removed; ruling C31 drops 6 and 7 to "implemented, not
  evidenced") · carried by `incentive_rationality.md` §6,
  `iterated_cost_model.md` §4–§5, `model_scope_freeze.md` §2 · the ch4 prose
  carries no incentive rule (tex FLAG).
- **MH-C.6** Axis 7 carries three measured negatives: the routing learner is
  "correct and that is the problem" (the verdict is not a progress signal;
  exploitation 13 % → 1 % of successes); the readiness key repairs the collapse
  and never exceeds not-learning (4.52 vs 4.60); the compound-exploit learner
  operates and moves nothing because breadth is host-gated · DESIGNED ·
  **feed**: UNFED (same as C.5) · carried by `learning_without_context.md`,
  `learning_readiness_findings.md`, `exploit_learning_yield_findings.md` ·
  **FOUNDATION**: the exploit-learning null rests on a perfect-exploit ceiling
  that D-19 (`d127f443`) has since dropped; a cheap pre-check is named.
- **MH-C.7** Forgetting *helps*: a learner that never forgets "becomes
  confidently committed to a policy the defence has already invalidated" (ρ = 0
  CI-worse than 0.5 under MTD) — which qualifies the on-record sentence "MTD is
  severely effective against the learner"; a second record argues that
  perishability was declared, not measured · measured; two readings on disk ·
  **feed**: UNFED · carried by `progress_credit_findings.md` U5,
  `learning_mechanism_feasibility.md` §3.1 — **no note; the two readings are
  reconciled nowhere**.
- **MH-C.8** Axis 4's three routes to advantage are closed on evidence:
  reactive (every defence clocked and attacker-blind), mechanism-shape (a
  richer function of one bit), structural (zero post-interrupt-rewarded
  tactics in 138 census-passing instances, ≈3.5 expected from noise; the
  post-interrupt window is "distinguishable but punitive") · measured-negative
  · **feed**: `subsec:aio-disruption` · carried by `axis4_structural_probe.md`
  §9–§14, criterion axis 4 amendments 2026-08-11/13; `successor_programme.md`
  carries the reactive route only.
- **MH-C.9 (limitations owned in one place)** — the eleven the record names,
  each with its home note: proof-of-concept boundary (ch4 L3881); the
  tactic-to-verb mapping as a chosen input with no interval — "the standing
  bound on every claim the chapter makes"; the comparability boundary,
  three-valued (cross-paper invalid; cross-arm counts/fractions/per-host ratios
  only, never time; within-arm all) plus D-35 (exploitation uninterruptible in
  the movement arm — the diversity family loses 89–97 % of its exploit-blocking
  windows there; "our design choice, not a bug"); corpus thinness (88 %
  single-observation; `technique_graph_construction.md`); operator
  concentration (8 clusters / 42 %; Conti 3 of 7 double-extortion;
  `operator_concentration.md`); declared parameters ("exposed to one declared
  input", the low-and-slow anchor; one-at-a-time only, no global claim;
  `evaluation_burden.md`); the detection-regime boundary (no detector; one
  clause in `structure_to_behaviour_binding.md`, **no note**); taxonomy
  snapshot (v19.1 pinned; `cti_corpus_as_snapshot.md`); the frozen,
  attacker-blind defender; the exponential's mode-at-zero "quietly working in
  the attacker's favour" (`exponential_as_tractability_choice.md`); Sargent's
  ceiling as the discipline's own prescription (bib entry needs activating).
- **MH-C.10** Row A: structure corpus-grounded in full; of 38 ledgered
  magnitudes six externally fixed, twenty-three declared judgement; the
  benefit/utility family survived no adversarial round · scored by
  aggregation · carried by criterion §(d2).
- **MH-C.11** Row B: RECOMMENDATION grade "at the operating interval,
  directionally at ten seeds" · **FOUNDATION — the grade is currently
  unproven**: the inversion does not reproduce on the restored substrate
  (§6 item 1); the criterion has not been re-scored though its §(h) trigger
  has fired.
- **MH-C.12** Placement: "the first model in this cross-section's frame to
  reach the procedural rung, carrying two of the three behavioural-rung
  components plus a learning mechanism … found not to confer adversarial
  advantage — and not a behavioural model"; the behavioural rung needs the
  credit signal alone · placed · carried by criterion §(e).
- **MH-C.13** Axis 5's fence and axis 8's closure are ruled, not defaulted:
  no detection model to be stealthy against (S2 rules out an evasion action);
  the three Jalowski primitives need an inference capability the timeframe
  cannot support; the §4.3 metric-manipulation route was attempted and closed
  (clocked triggering; the one metric-reading defence converges to
  constant-action policies); the timing half inverted on verification — the
  200 s trigger is a quasi-periodic clock with ~0.25 % jitter, so "inferring a
  quasi-periodic schedule needs no ML" and the honest closure is a bounded
  value (8.0–17.7 % of the clock) — and "the substrate is time-based MTD,
  therefore metric manipulation is impossible" is an **overclaim the chapter
  must not write** · ruled · carried by criterion axis 5, axis 8 amendments.
- **MH-C.14** The four progression measures that fed axis 1 failed silently
  (depth saturated from above; accepted-depth from below; retention's sign
  backwards; reward is not progress) and "the near-miss is more instructive
  than the verdict" · measured · carried by `instruments_fail_silently.md`,
  criterion §(f2) · **FOUNDATION**: a fifth failed since (the alignment
  degeneracy guard, `fsm_alignment_prereg.md` §4), which is the note's own
  revisit condition.

### Theme D — What changes for MTD evaluation (6.3)

- **MH-D.1** An MTD evaluation's recommendation is a function of its threat
  model: substituting the attacker changes which mechanism the evaluation
  recommends, and the mechanism is structural — position-driven vs
  exploit-driven, "each attacker best countered by the defence that attacks
  its dependency" · **FOUNDATION — hypothesis, not fact** (§6 item 1; "no
  sentence may state the inversion as a fact of the current substrate") ·
  **feed**: `subsec:eff-cross-arm`, `fig:eff-cross-arm`, `tab:eff-orderings`
  · carried by `defence_ranking_inversion.md` (stale),
  `state_bounds_measurable_disruption.md`, `hypothesis_tree.md` §8d.
  What *is* robust: the movement attacker's severance ≫ surface re-roll
  pattern survives the loop fix and the restoration (both columns agree to a
  tie); what moved is the inherited attacker's response (`fsm_token_hold_findings.md` H0).
- **MH-D.2** State what state the attacker had: a "defence disrupted the
  attacker by X" is uninterpretable without it; and the taxonomy the
  literature reads by (SDR) is not the taxonomy the attacker feels — shuffle
  spreads across both layers while diversity sits in one, so the 2 × 2
  severance / surface re-roll contrast is the reportable object, never a total
  order · declared / measured · **feed**: `subsec:aio-disruption` spanning
  pair, `tab:eff-orderings` · carried by
  `state_bounds_measurable_disruption.md`; the taxonomy point is tex comment
  only (L6047–6053) — **no note**.
- **MH-D.3** An evaluation must show its operating point can discriminate its
  metric before reporting it: at the inherited interval neither attacker
  completes the objective, success-rate metrics are pinned at zero, and "a
  floor is silent"; the degeneracy is metric-specific · measured design-fact ·
  **feed**: `sec:dimensions` (one sentence) · carried by
  `operating_point_discrimination.md` — "the cheapest and most transferable
  methodological finding the project owns".
- **MH-D.4** Change the attacker's shape and the instruments fail silently —
  re-validate every measure as if new; "of the progression measures this
  evaluation inherited or first built, *none* survived contact with the new
  attacker unmodified" · measured · **feed**: UNFED — ch5 must say which
  instruments were re-validated and how (one clause in `sec:dimensions`) ·
  carried by `instruments_fail_silently.md` · FOUNDATION as C.14.
- **MH-D.5** MTD buys at tempo: the 200 s point is an extreme-disruption point
  (35–70 % of the run with a layer under reconfiguration), relaxing the
  interval buys the defender out of disruption and suppression together, and
  whether MTD involves a trade-off at all depends on the attacker — a
  singleton Pareto set ("a free lunch") against the inherited attacker, six
  of seven conditions efficient against the profiled one · measured-positive ·
  **feed**: `sec:efficiency`, `fig:eff-frontier` · carried by
  `mtd_disruption_frontier.md` §6–§8; `emulation_rung.md` ("an evaluation
  that cannot see cost would have recommended the free lunch") — **no
  discussion note**.
- **MH-D.6** The simultaneous scheme ranks dose, not strategy (≈150 realised
  interrupts per run against 75); horizon and defence dose are confounded ("a
  4× longer run is also 4× more defence") · measured / declared · **feed**:
  `tab:factors-varied` (ruling C34 owed) · carried by
  `experiment_02_findings.md` §10, design handoff §14.4, §15.3 — **no note**.
- **MH-D.7** Aggregate metrics hide a 13-fold variation in per-tactic effect
  (suppression 0.08× on initial access to ≈1.0× on lateral movement): "a
  defence that looks moderately effective in aggregate may be *useless*
  against the tactic an actual campaign depends on" — and this needs no new
  mechanism, only a tactic-resolved measurement · measured-positive · **feed**:
  UNFED after the restructure (the tactic-resolved instrument has no float;
  Zaffarano's argmax-over-phases is the antecedent to cite) · carried by
  `fidelity_implications.md` F1 — **no note**.
- **MH-D.8** MTD reaches execution, not planning: pre-objective failures move
  1.00–1.12× under MTD while total failures rise 2.6× — "it disrupts whether
  actions succeed, never which actions are chosen" (the pyramid-of-pain
  observation of `architecture.md` §(j), confirmed) · measured-negative ·
  **feed**: UNFED · carried by `fidelity_implications.md` F3 — **no note**.
- **MH-D.9** Cost-denominated MTD metrics overstate against a rational
  attacker: the tax is real and a cost-rational attacker is "behaviourally
  indifferent to it"; "MTD raises attacker cost by X %" reports something that
  changes no modelled decision · measured · **feed**: `sec:efficiency`
  ledger · carried by `fidelity_implications.md` F2, `incentive_rationality.md`
  §6.3 — **no note**.
- **MH-D.10** Fidelity and adversary strength are not the same axis; the
  profiled attacker is not competing with the baseline — "its lower compromise
  counts are not its verdict; they are the condition under which its
  distinctive behaviours are observed"; the framing pre-dates the results
  (thread `comparability_and_census.md`) · ruled (Marc 2026-09-09: "ours is
  the new baseline") · **feed**: `subsec:eff-cross-arm`,
  `subsec:aio-unopposed` · carried by `refusing_the_baseline_race.md`,
  `fidelity_implications.md` F5.
- **MH-D.11** The success criterion is degenerate and fidelity supplies a
  better one ("the token visited its objective place while holding a live
  foothold" discriminates where NCR cannot) — bounded since by the
  reachability gate: located reach holds at layer 1 on the aggregate envelope
  only · measured (7 seeds) then bounded · **feed**: `tab:factors-varied`
  objective row · carried by `fidelity_implications.md` F4,
  `targeted_attacker_findings.md` §4 — **no note**.
- **MH-D.12** Two design warnings for whoever builds the learning,
  cost-sensitive attacker the literature asks for: representation and reward
  are independent requirements ("a study scoring attacker learning on the
  attacker's own friction would conclude the representation makes no
  difference, which is the reverse of what it does"); and "an evaluation that
  rewards an attacker for permitted or enabled actions, by any mechanism, will
  measure the attacker optimising into the state where the most actions are
  permitted" — the credit-signal finding reappearing in the alignment factor,
  a mechanism with no learning in it · measured · **feed**: UNFED (points at
  retired labels) · carried by `learning_without_context.md`,
  `fsm_alignment_prereg.md` §3, §5 (the alignment half is in **no note**) ·
  FOUNDATION as C.6.
- **MH-D.13** Procedural mismatch manufactures attacker failure an evaluation
  will misread as attacker weakness; the decomposition into refused / failed /
  succeeded is one "no conventional security metric performs" · measured ·
  **feed**: φ row of `tab:parameter-register`, App. B.7 · carried by
  `procedural_mismatch_artefact.md` · **FOUNDATION — revisit condition engaged
  and unapplied**: the alignment sweep found at most ~7.4 % of the breadth
  disadvantage removable by a declared bias ("substantial part" weakens to
  "minor part" by the note's own rule); aligning to the FSM's succession
  *widens* the gap and strengthens the inversion; 44 % of CTI out-sets contain
  nothing the FSM would run next — "the CTI structure and the FSM's chain are
  not two orderings of the same verbs; they mostly do not overlap"
  (`fsm_alignment_prereg.md`, `fsm_succession_prereg.md`,
  `fsm_token_hold_findings.md` H6).
- **MH-D.14** Belief destruction is a defence effect no conventional metric
  registers ("what has been destroyed is an estimate rather than a foothold")
  · measured · **feed**: UNFED · carried by
  `state_bounds_measurable_disruption.md` concession 3 · read with C.7's two
  readings.
- **MH-D.15** The confusion penalty is the diversity family's only teeth
  against the movement attacker (blocked fraction ≈0.16 unchanged under
  OS/Service vs 0.72 under IP/Topology); IP shuffle works by severing position,
  not by addressing — the attacker has no IP model · mechanism · **feed**:
  `subsec:aio-disruption`; the penalty ablation (0 vs 20 s) is a named C
  obligation, unrun · carried by `hypothesis_tree.md` §8d,
  `pure_interrupt_pair.md` (which the parked list marks **cut-if-unfed**).
- **MH-D.16** Realised disruption is attacker-dependent because "the defence
  stands down when it loses" (trigger loops return once the network is
  compromised) · measured · **feed**: `sec:efficiency` occupancy · carried by
  `mtd_disruption_frontier.md` §8 — **no note**.
- **MH-D.17** Reporting discipline this evaluation adds over the lineage: effect
  sizes with confidence intervals ("no lineage paper reports a confidence
  interval"); a run count derived from a declared tolerance (Brown states
  none); parameter bands derived from the formalism's own structure ("ahead of
  the field" — Hong, Anderson, Carroll, Zhang, Reti give no range rationale);
  and the concessions the field owes and rarely pays — Jalowski's third
  guideline (compare against a state-of-the-art protected system) "not met by
  this evaluation or by most of the corpus"; the attacker-side suite labelled
  as model-validation instruments, not MTD metrics · declared · **feed**:
  `sec:dimensions` · carried by tex L5540–5570, design handoff §2, §5b, §13.4 —
  **no note**; say it once, briefly.
- **MH-D.18** Two quantities are called MTTC and differ ~26×; cross-arm
  comparability of the internal one was withdrawn under S3-R, and it ranks the
  mechanisms perversely (IP shuffle best, OS diversity below no defence) — its
  brief is owed before any ch5 row names it · measured / ruled · **feed**:
  blocked · carried by `stochastic_timing_design.md` §0, handoff README "one
  finding with no owner".

### Theme E — The lineage read (enters 6.2 as three rows, 6.3 as one point)

- **MH-E.1** The lineage disagrees with itself — Zhang: shuffle outperforms by
  >130 %; Ho: diversity outperforms in every metric, by ~140 %; Brown: best
  single ≈ best combination against Zhang's own "single shuffle may be
  advantageous" — and "that is the phenomenon to explain: different attacker
  behaviours reward different mechanism families, which is the thesis in one
  sentence" · conjecture until E5 runs · **feed**: `subsec:eff-lineage`,
  `tab:eff-lineage` (direction agreement only; configurations re-run, numbers
  never comparable; must stay at the lineage horizon) · carried by
  `evaluation_grading.md`, `hypothesis_tree.md` L-H2-prior (unrun) · note the
  **name collision**: "E5" is the ranking-shift conclusion in
  `experiment_02_findings.md` and the prior-model comparison in
  `hypothesis_tree.md`.
- **MH-E.2** What each prior work's attacker is and what this one changes:
  Brown's fixed flowchart with two design-time objectives (and the
  framing-vs-execution gap: "theoretically intelligent" vs "will always follow
  the attack procedure"); Zhang's Scenario 1 only, with the one attacker-side
  addition (exploit-time halving — "learns the network, not the defender");
  Ho's two-sentence inherited attacker and its own §5.1 "more complex
  adversaries need to be developed", placed first among its limitations; Tay's
  one-sentence attacker and the defender-side detection knob (the inverse of
  Jalowski's beacon primitive); Masud runs no attacker; Kim's single scripted
  scenario · verified per extraction ("Eight-property verification") ·
  **feed**: `tab:fidelity-verdict` prior rows (copied from Table 3.3; sync
  obligation) · carried by the six extractions.
- **MH-E.3** The lineage's own higher-fidelity attacker rotted: Brown's
  targeted Scenario 2 is unreachable on the shipped simulator (target
  unconstructable; termination commented out) — "evaluation methods have
  consolidated around an attacker chosen for tractability, and the alternative
  decayed unnoticed"; and a named metric returns a constant
  (`attack_path_exposure` = 1.0 in every run because the targeted attacker was
  descoped and the metric kept reporting) · measured · **feed**: none (a
  lineage fact) · carried by `fidelity_implications.md` F7, F8,
  `targeted_attacker_feasibility.md` §4 — **no note**; F8 is "the sharpest
  anecdote", Marc's editorial call.
- **MH-E.4** Brown's own mechanism sentence — a blocked attacker "simply needs
  to reconnect and then exploit the same vulnerabilities" — is exactly the
  interrupt-only channel the pure-interrupt pair prices; the present work
  makes the separation explicit · argued · **feed**: as D.15 · carried by
  `pure_interrupt_pair.md`.
- **MH-E.5** Tay's published evaluation never consulted the trained network
  (ε defaults to 1.0): its figures characterise a uniform random selector; the
  checkpoints are numerically degenerate; the reward has no cost term ·
  documented-nowhere driver behaviour · **feed**: `tab:factors-fixed` (the
  adaptive selector "not exercised, with the reason") · carried by
  `mtd_ai_forensics.md` — **what to say is Marc's call**; the project's random
  scheme arm is the honest replication; belongs, if anywhere, to the
  frozen-defender concession and ch7, not to a lineage critique.

### Theme F — Future work handed off by 6.3 (ch7's material, listed so the
pointers are right)

Each is an exclusion ch5 or the criterion makes explicitly, so the claim is
earned by a measurement or a stated scope: the reactive defender ("every
defence in the inherited pool moves on its own clock and is blind to the
attacker — this single fact closed two fidelity axes at once", and closes the
stealth consequence and the incentive payoff with them); the tactic-level
action layer (nine post-ingress tactics with nothing to map onto; "an
action-layer upgrade is not 'improve the result'; it is 'reset the anchor and
re-roll'"); stealth as a specified next experiment ("what is missing is the
defender-side observer, not the attacker-side behaviour"); the located
objective at depth (a measured boundary, not an untried idea); the
progress-carrying credit signal ("the whole of what remains" for the
behavioural rung); the mapping-sensitivity leaf V-map ("the one leaf that
could demote the whole tree" — unrun); the emulation rung (the portability
contract; magnitudes do not carry). Carried by `successor_programme.md`,
`emulation_rung.md`, criterion M8b fields, `hypothesis_tree.md` §8b.

---

## 5. The forward-join map

**Discussion points with no ch5 measurement behind them (by the parked list's
own rule, each is a cut or an experiment not yet designed):**

| Point | Status of the join |
|---|---|
| Properties 6 and 7 in the fidelity walk (C.5, C.6) | fed by `subsec:aio-capabilities`, a **retired label**; ruling C31 drops them to "implemented, not evidenced"; no ch4 antecedent either |
| Instruments fail silently (D.4) | ch5 says nothing about which instruments were re-validated; one clause in `sec:dimensions` earns it |
| Pure-interrupt pair (D.15 / E.4) | "unplaced as drafted … cut rather than asserted"; two conditions already in the seven, so a column, not a run |
| Learning warnings (D.12) | pointers at `subsec:aio-capabilities` and `subsec:sens-tactic-verb-mapping`, both retired |
| Effective behavioural breadth (B.4) | "nowhere in this chapter" as scaffolded |
| Stealth spacing (B.6) | column not added; ruling C11 |
| Per-tactic 13-fold variation (D.7) | no float after the restructure |
| MTD reaches execution not planning (D.8), belief destruction (D.14), plural preference (B.5) | no float, no pointer |
| Tie-in map line `sec:supplementary → sec:captured` | retired label |

**Ch5 measurements with no discussion consumer (the reverse direction):**

`fig:eff-cost-decomposition` (does a defence make the attacker do more, or
make what it does take longer — movement arm only, D-37); `tab:eff-cost`
effort-per-host ratios; blocked fraction and censored delay to first
compromise in `tab:eff-conditions` beyond the generic pointer;
`subsec:eff-lineage` (no FED BY line in ch6; the reviewer says it "belongs in
the discussion"); the timing-regime factor (near-periodic default, CV ≈
0.0025 — "the property MTD is named for is not instantiated" by default,
"trivially learnable"; if it moves an outcome it is the nearest thing to a
scheme-awareness proxy the chapter has); the horizon / checkpoint result;
recovery time and foothold retention across mutations (listed as instruments,
in no float); the sensitivity readouts on the exponential corner, the inert
floor and the two decays; the fact that the two network-layer mechanisms are
one attacker-facing effect (0.721 vs 0.725, margin undeclared).

Two of these carry themes on the board already (D.5 takes the frontier; D.2
takes the spanning pair); the rest are either a sentence in 6.3 or a cut from
ch5.

---

## 6. Foundation-risk register — what has moved under the notes

Ordered by how much of the chapter rests on it.

1. **The headline inversion is unreproduced.** ρ = −0.893 at ten seeds
   pre-restoration; ρ = −0.071 at fifty seeds on the restored substrate
   (`fsm_token_hold_findings.md` H0; `hypothesis_tree.md` §8f.1). The movement
   ordering is unchanged; the *inherited* attacker's moved under `d127f443`
   (OS 89 → 58 %, IP 22 → 68 %, topology 18 → 56 %); prior: D-19 is the cause;
   H2 "may return as a *family* contrast at a lower ρ". Consequences: D.1 is a
   hypothesis; Row B (C.11) is at an unproven grade; `defence_ranking_inversion.md`
   is stale; the criterion has not been re-scored though its trigger fired;
   every §(f2)/§(g) sentence quoting −0.893 inherits the flag. E2-R precedes
   everything.
2. **Profile-divergence attribution** (B.1): objective conditioning vs corpus
   size, the size-matched label-blind arm unrun; the L2 null failed and the
   claim is L3-scoped by ruling.
3. **The E3(b) plurality-reaches-defence statistic cannot fail on noise**
   (B.2); the crossover form is owed from paired data already on disk.
4. **Axis 7's exploit-learning null is pre-restoration** (C.6, D.12); D-19
   dropped the perfect-exploit ceiling; cheap pre-check named.
5. **Procedural mismatch's revisit condition is engaged** (D.13): ≤ 7.4 %
   removable; alignment widens the gap; "substantial" → "minor" by the note's
   own rule.
6. **Instruments-fail-silently's revisit condition is engaged** (C.14, D.4):
   a fifth instrument failed by the same denominator error.
7. **The adaptivity control is between-arm, not matched** (B.9); placebo null
   owed; the contrast differs in shape on the rebuilt nets.
8. **Stale magnitudes everywhere**: experiment 1's baseline (10/10 → 0/10
   after re-baseline); the sweeps ran at ten seeds, pre-restoration, `random`
   scheme, fixed-dwell regime; the fresh-host contract supersedes every
   pre-contract breadth figure (5.13 → 7.92); three restored singles have never
   run against the movement attacker; two overlay versions (v3/v4) on the page.
9. **The criterion's own inconsistencies**: axis 3 DEMONSTRATED in §(c),
   DESIGNED in §(d) prose (moot for the tick, wants fixing); "behaviourally
   grounded" defined by the encoded Jalowski subset in `architecture.md` §(f)
   (empty) and re-grounded on the partition in §(j) (never reconciled).
10. **Two feed maps disagree about property 6**: the tie-in map routes
    `sec:efficiency` (the cost-benefit frontier) to it; the ch6 block routes it
    to the disengagement frontier (retired) — different objects.

Nothing on this list is a reason to soften a claim in advance; each is a reason
to write the claim at the grade the re-established measurement earns, which is
what the grading instrument was committed for.

---

## 7. Session-proposed compositions — for Marc to judge

Kept apart from §4: each is a *composition* of on-disk material into a point
no record states as one, offered because the affinity grouping made the join
visible. None is asserted; each names its parts.

- **N1 — Two blind spots, one cause.** The field's attacker is blind
  post-ingress (A.1); the CTI corpus is blind pre-intrusion (A.6); and the
  simulator's own action layer has no verb for nine post-ingress tactics
  (A.5), so the substrate encodes the very coverage bias the evaluation is
  meant to expose. The honest coverage of the model is the intersection — a
  capture-side sentence for 6.1 that closes A.7's weakest-link symmetry. Parts:
  ch3 L3601–3607; ch4 L3996–4005; `action_layer_anatomy.md` §5.2;
  `technique_graph_construction.md`.
- **N2 — Three kinds of attacker state, three kinds of MTD effect.** The
  record prices disruption by what it destroys — position (severance; the
  network layer), surface (re-roll; the application layer), and belief (the
  learner's decayed estimate) — and no conventional metric sees the third.
  Composing D.2, D.14 and E6 (the SDR taxonomy vs the attacker-felt taxonomy)
  gives 6.3 a single sentence: MTD mechanisms should be reported by the
  attacker state they reach, not by the SDR class they belong to. Parts:
  `state_bounds_measurable_disruption.md`; `learning_capability.md` §7.4; tex
  L6047–6053. Risk: the belief channel has two readings on disk (C.7).
- **N3 — Tempo is the shared currency.** The degenerate region (D.3), the
  cost frontier (D.5), realised occupancy, learning decay per mutation, stealth
  exposure under a clock ("patience is pure exposure with no compensating
  benefit"), and the exponential's corner effect all turn on the ratio of
  mutation interval to tactic dwell — which is also why shape-not-scale
  suffices ("the thesis's punchline is itself a ratio game between mutation
  interval and tactic dwell", `operational_validation.md`). One paragraph of
  6.3 could carry the ratio as the unifying variable, with the interval stated
  beside every claim. Risk: reads as a generalisation the OAT sensitivity
  design does not license globally (C.9).
- **N4 — Attribution instruments fail on a slow attacker.** The
  disengagement frontier validates completely on the inherited attacker and
  attributes nothing on the profiled one because its projection is dominated
  by the attacker's own low progress rate — "the defence's *attributability*
  inverts too" (`attacker_disengagement.md` §4). A sibling of D.4 specific to
  attribution rather than progression: an instrument that separates "the
  defence stopped it" from "it was slow anyway" must be validated on the slow
  attacker. On disk in one record, in no note.
- **N5 — One substrate property per closed axis.** The record already says
  "one cause, three failures" for the attacker-blind defence pool (axes 4, 8,
  and stealth's consequence). Extending it: six host-compromise verbs close
  axis 1's outcome, axis 6's payoff and axis 7's credit signal. A two-row
  table (substrate property → axes it closes → the successor upgrade that
  reopens them) is the shape of ch7's argument and the honest summary of
  6.2's negatives. Parts: criterion axis 8 amendment; `successor_programme.md`;
  `hypothesis_tree.md` §8b.
- **N6 — APT tactical behaviour without APT target-seeking.** The records'
  own self-description after the targeted probe (B.7, B.13): the movement
  layer freed the operational axis and dropped the strategic one; given
  navigation it is more directed than the baseline, and without it it cannot
  find a target. This is a capture-side sentence 6.1 owes and no note carries;
  it also explains, in one line, why the simulator's objective is unreachable
  (A.5) without blaming the objective.
- **N7 — The recommendation depends on threat model and tempo jointly.** On
  the pre-restoration record ρ = −0.893 at 200 s and +0.286 at 2 000 s
  (`experiment_02_findings.md` §9–§10; Row B). If E2-R re-establishes any
  family contrast, the interval-dependence of the *contrast itself* is a
  finding one grade below H2 that survives H2 failing at the ordering grade.
  Entirely contingent on E2-R; recorded so the failure disposition has a
  named fallback.

Nothing else is proposed. The record's coverage of discussion themes is
wide; the gaps are joins and staleness, not missing ideas.

---

## 8. Housekeeping the sweep surfaced

- **Notes dirs are one chapter off** since the 2026-09-08 merge: every note
  under `ch5_experimental_setup/`, `ch6_results/`, `ch7_discussion/`,
  `ch8_future_work/` carries a stale `chapter:` field, and the four READMEs
  describe the pre-merge structure; only `_writing_guide.md` is current.
- **Two notes orphaned by the merge** — `evaluation_burden.md`,
  `evaluation_grading.md` — need a status line (the tex already asks for it);
  their content lands as the stability ∧ divergence bar in 6.2 and the
  three-grade vocabulary at the metric's definition site.
- **Three notes with engaged revisit conditions** need updating before they
  are drafted from: `defence_ranking_inversion.md` (§6 item 1),
  `procedural_mismatch_artefact.md` (item 5), `instruments_fail_silently.md`
  (item 6).
- **Stale labels in the ch6 comments**: `subsec:aio-capabilities`,
  `subsec:sens-tactic-verb-mapping`, `sec:supplementary` — all retired on
  `be53d621` / 2026-09-13; the FED BY and PARKED blocks still point at them.
- **The criterion owes**: a Row B re-score (trigger fired 2026-08-31); the
  axis-3 §(c)/§(d) reconciliation; the "distilled, rubric-clearing note for the
  discussion chapter" its §(h) names as the deferred second artefact — which
  this board is the census for, not the note itself.
- **Terminology the discussion would introduce**: "envelope, not actor",
  "shape, not scale", "severance" / "surface re-roll", the four badge words —
  none is in ch3/ch4 prose; each needs a first-use definition or a registry
  row. "Baseline" names two things (the no-defence reference and the
  comparison arm) and the registry ratifies "baseline attacker" for the
  second, so the reference is "no defence" everywhere. "Axis" is repo
  vocabulary; the dissertation surface says "property".
- **The E5 name collision** (theme E.1).

---

## Validation gate

Marc has ruled on: the unit split (§2, in particular whether limitations gets
a unit); the heading set (§3); and, for each FOUNDATION item in §6, whether the
claim waits for E2-R, is written at the lower grade now, or is cut. After
those rulings the board becomes the ch6 drafting brief: each unit names its
MH items, each MH item names its ch5 float, and no float is added to ch5 for
a discussion point without a run behind it.

## Hard constraints

- The badge ceiling and the modest-claim ceiling (`apt_model_criterion.md`
  preamble; `architecture.md` §(j)): "behavioural fidelity changes the answer",
  never "the attacker model is true"; every scored row envelope-relative.
- No sentence states the inversion as a fact of the current substrate until
  E2-R (`hypothesis_tree.md` §8f.1).
- No success-rate claim at the operating interval; no time-denominated
  cross-arm comparison; no value chosen because it improves an outcome
  (`fidelity_implications.md` hard constraints; S3-R).
- Scores move on evidence only (S6); the reported configuration is the
  modulators-null arm (freeze §4).
- The discussion introduces no codebase internals into prose (Marc, design
  handoff §14.2); repo vocabulary stays in the evidence footers.
- Branch, commit, no push (`session_workflow.md`).

## Reading list

- `docs/handoffs/2026-09-08_ch5_ch6_structure.md` — the placement rule ("ch5
  commits the criterion, ch6 reads it, ch7 says what it means") and the three
  named comparisons.
- `docs/handoffs/2026-09-09_ch5_experiments_design.md` §4, §10.5 — the
  property-to-measurement map and the parked discussion points.
- `docs/implementation/apt_model_criterion.md` §(b), §(c), §(d2), §(g) — the
  discipline, the scorecard, Rows A/B, the one-sentence defensible form.
- `docs/implementation/pipeline/ogasp/hypothesis_tree.md` §8b, §8d, §8f — the
  bind, the mechanism, the unreproduced headline.
- `docs/notes/ch7_discussion/` (all seven) and `docs/notes/_writing_guide.md`
  (the spine matrix and the ledger).
- `docs/workflows/evaluation_conventions.md` §f–§h — what a discussion section
  in this field does and how limitations are owned.

## Out of scope

Drafting any discussion prose (Marc's, by the drafting pipeline); re-scoring
the criterion; running E2-R or any experiment; editing the notes flagged in
§8 (each is its own small commit once Marc rules).

## 9. Supervisor input, 2026-09-22 (register E10)

Dr Hong named the discussion's two set-ups on seeing the 100-seed results, and
said that once the two evaluation phases are done "we're good for the
discussion". Both are already on the board; this section records that they are
now the supervisor's spine, not a session's composition.

1. **The model is harder to detect while slower and less successful.** On the
   inherited metrics the APT attacker model reaches fewer hosts and compromises
   its first later; on the reinstated stealth and detectability readings it is
   quieter and more widely spaced (E4). The discussion reads the two together:
   this is why an APT attacker model is needed, and the methodology must have
   explained the metrics well enough for the reading to land (E3). Claim ceiling
   unchanged: observations, no stealth state, property 5 still blank.
2. **The effective defence differs with the attacker.** Host-layer mechanisms
   disrupt the model more, service-layer mechanisms the baseline more, user
   shuffle helps the attacker — "there is no single solution", so an evaluation
   run against one attacker model does not transfer, and more research is
   needed (the future-work hook). Now to be evidenced across the interval range
   and with MTDShield as an arm (E6), so the sentence is written after the
   thousand-seed corpus, not before.

Both cite the restructured chapter (landed 2026-09-23): set-up 1 reads §5.2
*APT attacker model versus baseline attacker*, set-up 2 the headline §5.3.2
*Effect of the attacker model*.

## 10. Post-results macrostructure and headings — conventions survey and proposal (2026-09-28)

**Supersedes §2 and §3. RULED 2026-09-28** (Marc: "as a macro structure I will accept that … I'll go with option A"; confirmed the same day: Discussion 6.1–6.5, Conclusion with contributions and future work). Marc's question: 6.3 *What changes for MTD evaluation*
and ch7 *Future work* read as the same thing, and future work usually sits
inside the discussion or conclusion; the placeholder headings predate the
narrative. Three read-only passes: (i) the lineage and the 25 evaluation
anatomies, (ii) the thesis-writing literature, (iii) a map of every promise
ch1–ch5 make to ch6–ch8. Awaiting Marc's ruling; nothing applied to the tex.

### 10.1 Evidence

**The field and the lineage** (`sources/lit_review/`, `implementation/evaluation_anatomies/`):

- Conclusion 25/25. A heading containing "Discussion" 11/25 (6 top-level).
  Future work **inside the conclusion 13/25** (7 name it in the heading:
  chobenasher, maleki, manadhatawing, torquato, venkatesan, ho, cho), inside
  the discussion 5/25 (alavizadeh, brown, hong, kim, masud), its own section
  4/25 (bland, zhang, tay, he), none 3/25. "Limitation" in a heading 5/25;
  "Threats to validity" 0/25.
- **Discussion → Future work → Conclusion as three siblings: Tay only, 1/25.**
  `evaluation_conventions.md` §h calls Tay's split "the ruled shape of this
  dissertation's ch5/ch6/ch7"; that records the 2026-09-08 choice, not a
  convention.
- Lineage: Brown §V *Discussion* (A. Attacker capabilities and realism; B.
  Regaining access…; C. Attacker limitations; D. Need for multiple MTD
  techniques) → §VI *Conclusion*, limitations and future work inside the
  discussion (brown2023.md:178–209). Hong §7 *Discussion* (7.1 Comparing MTD
  techniques; 7.2 MTD techniques and threats; …) → §8 *Conclusion*
  (1_2_hong2018dynamic.md:625–678). Zhang (Masters) *6 Scope for Future Work*
  → *7 Conclusion*, future work restated in 7 (zhang2023.md:497–532). Ho
  *5 Future Works and Conclusion*, 5.1–5.5 limitation-shaped, 5.6 Conclusion
  (ho2024.md:491–596). Tay *6 Discussion* mirroring §5 one to one → *7 Future
  Works* → *8 Conclusion* (tay2024.md:346–407). None states research questions;
  none's conclusion answers one.
- Heading shape: discussion subsections are topic noun phrases everywhere
  (Brown, Hong, Tay); none is a question; claim-shaped headings only in Cho's
  survey (bold run-in labels).

**The thesis-writing literature** (full texts read online; *secondary* marked):

- Discussion moves: report and comment on key results (obligatory), then
  limitations, then recommendations for future research (optional) — Swales &
  Feak 2012, Fig. 18, p. 368; Paltridge & Starfield 2007, ch. 10, pp. 145–147.
- Conclusion moves: restate purpose, consolidate the research space, recommend
  future research, implications — Bunton 2005, *JEAP* 4(3) (abstract; the 82 %
  thesis-oriented figure is secondary). Paltridge & Starfield Table 10.2,
  p. 152, groups future research with limitations under "recommendations and
  implications".
- **Computer science specifically** (Soler-Monreal 2016, *Ibérica* 32, 48 CS
  PhD theses): future research in **93.75 %** of conclusion chapters,
  limitations in 64.58 %, paired limitation-then-future-work; titles
  "Conclusion(s)" 56.25 %, "Conclusion(s) and future work" 37.5 %; two final
  chapters (future work + conclusion) 12.5 %, whose moves "match" the
  conclusion's — the genre reads a future-work chapter as a split conclusion.
- Evans, Gruba & Zobel 2014: "a separate chapter of conclusions is much
  preferable"; "only minimal discussion in the conclusions chapter";
  "summaries are not conclusions"; two or three pages (pp. 121–123); too many
  chapters means "some are really only sections" (p. 13); group the discussion
  and head each group — the headings become the discussion's sections (p. 116);
  examiners "particularly impressed by candidates who are alert to
  shortcomings" (p. 115). Zobel: headings need not be sentences (p. 30);
  conclusions are where limitations may be restated and the work looks beyond
  itself (2nd ed., p. 148).
- Software-engineering reporting standard (Jedlitschka, Ciolkowski & Pfahl
  2008, §§3.10–3.11): *Discussion* = evaluation of results and implications,
  threats to validity, lessons learned; then *Conclusions and future work* =
  summary, impact (incl. limitations), future work. ACM SIGSOFT Empirical
  Standards: the discussion states implications and discloses limitations; the
  anti-pattern is conclusions written "as though the limitations don't exist".
- **UWA CITS4001 marking guide** (CSSE, 2019): the *Discussion* criterion asks
  whether shortcomings are recognised, improvements suggested for future
  studies, further work or loose ends named; no separate conclusion criterion.
  A marking rubric, not a chapter prescription — any structure meeting it
  passes, but limitations and further work must both be visible.
- Examiners read abstract, introduction and conclusion first and "check
  carefully for the link between the introduction … and the conclusions"
  (Mullins & Kiley 2002, pp. 376, 385).
- Implications versus future work are distinct moves (Bunton; Jedlitschka;
  Rudestam & Newton via Paltridge & Starfield), but sources blur them (Evans
  p. 121 folds "impact on future work" into implications; Swales & Feak Move 5
  joins future implementation and future research). The overlap Marc feels is
  a known seam in the genre; the fix is a stated boundary, not a new chapter.

**What ch1–ch5 already commit** (dissertation.tex as of `cc358fe5`):

- ch1 outline, l.501–504: ch6 "reads the results against the eight properties
  and draws out what they change for MTD evaluation"; ch7 "sets out the work
  that would extend the model"; ch8 "answers the research question". The
  connective-prose ruling (§c4) makes this re-checkable.
- ch4 l.5224–5225: "Chapter~\ref{ch:futurework} returns to it" (scheme
  awareness, retention across runs); l.5232–5236: the action-set ceiling and
  "a richer set of actions" — both future-work obligations.
- ch5 hands the discussion: why the unopposed gap is this size, why c3 stalls
  (Marc 2026-09-21), why the failure matrix changes little (§5.4), MTDShield's
  service-diversity bet (Marc 2026-09-26), the owed low-and-slow and dwell-only
  concessions (l.6121, l.7373), the one-terrain limitation (l.8560 block).
- Supervisor E10 (2026-09-22): the discussion is set up by the two phases —
  (i) slower and less successful on the field's metrics, quieter on the
  stealth readings; (ii) the effective defence differs with the attacker, "no
  single solution", more research needed.
- Two ticks in `tab:fidelity-verdict` (properties 6, 7) rest on no current
  ch5 result and no ch4 mechanism (§5, §6 above; R3) — a structural risk
  whatever the headings.

### 10.2 Diagnosis of the placeholders

1. **The discussion is organised on the wrong axis.** The writing guide's
   discussion column (capture → what it licenses; model → fidelity verdict;
   evaluate → what changes) assigns one section per sub-question. Answering the
   sub-questions is the *conclusion's* move (Bunton: restate purpose,
   consolidate; Mullins & Kiley: the introduction–conclusion link). Organising
   ch6 by sub-question makes ch6 and ch8 do the same job, and leaves ch6
   without the discussion's own obligatory move — comment on the key results
   (Swales & Feak). The capture sub-question has no measurement of its own
   (the matrix's own empty cell), so 6.1 had nothing to interpret.
2. **6.1 and 6.2 are one section.** Both are the walk of the eight properties
   (the two comment blocks drifted into each other's jobs, §1 above).
3. **6.3 and ch7 overlap because nothing separates implication from
   future work.** 6.3's verb-shaped heading ("What changes…") reads forward.
4. **Future work is a section's worth (750 words, 3 units) standing as a
   chapter** — the form 1 of 25 field documents uses and Evans warns against.
5. **No home for limitations** — the charter's second movement
   (`ch7_discussion/README.md`) and six ch5 hand-offs.
6. **"Fidelity verdict" introduces two words ch1–ch5 never define** (*fidelity*
   appears once, in the ch4 opener; *verdict* nowhere) — the no-invented-terms
   rule (E2/E3).

### 10.3 Proposal

Two organising axes, one per chapter: **ch6 is organised by the results** (the
two phases, then the appraisal of the model, then what follows, then its
limits — the Swales & Feak order); **ch7 is organised by the research
question** (the answer, sub-question by sub-question, then the next step).
Future work becomes the last section of the conclusion — the modal form in
the field (13/25) and in CS theses (93.75 %), and the placement that lets the
dissertation end on the E10 hook.

**Chapter 6 — Discussion** (2 250 words, 9 units; unchanged)

| § | Heading | Job | Reads | Units |
|---|---|---|---|---|
| — | (opener) | the two phases in one sentence each; roadmap | — | — |
| 6.1 | Attacker behaviour without defence | interprets phase one: fewer hosts and slower on the field's outcome metrics, quieter on attack rate and confidentiality (E10 set-up i); why the gap is this size; why c3 stalls; not a race with the baseline (`refusing_the_baseline_race.md`) | §5.2 | 2 |
| 6.2 | MTD performance against the APT attacker model | interprets phase two: the layer reversal and its mechanism (a defence destroys only the state the attacker carries — position against exploit; `state_bounds_measurable_disruption.md`); user shuffle helping the attacker; MTDShield; ρ ≈ 0 (E10 set-up ii) | §5.3 | 2 |
| 6.3 | Properties of the APT attacker model | the return of Table 3.3 (`tab:fidelity-verdict`): the scoring discipline, then the walk property by property; adaptivity told frankly from the ablation (the staged placeholder); what the 38 flows license (the capture thread's ceiling) | §5.2–§5.4, ch4 | 2 |
| 6.4 | Implications for MTD evaluation | present-tense consequences for anyone running an MTD evaluation now: the attacker model is a variable of the evaluation; a recommendation against one attacker does not transfer ("no single solution"); success metrics alone misread a slow, quiet attacker; operating-point discrimination; re-validate instruments on an attacker change | §5.2, §5.3 | 2 |
| 6.5 | Limitations | owned in one place: one terrain; the action-set ceiling; declared parameters (the failure matrix, the low-and-slow exposure); single-analyst coding; 38 flows and the observability boundary; no cross-paper comparison; the frozen defender (Jalowski's third guideline); the simulation rung | ch4, ch5 | 1 |

**Chapter 7 — Conclusion** (500 + 750 = 1 250 words, 5 units; the future-work
chapter's budget moves here)

| § | Heading | Job | Units |
|---|---|---|---|
| — | (opener) | the research question answered directly, in the introduction's words | — |
| 7.1 | Contributions | each of ch1's three contributions restated as the answer to its sub-question, with its impact — not a recap (Evans: "summaries are not conclusions") | 2 |
| 7.2 | Future work | each item paired with the limitation (6.5) or unmet property (6.3) it would lift: a richer action set (ch4 l.5232); stealth against a detector (property 5 — the observer, not the behaviour); scheme awareness and retention across runs (property 8; ch4 l.5224); MTD selected or optimised against the APT attacker model (E1's declined third phase; MTDShield); other network sizes and the emulation rung. Run-in paragraphs, no subsections (the ledger: a heading is a 250-word claim) | 3 |

**The boundary between 6.4 and 7.2**, stated so a draft sentence can be sorted
mechanically: an *implication* rests on a ch5 result and says what an
evaluation should do now with the tools that exist; a *future-work item* rests
on a limitation or an unmet property and says what should be built next. The
E10 hook splits along it — "no single defence performs best against both
attackers" is 6.4; "more research is needed" is 7.2.

**Heading audit** (Marc's rules; `feedback_thesis_heading_conventions`):
sentence case; noun-phrase labels, the claim in each first sentence; APT
visible (6.2, 6.3); no acronym beyond APT and MTD; every noun already met in
ch1–ch5 — *attacker behaviour* is §4.5.1's metric class, *MTD performance*
echoes the research question ("How does MTD perform…"), *properties* echoes
§3.3.1 *Properties of a sophisticated attacker*, *MTD evaluation* is §3.2's
heading; four grammatical shapes across the five siblings, so no repeated
scaffold. *Limitations*, *Contributions*, *Future work* are the generic labels
the CS corpus uses (Soler-Monreal §4.2: generic headings, topic-specific
subheadings). 6.1–6.2 mirror §5.2–§5.3 in order (Tay's form, the one ch5 setup
handoff flagged as claimed but untrue of the current ch6).

### 10.4 Alternatives weighed

- **B — limitations and future work closing the discussion** (6.5 *Limitations
  and future work*, He's heading; a two-unit conclusion). Keeps each limitation
  beside the work that lifts it and matches the UWA guide's *Discussion*
  criterion literally. Not recommended: ch6 grows to 12 units, the conclusion
  shrinks to a recap, and the dissertation ends on a summary rather than the
  next step the writing guide asks the conclusion to name.
- **C — keep three chapters** (Tay). The 1-in-25 form; a 750-word chapter; the
  6.3/ch7 overlap persists and needs the boundary above anyway.
- **Chapter title "Conclusion and future work"** (37.5 % in CS; Ho's local
  inversion). Equivalent in substance; the section heading already puts future
  work in the contents page, and `ch:conclusion` stays.

### 10.5 What a ruling changes (not done here)

- tex: the ch6 headings and labels; `ch:futurework` → a section label under the
  conclusion; ch4 l.5224 re-pointed; ch1 outline l.501–504 rewritten (ch6's
  sentence can stand; ch7/ch8's two become one). The ch6 comment blocks re-keyed
  to the new sections; stale labels in them (§8) fixed in the same pass.
- `_writing_guide.md`: the matrix's discussion column (the sub-question threads
  close in the conclusion, not the discussion); the one-line-job rows; the
  ledger (Future work 3 → Conclusion 2 + 3; chapter count 8 → 7).
- `evaluation_conventions.md` §h: "the ruled shape" sentence overturned on the
  §10.1 census.
- `docs_map.md` and `notes/ch8_future_work/README.md`: the notes dir can stay
  (it names a body of ideas, not a chapter) but its README's "chapter" wording
  changes.
- Unchanged: the ch6 budget, the total, Table 3.3's return, every §4 board item
  (each re-homes by the table in §10.3).

## 11. Microstructure of ch6 and ch7 (2026-09-28, proposed)

Three read-only passes on 2026-09-28: (i) the internal moves of the lineage's
and the field's discussions plus the applied-linguistics move models; (ii) the
threats-to-validity literature, general and simulation-specific; (iii) an
inventory of every assumption, ceiling and concession in the tex (34 rows).
Numbers below are as the ch5 prose states them (100 seeds, `\prelim`); the
drafting session re-reads them from the 1 000-seed corpus.

### 11.1 What the conventions fix

- **One move cycle per finding.** A discussion is "recycled sequences" of
  reporting a result and commenting on it, "inside out", major findings first
  (Swales & Feak 2012, Fig. 18 p. 368, p. 369, p. 324); the statement of the
  result is the obligatory "head" of each cycle (Hopkins & Dudley-Evans 1988,
  secondary via Boonyuen 2018). In CS the cycle runs result → explanation or
  deduction more than result → literature (Posteguillo 1999, secondary). The
  lineage does exactly this: Tay §6 one subsection per §5 result
  (tay2024.md:350–388); Ho one paragraph per metric, result → "because"
  (ho2024.md:517–549).
- **The cycle, as this chapter uses it:** (a) restate the result with a
  back-reference, no new numbers or floats (Tay :356; Alavizadeh p. 14);
  (b) account for it by mechanism; (c) compare — the two attackers, or what the
  lineage expected; (d) bound it — hypotheses labelled as such (Tay :374 "We
  hypothesize"), negatives stated plainly (Alavizadeh p. 14; Tay :380);
  (e) deduction.
- **No headings below the section.** Discussion subsections in the lineage and
  field run 1–5 paragraphs and never carry a third level (Brown 3/1/1/1, Hong
  1–2, Tay 3/3/1/2/1, Zhang 3/1/1/1); Evans et al. 2014 p. 116: three or four
  groups, no more than three sub-headings in a section. Run-in labels (Kim,
  He, Alavizadeh) where a section needs internal signage.
- **Hedging is the discussion's register** (Hyland 1995: 36 hedges per 1 000
  words in discussions against 20 in results), "confidently uncertain"
  (Swales & Feak pp. 156–157), never over-hedged to "saying almost nothing"
  (p. 163).
- **Threats to validity** (full evidence in the pass-(ii) record, sources
  listed below): the four types come from Cook & Campbell via Wohlin et al.
  2012; de França & Travassos 2015 (*CLEI EJ* 18(1)) catalogue 28 threats
  specific to simulation studies in those four types, and name "simulation
  model simplifications (assumptions) forcing the desired outcomes" the most
  recurrent, and "the simulation model itself … the main threat to the study
  validity" (§4.2, §5); the ACM SIGSOFT Simulation standard expects typed
  threats "considering the supporting data and the simulation model", and lists
  as an *invalid* criticism "the mere presence of assumptions … as long as the
  assumptions are documented and justified". What makes the section defensible
  rather than boilerplate: each threat paired with the mitigation already
  carried out and the residual it leaves (Feldt & Magazinius 2010: 0.49
  mitigations per threat, 26.5 % "just mentioned as future work"; Lago et al.
  2024: 61.5 % of ICSE distinguished papers report none); no "laundry list"
  (Verdecchia et al. 2023); and the limitations *of the artefact* kept apart
  from the threats *to the investigation* (Verdecchia P7: "TTV are the
  consequences of the choices made due to the limitations"). No MTD paper in
  the 25 uses the typed form (0/25); security venues say "Limitations" by
  habit, with typed sections a recommended minority (Schloegel et al. 2024:
  20 % of 150 fuzzing papers). Placement: implications before threats
  (Runeson & Höst 2009 Table 9; ACM General Standard), with the antipattern
  "implications and conclusions [written] as though the limitations don't
  exist" answered by each implication carrying its own bound.
- **Name clash to avoid:** Sargent's model-validation technique called
  "internal validity" is not Cook and Campbell's (de França & Travassos §6).
  The thesis uses the Cook and Campbell sense only.

### 11.2 Chapter 6 — Discussion, section by section

**Opener** (no heading; connective_prose.md §b, ~100 words): the chapter reads
the two phases in turn, scores the model on the eight properties, draws what
follows for MTD evaluation, and bounds it.

**6.1 Attacker behaviour without defence** — reads §5.2; the E10 set-up (i).
Three cycles, major first:

1. *Less success, more slowly* (NCR 0.14–0.20 against 0.49; first compromise
   about three times later) → mechanism: seven of fifteen tactics have no
   action and hold the attacker in dwell (26–47 % of steps); 14–28 % of
   dispatched actions fail a precondition → compare: an APT is defined by
   persistence toward an objective, not by speed (Alshamrani) → bound: pace is
   a declared input (the low-and-slow family) → deduction: the model is not a
   competitor to the baseline (`refusing_the_baseline_race.md`).
2. *Quieter* (lower attack rate; attack confidentiality 69–93 % against 67 %
   falling to 43 %) → mechanism: dwell spaces the actions the detector counts
   → compare: the field's outcome metrics cannot see it, which is why an APT
   attacker model is needed (E10 i) → bound: one observation, a declared
   detector tuned on the baseline, property 5 stays blank.
3. *Behaviour differs by objective*; openings differ in over 70 % of runs
   except $c_3$; $c_3$ stalls → mechanism for $c_3$ (Marc's, ruled
   2026-09-21 as ch6's) → bound: the corpus-size confound (C4 below).

**6.2 MTD performance against the APT attacker model** — reads §5.3; the E10
set-up (ii). Four cycles:

1. *The layer reversal* (the host layer holds back the APT attacker model most,
   service diversity the baseline) → mechanism: a defence can destroy only the
   state an attacker carries — position against exploit
   (`state_bounds_measurable_disruption.md`) → compare: the lineage's own
   disagreement (Zhang favours shuffle, Ho diversity) read as the same
   phenomenon (MH-E.1) → bound: the disruption channels are not symmetric
   between the two attackers (S2) and fidelity is a bundle no control
   separates (E5).
2. *Time lost per MTD deployment* (host mechanisms cost the model 429–511 s,
   the baseline nothing measurable; service diversity the reverse) → mechanism:
   severance of the foothold against a retry of the same exploit (Brown's own
   "simply needs to reconnect", MH-E.4).
3. *User shuffle helps the attacker* (reduction below zero up to 500 s) →
   mechanism, or labelled as unexplained.
4. *Deployment strategies and MTDShield* (random and alternative favour the
   model; MTDShield the baseline; ρ ≈ 0 across mechanisms) → mechanism:
   MTDShield chooses service diversity at 70–76 % of decisions and was trained
   against the baseline (Marc's 2026-09-26 bet, stated as a hypothesis) →
   bound: MTDShield outside its training conditions (S4).
   Deduction closing the section: no single defence performs best against both
   attackers — handed to 6.4.

**6.3 Properties of the APT attacker model** — reads ch4 and §5.2–§5.4.

- ¶1 *The discipline*: the eight properties were fixed in §3.3.1 before the
  model was scored; Table 3.3 returns with the APT attacker model as a fourth
  row; the row's decode differs from Table 3.3's and the caption says so.
- ¶2–4 *The walk, grouped by verdict, not eight paragraphs* (the field's
  honest self-row is Torquato's Table VII, not Masud's all-ticks Table 5;
  run-in labels): **shown to change an outcome** (2 objective conditioning;
  3 plurality if §5.2's openings carry it); **implemented, no advantage shown
  on this simulator** (1 persistence; 4 adaptivity — the ablation told
  frankly, the staged placeholder); **not met** (5 stealth — the behaviour is
  measured, the detector is missing; 8 scheme awareness, ruled out). Properties
  6 and 7: see §11.6.
- ¶5 *What the capture licenses*: 38 flows give an envelope of documented
  behaviour, not one actor; the model can only be as good as the actions it
  adopts (ch4 l.5232), which points back to §3.3.3's "weakest link" as the
  ch3 comment asks.

**6.4 Implications for MTD evaluation** — present tense, for anyone running an
MTD evaluation now. Opens by scoping what transfers: the dependence and the
method, not the numbers (Tay :348 form). Each implication: source finding →
who it changes practice for → conditional recommendation → its bound (Hong
§7.1 :643; Brown §V.D :205).

1. *The attacker model is a variable of the evaluation*: a recommendation
   drawn against one attacker does not transfer (6.2) — evaluate against more
   than one attacker model, and name the one used.
2. *Outcome metrics alone misread a slow, quiet attacker* (6.1) — report
   attacker-behaviour metrics beside the outcome.
3. *Declare the attacker model against the eight properties*: closes the first
   half of ch3's gap ("the literature does not formally define its attacker
   models", l.4086) with the instrument the dissertation used — Table 3.3 as a
   reporting device any evaluation can fill in.
4. *Show the metric can discriminate at the chosen operating point* (ASP near
   its floor, E2; `operating_point_discrimination.md`).

The E10 hook splits here: "no single solution" is implication 1; "more
research is needed" is §7.2.

**6.5 Threats to validity** — the last section, handing its residuals to §7.2.

- ¶1 *Scope, then the four types.* The artefact's limitations by design —
  the six adopted actions, the frozen defender, no scheme awareness or
  learning across runs, one network, the simulation rung — stated once as
  scope, each paired forward with its §7.2 item (Verdecchia P7; He's
  limitation-with-future-work form). The four types defined in one sentence
  each, cited to Wohlin et al. 2012 and, for simulation, de França & Travassos
  2015.
- ¶2 **Internal** (first, because the headline is causal: the attacker model
  changes which defence wins). Threats: fidelity is a bundle of order, timing
  and failure response that no control separates (E5); the disruption channels
  reach the two attackers differently (S2); profiles may separate on corpus
  size rather than objective, the size-matched control unrun (C4); the
  inherited 20 s confusion penalty (S1). Mitigations: same network, defences,
  actions and seeds for both attackers; §5.4 isolates the failure matrix.
  Residual: the claim is "the APT attacker model changes the answer", not
  "behavioural fidelity does" (the 2026-09-25 mark-risk ledger's wording).
- ¶3 **Construct.** The declared inputs — the tactic-to-action mapping with no
  interval (the standing bound; one root with the action ceiling, the
  adaptivity cap and the precondition failures — consolidate, do not list four
  times), the dwell times and the low-and-slow family, the failure matrix;
  attack confidentiality read through a declared detector; time lost per MTD
  deployment as a lower bound in a window; objective classification by one
  coder (Runeson & Höst's reliability, filed here). Mitigations: Appendix C's
  robustness analyses, §5.4, the cross-check of App. B.2. Residual: the
  magnitudes at 200 s move across the low-and-slow band (44–89 % against 75 %);
  the orderings are what the chapter claims.
- ¶4 **External.** 38 flows, detected and published campaigns only, sparse
  before intrusion, 16 sharing an operator; one network of 50 hosts; MTDShield
  outside its training conditions; no numeric comparison with the lineage
  papers. Sargent's unobservable-system ceiling cited as the discipline's own
  prescription (explore the model's behaviour as thoroughly as possible), and
  de França & Travassos's "reduces the findings only to the simulation model".
- ¶5 **Conclusion.** 1 000 seeds; negligible below $d = 0.2$ (§4.5.4);
  Scott-Knott ranking; no correction across about 160 comparisons; ρ without
  an interval. Short, because it is the best-mitigated.

### 11.3 Chapter 7 — Conclusion

- **Opener** — the research question answered in the introduction's words, in
  two or three sentences; the introduction–conclusion link examiners check
  (Mullins & Kiley 2002, p. 385).
- **7.1 Contributions** — three paragraphs, one per ch1 contribution, each
  stated as the answer to its sub-question (SQ1 → contribution 1, …) with its
  impact on the field, not a recap (Evans p. 122). The strengths and the
  bounds of 6.3 and 6.5 travel with each claim (the ACM antipattern).
- **7.2 Future work** — run-in paragraphs, ordered as 6.5's scope paragraph
  names them, each opening on the limitation it lifts: a richer action set
  (ch4 l.5232; the binding constraint); stealth against a detector (property
  5 — the observer, not the behaviour); scheme awareness and learning across
  runs (property 8; ch4 l.5224); MTD selected or optimised against the APT
  attacker model (E1's declined third phase; MTDShield retrained); other
  network sizes and the emulation rung. The dissertation's last sentence names
  the next step (the writing guide's job for the conclusion).

### 11.4 Budget

| Unit | Words | Units |
|---|---|---|
| ch6 opener + 6.1 | 500 | 2 |
| 6.2 | 500 | 2 |
| 6.3 (+ Table 3.3's return, outside the count) | 500 | 2 |
| 6.4 | 500 | 2 |
| 6.5 | 750 | 3 |
| **ch6** | **2 750** | **11** (was 9) |
| ch7 opener + 7.1 | 500 | 2 |
| 7.2 | 750 | 3 |
| **ch7** | **1 250** | **5** |

The threats section's floor is about 700–900 words (pass (ii); no source sets a
norm) against the one unit §10.3 gave it; the two extra units are proposed
against the float (3 → 1), which the ledger's conservation rule requires naming.

### 11.5 Heading audit

*Threats to validity* is a field term new to the dissertation's surface; the
no-invented-terms rule is met by citing it (Wohlin et al. 2012; de França &
Travassos 2015) in 6.5's first paragraph, and neither is yet in
`references.bib` (Wohlin's section and page to be checked from the book, not
from secondary paraphrase). The other four headings stand as audited in §10.3.
*Limitations* remains the fallback heading if Marc prefers the MTD corpus's
word: the internal organisation above survives either way.

### 11.6 Open — Marc's rulings

1. **6.5's heading**: *Threats to validity*, typed (recommended), or
   *Limitations*, grouped by the claim each bounds.
2. **Two float units** to 6.5 (recommended), or 6.5 held at one unit and
   6.4 cut to one.
3. **Properties 6 and 7** in `tab:fidelity-verdict`: ticked, with no ch5
   result or ch4 mechanism behind them (§5, §6; R3). Drop to blank with a
   sentence in the walk ("built in earlier versions, not part of the evaluated
   model"), or restore an antecedent. Any structure inherits this.
4. **The order of 6.4 and 6.5**: implications then threats (recommended; the
   SE standards, and 6.5 hands straight to §7.2), or threats first (Swales &
   Feak's order; the implications then read already bounded).

### 11.7 Checks before drafting (flagged, not actioned)

- **E4 contradiction**: ch4 l.5641–5642 says the outcome metrics are
  "comparable with the field's"; `metrics_semantics.md` says cross-paper
  numeric comparison is invalid. A ch4 fix, not a ch6 concession.
- **S2 / D-35**: the disruption-channel asymmetry rests on the 2026-09-09
  record; check it against the ch4 l.4779–4781 claim that a deployment
  interrupts an action in flight before 6.2 or 6.5 states it.
- **Deployment count**: the ch5 setup handoff notes every mechanism logs
  exactly 75 deployments with zero spread — uninvestigated, and time lost per
  MTD deployment divides by it.
- **Six high-severity threats appear in no prose** (C4, M2's reach into
  outcomes, M4 as the standing bound, S2, E5, E7 while `\prelim` stands): 6.5
  is their first and only statement, which is why it needs the words.

Sources for §11 (read by the passes unless marked): Swales & Feak 2012;
Evans, Gruba & Zobel 2014; Hyland 1995 (*HKPLLT* 18); Yang & Allison 2003,
Hopkins & Dudley-Evans 1988, Posteguillo 1999 (secondary, via Amnuai &
Wannaruk 2013 and Boonyuen 2018); Runeson & Höst 2009; Feldt & Magazinius
2010; de França & Travassos 2015 (2016 *EMSE* paper unread); Verdecchia et al.
2023 (*IST* 164); Lago et al. 2024 (ESEM); Schloegel et al. 2024 (S&P);
ACM SIGSOFT Empirical Standards (General; Simulation); Sargent 2011; Law 2015;
Rossow et al. 2012; van der Kouwe et al. 2018; Wohlin et al. 2012 (via Feldt
& Magazinius — **not read**).

### 11.8 Rulings, 2026-09-28 (Marc, spoken, on §11)

- **6.1–6.5 and the conclusion's shape: ACCEPTED** as §11.2–§11.3 set them out
  — the contributions answer the sub-questions; future work answers the
  threats.
- **6.5 heading: *Threats to validity*** — the term Marc and Jin have already
  discussed; *Limitations* stays the fallback, the internal organisation is the
  same either way.
- **Budget (§11.6 item 2): no ruling needed** — "I'll just write and then I'll
  just cut later". The float proposal is withdrawn; §11.4 stands as a guide,
  not a claim.
- **Order (§11.6 item 4): implications before threats.**
- **E4 (§11.7): agreed wrong** — "comparable with the field's" does the work an
  injustice even within the lineage, since this dissertation's own two attackers
  do not compare one to one. Marc picks up the ch4 l.5641–5642 fix.
- **S2 (§11.7): holds by design, not a gap.** How disruption reaches each
  attacker, directly and indirectly, was modelled on purpose to make the
  comparison fair, and §5.3.1 *Response to disruption* reports it. 6.5's internal
  paragraph cites that design as the mitigation, rather than raising S2 as a new
  threat.
- **The 75-deployment flag (§11.7): retired.** 75 × 200 s is the 15 000 s time
  limit, so a fixed count at a near-periodic interval is expected.

### 11.9 Properties 6 and 7, and the vulnerability memory (2026-09-28)

Marc asked whether the attacker's vulnerability memory belongs in the method
with an ablation in the results. His recollections were that property 7 is the
memory, that a memorising attacker would be more successful, and possibly that
small networks were tested. What the code and the record hold:

- **The vulnerability memory is property 7.** `mtdnetwork/component/adversary.py`
  (l.92–100) keeps a count of prior *successful* exploits per vulnerability
  type, carried across hosts and never decayed across MTD, which raises the
  odds of re-exploiting a familiar type (λ). It is **off by default**. A second
  learner, the APT attacker model's within-run belief about which destinations
  pay (`src/mtdsim/l3_simulation/movement/learning.py`), forgets a fraction ρ on
  every deployment. Property 6 is the cost model (the utility modulator λ; the
  disengagement frontier).
- **"Memorises everything, so more successful" is the reverse of the record.**
  - The exploit memory operates, but moves no outcome: a *perfect* exploit adds
    about 0 hosts at every time limit, because breadth on this simulator is not
    gated by exploit success (`exploit_learning_findings.md` §(a)).
  - The routing learner that never forgets does *worse* under MTD: ρ = 0 was
    CI-worse than ρ = 0.5 (MH-C.7), and learning lowered breadth because the
    reward is not progress (criterion §(g)).
- **Neither is in the dissertation as it stands.** The ch4 prose defines no
  learning, memory, cost or utility mechanism; every reported run is the
  modulators-off configuration. The numbers also predate the substrate
  restoration: D-19 reinstated the OS gate, so the perfect-exploit ceiling
  behind the null may have dropped (the ch5 comment blocker at l.~7462).
- **No small-network run exists in the record.** The pre-registered sweep moved
  the vulnerability pool (`services_per_os`) and the time limit, never the
  network size. Marc's intuition has a mechanism in the record ("pool-mediated:
  a constrained pool grants re-encounters; diversity denies them", §(d)), but
  network size and pool size are different levers, and the one that matters is
  how often a vulnerability type recurs across the hosts the attacker reaches.

**Recommendation.** Keep the memory out of the method and results. Blank
properties 6 and 7 in `tab:fidelity-verdict`, each with one sentence in 6.3
("not part of the evaluated model"), and name the memory in §7.2 as a specified
next experiment: whether an attacker that remembers the vulnerability types it
has exploited gains where types recur more often (a smaller network, a narrower
pool, less diversity), measured by attempts per host taken as well as by
breadth. That fits Marc's own rule ("if there's nothing we can talk about,
there's nothing we can talk about"), keeps the ch5 antecedent rule, and costs
no runs three weeks before submission.

**If Marc wants it in instead**, the cheapest deciding step first: measure the
APT attacker model's exploit-success rate in one no-defence cell on the restored
simulator.

- If the OS gate refuses few exploits, the ceiling stands, the null stands, and
  the recommendation above holds.
- If it refuses many, the memory has headroom it lacked when measured. Then a
  ch4 insertion (one mechanism paragraph and its λ), a ch5 ablation (on/off ×
  pool or network size) and a float follow, about 370 runs.

Owed either way: the ch5 blocker comment and the orphaned "cost and memory"
scaffolding (l.~7400–7470) get a status line saying which way it went.

### 11.10 Applied, 2026-09-28 (Marc: "I accept all the changes in terms of heading … put any other placeholders where they need to be")

- **tex**: ch6 re-headed 6.1–6.5 as §11.2 sets them out (labels
  `sec:disc-behaviour`, `sec:disc-mtd-performance`, `sec:fidelity-verdict`
  kept for 6.3, `sec:evaluation-implications` kept for 6.4, `sec:threats`); the
  Future work chapter folded into the Conclusion as §7.2 (`sec:future-work`)
  beside §7.1 *Contributions* (`sec:contributions`); `ch:futurework` and
  `sec:captured` retired (a label map heads ch6). Every old comment block moved
  under the section that now owns it (verified: only the retired headings,
  labels and one re-pointed comment reference are gone). Placeholders carry
  §11.2's cycles for every section, the chapter opener and the conclusion's
  opener. Re-pointed: ch4's "Section~\ref{sec:future-work} returns to it"; the
  ch1 outline's last two sentences merged (Marc's words kept, ratify on read).
  Build clean, 101 pages, no undefined references.
- **Not changed**: the property 6 and 7 marks (§11.9, open); ch5 §5.4's heading
  and any exploit-memory placeholder (waiting on the pre-check); the ch4
  comparability sentence (E4 — Marc's fix).
- **Docs**: `_writing_guide.md` (matrix gains a Conclusion column — the threads
  close there; job rows; ledger), `evaluation_conventions.md` §h (the "ruled
  shape" overturned on the census), `docs_map.md` (the `ch8_future_work/` row).

### 11.11 Exploit-memory pre-check on the restored simulator (2026-09-28)

Run on HEAD `4ecabb69`, the §5.3.1 unopposed configuration (50 hosts, no
defence, targeted objective, 15 000 s), seeds 0–19 shared across arms; 800
runs, no errors; the control arm reproduces the corpus on those seeds (baseline
24.6 hosts, $c_{\mathrm{agg}}$ 8.95). 20 seeds, **preliminary**. The runner,
the analysis script and the raw rows sit in the session scratchpad
(`precheck/ceiling.py`, `analyse.py`, `*.jsonl`), not tracked. The 2026-08
"perfect exploit" arm was never in `tools/exploit_learning_sweep.py`, so it was
rebuilt as a wrapper around `Vulnerability.network` for this check.

- **Exploit success**: about 0.70 of rolls succeed. The restored OS gate
  refuses 0.49–0.57 of the APT attacker model's exploit attempts (0.41 of the
  baseline's) with no defence at all.
- **A perfect roll, gate kept, still adds about 0 hosts** to every profile, for
  both objectives and in a narrow pool (`services_per_os` = 3). Winning the
  roll is not the binding constraint.
- **Gate removed: about +2 hosts** (CI excludes zero for $c_{\mathrm{agg}}$ and
  $c_4$), with attempts per host falling from about 50 to about 28. The gate
  is the binding exploit-side limit on the restored simulator.
- **The memory (λ = 2) operates**: 22–39 vulnerability types per run are
  re-exploited on a second host, and success per roll rises 0.71 → 0.74 (0.85
  in the narrow pool). **But it moves breadth in no cell for the APT attacker
  model**, because it acts on the roll and a refused attempt never rolls.
- **Baseline attacker**: the only non-null is the general objective (memory
  +0.95 hosts, CI [+0.14, +1.76]; perfect roll +1.3), bounded by the 80 % stop.
  Under the targeted objective the dissertation evaluates, it is null.

**What this licenses.** The August null stands for the dissertation's
configuration, for a different reason than the record gives: the simulator's
OS-gated exploit action, not the roll, bounds what the attacker can take. That
is the adopted-actions threat (§11.2, 6.5) shown directly: a capability built
into the attacker cannot act on the constraint that binds. It is reportable
as a second ablation beside the failure matrix, and 6.3 can then read property
7 as "operates, no advantage, blocked by the actions", like property 4.

**What a §5.4 ablation needs before it is written.**
- A tracked runner with the perfect-roll and gate-off arms built into `tools/`,
  not the scratchpad wrapper.
- A ch4 mechanism paragraph for the memory and its λ (the antecedent rule).
- 100 seeds, then 1 000 per the seed-count protocol.
- The gate-off arm framed as a diagnostic of the simulator, never as an attacker
  configuration.
- Marc's ruling on §5.4's heading (two ablations).

### 11.12 Why the memory moves no hosts: the missing link is the hop, not the roll (2026-09-29)

Probes on HEAD `fc008c8d`, the §5.3.1 unopposed configuration (no defence,
targeted objective, 15 000 s), 20 seeds × {aggregate, exfiltration}, one process
per run; **preliminary, scratch-grade** (monkeypatched exploit core). Runners and
`numbers.json` in `data/results/vulnerability_memory_mechanism/` (raw rows
untracked; `summarise.py` rebuilds the numbers). A first pass reused worker
processes, stacked its patches across arms and was discarded; every number
below is from the clean re-run.

**The four steps a two-hop host takes** (the narrative Marc ruled for §5.4.2 and
§6.3, 2026-09-29):

1. **Exploit visit 1 usually wins and opens a service**, but the host does not
   fall: a host falls only when a compromised service (exploited impact past 7)
   sits next to its internal target node in the service graph, and for 71 % of
   the hosts attacked that node is two services in (`host.py` `check_compromised`,
   `get_services`). MTDSim returns a **failure verdict** — the host's, not the
   rolls'. Precision for the prose: exploit 1 does not "typically fail" its
   rolls (0.70 of rolls win); it fails to take the host.
2. **The failure matrix routes the token away.**
3. **A later port scan** is the only way the attacker sees the next hop: the scan
   reveals the exposed services and the neighbours of compromised ones only
   (`host.py` `port_scan`), and an exploit action's candidates are fixed at its
   start.
4. **Exploit visit 2 takes the host.**

Exploit visits to take a host: **2.52 off, 2.41 memory on (λ = 2), 2.40 with
every roll won**. The memory already captures almost all that better odds can
give; the floor is the hop structure. A multi-visit host takes a median 653 s
from first exploit visit to its fall, against ≈ 34 s per exploit action: the
expensive part is step 2's detour, which the roll cannot shorten.

What an exploit action that runs ends in (≈ 35 per run), memory off: host taken
21 %; opened a service, target a hop further 30 %; host cannot fall by exploit
even winning every roll the OS check allows 26 %; won, no service past 7 12 %;
takeable, won nothing 10 %. A perfect roll leaves "taken" at 22 % and moves the
won-some share into "all refused by the OS check" (21 % → 36 %): won instances
are never re-offered, so the next visit meets only the refused ones.

**Marc's ruling (2026-09-29).** Keep the memory as built (raised odds only), on in
the evaluated model per the 2026-09-28 ruling; no mechanism change before
submission. The four steps are the ablation's and the discussion's account of
why it confers no advantage: the adopted attack phases produce this two-visit
chain, and it persists for as long as the model drives MTDSim's actions
(§4.4.1's ceiling, now measured). §4.4.5 stays method-only.

**Future work (§7.2), with its dry-run evidence.** A memory that acts on the hop:
when a visit opens a service, the attacker uses a vulnerability it recognises on
the next hop within the same visit. Dry run (no extra time charged): hosts
**+3.55 [+2.22, +4.88]**, target reached 14/40 against 9/40, visits per host
1.48, multi-visit fall time 181 s. Chaining on every vulnerability (no memory)
bounds it at +4.85. Not in the evaluated model; it changes how the APT attacker
model uses the exploit action, which §4.4.1 holds identical for both attackers.

**Open, Marc's call: the exploit-shaped dwell's unit.** §4.4.2 anchors it at the
median time of *one* vulnerability attempt (4.5 s), but an exploit action tries
≈ 13 candidates and pays it once (S3-R, commit `8f2e34ad`: one draw per action).
Table C.1 sweeps the family ×0.5–×2 (inert); per-attempt pricing is ≈ ×13 on the
exploit action and costs ≈ 1.2 hosts (9.15 → 7.95; target reached 9/40 → 4/40).
Neither per-attempt pricing nor the pre-S3-R stacking lets the memory act (+0.07,
−0.12 hosts). Session recommendation: keep S3-R, say in §4.4.2 that the dwell
prices one exploit action, add per-attempt pricing as one robustness condition
beside Table C.1, and name it in §6.5's construct paragraph.

**Discrepancy for Part A to settle.** §11.11 found the OS check off adds about two
hosts (CI excluding zero for $c_{\mathrm{agg}}$, $c_4$); this probe finds +0.35
[−0.34, +1.04] on aggregate + exfiltration. Different profiles and a different
wrapper; the tracked runner decides.
