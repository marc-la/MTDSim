---
status: open — design; Marc's rulings owed on the section shape (§2), the heading set (§3) and the disposition of every board item marked FOUNDATION (§6). Feeds ch6 drafting; nothing here is prose.
created: 2026-09-15
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
