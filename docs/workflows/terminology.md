---
status: living
created: 2026-08-20
updated: 2026-09-04   # PROPOSED attacker-model/threat-model split row (§3.2.1 walk); 2026-09-03 flow-instance row (flow lowercase, Attack Flow reserved for the language) ratified from the §3.1.3 pass-6 split-stream census
---

# Terminology registry — one term per concept across the dissertation

**Status: living.** The dissertation-surface registry the drafting pipeline
standardises against: one canonical term per concept, ruled by Marc, growing
as drafting meets new clusters. Executes the registry step of the 2026-08-19
terminology-standardisation handoff (retired 2026-08-20; `git log` holds it);
consumed by pass 6 (the `voice-pass` skill), and — once ruled — by
`repair-dictation` (`[term]` flags) and `scrutinise-draft` (consistency row).

**The rules of the registry:**

- Every row is **RATIFIED** (Marc ruled it; source cited) or **PROPOSED**
  (recommendation awaiting his ruling). Only RATIFIED rows are enforced;
  PROPOSED rows are re-surfaced, never applied.
- **No auto-substitution, ever.** Sessions flag and propose; Marc's ruling (or
  his hand) makes the change.
- **Scope: the dissertation's surface only.** Repo/docs vocabulary (substrate,
  outcome overlay, OGASP, thesis-vs-repo ladder) is not renamed; where the two
  vocabularies meet, the mapping is stated once (architecture.md §(b) pattern).
- **Distinct objects are never merged.** Some apparent synonyms name different
  things (the token is not the attacker; the Petri net is not the profile) —
  conflations are flagged as errors, not standardised.
- A session meeting an unregistered cluster (two names for one concept in
  dissertation-bound prose) **adds a PROPOSED row** with census counts and one
  recommendation, and bumps `updated`.

Census counts below are from `docs/thesis/dissertation.tex` as of 2026-08-20
(§4.1–§4.2 drafted); reproduce with `grep -oi "<variant>" dissertation.tex | wc -l`.
Counts are occurrence counts, not defect counts — some uses of a deprecated
string are legitimate (noted per row).

## The registry

### Ratified

| Concept | Canonical | Deprecated / watched variants | Ruling |
|---|---|---|---|
| The proposed attacker model | **movement attacker** (10) | *attacker agent* — CARVE-OUT ruled (Marc, 2026-08-20): legitimate in the runtime-traversal sense (the walker in L4; the ratified L4 heading uses it); flag only uses naming the *model*. Bare *the model*. *Attacker model* (11) is legitimate as the generic concept (criterion contexts) — watch for uses meaning ours. **The token (8) is a distinct object** (the marking that moves in the net) — flag conflations only | V5, 2026-08-11; carve-out 2026-08-20 |
| The inherited scripted attacker | **baseline attacker** (2) | *inherited attacker* (2), *original attacker* (1), *existing attack model*; *the finite state machine* (1) when naming the attacker (as its mechanism, legitimate) | V5, 2026-08-11 |
| The layer trichotomy | **movement layer** (8) / **controller layer** (6) / **action layer** (11) | *porting layer*, *the interface*; *the join* as a name (as a description of what the controller does, legitimate) | architecture §(f); 2026-08-16 frame |
| The L2 object | **attack profiles** (10) | bare *the nets* for profiles — the GSPN is the L3 formalisation of a profile, not a synonym; flag conflations only | ratified (V-series) |
| The L3 formalism | **generalised stochastic Petri net** | *general* stochastic Petri net — never | Marc, 2026-08-16 |
| The added pre-intrusion structure | **pre-intrusion overlay** | *synthetic overlay* (repo term — stays out of the chapter) | Marc, 2026-08-17 |
| The genre identification | **threat model** is the field's recognised term for the section's role; **movement attacker** is this work's name for the model ("we are putting names on things") — the identification is stated **once**, in the ch4 preamble opener (the §4.2 preamble until the 2026-09-04 restructure), and after it *movement attacker* carries; *threat model* recurs only when speaking the genre's language against the literature, never as a drifting synonym for our model | bare *threat model* as a name for our model anywhere past the opener — watch (census: 2 — the §4.1.1 heading and the preamble opener; the §4.1.1 heading is gone with the 2026-09-04 cut of §4.1, so 1) | Marc, 2026-08-20 |
| The simulator | **MTDSim** at first use and wherever ambiguity threatens; **the simulator** as the running short form | *the original simulator*, *the inherited simulator* — the inheritance is established once in ch2; the qualifier re-argues it every time. *"the simulator we are inheriting"* (§4.2.4.2 penalty ¶) kept: the inheritance clause does argument work there (why the penalty is maintained) | Marc, 2026-08-20 (voice-pass ruling) |
| The six inherited operations (the callable unit) | **verb** — fixed by the load-bearing ruled phrase *tactic-to-verb mapping* | *attack operation*, *attack action*, *attack phase*. *Action* meaning a runtime execution (e.g. "the actions in MTDSim", "zero or one actions at a time") read as a distinct sense and left — flag conflations only | Marc, 2026-08-20 (voice-pass ruling) |
| The declared weight object | **failure matrix**; long form at first substantive use: *the tactic-to-tactic failure weight matrix* (placed at the §4.2.4.1 defining ¶ — the ruled spine sentence keeps the short form) | *failure weight set*, bare *weight set*; *outcome overlay* (repo term, stays out) | Marc, 2026-08-20 (voice-pass ruling) |
| Attacker time on a tactic | **dwell time** | *duration*, *draw time*, *tactic timing* when meaning dwell; *dwell* alone fine in compounds (dwell catalogue, dwell standard-of-evidence) | Marc, 2026-08-20 (voice-pass ruling) |
| The work's self-name | **this thesis** | *this paper* (dictation residue from paper-framing); *this work* / *this dissertation* unused | Marc, 2026-08-20 (voice-pass ruling) |
| The party MTD defends against (generic, any chapter) | **attacker** (106) | *adversary* (1, §2.1 S3 — replaced 2026-08-27); the field's *adversary* stays only inside quoted or cited phrasing | Marc, 2026-08-27 (§2.1 voice-pass ruling) |
| The mechanism that makes dwell stochastic | **the exponential draw** (noun form; *drawn exponentially* as the verbal form) | *exponentiation mechanism* (also imprecise: exponentiation is raising to a power), *exponential element*, *exponential factor*; *the exponential defence* (L3 ceiling ¶) is a different object (the justification, not the mechanism) — never merged | Marc, 2026-08-20 (voice-pass ruling) |
| Network depth (the tiers hosts sit in, ingress first) | **level** (Brown 2023's word: "levels of depth") | *layer* in the depth sense — collides with the three HARM layers (host / service / vulnerability); *depth* stays as the axis noun (*levels of depth*, the figure's face label) | Marc, 2026-08-27 (§2.2.1 voice-pass ruling) |
| The ingress hosts | **exposed endpoints** at first fix; **the endpoints** thereafter | *exposed first-layer hosts*, *the endpoints, the first layer* — appositive re-definitions | Marc, 2026-08-27 (§2.2.1 voice-pass ruling) |
| The two objectives of the baseline attacker | **objective** as the noun; **opportunistic objective** / **targeted objective** as the pair | *scenario* (Brown 2023's word) and *general* (Brown's label for the first objective) --- both stay only inside Brown's cited phrasing; the mapping is stated **once**, in the Table 2.3 caption (*Brown's general and target attack scenarios*), and after it *opportunistic* carries. *Takeover* (Brown's gloss), *network-wide*, *untargeted* --- never as names (as parenthetical descriptions, legitimate). **The manner sense of *opportunistic* is a distinct sense** (credentials reused opportunistically, opportunistic re-scan, holm2014's opportunistic population in the exponential note) --- never merged; flag conflations only. Repo vocabulary keeps *general* (`network_type == 1`, the probes, the handoffs, the code comments) --- registry scope rule | Marc, 2026-08-27 (*objective*, §2.2.3 voice-pass ruling); Marc, 2026-08-31 (*opportunistic* replaces *general*) |
| The five when-options (covering term) | **deployment strategy** (the five: four execution schemes + MTDShield) | *execution scheme* as the covering term — reserved for Zhang's four; *scheme* applied to MTDShield — never | Marc, 2026-09-02 (§2.2.2 drafting) |
| Tay's selector | **MTDShield** (Tay's own name); first-use apposition *Tay's reinforcement-learning selector*; classified **hybrid** (time-triggered evaluation, posture-conditioned movement) | *the reactive selector* (superseded 2026-09-02 — Tay's own word, kept only in cited phrasing), *learned selector*, *the defender agent* as its name | Marc, 2026-09-02 (hybrid ruling + §2.2.2 pass 6) |
| The defensive move as a scheduling event (the thing whose interval is drawn) | **deployment** | *MTD mutation* (only inside Zhang's cited phrasing); **rewrite is a distinct sense** — what a mechanism does to the network (the Rewrites column, "never rewritten") — never merged | Marc, 2026-09-02 (§2.2.2 pass 6) |
| The S family of SDR (class noun) | **shuffle** (with *diversity* as its pair) | *shuffling* — only inside the cited taxonomy's own phrasing (§2.1's primitive walk, Cho/Hong--Kim) | Marc, 2026-09-02 (§2.2.2 pass 6) |
| The APT party as a named class member | **APT attacker** (Alshamrani 2019's own phrase) | *APT actor* — never as the class name; *actor* stays only inside source-echo phrasing (*Volt Typhoon actors* is the advisory's term — legitimate, cited-adjacent) | Marc, 2026-09-02 (§3.1.1 pass-6 ruling) |
| An instance document of the Attack Flow language | **flow** (lowercase; *Attack Flow* reserved for the language/project) | *an Attack Flow* as a count noun; *example Attack Flow* | Marc, 2026-09-03 (§3.1.3 pass-6 ruling) |

### Proposed — awaiting Marc's ruling pass

| Concept | Recommendation | Alternatives considered | Census |
|---|---|---|---|
| The attacker-model / threat-model split, thesis-wide | **attacker model** as the one term for the modelled adversary everywhere the thesis speaks in its own voice; *threat model* survives only inside quotations, cited section titles, and where a surveyed work's own threat-model statement is the object (its genre role, per the ratified 2026-08-20 row). Marc's spoken ask (2026-09-04, §3.2.1 walk): "standardise to attacker models ... threat model is the superset ... so we're referring to the same thing everywhere". **Conflict to rule:** the RATIFIED row above already licenses *threat model* "when speaking the genre's language against the literature", which covers most of ch3 §3.3 (the cross-section scores the works' threat models; Table 3.2 caption; the §3.3.3 heading) and ch4 §4.1.1's heading (gone: §4.1 cut 2026-09-04). Applied in §3.2.1 only. **Data point, 2026-09-04:** Marc titled the restructured ch4 "APT attacker model" — own voice, *attacker model*; he queried *threat model definition* and rejected it ("means different things to different people") — consistent with (a), which stays his to rule thesis-wide. | (a) apply thesis-wide, retitle §3.3.3 and §4.1.1, recast the ch2 opener ("The threat model that existed originally", l.529); (b) keep the 2026-08-20 boundary and treat §3.2.1 as our-voice (done); (c) *attack model* (Cho's §V-D term) — rejected, third variant | tex 2026-09-04: *threat model* 17 prose occurrences outside §3.2.1 (l.529 ch2; l.1474 strand opener, Cho's own list; l.1677, 1791, 1813, 1826, 1830, 1859, 1864, 1877, 1905–1909, 1959 in §3.3; l.2041, 2095 in ch4), *attacker model* 8 |

## Ruling workflow

The PROPOSED table is designed for **one ruling pass** (ask once, whole table —
the 2026-08-19 handoff's step 3). On Marc's ruling: flip the row to RATIFIED
with date, move rejected recommendations into the deprecated column, bump
`updated`. Conflicts between a proposal and a ratified naming ruling are
surfaced to Marc, never resolved silently (guardrails).
