---
status: open                  # 2026-09-25: C1 entries and ALL blocking B entries APPLIED on Marc's rulings ('fix up all the facts ... all the contradictions'); the minor (M) entries beyond C1 remain for a later pass
created: 2026-09-25
companions: 2026-09-22_ch4_overview_figure_family.md (Part B, the term sweep), ../workflows/terminology.md, ../workflows/voice.md, .claude/skills/voice-pass/SKILL.md
---

# Chapter 4 mark-risk ledger — what is left after the one-term sweep

**Goal.** Clear chapter 4 of what would cost marks in a method chapter:
placeholders in live prose, the chapter contradicting itself or its floats,
overclaims, wrong cross-references, informal register, notation collisions.
These change the argument or the prose voice, so each is Marc's to rule (or to
dictate afresh); nothing below is applied unratified.

**Already applied (2026-09-25, commit after this file's creation):** every C1
one-term entry — B11 (Figure 4.5 caption: Petri-net band, timed/immediate
transitions), B12 (*edges*, not *directed flows*, in the attack graph), B13
(*the APT attacker model*; *a richer set of actions*), B21 (*add* the overlay,
not *join*), B22 (*numbered edges*), B23 (*deployment*, not *mutation*, ×4),
M1 (*actions*; the choice of the next tactic), M2 (*decision place*), M3 (*base
weights* $ throughout), M4 (repo version strings out of both mapping
captions), M6, M7 (*defence mechanism* is the ratified term: Figure 4.1's
Defence box and four prose sites, three of them in chapter 2), M8, M9, M10,
M11. Also *the substrate* → *the simulator* in Table B.5's caption. M47
(Table B.2's *class* and `objective_…` keys) is NOT yet applied: it is a
generator change in the classification-audit table, left for the next pass.

**Applied 2026-09-25, second pass (Marc: "fix up all the facts, all the
contradictions ... a nice clean fix"):** the 29-flow weighting disclosed where
$w_c$ is defined (§4.3), with the flow set renamed $\mathcal{A}_c$ (B9); the edge
weight defined as the number of attack flows that drew it (§4.1) and Appendix
Figure B.1d regenerated to match; a step within one tactic is not an edge (the
dwell covers it; `petri/build.py` drops it), so the attack graph is 122 edges
everywhere (B.1d, Figures 4.2–4.3, the nets); Wizard Spider for Conti and the
motivation overclaim (B7); the stochastic and exponential sentences (B8, B24);
B3, B4, B5, B6, B10 (σ, declared), B14, B15 (checked against commit 8f2e34ad:
the join calls MTDSim's own actions one at a time and supplies their
duration), B16, B17, B18, B19, B20; the two must-carry caveats placed from
their ruled wording (M46); the §4.4 disruption placeholder and §4.5's
placeholders commented out with restore notes (§4.5 shows its heading and the
metrics table until the definitions handoff lands).

**Was owed (before the second pass), most costly first:** B1–B2 (placeholders: §4.4's disruption paragraph
and all of §4.5 — comment out before anything is shared); B3, B4, B6, B16
(self-contradictions); B5 (wrong cross-reference); B7, B8 (overclaim, a wrong
definition of *stochastic*); B9, B10 (notation collisions: $, $); B15 (the
"inherited unchanged" caption vs "we made all of the actions independent" —
check the code before ruling); M46 (the ruled Table 4.2 sentence never landed).
Line numbers below are as of the screen and drift with edits.

**BLOCKING, found by the §4.2 figure scrutiny (2026-09-25; verified in code):**
the runtime reads the `operator_dedup` weights
(`src/mtdsim/l3_simulation/movement/net.py`, `PRIMARY_VARIANT`): one
representative attack flow per operator, 29 flows, not 38 (c₁ 14, c₂ 6, c₃ 5,
c₄ 4). Under those weights 8 of the attack graph's 122 edges (16 of c₁'s 90)
never fire. `dissertation.tex` mentions neither deduplication nor 29 flows, so
the method as written is not the method as run. Marc to rule: disclose the
deduplication in §4.2/§4.3 (one sentence and its reason: one operator's
repeated incidents should not outvote the corpus), or run on the raw weights.
The §4.1/§4.2 figures draw raw counts ("attack flows that drew the edge"),
which is true as labelled either way.

**Added 2026-09-25 from the §4.2 figure build (data checked against the text):**
- §4.2 "Three of the seven flows in the double extortion profile come from one
  APT group, Conti": `classification.csv` attributes the three to G0102, which
  ATT&CK names Wizard Spider; Conti is its ransomware. Say "Wizard Spider, the
  operator of Conti ransomware" or check the source reports.
- "The profiles share the tactics" is only roughly true: c₂ has no
  defense-impairment or exfiltration techniques, c₃ no defense-impairment, c₄
  no exfiltration or impact. Say "they differ in which tactics and edges they
  contain".
- Each profile's Petri net carries structure-only transitions that none of its
  own flows back (c₁ 19, c₂ 30, c₃ 25, c₄ 16 at raw weight zero): the profile's
  technique subgraph is the attack graph restricted to its techniques. They
  never fire (weight zero), but "built only from its own flows" should say
  "weighted only by its own flows" to stay true.
- Confirmed by the build: 19/7/7/5; "19 of the 38 attack flows land in a
  different attack profile"; 88 % of technique edges from a single flow (419 of
  478); reconnaissance in 10 of 38 flows.
- **The attack graph's edge weight is counted two ways (needs a ruling).**
  §4.1 says "weighted on how many times it is observed in the corpus".
  Appendix Figure B.1d (`tools/gap_appendix_figures.py`) sums observation
  counts (heaviest edge 26); the model's weights
  (`src/mtdsim/l3_simulation/petri/weights.py`) and the new §4.1/§4.2 figures
  count distinct attack flows (heaviest 11). Both are called "the attack graph".
  Recommended: rule "the number of attack flows that drew the edge" (what the
  model uses), reword §4.1 to say so, regenerate B.1d.
- Only 36 of the 38 flows contribute edges: `conti_cisa_alert` and
  `conti_pwc` draw techniques but no edges. "The 38 usable attack flows" is
  true for techniques; say so where the edge count matters.
- §4.3 (l.~4508) "carries every pair the profile's Section 4.2 subgraph
  admits" points back to an object neither §4.2 nor its figure defines (the
  profile as the attack graph induced on the profile's techniques). Either
  define it in §4.2 in one clause, or say in §4.3 "every tactic pair the
  attack graph has among the profile's tactics".
- Across pairs of flows: 10.5 % of the 630 pairs share any technique edge,
  55.1 % share a tactic edge — a cleaner T2 statistic for §4.1 than "much
  greater coverage", if Marc wants a number.

---

# Chapter 4 "APT attacker model": reader-overhead and mark-risk screen

2026-09-25. READ-ONLY screen of `docs/thesis/dissertation.tex` l.3917–5459 (prose, headings, captions; `%` lines skipped except as a do-not-re-flag list), plus the ch4 floats the captions point at (fig_4-0a, fig_4-3a, fig_4-4a/b/c, tab_4-4a, tab_4-5a, and the appendix tables the body points to where a number had to be checked). Nothing in the tex was changed.

Treated as fixed (Marc, 2026-09-25): the one-term list matching Figure 4.1 (attack flows, the attack graph, attack profiles c1–c4 and c_agg, Petri net, the join, MTDSim, actions, tactic-to-action mapping, APT attacker model, baseline attacker, evaluation metrics), the five headings, L-labels retired, and "MTDSim runs either attacker". Honoured do-not-re-flag rulings from the comment trail: "our existing simulator" (l.4163); "eight axes" (l.4139; the *properties* row is still PROPOSED in terminology.md, which is a pending ruling and not a finding); "We ruled out attack graphs, which we already have"; the SPN/GSPN/DSPN clause; the zero-or-one constraint sentence; the 45.0 s / 0 s worked examples; the three-citation sentence; "plausible"; "the simulator we are inheriting" (penalty paragraph).

Note on the registry: `terminology.md` still lists *verb* / *tactic-to-verb mapping* and *the profile net* as canonical. Today's rulings replace them. The registry rows need flipping, and that is outside this read-only screen.

Categories: **C1** one-term rule breach · **C2** invented term / acronym / notation · **C3** used before defined, or defined twice differently · **C4** examiner mark risk (unsupported claim, hedge, informal register, placeholder, wrong cross-reference, contradiction, process narrative).
Priority: **B** blocking (the reader cannot follow, or a mark is at risk) · **M** minor.

## Counts

| Category | Blocking | Minor | Total |
|---|---|---|---|
| C1 one-term breach | 6 | 10 | 16 |
| C2 invented / acronym / notation | 3 | 8 | 11 |
| C3 before-defined / defined twice | 2 | 5 | 7 |
| C4 mark risk | 13 | 25 | 38 |
| **Total** | **24** | **48** | **72** |

(Counted by each entry's first-listed category; seven entries carry a second one: B10, B18, B20, M4, M11, M37, M47.)

---

## Blocking (B), ordered by cost

| # | Line | Quoted text | Cat | Why it costs | One minimal fix | Conf. |
|---|---|---|---|---|---|---|
| B1 | 4894–4902 | "\emph{[Placeholder --- what a disruption does to the APT attacker model, explicit and emergent, owed for Section~\ref{subsec:aio-disruption}. ...]}" | C4 | This is a bracketed placeholder in live prose in the method chapter, and §5 reads against it. Examiners read an unfinished paragraph as unfinished work. | Dictate the paragraph from the placeholder's own content, or comment it out before the build goes to anyone. | high |
| B2 | 5320–5357 | "\emph{[Placeholder --- delete on drafting. The metrics ...]}", "\emph{[Definitions owed: relative tactic occurrence; attack path variation (APV); ...]}" (×4) | C4 | §4.5 is all placeholder. Chapter 5 reports metrics (NCR reduction, time lost per MTD deployment) that the method chapter never defines. The "defined once, here" contract is unmet. | Draft the three subsections. Until then, comment the four placeholders out so that no bracketed text is typeset. | high |
| B3 | 4549–4550 vs 4882–4885 | "A timed transition may also be cut short by an MTD mutation, which returns failure." vs "A mutation that lands during a dwell-only tactic cuts the dwell short ... no verdict to route on" | C4 | The two passages contradict each other. §4.3 says an interrupted timed transition returns *failure*. §4.4 says an interrupted dwell-only tactic returns *none*, and every tactic has a timed transition. A careful reader cannot tell which verdict routes. | 4549: "... cut short by an MTD deployment, which returns failure if an action was in flight (Section~\ref{subsec:runtime-mechanics})." | high |
| B4 | 5201–5205 (+ Table 4.1 l.4644) | "scaled down by a rate, the same rate whether the jump is forward or a fall back; ... The two rates and the floor are the only numbers" | C4 | The passage gives one rate and then counts two. Table 4.1 lists γ (forward) and δ (backward) as separate decays. App. B.6 declares γ = δ = 0.25. The reader cannot reconcile one rate with two. | "... scaled down by a rate, one forward and one backward, declared equal; ..." | high |
| B5 | 4502–4504 | "$M_0$ places one token on reconnaissance when the pre-intrusion overlay of the next paragraph is in place" | C4 | This is a wrong cross-reference. The next paragraph is the verdict-conditioned extension (l.4517). The overlay is defined four paragraphs later, after Table 4.1 (l.4658). The term is also used before it is defined. | "... the pre-intrusion overlay (defined below Table~\ref{tab:gspn-notation}) ..." or a `\label` on that paragraph and a `\ref`. | high |
| B6 | 4542–4543; 5175–5177 | "every flow in the corpus is a campaign that got through"; "these reports only capture success --- there is survivorship bias" | C4 | The claim is contradicted by the chapter's own partition: c4 is "no realised objective" (5 flows, l.4329). An examiner will set the two side by side. "got through" is also informal. | 4542: "every flow in the corpus records steps that succeeded, so the base proportions already are the success policy." (5176 similarly: "these reports record the steps that succeeded".) | high |
| B7 | 4345–4351 | "this shows that the motivation of these APT attackers typically translates to similar objectives. ... so we are not surprised there." | C4 | This overclaims from a handful of flows ("shows", "typically"). It also contradicts l.4299, "Motivation is something that we cannot ascertain." "not surprised there" is speech. | "... go to the same attack profile, which is consistent with a stable objective per APT attacker; three of the seven double-extortion flows come from Conti, which is known for double extortion." | high |
| B8 | 5086–5087 | "stochastic means it can be measured, but it cannot be predicted" | C4 | The definition is wrong. A stochastic process is predictable in distribution, and "measured" is not the property. A marker in probability or simulation will catch it at once. | Cut the gloss: "... but the behaviour of APT attackers is stochastic." | high |
| B9 | 4500 vs 4522 | "$F_c(p \to q)$ is the set of flows in $c$ that draw the pair" vs "$F = \{F_v : v \in V\}$" and $F_{\text{failure}}$ | C2 | The letter F names two unrelated objects, a set of attack flows and the verdict factors, within 25 lines of each other in the formal definition. $F_{\text{failure}}$ then carries the load in §4.4 and chapter 5. | Rename the flow set only, e.g. $\mathcal{A}_c(p \to q)$ in Eq.~\ref{eq:base-weight} and l.4500 (two sites). | high |
| B10 | 4670–4671 (+ Table 4.1 l.4638) | "a share $s = 0.1$ otherwise, the observed weights scaled to $1 - s$" | C2 / C4 | This is a declared number with no justification and no pointer. It is not among the declared inputs of Table C.0 ("the three inputs"), so it is neither argued nor swept. *s* also names the lifecycle stage in App. B.6 ($\Delta = s(b) - s(a)$, tab_B-6a "$s$ & Stage"). | Add one clause of justification and a pointer, e.g. "$s = 0.1$, a declared value (Appendix~\ref{app:sensitivity})", and rename one of the two *s* symbols. | high (unjustified) / med (the fix) |
| B11 | 4848–4850 | "The profile-net band shows a fragment of one profile's net" | C1 | *profile net* is retired, and the figure itself labels the band **Petri net** ("one Petri net, a fragment"). The caption contradicts its own figure. | "The Petri-net band shows a fragment of one attack profile's Petri net" | high |
| B12 | 4247–4249; 4272–4273 | "88\% of the technique-to-technique directed flows came from a single incident"; "the tactic-to-tactic directed flows had much greater coverage"; "we will later have to draw these flows in" | C1 | *flows* is used here for edges or transitions, in the section that fixes *attack flows* as the 38 documents. "88% of flows came from a single incident" then reads as a claim about the corpus of documents. | "directed flows" → "edges" (×2); "draw these flows in" → "draw these transitions in (Section~\ref{sec:petri-formalism})". | high |
| B13 | 4517–4518; 4961; 4963–4964 | "The attacker model of this dissertation needs them"; "the attacker model that we produce can only be as good"; "a stronger underlying attacker model can be built that operationalises all of MITRE's tactics" | C1 | The first two name the APT attacker model by the generic term. The third uses the same generic term for a different object, an executor with a richer action set, so the reader loses which "attacker model" is meant. | "The APT attacker model needs them"; "the APT attacker model can only be as good"; "a richer set of actions can be built that operationalises ..." | high |
| B14 | 4749–4754 | "The question for this section is: ... how do we join this to MTDSim? The Petri nets can act as inputs, but like source code they cannot run against the simulator on their own. A Petri net can be run on its own, but that produces a timeline ... The timeline is a dead end" | C4 | The passage opens on a meta rhetorical question. It then says the nets "cannot run ... on their own" and, one sentence later, "can be run on its own". "dead end" is used here as a metaphor, and l.4919 uses it as a structural term (two senses in one section). | Cut the question sentence. Change "cannot run against the simulator on their own" to "cannot run against the simulator without a join", and "The timeline is a dead end:" to "Such a run is one-way:". | high |
| B15 | 4805–4806 vs caption 4854–4855 | "We made all of the actions in MTDSim independent of each other" vs "the MTDSim band is inherited unchanged" and l.4770 "we adopt the existing actions" | C4 | It is unclear whether MTDSim was changed. The body says we made the actions independent; the figure caption says MTDSim is unchanged. An examiner will ask what was modified, and whether the baseline attacker still runs on the same actions. | "The join dispatches each MTDSim action on its own, outside the baseline attacker's phase order, so that ..." (confirm against the code that the action implementations are untouched). | med |
| B16 | 4999–5004 vs Table 4.2 and tab_B-4a | "the low-and-slow family at ten times it ... We then chose a band around each of the four: half to twice the value, and a quarter to four times for the low-and-slow family ... four free timing values rather than 15" | C4 | The chapter's own table shows 22.5 s for Execution and Defense impairment, a value the body's four families cannot produce (App. B.4 applies a per-tactic ×0.5 multiplier). App. B.4's bands are per tactic ([0.1, 2], [0.1, 4], [0.25, 4], [0.1, 5]), not per family as the body says. A reader who checks Table 4.2 against the text finds it does not add up. | Add one clause after "terminal acts": "with a per-tactic multiplier within a family and a per-tactic band (Appendix~\ref{app:dwell-derivation})"; replace the fixed bands sentence with that pointer. | med |
| B17 | 4243–4246 | "Once we had decided on Attack Flow as the preferred mode of CTI, we then had to decide what the correct resolution was (tactic or technique). That is why we decided to prioritise coverage at this stage, whereas in earlier stages fidelity was a large concern." | C4 | This is first-person process narrative, and "That is why" has no antecedent reason: the reason (88%) comes in the next sentence. The method convention is to state the design, then its justification. | "The node resolution (tactic or technique) trades fidelity for coverage; having chosen the input for fidelity, we chose the resolution for coverage." | med |
| B18 | 4307–4309 | "We are extrapolating the literature and saying the prefix is invariant, so we are going to treat the prefix of attackers as invariant and we are going to look at the terminal tactic" | C2 / C4 | *prefix* is never defined (the prefix of what: a flow's tactic sequence up to the objective?). The sentence says the same thing twice in speech register ("we are going to" ×2 is a standing [3b]). *terminal tactic* is also undefined at first use. | "Following \citet{alshamrani2019}, we treat the tactics before the objective as common to all APT attackers and classify each flow by its terminal tactic, the last tactic it reaches." | high |
| B19 | 4880–4881 (and caption 4859) | "But if they are on a dwell-only, there is no verdict" | C3 | *dwell-only* is used here, and in Figure 4.5's caption, before it is defined at l.5120 in §4.4.3. "they" has no antecedent, since the attacker is singular throughout. | "At a dwell-only tactic (one with no mapped action, Section~\ref{subsec:tactic-verb-mapping}) there is no verdict" | high |
| B20 | 4779; Table 4.1 l.4642; 5114–5116 | "the tactic-to-action mapping, $\varphi$" (used at l.4642, l.4779) ... "we are calling this the tactic-to-action mapping, $\varphi$" | C3 / C4 | The term and its symbol are used twice before the sentence that names them. "we are calling this" is the register the task names. The naming sentence is also redundant by then. | 5114–5116: "The tactic-to-action mapping $\varphi$ sends each tactic, a place of the Petri net, to at most one of the simulator's actions." | high |
| B21 | 4664–4665 | "we join it to the attack profiles to produce the executable Petri net" | C1 | *the join* is ruled as the name for the three declared inputs that connect the Petri nets to MTDSim. Here "join" names a different operation, overlay plus profile. | "we add it to each attack profile's Petri net" | high |
| B22 | 4807–4808 | "(the numbered joins of Figure~\ref{fig:runtime-loop})" | C1 | "joins" in the plural makes the ruled singular term countable. The figure numbers its *edges* (the caption's own word). | "(the numbered edges of Figure~\ref{fig:runtime-loop})" | high |
| B23 | 4549, 4882, 4935, 4950 | "an MTD mutation"; "A mutation that lands"; "the mutation schedule" (×2) | C1 | The ratified row (2026-09-02) is **deployment**: *MTD mutation* only inside Zhang's cited phrasing. Chapter 5 says "deployment interval", so the chapters disagree on the event's name. | mutation → deployment; "the mutation schedule" → "the deployment schedule" (4 sites). | high |
| B24 | 5085–5088 with 4452–4454 | "We are not claiming that the attacker dwell is exponentially distributed" | C4 | This reads as denying the model's own definition, since the GSPN fires timed transitions after an exponential delay by definition (l.4453). The intended claim, that the exponential is a modelling choice and not an empirical claim, is not stated. | "The exponential is a modelling choice, not a claim that attacker dwell is exponentially distributed; the behaviour of APT attackers is stochastic." | med |

## Minor (M)

| # | Line | Quoted text | Cat | Why it costs | One minimal fix | Conf. |
|---|---|---|---|---|---|---|
| M1 | 4151; caption 5144 | "shares the baseline attacker's action set, but its movement is dictated at runtime" | C1 | *movement* is retired, and *action set* is a variant of the ruled *actions*. | "shares the baseline attacker's actions, but its choice of next tactic is set at runtime by ..."; caption "one action of the action set" → "one of the simulator's actions" | high |
| M2 | 4479; 4598; 4633; fig_4-3a key | "one vanishing place $\hat{p}$" vs "the decision place $\hat{p}$" | C1 | Two names for $\hat{p}$. *vanishing* is defined at l.4467 for markings, not places. | 4479: "one decision place $\hat{p}$ for each (vanishing: left in zero time)" | high |
| M3 | 4540, 4606, 4637, 4671, 4864, 4885, 5171 | "corpus proportions", "base weights", "the base weight", "observed weights", "base proportions", "base transition weights are the recurrence values" | C1 | Six names for $w_c$. The reader has to work out that they are one object. | Hold **base weight** (Table 4.1's word) with $w_c$; re-key the other sites. | med |
| M4 | 4853–4855 | "(mapping \texttt{v2\_partial}, failure set \texttt{v4\_failure\_only})" | C1 / C4 | *failure set* is a variant of the ratified *failure matrix*. The two repo version strings break voice.md §e, which allows no internal codenames in `thesis/` (already a sweep-4 finding, 2026-09-22). | Delete the parenthesis. | high |
| M5 | 5143; 5287; tab_4-4a caption | "(\texttt{v2\_partial})"; "as committed (\texttt{v4\_failure\_only})"; "emitted from the declared catalogue (v0-uncalibrated)" | C4 | Internal codenames and repo vocabulary ("as committed", "emitted") on the dissertation's surface. | Delete each parenthesis and "as committed"; in tab_4-4a, fix the generator (`tools/dwell_catalogue_tables.py`) and do not hand-edit. | high |
| M6 | 4850, 4851, 4865 | "a timed dwell, filled bars the weighted moves"; "the token fires the chosen move" | C1 | The caption uses *move* for immediate transition and *timed dwell* for timed transition, while Figure 4.3's key and Table 4.1 use the formal words. | "the hollow bar a timed transition, filled bars the immediate transitions"; "fires the chosen immediate transition" | med |
| M7 | 4774 (and Fig. 4.1 box) | "so that the MTD mechanisms can be evaluated" | C1 | The ratified row (2026-09-07) is *defence mechanism*, but Figure 4.1's Defence box reads "MTD mechanisms". This is a conflict between a registry row and the figure. **Surfaced for Marc, not resolved.** | Rule once, then align either the prose (l.4774, l.4165) or the figure. | med |
| M8 | 4163 | "We are distilling that behaviour into structured representations" | C1 | Paraphrases the figure's named artefacts (attack graph, attack profiles, Petri nets) with a new phrase. | "... into attack profiles and their Petri nets" | med |
| M9 | 4317; 4324 | "we could not rely on the objective tactic alone"; "land in a different category" | C1 | *objective tactic* is a variant of *terminal tactic* (l.4309, l.4321). *category* is a variant of attack profile. | "the terminal tactic alone"; "a different attack profile" | med |
| M10 | 4992 | "What we could take from the six original actions" | C1 | The ratified simulator row drops *original* / *inherited* as qualifiers. | "the six actions" | med |
| M11 | 5001 (+ tab_B-4a "Objective execution") | "the objective family at eight times it" | C1 / C2 | *objective* is the attack profiles' partition word, and the appendix names this family "Objective execution". | "the objective-execution family" | low |
| M12 | 4386–4387 | "We needed a data structure to pipe in the attack profiles as an input, and this is what the Petri nets provide." | C4 | "pipe in" is informal. | "The attack profiles need an executable form; Petri nets provide it." | low |
| M13 | 4681 | "the exponential defence of the dwell times" | C2 | In an MTD dissertation, "defence" reads as a moving-target defence. The phrase is not defined anywhere in the chapter (the registry calls it the justification of the draw). | "the justification of the exponential draw" | high |
| M14 | 4601–4602 | "(a)~The gadget in general. (b)~The same gadget on initial access" | C2 | *gadget* appears only in the caption and is never defined or used in the body. | "(a)~One tactic in general. (b)~The same construction on initial access" | med |
| M15 | 4608–4609 | "which is the foothold-gate rule of Section~\ref{subsec:failure-matrix}" | C2 | The term is defined only in a caption. The cited section names no such rule (it says "the nine rules A to I"), and the name exists only as the repo key `ia_gate_foothold` (rule A, tab_B-6a). | "which is rule A of Section~\ref{subsec:failure-matrix} (Appendix~\ref{app:weight-sets})" | high |
| M16 | 4519–4520; 5297 | "A \emph{verdict-conditioned} Petri net is the pair"; "This is verdict-conditioned re-weighting" | C2 | A coined name used once more, in a different form; the equation labels carry the object. Check 1 (needs basis) is marginal. | Keep the definition and drop the name: "The Petri net extended with the verdict is the pair" (l.5297: "This is the re-weighting of Equation~\ref{eq:routing}"). | low |
| M17 | 4392 | "DAGs, because they are acyclic" | C2 | The acronym is never expanded anywhere in the dissertation, and it is used once. | "directed acyclic graphs, because they are acyclic" (or "DAGs, which cannot represent the attack graph's cycles") | high |
| M18 | 4394–4396 | "a stochastic Petri net (SPN) ... a deterministic and stochastic Petri net (DSPN)" | C2 | Each acronym is used once (check 5). The clause is Marc's and ruled; only the acronyms are flagged. | Drop "(SPN)" and "(DSPN)". | low |
| M19 | 4204–4206 | "Co-occurrence mining gave low coverage and keyword mining poor fidelity" | C2 | Two method names the reader has never met, and "to produce this corpus" is wrong: they would produce a different input. | "... to produce an input for our pipeline: co-occurrence mining of threat reports gave ..." | low |
| M20 | Table 4.1 l.4643 | "the rule kernel and the lifecycle-distance kernel" | C2 | The float's words differ from the body's ("the failure rules, $R$", "distance, $d$", l.5190–5193). | "the failure rules and the stage distance, whose product is $F_{\text{failure}}$" | med |
| M21 | 4684; 4917 | "sink retrace policy" (l.4684) ... "We employed a sink-retrace policy" (l.4917) | C3 | Used before it is defined. *sink* is never glossed, and the term is spelt two ways. | At l.4917: "a sink-retrace policy: when the token reaches a sink, a place with no out-transition, it retraces the edge it travelled"; hyphenate l.4684. | med |
| M22 | 4552; 4937 | "each arm of Chapter~\ref{ch:experiments}"; "a difference between the arms" | C3 | *arm* as an experimental condition is first defined in chapter 5 (ch3's "arm" is a different sense). | l.4937 "between the two attackers"; l.4552 "each experiment of Chapter~\ref{ch:experiments}" | med |
| M23 | 4929–4931 | "a 20-second confusion penalty that hits the attacker at certain phases" | C3 | Its only earlier definition (ch2, l.1030) is inside a placeholder, so the reader meets it here undefined. | Once the ch2 placeholder is drafted, nothing more is needed here; until then, "a 20-second delay, the confusion penalty, charged whenever a deployment interrupts the attacker" | med |
| M24 | 1773 vs 4199 | "Center for Threat-Informed Defense (CTID)" | C3 | Expanded twice (ch3 and ch4). | l.4199: "maintained by CTID" | high |
| M25 | 4240–4242 vs 4510–4512 | "preserving the logical AND/OR structure. But aggregation makes the logical AND vacuous" vs "so the AND structure Attack Flow preserves stays inert here" | C3 | The AND structure is dismissed twice for two different reasons (aggregation; a single token). | Keep l.4510–4512, the mechanism that decides; cut "But aggregation makes the logical AND vacuous, because there are many OR paths which an attacker can traverse." | med |
| M26 | 4483–4484 | "a tactic whose declared time is zero is immediate" | C4 | This contradicts "$T_T = \{\tau_p\}$: one timed transition per tactic". With $W_c(\tau_p) = 1/\mu_p$, resource development ($\mu_p = 0$) divides by zero in the formal definition. | "... is immediate, and its $\tau_p$ belongs to $T_I$" | med |
| M27 | 4227–4229 | "we judged the relatively low fidelity ... to be something we could not defend over the life of the project" | C4 | Process narrative ("the life of the project"). The reason should be methodological. | "... to be too low for a behavioural model" | med |
| M28 | 4671–4673 | "We can assume that they perform these because we know they do that (Section~\ref{sec:apt-survey}), and it is defensible because nothing detects pre-intrusion activity anyway." | C4 | Speech register ("they ... these ... that", "anyway"). The sentence reads as circular. | "APT attackers perform pre-intrusion activity (Section~\ref{sec:apt-survey}), and the defender cannot observe it." | high |
| M29 | 4770 | "We scoped it down: for this dissertation we adopt the existing actions" | C4 | First-person process narrative (a register the task names). | "This dissertation adopts the simulator's existing actions." | high |
| M30 | 5074–5077 | "Some tactics map to the same action, but in reality the tactics, we would assume, do not take the same amount of time." | C4 | A hedge inside the claim (a register the task names). The sentence is ruled to stay; only the hedge is flagged. | "Some tactics map to the same action but hold different dwell times." | high |
| M31 | 4329–4331 | "the smallest attack profile has a minimum of five flows, which provides enough coverage" | C4 | Unsupported sufficiency claim. | "... has five flows; Appendix~\ref{app:rejected-partitions} compares finer partitions." | med |
| M32 | 4299–4300 | "We can see what an APT group did; this is an analyst inference." | C4 | "this" attaches to what the attacker did, which is observed, so the sentence says the opposite of its intent. *APT group* is also a variant of *APT attacker*. | "Motivation is an analyst inference; what an APT attacker did is recorded." | med |
| M33 | 4962–4963 | "our Petri nets can be mapped to anything given an appropriate mapping" | C4 | Overclaim ("anything"). | "... can be mapped to another simulator's actions given an appropriate mapping" | high |
| M34 | 4978–4982 | "The dwell times do not exist in the literature; they do not exist in CTI vendor reports. Prior papers describe this as inherently arbitrary: trying to put times on an attack" | C4 | An absolute claim of absence, and the attribution is garbled (what is "inherently arbitrary"?). | "Per-tactic dwell times are not reported in the literature or in CTI; prior work describes timing an attack as inherently arbitrary~\citep{...}." | med |
| M35 | 5116 | "There is no real mapping here, so we used our best judgement." | C4 | "no real mapping" is ambiguous (none exists? none in the source?). | "No published mapping exists, so $\varphi$ is declared." | med |
| M36 | 5121–5123 | "many tactics are dwell-only" | C4 | A vague quantifier where Figure 4.4 gives the number (seven of 15). | "seven of the 15 tactics are dwell-only" | high |
| M37 | 5150–5152 | "forcing a total mapping was just another input that did not work: it was running a tightly ordered finite state machine in an unordered but stochastic manner" | C4 / C3 | Informal ("just", "did not work"). *total mapping* is first used here undefined. Two colons chain in one sentence. | "A total mapping, every tactic to an action, ran the baseline attacker's ordered finite state machine in stochastic order (Appendix~\ref{app:experiment-one})." | med |
| M38 | 5154–5155 | "We also considered using MITRE Caldera~\citep{applebaum2016}, but this would introduce too much overhead." | C4 | Unsupported ("too much overhead" of what kind?), and Caldera is introduced only here. | "... but Caldera executes against real hosts, not a simulated network." (only if that is the reason) | low |
| M39 | 4917–4918 | "because the token would frequently hit sinks" | C4 | A vague quantifier. | The count or share of runs, or "because the corpus leaves some places with no exit" | low |
| M40 | 4165 | "to evaluate our defence mechanisms" | C4 | "our": the mechanisms are MTDSim's and the field's, not the dissertation's. ("our existing simulator" is not re-flagged.) | "to evaluate the defence mechanisms" | med |
| M41 | 4266–4270 | "Another limitation we encountered was an issue with a lack of pre-intrusion dependencies ... passive recon" | C4 | Wordy spoken frame, and an informal abbreviation. | "The corpus also lacks pre-intrusion dependencies ... passive reconnaissance" | med |
| M42 | 4274–4275 | "This is persistent across CTI, so we would have to address it regardless of our input." | C4 | An uncited generalisation plus a hedge. | Cite it, or: "Any CTI source shares this gap, because pre-intrusion activity is not observed." | low |
| M43 | Table 4.1 l.4640; 4779; 4977 | "$v \in V$ ... \S\ref{subsec:runtime-mechanics}"; "$\mu_p$ of Equation~\ref{eq:gspn}" (×2) | C4 | Referencing slips: *v* is declared at Eq.~\ref{eq:vc-net} (§4.3), and $\mu_p$ is not in Eq.~\ref{eq:gspn}, which declares it through $W_c$ in the list after it. | "Eq.~\ref{eq:vc-net}"; "$\mu_p$ of Section~\ref{sec:petri-formalism}" | med |
| M44 | 4506 | "so the two nets are the same object in execution" ... "which is what makes the net plug and play" | C4 | "the two nets" has no antecedent (the definition's and the implementation's), and "plug and play" is informal. | "so the implemented net and $\mathcal{N}_c$ behave identically"; "plug and play" → "interchangeable" | low |
| M45 | 4770–4775 vs 4148–4150 | "MTDSim runs either one, on the same network and under the same defences, so that ..." | C4 | The chapter opener's sentence is restated almost verbatim, and l.4935–4937 says it a third time. A cut candidate (academic_register §e). | Keep the opener and l.4935–4937; cut l.4773–4775 "MTDSim runs either ... two attackers." | low |
| M46 | 5094–5102 (prose slot in the comments) | the must-carry "these are model parameters anchored to this simulator, not real-world measurements" | C4 | A standing must-carry, ruled to live in the prose beside Table 4.2, and still absent. A marker will ask whether the dwell times are claimed as real. | Marc's sentence in the slot. | med |
| M47 | 4325 → tab_B-2a captions | "(\texttt{objective\_exfiltration}, $n=19$)" and three siblings; "class" throughout | C4 / C1 | Repo codenames on the surface of an appendix the body points to. *class* is a variant of attack profile. | Fix in the generator: drop the `\texttt` keys and write "attack profile $c_1$ (exfiltration)". | med |
| M48 | 5000 vs 5073 | "at ten times it" vs "which is 10 times the exploit shape" | C4 | The same multiplier is styled two ways in one section (E5 rule: ten and below may be words, but one style). | "ten times" at l.5073 | low |

## Pending rulings restated (no finding)

- *axes* (l.4139) vs ch3's heading "Properties of a sophisticated attacker": the "eight axes" wording is ruled do-not-re-flag (2026-08-19). The terminology.md *property* row (PROPOSED 2026-09-07) would change it only on Marc's ruling. The reader meets *properties* in ch3 and *axes* here.
- *declared mean* (caption l.4857) vs *mean dwell*: PROPOSED row, not enforced.
- `terminology.md` rows for *verb* and *the profile net* are superseded by today's rulings (*actions*, *Petri net*) and need flipping.

## Passed as field terms or defined at use (one line each)

token, tangible / vanishing marking, timed / immediate transition, inhibitor arc (all Ajmone Marsan); terminal tactic (defined only in App. B, see B18); stall (defined at use, l.4921); scheme-aware attacker (cited, Jalowski); the exponential draw (ratified); lifecycle stage (ratified); failure matrix and its long form (ratified); scan-shaped / exploit-shaped / low-and-slow families (defined at use and read by the sensitivity floats); pre-intrusion overlay (ratified; see B5 for placement); targeted attack scenario (ch2, tab:attacker-objectives); the five headings (as ruled).

---

# Supervisor screen (2026-09-25, after the second pass) — what an examiner will push on

Read against the chapter as it now stands (l.3917–5619, §4.5 drafted), its
appendices (B, C.0–C.1) and the code where a claim had to be checked. The
line-level entries above are mostly the right fixes and are not repeated here.
This screen is about the **argument**: where a careful examiner can open a
hole, and the conventional move that closes it. Line numbers are as of this
screen.

**Overall.** The chapter is now honest, and in most places it says what was
done. What is left is structural. It makes a lot of declared choices but never
gathers them in one place. Its robustness evidence holds fixed the part that
does the work. It never shows that the model reproduces its own input. And it
does not rule out the alternative an examiner is most likely to name. None of
these needs new modelling. Each needs a sentence, a table row, or one run.

## Tier 1 — defensibility holes (fix before anything is shared)

**S1. The sensitivity analysis moves the parts that do nothing and holds the
part that does.** Table C.0: both failure-matrix rates are *inert*, and the
floor is "zero by structure: no Petri net carries a jump of three stages". So
the distance term has no measurable effect. The nine rules $R$ carry the
failure matrix's effect (Figure 4.3b: initial access → reconnaissance goes from
0.062 to 0.750 under failure), and they are "held". Meanwhile §4.4.4
(l.5238–5250) spends its paragraph on the distance term and one clause on the
rules. The examiner's question is: *does the failure matrix change anything,
and is that change an artefact of values you picked?*
→ Add one ablation row to Table C.0: $F_{\text{failure}}$ = identity (the
failure matrix off). This is the conventional test, and it answers both halves
of the question. Then weight the prose to match the evidence. Say that the rates
are inert and the floor never binds, so the rules are the substance. At present
l.5247–5249 describes a rule ("a jump of three stages falls below a floor ...
zero it out") that never acts.

**S2. The comparison mixes routing with timing, and the thesis claim needs the
two kept apart.** l.4977–4978: "a difference between the arms is a difference
in the attacker and nothing else". True. But the APT attacker model differs
from the baseline attacker through at least three channels: *order* (the net's
routing), *timing* (a drawn exponential dwell replaces the action's native
cost, l.4848–4850, and dwell-only tactics add time with no action), and
*retreat after failure* ($F_{\text{failure}}$). A chapter 5 difference could
come from any of them. The criterion's claim is "behavioural fidelity changes
the answer". An examiner will ask which part of the fidelity does it: a model
that is only slower would also change the answer.
→ In §4.4, name the three channels in one sentence. If a control arm exists
that isolates routing, point at it. (`movement/net.py` builds a uniform-weight
arm, "the null against which corpus concentration is the *strategic*
content". Check whether chapter 5 reports it.) If no arm isolates a channel,
chapter 6 should claim "the APT attacker model changes the answer", not that
behavioural fidelity does (the measurement-vs-attribution rule).

**S3. The model is never checked against its own input.** Nothing states that
$\mathcal{N}_c$, run with no defence, reproduces the corpus it was built from:
generated tactic shares against the profile's flows, or transition frequencies
against $w_c$. That is the standard verification and face-validity step for a
simulation model derived from data. Without it, "grounded in CTI" rests on the
construction alone.
→ One paragraph (end of §4.3 or §4.4) and one appendix table. Implementation
verification: the trace tool shows the implemented net fires in proportion to
$w_c$. Face validity: generated against corpus tactic occurrence per profile.
Relative tactic occurrence, §4.5's own metric, is the natural measure. Some of
this may already exist: `l2_subgraph/dedup.py` cites an L2 JSD re-check in
`tests/l2_subgraph/test_gasp.py`. That covers L2, not the runtime net. Verify
before citing it.

**S4. "Why a Petri net and not a Markov chain?" is not answered.** One token,
no concurrency, the AND structure inert (l.4547–4550). As run, the net is a
continuous-time Markov chain over tactics whose jump probabilities depend on
the verdict. An examiner with formal-methods training will say so at once. The
rule-out paragraph (l.4425–4435) names attack graphs, DAGs, SPN and DSPN, but
not the Markov chain. It also omits attack trees and the MDP/POMDP family that
Cho points to for rational attackers.
→ Rule it out in that paragraph, and **concede the reduction**. Say that the
net as run is equivalent to a CTMC. Then say what the GSPN buys: concurrency
(more tokens) as an extension within the same formalism, and the separation of
structure from weights ("plug and play", l.4546, which needs rewording
anyway). The MTD precedent is already cited. Also say that once $F_v$ depends
on the simulator's verdict, the net is used as an executable specification and
is not solved analytically. That heads off "why no steady-state analysis?".
Owning the reduction is stronger than leaving it to be found.

**S5. Judgement calls sit outside the parameter register.** Table C.0 claims to
be "each value the attacker model was given rather than derived". These values
were also given and are not in it:
- $\sigma = 0.1$ (l.4709)
- the operator-deduplication rule (one flow per operator, the one with most steps, l.4536–4539)
- the sink-retrace policy (l.4958)
- $M_0$ on reconnaissance
- the single token
- the per-tactic multipliers within each dwell family
- the detector's $\theta$ ($\kappa$ has App. C.4)
- APV's $k$, which the body never gives a value at all (l.5418–5426)

The phrases "we judged", "best judgement", "to the best of our judgement" and
"plausible" occur at six or more sites.
→ Either widen Table C.0 to every declared value (held values are fine; say
*held*), or put one "declared values and assumptions" table in chapter 4 with
value, basis, and whether it was moved and where. Then point each "we judged"
at its row. A chapter that lists its own judgement calls is hard to attack. A
chapter where the examiner finds them one at a time loses marks for each.

**S6. The most influential parameter rests on the weakest basis, and the body
does not say so.** Low-and-slow family: 13.4 / 8.1 / 3.0 hosts across its band,
a fourfold swing and the largest in Table C.0. §4.4.2 (l.5044–5045) says that
family "rests on our judgement alone", but not that the results are most
sensitive to it.
→ One sentence and a pointer in §4.4.2, and the same in the chapter 6
limitations. Once stated, the finding is the student's limitation and not the
examiner's discovery. Also correct l.5045–5046 ("four free timing values
rather than 15"). App. C.1 moves each family "the per-tactic multipliers ...
riding along unchanged", so say "four family values are moved; the per-tactic
multipliers are declared and held".

## Tier 2 — claims that need their reason, or their second count

**S7. Only one of the corpus's two biases is named.** Survivorship bias is named
(l.5220–5222) and answered by the failure matrix. Selection bias is not. Attack
Flow holds the incidents analysts chose to model from public reporting, which
means high-profile, well-documented cases, concentrated on a few operators.
Sixteen of the 38 flows fall in eight operator clusters, which is why the
deduplication exists at all. "38 usable" also never says *usable of how many*,
or why the rest were excluded.
→ In §4.1, one clause for the inclusion count and criterion (corpus v3.1.1).
One sentence naming selection bias next to "a different corpus would give a
different net" (l.5219–5220), which already concedes the consequence.

**S8. Half the corpus overrides the "primary" evidence, and the coding is one
person's.** l.4356–4360: "Terminal tactic is the primary evidence ... That is
why 19 of the 38 attack flows land in a different attack profile." When the
cross-check overturns half the flows, the terminal tactic is not the primary
evidence. The cross-check is.
→ (a) Reword: the terminal tactic *proposes* a profile, and the CTID
description, the ATT&CK page and vendor reports *decide* it; they overturned it
for 19 of 38. (b) State the rule for when those sources disagree, and make Table
B.2 show it. (c) Name single-analyst coding as a limitation. The conventional
fix, cheap at n = 38, is a second coder on a sample with Cohen's κ reported.
Also, l.4342–4344 treats "the tactics before the objective as common to all
APT attackers", yet each profile carries its own weights on those tactics.
Say that the assumption is used to *classify* by terminal tactic, not to pool
the prefix weights. Otherwise it reads as contradicting the profile-specific
nets.

**S9. The profile sizes are counted two ways, and the sufficiency claim uses
the larger count.** §4.2 gives 19 / 7 / 7 / 5 and says "the smallest attack
profile has a minimum of five flows, which provides enough coverage"
(l.4365–4366). The weights come from the deduplicated corpus, 14 / 6 / 5 / 4
(29 flows, l.4539), so $c_4$ rests on four. "Enough" is unsupported at either
count.
→ Give both counts where the deduplication is disclosed. Replace "enough
coverage" with what Appendix B.3 actually compares (M31). Give the
deduplication rule its reason (the fullest record of that operator's
campaign) and its cost (it favours long flows).

**S10. The pre-intrusion overlay is justified by the wrong property.**
l.4710–4712: "defensible because nothing detects pre-intrusion activity
anyway". That argues the overlay does not matter to the defender, which
undercuts including it. What the overlay does in the model is give a failed
intrusion somewhere to go: Figure 4.3b's retreat to reconnaissance carries
0.75 of the mass after a failed initial access.
→ Justify it by that role, with the lifecycle literature
(\citealt{alshamrani2019}, already cited), which describes attackers returning
to reconnaissance. Keep "not observable by the defender" only as the reason the
corpus lacks these edges (l.4284–4289 already says that).

**S11. The formal definition still has two live slips.** (a) $T_T = \{\tau_p\}$,
one timed transition *per tactic*, yet "a tactic whose declared time is zero is
immediate" (l.4516–4519). With $W_c(\tau_p) = 1/\mu_p$ and resource development
at $\mu_p = 0$, the definition divides by zero (M26). (b) $T_T$, $T_I$, $I$ and
$O$ vary with $c$ but carry no subscript. Also, l.4544 defines $T_I$ as the
pairs with $w_c > 0$, then argues that the implemented zero-weight form is
equivalent. Define it once, in the implemented form, and cut the equivalence
argument.

**S12. §4.5's statistics need four conventional guards.**
- ASP is a proportion that sits near 0 at short intervals. The criterion's
  degenerate region pins it at zero at 200 s, so a normal-approximation
  interval is wrong there; use Wilson or the bootstrap already in use.
- MTTC is a mean over $\mathcal{R}_1$, which can be small. Report
  $|\mathcal{R}_1|$ with every value; the text already says "the share of runs
  it covers".
- Spearman's ρ is computed over five or six defences. At that n, report it as
  descriptive and not as a test.
- $\theta$ is the median of $D$ over the baseline attacker's actions, so the
  baseline's pooled attack confidentiality is 0.5 **by construction**. Say so
  in §4.5, so that chapter 5 does not read it as a finding. Also state whether
  $\theta$ is fixed once or set per cell.

One more on robustness: Appendix C's runs are at "the random scheme mutating
every 200 s" (Figure C.1 caption). Chapter 5 reports six intervals, and the
metric windows assume 2 000 s. Hosts reached is breadth-shaped, so it stays
informative at 200 s (criterion §(b)). Even so, say in Appendix C why
robustness at 200 s carries to the reported intervals, or rerun at the headline
interval. ("Mutating" is also a B23 term that survives in that caption.)

## Tier 3 — leftover surface (one sitting)

- Figure 4.4b still reads "The committed failure matrix" / "as committed
  (\texttt{v4\_failure\_only})" (l.5332–5333): M4/M5 were applied to the
  mapping captions only.
- Figure 4.3's "gadget" ×2 and "foothold-gate rule" (M14, M15).
- Speech-register residue, all already in the M list: "pipe in" (l.4420),
  "plug and play" (l.4546), "anyway" (l.4712), "just another input that did not
  work" (l.5195), "we would assume" (l.5117), "over the life of the project"
  (l.4229), "We scoped it down" (l.4809), "our defence mechanisms" (l.4165),
  "too much overhead" for Caldera (l.5200), "The literature tells us" (l.4312).
- The opener: "it aims to meet the axes" (l.4139). The criterion records axes
  the model does not address, so say "it addresses the axes of Section 3.x;
  Section 6.x reports which it meets", or an examiner reads it as a claim on all
  eight.
- l.4313–4316: "We cannot produce an APT attacker model that could be
  considered behavioural, because the attack graph carries so many different
  motivations" asserts impossibility. What is meant is that a single net over
  the whole corpus would average over objectives that drive different
  behaviour. Say that.
- State in §4.4 that the baseline attacker runs the same targeted scenario
  (l.4852–4855 gives it to the APT attacker model only). `targeting.py` shares
  the host sorter across both arms; the prose should say so.

**Suggested order.** S1 and S3 are one short run each and close the two
largest holes. S5 is one table, and it absorbs S6, S9's counts and §4.5's $k$
and $\theta$. S2 and S4 are a sentence or two each, but they decide how chapter
6 may word the headline claim, so rule on them before chapter 6 is drafted.

## Marc's reply and corrections to this screen (2026-09-25)

- **S1 corrected: the ablation already exists.** §5.4 "Response to disruption"
  (l.~7333) uses the same attacker with $F_{\text{failure}}$ = identity as its
  control. The gap is only that chapter 4 does not point to it and Table C.0
  does not list it. **The real hole Marc names** is the provenance of the
  values: "how do you come up with those?" The per-value reasons already exist
  (Table B.4's *Why this value*, Table B.6a's *Rationale* and *Tier*, Table
  B.5's reasons). But the body never states the procedure, and the three
  appendices use three different vocabularies for a value's basis. Step 1 of
  the walk-through is the fix.
- **Ablations: Marc's structure is the conventional one.** The method declares
  the test and points to where its result is reported. The result lives in
  chapter 5 or an appendix.
- **S2: Marc's sentence stands.** "A difference between the arms is a
  difference in the attacker and nothing else" is a correct statement about
  holding the environment fixed. What is open is only what "the attacker"
  bundles (order, timing, failure response) and which parts have a control.
  That is a case to put to Marc, not a rewrite.
- **S6 retracted for chapter 4.** How much the low-and-slow family moves the
  results is an evaluation result (Appendix C / chapter 6 discussion), not
  method. §4.4.2 already says the family rests on judgement and has the widest
  band, which is all the method owes.
- **S8 reframed by Marc's actual process.** Each flow was classified by hand:
  the CTID description, the ATT&CK page and the vendor reports were read, and
  the profile was assigned, with the terminal tactic as the starting evidence.
  The defensible form describes that manual coding procedure, points to Table
  B.2 as the audit trail, and discloses the single coder.
- **S9: the reason stands** (the partition balances coverage against
  abstraction and fidelity). Only the second count (14/6/5/4 after
  deduplication) is owed.
- **S12: attack confidentiality was drafted before the metrics existed.**
  Marc accepts the point.

## Walk-through state (2026-09-25, continued)

**Ruled (Marc):**
- **Step 1:** the four-way basis vocabulary is accepted: *from the corpus*,
  *from the simulator*, *from the literature*, *our judgement*. Marc wants the
  paragraph crisp and factual, with no rhetorical flourish: what was done, the
  procedure, why it is defensible.
- **S2 = (a):** behavioural fidelity is defined as the bundle (order, timing,
  failure response). The headline holds for the bundle, and a part is claimed
  only where a control exists. No new run.
- Steps 4 (validation run and appendix table), 5 (concede the equivalence to a
  continuous-time Markov chain, argue from concurrency), 6 (hand-coding as a
  manual procedure) and 7 (formal slips) are accepted as proposed.

**Step 1 draft, proposed (NOT applied), to replace l.4825–4829:**

> Each value in the APT attacker model has one of four bases. The base
> weights $w_c$ and the membership of each attack profile come from the corpus.
> The scan-shaped and exploit-shaped dwell times come from the simulator: they
> are MTDSim's own enumeration and exploit costs, as is the 20-second confusion
> penalty. The order of the four lifecycle stages comes from the literature
> \citep{hutchins2011, alshamrani2019}, and with it the dependency the three
> gating failure rules encode: without a foothold, no post-intrusion tactic is
> reachable. The rest is our judgement: the multipliers that extend the
> simulator's costs to the tactics no action prices, each row of the
> tactic-to-action mapping, the size of each failure rule, the pre-intrusion
> share $\sigma$, and the choice of one attack flow per operator. Each value
> set by judgement has its reason recorded beside it
> (Tables~\ref{tab:dwell-derivation}, \ref{tab:controller-mapping}
> and~\ref{tab:overlay-failure-rules}), and is tested in one of two ways: it is
> moved across a band (Appendix~\ref{app:sensitivity}), or the evaluation runs
> a control without it (Section~\ref{subsec:aio-disruption}). A value tested
> in neither way is held, and Table~\ref{tab:parameter-register} says so.

Open checks on the draft:
- Does \citep{alshamrani2019} carry the foothold dependency? Verify in its
  extraction before committing.
- Table C.0 needs the *Basis* column, plus rows for $\sigma$, the
  one-flow-per-operator rule, sink-retrace and the identity control. It is
  generated, so the change goes in the generator (find it:
  `grep -rl declared_inputs tools/`).

**S2 (a) sentences, proposed:**
- Chapter opener, after "testing whether behavioural fidelity changes
  existing MTD evaluation" (l.4152–4153): "Behavioural fidelity here is three
  things the Petri net supplies together: the order of the attacker's tactics,
  the time each takes, and where it goes after a failure."
- §4.4, after "a difference in the attacker and nothing else" (l.4978): "The
  evaluation separates the third of these from the other two with a control
  (Section~\ref{subsec:aio-disruption}), and the profile from the aggregate with
  $c_{\mathrm{agg}}$; it does not separate order from timing."

**Step 2, the failure matrix: facts gathered for the case (measured 2026-09-25):**
- *What it is.* Nine rule values, each multiplied by a stage-distance factor.
  The distance factor's three parameters are inert or never bind (Table C.0).
  In effect, then, the matrix is nine judgement values. The body draws all 210
  cells (Figure 4.4b), which is why it reads as inflated.
- *It moves routing.* Composed onto the base weights of each routing net
  (`v4_failure_only`, the `operator_dedup` weights, synthetic overlay on), it
  shifts on average 0.15 of a place's out-mass (total variation, all profiles).
  At initial access it shifts 0.61–0.73, which is rule A: a failed initial
  access leaves no foothold.
- *It does not move outcomes.* In `ch5_s522_disruption_findings.md` (100 seeds,
  preliminary), the identity control is within 0.025 at every step, and the
  position by stage is unchanged. After a disruption the attacker's actions fail
  until it holds a host again. Recovery is governed by the base routing's chance
  of reaching a discovery tactic, not by the matrix.
- *Origin.* The supervisor's M2 ruling was "failure → another [weight set]
  (forward zeroed; retry/backward transitions live)". Marc's reversal idea (on
  failure, route along the place's in-edges, weighted by the corpus) is M2 in a
  form with no free values.
- *Reversal: for and against.* For: no declared values, a corpus basis, M2
  taken literally. Against: it removes lateral retries, which carry the most
  base mass after an intrusion because eight of the 15 tactics share one stage.
  It needs a code change, since `OutcomeOverlay.compose` only rescales existing
  out-edges. It needs a rerun of the defended corpus and every chapter 5 figure
  at 1 000 seeds. And at initial access it does what rule A already does.
- *Recommendation.* Keep the matrix. In the body, present the nine rules
  (rule, when it applies, value, basis) and move the 210-cell matrix to
  Appendix B.6, where it already exists as Table B.6c. Defend the matrix with
  the identity control: no reported conclusion depends on the nine values,
  because removing them changes no reported reading. Reversal is optional, as
  an appendix alternative in the manner of the forced-total mapping experiment,
  and only if time allows. Do not claim reversal was considered; it was not.

**Awaiting Marc:** a ruling on the step 1 draft (wording); a ruling on the
failure matrix recommendation (keep, show the rules in the body, move the cells
to the appendix; reversal as optional appendix work, or not at all).

## Walk-through state, round 2 (2026-09-25)

**Marc on the step 1 draft:** the direct sentences are right. Cut "recorded
beside it" and "tested in one of two ways" (flourish). Use the conventional
terms (*sensitivity analysis*, *ablation*). The last sentence was unclear.
**Revised draft (NOT applied):**

> Each value in the APT attacker model has one of four bases. The base
> weights $w_c$ and the membership of each attack profile come from the corpus.
> The scan-shaped and exploit-shaped dwell times and the 20-second confusion
> penalty come from the simulator: they are MTDSim's own costs. The order of
> the four lifecycle stages comes from the literature \citep{hutchins2011,
> alshamrani2019}. The remaining values are our judgement: the multipliers for
> the tactics no action prices, the tactic-to-action mapping, the nine failure
> rules, the pre-intrusion share $\sigma$, and the choice of one attack flow
> per operator. Appendix~\ref{app:movement} gives the reason for each
> (Tables~\ref{tab:dwell-derivation}, \ref{tab:controller-mapping}
> and~\ref{tab:overlay-failure-rules}). Appendix~\ref{app:sensitivity} reports
> a sensitivity analysis on the dwell times, the mapping and the failure
> matrix's scaling rates, and Section~\ref{subsec:aio-disruption} an ablation
> of the failure matrix. The values in neither are held fixed;
> Table~\ref{tab:parameter-register} lists them.

**Marc on step 2 (ruled):** keep the failure matrix. It is too late to replace
it, and reversal is hard to defend: ATT&CK has no backward edges, so the
forward/backward reading was already a forced binary. The failure matrix is
Marc's own construction ("not what I would have done if I had to do it
again"). **How it is presented and defended is the work.** The lateral-move
fact is the defence: a forward/backward rule leaves most post-intrusion moves
undefined.

**Step 2 draft, the §4.4.4 body (NOT applied):** it replaces the prose at
l.5216–5250, 5274–5278 and 5343–5346.

> The base weights $w_c$ are the success routing. The attack flows record the
> steps that succeeded, so they say where an attacker goes after a success and
> nothing about where it goes after a failure: the corpus has survivorship
> bias, and no record of failure. The failure matrix $F_{\text{failure}}$ of
> Equation~\ref{eq:vc-net} supplies the failure routing, and every value in it
> is our judgement.
>
> The matrix follows one principle: after a failure, a move back is more
> likely and a move forward less likely than after a success. ATT\&CK imposes
> no order on its tactics, so direction is read from four lifecycle stages
> drawn from the literature \citep{hutchins2011, alshamrani2019,
> mandiant2013, chemat2024}: preparation, intrusion, post-intrusion operations
> and objective. A forward-or-backward rule is not enough on these stages.
> Eight of the 15 tactics fall in post-intrusion operations, so most moves
> after an intrusion stay within one stage; in most post-intrusion tactics of
> the attack profiles, these lateral moves carry most of the out-weight. The
> matrix therefore separates three relations (backward, lateral and forward)
> and adds three rules for dependency: a failed initial access leaves no
> foothold, so no post-intrusion tactic is reachable, and a failed
> reconnaissance weakens initial access and rules out a deeper move.
> Table~\ref{tab:failure-rules} gives the nine rules, the value of each and its
> reason. Figure~\ref{fig:gspn-gadget}(b) shows the first at work: after a
> failed initial access, the share routed to reconnaissance rises from 0.062
> to 0.750.
>
> Each cell of the matrix takes the value of the first rule that matches the
> pair, scaled down when the move crosses two stages
> (Appendix~\ref{app:weight-sets}). The values were set from these reasons and
> not fitted to any evaluation outcome. Appendix~\ref{app:sensitivity} moves
> the scaling rates. Section~\ref{subsec:aio-disruption} ablates the matrix,
> replacing it with the identity so that the token routes on the base weights
> whatever the verdict. The nine rule values are held fixed.

Presentation changes that go with it:
- **Body float:** Figure 4.4b (the 210 cells) goes to Appendix B.6, where
  panel (c) of Figure B.6a already draws it. In its place in the body goes a
  new table, `tab:failure-rules`, with four columns: rule, applies when, value,
  basis. Its source is Table B.6a with the `\texttt` keys replaced by plain
  names. Basis: A–C take their direction from the literature (dependency) and
  their size from judgement; D–I are judgement. It is generated, so the change
  goes in the generator, not a hand edit.
- **The distance term's floor leaves the body.** It never binds (no net
  carries a three-stage move), and Table C.0 already records that.
- **The null goes in the results and discussion, not the method.** The
  ablation's result (the identity control is within 0.025) is reported in the
  results chapter. Chapter 6 carries the defence: no reported reading depends
  on the nine values. The method only states the test (ch5 antecedent rule, the
  mirror case).

Checks before applying:
- The lateral-share claim ("most post-intrusion tactics") was measured on the
  routing nets, 2026-09-25. Recompute per profile when the table lands.
- The citations for the stage order are the ones already at l.5240.
- The "not fitted to any evaluation outcome" wording must match the record:
  `success_failure_overlay_design.md` §2.3 says rule A was moved from 0.1 to
  0.02 on a *routing* diagnosis (IA-failure mass), never on an outcome. The
  sentence is true as worded. Do not strengthen it to "never adjusted".

**Step 1 APPLIED 2026-09-25** (Marc: "just push it in for now"), DRAFT STATE.
It follows "These are the three inputs we had to declare" in §4.4. Marc
rejected "the values in neither are held fixed; Table C.0 lists them" as
unclear. The applied text uses ten Broeke et al.'s conventional terms
(*one-factor-at-a-time sensitivity analysis*, *nominal values*;
`tenbroeke2016`, held at `docs/sources/methodology/tenbroeke2016_abm_sa.md`)
and names the fixed values outright. The build is clean (pdflatex ×2 + bibtex,
no undefined refs).

**Marc's question: does the ablation belong in the evaluation or in the
appendix?** Answer given: leave it where it is, as the control of the chapter 5
response-to-disruption subsection. The convention is that an ablation bearing on
a claim the evaluation reports sits with the results, and a sensitivity analysis
that only shows robustness goes in an appendix. The method points to both,
which the applied paragraph now does.

**Step 2 (the failure matrix) is next:** the draft above, the new nine-row rules
table, and Figure 4.4b moved to Appendix B.6. It is not yet applied.
