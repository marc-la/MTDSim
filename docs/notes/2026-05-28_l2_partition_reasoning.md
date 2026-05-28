---
status: durable
created: 2026-05-28
topic: L2 (GASP) partition — operational objective as the axis
---

# Why L2 exists, and why it slices by operational objective rather than motivation

## Why this is worth recording

L2 is the step the thesis lives or dies on. If the partition cannot be defended,
the research question — "how do MTD mechanisms perform against behaviourally-
grounded adversarial profiles?" — collapses to a single-cell comparison and
ceases to be comparative. The reasoning below is the standing answer to "why
this taxonomy and not another?" and to "is this step even necessary?", both of
which an examiner will reasonably ask. It also names the load-bearing risk
(the "position for future" bucket and its observability-bias confound) so
future-me does not stumble on it mid-defence. The partition decision is
deliberately deferred to the [follow-up investigation](../handoffs/2026-05-28_l2_partition_investigation.md);
what this note locks in is the *framing* against which that investigation is
scored.

## The substance

### What L2 is, in normal English

The pipeline takes raw threat-intelligence reports and gradually distils them
into something a simulator can drive an attacker with. L1 already built one
big graph of "what techniques real adversaries chain together," drawn from
39 documented incidents. L2's job is to slice that graph into a handful of
*behavioural variants* — so we can ask whether different MTD defences hold
up against different *kinds* of attackers, rather than against an
undifferentiated average. Without the slice, "the attacker" is the GAP-average,
and the comparison axis the research question depends on simply does not exist.

### Motivation vs operational objective

The early framing was to slice by **motivation** — espionage / financial /
disruption. The problem is that motivation is rarely written down in a
structured way; in CTI it is an analyst's *inference* from prose like "this
group is believed to be working for nation-state X." Building a partition on
top of an inference adds a layer of guesswork that is hard to defend — and
the structured-CTI fields that should carry it (STIX's `primary_motivation` on
group / campaign objects) are *empty* across all 187 ATT&CK groups and all
52 ATT&CK campaigns, as the 2026-04-16 motivation-exploration notebook
verified.

The cleaner alternative is to slice by **operational objective** — what the
attack actually *did* by the end. That is observable directly in the analyst's
Attack Flow diagram (the last action they drew), so it sidesteps motivation-
as-inference altogether. Alshamrani's APT survey
([`../extractions/alshamrani2019.md`](../extractions/alshamrani2019.md))
makes the structural case for slicing here rather than anywhere else: phases
1–2 of any APT (reconnaissance, foothold establishment) look the same
regardless of goal; **phases 3–5 are where the goal visibly changes the
attacker's behaviour**. That is exactly the region where a partition would
buy you something — slicing the invariant prefix gains nothing, slicing the
objective-conditioned suffix gains everything.

### Three reasons L2 is worth doing at all

Three independent arguments converge — any one would be a candidate
single-point-of-failure for the thesis's research-question framing; all three
agreeing is what makes the step defensible.

- **The research question is itself two-axis.** The lit review's RQ
  ([`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §V) is explicitly
  framed across SDR-family × "profiles differentiated by operational objective
  (Section III-C) — the dimension along which APT campaigns vary, and which
  parametric models collapse." Drop the L2 partition and the second axis
  collapses, leaving a single-cell comparison.
- **The behavioural rung is defined as motivation conditioning.** The lit
  review's fidelity ladder (§IV-B) places the behavioural rung — the bar the
  five surveyed MTD papers are said to fall short of — at "campaign-level
  intent, motivation conditioning, and learning capability." Without L2, the
  work sits at procedural, falls short of the same bar it critiques in others,
  and the §IV-B argument loses its force.
- **The corpus itself shows the structural premise holds.** Of the 38 flows
  in the v0.5 GAP, 11 terminate in exfiltration, 7 in impact-only, and only
  3 in both. Campaigns really do commit to one terminal objective in the data
  we have — exactly the "stages 4–5 split by objective" structure Alshamrani
  predicts. The premise is not borrowed from the literature; it is observed
  directly in the analyst-curated corpus the L2 partition would slice.

### Why these three NIST goals, and not STIX's ten

Three taxonomies are the live candidates: Alshamrani's three NIST-grounded
goals (steal data / damage / position for future), STIX's ten-category
`attack-motivation-ov` vocabulary, or the prior v0.4 code's 30-bucket
"one bucket per terminal technique" approach. They aim at the same target with
very different cardinalities, and the corpus already discriminates between
them:

- **STIX's 10 categories spread too thin.** When Marc hand-labelled 47
  campaigns from external CTI (Mandiant, CrowdStrike, vendor reports), the
  labels collapsed onto just *three* of the ten categories
  (organizational-gain : personal-financial-gain : dominance, split 31:9:7).
  The other seven categories add nothing for this corpus, and the three used
  ones are essentially the Alshamrani triad in STIX clothing.
- **The 30-bucket terminal-technique partition fragments.** Most buckets are
  too small to be useful — the v0.4 notebook reported many *n* < 3
  per-bucket sizes. Useful as a fragmentation-control comparison, not as a
  candidate winner.
- **Alshamrani's three goals are the candidate to beat.** Standards-grounded
  (NIST SP 800-39), derivable directly from each flow's terminal action
  without analyst inference (`exfiltration` → steal_data; `impact` →
  impediment; otherwise → position_for_future), and roughly the right number
  of buckets for downstream evaluation. It is the lightest defensible
  taxonomy: any coarser is the un-partitioned GAP; any finer reintroduces the
  fragmentation the 30-bucket scheme exhibits.

### The honest wrinkle: observability bias in the "position for future" bucket

On the v0.5 corpus the structural mapping yields 11 : 7 : 21 across
`{steal_data, impediment, position_for_future}` — a 28% : 18% : 54% split that
looks lopsided. The reason almost certainly is **observability bias** rather
than a real preponderance of surveillance campaigns. Incident reports stop at
the point of detection, before any exfiltration or impact has happened, so a
campaign that *would* have ended in exfiltration can appear in the corpus as
"ended in lateral movement." This is the same survivorship / selection bias
named in [`2026-05-27_gap_construction.md`](2026-05-27_gap_construction.md) —
the corpus sees the observable middle of the kill chain clearly and the ends
poorly, and the position-for-future bucket inherits that distortion.

Disentangling genuine position-for-future operations from documentation-
truncation is therefore the load-bearing risk for adopting Alshamrani's three-
way. The follow-up investigation either splits the bucket (e.g., "ongoing-
surveillance" vs "truncated-observation"), drops it (narrowing the contribution
claim to a two-class comparison on the observably-completed flows), or accepts
it as-is with a stated disposition. Which of those falls out of the data
rather than being decided in advance.

### Why the partition matters for the Petri-net endpoint

The downstream goal is to encode each behavioural variant as a Petri net for
analytical evaluation (the 2026-05-02 SNAKES primer on `feat/replay-viz`).
This adds a constraint the original framing did not surface: **per-bucket
state-space must be small enough to encode tractably**. An un-partitioned GAP
explodes; a GASP slice of ~14 places and low-tens of transitions does not.
The L2 partition is what *makes* the Petri-net encoding feasible in the first
place — not just a way of stratifying the simulator runs but a precondition
for the analytical substrate the thesis ultimately rests on. This is why the
follow-up investigation adds Petri-net tractability as a sixth rubric
criterion alongside the five from the 2026-04-17 notebook.

### What a negative result would look like

If the investigation's discrimination check shows that the partitioned
attackers produce *indistinguishable* simulator traces — same MTTC, same ASR,
same technique frequencies — then the partition has failed regardless of
rubric score, and the honest move is to drop L2 and let the contribution sit
at L1. That is itself a defensible result: "no partition of this corpus
produces distinguishable behaviour" is a finding worth stating, since it
locates the limit of what CTI-derived behavioural grounding can buy you on
a corpus this thin (88% of edges single-observation, per
[`2026-05-27_gap_construction.md`](2026-05-27_gap_construction.md)). The
contribution then becomes the L1 graph plus the negative result about L2,
rather than the L4 comparison the original framing aimed at.

## How it connects

- To the spec: [`../specs/architecture.md`](../specs/architecture.md) §(e)
  defines L2 / GASP and currently records the terminal-node-ancestor proxy as
  the implemented method with NLP as the parked alternative — this note
  reframes the *axis* (operational objective vs motivation) one level above
  the *method* the spec already discusses.
- To the GAP construction note:
  [`2026-05-27_gap_construction.md`](2026-05-27_gap_construction.md) for the
  observability-bias framing the position-for-future bucket inherits, and for
  the empirical 13/13/3 finding that underwrites the "campaigns commit to one
  terminal objective" claim.
- To the lit review: [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md)
  §III-C (APTs), §III-D (attack profiling), §IV-B (fidelity ladder), §V
  (research question) — the four passages that pin the partition to the
  research question.
- To the extractions: [`../extractions/alshamrani2019.md`](../extractions/alshamrani2019.md)
  for the invariant-prefix / objective-conditioned-suffix structural claim and
  the NIST three-goal source.
- To open work:
  [`../handoffs/2026-05-28_l2_partition_investigation.md`](../handoffs/2026-05-28_l2_partition_investigation.md)
  — the follow-up investigation that scores the four candidate partitions
  (Alshamrani 3-goal, terminal-technique, group-witnessed terminal, reduced
  STIX 3-cat) against a 6-criterion rubric and decides the partition (or
  refuses to).

## When this would need updating

- If the L2 partition investigation lands a winning partition that is *not*
  Alshamrani's three NIST goals — the "candidate to beat" framing here should
  be retired and the chosen taxonomy substituted.
- If the investigation lands a *negative* result (no partition discriminates)
  — the "what comes next" section should be rewritten to record the L1-only
  contribution.
- If the GAP corpus grows to the point where the position-for-future bucket
  is no longer dominated by observability bias — the lopsidedness framing
  here weakens and the bucket's interpretation needs revisiting.
- If the Petri-net workstream is dropped — the sixth rubric criterion
  (tractability) loses its grounding, and the case for keeping per-bucket
  cardinality small needs a different justification.
- If a hand-curated corpus extension (per the GAP per-flow seam) materially
  changes the 11/7/22 split — the empirical premise behind preferring
  Alshamrani's three to STIX's ten weakens, and the comparison needs re-
  running.
