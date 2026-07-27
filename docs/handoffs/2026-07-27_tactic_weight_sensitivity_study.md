---
status: open
created: 2026-07-27
---

# Fold the lifecycle-distance dependency into the tactic-pair weights and run the sensitivity study — so that far jumps fall to near zero on evidence rather than judgement, and the evaluation's conclusion is shown not to hinge on where in its band each value sits

**Chain position: wave 3 — after the lifecycle consensus overlay and after the
controller rebuild.** The consensus artefact is the input it folds in; the
controller version matters because a sweep run against a mapping that is about to
change would have to be re-run. Executes the study half of **S1**.

## State of play

**Two things are being delivered here, and they are separable.** The first is a
*re-derivation*: adding a distance dependency to the rules that generate the
tactic-pair weights, so a transition's likelihood falls with how far it travels
across the campaign lifecycle. The second is a *sensitivity study*: showing
whether the experiment's conclusions move when those declared values move within
their plausible range. The supervisor asked for both, and the second is the one
the evaluation's burden-of-proof note has been promising since before the numbers
existed.

**The weights are rule-generated, which makes both jobs tractable.** The canonical
artefact is a small model plus a handful of success and failure rules, each with
one rationale, compiled deterministically to the complete set of ordered tactic
pairs for both verdicts. Nothing is hand-enumerated. So the distance dependency
is **a new term in the model**, not an edit to hundreds of cells, and the sweep
has a small number of **rule constants** to vary rather than an unidentifiable
mass of free values. Preserve that property — it is the same
group-anchors-not-free-fit argument that keeps the duration catalogue defensible.

**What the current model does and does not do.** A pair is resolved by
relationship (forward, lateral, backward, from a five-band prior), by whether the
source enables the destination, and by foothold dependency on the failure side.
Success values run from a modal enablement tier down through forward, lateral and
backward tiers; failure values invert the ordering and add gates. None of these
terms sees *distance*, which is exactly the defect the supervisor named.

**The values are currently certified on internal coherence.** Four adversarial
review rounds converged on the present rule set with zero further changes, and
the panel's own reading was that the remaining confidence gap is the written
defence of the reasoning, not uncertainty in the values. This handoff should read
that as: the reasoning is coherent, and coherence was never external grounding.
Do not treat the certification as a reason to resist changing a value the
lifecycle consensus contradicts.

**The honest caveats already on record** — the soft-floor residual on
initial-access failure, a few objective-band destinations taking more failure
mass than success mass, non-conditionable point masses in sparse profiles, and
the flat enablement tier — are all candidates to be *re-examined under the
distance term*, since several are artefacts of a ladder with no distance in it.
Re-check them; do not assume they survive unchanged.

## Recommended approach

1. **Add distance as one term, and say what it multiplies.** Candidate forms,
   worth ranking explicitly in the record: a geometric decay in lifecycle
   distance; a hard cut beyond a stated distance with a graded region inside it;
   or a piecewise tier set. Recommend the decay with a declared floor — it has one
   free parameter, it degrades smoothly, and a hard zero can then be *derived*
   (values below the floor round to zero) rather than asserted per pair. Whatever
   is chosen, forward and backward distance must be allowed to behave
   differently: falling back three phases after a failure is ordinary, whereas
   leaping forward three phases after a success is the thing being suppressed.
2. **Regenerate, do not hand-edit.** The generator must still reproduce the full
   pair table deterministically from the rules, and the reproduction check is the
   guard against post-hoc fitting.
3. **Validate on the composed nets before sweeping.** Check the pairs that
   motivated the work — the long recon-to-objective jump should collapse, the
   adjacent forward step should stay dominant — and then check that nothing
   plausible has been destroyed: the fall-back regression bridge must still carry
   its mass on failure, and the enablement relations must still lead.
4. **Choose the sweep parameters deliberately, and keep them few.** The decay
   parameter and the small set of rule constants are the natural set. Sample each
   over a declared band, holding the rest fixed, then take the corners of the
   most influential pair together — a full factorial over every constant is not
   affordable and is not what identifiability requires.
5. **Report stability against the headline findings, not against the values.**
   The question is not whether the weights change — they will — but whether the
   *conclusions* do: the two failure modes, the invariance of the outcome to MTD,
   the ordering of profiles by how far they get, and once the full sweep exists,
   the ranking of MTD mechanisms. State in advance which of these the study is
   powered to speak to and which it is not.
6. **Write the result into the ledger, either way.** A finding that the
   conclusion *does* move with the weights is a real result and changes what the
   evaluation may claim — it does not get softened into a caveat.

*Alternatives considered:* sweeping the 210 pair values directly — rejected, the
parameter space is unidentifiable and the result would be uninterpretable.
Choosing the decay parameter so the profiles traverse well — rejected on
principle, and the reason this handoff is sequenced after the literature pass:
the parameter's *value* comes from the consensus, and only its *uncertainty* is
swept.

## Validation gate

Done when:

1. The distance term is in the rule model with a declared functional form, its
   parameters named, and its grounding traced to the consensus artefact rather
   than to this session's judgement.
2. The generator reproduces the complete pair table deterministically, and the
   reproduction is checked.
3. The motivating pairs behave: long jumps collapse toward zero, adjacent
   transitions stay dominant, the failure-side regression path survives.
4. The previously-recorded caveats are re-examined under the new term, and each
   is confirmed, resolved, or replaced.
5. The sweep has run over declared bands with the sampling design stated, and a
   written **stability verdict** exists naming which conclusions held and which
   moved.
6. The declared-value ledger and the overlay design record are updated, including
   an explicit statement that no value was selected to improve any profile's
   traversal.

## Hard constraints

- **No reverse-engineering.** Values are declared from literature and semantics,
  never solved backwards from how the nets then behave. This boundary is what
  separates the weights from the corpus, and the whole defence rests on it.
- **Conditions, never re-derives.** The corpus-derived base weights are not
  touched; the policy layer multiplies and renormalises over them.
- **Binary verdicts only** — the outcome model is not being enriched here.
- **Envelope, not actor.** The weights encode plausible next moves, never a real
  adversary's policy.
- Determinism (SIM-05); the baseline arm untouched; Australian English; branch
  hygiene; never push without an explicit ask.

## Reading list

- The consensus artefact — **landed 2026-07-27** (its handoff is deleted):
  [`../implementation/pipeline/ogasp/lifecycle_consensus.md`](../implementation/pipeline/ogasp/lifecycle_consensus.md)
  and `data/ogasp/controller/lifecycle_consensus.json` — the input this folds
  in. §5 of the record names the fold-in's first decision (whether the
  `relationship` term is recomputed from the consensus stages or kept on the
  five bands with distance added separately), and §7 fixes the sweep set to
  `γ`, `δ`, `z` only.
- [`../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md)
  §1 (composition), §2 (the value model and its caveats), §2.6 (what S1 changes).
- [`../implementation/declared_value_provenance.md`](../implementation/declared_value_provenance.md)
  — the reproducible / tiered / scrutinised requirements a declared value must
  meet, and where the outcome of this study is recorded.
- [`../notes/ch5_evaluation/evaluation_burden.md`](../notes/ch5_evaluation/evaluation_burden.md)
  — the stability-and-divergence burden this study is the first instalment of.
- `data/ogasp/controller/outcome_rules.json` — the canonical rule set and model
  the distance term enters.

## Out of scope (explicitly)

- Dynamic, attacker-state-conditioned weights — S1 names them as the eventual
  direction and defers them.
- The base flow-proportion weights (D3) and anything upstream of them.
- The full MTD-family sweep and the experiment-2 run — carried by the experiment-2
  handoff, which consumes this one's output.
- Re-opening the mapping. If the mapping is still in flux, wait: a sweep against a
  mapping that then changes has to be re-run.
