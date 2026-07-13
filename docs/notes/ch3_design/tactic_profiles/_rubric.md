---
status: durable
created: 2026-07-07
updated: 2026-07-13
lineage: formerly docs/notes @ 2026-07-07_thesis_backbone_rubric.md (relocated in the 2026-07-13 docs refactor)
topic: "the rubric the 15 tactic profiles in this directory must clear"
---

# The tactic-profile rubric — what "APT campaign profiling on dynamic networks" has to achieve, tactic by tactic

> **Process scaffolding** (underscore-prefixed, exempt from the notes register —
> see [`../../../workflows/notes_rubric.md`](../../../workflows/notes_rubric.md)).
> This is the quality gate for the 15 profile files in this directory, the
> profile-specific counterpart to the repo-wide notes rubric. §B is the operative
> part; §A records how the rubric was derived.

## Why this is worth recording

Before Step E of the state-duration work
(shipped 2026-07-09 as [`../../data/ogasp/tactic_durations.json`](../../../../data/ogasp/tactic_durations.json))
the purpose of the whole per-tactic layer was re-litigated: these profiles are not
a means to a duration catalogue, they are the **evidence layer of the thesis's
central novel claim** — *how an APT actor interacts with a dynamic (MTD) network,
tactic by tactic, and what that does to MTD evaluation*. This note (a) critiques
the stream-of-consciousness question set that motivated the reframe, separating
the **backbone questions** (thesis content) from the **meta/QA questions** (process
audit), and (b) consolidates the backbone into a **rubric**: the framing the
subsection must establish once, and the seven things each of the 15 tactic profiles
must deliver, mapped to the five themes (adversarial modelling, attack simulation,
APT behaviour, MTD systems, dynamic networks). It re-scopes Step E from "fill §3
with a reset verdict for the catalogue" to "write the APT × dynamic-network
interaction — the thesis's novel object — for each tactic." The rubric is the bar
the cross-sectional review scores against and the spec the per-tactic thesis drafts
are written to.

## The substance

### A. Reading the question set — themes, strengths, gaps

The motivating questions decompose into **six backbone themes** and a residue of
**meta-questions** that are process-QA, not thesis prose. Keeping them apart is the
first move (the stream-of-consciousness correctly senses they are different kinds
of thing).

**Backbone themes (thesis content):**

1. **The object — APT × dynamic-network interaction.** *"How does an APT attacker
   interact with dynamic networks qualitatively from the literature?"* This is the
   heart and it is correctly framed as an *interaction*, not APT-in-isolation or
   MTD-in-isolation. Strongest instinct in the set.
2. **Modelling / operationalisation.** *"How do we model this? How do we
   operationalise tactics to be executed in MTDSim? What aspects are we
   operationalising?"* — the methodology (the L3b binding, the envelope).
3. **The tactic abstraction as behaviour-carrier.** *"How do MITRE tactics
   encapsulate APT campaigns / capture behaviour?"*
4. **Positioning / contribution.** *"What will MTDSim add? How is this an
   improvement over prior? Do similar adversarial simulations exist?"*
5. **Substrate joining.** *"How are we joining tactics to the existing MTDSim
   substrate?"*
6. **Fidelity boundary.** *"What is important to capture / what are we not
   capturing?"* — the envelope-not-actor humility. A genuine strength: naming the
   omission is what makes the model defensible.

**What is strong:** framing around the *interaction*; the "what are we NOT
capturing" reflex; the positioning questions. These are examiner-facing instincts.

**What the question set under-weights (added to the rubric):**

- **The abstraction *altitude* is asserted, not defended.** The set asks how
  tactics capture behaviour but never *why tactic-granularity is the right level*
  vs technique or kill-chain phase. That defence exists (the precedent survey:
  timed models attach timing at technique/CVE level; the one tactic-level ATT&CK
  net is untimed) — but it must be argued, not assumed.
- **The MTD→attacker direction is the genuine unknown and is not foregrounded.**
  The questions ask how the attacker interacts with the network; they do not
  centre the fact that *no public logs ground the MTD→attacker effect*
  ([`./2026-06-18_cti_to_executable_behaviour.md`](../structure_to_behaviour_binding.md) §5).
  Every tactic must state its **reset verdict** (does a mutation invalidate the
  gain here, or does it survive?) and own the uncertainty. This is Step E and it
  is the novel half.
- **The attacker's *knowledge* is raised but not systematised.** The brief notes
  "MTD strengths/limits are known to an attacker with relative degrees, e.g. one
  successful in recon" — this is the observability/knowledge dimension and it is
  rich and under-theorised. Each tactic should say *what the attacker learns/holds*
  and *how a mutation degrades that knowledge*.
- **Epistemic status / validity is absent from the list** yet is central: what
  claim is each profile *allowed* to make (operational validation, shape-not-scale,
  envelope-not-actor). The rubric forces each section to badge it.
- **Objective-conditioning.** The questions treat "the APT attacker" as singular;
  the GASP profiles are objective-conditioned (steal / impede / extort / setup).
  Does behaviour in a tactic *vary by campaign goal*? If yes it is a discriminator;
  if inert, say so.
- **Discrimination / falsifiability** — the risk that matters more than the
  encoding (CTI note §10): does this profile contribute a behavioural distinction
  that *could change an MTD ranking*? A tactic whose dwell and reset are identical
  across all objective-profiles is inert and should be flagged as such.

**Meta-questions (process audit, not prose) — routed to the grey-box review, not
the thesis:** *"Have we litigated the literature well enough? Have we been probing
the correct areas? Have we extracted what we need?"* These are the criteria the
literature-adequacy audit answers; they do not become rubric rows for the writing.
(*"Do similar adversarial simulations exist?"* is half-and-half: the asking is QA,
the answer is related-work prose — theme 4.)

### B. The rubric

#### B.0 — Framing the subsection must establish once (not per tactic)

1. **The object and why it is under-served** — APT-on-dynamic-network interaction
   as the modelled thing; prior work models APT-on-static or MTD-vs-generic, rarely
   the join.
2. **The abstraction choice, defended** — why ATT&CK *tactics* are the right
   altitude to carry APT behaviour into an *executable* model (technique-level is
   unexecutable-at-corpus-size; kill-chain is too coarse; tactic is the groundable
   middle — cite the precedent survey gap).
3. **The contribution over prior** — over the procedural 6-phase attacker
   (objective-agnostic smash-and-grab), over untimed CTI nets (Rodríguez 2024),
   over technique/CVE-level timed models (Ling & Ekstedt). MTDSim adds an
   *executable, objective-conditioned, per-tactic-timed* attacker against *existing*
   MTD.
4. **The epistemic contract** — envelope-not-actor; operational validation
   (calibrate the unobservable to the observable, badge the tier, sweep);
   shape-not-scale; MTD-reset declared-not-evidenced. The humility is load-bearing.
5. **The fidelity boundary** — captured: objective, capability preconditions,
   low-and-slow dwell, MTD reset. Not captured (this cut): adaptivity/learning,
   detection/IDS, real CVEs. Named up front.

#### B.1 — What each of the 15 profiles must deliver (mapped to the five themes)

For tactic *T*, the profile answers — **from the literature, behaviour before
numbers**:

| # | Criterion | Theme | Lives in |
|--:|---|---|---|
| 1 | **Behavioural character** — how does an APT *act* in *T*: fast verb or low-and-slow dwell, and the behavioural logic (not the value). | APT behaviour | §1/§2 |
| 2 | **Temporal claim** — dwell character → timing group + *relative* structure, argued and tier-badged. No orphan point-number. | adversarial modelling | §2→§5 |
| 3 | **Attacker knowledge & the dynamic-network interaction** — what the attacker *learns/holds* in *T*, and whether a network mutation (IP/topology shuffle, service/OS diversity, redundancy) **invalidates** that gain or it **survives**. The reset verdict + its uncertainty. | dynamic networks | **§3** |
| 4 | **MTD interaction mechanism** — *which* MTD action bites, argued from mechanism (no logs exist), and *how hard* → the sweep width. | MTD systems | **§3** |
| 5 | **Operationalisation** — how *T* maps onto the substrate: a native verb it inherits (Tier 1) or a declared dwell (Tier 3), and what the L3b binding does with it (precondition/effect). | attack simulation | §5 (+ binding handoff) |
| 6 | **What is NOT captured in *T*** — the honest per-tactic omission. | fidelity boundary | §3/§5 |
| 7 | **Objective-conditioning & discrimination** — does behaviour in *T* vary by campaign objective; does the profile contribute a distinction that could move an MTD ranking, or is *T* inert? | adversarial modelling | §2/§5 |

The five-theme cross-product test: a complete profile can be written as
*T × APT-behaviour × adversarial-modelling × dynamic-networks × MTDSim-substrate
× MTD-mechanism*. A profile that cannot fill one column has a real hole, not a
stylistic one.

#### B.2 — Cross-cutting quality criteria (the grey/black-box scoring axes)

- **Numbers subordinate to themes.** Every figure earns its place by resolving
  dwell-character (crit. 1–2) or reset-verdict (crit. 3–4). A statistic that
  resolves neither is trim, however hard-won.
- **Literature adequacy for the *behavioural* question.** The right sources are
  those that describe *how APTs behave in T*, not those that merely report a
  macro duration. A profile can be number-rich and behaviour-poor.
- **Reset verdict present and owned.** Crit. 3–4 written, mechanism-argued,
  uncertainty → sweep width. (Currently unmet in all 15 — this is Step E.)
- **Discrimination declared.** Crit. 7 — inert tactics flagged.

### C. What the reframe does to Step E

Step E stops being "declare a reset fraction for the catalogue". It becomes **the
prose of criteria 3, 4, 6 for every tactic** — the APT × dynamic-network
interaction, argued from MTD mechanism, which is the thesis's novel contribution
and the theme the current profiles are thinnest on (§3 empty in all 15;
dynamic-networks is the least-developed of the five themes). The catalogue's
reset-fraction is then a *distillation* of that prose, exactly as the duration is a
distillation of §2. Writing §3 well is writing the thesis, not feeding a JSON file.

## How it connects

- **Governed** Steps E/F of the state-duration work (shipped 2026-07-09 as
  [`../../data/ogasp/tactic_durations.json`](../../../../data/ogasp/tactic_durations.json));
  the rubric's B.1 crit. 3–4 *are* Step E, crit. 2/5/7 feed Step F/§5.
- **Rests on** the epistemic contract in
  [`./2026-07-04_operational_validation_the_bar.md`](../operational_validation.md)
  (validity tiers, shape-not-scale) and the envelope/binding framing in
  [`./2026-06-18_cti_to_executable_behaviour.md`](../structure_to_behaviour_binding.md)
  (ontology gap, encoding ledger, MTD-reset-is-the-unknown, envelope-not-actor).
- **The gap it defends** (framing crit. 2–3) is evidenced in
  [`./2026-07-04_tactic_duration_precedent_survey.md`](../../ch2_background/tactic_duration_precedent_survey.md).
- **Needs a companion artefact:** a non-implementation-specific *substrate primer*
  (the attacker's-eye view of the HARM network + MTD mechanisms + what a successful
  recon/discovery attacker can know) so profiles reference it instead of re-deriving
  it. Currently that content is scattered across the CTI-note §2/§5/§6/§7.

## When this would need updating

- If the discrimination probe shows the objective-profiles do not separate under
  MTD — crit. 7 becomes the whole story and the negative-result disposition
  applies.
- If Marc/Hong reject envelope-not-actor or shape-not-scale — framing crit. 4 is
  rewritten and per-tactic crit. 2–3 re-open.
- If the substrate adopts real CVEs — crit. 5 (operationalisation) gains the
  vuln-instance binding and Tier-1 coverage widens.
