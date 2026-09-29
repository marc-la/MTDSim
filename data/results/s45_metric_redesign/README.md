# §4.5 metric redesign — dry runs (2026-09-29)

Read-only dry runs behind rulings E and F of
`docs/handoffs/2026-09-29_s45_equation_clarity.md`. None writes a tracked number.
Run from the repo root.

- `stealth_count.py`: attack confidentiality under a count-in-window scan-detector
  rule (N actions within T s; Snort's default is 5 in 60 s), on the no-defence corpus
  `ch5_s531_unopposed/runs.jsonl`.
- `rate_ratio.py [W]`: compromise rate in the W s after each deployment over the
  W s before, pooled per cell, with the same read on the no-defence run; time lost
  = W × (ratio with no defence − ratio under the defence). Default W = 1 000 s (I/2 at 2 000 s).
- `next_compromise.py`: the rejected alternative, the time from each deployment to
  the next compromise, censored at the next deployment.

The two deployment scripts read `ch5_defended/runs.jsonl` (4 GB) through
`disruption.load`, which takes a few minutes.
