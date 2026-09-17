---
status: findings — preliminary read 2026-09-17, landed section by section the same day (Marc's instruction: iterate §5.3.2 → §5.5 in sequence with preliminary numbers); §5.4.1 landed via tools/ch5_effectiveness_figures.py; captions DRAFT STATE, voice pass owed; §5.4.2 and §5.4.3 appended as they land
created: 2026-09-17
topic: "The §5.4 read of the defended corpus: what each defence condition does to the attacker model's breadth, delay and blocked fraction at both tempos and whether the answer depends on the profile (§5.4.1); the same conditions against the inherited attacker and the two orderings (§5.4.2); the lineage's headline claims re-run under both attackers (§5.4.3)"
---

# §5.4 Defence effectiveness — the preliminary read

**Design:** [`../../../handoffs/2026-09-17_ch5_s532_s55_defended_runs.md`](../../../handoffs/2026-09-17_ch5_s532_s55_defended_runs.md)
§1–§2. **Workspace:** `data/results/ch5_defended/` (gitignored): `run_corpus.py` →
`runs.jsonl` (30 200 runs); `analyse.py` → `numbers.json` §s541, §s542, §s543,
`preview_fig55.png`, `preview_fig56.png`. Configuration and sanity are in the
§5.3.2 record ([`ch5_s532_adaptivity_findings.md`](ch5_s532_adaptivity_findings.md)
§1); nothing here re-derives them. Every measure is the shipped suite's; the
suppression statistic and its interval are the analyser's (below).

**Suppression**, everywhere in §5.4: $1 -$ mean hosts reached under the
condition / mean hosts reached with no defence, on cell means, with a seeded
bootstrap interval on the ratio (2 000 resamples of each cell). Hosts reached is
`MovementRunResult`'s distinct compromised hosts on the model and the uuid-counted
compromise events on the baseline. The no-defence cell is one cell (interval 0),
read against both intervals.

## 1. §5.4.1 — the conditions against the attacker model

### Figure 5.5 and Table 5.5

The model pooled over its four profiles (400 runs per cell; 8.13 ± 0.42 hosts
with no defence), ordered by suppression at each interval. Adjacent conditions
whose intervals overlap carry the dagger in the table.

| condition | 200 s suppression | hosts | runs with no compromise | delay to first (s) | blocked | 2 000 s suppression | hosts | blocked |
|---|---|---|---|---|---|---|---|---|
| no defence | — | 8.13 | 0.04 | 2 100 | 0.24 | — | 8.13 | 0.24 |
| IP shuffle | 0.96 [0.95, 0.97] | 0.32 | 0.76 | 6 423 | 0.83 | 0.33 [0.27, 0.38] | 5.47 | 0.48 |
| host topology shuffle | 0.96 [0.95, 0.96] | 0.35 | 0.71 | 6 571 | 0.80 | 0.17 [0.11, 0.22] | 6.77 | 0.39 |
| complete topology shuffle | 0.96 [0.95, 0.96] | 0.37 | 0.72 | 7 059 | 0.80 | 0.16 [0.09, 0.22] | 6.83 | 0.39 |
| random (seven) | 0.75 [0.72, 0.77] | 2.07 | 0.17 | 4 651 | 0.64 | 0.09 [0.02, 0.15] | 7.42 | 0.34 |
| alternative (seven) | 0.72 [0.69, 0.74] | 2.31 | 0.13 | 4 511 | 0.62 | 0.03 [−0.04, 0.09] | 7.92 | 0.29 |
| service diversity | 0.36 [0.31, 0.41] | 5.20 | 0.05 | 2 277 | 0.23 | 0.04 [−0.04, 0.10] | 7.84 | 0.23 |
| port shuffle | 0.20 [0.13, 0.26] | 6.51 | 0.05 | 2 295 | 0.24 | 0.00 [−0.07, 0.07] | 8.11 | 0.24 |
| OS diversity | 0.07 [0.00, 0.14] | 7.56 | 0.04 | 2 324 | 0.25 | −0.01 [−0.08, 0.06] | 8.21 | 0.24 |
| user shuffle | −0.14 [−0.22, −0.05] | 9.23 | 0.03 | 2 082 | 0.24 | −0.04 [−0.11, 0.04] | 8.42 | 0.24 |

Interrupts per run at 200 s (75 mutations): the three network-layer conditions
75 of 75 in every profile; the schemes 52–60; port, OS and service 46–62;
user shuffle 0.2–1.3.

Four things are in the table.

1. **Three tiers at 200 s, and the tiers are the defence families.** The
   network layer (IP shuffle and the two topology shuffles) removes 96 % of the
   attacker's breadth and denies it every host in 71–76 % of runs; where it does
   compromise, the first compromise comes three times later (6.4–7.1 ks against
   2.1 ks). The two schemes over the seven mechanisms sit at 0.72–0.75. The
   application layer (service diversity 0.36, port shuffle 0.20, OS diversity
   0.07, whose interval touches zero) barely postpones the first compromise
   (2.3 ks) and leaves the blocked fraction at the no-defence level
   (0.23–0.25). The three network-layer conditions are one effect: their
   intervals overlap each other and nothing else; the blocked fraction is
   where the mechanism shows, 0.24 → 0.80–0.83, which is the position-severance
   reading the design comment predicted (0.15 → 0.72 in the record, at fewer
   seeds and the earlier overlay).
2. **User shuffle is not a null: it is negative.** 9.23 hosts against 8.13, and
   the interval excludes zero at 200 s (−0.14 [−0.22, −0.05]). It interrupts
   almost nothing (0.8 visits per run), so the effect is not through the
   interrupt path. The measurement is what it is; the attribution is open.
   The declared choice that could carry it: the mechanism re-rolls the user
   set on hosts, and the model's brute-force and enumerate-host activities read
   that set — a re-roll mid-campaign may hand the attacker a weaker set than
   the one it started against. Flagged for the trace tool; no sentence in
   the prose may say why until it is traced. *To verify.*
3. **Not profile-dependent at 200 s.** Every profile orders the conditions the
   same way; the spread of the point estimate across the four profiles is
   ≤ 0.05 on the network layer and the port and user conditions, 0.10–0.15 on
   the schemes and service diversity, where double extortion is suppressed
   most (0.81–0.82 on the schemes against 0.67–0.74) and the no-realised-objective
   profile least. The aggregate arm sits inside the four on every condition.
   The blocked fraction differs by profile under the network layer (0.65–0.67
   exfiltration, 0.93–0.94 double extortion) without the suppression differing,
   because exfiltration's hosts are already 7.4 unopposed and the profile keeps
   trying where the others do not.
4. **At 2 000 s everything attenuates and the tiers collapse into two.** Only
   the network layer remains separated from zero (IP shuffle 0.33, the topology
   shuffles 0.16–0.17); random is 0.09 [0.02, 0.15]; every other condition's
   interval includes zero and every condition but IP shuffle overlaps a
   neighbour. Eight mutations in a 15 000 s campaign reach the attacker eight
   times, and its breadth is already 5.5–8.4 hosts of the unopposed 8.1. This
   is what the interval-as-crossed-factor ruling (Q3) was for: the 200 s
   ordering is a property of the tempo, and at the lineage's own interval the
   defence landscape against this attacker is mostly flat. The profile spread
   widens here (0.22 on IP shuffle: double extortion 0.47, no realised
   objective 0.20), but the intervals widen with it and no profile's ordering
   inverts another's on a separated pair.

### Against the record

| quantity | record | here |
|---|---|---|
| network-layer blocked fraction | 0.15 → 0.72 (design comment, 50 seeds, earlier overlay) | 0.24 → 0.80–0.83 |
| the two network-layer mechanisms one effect | 0.721 vs 0.725 | IP 0.96, complete 0.96, host 0.96, intervals overlapping |
| application layer "barely reaches" the model | blocked stays ~0.16 | blocked stays 0.23–0.25; but service diversity still suppresses 0.36 and port shuffle 0.20 at 200 s — "barely" is the blocked fraction's reading, not breadth's |
| schemes over the seven (Q1) | never run | random 0.75, alternative 0.72 at 200 s: below the network-layer singles they contain, because a rotation spends 4 of 7 turns on the application layer |
| user shuffle | no record | negative suppression at 200 s; open (item 2) |

### What the floats needed changed (APPLIED 2026-09-17)

- Fig. 5.5 is four panels, not two: the interval is a crossed factor (Table
  5.2; ruling Q3), and the 2 000 s row is the finding that the ordering is
  the tempo's. The aggregate is drawn as the fifth series, as the table of
  §5.3.1 lists it.
- Tab. 5.5: the placeholder's "denied all hosts" share and the delay column's
  censored share are the same number (a run with no compromise has no first
  compromise), so one column carries both, named for what it is. The
  no-defence reference is one row, since it is one cell.
- The key wraps under the panels: five profile names in one row ran 0.4 cm
  past the page box.

## 2. §5.4.2 — the same defences against both attackers

*Owed: appended when the section lands.*

## 3. §5.4.3 — the lineage's headline claims

*Owed: appended when the section lands.*

## 4. Validation

§5.4.1: every cell at 100 (400 pooled); Fig. 5.5 fits the page box
(15.8 × 9.9 cm); every caption fact printed by the generator matches
`numbers.json`; the table's footnote spans its seven columns. The user-shuffle
attribution (§1 item 2) and the interrupt-tally cross-check (§5.3.2 record
§1) are open.
