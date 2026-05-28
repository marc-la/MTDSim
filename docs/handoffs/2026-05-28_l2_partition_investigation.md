---
status: open
created: 2026-05-28
---

# Decide and justify the L2 (GASP) operational-objective classification — evaluated against the v0.5 GAP

The investigation answers **two coupled questions**:

1. **Is L2 warranted at all?** I.e., does conditioning the GAP on an operational
   objective yield distinguishable downstream behaviour, or can L3 traverse the
   un-classified GAP directly?
2. **If yes, by what classification scheme?** Comparing candidate schemes against
   the v0.4 rubric (canonicity / coverage / distinctiveness / MTD relevance /
   validation), augmented for the v0.5 context.

The deliverable is a **notebook + a notes/-file write-up** that picks (or
refuses) a classification scheme with cited evidence. **No final code lands**
in `src/mtdsim/l2_subgraph/` from this handoff — that is a separate,
post-decision session.

> **Language note (load-bearing).** The original framing used "partition"
> throughout. *That word is wrong.* A partition is a disjoint split (every
> flow in exactly one class); but the v0.5 corpus already shows three flows
> (Conti CISA, Conti PWC, muddy_water) reaching **both** exfiltration and
> impact terminals — double-extortion campaigns where the same operation
> pursues steal_data *and* impediment simultaneously. Forcing those into one
> class destroys the dual-objective signal the corpus visibly carries, and
> mis-frames what real APT campaigns do. STIX's own `attack-motivation-ov`
> supports this: threat-actor / intrusion-set objects carry both
> `primary_motivation` (singular) *and* `secondary_motivations` (plural list).
> Multi-membership is the standards-faithful default; mono-membership is the
> simplification, and the investigation should be explicit about which it
> adopts and why. See §"Multi-membership default" under Goal alignment.

## Goal alignment + investigation authority (read first)

**The handoff is the recommended starting path, not a procedural limit.** This
is named explicitly because prior investigations on `feat/attacker-profiling`
executed their stated method, scored their rubric, produced a recommendation
— *and the recommendation did not survive the GAP rebuild that followed.*
The failure mode to avoid is **shipping a verdict because the steps were
completed, not because confidence was reached.**

**Before opening the notebook, write a one-line goal statement at the top
of the notebook, anchored to the project's stated goal.** The project goal
is *behaviourally-grounded MTD evaluation against CTI-derived attacker
profiles, with the eventual analytical substrate being Petri nets*
([`docs/specs/project_context.md`](../specs/project_context.md)). The
investigation goal that flows from this is something like *"decide which L2
partition produces behaviourally-distinguishable, Petri-net-tractable GASPs
that L3 can defensibly traverse against MTD, with enough confidence that
the verdict survives downstream re-baselines."* Phrase your own version
before you start; it is the steer for every "do I keep going / do I stop"
judgement the investigation hits.

**Authority granted.** The investigation has authority to:

- *Extend* — read sources or run analyses not enumerated in the
  Recommended approach, where the project goal demands it (e.g., a sixth
  candidate partition emerges from the metadata audit and is worth scoring;
  a sub-investigation into one bucket's internal structure is needed
  before the discrimination check is interpretable; a sibling
  branch's commit history needs a deeper read than was done here).
- *Iterate* — return to an earlier step when a later step changes what the
  earlier one should have produced (e.g., the discrimination check at step
  5 reveals the rubric weights at step 4 were wrong; go back, rescore).
  This includes the *rubric itself*: if step 2's metadata audit reveals
  the rubric is measuring the wrong things (e.g., the metadata-attestation
  criterion dominates so heavily that the other six become noise), reweight
  or replace before scoring.
- *Refuse* — decline to ship a "winner" verdict if neither concrete-confidence
  outcome is achievable. An honest *"inconclusive — here is what specifically
  is needed to converge, and why this corpus / substrate can't supply it yet"*
  verdict is gate-passing. A *"least-bad-of-the-five"* verdict
  ungrounded in confidence is **gate-failing** even if the rubric scores
  technically separate the candidates.
- *Sub-investigate* — spin out a sub-handoff under `docs/handoffs/` for any
  sub-question that's larger than a session-scoped detour (e.g., "the
  metadata audit needs an LLM-assisted read of 40 vendor reports — that's
  its own session"). Sub-handoffs are first-class outputs of this
  investigation, not failure modes.
- *Parallelise via batched sub-agents* — when sub-investigations are
  **independent** (no result of one feeds the next), spawn them as
  concurrent Agent calls in a single message rather than serially. Good
  fits: characterising the position_for_future bucket from vendor reports
  *while* scoring Petri-net tractability across all candidates *while*
  cataloguing CTID corpus page descriptions. Poor fits: anything where
  step N depends on step N–1 (rubric scoring, discrimination check,
  verdict-writing — these are serial). The pay-off is wall-clock; the
  cost is that parallel agents don't see each other's intermediate
  results, so synthesis still has to happen serially after the batch
  returns. Use the batched mode where it actually pays.

**Bias-agnostic clause (load-bearing).** The six candidate classification
schemes named in step 3 are a **starting set, not an exhaustive one**, and
the rubric weights are **defaults, not gospel**. The author of this handoff
(current session, Claude Opus 4.7) carries multiple leans visible in
earlier drafts — toward Alshamrani's NIST 3-goal as the "candidate to
beat", toward the metadata-attested variant (P5) as more defensible than
the structural one (P1), toward 3-class cardinality as natural, and
toward structural mechanisms with metadata as cross-check rather than
metadata as the primary mechanism. Marc has expressed a separate lean
toward Alshamrani. **None of those leans should pre-decide the
investigation.** Treat the candidate table as "schemes that were thought
worth considering at handoff-time" not "candidates I'm asked to choose
between." Treat the rubric criteria as "metrics considered worth scoring at
handoff-time" not "metrics that must rank the answer." If step 2's metadata
audit suggests a seventh candidate is more defensible, add it. If the
rubric is the wrong rubric for what the metadata reveals matters, change
it (with the change documented and justified). The verdict belongs to the
evidence the next session gathers, not to the handoff's framing. **A
verdict that matches any of the starting leans is suspect unless the next
session can argue from the evidence that it would have picked that
candidate even without the lean having been named.** A verdict that
*contradicts* the starting leans is correspondingly stronger evidence the
investigation reasoned from the data.

**Stopping rule (positive form).** The investigation is done when one of:

- A candidate classification passes the rubric *and* the discrimination
  check *and* the metadata-attestation check (and the Petri-net
  tractability check, *if* the investigation retained that criterion —
  §"Bias warning on Petri-net tractability"), with the notebook narrative
  explicitly arguing why a future re-baseline would not change the
  verdict. "I'd back this" is the bar.
- Or — no candidate passes the retained checks, *and* the notebook narrative
  defends why the next concrete step is needed (a richer corpus / a
  different substrate / a different evaluation axis) before any
  classification could. "Here is what we need before we can decide" is the
  bar.
- Or — the investigation has run a defended number of iterations (you
  judge "defended") without converging on either of the above, *and* the
  notebook spells out the specific blocker and a pointer to the
  sub-handoff that resolves it. "We hit a wall, here it is, here's the
  next session." That is the failure-mode escape hatch and it is honest
  by design.

**Anti-creep clause.** Extension authority is *goal-anchored*, not curiosity-
driven. Every extension beyond the Recommended approach should be
justifiable in one sentence as *"this is needed because [the project goal]
requires it."* If the justification is *"because it's interesting,"* defer
it to a notes file and move on. Past failure mode: investigations that
wandered into CTI-taxonomy theory while the partition decision sat
unstarted. Don't.

**Document the path, not just the destination.** The verdict notes file
should show what was investigated, what got ruled out and why, where the
investigation iterated (and what triggered it), and what the next session
would need to do *to disagree with the verdict from a stronger position*.
The audit trail is itself part of "concrete confidence" — a verdict the
reader can't trace back to evidence is not one you can defend later.

**Multi-membership default (consequence of the language note above).** Treat
flows as carrying **0+ operational-objective memberships**, not exactly one.
Every candidate classification scheme should be specified as a function
*flow → set[class]*, not *flow → class*. A double-extortion ransomware
campaign that reaches both exfiltration and impact terminals carries both
`steal_data` and `impediment` memberships; that is the corpus-faithful
representation, not a problem to be normalised away. The corollary GASPs
overlap by construction — a technique appearing in two membership classes'
ancestor cones lives in both GASPs — which is **expected and not a bug**.

Three knock-on consequences the investigation has to think through, not
hand-wave:

- *Rubric scoring breaks under overlap.* The "Balance" criterion (coefficient
  of variation on class sizes) is less meaningful when classes overlap; the
  "Distinctiveness" criterion (pairwise Jaccard) is too — overlap is no
  longer a bug, so low Jaccard isn't automatically high distinctiveness. The
  investigation should either reweight these criteria or replace them with
  multi-membership-aware analogues (e.g., *"what fraction of flows are
  mono-class vs multi-class? if multi-class is a major mode, the scheme is
  saying something interesting about compound objectives; if it's a long
  tail, mono-class is the operative behaviour."*).
- *Discrimination check has to handle the overlap.* A flow contributing to
  multiple class-averages dilutes per-class behavioural signatures. Two
  honest options: (a) weight a flow's contribution by 1/|memberships|, or
  (b) for discrimination only, run the check on mono-class flows separately
  from multi-class flows, treating each multi-class combination as its own
  effective class. Either is defensible; pick one with a stated reason.
- *Compound-classes are a real alternative to multi-membership.* If most
  multi-class cases cluster around a small number of recognisable compound
  objectives — double-extortion ransomware being the obvious one — the
  better abstraction may be **a finer disjoint taxonomy that names compound
  classes** (`{pure_steal, pure_impediment, double_extortion,
  pure_surveillance, infrastructure_only}`) rather than multi-membership
  over the original three. That trades more classes for restored
  disjointness. The investigation should **evaluate this as an explicit
  alternative, not assume multi-membership is the only fix.** This becomes
  candidate P6 if pursued.

## State of play

### Why L2 is on the docket now

Pipeline status: L1 (GAP v0.5) is built and lossless on this branch; L2
(`src/mtdsim/l2_subgraph/`) is a stub (README + `__init__` only,
[`src/mtdsim/l2_subgraph/README.md`](../../src/mtdsim/l2_subgraph/README.md));
L3/L4 are seam pointers. The pipeline can't be exercised end-to-end until L2
exists, and the **shape** of L2 is a design choice that bounds what L3 can do
and what L4 can claim.

### What's already known (so the next session doesn't re-derive)

**Three independent arguments converge on "L2 is warranted":**

1. *Lit-review framing.* The RQ is explicitly two-axis — SDR-family × *"profiles
   differentiated by operational objective (Section III-C) — the dimension
   along which APT campaigns vary, and which parametric models collapse"*
   ([`docs/sources/LIT_REVIEW.md:233`](../sources/LIT_REVIEW.md#L233)). Without
   L2, the profile axis collapses to a single cell and the RQ is no longer
   comparative.

2. *Fidelity-ladder definition.* The lit review's behavioural rung is defined
   as *"campaign-level intent, motivation conditioning, and learning
   capability"* ([`LIT_REVIEW.md:175`](../sources/LIT_REVIEW.md#L175)).
   Motivation conditioning **is** L2. No L2 → the work sits at Procedural,
   weakening §IV-B's claim to operate at the rung MTD targets.

3. *Empirical structure in the v0.5 corpus.* The GAP construction note already
   records the structural finding: *"of 40 flows, 13 reach exfiltration, 13
   reach impact, but only 3 reach both — campaigns commit to one terminal
   objective, exactly the 'stages 4–5 split by objective' structure"*
   ([`docs/notes/2026-05-27_gap_construction.md`:110-115](../notes/2026-05-27_gap_construction.md#L110)).
   Re-computed at terminal-action granularity (i.e. action with zero
   out-degree in its per-flow extract) on the canonical v0.5 GAP:

   | Bucket (Alshamrani 3-way, structural mapping) | n / 40 | % |
   |---|---:|---:|
   | `steal_data` — terminal in `exfiltration` | 11 | 28% |
   | `impediment` — terminal in `impact` only | 7 | 18% |
   | `position_for_future` (or unobserved suffix) | 22 | 55% |
   | (overlap: exfil ∩ impact) | 3 | 8% |

   Lopsided toward "position_for_future" — but that bucket is **conflated with
   observability bias** (incident reports that stop at the documented intrusion
   without reaching the published terminal). The 11:7 split on the
   observably-completed flows is the cleaner signal and is the empirical
   warrant for splitting at the terminal tactic.

**Why the candidate set in step 3 looks like it does** (informational — not a
ranking; see §"Bias-agnostic clause"):

- *Alshamrani-NIST 3-class candidates (P1, P5) exist because* Alshamrani §II-C
  derives stages 3–5 conditioning from NIST SP 800-39's three APT goals —
  *Steal Organization Data* / *Undermine Organization's Critical Aspects* /
  *Position for Future*
  ([`docs/extractions/alshamrani2019.md:54`](../extractions/alshamrani2019.md#L54);
  source verbatim at [`docs/sources/2_3_alshamrani2019survey.md:85`](../sources/2_3_alshamrani2019survey.md#L85))
  — i.e., a peer-reviewed survey ties an explicit 3-way taxonomy to a NIST
  document on the strength of a documented structural argument. Whether the
  3-class cardinality is *right* for this corpus is what the investigation
  has to decide; that the candidate is *present* in the starting set is just
  "literature exists here." It is not a recommendation.
- *Terminal-technique / group-witnessed candidates (P2, P3) exist because*
  v0.4 prior art on `feat/replay-viz` implemented and scored both, and
  carrying their performance forward to v0.5 is cheaper than re-deriving the
  alternative.
- *Reduced STIX-motivation candidate (P4) exists because* Marc hand-labelled
  47 campaigns in the 2026-04-16 motivation notebook against the STIX
  `attack-motivation-ov` vocabulary, so this candidate carries already-done
  manual analyst labour. The labels happened to collapse onto 3 of the 10
  STIX categories with a 31:9:7 split, which is informational about the
  vocabulary's effective cardinality on this corpus, not a vote for any
  cardinality being correct.
- *Compound-class candidate (P6) exists because* the multi-membership default
  (§"Multi-membership default") makes compound classes a structurally
  natural alternative; the investigation may need it.

There is no "candidate to beat" here at handoff-time. The empirical
discrimination check and the metadata audit are what produce a winner —
neither is run yet.

**Three taxonomies are demonstrably dead-ends for L2 classification** (do not
re-run these — the evidence is recorded):

- *STIX `primary_motivation` field as the key.* 0 / 187 groups and 0 / 52
  campaigns populate it (2026-04-16 motivation notebook on
  `origin/feat/replay-viz:notebooks/2026-04-16_MTDSim_ATTACKMotivationExploration.ipynb`,
  Part 1 — read via `git show`). Adopting it commits to per-campaign manual
  labelling against an unpopulated field.
- *STIX `attack-motivation-ov` (10-cat vocab) as the key.* Spreads thin: 47
  campaigns labelled by hand from external CTI collapse onto 3 of the 10
  categories with a 31:9:7 (organizational-gain : personal-financial-gain :
  dominance) split. The 7 unused categories give nothing on this corpus —
  the *active* cardinality is 3 (P4 carries this collapsed form). The 10-cat
  vocab itself is a dead-end as a partition key; whether the 3 active
  categories are a defensible classification is what P4 has to decide.
- *Entry-node anchoring.* T1566 (spear-phishing) alone reaches ~49% of v0.4
  GAP nodes → lopsided 1-to-many partition with one dominant bucket
  (2026-04-17 GAPSubgraphExploration notebook, Candidate C). Same property
  expected to hold on v0.5.

**Selector prior art** lives on `feat/attacker-profiling` /
`feat/replay-viz` (same blob hashes for the selector modules; the latter
has 9 extra commits adding notebooks). The four implemented selectors are:

| Module (v0.4) | Strategy | Rubric (in 2026-04-17 nb) | Status against current question |
|---|---|---:|---|
| `selectors/terminal.py` | Terminal-objective ancestor cone | 21–22/30 | Closest existing analogue — needs **re-labelling** to NIST 3-goal classes |
| `selectors/platform.py` | Platform bucket | 23/30 | **Orthogonal axis** — defender-posture partition, not motivation |
| `selectors/terminal_constrained.py` | Group-witnessed terminal | 22/30 | Tightens A by requiring group co-occurrence — keep as candidate |
| `selectors/base.py` | `ancestor_subgraph()` helper | — | Reuse pattern, not literal port (per zero-trust stance) |

**Discrimination evidence at proof-of-concept scale** (v0.4): two terminal-cone
GASPs — T1486 (ransomware) vs T1567 (cloud exfil) — on identical network +
scalar params produced measurably different technique-level and tactic-level
traces under the simulator (2026-04-22 GAPSubgraphAttackerDemo notebook).
*Read this narrowly.* The pair is essentially the most-different two
terminals you could pick — different parent tactics, different platforms,
different objectives. That such a pair separates is necessary but not
sufficient for any candidate's discrimination claim. **Specifically, it does
not warrant assuming coarsened classifications discriminate**: when P1
folds T1486 and (say) T1485 both into `impediment` and asks whether
`impediment` separates from `steal_data`, that's a different empirical
question and has to be re-run, not inherited. The same caveat applies to
any other coarsening candidate.

**Petri-net consideration downstream — handle with care**
(`origin/feat/replay-viz:notebooks/2026-05-02_MTDSim_PetriNetPrimer.ipynb` —
read via `git show`). The SNAKES-formalisation primer uses
`TerminalObjectiveSelector(technique='T1486')` as its exemplar GASP and
articulates: bounded reachability is the reason a partition makes the Petri
encoding tractable — a GASP-shaped subgraph yields a tractable CTMC state
space for analytical MTTC / ASR computation; the un-partitioned GAP does
not. *However*, the architecture explicitly positions Petri nets as a
*candidate alternative* analytical substrate at L4, **not** as a step
inside L1/L2 ([`architecture.md`](../specs/architecture.md) §(f): *"Architecturally,
a Petri-net encoding of GASP would sit parallel to MTDSim/DES execution as
an alternative substrate for L4 analytical evaluation — not inside L1/L2."*).
The primary L3 path is graph-driven traversal inside MTDSim/DES, where
"tractability" means "the simulator runs," not "the reachability graph
fits."

**Bias warning on Petri-net tractability as a rubric criterion.** The
handoff includes "Petri-net tractability" as criterion #6 because the
primer makes the constraint concrete, but the investigation should
**check whether that criterion deserves the weight it carries** before
scoring. If the Petri-net substrate is *parallel* rather than *primary*
at L4, then a classification scheme that fails Petri-net tractability but
passes the primary-substrate (DES) check may still be the right answer,
with Petri-net encoding deferred to the cases it fits. Re-weight or drop
the criterion if §(f)'s positioning persuades you it is over-weighted here.

### What's not yet known (this investigation is to settle)

- Whether the v0.5 GAP's per-bucket sizes (under Alshamrani 3-way or
  alternatives) are usable, or whether `position_for_future` is so dominated
  by observability bias that the partition is effectively binary on what
  remains.
- Whether the v0.4 demo's behavioural-discrimination finding (T1486 vs T1567
  produce different traces) survives the re-labelling to NIST 3-goal classes
  on the v0.5 GAP — i.e. does coarsening 30 terminals into 3 classes preserve
  the discrimination, or does bucket-averaging wash it out?
- Whether any partition produces tractable Petri-net encodings across **all**
  buckets, or whether one bucket (e.g. impediment) is too sparse / fragmented
  to encode usefully.
- Whether the v0.4 rubric's MTD-relevance and validation criteria are still
  the right adjudicators against the v0.5 substrate, or whether new criteria
  (e.g. Petri-net tractability bound) need to be added.
- **What metadata beyond the STIX bundle the Attack Flow corpus carries**
  per flow, how reliably it states each flow's operational objective, and
  whether that metadata changes any of the bucket assignments a purely-
  structural mechanism (terminal-tactic) would produce. Two separate
  motivations for digging here: (a) it cross-checks P1's structural mapping
  against analyst-stated intent, raising or lowering confidence in the
  partition independently of the rubric; (b) it is the principal lever for
  disambiguating the `position_for_future` bucket, which a structural
  mechanism cannot tell apart from a truncated incident report. **This is
  the load-bearing addition vs the original handoff scope** — without it,
  the Alshamrani 3-way's largest bucket is ungrounded.

## Recommended approach

A single **investigation notebook** under `notebooks/`, dated
`YYYY-MM-DD_MTDSim_L2PartitionInvestigation.ipynb`, that runs the comparison
end-to-end against the v0.5 GAP and writes a notes file with the verdict.
**Do not modify `src/mtdsim/l2_subgraph/`** — the package stays a stub until
this investigation lands a recommendation Marc signs off on.

### Notebook structure (suggested — adjust as findings dictate)

1. **Load** `data/gap/gap_v0.5.json` and the 40 per-flow YAML extracts under
   `data/gap/flows/`.

2. **Audit non-STIX metadata across the 40 flows.** The per-flow YAMLs already
   carry richer metadata than the aggregate GAP consumes; the CTID corpus
   site and the referenced vendor reports carry more still. The aim of this
   step is to produce a 40-row reference table that grounds (or falsifies)
   the structural classification before any partition mechanism is chosen.

   Sources to inventory, in order of cheapness:

   - **Per-flow YAML fields already in-tree** (`data/gap/flows/<id>.yaml`):
     `flow_name` (often objective-bearing — *"Black Basta Ransomware"*,
     *"Equifax Breach"*, *"Operation Dust Storm"*); `scope`
     (incident / campaign / threat-actor — informs how representative one
     flow is of a wider operation); `references[]` (vendor URL + description
     — the link to authoritative narrative); per-action `name` fields
     (often domain-suggestive even when tactic is generic).
   - **CTID corpus page descriptions** at
     `https://center-for-threat-informed-defense.github.io/attack-flow/corpus/` —
     CTID curators write short blurbs per flow that don't round-trip into
     the STIX bundle. Mirror once into a notebook-local cache; don't re-fetch.
   - **ATT&CK attribution where present** — a flow whose name maps to an
     ATT&CK Group or Campaign (e.g. `solarwinds` → C0024 → APT29 / G0016)
     inherits the group/campaign description, which sometimes states
     objective even when STIX `primary_motivation` is empty.
   - **Vendor report executive summaries** (referenced via `references[]`) —
     manual read of ~40 short summaries is bounded analyst effort and the
     most authoritative source; an LLM-assisted pass on the URLs is the
     scalable alternative. **Don't over-engineer** — read the executive
     summary only; full report comprehension is out of scope.

   Deliverable: a notebook table indexed by `flow_id` with columns
   `flow_name`, `scope`, `n_actions`, `terminal_tactic` (computed),
   `stated_objective` (from sources above, in plain language),
   `attribution` (group / campaign / unknown), `metadata_confidence`
   (high / medium / low — how confidently the operational objective can be
   stated from the available metadata). The `stated_objective` column is
   the ground-truth lens against which P1 (and any other structural
   partition) is cross-checked in step 4.

   Two patterns are worth looking for explicitly, since they directly affect
   how *any* terminal-tactic-based scheme (P1, P5, P6, and any added in
   step 3) interprets the corpus:

   - **Disambiguating "no observable exfil-or-impact terminal" flows** — for
     each flow whose terminal action is *not* in exfiltration or impact,
     does the vendor report describe it as (a) genuine surveillance /
     pre-positioning, (b) an incident truncated before exfiltration / impact,
     (c) ransomware-as-a-service infrastructure setup that never reached the
     victim payload, or (d) something else? The mix of these is what makes
     the residual class interpretable (or reveals it isn't).
   - **Catching structural mis-classifications** — flows whose vendor-stated
     objective is clearly *exfiltration* or *impact* but whose terminal
     action sits elsewhere (because the report stopped before the analyst
     drew the terminal node). These are the cases where any structural
     mechanism under-credits its target classes and over-credits the
     residual. Produce a count; if it is large, structural-only candidates
     should be down-weighted on the metadata-attestation criterion.

3. **Implement candidate classification schemes** — fresh, in-notebook, not
   ported. Each scheme yields a function *flow → set[class_name]* over the
   per-flow extracts (multi-membership default, §"Multi-membership default"
   — flows with both exfil and impact terminals get both `steal_data` and
   `impediment` memberships, not one or the other). From that, derive
   `{class_name: set[flow_ids]}` (with flows appearing in multiple class
   sets where memberships overlap), and `{class_name: SubgraphView-like}`
   from the aggregate GAP (induced subgraph of each class's ancestor cone
   — these subgraphs overlap by construction where memberships overlap).

   *Starting set, not exhaustive (see §Goal alignment "Bias-agnostic
   clause"). Score these; add a P6 / P7 / … if the metadata audit suggests
   one is more defensible than these five; remove any of these if you can
   argue the mechanism is incoherent on the v0.5 corpus.*

   | # | Candidate | Mechanic |
   |---|---|---|
   | P1 | **Alshamrani-NIST 3-class — structural** | Tag each flow with one membership per terminal-action tactic it carries: `exfiltration ∈ terminals → steal_data`; `impact ∈ terminals → impediment`; otherwise → `position_for_future`. A flow with both exfil and impact terminals carries both `steal_data` and `impediment`. Class GASP = ancestor cone of the class's terminal techniques. *Purely structural — no metadata.* |
   | P2 | **Terminal-technique** (v0.4 baseline) | One class per objective technique (`gap.objective_nodes`, 15 classes in v0.5). A flow with multiple objective-technique terminals carries multiple memberships. Class GASP = single-objective ancestor cone. The "fragmentation control" against which P1's coarsening earns its keep — or fails to. |
   | P3 | **Group-witnessed terminal** (v0.4 best by rubric) | P2 restricted to ancestors that co-occur in ≥1 ATT&CK group with the terminal. Requires loading ATT&CK group→technique mappings (already available in the build via `attack_stix.py`). Multi-membership rules inherit from P2. |
   | P4 | **Reduced STIX-motivation 3-cat** | Tag each *flow* (not technique) using Marc's 47-campaign hand-labels onto `{organizational-gain, personal-financial-gain, dominance}`. The 2026-04-16 notebook captured these as primary labels; the multi-membership extension assigns secondary labels when the vendor evidence supports more than one (some flows have no ATT&CK Campaign ID at all — those are explicitly tagged `unknown`, not silently dropped). Labelling file: 2026-04-16 motivation notebook (Part 4) on `feat/replay-viz`. |
   | P5 | **Alshamrani-NIST 3-class — metadata-attested** | Same 3-class structure as P1, but each flow's memberships are sourced from the step-2 `stated_objective` column when `metadata_confidence` is high or medium; falls back to P1's structural mapping only when metadata is silent. Disambiguates the `position_for_future` class into *genuine* (vendor report names surveillance / pre-positioning), *truncated* (report stopped before exfil / impact — re-assign to the inferable membership), or *kept-as-unknown* if neither resolves. Multi-membership emerges naturally where reports cite multiple objectives (e.g. Conti = steal_data + impediment from the report's own narrative). Produced only after step 2; emerges from it. |
   | P6 | **Compound-class disjoint taxonomy** (alternative to multi-membership) | A finer disjoint classification that names compound objectives explicitly: e.g. `{pure_steal, pure_impediment, double_extortion, pure_surveillance, infrastructure_only, unknown}`. Each flow gets exactly one class. Trades more classes (and lower per-class sample size) for restored disjointness, which simplifies rubric scoring and L4 evaluation. Produced **only if** the multi-membership analyses in P1/P5 reveal that multi-class cases cluster around a small number of recognisable compound objectives rather than scattering; otherwise this scheme has no empirical basis and should be skipped with a one-line explanation. |

   *Don't* re-run motivation, entry-node, Louvain, or tactic-clustering
   experiments — they have documented negative findings (see *Out of scope*).

4. **Score each partition on the rubric** (carry the 5 criteria from the
   2026-04-17 notebook + **add a sixth, Petri-net tractability**, and a
   **seventh, metadata-attestation**):

   - *Canonicity* (0–5) — is the partition key MITRE-/standards-canonical?
   - *Coverage* (0–5) — fraction of GAP nodes/edges represented across buckets
     (no bucket dropping techniques the lit review claims to model).
   - *Distinctiveness* (0–5) — mean / median pairwise Jaccard overlap on the
     per-bucket technique sets; lower is more distinct. Report distribution
     not just mean.
   - *Balance* (0–5) — coefficient of variation of bucket sizes; a partition
     with one bucket holding 80% of techniques scores low. Use IQR / CV.
   - *Validation path* (0–5) — can the bucket assignment be defended without
     analyst inference? (P1 = high: structural; P4 = low: hand-labelled.)
   - **NEW** *Petri-net tractability* (0–5) — per-bucket node count + edge
     count vs the primer's stated tractability bounds (~14 places, low-tens
     of transitions). Buckets that exceed need to demonstrate analytical
     encoding remains feasible.
   - **NEW** *Metadata attestation* (0–5) — fraction of bucket assignments
     that the step-2 audit's `stated_objective` column corroborates (high
     attestation = partition is grounded in analyst-stated intent, not just
     structural shape). This is the rubric column that distinguishes a
     defensible structural partition (P1 corroborated by metadata) from a
     plausible-but-ungrounded one (P1 with no metadata cross-check).

5. **Pick the top two partitions on the rubric** and run the **discrimination
   check** the 2026-04-22 demo established:
   - For each top candidate's buckets, build a `SubgraphAttackerProfile`-style
     wrapper *in the notebook* (do not port the v0.4 wrapper).
   - Run the simulator across (bucket × at-least-2-MTD-schemes × 3 seeds),
     report MTTC / ASR / technique-frequency per bucket.
   - **Discrimination is the load-bearing finding**: if buckets within a
     partition don't produce distinguishably different simulator traces, that
     partition has failed regardless of rubric score.

6. **Sketch Petri-net encoding** for one bucket from the winner:
   - Reuse the primer's place=tactic / transition=GAP-edge mapping.
   - Report per-bucket reachability set size and confirm CTMC construction
     remains feasible.
   - **Not** a full SNAKES implementation — a sketch that confirms or
     falsifies the tractability claim.

7. **Write the verdict** as
   `docs/notes/YYYY-MM-DD_l2_partition_decision.md`:
   - Which partition (or none).
   - Rubric scores, discrimination evidence, Petri-net tractability check.
   - The `If revisited:` line stating what would change the decision.
   - A pointer for the *next* session to take the verdict into
     `src/mtdsim/l2_subgraph/` as the implementation step.

### Alternatives considered (don't take them — recorded so the next session disagrees from a shortlist, not from scratch)

- *Skip the investigation; port the v0.4 `TerminalObjectiveSelector`
  directly.* Rejected: re-runs the same partition the 2026-04-17 notebook
  already scored 21–22/30 on v0.4, with no re-evaluation against the v0.5
  (Enterprise-only, lossless) GAP and no coarsening to a NIST-defensible
  3-way. Skips the standards-grounding move that turns the partition from
  "structural surrogate" into "Alshamrani-anchored category".
- *Try a richer motivation-attribution method (NLP / LLM on group
  descriptions).* Rejected for now: the 2026-04-16 notebook already showed
  keyword extraction has F1 0.47; an NLP/LLM pipeline is doable but the
  payoff (labelling 47 campaigns against an unpopulated STIX field) is
  bounded — and even if it succeeded, the labels collapse onto 3 categories.
  Defer to a separate workstream if P4 (reduced STIX 3-cat) turns out to be
  the winner *and* the manual labels are the limiting factor.
- *Take the corpus partition Marc has already started (the 2026-04-16
  motivation notebook's external CTI labels) as a candidate without
  re-deriving.* Worth doing — that's P4 above. (The earlier version of this
  bullet said "don't add a sixth"; P6 has since been added as a structurally-
  motivated compound-class candidate. Adding further candidates beyond P1–P6
  remains in the investigation's authority per §"Bias-agnostic clause".)
- *Decide a partition by inspection of the v0.5 GAP visualisation, skip the
  experiment.* Rejected: looking at the graph cannot establish behavioural
  discrimination, which is the load-bearing finding. The rubric is necessary
  but not sufficient.

## Validation gate

The investigation is **done** when:

1. The notebook produces a **40-row metadata audit table** (step 2 deliverable)
   covering every flow with `flow_name`, `scope`, `terminal_tactic`,
   `stated_objective`, `attribution`, `metadata_confidence` — and the
   `stated_objective` column is filled for at least 80% of flows at medium
   or high confidence. The remaining 20% are explicitly listed as "metadata
   silent" with a one-line reason each. This table is committed alongside
   the notebook (CSV or markdown table) so the next session can audit the
   labelling without re-running.
2. The notebook executes end-to-end against `data/gap/gap_v0.5.json` and
   produces, for each candidate classification scheme that survives step 3
   (the starting set is six; the investigation may add or remove with
   justification):
   - A complete class-membership assignment (every flow has ≥1 membership
     under the scheme, *or* is in an explicit `unknown` class the scheme
     declares — silent drops are a gate-fail). Multi-membership is allowed
     and expected per §"Multi-membership default"; disjoint schemes (P6,
     P4's primary-label variant) should report this in their assignment
     metadata.
   - Numerical scores against the 7-criterion rubric (the 5 from 2026-04-17
     + Petri-net tractability + metadata-attestation), with criterion
     re-weighting / replacement justified inline if step 2 motivates it.
   - A class-by-class size table (n flows, n techniques, n edges, % of GAP),
     with a separate column noting mono-class vs multi-class counts.
3. For the top-2 partitions on the rubric, simulator runs across
   (bucket × ≥2 MTD schemes × ≥3 seeds) report MTTC and ASR per bucket, with
   a clear *discriminates / does not discriminate* verdict per partition.
4. *Conditional, only if the investigation retains Petri-net tractability
   as a load-bearing rubric criterion (see §"Bias warning on Petri-net
   tractability" — re-weighting or dropping it is in scope).* For the
   winning scheme, one class's reachability-set size is computed and
   confirmed to fit the primer's tractability bounds (or shown to exceed
   them, with a documented mitigation). If the investigation drops the
   criterion as over-weighted, this gate item is replaced with a
   one-paragraph justification of the drop, citing
   [`architecture.md`](../specs/architecture.md) §(f).
5. `docs/notes/YYYY-MM-DD_l2_partition_decision.md` exists with: the verdict,
   the rubric table, the metadata-audit summary, the discrimination evidence,
   the Petri-net tractability check, the `If revisited:` line. For *any*
   winning scheme that has a "residual" or "other" or "position_for_future"
   class — i.e. a class defined by what it's *not* rather than by what it
   *is* — an explicit breakdown of what's in that class (genuine /
   truncated / unknown counts, with one citation per genuine instance to
   its vendor report). A residual class that isn't unpacked is a
   gate-fail.
6. This handoff (`2026-05-28_l2_partition_investigation.md`) is **deleted
   in the same commit** that ships the notebook + notes file (per
   [`session_workflow.md`:32-35](../specs/session_workflow.md#L32) handoff
   lifecycle).

A *negative* result is also a valid gate-pass: if no partition discriminates,
the notes file records that and recommends the alternative (`L2 collapses to
the un-partitioned GAP — the contribution lives at L1; revisit if a richer
corpus changes the discrimination signal`).

An *inconclusive* result is **also** a valid gate-pass, per the stopping
rule's third clause — but only with the documented blocker + sub-handoff
pointer the §"Goal alignment" section requires. "We're not sure" without
naming what would resolve the uncertainty is gate-failing; "we're not sure,
here's the specific information / corpus / substrate change that would
resolve it, here's the sub-handoff that pursues it" is gate-passing.

## Hard constraints

- **Branch hygiene.** Work on `feat/l2-partition-investigation` (already cut
  and pushed; this handoff lives there). Per
  [`guardrails.md`](../specs/guardrails.md): never on `main`, never push
  without an explicit ask.
- **Zero-trust against prior code.** The v0.4 selector implementations on
  `feat/attacker-profiling` / `feat/replay-viz` are *inspiration only* — do
  not import or copy them into the notebook. The notebook implements the four
  partition mechanisms fresh, justified against the v0.5 spec.
- **Source markdown is authoritative.** When citing literature, cite the
  [`docs/extractions/*.md`](../extractions/) files (Alshamrani, Ferraz,
  Rodríguez) — do not chase external URLs for non-peer-reviewed material when
  the extraction is the source of record.
- **No final code in `src/mtdsim/l2_subgraph/`.** The package stays a stub
  until this investigation lands a recommendation. The notebook is the
  decision artefact; implementation is the *next* handoff after Marc reviews.
- **GAP is the only data input.** Do not re-run L1 (`gap_v0.5.json` is the
  pinned artefact for this investigation). If the GAP changes mid-session,
  flag and pause.
- **Determinism.** Notebook seeds for the simulator runs are fixed and
  reported; re-running the notebook reproduces the same bucket assignments
  and the same simulator traces.
- **Don't action out-of-scope findings.** If the investigation surfaces
  observations about L1 (the GAP) or L3 (the substrate seam), record them as
  a follow-up handoff or a notes file — do not modify either.

## Reading list

In order, before touching the notebook:

1. **[`docs/specs/architecture.md`](../specs/architecture.md) §(e)** — the
   L2 GASP spec block (motivation specifier, terminal-node-ancestor proxy,
   the *"if comparative pass shows motivation-by-attribution matters more
   than motivation-by-terminal-node, swap in the NLP path"* revisit clause).
2. **[`docs/specs/01_gap_schema.md`](../specs/01_gap_schema.md)** — the v0.5
   GAP data model (so the notebook reads `TechniqueNode` / `DependencyEdge` /
   `Occurrence` correctly) + the §(e) views section (the existing
   `support_filter` / `acyclic_projection` views are the API L2 consumes from).
3. **[`docs/notes/2026-05-27_gap_construction.md`](../notes/2026-05-27_gap_construction.md)
   §"What the assembled graph looks like" + §"The observability boundary"** —
   the empirical structure of the v0.5 GAP and *why* the position-for-future
   bucket is conflated with observability bias.
4. **[`docs/extractions/alshamrani2019.md`](../extractions/alshamrani2019.md)
   §"Five-phase APT lifecycle"** — the load-bearing claim that stages 3–5
   are objective-conditioned; the NIST 3-goal source for P1.
5. **`docs/sources/LIT_REVIEW.md` §III-C, §III-D, §IV-B, §V-B**
   ([line 120 onwards](../sources/LIT_REVIEW.md#L120)) — the RQ framing, the
   behavioural rung definition, the two-axis (SDR × operational-objective)
   structure.

Optional but useful (skim if unfamiliar):

- **The v0.4 partition exploration**, viewable via
  `git show origin/feat/replay-viz:notebooks/2026-04-17_MTDSim_GAPSubgraphExploration.ipynb`
  (the 5-criterion rubric design + the 6 candidate evaluations).
- **The v0.4 demo**, viewable via
  `git show origin/feat/replay-viz:notebooks/2026-04-22_MTDSim_GAPSubgraphAttackerDemo.ipynb`
  (the discrimination check pattern this investigation reuses).
- **The Petri-net primer**, viewable via
  `git show origin/feat/replay-viz:notebooks/2026-05-02_MTDSim_PetriNetPrimer.ipynb`
  (the tractability bounds the 6th rubric criterion uses).

## Out of scope (explicitly)

The investigation is *not* asking for:

- **A motivation NLP/LLM pipeline as a partition-deciding method.** The
  2026-04-16 notebook already showed keyword extraction is poor (F1 0.47);
  an NLP/LLM pass *as a partition mechanism* is a separate workstream if P4
  wins *and* hand-labels are the limiting factor. Don't run it pre-emptively
  for that purpose. **However**, LLM-assisted reading of the ~40 vendor
  reports during step 2's metadata audit is a tooling choice, not a research
  escalation — use whichever read-mechanism gets the `stated_objective`
  column populated reliably within session bounds, including LLM-assisted
  summarisation if manual reads exceed the time budget. The line is:
  *deciding the partition* with NLP/LLM = out of scope; *populating the
  metadata audit* with NLP/LLM = in scope as tooling.
- **Re-evaluating Candidates C (entry-node) / D (tactic-clustering) /
  E (Louvain) / F (raw STIX `primary_motivation`)** from the 2026-04-17
  notebook. All four have recorded negative findings; re-running them is
  re-deriving rejected hypotheses.
- **A full SNAKES Petri-net implementation.** A reachability-size sketch
  confirms (or falsifies) tractability — that's the criterion. Full
  implementation is a separate workstream after the partition decision.
- **Modifying the GAP** (`src/mtdsim/l1_construction/`,
  `data/gap/gap_v0.5.json`, the per-flow extracts) to "fix" anything the
  investigation surfaces. Record findings as a follow-up handoff.
- **Modifying `mtdnetwork/` substrate** to plug the chosen partition into L3.
  That is the *next* handoff after this one's verdict lands.
- **Touching `feat/attacker-profiling` / `feat/replay-viz`.** Those branches
  hold the v0.4 prior art; do not commit to them.
- **Cross-flow AND/OR reconciliation** ([`01_gap_schema.md`](../specs/01_gap_schema.md)
  §(h) Q1). The aggregate edge metadata preserves the operator data; how it
  reconciles at the Petri-net step is itself a separate question.
- **An exact partition cardinality target.** There is *no* pre-decided
  preferred number of classes. Two bounds apply but neither sets a target:
  (a) the *upper* bound is roughly L4 evaluation tractability (an
  experiment matrix of SDR-family × C classes × MTD-interval grows linearly
  in C and is bounded by simulator time — but the architecture's L4 matrix
  shape is itself open at [`architecture.md`](../specs/architecture.md)
  §(l) Q6, so don't over-pin); (b) the per-class Petri-net tractability
  bound from the primer is a *per-class* constraint, not a count constraint.
  P2's 15-class scheme is included precisely so an investigation that finds
  fewer classes wash out discrimination has somewhere to escalate;
  classifications larger than P2 would need their own justification but
  aren't categorically out of scope.

---

*Author's note (current session, 2026-05-28). What follows is a
candidate-by-candidate risk summary — explicitly **not** a recommendation.
The point is to give the next session a per-candidate falsification
checklist so the rubric scoring doesn't run on autopilot. Per the
bias-agnostic clause, any of the six candidates can win, and an unranked
seventh that emerges from step 2's metadata audit can win over all of them.*

*Risk surface per candidate:*

- **P1 (Alshamrani-NIST 3-class, structural).** Risks: (a) bucket-averaging
  may wash out discrimination — the 2026-04-22 demo separated T1486 vs T1567
  but those are the most-different pair; the coarsening folds many terminals
  into one class and the discrimination claim has to be re-run. (b) The
  residual class (`position_for_future`, structurally) is 55% of the corpus
  and conflates genuine surveillance, truncated reports, infrastructure
  setups, and undrawn-suffix flows — without metadata you cannot tell them
  apart. (c) NIST SP 800-39's authority is risk-management vocabulary, not
  adversary-behaviour taxonomy; the standards-grounded framing buys
  defensibility, not natural-kind status. (d) The 11:7:22 raw split is
  lopsided enough that even with the residual unpacked, the scheme may
  collapse to binary (steal_data vs impediment) on the observably-completed
  flows — re-framing the contribution.
- **P2 (Terminal-technique, 15 classes).** Risks: (a) many classes are tiny
  (n<3 on v0.4 corpus); per-class sample sizes may be too small for the
  discrimination check to separate signal from noise. (b) "What this scheme
  means" is harder to defend at L4 — "MTD X is best against T1486 attackers"
  is a narrow claim, hard to generalise. (c) Multi-membership inherits
  cleanly but most flows still have ≤2 terminals, so the multi-membership
  dimension may be under-exercised.
- **P3 (Group-witnessed terminal).** Risks: (a) v0.4 rubric advantage (22/30
  vs P2's 21/30) was *marginal*; whether it survives v0.5 (smaller
  Enterprise-scoped GAP, different group attribution density) is empirically
  open. (b) Depends on ATT&CK group→technique mappings being well-populated,
  which may be sparser than v0.4 assumed. (c) Inherits P2's small-class risk.
- **P4 (Reduced STIX 3-cat).** Risks: (a) hand-labels exist only for
  ATT&CK-Campaign-attributed flows (≤47 of 187 groups; the 40 Attack Flow
  corpus flows have partial overlap, not 1:1); coverage on the v0.5 corpus
  may be much less than 100% even before extension. (b) STIX
  `attack-motivation-ov` is a vocabulary about *actors*, not about
  *operations* — assigning it to a per-incident flow inherits an actor-level
  attribution that may not apply to a specific operation (an espionage group
  can run a financially-motivated operation). (c) The 31:9:7 distribution
  is lopsided enough to risk the same "effectively binary" collapse as P1.
- **P5 (Alshamrani 3-class, metadata-attested).** Risks: (a) the
  metadata-attestation criterion *can be gamed* by the labelling process —
  if the same person populates `stated_objective` and assigns the class,
  attestation is circular. The audit's `stated_objective` column must be
  populated before the classification is computed, and the labelling must
  be reproducible from the cited evidence. (b) Vendor reports have their
  own attribution biases (vendor X may consistently frame everything as
  "espionage" because that's its commercial framing); the metadata
  audit's `metadata_confidence` column should reflect this, not paper
  over it. (c) Inherits P1's class-cardinality risks (the metadata
  changes which flows go where, not how many classes there are).
- **P6 (Compound-class disjoint).** Risks: (a) compound classes only earn
  their keep if multi-class cases *cluster*; if they scatter across many
  one-off combinations, P6's class count balloons and per-class samples
  shrink. (b) Naming a compound class (e.g. `double_extortion`) introduces
  an analytical category not present in standards-grounded taxonomies —
  defensibility weakens vs P1/P5 unless the cluster is large and
  recognised in CTI vocabulary independently. (c) Disjointness is
  recovered at L4-evaluation cost: a flow that genuinely pursues two
  objectives is forced into "compound" rather than appearing in both
  underlying classes.*

*Cross-cutting concerns the investigation should hold in mind regardless
of candidate:*

- *The corpus is small (40 flows) and uneven (single-observation share at
  88%). Some candidates may fail the discrimination check not because the
  classification is wrong but because the corpus is too thin to separate
  signal at any classification. "More data needed" is a legitimate verdict.
- *The framing question "structural mechanism with metadata cross-check
  vs metadata mechanism with structural cross-check" is genuinely open at
  handoff-time. The handoff's earlier drafts leaned toward the former
  (P5's mechanic is "structural with metadata override"), but a coherent
  P7 — "metadata-primary, structural-fallback" — exists and is worth
  considering if the metadata audit yields high coverage.
- *The discrimination check measures what the simulator surfaces about
  attacker behaviour under MTD. If the simulator's metrics (MTTC, ASR,
  technique frequencies) are themselves not the right discriminators,
  the check is asking the wrong question. The investigation may need to
  flag this as a sub-handoff rather than answer it.*
