# NITRD 2009 — extraction notes

> NITRD CSIA-IWG. *Cybersecurity Game-Change Research & Development Recommendations*, "Moving Target Defense" theme. National Coordination Office for Networking and Information Technology Research and Development, 2009.
> Source file: `docs/sources/1_1_ghosh2009NITRD.md` (gitignored).
> Relevance to this thesis: foundational definition of MTD — cited as [1] in the lit review opening ("attacks can be thwarted but not prevented"); supplies the framing that MTD inverts the eliminate-vulnerabilities assumption.

## Bibliographic anchor

- **Citation key**: `nitrd2009` (institutional form; renamed from the earlier `ghosh2009nitrd` per Marc's confirmation — NITRD CSIA-IWG is a working-group product, not personally authored by Ghosh).
- **Year**: 2009 — confirmed from filename `1_1_ghosh2009NITRD.md`; the source body carries no internal date stamp but matches the NITRD CSIA-IWG *Cybersecurity Game-Change Research & Development Recommendations* released in 2009 (predates the Jajodia et al. 2011 *Moving Target Defense* edited volume, which is a separate artefact).
- **DOI / URL**: n/a — working-group report, not peer-reviewed. The source markdown at `docs/sources/1_1_ghosh2009NITRD.md` is the authoritative artefact for citation purposes.
- **In-text / bibliography form**: `NITRD CSIA-IWG (2009), Cybersecurity Game-Change Research & Development Recommendations, §1 "Moving Target Defense"`.
- **Pages cited from**: §1 "Moving Target Defense" (lit-review `[1]` maps to the §1 framing: §1 "New Game: Attacks only work once if at all" + §1.6 "Most applications, systems and networks are not perfectly secure").

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### Relevance class

**S — Supporting-argument.** NITRD 2009 supplies the opening rhetorical framing of the lit review (§I opener at [`../sources/LIT_REVIEW.md:20`](../sources/LIT_REVIEW.md) — "attacks can be thwarted but not prevented") and the conceptual premise that no system is perfectly secure. It does not drive a specific methodology decision in [`../specs/architecture.md`](../specs/architecture.md) §(c)–(g); the L0→L4 pipeline inherits the *premise* (MTD inverts the eliminate-vulnerabilities assumption) but not any concrete primitive from this document.

### "New game" framing — attacks only work once if at all

**Source locator:** §1 "Moving Target Defense" → §1 sub-heading "New Game: Attacks only work once if at all" → §1 "What is the new game?" (the source markdown does not expose page numbers; locator is by section / heading).

**Paraphrase:** The report frames MTD as a reversal of the prevailing static-defence game. Under the current game, attackers exploit the long-lived stability of system parameters (addresses, names, port numbers), allowing reconnaissance and exploit-development costs to be amortised across many targets and across time. The "new game" wins by increasing randomness and decreasing predictability of the defender's cyber terrain, so that the adversary is forced to redo reconnaissance and launch exploits anew for each penetration — denying the attacker any amortisation of development costs. MTD is positioned as the path to that new game.

**Quote (essential — anchors the §I opener phrasing):**
> "In the new game we win by increasing the randomness or decreasing the predictability of our systems. By making the cyber terrain appear chaotic to the adversary, we force him to do reconnaissance and launch exploits anew for every desired penetration; the attacker enjoys no amortization of development costs." (§1 "What is the new game?")

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(a) "Goal and scope" — the goal frames MTD as the defence whose value the L0→L4 evaluation pipeline is built to measure; this passage is the foundational statement of *why* such evaluation is worth doing. Also [`../sources/LIT_REVIEW.md:20`](../sources/LIT_REVIEW.md) — citation [1] anchoring "attacks can be thwarted but not prevented".

**Disposition for this thesis:** *adopted-as-baseline framing.* The thesis inherits the MTD premise wholesale (MTD inverts the eliminate-vulnerabilities assumption; reconnaissance decays under continuous configuration change) and does not contest it. The contribution sits *downstream* of this framing — given that MTD claims to disrupt the attacker at the apex of the Pyramid of Pain, are existing MTD mechanisms evaluated against attackers modelled at that fidelity? — rather than relitigating whether MTD is worthwhile in principle.

---

### Imperfect-security premise

**Source locator:** §1.6 "Decoys" opening paragraph (the source markdown does not expose page numbers; locator is by section).

**Paraphrase:** The decoys idea opens with an explicit statement of the imperfect-security premise that underlies the broader NITRD MTD theme: most applications, systems and networks are not perfectly secure, and so compromise of a targeted system is a matter of time. The decoys discussion uses this premise to motivate detection-via-deflection; for the present thesis the load-bearing element is the premise itself, not the decoys mechanism that follows from it.

**Quote (essential — exact phrasing maps to lit-review citation):**
> "Most applications, systems and networks are not perfectly secure. Hence, it is a matter of time until they can be compromised in a targeted attack." (§1.6 "Decoys", opening sentence)

**Maps to:** [`../sources/LIT_REVIEW.md:20`](../sources/LIT_REVIEW.md) — citation [1] anchoring the §I opener ("it proceeds from the premise that no system is perfectly secure"). Also [`../specs/architecture.md`](../specs/architecture.md) §(a) — the L4 comparative question presupposes that MTD is the defensive response to this imperfect-security premise.

**Disposition for this thesis:** *adopted-as-baseline framing.* The premise is the philosophical entry-point for the entire MTD literature reviewed in the dissertation; no methodological divergence is taken from it.

### Used in lit review

- [`../sources/LIT_REVIEW.md:20`](../sources/LIT_REVIEW.md) — §I "Introduction" opener, citation `[1]`: anchors the claim that MTD "proceeds from the premise that no system is perfectly secure, so that attacks can be thwarted but not prevented". This is the only citation site for `nitrd2009` in the lit review. The matching bibliography entry is at [`../sources/LIT_REVIEW.md:237`](../sources/LIT_REVIEW.md) (full reference: NITRD Program, *National Cyber Leap Year Summit 2009 Co-Chairs' Report*; MTD working group co-chaired by A. K. Ghosh, D. Pendarakis, W. Sanders).

---

## Open questions / things to verify

None outstanding. The two anchor passages (§1 "new game" framing and §1.6 imperfect-security premise) both sit inside the source markdown verbatim; no external follow-up is required. Per the source-markdown-authority note ([memory:feedback_source_markdown_authority]), `docs/sources/1_1_ghosh2009NITRD.md` is itself the citable artefact for this NITRD working-group report.

## Out of scope for this thesis

- NITRD's broader cybersecurity game-change themes outside MTD.
