---
status: open                  # executes register E2; ONE ruling pass by Marc on the replacement table (§2), then the sweep is mechanical
created: 2026-09-22
executes: docs/implementation/pipeline/ogasp/supervisor_decision_register.md §E2
companions: ../workflows/terminology.md (the registry — rows overturned and PROPOSED rows added in this commit), 2026-09-22_ch5_two_phase_restructure.md (headings), 2026-09-22_ch4_overview_figure_family.md (the figure that defines whatever names survive)
---

# Remove every term that does no work — starting with the three the supervisor named — and rename the model to what its chapter already calls it

## State of play

**The ruling (E2).** No invented terms; every name on a needs basis. "Movement attacker" goes — the model "already got a name, APT attacker"; the *movement / controller / action layer* trichotomy is not a set of layers ("layer is like OSI layers") but a process, part of the pipeline, and may not need names at all; *suppression* is not a term in the field (the metrics handoff decides what replaces the quantity — this file only removes the word). *Baseline attacker* and *MTDSim* stay. The cost is stated in marks: each unexplained term lowers the top of the range.

**The census** (`docs/thesis/dissertation.tex`, 2026-09-22, comments included — reproduce with `grep -oi "<term>" docs/thesis/dissertation.tex | wc -l`; the prose-only count is the sweep's first job):

| Term | Count | Sites that are not prose |
|---|---|---|
| movement attacker | 58 | headings: §6.1 l.7058 *What the movement attacker has captured*; App. B l.7432 *Supplementary material for the movement attacker*; Table 7.1 caption l.7211; the shared chapter 5 key label in `tools/_ch5_style.py` (fixed to "movement attacker" on 2026-09-22, commit `2fbcda08`) — so every chapter 5 float regenerates; `FLOATS.md`; the ch4 preamble's naming sentence ("which we are terming the movement attacker") |
| movement layer | 7 | ch4 §4.4 opener l.~4537 ("Everything from L0 to L3 is what we are considering the movement layer") |
| controller layer | 6 | ch4 §4.4 opener; the retired heading "The controller layer" survives in comments |
| action layer | 14 | ch4 §4.4 opener; §4.4.3 |
| suppression | 23 | Table 5.2 row; Figure 5.3/5.4/5.5 captions; Tables 5.4–5.6 headers (all generated) |
| substrate | 18 | expected to be comments only (repo word; thesis says *the simulator*) — verify |
| L0 … L4 | 12 / 20 / 15 / 22 / 23 | section headings §4.1–§4.4 carry them as prefixes (Marc's ruled signage) |
| APT attacker | 36 | ch3's Alshamrani class term (ratified 2026-09-02) — the collision to manage, §2 |
| APT attacker model | 7 | ch4 title and opener |

**Why the registry cannot simply be applied.** Two RATIFIED rows are overturned by the supervisor's ruling (the model's name, V5; the layer trichotomy, architecture §(f)), and the registry's own rule is that a session proposes and Marc rules — so this commit *banners* those rows and adds PROPOSED rows; nothing is substituted until the ruling pass.

## Recommended approach

### 1. Census first, prose only

Strip comments (`sed '/^\s*%/d'`) and re-count each term; list every heading, caption and generated-float site separately, because those are edited through generators and `FLOATS.md`, not by hand. Add to the list every noun phrase used three or more times in the ch4–ch5 body that is neither a chapter 2–3 term nor a field term (candidates from the results context's vocabulary table: *arm*, *token* and *place* outside §4.3, *instrument*, *observation*, *the join*).

### 2. The replacement table — Marc rules once

| Cluster | Today | Proposed canonical | Collision / note |
|---|---|---|---|
| the model | movement attacker | **APT attacker model** — the ch4 title, long form everywhere including float keys and table row groups ("APT attacker model" beside "baseline attacker") | *APT attacker* alone is Alshamrani's class term for the real-world party (ch3, ratified 2026-09-02); in ch4–ch5 no real APT is discussed, so context would disambiguate, but the registry's distinct-objects rule says do not merge — keep *model* on. The ch4 opener's naming sentence is **deleted**, no naming sentence replaces it (E2: a name that does no work is a step of confusion) |
| the trichotomy | movement layer / controller layer / action layer | **dissolve into the nouns the chapter already has**: *the profile net* (what L0–L3 produce, $\mathcal{N}_c$), *the join* (L4's three declared inputs — §4.4's own sentence "the three inputs we had to declare to join the attack profiles to MTDSim": dwell times, tactic-to-verb mapping, failure matrix), and *the simulator's verbs* / *the attacker's actions* (the six inherited operations, ratified *verb*) | (b) *phases of the pipeline* — Jin's word if names are wanted, but *phase* is ratified for the baseline attacker's six and *stage* for the four lifecycle bands, so a third sense is a collision on the page; (c) keep the three as named parts under new class noun *component*. Recommendation (a): no names; the overview figure (figure handoff) boxes L0–L3 / L4 / MTDSim, which is the definition Jin asked for |
| the pipeline's parts | "layer" as class noun for L0–L4 ("layer-by-layer", "L0 to L3 … the movement layer") | keep **L0–L4 as bare labels** (Marc's signage; Jin: "part of your pipeline"); each already has its noun (L1 the attack graph, L2 the attack profiles, L3 the profile net, L4 the join) — use the noun, never a class noun | *step* is Figure 5.1's unit (a tactic entered); *stage*, *phase*, *level*, *tier* are all taken |
| the metric name | suppression | the word goes with the metric (metrics handoff): report the field's before-and-after pair, or the relative reduction described in words ("the reduction in hosts reached relative to no defence") | Table 5.2's definition cell, the generated captions and headers, `tools/_ch5_style.py`, `data/results/ch5_defended/analyse.py` field names (repo side — may keep `suppression` as a key; only the surface changes) |
| genre identification row | "the identification is stated once, in the ch4 preamble opener" | **retire the row**: with the model named by its genre there is nothing to identify | — |
| the L4 heading | "L4: Joining the profile net to MTDSim" | stands — it already uses the dissolved vocabulary | — |

### 3. Apply

1. Registry: flip the rows with the date, name what is overturned (rule-on-merit), move *movement attacker* and the three *layer* names to the deprecated column.
2. Tex, by section, comments excluded: the ch4 preamble and §4.4 opener first (they define the words), then ch5, ch6, appendices, the notation table, the three headings.
3. Generators: `tools/_ch5_style.py` label map; `tools/ch5_*_figures.py` and `tools/ch5_disruption_figure.py` caption strings; regenerate every ch5 float; `FLOATS.md`.
4. `docs/notes/` is *not* swept (staging prose, superseded on absorption); a one-line note in `docs/notes/README.md` or the writing guide that the surface term changed on 2026-09-22 is enough. Repo vocabulary (`movement/` package, `movement_attacker`, `controller.py`) is **never** renamed (registry scope rule; architecture.md §(b) states the mapping once).
5. Re-census: the deprecated strings at zero in the prose, headings, captions and generated floats.

## Rulings owed (Marc)

The §2 table, one pass. Also: whether *APT attacker model* is acceptable as a repeated long form in tables (it is three words against two), or whether Marc prefers a short form after first use in each float — the recommendation is the long form, so no reader meets a second name.

## Validation gate

`grep -oi` for *movement attacker*, *movement layer*, *controller layer*, *action layer* and *suppression* over the comment-stripped tex, the captions and `docs/thesis/tables/*.tex` and `figures/*.tex` returns 0; the ch4 preamble opener has no naming sentence; the three headings are re-titled; build clean; registry rows flipped with dates and the overturned rulings named; `FLOATS.md` current.

## Hard constraints

- No auto-substitution before the ruling; sessions flag and propose (registry rule).
- Distinct objects are never merged: the token is not the attacker; the profile is not the net; the real APT attacker (ch3) is not the model.
- Repo/docs vocabulary stays; only the dissertation surface changes.
- Every regenerated float is regenerated, never hand-edited.

## Reading list

- `docs/workflows/terminology.md` — the registry, with today's banners.
- `docs/thesis/dissertation.tex` l.3694–3760 (ch4 preamble), l.4525–4575 (§4.4 opener).
- `tools/_ch5_style.py` — the label map every ch5 float keys through.
- `docs/implementation/architecture.md` §(b), §(f) — the repo↔thesis vocabulary mapping and the trichotomy's origin.
- `docs/implementation/research_record/threads/three_layer_seam.md` — how the trichotomy was coined (2026-07-16), so its dissolution is recorded against its origin.

## Out of scope

What replaces the suppression *quantity* (metrics handoff); the headings of ch5 (restructure handoff); the figure that boxes the parts (figure handoff).
