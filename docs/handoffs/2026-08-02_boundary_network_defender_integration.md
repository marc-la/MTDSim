---
status: open — Part A done 2026-08-02, confidence gate passed; blocked on Marc's dispositions (D-23, with D-24/D-25 record-grade)
created: 2026-08-02
updated: 2026-08-02
---

# Boundary review 2 of 3 — NETWORK / DEFENDER: does each MTD mechanism move the whole attack surface in its purview, and are the purviews fair to compare?

## 0. Where this stands (2026-08-02 Part A session, branch `chore/boundary-network-defender-review`)

Part A is complete. The deliverable is
[`../implementation/mtd_write_surfaces.md`](../implementation/mtd_write_surfaces.md):
all eight mechanisms' write sets enumerated with locators and **live-verified**
(one firing per mechanism on a seeded default-geometry `TimeNetwork`, full
state diff), the §2 shared questions answered with evidence, the §c
cross-examination recorded, and the purview/fairness table built with brief 1's
liveness column cross-filled. Disposition requests are appended to the audit as
**D-23..D-25** (numbering follows boundary review 3's concurrent D-20..D-22
allocations — brief 3 ran first; its Part A commit `246adf8` sits on this
session's branch because the two sessions shared the working tree).

**How the seeded questions resolved, in brief:**

1. *Exposed-endpoint exemption* — *not* universal as seeded: UserShuffle has no
   exemption (conforming to IS-MTD-03), and CTS moves endpoint adjacency. For
   the five mechanisms that carry it, it is endpoint-total and uniform →
   **D-23** (keep-and-document recommended).
2. *Target-node exemption* — structural, not a gap: the target node carries no
   service and no port at generation (verified live), so there is nothing to
   diversify and un-skipping would `KeyError`. The compromise-critical
   services (those adjacent to the target) **are** redrawn. No disposition
   needed.
3. *Ports under a service redraw* — immobile, and that CONFORMS: no IS row
   couples ports to service replacement; PortShuffle owns ports and is latent.
   Consequence recorded: the attacker's discovered ports remain valid
   addressing across every diversity firing.
4. *Stale derived state* — the attacker-visible cache (`reachable`) is
   refreshed by exactly the mechanisms that invalidate it (CTS/HTS); the rest
   are scorer feeds, and two are **degenerate in the time-domain arm**
   (`target_node=None` makes `add_shortest_path` record a 50-entry paths-dict;
   APE never runs) with no recorded consumer → **D-24** (record-only; a
   precondition of the Tay-benchmark phase). Attacker caches
   (`curr_ports`/`curr_vulns`) are brief 3's channel; this brief established
   the object-identity half (stale handles point at orphans).
5. *Exploited-flag continuity* — a redraw **fully revokes** service-level
   standing (fresh instance, `exploited`/`exploit_attempt` reset, ATK-04
   discount lost; verified live); `host.compromised` persists per D-02;
   `compromised_services` is reader-less bookkeeping.
6. *The latent four / family scope* — in the reported family, ports, users,
   host-internal topology and the entry set have **no mover**; the family's
   two live write surfaces are adjacency (CTS) and the service/vulnerability
   surface (SD = OSD per D-18), plus two dead ones (ip, os label). The
   fairness statement is `mtd_write_surfaces.md` §c.

One unseeded find beyond D-24: `gen_graph` re-selects the target node on
`network_type == 0`, so CTS on a targeted network silently re-sites the
objective — latent in every recorded arm → **D-25** (record-only).

**Confidence evaluation (the §5 gate) — PASSED, with residual doubts named.**
Against the checklist: (i) write sets enumerated and live-verified for all
eight mechanisms, locator-complete — yes; (ii) every exemption either
documented intent (IS-MTD-01), structural (target node), ruled (D-02, D-18
consumed), or D-numbered (D-23) — yes; (iii) purview table complete with
per-cell locators and brief-1 liveness — yes; (iv) the adversarial pass had
teeth: it falsified one of the brief's own premises (the exemption is not
universal) and surfaced three unseeded behaviours (D-24, D-25, the scorer
ip-feed asymmetry). Residual doubts, each named with why it is tolerable:
the adversarial pass was same-session rather than fresh-session (mitigated by
the full-surface snapshot diff — every host and node attribute — and by the
unseeded finds); cosmetic state (`colour_map`, `pos`, `tags`) was not diffed
(no attacker read path; plotting only); §b5's revocation was verified on
ServiceDiversity's code path and inferred for OSD/OSDA (identical call,
same lines); the CTS node-floor caveat applies only to non-default
geometries no experiment uses. None of these can plausibly move a comparative
ranking of the reported family, so the answer to the gate question is **yes,
≥ 95 %** — for the write side as reviewed, with the D-23 ruling outstanding as
a *decision*, not an unknown.

**To close this handoff:** Marc rules on D-23 (and notes D-24/D-25); if D-23(b)
or any D-18(a)-style repair is taken, Part B runs under §4 (D-05 procedure,
regression tests per `mtd_write_surfaces.md` §f); then delete this file in the
commit that ships the last piece.

**Programme framing.** Second of the three boundary briefs Marc directed on
2026-08-02; the shared rationale and the ownership rule live at the head of
[`2026-08-02_boundary_network_attacker_integration.md`](2026-08-02_boundary_network_attacker_integration.md)
(brief 1). This brief owns the **write side**: what each mechanism mutates when
it fires, whether that is the *whole* surface its defence idea claims, and
whether the mechanisms' purviews are symmetric enough that comparing their
measured effects compares defence ideas rather than implementation reach. A
surface moved but never read is brief 1's finding; a defender-to-attacker
signal that bypasses network state (interrupts, penalties) is brief 3's.

## 1. Goal

Establish, at 95 % confidence (§6), that for every mechanism in the reported
defence family: (a) its mutation reaches every component its documented defence
idea covers — no silent exemptions, no stale derived state, no dangling
partners; (b) exemptions and scope limits are either documented intent or
carry a Marc disposition; and (c) the family's purviews are stated side by
side so the comparative evaluation can say what was actually compared. Marc's
own summary of this boundary is the brief's question verbatim: *are the MTD
mechanisms moving the right/whole attack surface?*

## 2. State of play — write surfaces, seeded with what is already verified

The reported family is the default set (`mtd_scheme.py:22-31`): Complete
Topology Shuffle, IP Shuffle, OS Diversity, Service Diversity — Zhang's four.
PortShuffle, UserShuffle, HostTopologyShuffle, OSDiversityAssignment exist but
are commented out of the default set (latent; every recorded experiment ran
without them).

| Mechanism | Verified write surface | Already-known gaps/questions |
|---|---|---|
| IPShuffle | `host.ip` per non-endpoint host (`ipshuffle.py:14-25`) | Writes a property with **zero readers repo-wide** — the mechanism's entire measured effect arrives via brief 3's channels. Is "IP" a real surface in this simulator at all, or a label on an interrupt generator? |
| CompleteTopologyShuffle | full `gen_graph()` regeneration, host instances re-attached (`completetopologyshuffle.py:15-27`) | Moves adjacency but not identity: node ids persist and `compromised_hosts` (a list of node ids) survives — compromise is never revoked (D-02, ruled: Zhang's persistence is operative). So what CTS moves is paths-to-uncompromised, not the attacker's holdings. Is that the documented purview? |
| OSDiversity | `os_type`/`os_version` relabel + **all** services redrawn (guard inert, D-18) (`osdiversity.py:19-44`) | Version index preserved on relabel (delta on record); the OS write is read by nothing live (D-19 / brief 1). Post-D-18-ruling this row's true surface is either "OS label + incompatible services" or "OS label + all services". |
| ServiceDiversity | every non-target service on non-exposed hosts redrawn at random version (post-D-05) (`servicediversity.py:12-30`) | See shared questions below. |

**Shared purview questions, already visible from this session's reads:**

1. **The exposed-endpoint exemption** is applied by *every* mechanism, but it
   is documented only for IPShuffle ("all internal hosts"); for the
   application-layer mechanisms it is a beyond-paper narrowing (audit §l
   item 5, flagged "worth Marc's eye" since the original audit). The
   attacker's entry surface is therefore **permanently unmoved** for the whole
   family — defensible, but it must be a decision, not a drift.
2. **The target-node exemption**: OS Diversity and Service Diversity both skip
   `host_instance.target_node`, so the compromise-critical service on every
   host is never diversified. Documented nowhere that the audit records.
3. **Ports do not move when services do**: a redrawn service keeps its node's
   `"port"` attribute (`host.py:123-124` assigns both only at generation;
   neither diversity mechanism touches `"port"`). Port movement is
   PortShuffle's purview — and PortShuffle is latent. Is a service redraw that
   preserves the port the intended granularity?
4. **Stale derived state**: mechanisms differ in which derived structures they
   refresh (`add_attack_path_exposure` is gated to network-type 0 and never
   runs in the time-domain arm; `add_shortest_path` is called by some
   mechanisms). Does every mechanism leave the network's derived caches (and
   the attacker's cached `curr_ports`/`curr_vulns`) in a state consistent
   with its mutation, or do some mechanisms get "free" staleness effects that
   others don't?
5. **Vulnerability/exploited-flag continuity**: vulnerabilities are per-host
   copies with preserved ids; when a service is redrawn, what happens to the
   old instance's `exploited` flags and to RoA bookkeeping — does a redraw
   actually revoke the attacker's standing on that service, or can prior
   exploitation survive the shuffle through shared-id copies?
6. **The latent four**: every read-surface with no live mover (users →
   UserShuffle, ports → PortShuffle, intra-layer position →
   HostTopologyShuffle) narrows what "the defence family" means. The reported
   family's cardinality question (decision C) is the same question one level
   up — the review should state, per component, whether the family *as
   reported* can move it at all.

**Fairness statement this brief must end with.** A side-by-side purview table:
per mechanism, the components moved, the exemptions, the derived-state
refreshes, and the (brief-1) liveness of each moved component — so that any
future ranking claim can cite what each contestant was actually allowed to do.

## 3. Recommended approach — Part A (review / cross-examination; no code changes)

1. **Enumerate each mechanism's write set exactly** — every attribute mutated,
   every structure refreshed, every exemption — by reading `mtd_operation()`
   of all eight mechanisms (latent ones included, briefly: they define what
   the family *could* be) with locators.
2. **Cross-examine against the documented defence idea, by IS-ID**
   (IS-MTD-01..09), under the §c procedure — audit against the intent spec's
   rows, never paper memory. For each mechanism: what does the paper say it
   moves; what does it move; classify every delta. The internal consistency
   Marc believes the mechanisms inherit from prior works is the null
   hypothesis to *test*, not assume.
3. **Live-verify the write sets** (tracer or direct inspection runs): fire
   each mechanism once on a seeded network and diff the network state —
   the definitive write-set enumeration, and the template for the regression
   tests Part B will want. Verify the shared questions (§2.1–5) empirically,
   not by read alone.
4. **Build the purview table** (§2, fairness statement) with per-cell
   locators, cross-filled with brief 1's liveness column.
5. **Findings table with costed options** per undispositioned gap
   (repair / keep-and-document / re-scope), golden impact per option,
   appended to the audit's disposition list (numbering after brief 1's
   allocations). Consume D-18's ruling for the OS Diversity row rather than
   re-opening it.

## 4. Part B (implementation; only after Marc's dispositions)

Identical discipline to brief 1 §4: dispositioned changes only; D-05 procedure
(deliberate re-baseline, `baseline/CHANGELOG.md`, SIM-05, full suite green);
one regression test per repaired write-surface (template: fire the mechanism,
assert the component moved / the exemption holds as dispositioned); no
recorded experiment re-run; comparability boundary recorded.

## 5. The A/B cycle and the confidence gate

Same standing instruction as brief 1 §5, with this boundary's question: **"Are
we ≥ 95 % confident that no mechanism in the reported family silently fails to
move a component its defence idea covers, and that no purview asymmetry
remains unstated that could change a comparative ranking?"** The evaluation is
a written judgement against the checklist (write sets enumerated and
live-verified; every exemption dispositioned or D-numbered; purview table
complete; adversarial pass found nothing), with residual doubts named; any
doubt that could plausibly move a ranking fails the gate and scopes the next
A/B iteration, recorded in this handoff.

## 6. Validation gate

1. The per-mechanism write-set enumeration and the purview table exist as an
   implementation record, live-verified, locator-complete.
2. Every §2 shared question answered with evidence and, where divergent,
   classified and dispositioned by Marc.
3. Part B changes (if any) landed under the D-05 procedure with per-mechanism
   regression tests.
4. A passed confidence evaluation written into this handoff's final update.

## 7. Hard constraints

- §c classification before any "bug" talk; only Marc's disposition makes a
  gap fixable. The exposed-endpoint and target-node exemptions may well be
  deliberate — the review's job is to make them *decided*, not to remove them.
- No recorded experiment re-run; goldens via D-05 procedure only; SIM-05.
- The latent mechanisms are reviewed for what they imply about the family's
  scope, but changing their default-set membership is an experiment-design
  decision for Marc, not a Part B change.
- D-18 (inert compatibility test) is owned by the indistinguishability brief —
  its ruling is an *input* here.
- Australian English; branch per session; commit locally; **never push**.

## 8. Reading list

- `mtdnetwork/mtd/*.py` — all eight mechanisms, side by side.
- `mtdnetwork/component/host.py` (node attr assignment, 108-130;
  vulnerability copies), `mtdnetwork/component/services.py`
  (generator, copies, ids), `mtdnetwork/component/network.py`
  (derived structures, scorer feeds).
- `docs/implementation/intent_conformance_audit.md` §c (IS-MTD rows), §l
  items 5/6, and the disposition list.
- `docs/implementation/mtdsim_intent_spec.md` IS-MTD-01..09 — the yardstick.
- [`2026-08-02_os_service_diversity_indistinguishability.md`](2026-08-02_os_service_diversity_indistinguishability.md)
  — D-18/D-19 and decision C (the family-cardinality question this brief
  generalises).

## 9. Out of scope (explicitly)

- The read side (brief 1) and the direct channels (brief 3).
- Designing new MTD mechanisms (defender pool is frozen; existing mechanisms
  only).
- Re-running or re-analysing recorded experiments; decision C's reporting
  edit stays with its own brief.
- Dissertation prose.
