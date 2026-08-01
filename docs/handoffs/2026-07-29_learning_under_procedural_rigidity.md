---
status: open
created: 2026-07-29
supersedes: 2026-07-29_controller_composition_unification.md (folded in whole)
---

# Generalise the learning capability so it can represent a precondition constraint — the proof of concept works and makes the attacker worse, and the reason is representational

**Chain position: after
[`2026-07-29_reconcile_stranded_axis_work.md`](2026-07-29_reconcile_stranded_axis_work.md),
which is blocking.** The whole argument below rests on a sweep `dev` cannot
currently see. Governed by
[`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md).

This handoff replaces `2026-07-29_controller_composition_unification.md` and
carries its content unchanged where it still applies. The two were separate on the
assumption that the FSM-alignment factor and the learner addressed different
problems; they address the same one, and the alignment factor is best understood
as the learner's missing input rather than as a mechanism beside it.

## State of play

**The mechanism works and makes the attacker worse.** The within-run learner
drives its own blocked fraction from 91 % to 21 % as the capability rises, within
runs, against an ablation arm that barely improves — so it demonstrably operates.
Compromise breadth falls from 6.5 hosts to 0.8 across the same band, exploitation
falls from 13 % of its successes to 1 %, and no run at any parameter point reaches
the objective. As a proof of concept it is sound. As an attacker it is worse than
not having it.

**The diagnosis, and it is not a tuning problem.** Being blocked is a function of
*state*: an exploit fails because this host has not yet been port-scanned. So the
quantity the attacker would need is the success probability of a tactic
**conditioned on its current phase-state**. The learner is keyed on the destination
tactic alone, so it can only represent the marginal, averaged over every context it
has been in — and marginalising over phase-state discards precisely the variable
the precondition depends on. No quantity of runs repairs a representation that
cannot express the dependency.

**What it does instead is route around the constraint.** Unable to learn *exploit
after scanning*, it learns *exploit fails often*, and moves weight onto the tactics
with the fewest preconditions — reconnaissance and host discovery, which succeed
almost unconditionally. There is a self-reinforcing loop behind the monotonicity:
avoiding exploitation drives the phase-state distribution further from the states
in which exploitation would have worked, which depresses the estimate further.

**So the generalisation problem is stated precisely**: give the attacker a
representation in which "this tactic pays *here*" is expressible, **without**
reinforcement learning — no eligibility traces, no discount factor, no value
function — because that machinery is out of scope on timeframe and is the same
machinery the scheme-awareness axis was ruled out over.

## Recommended approach

**Part A — settle the representation before writing any code.** This is the whole
research content of the session and it should be argued in a design record first,
in the shape the four prior studies used.

1. **Rank the candidate keys on an explicit axis** — coarsest to finest, cheapest
   to most faithful — and pick with reasons in both directions. At minimum:
   - `(destination tactic)` — today. Cannot express the dependency.
   - `(destination tactic, current phase)` — the smallest key that can. Costs a
     table of roughly fifteen tactics by six phases, most of it sparse.
   - `(destination tactic, precondition-satisfied?)` — a one-bit context, far
     denser and arguably the honest minimum: the attacker learns "this pays when
     I am ready for it" rather than memorising a phase table.
   - `(previous tactic, destination tactic)` — the chain form. Note this is
     **pairwise**, not trajectory credit; it needs no eligibility trace, and it is
     the option closest to what a campaign-shaped attacker would plausibly track.
2. **Confront the sparsity honestly.** A finer key means fewer observations per
   cell in a bounded run, and the Laplace prior that keeps unvisited cells at 0.5
   will dominate a sparse table — the learner would spend the run at its prior and
   look inert. Say what the observation budget per cell is under each candidate
   before choosing, using the measured visit counts rather than an estimate.
3. **Keep the exploration guarantee.** Whatever the key, an unvisited cell must sit
   at a neutral value and never at zero, or the mechanism silently deletes parts of
   the net. This property is why the current estimator is what it is.

**Part B — the FSM-alignment factor, as the supplied signal.**

4. **Build it as a declared bias toward the host's successor phase**, firing at
   places the mapping declares dwell-only. Those dispatch nothing, raise no verdict
   and currently route on base weights alone, so a bias there overwrites no
   existing conditioning and nudges *sequencing* rather than substituting actions.
5. **Transcribe the successor relation into a declared, versioned artefact** rather
   than reading it live from the substrate. That makes it a controller artefact
   under the same discipline as the tactic-to-verb mapping, and it is what carries
   the portability claim: to port this framework to another simulator you declare
   its action vocabulary **and** its procedural order.

   **Ruled by Marc, 2026-07-29 — the observation question is closed and does not
   need re-litigating.** The concern was whether consuming the attacker's current
   phase is legitimate self-knowledge or privileged information about the
   environment. It is neither: the movement layer *is* the attacker choosing its
   next objective, and the action layer's phases *are* the tradecraft available to
   it, so the phase is a description of what the attacker is itself attempting.
   Knowing it is not an observation at all.

   The ruling extends to the successor relation, and that extension is the part
   worth writing into the record. The ordering constraints of the action layer are
   constraints on the attacker's own tradecraft — an operator knows a service must
   be examined before it can be exploited — so declaring them is a statement of
   attacker competence rather than a cheat sheet about the host. This is also why
   the artefact belongs beside the tactic-to-verb mapping: both declare what the
   attacker can do in this environment and in what order, which is exactly what an
   adopter re-declares when porting. **Nothing here reads the defender**, so the
   scheme-awareness exclusion is untouched and no part of this needs re-arguing
   against it.
6. **Decide whether it biases routing or feeds the learner** — the two designs
   differ and the record should choose. Biasing routing is a static declared factor.
   Feeding the learner means phase agreement enters the credit counts, so the
   attacker learns *which contexts pay* from a signal that carries progress rather
   than mere verdict satisfaction. The second is the one that generalises the
   capability; the first is the one that ships in an afternoon. Recommend the
   second if Part A's key supports it, and say why if it does not.

**Part C — the composition record and the joint sweep** (carried from the
superseded handoff).

7. **Keep the seam split, and write it down.** Portable modulators stay on the
   movement seam; substrate-coupled ones go on the controller seam. That boundary
   is the portability claim made structural — it is the statement of which parts an
   adopter keeps and which they re-declare for their own simulator — and moving the
   learner or the utility model into the port would dissolve it. No document
   currently states what the factors are, where each lives, and which are active in
   the reported configuration; this is where that record belongs.
8. **Run the joint-composition check that has never run.** The three declared
   families have only ever been swept one at a time. Two independently narrow
   traversal, so composing them compounds the narrowing, and axis 3's demonstrated
   badge was earned with all of them null. A small crossed arm reporting path
   entropy settles whether the reported configuration is still the measured one.

## Validation gate

Done when: the representation choice is argued against the ranked alternatives with
its sparsity budget stated; the null configuration is bit-identical to the model
without the mechanism; the successor map is a tracked, versioned, regenerable
artefact; conclusions are pre-registered in their own commit before any output; the
coupling finding is shown to survive at null strength; the sweep reports whether the
generalised learner raises breadth or stage advance **against its own ablation
arm**; the joint-composition check has run; and a tracked record exists.

## Hard constraints

- **No reinforcement learning.** No eligibility traces, no discount factor, no
  value function, no policy gradient. If the design needs them, the honest output
  is that it needs them and the work stops there.
- **Null is bit-identical to today**, and the coupling finding must remain
  reportable at null strength — a mechanism that quietly routes around every unmet
  precondition would hide the project's own finding.
- **Values are declared, tiered, rule-generated and swept**, never chosen because
  they improve an outcome. This is the most tempting place in the project to fit a
  value to the layer it conditions.
- **Badge discipline.** A generalised learner moves axis 7 only if it raises
  breadth or stage advance against its ablation arm — which is the criterion the
  axis-7 record already fixed. If it merely lowers the blocked fraction again, that
  is the same result as before and the badge does not move.
- No substrate change; no change to the tactic-to-verb mapping; determinism;
  envelope-not-actor phrasing; Australian English; never push.

## Reading list

- `docs/implementation/pipeline/ogasp/learning_capability.md` §3.1 (why the key is
  the destination place, and the three rejected alternatives), §7.6 (the
  breadth collapse and its mechanism), §8 (what would move the badge) — **after
  reconciliation; on `dev` today §7 is a stub.**
- `docs/implementation/pipeline/ogasp/model_scope_freeze.md` §5 — the
  representation argument in full, and the three things the alignment factor is not.
- `docs/implementation/pipeline/ogasp/experiment_01_findings.md` §3 — the coupling
  finding this must not dissolve.
- `docs/implementation/pipeline/ogasp/attacker_state_seam.md` — the modulator
  Protocol, the composition rule and the null-equivalence guarantee.

## Out of scope

- Reinforcement learning in any form.
- Cross-run memory, and anything reading defender behaviour.
- Relocating the existing modulators into the controller layer.
- Dissertation prose.
