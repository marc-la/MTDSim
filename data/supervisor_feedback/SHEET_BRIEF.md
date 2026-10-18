# Brief: before/after sheets for the supervisor's final feedback (2026-10-18)

Every sheet agent reads this brief. The register, with each item's scoping, verdict and recommendation, is [`docs/handoffs/2026-10-18_supervisor_final_feedback.md`](../../docs/handoffs/2026-10-18_supervisor_final_feedback.md). The format to mimic is `data/claim_check/rulings/G1.md`; read it first.

## What a sheet is for

Marc reads each sheet and rules before any change touches the tex. The thesis is one day from submission and its shape is set. So:
- every change must be **warranted** (the supervisor asked for it, or the scoping showed the text is wrong);
- every change must be **needed** (the minimum that closes the item);
- every change must be **seamless** (it reads as if the paragraph had always said it).

The bar is "right the first time".

## Rules for every proposed "after"

1. **The five checks** (`docs/workflows/voice.md` §(0)): purpose, context, audience, clarity, relevance. The audience is a fourth-year CS student and the examiner. Say more with less, and stop at the peak.
2. **Edit, don't rewrite.** Change only the words the item needs. Keep Marc's ratified wording around the change.
3. **One term per thing, repeated verbatim.** Use only terms the thesis already defines; grep the tex for the exact form before using one. Examples: tactic-to-action mapping, time lost per MTD deployment, NCR reduction, ASP reduction, host layer, service layer, attack action, exposed endpoint, the baseline attacker, the APT attacker model, attack profile, in full / in part. Coin nothing.
4. **Marc's known dislikes:**
   - the not-X-but-Y / "rather than" contrast in short prose;
   - "pace";
   - "held back" (use "disrupts");
   - hedges stacked on hedges;
   - a paragraph that U-turns;
   - the important point anywhere but first;
   - clause fluff.
5. **Where the conventions live:**
   - Ch6 paragraphs open on the property or metric names the reader already has (`docs/workflows/evaluation_conventions.md`, if relevant).
   - Threats use threat → mitigation → what remains wording (`docs/workflows/threats_terminology.md`, load it for any T edit).
   - Ch5 prose is plain description: comparison, numbers, no method philosophy.
6. **Citations.** Add, move or remove one only where the item needs it; say why.
7. **Gate.**
   - Ch1–5 and ch7 are proposals, so mark them **PROPOSE**.
   - Ch6 and the appendices apply after Marc's ruling, so mark them **APPLY ON RULING**.

## Sheet format (Markdown, one file per cluster in `data/supervisor_feedback/`)

1. **Title and the rule.** One paragraph:
   - **Purpose:** what this change protects, from the examiner's side.
   - **Context:** what the evidence is.
   - **Audience:** who reads the touched text.
2. **Table:** `# | Location (section, tex line) | Before | After | Why | Risk`.
   - **Before** is quoted EXACTLY from the current tex (re-read it; another session may have edited it).
   - **After** gives **Rec.** first, and at most one alternative only where there is a real choice.
   - **Risk** names what could go wrong at that location: a ripple, a term clash, a hedge, a number that must agree elsewhere, a word-band cost.
3. **In place.** For every paragraph touched, print the whole paragraph as it would read after the change, with the changed words in **bold**. This is the seamlessness test: read it aloud in your head, and fix anything that jars before handing over.
4. **Considered, no change.** Every place you checked and left, each with a one-line reason.
5. **Net.** Words added or removed (hand count is fine; say so), and citations changed.

Do not edit `docs/thesis/` or any other tracked file except your own sheet. Do not commit.
