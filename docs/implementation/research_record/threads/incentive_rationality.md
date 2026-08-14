# Incentive rationality — a mechanism sought, nothing to be rational toward, a measurement shipped

**Span:** 2026-07-29 → 2026-08-02 (final disposition). **Prompts:** #50, #57,
#58, #59, #60, #64. Heavily recorded —
[`../../apt_model_criterion.md`](../../apt_model_criterion.md) axis 6 final
disposition, [`../../pipeline/ogasp/incentive_rationality.md`](../../pipeline/ogasp/incentive_rationality.md),
[`../../pipeline/ogasp/iterated_cost_model.md`](../../pipeline/ogasp/iterated_cost_model.md),
[`../../pipeline/ogasp/attacker_disengagement.md`](../../pipeline/ogasp/attacker_disengagement.md) —
so this thread records only the search path the records compress.

**The struggle was diagnosed before the mechanisms were built.** #57
(2026-08-01): "There is no utility built into this simulator, so there is
nothing the attacker can reason about really" — Marc's own words, three weeks
before the criterion's final-disposition phrasing ("something to be rational
about but nothing to be rational toward"). The intermediate steps: incentive
defined as cross-network opportunity cost — "an attacker expects future payoffs
from reaching objective are at least as good as spending their resources
attacking another network" (#58); the three run outcomes (target hit / rational
give-up / timeout); and the simplification that carried the resolution (#59):
"MTD in this simulator is a **progress-destroying exercise**, and thus the
rationality of an attacker in this world is measured in progress / effort."

**The objection that redirected the whole thread (75–150 band, 2026-08-01/02).**
The first cost model made effort a function of *time*, and Marc rejected the input
rather than the mechanism: "using time to weigh decisions when the times are
inherently arbitrary is a bad research direction" — time-as-cost "directly conflicts
with the low-and-slow of APT attackers", since a time-denominated utility rewards
*fast* attacks, which is the opposite of the patience the disengagement argument
needs, and the tactic durations are themselves declared and arbitrary, so
"hardcoding further into this model is not the right decision". This is the reasoning
behind the pivot away from a time-based cost that the later records only carry the
outcome of; it sits below the 150-word band the main triage read, recovered in the
2026-08-14 short-band scan.

**Ideas tried and dropped on the way:** renaming objective classes onto tactic
buckets to manufacture an incentive ("incentive ≠ objective", self-rejected
within #57); attacker-gives-up-after-X-attempts as a built behaviour (#50 —
became a *frontier over patience* instead, never a switch in the attacker); the
utility modulator and the iterated cost model (both built, both measured
negative, the latter's implementation deleted — the shipped records own these).
The method note in #60: design and cross-examination run by *separate*
independent subagents — rubric first, information set second, model choice
third — the same adversarial-separation discipline as the overlay scrutiny.

**Resolution (#64, 2026-08-02).** "Maintain the implementation as metric only …
if the attack cost = effort is too high … the run terminates as the attacker
gives up." A measurement, not a mechanism — the disengagement frontier — with
the axis closed at DESIGNED by Marc's final disposition the same day.
