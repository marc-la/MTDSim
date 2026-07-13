# Xiong et al. 2021 — extraction notes

> Wenjun Xiong, Emeline Legrand, Oscar Åberg, Robert Lagerström, "Cyber
> security threat modeling based on the MITRE Enterprise ATT&CK Matrix",
> *Software and Systems Modeling* 21:157–177, 2022 (online 18 June 2021; open
> access).
> Source file: `docs/sources/tactic_profiles/step_c/s10270-021-00898-7.md`
> (+ `.pdf`, gitignored).
> Relevance to this thesis: the flagship ATT&CK-wide attack-simulation
> language (enterpriseLang, MAL-based) — the precedent survey's technique-level
> TTC precedent. Read cover-to-cover for Step C; the survey's `[search]` flag on
> "expert-declared distributions" is **resolved with a correction** below.

### Relevance class

**C** (contrasted) — same layer as the substrate-comparability precedents: a
simulation formalism over ATT&CK whose timing, on inspection, is *absent at
publication*. Strengthens the gap statement beyond what the survey recorded.

### Used in lit review

Precedent survey (technique-level TTC row — corrected 2026-07-05);
tactic-profile §4 rows (Step C).

## Bibliographic anchor

- **Citation key**: `xiong2021`
- **DOI / URL**: https://doi.org/10.1007/s10270-021-00898-7
- **Pages cited from**: full text (157–177)

⚠ **Disambiguation:** there are two load-bearing "Xiong 2021"s. This file is
the **SoSyM enterpriseLang** paper. The companion that actually addresses
where TTC distributions come from is **Xiong, Hacks & Lagerström 2021, CSIMQ
26:55–77** (ref [56] of this paper) — fetched to
`docs/sources/tactic_profiles/step_c/xiong2021_csimq_distributions.*`, not yet
extracted. Do not conflate them in citations.

## Relevant artefacts

### The headline reconciliation — enterpriseLang ships *untimed*

**Source locator:** §6.1 (Ukraine simulation, text at Fig. 9); §8 Conclusion

**Paraphrase:** the precedent survey characterised enterpriseLang as carrying
"expert-declared per-technique TTC distributions" `[search]`. The primary
source says something stronger for our gap argument: the MAL machinery
*supports* per-step TTC distributions, but **the published enterpriseLang does
not assign them** — the simulation figures are drawn with equal-width edges
for exactly this reason, and assigning distributions is deferred to future
work, pointing at the CSIMQ companion [56].

**Quote (the two load-bearing sentences):**
> "Here, the lines are of equal width owing to the lack of probability
> distributions that can be assigned to attack steps and defenses to describe
> the efforts required for attackers to exploit certain attack steps." (§6.1)

> "Thus, another direction for future work is to assign probability
> distributions to the attack steps/defenses in order to provide more
> realistic simulation results [56]." (§8)

**Maps to:** [`../notes/2026-07-04_tactic_duration_precedent_survey.md`](../notes/2026-07-04_tactic_duration_precedent_survey.md)
§"The one per-technique yes" (Xiong bullet — corrected)

**Disposition for this thesis:** verified [fetched], **corrects the survey**:
even the flagship ATT&CK-wide simulation language was published with timing as
an open slot, not expert-declared defaults. Secondary characterisation of the
CSIMQ method (via [`ling2023`](ling2023.md) §Related Work): distributions
assigned by systematic literature review with per-source credibility rating,
"qualitative rather than quantitative" — reconcile against the fetched CSIMQ
PDF before citing that method directly.

---

### MAL TTC semantics — additive dwell along a shortest path

**Source locator:** §3.2 (global/local TTC definition); §5.3 Computational
performance

**Paraphrase:** MAL's timing model: each attack step has a **local TTC**
sampled from an assigned probability distribution; the **global TTC** of a
step is the shortest time to reach it from the entry point — parent's global
TTC plus the child's local increment, computed with a modified single-source
shortest-path algorithm wrapped in Monte Carlo (sampled graphs; the resulting
global-TTC set approximates the distribution). A larger TTC ⇒ more secure
system. Performance: 1000 sampled graphs at ~half a million nodes in under
three minutes on a MacBook. Rational-adversary assumption: the attacker takes
the shortest path. Steps are typed **OR** (reachable when any parent
completes) vs **AND** (all parents required — and a step is forced to type
`&` merely by having at least one Defense attached, §5.1.2); the modified
SSSP only *approximates* AND-step composition ("the benefit of the
modification is the ability to approximate AND attack steps with maintained
computational efficiency", §5.3). Conjunctive dwell composition is exactly
the decision our timeline runner faces, and the formal precedent handles it
by approximation, not exactly — carry the caveat if citing this as the TTC
precedent. (The §5.3 OR/AND formulas themselves are lost in the md parse —
headers survive, equations don't; `[parse-uncertain]`, recover from the PDF
if ever needed.)

**Maps to:** [`../handoffs/2026-07-03_l3_timeline_runner.md`](../handoffs/2026-07-03_l3_timeline_runner.md)
(the timeline = sum of per-state dwells is the same additive semantics, at
tactic rather than technique grain) · [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md)
(internal MTTC)

**Disposition for this thesis:** contrasted — direct formal precedent that
"time to objective = sum of per-state times along a path" is standard
attack-simulation semantics; the innovation gap is only *which grain* carries
the time and *how the values are justified*.

---

### The pre-split tactic surface — technique counts per tactic

**Source locator:** §3.1.1 (12-tactic list); §3.1.2

**Paraphrase:** the paper works on the pre-v19 Enterprise Matrix: **12
tactics** (no Reconnaissance / Resource Development, no stealth /
defense-impairment split), **266 techniques**, with per-tactic technique
counts ranging from **9 (Exfiltration, the thinnest) to 69 (Defense Evasion,
the fattest)**. Commensurability caveat: 266 flat techniques is the
*pre-sub-technique* matrix (submitted July 2020, before the October 2020
restructure), so these per-tactic counts are **not directly comparable** to
v19.1 counts — use them only as relative-breadth texture. Multi-tactic
techniques are handled as tags (Valid Accounts carries four tactics).
Asset-side counts after conversion: 222 attack steps on Windows, 134 Linux,
160 macOS; 41 defenses, the top one (Privileged Account Management) covering
37 attack steps (Table 2). Design claim licensing the "ATT&CK-wide" label:
"The full range of attacks/defenses (techniques/mitigations) detailed by the
MITRE ATT&CK Matrix is covered in our proposed enterpriseLang" (§4, Step 2).

**Maps to:** profiles [`07_stealth`](../tactic_profiles/07_stealth.md) /
[`08_defense-impairment`](../tactic_profiles/08_defense-impairment.md) (the
old defense-evasion's 69-technique breadth is context for the v19.1 split
allocation) · [`14_exfiltration`](../tactic_profiles/14_exfiltration.md)
(thinnest tactic).

**Disposition for this thesis:** verified [fetched] — background texture, no
timing content.

---

### Privilege escalation as an explicit permission gate

**Source locator:** §5.1.2 "Permissions Levels" bullet; §5.1.1 (Process
Discovery example)

**Paraphrase:** enterpriseLang models permissions as a hard reachability
gate: an adversary holding only `userRights` **cannot execute
Administrator-required attack steps** (e.g. Process Discovery requires
Administrator); `adminRights` implies `userRights`; and "an adversary can
level up through Privilege Escalation tactic to gain adminRights from
userRights". Structurally: privilege-escalation is the state transition that
*unlocks a whole class of downstream techniques* — its dwell is spent before
an admin-only subset of every later tactic becomes reachable.

**Maps to:** [`06_privilege-escalation`](../tactic_profiles/06_privilege-escalation.md)
§4 (structural-role evidence; no timing).

**Disposition for this thesis:** verified [fetched] — formal-model precedent
for PE as a gating state rather than an optional detour.

---

### Case-study dwell anecdote — Cayman National Bank heist

**Source locator:** §6.2

**Paraphrase:** in the modelled real-world case, two attacker groups gained
access (VPN exploit; spearphish + user execution), used account manipulation
to persist and follow the bank's investigation by reading investigators'
e-mail, and **"remained active on the bank's networks for a few months"**
before the first fraudulent SWIFT transaction (~£100k). Months-scale
persistence/C2 dwell with objective-execution deferred to the end — narrative
corroboration for the low-and-slow group at whole-campaign scale, financial
(not espionage) motive.

**Maps to:** profiles [`05_persistence`](../tactic_profiles/05_persistence.md) /
[`13_command-and-control`](../tactic_profiles/13_command-and-control.md) §4
(anecdote row) · consistent with alshamrani2019's APT dwell character.

**Disposition for this thesis:** verified [fetched] (as the paper reports the
case, which itself cites a CSO Online account — second-hand at origin; treat
as narrative corroboration, not a statistic).

## Open questions / things to verify

- **CSIMQ companion** (Xiong, Hacks & Lagerström 2021, CSIMQ 26:55–77) —
  fetched to `step_c/xiong2021_csimq_distributions.*` and read for the sourcing
  question. **Flag settled (2026-07-05):** its method is a **systematic
  literature review with credibility assessment** — "Because the sources are of
  various types and include qualitative studies, we assess their quality by
  credibility assessment. We then interpret and convert information into
  probability distributions" (§4–5) — explicitly framed as an *improvement* on
  the prior default that "we often rely on security experts to model them" (§Abstract/§5).
  So the survey's "expert-declared per-technique TTC" [search] is **corrected**:
  the distributions are SLR-derived-and-credibility-rated qualitative→quantitative
  conversions (matching [`ling2023`](ling2023.md)'s characterisation), not raw
  expert declaration — but still *not empirically fitted rates*. A worked
  example assigns e.g. `Bernoulli(0.712)·Exponential(1)` to a step. Treat as a
  Targeted source; no separate full extraction — this note + the survey update
  carry it.
- **md-parse coverage gaps in the working copy**: the §5/§5.1.1 opener (the
  per-technique extraction-item list), Table 1, the §6/§6.1 openers, the §5.3
  OR/AND equations, and nearly all of **§7 Discussion** are lost to figure
  text in the parse — so any §7 limitation caveats bearing on timing are
  unverifiable from the md; recover from the PDF before citing §7. "Pages
  cited from: full text" means *the surviving md text* was read in full.
- Ukraine/Cayman case narratives originate in secondary reports (MIT thesis,
  CSO Online) — fine as texture, not as timing statistics.

## Out of scope for this thesis

MAL/DSL construction mechanics (§5.1 conversion rules, AND/OR step types,
asset associations); securiCAD tooling; the 79 test cases; EA/ontology related
work (§2.3); defense-coverage Table 2 beyond the count quoted above.
