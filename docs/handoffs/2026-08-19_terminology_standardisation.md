---
status: open
created: 2026-08-19
---

# Terminology standardisation — one term per concept, ruled registry, guardrails wired into the drafting skills

**Goal (one line).** Marc's ask (2026-08-19, L4 pass-5 session): the draft
"uses multiple terms for the same idea"; research writing uses the same term
over and over. Build a term census from the dissertation, propose one
canonical term per concept cluster, get Marc's ruling, then bake the registry
into the drafting pipeline so the problem cannot propagate past the §4.2.4
pilot.

## State of play

- §4.2 is the pilot; the conflation is worst in §4.2.4. Known clusters, from
  Marc's own listing plus this session's reading of the draft:
  1. **The six inherited operations**: "verbs" / "attack phases" / "attack
     actions" / "attack operations" / "the six phases". One noun for the
     callable operation, one for the layer.
  2. **The inherited attacker**: "baseline attacker" (the RATIFIED name, V5)
     / "inherited attacker model" / "original attacker model" / "existing
     attack model" / "the finite state machine".
  3. **The simulator**: "MTDSim" / "the simulator" / "the original
     simulator" ("the substrate" is a repo term — likely not for the
     chapter).
  4. **The layer vocabulary**: "movement layer / controller layer / action
     layer" (ratified trichotomy) vs ad-hoc "porting layer", "the join",
     "the interface" --- and the §4.2.4 finding that the three declared
     inputs are never tied to the controller layer by name.
  5. **The weight object**: "failure matrix" / "failure weight set" /
     "tactic-to-tactic weight set" ("the outcome overlay" is the repo term).
  6. **The profile object**: "attack profiles" (ratified) / "the Petri
     nets" / "attack-profile Petri nets" / "the nets".
  7. **Timing**: "dwell time" / "duration" / "draw time" / "tactic timing".
  8. **The proposed attacker**: "movement attacker" (ratified) / "attacker
     agent" / "attacker model" / "the token" (the token is a distinct
     object --- flag conflations only).
- Ratified rulings that constrain the registry: movement attacker / baseline
  attacker naming pair (V5); "attack profiles"; "generalised stochastic
  Petri net"; sentence-case, no-acronym headings; Australian English.

## Progress (2026-08-20 — pass-6 session)

Steps 1–2 executed; the enforcement home moved by Marc's 2026-08-20 ask:

- **Registry created:** [`../workflows/terminology.md`](../workflows/terminology.md)
  — the eight clusters seeded with census counts from `dissertation.tex`
  (2026-08-20). Six rows RATIFIED from existing rulings (movement/baseline
  attacker, the layer trichotomy, attack profiles, GSPN, pre-intrusion
  overlay); four rows PROPOSED with one recommendation each (simulator
  naming, the operation noun — recommendation *verb*, anchored on the ruled
  "tactic-to-verb mapping" phrase — the weight object post-v4, dwell time).
- **Primary enforcement is now pass 6**, the `voice-pass` skill (sweep 3):
  ratified rows enforced as batch proposals per section, new clusters
  harvested into the registry as PROPOSED rows. Back-apply to §4.2 (step 5)
  happens as pass 6's first run on the section.
- **Still open:** Marc's single ruling pass over the PROPOSED table (step 3);
  then the `repair-dictation` `[term]` sweep and the `scrutinise-draft`
  consistency row (step 4 — deliberately deferred until the ruling, per this
  handoff's own plan).

## Recommended approach

1. **Census.** A small script (or disciplined grep) over
   `docs/thesis/dissertation.tex`: per cluster, count each variant's
   occurrences with line numbers. Numbers first --- the registry should show
   Marc what the draft actually does.
2. **Registry proposal.** One canonical term + permitted variants (e.g. the
   full name on first use, the short form after) per cluster, each with a
   one-line reason, aligned with the ratified rulings. Present as ONE table
   for a single ruling pass (ask once, whole table).
3. **Marc rules.** The ruled table lands as
   `docs/workflows/terminology.md` (or a section of the writing guide ---
   placement per docs_map criterion).
4. **Wire the guardrails** (only after the ruling):
   - `repair-dictation` (pass 3a) gains a **term sweep**: non-canonical
     variants flagged as `[term]` markers against the registry --- flagged,
     never auto-substituted (the no-word-choice rule stands; Marc resolves
     at 3b).
   - `scrutinise-draft` question set gains a term-consistency check row.
   - The registry is added to the drafting handoff's reading list and the
     writing guide.
5. **Back-apply to §4.2** as a Marc-run Ctrl+F pass (the registry makes it
   mechanical).

## Validation gate

The ruled registry exists in `docs/workflows/`; both skills carry the sweep;
§4.2.4's clusters each resolve to one canonical term in a Marc-applied pass;
a cold session dictation-repair flags a non-canonical term without being
told.

## Hard constraints

- No auto-substitution of terms in Marc's prose --- flag only (voice rules).
- The registry must not contradict ratified naming rulings; conflicts are
  surfaced to Marc, not resolved silently.
- Repo/docs terminology (substrate, overlay, OGASP) is NOT renamed --- this
  registry governs the dissertation's surface only; the architecture.md
  §(b)-style divergence note pattern applies if the two vocabularies drift.

## Reading list

1. `docs/thesis/dissertation.tex` (§4.2 --- the pilot)
2. `docs/workflows/voice.md` + `docs/workflows/_writing_guide` (heading/naming rulings)
3. `docs/handoffs/2026-08-16_drafting_movement_attacker_section.md` (term rulings scattered through the pass records)
4. `docs/implementation/architecture.md` §(f) (the ratified layer vocabulary)
5. `.claude/skills/repair-dictation/SKILL.md`, `.claude/skills/scrutinise-draft/SKILL.md` (wiring targets)
