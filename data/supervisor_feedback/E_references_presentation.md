# E: references and presentation (items 10, 11, 12)

**The rule.**
- *Purpose:* an examiner reads a working note left in a reference, a misdescribed entry or an unselectable page as a lack of care. They are cheap to fix and costly to leave.
- *Context:* his numbers [4] [14] [17] [26] [32] [62] name the same keys in the 2026-10-15/16 builds and today. "Page 29" matches no page in any candidate build. The only pages with both symptoms, a different face and unselectable text, are Appendix A, the proposal (printed pp. 49–54).
- *Audience:* the examiner, at the reference list and the appendix.
- **Gate:** the bib and the appendix are **APPLY ON RULING**. The preamble line is a build fix with no printed words.

## Item 10: notes left in references

`ieeetr` prints neither `url` nor `doi`, so each URL stays in `note` and only the working remark goes.

| # | Ref, key (bib line) | Before (`note`) | After (`note`) | Why | Risk |
|---|---|---|---|---|---|
| 10a | [4] ghosh2009nitrd (l.47) | Multi-author summit report; Moving Target Defense working group co-chaired by A.\ K.\ Ghosh, D.\ Pendarakis, and W.\ Sanders. Sponsored by the {U.S.} Office of Science and Technology Policy ({OSTP}). [Online]. Available: \url{…CoChairs_Report.pdf} | [Online]. Available: \url{…CoChairs_Report.pdf} | The author and institution fields already name NITRD; the co-chairs and the sponsor are our remarks. | The key says "ghosh", but the text cites it without an author name (l.291, l.295), so nothing in the prose depends on Ghosh. |
| 10b | [26] rodriguez2024 (l.434) | Brazilian SBC publication; distinct from the Springer JISA. [Online]. Available: \url{…/3902} | [Online]. Available: \url{https://journals-sol.sbc.org.br/index.php/jisa/article/view/3902} | The remark was a note to ourselves. Claim check R6 confirmed the entry (2024, 15(1), pp. 212–232). | None. |
| 10c | [32] mcqueen2006 (l.850) | INL preprint INL/CON-05-00649; OSTI 911165 | *(delete the `note` line)* | The preprint IDs are our lookup trail; the published chapter is the citation. | The DOI does not print under `ieeetr`, so the entry shows no link. That is normal for a book chapter. |
| 10d | [62] cybereasoncobaltkitty (l.1081) | Published 24~May 2017; original page no longer available, archived copy. [Online]. Available: \url{http://web.archive.org/…}. Accessed 20~August 2026 | Published 24~May 2017. [Online]. Available: \url{http://web.archive.org/web/20260803042637/https://www.cybereason.com/blog/operation-cobalt-kitty-apt}. Accessed 20~August 2026 | The web.archive.org URL already shows it is an archived copy. | None. |
| 10e | [37] mitre2026attackv19 (l.581), *found in the sweep* | {ATT\&CK} v19. Released 28~April 2026; Enterprise: 15 tactics. [Online]. … | {ATT\&CK} v19. Released 28~April 2026. [Online]. … | "15 tactics" is a fact the text uses, not bibliographic data. | None; the text states the 15 tactics with this citation (l.4014). |

Kept after the sweep of all 74 entries:
- the version and date notes in [15], [21], [22] and [24];
- "Art. no." in [8] and [25];
- [2]'s co-authoring agencies, which back "agencies from five countries" (l.264).

## Item 11: Tay [14] and Ho [17]

| # | Ref, key (bib line) | Before | After | Why | Risk |
|---|---|---|---|---|---|
| 11a | [14] tay2024 (l.160) | `type = {{GENG5512} Engineering Research Project Report},` | *(delete the line)* | Under `@mastersthesis`, `ieeetr` then prints "Master's thesis, The University of Western Australia, Perth, Australia, Oct. 2024". This matches the proposal and zhang2023, a work of the same kind (its cover reads "MASTERS THESIS"). Tay's own conclusion calls the work "this thesis". | GENG5512 being a Master of Professional Engineering unit is general knowledge, not checked locally. |
| 11b | [17] ho2024 (l.188) | `type = {{GENG5512} Engineering Research Project Report},` | *(delete the line)* | Same as 11a, so the three lineage entries read alike. | Ho's text calls itself "this report". "Master's thesis" describes the kind of degree work, the same as for Zhang's. |
| 11c | zhang2023 (l.902), *consistency* | `school = {University of Western Australia},` | `school = {The University of Western Australia},` | The three lineage entries then print the same institution name. | None. |

**The near-identical titles are correct.** Each title matches its own cover: Tay, "Using Artificial Intelligence to Automate the Deployment of Moving Target Defence Operations"; Ho, "… of MTD Operation". They were two students with one supervisor in the same semester, on one project title. Nothing in the text describes either as a "report", so no prose changes.

## Item 12: page 29

| # | Location | Before | After | Why | Risk |
|---|---|---|---|---|---|
| 12a | `docs/thesis/proposal.pdf` | Recompiled locally on 2026-08-20 without cm-super: Type3 bitmap fonts, no ToUnicode, so the text copies as symbols. 6 pages. | The original submission, `…/Downloads/2902212125 - Marc Labouchardiere - 23857377_Proposal_13032026.pdf`: Type1 fonts, text selectable. 7 pages; page 1 is the UWA declaration. | Pages 2–7 have the same text as the current pages 1–6. "As submitted in March 2026" becomes literally true. | Checked 2026-10-18: Type1 SF fonts with ToUnicode on pages 1 and 2. |
| 12b | `dissertation.tex` l.9990, l.9995 | `\includepdf[pages=1,pagecommand=…]{proposal.pdf}` … `\includepdf[pages=2-]{proposal.pdf}` | `pages=2` … `pages=3-` | This skips the declaration page, so Appendix A's length is unchanged (6 pages). The comment above changes to say the PDF is the submitted file, not a build of proposal.tex. | Item 8's sentence goes in the same `pagecommand` margin label. Build-check both together. |
| 12c | Preamble (after the `\propstandin` block) | *(none)*. cshonours.cls sets `\labelitemi{\textbullet}`, which renders as a Type3 bitmap (`tcrm1200`). | `\renewcommand\labelitemi{\(\bullet\)}` | The contribution bullets (printed p.2) and the §7.2 bullets (p.47) become Type1 glyphs. | The maths bullet is the same size. Check p.2 by eye after the build. |
| 12d | Six figures built through Chromium (Figs 2.1–2.3, 4.1–4.3, 4.5, C.2) | Type3 Nimbus Sans. The text is selectable, but haloed labels copy twice. | **Not proposed today.** A TrueType font swap in the generators is 2–3 h. | They are selectable and in the house figure face, so they do not match Jin's symptom. | Leave unless time remains after everything else. |

**Ask Jin, if convenient:** whether "page 29" was printed 49, the proposal's first page. If it was another page, 12a–12c still fix every page with unselectable text.

## Net

- Reference list: about −48 words (10a–10e). The reference list counts toward the band (UWA page).
- Body: 0 words.
- Keys cited: unchanged (74).
