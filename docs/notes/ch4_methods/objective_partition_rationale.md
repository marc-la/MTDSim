---
status: durable
chapter: ch4_methods
created: 2026-05-28
updated: 2026-07-13
lineage: 2026-05-28_l2_partition_reasoning.md
---

# Why the attacker model is sliced by operational objective, not motivation

## Position in the dissertation

The methodology chapter's defence of the profile-partitioning step: why the aggregated technique graph is sliced into behavioural variants at all, and why the slicing axis is the campaign's *operational objective* (what the operation demonstrably did) rather than the actor's *motivation* (why an analyst believes they did it). The standing answer to two examiner questions: "why this taxonomy and not another?" and "is this step even necessary?".

## The idea

The pipeline distils published threat intelligence into something a simulator can drive an attacker with. The first stage builds one large graph of the techniques real adversaries chain together, aggregated from thirty-eight documented incidents (see the construction note). This step slices that graph into a handful of *behavioural variants*, so the evaluation can ask whether different MTD defences hold up against different *kinds* of campaign rather than against an undifferentiated average. The thesis lives or dies on this step: its research question — how do existing MTD mechanisms perform against behaviourally-grounded adversarial profiles? — is two-axis (defence family × attacker profile), and without a defensible partition the second axis collapses and the comparison ceases to exist.

### Motivation versus operational objective

The early framing sliced by **motivation** — espionage, financial gain, disruption. The problem is that motivation is rarely written down in a structured way: in threat intelligence it is an analyst's *inference* from prose ("this group is believed to work for state X"), and building a partition on an inference adds a layer of guesswork that is hard to defend. The structured fields that should carry it are empirically empty: STIX's `primary_motivation` is unpopulated across all 187 ATT&CK groups and all 52 ATT&CK campaigns (verified directly against the corpus).

The cleaner alternative is to slice by **operational objective** — what the operation actually *did* by its end, observable directly in the analyst's incident diagram. Alshamrani et al.'s (2019) APT survey makes the structural case for slicing exactly here: the early phases of any APT campaign (reconnaissance, foothold establishment) look alike regardless of goal, while the later phases are where the goal visibly changes behaviour. Slicing the invariant prefix gains nothing; slicing the objective-conditioned suffix gains everything.

### Three independent reasons the step is worth doing

Any one of the following would be a single point of failure for the research question's framing; all three converging is what makes the step defensible. First, the research question is itself two-axis, explicitly framed across defence families and objective-differentiated profiles — the dimension along which APT campaigns vary and which parametric attacker models collapse. Second, the fidelity ladder this work's literature review builds — procedural, parametric, behavioural — places the behavioural rung at campaign-level intent conditioning; without the partition, this work would sit at the same rung it critiques prior work for occupying. Third, the corpus itself exhibits the structural premise: of the 38 incidents, 13 terminate in data exfiltration, 13 in impact, and only 3 in both. Campaigns really do commit to one terminal objective in the data we have — the premise is not borrowed from the literature but observed in the corpus being sliced.

### Why a small objective taxonomy, and not the alternatives

Three candidate taxonomies were live. **STIX's ten motivation categories spread too thin:** hand-labelling 47 external campaigns collapsed onto just three of the ten (organisational gain, personal financial gain, dominance — essentially the survey triad in STIX clothing), leaving seven categories empty. **A per-terminal-technique partition fragments:** it yields dozens of buckets, most with fewer than three members — useful as a fragmentation control, not as a scheme. **Alshamrani's three NIST-grounded goals (steal data / impede / position for future) were the candidate to beat:** standards-grounded, derivable from each incident's terminal action without analyst inference, and roughly the right cardinality. Any coarser is the unpartitioned graph; any finer reintroduces fragmentation.

The adopted scheme is a corpus-shaped refinement of that anchor — four classes: *exfiltration objective*, *impact objective*, *double extortion* (both simultaneously — a compound objective in active operational usage), and *no realised objective* (pre-payload operations; see the honest wrinkle below). The decision record with the full candidate comparison is an implementation-side document; the finding that drove it is summarised in the partition-findings note.

### The honest wrinkle: observability bias in the residual class

A structural reading of terminal actions initially placed over half the corpus in "position for future". That lopsidedness is almost certainly **observability bias**, not a preponderance of surveillance campaigns: incident reports stop at the point of detection, before exfiltration or impact has occurred, so a campaign that *would* have ended in theft appears in the corpus as having ended in lateral movement. The same survivorship bias that blinds the corpus's front end (reconnaissance under-observed) distorts its back end. Disentangling genuine pre-positioning from documentation truncation was the load-bearing risk of the whole partition, and it is why classification was ultimately sourced from the analyst's *stated narrative* rather than from graph structure — a pivot defended at length in the partition-findings note.

### What a negative result would look like

If partitioned attackers produce indistinguishable simulator traces — the same time-to-compromise, success rates, and technique frequencies — the partition has failed regardless of how defensible its construction is, and the honest move is to drop it and let the contribution rest at the aggregated graph plus the negative result. That would itself be a finding worth stating: "no partition of this corpus produces distinguishable behaviour" locates the limit of what CTI-derived behavioural grounding can buy on a corpus where 88% of edges are single-observation.

## Evidence and repo anchors

- Upstream: [`technique_graph_construction.md`](technique_graph_construction.md) (the graph, its thinness, the 13/13/3 terminal-objective observation and observability-bias framing).
- The adopted scheme's full decision record (six candidate schemes, rubric, discrimination evidence, per-incident audit): [`../../implementation/pipeline/gasp/partition_decision.md`](../../implementation/pipeline/gasp/partition_decision.md) and [`per_flow_justifications.md`](../../implementation/pipeline/gasp/per_flow_justifications.md); canonical data model in [`gasp_schema.md`](../../implementation/pipeline/gasp/gasp_schema.md).
- What the partition *found*: [`objective_partition_findings.md`](objective_partition_findings.md); the operator-concentration caveat: [`operator_concentration.md`](operator_concentration.md).
- Literature: [`alshamrani2019`](../../sources/extractions/alshamrani2019.md) (three-goal anchor; invariant prefix / objective-conditioned suffix).

## Revisit conditions

- If the simulator-level discrimination test fails (see [`../ch5_experimental_setup/evaluation_burden.md`](../ch5_experimental_setup/evaluation_burden.md)) — rewrite around the negative-result disposition.
- If the corpus grows enough that the residual class disambiguates (genuine surveillance vs pre-payload vs truncation) — the four-class cardinality re-opens.
- If a hand-curated corpus extension materially changes the class ratio — the empirical premise for preferring the small taxonomy needs re-running.
