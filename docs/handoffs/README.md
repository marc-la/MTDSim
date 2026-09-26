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

**Swept 2026-09-25 (Marc: "any handoffs that are stale, can we remove them ...
have a look for the others").** Nine retired: the 2026-09-09 experiments design,
the 2026-09-20 results context, the 2026-09-22 ch4 overview figure family, the
2026-09-22 defended corpus brief, the 2026-09-24 introduction design and the
2026-09-24 §4.5 brief (all six named stale by Marc); the 2026-09-25 MTDShield
preliminary run (evidence: run, floats and Appendix E.5 landed, commit
7fca1e0b); the 2026-09-21 seminar design and the 2026-09-22 setup-number brief
(deleted by their session, uncommitted until this sweep). `git log` holds each.
The §4.5 drafting records stay tracked in
[`../sources/extractions/s45_metric_definitions/`](../sources/extractions/s45_metric_definitions/).

---

## Open work

- [`2026-09-15_ch6_discussion_affinity_board.md`](2026-09-15_ch6_discussion_affinity_board.md)
  — the discussion board; rulings on the unit split and heading set owed.
- [`2026-09-25_connective_prose_rulings.md`](2026-09-25_connective_prose_rulings.md)
  — ch1–5 connective prose shipped and ratified 2026-09-26; left: fourteen minor
  ch5 wording items, ch5 S20, flagged content, re-check the ch1 overview when
  ch6–8 are drafted; blocks nothing.
- [`2026-09-25_ch4_mark_risk_ledger.md`](2026-09-25_ch4_mark_risk_ledger.md)
  — chapter 4's minor (M) entries beyond C1, for a later pass.
- [`2026-09-25_ch5_setup_defence_and_prose_slots.md`](2026-09-25_ch5_setup_defence_and_prose_slots.md)
  — §5.1 / Table 5.1 defended row by row (17 rows; four facts wrong, three
  stale against §4.5, one variation and one control never reported, one
  scheme dropped unexplained) and the slot plan for every owed chapter 5
  paragraph; §5.1 fixes and all six prose elements LANDED (DRAFT STATE); seven \owed marks and the agents' flags open (Part G).
- [`2026-09-05_generated_tables_house_style.md`](2026-09-05_generated_tables_house_style.md)
  — typography only (the appendix generators onto `\tablestyle`); blocks
  nothing; last-week polish, or drop.

### Carried from the retired briefs (owed, no handoff yet)

The live residue of the nine, so nothing is stranded by the sweep; each line
names the commit or record that holds the detail.

- **The 1 000-seed overnight corpus** at the six intervals (the thesis declares
  1 000; every chapter 5 number is 100-seed preliminary). Retired corpus brief;
  seed-count protocol.
- **Resample by seed** (4.5.4 Variant B): intervals over seeds, the NCR-reduction
  and time-lost bootstraps paired by seed; then swap 4.5.4 to Variant B (commented
  in the tex). §4.5 brief, "Drafted 2026-09-25" (commit 07150a0c).
- **§4.5 open calls** (commits 07150a0c, 07ff1897): APV keeps Hong's name, raise
  it with Dr Hong; the Welch/Holm check in `analyse.py` or the assumption stays;
  θ ≈ 2.95 regenerated at 1 000; Appendix C.4 (detector memory) is a placeholder;
  C.5's numbers regenerate at 1 000.
- **Knock-ons of §4.5:** Table 5.2 prints MTTC without its share of runs; the
  appendix `tab:experiment-one` "ASR" column (rename to ASP) and its MTTC count;
  `tab_5-3-3a_lineage.tex` "mean suppression" → NCR reduction; §5.1's Runs
  paragraph checked against 4.5.4; a Wilson interval for ASP; Figure 5.1's APV
  k = 1 clause; the §5.2 reader's target rule aligned with the record rule; the
  metric catalogue's three stale rows; Table 3.1's missing anchors (Zhan,
  Bruneau, Alavizadeh's mitigation factor); the end-of-run marker filtered from
  steps at the 1 000-seed run; the attack-rate concession sentence owed to §5.2's
  body.
- **The inherited 80 % stop** under the targeted scenario: declared (Marc
  2026-09-25); not yet classified against the intent spec
  (`targeted_objective_probe.md:575`).
- **The introduction** (nine rulings owed, then dictation): its design is in
  the retired introduction brief (`git show <commit>:docs/handoffs/...`).
  Chapter 5's body prose is now owned by the 2026-09-25 setup-and-slots
  handoff above, which also takes §5.1's Runs paragraph against 4.5.4 from the
  §4.5 knock-on list.
- **Seminar:** the submitted title and abstract, re-checked against the
  1 000-seed floats.

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
