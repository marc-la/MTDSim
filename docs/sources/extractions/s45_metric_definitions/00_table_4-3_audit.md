# Table 4.3 (`tab:metrics`): table audit

Auditor's output, 2026-09-25. No repository file edited. The width test was compiled in `scratchpad/s45/tabtest/` (`t2.tex` is the recommended table, `t3.tex` the rotated-label variant that was rejected; PNGs alongside).

**Verdict in one paragraph.** Table 4.3 reads as an acronym list because the 2026-09-24 rebuild removed the one column that every metric table in the corpus has: a one-line description (Zaffarano Table 4 "Metric | Description", Ho Table 3 "Symbol | Description", Masud Table 3 "Symbols | Explanation | Formula"). What is left is a name, an acronym and a citation. The recommendation is five columns: an **unheaded** class key, **Metric**, **Description**, **Source**, **Equation**.
- The description restores the corpus convention and makes the table a real landing page for the six chapter 5 floats and the one §5.1 sentence that send the reader to it.
- The equation column does the lookup precisely. It has a corpus precedent (Masud's "Formula: Eq. (n)") and a house precedent (`tab:gspn-notation`'s "Declared in").
- Drop the word "Class". House rule 4 and Table 3.1 both leave the key column unheaded, and no held source uses "class" for a group of metrics.
- Keep the source grammar to three states: a bare citation, "adapted from", or "this thesis". "In the form of" should go.
- No direction, unit or "read in" column, and no separate §4.5 symbols table.

---

## LaTeX

Replace the `table` environment in `docs/thesis/tables/tab_4-5a_metrics.tex`. Put the new comment block at the head of the file and keep the existing comment history under it unchanged.

```latex
% REFORMED 2026-09-25 (table audit, s45; Marc: "is Table 4.3 conventional ...
% it's literally the symbol table ... what does it need to carry? ... is 'Class'
% the right word?"). Evidence: scratchpad s45/00_table.md. What changed and what
% it overturns:
% (1) DESCRIPTION column RESTORED as a one-line gloss (not a definition). This
%     overturns the 2026-09-24 removal ("each metric is defined in the subsection
%     of its class") on merit: every metric table in the held corpus has a
%     description (zaffarano2015 Table 4 "Metric | Description"; ho2024 Table 3
%     "Symbol | Description"; masud2025 Table 3 "Symbols | Explanation |
%     Formula"). Without one the table was a list of names with citations.
% (2) EQUATION column ADDED: the number of the equation that defines each metric
%     (masud2025 Table 3's "Formula" column; tab:gspn-notation's "Declared in").
%     It replaces the caption's "defined in the subsection of the same name".
% (3) CLASS HEADER REMOVED: the key column is unheaded, per house rule 4
%     (figure_table_conventions.md §k) and Table 3.1's own unheaded row groups.
%     The labels are §4.5.1-§4.5.3's subsection titles, word for word. Still
%     horizontal, per Marc's 2026-09-24 ruling: re-measured, the rotated labels
%     (82.9 pt) overrun their 3- and 4-row groups.
% (4) SOURCES: three states only (a bare citation = the field defines it as used
%     here; "adapted from" = one difference, stated in §4.5; "this thesis" =
%     introduced, with why, in §4.5). "In the form of" is gone (NCR's source
%     sits on its own row). "Introduced here" -> "this thesis" (masud2025
%     Table 5 "This paper*"). Cells marked VERIFY await the per-metric agents.
% (5) NOT ADDED, on evidence: direction marks (re-verified 2026-09-25, no held
%     source uses one; direction goes in each definition's S4, as alavizadeh2022
%     "a larger value of MF^m is more desirable"); a unit column (none in the
%     corpus's tables; the three timed metrics carry their unit in the gloss or
%     in chapter 5's headers); "read in" (the floats already point here).
% Geometry: 1.9+3.4+5.4+2.35+1.45 = 14.5 cm; the tabular measured 452.6 pt
% against 455.24 pt with realistic [nn, nn] citations (cshonours, margin 2.5 cm,
% \tablestyle, tabcolsep 5pt); no overfull box. The Equation column prints ??
% until each block's \label is uncommented. DRAFT STATE: ratify on read.
\begin{table}[htbp]
  \centering
  \caption[The evaluation metrics]{The evaluation metrics, each with its source and the equation that defines it. A source cited alone defines the metric as it is used here.}
  \label{tab:metrics}
  \tablestyle\setlength{\tabcolsep}{5pt}
  \begin{tabular}{@{}P{1.9cm}P{3.4cm}P{5.4cm}P{2.35cm}P{1.45cm}@{}}
    \toprule
    & Metric & Description & Source & Equation \\
    \midrule
    & Relative tactic occurrence & share of an attacker's steps that fall in each tactic & \citep{rodriguez2024} & \eqref{eq:rto} \\
     & Attack path variation (APV) & share of runs that open differently from the attacker's commonest opening & adapted from \citep{hong2018} & \eqref{eq:apv} \\
     & Attack rate & actions per 1\,000\,s of active time & adapted from \citep{zhan2013, pendleton2016} & \eqref{eq:attack-rate} \\
    \multirow{-4}{1.9cm}{Attacker behaviour} & Attack confidentiality & share of actions a declared rate detector would not flag & adapted from \citep{zaffarano2015} & \eqref{eq:confidentiality} \\
    \midrule
    & Attack success probability (ASP) & share of runs that compromise a target host & \citep{cho2020} & \eqref{eq:asp} \\
     & Network compromise ratio (NCR) & share of the network's hosts compromised by the end of a run & \citep{zhang2023, ho2024} & \eqref{eq:ncr} \\
    \multirow{-3}{1.9cm}{Attack outcome} & Mean time to compromise (MTTC) & mean time from the start of a run to its first compromise & \citep{mcqueen2006, zhang2023} & \eqref{eq:mttc} \\
    \midrule
    & NCR reduction & share of the no-defence NCR that a defence removes & adapted from \citep{alavizadeh2022, sharma2025} & \eqref{eq:ncr-reduction} \\
     & NCR growth rate & rate at which NCR grows, read around a deployment & this thesis & \eqref{eq:ncr-growth} \\
    \multirow{-3}{1.9cm}{MTD effectiveness} & Time lost per MTD deployment & progress one deployment costs the attacker, in seconds at its own pace & this thesis & \eqref{eq:time-lost} \\
    \bottomrule
  \end{tabular}
\end{table}
```

Caption: 20 words, two sentences. The second sentence decodes the one piece of cell grammar that carries meaning: a bare citation against "adapted from" (house rule 3: "anything that does carry meaning ... is decoded").

**The lean fallback,** if Marc prefers no gloss: drop the Description column, widen Metric to 4.6 cm and Source to 4.0 cm, and keep the unheaded key (1.9 cm) and Equation (1.45 cm). That is 11.95 cm plus 30 pt, well inside `\textwidth`. It leaves lookup and provenance intact but keeps the "acronym table" look Marc objected to.

---

## Structure (the audit, questions 1–6)

### 1. Purpose, context, audience: the jobs, derived

| Reader, moment | Evidence the reader exists | Job the table must do | Column that does it |
|---|---|---|---|
| A chapter 5 reader at a float's column head (ASP, NCR, "MTTC (s)", "NCR reduction", "Attack rate (per 1 000 s)") | Six sentences send the reader to `tab:metrics`: `tab_5-2-1a` caption "The attack outcome and the attack rate (Table~\ref{tab:metrics})"; `tab_5-3-2d` "Metrics as Table~\ref{tab:metrics}"; `tab_F-1` ×2 "on the metrics of Table~\ref{tab:metrics}"; `tab_5-1a` l.116; §5.1 l.6353 "outlined in Table~\ref{tab:metrics}". Figures 5.1, 5.2 and 5.4 point to `sec:evaluation-metrics` instead. | **J1, lookup:** from a column head to the meaning, and from there to the exact definition | Metric (the same name and acronym as the floats) + Description + Equation |
| The examiner, first question per metric | Handoff, supervisor's questions: "Where is this metric from? → Table 4.3's Source column"; catalogue: "look me in the eye — this exists, or this doesn't and we are inventing it" | **J2, provenance:** adopted, adapted or introduced, at a glance | Source |
| A reader at the head of §4.5, before ten definitions | §4.5's opener placeholder: "three classes, one per question the results ask of the attacker; Table~\ref{tab:metrics} lists them" | **J3, overview:** which question each group of metrics answers, and what is coming | Key column (= subsection titles) + Description |
| A reader placing a metric on the field's map (Table 3.1) | literature_conventions §d; the 2026-09-18 comment's "tie-back" argument | **J4, the field's map.** A citation shared with a Table 3.1 row does this implicitly. An explicit column would be a second grouping that cuts across the three classes (ASP and NCR sit in different Table 3.1 rows but in the same class here). | none (Source carries it; handoff Open 2 adds the missing anchors to Table 3.1) |

**What does not belong** in the table: statistics (the ranking and ρ are computed across runs, so they are 4.5.4's, per the handoff's pitfalls table); results; direction; units as a column; symbols.

### 2. Convention: how the corpus presents its metric set

| Source | Table | Columns | Source column? |
|---|---|---|---|
| Zaffarano 2015 | Table 4 "MTD Effectiveness Metrics" | Metric, Description (8 metrics, paired mission/attack) | no |
| Ho 2024 | Table 3 "Metrics and Symbols" | Symbol, Description (symbols and metrics mixed; host $h_i$ beside `SCAN_PORT`) | no |
| Masud 2025 | Table 3 "Symbols, explanations, and formulas: a reference for the reader" | Symbols, Explanation, Formula (cells "Eq. (1)" …) | no |
| Hong 2018 | Tables 1–2 | Terms / Functions, Descriptions (symbols only; the metrics are in prose, §5.1–5.2) | no |
| Cho 2020 | none for metrics; bullets with bracketed references, and Figs. 6–8 | n/a | inline refs |
| He 2025, Zhang 2023, Alavizadeh 2022, Kim 2026, Sharma 2025 | none; prose lists | n/a | n/a |
| Pendleton 2016 (survey) | Table I | "Measuring what?", representatives (with inline citations), desirable metrics | inline citations |
| Masud 2025 Table 5; Kim 2026 Table 1 | comparison / mapping tables | "Ref." / "Ref(s)" column; own row "This paper*" | yes |

**Conclusion.**
- A summary table of the metrics is conventional (3 of the 10 primary papers), and each of them has a **description**.
- A **source** column is survey and comparison-table practice (Pendleton, Masud Table 5, Kim Table 1, the thesis's own Table 3.1). Importing it for provenance is defensible, because provenance is this table's distinctive job (J2) and register E3 demands it.
- A **formula or equation pointer** has one corpus precedent (Masud).
- No corpus table has a direction, unit or "read in" column.

### 3. Shape

- **Equation column.** Recommended. It does not turn the table into a symbols table, because each row is still a metric: the acronym stays in the name cell, as in Table 3.1, and no symbol column is added (seven of the ten metrics have no symbol).
  - It gives lookup a target to the equation: the run-in heads already match the names, but an equation number takes the reader to the exact place.
  - It makes the validation gate ("each of the ten has its equation") visible.
  - Cost: +1.45 cm. It prints "??" until the equations are uncommented.
- **Direction column.** Not recommended. The 2026-09-20 ruling "no paper in the corpus uses one" was **re-verified** by grepping the held sources for ↑, ↓, `\uparrow`, "higher is better" and "lower is better": no hits in `lit_review/`, `extractions/` or `methodology/`. The corpus states direction in the definition prose (Alavizadeh; He), which is template slot S4.
- **Unit column.** Not recommended. No corpus table has one. Seven of the ten metrics are shares. The attack rate's and time lost's units are in their glosses, and MTTC's is in chapter 5's header "MTTC (s)".
- **"Read in" column.** Not recommended. The floats already point back here, a ch4→ch5 pointer runs against the reading order and would need upkeep, and each class opener in §4.5 says which part of the results reads it.
- **§4.5 symbols table.** Recommendation: **drop it and use "where" clauses** at the owning definition. Reasons:
  1. "Where" clauses are the corpus's commonest form (the handoff template, S3).
  2. The brief already assigns every shared symbol an owner definition. Only $H_r$/$N$, $A_r$/$T_r$ and $t_d$ are used by more than one metric.
  3. Merging it into Table 4.3 would mix metric rows with symbol rows, which is Ho Table 3's jumble.
  4. Hong's precedent is a symbol table for 17 equations over 5 terms and 12 functions. Ten mostly single-use symbols do not earn a second float before §4.5's first sentence.
  5. `tab:gspn-notation` is chapter 4's symbols table and should stay the only one.

  This is Marc's call, because he OK'd a symbols table (see Open).
- **Status as its own column.** Not recommended. The three-state source grammar already carries it in one cell, and a separate column would cost 2 cm for a word the cell already says.

### 4. The word "Class"

| Candidate | Evidence | Verdict |
|---|---|---|
| none (unheaded key) | house rule 4: "The *outer* key is a `\rowgroup` in an unheaded first column (`c`; the header cell is empty)"; Table 3.1's Effectiveness/Efficiency groups are unheaded; the labels equal the §4.5.1–§4.5.3 titles | **recommended for the table** |
| category | He 2025 V-B: "These metrics are organized into three distinct categories: attack metrics, defense metrics, and diversity metrics", the same count and the same run-in-head structure; Pendleton §7: "the 4 categories systemized above" | **recommended if the opener's prose needs a noun** |
| type | Zhang 2023 §3.4: "two types of metrics: static metrics … and dynamic metrics" (a property of the metric, not a question it answers) | acceptable second |
| class | no hit for class of metrics / metric class in the held corpus (grep). The thesis already uses "class" for the formalism class (GSPN) and "APT attacker" as the ch3 class term (terminology.md l.45, l.47). Rodriguez's Table 3, cited in this very table, uses "class" for the *tactic* | reject: three senses already, none from the field |
| family | Table 3.1 is "Metric families in MTD evaluation", one row per quantity basis. ASP and NCR are different Table 3.1 families but the same group here | reject: collision |
| dimension | implies orthogonal axes (Cho's perspective × purpose, drawn as Table 3.1's rows × columns). These three are a partition | reject |

The opener can also avoid the noun altogether: "The metrics answer three questions of the attacker: what it does, what it achieves, and what a defence does to it (Table~\ref{tab:metrics})." The caption no longer says "by class".

### 5. Source cells: wording and table-level flags

- **"adapted from"** is general academic attribution wording. I found no verbatim instance in the held corpus. The corpus verb is "extend": Masud 2025 l.442, "We extend this metric to derive the comprehensive AC". I could not open a style-guide page to confirm it (the APA page fetch returned empty). Keep it.
- **"in the form of"**: no corpus use for metric provenance. It is a fourth state the table's own rule (2) does not define. Drop it (see NCR reduction below).
- **"introduced here"**: "here" is deictic inside a float (this table? this section?). Corpus equivalent: Masud Table 5's own row "This paper*". Use **"this thesis"**.
- Per-cell flags for the per-metric agents. These are table-level only; I did not verify them in depth.
  - *Relative tactic occurrence:* Rodriguez's "Occur. (rel.)" is a column of the ProM log summary (Table 3, l.358–370), not a metric Rodriguez names. The quantity holds; the name is ours.
  - *APV:* the catalogue's §(a) verdict for this quantity is still "**Does not exist**". The handoff ruled it "adapted" on 2026-09-24. Hong's APV compares available attack-path sets between network states (Eq. 1), so "adapted" holds only if §4.5 states that difference (convention §d2). Reconcile the catalogue row.
  - *Attack rate:* `zhan2013` is **not held** (paywalled, on the download list). Pendleton 2016, held, relays it: p. 15 "attack rate metric measures the number of attacks that arrive at a system of interest per unit time [Zhan et al. 2013; Zhan et al. 2015]". I added `pendleton2016` so the cell has one read source. It is in the bib but not yet cited, so its number will be new.
  - *NCR:* Ho's name is **HCR** (ho2024.md l.350, "Host Compromised Ratio (HCR)"). Zhang's is NCR (zhang2023.md l.420). Citing Ho bare on a row named NCR credits Ho with the name. Acceptable as "the same ratio", but the NCR agent should say so in the definition, or the cell should keep only zhang2023.
  - *MTTC:* Zhang reads MTTC at 0.8 NCR (zhang2023.md l.449, "Mean Time to Compromise on 0.8 NCR"). Here it is the first host. Under the caption's "a source cited alone defines the metric as it is used here", zhang2023 fails that test and McQueen passes ("the time to compromise a system component"). Either cite McQueen alone or write "adapted from" for Zhang. The MTTC agent decides.
  - *NCR reduction:* Alavizadeh's MF is **clamped**: "MF^m takes values within the range [0,1]" and is 0 "otherwise" (Eq. 13). NCR reduction can be negative. Sharma 2025's SRRP is unclamped, named a *reduction*, and has the same with/without form: "comparing the defended network to a baseline model without any MTD methods" (Eq. 17). Hence "adapted from alavizadeh2022, sharma2025"; NCR's own source is on the NCR row.

### 6. Caption

"The evaluation metrics, each with its source and the equation that defines it. A source cited alone defines the metric as it is used here." Short form: "The evaluation metrics". It decodes only the bare-versus-adapted grammar. Shading is not decoded (house rule 3) and the unheaded key needs no decode, as in Table 3.1.

**Length:** a 5-column, 10-row table, 277 pt tall (measured, t2.log) at 452.6 pt wide.

---

## Verification

| Claim | Source, locator | Verbatim quote | Verdict |
|---|---|---|---|
| Corpus metric tables carry a description | zaffarano2015.md l.331–333, Table 4 | "Table 4: MTD Eﬀectiveness Metrics / Metric Description" | holds |
| | ho2024.md l.320–322, Table 3 | "Table 3: Metrics and Symbols … \|**Symbol**\|**Description**\|" | holds |
| | 1_3_masud2025vulnerability.md l.258–263, Table 3 | "Symbols, explanations, and formulas: a reference for the reader. \|Symbols\|Explanation\|Formula\|" | holds |
| | 1_2_hong2018dynamic.md l.194–198, 204–206 | "Table 1 – Network and characteristics terms. \|Terms\|Descriptions\|" | holds (symbols, not metrics) |
| An equation-pointer column has a corpus precedent | masud2025 l.279 | "\|_𝐴𝑆 𝑃𝑉𝑖_\|Attack success probability associated with _𝑖𝑡ℎ_ \|Eq. (1)\|" | holds |
| A house precedent for a pointer column | dissertation.tex l.4667–4669, `tab:gspn-notation` | "Symbol & Meaning & Declared in" | holds |
| Mixing symbols and metrics reads as a jumble | ho2024.md l.324 | the Symbol cell runs "_hi_ … _Ct_ … _Thost_ … `SCAN`~~`P`~~`ORT`" in one table | holds (my reading) |
| Source columns are survey and comparison practice | pendleton2016 l.1079–1081, Table I | "Summary of the taxonomy, the representative examples of security metrics … Measuring what?" | holds |
| | masud2025 l.636–642, Table 5 | "Comparison of MTD papers … \|Ref.\|… \|This paper*\|" | holds |
| | 3_2_kim2026mtdid.md l.161–165, Table 1 | "\|MTD\|Model\|Layer\|Digital Artifact(s)\|Attack(s)\|MTD sub-technique(s)\|Ref(s)\|" | holds |
| Cho presents metrics as bullets with references, not a table | 1_1_cho2020toward.md l.572, 580 | "**Attack success probability (ASP)** [3], [11], [22] … This metric refers to the probability that attacks are successfully performed." | holds |
| No direction marks in the corpus | grep of `lit_review/`, `extractions/`, `methodology/` for ↑, ↓, `\uparrow`, `\downarrow`, "higher is better", "lower is better" | no hits (only unrelated "(lower" in lee2015, Attack Flow capitalisation) | holds |
| Direction is stated in the prose | alavizadeh2022.md l.599–601 | "Note that, a larger value of MFm is more desirable." | holds |
| | 3_2_he2025MTD-AD.md l.237 | "for defense, ADR should be as high as possible" | holds |
| "Category" is the corpus word for this structure | 3_2_he2025MTD-AD.md l.227 | "These metrics are organized into three distinct categories: attack metrics, defense metrics, and diversity metrics." | holds |
| | pendleton2016 l.1057 | "we discuss the 4 categories systemized above" | holds |
| "Type" | zhang2023.md l.246 | "This evaluation involves two types of metrics: static metrics … and dynamic metrics" | holds |
| No corpus use of "class" for a group of metrics | grep of `lit_review`/`methodology`/`extractions` for metric class, class of metric, categor* of metric, metric famil*, types of metric | only "types of metrics" (Cho l.613, 646; Zhang l.246) and Hong's "metric family" in our own extraction | holds |
| Rodriguez uses "class" for the tactic | 2_4_rodriguez2024process.md l.367 | "\|**class**\|**Occur. (abs.)**\|**Occur. (rel.)**\|" | holds |
| House rule: the outer key column is unheaded | docs/workflows/figure_table_conventions.md §k rule 4 | "The *outer* key is a `\rowgroup` in an unheaded first column (`c`; the header cell is empty)" | holds |
| Table 3.1's group key is unheaded | dissertation.tex l.2692–2694 | "& Measures & Attacker-side & Defender-side \\" (first cell empty) | holds |
| "This paper" is the corpus's self-attribution in a table | masud2025 l.642 | "\|This paper*\|S, D, R\|✓\|" | holds |
| Corpus verb for adapting a metric | masud2025 l.442 | "We extend this metric to derive the comprehensive AC" | holds |
| Ho names the ratio HCR, not NCR | ho2024.md l.350 | "4) Host Compromised Ratio (HCR): The ratio of hosts that are compromised in the system." | holds (flag) |
| Zhang names NCR | zhang2023.md l.420 | "NCR is the ratio of compromised hosts to the total number of hosts in the network." | holds |
| Zhang's MTTC checkpoint is 0.8 NCR | zhang2023.md l.449 | "Figure 8: Single MTD Evaluation - Mean Time to Compromise on 0.8 NCR" | holds (flag) |
| McQueen's TTC is per component | tactic_profiles/step_c/mcqueen2006_time_to_compromise.md l.51–52 | "a new model for estimating the time to compromise a system component that is visible to an attacker" | holds |
| Alavizadeh's MF is clamped to [0,1] | alavizadeh2022.md l.597–603 | "MFm takes values within the range [0,1] as in Equation 13 … 0, otherwise" | holds (flag) |
| Sharma's reduction is unclamped and uses a no-MTD baseline | sharma2025.md l.365–366, 383–386 | "comparing the defended network to a baseline model without any MTD methods"; "SRRP(hi) = … ×100%=(1− … no−mtd …) ×100%. (17)" | holds |
| Pendleton relays Zhan's attack rate | pendleton2016 p.15 (l.770–772) | "Another related attack rate metric measures the number of attacks that arrive at a system of interest per unit time [Zhan et al. 2013; Zhan et al. 2015]. These metrics reflect the aggressiveness of cyber attacks." | holds |
| Rodriguez's relative occurrence | rodriguez2024 l.358, 367–368 | "Table 3. Log Summary (ProM) … \|execution\|3270\|45.01%\|" | holds (the quantity; the name is ours) |
| Zaffarano's attack confidentiality | zaffarano2015.md Table 4 | "Attack Conﬁdentiality is a measure of how much attacker activity may be visible by detection mechanisms" | holds |
| Chapter 5 floats use Table 4.3 for lookup | tables/tab_5-2-1a l.8; tab_5-3-2d l.7; tab_F-1_* l.5; tab_5-1a l.116; dissertation.tex l.6353 | e.g. "Metrics as Table~\ref{tab:metrics}" | holds |
| Floats use the acronyms and units in their heads | tab_5-2-1a l.8 | "Attacker & ASP & NCR & MTTC (s) & Attack rate (per 1\,000\,s)" | holds |
| The run-in heads match the table's names | dissertation.tex §4.5 `\paragraph{}` heads (ten, l.~5437–5567) | "\paragraph{NCR reduction.}" etc. | holds |
| The table fits `\textwidth` | scratchpad `tabtest/t2.log` | "TABWIDTH=452.56448pt"; "TEXTWIDTH=455.24411pt"; no overfull after the header fix | holds |
| Rotated labels would not fit | `tabtest/t3.png`; t2.log | "ROT-AB=82.87573pt" against 3–4-row groups (the render shows the labels overrunning) | holds (confirms Marc's 2026-09-24 ruling) |

**Code check.** Not applicable: the table carries no equation. The glosses were written from the handoff's entries and must match each drafter's final S2 sentence (see For elsewhere).

**Status check.**
- Adopted, adapted and introduced are honest per cell except for the flagged cells: MTTC's zhang2023 under "cited alone", NCR's ho2024 name, APV against the catalogue's "does not exist", and attack rate's unread `zhan2013`.
- The "introduced" pair, NCR growth rate and time lost, has no field precedent in the catalogue. The catalogue has no row for NCR growth rate itself; a derivative of NCR over time is close to Cheng 2014's CHP "at time t" (census F). The growth-rate agent should check that before "this thesis" stands.

---

## Symbols

- **Table 4.3 introduces no symbols.** $k$ was deliberately taken out of the APV gloss so that no symbol appears before its definition. The only mathematics is `\eqref`.
- **Collisions spotted for the other agents:**
  - The handoff's time-lost entry writes the NCR growth rate as **$r(t)$**, but the shared notation reserves **$r$ for a run** (so $H_r$, $A_r$, $T_r$). The growth-rate and time-lost agents need another letter, or a subscript form.
  - Chapter 4 also writes $\mathcal{R}$ (runs of a cell) near $R$ (the rule kernel, `tab:gspn-notation`). They are distinct glyphs but close.
  - The handoff's $H(t)$ (hosts by time $t$) sits beside $H_r$ (a set of hosts).

---

## For elsewhere

- **§4.5 opener:** if a noun is needed, "category" (He 2025), or no noun at all (see §4 above). The current placeholder says "three classes", so change it.
- **Every drafter:** the Description cell is a compressed S2. Once the definitions are drafted, re-read each gloss against its S2 so the table and the text agree (validation gate: "Table 5.2's Source column and §4.5 agree"). If a drafter changes status (for example MTTC to adapted, or APV to introduced), the Source cell follows.
- **Attack rate agent:** add `pendleton2016` at the name (held; p. 15). `zhan2013` stays "to download".
- **NCR reduction agent:** state the one difference from Alavizadeh (unclamped: it can be negative) and cite Sharma's SRRP as the unclamped *reduction* precedent.
- **NCR growth rate / time lost agents:** the $r$ collision above. The gloss says "rate at which NCR grows, read around a deployment": keep "live time" versus "active time" consistent with the attack rate's "active time".
- **Chapter 5:** `tab_5-3-2d`'s caption points the ranking to `sec:evaluation-metrics`. It should point to `subsec:metrics-statistics` (4.5.4). `tables/tab_5-3-1a_conditions.tex` still has an "Attack actions blocked" column, but it is no longer `\input`: stale file only.
- **Catalogue:** reconcile §(a)'s "Does not exist" row for the opening-variety quantity with the 2026-09-24 "APV, adapted" ruling.

---

## Open for Marc

1. **Restore a Description column** (a gloss, not a definition), overturning the 2026-09-24 removal. **Recommend yes:** every corpus metric table has one, and it is what stops the table reading as an acronym list.
2. **Add the Equation column.** **Recommend yes** (Masud's Formula column; `tab:gspn-notation`'s Declared in). It is the first thing to drop if you want the table lean.
3. **Remove the "Class" header** (unheaded key, as in Table 3.1). If prose needs a noun, **recommend "category"** (He 2025), not "class".
4. **The §4.5 symbols table** you OK'd. **Recommend dropping it** for "where" clauses at each owner definition; ten mostly single-use symbols do not earn a second float.
5. **MTTC source cell.** **Recommend `mcqueen2006` alone** under "cited alone", with Zhang's 0.8 NCR checkpoint named in the definition. The alternative is "adapted from" for Zhang.
6. **NCR reduction source.** **Recommend "adapted from alavizadeh2022, sharma2025"** in place of "…, in the form of …".
7. **Zhan 2013** (TIFS, paywalled): still **to download**. Until then the attack-rate cell leans on Pendleton's relay.
