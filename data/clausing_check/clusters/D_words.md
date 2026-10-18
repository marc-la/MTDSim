## D. Words: figurative wording, term overload, needless definitions, unneeded content

**Rule.** Technical prose avoids metaphor and idiom (Zobel pp. 77, 115) and describes a concept "always … in the same way … not by a series of synonyms" (Zobel p. 117; ISO 704 §7.2). A term defined but barely used, and content the reader does not need, are cut (Zobel pp. 120, 174, 177, 196).

**The cluster-wide move.**
- (a) Swap a word only where a defined or registered term exists, at Δ ≤ 0. Pro: seamless, and each swap is checkable against terminology.md. Con: leaves plain idioms ("behind", "sit") in place.
- (b) Purge every flagged cue word. Pro: uniform. Con: most cues are literal ("answers the research question"), so it churns ratified prose for nothing.
- (c) Keep all. Pro: no risk. Con: leaves real term collisions (*stage*, *method*, *outcome*, *procedure*) that the registry already rules out.
- **Recommended:** (a). It fixes only what the registry or a defined term licenses, and the flags proved mostly false positives.

**Kept as warranted (44).**
- `L667` — "answers the research question" is literal.
- `L721` — SDR triad of parallel definitions. *Shuffle* is used throughout.
- `L729` — owned by calibration item 6. Table 2.2 reuses all three terms.
- `L797` — plain verb. The registry row itself says "sit in".
- `L799` — "deeper" is literal, given *levels of depth*.
- `L803` — *target host* is used about 10 times (the census undercounted).
- `L805` — *internal host* is used six times in Table 2.1.
- `L1235` — owned by calibration item 14 (delete).
- `L1236` — emphasis marks the name's words, kept after item 14.
- `L3961` — sections answer sub-questions: literal.
- `L3964` — literal, as for L3961.
- `L3965` — literal, as for L3961.
- `L4095` — plain idiom. No defined term replaces it.
- `L4211` — yes-or-no answers to the two questions: literal.
- `L4241` — "the answers" to those questions: literal.
- `L4281` — the evidence for "differ in actions on objectives".
- `L4418` — forward-referenced at L4108. Used three more times.
- `L4575` — "carry out" is literal. The next sentence echoes it.
- `L4926` — the reason one tactic is unmapped. The reader asks why.
- `L4927` — the reason, as for L4926.
- `L4928` — the reason, as for L4926.
- `L5123` — "behind" means "the source of". Plain idiom.
- `L5124` — motivates the failure matrix.
- `L5190` — "tell apart" is plain. No term exists.
- `L5357` — motivates the attacker behaviour metrics.
- `L5762` — literal.
- `L7623` — explains the low count of attack actions blocked.
- `L7628` — the result itself.
- `L8534` — *diversity pool* is a defined term (§4.4.4).
- `L8569` — literal.
- `L8579` — literal.
- `L8585` — literal.
- `L8633` — the attribution sentence. It carries the ablation result.
- `L8775` — literal.
- `L8957` — literal.
- `L9160` — the scope statement. It carries the design bounds.
- `L9293` — the threat's own content.
- `L9870` — a contribution answers a sub-question. Standard.
- `L9926` — `\emph` run-in item label. Not a definition.
- `L9939` — run-in item label, as for L9926.
- `L9961` — run-in item label, as for L9926.
- `L10100` — plain idiom. "Predicates behind each mark" is clear.
- `L10179` — plain idiom, as for L10100.
- `L10405` — disclosure ruled "that's fine" (2026-10-15).

**Proposals (8).**

### D.1 · L941 · Baseline attacker · K6
> It follows a fixed procedure of six *attack actions*, modelled on the Cyber Kill Chain [brown2023, hutchins2011]: it scans for hosts, …

**After:** It follows a fixed sequence of six *attack actions*, modelled on the Cyber Kill Chain [brown2023, hutchins2011]: it scans for hosts, …
Δ 0 · *Procedure* is ATT&CK's defined term ("one recorded instance of a technique", §3.1.2), and the registry lists it as a watched variant. Here it means only a fixed order.
**Mark:** ok / alt / keep / look —

### D.2 · L2183 · MTD modelling approaches · K6
> An MTD modelling approach is a method for finding an optimal deployment strategy.

**After:** An MTD modelling approach finds an optimal deployment strategy.
Δ −4 · The registry rules that an approach is not a *method*, which is reserved for §3.2.3's *evaluation method*. Alt: "searches for" (Δ −3) if "finds" claims too much.
**Mark:** ok / alt / keep / look —

### D.3 · L3469, L3474, L3485 · Recent MTD attacker models · K6
> Their attacker model is an automated attack script that runs four stages in a fixed order: …
> … each attack runs all four stages, but in one short attempt, …
> … every attack follows one attack scenario, in the same four stages.

**After:** *stages* → *steps* at all three sites ("runs four steps in a fixed order", "runs all four steps", "in the same four steps").
Δ 0 · *The four stages* is the registered name for §3.1.1's lifecycle (preparation to actions on objectives), and Figure 4.2 groups the tactics by it. Kim's four script steps are a different object.
**Mark:** ok / alt / keep / look —

### D.4 · L4036 · Attack graph from attack flows · K4
> Each technique in an attack flow stands for its tactic, and a technique listed under several tactics stands for the leftmost of them in the ATT&CK matrix.

**After:** Each technique in an attack flow counts as its tactic, and a technique listed under several tactics counts as the leftmost of them in the ATT&CK matrix.
Δ 0 · "Stands for" is figurative, the same instance as calibration item 14. The aggregation literally counts each technique as its tactic.
**Mark:** ok / alt / keep / look —

### D.5 · L4360 · Petri-net formalism · K6
> A timed transition models the time the attacker spends on a tactic, and an immediate transition models its choice of the next tactic.

**After:** A timed transition models the tactic duration, and an immediate transition models the attacker's choice of the next tactic.
Δ −5 · Chapter 4 phrases one concept three ways: time spent "within" (L4042), "on" (here) and "in" (L4394) a tactic. *Tactic duration* is the registered term, already used at L4042.
**Mark:** ok / alt / keep / look —

### D.6 · L4365 · Petri-net formalism · K4
> Tokens sit on places.

**After:** Places hold tokens.
Δ −1 · The next sentence says "each of its input places holds a token". One verb now serves both sentences.
**Mark:** ok / alt / keep / look —

### D.7 · L4394 · merged into C.28

### D.8 · L4436 · Petri-net formalism · K6
> Each attack action the APT attacker model runs in MTDSim succeeds or fails; this outcome is the attack action's *verdict* (Section 4.4).

**After:** The *verdict* of each attack action the APT attacker model runs in MTDSim is success or failure (Section 4.4).
Δ −3 · *Outcome* collides with *attack outcome*, §4.5.2's metric group. The term now opens its own copula definition, and the semicolon goes.
**Mark:** ok / alt / keep / look —
