---
status: open                  # retire in the commit that lands the introduction through pass 6
created: 2026-09-24
companions: 2026-09-21_seminar_title_abstract_design.md (the generalist reader, the claim tiers, the ratified hook; deleted in the working tree at the time of writing, in git at 9d6e3a10), ../notes/ch1_introduction/mtd_absent_from_volt_typhoon_response.md (the hook's evidence), ../notes/_writing_guide.md (the introduction's job and the unit ledger), ../workflows/literature_conventions.md §(g) (the three ch1 structural rulings)
---

# Chapter 1 introduction: the design the slots are cut from

> **Mode note.** This is a top-down design, done at Marc's request on
> 2026-09-24: the conventions, the reader, the length, the move order, a job
> for each paragraph, the ceiling and the term budget. **No sentence of the
> chapter is drafted here.** The next step is the slot generator (one slot
> per sentence, with facts and ceiling), and then Marc dictates. §8 lists the
> decisions that are his.

## 1. What the introduction is for, and who reads it

Examiners read the introduction and the conclusion first, then check that
the two link up (Evans, Gruba & Zobel 2014, p. 5). Referees have "probably
made an initial decision" by the end of the introduction (Widom). The design
consequence runs both ways:

- the introduction promises only what the conclusion can answer, point for
  point;
- the conclusion is designed against this chapter, answering SQ1–SQ3 in
  order and then the research question.

**The reader.** The reader is a computer-science examiner who is not an MTD
specialist. They are fluent in networks, simulation and benchmarking, and
have met APTs in the news. They have not met moving target defence, ATT&CK,
cyber threat intelligence as a term of art, attack graphs or Petri nets.

The genre sources agree that the introduction is written for a wider reader
than the rest of the thesis:

- "broad in topic and conversational in tone … theory, jargon, and notation
  are inappropriate" (Zobel 2014, p. 67);
- "written for a wider readership than the bulk of the thesis, and may use
  illustrative examples" (Evans, Gruba & Zobel 2014, p. 12).

**The abstraction gradient.** ¶1–¶3 sit at the seminar abstract's level:
plain words, two defined terms. ¶4–¶8 rise to chapter 2's level. By then the
reader has chosen to go on, and each field term is defined once, in the
clause that introduces it. Nothing in the chapter sits at chapter 4's level.

## 2. The evidence: what the field and the genre literature do

Two independent surveys were run on 2026-09-24:

- a move-by-move dissection of the 29 introductions in `docs/sources/lit_review/`
  (25 papers, the three MTDSim student reports, and Marc's literature review);
- a survey of the genre-analysis research and the practitioner authorities.

Where they bear on the design:

| Question | Finding | Source |
|---|---|---|
| Move order | Establish the territory, then the niche (in computing: the *problem*), then occupy it. Thesis introductions keep the three moves and add steps: research questions, method, findings, scope, chapter overview | Swales 2004; Bunton 2002 (secondary); Soler-Monreal et al. 2011 (English computing PhDs) |
| Which steps computing theses carry | Out of 10 English computing PhD introductions: thesis structure 10, findings or contributions 9, out-of-scope statement 9, problem 8, gap 7, examples 7, method 6, research questions 5 | Soler-Monreal et al. 2011, Tables 6–8 |
| Announce results? | **Yes in computing.** Findings are announced in 70–75 % of CS and SE article introductions. Zobel: "a paper isn't a story in which results are kept secret until a surprise ending" (p. 58). Against: Dunleavy (humanities: "no potted version") and Thomson ("the argument, not all the results") | Anthony 1999, Posteguillo 1999, Shehzad 2010; Zobel 2014; Dunleavy 2003, p. 206 |
| Open on an event? | Licensed, with conditions. An example beats "X is important" (Peyton Jones: "use an example", "molehills not mountains"). An event can serve as a high-impact start (Dunleavy, p. 94) if framing text follows immediately to tie it to the general problem (p. 95). It must motivate *what the thesis tests* (Zobel, p. 80), and a vignette runs to a couple of hundred words at most (Thomson) | as named |
| The field's openers | 13 of 25 papers open with a field-importance sentence, and all three student reports do. Zobel calls this "flat and uninspiring" (p. 97). Only 8 of 25 use an incident or a statistic. **No MTD paper in the corpus opens on a named campaign** | corpus dissection |
| The stock MTD motivation | Static systems give the attacker time (Ghosh/NITRD: adversaries "plan at their leisure"). MTD changes the attack surface to raise the attacker's uncertainty and cost. Perfect security is impossible (Cho 2020) | corpus: ghosh2009 l.9, cho2020 l.40, brown2023 l.15 |
| Research question | State a single aim. State the research question in chapter 1, at least broadly. Several aims in one sentence are usually steps in the method | Evans, Gruba & Zobel 2014, pp. 64–70 |
| Contributions | A bulleted list of **refutable** claims, each forward-referenced to its evidence. The list can double as the outline (Widom). In the corpus the list is 3 items (modal) and mostly activity-shaped ("we propose…"); only three papers state findings a reader could check | Peyton Jones slides 20–22; Widom; corpus |
| Roadmap | A paper can do without one: Peyton Jones rejects "the rest of this paper is …" (slide 23). A thesis cannot: 10 of 10 computing theses have one, and Thomson says "the examiner expects to see some kind of road map". The form wanted is a narrative synopsis, not a list of sections (Evans, Gruba & Zobel, p. 67; Zobel, p. 80) | as named |
| Length | Peyton Jones: one page for a paper. Corpus papers: median about 740 words (IQR 620–850). Student reports: 560–630 words, about 7 % of the body. Evans, Gruba & Zobel give 7–10 pages for a PhD, about 3–5 % of the words, and treat honours as a "minor thesis" whose reader is known. The fixed moves (question, contributions, scope, overview) do not shrink with the thesis | as named |
| Draft order | "Write it last" is the writing guide's advice, **not** Evans, Gruba & Zobel's. They say to draft the introduction early and revise it to the end (pp. 70–71; Zobel p. 64). The two reconcile: design now, draft ¶1–¶5 now, fill the result slots last | as named |

**What the local lineage does, and where to differ.** Tay, Zhang and Ho
(`tay2024.md`, `zhang2023.md`, `ho2024.md`) share one template, and Ho and
Tay reuse Zhang's sentences. Each follows the same pattern:

- a field-importance opener;
- a one-paragraph gap;
- a four-item, activity-shaped contributions list that doubles as the
  table of contents;
- no research question, no stated result, no roadmap, no example.

The dissertation should differ from them on four counts:

- an explicit research question;
- a finding stated as a claim a reader can check;
- a concrete case, where their openers are generic;
- a scope statement.

Brown 2023 (problem opener, an incident, findings stated qualitatively) is
the lineage's stronger model. Marc's own literature review introduction
already has the shape the design below extends: a definition, a
counter-claim, a displayed question and an outline.

## 3. Marc's arc, read against the conventions

Marc's spoken sketch (2026-09-24): Volt Typhoon → MTD as a solution that has
been around but is not applied → the gap → method → results → discussion
points → research question and sub-questions → contributions → source code.

The first four links are the canonical CARS sequence and stand as sketched.
Five adjustments:

1. **Move the research question up, to straight after the gap.** Every
   authority puts the aim where it follows logically from the problem, and
   the reader needs the question before the answer. After the results, the
   question reads as reverse-fitted, which is the circularity an examiner
   reaches for first (voice.md §(c)10).
2. **"Hasn't been applied" is not licensed.** The note licenses one
   narrower observation: the February 2024 advisory answers the campaign
   entirely with static hardening and detection and never names MTD
   (verified against AA24-038A only). The honest bridge is that this
   advisory does not name the defence aimed at what this attacker banks,
   and the evidence that would argue for it does not exist, because
   evaluations test MTD against simplified attackers. That bridge is ¶2's
   turn and ¶3's problem.
3. **"Discussion points" are not a move in any introduction surveyed.** The
   discussion's role in chapter 1 is the *value* step: one sentence on what
   the result means for MTD evaluation. It closes the findings paragraph (¶6).
4. **Add the "why is it hard" step.** This is Widom's question 3, and the
   sketch has nothing for it. Turning narrative threat reports into an
   attacker that runs in a simulator is not obvious for three reasons:
   - the reports are prose written after the fact;
   - they rarely report timing;
   - the simulator's attacker acts through a small fixed set of actions.

   This is also what makes SQ1 and SQ2 questions rather than steps.
5. **Add scope and an overview.** Both are near-universal in computing
   theses (9/10 and 10/10). Scope is two sentences; the overview is one
   short narrative paragraph. The source-code sentence rides the
   contributions list, as ruled in §(g)3.

## 4. The design: paragraph by paragraph

**Budget for the recommended length: about 1 100 words.** That is roughly
two pages at the compiled density: a full prose page of this dissertation
holds about 600 words (pages 31–33, measured). The RQ block and the
contributions list are included in the count.

The ledger allows 1 500 words (six units). Coming in about 400 under returns
one to two units to the float, which chapters 5 and 6 need. §8 decision 1 is
the length.

| ¶ | Move | Job (the claim the paragraph establishes) | Facts available | Ceiling / must not | ~words |
|---|---|---|---|---|---|
| 1 | M1: territory, through a case | An APT is a real, dated, local threat whose advantage is time spent inside the network | AA24-038A (Feb 2024; nine agencies including ASD's ACSC): Volt Typhoon held footholds for **at least five years**; used valid credentials and native tools, no malware; refreshed domain-controller credentials over four years; pre-positioning, not espionage. APT defined in one clause (alshamrani2019). Optional class fact: M-Trends 2026 puts the global median dwell at 14 days and the espionage-class median at 122 days (the corpus's best exemplar *measures* the asymmetry; cho&benasher2018) | An instance of the class and motivation only; the corpus excludes this campaign, so nothing may imply MTD was scored against it. Not the abstract's first sentence reused verbatim. No colon-list of tradecraft; no "rapidly evolving"; no AI-acceleration opener | 110 |
| 2 | M1: the defence aimed at exactly that, then the turn | MTD's stated mechanism targets what this attacker banks, yet the authoritative response does not name it | MTD defined (ghosh2009nitrd origin; cho2020): continually changes the configurations an attacker has learned, so the knowledge goes stale; the static-network asymmetry (Ghosh's "plan at their leisure"). The advisory's mitigations are patching, MFA, logging and hunting, with zero mentions of MTD | The *stated* mechanism, not a proven effect. The absence is "this advisory", never "nobody". No "novel", no "promising"; MTD has been around since 2009 at the latest, so say so rather than hide it | 110 |
| 3 | M2: the problem, and why it is unsolved | The evidence that would support MTD against this attacker does not exist: evaluations test it against scripted attackers, and building a campaign-shaped attacker is hard | MTD is evaluated overwhelmingly in simulation (cho2020 Sec. VIII-B). Attacker models have no multi-stage knowledge to lose and cannot adapt (ch3 §3.3.3's verdict, stated once at this altitude). jalowski2026 p. 8 calls the attacker model the field's "most glaring flaw". Metrics are computed over the attacker model, so the attacker is the evaluation's weakest link. *Why hard*: the reports are narrative, untimed and after the fact; the simulator's attacker has a small fixed action set. The means exist next door (attack profiling from CTI; ATT&CK) but have not been brought to MTD evaluation | "In the evaluations surveyed"; name no paper as at fault in ch1. "Simplified" or "scripted", never "weak" (the baseline reaches more hosts sooner; seminar ruling). No literature review: one citation per claim, the landmark only | 150 |
| 4 | M3: aim → RQ block | One aim, then the question and its three parts | One lead-in sentence, then the RQ and SQ1–SQ3 as already typeset (enumitem, `\label{sq:*}`) | The aim is singular (Evans, Gruba & Zobel). Terms fixes are in §6 | 90 |
| 5 | M3: approach, plus the positioning line | How the question is answered, in one pass the reader can hold | 38 analyst-curated attack flows (MITRE ATT&CK; Attack Flow) → an attack graph → attack profiles conditioned on operational objective → a stochastic Petri-net formalism → executed in MTDSim beside its baseline attacker → two phases: without defence (behaviour), then under MTD (every deployment strategy including MTDShield, across deployment intervals). The flag C4 line (Marc's to dictate): the thesis keeps the field's dominant method, simulation, on purpose and changes only the attacker. Forward references to chapters 4 and 5 | No layer labels, no GSPN symbols, no $c_1$–$c_4$, no metric acronyms, no "movement". Use a number only where it carries the claim (Marc's rule on decorative numbers): "38" earns its place if it answers "how much evidence?"; otherwise cut it | 140 |
| 6 | M3: principal finding + value | What the evaluation found, and what it means for MTD evaluation (Marc's "discussion points", as one sentence) | **Filled last**, from the 1 000-seed corpus (E6/E7: rankings on the APT attacker model). The candidates are the seminar brief's §4 tiers: T2, which defence ranks best depends on the attacker; T3, the direction (shuffling against the APT attacker model, diversity against the baseline). A phase-one clause is optional (the attacker's behaviour differs without any defence). Value: an evaluation's recommendation depends on the attacker it assumed | Re-read against `tab_5-3-2a_orderings.tex` at the reported seed count; no "preliminary" once the 1 000 seeds are reported. Never "MTD defeats APTs", "inverts", "realistic" or "validated". A number only if the headline *is* the number | 100 |
| 7 | M3: scope | What the work does not claim, before the examiner says it | Existing defences only (no new mechanism); simulation only; the attacker model is an envelope of documented behaviour, not a named actor; no detection channel in the simulator, so stealth is measured but nothing reacts to it | Two sentences. It can close ¶5 or ¶6 instead of standing alone; it must not become a limitations section (chapter 6 owns that) | 50 |
| 8 | M3: contributions list + availability | The refutable claims, keyed SQ1–SQ3 and forward-referenced | See §5 | Claims, not activities (the lineage's defect). Each item maps to a conclusion sentence | 200 |
| 9 | Thesis overview | A synopsis of the storyline, not a table of contents | Chapters 2–8, one clause each, carrying the capture/model/evaluate spine | Functional signposting only (voice.md §(h) bans the empty kind). If the contributions list carries chapter pointers, this can shrink to the chapters it does not cover (2, 3, 6–8) | 100 |

**Total ≈ 1 050.**

**Figures.** No introduction figure. At most one sentence points forward to
the chapter 4 overview (E8's box figure). A teaser figure is rare in the
corpus (4 of 25) and would duplicate E8. Missing examples cost marks on the
literature review, and ¶1 is the example that fixes that at this altitude.
§8 decision 7 is open if Marc wants a picture.

## 5. The contributions list, candidates only (Marc words and selects)

The form: three items keyed to the sub-questions, with the availability
sentence riding the last item, per the §(g)2–3 rulings. Each item is a claim
a reader could check, with a chapter pointer.

| Item | Key | Candidate claim (content, not wording) | Evidence badge today |
|---|---|---|---|
| C1 | SQ1 | Attack profiles are derived from 38 analyst-curated campaign reports and conditioned on operational objective. The conditioning changes the attacker's behaviour | demonstrated (criterion axis 2, the one property shown to change an outcome) |
| C2 | SQ2 | An APT attacker model is executed inside an existing MTD simulator, beside its baseline attacker, on the same action set. Its declared inputs (dwell times, tactic-to-verb mapping, failure matrix) are stated and tested for robustness | built; robustness in Appendix C |
| C3 | SQ3 | A two-phase evaluation (without defence, then under every deployment strategy including MTDShield across the interval range), whose finding is ¶6's | waits for the 1 000-seed corpus |
| (C4?) | ch3 | The cross-section scoring of recent MTD attacker models against the eight properties of a sophisticated attacker | ch3 Tables 3.2–3.3; Marc's call whether a literature-review product is listed |
| (C5?) | ch4 §4.5 | MTDSim instrumented with the attacker-behaviour metrics, released as open source | §4.5 in progress; could fold into C2 plus the availability sentence |

**Retired, do not list.** The learning and cost-sensitivity negatives are
out: the ablation subsection was removed on 2026-09-13 ("ablation is
going"), and both marks dropped to implemented, not evidenced. The ranking
inversion is out too (ρ = −0.893 did not reproduce).

**Open sub-decision carried from §(g)3.** The public `main` branch is the
standalone simulator, so the link does not land on the attack-model
pipeline. Before the list is final, decide whether to freeze a thesis
release tag.

## 6. The term budget

| Term | Where defined in ch1 | Note |
|---|---|---|
| advanced persistent threat (APT) | ¶1, one clause | carried forward as APT |
| moving target defence (MTD) | ¶2, one clause | carried forward as MTD |
| simulation / the baseline attacker | ¶3 or ¶5 | "the simulator's own scripted attacker, here the *baseline attacker*" (the registry canonical) |
| cyber threat intelligence (CTI) | ¶3 or ¶5 | **Open registry row (L0):** CTI, or *campaign intelligence* as its gloss. SQ1 uses the gloss, so the definition sentence must make them one thing |
| MITRE ATT&CK | ¶5, full name + citation | literature_conventions §(a)1: this is its first use in the document. The version pin is stated in ch4, not here |
| attack profile, operational objective | ¶5 | Marc's keywords (seminar ruling: precise term over plain paraphrase) |
| MTDSim | ¶5 | named once, with brown2023 |

**Never in ch1:**

- layer names or L0–L4;
- GAP/GASP/OGASP, the token, $c_1$–$c_4$ and all notation;
- NCR, ASP and MTTC as acronyms (a result sentence uses plain words);
- *suppression*, *movement attacker*, *tactic-to-verb mapping*, *failure
  matrix* (outside C2), *envelope* (outside the scope sentence).

**Fixes the RQ block needs before dictation** (for Marc to confirm; the tex
is not touched here):

- SQ3 says "the inherited scripted attacker". The registry canonical is the
  *baseline attacker*. Either SQ3 adopts it, or ¶3 defines the scripted
  attacker as the baseline attacker first.
- SQ1 says "published campaign intelligence". This waits on the open CTI
  row above.
- The RQ asks how MTD performs "against APT attackers". The thesis measures
  performance against an APT *attacker model*. Posing the RQ at the
  real-world level is the convention, and SQ3 carries the model, so the
  recommendation is to keep it. Marc should rule on it knowingly, though,
  because the ceiling sits exactly there.

## 7. The ceiling (what ch1 may claim)

The seminar brief's §4 tiers still hold. Tier 1 is always sayable: what was
built and run. The headline is the tier the 1 000-seed corpus supports at
drafting time; on the 100-seed corpus that is tier 3, stated under
"preliminary".

Standing bars:

- the defensible claim is *behavioural fidelity changes the answer*, never
  *the attacker model is true* or *the defence works*;
- Volt Typhoon is motivation, not an evaluated scenario;
- the advisory-absence claim is scoped to AA24-038A;
- there is no "novel", "realistic", "validated" or "comprehensive";
- where a criterion badge is *designed*, ch1 says built, not shown.

## 8. Decisions that are Marc's

1. **Length.**
   - (a) About 1 100 words, two pages, returning one to two units to the
     float. *Recommended*: it clears every fixed thesis move and still sits
     near a paper introduction.
   - (b) Marc's "one page": about 600 words of prose plus the RQ block and
     the list, roughly 1.5 pages. It is only reachable by cutting ¶7 into
     ¶5, cutting ¶9 to one sentence and holding ¶3 to 100 words.
   - (c) The ledger's 1 500.
2. **Order.** The canonical order of §4, with the RQ after the problem
   (*recommended*), or the spoken order, with the RQ after the results.
3. **The advisory-absence sentence in ¶2.** Keep it as one observational
   sentence (*recommended*: it is the bridge from the case to the problem)
   or drop it, and go from the MTD definition straight to ¶3.
4. **The M-Trends class statistic in ¶1.** Yes (*recommended*: it turns
   one campaign into a class, and it is the corpus's strongest opener type)
   or no. Watch the decorative-number rule: one number pair, only if it
   carries the claim.
5. **The overview.** A short narrative paragraph (*recommended*; the thesis
   genre expects it) or folded into the contributions' chapter pointers.
6. **The contributions.**
   - Three keyed to SQ1–SQ3, plus availability (*recommended*).
   - Or four to five, adding C4 and/or C5.
7. **An introduction figure.** None, with a forward pointer to chapter 4's
   overview (*recommended*), or a teaser figure.
8. **The RQ's wording level** (§6).
9. **The headline tier.** Deferred until the 1 000-seed corpus lands.

## 9. What is stale in the tex's ch1 comments (flag; not actioned here)

The planning comment at the head of `\chapter{Introduction}` still says:

- "executable movement attacker": the name was retired by E2;
- "the anchor inversion, once the V1 hand-validation pass clears it": the
  inversion did not reproduce;
- "Written last": Evans, Gruba & Zobel advise otherwise, as reconciled in §2.

Rewrite the comment to point here when the slots are cut. The abstract in
the tex is still the seminar abstract, marked PRELIMINARY; it is
re-designed after this chapter.

## 10. Next steps

1. Marc rules on §8.
2. Slot generator, one per sentence: job, shape, facts, ceiling, and what
   the sentence must not do. File:
   `docs/handoffs/2026-09-24_ch1_introduction_slot_generator.md`, or as §11
   here. Before the slots, run the antecedent audit: every term ¶3–¶5 lean
   on must exist in chapters 2–4.
3. Dictate ¶1–¶5 and ¶7–¶9 now; they do not depend on results. Dictate ¶6
   and C3 when the 1 000-seed floats land.
4. Run the pipeline: repair-dictation → scrutinise-draft →
   compress-to-ledger → voice-pass. Then the cold-reader gate below.
5. Design the conclusion against this chapter, with the answers keyed to
   SQ1–SQ3.

## Validation gate

The introduction is done when all of the following hold:

- **(a) Cold read.** A reader who holds only §1's profile, given only the
  chapter and tested cold on a subagent, restates the problem, the question,
  the approach and the finding in four sentences.
- **(b) Moves.** Every paragraph maps to one row of §4, and every move in
  §4 is present.
- **(c) Terms.** No term outside §6's budget is used undefined.
- **(d) Ceiling.** No claim exceeds §7.
- **(e) Conclusion link.** Every contribution item has an answering sentence
  in the conclusion's design.
- **(f) Length.** The word count is within the band Marc picks in §8.1.
- **(g) Voice.** The voice.md §(f) gate passes, including Marc's
  showcase-prose rules: one main clause per opener, no "not X but Y", no
  colon-lists, no decorative numbers.

## Out of scope

- The dissertation abstract and title: re-designed after this chapter.
- The conclusion's prose: its design is coupled here, its drafting is not.
- Any edit to `dissertation.tex`.
- The wider "nobody proposes MTD for Volt Typhoon" discourse check. The note
  flags it, and it is needed only if ¶2 is ever strengthened beyond this
  one advisory.

## Sources (for the genre evidence in §2)

Swales, *Research Genres* (2004), pp. 230–232 (via reproductions); Anthony,
*IEEE Trans. Prof. Comm.* 42(1), 1999; Posteguillo, *ESP* 18(2), 1999;
Shehzad, *Ibérica* 19, 2010; Bunton in Flowerdew (ed.), *Academic Discourse*,
2002 (secondary, via Mort & Holloway 2006); Soler-Monreal, Carbonell-Olivares
& Gil-Salom, *ESP* 30(1), 2011; Widom, "Tips for writing technical papers";
Peyton Jones, "How to write a great research paper"; Zobel, *Writing for
Computer Science*, 3rd edn, 2014; Evans, Gruba & Zobel, *How to Write a
Better Thesis*, 3rd edn, 2014; Thomson, patter (2014, 2017, 2019); Dunleavy,
*Authoring a PhD*, 2003; UWA CITS4001 project components (15 000 words,
30–50 pages). Corpus locators are in the dissection (file:line), summarised
in §2. None of these is in `references.bib`: they ground the design, not the
thesis.
