---
status: durable
created: 2026-07-13
updated: 2026-07-13
topic: "L3b binding design space — impartial cross-examination + MVP recommendation"
---

# The Petri-net → MTDSim binding design space — enumeration, cross-examination, and an MVP recommendation that is not a re-skin of the phased attacker

**Status:** investigation record (codebase-shaped cross-examination; lives in
`implementation/`, not `notes/`). Produced under
[`../../../handoffs/2026-07-13_l3_mvp_binding_investigation.md`](../../../handoffs/2026-07-13_l3_mvp_binding_investigation.md).
The recommendation here is **pending supervisor confirmation** (Dr Jin Hong) and
is the input to the tactic-operationalisation scaffold
([`../../../handoffs/2026-07-13_l3_tactic_operationalisation.md`](../../../handoffs/2026-07-13_l3_tactic_operationalisation.md))
and the deferred replay-attacker build. The one-page sign-off summary is
[`binding_signoff_summary.md`](binding_signoff_summary.md); the per-tactic ledger
is [`../../../../data/ogasp/timeline/tactic_action_map.csv`](../../../../data/ogasp/timeline/tactic_action_map.csv).

> **Correction — 2026-07-13 (Marc). Read before the rest of this record; a
> re-run of the recommendation is expected.**
> This record treated substrate comparability — the frozen vuln-pool
> distribution, the untouched goldens, D5 attacker-only — as a **hard
> constraint**, and let it drive both the §5(d) blast-radius scoring and the
> deferral of the CVE-grounded binding (§8). **That weighting is corrected.**
> Per **R4** ("simulation settings can be updated to suit the experiments")
> and Marc's direction, this work does **not** need 1:1 comparison to
> Zhang/Tay — which is `INVALID` regardless
> ([`../../metrics_semantics.md`](../../metrics_semantics.md) §d) — so
> preserving pool-distribution comparability is a **secondary consideration,
> not a dealbreaker.** Re-baselining the goldens on a changed substrate is an
> accepted, logged operation ([`../../../../baseline/CHANGELOG.md`](../../../../baseline/CHANGELOG.md)),
> not a prohibition. Consequences:
> - **The CVE-grounded binding (C0b) is re-opened as a live candidate**, not a
>   deferred bracket. Its "terminus problem" (§8) was an artefact of assuming
>   the pool is a *fixed synthetic set to join onto*; it **dissolves** if the
>   pool is **constructed from** the crosswalk — seed real CVE/CWE/CVSS into
>   MTDSim's `Vulnerability` model so techniques bind by construction. The real
>   open questions become **coverage/tractability** (how much of ATT&CK
>   actually reaches a CVE+CVSS through the published crosswalks) and **seeding
>   mechanics** (CVSS vector → the substrate's complexity/impact/exploit_time).
> - The **framing question** Marc raised — *is "bind" even the right question,
>   vs "ground/construct the substrate in the CTI ontology" so the join is
>   native?* — is carried forward, and a **synthesis mapping layer** is itself
>   a candidate join strategy.
> - The §5(d) weighting and the §6 recommendation should be **re-run** with
>   comparability demoted.
> Both precede the re-run:
> [`../../../handoffs/2026-07-13_l3_crosswalk_join_investigation.md`](../../../handoffs/2026-07-13_l3_crosswalk_join_investigation.md)
> — the ATT&CK↔CAPEC↔CWE↔CVE↔CVSS anatomy, coverage, seeding tractability,
> reading list and visualisations a CVE-grounded-binding decision needs.

---

## 0. What this record answers, and the bar it clears

The question: *given a class-profiled Petri-net behaviour envelope — realised as
a timed sequence of attacker tactic-states (`ogasp-timeline/v1`) — what does the
simulator **do** for each state, such that different operational-objective
classes produce **substrate-observable** behavioural differences, both from each
other and from the inherited 6-phase baseline?*

The governing constraint is the **anti-goal** (Marc, 2026-07-13): the binding must
not be "simply a mapping onto the existing CKC-phased attacker". A binding whose
substrate-visible behaviour is the old phase loop with new state labels adds
nothing an examiner can see, however clean its implementation. Every candidate
below carries a **distinguishability test** — the named substrate-observable
behaviour (action sequence, target selection, timing structure, outcome/survival
semantics) that would differ between two classes and between any class and the
baseline. No re-skin survives.

---

## 1. Impartiality evidence — what was enumerated before the superseded handoff was read

Per the brief's impartiality protocol, the candidate space in §§3–4 was built
from the substrate code, the net/timeline contracts, and the external precedent
sweep (§2) **before** opening the superseded 2026-07-03 binding-scoping handoff.
The independent enumeration reached:

- **Killed brackets:** a naïve phase/verb re-skin (C0a); the
  technique→CAPEC→CWE→CVE→CVSS chain as an MVP bridge (C0b, deferred); the full
  net-driven two-way coupling (C0c, deferred).
- **Live candidates:** schedule-authoritative tempo-replay over verb-wrapped
  tactics (**C1**); the capability precondition/effect contract (**C2**); and the
  net-as-policy-prior over the substrate action space (**C3**, sourced from the
  RL-environment precedent, novel to the repo).
- **Independent recommendation:** stage **C1 → C2** as one pipeline (C1 the
  "get it running end-to-end" cut, C2 the "make it distinguishable enough to
  matter" cut), with **C3** as the designated R2/R3 and two-way extension seam.

**Convergence with the superseded handoff** (evidence the space is real): both
independently land on tactic→verb wrapping over the six existing verbs as the
executable spine (C1); both position the CVE chain as a *tag over the synthetic
pool with the aggregate-CVSS-distribution invariant, pending confirmation*; both
name the same three MTD-interruption candidate policies; both take cost-only
(now R5-confirmed) for the no-network-state tactics.

**Divergence (the load-bearing disagreement):** the superseded handoff
**demotes the capability precondition/effect contract wholesale to the deferred
two-way upgrade path**, on the reasoning that "v1 is one-way replay, so the
binding is simpler". This investigation finds that reasoning **conflates two
independent things**: the *coupling* is one-way (the net does not observe the
simulator), but the *bound attacker can still gate tactic realisation on the
capability footprint the simulator already tracks* — no net reaction is required,
so no two-way coupling is needed. The capability contract (C2) is therefore
compatible with one-way replay and can be brought **forward into v1**. And it
should be, because (a) the substrate *already implements* the survivor-vs-
vulnerable reset model the contract exploits (primer §(e)), so C2's marginal
cost over C1 is small; and (b) the class nets separate only **weakly** at the
routing level (all four classes' mean per-place JSD sits **below** the
shuffled-label null p95 — [`../../../../data/ogasp/petri/README.md`](../../../../data/ogasp/petri/README.md)),
so a tempo-and-order-only binding (C1 alone) risks classes that look alike. C2
adds a *second, independent* separation axis (reset-survival by capability
modality) that does not depend on the nets being far apart. This is the
investigation's substantive correction to the superseded stance.

---

## 2. External precedent sweep — how others bind an abstract attacker to an executable environment

Verdicts: **transfers / partially transfers (what part) / doesn't (why)**.
Extraction stubs precede every load-bearing citation (one framework family per
stub).

| Precedent | What it is | Verdict | What transfers / why not |
|---|---|---|---|
| **MITRE Caldera** (ability + fact model) | Emulation platform; abilities declare required/produced facts (pre/post-conditions); adversary profiles = ability sets | **Partially** | The pre-condition→behaviour→post-condition *triple* is candidate C2's shape and corroborates it as established practice, not invention. Machinery (real command execution on agents) does not transfer to a DES. → [`../../../sources/extractions/adversary_emulation_frameworks.md`](../../../sources/extractions/adversary_emulation_frameworks.md) |
| **CyberBattleSim / NASim / CybORG** | RL security environments; attacker = policy over a typed action space (local/remote exploit, credential lateral movement), outcome model with per-action cost + success prob | **Partially** | The *attacker-as-distribution-over-an-action-space* framing is candidate C3, and CyberBattleSim's first-class **credential handling** independently corroborates primer §(e)'s "credentials survive mutation". The **learning loop does not transfer** — the net *is* the fixed policy prior; RL training would reintroduce deferred adaptivity and break SIM-05. → [`../../../sources/extractions/rl_security_environments.md`](../../../sources/extractions/rl_security_environments.md) |
| **MulVAL / MAL / coreLang** | Logic/asset attack-graph languages; attack steps carry preconditions + acquired-asset postconditions | **Partially** | Confirms the precondition/effect model (C2) is the *standard* executable reading of an attack graph. Coverage is thin (MulVAL < ¼ of ATT&CK; coreLang ~11 techniques), so they are precedent for the *contract*, not a rule base to import. → [`../../../sources/extractions/attack_crosswalk_density.md`](../../../sources/extractions/attack_crosswalk_density.md) |
| **CTID ATT&CK↔CVE / BRON / CVE2CAPEC** | Published technique↔CAPEC↔CWE↔CVE crosswalks | **Doesn't (for MVP)** | Sparse at every hop (~419 CVEs curated to ATT&CK; ~112/546 CAPECs mapped) **and** the substrate has no CVE keys to terminate on — the chain yields a label, not a join. Positions the CVE bridge as future work (§8). → [`../../../sources/extractions/attack_crosswalk_density.md`](../../../sources/extractions/attack_crosswalk_density.md) |
| **Bland 2020 / Outkin 2023 / timed attack models** (already extracted) | Agent-side ML attacker; game-theoretic defender; SPN/TPN firing | **Partially** | Bland is the agent-construction template (already cited in ch3 §V). Timed-Petri firing semantics are the deferred GSPN path (D10), not v1. → existing stubs. |

**Novelty (gate 1):** candidate **C3** — reading the OGASP net as a *policy prior
over the substrate's verb action space* — appears in **no existing repo
document** (the repo frames the net as envelope/script, i.e. replay). It is
sourced from the RL-environment precedent above and from first principles.

---

## 3. The design space — five axes

The candidate space is spanned by the brief's five axes; each candidate in §4 is
a *coherent selection of one value per axis*.

- **A — Binding altitude:** (i) tactic→verb wrapping; (ii) tactic→technique→action
  synthesis (techniques inside the place select behaviour); (iii) new
  tactic-native actions (greenfield capabilities); (iv) hybrid per tactic group.
- **B — Semantic bridge:** (i) direct hand-authored tactic→verb map (D6); (ii)
  technique→CAPEC→CWE→CVE→synthetic-CVSS chain → tag over the pool; (iii)
  capability precondition/effect contract.
- **C — Sequencing authority:** (i) timeline-replay, schedule-authoritative
  (verbs run inside the state's dwell window); (ii) event-authoritative (timeline
  gives order, substrate gives duration); (iii) net-driven in-SimPy stepping
  (the deferred two-way coupling).
- **D — Success semantics:** (i) action-completion; (ii) state-gated (D7 — the
  tactic-state decides whether the verb is even attempted); (iii) objective-read
  (objective tactics visited *and* substrate-realised). Backward transitions:
  failure/retry vs cost-only.
- **E — Substrate rework:** the minimal change set, file-by-file, and whether the
  synthetic-vuln pool is touched (it must not be, per the comparability
  invariant).

**The degenerate-in-SimPy check (axis C-iii), settled before dismissal.** The
brief asks whether a *degenerate* in-SimPy net walk is actually simpler than
replay. Verdict: **no.** A precomputed timeline (`ogasp-timeline/v1`, already
shipped, seeded, tested, byte-reproducible) is strictly simpler than re-walking
the net inside SimPy — the walk logic, the objective-condition check, and the
determinism guarantees already exist in the standalone runner and would have to
be re-implemented (and re-verified) inside the DES with no MVP benefit. Replay
(C-i) wins for v1; the in-SimPy walk returns *with* two-way coupling, where the
net must observe live state (D2/D10 deferral). C3 is the on-ramp: its policy
layer is what an in-SimPy walk would sample from.

---

## 4. The candidates

### Dead on arrival / deferred (the brackets of the space)

**C0a — Naïve phase/verb re-skin.** Altitude (i), bridge (i), authority — none
(the substrate's greedy loop keeps driving); each tactic relabels one of the six
verbs and the inherited loop races to compromise-fraction 0.8 as before.
**KILLED on distinguishability (gate a):** the timeline is decorative — the
substrate ignores it, so all classes and the baseline produce the *same* greedy
walk with different labels. This is the anti-goal itself, named so it is on the
record with its cause of death.

**C0b — CVE-chain semantic bridge as the MVP.** Altitude (ii), bridge (ii).
**DEFERRED to future work (§8):** the substrate has no CVE keys, so the chain
terminates in a low-confidence label, not a join; and nothing at MVP reads the
label. Grounded in the crosswalk-density figures (§2), not assumed.

**C0c — Full net-driven two-way coupling.** Authority (iii). **DEFERRED (D2/D10):**
the end goal, not the MVP; the net observing the simulator each event is
explicitly out of scope. C3 preserves the on-ramp.

### Live candidates

**C1 — Schedule-authoritative tempo-replay over verb-wrapped tactics.**
*Altitude (i) · bridge (i) · authority (i) · success (i)+(iii).* The bound
attacker reads the timeline as an authoritative script: for each state in
`sequence`, it consumes `dwell_s` on the SimPy clock and fires the mapped verb(s)
for that tactic against the current substrate position; run success is
objective-read. **What the timeline drives:** ordering + tempo + termination —
replacing the greedy loop's fixed scan→exploit→pivot cycle and its 0.8
fraction-stop.
- **Distinguishability:** classes route through different tactic sequences with
  different dwells (scan-shaped 35 s, stealth 45 s, exploit 4.5 s,
  objective-execution 36 s), so against a *fixed* MTD schedule they absorb
  **different numbers of mutations per objective** and yield different MTTC/ASR.
  vs baseline: the baseline sprints (short fixed verb durations, no stealth
  dwell) and self-directs its order; the bound attacker follows a CTI-grounded
  order at a CTI-grounded tempo. **Named observable:** MTD-interrupts absorbed
  per objective, and the resulting MTTC/ASR, differ by class and vs baseline
  because dwell-driven tempo differs. This is the thesis punchline (primer §(d):
  outpacing a sprint ≠ beating a low-and-slow campaign).
- **Honest weakness:** distinguishability rides on inter-class tempo/routing
  differences, which are **weak-to-moderate** (JSD < null p95). Tempo alone may
  under-separate the classes — which is exactly why C2 is staged immediately
  behind it.

**C2 — Capability precondition/effect contract (C1 + a capability-state layer).**
*Altitude (i)+(iv) · bridge (iii) · authority (i) · success (ii)+(iii).* Adds a
capability footprint to the attacker state — {footholds, credentials (the
survivor "key"), map-knowledge, persistence-hold} — most of which the substrate
*already tracks* (`compromised_hosts`, `compromised_users`, the host-stack). Each
tactic declares a precondition (capability needed to realise) and an effect
(capability granted). A timeline state realises only if net-enabled **and** its
precondition holds in the world; otherwise it is refused (backward-transition
reading, §5.3).
- **Distinguishability (the strongest):** classes differ in *what capability they
  accumulate* and therefore *how they survive MTD*. A credential-first class
  (routes through credential-access early → holds the key) executes
  lateral-movement that **survives** a network mutation via credential reuse; a
  scan-first class gets thrown back to host-discovery by the same mutation. The
  substrate already implements this split (primer §(e)) — C2 merely lets the
  *class-conditioned capability accumulation* drive the *class-conditioned MTD
  survival*. **Named observable:** post-mutation recovery path (re-scan vs
  key-reuse) and its MTTC cost differ by class, on the *same* terrain, even when
  routing barely differs. This is the axis that rescues distinguishability from
  weak net separation, and it directly stresses the "generic attacker
  under-uses the one modality MTD cannot reset" gap (primer §(d)).
- **Weakness:** more design surface (per-tactic pre/effect declarations, gating
  logic, backward-transition handling); slower to first results than C1. But it
  is a strict superset of C1, so it is an increment, not a rewrite.

**C3 — Net-as-policy-prior over the substrate action space (the novel candidate;
the R2/R3 + two-way seam).**
*Altitude (ii) · authority (i)→(iii) · success (ii).* Reframes the binding from
"replay a script" to "sample the substrate action from a **class-conditioned
selection distribution**". At MVP (degenerate): the timeline still fixes the
tactic *order* (replay), but where a tactic admits more than one substrate
action/target, the choice is drawn from a class- (later style-) conditioned prior
under the seeded stream.
- **Distinguishability:** classes induce different empirical verb-mix and
  target-preference distributions even on identical terrain — and this is the
  natural home for R2 (per-action success as a distribution parameter) and R3
  (styles as selection temperature / reward shape).
- **Honest finding:** at *pure* MVP (R2/R3 out of scope, one candidate action per
  tactic), C3 **reduces toward C1** — the distribution is a point mass. Its value
  is **extensibility**, not standalone MVP distinguishability: it is the seam that
  admits R2/R3 and the two-way coupling *without redesign*. Recommended as the
  *architecture* C1/C2 are built inside, not as a separate v1 deliverable.

---

## 5. Cross-examination against the five criteria

Argued in prose; kill/keep per candidate. Where criteria conflict (richness vs
practicality, chiefly), the trade is argued, not averaged.

**(a) Distinguishability (first gate).** C0a fails outright. C1 passes via tempo
(honest but thin under weak net separation). C2 passes strongest (reset-survival
by modality — an independent axis). C3 passes only *with* R2/R3 (point-mass at
MVP). → **C1 keep (thin), C2 keep (strong), C3 keep (as seam).**

**(b) MVP practicality (effort to preliminary results).** C1 is the cheapest path
to end-to-end results — a timeline reader, a tactic→verb dispatch, a record
emitter, an objective-read termination check; no substrate behaviour touched. C2
adds a capability tracker (largely existing state) + pre/effect declarations +
gating — a bounded increment, and the *survival behaviour it exploits already
exists*. C3-at-MVP is nearly free (a dispatch indirection) but buys nothing until
R2/R3. → **C1 fastest; C2 close behind; C3 architectural, not costly.**

**(c) Academic richness (a design section, not plumbing).** C1 alone is a
defensible but modest argument (tempo-vs-interval). C2 is the richest: it *is* the
ch3 precondition/effect contract realised, with the per-modality reset split —
"the strongest, most falsifiable claim in the work" (primer §(e)). C3 adds the
policy/action-space framing that connects the work to the RL-environment
literature and to R2/R3. → **C2 richest; C1 modest; C3 connective.**

**(d) Substrate blast radius (D5 attacker-only; goldens untouched).** All three
are attacker-side and leave the vuln pool, network, MTD, and statistics maths
untouched (§6). C1/C2/C3 all preserve the byte-identical baseline path. The only
question is *how much new attacker-side code* — C1 least, C2 a bounded increment,
C3 an indirection. → **all keep on blast radius.**

**(e) Extensibility (R2 / R3 / two-way without redesign).** C1 alone has no
natural R2/R3 seam — success is action-completion, styles have nowhere to attach.
C2 adds capability but still no stochastic selection point. **C3 is the seam** —
R2 is a distribution parameter, R3 a selection temperature, two-way coupling
swaps the precomputed timeline for a live net walk that samples the same policy.
→ **C3 essential for extensibility; C1/C2 need it to avoid a later rewrite.**

**The conflict, argued:** richness (C2) vs practicality (C1) is the live tension.
The supervisor's standing MVP principle (pipeline-first, early results,
practicality > fidelity) points at C1; the anti-goal and the weak net separation
point at C2. The resolution is **not to average** but to **stage**: build C1's
replay spine first (it is the shared substrate of all three and yields results
earliest), *inside* the C3 dispatch architecture (so R2/R3/two-way attach later
for free), then layer C2's capability gating as the immediate next increment (it
is what makes the results *mean* something under the anti-goal). C1 alone is
shippable but at risk of thin separation; C2 is the target the moment C1 runs.

---

## 5b. The load-bearing constraint the map is not free to ignore — MTTC verb identity

**Finding (grounded, file-level):** internal MTTC is defined as the mean duration
over exactly three record names — `SCAN_PORT`, `EXPLOIT_VULN`, `BRUTE_FORCE`
([`../../metrics_semantics.md`](../../metrics_semantics.md) §(a);
[`../../../../mtdnetwork/statistic/evaluation.py`](../../../../mtdnetwork/statistic/evaluation.py)
`evaluation_result_by_compromise_checkpoint`). Therefore the tactic→verb map is
**constrained, not free**: for MTTC to be non-degenerate per class, the
exploit-shaped and scan-shaped tactics **must** emit these three verb names. A map
that routed, say, all objective tactics to cost-only records and left the
exploit tactics unmapped would compute MTTC = 0 for that class. The ledger (§7)
honours this: every exploit-shaped tactic (initial-access, privilege-escalation,
credential-access, lateral-movement) emits `EXPLOIT_VULN`/`BRUTE_FORCE`, and the
enumeration tactics (reconnaissance, discovery) emit `SCAN_PORT`, so MTTC is
populated for every class that routes through them. This is a *stronger* form of
the constraint than the superseded handoff recorded (it named the comparability
consequence but not the forcing on the map). The 6-phase baseline's MTTC event
definition stays **byte-identically unchanged** — the bound attacker merely emits
rows the same pipeline reads.

---

## 6. The recommendation — C1→C2 staged, inside the C3 dispatch architecture

**Recommended MVP binding:** schedule-authoritative timeline-replay over
verb-wrapped tactics (**C1**), built inside a class-conditioned dispatch
indirection (**C3** architecture, point-mass at MVP), with the capability
precondition/effect layer (**C2**) as the immediate next increment. The seven
contract elements the replay-attacker build needs:

**6.1 Input contract.** The bound attacker consumes `ogasp-timeline/v1`
([`../../../../data/ogasp/timeline/timeline_schema.md`](../../../../data/ogasp/timeline/timeline_schema.md))
and pins the schema version (any field/semantics change bumps it). It reads
`sequence[]` (tactic, dwell_s, transition_fired), `objective_tactics`,
`objective_rule`, and `seed`. It never re-walks the net (the runner already did)
and never imports the net builder.

**6.2 Per-tactic dispatch.** The complete ledger is §7 /
[`tactic_action_map.csv`](../../../../data/ogasp/timeline/tactic_action_map.csv).
Six tactics map to MTTC-counted verbs; nine are cost-only dwell or
objective-realisation markers (R5-confirmed for the stealth/no-network-state
tactics).

**6.3 Realisation and outcome semantics (D7 three-layer).** Layer 1 = timeline
state (which tactic, when). Layer 2 = the substrate action the state triggers.
Layer 3 = outcome. For MTTC-verb tactics, outcome is the *substrate's own*
success (exploit lands iff `random() < complexity` — the state decides *whether
the verb is attempted*, the substrate decides *whether it lands*: D7's
"state decides the outcome" read as *state-gating*, not as overriding the dice).
For cost-only tactics, outcome = dwell elapsed (a state transit; nothing
realised). **Backward transitions read as cost-only re-attempt** (the token
revisiting a tactic = the attacker re-doing it: dwell + re-emitted verb), **not**
as a failure model — failure is the substrate's business (D7), and inventing a
net-level failure semantics would demand precision the envelope does not carry.
**"The attack succeeded"** is derived attacker-side: the class objective set is
visited in the timeline **and** substrate-realised (objective-marker preconditions
held). This coexists with, and does not touch, the baseline's compromise-
checkpoint MTTC.

**6.4 MTD-interruption policy.** *Recommended:* **inherit the substrate's existing
interrupt handling** — a network-layer mutation throws the current tactic back to
host-discovery (position/map lost), an application-layer mutation back to
port/vuln re-enumeration on the same still-owned foothold, with the existing
confusion penalty; capability (footholds, credentials) survives per primer §(e).
Under C2 this becomes *capability-conditioned* for free: a credential-backed
tactic survives, a scan-backed tactic resets — the substrate already routes it
that way. *Alternatives named and rejected:* **timeline-rigid** (mutation imposes
penalty but the attacker resumes its scripted state — rejected: makes the
attacker effectively MTD-immune, defeating the evaluation); **state-fails-and-
timeline-advances** (rejected for MVP: discards the interrupted work and needs a
failure model the envelope lacks; revisit with R2).

**6.5 Record contract.** The bound attacker calls the existing
`append_attack_operation_record(name, start, finish, adversary[, mtd])` with
`name ∈` the six verbs, so the existing statistics pipeline computes MTTC/ASR
unchanged. Cost-only tactics emit a **sidecar record** under a *new* name the
statistics pipeline ignores (must not collide with the three MTTC verbs), so the
dwell is visible for provenance without polluting MTTC.

**6.6 Determinism (SIM-05).** Same timeline + seed → same records. The timeline
is already seeded and byte-reproducible; the bound attacker must draw **all**
randomness from the seeded `random` stream (as `Host.uuid` / `Vulnerability.id`
do) — no wall-clock, no unseeded `random`. The only randomness in play is the
substrate's own (exploit success, target-order jitter), already seeded.

**6.7 Extension hooks (not designs).** R2 (per-action success rate): a
class/style-conditioned multiplier at the C3 dispatch point, over the substrate's
native success check (no double-counting — it *modulates* the existing dice).
R3 (styles): a style vector parameterising dwell scaling, the R2 multiplier, and
the C3 selection temperature; the dispatcher takes both a class-timeline and a
style-vector (composes-with or replaces classes — the open R3 question, left
open). Two-way coupling: C3's policy is what an in-SimPy net walk samples from.

---

## 7. The substrate minimal-change set (file-by-file, recommended candidate)

Respects D5 (attacker-only) and the goldens (baseline path byte-identical).

| File | Change | Baseline impact |
|---|---|---|
| **NEW** `mtdnetwork/operation/timeline_attack_operation.py` | The bound attacker operation: same constructor signature as `AttackOperation(env, end_event, adversary, proceed_time)` + `proceed_attack()`; consumes a timeline; dispatches verbs; emits records | none (new file) |
| **NEW** attacker-side dispatch module (tactic→verb map + capability tracker) | The §7 ledger as code + the C3 dispatch indirection; C2 pre/effect declarations | none |
| `mtdnetwork/component/adversary.py` | *Additive only* — capability-footprint accessors if the tracker rides on the adversary (or a thin subclass) | none (additive) |
| `baseline/run_baseline.py` (or the run harness) | *Additive branch* — construct `TimelineAttackOperation` instead of `AttackOperation` when a timeline is supplied; pass it to `MTDOperation` identically (`attack_operation=`) | baseline branch unchanged; goldens re-run the 6-phase path |
| **UNCHANGED** | `attack_operation.py` (baseline), `services.py` (vuln pool), network, MTD mechanisms, `statistic/*` | frozen — comparability invariant holds |

**Comparability invariant (stated):** the recommended binding **does not touch the
synthetic-vuln pool** — it only *reads* it through the same `exploit_time` /
`get_vulns` paths. The aggregate CVSS distribution is unchanged, so baseline MTTC
is untouched ([`../../metrics_semantics.md`](../../metrics_semantics.md) §(d)).

---

## 8. The technique→CAPEC→CWE→CVE→synthetic-CVSS chain — position

> **Corrected 2026-07-13 (see the top banner):** the position below is
> **superseded** — the CVE-grounded binding is now a **live candidate**, not
> deferred future work. Reasons (1) [terminus] and (2) [density] below are
> re-read as follows: (1) *dissolves* under a **constructed** pool (seed CVEs
> in, don't join onto synthetic), and (2) becomes the central *tractability*
> question the crosswalk-join handoff investigates rather than a reason to
> defer. The comparability invariant is now secondary (R4), not a gate.

**Original position (retained for the record): dissertation-defensible future
work (or a v1.1 enrichment *iff* the substrate adopts NVD CVEs), NOT the MVP
semantic bridge.** Grounded in what the crosswalks *actually contain*
([`../../../sources/extractions/attack_crosswalk_density.md`](../../../sources/extractions/attack_crosswalk_density.md)),
not in an assumption of density:

1. **Terminus (decisive):** the chain ends at a CVE; the substrate's vulns are
   synthetic with no CVE key, so the best output is a *tag*, not a *join*. A tag
   changes nothing behaviourally unless something reads it — and the reader would
   be the C3 policy layer, which is post-MVP.
2. **Density (corroborating):** every hop is sparse (~419 CVEs curated to ATT&CK;
   ~112/546 CAPECs mapped; MulVAL < ¼ of techniques), so even the tag is
   low-coverage and low-confidence.

If ever adopted, the tag must be a **pure overlay** holding the aggregate CVSS
distribution fixed (comparability invariant), and it becomes meaningful only once
C3's action-selection reads it (e.g. an exploit-shaped state prefers
tag-matching vulns). The trigger to revisit is the substrate adopting NVD CVEs —
the same trigger the primer §(b).3 and ch3 revisit-conditions already name.

---

## 9. What the recommendation defers and forecloses

**Defers:** R2 success-rate model and R3 styles (hooks only, §6.7; owned by the
operationalisation handoff); timing calibration (post-MVP, R1); the CVE-chain
bridge (§8); two-way coupling and in-SimPy net stepping (D2/D10); the inferred
recon→initial-access prefix bridge (GAP Decision 6 Option B — the nets stay
observed-only, so classes with a disconnected recon island are seeded at
initial-access per D8).

**Forecloses (things this design rules out, not merely postpones):** a binding
where the net's transition dice are *overridden* by a net-level success model
(D7 keeps the substrate's dice; the net gates, it does not re-roll); any binding
that flattens class routing back into the fixed phase loop (the anti-goal).
*(The earlier third foreclosure — "any pool-touching design that moves the
aggregate CVSS distribution" — is **withdrawn** per the top banner: a
pool-touching, re-baselined design is now permitted; comparability is secondary,
R4.)*

**The residual risk, stated:** if C1+C2 still fail to separate the classes under
MTD, the executable track inherits the negative-result disposition declared at
the partition stage (ch3 §"the risk that outranks the encoding") — and *that
finding, argued, is a legitimate result*, not a failure of the binding. C2's
independent survival axis is the design's best hedge against it; C3's R2/R3 seam
is the next.

---

## 10. How this connects

- Register: [`supervisor_decision_register.md`](supervisor_decision_register.md)
  (D1–D10, R1–R5) — D5/D6/D7 executed here (scoping); R5 cost-only recorded on
  every cost-only ledger row.
- Conceptual base: [`../../../notes/ch3_design/structure_to_behaviour_binding.md`](../../../notes/ch3_design/structure_to_behaviour_binding.md)
  (the three binding levels; C2 = the "capability precondition/effect contract"
  it names as the right target).
- Substrate facts: [`../../substrate_primer.md`](../../substrate_primer.md) §(d)/§(e)
  (the reset model C2 exploits); [`../../metrics_semantics.md`](../../metrics_semantics.md)
  §(a)/§(d) (MTTC identity + comparability invariant).
- Upstream contract: [`../../../../data/ogasp/timeline/timeline_schema.md`](../../../../data/ogasp/timeline/timeline_schema.md);
  net structural summary + weak-separation finding: [`../../../../data/ogasp/petri/README.md`](../../../../data/ogasp/petri/README.md).
- Downstream: [`../../../../data/ogasp/timeline/tactic_action_map.csv`](../../../../data/ogasp/timeline/tactic_action_map.csv)
  (the ledger); [`binding_signoff_summary.md`](binding_signoff_summary.md) (the
  one-pager for Jin); the operationalisation handoff (R2/R3); the deferred
  replay-attacker build (implements this).
