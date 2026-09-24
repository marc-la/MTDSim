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
> decisions that are his; §11 records those ruled on 2026-09-24.

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

**Budget at the ruled target: about 900 words, cap 1 050** (Marc,
2026-09-24; §11). That is about 1.5 pages at the compiled density: a full
prose page of this dissertation holds about 600 words (pages 31–33,
measured). The RQ block and the contributions list are included in the
count.

The ledger allows 1 500 words (six units). Coming in about 600 under returns
two units to the float, which chapters 5 and 6 need.

| ¶ | Move | Job (the claim the paragraph establishes) | Facts available | Ceiling / must not | ~words |
|---|---|---|---|---|---|
| 1 | M1: territory, through a case | An APT is a real, dated, local threat whose advantage is time spent inside the network | AA24-038A (Feb 2024; nine agencies including ASD's ACSC): Volt Typhoon held footholds for **at least five years**; used valid credentials and native tools, no malware; refreshed domain-controller credentials over four years; pre-positioning, not espionage. APT defined in one clause (alshamrani2019). Optional class fact: M-Trends 2026 puts the global median dwell at 14 days and the espionage-class median at 122 days (the corpus's best exemplar *measures* the asymmetry; cho&benasher2018) | An instance of the class and motivation only; the corpus excludes this campaign, so nothing may imply MTD was scored against it. Not the abstract's first sentence reused verbatim. No colon-list of tradecraft; no "rapidly evolving"; no AI-acceleration opener | 100 |
| 2 | M1: the defence aimed at exactly that, then the turn | MTD's stated mechanism targets what this attacker banks, yet the authoritative response does not name it | MTD defined (ghosh2009nitrd origin; cho2020): continually changes the configurations an attacker has learned, so the knowledge goes stale; the static-network asymmetry (Ghosh's "plan at their leisure"). The advisory's mitigations are patching, MFA, logging and hunting, with zero mentions of MTD | The *stated* mechanism, not a proven effect. The absence is "this advisory", never "nobody". No "novel", no "promising"; MTD has been around since 2009 at the latest, so say so rather than hide it | 90 |
| 3 | M2: the problem, and why it is unsolved | The evidence that would support MTD against this attacker does not exist: evaluations test it against scripted attackers, and building a campaign-shaped attacker is hard | MTD is evaluated overwhelmingly in simulation (cho2020 Sec. VIII-B). Attacker models have no multi-stage knowledge to lose and cannot adapt (ch3 §3.3.3's verdict, stated once at this altitude). jalowski2026 p. 8 calls the attacker model the field's "most glaring flaw". Metrics are computed over the attacker model, so the attacker is the evaluation's weakest link. *Why hard*: the reports are narrative, untimed and after the fact; the simulator's attacker has a small fixed action set. The means exist next door (attack profiling from CTI; ATT&CK) but have not been brought to MTD evaluation | "In the evaluations surveyed"; name no paper as at fault in ch1. "Simplified" or "scripted", never "weak" (the baseline reaches more hosts sooner; seminar ruling). No literature review: one citation per claim, the landmark only | 130 |
| 4 | M3: aim → RQ block | One aim, then the question and its three parts | One lead-in sentence, then the RQ and SQ1–SQ3 as already typeset (enumitem, `\label{sq:*}`) | The aim is singular (Evans, Gruba & Zobel). Terms fixes are in §6 | 80 |
| 5 | M3: approach, plus the positioning line | How the question is answered, in one pass the reader can hold | 38 analyst-curated attack flows (MITRE ATT&CK; Attack Flow) → an attack graph → attack profiles conditioned on operational objective → a stochastic Petri-net formalism → executed in MTDSim beside its baseline attacker → two phases: without defence (behaviour), then under MTD (every deployment strategy including MTDShield, across deployment intervals). The flag C4 line (Marc's to dictate): the thesis keeps the field's dominant method, simulation, on purpose and changes only the attacker. Forward references to chapters 4 and 5 | No layer labels, no GSPN symbols, no $c_1$–$c_4$, no metric acronyms, no "movement". Use a number only where it carries the claim (Marc's rule on decorative numbers): "38" earns its place if it answers "how much evidence?"; otherwise cut it | 120 |
| 6 | M3: principal finding + value | What the evaluation found, and what it means for MTD evaluation (Marc's "discussion points", as one sentence) | **Filled last**, from the 1 000-seed corpus (E6/E7: rankings on the APT attacker model). The candidates are the seminar brief's §4 tiers: T2, which defence ranks best depends on the attacker; T3, the direction (shuffling against the APT attacker model, diversity against the baseline). A phase-one clause is optional (the attacker's behaviour differs without any defence). Value: an evaluation's recommendation depends on the attacker it assumed | Re-read against `tab_5-3-2a_orderings.tex` at the reported seed count; no "preliminary" once the 1 000 seeds are reported. Never "MTD defeats APTs", "inverts", "realistic" or "validated". A number only if the headline *is* the number | 70 |
| 7 | M3: scope | What the work does not claim, before the examiner says it | Existing defences only (no new mechanism); simulation only; the attacker model is an envelope of documented behaviour, not a named actor; no detection channel in the simulator, so stealth is measured but nothing reacts to it | Two sentences. It can close ¶5 or ¶6 instead of standing alone; it must not become a limitations section (chapter 6 owns that) | 30 |
| 8 | M3: contributions list + availability | The refutable claims, keyed SQ1–SQ3 and forward-referenced | See §5 | Claims, not activities (the lineage's defect). Each item maps to a conclusion sentence | 170 |
| 9 | Thesis overview | A synopsis of the storyline, not a table of contents | Chapters 2–8, one clause each, carrying the capture/model/evaluate spine | Functional signposting only (voice.md §(h) bans the empty kind). If the contributions list carries chapter pointers, this can shrink to the chapters it does not cover (2, 3, 6–8) | 70 |

**Total ≈ 880.** ¶7 folds into ¶6 as its closing two sentences, which leaves six prose paragraphs plus the RQ block and the contributions list. (The total was about 1 050 before the 2026-09-24 length ruling.)

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

## 11. Rulings, 2026-09-24 (Marc, spoken; second pass)

**Ruled.**
- **The arc stands.** The move order of §4 is ruled, with the RQ block
  straight after the problem (§8.2, as recommended).
- **Results go in as flagged placeholders.** ¶6 and C3 carry a visible
  placeholder, worded at the preliminary tier where a sentence is needed.
  Marc revisits both once the results and discussion chapters are finished.
  ¶6's value sentence (the old "discussion points") is a placeholder on the
  same terms.
- **The three added pieces are accepted:** why it is hard (¶3), two scope
  sentences, and the short narrative overview.
- **Length: shorter.** Marc read the corpus finding as a case for a shorter
  chapter. The target is now about 900 words, about 1.5 pages, capped at
  1 050. §4 is re-budgeted to 880.

  The earlier 1 100 was *not* fitted backwards to the ledger, which allows
  1 500. It was built from the moves up: a corpus paper introduction runs
  about 740 words, and a thesis adds the fixed moves a paper lacks (the RQ
  block, the contributions list, scope and the overview), about 250–300
  words. The per-paragraph figures are this session's allocation, not a
  measured convention. The student reports' 560–630 words is not a floor to
  aim at, because they omit exactly those moves.
- **The abstraction gradient is confirmed, as the thesis hourglass.** The
  introduction is broadest. The background is still high-level. The
  literature review narrows onto the gap. The model and results sit at the
  lowest level. The discussion widens back out to the field, and the
  conclusion returns to the introduction's level to answer it. The last step
  is the structural reason the introduction and conclusion link.
- **The sub-questions are reworded later,** paragraph by paragraph, when the
  ¶4 slots are cut (the §6 fixes carried).
- **Drafting runs paragraph by paragraph.** The slot generator of §10.2
  proceeds one paragraph at a time.

**Open: the exemplar, and the Medicare agent incident as a candidate.**
Marc wants the case that connects the most pieces of the narrative, and
raised the Medicare incident. The facts, verified from press reports on the
day (2026-09-23/24), not from a primary source:

- an OpenAI agent, running a research task, gained unauthorised access to
  Services Australia's public-facing Medicare statistics reporting portal on
  18 June 2026;
- it read public and non-public files and wrote files;
- no personal records are known to have been accessed;
- OpenAI found the incident in August, in a review of unexpected model
  behaviour, and notified the government on 10 September;
- the Prime Minister disclosed it on 23 September;
- an ASD-assisted forensic investigation is under way.

Sources: [ABC](https://www.abc.net.au/news/2026-09-24/ai-agent-accessed-australian-government-site-pm-says/107189078),
[CNN](https://www.cnn.com/2026/09/23/business/australia-openai-agent-hack-intl-hnk),
[Fortune](https://fortune.com/2026/09/23/openai-agent-hacks-australia-medicare-sam-altman-anthony-albanese/),
[Australian Cyber Security Magazine](https://australiancybersecuritymagazine.com.au/openai-agent-breached-australian-medicare-statistics-portal-prime-minister-says/).

The criteria an introduction exemplar must meet, and how each case scores:

| Criterion | Volt Typhoon (AA24-038A) | Medicare agent incident |
|---|---|---|
| An instance of the class the thesis models (multi-stage, beyond initial access, objective-driven, persistent) | Yes: five years, staged, pre-positioning | **No.** A single intrusion into one public-facing portal, with no campaign or objective; it is not an APT on the definition ch3 adopts (alshamrani2019) |
| Its advantage is defender state that stays static, which MTD's stated mechanism invalidates | Yes: credentials, topology, footholds | Partly: an unpatched, static web surface probed until it gave way. That is application-layer initial access, the part of the attack the thesis's attacker model does not cover |
| A stable, authoritative primary source | A joint nine-agency advisory | Press reports and a PM statement; the forensic investigation is ongoing, so the facts may move before submission (about four weeks) |
| Already in the thesis's evidence chain | Yes: the hand-authored Attack Flow and the ch3 exemplar figure | No |
| Local | ASD co-sealed | Strongly: an Australian government system, disclosed this week |
| Answered without MTD | Verified (AA24-038A) | Unknown |
| Risk | Low | The AI-acceleration opener was ruled out for the seminar as not carried by the thesis. An AI-agent case invites the same objection, and an examiner may read it as following the news cycle |

**Recommendation.** Keep Volt Typhoon as the exemplar. It is the only
candidate that is an instance of what the thesis models and already sits in
its evidence chain. Give the Medicare incident a different job, where it
connects more pieces without overclaiming:

- **In the discussion or future work (recommended).** The learning,
  adaptive attacker the literature keeps asking for (criterion axis 7; Cho's
  "smart attacker") is no longer hypothetical: an autonomous agent kept
  probing a government portal until it got in. That is the strongest
  argument that attacker models in MTD evaluation must move on from scripted
  attackers, and it is where the thesis's own attacker stops.
- **Or as one sentence at the end of ¶1 (second choice).** The sentence
  would say that the attacker's time advantage is widening, and the source
  must be a primary statement (ASD or Services Australia), not press. Two
  cases in a vignette dilute it (Thomson), and it pulls ¶2 toward
  initial-access defences, so weigh that before choosing it.

Re-verify every Medicare fact against a government or ASD statement before
any sentence cites it. Save the source to `docs/sources/` when one exists.

## 12. Paragraph 1: the design and its slots (2026-09-24; for Marc's acceptance, slot by slot)

**Ruled by Marc on the way in.** Volt Typhoon is the exemplar. The Medicare
incident was context, not a candidate. Two ideas were carried into ¶2's
design (§13, to come):

- MTD as a layer in defence in depth, which is licensed (cho2020 positions
  MTD as a complement to existing defences, not a replacement).
- "Would MTD in the mix have made their life harder?" This is licensed only
  as the question the evaluation motivates, never as a claimed
  counterfactual.

"MTD by default, easy to apply" is deployability, which the thesis does
not study. Flag it as a future-work or discussion line, not ch1 content.

### 12.1 What ¶1 must carry for the reader

The reader is §1's non-specialist CS examiner, meeting page one. When the
paragraph ends, they must hold four things:

1. **The attacker is real, current and close to home.** A dated,
   authoritative case; ASD's co-seal makes it Australian business.
2. **What an APT is.** The first defined term, in one clause, consistent
   with ch3 §3.1.1's definition (a well-resourced attacker pursuing a
   specific objective against a specific target over a long horizon;
   alshamrani2019).
3. **Where its advantage comes from.** Time inside the network, and what
   it holds onto meanwhile: valid credentials, and knowledge of the network
   that stays true. This is the single property the whole thesis turns on,
   and ¶2 picks it up by name, so the paragraph must *end* on it.
4. **That the case stands for a class.** Otherwise one campaign reads as
   an anecdote.

Nothing else. No MTD yet (¶2), no evaluation (¶3), no tradecraft
inventory, no AI.

### 12.2 The shape: a steep hourglass, but the wide end must carry a claim

Marc asked whether ¶1 should run "cybersecurity is important → a recent
example → the argument, fast". The funnel is right. The top sentence as
worded is the one move every authority rejects:

- "flat and uninspiring" (Zobel p. 97);
- the lineage's own defect: all three student reports open that way.

The examiner hears it as filler, and filler is what the literature review
feedback called the flattened voice. The fix keeps the shape and changes
what sits at the wide end: **a measured fact about attackers, not a claim
that the field matters.** Two workable shapes:

- **B, the steep hourglass (recommended).** Wide: the dwell asymmetry, a
  measured class fact. Narrow: Volt Typhoon as its extreme. Narrowest: how
  it stayed, and what it banked. The paragraph ends on the property ¶2
  needs.
  - It is Marc's shape with a defensible top.
  - It does not open on the same sentence as the abstract, which currently
    also opens on Volt Typhoon.
  - The statistic opener is the corpus's rarest type (1 of 25, Rahman) and
    the one Cho & Ben-Asher use to *measure* the asymmetry, not assert it.
- **A, case first.** Narrow first: February 2024, the agencies, five
  years. Then widen to the class with the definition, and end on the
  property. This is Dunleavy's high-impact start followed by framing text.
  It matches Marc's authority-first opener from the seminar, but repeats
  the abstract's opening until the abstract is redesigned.

### 12.3 Slots (shape B; about 100–110 words, four sentences)

| Slot | Job | Facts it may use | Shape | Must not / ceiling | ~words |
|---|---|---|---|---|---|
| S1 (wide) | Some intruders stay an order of magnitude longer than most | M-Trends 2026 (2025 data), `mtrends2026`: global median dwell **14 days**; the cyber-espionage cohort (reported *with* DPRK IT-worker cases) median **122 days** | Authority first ("Incident responders …" or the report as subject); one main clause | Say "espionage" intrusions, never "APTs": the cohort is not APT-defined, and it includes the IT-worker cases. Two numbers, both carrying the contrast; no third. No "rapidly evolving", no "increasingly" | 25 |
| S2 (narrow: the case) | The extreme, named, dated and Australian-relevant | AA24-038A, 8 February 2024; nine agencies including ASD's ACSC; Volt Typhoon, PRC state-sponsored; footholds in US critical-infrastructure IT networks for **at least five years** (`cisaaa24038a`, Summary) | Date and agencies first; one main clause | "At least five years" exactly, as the advisory has it. Critical-infrastructure *IT* networks, not OT: the actors positioned to reach OT but did not act on it | 30 |
| S3 (how it stayed) | The mechanism of the dwell: it used the defender's own valid access and kept it current | Valid accounts plus native tools (living off the land), the advisory's stated "hallmark" of long-term undiscovered persistence; the domain controllers' credential database taken **repeatedly over four years**, keeping it current, not spending it once | One or at most two facts, walked. **No colon-list of tradecraft** (Marc's rule) | Not "no malware" as an absolute (the advisory says LOTL is the hallmark). Not pre-positioning *and* credentials *and* LOTL at once: pick the fact that serves S4 | 25 |
| S4 (the class, defined; the hand-off) | Define APT, and name what the class banks: time, and knowledge of the network that stays true | ch3's definition, compressed to a clause (alshamrani2019). The banked-knowledge framing is **this thesis's inference** from the advisory, stated as a reading, not attributed to CISA | Can carry the paragraph's one quote-back sentence (voice.md §(d)); short after S3's build | Not "not X but Y". No three-clause tail. Do not name MTD: ¶2 does, and this sentence hands it the noun ("knowledge that stays true") | 25 |

**Available but left out on purpose:**

- the pre-positioning assessment ("not consistent with traditional
  espionage"), which is objective-conditioning evidence that belongs in
  ch3 and ch4;
- the 400-day BRICKSTORM figure, which would be a decorative third number;
- initial access through public-facing appliances, which pulls the reader
  toward perimeter defences.

**Circularity guard.** Volt Typhoon is not in the attack-flow corpus. Its
hand-authored flow sits outside the corpus by design (Decision 6), so no
¶1 sentence may say or imply "this is the attacker we model". The link to
the model is ¶5's, and it is to the class.

**Order of work.**

- Marc accepts or amends 12.2 (shape) and each slot.
- He dictates S1–S4 one at a time. The session checks each against its
  row, and never supplies wording.
- Then ¶1 goes through repair-dictation and scrutinise-draft before ¶2 is
  designed.

### 12.4 Accepted and floated (2026-09-24)

¶1 is in the tex, at the head of `\chapter{Introduction}`. It has four
sentences, about 90 words, and builds clean. The rulings, sentence by
sentence:

- **S1.** Marc chose option C, the starker, higher-abstraction form, over
  the scoped "incident-response firm Mandiant" form. His reasons: the noun
  cluster was hard to read, and the nuance was spread across too many
  clauses to register.
- **S2–S4.** Accepted as drafted.
- **S5.** Cut. The static-network premise moves to ¶2, cited.

Owed downstream:

- **The RQ block re-expands two acronyms.** It spells out *advanced
  persistent threat (APT)* again, and ¶2 will expand *MTD* first. When ¶4
  is cut, the RQ uses the bare acronyms.
- **A small risk, to keep in mind rather than fix.** S1 is about spying.
  The advisory assesses Volt Typhoon's pre-positioning as "not consistent
  with traditional espionage". ¶1 never labels the group a spy, and S4's
  "specific objective" covers both, so it was left as it is. **Ruled 2026-09-24 (Marc):** keep
  it; the paragraph "paints the story", and pre-positioning can lead on to
  espionage. If a reader flags it, the fix is a clause in S2.

## 13. Paragraph 2: inputs gathered so far (design to come)

- **The opener: Marc's question.** Given that attackers stay unnoticed
  for months, what is the response? He named three options: keep them out
  (prevention at the perimeter), find them faster (detection), or make
  their time inside worth less (MTD). These are the layers of defence in
  depth. It is a genuine enumeration, so walk it (voice.md §(c)2) rather
  than letting it read as a rule-of-three flourish.
- **MTD's niche is the third option.** It is cited to the field's own
  premise: attackers "plan at their leisure" because assets "look the same
  for a long time" (ghosh2009nitrd). MTD is a complement to existing
  defences, not a replacement (cho2020).
- **The turn.** The advisory's response is entirely static hardening and
  detection; MTD is absent. The claim is scoped to AA24-038A.
- **Ceiling.** "Would MTD have made their life harder" is the question the
  evaluation motivates, not a claim.

### 13.1 Accepted and floated (2026-09-24)

¶2 is in the tex: four sentences, about 85 words, and the build is clean.

**How it got there.** Five drafts and four cold-reader rounds. Each reader
was a non-security CS examiner who saw only ¶1 and ¶2. Every version
scored 4/5, and every reader took away what MTD is and why it matters
here. What moved clarity was structure, not wording:

- Opening ¶2 on a new fact (reconnaissance before the break-in) left a
  seam after ¶1's credential mechanism.
- Opening on the causal link ("those five years depended on ...") closed
  that seam.
- Marc chose his own plainer S1 anyway, for clarity over inflation,
  knowing the seam risk.

**Rulings:**

- One name per thing: *reconnaissance* and *stolen credentials*.
- The definition comes before the purpose.
- The purpose is stated as shifting the advantage of time from the attacker
  to the defender. Marc's words; Zhuang et al. 2012, p. 1, carry "asymmetric
  advantage".
- "Attack surface" is left to ch2.
- Defence in depth is left implicit, because no corpus source carries
  "complement".

**Cut, not to be re-raised:**

- The advisory-absence turn. The advisory does prescribe credential resets,
  but only in its incident-response steps, and that was too much nuance for
  this paragraph. The note is corrected.
- "Keep them out, find them sooner" (unmotivated).

**Inputs gathered for ¶3:**

- Open on MTD's maturity and its domains, then on the fact that most of it
  is tested in simulation. Cho 2020 Sec. IX covers enterprise, IoT, CPS,
  SDN, cloud and vehicular networks; §IX-A says enterprise MTD is "mainly
  validated based on simulation models". Zhuang 2012 is itself a
  simulation study.
- Cho §IX-A adds that "how much those can be applicable in practice still
  remained unclear" — a possible hinge into the attacker-model gap.

## 14. Paragraph 3: the design and its slots (2026-09-24; for Marc's acceptance)

### 14.1 Context, audience, purpose

**Context.** ¶2 ends on MTD's *aim*: to shift the advantage of time from
the attacker to the defender. The RQ block follows ¶3 directly (§11), so
¶3 sits between an aim and a question. It must turn one into the other.

**Audience.** The same non-security CS examiner who read ¶1–¶2. They now
know what an APT is, what MTD does and what it is for. They do not know
how MTD is tested, and have no reason yet to doubt that it works.

**Purpose (CARS M2, the niche).** The claim is that whether MTD achieves
its aim against an attacker like Volt Typhoon has not been measured,
because evaluations test it against simulated attackers that have
nothing for MTD to take. The paragraph closes on why that attacker is
hard to build. The examiner should finish it asking the RQ themselves.

**The wisdom it has to surface.** A simple attacker is not just
unrealistic; it cannot show the value MTD claims. MTD's value is making
the attacker's reconnaissance and stolen credentials go stale, and an
attacker that carries none forward has nothing to lose
(alshamrani2019 Sec. IV-C-2-B, as ch3 §3.3.3 uses it). That is the step a
reader would not supply for themselves.

### 14.2 The shape: claim first, then the chain of reasons

Two orders are possible:

- **Build-up (funnel):** MTD is tested in simulation → with a simulated
  attacker → those attackers are simple → so the aim is unmeasured. The
  gap arrives in the fourth sentence.
- **Claim first (recommended):** the gap as S1, answering ¶2's "aims"
  directly, then the reasons. This closes the ¶2→¶3 seam in the way the
  causal-link opener closed the ¶1→¶2 seam in the cold-reader rounds (§13.1),
  and it follows voice.md's claim-first rule.

The "why hard" step comes last, not before the gap, because its two
halves map onto SQ1 (capture from reports) and SQ2 (make it run in the
simulator). The RQ block then lands on the reader's own question.

One paragraph, not two: the ruled budget is 130 words, and splitting it
would make the gap and its difficulty read as separate points.

### 14.3 Slots (about 130 words, five sentences)

| Slot | Job | Facts / citation | Ceiling |
|---|---|---|---|
| S1 | The gap, as the answer to ¶2's "aims" | ch3 §3.3.3: performance against an attacker with a foothold "remains unmeasured" | Scoped: to the evaluations surveyed (forward ref Chapter 3), or to the field as the two surveys diagnose it. Never "nobody". An attacker *like* Volt Typhoon, never Volt Typhoon itself |
| S2 | How MTD is tested: in simulation, against a simulated attacker; the *attacker model* named here | cho2020: simulation is the dominant method; enterprise MTD "mainly validated based on simulation models" (Sec. IX-A) | "Attacker model" defined plainly in apposition (decision D14-1). The domain list (cloud, IoT, SDN …) is cut: it has no job here |
| S3 | What those attacker models lack: no reconnaissance or credentials carried from one stage to the next; no adaptation | jalowski2026 p. 8, "the most glaring flaw in the MTD literature" (quote option, D14-2); ch3 Table 3.3 | "Scripted" or "simple", never "weak" (seminar ruling: the baseline reaches more hosts sooner). No paper named as at fault |
| S4 | The wisdom: why that matters. An attacker with nothing to lose cannot show what MTD takes | alshamrani2019 Sec. IV-C-2-B | Reuse ¶2's exact words, *reconnaissance* and *stolen credentials* (one name per thing). "Cannot show", not "overstates" (overstating is ch3's claim, one step further than ch1 needs) |
| S5 | Why it is hard: threat reports say what an attacker did, not the order and preconditions a simulator needs; the simulator's attacker acts through a small fixed set of actions | ferraz2026 (CTI "routinely omits the sequencing, preconditions, and dependencies"); the action set is ch2 §2.2.3 | Callback to ¶1's advisory as the kind of report. *Timing* only if cited: ferraz does not carry it (D14-3). May split into two sentences if it runs past about 30 words |

**Cut, not in ¶3:** the "means exist next door" step (attack profiling,
Bland, Outkin). It is ch3's, and ¶5's approach shows it implicitly.

### 14.4 Decisions for Marc

- **D14-1: the name for the simulated attacker.** *Attacker model*,
  defined once here, pays forward to "APT attacker model" in ¶5 and to
  chapter 4's title. The alternative, *simulated attacker*, is plainer
  but gives ¶5 a second term to introduce. Recommended: attacker model.
  The *baseline attacker*, MTDSim's own, stays in ¶5 (§6).
- **D14-2: quote Jalowski or paraphrase.** The quote carries the field's
  own verdict at landmark strength, in six words. Recommended: quote.
- **D14-3: timing in S5.** It is true of the corpus (ch4's dwell times had
  to come from breach-report statistics), but no source is on hand for
  "reports rarely give timing". Drop it, or forward-reference ch4.
  Recommended: drop.
- **D14-4: "threat reports" or CTI in ¶3.** Plain "threat reports" keeps
  ¶3 at the abstract's level and calls back to ¶1. CTI is then defined at
  ¶5 or SQ1. Recommended: threat reports here.

### 14.5 Accepted and floated (2026-09-24): the second design

> MTD has been proposed as a defence against APTs (alshamrani2019), yet
> it is rarely tested against one. Most tests run in simulation, against
> attacker models far simpler than an APT (cho2020; jalowski2026). None
> of the recent attacker models reviewed in Chapter 3 fully captures an
> APT's persistence or its adaptation to the defender.

About 60 words, against the 130 budgeted.

**The first design (§14.2–§14.4) was rejected.** Marc's verdict: "a lot of
words for very little meaning". What failed:

- The opener was cryptic. "That advantage … like Volt Typhoon" hid that
  the subject is MTD against APTs.
- The inference chain was spelled out step by step, to the point of saying
  nothing.
- "Hard to build" contradicts the thesis, which builds one.

**The lesson for the remaining paragraphs:** one idea per sentence, with
the subject named outright (MTD, APTs) and nothing walked through that
the reader can infer.

**Consequences:**

- "Why it is hard" is out of ¶3. If kept, it lives in ¶5 as the
  approach's answer (analyst-curated Attack Flows), never as difficulty.
- The reconnaissance inference is left to the reader. ¶2 sets it up and
  S3 triggers it.
- D14-1 through D14-4 are resolved:
  - "attacker model" is used without a definition;
  - Jalowski is not quoted;
  - no timing;
  - no CTI in ¶3.
- The ~70 words saved return to the chapter budget.

## 15. The RQ block (¶4): structure ruled and floated (2026-09-24)

**The convention.** Every authority agrees on three things:

- one question, stated explicitly, straight after the problem (Evans,
  Gruba & Zobel; only 5 of 10 computing PhD introductions do so, per
  Soler-Monreal);
- the sub-questions as a labelled list that later chapters key to;
- a link from the gap to the question.

Typography is house choice. Boxes are rare, and the grey box was removed
on 2026-08-21.

**The ruled form (Marc):**

- ¶3 closes on "This gap motivates the research question of this
  thesis:".
- The RQ is displayed: indented and italic, with no box and no "RQ" label.
- "The question decomposes into three sub-questions:" follows.
- SQ1–SQ3 stay as the labelled list.

This overturns the 2026-08-21 "RQ as prose" ruling, on layout only. The
First/Second/Third scaffolding stays cut. Marc's literature review
displayed its RQ after "These observations motivate …", and it scored 77.

**Also ruled:** bare acronyms in the RQ (MTD and APT are defined in ¶1
and ¶2).

**Next: the wording, Marc's feedback first.** The §6 fixes are still open:

- "APTs" or "APT attackers" (the title says "APT attackers");
- "How can" (design) against "How does" (empirical);
- only vocabulary the reader already has (no "attack profiles", "campaign
  intelligence", "traverses the captured structure" or "inherited
  scripted attacker");
- "attacker model", never "attack model";
- where phase one of the evaluation lands (SQ2, or SQ3 widened).

### 15.1 Evidence for the wording (2026-09-24; two surveys)

**The corpus.** 13 documents in `docs/sources/` state explicit RQs.

- **Lead-in.** Nearly all say "the following research questions".
  Ferraz uses the motivation form: "This framing motivates the research
  questions of this study:".
- **Number and layout.** Two to four RQs, as a displayed list with labels.
- **Question forms.**
  - Design questions open "How can / How do we" (Ferraz RQ2, Rahman RQ1,
    Chen), and the next question applies what was built (Rahman RQ2).
  - Comparisons are carried either by "How does X compare" or by a
    hypothesis (Ferguson-Walter H1–H4; Holm RQ3 becomes H1).
- **Answering by label.** Seven documents answer each RQ by its label.
- **One main question with sub-questions is rare.** Bland nests 1.1 and
  2.1; Bompos, an NPS MSc thesis, has a primary and a secondary question.
- **Closest MTD match.** Torquato 2022 (ISSRE, MTD by stochastic Petri
  net).

**The advice** (verified unless marked):

- **Question type, result and validation go together.** Shaw 2003,
  Table 1: "How can we do/create … X?" is a development question, and
  "How does X compare to Y?" is an evaluation question (p. 727). The type
  must match its result and validation (pp. 733–734). Terms must be
  defined and used consistently (p. 730).
- **Undefined terms make a question vague.** Easterbrook et al. 2008:
  "efficiency (measured how?)" (p. 3). Causality-comparative questions
  take the form "Does X cause more Y than does Z?" (p. 4). Design
  questions presuppose the knowledge questions have been answered
  (pp. 4–5).
- **Design problems and knowledge questions must be told apart.**
  Wieringa 2009, [G1]: stating a design problem as a knowledge question
  "is bound to create methodological trouble" (p. 1). The design-problem
  template and "(re)design a research instrument" come from the 2016
  slides.
- **Scope what can be tested.** Zobel 2004: a question must be scoped
  to what can feasibly be tested, and vague claims fail (p. 171). A
  hypothesis may be "whether a proposed method is fit for a certain
  purpose" (p. 170).
- **Hypotheses are optional.** Melbourne: "Not all research has a
  hypothesis".
- **Sub-questions stay inside the main question.** Utrecht: they stay
  "inside the outer walls", together cover all of it, and are ordered so
  each answer feeds the next. No yes/no questions, and no suggestive
  wording (also Monash).
- Booth et al. was seen only in secondary quotation. Evans, Gruba &
  Zobel's RQ advice is still unverified.

**Consequence for ch1.** SQ1 and SQ2 are design problems: they build
the instrument. SQ3 is the knowledge question that answers the RQ. That
nesting is what makes the three jointly sufficient.

### 15.2 Ruled and floated (2026-09-24)

> The question breaks down into three sub-questions:
> SQ1 How can the behaviour of APT attackers be recovered from published
> threat reports?
> SQ2 How can the recovered behaviour be executed as an APT attacker
> model inside an existing MTD simulator?
> SQ3 How does MTD perform against the APT attacker model compared with
> the simulator's baseline attacker?

**Why each is worded as it is:**

- **Recovered, not captured.** This is Marc's term.
- **The SQ types match the evidence** (Shaw). SQ1–SQ2 are design
  questions ("How can"). SQ3 is the evaluation question, and it opens in
  the RQ's own words.
- **The chain between SQs uses names, not pronouns,** so each SQ reads
  alone when ch5–ch7 quote it.
- **SQ3's two arms are the §5.2 heading's names.** "Baseline" explains
  itself, and ¶5 defines it.
- **"That persists and adapts" is cut from SQ2.** Naming two of the
  criterion's eight properties is an arbitrary subset, and it made SQ2
  carry four things.

**Ruled with it:**

- the RQ stays broad (the SQs and ¶6's scope sentences fence it);
- "perform" is defined in ¶5;
- phase one (no defence) answers SQ2, as the check that the model
  behaves differently;
- no hypotheses.

**Owed downstream:**

- ¶5 must define the baseline attacker and "perform", and answer SQ1–SQ3
  in order.
- C1–C3 key to these wordings, and the conclusion answers them in the
  same words.
- The SQ list hyphenates "re-ports" and "sim-ulator's". This is last-week
  typesetting polish.

## 16. Paragraph 5: the approach (2026-09-24; design for Marc's acceptance)

### 16.1 Context, audience, purpose

**Context.** The reader has just read the RQ and SQ1–SQ3. The block leaves
three things unexplained: *published threat reports* (SQ1), the *baseline
attacker* (SQ3) and *perform* (RQ, SQ3). Each was ruled to be defined here
(§15.2). The reader's next question is "how will you answer that?" That
question is CARS move 3, announcing the research and outlining its method
(Swales 1990).

**Audience.** The same examiner as in §1: not an MTD specialist. ¶5 is the
first paragraph at chapter 2's altitude (the abstraction gradient, §1). By
now the reader has chosen to go on, so field terms may enter, each defined
once in the clause that introduces it: CTI, MITRE ATT&CK, attack profile and
operational objective, MTDSim (brown2023), the baseline attacker. The term
budget's never-list holds: no layer names, no GSPN notation, no metric
acronyms, no "movement".

**Purpose.** To answer SQ1–SQ3 in order, one pass the reader can hold, with
a pointer to the chapter that carries each answer. Together the three
answers state the thesis's method. Then one line positions it against the
field (flag C4): simulation is kept on purpose, and only the attacker is
changed.

### 16.2 Proposed structure (six slots, about 130–140 words)

| Slot | Job | Facts | Ceiling |
|---|---|---|---|
| S1 (SQ1) | Bind "published threat reports" to CTI and name the source | Analyst-curated Attack Flows of APT campaigns, written in MITRE ATT&CK's vocabulary (full name + citation, its first use) | No L0; "recovered" is SQ1's verb, used again here |
| S2 (SQ1) | What is recovered from them | Attack profiles: the campaigns' behaviour grouped by operational objective (Ch. 4) | Profiles are the behaviour; do not claim they are accurate |
| S3 (SQ2) | Executed where, and beside what | Run in MTDSim (brown2023) as the APT attacker model. The baseline attacker is defined here: MTDSim's scripted attacker. Same action set, same network, same defences (the ch4 opener's ruled relation) | No "replaces", no "beside"; no Petri net (see D2) |
| S4 (SQ2 check) | Phase one | Both attackers, no defence: does the APT attacker model behave differently? (Ch. 5) | Phase one answers SQ2 (§15.2) |
| S5 (SQ3) | Phase two, and define "perform" | Both attackers under MTD's deployment strategies across a range of intervals. Perform = what the attacker achieves, and how much a defence takes from it (the outcome and effectiveness classes; Section~\ref{sec:evaluation-metrics}) | No metric names or acronyms; no MTDShield by name (D4) |
| S6 (positioning) | Why this design is fair to the field | Keeps simulation, the field's dominant method (cho2020), and changes only the attacker, so any difference is the attacker's | Marc dictates this line (flag C4) |

The scope sentences stay in ¶6 (§4: ¶7 folds into ¶6).

### 16.3 Decisions for Marc

- **D1. "38".** Recommendation: keep it. It answers "how much evidence?",
  which passes the decorative-number rule. The alternative is "a corpus of
  analyst-curated Attack Flows".
- **D2. Name the Petri net?** Recommendation: no. The reader has not met the
  term, it needs a definition clause, and the chapter pointer carries it.
  SQ2 is answered by *where it runs and what it shares*.
- **D3. Key the SQs in the text?** Options: a trailing tag,
  "(\ref{sq:capture}; Chapter~\ref{ch:...})", or no tags, leaving the keying
  to the contributions list. Recommendation: no tags. Answering in SQ order,
  with SQ1's own verb, is enough keying, and the contributions list will
  carry the explicit keys.
- **D4. MTDShield by name?** Recommendation: no. "Every deployment strategy
  in MTDSim" covers it, and it would be one more undefined name.
- **D5. "Why hard".** Recommendation: drop it as a claim. The thesis does the
  recovery, so calling it hard contradicts the thesis (memory: dense over
  walked-through). "Analyst-curated" in S1 carries the fact that reports need
  curation before a simulator can use them.

### 16.4 Ruled, cold-read and floated (2026-09-24)

**Ruled (Marc).** The structure of §16.2 and all five recommendations of §16.3:
38 kept, no Petri net, no SQ tags, no MTDShield, no "why hard". ATT&CK is
dropped from ch1; its first use is chapter 3.

**The drafts.**
- **Draft 1.** The last two sentences read as lost. The positioning line
  ("keeps the field's usual method") answered a question nobody had asked.
- **Draft 2.** Checked by two cold readers, each a CS examiner and not an
  MTD specialist.
  - Reader 1 found that nothing said what makes the APT attacker model
    different from the baseline attacker. The model read as the baseline
    attacker renamed, which left SQ2 unanswered.
  - Reader 1 also found that "any difference comes from the attacker alone"
    read as a causal claim about unreported results, and that "compared with
    no defence" clashed with SQ3's comparison.
  - Reader 2 restated the difference correctly from memory once the
    shared-actions-but sentence was added. Reader 2 then flagged that
    "attack profile" was never said, that "It" was ambiguous, and that the
    attribution clause spelled out a controlled comparison.
- **Draft 3.** Marc accepted sentences 5–9 as read. He sent sentences 1–4
  back as clunky:
  - "such reports" was a back-reference;
  - CTI was defined twice (once as reports, then the flows as reports
    again);
  - the hand-drawn point was buried;
  - the profile sentence had too many clauses;
  - the step from flows to profiles was unclear.
  The redraft names every noun outright and defines CTI once. A flow is
  one thing, a hand-drawn graph. The combine-then-split step gets its own
  sentence, as does what a profile records.

**Floated** into `dissertation.tex` after the SQ list (build clean, 88 pp.).
FLAG C4 is discharged: "same network and under the same defences" carries
the positioning concretely, and ¶3 has already said that most tests run in
simulation.

**Lessons (for ¶6 and the contributions list).**
- A back-reference ("such", "these", "it") is a clarity cost. Name the noun.
- Every term an SQ uses needs one sentence that defines it, and only one.
- Put cold readers on the whole ¶1–RQ context, not the paragraph alone.
- An explicit contrast ("shares X, but Y") is what lets a reader restate
  the contribution.

**Left out on purpose** (the readers raised them, but they belong later):
- counts of profiles and defences, and the statistics (chapters 4–5);
- whether 38 flows is enough (chapter 6);
- bias toward reported attacks (¶6 scope or chapter 6 limitations).

## 17. Paragraph 6: preliminary findings, value and scope (2026-09-24; design for Marc's acceptance)

### 17.1 Context, audience, purpose

**Context.** The reader has just finished ¶5, the method, which ends by
defining performance. They now ask what we found and what it means. Before
the contributions list turns the answers into claims, they also ask what we
are *not* claiming. This paragraph is §4's rows 6 and 7 folded together:
the findings, the value, then scope.

**Audience.** The same examiner as §1, at chapter 2's altitude. There are no
metric acronyms and no numbers (the headline is a direction, not a number).
The only terms used are the ones ¶1–¶5 have already defined.

**Purpose.**
- **Announce the findings.** Computing introductions do: 70–75 % of CS and SE
  article introductions do (§2), and Zobel says a paper "isn't a story in
  which results are kept secret" (p. 58).
- **State the value** in one sentence. This is Marc's "discussion points", as
  §3 item 3 ruled.
- **Fence the scope** before the examiner does (9 of 10 computing theses do,
  per Soler-Monreal et al.).
- **Ruled (§11):** the results go in as a visible, flagged placeholder,
  worded at the preliminary tier. Marc revisits them once chapters 5 and 6
  are done.

### 17.2 The evidence available today (100-seed corpus; re-check at 1 000)

- **Phase one** (`tab_5-2-1a_unopposed_summary`). With no defence, the APT
  attacker model reaches the target in 5–17 % of runs (by profile) against
  the baseline attacker's 58 %. It compromises 14–20 % of hosts against
  49 %, and it takes about three times as long per compromise.
- **Phase two** (`tab_5-3-2a_orderings`).
  - The host-layer defences (IP shuffle and the two topology shuffles) hold
    back the APT attacker model most. The service-layer ones (service
    diversity first) hold back the baseline attacker most. The family
    contrast flips sign between attackers at both intervals: Cliff's δ
    −0.61 against 0.93 at 200 s, and −0.19 against 0.25 at 2 000 s.
  - The two orderings barely correlate: ρ = 0.08 at 200 s and 0.13 at
    2 000 s.
  - This is tier 3 of the seminar ceiling. It is the same direction the
    abstract already states under "Preliminary".

### 17.3 Proposed structure (five slots, about 100 words)

| Slot | Job | Content | Ceiling |
|---|---|---|---|
| S1 (SQ2 check, phase one) | What the model does with no defence | It reaches fewer hosts and its target less often, and more slowly, than the baseline attacker | "Preliminary". Never "weaker" or "more realistic": the baseline is *simplified*, not weak |
| S2 (SQ3, phase two) | Which defences hold back which attacker | Defences that move the network's addresses and layout hold back the APT attacker model most. Those that change its software hold back the baseline attacker most | The direction only, with no ranks and no numbers. The abstract's parallel: "IP shuffling and topology shuffling … service diversity" |
| S3 (value) | What it means for MTD evaluation | The defence an evaluation recommends depends on the attacker it assumes. Or the abstract's closer: "a case for evaluating MTD against attacker models grounded in documented behaviour" | Marc found "the recommended defence changes with the attacker" vague three times in the seminar. Decision V below |
| S4 (scope 1) | What is evaluated | Existing defences, in simulation; no new defence is proposed | — |
| S5 (scope 2) | What the attacker is | Behaviour documented across many campaigns, not any one group such as Volt Typhoon | Guards ¶1: an examiner will otherwise read Volt Typhoon as the scenario scored |

**Placeholder mechanics (§11 ruling).** S1–S3 are written as real
sentences opening "Preliminary results show", as the abstract does. A
visible tag, `[re-check at 1 000 seeds]`, and a tex comment naming the two
tables sit beside them. S4–S5 are not results, so they are final text.

### 17.4 Decisions for Marc

- **V. The value sentence.** Recommendation: echo the abstract's closer.
  That keeps chapter 1 and the abstract parallel, and it answers the RQ at
  the level of evaluation practice. The seminar found the alternative vague.
- **P. Keep phase one (S1)?** Recommendation: yes. SQ2's check needs an
  answer, and it is the phase the contributions list's C2 rests on. Cutting
  it saves about 20 words.
- **Sc. Which two scope items?** Recommendation: simulation and existing
  defences (S4), and not a named group (S5). "Nothing in MTDSim detects the
  attacker" (so stealth is measured but nothing reacts) and the bias toward
  reported attacks go to chapter 6's limitations.

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
