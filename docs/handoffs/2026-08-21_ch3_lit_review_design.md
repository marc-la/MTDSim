---
status: open                  # design only; retire when the ch3 skeleton is ratified into dissertation.tex and the strand notes are written
created: 2026-08-21
---

# Standing context for the literature review (ch3) — what the chapter has to achieve, and a unit-level structure that achieves it

> **Grey-box note.** This design was built from the *context* layer only, on Marc's
> instruction: the writing guide, the chapter READMEs, the notes rubric, the
> literature conventions, the `dissertation.tex` skeleton comments, and the two
> notes already staged in `ch3_lit_review/`. The implementation records, the
> supervisor decision register and the APT-model criterion were deliberately **not**
> read — including the criterion that CLAUDE.md normally mandates each session —
> so that the structure is derived from the chapter's declared job rather than
> reverse-engineered from rulings already taken. Anything below that would need a
> ruling is flagged as a CONFIRM, not applied. Nothing in `dissertation.tex` was
> touched.

---

## Part 1 — What the chapter has to achieve

### The job, in one line

The literature review earns the gap: by its last paragraph the reader should
already have concluded, unprompted, that **no existing work evaluates moving
target defence against a behaviourally-grounded, objective-driven campaign that
is already inside the network** — and the chapter then says so plainly.

### Six things it owes the rest of the document

1. **Earn the gap, don't announce it.** The chapter README's contract: each
   category of prior work is told as a chronological story — a method, what it
   achieved, the limitation that forced the next method — never a neutral
   catalogue. Every cited work earns a sentence of evaluation. The conclusion is
   the reader's before it is the author's.

2. **Fill the "what exists" row for all three threads.** The whole document runs
   on the capture / model / evaluate spine, and the literature review is the
   column where each thread's prior art is established. Each section is
   answerable to exactly one sub-question: 3.1 → capture, 3.2 → model, 3.3 →
   evaluate. A paragraph that cannot name its cell is a cut candidate.

3. **Plant the landmarks the introduction sprints between.** Chapter 1 is a
   compression of this chapter — a landmark-to-landmark hop straight to the gap.
   That only works if this chapter has identifiable landmarks. One or two per
   strand, deliberately chosen and visibly load-bearing, so the introduction has
   something to hop to.

4. **Supply the raw material for the methodology's yardstick without spending
   it.** The methodology opens by deriving a fidelity criterion *from the
   literature*. That derivation is only legitimate if the literature it derives
   from has already been surveyed here. The chapter therefore owes the APT
   characterisation and the field's own self-criticism of its attacker models —
   and owes them **as literature**, not as criteria. Posing the axes is §4.1's
   job; ch3 must not pre-empt it.

5. **Stay off the neighbouring chapters' turf.** Background (ch2) carries the
   inherited simulator; the literature review carries the field. Methodology
   (ch4) carries what this work did; the review carries what exists and what it
   cannot do. Discussion (ch6) carries what changes for the field in light of
   results; the review argues from the literature alone and cites nothing of this
   thesis's own findings.

6. **End on the demonstrated need.** Not on a summary. The chapter's final unit
   is the hinge the methodology's first sentence swings on.

### The constraint sheet

| Constraint | Value |
|---|---|
| Budget | 3 000 words / **12 units** (writing guide ledger) — the largest chapter in the document |
| Unit definition | one subsection = 1–2 concise paragraphs ≈ 250 words; every heading is a claim on a unit, and no heading is added without a budget line |
| Source pool | the tiered review corpus in `docs/sources/lit_review/` (~20 papers) plus ~50 extractions |
| Provenance | the existing 7 090-word review is the **quarry, not the draft** — ch3 is a 42 % boil-down *restructured* onto the three strands, not an edit of the old section order |
| Citation selection | per category: the **first** method (sets the direction), the **most established** (survived the test of time), the **latest** (current year where possible — a stale newest reference dates the whole review) |
| Field conventions | ATT&CK first-use form and version stamp; concepts cited to their origin, not to whichever survey mentioned them; metrics defined with equation and better-direction before use; Australian spelling outside proper names |
| Headings | sentence case, acronyms spelled out at the final pass (working titles until then) |
| Voice | notes rubric + `voice.md`; drafting via Marc's dictation pipeline, sessions scaffold and scrutinise only |

### The chapter's rhetorical shape — the scissors

The three strands are not three surveys stapled together; they are two blades and
a missing hinge, and saying so in the preamble is what stops the chapter reading
as a catalogue:

- **Blade one (3.1).** The field knows a great deal about how real intrusion
  campaigns behave, and has spent a decade turning that knowledge into structured,
  machine-usable artefacts.
- **The missing hinge (3.2).** The attacker models that moving target defence is
  evaluated against draw almost none of it. They are abstract, memoryless and
  aimed at the surface; the field says so about itself.
- **Blade two (3.3).** The evaluation machinery — the ladder of methods, the
  metric suite — is mature, but every metric in it is scored *over* an attacker
  model, so a thin attacker model silently bounds what any of them can express.

The gap is the space between the blades, and the order capture → model → evaluate
is also a dependency order: the reader cannot judge that MTD's attacker models are
thin until they have seen what a rich one would look like, and cannot see the
evaluation gap until they accept that the attacker model bounds the metric.

---

## Part 2 — The structure

### Answering the 3.1 question

The slot is already named in the skeleton — *Survey of APT attackers*, feeding
capture. The design problem is not which slot, it is **what job the slot does**,
because the working title invites the single worst outcome available to this
chapter: three units of threat-group colour (APT1, Lazarus, Volt Typhoon), which
is a catalogue, fails the chapter's own contract, and buys the methodology
nothing.

**Recommendation: keep the slot, re-aim the job.** Section 3.1 is not *who the
advanced persistent threats are*. It is:

> **Can the literature hand you a machine-usable behavioural specification of an
> intrusion campaign — and what does that specification still not carry?**

Named that way the strand does real work: it establishes that campaign behaviour
is publicly documented at technique granularity, that a mature line of work
converts prose reporting into structure, and that what those artefacts encode is
*order, not tempo* — the residual blank that the methodology's timing layer later
fills. Individual campaigns then appear as evidence for a claim, one clause each,
rather than as a gallery.

**The alternative considered and rejected:** making 3.1 a moving-target-defence
primer (taxonomy, shuffle/diversity/redundancy, what-when-how, coverage). It
breaks the one-strand-per-sub-question keying, costs the capture thread its
"what exists" cell entirely, and duplicates vocabulary the background chapter
already owes when it describes the inherited mechanisms. See CONFIRM 3.

### The unit ledger — 12 units

| Block | Units | Words |
|---|---|---|
| Preamble (unnumbered) | 1 | 250 |
| 3.1 Capture — the behavioural record | 3 | 750 |
| 3.2 Model — attacker models in MTD | 4 | 1 000 |
| 3.3 Evaluate — how MTD is judged | 4 | 1 000 |
| **Total** | **12** | **3 000** |

**Preamble (unnumbered, ~250 words).** Declares the scissors, the three strands
and the sub-question each feeds, and the selection rule the reader is entitled to
know (first / most established / latest). One sentence plants the coverage claim
the chapter will close on, so the reader reads the rest as evidence gathering
rather than as survey. No literature is argued here — it is the map, not the
territory.

**3.1 — Capture: the behavioural record (3 units)**

- **3.1.1 — What makes these campaigns structurally different.** Phase-structured,
  objective-driven, long-dwell, human-operated: the kill chain as the move that
  first made intrusion a *sequence* rather than an event, the survey literature
  that established the characterisation, and current campaign reporting as the
  live evidence. The unit's payload is the contrast that the whole thesis rests
  on — this adversary is nothing like the fast, uniform, surface-directed
  attacker that section 3.2 will show MTD evaluation assumes.
- **3.1.2 — The behavioural lingua franca.** ATT&CK as the field's shared
  vocabulary, introduced to its origin and pinned to its version; and the
  argument for why the technique-and-tactic level is the *durable* level to model
  at rather than the indicator level. This unit is the one that licenses the
  entire pipeline's choice of unit of analysis.
- **3.1.3 — From prose reports to executable structure.** The decade of work
  turning narrative threat reporting into structured artefacts — automated
  extraction, flow representations, process-mined models — told chronologically
  as capability accruing. Closes on the residual: these artefacts encode
  *sequence*, and essentially never *duration*. That closer is the capture
  strand's handover to the methodology and the citable answer to "did you look?".

**3.2 — Model: attacker models in MTD (4 units)**

- **3.2.1 — The default adversary.** The abstract, probabilistic, surface-directed
  attacker inherited from the analytic security-modelling tradition: what it
  assumes, and — argued fairly — why those assumptions were reasonable for the
  question that tradition was asking.
- **3.2.2 — Strategic attackers.** Game-theoretic MTD: what modelling the
  adversary as a rational opponent buys (interaction, timing, equilibrium
  reasoning) and what it costs (a payoff function standing in for behaviour, so
  the model can be strategically sophisticated and behaviourally empty at once).
- **3.2.3 — Learned attackers.** Reinforcement-learning attackers and
  attacker–defender co-training: the current frontier, its realism claim, and
  what it actually models — reward-shaped exploration over an abstract state
  space, not a campaign pursuing an objective.
- **3.2.4 — What recent work actually assumes, in cross-section.** The strand's
  verdict unit: a comparison of the attacker models used across recent MTD
  evaluations on a common set of axes, and the field's own published criticism of
  ill-defined and unrealistic attacker models. Closes on the gap sentence —
  campaign-behaviour modelling and MTD attacker modelling are two literatures
  that barely touch.

**3.3 — Evaluate: how MTD is judged (4 units)**

- **3.3.1 — The ladder of evaluation methods.** Analytical model, simulation,
  emulation, real testbed: where MTD evaluation sits, why simulation dominates,
  and what each rung can and cannot support. This is also where the field's own
  pros-and-cons framing is put on the record, so the methodology can position
  this work on the ladder and own the costs rather than discovering them.
- **3.3.2 — The metric suite, and what it is scored over.** The canonical
  metrics cited to their origins and defined to convention, followed by the
  strand's hinge observation: each of them is computed against an attacker's
  progress, so the attacker model is not an input to the evaluation, it is a
  *bound* on it.
- **3.3.3 — What the instruments presuppose.** The scenarios, the metrics and the
  reported outcomes of the field are shaped around an adversary who is still
  outside — reconnaissance defeated, a known-configuration exploit missed. The
  consequence is precise and worth stating precisely: performance against an
  adversary who already holds a foothold is not so much unanswered as **unasked**.
- **3.3.4 — The demonstrated need** *(may be an unnumbered closing block)*. The
  three strands closed in one paragraph: the behaviour is capturable, the models
  do not capture it, and the instruments cannot see the phase where it would
  matter. Names what would have to be built to ask the question — and stops
  there, because building it is chapter 4.

### Figures and tables

Figures and tables sit **outside** the word budget, which makes them the cheapest
real estate in a chapter that is 3 000 words for the largest survey job in the
document. Two candidates, in priority order:

1. **The attacker-model cross-section table (3.2.4)** — highest value, and the
   material is already drafted in the existing review. It is the chapter's single
   strongest piece of evidence, it converts what would be three paragraphs of
   enumeration into one paragraph of argument, and it is exactly the artefact an
   examiner looks for when a thesis claims a modelling gap.
2. **A phase-coverage figure (3.3.3)** — mapping what the surveyed mechanisms
   reach onto the tactic sequence, making the unasked-question claim visible in
   one look. Second priority because it must be built rather than harvested, and
   because it has to be genuinely readable to earn its place.

Per the writing guide's order of operations, both are drawn *before* their units
are drafted, with captions written long and squeezed as the body absorbs them.

### Boundaries — what ch3 must not do

- **Not describe the inherited simulator.** Background's job. Where 3.2 needs the
  scripted six-phase attacker as an example of the default adversary, it points
  forward rather than re-describing it.
- **Not do method.** Especially at 3.1.3: the strand says the corpus lacks
  timing; it must not describe how this work derives durations.
- **Not pose the fidelity criterion.** The review supplies the literature; §4.1
  turns it into axes. A ch3 unit that starts numbering requirements has taken the
  methodology's opening move.
- **Not cite this thesis's own results.** The gap is argued from the literature,
  and stays argued from the literature even after the numbers exist.
- **Not rehearse the introduction.** Chapter 1 compresses this chapter; the
  dependency runs one way.

---

## Open CONFIRMs — Marc's calls before the skeleton is cut

1. **3.1's job and working title.** Re-aim from *survey of the attackers* to
   *survey of the behavioural record and what it does and does not carry*. This is
   the substantive one: it decides whether 3.1 spends three units on evidence or
   on colour.

2. **The altitude of the gap** *(this one re-aims an existing note)*. The staged
   gap note argues coverage bias as a claim about what the **mechanism reaches**
   (surface-shifting cannot touch capability and credential state). The structure
   above closes instead on an **evaluation** claim — the field's instruments and
   scenarios are built around a pre-foothold adversary, so post-ingress
   performance is unasked. The evaluation framing is recommended: it sits inside
   the research question rather than beside it, it is far harder to falsify (it
   survives the discovery that post-ingress MTD work exists — that work would
   still be evaluated against thin attackers), and it hands the methodology a
   cleaner mandate. The mechanism-level claim then rides as supporting evidence in
   3.3.3 rather than as the load-bearing gap.

3. **Where the mechanism taxonomy is taught.** Recommended: the background
   chapter, when it describes the inherited defences — the field's conventions
   already expect each mechanism to arrive with its taxonomy class and its
   what/when/how answers, so the vocabulary is paid for there and the review
   inherits it. The alternative is one sentence in the ch3 preamble, which is
   affordable but duplicative.

4. **The ledger split.** Recommended 1 / 3 / 4 / 4. The alternative is
   1 / 4 / 4 / 3, which buys 3.1 room for the campaign evidence at the cost of
   compressing the evaluate strand — the strand that has to carry both the metric
   argument and the chapter's closing move. Recommend against.

5. **Whether 3.3.4 is a numbered subsection or an unnumbered closing block.**
   Costs the same 250 words either way; the choice is whether the chapter's most
   important paragraph appears in the table of contents.

## Scrutiny of the source review

The submitted review has since been read against this design and the critique
protocol; the record is
[`2026-08-21_lit_review_scrutiny.md`](2026-08-21_lit_review_scrutiny.md). It carries
per-section keep/rework/cut verdicts, the diagnosis of why the gap section reads
weak, and **a revision to CONFIRM 2 below**: on the evidence (the phase-coverage
argument appears nowhere in the review), fidelity should be the chapter's spine and
coverage its consequence, rather than the evaluation-altitude framing recommended
here.

## What is not yet staged

The chapter directory holds two notes — the gap statement and the timing-precedent
survey — and both feed the *closers* (3.3.3/3.3.4 and 3.1.3 respectively). **No
note exists for any of the three strands' bodies**: the capture-maturity argument,
the attacker-model cross-section, or the evaluation-ladder-and-metric argument.
That is the drafting dependency, and it is the work this design brief hands to the
next session — one rubric-gated note per strand, each marking its landmark works
so the introduction has something to hop between.

## Out of scope (explicitly)

Cutting the skeleton into `dissertation.tex`; drafting any ch3 prose; writing the
strand notes; re-reading the review corpus to fix the per-unit citation lists.
This brief is structure and contract only.
