---
status: living
created: 2026-08-20
updated: 2026-08-20   # voice-pass ruling: all six PROPOSED rows RATIFIED and applied to §4.2
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
| The genre identification | **threat model** is the field's recognised term for the section's role; **movement attacker** is this work's name for the model ("we are putting names on things") — the identification is stated **once**, in the §4.2 preamble opener, and after it *movement attacker* carries; *threat model* recurs only when speaking the genre's language against the literature, never as a drifting synonym for our model | bare *threat model* as a name for our model anywhere past the opener — watch (census: 2 — the §4.1.1 heading and the preamble opener) | Marc, 2026-08-20 |
| The simulator | **MTDSim** at first use and wherever ambiguity threatens; **the simulator** as the running short form | *the original simulator*, *the inherited simulator* — the inheritance is established once in ch2; the qualifier re-argues it every time. *"the simulator we are inheriting"* (§4.2.4.2 penalty ¶) kept: the inheritance clause does argument work there (why the penalty is maintained) | Marc, 2026-08-20 (voice-pass ruling) |
| The six inherited operations (the callable unit) | **verb** — fixed by the load-bearing ruled phrase *tactic-to-verb mapping* | *attack operation*, *attack action*, *attack phase*. *Action* meaning a runtime execution (e.g. "the actions in MTDSim", "zero or one actions at a time") read as a distinct sense and left — flag conflations only | Marc, 2026-08-20 (voice-pass ruling) |
| The declared weight object | **failure matrix**; long form at first substantive use: *the tactic-to-tactic failure weight matrix* (placed at the §4.2.4.1 defining ¶ — the ruled spine sentence keeps the short form) | *failure weight set*, bare *weight set*; *outcome overlay* (repo term, stays out) | Marc, 2026-08-20 (voice-pass ruling) |
| Attacker time on a tactic | **dwell time** | *duration*, *draw time*, *tactic timing* when meaning dwell; *dwell* alone fine in compounds (dwell catalogue, dwell standard-of-evidence) | Marc, 2026-08-20 (voice-pass ruling) |
| The work's self-name | **this thesis** | *this paper* (dictation residue from paper-framing); *this work* / *this dissertation* unused | Marc, 2026-08-20 (voice-pass ruling) |
| The mechanism that makes dwell stochastic | **the exponential draw** (noun form; *drawn exponentially* as the verbal form) | *exponentiation mechanism* (also imprecise: exponentiation is raising to a power), *exponential element*, *exponential factor*; *the exponential defence* (L3 ceiling ¶) is a different object (the justification, not the mechanism) — never merged | Marc, 2026-08-20 (voice-pass ruling) |

### Proposed — awaiting Marc's ruling pass

| Concept | Recommendation | Alternatives considered | Census |
|---|---|---|---|
| *(none open — the 2026-08-20 voice-pass ruling ratified the whole table; all six applied to §4.2 the same day)* | | | |

## Ruling workflow

The PROPOSED table is designed for **one ruling pass** (ask once, whole table —
the 2026-08-19 handoff's step 3). On Marc's ruling: flip the row to RATIFIED
with date, move rejected recommendations into the deprecated column, bump
`updated`. Conflicts between a proposal and a ratified naming ruling are
surfaced to Marc, never resolved silently (guardrails).
