---
status: findings (2026-09-20: the body section was cut; the table leads Appendix C as tab_C-0a and no §5.1 prose is owed — see the overhaul handoff's Ruling) — the §5.1 re-run read 2026-09-17; the four fragments and the appendix figure landed the same day; §5.1's prose is Marc's dictation (overhaul brief D2), owed
created: 2026-09-17
topic: "The §5.1 re-run: chapter 4's three declared inputs, each moved across its band at the chapter's pins (100 seeds, v2_partial, the failure-only overlay, the targeted objective, the quasi-periodic regime, 15 000 s), under no defence and the random scheme at both intervals — what carries the chapter and what does not"
---

# §5.1 Sensitivity analysis — the re-run at the reported configuration

**Design:** [`../../../handoffs/2026-09-17_ch5_s51_sensitivity_overhaul.md`](../../../handoffs/2026-09-17_ch5_s51_sensitivity_overhaul.md)
§D7. **Workspace:** `data/results/ch5_s51_sensitivity/` (gitignored but for the
recorder, the analyser, `design.json`, `numbers.json` and `sim05_check.json`):
`run_sweep.py` → `runs.jsonl` (33 000 runs, 77 min on seven workers, zero
errors); `analyse.py` → `numbers.json`, `per_run.csv`, the four fragments under
`docs/thesis/tables/` and `preview_families.png`;
`tools/ch5_sensitivity_figure.py --csv … --stem fig_C-1a_sens_dwell_family` →
the App. C.1 figure. The analysis is a reader; the only RNG is the seeded
bootstrap that shadows the chapter's interval.

## 1. Configuration and sanity

Twenty-two points on the movement arm, five profiles, three conditions (no
defence; `random` over the seven mechanisms at 200 s and at 2 000 s), 100 seeds
shared: 330 cells at 100 runs each, no error rows, no `max_events`
termination. The pins are the defended corpus's, imported from its recorder
rather than retyped. **The centre point reproduces the defended corpus run for
run:** all 1 500 centre rows (five profiles × three conditions × 100 seeds)
match `ch5_defended/runs.jsonl` on hosts, termination time and action count
(`sim05_check.json`: 1 500 compared, 0 mismatches). So every number here is on
the same footing as every number in §5.3–§5.5.

The declared point the sweep moves from is the chapter's overlay's own recipe
(`v4_failure_only`: γ 0.25, δ 0.25, z 0.1), asserted at start against the
registry, whose reproduction check passed the same day (`rules.py --check`: no
differing cell in any version). The dwell bands are the catalogue's
(`rate_feasibility_study.py ANCHOR_BANDS`), the family factor multiplying every
tactic in the family with the per-tactic multipliers riding along. The
Erlang-4 source was checked to change a run at k = 4 and to reproduce the
centre bit for bit at k = 1 (same derived-seed stream), so the shape
substitution is the only thing that differs on those rows.

## 2. The criterion, and one note on the interval

Fixed in the recorder's docstring before the first run: a point is *inert*
under a condition when its pooled mean of distinct hosts reached lies inside
the interval at the declared value; *moved* otherwise; the floor is *zero by
structure* if and only if its rows are bit-identical to the centre's. Pooling
is the four objective profiles (400 runs per cell); the aggregate is read
beside and never pooled in. A family is inert when both band ends are inert
under every condition.

The docstring named a seed bootstrap for the interval; the analyser reports
the chapter's interval (the suite's `mean_ci`, mean ± 1.96 SEM, the same one
every §5.3–§5.5 table prints) as primary and computes the bootstrap beside it.
**No verdict on the four-profile pooling differs between the two forms.** Two
aggregate-arm cells do (γ 0.5 and the γ 0.5 / δ 0.1 corner at 2 000 s: inert by
the chapter's interval, a hair outside the bootstrap's); they are on the
aggregate only and change nothing reported.

**What 400 runs per cell does to the criterion.** The interval at the declared
value is about ±0.4 hosts under no defence and ±0.2 under the 200 s defence,
so the criterion detects a shift of half a host. At ten seeds it detected a
shift of about a host and a half. Three of the four families now register
*moved* somewhere; the honest reading is therefore the magnitude beside the
verdict, and the analyser reports hosts lost per doubling of the family's
dwell for exactly that reason. The verdict column is kept as the criterion
says; nothing was re-cut after the numbers were seen.

## 3. The dwell times (Table 5.1's first group; App. C.1)

Hosts reached at band low / declared / band high, four profiles pooled, and
hosts lost per doubling of the family's dwell:

| Family (band) | No defence | 200 s | 2 000 s | Lost per doubling (none / 200 / 2 000) |
|---|---|---|---|---|
| scan-shaped (×0.5–×2) | 8.6 / 8.1 / 7.3 | 2.7 / 2.1 / 1.5 | 8.2 / 7.4 / 6.3 | 0.7 / 0.6 / 1.0 |
| exploit-shaped (×0.5–×2) | 8.3 / 8.1 / 7.9 | 2.2 / 2.1 / 1.9 | 7.7 / 7.4 / 7.4 | 0.2 / 0.1 / 0.1 |
| **low-and-slow (×0.25–×4)** | **13.4 / 8.1 / 3.0** | **7.5 / 2.1 / 0.3** | **14.7 / 7.4 / 2.0** | **2.6 / 1.8 / 3.2** |
| objective (×0.5–×2) | 8.5 / 8.1 / 7.4 | 2.3 / 2.1 / 1.7 | 8.4 / 7.4 / 6.6 | 0.6 / 0.3 / 0.9 |

Verdicts by the criterion: exploit-shaped **inert** at both ends under every
condition; low-and-slow **moved** at both ends everywhere, CI-separated
everywhere; scan-shaped and objective **moved** at one or both ends under
every condition, by well under a host across a fourfold range, CI-separated
at the ×2 end only. The relationship for the low-and-slow family is monotone
and close to linear in the logarithm of the multiple (the figure); no
threshold, no reversal. Under no defence, 26 % of runs reach the target at
×0.25 against 9 % at the declared value and none at ×4.

**Against the record** (`rate_feasibility_study.md` §10, ten seeds, one
scheme, pre-restoration): the low-and-slow reading was 7.8 / 4.6 / 1.8; at the
chapter's pins it is 13.4 / 8.1 / 3.0 — the same shape, higher throughout
because the restored substrate and the targeted objective let the attacker
reach more. The record's "the other three are inert" was a ten-seed
statement; at 100 seeds one of the three is inert and two shift by a fraction
of what the low-and-slow family does. **The concentration claim sharpens
rather than weakens:** the family whose provenance is weakest carries three to
five times the per-doubling sensitivity of the next family and about fifteen
times the exploit-shaped family's, under every condition.

## 4. The draw's shape (Table 5.1's fifth row; App. C.2)

Paired Erlang-4 minus exponential, four profiles, 400 pairs per cell:

| | No defence | 200 s | 2 000 s |
|---|---|---|---|
| at the declared dwell | −0.01 ± 0.06 (330 ties) | **−0.24 ± 0.22** (170 lower / 91 tied / 139 higher) | −0.06 ± 0.38 |
| at low-and-slow ×4 | 0.00 ± 0.05 | −0.04 ± 0.07 | −0.15 ± 0.15 |

The concentrated draw is inert under no defence at both dwells (a third to
four fifths of the pairs tie). Under the 200 s defence at the declared dwell
it reaches fewer hosts, a quarter of a host on 2.1, with its interval clear
of zero, and completes thirteen fewer actions per run (−13.3 ± 1.8). At the ×4
corner the attacker is at the floor (0.3 hosts) and the difference is too
small to separate; at 2 000 s the corner difference sits on the boundary
(−0.15 ± 0.15) and is not claimed. Every defended difference is negative.

**Against the record** (§10 of the rate study: inert everywhere but the ×4 ×
200 s corner, −0.28 ± 0.19): the mechanism is the same — a long draw is
likelier to be cut by a mutation, and the exponential's mass of very short
dwells is what lets the attacker slip an action between mutations — but at
the chapter's pins it shows *at the declared dwell* under the 200 s defence
and not at the corner, because the corner is now at the floor. The claim the
chapter may carry: the shape is inert where no defence acts; under mutation
pressure the more faithful shape costs the attacker a little, never helps it.

## 5. The mapping (Table 5.1's second group; App. B.7)

Forced-total `v1_ckc_total` at the declared point against the partial mapping:
0.15 hosts against 8.13 under no defence (blocked fraction 0.58 against 0.24),
0.09 against 2.07 at 200 s, 0.12 against 7.42 at 2 000 s; the target is never
reached under the forced-total mapping. The record's verdict stands at the
chapter's pins: the forced-total mapping runs a tightly ordered machine in an
unordered way and stalls on preconditions. The partial mapping is a declared
input, and the effectiveness claims carry it as such.

## 6. The failure matrix (Table 5.1's third group; App. C.3)

At every band end of every rate, and at all four corners of the two rates,
under every condition, the pooled mean sits inside the interval at the
declared value: the largest shift anywhere is 0.18 hosts (the γ 0.1 / δ 0.1
corner at 200 s: 2.24 against 2.07). **The floor is zero by structure:** its
rows are bit-identical to the centre's on every recorded field, because no
profile net carries a jump of three stages (App. B.6's bands figure). The
nine rules were not moved.

**Against the record** (`weight_sensitivity_study.md` §6.2, fixed-dwell
regime, both mappings, ten seeds): δ was the most influential (101 % on
actions per host) and γ moved outcomes on the forced-total mapping. At the
chapter's pins, on the mapping the chapter runs, neither rate moves distinct
hosts reached, and the floor's inertness is reproduced exactly. The record's
influence ranking was a fact about the rejected mapping and the superseded
regime; the chapter's fact is that the distance term's numbers do not carry
it.

## 7. What §5.1 may now say (content for Marc's three paragraphs, brief D2)

- **The one input the chapter's claims are exposed to is the low-and-slow
  family's dwell.** It is held at its declared value (Table 5.3's row), and
  every claim that could turn on it says so. Nothing else in the model's
  declared inputs moves the outcome by more than a host across its band.
- **The concentration sentence:** the model's timing sensitivity sits in the
  family whose provenance is weakest; the two families priced by the
  simulator carry a fraction of it (one is inert; the other shifts by under a
  host across a fourfold range), and the objective family likewise.
- **The shape:** inert where no defence acts; under mutation pressure the
  concentrated draw costs the attacker a little, never helps it.
- **The mapping:** a comparison, not a band; the alternative stalls.
- **The failure matrix:** neither rate moves the outcome at any band end or
  corner; the floor cannot, on this corpus; the rules were held.
- **Not sayable:** that the scan-shaped and objective families are inert
  (they are not, at this power); anything about the mutation interval (a
  factor, §5.2's); a per-profile ordering.

## 8. What changed in the floats

- `tab:parameter-register` → generated `tab_5-1a_declared_inputs.tex`: ten
  rows, three groups, four columns in words; the effect column is the
  analyser's, from the criterion.
- `fig:sens-dwell-anchor` → App. C.1 as `fig_C-1a_sens_dwell_family`, the
  low-and-slow family under no defence and at 200 s (13.7 / 8.3 / 3.0 and
  7.9 / 2.2 / 0.3 with the aggregate included in the tool's pooling, 500
  runs per point; the four-profile numbers are the table's).
- `tab:anchor-sensitivity`, `tab:shape-substitution` → generated fragments;
  `tab:decay-sensitivity` filled from the placeholder. All three carry the
  DRAFT-STATE caption mark for the voice pass.
- **The run count.** The §5.2 redraft (2026-09-17, handoff
  `2026-09-17_ch5_s52_setup_critique.md` §J) carries Marc's ruling that the
  thesis reports a thousand seeds per cell, with a hundred as the working
  preliminary pass. This sweep is at the hundred-seed corpus the chapter's
  floats are currently argued from, and matches it run for run. When the
  defended corpus is re-run at a thousand seeds, this sweep is re-launched
  from it (the recorder takes `SEEDS`, the pins and the cell from
  `ch5_defended/run_corpus.py`, so nothing is retyped): ~330 000 runs, about
  thirteen hours on seven workers at the rate measured here (0.14 s per run
  per worker), and the fragments regenerate by the same command.
- The stale `DistanceKernel.delta_ratio = 0.5` dataclass default at
  `rules.py:97` differs from the declared 0.25; nothing on the declared path
  reads it (the loader takes the JSON). Flagged, not changed.
