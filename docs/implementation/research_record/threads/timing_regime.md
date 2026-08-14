# The timing regime — calibration refused, declaration owned, and time handed to the movement layer

**Span:** 2026-07-09 → 2026-07-28 (S3-R). **Prompts:** #7, #9–#10, #15, #42, #43.
Heavily recorded already —
[`../../../notes/ch4_methods/operational_validation.md`](../../../notes/ch4_methods/operational_validation.md),
[`../../../notes/ch4_methods/exponential_as_tractability_choice.md`](../../../notes/ch4_methods/exponential_as_tractability_choice.md),
[`../../pipeline/ogasp/stochastic_timing_design.md`](../../pipeline/ogasp/stochastic_timing_design.md) —
so this thread carries only what those do not: the order in which the position
was reached, and the one sentence of intent behind it.

**The dilemma was stated before the answer existed.** The 10-Jul question set
(#9–#10) already contains the whole problem in Marc's words: no literature for
per-tactic timing; fitting dwell times "would be overfitting to sparse and
incomplete timings"; tuning them to expected timelines is "a frivolous task …
weak validation power"; and the scale clash (old sims 5 000 s, petri timelines
200–500 s). The resolution — declare, tier, sweep; validate output shape, not
input values — was then *commissioned as a dissertation defence first* (#7:
flesh out each tactic profile "and defend it in a section in a dissertation,
then I can point to it"), before any number was trusted. Argue-then-build is
this project's signature move and this thread is where it first appears.

**The sentence the polished records soften.** #42 (2026-07-28): GSPN "is more of
a veneer to cover up the cracks of the inherently arbitrary nature of these
'tactic timings', which is an impossible idea in real life." The published
defence says the same thing diplomatically ("a true per-tactic duration is not a
measurable property of the world"); the prompt shows the honesty was the
starting point, not a reviewer concession.

**The reversal.** Timing initially lived on both sides (movement layer and
substrate action costs — the conflict named in #31). S3 made tactic time
stochastic (exponential, supervisor-directed); **S3-R** (#43) then retired the
hybrid entirely: "my model should only use timings from the GSPN … I am retiring
the MTDSim timings except for the confusion penalty, which does not exist on the
attacker itself, [but] on the border of the attacker and the defender." The
portability argument carried it (#42): the movement layer must be portable
across simulators via a controller, so simulator-specific thwarting stays on the
simulator's side of the border. Landed as the register's S3/S3-R and the
movement-owns-all-time regime.

**Abandoned on this thread:** absolute-time realism (shape-not-scale ratified
10-Jul); the recon-as-capability-parameter idea (#15 — "how much info an
attacker has … relative strength" — later partially reborn as the synthetic
pre-intrusion overlay M6, but the parameterised-strength version was never
built).
