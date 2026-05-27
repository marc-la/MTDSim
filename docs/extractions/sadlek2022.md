# Sadlek 2022 — extraction notes

> P. Čeleda, L. Sadlek, D. Tovarňák. "Current Challenges of Cyber Threat and Vulnerability Identification Using Public Enumerations." Masaryk University, 2022.
> Source file: `docs/sources/2_2_sadlek2022current.md` (gitignored).
> Relevance to this thesis: peer-reviewed corroboration of the Pyramid of Pain's ordering (lit review §III-B) — TTPs as "the most mature indicators used for the security defense"; IP-address validity decays within a day; behavioural patterns persist with operational habits.

## Bibliographic anchor

- **Citation key**: `sadlek2022` (preserved pending Marc's decision — see Open questions)
- **DOI / URL**: `https://doi.org/10.1145/3538969.3544458`
- **Venue**: *The 17th International Conference on Availability, Reliability and Security* (ARES 2022), August 23–26, 2022, Vienna, Austria. ACM, New York, NY, USA, 8 pages.
- **Author order — canonical (ACM Reference Format, source p. 1)**: Lukáš Sadlek, Pavel Čeleda, and Daniel Tovarňák. The running header on p. 2 also reads "L. Sadlek et al.", confirming the "Sadlek et al." short form used in the lit review (§III-B, line 116) is correct per the publisher's own citation format. The earlier byline block at the top of the source PDF text (which renders Čeleda first) appears to reflect affiliation-block layout, not citation order. The blockquote header at line 3 of this stub should be reordered to match the ACM Reference Format — flagged in Open questions.
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

- **Author-order — resolved factually, pending Marc's stylistic choice.** The source PDF's affiliation block (top of `docs/sources/2_2_sadlek2022current.md`, lines 3–7) lists Čeleda first, but the ACM Reference Format on the same page (line 33 of the source markdown) and the paper's own running header give the citation order as **Sadlek, Čeleda, Tovarňák** — so the lit review's "Sadlek et al. [15]" at `docs/sources/LIT_REVIEW.md:116` matches the publisher's canonical form. Question for Marc:
  - (a) The actual first author per the paper's ACM Reference Format is **Lukáš Sadlek**; the lit review is consistent with this.
  - (b) Choose between (i) keeping `Citation key: sadlek2022` and the "Sadlek et al." short form as-is (recommended — matches ACM Reference Format), or (ii) renaming to a Čeleda-first form (`celeda2022`, "Čeleda et al.") if you have a separate bibliographic-style reason to prefer affiliation-block order over the publisher's citation block.
  - (c) If (ii) is chosen, the only lit-review locator needing an update is **`docs/sources/LIT_REVIEW.md:116`** (three uses of `[15]` on that line — the "Sadlek et al. [15]" prose phrase plus two bare `[15]` parenthetical cites). The reference-list entry for `[15]` (not shown in the excerpt I checked) would also need rewording.
- The blockquote header at line 3 of this stub currently renders Čeleda first; if (i) is chosen, reorder it to "L. Sadlek, P. Čeleda, D. Tovarňák" to match the ACM Reference Format. Left as-is for now pending Marc's call.
- Exact §-locator for the "IP-address validity decays within a day" claim (Pass 2).

## Out of scope for this thesis

- The broader CVE / CWE enumeration challenges discussed in the paper.
