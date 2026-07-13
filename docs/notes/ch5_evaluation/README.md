# ch5_evaluation — notes feeding the Evaluation & Results chapter

## What this chapter does

The evaluation chapter is the **empirical validation** — the part that converts the defended design into a demonstrated (or honestly negative) result. Its rules: results on shared ground (the inherited simulator's baseline and metrics are this work's benchmark; comparability discipline applies), comparison never skipped (even where the profiled attacker poses a new problem, the inherited procedural attacker is the adapted baseline that anchors the comparison), and an **ablation habit** — which component of the behavioural model actually moves the outcome: the objective conditioning, the timing layer, the reset semantics? The chapter reports outcomes against the pre-declared burden of proof rather than sympathetically: ranking stability across sweeps, divergence from the baseline attacker, and the negative-result disposition if either fails. (Whole-document guidance: [`../_writing_guide.md`](../_writing_guide.md).)

What lands here: *experimental-design arguments and results framing* — what the evaluation must demonstrate and why, metric and protocol defences, and (once the experiments run) the framing of what was found. Rubric-gated ([`../../workflows/notes_rubric.md`](../../workflows/notes_rubric.md)).

Current notes: [`evaluation_burden.md`](evaluation_burden.md) — the two-part burden of proof (ranking stability across swept parameters, and divergence from the baseline attacker) and the pre-declared negative-result disposition.
