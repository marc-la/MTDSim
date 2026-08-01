---
status: open
created: 2026-07-29
---

# Add the two rows the criterion cannot currently score — evidential provenance and evaluative consequence — because the project's largest result scores on none of the existing eight

**Chain position: independent of everything, and cheap.** Documentation and
scoring only; no mechanism, no run. **Unblocked 2026-08-01** — it waited only on
the stranded-axis reconciliation, which landed on `dev` that day (and its handoff
was deleted with it), so the criterion file is no longer contested.

**Premise re-verified 2026-08-01:** the criterion still carries exactly the eight
original axes and no consequence or provenance row, so this brief's motivating
gap is unchanged and unshipped.

## State of play

The eight-axis criterion was derived from three surveys before the model was
scored, and it has done its job: it is why the fidelity claim is falsifiable
rather than asserted, and it has twice forced a badge to be withheld or withdrawn
after the numbers would have supported it.

It has one structural blind spot, and the comparative experiment made it
impossible to ignore. **The project's largest result scores on no axis.** The
ranking of MTD mechanisms inverts between the inherited attacker and the profiled
one — the diversity family suppresses the vulnerability-exploiting baseline far
more than it suppresses the profiled attacker, and the position-destroying family
does the reverse, with the effort-to-breadth crossover to match. That is the
project's modest claim in its strongest form: behavioural fidelity does not merely
change the magnitude of an evaluation's answer, it can change which mechanism the
evaluation recommends.

No axis scores it, because the eight axes score *properties of an adversary* and
this is a property of *an evaluation*. An attacker could satisfy all eight and
change no defence ranking; this one satisfies two and inverts it.

That distinction also decides who the instrument is useful to. The eight axes help
someone **building** this attacker. A consequence row helps anyone assessing
whether their own attacker model is doing any work — which is the difference
between a private development checklist and a transferable instrument.

## Recommended approach

**Derive and commit the rows before scoring them**, exactly as the original eight
were, so the additions cannot be reverse-fitted to flatter the result that
prompted them. Write the definitions and their evidence bars in one commit; score
the model in a second.

### Row A — evidential provenance

**What it asks:** what proportion of the model's behavioural parameters are
traceable to an external, dated, third-party artefact, as against declared by the
modeller?

**Why it is not the row Marc first proposed.** The instinctive phrasing —
*is the CTI-derived model an upgrade on prior worked examples?* — should be
rejected on two grounds. It is comparative and self-scored, so every author
answers yes, which is precisely the reverse-fitting the criterion exists to
prevent. And it welds together two things that separate cleanly: whether the
behaviour is *evidenced*, and whether the evidence *changes anything*. Provenance
without consequence is bookkeeping; consequence without provenance is a
differently-arbitrary attacker. Score them apart and the pair becomes an argument.

**How to score it honestly.** The declared-value ledger already carries tier
badges, so this is largely an aggregation rather than new judgement. Expect the
result to be *modest*: the transition weights are corpus-derived, the duration
catalogue is mixed-tier, and the outcome overlay, the rationality exponent, the
learning capability and the forgetting fraction are all declared judgement. A row
that scores the project roughly a third externally attested is far more credible
than a binary claim to CTI-groundedness, and it is the honest answer.

### Row B — evaluative consequence

**What it asks:** does substituting this attacker for the incumbent, on the same
substrate, change the evaluation's *ordering* of defences, the *magnitude* of
their measured effect, or the *recommendation* a practitioner would draw?

**Three graded outcomes**, which should be fixed before scoring: magnitude only
(the same defences win, by different margins); ordering (the ranking changes);
recommendation (the top-ranked mechanism changes). The comparative experiment
reached the third, at the operating mutation interval, directionally at ten seeds.

**The caveats travel with the row, not in a footnote.** Ten seeds supports a rank
comparison and not a significance test; the effect is interval-dependent and
attenuates once mutation pressure is relaxed; and the whole result is bounded by
the tactic-to-verb mapping remaining a chosen input parameter rather than a
fidelity claim.

### Scoring and placement

1. **Do not renumber the existing eight.** They are cited by number across the
   implementation records, the experiment findings and the handoff chain.
   Add the rows as A and B, or as a separate short section, and say explicitly that
   they are **this project's addition** rather than derived from the three source
   surveys — the same flag the original axis synthesis carries.
2. **Note the axis-independence problem while editing.** The eight rows are not
   independent and two are in direct tension: both built modulators narrow
   traversal, so improving the incentive or learning rows provably degrades the
   plurality row. The scorecard's row-counting summary implies an additive scale
   the axes do not support. One paragraph near the badge definitions fixes it.
3. **Consider a fifth badge.** Three axes sit at DESIGNED for materially different
   reasons — one because an outcome was never shown, two because a swept,
   ablatable mechanism was shown *not* to help. A measured negative is a result and
   an unevidenced outcome is an absence; one badge for both loses that. The
   criterion already argues the distinction in prose without encoding it.

## Validation gate

Done when both rows exist with their definitions and evidence bars committed
*before* their scores; both are scored against the current evidence; the
row-counting summary no longer implies an additive scale; and the additions are
flagged as this project's synthesis.

## Hard constraints

- **Derive before scoring**, in separate commits.
- **No existing badge is re-decided** by this work.
- **Do not renumber axes 1–8.**
- Envelope-not-actor phrasing; Australian English; never push.

## Reading list

- `docs/implementation/apt_model_criterion.md` §(a) for how the original axes were
  derived and flagged, §(b) for the badge definitions, §(g) for where the
  consequence result currently lives for want of a row to hold it.
- `docs/implementation/pipeline/ogasp/experiment_02_findings.md` — the consequence
  evidence and its caveats *(reachable only after the reconciliation handoff)*.
- `docs/implementation/declared_value_provenance.md` — the tier badges Row A
  aggregates.
