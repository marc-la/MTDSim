---
status: durable
chapter: ch6_discussion
created: 2026-08-14
updated: 2026-08-14
---

# The profiled attacker is not competing with the baseline — it is a census of what the field's attacker cannot express

## Position in the dissertation

The discussion chapter's framing of the whole comparison, and the interpretive
move the reader must accept for the results to mean what this work claims. Almost
every experiment sets the intelligence-derived attacker beside the inherited
scripted one, and the natural reading — the new attacker is trying to out-perform
the old — is the wrong one. This note replaces it, and in doing so defends a
finding the naive reading would score as failure: the profiled attacker is, on the
headline metrics, usually worse. It underwrites how every comparative result in the
chapter should be read.

## The idea

When one attacker is repeatedly measured against another, a reader assumes a
contest, and a contest has a winner. On that assumption this project's central
comparison looks like a defeat: the intelligence-derived attacker compromises fewer
hosts than the inherited scripted attacker and reaches no objective the scripted one
does not reach faster. If the question were "which attacker is stronger", the answer
would embarrass the thesis. But that is not the question, and treating it as one
mistakes the instrument for the subject.

The inherited attacker is not this work's competitor. It is this work's *stand-in for
the field* — the scripted, objective-agnostic, single-behaviour adversary that the
surveyed moving-target-defence literature almost uniformly evaluates against. Its
presence in every experiment is not there to be beaten; it is there so that each
result reads as a statement about the evaluations that use such an attacker, rather
than about one program. The comparison is diagnostic, not competitive: it exposes
what an evaluation cannot see when its attacker has a single fixed behaviour, by
placing beside it an attacker that has several and letting the difference speak.

Reframed this way, the profiled attacker's job is not to score higher but to
*express things the baseline structurally cannot*, and to make their evaluative
consequences visible. A scripted attacker has one behaviour, so it cannot show
whether a defence's advantage survives the attacker having options; it pursues no
particular objective, so it cannot show whether a defence tuned against one goal
holds against another; it sprints toward compromise, so it cannot show how a defence
fares against a slow campaign that trades speed for reach. Each of these is a
property the field's attacker lacks by construction, and each is a dimension along
which a defence evaluation could be drawing the wrong conclusion without anyone
noticing — because the attacker that would reveal the error is not in the room. The
profiled attacker is the attacker in the room. Its lower compromise counts are not
its verdict; they are the condition under which its distinctive behaviours are
observed.

### Why declining to close the gap is the correct call, not a concession dodged

There is a standing temptation, surfaced repeatedly while the model was built, to
tune the profiled attacker until it matches the baseline — to give it the scripted
attacker's objective logic, or to bias its routing toward the substrate's own
preferred order, until the compromise counts converge. Every such move was declined,
and the reasoning is the point rather than an excuse. Optimising the profiled
attacker toward the baseline would erase exactly the differences the comparison
exists to measure: an attacker made to behave like the scripted one can no longer
show what the scripted one misses. The convergence that looks like progress is the
destruction of the signal. The honest position is therefore to accept the profiled
attacker's weaker headline performance as a fixed condition of the study — much of
it an artefact of the inherited substrate's procedural rigidity rather than of the
attacker's design — and to read the results as a census of *differences*, not a
scoreboard of *outcomes*.

This does not make the attacker beyond criticism, and the framing is not a shield
against the modest-claim ceiling the rest of the work observes. The census reports
what differs, and a difference is only a finding where it changes an evaluation's
answer; where the profiled attacker's distinctive behaviour changes nothing
measurable, that null is reported as a null. What the reframing buys is protection
against the specific misreading that would otherwise dominate — scoring a diagnostic
instrument as a failed competitor — and it aligns the interpretation with the
thesis's actual contribution, which is to the *methodology* of MTD evaluation and
not to the construction of a stronger attacker. The attacker is the means; the
finding is what its presence makes visible about how the field measures defence.

## Evidence and repo anchors

- The framing reversals in Marc's own words, and their pre-dating of the results
  that might otherwise be suspected of motivating them:
  [`../../implementation/research_record/threads/comparability_and_census.md`](../../implementation/research_record/threads/comparability_and_census.md),
  [`../../implementation/research_record/threads/movement_objectives.md`](../../implementation/research_record/threads/movement_objectives.md).
- The census-not-scale reading of the fidelity criterion:
  [`../../implementation/apt_model_criterion.md`](../../implementation/apt_model_criterion.md) §(b).
- The headline comparative result this framing governs:
  [`../ch5_results/defence_ranking_inversion.md`](../ch5_results/defence_ranking_inversion.md).
- The substrate-rigidity source of the weaker headline performance:
  [`procedural_mismatch_artefact.md`](procedural_mismatch_artefact.md).
- Sibling on scope honesty: [`instruments_fail_silently.md`](instruments_fail_silently.md).

## Revisit conditions

- If the evaluation ultimately shows the profiled attacker's distinctive behaviours
  change *no* defence conclusion anywhere, the census returns only nulls and the
  contribution narrows to a methodological negative result — reported as such, not
  reframed away.
- If a future substrate lets the profiled attacker match or exceed the baseline on
  headline metrics without being tuned toward it, the "accept weaker performance"
  premise no longer holds and the framing simplifies.
- If a reviewer insists the comparison must declare a winner, the diagnostic-versus-
  competitive distinction is the load-bearing rebuttal and must lead.
