---
status: durable — the verified statistics of the four L2 attack profiles at
        tactic-to-tactic resolution, under the size-matched null, per Marc's
        rulings of 2026-08-17. Supersedes tactic_resolution_restatement.md
        (kept as the drafting-session record it verifies).
created: 2026-08-17
updated: 2026-08-17
scope: L2 (GASP). Tool: tools/gasp_tactic_profile_stats.py (independent
       re-derivation). Gate: tests/l2_subgraph/test_gasp.py (size-matched
       transition-share check added; JSD unit corrected to bits).
---

# The four attack profiles at tactic-to-tactic resolution — verified statistics under the size-matched null

## 0. The rulings this record executes

Marc, 2026-08-17, at the §4.2.2 scrutiny and after reading
[`tactic_resolution_restatement.md`](tactic_resolution_restatement.md):

1. **Resolution.** The L2 unit speaks in **tactic-to-tactic attack
   profiles** — the tactic-pair transition structure §4.2.1 describes and
   L3 quotients into transitions — not in technique frequencies.
2. **Null.** The discrimination claim stands on the **most structurally
   rigorous null, not the lenient one**: the **size-matched label shuffle**
   (class sizes preserved, labels reassigned at random — the null
   [`divergence.py`](../../../../src/mtdsim/l3_simulation/petri/divergence.py)
   already uses at L3), not the L2 gate's half-split.
3. **Goal.** Produce and report the statistics of the profiles the
   dissertation argument needs — including a negative result, reported as
   such.

Everything below was computed by
[`tools/gasp_tactic_profile_stats.py`](../../../../tools/gasp_tactic_profile_stats.py),
an independent re-derivation from `gap_v0.5.json` + `classification.csv` + the
dedup rule (own code; it does not import the restatement tool). Seeds:
`20260528` (nulls, mirrors the gate), `1` (per-pair permutations); 2 000
relabellings per null. **JSD is reported in bits** (`jensenshannon(p, q,
base=2) ** 2`, in [0, 1]) throughout — see §1 for why that needs saying.

## 1. Verification of the restatement — everything reproduces, up to one unit

Every structural number in the restatement's §1 reproduces exactly:
15/14/14/13 tactic places of 15; 89/54/45/38 transitions of 122; twelve
tactics and twelve transitions common to all four classes; tactic-set Jaccard
0.800–0.933; transition-set Jaccard 0.239–0.353; the tactic-share table to
the decimal (impact 0.4 / 14.3 / 16.3 / 0.0 %; exfiltration 3.9 / 0.0 / 3.1 /
0.0 %). Every per-pair permutation *p* reproduces to within Monte-Carlo noise
(2 000 vs 1 000 shuffles).

**The one discrepancy is the logarithm base.** The restatement's, the L2
gate's and spec §(g)'s JSD values were computed with scipy's *default* base
(natural log) and are therefore in **nats**, in [0, ln 2 ≈ 0.693] — while
the gate's comment, the restatement and spec §(g) all describe them as
"base 2 … in [0, 1]", and L3's `divergence.py` (which explicitly passes
`base=2`) says its "convention matches the L2 gate". It did not: L3 reports
bits, L2 reported nats. Every L2 number divided by ln 2 lands on this tool's:
0.297 nats → 0.429 bits (technique, full), 0.351 → 0.506 (transition share,
occurrence pooling), 0.401 → 0.578 (its size-matched p95), the README's
0.3149 → 0.454, and so on. This is a monotone rescale applied equally to
observed and null, so **no verdict changes**; but the dissertation must cite
one unit, and it is bits. The gate now passes `base=2` and its README lines
carry the unit; the historical nats numbers are noted where they were recorded
(spec §(g), README, this record).

## 2. Why the size-matched null is the right comparator (the ruling's grounds)

The gate's half-split null draws two 19-flow (or 14/15-flow) halves at random
and records the JSD between them — a statistic of *one pair of large groups*.
The observed statistic is the mean over the six pairs of the 19 : 8 : 6 : 5
partition, four of which involve a class of 5–8 flows. Empirical JSD between
sparse distributions is biased upward as the samples shrink: two random
5-flow groups drawn from the same population sit far apart on a 122-cell
support simply because most cells are empty in each. A half-split null
therefore understates chance separation for this partition — it is not the
distribution of the statistic under "labels carry no information". The
size-matched label shuffle *is* that distribution: it holds the class sizes
fixed and randomises only the labels, which is the exchangeability null the
question actually poses. Two consequences follow. First, the size-matched null
is the correct one and the half-split is disclosed as lenient. Second, a
comparison at transition resolution against a size-matched null is a *hard*
test at n = 38 — the null band is wide precisely because the classes are
small — and a negative result there is a statement about power as much as
about structure. Both are recorded below.

## 3. Structure of the four profiles

Corpus: 38 flows (29 after operator deduplication), 124 techniques in 15
tactics; 478 technique-edges, of which 56 intra-tactic (dropped at the
quotient, as L3 drops them) → **122 inter-tactic transitions**.

| | exfiltration (19 → 14) | impact (8 → 7) | exfiltration_impact (6 → 4) | none_c2 (5 → 4) |
|---|--:|--:|--:|--:|
| tactic places (of 15) | 15 → 15 | 14 → 14 | 14 → 12 | 13 → 12 |
| missing tactic(s) | — | exfiltration | defense-impairment (→ + recon, resource-dev) | exfiltration, impact (→ + defense-impairment) |
| inter-tactic transitions (of 122) | 89 → 73 | 54 → 51 | 45 → 45 | 38 → 34 |
| transitions unique to this class | 37 → 31 | 9 → 13 | 9 → 14 | 3 → 3 |
| transitions backed by a single flow | 48 % → 62 % | 67 % → 71 % | 80 % → 80 % | 68 % → 68 % |
| median / max flows per transition | 2 / 7 → 1 / 6 | 1 / 3 | 1 / 2 | 1 / 3 |

(“a → b”: full corpus → operator-deduplicated.)

**Common core.** Twelve tactics and twelve transitions appear in all four
classes (ten and eleven on the deduplicated corpus). The common transitions
are the tactic-agnostic scaffold: initial-access → execution; execution →
{command-and-control, persistence}; command-and-control → {discovery,
lateral-movement, persistence, stealth}; persistence → {command-and-control,
discovery}; stealth → {discovery, execution}; lateral-movement → execution.

**Jaccard.** Tactic sets 0.80–0.93 (0.71–0.93 dedup): the classes are the
same tactic vocabulary. Transition sets 0.24–0.35 (0.24–0.32 dedup): they draw
different transition sets — but see the single-flow-backed row: half to
four-fifths of each class's transitions are drawn by exactly one flow, so a
class's transition set is largely the union of its members' idiosyncrasies.
Low transition-set Jaccard is what any 19 : 8 : 6 : 5 split of this corpus
shows: the observed mean pairwise transition-set Jaccard is 0.300 against a
size-matched-relabelling null of p5 / p50 / p95 = 0.241 / 0.299 / 0.354
(*p* = 0.50; deduplicated 0.289 vs 0.205 / 0.256 / 0.302, i.e. the real
classes overlap slightly *more* than random ones). The classes do not draw
detectably more distinct transition sets than random groups of the same
sizes.

## 4. The profiles, described (flow-presence pooling — the L3 W-A count)

Transition share is the distinct-flow count per tactic pair, normalised over
the 122 pairs — the quantity L3's weight layer is built from, so this *is* the
profile L3 consumes. Full corpus; the deduplicated figures are in the tool
output and move by at most a point or two.

| profile | mass into **exfiltration** (feeders) | mass into **impact** (feeders) | heaviest transitions (% of mass) |
|---|---|---|---|
| exfiltration | 6.4 % (collection, C2, credential-access, discovery, stealth) | 0.5 % (execution) | execution→persistence 3.7, execution→stealth 3.7, initial-access→execution 3.7, collection→exfiltration 2.7 |
| impact | 0 | 12.0 % (C2, discovery, execution, persistence, stealth) | execution→impact 4.0, stealth→execution 4.0, stealth→discovery 4.0, C2→impact 2.7 |
| exfiltration_impact | 5.6 % (C2, discovery) | 14.8 % (C2, discovery, execution, exfiltration, persistence, stealth) | C2→discovery 3.7, C2→exfiltration 3.7, discovery→impact 3.7, execution→impact 3.7, impact→discovery 3.7 |
| none_c2 | 0 | 0 | credential-access→lateral-movement 5.7, C2→stealth 5.7, discovery→C2 5.7 |

The read-offs that survive: the objective tactic's in-mass is the profile's
signature (0 / 12.0 / 14.8 % into impact; 6.4 / 0 / 5.6 / 0 % into
exfiltration); `exfiltration_impact` alone carries an exfiltration → impact
transition (the double-extortion order, drawn by its members) and is the only
class where impact feeds *onward* (impact → discovery / execution /
persistence / collection); `none_c2` is the class with no objective in-mass at
all — Decision 5's defining absence survives the change of resolution — and
its heaviest transitions are lateral-movement and C2 re-entry, the shape of an
operation evicted mid-movement.

## 5. Tactic-share table (verified; primary-tactic pooling; % of (flow, technique) occurrences)

| tactic | exfiltration | impact | exfiltration_impact | none_c2 |
|---|--:|--:|--:|--:|
| collection | 7.4 | 1.9 | 1.0 | 3.4 |
| command-and-control | 11.6 | 11.4 | 7.1 | 15.3 |
| credential-access | 9.5 | 4.8 | 4.1 | 6.8 |
| defense-impairment | 1.4 | 1.0 | 0.0 | 1.7 |
| discovery | 13.0 | 13.3 | 19.4 | 22.0 |
| execution | 9.8 | 12.4 | 12.2 | 18.6 |
| exfiltration | 3.9 | 0.0 | 3.1 | 0.0 |
| impact | 0.4 | 14.3 | 16.3 | 0.0 |
| initial-access | 9.8 | 6.7 | 8.2 | 3.4 |
| lateral-movement | 5.6 | 5.7 | 2.0 | 5.1 |
| persistence | 8.8 | 7.6 | 6.1 | 5.1 |
| privilege-escalation | 1.8 | 4.8 | 6.1 | 5.1 |
| reconnaissance | 3.5 | 1.9 | 1.0 | 1.7 |
| resource-development | 1.1 | 1.9 | 2.0 | 1.7 |
| stealth | 12.6 | 12.4 | 11.2 | 10.2 |

Read-offs: impact 0.4 / 14.3 / 16.3 / 0.0 % (the findings note's "0 % →
11.3 %" was a different pooling and is superseded); exfiltration present
only in the two theft classes; discovery the largest or second-largest share
in every class; the two small classes lean on discovery + execution
(31.6 % and 40.6 % combined, against 22.8 % and 25.7 %).

## 6. Separation under the size-matched null — the negative result

Mean pairwise JSD over the six class pairs (bits), against the size-matched
label-shuffle null (2 000 relabellings; *p* = fraction of relabellings whose
statistic ≥ observed). The half-split p95 is shown only to document the
gate's lenient comparator.

| statistic | corpus | observed | null p50 | null p95 | ***p*** | half-split p95 |
|---|---|--:|--:|--:|--:|--:|
| **transition share (flow-presence) — the profile** | n = 38 | 0.501 | 0.500 | 0.576 | **0.495** | 0.349 |
| | n = 29 | 0.534 | 0.558 | 0.632 | **0.733** | 0.389 |
| transition share (edge-occurrence; restatement's pooling) | n = 38 | 0.506 | 0.494 | 0.578 | 0.393 | 0.344 |
| | n = 29 | 0.540 | 0.554 | 0.632 | 0.635 | 0.392 |
| transition share, objective-tactic transitions stripped | n = 38 | 0.451 | 0.476 | 0.563 | 0.714 | 0.323 |
| | n = 29 | 0.485 | 0.534 | 0.619 | 0.883 | 0.373 |
| tactic share (15 cells) | n = 38 | 0.100 | 0.056 | 0.090 | **0.019** | 0.037 |
| | n = 29 | 0.120 | 0.073 | 0.112 | **0.032** | 0.047 |
| technique (124 cells; the old gate's statistic) | n = 38 | 0.429 | 0.364 | 0.425 | 0.040 | 0.219 |
| | n = 29 | 0.454 | 0.438 | 0.503 | 0.325 | 0.267 |

**Reading.** At the resolution the profiles are defined and consumed —
tactic-to-tactic transition share — the observed separation sits **at the
median of the size-matched null** on the full corpus (*p* = 0.50) and *below*
it on the deduplicated corpus (*p* = 0.73). The four transition-share
distributions are, as distributions, what a random 19 : 8 : 6 : 5 relabelling
of this corpus produces. Stripping the objective-tactic transitions moves the
statistic further *into* the null (*p* = 0.71 / 0.88): there is no residual
tactic-to-tactic signal beyond the objective. The only resolution that clears
the strict null is the coarse 15-cell tactic share (*p* = 0.02 / 0.03), and
the technique statistic — the one the old gate certified "modest but real,
operator-robust" — clears on the full corpus only (*p* = 0.04) and fails on
the deduplicated one (*p* = 0.33).

**Per pair** (2 000 relabellings of the two classes' pooled flows; JSD in
bits, *p* in brackets; \* = *p* < .05; full corpus, deduplicated in the tool
output with the same pattern):

| pair | transition share | objective stripped | tactic share | technique |
|---|--:|--:|--:|--:|
| exfiltration vs impact | 0.479 (.120) | 0.419 (.332) | 0.110 (**.002**\*) | 0.357 (.065) |
| exfiltration vs exfiltration_impact | 0.536 (.194) | 0.456 (.384) | 0.140 (**.003**\*) | 0.389 (.084) |
| exfiltration vs none_c2 | 0.411 (.630) | 0.379 (.709) | 0.074 (.144) | 0.408 (.141) |
| impact vs exfiltration_impact | 0.479 (.857) | 0.488 (.900) | 0.039 (.606) | 0.470 (**.032**\*) |
| impact vs none_c2 | 0.462 (.644) | 0.411 (.905) | 0.096 (.104) | 0.485 (.110) |
| exfiltration_impact vs none_c2 | 0.638 (.208) | 0.550 (.408) | 0.143 (**.009**\*) | 0.462 (**.028**\*) |

No pair separates at transition resolution. The three pairs that separate at
tactic share are the pairs on opposite sides of the *impact present / absent*
line (exfiltration vs impact; exfiltration vs double extortion; double
extortion vs none_c2); pairs on the same side (impact vs double extortion;
exfiltration vs none_c2) do not. Decomposing each pair's transition-share JSD
by transition, 9–34 % of it sits on transitions touching an objective tactic
and the remainder is spread thinly across single-flow transitions (the
largest single contributor to any pair is 6 %). The partition's signal, at
tactic resolution, is the objective tactic itself.

### 6b. The "what next" test — per-place conditionals, not the marginal

Marc's objection (2026-08-17, on reading the above): the profiles are
weighted *directed* graphs whose weights are **per-place out-transition
proportions** — at execution, two flows go on to impact and one to stealth,
so 2/3 and 1/3 — and the transition-share statistic above is the *marginal*
over all 122 pairs, not that conditional. The *what* (which transitions
exist) may well be null; the *what next* (given the current tactic, where the
attacker goes) is what the profile encodes and what should differ. Two
statistics test it, both against the same size-matched null (tool §8):

- **(a) mean per-place JSD, class vs class** — for each pair of classes, the
  JSD between their out-distributions at each place where both have one,
  averaged over those places (the `divergence.py` form, but between classes
  rather than class-vs-aggregate); unweighted, and support-weighted so that
  sparse places do not count as much as execution or command-and-control.
- **(b) the deviance G** of the class-conditional next-tactic model against
  the pooled model, 2 Σ n_c(p→t) ln[P_c(t|p) / P_pool(t|p)] — the
  likelihood-ratio statistic for "the next-transition probabilities depend
  on class", weighting every place by its support; permutation-tested, so no
  distributional assumption. Also decomposed by place, and per pair.

| statistic | corpus | observed | null p50 | null p95 | *p* |
|---|---|--:|--:|--:|--:|
| (a) mean pairwise per-place JSD, unweighted | n = 38 | 0.564 | 0.568 | 0.636 | 0.55 |
| | n = 29 | 0.584 | 0.603 | 0.673 | 0.69 |
| (a) support-weighted | n = 38 | 0.457 | 0.467 | 0.542 | 0.57 |
| | n = 29 | 0.489 | 0.518 | 0.596 | 0.78 |
| (b) deviance G, four-class model vs pooled | n = 38 | 289.0 | 282.6 | 311.8 | 0.36 |
| | n = 29 | 277.7 | 257.0 | 283.2 | 0.10 |
| (b) deviance G, objective-tactic transitions stripped | n = 38 | 224.2 | 228.5 | 254.8 | 0.60 |
| | n = 29 | 221.4 | 207.4 | 231.4 | 0.17 |

**Four-class verdict: the conditionals do not separate either.** The
per-place JSD sits at the null median; the deviance clears nothing (*p* =
0.36; *p* = 0.10 on the deduplicated corpus, and 0.17 with the objective
transitions removed). "What next" is as null as "what", for the four-way
question.

**Where it is not null.** Two places where the *what next* does show, both
of them the objective again:

- **Per place**, the one tactic whose out-distribution differs by class is
  **discovery** (G = 37.9 vs null p95 34.8, *p* = 0.013; deduplicated *p* =
  0.009): after discovery the exfiltration class goes to collection,
  command-and-control and credential-access; the impact class to
  command-and-control; double extortion to impact and stealth; `none_c2` to
  command-and-control. Execution is next (*p* = 0.09 / 0.10: exfiltration
  → stealth/persistence 7/7 flows; impact → impact 3). Fifteen places were
  tested, so one at *p* ≈ 0.01 is not multiplicity-robust (Bonferroni
  threshold 0.003) — but its direction is the mechanism the partition is
  built on, not noise.
- **Per pair**, the one pair whose next-transition structure separates is
  **exfiltration vs impact** — the two largest classes, the pair with the
  power: deviance *p* = 0.030 (n = 38), 0.011 (n = 29); per-place JSD *p* =
  0.058 / 0.029. With the objective-tactic transitions stripped it is *p* =
  0.106 / 0.021 — suggestive on one corpus, not on the other. No other pair
  separates on any what-next statistic (all *p* > 0.13).

So the intuition is half right, and the record now says which half: **theft
versus ransomware do route differently after discovery and execution**, and
that is measurable at 19 vs 8 flows; the four-way claim, and every pair
involving a 5- or 6-flow class, is not — the null band for a 4-flow class's
conditionals at fifteen places is wider than any real difference the corpus
could carry.

**Consistency with L3.** The committed L3 structural report
([`data/ogasp/petri/divergence_report.md`](../../../../data/ogasp/petri/divergence_report.md))
already says the same thing from the other side: on the deduplicated corpus
no class net's per-place out-distribution diverges from the aggregate beyond
the shuffled-label null p95 (exfiltration 0.19 vs p95 0.22; impact 0.33 vs
0.42; double extortion 0.30 vs 0.53; none_c2 0.38 vs 0.51). Its verdict —
"the structural weight layer alone does not discriminate the envelopes at
this corpus size; the behavioural half of the verification carries the
question" — is now the L2 verdict too, in the same unit and under the same
null.

## 7. Pooling sensitivity (the handoff's step 2)

- **(a) primary tactic vs all tactics.** Twenty of 124 techniques carry more
  than one tactic. Under all-tactics pooling the read-offs hold: impact 0.3 /
  11.4 / 13.7 / 0.0 %; exfiltration 3.2 / 0 / 2.6 / 0 %; discovery first or
  second in every class. Privilege-escalation and stealth rise (the
  multi-tactic techniques are mostly theirs); nothing else moves by more than
  three points. The chapter should mean *primary tactic* (the L1 convention).
- **(b) flow-presence vs edge-occurrence.** Both transition-share poolings
  give the same verdicts (table above; per-pair *p* differ by up to .24 on
  one pair and never cross .05). The chapter should mean *flow-presence*: it is what L3's
  weights are built from, so the profile described is the profile executed.
- **(c) intra-tactic edges.** 56 of 478 technique-edges are intra-tactic and
  are dropped, mirroring the L3 quotient. They carry no tactic-to-tactic
  information by construction.

## 8. What the L2 unit can and cannot now say

**Sayable, verified:**

- The four profiles are **objective-conditioned envelopes drawn from one
  substrate**: the same fifteen tactics (15/14/14/13 present; twelve in all
  four), a shared twelve-transition scaffold, and *different transition
  supports* — 89 / 54 / 45 / 38 of the 122 inter-tactic transitions, with 37 /
  9 / 9 / 3 transitions drawn by one class alone.
- **What distinguishes them is the objective tactic** — categorically
  (impact absent from two classes, exfiltration absent from two, both absent
  from `none_c2`), and in mass (0 / 12.0 / 14.8 % of transition mass into
  impact; 6.4 / 0 / 5.6 / 0 % into exfiltration) — plus a discovery/execution
  lean in the two small classes. At the coarse tactic-share resolution this
  clears the strict null (*p* = .02), and only across the impact-present /
  impact-absent line.
- **As tactic-to-tactic transition distributions — marginal *or* per-place
  conditional — the four profiles do not differ from chance** at this corpus
  size (marginal *p* = 0.50 / 0.73; conditional deviance *p* = 0.36 / 0.10;
  L3's per-place report agrees). Half to four-fifths of each profile's
  transitions are single-flow. This is a power statement about a 38-flow
  corpus quotiented onto 122 cells as much as a structural one — but it is
  the honest statement, and the one the dissertation carries.
- **The one pairwise exception is theft vs ransomware**: exfiltration and
  impact — the two classes large enough to test — route differently after
  discovery and execution (next-transition deviance *p* = 0.03 / 0.01;
  discovery's out-distribution differs by class at *p* ≈ 0.01, the only
  place that does). Sayable as *the objective shows in the routing of the
  two largest classes*; not sayable as a four-way result.

**Not sayable (retired):** "the separation signal is real, operator-robust"
(finding 5) as an unqualified statement; "clears the null" without naming
the null; any implication that L3 inherits four *statistically distinct*
transition profiles. The discrimination claim moves off corpus structure and
onto the execution-level result
([`../ogasp/profile_divergence_findings.md`](../ogasp/profile_divergence_findings.md),
P1 held 40–110× — whose own size-matched, label-blind control, arm 3, has not
run; the same null discipline applies there and is the open item).

**Chapter-facing number set** (each verified by the tool and, where marked,
pinned by the gate):

| figure | value | definition | status |
|---|---|---|---|
| tactic places per profile | 15 / 14 / 14 / 13 of 15 | distinct primary tactics of the class's techniques | verified |
| transitions per profile | 89 / 54 / 45 / 38 of 122 | distinct inter-tactic pairs drawn by ≥ 1 class flow | verified |
| shared scaffold | 12 tactics, 12 transitions in all four | intersection over classes | verified |
| single-flow-backed transitions | 48 / 67 / 80 / 68 % | transitions drawn by exactly one class flow | verified |
| tactic-set Jaccard | 0.80–0.93 | pairwise, on tactic sets | verified |
| transition-set Jaccard | 0.24–0.35 (mean 0.300 vs size-matched null p50 0.299) | pairwise, on transition sets | verified |
| mass into impact | 0 / 12.0 / 14.8 / 0 % | flow-presence transition share summed over pairs ending in impact | verified |
| mass into exfiltration | 6.4 / 0 / 5.6 / 0 % | as above, ending in exfiltration | verified |
| impact tactic share | 0.4 / 14.3 / 16.3 / 0.0 % | (flow, technique) occurrences pooled to primary tactic | verified |
| separation, transition share | 0.501 bits vs null p50 0.500 / p95 0.576, *p* = 0.50 (n = 38); 0.534 vs 0.558 / 0.632, *p* = 0.73 (n = 29) | mean pairwise JSD, size-matched null, 2 000 trials | verified; **gate-pinned** |
| separation, tactic share | 0.100 vs p95 0.090, *p* = 0.02 (n = 38); 0.120 vs 0.112, *p* = 0.03 (n = 29) | as above, 15-cell tactic share | verified |
| pairs separating at tactic share | 3 of 6, all across the impact-present/absent line | per-pair permutation, *p* < .05 | verified |
| what-next (per-place conditional), four-class | deviance G 289.0 vs null p95 311.8, *p* = 0.36 (n = 38); *p* = 0.10 (n = 29) | class-conditional next-tactic model vs pooled, size-matched permutation | verified |
| what-next, exfiltration vs impact | deviance *p* = 0.030 / 0.011; objective-stripped 0.106 / 0.021 | pairwise permutation | verified |
| places whose next-tactic distribution differs by class | discovery (*p* = 0.013 / 0.009); execution borderline (0.09 / 0.10); of 15 | per-place deviance, permutation | verified; not multiplicity-robust |

## 9. What changed in the repo (this session)

- **Gate** ([`tests/l2_subgraph/test_gasp.py`](../../../../tests/l2_subgraph/test_gasp.py)):
  JSD now in bits (`base=2`); the half-split technique test kept and
  re-labelled as the historical (lenient) calibration; a new
  `test_transition_share_size_matched_null_verdict` (both corpora) pins the
  cited transition-share JSD to 3 d.p. and the recorded verdict
  (`observed <= null p95`) — a corpus change that makes the profiles clear
  the strict null fails the test and reopens this record. Both tests write
  their lines into [`data/gasp/README.md`](../../../../data/gasp/README.md).
- **Spec** ([`gasp_schema.md`](gasp_schema.md) §(g)): the size-matched check
  added as the load-bearing row; unit disclosed on the historical numbers.
- **Note** ([`../../../notes/ch4_methods/objective_partition_findings.md`](../../../notes/ch4_methods/objective_partition_findings.md)):
  finding 1's impact-share numbers replaced by the verified ones; finding 5
  rewritten to the null-dependent, resolution-honest statement.
- **No artefact changes**: class memberships, the audit CSV, the four
  `SubgraphView`s and the L3 nets are untouched.
- The restatement record is kept, marked superseded by this one; the
  drafting-session tool is kept as the thing this tool verified.

## Related

- [`tactic_resolution_restatement.md`](tactic_resolution_restatement.md) —
  the drafting-session numbers this record verified (nats; superseded).
- [`gasp_schema.md`](gasp_schema.md) §(g) — the gate as specified.
- [`../ogasp/profile_divergence_findings.md`](../ogasp/profile_divergence_findings.md)
  — where the discrimination claim now lives; arm 3 open.
- [`data/ogasp/petri/divergence_report.md`](../../../../data/ogasp/petri/divergence_report.md)
  — the L3 structural report this agrees with.
- Same-operator-same-class check (Marc's 2026-08-17 reframe): Conti ×3,
  FIN13 ×2, Turla ×2, OceanLotus ×2, Sandworm ×2 each within one class; the
  Lazarus umbrella straddles impact / exfiltration; the CISA AA22-138B
  advisory trio splits exfiltration / none_c2 ×2. Five of five single-G-ID
  clusters are within-class.
