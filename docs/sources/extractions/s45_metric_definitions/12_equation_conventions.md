# Conventions and pitfalls for defining metrics with displayed equations

Research record, 2026-09-29. Read-only: no repo file was edited. Every quote below was read from a fetched copy or from the repo's held markdown in this session. Local copies of the fetched texts are in `docs/sources/s45_fetched/conv/` (gitignored).

## Sources read (open access, fetched this session)

| Key | Source | Copy read |
|---|---|---|
| KNUTH | D. E. Knuth, T. Larrabee, P. M. Roberts, *Mathematical Writing*, Stanford STAN-CS-88-1193 (1989); also MAA Notes 14 | https://jmlr.csail.mit.edu/reviewing-papers/knuth_mathematical_writing.pdf (text-checked). The official scan is at http://i.stanford.edu/pub/cstr/reports/cs/tr/88/1193/CS-TR-88-1193.pdf (downloaded, 65 MB, not text-checked). **The brief's arXiv ID 2010.15924 is wrong**: that ID is Çano & Bojar, "How Many Pages? Paper Length Prediction from the Metadata". Do not cite it. |
| HALMOS | P. R. Halmos, "How to write mathematics", *L'Enseignement Math.* 16 (1970) 123–152; reprinted in *How to Write Mathematics*, AMS 1973, pp. 19–48 | A retypeset open copy: https://entropiesschool.sciencesconf.org/data/How_to_Write_Mathematics.pdf. **Its page numbers are not the journal's**, so the locators below use Halmos's own section numbers (§1–§21). |
| MERMIN | N. D. Mermin, "What's wrong with these equations?", *Physics Today* 42(10):9–11, Oct 1989 | A scan of the printed article: https://wp.optics.arizona.edu/kupinski/wp-content/uploads/sites/91/2023/05/MerminEquations.pdf (the second scanned page carries the folio "11"). |
| ISO15939 | ISO/IEC/IEEE 15939:2017, *Measurement process*, clause 3 (terms) | The official iTeh preview, clauses 1–4 only: https://cdn.standards.iteh.ai/samples/71197/1c61ba3beaa343dda09217cc4c58844d/ISO-IEC-IEEE-15939-2017.pdf. **Annex A, the measurement information model, is not in the preview.** |
| SP811 | A. Thompson, B. N. Taylor, NIST SP 811 (2008 ed.), *Guide for the Use of the SI* | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication811e2008.pdf |
| SP800-55 | NIST SP 800-55v1 (Dec 2024), *Measurement Guide for Information Security, Vol. 1* | https://doi.org/10.6028/NIST.SP.800-55v1. SP 800-55r1 (2008), which has the older template in Table 2, was **withdrawn** on 2024-12-04, so cite v1. |
| NISTIR7564 | W. Jansen, NISTIR 7564, *Directions in Security Metrics Research* (2009) | https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir7564.pdf |
| KITCH | B. A. Kitchenham et al., "Preliminary guidelines for empirical research in software engineering", NRC/ERB-1082 (2001); published in IEEE TSE 28(8), 2002 | https://doi.org/10.4224/8914084 (the NRC archive copy). The page numbers below are the tech report's, not the TSE article's. |
| EMPSTD | ACM SIGSOFT Empirical Standards (Ralph et al.): the Simulation (Quantitative), Experiments and Optimization Studies standards | https://github.com/acmsigsoft/EmpiricalStandards/tree/master/docs/standards (the line numbers below are from the raw `.md` files) |
| ODD | V. Grimm et al., "The ODD protocol for describing agent-based and other simulation models: a second update", *JASSS* 23(2):7, 2020 | https://www.jasss.org/23/2/7.html (the locators are section headings) |

## To download (paywalled or no legitimate open copy; not quoted here)

- N. J. Higham, *Handbook of Writing for the Mathematical Sciences* (SIAM, 3rd ed. 2020). Its chapter on notation is the most direct source on multi-letter names and on "define symbols at first use".
- J. Zobel, *Writing for Computer Science* (Springer, 3rd ed. 2014), ch. 9 "Mathematics". The only open copies found were unauthorised mirrors (kashanu.ac.ir, slideshare), so I did not use them.
- C. Wohlin et al., *Experimentation in Software Engineering* (Springer 2012/2024). The chapter on threats to validity is ch. 8.
- B. Kitchenham, S. L. Pfleeger, N. Fenton, "Towards a framework for software measurement validation", IEEE TSE 21(12), 1995. This is the canonical entity/attribute/unit/scale framework.
- ISO/IEC/IEEE 15939:2017 in full, for Annex A (the measurement information model diagram and the base → derived → indicator worked examples).
- A. Arcuri, L. Briand, ICSE 2011 statistical-tests guide, and A. Arcuri, G. Fraser, EMSE 2013, "Parameter tuning or default values?". An open copy of the second exists at evosuite.org/wp-content/papercite-data/pdf/tuning13.pdf, but I did not fetch it and it is not quoted here. Both matter less to this problem than EMPSTD and ODD.

## Held MTD corpus: how these papers present metric equations

The paths are under `/home/marc/GitHub/MTDSim/docs/sources/lit_review/`. Ho 2024 and Zhang 2023 are UWA GENG5512 reports supervised by J. B. Hong. Hong 2018 is the supervisor's own paper, so its style is the nearest thing to a house style.

| Paper | Named metric or Greek letter? | Symbols defined right after the equation? | Symbol table? | Worked example? | Range, direction, degenerate case? |
|---|---|---|---|---|---|
| hong2018 (`1_2_hong2018dynamic.md`) | Named acronyms used as the left-hand side (APV, APN, APE, ACE, ACD, NVC, NVDT, EVC, EVT) | Partly. The sets and functions are defined up front in Tables 1–2 (l.194, l.204), and the display is introduced by prose ("Here, *AP_i* represents the set of attack paths found in the *i*th network state", l.233) | Yes, Tables 1–2 | Yes. §5.3 runs one example SDN through every metric: "The APV value 0.6667 represents the expected proportion of changes to the set of attack paths" (l.408) | Normalised: "transformed into the range [0, 1]" (l.303). Direction: "Lower APV value means the set of attack paths tends to be more static" (l.408). Boundary: "If the number of attack paths stays the same, then it equates to value 1. But if the previous network state had no attack paths, then it equates to 0" (l.253). **Pitfalls:** several acronyms are never expanded ("Eq. (5) shows the computation of APN metric", l.267; see also `extractions/metric_census/A_hong.md` l.33–45). Sum indices start at *i* = 0 in Eqs. 6, 8 and 9 but at *i* = 1 in Eqs. 2 and 5 (l.279, 299, 310 against l.243, 270). In Table 2 the index *i* means both a network state, *t*(*s_i*), and a path, *t*(*ap_i*). |
| ho2024 (`ho2024.md`) | Named metric with acronym, e.g. "Time Since Last MTD (TSLM) = Timenow − TimeLME" (l.380) | Yes, in a `where` clause after each display: "where *Ct* is the number of compromised hosts at time *t* and *Thost* is the total number of hosts in the network" (l.354) | Yes: "Table 3: Metrics and Symbols" (l.320) | No | Degenerate cases are stated: "If no compromised hosts are recorded, the attack success rate is zero" (l.364); "If no attack events are present, the MTTC is set to zero" (l.376). Range: NAV "takes values in the range [0, 1]" (l.400). **Pitfalls:** TimeLME is defined wrongly ("the time since last MTD is executed", l.382; it should be the time *at which* the last MTD executed). The zero-if-empty convention gives MTTC the value "zero" for "never compromised". |
| masud2025 (`1_3_masud2025vulnerability.md`) | Named acronyms (ASP, AC, AR, RoA) | No. The equations sit inside Algorithm 2 (l.412–424), and each §3.5.x section describes the inputs in prose | Yes: "Table 3 Symbols, explanations, and formulas: a reference for the reader" (l.258). Parameters are in "Table 4 System parameters and initial VM security metrics" (l.307) | Yes, for the model rather than the metrics: "we break it down into four specific definitions, providing illustrative solutions" (l.335) | Direction: "A higher RoA number means that attackers are more likely to take advantage of weaknesses" (l.446). **Pitfalls:** the same metric carries two names (Table 3 has "RoC", l.289; §3.5.4 has "RoA", l.446; Table 3 has "R" where the prose has "AR"). The prose "ratio between how much an attack costs and the benefit it provides" (l.446) inverts the computed *R*/*AC* (l.420). |
| zaffarano2015 (`zaffarano2015.md`) | Word-named functions: "Productivity(M,ν) = 1/\|T\| Σ_{τ∈T} ν(τ,duration)" (l.318), with Success and Confidentiality the same template over another attribute (l.385) | Yes. The template is defined once ("the average of the duration attribute over the tasks in M", l.315–317) and reused | No (Table 4 is descriptions only) | No | Range: "real-valued numbers in the range [0,1]" (l.383). Direction: "decreased duration is typically a good result for mission tasks, and … increased duration of attacker tasks is typically a good result from a defensive standpoint" (l.360–362). Aggregation caveat: "the arithmetic mean of duration may not be the single best indicator of task time: a single outlier could change the average" (l.363–365). Data kept apart from metric: "a clean distinction between the data that we collect (that is, the task attributes), and the metrics that we define based on this data" (l.369). |
| zhang2023 (`zhang2023.md`) | Symbolic (*TA*exploit, µ); MTTC is named but not given an equation | Partly. Displays are introduced in prose before the equation ("The formula to calculate the time duration of Phase 2 *TA*phase2 is shown in Equation 2", l.394) | No | No | Parameter basis stated: "The parameter µ is the historical average elapsed time, which can be determined via empirical study and sensitivity analysis" (l.410) |
| cho2020 (`1_1_cho2020toward.md`) | Survey. It names metrics with acronyms (ASP, MTTC, DSP) and gives **no equations** | n/a | n/a | n/a | "no standard metrics have been proposed to measure their effectiveness and efficiency" (l.568). Direction is stated per metric: ASP is "a dominant metric … aiming to minimize this metric" (l.636). |

The equation images in ho2024 and zhang2023 were dropped in extraction ("picture intentionally omitted"), so only the surrounding prose is quotable from the markdown.

**Domain pattern.** The MTD papers use **named multi-letter metrics** (acronym on the left-hand side), a **symbol table**, and a **`where` clause** after the display. The better ones also state the **range, the direction and the empty case**. Hong 2018 is the only one with a **running worked example**.

---

## Conventions and pitfalls

Each entry gives (a) the rule, (b) the evidence, and (c) whether it is a hard convention or a stylistic preference.

### A. Symbols: fewer, defined, consistent

**1.** (a) Define every symbol when it is introduced, at the display or in the sentence right after it.
(b) KNUTH §1 rule 11, p. 2: "All variables must be defined, at least informally, when they are first introduced." In the corpus: ho2024 l.354 and hong2018 l.233 (see the table).
(c) **Hard.** Every guide and every well-formed paper in the corpus does this.

**2.** (a) Don't use a symbol you don't need. A symbol used once should be a word.
(b) HALMOS §16 "Resist symbols": "The best notation is no notation; whenever it is possible to avoid the use of a complicated alphabetic apparatus, avoid it." Also: "avoid the use of irrelevant symbols. Example: 'On a compact space every real-valued continuous function *f* is bounded.' What does the symbol '*f*' contribute to the clarity of that statement?"
(c) Stylistic, but every source agrees on it. This is the cure for per-metric letters such as λ, θ and κ that appear once.

**3.** (a) Replace logical and set-builder shorthand with words when the idea is simple.
(b) KNUTH rule 3, p. 1: "Don't use the symbols . . . , ⇒, ∀, ∃, ∋; replace them by the corresponding words. (Except in works on logic, of course.)" KNUTH rule 26, p. 5 sets the Linderholm "Bad" example (∃ n₀ ∀ p …) against the "Better" prose statement of the fundamental theorem of arithmetic.
(c) Stylistic in CS, near-hard in expository mathematics. It directly covers "set-builder notation for simple ideas".

**4.** (a) The prose must carry the metric's meaning on its own. An equation the reader can skip without losing the argument is a check on the prose, not a replacement for it.
(b) KNUTH rule 13, p. 3: "Many readers will skim over formulas on their first reading of your exposition. Therefore, your sentences should flow smoothly when all but the simplest formulas are replaced by 'blah' or some other grunting noise." KNUTH rule 10, p. 2: "Don't use the style of homework papers, in which a sequence of formulas is merely listed. Tie the concepts together with a running commentary."
(c) Hard, as a writing standard. This is the direct diagnostic for equations that "read as decoration".

**5.** (a) Test whether each equation is needed at all. If no short phrase can say what it is, drop it or restructure.
(b) MERMIN p. 11: "If the nature of the equation is inherently uncharacterizable in a compact phrase, is the cross-reference really necessary? Indeed, is the equation itself essential? … If so, drop it."
(c) Stylistic.

**6.** (a) Use one notation per thing and one thing per notation, with consistent index letters.
(b) KNUTH rule 14, p. 3: "Don't use the same notation for two different things. Conversely, use consistent notation for the same thing when it appears in several places. For example, don't say '*A_j* for 1 ≤ *j* ≤ *n*' in one place and '*A_k* for 1 ≤ *k* ≤ *n*' in another place unless there is a good reason." Also: "Typographic conventions (like lowercase letters for elements of sets and uppercase for sets) are also useful." HALMOS §17: "it is good to use a symbol so consistently that its verbal translation is always the same."
(c) **Hard.** The corpus shows the failure: masud2025 names one metric both RoA and RoC; hong2018 uses *i* for both a state and a path, and starts its sums at *i* = 0 in some equations and *i* = 1 in others. Borrowing a symbol from another section is safe only if it means exactly the same thing there. Otherwise rename it.

**7.** (a) Design the symbol set once, before writing, and keep it small. A reader can hold far fewer symbols than an author can coin. Avoid labels that do not suggest what they stand for.
(b) HALMOS §6 "Think about the alphabet": "a human being's ability to distinguish between symbols is very much more limited than his ability to conceive of new ones". He calls "matrices with 'property L'" "a frozen and unsuggestive designation", and says "ad hoc decisions about notation, make mid-sentence in the heat of composition, are almost certain to result in bad notation."
(c) Stylistic. It argues against a new Greek letter for each metric, and for a small shared set of base symbols.

**8.** (a) Don't index what needn't be indexed, and avoid subscripted subscripts.
(b) KNUTH rule 15, p. 3: "Don't get carried away by subscripts, especially when dealing with a set that doesn't need to be indexed … Don't name the elements of X unless necessary."
(c) Stylistic.

**9.** (a) Put qualifiers on the quantity as a descriptive subscript, never on the unit. Set descriptive subscripts upright (roman).
(b) SP811 §7.4, p. 16: "it is incorrect to attach letters or other symbols to the unit in order to provide information about the quantity … Example: *V*max = 1000 V but not: *V* = 1000 Vmax." SP811 §10.2, p. 34: "a subscript or superscript on a quantity symbol is in roman type if it is descriptive … but it is in italic type if it represents a quantity, or is a variable … or an index".
(c) **Hard in metrology and physics**, and good practice in CS. It supports writing *t*_window = 1 000 s rather than an unexplained "1 000 s" inside a formula.

**10.** (a) Multi-letter metric names are a real **tension between conventions**. Pick one policy, state it, and expand every acronym at first use.
(b) Against: SP811 §10.1.1, p. 33: "The use of words, acronyms, or other ad hoc groups of letters as quantity symbols should be avoided by NIST authors. For example, use the quantity symbol *Z*m for mechanical impedance, not MI." For: all five MTD papers with equations put a named acronym on the left-hand side (hong2018 APV/APE/…; ho2024 TSLM; masud2025 ASP/AC/RoA; zaffarano2015 "Productivity(M,ν)").
(c) SP811's rule is a physics convention. The **domain convention in MTD/security is named acronyms**, and the supervisor's own paper uses them. The pitfall both sides agree on is the unexpanded acronym (hong2018: "Eq. (5) shows the computation of APN metric", l.267, with APN never spelled out). Typesetting a multi-letter name upright, so that MTTC is not read as M·T·T·C, is common LaTeX practice. **No fetched source states this**, so treat it as a recommendation and not a cited rule.

### B. Displayed equations as prose

**11.** (a) Number displayed equations, and be consistent about it.
(b) MERMIN p. 9, Rule 1 (Fisher's rule): "simply enjoins one to number all displayed equations. The most common violation … is the misguided practice of numbering only those displayed equations to which the text subsequently refers back." KNUTH rule 16, p. 3 is milder: "Display important formulas on a line by themselves. If you need to refer to some of these formulas from remote parts of the text, give reference numbers to all of the most important ones, even if they aren't referenced."
(c) Stylistic. The two authorities differ on number-all versus number-the-important. Either is defensible if applied uniformly.

**12.** (a) When referring back to an equation or a symbol from another section, name it in words as well as by number.
(b) MERMIN p. 9, Rule 2 (Good Samaritan rule): "When referring to an equation identify it by a phrase as well as a number." His example: "inserting the form (2.47) of the electric field E and the Lindhard form (3.51) of the dielectric function e into the constitutive equation (5.13)", not "inserting (2.47) and (3.51) into (5.13)".
(c) Stylistic, but strong. This is the remedy for notation borrowed from another section.

**13.** (a) Punctuate a displayed equation as part of its sentence, with no colon before it and a comma or full stop after it. Don't start a sentence with a symbol.
(b) MERMIN p. 11, Rule 3 (Math Is Prose): "End a displayed equation with a punctuation mark." HALMOS §17: "punctuate symbolic sentences just as would verbal ones … never start a sentence with a symbol." KNUTH rule 23, p. 4 shows the pattern "…of 'nonincreasing' vectors: *A_n* = … (1)" and says "those colons are wrong". KNUTH rules 1–2, p. 1: "Symbols in different formulas must be separated by words" and "Don't start a sentence with a symbol."
(c) **Hard** in mathematical publishing.

### C. What a metric definition must state

**14.** (a) Define each measure fully: the entity it is about, the attribute, the unit, and the counting rule.
(b) KITCH DC1, p. 13: "Define all software measures fully, including the entity, attribute, unit and counting rules." Also: "we need to define measures carefully enough so that we can understand the differences in measurement". EMPSTD Experiments, l.35: "describes the dependent variable(s) and justifies how they are measured (including units, instruments)".
(c) **Hard** in empirical software engineering.

**15.** (a) Separate *base measures* (what is recorded per run) from *derived measures* (the functions of them). Define the base measures once, then give each metric as a function of them.
(b) ISO15939 cl. 3.3: "base measure: measure defined in terms of an attribute and the method for quantifying it. Note 1 to entry: A base measure is functionally independent of other measures." Cl. 3.8: "derived measure: measure that is defined as a function of two or more values of base measures". Cl. 3.20: "measurement function: algorithm or calculation performed to combine two or more base measures". Cl. 3.7: "decision criteria: thresholds, targets, or patterns used to determine the need for action or further investigation". ZAFFARANO l.369 draws the same line in the MTD literature ("a clean distinction between the data that we collect … and the metrics that we define based on this data") and gives the benefit: "it may not be necessary to rerun tests, but rather only to compute new values from the data".
(c) **Hard** as standard vocabulary (ISO), and a strong structural convention. It is the most useful single idea for a ten-metric section: a few shared base measures (e.g. the time of each compromise, each MTD firing) plus ten short measurement functions, in place of ten self-contained equations.

**16.** (a) State the scale type and the range.
(b) ISO15939 cl. 3.34: "scale: ordered set of values, continuous or discrete, or a set of categories to which the attribute is mapped". It lists nominal, ordinal, interval and ratio, the last being where "the value of zero corresponds to none of the attribute". Corpus: zaffarano2015 l.383 "real-valued numbers in the range [0,1]"; ho2024 l.400 NAV "takes values in the range [0, 1]"; hong2018 l.303 "transformed into the range [0, 1]".
(c) Hard (ISO), and the domain norm.

**17.** (a) State the direction: which way is better, and for whom (attacker or defender).
(b) ZAFFARANO l.360–362 (quoted in the table). hong2018 l.408: "Lower APV value means the set of attack paths tends to be more static". masud2025 l.446: "A higher RoA number means that attackers are more likely to take advantage of weaknesses". cho2020 l.636: "aiming to minimize this metric".
(c) The domain norm. Every MTD paper in the corpus does it for at least some metrics.

**18.** (a) State what the metric is when its event never happens (the empty or censored case), and make sure that value cannot be confused with a real one.
(b) ho2024 l.364 and l.376: "If no attack events are present, the MTTC is set to zero". hong2018 l.253: "if the previous network state had no attack paths, then it equates to 0".
(c) Stating the empty case is the domain norm. **Pitfall:** Ho's "set to zero" makes "never compromised" read as "compromised instantly". Choose a value that cannot be mistaken (undefined, censored at the window, or reported as a separate count).

**19.** (a) Justify the choice of aggregation (mean, median, proportion), or at least name its known weakness.
(b) ZAFFARANO l.363–365: "we recognize that the arithmetic mean of duration may not be the single best indicator of task time: a single outlier could change the average task time significantly".
(c) Stylistic.

**20.** (a) Record a metric as separate fields (statement, formula, target/threshold, unit, data source) rather than as a formula alone. Phrase the statement as a numeric noun phrase.
(b) SP800-55 §3.1.1, pp. 12–13: "Measure: Statement of measurement. Use a numeric statement that begins with the words 'percentage,' 'number,' 'frequency,' 'average,' or other similar term." "Formula: Calculation that results in a numeric expression of a measure." "Target: A range or a designated upper or lower bound." SP800-55 §3.2, p. 17: "Unit-based standardization: Data that is expressed using standardized units and formats."
(c) Hard within NIST security-measurement practice, and a stylistic template for a thesis. The "numeric statement" rule is a cheap test: each metric should open with "the number of…", "the proportion of…" or "the mean time from…".

**21.** (a) State units, and make the measurement method explicit. Security metrics are known to be weak on exactly this.
(b) NISTIR7564 p. 3: "the method of measurement well defined, including details of how specific factors are to be measured or assessed and explanations of sources of uncertainty." NISTIR7564 p. 4: "the concepts of fundamental units, scales, and uncertainty prevalent in scientific metrics have not traditionally been applied to IT or have been applied less rigorously." SP811 §7.11, p. 21: a quantity equation "is independent of the units used … it is incorrect to associate the equation with a statement such as 'where *l* is in meters…'".
(c) Hard (metrology). The SP811 §7.11 point is fine-grained: in a quantity equation, give the unit with the *value* ("*t*_window = 1 000 s"), not as a gloss on the equation.

### D. Constants and free parameters

**22.** (a) Name every constant, and give each value a stated basis: literature, data, calibration, or a declared design choice.
(b) ODD, §"Issues and Challenges": "provide the basis for all parameter values (e.g., taken from which literature, and why; developed from what data, and how; estimated via calibration, how)". EMPSTD Optimization Studies l.64: "justifies the parameter values used when executing the evaluated approaches". EMPSTD Simulation l.25: "describes the simulation model … including input parameters and response variables"; l.32: "clearly explicates the assumptions of the simulation model".
(c) **Hard** in simulation reporting. The six bare constants (1 000 s, 750 s, 1 250 s, 125 s, 1 500 s, 60 s) each need a name, a unit and a one-line basis. If some are derived from one another (e.g. 750 and 1 250 as ±250 around 1 000, or 125 as 1 000 / 8), say so: then only the root constants are free.

**23.** (a) Report sensitivity to those parameters, or say why it is not needed. Documented assumptions are not in themselves a weakness.
(b) EMPSTD Simulation, Desirable, l.48: "reports sensitivity analysis for input parameters or factors". Invalid Criticisms, l.79: "The mere presence of assumptions in the model is not a valid basis for criticism _as long as_ the assumptions are documented and justified, and their implications for the validity of the simulation are sufficiently addressed." zhang2023 l.410: µ "can be determined via empirical study and sensitivity analysis".
(c) "Desirable", not "Essential", under EMPSTD. Stylistic for a thesis, but it pre-empts the examiner's obvious question.

**24.** (a) Put parameters, and if needed the equations, in a table. Keep the rationale in the text, and use the same names in text and code.
(b) ODD, §"Improving Clarity, Replication, and Structural Realism with ODD": "if numerous equations are used, summarize these in tables and explain the rationale of each equation in the text. This disentangling of equations and text is more concise, provides a better overview". ODD, same section: "group parameters according to the submodels in which they are used rather than providing a single large table". ODD: "Using the same names for variables, parameters, and submodels in both ODD and code makes it easier to find the code". Corpus: masud2025 Table 3 (l.258) and Table 4 (l.307); ho2024 Table 3 (l.320); hong2018 Tables 1–2 (l.194, 204).
(c) Stylistic, and the domain norm.

**25.** (a) Write numbers consistently: digits for measured values with units, grouped with thin spaces.
(b) SP811 §10.5.3, p. 37: "digits should be separated into groups of three … by the use of a thin, fixed space. However, this practice is not usually followed for numbers having only four digits … except when uniformity in a table is desired." KNUTH rule 18, p. 3: "Small numbers should be spelled out when used as adjectives, but not when used as names".
(c) Hard (SI style). "1 000 s" is correct if used uniformly, and so is "1000 s".

### E. Examples

**26.** (a) Give a worked example, ideally one running example carried through every metric, and state each definition twice in complementary ways (a formula and a sentence).
(b) KNUTH rule 11, p. 2: "Try to state things twice, in complementary ways, especially when giving a definition. This reinforces the reader's understanding." HALMOS §16: "a general statement about n × n matrices is frequently best proved not by the exhibition of many a_ij's … but by the proof of a typical (say 3 × 3) special case." hong2018 §5.3 (l.390–408) is the corpus exemplar: one example SDN, every metric computed on it, each value read back in words ("The APV value 0.6667 represents the expected proportion of changes…").
(c) Stylistic, but the strongest single fix for "decoration". It also matches the recorded examiner feedback that missing examples cost marks.

---

## What this implies for a metric definition template

For a section defining ten metrics for a general CS reader:

1. **One shared preamble before the metrics.** Define the few *base measures* recorded per run (ISO15939 3.3; items 15 and 22), each with a name, unit and counting rule (KITCH DC1). List the named constants in one small table with value, unit and basis (ODD). Mark which constants are derived from others. Every later equation draws only on these symbols. None is borrowed from another section without a phrase-and-number back-reference (MERMIN Rule 2).
2. **Per metric, in this order:**
   - **Name**, in words, with any acronym expanded (item 10). No per-metric Greek letter unless it is reused later (items 2 and 7).
   - **One sentence** that is a numeric noun phrase: "the proportion of …", "the mean time from … to …" (SP800-55 "Measure"). This sentence must stand alone if the equation is skipped (KNUTH rule 13).
   - **The APT property or question it records** (the "information need" in ISO15939 terms). This is one clause, not a paragraph.
   - **The equation**, only if it adds precision the sentence cannot. Write it as a *measurement function* of the base measures (ISO 3.20), in plain operators rather than set-builder notation (KNUTH rule 3), numbered and punctuated as part of the sentence (MERMIN Rules 1 and 3).
   - **A `where` clause** for any symbol not in the preamble (KNUTH rule 11).
   - **Unit, range and direction** in one line: "seconds; ≥ 0; higher is better for the defender" (items 16, 17 and 21).
   - **The empty case**: what is reported when the event never occurs, chosen so it cannot be mistaken for a real value (item 18).
   - **Parameters it uses**, by name, pointing to the constants table rather than repeating bare numbers (items 9 and 22).
3. **One running example.** A single small trace (one run, a few events), with every metric computed on it and read back in a sentence (item 26; hong2018 §5.3).
4. **Once, at the end:** which constants were varied in a sensitivity check and where that check is reported, or why it was not needed (item 23).

Hard conventions (do not break): items 1, 6, 13, 14, 15, 21, 22. Domain norms (expected by an MTD reader and the supervisor): 10 (named metrics, expanded), 16, 17, 18, 24. The rest are stylistic preferences backed by the writing guides.
