---
status: durable
created: 2026-07-21
updated: 2026-07-21
topic: "L3 synthetic overlay — the declared pre-intrusion structural sublayer: bidirectional connective tissue (recon→resource-development→initial-access forward chain + initial-access→reconnaissance backward regression bridge) for the profiles whose observed corpus leaves the pre-intrusion band detached"
lineage: extracted + reframed from tactic_action_map.md §6 (the former 'M6 prefix join')
---

# The synthetic overlay — declared pre-intrusion structure, composed apart from the corpus

**Status:** durable. The implementation record for the **synthetic overlay** — a
declared structural sublayer, in its own right, that composes non-corpus edges
onto the observed nets at construction. It executes supervisor decision **M6**
(supervisor_decision_register.md §M6: "join the detached pre-intrusion tactics
manually at the front") but is **not** branded "the M6 join": it is a maintained
sublayer with its own artefact, guard, and merge rules. The success/failure
*policy* overlay is a separate layer
([`success_failure_overlay_design.md`](success_failure_overlay_design.md)); this
one is *structure* (which edges exist), that one is *policy* (which edge fires on
which verdict).

Code: [`synthetic_overlay.py`](../../../../src/mtdsim/l3_simulation/petri/synthetic_overlay.py);
artefact [`synthetic_overlay.json`](../../../../data/ogasp/petri/synthetic_overlay.json);
gate [`tests/l3_simulation/test_petri.py`](../../../../tests/l3_simulation/test_petri.py) §7.

## 1. The gap

The corpus starts at the point of detection, so it is blind to pre-intrusion
activity. On the observed-only base this shows up directly in the single-token
reachability: in some profiles `reconnaissance` and `resource-development` are
**detached islands**, and a recon-seeded token can never reach `initial-access`.

| Profile | recon → initial-access (observed) | resource-development (observed) |
|---|---|---|
| `aggregate` | **yes** — one real corpus edge | in/out edges present |
| `pure_steal` | **yes** — one real corpus edge | out to initial-access |
| `pure_impediment` | **yes** — bridged | out to C2/execution; none to initial-access |
| `double_extortion` | **no — island** | fully detached (no in/out) |
| `infrastructure_setup` | **no — island** (recon has in-edges, no out) | fully detached |

The overlay acts on exactly the two island profiles (`double_extortion`,
`infrastructure_setup`); the guard rule leaves the three already-bridged profiles
untouched and catches any future class that regresses.

## 2. The shape — bidirectional pre-intrusion connective tissue

For each island profile the overlay adds a **kill-chain-correct pre-intrusion
chain plus a backward regression bridge**, so a *successful* attacker can traverse
into the network and a *failed* one can fall back into the pre-intrusion band:

- **Forward chain.** `reconnaissance → resource-development` and
  `resource-development → initial-access`. Kill-chain-correct (CKC:
  Reconnaissance → Weaponisation → Delivery). resource-development becomes a
  genuine forward pass-through — off-clock today (×0 dwell, no mapped substrate
  action) but a first-class place, because **the action set is extensible**: a
  verb may later map to resource-development, and the structure is ready for it.
- **Backward regression bridge.** `initial-access → reconnaissance`. It lets a
  failed attacker route back into the pre-intrusion band and, from reconnaissance,
  re-enter the forward chain — the structural substrate the *policy* overlay's
  failure treatment amplifies. (In the island profiles the observed body carries
  no edge back into the pre-intrusion tactics, so without this bridge no amount of
  runtime policy could route a regression there — the edge must exist first.)

This **reverses the earlier recon-only resolution** (2026-07-21, first pass), which
left resource-development a documented island on the ground that a lone
`resource-development → initial-access` edge would be dead structure. The
bidirectional chain resolves that: resource-development now has an in-edge
(`reconnaissance → resource-development`) and an out-edge, so it is reachable and
alive, and the backward bridge makes the whole pre-intrusion band a participant in
the failure-regression structure (Marc's direction).

## 3. Guard and merge rules

- **Guard.** The overlay acts only where the observed net leaves reconnaissance
  unable to reach initial-access. The two **forward** chain edges are added only
  out of **island places** (reconnaissance and resource-development have no
  observed out-edges in these profiles), so each is the sole out-transition of its
  source and touches no observed distribution. `curate_synthetic_overlay` raises
  if reconnaissance *or* resource-development has observed out-edges yet recon
  cannot reach initial-access — that shape needs a new declared decision, not a
  silently invented weight.
- **Merge (the declared exception).** The one **backward** edge leaves
  `initial-access`, which *does* carry observed out-edges. It therefore carries a
  declared **share** of initial-access's composed out-mass (`BACKWARD_SHARE = 0.1`);
  the observed edges keep their relative flow proportions across the remaining
  `1 − share`. This is a declared, documented departure from the original overlay's
  "never renormalise an observed distribution" rule — **confined to the single
  backward bridge**, flagged synthetic, and applied only in the composed runtime
  net (the observed `*_structural.json` artefacts stay byte-identical, exactly as
  the forward edges do). *This is the one place the synthetic overlay perturbs a
  D3 flow-proportion distribution — surfaced here for review, not hidden.*

## 4. Weights (declared routing shares, no flow backing)

A synthetic edge has no backing flow, so the D3 W-A flow-proportion regime does not
apply; it carries a **declared routing share** instead
([`weights.py`](../../../../src/mtdsim/l3_simulation/petri/weights.py) is
unmodified — it weights observed edges only, so the no-synthesis invariant on
`transitions` is untouched):

- Forward chain edges: share **1.0** (sole out-transition of their island source).
- Backward bridge: share **0.1** of initial-access's composed out-mass.

The composed per-place routing distribution merges observed flow-proportions and
declared shares per the merge rule (§3); the runtime consumer (the profiled-attacker
driver) implements the merge. Every synthetic spec carries `synthetic: true` and the
overlay provenance string, so it is never mistaken for corpus structure
([`provenance.md`](../../provenance.md), synthetic-overlay row).

## 5. Separation, invariant, composition

- The overlay lives in `StructuralNet.synthetic_transitions`, **never** in
  `transitions`; the observed `*_structural.json` artefacts stay observed-only and
  `test_no_synthesis_invariant` runs on the observed-only build unchanged.
- `build_all_profiles` / `build_all` compose the overlay **by default**
  (`with_synthetic_overlay=True`); observed-only is the explicit opt-out used by
  the artefact emitter and the invariant tests.
  `synthetic_overlay.apply_synthetic_overlay` is the single-net entry point the
  live runner uses. Reachability (`analysis._place_adjacency`) unions the overlay;
  the prefix-gap probe reports **"BRIDGED synthetically"** on composed island nets
  (the pre-intrusion chain). **Overlay off + an `initial-access` seed remains the
  comparison arm** — the entry-point experiment is a toggle, not a second code path.
- `test_petri.py` §7 pins the overlay: exact edges + declared shares
  (`EXPECTED_SYNTHETIC`), the synthetic-spec contract (forward edges sole-out of an
  island place; backward edge out of a populated initial-access), composed
  reachability for all five profiles, the forward chain firing recon →
  resource-development → initial-access, the backward bridge's presence, and
  artefact freshness.

## 6. Where this connects, and when to update

- **Executes:** supervisor decision **M6**
  ([`supervisor_decision_register.md`](supervisor_decision_register.md) §M6).
- **Consumed by:** the profiled-attacker build (the composed nets are what the live
  runner steps); the *policy* overlay
  ([`success_failure_overlay_design.md`](success_failure_overlay_design.md)) treats
  the synthetic edges as ordinary structure to condition (the backward bridge is the
  regression edge its failure treatment amplifies in the island profiles).
- **Provenance:** [`provenance.md`](../../provenance.md) synthetic-overlay row.
- **When to update:** if the guard/merge rules or declared shares change; if a
  substrate verb is later mapped to resource-development (it stops being a pure
  pass-through — the durations catalogue and the policy overlay gain a
  resource-development verdict); if a new class regresses to an island (the guard
  raises — a new declared decision). This is a code snapshot dated in the
  frontmatter.
