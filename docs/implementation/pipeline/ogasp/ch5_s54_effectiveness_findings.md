---
status: findings — preliminary read 2026-09-17, landed section by section the same day (Marc's instruction: iterate §5.3.2 → §5.5 in sequence with preliminary numbers); §5.4.1–§5.4.3 landed via tools/ch5_effectiveness_figures.py; captions DRAFT STATE, voice pass owed; the Zhang and Brown claim locators are Marc's to verify (handoff Q5)
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

### Figure 5.6 and Table 5.6

The same nine conditions, the baseline attacker (100 runs per cell; 24.34 ±
1.87 hosts with no defence) beside the model pooled (8.13). Ranks are by
suppression at each interval; the family contrast follows the 2026-09-09
inference ruling: Cliff's δ on hosts reached, the network layer (IP shuffle,
complete topology, host topology) against the application layer (port shuffle,
OS diversity, service diversity), positive when the network layer leaves
fewer hosts. User shuffle is in neither family.

| 200 s | baseline | rank | model | rank |
|---|---|---|---|---|
| service diversity | 0.91 [0.88, 0.93] | 1 | 0.36 [0.31, 0.41] | 6 |
| port shuffle | 0.90 [0.87, 0.93] | 2 | 0.20 [0.14, 0.26] | 7 |
| IP shuffle | 0.68 [0.62, 0.72] | 3 | 0.96 [0.95, 0.97] | 1 |
| OS diversity | 0.64 [0.57, 0.71] | 4 | 0.07 [0.00, 0.14] | 8 |
| complete topology | 0.41 [0.33, 0.47] | 5 | 0.96 [0.95, 0.96] | 3 |
| host topology | 0.40 [0.32, 0.47] | 6 | 0.96 [0.95, 0.96] | 2 |
| alternative | 0.39 [0.31, 0.45] | 7 | 0.72 [0.69, 0.74] | 5 |
| random | 0.33 [0.25, 0.40] | 8 | 0.75 [0.72, 0.77] | 4 |
| user shuffle | −0.07 [−0.19, 0.04] | 9 | −0.14 [−0.22, −0.06] | 9 |

| statistic | 200 s | 2 000 s |
|---|---|---|
| Spearman ρ, seed bootstrap (1 000) | 0.08 [−0.13, 0.10]; 32 % of resamples negative | 0.13 [−0.27, 0.33]; 41 % negative |
| Cliff's δ network below application, baseline | −0.61 [−0.67, −0.54] (network 12.4 hosts, application 4.5) | −0.19 [−0.29, −0.10] (24.7 / 21.9) |
| Cliff's δ, model | 0.93 [0.91, 0.94] (0.34 / 6.43) | 0.25 [0.20, 0.29] (6.36 / 8.06) |
| top mechanism | baseline service diversity, model IP shuffle | the same two |

Three things are in the table.

1. **The two attackers disagree about which family matters, and the
   disagreement is at the family grade with the intervals nowhere near
   zero.** Against the model the network layer leaves fewer hosts in nearly
   every paired comparison (δ 0.93); against the baseline the application
   layer does (δ −0.61). The baseline's top two are service diversity and port
   shuffle at 0.90–0.91, both surface re-rolls (port shuffle re-rolls what
   the baseline's port scan finds); the model's top three are the three
   position-destroying mechanisms at 0.96. The design comment's 2 × 2 —
   severance against re-roll, and which half matters — is what the corpus
   returns.
2. **The full orderings are uncorrelated, not inverted.** ρ = 0.08 at 200 s
   with a bootstrap interval that straddles zero and a third of resamples
   negative. The record's −0.893 (10 seeds, 2026-07-29) does not return and
   the hard block in the tex stands: no sentence may say the orderings are
   inverted. What the seeds separate is the family sign, and the prose
   should say exactly that and no more. The two arms agree on user shuffle
   (last on both, negative on both) and on the schemes' middle placement.
3. **At 2 000 s the sign survives and the magnitude does not.** δ 0.25 (model)
   against −0.19 (baseline), both separated from zero, both a quarter of the
   200 s values; only service diversity (baseline, 0.30) and IP shuffle
   (model, 0.33) are separated from zero as singles, and each is the other
   arm's second. Complete topology shuffle is negative against the baseline
   at 2 000 s (−0.13 [−0.24, −0.04]): a re-wire eight times per campaign hands
   the scripted attacker more hosts than it would otherwise reach. Open, as
   user shuffle is (§1 item 2). *To verify.*

The schemes read the family split too: random and alternative over the seven
place 4th–5th against the model (0.72–0.75, a rotation that spends three of
seven turns on the network layer) and 7th–8th against the baseline
(0.33–0.39). Neither arm's best scheme approaches its best single.

### Against the record

| quantity | record | here |
|---|---|---|
| ρ, movement vs inherited ordering | −0.893 (10 seeds, pre-restoration); −0.071 (50 seeds, restored substrate, token-hold record H0) | 0.08 [−0.13, 0.10] at 100 seeds, the chapter's pins |
| inherited attacker's ordering after `d127f443` | service ≫ plateau {IP 0.68, OS 0.58, CT 0.56} | service 0.91 ≈ port 0.90 > IP 0.68 ≈ OS 0.64 > CT 0.41 ≈ HT 0.40; the plateau has split, and the three restored mechanisms enter it at both ends (port 2nd, user last) |
| model's ordering | IP 0.93, CT 0.91, service 0.29, OS 0.08 | IP 0.96, CT 0.96, HT 0.96, service 0.36, OS 0.07: unchanged in shape |
| hypothesis tree E2-R (re-establish H2 at the post-gate configuration) | owed | this is it, at the chapter's pins: H2 returns as a family contrast (tree §1's stated prior), not as a rank inversion |
| the baseline's blocked fraction | structural zero | structural zero in every row (sanity) — the channel exists only on the model |

### What the floats needed changed (APPLIED 2026-09-17)

- Fig. 5.6: four panels as Fig. 5.5, the baseline hatched grey, the model
  solid; the model is the four profiles pooled, the aggregate is not an arm
  here.
- Tab. 5.6: the family contrast is stated in the footnote as the primary and
  the rank correlation as its companion, the two families named there, user
  shuffle placed outside both. The caption's "statistic summarising how far
  apart the two orderings are" is ρ; the table says at which grade the
  evidence holds.

## 3. §5.4.3 — the lineage's headline claims

### Table 5.7

The lineage arm: the same matrix under the opportunistic objective
(`attack_objective="general"`, the lineage's 80 % compromise-ratio stop), 100
seeds, both arms. With no defence the baseline reaches 31.82 ± 1.90 hosts
and stops on the ratio in 27 % of runs; the model reaches 8.35 ± 0.44 and
never stops on it — the objective changes the baseline's breadth (24.3 →
31.8) and not the model's (8.13 → 8.35), which is §5.3.1's reading of what
the objective does to each. The suppression matrix at 200 s:

| condition | baseline | model |
|---|---|---|
| service diversity | 0.93 [0.91, 0.95] | 0.36 [0.31, 0.41] |
| port shuffle | 0.93 [0.90, 0.94] | 0.23 [0.17, 0.29] |
| IP shuffle | 0.71 [0.67, 0.75] | 0.96 [0.95, 0.97] |
| OS diversity | 0.64 [0.57, 0.70] | 0.05 [−0.03, 0.12] |
| host topology | 0.60 [0.56, 0.65] | 0.96 [0.95, 0.97] |
| complete topology | 0.58 [0.53, 0.63] | 0.96 [0.95, 0.96] |
| alternative | 0.48 [0.42, 0.54] | 0.73 [0.70, 0.75] |
| random | 0.39 [0.32, 0.45] | 0.75 [0.72, 0.77] |
| user shuffle | −0.09 [−0.18, −0.01] | −0.14 [−0.23, −0.06] |

ρ = 0.10 [−0.02, 0.27] at 200 s; 0.60 [0.03, 0.72] at 2 000 s. Family δ at
200 s: model 0.93 [0.91, 0.94], baseline −0.53 [−0.61, −0.45]. The same shape
as the targeted arm (§2): the objective does not move the family sign on
either attacker.

The three claims, direction read on suppression of hosts reached:

| claim | source | inherited attacker | attacker model | agreement |
|---|---|---|---|---|
| shuffling > diversification, singles, 200 s | Zhang (*verify*) | diversity higher: family means 0.55 against 0.78; best of each (port 0.93, service 0.93) not separated | shuffle higher: 0.59 against 0.21 | model only |
| best single ≈ best scheme, 200 s | Brown (*verify*) | single higher: service 0.93 against alternative 0.48 | single higher: IP 0.96 against random 0.75 | neither |
| diversification > shuffling, OS diversity against IP shuffle, 200 s | Ho §4.3 (extraction "Headline findings") | diversity higher: family means 0.78 against 0.55; the pair OS 0.64, IP 0.71, not separated | shuffle higher: 0.21 against 0.59; OS 0.05, IP 0.96 | inherited only (family), neither on the pair |

Three things are in the table.

1. **The lineage disagrees with itself, and this simulator sides with each
   once.** Zhang's direction and Ho's are opposite at the same interval;
   under the inherited attacker the diversity family suppresses more (Ho's
   direction), under the model the shuffle family does (Zhang's). Which
   published claim "survives a change of attacker" is therefore the wrong
   question: each survives under one attacker, and the family contrast of §2
   is the reason.
2. **Brown's "best single ≈ best combination" holds under neither.** On both
   arms the best single beats the best scheme by 0.2–0.45 with the intervals
   far apart. The schemes here draw from the seven mechanisms (Q1), so a
   rotation spends turns on mechanisms that do not reach the attacker in
   question: against the model four of seven turns go to the application
   layer, against the baseline three of seven go to the network layer. A
   scheme over the four (the record's pool) would be a different condition.
3. **Ho's named pair is not separated under the inherited attacker.** OS
   diversity 0.64 against IP shuffle 0.71 with overlapping intervals: the
   family direction agrees with Ho and the pair does not, at 100 seeds. The
   claim was read at 200 s because that is where the extraction locates it;
   the design record's "at long intervals" framing (the placeholder's third
   row) is not the extraction's and was not drawn. At 2 000 s the diversity
   family still leads on the baseline (0.17 against −0.02, service diversity
   0.38 the only separated single) and trails on the model (0.01 against 0.15).

### Against the record

| quantity | record | here |
|---|---|---|
| the lineage arm | never run under the general objective on the restored substrate with both arms | run; ρ at 2 000 s is 0.60 [0.03, 0.72] — the only cell in the chapter where the two orderings correlate, and at the tempo where the baseline's landscape is service diversity alone |
| Zhang / Brown claim locators (Q5) | not carried as result rows in the extractions | still not; the source column carries the verify mark, the footnote says so |
| Ho's claim | placeholder: "diversification dominates at long intervals" | extraction: at interval 200, OS Diversity vs IP Shuffle, hybrid metric, up to 140 % — read there |

### What the float needed changed (APPLIED 2026-09-17)

- Tab. 5.7's third row reads Ho at 200 s with the named pair beside the
  family means, not at 2 000 s; the analyser carries both readings.
- The agreement column separates the family reading from the pair reading
  where the source names a pair.
- The footnote restates the comparability boundary (the published metric is
  time to compromise or a composite of it; the direction only is compared)
  and decodes the verify mark.

## 4. Validation

§5.4.1: every cell at 100 (400 pooled); Fig. 5.5 fits the page box
(15.7 × 9.9 cm); every caption fact printed by the generator matches
`numbers.json`; the table's footnote spans its seven columns. §5.4.2: Fig. 5.6
fits (15.7 × 9.5 cm); the ranks in Tab. 5.6 are the analyser's, the footnote
statistics match `numbers.json` §s542. Open: the user-shuffle attribution
(§1 item 2), complete topology's negative suppression of the baseline at
2 000 s (§2 item 3), and the interrupt-tally cross-check (§5.3.2 record §1).

## 5. Addendum 2026-09-22 — the §5.3.1 scrutinise-figure pass (Figure 5.3, Table 5.4)

Record in the results context handoff §8h; this section carries the numbers
the pass added to the read of §1. Five reviewers in round one (cold reader,
context critic, numbers auditor, convention reader, sceptical examiner), then
two more rounds; every accepted finding was checked against `numbers.json`
or the raw runs. Old section numbers in §1 (5.4.1, Fig. 5.5, Tab. 5.5) are
today's §5.3.1, Figure 5.3, Table 5.4.

- **Audit: 243 of 243 printed table values and 90 of 90 bars and whiskers
  reproduce** from `summaries.pkl` with independent code, five cells
  spot-checked against `runs.jsonl` (0 per-run mismatches); the bootstrap
  stream replays exactly at seed 0, and an independent stream moves a bound by
  at most 0.005. Nothing is clipped by the axis (lo min −0.381, hi max 0.989).
- **§1 item 3 corrected: "not profile-dependent" is true of the tiers, not
  of the magnitudes.** Every profile orders the tiers the same way at 200 s.
  Inside a tier, separated profile differences exist: IP shuffle $c_1$ 0.93
  [0.90, 0.95] against $c_4$ 0.98 [0.97, 0.99]; random $c_3$ 0.81
  [0.76, 0.86] against $c_1$ 0.69 [0.64, 0.74]; alternative $c_3$ 0.82
  against $c_1$ 0.69. At 2 000 s: IP shuffle $c_3$ 0.47 against $c_1$ 0.25,
  alternative $c_1$ 0.16 against $c_3$ −0.11; the tiers are not separated per
  profile there. Power to detect a 0.10 profile difference at 100 seeds
  (examiner's estimate): host layer ≈ 1.0, schemes 0.77, service layer
  0.20–0.33, user shuffle 0.14 — on the service layer "no profile
  dependence" is absence of evidence at this seed count.
- **§1 item 4 read exactly: random is separated from zero at 2 000 s** (0.09
  [0.02, 0.15]) beside the host layer; the takeaway now says so.
- **Dagger semantics changed in the generator:** the mark sits on the UPPER
  row of each unseparated adjacent pair ("overlaps the row below's"), so a
  reader recovers every adjacent pair from the marks. Non-adjacent overlaps
  are not marked (200 s: IP–complete topology; 2 000 s: thirteen pairs); the
  body must not read a non-adjacent separation off the marks.
- **Estimator robustness (examiner):** ratio of means, medians, paired
  per-seed differences and Cliff's δ return the same ordering at both
  intervals; no tier boundary moves. Excluding runs that reach the target
  moves suppression ≤ 0.02 at 200 s.
- **Paired against unpaired bootstrap (auditor):** every cell shares seeds
  0–99 and the network per seed. Pairing narrows the weak-defence intervals
  by 25–45 % (service diversity 200 s 0.095 → 0.071 wide; user shuffle 0.166
  → 0.090; IP shuffle 2 000 s 0.111 → 0.074) and the strong ones not at all
  (IP shuffle 200 s 0.016 either way); no dagger verdict flips at 200 s. The
  seed correlation is 0.19–0.24 under the host layer and 0.59–0.81 under
  the service layer, because every mechanism draws from the one global RNG,
  so the pairing holds only until the first deployment. Kept unpaired; ruling
  Marc's (§8h).
- **Saturation, for chapter 6 (examiner):** under the host layer at 200 s the
  attacker still compromises in 24–29 % of runs (126–146 events per 400
  runs), 85–89 % of them 100–200 s after the last interrupt (median
  158–160 s); with no defence the median gap between compromises is 891 s
  and 11 % of gaps are under 200 s. So the 200 s magnitude is the dose and
  the layer is the ordering (held at both intervals). The chapter 5 sentence
  is conditioned on the interval; "the mechanism removes" is not licensed.
- **Convergence at the time limit (examiner):** the tier order is stable
  from 2 500 s to 15 000 s at 200 s; magnitudes are not (service diversity
  0.19 → 0.36, OS diversity 0.23 → 0.07, user shuffle 0.02 → −0.135; at
  2 000 s topology 0.29 → 0.16, alternative 0.28 → 0.03). Every §5.3.1
  number is a 15 000 s reading.
- **User shuffle, what a trace must show (examiner; cause still open):**
  paired +1.10 ± 0.32 hosts, consistent on all four profiles (+0.92 to
  +1.29), growing with run time, with no change in actions, successes or
  tactic visits and 0.76 interrupts per run. The mechanism re-draws five
  users per internal host from the 50-user pool with replacement, 75 times
  per run; the attacker reads the set on enumerate host
  (`can_auto_compromise_with_users`: any harvested reused-password user
  compromises at once) and on brute force (`compromise_with_users`,
  p = 0.01·|overlap|/total_users, where a duplicate draw shrinks
  `total_users`). The trace must show, per compromise under user shuffle
  against no defence, which path fired, the overlap size and `total_users`
  after the re-roll.
- **Schemes' pool composition measured:** random 13.8–14.6 % per mechanism,
  alternative 13.3–14.7 %, i.e. three of seven firings on the host layer.
- **Seed-count projection (examiner):** at 200 s the host-layer trio's
  differences are 0.004–0.006 (z 0.7–1.0 now, 2.2–3.2 projected at 1 000
  seeds), so "one effect" will likely fail the overlap test at the thousand
  unless an effect floor is declared; the design's inference ruling
  (2026-09-09 §13.2) asked for floors and none is on record. Random against
  alternative projects to z 4.8. At 2 000 s the service / scheme / user
  cluster stays unseparated even at 1 000 (projected z ≤ 2).
- **Other metrics (examiner):** at 200 s the suppression order holds on runs
  with no compromise (ρ 0.98), delay (0.87) and blocked fraction (0.87);
  the service-layer tier is hosts-reached-only (blocked 0.23–0.25, delay
  2 082–2 324 s, the no-defence level). At 2 000 s runs-with-no-compromise is
  uninformative (ρ −0.10).
