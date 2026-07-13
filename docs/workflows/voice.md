---
status: durable
created: 2026-07-13
updated: 2026-07-13
provenance: codified from the ratified prose corpus — docs/notes/ (rubric-cleared notes) and dissertation.tex §3.2 — not from prompts; maintained from Marc's edits per §(g)
---

# Voice — the prose contract for dissertation-bound writing

**Status:** durable. Load in full before drafting or editing any prose destined for the dissertation, whether it is staged (`docs/notes/`) or final (`docs/thesis/`).

## (a) Force — where this applies, and how hard

| Target | Force |
|---|---|
| [`../thesis/`](../thesis/) | **Hard rubric.** Every section passes the §(f) gate before it is committed. A section that fails the gate is not committed — fix it or don't write it. |
| [`../notes/`](../notes/) | **Default voice.** [`notes_rubric.md`](notes_rubric.md) governs structure, placement, and register; this file governs the sentences. Write in this voice by default; deviate only where a specific note's job demands it, and knowingly. |
| `implementation/`, `handoffs/`, `workflows/` | Out of scope — those registers are set in [`docs_map.md`](docs_map.md). |

Division of labour: [`docs_map.md`](docs_map.md) decides where a document lives; [`notes_rubric.md`](notes_rubric.md) decides what a note is and who reads it; [`../notes/_writing_guide.md`](../notes/_writing_guide.md) decides what each dissertation part does and in what order to draft; **this file decides how the prose itself sounds** — the layer beneath all three.

## (b) What this voice is, honestly

No corpus of Marc's unaided academic prose exists. What exists is more useful than either unaided samples or prompt history: a **ratified corpus** — prose drafted in collaboration with AI and then kept, corrected, or rewritten by Marc across months of review, under a supervisor-facing register. This file codifies the fixed point of that write⇄edit loop. It is the house voice of the collaboration, not a reconstruction of what Marc would write alone — and it converges on Marc over time through §(g), because his edits to drafted prose are the evidence this file is maintained from. Voice is not prompting style: no rule here derives from how prompts are phrased; every rule traces to a passage that survived review.

## (c) How paragraphs argue

1. **Claim first, unpack after.** The first sentence of a paragraph states what the paragraph establishes; everything after is support. Titles and headings are claims or questions in plain English, not topic labels.
2. **Enumerate, then walk.** Announce the count, then take the items in order: *"Four boundaries fix what the model does not attempt. First, … Second, …"* Never announce three and deliver two; never bullet what should be walked.
3. **Alternatives are ranked and dismissed with reasons.** When a choice is defended, name the live options on an explicit axis (*"Three bindings are possible, from cheapest to most faithful"*), give each its genuine strength, and justify the selection from both directions — why not the cheaper, why not the dearer.
4. **Mechanism, not assertion.** A claim earns its place by carrying its *why*. If the cause can't be named, the claim is flagged as open, not asserted with a hedge.
5. **Concessions are made up front and owned.** Weaknesses are disclosed as design facts, in the same breath as the strength they trade against: *"The strength (real, analyst-drawn technique dependencies) and the limitation (aggregation over-generates) are the same fact."* — *"This is accepted and disclosed rather than corrected."* Never let an examiner discover a limitation the text could have named.
6. **Negative scope is explicit.** Say what the argument does *not* claim, as a section or a closing move, before someone else says it.
7. **The modest-claim ceiling.** Claims stop at what the evidence carries: *designed* is not *demonstrated*; the standing formula is *"not that the model is true, but that fidelity at this level changes the answers an evaluation returns."* No claim outranks its experiment.

## (d) How sentences sound

- **Paired opposition is the signature move.** Antithesis across a semicolon (*"Capability and credential state survives a network mutation; network-position state is invalidated by it."*) and the X-not-Y compression (*"envelope, not actor"*, *"defended, not demonstrated"*, *"explicitly deferred, not quietly dropped"*). Use it where the contrast is load-bearing; it dulls with overuse.
- **Em-dashes carry argument, not decoration.** An interpolation earns its dashes by adding a turn (*"But — and this is the hinge of the argument — automation changes MTD's responsiveness, not its phase reach."*). If the aside could be deleted without loss, delete it.
- **Long sentences are allowed when controlled; verdict sentences are short.** After a long build, land on a short one. Vary shape — three consecutive sentences with the same skeleton is a redraft signal.
- **Present tense, active by default.** Passive only where the agent is genuinely irrelevant. Cited work acts as a subject: *"\citet{ling2023} derive time-to-compromise estimates…"*.
- **Controlled vividness, rationed.** One pointed, plain-English formulation per section, doing real argumentative work (*"A field that automates incomplete coverage is faster at the same thing."* — *"MTD reads well on paper and deploys rarely."*). Never two in a row; never as ornament.
- **Emphasis is semantic and sparse.** Italics introduce a term at first fix; bold marks a load-bearing claim or fixed term (markdown) — in LaTeX, `\emph` only. Emphasis that merely raises volume is removed.
- **Australian English throughout** (-ise, -our, *defence*), per the [guardrails](guardrails.md).

## (e) Terminology and evidence

- **Define before use, then hold.** Fix boundary terms explicitly (*"post-ingress = ATT&CK Initial Access and every tactic after it"*) and use them consistently thereafter. One taxonomy per document region; if two vocabularies must meet, map them once and pick one to continue in.
- **No synonym rotation.** The same technical thing gets the same word every time. Elegant variation is for objects, not concepts.
- **Internal codenames**: defined-or-absent in notes (per the rubric); **absent, full stop, in `thesis/`** — the dissertation never says GAP, GASP, OGASP, L0–L4, "the substrate", or any repo-internal name.
- **Cited or flagged, never silently asserted.** In notes, an unsourced empirical claim carries an in-text *citation anchor to reconcile*. In `thesis/`, anchors are not permitted: a claim is cited (`\citep`/`\citet`) or the sentence does not commit to it. Never assert a paper wrong; never attribute a source unread.
- **Epistemic status is explicit**: demonstrated vs designed vs conjectured, stated where the reader needs it, not in a distant caveat.

## (f) The hard gate for `thesis/` — run per section, before committing LaTeX

1. **Claim-first check.** Does each paragraph's opening sentence state what the paragraph establishes?
2. **Enumeration check.** Every announced count walked to completion; every "First" has its "Second".
3. **Citation check.** Every empirical claim carries `\citep`/`\citet`; zero unresolved anchors, zero "to reconcile" residue.
4. **Terminology check.** Every term defined at or before first use; no internal codenames; no synonym drift; one taxonomy in play.
5. **Tell check.** None of the §(h) banned patterns present.
6. **Ceiling check.** No claim exceeds its evidence; designed/demonstrated boundary honest; negative scope stated.
7. **Rhythm check.** Read aloud (or simulate it): sentence shapes vary; each em-dash interpolation earns its place; at most one vivid formulation per section.
8. **Calibration check.** Set the section beside a §(i) passage — same person on the page?

A section failing any check is redrafted before commit. For `notes/`, run the same list as a diagnostic, not a gate — checks 3 and the codename half of 4 relax per the notes rubric; the rest is the default.

## (g) Maintenance — how this file converges on Marc

- **Marc's edits are the data.** When Marc rewrites, cuts, or re-words drafted prose, the diff is voice evidence. A recurring correction becomes a rule here; a rule his edits repeatedly contradict is removed.
- **Every rule must trace to a ratified passage.** No rule enters from taste, a style guide, or model priors alone. If a rule can't be pointed at surviving prose, it doesn't belong.
- Bump `updated` on material change; keep the file lean — this is a contract, not an essay on style.

## (h) Banned tells — the machine leaks to remove on sight

| Banned | Write instead |
|---|---|
| Hype adjectives on own work: *novel, comprehensive, significant(ly), robust, powerful, crucial(ly)* | Name the specific technical move and let it carry the weight: *"an advance in MTD evaluation methodology that requires touching neither the defences nor the network model"* |
| *It is important to note that…*, *It should be emphasised…* | Delete the frame; if it matters, the claim-first sentence already shows it |
| *delve*, *landscape* (as in "threat landscape" filler), *in today's world*, *rapidly evolving* | Concrete nouns and dated facts |
| *Moreover / Furthermore / Additionally* chains | Connect by logic — cause, contrast, consequence — or start the new claim plainly |
| Rule-of-three adjective triads (*fast, scalable, and efficient*) | One precise adjective, or the mechanism that makes it so |
| Bold-term-colon listicles as argument (*"**Flexibility:** the system…"*) | Prose that argues; enumerate-then-walk if it's genuinely a list |
| Hedging stacks (*may potentially suggest*) | One calibrated hedge, then commit — or flag the claim as open |
| Empty signposting (*"In this section, we will discuss…"*) | Functional signposting that says what each part *does*: *"Section X derives both properties; Section Y draws out the pattern they form."* |
| Rhetorical questions as transitions | A question only when it is a real, attributed question the text then answers |
| Symmetric paragraph openers across a section | Vary the entry point: claim, contrast, consequence, concession |

## (i) Calibration passages

Before drafting, re-read one of these; they are the voice at full strength:

- [`../notes/ch2_background/post_ingress_mtd_gap.md`](../notes/ch2_background/post_ingress_mtd_gap.md) — §"Why the two observations are one claim" (the mechanism move, antithesis, controlled vividness).
- [`../notes/ch3_design/structure_to_behaviour_binding.md`](../notes/ch3_design/structure_to_behaviour_binding.md) — §"The binding, done properly" (ranked alternatives, both-directions justification).
- [`../thesis/dissertation.tex`](../thesis/dissertation.tex) §"Profile Construction and Scope" (boundaries walked, modest-claim ceiling, disclosure-as-strength — the voice in LaTeX register).
