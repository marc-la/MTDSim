# Sadlek 2022 — extraction notes

> L. Sadlek, P. Čeleda, D. Tovarňák. "Current Challenges of Cyber Threat and Vulnerability Identification Using Public Enumerations." *The 17th International Conference on Availability, Reliability and Security* (ARES 2022), Vienna, Austria, August 23–26, 2022. ACM, 8 pp. doi:10.1145/3538969.3544458.
> Source file: `docs/sources/2_2_sadlek2022current.md` (gitignored).
> Relevance to this thesis: peer-reviewed corroboration of the Pyramid of Pain's ordering (lit review §III-B) — TTPs as "the most mature indicators used for the security defense"; IP-address validity decays within a day; behavioural patterns persist with operational habits.

## Bibliographic anchor

- **Citation key**: `sadlek2022`
- **DOI / URL**: `https://doi.org/10.1145/3538969.3544458`
- **Venue**: *The 17th International Conference on Availability, Reliability and Security* (ARES 2022), August 23–26, 2022, Vienna, Austria. ACM, New York, NY, USA, 8 pages.
- **Author order**: Lukáš Sadlek, Pavel Čeleda, Daniel Tovarňák — per the ACM Reference Format on source p. 1 and the "L. Sadlek et al." running header on p. 2. (The byline block at the top of the source PDF text renders Čeleda first; that is affiliation-block layout, not citation order.) The lit review's "Sadlek et al. [15]" at `docs/sources/LIT_REVIEW.md:116` matches the publisher's canonical short form.
- **Pages cited from**: p. 3 (TTP-maturity claim — quoted at lit review line 116). IP-decay locator within the paper still TODO for Pass 2.

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### TODO — Pass 2

(awaiting Pass-2 deep extraction)

Sections to lift in Pass 2:
- The TTP-as-mature-indicator framing (p. 3).
- The empirical IP-address-validity-decay claim ("within a day").
- The categorical-distinction argument used in lit review §III-B.

---

## Open questions / things to verify

- Exact §-locator for the "IP-address validity decays within a day" claim (Pass 2).

## Out of scope for this thesis

- The broader CVE / CWE enumeration challenges discussed in the paper.
