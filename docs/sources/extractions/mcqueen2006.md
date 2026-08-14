# McQueen et al. 2006 — extraction notes

> Miles A. McQueen, Wayne F. Boyer, Mark A. Flynn, George A. Beitel,
> "Time-to-Compromise Model for Cyber Risk Reduction Estimation", in *Quality
> of Protection* (QoP Workshop @ ESORICS 2005), Springer, 2006, pp. 49–64.
> INL preprint INL/CON-05-00649 (September 2005), OSTI 911165.
> Source file: `docs/sources/tactic_profiles/step_c/mcqueen2006_time_to_compromise.md`
> (+ `.pdf`; companion HICSS/SCADA report fetched alongside as
> `mcqueen2006_scada_risk_reduction.*`, unread).
> Relevance to this thesis: **the MTTC lineage root** — the model every later
> TTC variant adapts (Leversage & Byres, Nzoukou, Zieger β-TTC,
> [`ling2023`](ling2023.md) TTC_ICS), and the canonical citation for "declare a
> stage time, justify it in prose, admit what isn't validated".

### Relevance class

**L** (lineage) — definitional ancestor of the MTTC family our internal MTTC
metric descends from ([`../specs/metrics_semantics.md`](../../implementation/metrics_semantics.md));
also the strongest precedent for the Tier-3 declare-and-justify discipline.

### Used in lit review

Precedent survey (the "somewhat arbitrarily" bullet — now [fetched] against
the full text); tactic-profile §4 rows (Step C, 2026-07-05); methodology
chapter (validity register).

## Bibliographic anchor

- **Citation key**: `mcqueen2006`
- **DOI / URL**: https://doi.org/10.1007/978-0-387-36584-8_5 · open preprint
  https://www.osti.gov/biblio/911165
- **Pages cited from**: full preprint text (17 pp; page locators are preprint
  PDF pages)

## Relevant artefacts

### The model — TTC as a three-process random variable

**Source locator:** §3 (pp. 4–5); §3.4 Eq. (6) (pp. 11–12)

**Paraphrase:** T_pi = time for an attacker to gain privilege level *p* on
component *i*, "a measure of the effort expended by an attacker for a
successful attack assuming effort is expended uniformly" (§1). Three
subprocesses: **P1** — a known vulnerability with a readily available exploit
(always succeeds); **P2** — known vulnerability, no ready exploit (may fail);
**P3** — discovery of new vulnerabilities/exploits, always running in
parallel. P1/P2 mutually exclusive. Composite expectation (Eq. 6, under a
stated mutual-exclusivity approximation, justified because P3's PDF is far
more dispersed):

- `P1 = 1 − e^(−vm/k)` (search theory per Major; **stated simplifying
  assumption that exploits are uniformly distributed over vulnerabilities**)
- `t2 = 5.8 · ET` with ET the expected number of tries (Eq. 4, derived in the
  appendix from sampling-without-replacement)
- `t3 = ((V/AM) − 0.5) · 30.42 + 5.8`
- `T = t1·P1 + t2·(1−P1)(1−u) + t3·u·(1−P1)`, `u = (1 − AM/V)^v`, `u = 1` if
  `V = 0`.

Distribution shapes are *hypothesised*, not fitted: P1 ~ beta (1.3, 5.2, mean
1 day), P2 ~ gamma (2, 2.9, mean 5.8 days), P3 ~ exponential (constant
discovery rate, supported by Rescorla's finding that constant-rate could not
be rejected).

**Maps to:** [`ling2023`](ling2023.md) (TTC_ICS adapts every element) ·
[`../specs/metrics_semantics.md`](../../implementation/metrics_semantics.md) (MTTC
definitional lineage: McQueen → Leversage & Byres → Nzoukou → Zieger β-TTC →
TTC_ICS → substrate MTTC).

**Disposition for this thesis:** contrasted / lineage — note for
[`ling2023`](ling2023.md)'s open question: **McQueen's t1 is a flat 1 day
(8 h), with no CVSS term** — the `((10/c2 + 3.9/c3)/2)` form is TTC_ICS's own
modification, so the `/2`-as-average reading must be settled against Rencelj
Ling & Ekstedt's ICISSP 2022 paper, not here.

---

### Provenance of every number — the declare-and-justify register, verbatim

**Source locator:** §1 (p. 3); §3.1 Table 1 + §3.1.2 (pp. 5–6); §3.2.2 (p. 8);
Table 2 + §3.2.2 (pp. 9–10); §3.3 (pp. 10–11)

**Paraphrase:** each parameter's source is explicit, and the register is the
point:

- **The honest framing (§1):** "The estimation of time-to-compromise is
  particularly difficult because of the lack of reliable data. We recognize
  that some of the assumptions associated with our model have not been
  validated but we have attempted to provide justification with real data
  when data is available. **We have used expert elicitation or have made
  simple assumptions when data is unavailable.**"
- **k = 9447** — non-duplicate known vulnerabilities in the ICAT database
  (2005 era).
- **m by skill (Table 1): novice 50, beginner 150, intermediate 250, expert
  450** — novice anchored to "a Web site (metasploit) that has 50 exploits
  that are trivial to use"; the rest a "**postulated exponential growth** in
  readily available exploits as a function of skill level".
- **t1 = 8 hours (1 working day):** triangulated between Cohen's "a few days"
  and Jonsson's measured ~4 h (team of two, possibly 8 h total) — then:
  "**Somewhat arbitrarily, we decided to use 8 hours (one working day) as the
  mean time for a successful attack in Process 1**". Skill-independent by
  declared assumption ("the time it takes for an expert or novice … is
  considered to be roughly similar").
- **5.8 days** — average time from vulnerability announcement to exploit-code
  availability, Symantec Internet Security Threat Report VI (2004). The one
  cleanly empirical anchor.
- **AM/V by skill (Table 2): 0.15 / 0.30 / 0.55 / 1.00** — a team expert
  judged a **sample of 20 ICAT vulnerabilities** for exploit availability per
  skill level. Expert elicitation, n = 20, criteria stated per level.
- **MTBV = 30.42 days** — from Rescorla's OS vulnerability data; scaled by
  V/AM per skill; midpoint correction (−0.5·MTBV); plus the 5.8-day exploit
  lag.
- **Self-declared drawbacks (§6):** dependencies between components
  unmodelled; m-as-skill-proxy **not validated**; "The assumption that
  exploits are uniformly distributed over vulnerabilities **is incorrect**"
  (their hypothesis: popular exploits concentrate); P1/P2 PDFs not validated.
  §7: validation experiments and **sensitivity analysis** named as future
  work.

**Maps to:** [`../notes/2026-07-04_operational_validation_the_bar.md`](../../notes/ch4_methods/operational_validation.md)
(Tier-3 discipline: declared + justified + swept is the lineage norm from the
root) · [`../notes/2026-07-04_tactic_duration_precedent_survey.md`](../../notes/ch2_background/tactic_duration_precedent_survey.md)
(the "somewhat arbitrarily" bullet — confirmed [fetched], full text).

**Disposition for this thesis:** verified [fetched] — the survey's
characterisation is exact: a blend of expert elicitation, thin empirical
anchoring, and admitted arbitrariness, *with the admissions in the text*.
This is the citation that makes honest declaration a methodological register,
not a weakness.

---

### Worked numbers — the CS60 case study and the skill gradient

**Source locator:** §4 (pp. 12–14), Fig. 9

**Paraphrase:** on the CS60 SCADA testbed, the dominant-path component
(APPS1) gets expected TTC (days, novice / beginner / intermediate / expert):
**baseline 55.5 / 13.2 / 6.5 / 2.9; enhanced 79.1 / 15.2 / 7.6 / 3.8;
hypothetical zero known vulnerabilities 193.4 / 92.0 / 45.9 / 21.0.** The
punchline pair: total system vulnerabilities cut **86%**, but the dominant
attack path's TTC rose only **13–30%** (component-level vuln cut only 42%);
a hypothetical 100% cut raises TTC 240–624%. And the model's own reading:
"**for skilled attackers the time-to-compromise is not a strong function of
the number of vulnerabilities**" (§3.4, Fig. 8 discussion). Explicitly:
"These estimates of time-to-compromise have not been validated but simply
show how the model may be applied to a real system."

The APPS1 vulnerability inputs behind these (Eq. 6): **19** baseline / **11**
enhanced root-access vulnerabilities (the 42% component-level cut), for the
compromise type "root access from a launch site" — so the worked TTCs are
reproducible from the extraction. Expert degeneracy is explicit in the model:
"For an expert, the average number of tries is one" (§3.2.2), so expert t2 is
a flat 5.8 days and the Process-3 term drops (u = 0).

**Maps to:** the group-anchor argument (skill dominates technique/vuln detail
— same degeneracy [`ling2023`](ling2023.md) shows at expert level) · L4
metrics framing: aggregate hardening ≠ dominant-path hardening is the same
logic as our attack-path-exposure metric
([`../specs/metrics_semantics.md`](../../implementation/metrics_semantics.md)).

**Disposition for this thesis:** verified [fetched]. Hour-to-month scale:
expert 2.9 days → novice 55.5 days on the same component — relative-structure
evidence (skill spread ~19×), not absolute anchors for our substrate.

---

### The zero-vulnerability row IS a declared per-skill dwell constant (t3)

**Source locator:** §3.3 Eq. (5), p. 11; Fig. 9 "zero known vulnerabilities"
row, p. 13

**Paraphrase:** the most directly reusable finding, surfaced by the
completeness critic. Eq. (5)'s scaling term V/AM is the **reciprocal of the
Table-2 fraction** (6.67 / 3.33 / 1.82 / 1.0 for novice→expert), *not* the
component's own vulnerability count — so t3 is a per-**skill** constant, not a
per-component one. Substituting: t3 = (1/0.15 − 0.5)·30.42 + 5.8 = **193.4 d
(novice)**, and likewise **92.0 (beginner), 45.9 (intermediate), 21.0
(expert)** — exactly the Fig. 9 "zero known vulnerabilities" row (verified
arithmetically). These are the model's standalone **Process-3 dwell constants
per skill level**: the declared time to compromise a component with *no known
vulnerability*, i.e. the "find-a-new-vuln-and-write-an-exploit" dwell. For an
expert-APT assumption this is **21 days** — the closest thing in the lineage
to a declared per-stage dwell for the hard, no-easy-exploit case, and a sane
order-of-magnitude sanity check for any stealth-tactic dwell (weeks, not
seconds or years).

**Maps to:** [`../notes/2026-07-04_operational_validation_the_bar.md`](../../notes/ch4_methods/operational_validation.md)
(a Tier-2/3 declared dwell with full provenance) · the objective/stealth group
anchors (order-of-magnitude plausibility envelope).

**Disposition for this thesis:** verified [fetched] — the single most usable
number in the paper for a *declared per-stage dwell* precedent; badge as
Tier-2 (literature-derived, McQueen expert elicitation + Rescorla MTBV), swept.

---

### Definitional register — what TTC is and its stated limits

**Source locator:** §1 p. 3; §3.4 p. 11; §3.3 p. 11; §6 p. 15; abstract p. 2

**Paraphrase:** the definitional moves that belong in the methodology
chapter's validity register, all *asserted* at the lineage root:

- TTC is a **risk proxy by stated belief**: "We *believe* that as the
  time-to-compromise is increased, the likelihood of successful attack, and
  therefore risk, tends to decrease" (§1). Never validated — a declared bridge.
- **Finite TTC at zero known vulnerabilities** is deliberate: "a system with no
  known vulnerabilities continues to be at risk because of vulnerabilities that
  exist but are currently unknown, and we would like to measure that risk"
  (§1) — the definitional ground for Process 3 and the 21–193 day constants.
- **Expected-value-only**: "For now, the analysis only uses the expected value
  of the time-to-compromise" (§3.4) — the hypothesised beta/gamma/exponential
  PDFs are never actually used; every reported number is a mean. Precedent for
  our own mean-vs-distribution choice: the lineage root ran on expectations.
- **TTC decays over time absent constant defender effort**: "the
  time-to-compromise a component *decreases over time*, unless there is
  constant effort to install patches or disable services as soon as new
  vulnerabilities are discovered" (§6) — TTC is time-varying, held up only by
  continuous defender action. Near-direct MTD relevance (a shuffle is exactly
  such continuous effort).
- **Patching assumed ineffective in Process 3**, defended with data: patch
  release is assumed not to close the window because Browne et al. "seems to
  confirm" poor-system-administration, "and control systems may be slower"
  (§3.3) — a declared assumption backed by a citation, the register exactly.
- Scope qualifier: TTC is defined only for components **"visible to an
  attacker"** (abstract, §6).

**Disposition for this thesis:** verified [fetched] — the founding-paper
evidence that declare-a-definition-and-state-its-limits is the lineage
practice; cite in the validity section alongside the parameter register.

---

### Emergent idea — the sweep discipline is inherited, not invented

**Source locator:** §5 (alternative simplistic models); §6–§7

**Paraphrase:** the paper rejects the binary "open/closed door" model (too
pessimistic, ignores skill) and vulnerability-count metrics (too optimistic,
implies linear TTC) — arguing that a *structured, skill-conditioned,
declared* model beats both naive extremes even unvalidated. Combined with §7
naming sensitivity analysis as the required follow-up, this is the
declare-and-sweep norm being *founded*: twenty years on, the field (Bland
2020, MAL, TTC_ICS) still runs exactly this pattern, which is what licenses
our Tier-3 + sweep as continuous with the lineage rather than a shortcut.

**Disposition for this thesis:** adopted-as-argument (our synthesis; the
paper doesn't make the historical claim).

## Open questions / things to verify

- Companion report (`mcqueen2006_scada_risk_reduction.*`, HICSS/INL) — fetched,
  unread; contains the full 10-step methodology and compromise graphs. Read
  only if the graph-theoretic side ever becomes load-bearing.
- Figure-adjacent text (flow-chart labels, Figs 1/3/6) interleaves the pypdf
  text at pp. 5–10 — harmless, but quote only from sentences verified in
  running prose.
- Eq. (4)'s full symbolic form is glyph-mangled in the parse (`/g184…`); the
  appendix derivation logic is legible and captured, the typeset formula is
  `[parse-uncertain]` — recover from the PDF if the exact form is ever quoted.

## Out of scope for this thesis

The 10-step risk-reduction methodology (steps 1–5, 7–10) beyond context; CS60
testbed scan inventories (ports/holes/warnings counts); related-work survey
(HMMs, privilege graphs, attack trees); the false-exploit-publication and
scanner-spoofing defence speculations (§6).
