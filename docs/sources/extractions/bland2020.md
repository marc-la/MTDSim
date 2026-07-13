# Bland 2020 — extraction notes

> J. A. Bland, M. D. Petty, T. S. Whitaker, K. P. Maxwell, W. A. Cantrell. "Machine Learning Cyberattack and Defense Strategies." *Computers & Security*, vol. 92, art. 101738, 2020.
> Source file: `docs/sources/4_bland2020machine.md` (gitignored).
> Relevance to this thesis: cross-cutting reference for §V — a relatively early example of *attacker-side* ML, the kind of asymmetry-reversing modelling that Cho et al.'s critique calls for and that MTD evaluation seldom adopts.

## Bibliographic anchor

- **Citation key**: `bland2020`
- **DOI / URL**: 10.1016/j.cose.2020.101738
- **Pages cited from**: full text

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### Relevance class

**S — Supporting-argument.** Bland is cited in §V (Research Gap and Approach), [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) lines 217 and 223, as the agent-side exemplar that demonstrates *"the sequencing, adaptive adversary the surveyed evaluations omit is constructible"* — anchoring the §V claim that the apparatus to close the attacker-modelling gap already exists. The §V approach prescribes *"a Bland-style agent"* (line 223) on a different substrate (MTDSim, not PNPSC). Bland supplies the agent-construction template, not the substrate; the citation does not place Bland on Table II in §IV-B. Anchored on the architecture side at [`../specs/architecture.md`](../specs/architecture.md) §(f) (L3 — OGASP graph-driven attacker, currently unbuilt).

---

### RL attacker as partial-observation, cost-incurring, learning agent

**Source locator:** §1 (Introduction, research questions); §2.2 (Reinforcement learning); §5 (Machine Learning in Cyberattack Models). Markdown source has no page numbers — locators are by section.

**Paraphrase:** Bland et al. formalise the attacker as a reinforcement-learning agent whose *state* is the marking of the player's observable subset of places and the rates of its controlled transitions; whose *action* is to change the firing rates of its controlled transitions (set to 0 or 10 in the experiments, i.e., deactivate or activate); and whose *reward* combines a success signal (100 when a success place is marked, 0 otherwise) with a scaled penalty proportional to the magnitude of the rate change, capturing the *C₂* cost component of the PNPSC formalism. Strategy learning uses an ε-Greedy policy over running-average rewards per (observable marking, rate-set) pair across up to 500,000 episodes (most learning happens in the first 100,000). The experimental design includes three conditions — dynamic attacker vs static defender, static attacker vs dynamic defender, and dynamic-vs-dynamic — and the paper reports improvement under all three, with average rewards shifting symmetrically when both players learn (§6).

**Quote (essential):**
> "An action is a player's change to the player's controlled transitions, as guided by its strategy. The reward is a function of whether the attacker's goals were achieved and the cost to the players' actions." (§2.2)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(f) (L3 OGASP graph-driven attacker — partial-observation, cost-incurring, learning agent is the template the §V approach prescribes); [`../specs/architecture.md`](../specs/architecture.md) §(f) Decision-block on Jalowski primitives (Bland's per-marking rate-set memory is a near-relative of primitive (1) state-collision recognition, though Bland's memory is across episodes of a fixed Petri net rather than across post-shuffle target states).

**Disposition for this thesis:** *adopted-as-baseline* for the agent-construction template (per §V line 223 — "a Bland-style agent enacts it"). On the §IV-B fidelity descriptor the attacker sits at **procedural** rather than behavioural: rule-based action selection at runtime against an observable marking, learned over episodes, but without campaign-level intent, motivation conditioning, or cross-target memory. The §V usage is the rhetorical-role anchor — proof that a sequencing, adaptive agent over expert-validated attack patterns is constructible — not a substrate borrowing. (Resolves stub open question on fidelity-rung placement.)

---

### CAPEC-validated attack patterns as the agent's environment — substrate distance from MTDSim

**Source locator:** §1 (motivating paragraphs on CAPEC); §4 (Petri Net Models of Cyberattacks); §6 (Results discussion of player-controlled transitions).

**Paraphrase:** The agent runs over PNPSC (Petri net with players, strategies, and costs) models of two CAPEC patterns — cross-site scripting (CAPEC-66) and spear phishing (CAPEC-163) — validated by a panel of cybersecurity subject-matter experts in a structured face-validation process. The PNPSC structure encodes the four CAPEC phases (Explore, Experiment, Exploit, Goal) explicitly as place subgraphs, with player-controlled transitions partitioned between attacker and defender (e.g., cross-site scripting attacker controls 16 transitions, defender controls 13, of which only one represents active blocking). The transition firing rates used in the experiments are stated to be notional, randomly drawn from [1, 10], with realistic-rate identification flagged as future work (§2.1).

**Quote (essential):**
> "The rates used in this work were notional and randomly selected between one and ten. Identifying realistic rates is a future effort to enhance this research." (§2.1)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(i) (substrate seam map — Bland's PNPSC is an alternative analytical substrate); [`../specs/architecture.md`](../specs/architecture.md) §(f) Decision-block "Petri-net (SNAKES) formalisation is positioned as a candidate alternative analytical substrate, not as a step inside L1/L2".

**Disposition for this thesis:** *contrasted-against* on the substrate axis. The §V approach takes the *agent template* from Bland (partial-observation, cost-incurring, learning) but operationalises it on MTDSim's discrete-event substrate with attack-graph traversal rather than on a per-CAPEC-pattern Petri net (see [[brown2023]] for the MTDSim substrate and [[tay2024]] for the existing RL-on-MTDSim precedent). Two consequences for this thesis: (a) Bland's two-pattern, hand-built PNPSC scope — explicitly flagged as a coverage limitation in lit-review §V — motivates the move to a graph-traversal agent whose behavioural content comes from curated CTI rather than from per-CAPEC Petri-net authoring; (b) Bland's notional-rate caveat is the same parameter-calibration gap the §V approach addresses by parameterising the agent against engagement data after [[outkin2023]], not on Petri-net inter-firing times.

---

### Used in lit review

- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) **line 217** (§V Research Gap and Approach): *"Bland et al. [20] build an attacker that observes partial state, acts at a cost, and learns its strategy against a dynamic defender. Their attacker runs over expert-validated Common Attack Pattern Enumeration and Classification (CAPEC) patterns — evidence that the sequencing, adaptive adversary the surveyed evaluations omit is constructible, if so far only on narrow, hand-built cases."* Anchors the §V claim that a sequencing/adaptive attacker is constructible — the *agent-side* half of the apparatus the thesis assembles.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) **line 223** (§V-A Approach): *"a Bland-style agent enacts it, parameterised against engagement data after Outkin et al."* Anchors the prescription — the agent template this thesis adopts, paired with [[outkin2023]] for parameter grounding and curated CTI ([[attackflow]]) for behavioural content.

Bland is *not* cited in §IV-B and is not placed on Table II. (Resolves stub open question on §V placement.)

---

## Open questions / things to verify

- Bland's per-marking memory of rate-sets across episodes is reset between independent runs of the simulator; whether the §V "Bland-style agent" inherits per-marking-memory across attack-graph traversal episodes, or carries memory across runs against a shuffling MTD substrate, is an architectural question for [`../specs/architecture.md`](../specs/architecture.md) §(f) primitive (1) (state-collision recognition). Not a Bland question — flagged so it does not get smuggled in unspoken.
- Bland's reward is end-of-episode only (success-place marking), with intermediate states updated from the final reward (§8). Whether the L3 graph-driven attacker uses end-of-episode reward against an attack-graph terminal, dense per-technique reward, or something else, is architecturally open and not constrained by what Bland did.

## Out of scope for this thesis

- The defender-side ML details, unless they illuminate the attacker's learning regime.
