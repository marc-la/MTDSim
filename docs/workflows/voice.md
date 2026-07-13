---
status: durable
created: 2026-07-13
updated: 2026-07-13
provenance: codified from the ratified prose corpus (dissertation-bound prose Marc kept or reworked under review), Marc's typed prompt history (argumentation layer only), and unit assessor feedback; maintained per §(g)
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

No corpus of Marc's unaided academic prose exists. Two evidence streams substitute for it, each admissible at a different layer:

1. **The ratified corpus** — prose drafted in collaboration with AI and then kept, corrected, or rewritten by Marc under review, at a supervisor-facing register. This is the only evidence for sentence-level rules (§d): how the prose sounds is defined by what survived his edits.
2. **Marc's typed prompt history** — his genuinely unaided writing. It is a different genre from academic prose, so it grounds nothing at the sentence level, but it is direct evidence of the **argumentation layer** (§c): how he decomposes problems, what he demands of an argument, what he rejects.

This file codifies the fixed point of the write⇄edit loop. It is the house voice of the collaboration, not a reconstruction of what Marc would write alone — and it converges on Marc over time through §(g), because his edits are the evidence it is maintained from. This file is **first-principles by design**: it states how prose argues and sounds, and binds to no thesis content, framing, or terminology — those may pivot; the voice should not have to.

The failure mode this file exists against has been named by an assessor of the preceding unit work: AI-assisted academic writing flattens until *the author's natural voice doesn't come through* — plain register is expected, but anonymity is a defect that costs marks. The test of every rule here is therefore not "is the prose correct?" but "is it recognisably one person's?" A paragraph that any model could have produced for any thesis fails this file even when it is accurate, cited, and clear.

## (c) How paragraphs argue

1. **Claim first, unpack after.** The first sentence of a paragraph states what the paragraph establishes; everything after is support. (Headings are the deliberate exception — see §d.)
2. **Enumerate, then walk.** Announce the count, then take the items in order: *"Three constraints fix the design. First, … Second, … Third, …"* Never announce three and deliver two; never bullet what should be walked.
3. **Alternatives are ranked and dismissed with reasons.** When a choice is defended, name the live options on an explicit axis (*cheapest to most faithful; coarsest to finest*), give each its genuine strength, and justify the selection from both directions — why not the cheaper, why not the dearer.
4. **Mechanism, not assertion — and every inferential step walked.** A claim earns its place by carrying its *why*; if the cause can't be named, the claim is flagged as open, not asserted with a hedge. When the text moves from a definition to a chosen number, shape, or classification, the route between them is on the page — a leap the reader must reconstruct is a defect, however obvious it felt to write.
5. **Concessions are made up front and owned.** Weaknesses are disclosed as design facts, in the same breath as the strength they trade against — the strongest form notes when *the strength and the limitation are the same fact*, and the standing register is *accepted and disclosed rather than corrected*. Never let an examiner discover a limitation the text could have named.
6. **Negative scope is explicit.** Say what the argument does *not* claim, as a section or a closing move, before someone else says it.
7. **The modest-claim ceiling.** Claims stop at what the evidence carries: *designed* is not *demonstrated* is not *true* — say which one the text has earned. No claim outranks its experiment.
8. **Ground the abstract in the concrete.** An abstract claim earns its keep with an instance: a worked example, a named case, a number, or a figure. A concept that takes more than a paragraph to state abstractly wants an example or an image instead — these are argument, not decoration, and their absence is an assessor-named defect, not a stylistic preference. A figure earns its place the same way a sentence does: it must carry part of the argument, and its caption must stand alone.
9. **Criteria before the thing judged.** State what would count as success — the bar, the validation criteria, the rubric — before presenting what is measured against it. A result that arrives before its yardstick reads as advocacy; a design presented before its requirements reads as improvisation.
10. **Name the circularity risk.** Where a modelled quantity or a result could have been shaped by expectation — tuned until it looked right, fitted to sparse data, chosen to confirm the motivation — say so, and show what independent grounding breaks the loop. Unacknowledged circularity is the first thing an examiner reaches for.

## (d) How sentences sound

- **Paired opposition is the signature move.** Antithesis across a semicolon — *what X changes is A; what X cannot touch is B* — and the X-not-Y compression (*a bound, not an estimate*; *defended, not demonstrated*). The authored substrate is the loose form — *rather than*, *not …, more along the lines of …* — with the tight comma form and the semicolon antithesis as its formal-register compressions; all are licensed. Use it where the contrast is load-bearing; it dulls with overuse.
- **Interpolations carry argument, not decoration — and the authored device is the parenthesis.** Marc's hand tags its own claims inline with a parenthesised status, scope, or gloss (*"(less important at this stage)"*, *"(my feedback is non exhaustive)"*); the em-dash turn (*"But — and this is the hinge — …"*) is the ratified-register alternative and the rarer of the two. Either way, an aside that could be deleted without loss is deleted.
- **Long sentences are allowed when controlled; verdict sentences are short.** After a long build, land on a short one. The authored instinct is the clipped fragment (*"These are design choices."*) — in formal register, polish it into a short full sentence; do not sand it away. Vary shape — three consecutive sentences with the same skeleton is a redraft signal.
- **Two-beat anaphora is a native device.** The same opener twice for parallel claims (*"…, yet to be seen. …, yet to be seen."*): deliberate, in pairs, never runs of three — distinct from the accidental symmetric openers banned in §h.
- **Present tense, active by default.** Passive only where the agent is genuinely irrelevant. Cited work acts as a subject: *"\citet{author2020} derive…"*, not *"estimates were derived in \citep{author2020}"*.
- **Controlled vividness, rationed.** One pointed, plain-English sentence per section that *compresses* the argument rather than decorates it — the sentence a reader would quote back. Never two in a row; never as ornament.
- **Emphasis is semantic and sparse.** Italics introduce a term at first fix; bold marks a load-bearing claim or fixed term (markdown) — in LaTeX, `\emph` only. Emphasis that merely raises volume is removed.
- **Headings state what the section is on — nothing more.** The arguing is done by prose; a heading that performs (a claim, a flourish, a mini-thesis) is over-dressed for the register. Marc's ruling, verbatim: headings that *"try to do more than just state what the section is on"* are not academically aligned. (His native working-structure poses a section as the question it answers — that interrogative form stays licensed where the rubric licenses it, note titles above all; in thesis headings it is out of register by the same ruling.)
- **The working vocabulary is allowed through.** Marc's own evaluation lexicon — *defensible* (attested in his prompts *and* his authored prose), *grounded*, *tradeoff*, *distil* (prompt-attested) — is part of the voice; prefer these over synonyms when judging or positioning work. Sparingly: seasoning, not scaffolding.
- **Australian English throughout** (-ise, -our, *defence*), per the [guardrails](guardrails.md).

## (e) Terminology and evidence

- **Define before use, then hold.** Fix a boundary term explicitly at first use (*term = its exact extension*) and use it consistently thereafter. One taxonomy per document region; if two vocabularies must meet, map them once and pick one to continue in.
- **No synonym rotation.** The same technical thing gets the same word every time. Elegant variation is for objects, not concepts.
- **Internal codenames**: defined-or-absent in notes (per the rubric); **absent, full stop, in `thesis/`** — the dissertation never uses a repo-internal name, whatever the current crop is.
- **Cited or flagged, never silently asserted.** In notes, an unsourced empirical claim carries an in-text *citation anchor to reconcile*. In `thesis/`, anchors are not permitted: a claim is cited (`\citep`/`\citet`) or the sentence does not commit to it. Never assert a paper wrong; never attribute a source unread.
- **Epistemic status is explicit**: demonstrated vs designed vs conjectured, stated where the reader needs it, not in a distant caveat. Beliefs carry their source — assumed, reported, observed, verified — which formalises the authored habit (*"I am assuming, and my impression from prior meetings"*).

## (f) The hard gate for `thesis/` — run per section, before committing LaTeX

1. **Claim-first check.** Does each paragraph's opening sentence state what the paragraph establishes?
2. **Enumeration check.** Every announced count walked to completion; every "First" has its "Second".
3. **Citation check.** Every empirical claim carries `\citep`/`\citet`; zero unresolved anchors, zero "to reconcile" residue.
4. **Terminology check.** Every term defined at or before first use; no internal codenames; no synonym drift; one taxonomy in play.
5. **Tell check.** None of the §(h) banned patterns present.
6. **Ceiling check.** No claim exceeds its evidence; designed/demonstrated boundary honest; negative scope stated; circularity risks named, with the grounding that breaks them.
7. **Rhythm check.** Read aloud (or simulate it): sentence shapes vary; each em-dash interpolation earns its place; at most one vivid formulation per section.
8. **Concreteness check.** Every complex concept is grounded by an example, a number, or a figure; every figure carries part of the argument and its caption stands alone; headings state their section's topic and no more.
9. **Calibration check.** Set the section beside the most recently ratified prose (§i) — same person on the page?

A section failing any check is redrafted before commit. For `notes/`, run the same list as a diagnostic, not a gate — checks 3 and the codename half of 4 relax per the notes rubric; the rest is the default.

## (g) Maintenance — how this file converges on Marc

- **Marc's edits are the data.** When Marc rewrites, cuts, or re-words drafted prose, the diff is voice evidence. A recurring correction becomes a rule here; a rule his edits repeatedly contradict is removed.
- **Evidence is layered.** Sentence-level rules (§d) may only be grounded in ratified prose or Marc's explicit prose-style rulings. Argumentation rules (§c) may additionally be grounded in his typed prompt history — his unaided writing — because reasoning moves survive the genre change; sentence rhythm does not. Assessor and supervisor feedback is admissible at every layer and outranks both.
- **The genre firewall.** Prompt evidence admits reasoning moves only. Conversational artefacts of prompting — filler hedges, telegraphic fragments, informal cadence — are speech, not voice, and never become prose rules.
- **No rule enters from taste alone** — not from a style guide, not from model priors. If a rule can't be pointed at surviving prose or recurring prompt evidence, it doesn't belong.
- **Stay first-principles.** No rule may bind to thesis content, framings, or terminology; if an example drifts into project specifics, schematise it.
- **Evidence status (2026-07-13).** Argumentation rules: grounded in the prompt corpus, corroborated by authored working prose (strongest: concession-up-front, epistemic tagging, enumeration, concrete grounding). Sentence rules: ratified-corpus, except where authored evidence corrected the device — parenthesis over em-dash, the anaphora and hedge-layering carve-outs, the loose opposition forms. The authored corpus is small (~900 words of working register): enough to correct devices, not to ground cadence, so §d remains this file's most provisional layer. Evidence records live with the assistant memory, not the repo — Marc's verbatims are not committed.
- Bump `updated` on material change; keep the file lean — this is a contract, not an essay on style.

## (h) Banned tells — the machine leaks to remove on sight

| Banned | Write instead |
|---|---|
| Hype adjectives on own work: *novel, comprehensive, significant(ly), robust, powerful, crucial(ly)* | Name the specific technical move and what it does *not* require, and let that carry the weight |
| *It is important to note that…*, *It should be emphasised…* | Delete the frame; if it matters, the claim-first sentence already shows it |
| *delve*, *landscape* (as in "threat landscape" filler), *in today's world*, *rapidly evolving* | Concrete nouns and dated facts |
| *Moreover / Furthermore / Additionally* chains | Connect by logic — cause, contrast, consequence — or start the new claim plainly |
| Rule-of-three adjective triads (*fast, scalable, and efficient*) | One precise adjective, or the mechanism that makes it so |
| Bold-term-colon listicles as argument (*"**Flexibility:** the system…"*) | Prose that argues; enumerate-then-walk if it's genuinely a list |
| Decorative hedge-stacking (*may potentially suggest*) | One calibrated hedge, then commit — or flag the claim as open. (Epistemic layering — successive hedges each scoping a *different* part of the claim — is an authored habit and stays licensed.) |
| Empty signposting (*"In this section, we will discuss…"*) | Functional signposting that says what each part *does*: *"Section X derives the parameters; Section Y draws out the pattern they form."* |
| Rhetorical questions as transitions | A question only when it is a real, attributed question the text then answers |
| Symmetric paragraph openers across a section | Vary the entry point: claim, contrast, consequence, concession. (Deliberate two-beat anaphora per §d is exempt — it is a device, not a tic.) |

## (i) Calibration

Before drafting, re-read one or two **recently ratified** pieces — the newest rubric-cleared notes (`git log docs/notes/` finds them) and, once thesis prose exists, the most recently committed dissertation section. The live corpus is the calibration set; this file deliberately names no passages, because ratified prose supersedes and pivots as the research does. If what you draft would look out of place beside what was most recently kept, redraft.
