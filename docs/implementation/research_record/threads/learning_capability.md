# Learning capability — four builds, one moving target, and the credit-signal isolation

**Span:** 2026-07-28 → in flight (exploit learning). **Prompts:** #45, #49, #51,
#54, #61, #62, #75, #88, #96. The builds are recorded —
[`../../pipeline/ogasp/learning_capability.md`](../../pipeline/ogasp/learning_capability.md),
`learning_representation.md`, `learning_readiness_findings.md`, the criterion's
axis 7 — so this thread carries the intent arc.

**What learning was *for*, in the original intent (#45, #49).** Two motives the
records under-state. First, compensation: learning was conceived as "the
mitigation and the saving grace" for the substrate's rigidity — an attacker that
cannot be told the FSM's happy path should be able to *find* it by trial and
error. Second, portability: "mechanisms to fit petri nets to whichever
[substrate] naturally works without tying to one specifically is the key, the
natural adaptation at runtime of the attacker to fit the shape of the attack
model … if the attack model changes, the mapping will naturally adapt to this
new shape" (#49). Learning as a generic adaptor between intelligence-derived
structure and arbitrary hosts — a framing worth keeping for the discussion
chapter, because it explains why the learner's failure is a finding about
substrates, not a dead feature.

**The consolidation ask (#61, 2026-08-02)** is the corpus's precedent for this
whole mining exercise: "find all the conversations I have had over the last week
for axis 7 … compile all my messages … and look at the themes present". It also
records a live disagreement: the assistant had classed workflow (tactic-chain)
memory as an ML/RL mechanism; Marc: "I would disagree" — chains could be done
simply. Chains were never built; the representation went to
`(destination, precondition-satisfied?)` instead, and cross-run memory stayed
ruled out (M8d).

**The FSM-overlay concession (#54, #62).** Piping the substrate's legal next
phase into the weights, owned explicitly as "a concession … the direct piping in
[of] the next phase is an okay proxy … in lieu of no updates to the underlying
attack implementation", with the honest future-work framing attached (the
indirect trial-and-error version named as what a successor would build). This
became the alignment dial (see
[`three_layer_seam.md`](three_layer_seam.md)).

**In flight at the time of mining:** the exploit-learning mechanism (vulnerability
memory raising repeat-exploit success — #75, #88, #96), including a wiring
debug in Marc's own diagnosis ("your implementation is in parallel with the
impact gate … ironically having no impact", #96) and a pre-registered
evaluation hypothesis (#88): under a constrained service pool the effect should
be pronounced and **diversity defences should be hit hardest** — "diversity acts
on the premise there are a set of different vulnerabilities the attacker would
have to try … if diversity is constrained it is not particularly effective."
`data/ogasp/movement/exploit_learning_yield_sweep.json` is this work's artefact.
The second mining pass should pick this thread up where it lands.
