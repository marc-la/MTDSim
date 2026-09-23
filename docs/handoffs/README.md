# The open chain — dependency order

`ls docs/handoffs/` is the inventory of open work; this file carries only the
thing a directory listing cannot — **what depends on what**, and what is waiting
on a ruling. Delete a handoff in the commit that ships its work, and prune its
line here in the same commit.

**Reset 2026-08-05.** This file had accumulated ~450 lines of shipped-work
archaeology, which its own contract says to prune. Every shipped entry named the
record it landed as; those records are the permanent account, and `git log` is
the permanent history. Parked work is in [`__archive/`](__archive/).

**Swept 2026-09-22 (post-meeting, on Marc's direction).** Ten handoffs
retired, each by evidence: the four-file ch3 chain (design brief, port plan,
patchwork draft, §3.3 context — §3.1–§3.2 through pass 6, §3.3.2 ratified,
§3.3.3 through pass 5; the residue is in the tex's own DRAFT STATE comments at
l.~3643 and one CONFIRM, the ATT&CK pin v19.1 against Marc's spoken "19.2"); the
§4.3 formalism inventory (the formalism landed 2026-09-08 and the supervisor
accepted it 2026-09-22 — the notation simplification is Marc's own item, register
E9); the ch5/ch6 structure question (superseded twice, by the 2026-09-08
one-chapter ruling and by E1); the two run plans and the two §5.1 briefs (their
floats and rebuilt units landed; every owed item they still carried is named in
the 2026-09-22 corpus and setup handoffs). `git log` holds each file.

---

## Open work — the 2026-09-22 chain, in the order to run it

The supervisor's 22 September rulings (register E1–E11) reshape the evaluation.
Six briefs execute them. The order below is the critical path, not the file
order: the corpus is the long pole and depends on no wording, so it starts
first; the rulings pass is one sitting; the three middle briefs run in
parallel sessions; the restructure moves the tex last, once the words, the
metrics and the numbers exist.

1. [`2026-09-22_ch5_defended_corpus_schemes_intervals_mtdshield.md`](2026-09-22_ch5_defended_corpus_schemes_intervals_mtdshield.md)
   — **the runs (E6, E7)**: every deployment strategy including MTDShield as
   released, the interval as a six-point range, both attackers, 100-seed smoke
   tonight then 1 000 overnight. Q1–Q5 owed; Q5 is "launch the smoke". Feeds
   every other brief's floats.

2. **Marc's rulings pass, one sitting**: the metric dispositions
   (`metrics_provenance_and_instrumentation` §1), the setup rulings
   (`ch5_setup_number_justification`). Everything downstream regenerates floats
   with these words on them, so nothing is applied before this. *(The
   terminology table was ruled and applied 2026-09-22 — the model is the APT
   attacker model, the layer names are dissolved, the registry is flipped and
   every float regenerated; only the word* suppression *waits, with the metrics
   brief. The reader-overhead screen that came out of it is now sweep 4 of the
   `voice-pass` skill, with `tools/term_screen.py` as its census.)*

3. In parallel, after the rulings:
   - [`2026-09-22_metrics_provenance_and_instrumentation.md`](2026-09-22_metrics_provenance_and_instrumentation.md)
     — **the metrics (E3, E4)**: a source for every Table 5.2 row, the chapter 4
     unit that defines the new ones with why, stealth and detectability back in
     Table 5.3; owns the internal-MTTC finding. Marc dictates the unit.
     *Re-cut 2026-09-23 on Marc's direction (efficiency rows out, grouped by
     phase, the field's names; stealth as attack intensity, adapted from He);
     §4.5 Instrumenting MTDSim heading placed; §5.2's fidelity picture
     proposed with a dry-run. Six rulings owed.*
   - [`2026-09-22_ch5_setup_number_justification.md`](2026-09-22_ch5_setup_number_justification.md)
     — **the numbers (E5)**: the background table of the lineage's
     configurations and one clause per §5.1 value; the numerals rule.
     *Landed 2026-09-23 (Table 2.2, Table 5.1's citations, the §5.1 clauses,
     the rule; clauses ratified, 2 000 s ruled the top of a 50–2 000 s range).
     Only the two-target reason is owed.*
   - [`2026-09-22_ch4_overview_figure_family.md`](2026-09-22_ch4_overview_figure_family.md)
     — **the figure (E8)**: the head figure as boxes, a zoom per section, and the
     three chapter 5 figure fixes. Marc's day; the terminology ruling it waited
     on (the boxes' names) landed 2026-09-22: the profile net, the join, MTDSim.

4. *The chapter (E1, E7, E10) landed 2026-09-23:* the heading set ruled
   (§5.2 *APT attacker model versus baseline attacker*; §5.3 *APT attacker model
   versus MTD* = response to disruption, effect of the attacker model, defence
   mechanisms and execution schemes), the tex moved, §5.3.3 and §5.4 retired,
   the brief retired. Its residue rides the metrics, figure and results-context
   briefs.

5. Then the discussion:
   [`2026-09-15_ch6_discussion_affinity_board.md`](2026-09-15_ch6_discussion_affinity_board.md)
   — the board, with the supervisor's two set-ups appended (§9). Rulings on the
   unit split and the heading set still owed. Jin: "once this is done then we're
   good for the discussion".

Standing context that survives the sweep:

- [`2026-09-20_ch5_s52_s54_results_context.md`](2026-09-20_ch5_s52_s54_results_context.md)
  — the frame (§5), the paragraph shape (§3) and every figure's record (§8)
  stand; its §2–§4 and §6 are superseded in shape by the restructure brief
  (banner at its head). Retires with the last results section through pass 6.
- [`2026-09-09_ch5_experiments_design.md`](2026-09-09_ch5_experiments_design.md)
  — the design record: the funnel, the property-to-measurement map the
  discussion's fidelity table depends on, and the debt ledger. Its section
  shape is superseded by E1 (frontmatter says so); the rest stands.
- [`2026-09-21_seminar_title_abstract_design.md`](2026-09-21_seminar_title_abstract_design.md)
  — retires when the submitted title and abstract are recorded; its two
  results sentences re-check against the thousand-seed floats.
- [`2026-09-05_generated_tables_house_style.md`](2026-09-05_generated_tables_house_style.md)
  — typography only (the appendix generators onto `\tablestyle`); blocks
  nothing; last-week polish, or drop.

---

## Decisions waiting on Marc

Nothing below blocks a handoff except where noted; all of it blocks *closing*
one. The full rows, with costed options, are in the disposition list of
[`../implementation/intent_conformance_audit.md`](../implementation/intent_conformance_audit.md).

| # | What | Blocks |
|---|---|---|
| **The 2026-09-22 rulings pass** | the four tables named in step 2 above — one sitting | every 2026-09-22 brief's apply step |
| **Overleaf** | the dissertation project's ID and git token (the only configured project is the literature review) | the push of every landed float |
| **Overlay: re-key experiment 2 under `v4`?** | `v4_failure_only` is the go-forward overlay (2026-08-19) and the chapter runs on it; whether the older experiment-2 record is re-run under it or stands on `v3` with the feasibility study as the bridge | nothing in ch5 now — a ch6/ch7 sentence at most |
| **D-09** | Zhang's unimplemented give-up threshold — the generalising measure shipped; whether it is ratified ([`attacker_disengagement.md`](../implementation/pipeline/ogasp/attacker_disengagement.md) §8) | — |
| **D-16 · D-17 · D-19 · D-26** | Eq 2's `V_exploited` half; the decoupled OSDA formulation; the commented-out OS gate; `Host.total_users` | — |
| **D-18** | OS Diversity's inert compatibility guard: a repaired guard replaces 13.9 % against Service Diversity's 100 % | the diversity pair's separability |
| **D-27** | the credential channel carries 10–23 % of compromises and no reported mechanism moves it | family scope |
| **D-29** | two shared RNG streams: seed-matched arms are independent, not paired — state once where the cross-arm test is named | seed budgeting; the corpus brief states it |
| **D-30/31/32** | NAV feed degeneracy; HostTopologyShuffle desync; UserShuffle's ratchet — the last is the mechanism behind user shuffle's negative effect on the model (corpus brief §4) | the attribution sentence |
| **D-33** | SCAN_NEIGHBOR dispatched from uncompromised hosts (48 % of calls in the model's arm); measured to move a ranking | any scheme ranking |
| **D-34 · D-35 · D-36 · D-37 · D-38** | HostTopologyShuffle's direct write; EXPLOIT_VULN uninterruptible in the model's arm (89–97 % of the diversity family's windows lost); the lost cursor clear (the one candidate bug, repair recommended); the unpriced confusion penalty; the priority-queue extra firing (identical in both arms) | the diversity family's cross-arm reading; within-pair claims |

**Attached to no handoff:** the axis-7 records report the axis in performance
terms and under-report it (re-frame?); the retrace re-take for the three
sink-bearing profiles; tempo claims confined to within-arm comparisons
([`stealth_dutycycle.md`](../implementation/pipeline/ogasp/stealth_dutycycle.md)
§8 — now load-bearing for the reinstated stealth column, so the metrics brief
carries the caveat); the per-vulnerability row count (3.75× against per-action
counts; `baseline_action_rows` is the correction).

*(The internal-MTTC finding this section carried unowned since 2026-08-05 is now
owned by the metrics brief, §2.)*

---

## The boundary programme — closed 2026-08-05

Two durable records survive it and are the reference for anything touching the
attacker/defender/network seams:
[`attacker_read_surface.md`](../implementation/attacker_read_surface.md) (what
the attacker perceives — no host label at all) and
[`mtd_write_surfaces.md`](../implementation/mtd_write_surfaces.md) (every
mechanism's write set). IP Shuffle's invisibility to the attacker is documented
behaviour, not an integration artefact; the OS/Service half is a broken
documented wire (D-18). The open dispositions live in the audit's list above.

## Parked

A sensitivity study over `VULN_PERCENT_CROSS_PLATFORM` (the diversity pair as
one mechanism at the lineage's default) — parked by Marc 2026-08-05; needs a
joint move, evidence in `attacker_read_surface.md` §(g). Older parked work is in
[`__archive/`](__archive/).
