---
status: durable
created: 2026-07-21
updated: 2026-08-17 (share rule generalised)
topic: "L3 synthetic overlay — the declared pre-intrusion structural sublayer: bidirectional connective tissue (recon→resource-development→initial-access forward chain + initial-access→reconnaissance backward regression bridge) for the profiles whose observed corpus leaves the pre-intrusion band detached"
lineage: extracted + reframed from controller.md (formerly tactic_action_map.md) §6 (the former 'M6 prefix join')
---

# The synthetic overlay — declared pre-intrusion structure, composed apart from the corpus

> **Retired class labels.** This record is investigation history and is left as
> written: it reports the pre-2026-08-06 labels `pure_steal` / `pure_impediment` /
> `double_extortion` / `infrastructure_setup`, which the objective-tactic rename
> replaced with `objective_exfiltration` / `objective_impact` /
> `objective_exfiltration_impact` / `objective_none_c2`. Rewriting them would
> re-attribute evidence to labels that did not exist when it was taken. Crosswalk:
> [`gasp_schema.md`](../gasp/gasp_schema.md) §(c).

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

## 3. Guard and share rule

*(Rewritten 2026-08-17. Until then the forward edges were added only out of
island places and `curate_synthetic_overlay` refused any other shape; the
backward bridge was the single merged edge. When SearchAwesome's malvertising
step gave `objective_none_c2` an observed `resource-development →
{command-and-control, execution}` — Marc's 2026-08-17 membership ruling — the
forward edge `resource-development → initial-access` would have merged into an
observed distribution. Marc's ruling: **improve the mechanism, do not exempt one
profile.** The rule below is the result: one share rule for every synthetic
edge, read off the observed net.)*

- **Guard.** The overlay acts only where the observed net leaves reconnaissance
  unable to reach initial-access (and reconnaissance, resource-development and
  initial-access all exist as places). It then adds the same three edges in
  every such profile: `reconnaissance → resource-development`,
  `resource-development → initial-access`, `initial-access → reconnaissance`.
- **Share rule (`declared_share`).** Each synthetic edge's declared share is
  decided by whether its *source* has observed out-transitions:
  - **island source** (no observed out-edges) → the synthetic edge is the
    place's whole out-mass (`ISLAND_SHARE = 1.0`); it perturbs no observed
    distribution;
  - **source with observed out-edges** → the synthetic edge carries
    `MERGE_SHARE = 0.1` of that place's composed out-mass and the observed edges
    are scaled to `1 − Σshare` in their flow proportions.
  The rescaling exists only in the composed runtime net; the observed
  `*_structural.json` artefacts stay byte-identical. *This is the one mechanism
  by which the synthetic overlay perturbs a D3 flow-proportion distribution —
  surfaced here for review, not hidden — and it now applies wherever the observed
  net puts a synthetic edge's source, not to one named edge.*
- **What the rule gives today.** In `objective_exfiltration_impact` recon and
  resource-development are islands: forward edges 1.0, backward bridge 0.1
  (unchanged from 2026-07-21). In `objective_none_c2` recon is an island (1.0),
  resource-development is not (`resource-development → initial-access` at 0.1;
  the observed `→ command-and-control / execution` keep 0.9), backward bridge 0.1.
  The exfiltration and impact profiles bridge recon → initial-access in the
  observed corpus and get no overlay.

## 4. Weights (declared routing shares, no flow backing)

A synthetic edge has no backing flow, so the D3 W-A flow-proportion regime does not
apply; it carries a **declared routing share** instead
([`weights.py`](../../../../src/mtdsim/l3_simulation/petri/weights.py) is
unmodified — it weights observed edges only, so the no-synthesis invariant on
`transitions` is untouched):

- Out of an island source: share **1.0** (the place's whole out-mass).
- Out of a source with observed out-edges: share **0.1** of the composed
  out-mass (`MERGE_SHARE`; the historical `BACKWARD_SHARE` and `FORWARD_SHARE`
  names are aliases of `MERGE_SHARE` and `ISLAND_SHARE`).

The composed per-place routing distribution merges observed flow-proportions and
declared shares per the share rule (§3); the runtime consumer
([`movement/net.py`](../../../../src/mtdsim/l3_simulation/movement/net.py)
`_compose_out`) implements the merge generically. Every synthetic spec carries
`synthetic: true` and the overlay provenance string, so it is never mistaken for
corpus structure ([`provenance.md`](../../provenance.md), synthetic-overlay row).

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
- **When to update:** if the guard or share rule or the declared shares change;
  if a substrate verb is later mapped to resource-development (it stops being a
  pure pass-through — the durations catalogue and the policy overlay gain a
  resource-development verdict); if a profile's observed net changes shape at
  the pre-intrusion band (the share rule re-reads it — record which shares
  moved, as §3 does for 2026-08-17). This is a code snapshot dated in the
  frontmatter.
