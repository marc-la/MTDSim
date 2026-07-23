---
status: resolved — grounding depth settled shallow by the 2026-07-14 meeting (M4)
created: 2026-07-13
updated: 2026-07-15
topic: "L3b reframe — grounding MTDSim in the CTI ontology (the latent-layer program)"
---

# Grounding MTDSim in the CTI ontology — the reframe, the latent layers, and the grounding-depth spectrum

> **RESOLVED (2026-07-14 meeting, M4) — the depth question this program was
> built to answer empirically was answered by the supervisor instead, at the
> shallow end.** The tactics/techniques layer and the substrate's vulnerability
> ecosystem stay **separate concepts**: the net supplies movement/behaviour, the
> substrate's existing vulnerability-based machinery supplies binary outcomes
> ("the vulnerability details are just an enabler; fetch the success outcome
> from the bottom"). No CVE/CWE/CVSS grounding of the pool, no synthesis mapping
> layer — the join is a manual, justified **tactic→action influence map** (M5)
> plus an outcome feedback loop into conditional net weights (M1/M2). The §4
> program steps are therefore retired: the crosswalk-join investigation is
> deleted unexecuted (retired by evidence), the synthesis-layer proposal is not
> happening, and the binding re-run is subsumed by the meeting's decisions.
> Register: [`supervisor_decision_register.md`](supervisor_decision_register.md)
> §M1–M8. This record is retained as the map of the design space the decision
> was made *in* — the depth spectrum (§3) is now dissertation material for the
> "why not deeper" limitation/future-work paragraph, not a live question.
>
> **FURTHER REFRAME (2026-07-22).** The tactic→action *binding* this record is
> built around is itself retired: the join is now the **controller**, an explicit
> **swappable input parameter** (a CKC-mediated tactic→verb position map), not a
> single correct binding to be discovered or grounded —
> [`controller.md`](controller.md). The `binding_design_space.md` /
> `binding_signoff_summary.md` records this document links to were **removed**
> that day; those links are historical. What survives here is only the §3
> grounding-depth spectrum, as the "why not deeper" future-work argument.

**Status (historical):** direction-setting record (broad brushstrokes; the north star the L3b
sub-investigations point at). Not a spec, not a decision — a framing Marc is
choosing to maintain (2026-07-13) and will flesh out by investigating the latent
layers and proposing a grounding approach in a later session. Currently
**Marc-driven**; supervisor sign-off is downstream of a concrete grounding
proposal, not of this framing.

---

## 1. The reframe — from *bind* to *ground*

The original L3b question was **binding**: *given two fixed ontologies — the CTI
technique graph and the substrate's synthetic vulnerability model — where is the
connector?* That question has a structural trap. If the substrate is a fixed
given, the best a binding can do is map the attacker's tactics onto the
substrate's **existing** action set — and because those six verbs are data-coupled
and taxonomy-free, the result is close to the inherited phased attacker with new
labels (the **anti-goal**; the re-skin). The binding investigation
(`binding_design_space.md`, removed 2026-07-22 — see [`controller.md`](controller.md))
confirmed this: the only
in-scope lever that is *materially* different from a re-skin is technique-driven
behaviour the substrate's action set cannot currently express.

The reframe (Marc, 2026-07-13) is **grounding**: *how far can MTDSim be grounded
in the CTI ontology, so the join is native rather than bolted on?* This is
materially different because it makes the **substrate side malleable**. Two things
unlocked it:

- **The attacker side was always malleable** (D5) — new attacker code, records,
  overlays are fair game.
- **The substrate's vulnerability model is now malleable too** — because
  comparability with the frozen synthetic pool is **secondary, not a gate** (R4;
  Zhang/Tay comparison was already invalid — [`../../metrics_semantics.md`](../../metrics_semantics.md) §d).
  Re-baselining on a reshaped substrate is an accepted, logged operation.

Once the substrate can be *reshaped to speak CTI*, the design question stops being
"where is the connector?" and becomes **"how deep does the grounding go?"** — a
spectrum, not a point. Technique-driven vulnerability selection — the non-re-skin
lever — lives at the deep end of that spectrum, and grounding is what makes it
reachable.

*Is "bind" the right word?* Only at the shallow end. At depth the substrate is
**co-designed** to carry the CTI ontology, so there are not two things to bind —
there is one ontology realised at two altitudes. "Grounding" names that; "binding"
names only the shallow special case.

## 2. The two endpoints and the latent layers between them

The design lives between two endpoints, with **latent layers** in between that a
grounding must pass through or deliberately bypass:

```
  CTI ONTOLOGY            ATT&CK tactics / techniques
        │
   (upstream, built)      L1 GAP → L2 GASP → L3a weighted nets → ogasp-timeline/v1
        │
  ── LATENT LAYERS ──     technique ↔ CAPEC ↔ CWE ↔ CVE ↔ CVSS   (the published crosswalks)
   (the gap to bridge)    …and/or a designed SYNTHESIS MAPPING LAYER (an intermediate
        │                  representation that mediates technique ↔ vulnerability)
        │
  MTDSim SUBSTRATE        host / service / synthetic Vulnerability (complexity, impact,
                           cvss, exploit_time, dependent_vuln_id)
```

The upstream half (CTI → timelines) is **built and stable**. The substrate half is
**inherited and — newly — reshapeable**. The middle is the open territory: the
crosswalk chain is one set of latent layers (real, but sparse); a **synthesis
mapping layer** is a *designed* latent layer that can stand in where the crosswalk
does not reach. **The extent of grounding achievable is exactly what these latent
layers can support** — which is why it is an empirical question (§4), not a
choice to make from the armchair.

## 3. The grounding-depth spectrum (broad brushstrokes)

From shallow (near re-skin) to deep (native CTI substrate). Each depth is a
candidate; "how far" = which depth the latent layers can actually sustain over
*this project's* technique vocabulary.

| Depth | What is grounded | Where it lives | The lever it unlocks | Re-skin risk |
|---|---|---|---|---|
| **0 — verb wrapping** | nothing (tactics relabel verbs) | attacker | tempo/order only | high (the anti-goal) |
| **1 — capability contract** | attacker *behaviour* (pre/effect, survivor-vs-vulnerable) | attacker | class-conditioned MTD survival | moderate |
| **2 — tag overlay** | vulnerability *labels* (CWE/technique tags on the unchanged pool) | attacker + pool metadata | technique-preferred vuln *instances* | thin unless tags correlate with pricing |
| **3 — native CVE pool** | the vulnerability *model itself* (real CVE/CWE/CVSS seeded in) | substrate (re-baselined) | technique-driven vuln **selection & pricing** | none — genuinely CTI-native |
| **synthesis layer** | a *designed* mediator (any depth) | new intermediate layer | decouples attacker vocabulary from pool realism; covers what the crosswalk misses | depends on design |

Depths compose: a **hybrid** grounds natively where the crosswalk reaches and
falls back to a synthesis layer (or capability contract) where it does not. The
recommended L3b design becomes *"ground to depth N, mediated by a synthesis layer
over the gap"* — with N set by evidence.

## 4. "How far" is an empirical question — the program

The depth achievable depends on what the latent layers actually contain, so the
program is **investigate the layers → propose a grounding → decide the depth →
build**:

1. **Latent-layer anatomy + coverage + seeding tractability** — the crosswalk-join
   investigation ([`../../../handoffs/2026-07-13_l3_crosswalk_join_investigation.md`](../../../handoffs/2026-07-13_l3_crosswalk_join_investigation.md)):
   what maps, how far it reaches over *our* technique set, how a CVSS vector seeds
   the substrate's pricing, and where a synthesis layer must cover the gap.
2. **Marc's synthesis-layer proposal** (a later session) — the designed
   intermediate representation(s) that bridge where the crosswalk is thin; the
   thing Marc "plans to investigate and propose in a future chat".
3. **Grounding-depth decision** — pick N on the §3 spectrum from the coverage
   evidence + the synthesis-layer design.
4. **Binding re-run** — the `binding_design_space.md` (removed 2026-07-22)
   candidates re-scored at the chosen depth (its C1/C2/C3 analysis stays valid;
   only the comparability weighting and CVE deferral were wrong and are corrected
   in place). This produces the recommendation that actually goes to the
   supervisor.
5. **Build + re-baseline** — the deferred replay attacker, on the reshaped
   substrate.

## 5. What is settled, what is open, who decides

- **Settled:** the reframe (bind → ground); comparability is secondary (R4);
  the substrate vuln pool is reshapeable; the latent layers are the gating
  unknown; technique-driven vuln behaviour is the lever worth reaching for.
- **Open (no decision made):** the grounding depth; whether the crosswalk or a
  synthesis layer (or both) carries the join; the coverage yield over our
  techniques; the seeding mechanics; whether the re-baseline cost is worth the
  yield.
- **Who decides now: Marc.** This is a Marc-driven reframe of the question
  itself. The investigations feed *his* grounding proposal; the supervisor sees a
  recommendation only once that proposal + the binding re-run exist. The earlier
  "pending supervisor confirmation" framing on the binding record is superseded by
  this.

## 6. Relationship to the existing artefacts

- **Supersedes the framing of** the MVP-binding investigation + its goal
  (handoffs since deleted per lifecycle) — their impartial enumeration *landed* as
  `binding_design_space.md` (itself removed 2026-07-22 in the controller reframe)
  and stayed valid as candidate analysis; their "recommend one MVP binding for sign-off" goal is
  **paused**, re-sequenced behind this program (depth first, recommendation
  after).
- **Consumes** the crosswalk-join investigation (§4.1) and Marc's synthesis-layer
  proposal (§4.2).
- **Feeds** the binding re-run (§4.4) and, through it, the tactic-operationalisation
  scaffold ([`../../../handoffs/2026-07-13_l3_tactic_operationalisation.md`](../../../handoffs/2026-07-13_l3_tactic_operationalisation.md))
  and the deferred replay-attacker build.
- **Will touch, when a depth is chosen (not yet):** the L3 attacker seam in
  [`../../architecture.md`](../../architecture.md) §(f) (Marc-driven) and the
  substrate vuln model in [`../../../../mtdnetwork/component/services.py`](../../../../mtdnetwork/component/services.py);
  the encoding ledger in [`../../../notes/ch3_design/structure_to_behaviour_binding.md`](../../../notes/ch3_design/structure_to_behaviour_binding.md)
  (the "vulnerability-instance binding" it calls the faithful ceiling is exactly
  the deep end of this spectrum, now reachable).

## 7. When this would need updating

- When the crosswalk-join investigation reports coverage — §3's reachable depth
  becomes evidenced rather than hypothetical.
- When Marc proposes the synthesis layer(s) — §2's "designed latent layer"
  becomes concrete and §3 gains its real middle rows.
- When a grounding depth is chosen — this record stops being direction-setting
  and becomes the rationale banner over the chosen design.
- If comparability is ever re-elevated to a hard constraint (it is not now) — the
  substrate-malleability premise in §1 collapses and the spectrum truncates at
  depth 2.
