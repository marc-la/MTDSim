# The movement-objectives problem — churn diagnosed, the weakest link conceded, the race refused

**Span:** 2026-08-01 and 2026-08-11. **Prompts:** #54, #96–#99. Partially
recorded ([`../../../notes/ch6_discussion/procedural_mismatch_artefact.md`](../../../notes/ch6_discussion/procedural_mismatch_artefact.md)
carries the artefact argument); the concession's *scope logic* is argued in
[`../../../notes/ch6_discussion/refusing_the_baseline_race.md`](../../../notes/ch6_discussion/refusing_the_baseline_race.md).

**The acceptance (#54, 2026-08-01).** "I think I have accepted the fact that
with (1) no changes to the underlying attack phases … the performance of my
model is constrained by the weakest link, which is the FSM … (2) there is not
enough time to produce research-worthy updates to the underlying MTDSim model."
With it, the freeze ("whatever we have, we have to freeze"), the expectation
("our model essentially will be, at best, on par with the baseline attacker,
and on average significantly worse"), and the integrity rule that governed the
remaining weeks: "I don't want to embellish my research with half-cooked
implementations that are not research worthy."

**The sharper diagnosis (#97–#98, 2026-08-11).** The verb *decoupling* had
succeeded, but the substrate's **attack objectives** (Brown's general/targeted)
were still optimised around the baseline's one behaviour — so a stochastic
tactic order breaks the emergent objective: the attacker "dwells on already
compromised hosts, and is not on the frontier of the network", i.e. the churn
experiment 1 measured. #98 asks whether an objective must be reinstated at all
("is this even relevant to my research question? … APT attackers are somewhat
competent — this behaviour is not reflective of such") — the question that
separates repairing the model from repairing the evaluation.

**The refusal (#99), the thread's decision.** A `movement_general` /
`movement_targeted` objective set was considered and declined: "all the workshop
we have done here today is suggesting my movement attacker is wrong and we
should move towards the baseline attacker so we can be more successful. **That
is the wrong outcome.**" The dissertation position drafted in the same prompt:
concede the weakest link, measure what can be measured, flag the action-layer
upgrade as future work — "the real power from the model is it's extendable; if
somebody tried implementing a new set of underlying attacker actions … this
would solve the integration problems here." Feedback was to be sought from the
supervisor; the 11-Aug meeting's structure rulings landed the same week and the
concession stands as drafted.

**Negative space:** movement-specific objective sets (considered, declined);
optimising the mapping until the movement attacker matches the baseline
(refused on principle, twice — see also
[`comparability_and_census.md`](comparability_and_census.md)).
