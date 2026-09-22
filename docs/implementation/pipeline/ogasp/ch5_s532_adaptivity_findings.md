---
status: findings — the §5.2.2 float this record shaped was RETIRED 2026-09-22 (wrong resolution: the verb is downstream of the mapping); superseded for §5.2.2 by ch5_s522_disruption_findings.md, kept as the record of the verb-level instrument (its numbers stand in numbers.json §s532). Original: preliminary read 2026-09-17; the §6 changes APPLIED the same day (Marc's instruction 2026-09-17: iterate §5.3.2 → §5.5 with preliminary numbers, no acceptance stop); fig_5-3-2a landed via tools/ch5_adaptivity_figure.py; caption DRAFT STATE, voice pass owed
created: 2026-09-17
topic: "The §5.3.2 read of the defended corpus: what the attacker model does in the five visits before and after each defensive interrupt, against the verdict-blind control and the placebo null, under the spanning pair at two tempos — and the finding that the outcome-conditioned routing leaves no signature in the activity mix"
---

# §5.3.2 Under disruption — the preliminary read

**Design:** [`../../../handoffs/2026-09-17_ch5_s532_s55_defended_runs.md`](../../../handoffs/2026-09-17_ch5_s532_s55_defended_runs.md)
§1–§2. **Workspace:** `data/results/ch5_defended/` (gitignored): `run_corpus.py` →
`runs.jsonl` (30 200 runs, 2.0 GB, 97 min on seven workers); `analyse.py` →
`numbers.json` §s532, `preview_fig54.png`, `summaries.pkl` (the per-run
summaries, cached). Every measure is the shipped suite's
(`measures.py` §3 `interrupt_action_mix`, window 5; `jsd`; `mean_ci`); the
analysis is a reader.

## 1. Configuration and sanity

The corpus: six arms × ten conditions × two intervals (no defence once) × 100
seeds under the targeted objective (core, 11 400 runs); the same under the
general objective (lineage arm, 11 400); the four profiles under IP shuffle and
OS diversity at both intervals and unopposed with the verdict-blind overlay
(blind arm, 2 000); the nine defended conditions at 200 s under the exponential
regime (regime arm, 5 400). `v2_partial`, `overlay_version="v4_failure_only"`
passed by name (or `overlay=verdict_blind_overlay()` on the blind arm),
synthetic overlay on, retrace on, fresh-host contract on, modulators off,
random and alternative over the **seven** mechanisms (the substrate's default
pool is the lineage four; the seven are passed explicitly).

Sanity: zero error rows; 302 cells, every one at 100; no `max_events`
termination; the baseline's blocked fraction is the structural zero in every
row; its uuid-counted and positional host counts agree in every run. **One
cross-check fails:** in 2 405 of 26 800 movement runs the count of interrupted
records differs from the substrate's own `Total attack interrupted` tally.
Nothing drawn here reads the substrate tally (the figure keys on the record's
interrupted visits), but the discrepancy is unexplained and is flagged for
the trace tool — likely an interrupt landing on a dwell-only visit or on the
retrace step, which the substrate counts and the record does not, or the
reverse. To verify.

§5.3.2 reads the four profiles pooled (400 runs per cell); the aggregate is
§5.3.1's fifth arm, not this section's.

## 2. Figure 5.4 — the activity mix before and after an interrupt

Shares of the five visits before and the five after each MTD-interrupted
visit, pooled over interrupts and runs. Every mutation under IP shuffle
interrupts the attacker (75.0 interrupts per run at 200 s, 7.9 at 2 000 s);
under OS diversity 53 of 75 do (5.6 of 8). Every run in every cell has at least
one interrupt.

| panel | interrupts (model / blind) | JSD before→after: model | blind | placebo (model's positions in its unopposed run) | hosts model / blind |
|---|---|---|---|---|---|
| IP shuffle, 200 s | 30 000 / 30 000 | 0.0004 | 0.0003 | 0.00003 | 0.32 / 0.29 |
| IP shuffle, 2 000 s | 3 171 / 3 179 | 0.0025 | 0.0036 | 0.0021 | 5.47 / 5.11 |
| OS diversity, 200 s | 21 224 / 21 892 | 0.0003 | 0.0004 | 0.00006 | 7.56 / 7.51 |
| OS diversity, 2 000 s | 2 222 / 2 323 | 0.0028 | 0.0057 | 0.0023 | 8.21 / 8.12 |

The paired per-run shift (after minus before, mean ± 95 % interval over 400
runs), attacker model, and the control beside it:

| activity | IP 200 s model | blind | IP 2 000 s model | blind | OS 2 000 s model | blind |
|---|---|---|---|---|---|---|
| scan host | −0.003 ± 0.001 | −0.002 | −0.017 ± 0.003 | −0.019 | −0.016 ± 0.004 | −0.023 |
| enumerate host | −0.004 ± 0.002 | −0.002 | −0.001 ± 0.006 | −0.002 | −0.004 ± 0.008 | −0.004 |
| scan port | +0.004 ± 0.002 | +0.004 | +0.008 ± 0.006 | +0.010 | +0.012 ± 0.008 | +0.014 |
| exploit | −0.009 ± 0.002 | −0.008 | −0.016 ± 0.008 | −0.014 | −0.025 ± 0.011 | −0.026 |
| brute force | +0.007 ± 0.001 | +0.005 | +0.006 ± 0.006 | +0.006 | +0.007 ± 0.007 | +0.002 |
| scan neighbours | +0.005 ± 0.002 | +0.005 | +0.010 ± 0.007 | +0.010 | +0.003 ± 0.009 | +0.014 |
| dwell | 0.000 ± 0.002 | −0.003 | +0.009 ± 0.009 | +0.010 | +0.023 ± 0.012 | +0.027 |

Three things are in the table.

1. **The mix barely moves.** The largest shift on any activity is 2.5 points
   of share (exploit, OS diversity at 2 000 s); the before→after divergence is
   three to four orders below the between-profile divergences of Fig. 5.3
   (0.07–0.21). What direction there is is consistent: after an interrupt the
   attacker exploits less and scans ports and neighbours and brute-forces
   more, which is what a severed position looks like — it has to find a host
   again before it can exploit one.
2. **The verdict-blind control moves the same way by the same amount**, on
   every activity in every panel (the blind column is inside the model's
   interval in 26 of 28 cells). The shift is therefore the interrupt's own
   effect on the token's position and on what the substrate lets it do next,
   not outcome-conditioned routing: with $F_v$ set to the identity the
   attacker re-orients identically. The adaptive loop leaves **no signature**
   in this instrument.
3. **At 200 s the shift clears the placebo null; at 2 000 s it does not.**
   The placebo applies each defended run's interrupt positions to the same
   seed's unopposed run: at 200 s the placebo divergence is a tenth of the
   model's (0.00003 against 0.0004), so the shift is the interrupt's and not
   drift; at 2 000 s the placebo (0.0021–0.0023) is the same size as the model's
   (0.0025–0.0028) — with eight interrupts per run late in a 15 000 s campaign
   the "after" window is also later in the campaign, and drift and response
   are collinear exactly as the 2026-09-09 inference note said they would be.

The breadth side says the same: the outcome-conditioned attacker reaches 0.32
hosts under IP shuffle at 200 s against the blind control's 0.29, 5.47 against
5.11 at 2 000 s, and 8.13 against 8.00 unopposed. Reading verdicts buys the
attacker nothing measurable against this defence family.

**Per profile** (numbers.json `per_profile`): the same picture in every profile;
impact and no-realised-objective carry the largest exploit drop (−0.02 to
−0.05 at 2 000 s) and exfiltration the smallest (≈ 0), on both arms alike.

## 3. What the spanning pair spans

The two mechanisms differ in **how often** they reach the attacker (every
mutation against 71 %) and in **what they do to breadth** (IP shuffle 0.32
hosts, OS diversity 7.56 at 200 s — the severance / surface-re-roll split of
§5.4), not in the **shape** of the response: the six shift vectors are the same
sign and size under both. The pair spans the effect space on outcome and does
not span it on behaviour, because there is no behavioural response to span.

## 4. What the float needs changed — for Marc (APPLIED 2026-09-17)

*Applied as recommended: the figure stands as the null result the section
owes; the caption says the window is interrupt-keyed and pooled over the four
profiles; the placebo null is in the record. The prose (Marc's) has to carry
item 1.*

1. **The figure is a null result and the prose must say so.** The
   placeholder's intention — "to show the adaptive loop operating" — is not
   met: the loop does not operate visibly in the activity mix, and the control
   is indistinguishable from the treatment. Recommended: keep the figure (a
   declared capability reported against the setting at which it is inert,
   whichever way it falls — the ch5 design's own ground for reporting the
   rung), and write the finding as "the model re-orients after an interrupt
   exactly as an attacker that reads no outcomes does". This is the strongest
   form of "operating is a weaker claim than changing an outcome": here even
   operating is not demonstrated by this instrument.
2. **The window is interrupt-keyed, not mutation-keyed.** The caption said
   "each defensive mutation"; a mutation that does not interrupt a visit leaves
   nothing in the record to pair. Caption edited to say so (29 % of OS
   diversity mutations are unpaired).
3. **The placebo null belongs in the prose, not the figure.** One sentence:
   at 200 s the shift is the interrupt's (ten times the placebo); at 2 000 s it
   is not separable from drift.
4. **Dwell is 35 % of every window** and is drawn as an activity. Fine as it
   is; the caption calls the seven "activities".

## 5. Against the record and the board

| quantity | record | here | what moved it |
|---|---|---|---|
| verdict-blind arm | designed as axis 4's control; never run (`outcome.py` docstring: "nothing on record separates *the loop operates* from *the loop helps*") | run at 100 seeds under both spanning mechanisms and two tempos | first measurement |
| board foundation-risk 7 (the control is between-arm; placebo owed) | placebo null "free, owed" | computed: clears at 200 s, not at 2 000 s | the paired positions on the unopposed run |
| board D.2 (the spanning pair) | pair spans severance / re-roll | spans outcome, not behaviour (§3) | no behavioural response exists to span |
| axis 4 badge (`apt_model_criterion.md`) | DESIGNED | the evidence here is that the loop is inert on this instrument; nothing re-scores a badge from a preliminary | — |

## 6. Validation

Zero error rows; every cell at 100; every run has an interrupt in every
drawn cell; the figure fits the page box (15.5 × 10.7 cm); every caption fact
printed by the generator matches `numbers.json`. The interrupt-tally
cross-check (§1) is open.
