# Rodríguez 2024 — extraction notes

> M. Rodríguez, G. Betarte, D. Calegari. "A process mining-based method for attacker profiling using the MITRE ATT&CK taxonomy." *Journal of Internet Services and Applications*, vol. 15, no. 1, 2024. doi:10.5753/jisa.2023.3902.
> Source file: `docs/sources/2_4_rodriguez2024process.md` (gitignored).
> Relevance to this thesis: the process-mining exemplar in lit review §III-D (the [7] citation) — recovers attacker process structure (Petri nets) from labelled runtime event logs, shifting the manual cost from narrative curation to authoring/maintaining technique-labelling rules.

## Bibliographic anchor

- **Citation key**: `rodriguez2024`
- **DOI / URL**: 10.5753/jisa.2023.3902
- **Pages cited from**: full text

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### TODO — Pass 2

(awaiting Pass-2 deep extraction)

Sections to lift in Pass 2:
- The process-mining pipeline — event-log labelling → process discovery (Petri-net or similar formalism).
- The attacker-profiling framing — particularly the lit review §III-D opening sentence locator ("connecting individual tactics, techniques, and procedures into chains shaped by the attacker's objectives, motivations, and knowledge").
- The technique-labelling rules and their manual-cost profile.

---

## Open questions / things to verify

- **Flag to Marc — citation-key year decision.** Filename and current citation key use `rodriguez2024`; DOI suffix is `2023` (`10.5753/jisa.2023.3902`); source frontmatter reads "Journal of Internet Services and Applications, 2023, 15:1" with Received 05 Dec 2023 / Accepted 17 Apr 2024 / Published 01 Aug 2024. The `2023` in the DOI reflects the journal volume's opening year (vol 15 opened 2023); actual publication is August 2024. Decision needed: keep `rodriguez2024` (tracks publication year, matches filename, aligns with how the lit review reads it) or switch to `rodriguez2023` (tracks the DOI year and the volume's nominal year). **Recommendation:** keep `rodriguez2024` — publication year is the more useful disambiguator for the reader, the filename is already `rodriguez2024`, and the bibliography entry can carry the full date metadata regardless of the key. If Marc prefers DOI-year tracking, the rename touches the citation key, filename, and the lit-review prose's `[7]` resolution.
- Whether the Petri-net output is operationalisable as a simulator-runnable attacker process, or whether it remains analytical.
- The attacker's objectives/motivations/knowledge framing — confirm exact wording for the lit-review §III-D opening citation.

## Out of scope for this thesis

- Process-mining theory beyond what's needed to assess applicability.
