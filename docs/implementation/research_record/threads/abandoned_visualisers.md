# The abandoned visualiser programme — April's biggest investment, June's cleanest cut

**Span:** 2026-04-19 → dropped by 2026-06-23. **Prompts:** #0, #1, #5, #6.
**No shipped record owns this**; the branches survive as `archive/replay-viz`
(and the pre-pivot layout on `archive/attacker-profiling`).

April was substantially a visualisation programme. Two artefacts were being
built in parallel: the **GAP visualiser** (`gap.html` — APT-group and campaign
filters, subgraph selection, attack-path generation; #0–#1 are dense UX
iteration) and the **replay visualiser** (#5–#6): a full situational-awareness
suite — network/attacker/defender/AI-agent/IDS/evaluation panels on a shared
time axis, scoped in a six-layer checklist plan with MUST/SHOULD/STRETCH tags,
POMDP belief views, Q-value inspection at MTD trigger time, and a "core user
flow" in which a user selects a subgraph, operationalises it, runs the sim and
scrubs a timeline. The framing then was **cyber situational awareness**, quoting
the proposal's IDS line — a research direction in its own right.

**The cut, and the stated reasons.** The 23-Jun supervisor update (#13) records
both: "MTDSim visualiser — dropped … too much overhead, consuming too much of my
claude resource". The IDS/detection framing that motivated the SA suite was
culled separately (lit-review §1.3 fold; project_context). Nothing of the
programme's *purpose* survived, but two of its by-products did: the event-log
contract idea (#2, #5) is an ancestor of the trace tooling
([`../../trace_tool.md`](../../trace_tool.md)), and the diagram discipline (#22,
#25, #32 — "speak through visuals", no-bias open diagrams) became the standing
viz conventions.

**Why this thread matters to the dissertation.** It is the cleanest example in
the corpus of scope discipline paying: an entire deliverable class was cut to
fund the pipeline, four weeks before the July reorientation that produced the
thesis's current shape. Candidate one-line mention in discussion/future work; no
more than that.
