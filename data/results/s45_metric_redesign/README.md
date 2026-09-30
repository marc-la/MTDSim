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

## 2026-09-30: disruption from the mechanism

Behind `docs/implementation/disruption_mechanism.md`.

- `disruption_from_mechanism.py OUT.json [PREVIEW.png]`: attack actions blocked per
  deployment and the time to resume a blocked action (from the deployment's
  completion to the next run of the same action), against the usual gap with no MTD;
  writes the preview of the proposed Figure 5.3 (`preview_fig53_resume.png`).
  It supersedes `blocked_resume.py`, which measured from the blocked record's end
  (penalty included on the APT model only) and used the baseline's
  `termination_time` (always the horizon).
- `event_rates_around_deployment.py OUT.json`: actions, interrupts, failed actions
  and compromises per minute from 5 min before to 15 min after each deployment, with
  the same moments on the no-MTD run. Note: its baseline live time still uses
  `termination_time` (see the record, M3); read its baseline rows as indicative.

**2026-09-30, after the metric change.** `disruption.py` is retired;
`data/results/ch5_defended/time_lost.py` is the reader (attack actions blocked per run,
time lost per MTD deployment). `rate_ratio.py` and `next_compromise.py` import the
retired module and run only against the tree before this change (git history).
`time_to_next_compromise.py` is the dry run the reader grew from.
