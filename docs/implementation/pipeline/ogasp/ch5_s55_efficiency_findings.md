---
status: findings — preliminary read 2026-09-17, landed the same day (Marc's instruction: iterate §5.3.2 → §5.5 in sequence with preliminary numbers) via tools/ch5_efficiency_figures.py; captions DRAFT STATE, voice pass owed
created: 2026-09-17
topic: "The §5.5 read of the defended corpus: what each defence condition costs on both sides — the defender's reconfiguration occupancy against the suppression it buys, on both attackers; where the attacker model's time goes under each condition; and the event-wise effort per host reached on both arms"
---

# §5.5 Defence efficiency — the preliminary read

**Design:** [`../../../handoffs/2026-09-17_ch5_s532_s55_defended_runs.md`](../../../handoffs/2026-09-17_ch5_s532_s55_defended_runs.md)
§2. **Workspace:** `data/results/ch5_defended/` (gitignored): `analyse.py` →
`numbers.json` §s55, `preview_fig57_58.png`. Configuration and sanity are in
the §5.3.2 record ([`ch5_s532_adaptivity_findings.md`](ch5_s532_adaptivity_findings.md)
§1); suppression is as defined in the §5.4 record
([`ch5_s54_effectiveness_findings.md`](ch5_s54_effectiveness_findings.md)).
The defender-side measures are `measures.py`'s `disruption_ledger`
(occupancy = the union of the mutation execution windows over elapsed time;
executions per 1 000 s), read identically on both arms from the substrate's
own MTD execution record; the attacker-side split is `cost_ledger` on the
model (dwell, MTD penalty, residual) with the served dwell further divided
into visits that returned an outcome and visits a mutation cut short.

## 1. Figure 5.7 — the frontier

Suppression against occupancy, one marker per condition per arm, at each
interval. Occupancy is set by the tempo and the mechanism's execution time,
not by the attacker: at 200 s the two arms' occupancies agree to 0.02 on every
condition (IP shuffle 0.50 / 0.50, complete topology 0.55 / 0.55, port 0.36 /
0.35, user 0.11 / 0.10), and at 2 000 s they are 0.01–0.06 on both. The
horizontal axis is therefore the same axis on both arms, which is what the
placeholder claimed for it and the corpus confirms.

| 200 s | occupancy | model suppression | baseline suppression |
|---|---|---|---|
| complete topology | 0.55 | 0.96 | 0.41 |
| IP shuffle | 0.50 | 0.96 | 0.68 |
| host topology | 0.50 | 0.96 | 0.40 |
| OS diversity | 0.42 / 0.40 | 0.07 | 0.64 |
| alternative | 0.40 | 0.72 | 0.39 |
| random | 0.40 | 0.75 | 0.33 |
| port shuffle | 0.36 / 0.35 | 0.20 | 0.90 |
| service diversity | 0.36 / 0.35 | 0.36 | 0.91 |
| user shuffle | 0.11 / 0.10 | −0.14 | −0.07 |

Spearman correlation of suppression with occupancy across the nine
conditions: model 0.75 at 200 s and 0.77 at 2 000 s; baseline 0.05 and −0.25.

Two things are in the figure.

1. **The shape of the trade inverts with the attacker.** Against the model,
   what a defence buys rises with what it spends: the three most occupying
   mechanisms (the network layer, 0.50–0.55 of the run) are the three that
   work, and the cheap ones do nothing or worse. Against the baseline the
   frontier is flat-to-falling: its two best mechanisms (service diversity,
   port shuffle) are among the cheaper ones at 0.35, and the most occupying
   (complete topology, 0.55) buys 0.41. This is the design comment's
   recorded result ("the SHAPE of the trade inverts") returned at the
   chapter's pins, and its defender-side axis is arm-invariant, which is why
   it is the more robust of the chapter's two cross-arm claims.
2. **At 2 000 s the frontier collapses to a point cloud.** Every condition
   occupies 0.01–0.06 of the run and only IP shuffle (model, 0.33) and service
   diversity (baseline, 0.30) are separated from zero; the two arms' best
   buys at the lineage tempo cost the same (0.04–0.06) and are different
   mechanisms. The panel is drawn on its own x range (0–0.08) so the cloud
   is legible; the y axis is shared.

## 2. Figure 5.8 — where the attacker model's time goes

| 200 s | completed activity | activity cut short | imposed delay | actions per run | interrupts per run |
|---|---|---|---|---|---|
| no defence | 1.00 | 0 | 0 | 317 | 0 |
| IP shuffle, topology shuffles | 0.71 | 0.19 | 0.10 | 355–356 | 75 |
| port, OS, service | 0.80 | 0.13 | 0.07 | 336–341 | 53–54 |
| random, alternative | 0.78–0.79 | 0.14 | 0.08 | 347–348 | 55–56 |
| user shuffle | 1.00 | 0.00 | 0.00 | 316 | 0.8 |

At 2 000 s: completed 0.97–0.98 everywhere, cut short 0.01–0.02, delay 0.01.

1. **The remainder segment is structurally empty.** The placeholder's third
   segment ("the remainder") is the ledger's residual, which is ≈ 0 under the
   token-always-in-a-place contract (S3-R): dwell plus penalty is the whole
   run. The segment drawn in its place is activity a mutation cut short — the
   ledger's re-work term — which is the half of the cost the caption should
   have named: a mutation costs the attacker the visit it was in (0.13–0.19 of
   the run at 200 s) more than it costs it the delay it then imposes
   (0.07–0.10).
2. **The split is the interrupt count's, not the mechanism's.** The three
   network-layer conditions, which interrupt every one of the 75 mutations,
   have the same split to two decimals; the application layer and the
   schemes, which interrupt 53–56, have the same split as each other. What
   differs between the families is not how much time the defence takes from
   the attacker but what the attacker has when it resumes: under the network
   layer the position is gone (blocked fraction 0.80–0.83, §5.4 record), under
   the application layer it is not (0.23–0.25). The time decomposition is
   therefore not where the effectiveness difference lives, and the caption's
   "whether a defence works by making the attacker do more, or by making what
   it already does take longer" resolves as: neither; it works by what it
   destroys.

## 3. Table 5.8 — cost by condition and attacker, at 200 s

Actions and successes per host reached are cell totals (all actions over all
hosts in the cell's runs) with a seeded bootstrap interval, so a run that
reaches one host does not dominate; a success on the baseline is a compromise
event (its record carries no other verdict), so its successes per host is
the structural 1.0.

| condition | actions per host, baseline | model | successes per host, model |
|---|---|---|---|
| no defence | 49 [47, 52] | 39 [37, 41] | 20 [19, 21] |
| IP shuffle | 143 [128, 161] | 1 128 [933, 1 402] | 144 [121, 175] |
| complete / host topology | 96 / 95 | 975 / 1 024 | 144 / 154 |
| port shuffle | 538 [418, 709] | 52 [50, 56] | 25 |
| OS diversity | 144 [122, 172] | 44 [42, 47] | 22 |
| service diversity | 730 [597, 924] | 65 [62, 69] | 32 |
| random / alternative | 93 / 110 | 168 / 151 | 46 / 44 |
| user shuffle | 48 [45, 50] | 34 [32, 36] | 18 |

1. **Effort per host is the family split again, event-wise and on both
   arms.** The network layer makes the model spend 25–29 times the unopposed
   actions per host (1 000+ against 39) and the baseline 2–3 times; the
   application layer makes the baseline spend 3–15 times (service diversity
   730 against 49) and the model 1.1–1.7 times. The same defences make each
   attacker work hardest, and they are different defences.
2. **Successes per host on the model rise sevenfold under the network layer**
   (20 → 144–154): the attacker keeps succeeding at scans and enumerations
   on positions it then loses, so successes accumulate without hosts. This is
   the §5.3.1 saturation reading (successes per host is a churn measure) in
   its defended form.
3. **User shuffle costs less than no defence on both arms** (34 against 39;
   48 against 49), consistent with its negative suppression (§5.4 record §1
   item 2); open there.
4. Occupancy and executions per 1 000 s are identical across arms to the
   second decimal (5.0 mutations per 1 000 s, occupancy 0.10–0.55), which is
   the arm-invariance the column pair exists to show; the 2 000 s rows
   (0.5 per 1 000 s, occupancy 0.01–0.06) are in `numbers.json` and not in
   the table.

## 4. Against the record

| quantity | record | here |
|---|---|---|
| the frontier's shape inverts with the attacker (design C9) | recorded at fewer seeds, pre-restoration | returned at the chapter's pins: ρ(occupancy, suppression) 0.75 model against 0.05 baseline |
| the remainder segment | placeholder's third segment | structurally ≈ 0 (S3-R); replaced by activity cut short, the caption edited |
| confusion penalty on the inherited arm (D-37) | no record row | still none; the decomposition is the model's only, the cross-arm comparison event-wise in Tab. 5.8 |
| quality of service / performance overhead | not instrumentable | unchanged; not in any float |

## 5. What the floats needed changed (APPLIED 2026-09-17)

- Fig. 5.7: two lettered panels, one per interval, because occupancy is set
  by the tempo; the 2 000 s panel on its own x range; model labels right of
  the marker and baseline labels left, spread so none collide; the key
  under the panels, not inside panel (a) where the user-shuffle markers sit.
- Fig. 5.8: the third segment is activity cut short, not the remainder; two
  panels, one per interval; values printed where a segment is ≥ 0.045.
- Tab. 5.8: at 200 s only; the 2 000 s rows are in the record.

## 6. Validation

Every cell at 100 (400 pooled); Fig. 5.7 and Fig. 5.8 fit the page box; every
printed segment value and every table cell is read from `numbers.json` §s55;
the baseline's successes per host is the structural 1.0 in every row and the
footnote says so. Open: the user-shuffle attribution (§5.4 record).
