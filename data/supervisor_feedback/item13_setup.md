# Item 13: the tactic-duration ablation under MTD (setup, for Marc's approval before launch)

## The question

Section 6.2 ¶3 explains why the service layer reduces the APT attacker model's NCR less than the baseline attacker's:
- a service-layer deployment disrupts an attacker only during an attack action;
- the APT attacker model's tactic durations keep it in unmapped tactics, which run no attack action.

The thesis has not tested this under MTD (T2: "We did not repeat this ablation under MTD"). Jin: "Run the model with unmapped tactics at 0 s, under IP shuffle and service diversity at 200 s."

## The design: one change, everything else as reported

| | |
|---|---|
| Change | The seven unmapped tactics take 0 s. The mapped tactics keep their declared means. This is the same catalogue as the first step of Appendix D.6 (`unmapped_zero`). |
| Held at the reported corpus's settings | mapping v2_partial, failure-only overlay, retrace on, targeted attack scenario, 15 000 s, vulnerability memory at rate 2 |
| Attacker | APT attacker model, $c_1$ to $c_4$. The baseline attacker is not re-run: it uses no tactic durations, so its reported rows stand. |
| Conditions | no MTD; IP shuffle at 200 s; service diversity at 200 s |
| Seeds | 0–999, the same 1 000 as every reported cell |
| Runs | 4 profiles × 3 conditions × 1 000 = **12 000** |

**Checks before any number is read.**
1. **Smoke check.** With the declared durations, seed 0 must reproduce the reported corpus's rows exactly for all three conditions.
2. **Determinism check.** The no-MTD rows must equal D.6's `unmapped_zero` rows seed for seed.

## Measures (two, both already defined in §4.5)

| Measure | Why | Reference at 200 s, declared durations |
|---|---|---|
| **NCR reduction**, averaged over $c_1$–$c_4$, 95 % interval | The outcome §6.2 explains | APT attacker model: IP shuffle 0.96, service diversity 0.36. Baseline attacker: 0.68, 0.92 |
| **Attack actions blocked per MTD deployment** | The mechanism ¶3 names | APT attacker model: IP shuffle 0.11, service diversity 0.17. Baseline attacker: 1.00, 0.99 |

## What the result would mean (fixed before the run, reported whichever way)

| Outcome | What it means for §6.2 |
|---|---|
| Under service diversity, **both** measures rise, with the 95 % intervals apart from the declared values | ¶3's explanation is **supported**: the time in unmapped tactics keeps service-layer deployments off its attack actions |
| Blocked per deployment rises, but NCR reduction does not | ¶3's mechanism holds, but it is **not what limits** the service layer's NCR reduction. ¶3 is reworded to the mechanism alone, and T2 keeps the rest as untested. |
| IP shuffle's NCR reduction stays above service diversity's | The host layer's lead does **not** depend on the time in unmapped tactics. This is consistent with item 2's attribution to the tactic-to-action mapping. |

**Known in advance.** With unmapped tactics at 0 s, no-MTD NCR rises (0.15–0.21 → 0.20–0.35 by profile; Table D.6). NCR reduction is relative to no-MTD NCR, so it can fall under every mechanism even when more attack actions are disrupted. That is why the mechanism is measured alongside the outcome.

## Where it is reported

- **Appendix D.** Merge D.4 (ablation studies) and D.6 (ablation of the tactic durations) into one section, *Ablation studies*:
  - §5.4's three tables first;
  - then the tactic-duration ablation: Table D.6 with no MTD, and the new table with MTD.
  - The disclosure that this ablation was chosen after the results (T7) stays.
  - D.5, the sensitivity analysis, stays a section of its own.
  - The labels move with their text, so no cross-reference breaks.
- **New table.** Two rows (IP shuffle, service diversity) × columns for the APT attacker model with declared durations, the APT attacker model with unmapped tactics at 0 s, and the baseline attacker, for each of the two measures.
- **Text that follows the result** goes on the §6.2 sheet with items 2 and 3:
  - §6.2 ¶3 (one clause citing the table);
  - T2 ("We did not repeat this ablation under MTD …");
  - T7 (post hoc);
  - ch7 l.9804 ("Our ablation of the tactic durations ran with no MTD", a proposal).

## Cost

- **Script:** about 30 min. It copies `run_duration_ranking.py`'s harness and keeps the event records, so `time_lost.py` computes blocked per deployment exactly as §4.5 defines it.
- **Compute:** about 35–60 min on 7 workers. Another session is using all 7 cores at present (`verify_ledgers.py`), so launch waits for it.
- **Analysis and table:** about 45 min.

**Not chosen:**
- All ten conditions at 200 s as a column in Table C.1b. That would be 44 000 runs over 2–3 h. Jin asked for two mechanisms.
- Time lost per MTD deployment as a third measure. It is cheap from the same records, but not needed for the question.
