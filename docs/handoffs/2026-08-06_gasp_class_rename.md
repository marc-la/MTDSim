---
status: open
created: 2026-08-06
---

# Rename the four GASP classes to self-documenting objective-tactic labels, and carry the rename through code, data, figures and docs

## State of play

### The naming problem, as posed

The four L2 classes are named `pure_steal`, `pure_impediment`,
`double_extortion`, `infrastructure_setup`. Three of the four are internal
coinages (`pure_steal` and `pure_impediment` are Alshamrani's `steal_data` /
`damage` re-worded; `infrastructure_setup` is this project's rename of
Alshamrani's `position_for_future`, argued in
[`gasp_schema.md`](../implementation/pipeline/gasp/gasp_schema.md) §(b)
Decision 5). None of them tells a reader which ATT&CK tactic the class is
about, and every downstream record — the Petri feasibility study, the
timeline report, the demonstration arms, the exposure study — has to
re-explain the mapping in prose each time it needs it. The ask is to make the
label carry that information.

### The premise as stated is falsified — check this before writing any prose

The task was framed as *"the profiles were created filtered on their
terminating tactic"*. **They were not, and the schema's central invariant says
so explicitly.** This matters for the rename because a tactic-derived name
would otherwise read as a claim about how membership was decided.

[`gasp_schema.md`](../implementation/pipeline/gasp/gasp_schema.md) §(a):

> **Central invariant — every class membership corresponds to an objective the
> analyst stated, not an objective inferred from graph structure.** No flow's
> class is decided by terminal-node detection, ancestor closure, or any other
> structural heuristic over the GAP.

Membership comes from the `stated_objective` column of
[`data/gasp/metadata_audit.csv`](../../data/gasp/metadata_audit.csv), read by
analysts out of CTI narrative, and is remapped to the class label at build time
by `CSV_LABEL_TO_CLASS` in
[`selector.py:25`](../../src/mtdsim/l2_subgraph/selector.py#L25). The
terminal-tactic scheme was a *candidate that lost*: P1 (structural-terminal
3-class) is scored and rejected in
[`partition_decision.md`](../implementation/pipeline/gasp/partition_decision.md),
and it disagrees with the audit on 15 of 38 flows (40 %), systematically
mis-classifying truncated breach reports.

The audit CSV's own descriptive columns confirm it — the classes are not
terminal-tactic-separable even loosely:

| Class | n | flows with the "expected" tactic among `terminal_tactics` | `reaches_exfiltration` | `reaches_impact` |
|---|--:|--:|--:|--:|
| `pure_steal` | 19 | exfiltration in 7/19 (and one flow terminates on `impact`) | 10/19 | 1/19 |
| `pure_impediment` | 8 | impact in 6/8 | 0/8 | 6/8 |
| `double_extortion` | 6 | exfiltration **and** impact in 1/6 | 3/6 | 6/6 |
| `infrastructure_setup` | 5 | command-and-control in 1/5 | 0/5 | 0/5 |

`terminal_tactics` is multi-valued and messy (one `pure_steal` flow's terminal
set is seven tactics wide). The CSV header itself marks these columns
*"Structural metadata (descriptive — **not** the class mechanism, per Decision
3)"*.

### What *is* true, and what the rename should be named after

There **is** a per-class tactic mapping in the codebase, and it is exactly the
one recalled in the ask — all four guesses match. It lives at
[`analysis.py:44`](../../src/mtdsim/l3_simulation/petri/analysis.py#L44):

```python
OBJECTIVE_TACTICS: dict[str, tuple[str, ...]] = {
    "pure_steal": ("exfiltration",),
    "pure_impediment": ("impact",),
    "double_extortion": ("exfiltration", "impact"),
    "infrastructure_setup": ("command-and-control",),
    "aggregate": ("command-and-control", "exfiltration", "impact"),
}
```

This is a **declared downstream choice**, not the L2 filter: it is the
class-semantic objective tactic each profile's Petri net is analysed against,
sourced from the feasibility study §4. It is load-bearing — consumed by
`petri/divergence.py`, `movement/utility.py`, `timeline/report.py` and two test
modules — and it is already the thing every record means when it says "the
class's objective".

**So the rename is defensible, but only if it is named against
`OBJECTIVE_TACTICS` and described as the declared objective, never as the
selection filter.** The next session should write the rename's justification in
those terms and should not repeat the "filtered on terminating tactic" framing
anywhere.

One caveat rides on the fourth class, recorded in the same comment block:

> `infrastructure_setup -> command-and-control` (no impact/exfiltration exists;
> its absorbing condition is C2-established, **a foothold, not an attacker goal
> in the impact sense**)

Naming that class after C2 promotes a documented *non*-objective to an
objective in the label. That is the one naming decision that needs a ruling
(below).

### Blast radius, measured

249 text files contain at least one class name. 93 are tracked; 156 are
gitignored regenerable workspaces. 102 files carry a class name in the
*filename* (8 tracked).

| Where | Files | What |
|---|--:|---|
| `docs/` (tracked) | 37 | schema, architecture, criterion, ~25 ogasp records, 3 notes, 1 archived handoff, 2 extractions |
| `src/mtdsim/` | 16 | 4 duplicated name tuples, `OBJECTIVE_TACTICS`, `CSV_LABEL_TO_CLASS`, docstrings, report prose |
| `tests/` | 15 | parametrised class ids, golden assertions |
| `data/` (tracked) | 23 | 8 class-named JSONs, 2 CSVs, 3 reports, 4 declared-value families, 6 READMEs/schemas |
| other (tracked) | 2 | `tools/mtd_golden_streams.py`, `baseline/CHANGELOG.md` |
| `data/results/*` (ignored) | ~65 | 16 experiment workspaces: runners, `numbers/`, figure scripts |
| `data/ogasp/timeline/_timelines/` (ignored) | 55 | one JSONL per (profile × entry × policy × variant) cell |
| `data/gasp/_viz/`, `data/misc/_viz/`, `data/ogasp/*/_viz/` (ignored) | ~22 | 24 GASP figures, 12 petri figures, 4 walk figures, 2 viz scripts |

Tracked class-named files that must be renamed on disk:

```
data/gasp/gasp_{pure_steal,pure_impediment,double_extortion,infrastructure_setup}.json
data/ogasp/petri/{pure_steal,pure_impediment,double_extortion,infrastructure_setup}_structural.json
```

## Recommended approach

### 1. Fix the vocabulary in one commit

The name set is the only thing that cannot be reversed cheaply once ~90 tracked
files have moved. It is now ruled (2026-08-06), so this is unblocked.

**The set** — `objective_`-prefixed, one token per ATT&CK tactic:

| Current | Proposed |
|---|---|
| `pure_steal` | `objective_exfiltration` |
| `pure_impediment` | `objective_impact` |
| `double_extortion` | `objective_exfiltration_impact` |
| `infrastructure_setup` | `objective_none_c2` — **ruled by Marc 2026-08-06**, reasoning below |

**Why the prefix, rather than bare `exfiltration` / `impact` / `c2`.** The
tactic vocabulary is *already in use as a first-class namespace* in this
codebase: Petri-net **places are tactics**, spelled exactly
`"exfiltration"`, `"impact"`, `"command-and-control"`. A bare rename produces
`OBJECTIVE_TACTICS["exfiltration"] = ("exfiltration",)`, makes every grep for a
tactic return profile hits and vice versa, and makes the 55 timeline filenames
(`<profile>--<entry>--<policy>--<variant>.jsonl`) ambiguous where `entry` is
already a tactic. The prefix costs eight characters and removes the collision
entirely.

**Why underscores, not hyphens, in `command_and_control`.** The class names are
Python identifiers, dict keys and filename stems; the tactic strings are
hyphenated. Keeping the two spellings distinct is a feature — it makes the
class-vs-tactic distinction visible at a glance.

**Alternatives considered.** *(a)* Bare tactic names — rejected on the
collision above. *(b)* Keep the semantic head and append the tactic
(`steal_exfiltration`) — carries the coinage forward, which is what the rename
is trying to remove. *(c)* `ta0010` / `ta0040` / `ta0011` ATT&CK IDs — precise
and collision-free, but self-documenting only to a reader who has the ID table
memorised, which is the opposite of the goal. *(d)* Leave `double_extortion`
alone because it is genuine operational CTI vocabulary (the schema defends it
on exactly that ground, §(b) Decision 2) — a reasonable partial position, but
it leaves the set internally inconsistent, and the compound name is the one
that most needs to say *which two* tactics.

### 2. Do **not** re-issue the audit CSV

[`gasp_schema.md`](../implementation/pipeline/gasp/gasp_schema.md) §(c)
carries an *If revisited* clause offering to re-issue
`metadata_audit.csv` with renamed labels. **Decline it.** The CSV's
`stated_objective` values (`steal_data`, `impediment`, `double_extortion`,
`position_for_future`) are Alshamrani's vocabulary as the analysts applied it;
they are the audit trail, and `CSV_LABEL_TO_CLASS` is the seam that keeps the
provenance layer and the spec layer separately nameable. Rewrite the seam's
right-hand side only, and add a line to §(c) saying the seam now spans three
vocabularies (Alshamrani → spec → tactic) and why the left-hand side is frozen.

### 3. Rename in code, preserving tuple order exactly

Four separate hard-coded name tuples exist and must all move together:

- [`l2_subgraph/schema.py:16`](../../src/mtdsim/l2_subgraph/schema.py#L16) `CLASS_NAMES` — the canonical one
- [`l3_simulation/timeline/walk.py:46`](../../src/mtdsim/l3_simulation/timeline/walk.py#L46) `CLASS_NAMES` — a duplicate
- [`l3_simulation/movement/net.py:43`](../../src/mtdsim/l3_simulation/movement/net.py#L43) `PROFILES`
- sorted literals in [`movement/succession.py:457`](../../src/mtdsim/l3_simulation/movement/succession.py#L457), [`movement/alignment.py:522`](../../src/mtdsim/l3_simulation/movement/alignment.py#L522), [`petri/viz.py:267`](../../src/mtdsim/l3_simulation/petri/viz.py#L267)

Collapsing the duplicates onto one import is a defensible tidy-up and is
in scope; **re-sorting any of them is not** (see Hard constraints).

### 4. Regenerate, in dependency order

```sh
PYTHONPATH=src python -m mtdsim.l2_subgraph              # classification.csv + 4 × gasp_<class>.json
python data/gasp/_viz/gasp_viz.py                        # 24 GASP figures (gitignored)
PYTHONPATH=src python -m mtdsim.l3_simulation.petri      # 5 structural nets + divergence report + _viz/
PYTHONPATH=src python -m mtdsim.l3_simulation.timeline   # timeline library + example + report + _viz/
PYTHONPATH=src python -m pytest tests/                   # full gate
```

The 16 `data/results/` workspaces are gitignored and regenerable but **not
free** — several are multi-hour sweeps. Do not re-run them wholesale. Patch
each workspace's runner and analysis script so a *future* run uses the new
names, and leave the existing `numbers/` where they are; the tracked record
that quotes them is the durable artefact, and it gets a banner (step 5) rather
than a re-run. Flag any workspace where this leaves a runner and its committed
numbers disagreeing.

### 5. Split the docs two ways — this is the half that is easy to get wrong

[`docs_map.md`](../workflows/docs_map.md) §`implementation/` contract:
*"Investigation records are immutable history — annotate with status banners
rather than rewriting them."* Frontmatter does not distinguish the two kinds
(nearly every affected file says `status: durable`), so apply the test by kind,
per file:

- **Live specs, schemas and READMEs → rewrite in place.**
  `gasp_schema.md`, `architecture.md`, `apt_model_criterion.md`,
  `metrics_semantics.md`, `provenance.md`, `trace_tool.md`,
  `boundary_attacker_defender_channels.md`, `data/gasp/README.md`,
  `data/ogasp/petri/README.md`, `data/ogasp/timeline/timeline_schema.md`,
  `src/mtdsim/l2_subgraph/README.md`. Bump `updated` in the same commit.
- **Records of a run, with dated numbers → banner, do not rewrite.**
  The ~25 `pipeline/ogasp/*` findings, studies, pre-registrations and
  feasibility records, plus `partition_decision.md` and
  `per_flow_justifications.md`. A record that reports figures produced under
  the old names should keep saying the old names; rewriting them silently
  re-attributes evidence to labels that did not exist when it was taken. Add a
  one-line banner under the frontmatter pointing at the rename commit and the
  mapping table.
- **Notes (`docs/notes/ch3_design/`) → rewrite**, but they are
  dissertation-bound prose: load [`voice.md`](../workflows/voice.md) and
  [`notes_rubric.md`](../workflows/notes_rubric.md) first, and note that
  `objective_partition_findings.md` and `objective_partition_rationale.md`
  argue the partition *axis*, so their prose may need more than a token swap.
- **`docs/sources/extractions/` → do not touch.** `alshamrani2019.md` and
  `mandiant2013.md` use `steal_data` / `position_for_future` because
  Alshamrani does. They are fair-use extracts of someone else's vocabulary.
- **`docs/handoffs/__archive/` → do not touch.** Parked history.

Put the mapping table itself in `gasp_schema.md` §(c) as a permanent
three-column crosswalk (CSV label → old spec label → tactic label), so every
banner has one place to point at and so the ~30 untouched records stay
readable.

## Validation gate

1. `PYTHONPATH=src python -m pytest tests/` — green, with **the same test count**
   as before the rename (a parametrised id that silently stops matching is the
   most likely way to lose coverage here; compare `--collect-only -q` counts).
2. `command grep -rIn "pure_steal\|pure_impediment\|double_extortion\|infrastructure_setup" $(git ls-files)`
   returns hits **only** in: the crosswalk table, banner lines, the
   `sources/extractions/` pair, `handoffs/__archive/`, and the record files
   deliberately left as history. Every remaining hit is on that list or it is a
   miss. (Use `command grep` — the shell's `grep` respects `.gitignore` and will
   hide the workspaces.)
3. **The divergence report's numbers are unchanged.** Diff
   `data/ogasp/petri/divergence_report.json` before and after: every value must
   be identical, only keys renamed. A changed null band means the class tuple
   was re-ordered — see Hard constraints.
4. `data/gasp/classification.csv` still has 38 rows with the 19 : 8 : 6 : 5
   split, and `data/gasp/gasp_*.json` still report 98 / 62 / 57 / 39 nodes.
5. The four class-named JSON pairs are renamed on disk via `git mv`, so the
   rename shows as a rename in `git log --follow`.
6. Every rewritten `implementation/` file has `updated: 2026-08-06` in its
   frontmatter; every banner-only file does **not**.
7. Figures regenerate and the 2×2 grids still carry four legible panels — panel
   order changes if the tuple order changes, which is the visual tell for
   constraint 1.

## Hard constraints

- **Preserve the class tuple order.** `petri/divergence.py:168` builds
  `sizes = [(cls, len(class_flows[cls])) for cls in CLASS_NAMES]` and slices a
  seeded shuffled pool by cursor in that order. The four class sizes are all
  distinct (19, 8, 6, 5), so **any re-ordering of `CLASS_NAMES` silently changes
  every per-class null band** in the committed divergence report. Rename in
  place, position for position. Do not alphabetise, do not "tidy" the order to
  match the new names.
- **`aggregate` is not a GASP class** and is not renamed. It appears alongside
  the four in `PROFILE_NAMES`, `OBJECTIVE_TACTICS` and the stall reports as the
  null profile.
- **The audit CSV's `stated_objective` values are frozen** (§2 above).
- **Investigation records are immutable** ([`docs_map.md`](../workflows/docs_map.md)
  §`implementation/`) — banner, don't rewrite.
- **No re-baseline.** Nothing here should move a number. If a golden or a
  committed report changes by more than its keys, stop and diagnose — that is a
  bug in the rename, not an expected consequence.
- **Do not re-frame the classes as terminal-tactic-derived** in any prose. The
  schema's central invariant forbids it and the audit data contradicts it.
- Branch / commit / push rules from
  [`session_workflow.md`](../workflows/session_workflow.md): dedicated branch
  (`chore/gasp-class-rename`), stage by file, never push, delete this handoff in
  the commit that ships the work.

## The fourth class — ruled 2026-08-06

**`infrastructure_setup` → `objective_none_c2`.**

`OBJECTIVE_TACTICS` maps this class to `command-and-control`, but the code
comment that declares the mapping says C2 here is *"a foothold, not an attacker
goal in the impact sense"*, and `gasp_schema.md` Decision 5 defines the class by
what its flows **did not reach** — five pre-payload operations, three of them
carrying DFIR's *"evicted before completing their mission"*. The other three
classes are named after a tactic the operation was *for*; a bare C2 name would
name this one after the tactic it *stopped at*.

Two measurements decided it. First, the class's surface subgraph is **the only
one of the four with zero exfiltration and zero impact techniques** — that
absence, not any tactic's presence, is what makes it a distinct class. Second,
C2 is **not** distinctive for it:

| Class | techniques | C2 | exfiltration | impact |
|---|--:|--:|--:|--:|
| `infrastructure_setup` | 39 | 5 (11 %) | **0** | **0** |
| `pure_steal` | 98 | 10 (9 %) | 5 | 1 |
| `pure_impediment` | 62 | 5 (8 %) | 0 | 7 |
| `double_extortion` | 57 | 4 (7 %) | 2 | 6 |

At 11 % against 7–9 % elsewhere, C2 is barely elevated.
`objective_command_and_control` sitting beside `objective_exfiltration` would
invite the reading *"this is the C2 one"*, and that inference is false.
`objective_none_c2` states the distinctive fact first and keeps the declared
absorbing tactic visible for anyone reading `OBJECTIVE_TACTICS`.

Alternatives rejected: `objective_command_and_control` (set-consistency, but
asserts what three sources deny and what the shares above do not support);
`pre_objective_c2` (`pre_objective` is a coinage, leaving the class half-coined —
the thing the rename exists to remove); keeping `infrastructure_setup` (see the
collision below).

**The current name is the least MITRE-aligned in the set, independently of all
this.** MITRE TA0042 *Resource Development* is literally adversary
infrastructure setup — `T1583 Acquire Infrastructure`, `T1584 Compromise
Infrastructure` — and `resource-development` is a live tactic in this repo's own
vocabulary. `infrastructure_setup` therefore reads as "the TA0042 class", which
is adversary-side infrastructure and not what this class is at all. Renaming it
is well-motivated on that ground alone.

`gasp_schema.md` Decision 5 still gains a sentence in the rename commit
recording that the label names the class's declared absorbing tactic and not a
realised objective — the caveat belongs at the definition site.

**Still open, smaller:** whether `double_extortion` is renamed at all. It is the
one label that is real CTI vocabulary rather than a coinage, and the schema
defends it as such — but it is also the one whose tactic content a reader cannot
guess.

## Corpus and ATT&CK freshness — verified 2026-08-06

Checked before settling the vocabulary, since a stale corpus would undercut a
tactic-derived naming scheme. **Nothing is pending; the rename proceeds on the
committed artefacts.**

- **The tactic vocabulary is stock ATT&CK, not a project coinage.** The pinned
  bundle is `enterprise-attack-19.1.json`, **byte-identical (sha256) to
  upstream**. `stealth` is TA0005 (renamed from *Defense Evasion* at v19) and
  `defense-impairment` is TA0112 (new at v19). All 15 shortnames in
  `gap_v0.5.json` are the bundle's own, so "MITRE-aligned" needs no caveat — the
  namespace already is MITRE.
- **ATT&CK v19.2 exists and is a no-op here.** Identical tactic vocabulary,
  identical 697-technique live catalogue, and **0 changes** across all 124 GAP
  techniques — no revocations, no renames, no tactic reassignments. Bumping the
  pin would change nothing; leave it at 19.1 unless something else motivates it.
- **The corpus was fetched *after* the version change, not before.** Attack Flow
  v3.2.0 ("ATT&CK v19.1") was tagged 2026-05-15; `data/gap/_corpus_stix/` was
  fetched 2026-05-27.
- **0 of 38 flows have changed** in anything L1 consumes. All 38 live STIX
  exports were re-fetched and compared on action count, technique set, operator
  count and condition count: every flow identical. The sole delta is `Equifax
  Breach` gaining 9 `x-detection` + 9 `x-mitigation` objects (AF-392,
  2026-07-24) — a new annotation layer the GAP does not read; its 12 actions and
  12 techniques are unchanged.
- **One new upstream flow**, `OpenClaw Command & Control via Prompt Injection`
  (2026-07-24) — an OpenClaw variant, covered by the exclusion already recorded
  in `fetch.py` and in `per_flow_justifications.md` (§*Dropped from corpus*).
  Worth one line in `fetch.py` naming it explicitly, so the next session does not
  re-derive the exclusion.

**One fragility found, out of scope for this handoff.** `CORPUS_BASE_URL` points
at CTID's GitHub Pages docs site, which serves *current* content — so
`CORPUS_REF = "attack-flow@v3.1.1"` is a recorded claim, not an enforced pin, and
`python -m mtdsim.l0_cti --force` today would silently pull the Equifax
annotation layer. Harmless as of this check, but the corpus half of L0 is
unpinned in a way the ATT&CK half is not. Note also that v3.2.0 was already
tagged 12 days before the fetch, so the recorded `v3.1.1` ref probably
understates what is held — the substance is identical either way. Flagged for its
own brief.

## Reading list

- [`docs/implementation/pipeline/gasp/gasp_schema.md`](../implementation/pipeline/gasp/gasp_schema.md)
  — §(a) central invariant, §(b) Decisions 2 and 5, §(c) CSV↔spec mapping. The
  canonical target of the rewrite.
- [`src/mtdsim/l3_simulation/petri/analysis.py:30-50`](../../src/mtdsim/l3_simulation/petri/analysis.py#L30-L50)
  — `OBJECTIVE_TACTICS` and the comment block that justifies it. The thing the
  new names are named after.
- [`src/mtdsim/l3_simulation/petri/divergence.py:155-190`](../../src/mtdsim/l3_simulation/petri/divergence.py#L155-L190)
  — the order-sensitive null calibration. Read before touching any name tuple.
- [`docs/implementation/pipeline/gasp/partition_decision.md`](../implementation/pipeline/gasp/partition_decision.md)
  — why P1 (structural-terminal) lost. The evidence that the premise correction
  rests on.
- [`docs/workflows/docs_map.md`](../workflows/docs_map.md) §`implementation/`
  — the immutable-records contract that splits step 5.

## Out of scope (explicitly)

- **Re-partitioning.** The 19 : 8 : 6 : 5 membership does not change. This is a
  vocabulary refactor, not a re-classification. The open questions in
  `gasp_schema.md` §(h) — the ToolShell flow-split, the fifth `monetisation`
  class, corpus-growth thresholds — all stay open and untouched.
- **Re-running the `data/results/` sweeps.** Patch the runners; leave the
  numbers.
- **Re-issuing `metadata_audit.csv`.**
- **Changing `OBJECTIVE_TACTICS`' values.** The mapping is the input to the
  rename, not a thing the rename gets to revise. If it looks wrong, that is a
  separate disposition.
- **Renaming `aggregate`, the entry-tactic names, or the Petri place vocabulary.**
- **Anything on the axis chain** (items 1–3 of the
  [open chain](README.md)). This handoff is independent of all three and blocks
  none of them, but it touches nearly every file they write into — so it should
  land *between* their commits, not alongside them.
