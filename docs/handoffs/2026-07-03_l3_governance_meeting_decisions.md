---
status: open
created: 2026-07-03
---

# Encode the July-2026 supervisor-meeting decisions into the canonical specs — the weighting regime, the v1 coupling model, scope, the deferred register, and the envelope framing

> **Run this first.** Every other 2026-07-03 handoff premises a decision that
> currently exists only in Marc's meeting minutes. This handoff gives those
> decisions a durable home (a note) and reconciles the canonical specs with
> them (Marc-approved wording — [`../specs/guardrails.md`](../specs/guardrails.md):
> spec edits are Marc-driven; propose, don't unilaterally edit).
>
> This handoff **absorbs**
> `2026-06-18_envelope_not_actor_framing.md` (deleted 2026-07-03; its
> commits-to / rules-out block is reproduced below) and supersedes the
> Stage-0 governance items of `2026-06-18_l3_ogasp_petri_implementation.md`
> (deleted 2026-07-03; see git log).

## State of play

- A supervisor working session with Dr Jin Hong (early July 2026; minutes held
  by Marc) settled the L3 execution model. The decisions are **not yet recorded
  anywhere in the repo** — the minutes live outside it, and the specs still
  reflect the pre-meeting state (e.g. [`../specs/architecture.md`](../specs/architecture.md)
  §(f) says L3 is "unbuilt" and that `src/mtdsim/l3_simulation/` "holds no
  code" — both stale: the L3a structural nets are shipped at
  [`../../data/ogasp/`](../../data/ogasp/) with build code at
  [`../../src/mtdsim/l3_simulation/petri/`](../../src/mtdsim/l3_simulation/petri)).
- **The decision register to encode (D1–D10):**
  - **D1 — Both tracks.** Not formalism-only: "incorporate the petri net into
    MTDSim so the attack behaviour is dictated by this", *and* examine the
    attack behaviour the net generates on its own.
  - **D2 — v1 coupling is one-way.** Run the Petri net independently of the
    simulator. A **single token** moves through the net; record the state at
    each node; each state has a duration; output = a **timed sequence of
    attacker states** (cumulative timeline) fed into the simulator. Two-way
    interaction (simulator ↔ net each event) is the end goal, **deferred**.
  - **D3 — Edge weights.** Derived as the **proportion of attack flows leaving
    each node**, computed at **tactic level** (aggregation up from techniques
    is what makes the weights groundable at this corpus size). The sparsity of
    the ~38-flow corpus is **accepted**: "it's the only quantitative evidence
    available to populate the Petri nets. Looking thin is fine."
  - **D4 — Durations.** Since the simulator is discrete-event, **every state
    needs a time**. Reuse timing values from relevant work where they exist;
    otherwise assign a **reasonable, justified** number (e.g. for stealth).
    No ready-made MITRE-tactic→time resource exists — define it, with
    justifications.
  - **D5 — Scope of MTDSim change: attacker only**, for comparability with
    previous work. HARM / network / MTD mechanisms untouched.
  - **D6 — Uncaptured behaviours** (stealth, evasion, access/response
    development): manually define reasonable connections/values as a starting
    point. Detection-rate effects and evasion come later if time allows;
    **attack behaviour is the priority**.
  - **D7 — Success model.** Keep the same routes, but let the attack
    behaviour/state decide the outcome (an attacker in a stealth state won't
    launch the exploit the simulator would otherwise expect). Three layers:
    net state → simulator action → outcome. **Scoping only for now.**
  - **D8 — Entry point.** Test **both**: seed at `initial-access` (the
    corpus's real entry) and the recon-back curation — "straightforward to
    test".
  - **D9 — Structural sparsity at node level is fine** so long as there is a
    coherent path from start nodes to end nodes.
  - **D10 — Priority & deferrals.** Working implementation **before Semester 2
    starts**; the scoped implementation is already distinction-level.
    **Deferred:** two-way integration, sensitivity analysis on net weights,
    evasion/detection-rate modelling, timed Petri nets (GSPN/SPN/TPN firing
    semantics), aggregated cross-profile variation analysis.
- **Still open with the supervisor** (flag in the note; do not decide here):
  the 5th **aggregate/null profile** (Marc's proposal, unanswered — the
  downstream handoffs treat it as accepted pending confirmation because it
  doubles as the "do the classes differ" verification); **corpus expansion**
  (other MITRE-based databases, or GenAI-sequenced 59 MITRE campaigns with
  Attack-Flow overlap as cross-verification); the **CVE↔synthetic-CVSS binding**
  approach (confirm); cost-only vs proto-IDS for stealth tactics (note:
  [`../specs/project_context.md`](../specs/project_context.md) already rules
  out building IDS — cost-only is the only compliant MVP option; say so).
- **The spec collision that must be resolved deliberately (the crux):**
  [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f) rules
  "seeding L3 transition probabilities directly from edge weights" **INVALID
  as-is** — but its own text names the escape: it becomes valid with "an
  *explicit, documented* normalisation + closed-world assumption". D3 is the
  supervisor authorising exactly that, at tactic level. The work is to write
  that disposition down, not to silently start normalising.
- Four pre-meeting handoffs were deleted in the 2026-07-03 sweep (dispositions
  in the git log and in each new handoff's banner).

## Recommended approach

**1 — Author the meeting-decision note (the durable record).** Write
`docs/notes/2026-07-03_supervisor_meeting_l3_decisions.md` from the D1–D10
register above plus the still-open list, in the notes template. Handoffs get
deleted when work lands; the decisions must survive that. Cross-link the six
2026-07-03 handoffs and mark which decision each one executes.

**2 — Propose the `metrics_semantics.md` §(f) disposition block** (Marc
approves wording before commit). Content: tactic-level aggregation of
technique-edges to tactic-pair transitions; weights = out-edge-normalised
**flow proportions** (not raw `observation_count` magnitudes — the count stays
recorded but un-normalised at technique level); the **closed-world assumption**
stated (the corpus's out-edges are treated as the complete choice set at each
tactic); the **survivorship framing** carried over (§(f) row 1: this measures
disruption of *typical observed workflow*, never adversary optimality or
efficacy); sourced to the supervisor decision (D3) with date. The uniform
policy is retained as the **structural floor** for sensitivity, replacing the
retired "uniform-only" regime of the deleted analytical handoff.

**3 — Propose the `architecture.md` §(f) updates.** (a) Fix the stale status
(L3a shipped; code exists). (b) Add a **v1 coupling decision block**: one-way
timeline replay per D2, single token, alongside-not-replace unchanged, two-way
integration named as the deferred end-state. (c) Re-position the Petri-net
decision: no longer merely a "candidate alternative analytical substrate" —
it is now the **primary behaviour source** for the executable attacker (D1);
the closed-form CTMC solve moves to the deferred register. (d) Record the
working layer ledger the 2026-07-03 handoffs use: L3a = structural nets +
parameterisation (weights, durations); timeline generation = standalone net
execution; binding/replay = the MTDSim coupling.

**4 — Propose the `provenance.md` regime rows.** One row for the weighting
regime (D3: corpus → flow-proportion → code pointer once H2 lands) and one for
the duration regime (D4: tiered sourcing — substrate / literature / justified
estimate — the catalogue itself is the `l3_state_durations` handoff's job).

**5 — Place the envelope-not-actor block** (absorbed from the deleted framing
handoff; rationale at
[`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md)
§1). *Commits to:* each class net is a **behavioural envelope / generative
grammar for an operational objective** (a union of 5–19 flows); a run is *one
instantiation* under a declared policy; the claim is
*fidelity-changes-the-answer* over a CTI-grounded envelope. *Rules out:*
claiming a traversal *is* a named actor; reading the envelope MTTC as a real
campaign's dwell time; reading weighted paths as actor-likelihood. Wording
lands in `architecture.md` §(j), one-liners in `metrics_semantics.md` and
[`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md). Every downstream
claim is phrased envelope-relative ("under the `pure_steal` envelope…").

*Alternative considered:* skip the governance pass and let the downstream
builds cite the minutes directly. Rejected — the minutes are outside the repo,
the §(f) prohibition would then be violated silently rather than dispositioned,
and the viva-facing framing (envelope, closed-world, survivorship) is exactly
the material that must exist *before* numbers are produced.

## Validation gate

Done when:
1. `docs/notes/2026-07-03_supervisor_meeting_l3_decisions.md` is committed,
   carrying D1–D10 + the still-open list, each cross-linked to the handoff
   that executes it.
2. The §(f) disposition block, the §(f)-architecture updates, the provenance
   regime rows, and the envelope block are **drafted, approved by Marc, and
   present** in the canonical specs.
3. No downstream 2026-07-03 handoff premises a decision that is not traceable
   to the note or a spec block.

## Hard constraints

- **Canonical-spec edits are Marc-driven** — propose wording; Marc approves
  before commit ([`../specs/guardrails.md`](../specs/guardrails.md)).
- This handoff is **docs only** — no code, no data artefacts beyond the note.
- Do not decide the still-open supervisor questions; record them as open.
- Do not re-open the L2 partition/aggregation decision.
- Branch hygiene, **never push without an explicit ask**, Australian English —
  [`../specs/session_workflow.md`](../specs/session_workflow.md).

## Reading list

- [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f) — the
  prohibition being dispositioned; read the whole section before drafting.
- [`../specs/architecture.md`](../specs/architecture.md) §(f), (j), (l) — the
  blocks being updated.
- [`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md)
  — §1 (envelope), §5 (encoding ledger), §11 (the MVP cut the meeting largely
  ratified).
- [`../../data/ogasp/README.md`](../../data/ogasp/README.md) — what L3a
  actually shipped (the stale-status fix needs this).
- [`../specs/provenance.md`](../specs/provenance.md) — row format for the two
  regime rows.

## Out of scope (explicitly)

- Building anything: weights, durations, the runner, the binding (handoffs 2–6).
- Deciding the aggregate-profile, corpus-expansion, or CVE-binding questions —
  record them as open-with-supervisor.
- Rewriting `02_gasp_schema.md` beyond the envelope one-liner.
- IDS / detection features (project-wide out of scope).
