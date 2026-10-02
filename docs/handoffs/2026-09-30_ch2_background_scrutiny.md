---
status: open                  # 2026-09-30: APPLIED on Marc's rulings (redraft, see "Applied" below); residue listed there
created: 2026-09-30
companions: ../workflows/background_conventions.md (the yardstick), ../workflows/voice.md §(0), ../workflows/terminology.md, ../notes/ch2_background/README.md
---

# Chapter 2 scrutiny: say more with less, and fix the figures

**Goal.** Bring chapter 2 (Background) to the point where every sentence and float
does something a later chapter needs, in one term per thing, at the altitude
of a fourth-year computer science student and the examiner. Each entry below is
a proposal for Marc to rule on. Nothing is applied until he rules.

## Applied, 2026-09-30

Marc ruled on this ledger and walked the chapter the same day. He accepted the
inbound references and the lean test, and asked for everything unused to be cut,
the missing facts added, one term per thing, the contradictions fixed, and "clarity
and relevance" as the two main games. He licensed overturning any prior ruling.
The redraft is in the tex, commented "REDRAFT 2026-09-30", and is to be ratified
on read.

**Totals.** Prose 1 290 → 1 040 words, with the disruption placeholder now written
as prose. Caption words about 460 → about 200. Floats 10 → 8. The chapter runs 8
pages → 5. The build is clean at 102 pages, with 0 undefined references and 13
overfull boxes (was 15).

**Where the ledger and the redraft differ, on Marc's walk-through:**

- Table 2.6 (the scenarios) is **kept**: "nice and brief". T6 is not applied.
- Table 2.1 (the lineage) is **cut**: "the language is so imprecise … no aim or
  intent". Each part is attributed where it is described. This makes T1's
  Alavizadeh fix moot. Ch3 l.~3587 was re-pointed.
- The simultaneous deployment strategy is **dropped** ("we don't use it"). The
  ch5 owed mark is retired and registry row 62 amended. Zhang's term *execution
  scheme* is no longer named.
- The six are **phases** (Marc), bound once to ch4's *actions* ("Each phase is one
  of the simulator's six actions"). Registry row 77 is amended.
- §2.1 is reshaped from four paragraphs to two.
- Figure 2.2 is **rebuilt**, not patched. It is now (a) the network (levels,
  subnets, endpoints, target hosts, what is visible to the attacker) and (b) one
  host (IP address, operating system, services with vulnerabilities, user
  accounts). This answers Marc's "should there be a diagram for the CS student …
  subnet, hosts, levels of depth, endpoints". The service graph, the internal
  target node and the threshold bar are gone.
- Figure 2.4 lost its "What it holds" panel (now prose, the last sentences of
  §2.2.3). Each box has one name; the failure edges are labelled; the interrupts
  read host-layer deployment / service-layer deployment / user shuffle.
- Figure 2.1 has content lines in place of panel pointers. The loop is stated
  once, in the §2.2 preamble, and the caption is one line.
- Table 2.2 (configurations) moved to the end of §2.2.3, after its terms. Brown's
  interval is converted to seconds and the caption no longer says "lineage".
- MTDShield: "no detection channel is encoded" is replaced by what the code does
  (X2). It is told the attacker's current phase and decides at a fixed tick with a
  forced deployment, which is Cho's hybrid.
- "Discrete-event simulator \citep{brown2023}" is corrected: time is Zhang's
  addition.
- CVSS, impact and return on attack are defined in ch2. Ch3 l.~3595 refers back,
  and ch3 "two objectives" becomes "two attack scenarios".

**Round 2, the same day (Marc's second walk-through):**

- The opener spells out "when to move".
- §2.1 is now three paragraphs: the definition and the three questions; the move
  (what and how, answered by the mechanisms of Table 2.1); its timing (when,
  answered by the deployment strategies of Table 2.2).
- The §2.2 breakdown names what each subsection holds and mirrors the §5.3.3
  heading.
- *Rewrite* is replaced by *reconfigure* everywhere, including two ch5 captions
  and registry row 64.
- The endpoint sentence leads with its subject.
- Table 2.1: mechanisms indented under the layer rows. The column is now *What it
  reconfigures*, with precise noun phrases.
- The deployment interval is cut to "200 s by default, and near-periodic".
- The MTDShield row is framed around the agent.
- The targeted scenario reads "one of the database hosts at the deepest level".
- The confusion penalty is "about 20 s": it is a draw of 20 s plus a small
  exponential term (`attack_operation.py` apply_mtd_interrupt_cost).
- **The phases table is folded into Figure 2.3.** Each box carries one line saying
  what the phase does. The success and failure edges are labelled "succeeds" and
  "fails", with no colour. The interrupt arrows read "after a host-layer
  deployment" and so on. Every transition was re-verified against
  `attack_operation.py` l.349–668 and l.226–264.
- **Code names retired dissertation-wide** (the supervisor had flagged them in
  Figure 5.1). The phases now use the plain names of `_ch5_style.ACTIVITY` (scan
  host, enumerate host, scan port, exploit, brute force, scan neighbours) in
  Figure 2.3, Figure 4.4, Table B.5, Figure 5.1 and ch4 l.~5258. The regenerated
  floats differ only in those labels; Table 5.2 regenerated byte-identical.
  Registry row 77 is updated.
- Figure 2.1 is now plain boxes in Figure 4.1's style.
- Figure 2.2:
  - (a) is the host layer with no visibility encoding, the attacker glyph entering
    at the endpoints, and prominent target hosts.
  - (b) names the mechanism that reconfigures each part of a host.

**Round 3 (Marc, same day):**

- Figure 2.1: the Attacker and MTD boxes are shrunk to fit their titles (150 ×
  104 px, centred on the network box). Boxes are sized to their contents rather
  than titles being enlarged, to keep Figure 4.1's type.
- Figure 2.3: the phase names are bold. The descriptions were re-verified against
  `attack_operation.py` and corrected:
  - scan host: "lists the visible hosts it has not compromised";
  - enumerate host: "takes the next host in the list";
  - scan port: "scans the host's ports, then tries stolen credentials"
    (`_do_scan_port`: port scan plus credential reuse);
  - exploit: "exploits the vulnerabilities by return on attack";
  - brute force: "guesses a login with stolen passwords" (`compromise_with_users`:
    success odds scale with the stolen accounts valid on the host);
  - scan neighbours: "puts the new host's neighbours at the front of the list"
    (`_do_scan_neighbors` prepends them).

**Round 4 (Marc, same day): Table 2.3 framed around its heading.**

- The columns are *Attack scenario* and *Goal*: General "compromise 80 % of the
  hosts"; Targeted "compromise a target host". The target host is already defined
  in §2.2.1, so the old row restated it.
- The shared stop, no new host discoverable, applies to both scenarios
  (`attack_operation.py:355-360`), so it moved to the caption.
- The table is set at natural width.
- The column is *Goal*, not *Objective*: registry row 61 reserves *objective* for
  the attack profiles.

**Round 5 (Marc, same day): the close and Table 2.4 in the chapter's own terms.**

- The chapter close now says what ch3 does: it draws eight properties from the
  literature and checks which each model has.
- Table 2.3's "no new host" fact moved into the §2.2.3 prose.
- Table 2.4, generated from `data/misc/lineage_configurations.yaml`:
  - *Run ends* is replaced by *Time limit*, Table 5.1's row name. The goals are
    carried by the *Attack scenario* row: Zhang "general, to 80 % of the hosts";
    Brown "general; targeted", since *target host* is defined.
  - *Runs per combination* became *Runs per configuration*.
  - Optimised OS assignment was dropped from Zhang's durations. It is not in
    MTDSim's pool, and the locator records the omission.
  - The caption reads "Where a study ran several values, each is listed" in place
    of the semicolon rule.

**Round 6 (Marc, same day):**

- Table 2.4's caption is cut to what a reader needs to read it: what it is, the
  dash, Ho's missing units, Tay.
- The chapter close is back to a pure hand-over, "Chapter 3 compares the baseline
  attacker, and the attacker models of recent MTD evaluations, with an APT
  attacker"; the specific version "lost sight of its purpose".
- Table 2.2's column is now *What it deploys at each interval*, with cells that
  answer it: a mechanism drawn at random; the next mechanism in a fixed rotation;
  the same mechanism every time; the mechanism its agent chooses, or none.
- Table 2.1's complete topology shuffle cell is cut to "every connection between
  hosts, regenerated", so every cell answers *What it reconfigures*.
- Figure 2.1's four arrows are all ink. The accent had singled out the attacker's
  two for no reason; §n rules that module couplings are carried by words, not hue.

**Round 7 (Marc, same day): one colour for one story in Figure 2.2.**

- The attacker's entry arrow and route are now red (were accent blue), the same
  red as the hosts it compromised.
- The target hosts' blue outline is gone; they stand out by size and the bold
  label.
- The caption reads "red marks its route and the hosts it has compromised".
- No ch2 figure now uses the accent: Figures 2.1 and 2.3 are ink, and 2.2 is ink
  plus compromise red.

**Residue, not ch2's to fix:**

- X4: §5.1 says the random strategy draws on the whole pool; Appendix E says the
  same four as MTDShield.
- Ch4 l.~5721 says "no detection mechanism" while MTDShield reads a detection
  signal (X2's twin).
- Ch3 Masud's "hybrid MTD" is Cho's *other* hybrid (combining SDR types), not
  §2.1's trigger sense. Rename one or gloss it.
- "Synthetic vulnerabilities" is cut from ch2 as unused. It is a validity limit
  §6's threats section should state if it wants it.
- The `scrutinise-figure` gate has not yet run on Figures 2.1–2.3.
- The ch2 notes README is refreshed to match.

---

**How to read the IDs.** G = chapter level, S = structure and headings,
F = figure, T = table, O / M / P / N / D / A = prose in the opener, §2.1, the §2.2
preamble, §2.2.1, §2.2.2 and §2.2.3, X = factual corrections verified against the
code or a source extraction, C = content the chapter lacks (named, never drafted).
Tiers follow [`critique_protocol.md`](../workflows/critique_protocol.md) §(b). T1 is
a deletion or merge of Marc's own words. T2 is a rewording, offered as one
suggestion. T3 is content: the gap is named, not written. Line numbers are
`dissertation.tex` as of commit 2e089a92 and drift with edits.

**Evidence base.** The PDF pages 3–10 as rendered, read as a reader meets them. A
forward-use audit of every chapter 2 fact against chapters 3–7 and the appendices
(which later line uses it, or "not used later"). Four code checks (`host.py`,
`mtd_scheme.py`, Appendix E's MTDShield table, the Zhang and Cho extractions). The
yardstick in [`background_conventions.md`](../workflows/background_conventions.md),
distilled from the thesis-writing literature.

---

## 1. The yardstick, in five lines

- **Purpose.** Chapter 2 gives the reader the vocabulary and the platform that
  chapters 3–5 use without re-explaining: the MTD terms chapter 3 scores with, and
  the network, MTD mechanisms and baseline attacker that chapter 4 builds beside
  and chapter 5 runs.
- **Context.** It describes things that already exist, one level above the code.
  It argues nothing. The arguments about these things belong to chapters 3 and 4.
- **Audience.** A fourth-year CS student arrives from the introduction knowing MTD
  in one plain paragraph (ch1 P2), MTDSim by name, and "baseline attacker" by
  apposition. The examiner reads chapter 2 to check that nothing later rests on an
  undefined object, and that inherited work is kept apart from what the
  dissertation built.
- **The lean test** (the ch2 README's own rule). Nothing enters that a later
  chapter does not lean on, and nothing a later chapter leans on is missing. The
  literature says the same: "Be ready to cut material out of background chapters
  if it is not used elsewhere… Be ruthless!" (Evans, Gruba & Zobel, p. 81). It also
  says to remove anything "to do with the design of your own work" (pp. 81–82),
  which is the ground for D2.
- **The float test.** Each float carries something the prose does not. It is
  referenced from its own section, and its caption says how to read it, not what
  it shows twice. A float complements the text; it does not duplicate it (EGZ
  p. 108; Zobel p. 112), which is the ground for F3 and T6.

## 2. Verdict and the three moves that matter most

**Chapter verdict: tighten.** The shape is right: MTD first, then the simulator
with its three modules nested beneath it. The prose is on budget (1 290 words
against 1 250, with the disruption paragraph still owed). The problem is density
and fit, not length:

- **The floats.** There are ten floats for 1 290 words, with about 460 caption
  words. Two pairs repeat each other: Figure 2.3 and Table 2.3 list the same seven
  mechanisms, and Figure 2.4 and Table 2.5 describe the same six states. Two
  figures are never referenced from chapter 2's prose.
- **The lean test.** About a third of the facts are used nowhere later. The
  facts later chapters do need (the confusion penalty, return on attack, CVSS,
  Zhang's exploit-time halving) are missing, left in a placeholder, or defined
  only in chapter 3.
- **Naming.** The chapter names its central objects two ways. The six are
  "states", "phases" and, from chapter 4 on, "actions". The disruption layers are
  "network-layer / application-layer" in the prose but "host layer / service
  layer" in the tables and in all of chapter 5.

**The three moves, in priority order:**

1. **Make chapter 2 carry what chapters 3–5 lean on, and nothing else** (G1).
   - Fill the disruption paragraph (A6, C1). A visible placeholder in the PDF is
     the costliest single defect.
   - Move the definitions of CVSS, return on attack and impact to their first use
     in chapter 2 (C2). Chapter 3 then refers back to them instead of defining them
     after chapter 2 has used them.
   - Cut what nothing later uses (M1, N2, N6, D2, D3, D6, A1, A3, A5): about 230
     words.
2. **One term per thing, across the prose and the floats** (G2). Use host layer
   and service layer throughout. Bind states to actions once. Keep *deployment*
   for the event and *rewrite* for what a mechanism does. Use *target host*, never
   *objective*.
3. **Floats: ten to eight, each doing work the prose cannot** (F1–F4, T1–T6).
   - Cut Figure 2.3, whose content is Table 2.3 plus Table 2.4.
   - Fold the two-row Table 2.6 into one sentence.
   - Make Figure 2.4's top panel draw what its caption claims.
   - Give Figure 2.1's boxes content in place of pointers.
   - Fix Figure 2.2's legend, depth label, text overflow and over-claiming
     caption.
   - Cut each caption to how to read the float.

Projected: about 1 050 prose words, including a drafted disruption paragraph of
about 90 words, and about 250 caption words.

---

## 3. Chapter-level findings (G)

**G1. The lean test fails both ways.** These ch2 facts are used nowhere later:

- attack surface;
- the "inverts the assumption" sentence;
- redundancy;
- proactive / reactive / hybrid, used only as Table 2.4's labels;
- the cost–security tension;
- discrete-event;
- Barabási–Albert, Watts–Strogatz and scale-free;
- the vulnerability layer;
- the internal target node;
- the endpoints never being rewritten (said twice);
- synthetic vulnerabilities;
- double deep Q-network;
- the 38 agents and three sweeps (Appendix E repeats them);
- the optimised-OS withdrawal;
- the same-layer concurrency rule;
- "uniform in skill";
- the Kill Chain / ATT&CK attribution;
- "ten enumerations";
- Table 2.1's "combined-MTD evaluation" and "extended metric suite".

These are needed later and are not in chapter 2:

- the confusion penalty (ch4 l.5250, l.5088; ch5 l.8036; ch6 l.9279);
- return on attack and CVSS, which chapter 2 uses at l.848, l.1118 and in
  Figure 2.2, but chapter 3 defines at l.3929–3930;
- Zhang's exploit-time halving (ch3 l.3921 says Table 2.1 shows it; it does not);
- how each layer's deployment interrupts the attacker (ch5 l.8023–8028);
- which of the default network's hosts are targets (ch5 l.6361 uses "two database
  hosts").

Not every unused fact should go. Some are the frame the floats are organised by.
The three questions are the column headers of Tables 2.3 and 2.4. Proactive and
hybrid label Table 2.4's groups. Synthetic vulnerabilities is a validity limit
chapter 6 should cite. The per-item verdicts below say which to keep and why.

**G2. Naming drift, within chapter 2 and against the chapters that use it.**

| Object | Chapter 2 says | Later chapters say | Proposal |
|---|---|---|---|
| the six things the baseline attacker does | states (l.1079), phases (l.1082), state machine | *actions* (ch4 l.5256, l.5320, Figure 4.4a; ch5 l.7221); *phases* (l.5304) | ch2 binds them once, e.g. "a six-state machine whose states are its actions". **Registry ruling needed**: row 77 ratified *phase* for the baseline's six (2026-09-08), and row 47 ratified *action* for the method's parts (2026-09-25). Both are in live use for one object |
| the layer a deployment rewrites | network-layer / application-layer (l.1158–1161) | host layer / service layer (Tables 2.3, 5.3; ch5 l.8024 ff.) | host layer / service layer / credentials, as the placeholder's item (iv) already asks |
| the MTD event | rewrite (Fig 2.1 and 2.4 captions), MTD moves, mechanism fires (Fig 2.3), deployment (l.1011) | deployment | *deployment* for the event, *rewrite* for what a mechanism does to the network (registry row 64, which already rules this). Figure 2.4's caption "what an MTD rewrite leaves it" should read "what a deployment leaves it" |
| the database hosts | "database hosts" (l.833); "the objective" (Fig 2.2 legend); "target host" (Table 2.6) | two database hosts (l.6361), target (ch4 l.5131) | *target host* (registry row 61 retired *objective* for this sense: it collides with the attack profiles' operational objectives) |
| a run | "attack campaign" (l.995), "the life of the simulation" (l.844) | run; *campaign* is the APT's (l.4071) | *run* |
| MTDShield | selector, learned selector (Fig 2.3), "these agents" (l.1004) | agent (App. E) | one noun, defined at Table 2.4 |
| reactive | event-triggered (l.628), detection-triggered (l.1030) | — | one gloss |

**G3. Ch1 overlap.**

- §2.1 P1 sentences 2–3 restate ch1 P2 (the static-network premise, reconnaissance
  going out of date, the time advantage), with the same two citations.
- §2.2.3's first sentence restates ch1 P5's naming of the baseline attacker.
- The opener's first sentence restates ch1 P5.

The introduction has already given the reader all four. See M1, A1 and O2.

**G4. Placeholders and unresolved flags visible to a reader.** The disruption
placeholder (l.1170–1179) prints in italics on pages 8–10. Table 2.1 attributes
the two-layer HARM to Alavizadeh et al. with no citation (the l.722 VERIFY
comment: no bib entry). Both must be closed before the chapter is shared.

## 4. Structure and headings (S)

The chapter structure is fixed and right. It follows the V7 ruling and the README.
Two titles misstate their sections:

- **S1. §2.2.2 "MTD mechanisms" → "MTD mechanisms and deployment strategies."**
  Half the section, and Table 2.4, is the deployment strategies. This is the
  §5.3.3 heading's exact wording, so the two sections use the same name for the
  same pair. Tier: heading, Marc's ruling. The label `subsec:defence-mechanisms`
  can stay.
- **S2. §2.2.3 "Attacker model" → "Baseline attacker."** The section describes one
  attacker, and "attacker model" is the generic concept (registry row 68) that
  chapter 3 scores and chapter 4 builds. Four inbound `\ref`s already read as
  "the baseline attacker of Section 2.2.3" (l.3920, l.6388). Figure 2.1's module
  box stays "Attacker".
- **S3 (no change).** The §2.1 four-paragraph shape, one paragraph per question, is
  Marc's 2026-08-27 ruling and reads well. What changes is inside the paragraphs
  (M1–M5).
- **S4. §2.2.2's second paragraph carries seven ideas:** the strategies,
  proactive, MTDShield's choice, the 38 agents, the interval, the durations,
  concurrency and no reactive strategy. Split it into a strategies paragraph and a
  timing paragraph (D4), each opening on its claim (voice §(c)1).

## 5. Figures (F)

Every figure was run against the pitfall catalogue
(`.claude/skills/scrutinise-figure/diagram_best_practice.md` §4). Only hits are
listed. A full `scrutinise-figure` run (a cold reader who sees only the figure,
and a context critic) is the gate after the fixes land, not before.

### F1. Figure 2.1, the three modules (p. 4)

- **P2 / P10 (blocking for its job).** The Attacker box lists "what it holds / its
  procedure": the names of Figure 2.4's panels. These tell a reader nothing about
  the attacker. The MTD box's "deployment strategy / seven mechanisms" works.
  Proposal: give each box its content, not its sub-figure's panel names. For
  example: Attacker "six actions · visible subgraph"; MTD "five deployment
  strategies · seven mechanisms". The network box's three layers already do this.
  This overturns the 2026-09-09 rule that the modules "list exactly the panels of
  their own component figure" (conventions §n). It was a contents-page device, and
  a contents page is navigation, not content.
- **P12, caption (83 → about 35 words).**
  - Cut "The network is one network drawn at three magnifications, not three
    systems." It pre-empts a misreading of Figure 2.2, not of this figure, and
    belongs in 2.2's caption if anywhere.
  - Cut "Each module is opened in the figure named beneath it, and holds the panels
    that figure is built from." The italic "Figure 2.x" under each box already
    says it.
  - Keep the first two sentences.
- **P21 (clear).** The four couplings (observes, compromises, rewrites,
  interrupts) are the only float in the chapter that shows *interrupts*. That
  coupling is the one chapter 5 measures, and it is why the figure earns its place.

### F2. Figure 2.2, the network at three magnifications (p. 5)

- **Unreferenced in its own section.** No sentence in §2.2.1 points to it. Only
  ch5 l.6360 does. Add "(Figure 2.2)" to §2.2.1's first sentence (T1).
- **P14 / G2.** The legend's "the objective" (the database icon) should be *target
  host*, per registry row 61.
- **False caption claim.** "The host layer keys the four states a host can be in".
  The legend has five entries, and the target host is a role, not a state. The
  forward audit finds "four states" named and used nowhere. Proposal: "The host
  layer keys what the attacker has taken, what it can see, and the target host."
- **Depth label.** "exposed, depth 0" disagrees with the prose's "the first level
  is the exposed endpoints". Registry row 59 makes *level* the word. Proposal:
  "exposed endpoints, level 1". The figure's "deeper into the network" arrow can
  stay.
- **Rendering defect.** "credentials" overruns its inner box on the service-layer
  panel (visible at 2× on p. 5). Widen the box or shorten the label
  (`tools/ch2_fig22_network_model.html` l.121).
- **Over-claim, X1.** "runs the services, every one of which attaches to an
  internal target node". The code does not do this. `gen_internal_network`
  (`mtdnetwork/component/host.py:545-590`) attaches every *internal* service to
  the target node. The host's *exposed* services attach to internal services, and
  only keep a target edge where the Watts–Strogatz seed happened to draw one. The
  hub drawing is therefore silent on the exposed services, which is licensed; the
  caption's "every one" asserts a falsehood, which is not. Fix the caption (cut
  "every one of which attaches to an internal target node that carries no service
  of its own"), or draw one exposed service off the hub. Both are Marc's call.
- **P14.** "tried by return on attack" uses a term defined only in chapter 3. C2
  fixes it at the source.
- **P7 / P15 (option, not a defect).** The vulnerability panel's second gate ("and
  if adjacent to the internal target node") is simulator internals that no later
  chapter uses. It is true, so it may stay. If N8's silent form is taken, the gate
  leaves the panel too.

### F3. Figure 2.3, when MTD moves and what each mechanism rewrites (p. 7): **cut**

- **Referenced nowhere in the document** (the forward audit; confirmed by grep).
- **Its mechanism panel is Table 2.3 again.** Both list the same seven mechanisms,
  grouped by what each rewrites. The table adds the SDR class and a description of
  each; the figure adds a pictogram of each target.
- **Its strategy panel is Table 2.4's first column plus one sentence of prose.**
- The two floats also disagree in their row order (the figure has complete
  topology first, the table IP shuffle first). The caption says "group" where the
  prose says "layer". The arrows say "rewrite" twice and "rewrites" once.

Recommendation: cut Figure 2.3 and keep Table 2.3. Chapter 5's captions cite
`tab:defence-mechanisms` (l.8223, l.8377), and the table holds what is cited.
This overturns, on the duplication, the 2026-09-09 ruling that drew the roster
("a styled list reads very dry"). That ruling chose the figure's form over a list
*within* the figure. It did not weigh the figure against the table beside it.

Alternative, if Marc keeps the picture: cut Table 2.3's rows down to the
description column and put the class on the figure. That loses the one place the
SDR class and the layer sit side by side, which chapter 5 reads.

### F4. Figure 2.4, what the baseline attacker holds and how it proceeds (p. 9)

- **The caption claims what the drawing does not encode (P12, blocking).** "The
  upper panel gives what an MTD rewrite leaves it: the attack scenario, the hosts
  and the credentials survive; its view of the network does not." The four items
  are drawn identically in a 2 × 2 grid. Proposal: split the panel into "kept
  after a deployment" (attack scenario, compromised hosts, credentials stolen) and
  "rebuilt after a deployment" (the visible subgraph). This is the 2026-09-09
  intent (the tex comment at l.1050: "the holds table separates what a rewrite
  never takes back … from what it recomputes"), and it did not survive into the
  drawing.
- **P2, unlabelled transitions.** Three grey edges carry no label:
  - neighbours → enumerate;
  - brute-force → enumerate (failure abandons the host);
  - scan hosts ⇄ enumerate (the queue, and the re-route when no visible host
    remains).

  Table 2.5 explains them in prose. The figure's reader cannot tell a success edge
  from a failure edge. Proposal: label the brute-force return "fails", and the
  scan hosts ← enumerate edge "no host left". The other two read without labels.
- **G2.** The caption's "MTD rewrite" should be "deployment" (row 64).
- **Caption (68 → about 45 words).** Once the drawing encodes it, "the attack
  scenario, the hosts and the credentials survive; its view of the network does
  not" becomes redundant, so cut it. Replace the em dash in "the procedure — six
  states" with a colon.
- **Keep.** The dashed interrupt edges, one meaning for dash as §n rules, and the
  accent on the three moves that take a host. These are what chapter 5's
  disruption results need a reader to carry.

## 6. Tables (T)

- **T1. Table 2.1 (lineage).**
  - **Blocking:** the Alavizadeh attribution has no `\citep` (G4). Add the entry,
    or cut the clause "adding a service layer to Alavizadeh et al.'s two-layer
    HARM". Cutting it re-opens the §2.2.1 pass-5 condition C7, which traded that
    attribution out of the prose on the condition that the table carries it.
  - **Zhang's row** should add the confusion penalty and the exploit-time halving.
    Both are his (Zhang §4.4.3; extraction rows Z-TIM-07, Z-TIM-08). Chapter 3
    l.3920 already says the lineage table shows the halving, and chapter 4 leans on
    the penalty.
  - **Brown's "the combined-MTD evaluation" and Ho's "the extended metric suite"**
    are vague, and nothing later uses them (the forward audit). Name the metrics
    Ho added, or say what of Ho's the thesis uses: Ho is cited later only for
    intervals and the time limit (l.6444, Table 5.1). T3.
- **T2. Table 2.2 (lineage configurations).**
  - Its purpose goes unsaid. The sentence introducing it (l.710) says what it
    holds, not why the reader needs it now. It is the reference Table 5.1 is read
    against (the E5 ruling). One clause saying so tells a student why a parameter
    table sits in the background (T3).
  - Brown's interval is in ms while every other column is in seconds: "uniform on
    1 000–5 000 ms" reads as 1–5 s. Convert it in
    `data/misc/lineage_configurations.yaml`, and keep the ms value in the locator
    comment.
  - The row set stays: it mirrors Table 5.1's by design (E5).
- **T3. Table 2.3 (seven mechanisms).** Keep; it is the one F3 recommends
  surviving. Its caption "What to move and how: …" pre-states the two column heads
  the table already shows. Proposal: "The seven MTD mechanisms, from the pool of
  Brown, added to by Zhang, by SDR class and by what each rewrites." "Internal
  host" and "non-target service" appear in cells without definition. "Internal
  host" follows once the endpoints are defined. "Non-target service" goes if N8
  removes the target node from the prose.
- **T4. Table 2.4 (deployment strategies).**
  - MTDShield's cell runs to 36 words. "so movement follows the observed posture
    rather than the schedule" is the hybrid justification, and should move to
    §2.1's definition of hybrid (C3) so the cell can say what it does.
  - "the network's security metrics" names nothing a reader can picture. Appendix
    E names the inputs; name one or two, or say "the network's state".
  - X2 bears on the "hybrid" label (see §9).
- **T5. Table 2.5 (six states).**
  - Keep. The code names are used later (ch4 l.5613, Figure 4.4a).
  - "nearest to the foothold first": *foothold* is never defined. Say "nearest to
    the attacker's first compromised host", or define it in §2.2.3.
- **T6. Table 2.6 (two attack scenarios): fold into one sentence.** It is a
  two-row table. §2.2.3's first paragraph can carry it in the words the table
  already uses: "The attacker follows one of two attack scenarios: the general,
  which compromises 80 % of the hosts or stops when nothing new is discovered, and
  the targeted, which compromises one deep-embedded target host such as a database
  [brown2023; the 80 % is Zhang's]."
  - Re-point `tab:attacker-objectives` at l.5130 and l.6392 to
    `subsec:attacker-model`.
  - The move saves a float and a caption, and the prose loses nothing it did not
    already carry.

## 7. Prose ledger

Word deltas are measured on the rendered text. "Ruling" marks a proposal that
re-opens a recorded ruling; the ruling is named.

### Opener (session-generated connective prose, ratified 2026-09-26)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| O1 | cut "This chapter describes MTDSim and the MTD it models." | −9 | T1. The next sentence names both sections by what they do |
| O2 | S1 "The APT attacker model is executed inside MTDSim, the MTD simulator this dissertation inherits, and compared with the simulator's baseline attacker." restates ch1 P5 | ±0 | T2. The one sentence the opener lacks is the chapter's purpose: what later chapters take from it. Suggestion: "Chapter 3 scores attacker models in the vocabulary of MTD, and Chapters 4 and 5 build and evaluate an attacker inside MTDSim; this chapter gives both." Ratified text, so ratify on read |

### §2.1 Moving target defence (243 words)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| M1 | cut P1 sentences 2–3: "It inverts the conventional assumption … thwarted but not prevented \citep{ghosh2009nitrd}. By continuously changing … faster than it can be acted upon \citep{cho2020}." | −50 | T1, claim flag. S3 restates ch1 P2 (reconnaissance going out of date; the time advantage). S2 is used nowhere later, and "thwarted but not prevented" reads as a contradiction. `ghosh2009nitrd` stays cited in ch1. P1 becomes the definition alone |
| M2 | P3: cut "canonical" and "whose three primitives are complementary rather than partitioned \citep{cho2020}" | −9 | T1. *Canonical* is a §(h) hype adjective. The complementarity nuance is used nowhere later (the forward audit) |
| M3 | P3 examples "(IP mutation, topology reconfiguration)" → "(IP shuffle, topology shuffle)" | ±0 | T2, G2. Use the names Table 2.3 uses; one term per thing |
| M4 | P3 "*Redundancy* replicates components to preserve service while the other two operate." → "… to preserve service under compromise" | −3 | **X3, correctness.** Cho's definition (extraction l.60) is "to preserve service availability under compromise". "While the other two operate" is not in the source |
| M5 | P4: cut "for longer than it should be"; "When to move is the tension between cost and security" → "The choice of when trades cost against security" | −4 | T1 + T2. A question is not a tension. "Valid for longer" already carries the claim |
| M6 | keep P2 (the three questions and *what*) | 0 | keep. Tables 2.3 and 2.4 head their columns with these questions; this is where the reader learns them |

§2.1's hole is C3: *hybrid* is never defined. Yet Table 2.4 files MTDShield under
it, and the README's roster test asks that a reader classify every mechanism from
§2.1 alone.

### §2.2 preamble (91 words; session-generated, ratified)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| P1 | cut "and each addition is described where it is used" | −7 | T1. A promise the subsections keep without being told |
| P2 | Table 2.2 sentence: add why (T2 above) | +8 | T3 |
| P3 | keep "discrete-event simulator" without a gloss | 0 | Used nowhere later. It identifies the simulator, and a student can place it |

### §2.2.1 Network model (321 words incl. the pointer sentence)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| N1 | first sentence: add "(Figure 2.2)" after "a graph of graphs" | +2 | T1. F2's missing reference |
| N2 | cut "The construction mimics the scale-free characteristic of a real-world network \citep{brown2023}." and "constructed using the Barabási–Albert model \citep{barabasi1999}" | −17 | T1, claim flag. Used nowhere later. Without *scale-free*, "Barabási–Albert" says nothing to a student, so the pair goes or stays together. Marc's call: an examiner may value the realism grounding, and if so keep both |
| N3 | cut "the services connected in a service graph constructed using the Watts–Strogatz model \citep{watts1998}" | −14 | T1, **X1**. Used nowhere later. It also describes the seed, not the graph a host ends up with: the code removes the internal Watts–Strogatz edges and hubs every internal service to the target node (host.py:560-568). Figure 2.2 draws the hub, so the prose and the figure currently disagree |
| N4 | "five database hosts at the deepest level" → name them as the targeted attack scenario's target hosts | +4 | T3, G2. Chapter 5 (l.6361) sets two of them; nothing here says that they are the targets |
| N5 | "a small number of versioned services": give the number, or cut "versioned" | −1 | T3. Vague. "Versioned" does no work later |
| N6 | "The endpoints are never rewritten: they persist unchanged through the life of the simulation while everything around them can move, because …" → "The endpoints are never rewritten while everything around them can move, because …" | −10 | T1. "Never rewritten" and "persist unchanged through the life of the simulation" are one claim said twice. The rider "while everything around them can move" is kept (see D3) |
| N7 | P4 CVSS, impact | +15 | T3 → C2 |
| N8 | P4 host-falls rule: option (a) keep as is (true; the target node is explained only by Figure 2.2). Option (b), silent form: "A service is compromised when the impact of its exploited vulnerabilities accumulates past its threshold, and a compromised service can compromise its host." | (b) −6 | T2, Marc's call. The internal target node is used nowhere later (the forward audit) and is simulator internals (diagram P15). Silent is licensed, false is not, and "can" is true. (b) also takes the gate out of Figure 2.2 and "non-target" out of Table 2.3 |
| N9 | "The vulnerabilities are synthetic …": keep | 0 | Used nowhere later, but it is the validity limit an examiner raises first. The fix is for chapter 6's threats section to cite it (out of scope; flagged) |
| N10 | "The attacker never sees the whole topology. It only sees a visible subgraph, which comprises the endpoints plus all the compromised hosts and all of their neighbours." → "The attacker only sees a visible subgraph: the endpoints, the compromised hosts and their neighbours." | −12 | T1 (merge; the colon is the joint, flagged) |

### §2.2.2 MTD mechanisms (248 words)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| D1 | keep sentences 1–2 (shuffle and diversity only; split on attacker effect) | 0 | keep. This is where §2.1's vocabulary earns its place (README). Add "Table 2.3" as the only float pointer once F3 cuts Figure 2.3 |
| D2 | cut "The optimised OS assignment variant \citep{zhang2023} has been withdrawn from the mechanism pool: it added overhead without providing the diversity-assignment value." → one clause in §5.1 where the pool is declared | −22 | T1 move, claim flag. The withdrawal is this dissertation's ruling (D-17(c), 2026-08-27; `mtdsim_spec.md` MTD-09), stated as an agentless passive in a chapter that describes inherited things. That is methodology. "The diversity-assignment value" names nothing. Table 2.2 keeps Zhang's 80 s faithfully, because it is what Zhang ran |
| D3 | cut "Across all seven mechanisms, the endpoints are not manipulated, so their attack surface remains the same throughout the attack campaign, although the topology around them can move (Section~\ref{subsec:network-model})." | −33 | T1. **Ruling: overturns the "DO NOT RE-FLAG" on the W-6 rider (l.977)** on duplication, not on the rider's merit. The rider's scope, "while everything around them can move", survives verbatim in §2.2.1 (N6), where the endpoints are introduced. This sentence is the second telling of N6's claim, and its "attack campaign" means a run (G2) |
| D4 | split P2 at "The interval between deployments" into a strategies paragraph and a timing paragraph | 0 | S4 |
| D5 | "Four are time-triggered, or proactive;" → "Four are proactive;" | −3 | T1. §2.1 glosses *proactive* |
| D6 | cut "Tay trained 38 of these agents across three hyperparameter sweeps, released them with the simulator, and named the one with the highest score \citep{tay2024, tay2024code}." | −25 | T1 move, claim flag. Appendix E (l.10192) states it again and makes the choice from it; §5.1 (l.6441) can point there. "These agents" has no antecedent ("MTDShield" is introduced as a selector), and "38" collides with the 38 attack flows a reader has just met in ch1. Re-opens the 2026-09-25 placement ruling (l.1007): the background was to state the fact the choice rests on. The appendix states it next to the choice |
| D7 | "No operation is a policy choice: MTDShield chooses one of four of the MTD mechanisms, or nothing. That is the when not to move." → "MTDShield chooses one of four of the MTD mechanisms (complete topology shuffle, IP shuffle, OS diversity, service diversity), or *no operation*." | −6 | T1 cut ("That is the when not to move" is spoken residue) + T3 (name the four, App. E's table). Unnamed, "four of" is a number the reader cannot check. Chapter 5's "draws on the whole pool" contradicts Appendix E's "same four" (X4) |
| D8 | "The interval between deployments is 200\,s plus …, so deployments arrive close to periodically." → "The deployment interval is 200\,s plus …, so deployments arrive near-periodically." | −2 | T2, G2. *Deployment interval* is the ratified term (registry row 96) and is not defined anywhere in chapter 2. Table 5.1 (l.134) says "near-periodic (§2.2.2)", pointing here for a word this section does not use |
| D9 | keep "Two mechanisms rewriting the same layer cannot operate concurrently \citep{zhang2023}."; cut its repeat in the Figure 2.3 caption (moot if F3 lands) | 0 | Used nowhere later, but it constrains every strategy that deploys more than one mechanism. Keep one telling |
| D10 | "There are no purely reactive deployment strategies in the simulator: no detection channel is encoded, so a detection-triggered strategy is not possible." | — | **X2, contradiction.** See §9. Resolve before any rewording |

### §2.2.3 Attacker model (322 words incl. the placeholder)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| A1 | "The attacker model that existed originally in the simulator is what this dissertation terms the baseline attacker. It is scripted: …" → "The baseline attacker is scripted: …" | −16 | T1 (merge; "The baseline attacker" is the joint, flagged). Chapter 1 P5 named it. Naming it again is the re-definition voice §(0)5 bars |
| A2 | "a closed six-state machine" → "a six-state machine"; bind states to actions once (G2) | −1 | T1 + registry ruling. "Closed" is undefined |
| A3 | cut "This finite state machine is inspired by Lockheed Martin's Cyber Kill Chain and MITRE ATT\&CK \citep{…}." | −13 | T1, Marc's call. Used nowhere later as a fact about the baseline. ATT&CK is taught in §3.1.2, so here it arrives unexplained. The README licenses the attribution; it does not require it |
| A4 | cut "; Brown \citep{brown2023} gives the implementation detail" and carry the citation on the scenario sentence | −6 | T1. The pass-5 proposal already on the record (l.1093), still unruled. T6 absorbs it |
| A5 | P2: cut sentences 2–3 ("It exploits vulnerabilities in services, … reaching the host's neighbours. When a compromise is successful, … starts scanning its ports.") | −40 | T1, claim flag. S2 re-tells §2.2.1's compromise rule. S3 walks the transitions Table 2.5 and Figure 2.4 carry, contrary to the unit's own design note (l.1071: "floats carry the procedure … so the prose carries rules and assumptions"). S1 "advances using reachability and CVSS" is then replaced by the return-on-attack rule (C2). S4, the visible subgraph growing from its foothold, stays, with *foothold* defined or replaced (T5) |
| A6 | P3 disruption: "network-layer / application-layer" → "host-layer / service-layer"; add the credentials case; draft the placeholder's items (i)–(iii); keep "Compromised hosts stay compromised" as the closer | +60 net | T3, C1. Marc dictates (the l.1164 placeholder note: "I'll get back to it"). Content points in C1 |
| A7 | keep the closing sentence to chapter 3 | 0 | keep (ratified 2026-09-26) |

**Ledger arithmetic.** Cuts total about −300 words (O1, M1, M2, M4, M5, P1, N2, N3,
N6, N10, D2, D3, D5, D6, D7, D8, A1–A5). Additions total about +90 (N1, N4, N7,
P2, the C3 hybrid clause, the C2 definitions) plus about 90 for A6/C1. The result
is about 1 050 words, about 200 under the ledger, and the placeholder is gone.

**Minimal set**, if Marc takes only the highest-value cuts: M1, D3, D6, A1, A5 (−164
words). These are duplications of chapter 1, of §2.2.1, of Appendix E or of the
floats, and each one's claim survives elsewhere.

## 8. Content the chapter lacks (C), named, not drafted

- **C1. How a deployment disrupts the baseline attacker** (the placeholder, for
  §5.3.1 and ch4 l.5250).
  - The confusion penalty: about 20 s charged at each interruption, whatever the
    mechanism (Zhang §4.4.3, Z-TIM-08).
  - A host-layer deployment interrupts every action and costs the attacker its
    place, which sends it to scan hosts. A service-layer deployment interrupts only
    scan ports, exploit and brute force, and sends it to scan ports.
  - A user shuffle interrupts only brute force and sends the attacker to exploit.
    This explains the 1-in-100 result at ch5 l.8027.
  - In one vocabulary: host layer / service layer / credentials.

  Grounding: the placeholder's own items (i)–(iv), verified at
  `attack_operation.py` `apply_mtd_interrupt_cost` / `_handle_interrupt` and
  `mtd_operation.py` `_interrupt_adversary`. **The worked example the chapter
  lacks belongs here** (voice §(c)8): one deployment arriving mid-exploit, and what
  the attacker keeps and loses. Figure 2.4, once F4's split lands, is that example
  drawn. One sentence pointing at it may be enough.
- **C2. CVSS, return on attack and impact at first use.** Chapter 3 l.3929–3930
  already has the definition ("return on attack (RoA), a cost/impact ratio derived
  from Common Vulnerability Scoring System (CVSS) metrics"). It arrives after
  chapter 2 has used both, in §2.2.1 P4, Figure 2.2, Table 2.5 and §2.2.3 P2. Move
  it to §2.2.1 P4, where CVSS first appears, and have chapter 3 refer back.
  *Impact* (l.849, l.1143) needs one clause: what accumulates.
- **C3. Hybrid.** One clause in §2.1 P4 saying what *hybrid* combines (Cho 2020;
  the extraction's l.87 pointer is to the lit review, so verify the locator in
  Cho). Without it, Table 2.4's "hybrid" is a label the reader cannot check.
- **C4. The deployment interval and the time limit named as terms.** Table 5.1
  points to §2.2.2 for "near-periodic" (D8). The 15 000 s time limit appears in
  chapter 2 only as Ho's value in Table 2.2; chapter 4 (l.5655) uses it as a
  simulator fact. Decide whether the time limit is a simulator fact (it belongs in
  §2.2) or a setup choice (it belongs in chapter 5 only). The registry (row 98)
  treats it as a setup parameter, which argues for chapter 5.

## 9. Factual corrections and contradictions (X), verified

- **X1. Service graph (§2.2.1 P3; Figure 2.2 caption).** Prose: "a service graph
  constructed using the Watts–Strogatz model". Figure: every service on a hub.
  Code (`host.py:545-590`): the Watts–Strogatz graph seeds the host, then every
  edge between internal services is removed, and every internal service is joined
  to the target node. The exposed services keep edges to internal services and
  only sometimes to the target. So the prose names the seed, and the caption's
  "every one of which attaches" over-claims. N3 and the F2 caption fix resolve
  both.
- **X2. "No detection channel is encoded" (l.1030) against Appendix E.** Appendix
  E's configuration table (l.10245–10261) runs MTDShield at detection rate 1: "the
  share of decisions at which the agent is told the attacker's current action". A
  detection signal exists, and MTDShield reads it; nothing *triggers* a deployment
  on it. The true statement is narrower: no deployment strategy deploys on
  detection. MTDShield deploys on its fixed tick, choosing from what it is told.
  This also decides Table 2.4's classification. Time-triggered and
  detection-informed is exactly what makes "hybrid" right, and C3's definition
  should say so. Check the code before rewording; it is Marc's ruling.
- **X3. Redundancy** (M4): the Cho paraphrase is wrong. Fix as above.
- **X4. The pool random draws from** (out of chapter 2 scope, flagged). §5.1
  l.6440 says the random deployment strategy draws "on the whole pool (§2.2.2)".
  Appendix E l.10206 says it runs "over the same four mechanisms beside
  MTDShield". Chapter 2 is the target of the first reference, so its D7 wording
  should make the two pools visible.
- **X5. Zhang's lineage row** (T1): the confusion penalty and the halving are his,
  and chapter 3 l.3920 already says the table shows the halving.

## 10. Stale records to refresh once the rulings land

[`../notes/ch2_background/README.md`](../notes/ch2_background/README.md) is the
declared authority on ch2's shape, and it is stale in four places:

- "The tex has not been restructured": it has.
- Table 2.1 has "three columns": two, since 2026-09-02.
- Figure 2.1 "pre-installs … diversity [rewrites] the host layer": diversity
  rewrites the service layer (Table 2.3).
- The §2.2.2 heading is "Defence mechanisms".

Refresh it in the commit that applies these rulings. Out of chapter 2 but on the
same terms: ch3 l.3926 says "the two objectives" for the attack scenarios
(registry row 61), and Table B.5 l.9 says "substrate action" (row 51).

## Validation gate

- Every G / S / F / T / prose / C / X entry carries Marc's ruling (applied,
  declined, or amended).
- Applied entries are in the tex. Figures regenerate through
  `tools/ch2_model_figures.py` with its pool and type-floor checks passing.
- `tools/term_screen.py` shows 0 *network-layer* / *application-layer*, and 0
  *objective* in the scenario sense in chapter 2.
- The PDF builds with 0 undefined references and no new overfull boxes.
- A fresh cold reader who holds only chapter 1 and the revised chapter 2 can
  state what each MTD mechanism rewrites and what a deployment costs the baseline
  attacker. They can do it from the text and floats, without chapter 3.
- The `scrutinise-figure` gate passes on Figures 2.1, 2.2 and 2.4.

## Hard constraints

- Nothing applied unratified. Marc's dictated units (§2.1 ported from the lit
  review, §2.2.1, §2.2.2, §2.2.3) change only by the deletions and merges
  ratified here. Anything reworded is his.
- A figure may be silent on a nuance; it may not assert a falsehood (conventions
  §n).
- Registry rows 47, 59–64, 68, 72, 77 and 96 bind the terms. G2's states / phases
  / actions question needs a registry ruling before A2 is applied.

## Reading list

- `docs/thesis/dissertation.tex` l.542–1206, and the rendered pages 3–10.
- [`../workflows/background_conventions.md`](../workflows/background_conventions.md):
  the yardstick.
- [`../notes/ch2_background/README.md`](../notes/ch2_background/README.md): the
  shape authority (stale in places, §10).
- `docs/workflows/figure_table_conventions.md` §(n): the figure family's rulings.
- `tools/ch2_model_figures.py` and the four `tools/ch2_fig2*.html` sources.
