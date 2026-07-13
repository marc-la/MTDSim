# <Author Year> — extraction notes

> <Full citation: author(s), title, venue / publisher, year.>
> Source file: `docs/sources/<filename>.<ext>` (gitignored).
> Relevance to this thesis: <one line — why this paper is in the lit review>.

**Institutional / spec sources** (no author, e.g. CTID Attack Flow, NITRD documents, MITRE ATT&CK as a standard rather than a paper): use `<institution><year>` or `<projectname><year>` in place of `<Author Year>` in the heading. Citation key follows the same form (e.g. `attackflow`, `nitrd2009`). The remaining sections are unchanged — `Pages cited from` becomes `Section / version cited from` for a versioned spec.

## Bibliographic anchor

- **Citation key**: `<lastname-year>` (matches the BibTeX entry in the dissertation; institutional form `<institution><year>` for non-author sources)
- **DOI / URL**: <if available>
- **Pages cited from**: <range, or "full text", or version-N for specs>

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### <Concept 1 — e.g. "MTD scheduling formula">

**Source locator:** §3.2, eqn (4); p. 17

**Paraphrase:** what the paper says, in your own words. State what's being claimed, under what assumptions, and what's left implicit.

**Quote (if essential):**
> "<verbatim, short>"

**Maps to:** [`../specs/mtdsim_spec.md`](../specs/mtdsim_spec.md) MTD-XX · [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §c

**Disposition for this thesis:** <verified / divergent / unimplemented / adopted-as-baseline / contrasted-against — and why>

---

### <Concept 2>

...

---

## Open questions / things to verify

Items extracted from the paper that you weren't certain about and would want to chase up:
- <question>, p. <n> — <why it matters>

## Out of scope for this thesis

What the paper covers that isn't load-bearing for this work. Recording these prevents re-reading the same sections later wondering whether they're relevant.
