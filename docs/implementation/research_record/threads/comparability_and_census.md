# Two framing reversals — comparability abandoned, then the race itself

**Span:** 2026-07-13 and 2026-07-29. **Prompts:** #17; #51 → #52, #53.
Landed: [`../../metrics_semantics.md`](../../metrics_semantics.md) (comparability
boundary), the criterion's census-not-scale rule
([`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(b)), and the new
note [`../../../notes/ch7_discussion/refusing_the_baseline_race.md`](../../../notes/ch7_discussion/refusing_the_baseline_race.md).

**Reversal one — cross-paper comparability (#17, 2026-07-13).** The assistant
was treating preservation of MTTC comparability with Zhang/Tay as a hard
constraint; Marc overruled it as "a fundamental flaw you are overconsidering",
citing Dr Hong's written ruling that "simulation settings can be updated to suit
the experiments", and ordered the work re-run under the new weighting. The
mature form is the comparability boundary: within-substrate comparison valid,
cross-paper numeric comparison INVALID. The prompt shows the boundary was not a
concession discovered late but a deliberate re-prioritisation made the same week
the pipeline was being scoped.

**Reversal two — the race itself (#51 → #52, 2026-07-29, hours apart).** #51
still reasons inside the old frame: "the goal of learning capability … is to
bring the attacker in line with the performance of the baseline attacker, so we
can compare them". #52 breaks it: "let's be real, there doesn't have to be a
qualitative comparison between the baseline and the movement attacker … We need
to break the framing that we are comparing the baseline and the movement
attackers; we are measuring the qualities of the movement attacker that the
baseline does not demonstrate, **and the baseline is analogous to all the other
attack models in the MTD field as cited in lit review**." The baseline stops
being a competitor and becomes the field's representative — which is what makes
its presence in every experiment an argument about the literature rather than a
score to beat.

**The corollary (#53, same day).** "The attack model is only a means to achieve
the thesis goal" — fidelity findings about MTD evaluation are the contribution,
the model is instrument; "the APT criterion is a tool … not the end in itself."
Also here: the extensibility claim in its earliest form (port the framework to
your own simulator; capability at tactic level, extensible to technique or
sub-technique level).

**Superseded positions recorded as such:** matching Zhang/Tay numerics
(pre-#17); learning-to-match-baseline (#51, reversed within hours — the
sharpest same-day reversal in the corpus, and the best evidence that the census
framing was a decision, not a rationalisation after weak results: it predates
experiment 2 and the criterion's census rule by days).
