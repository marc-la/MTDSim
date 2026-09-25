# Shared brief: drafting one part of §4.5 *Evaluation metrics* (2026-09-25)

You are one of eleven drafting agents, plus one table auditor. Each drafter writes one definition (or 4.5.4) of §4.5 in Marc Labouchardiere's honours thesis. The thesis evaluates moving target defences (MTD) in MTDSim, against an APT attacker model built as a generalised stochastic Petri net.

Marc's instruction:
- Meticulously assemble the best structure for your definition, which already exists as a template.
- Verify the sources and adaptations: authenticate and scrutinise, as a supervisor would expect to see them.
- Draft tight and crisp, keeping purpose, context and audience in mind.
- Use the standard terms and chapter 4's formalism, with maths where it is needed (e.g. a growth rate is a derivative).
- New symbols are allowed only if conventional and strictly defensible.
- **The primary goal is to be strictly conventional and defensible.**

## Hard rules

- **Do not edit any repository file.** Other sessions are editing the same files. Write only your own output file, at the path your prompt gives. Read anything.
- **Open-access sources only.** You may fetch open-access or arXiv sources to verify a claim. A paywalled source you could not read goes under "Open for Marc" as "to download". Never cite from memory: every source claim carries a locator and a verbatim quote from the text you read.
- **The markdown in `docs/sources/` is the authoritative citable text** (gitignored but present). `docs/sources/extractions/mtd_metric_catalogue.md` is the evidence catalogue for every metric.

## Read first, in this order

1. `docs/handoffs/2026-09-24_s45_instrumenting_mtdsim.md`, **the whole file**. Read in particular:
   - "Start here": the structure, the template S1–S6, the length budget, Marc's calls, the pitfalls table, the 4.5.4 content points;
   - "What each definition must carry";
   - "Symbols";
   - **your entry** under "The ten entries";
   - "Open".
2. `docs/thesis/dissertation.tex`:
   - l.4411–4785, §4.3 *Generalised stochastic Petri-net formalism*, including `tab:gspn-notation` (~l.4664). These are the symbols you must reuse and must not collide with.
   - l.4785–5363, §4.4 *Integration with MTDSim*. This gives the vocabulary a reader has met by §4.5: action, verb, precondition, interrupt, verdict, dwell, deployment.
   - l.5363–~5640, §4.5 as it stands. Your `\paragraph{}` head, placeholder and the commented S1–S6 slots and DRAFT equation are there. Use the label it proposes.
   - `docs/thesis/tables/tab_4-5a_metrics.tex`, Table 4.3 (the metrics table) and its comment history.
   - l.6096 onwards, chapter 5's §5.1 *Experimental setup* and the floats that read your metric. Grep its name to see exactly how chapter 5 uses it, because your definition must license every such use.
3. `docs/workflows/voice.md`. **This is a hard gate for thesis prose; obey it.** Also read:
   - `docs/workflows/literature_conventions.md` §d (define every metric in the method; a field name is never reused with a changed meaning silently);
   - `docs/workflows/terminology.md`;
   - `docs/workflows/academic_register.md`.
4. The code that computes your metric. **The equation must describe what the code computes.** If they mismatch, that is a finding, reported and never papered over. The code is at:
   - `data/results/ch5_defended/analyse.py`;
   - `src/mtdsim/l3_simulation/movement/measures.py`;
   - `data/results/ch5_defended/disruption.py`;
   - `data/results/ch5_defended/sk_esd.py`;
   - `data/results/ch5_defended/numbers.json`.

   You may run small read-only Python checks. Do not re-run the corpus or `analyse.py`.

## Standing style rules (Marc's rulings)

- **Australian English.** Examples: behaviour, defence, analyse.
- **No invented terms or acronyms.** Every term is on a needs basis. An introduced name says what it does. The field's names and acronyms are used as the field uses them: ASP, NCR, MTTC, APV. Attack rate and attack confidentiality have none.
- **Dense over walked-through.** One idea per sentence, the subject named outright, no inference chains spelled out.
- **No "not X but Y" formula.** Openers have one main clause, no brackets, authority first.
- **Brackets over em-dashes** in prose.
- **No statistics and no results in a definition.** The one exception is a worked value where the reading is not intuitive. Intervals, ranking and ρ are 4.5.4's.
- **Say "the simulator" or "MTDSim", never "substrate".** Say "APT attacker model" and "baseline attacker".
- **Measurement is not attribution.** Bound every stealth or detection claim to the declared detector.
- **Length budget:**
  - adopted: 2–4 sentences, about 40–80 words;
  - adapted: the same, plus one clause saying what differs and why;
  - introduced: 8–15 sentences.
  - **Tighter is better.**

## Shared notation (all agents use these; do not redefine them)

Chapter 4's symbols are reserved (`tab:gspn-notation`): $c$, $\mathcal{N}_c$, $p$, $\hat p$, $\tau_p$, $t_{pq}$, $\mu_p$, $w_c$, $\sigma$, $M_0$, $v\in V$, $F_v$, $\varphi$, $R$, $d$, $\gamma$, $\delta$, $z$. **$\tau$ is taken, so the detector's memory is $\kappa$.**

§4.5's shared symbols (from the brief's proposal):

| Symbol | Meaning |
|---|---|
| $r$ | a run |
| $\mathcal{R}$ | the runs of one cell (one attacker, one condition, one interval) |
| $N$ | the network's hosts ($N = 50$) |
| $H_r$ | the hosts run $r$ compromises |
| $A_r = (a_1, a_2, \dots)$ | the start times of run $r$'s actions |
| $T_r$ | run $r$'s active time |
| $k$ | the opening length |
| $\kappa$ | the detector's memory |
| $\theta$ | the alarm level |
| $t_d$ | the moment a deployment completes |

If you need another symbol:
- grep the tex to confirm it is free;
- prefer the field's own symbol, taken from your source;
- list it under "Symbols" with the reason.

**Who defines a shared term** (define yours; assume the earlier ones are defined):
- **Step:** relative tactic occurrence.
- **Opening of length $k$:** APV.
- **Action** (a verb that runs on the network, once for both stealth metrics) and **active time $T_r$:** attack rate.
- **Detector and alarm level:** attack confidentiality.
- **Target:** ASP.
- **$H_r$ and $N$:** NCR.
- **The first compromise:** MTTC.
- **The no-defence reference:** NCR reduction.
- **The NCR curve:** NCR growth rate.
- Time lost uses the growth rate.
- The unit, intervals, ranking and ρ: 4.5.4.

## Your output file (markdown, these sections in order)

1. **`## LaTeX`**. The drop-in block:
   - starts with the `\paragraph{...}` head as in the tex, or `\subsection` content for 4.5.4;
   - carries the prose and the numbered equation(s) with the proposed `\label`s;
   - uses real `\citep`/`\citet` keys from `docs/thesis/references.bib`. A missing key goes in Open, with the full reference found.

   Then the word count.
2. **`## Structure`**. Which template slots you used, any you merged or dropped and why, and your length against the budget.
3. **`## Verification`**. A table with one row per claim:
   - the claim;
   - the source file and locator (page, equation, section);
   - a **verbatim quote**;
   - the verdict (holds / partly / fails).

   Then the code check, as file:line against each term of your equation, verdict matches/mismatches. Then the status check: is "adopted / adapted / introduced" honest, and is the name used as the source uses it?
4. **`## Symbols`**. Those used, any new ones proposed, and a collision check (grep evidence).
5. **`## For elsewhere`**. What your definition needs said in the §4.5 opener, in 4.5.4, in Table 4.3 (source cell) or in chapter 5, and any mismatch with chapter 5's current use.
6. **`## Open for Marc`**. Only decisions that are his. Each gets a recommendation, one line each.

Then **return a summary of at most 150 words**: the verdict on sources, any code mismatch, and the open calls.
