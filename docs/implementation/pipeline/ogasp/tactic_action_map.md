---
status: durable
created: 2026-07-21
topic: "L3 M5/M6 — the manual tactic→action influence map: the six substrate verbs, which tactics each influences, the M2 binary verdict per tactic, and the M6 pre-intrusion synthetic join (applied 2026-07-21)"
updated: 2026-07-21
---

# The tactic→action influence map — the substrate's six verbs, the 15-tactic mapping, the outcome-oracle verdicts, and the M6 pre-intrusion join

**Status:** durable. The implementation record that executes **M5** (the manual,
justified tactic→action influence map) and **defines the M2/M4 outcome-oracle
verdicts** the live feedback net consumes, and that specifies **and applies
(2026-07-21, on Marc's go-ahead) M6** (the synthetic pre-intrusion join). It sits on top of
the read-only action-layer anatomy
([`action_layer_anatomy.md`](action_layer_anatomy.md)): the anatomy says what
the attacker *is as a machine*; this record says **which CTI tactic each verb
realises**, and **what "success" and "failure" concretely are** when the net
asks the substrate for an outcome.

**What this consumes, and does not re-derive.** The action inventory, the
coupling graph, the callability classes, the affordance/limitation register,
and the interpretive ATT&CK coverage all live in the anatomy record; §2 here
restates only the per-verb facts the mapping and the verdicts turn on, at their
seam. The 15 per-tactic behaviour profiles
([`../../../notes/ch3_design/tactic_profiles/`](../../../notes/ch3_design/tactic_profiles/))
are the single authority for what each tactic *attempts*; the justification
column cites each profile's §5 catalogue block and never forks it. The rulings
this executes are in the supervisor decision register
([`supervisor_decision_register.md`](supervisor_decision_register.md) §M1–M8,
D3/D4, R2/R5).

**Governing constraint (guardrails):** existing action vocabulary only — no new
verbs, no edits to `attack_operation.py` *behaviour* (M5/M7); the map is
analysis over the carved surface, not a change to it. The only code this record
carries is the **M6 net-build curation** (§6) — L3 net-build code
(`src/mtdsim/l3_simulation/petri/`), applied 2026-07-21 on Marc's go-ahead; the
simulator (`mtdnetwork/`) is untouched.

---

## 1. What changed since the handoff was written: the carve landed

The handoff ([`../../../handoffs/2026-07-15_l3_tactic_action_influence_map.md`](../../../handoffs/2026-07-15_l3_tactic_action_influence_map.md))
asked every map row to carry a callability constraint drawn from three classes —
*unconditional* / *conditional on carve* / *conditional on context synthesis*.
**The middle class is now discharged.** The §3.3 carve specified in the anatomy
record **landed 2026-07-21** (anatomy §3 banner;
[`attack_operation.py`](../../../../mtdnetwork/operation/attack_operation.py),
[`tests/test_action_layer_carve.py`](../../../../tests/test_action_layer_carve.py)):
each verb's `_do_*` core is now independently callable via `step(verb)`, which
runs one verb with its native time cost, returns its outcome, and dispatches **no**
successor — the driver owns succession. `assert_action_context(verb)` fails loud
on an unmet precondition rather than degenerating silently or crashing.

Consequently the map's callability dimension collapses to **two** classes:

- **callable-as-is** — `SCAN_HOST` only; it manufactures its own `host_stack`
  from network state, no precondition.
- **callable-with-context** — the other five; the driver must satisfy the verb's
  precondition (a populated `host_stack`, a set `curr_host`, a populated
  `curr_ports`) before `step()` will run it, or `assert_action_context` raises.
  This is the "context synthesis" the handoff named; post-carve it is a
  *supported* operation, not a workaround.

No row is "conditional on carve" any longer. What remains conditional is only
whether the driver supplies the verb's shared-state context — a mechanical
precondition, now guarded — and the standing **module-global tunables**
limitation (§3, §5): tempo/threshold levers exist but bite uniformly across the
run, not per invocation, absent a further carve (anatomy §4.2).

---

## 2. The action inventory — the six verbs at the oracle seam

Every attacker action, with the four facts the verdict contract needs: what
adversary/substrate **state** it effects, how it is **priced** (time), the
**native dice** it rolls (the outcome is *read from* these — never re-rolled;
§5), and the **readable outcome** a driver observes (the `_do_*` return value).
Full coupling detail is anatomy §2.2; this is the seam view.

| Verb | State effect | Pricing (time) | Native dice (the substrate's own roll) | Readable outcome (`_do_*` return) | Callability |
|---|---|---|---|---|---|
| **`SCAN_HOST`** | rebuilds `host_stack` from the hacker-visible graph; `pivot ← −1` | `ATTACK_DURATION['SCAN_HOST'] = 5 s` | none — deterministic enumeration over network state | `bool`: `host_stack` non-empty (≥1 reachable uncompromised host found) | callable-as-is |
| **`ENUM_HOST`** | pops `host_stack → curr_host`; ticks `attack_counter` (+ give-up list, targeted net only); clears `curr_ports`/`curr_vulns`; sets pivot | `ATTACK_DURATION['ENUM_HOST'] = 5 s` | none | `bool`: enumerated host **already** compromised (→ re-control) vs **fresh** | callable-with-context (`host_stack` non-empty) |
| **`SCAN_PORT`** | `curr_ports ← curr_host.port_scan()`; tests credential reuse | `ATTACK_DURATION['SCAN_PORT'] = 25 s` | `can_auto_compromise_with_users`: deterministic **if** a harvested user has a reused password on the host (gated by `possible_user_compromise`) | `bool`: reuse compromised the host (T1078 shortcut) | callable-with-context (`curr_host`) |
| **`EXPLOIT_VULN`** | per vuln: `vuln.network(host)` marks exploited, `curr_attempts += 1`; on compromise bumps exploitability + scores | per vuln `exp(exploit_time, 0.5)`, `exploit_time = 15 s × (1 − complexity)`, `÷2` if the *instance* was exploited before (ATK-04), `×2.5` on OS mismatch | per vuln `random.random() < complexity`; host compromised once **Σ exploited impact > `SERVICE_COMPROMISED_THRESHOLD = 7`** (impact ∈ [0, 10]) | `EXPLOIT_COMPROMISED` / `EXPLOIT_UNCOMPROMISED` / `EXPLOIT_HALTED` (interrupt/sim-end) | callable-with-context (`curr_host` + `curr_ports`) |
| **`BRUTE_FORCE`** | `curr_host.compromise_with_users` may compromise the host | `ATTACK_DURATION['BRUTE_FORCE'] = 20 s` | `random.random() < HOST_MAX_PROB_FOR_USER_COMPROMISE × (harvested users on host ÷ total users)` — probability rises with credential footprint (credential stuffing) | `bool`: host compromised | callable-with-context (`curr_host`) |
| **`SCAN_NEIGHBOR`** | `host_stack ← discovered_neighbors + existing` (new pushed to front) | `ATTACK_DURATION['SCAN_NEIGHBOR'] = 5 s` | none — deterministic neighbour discovery from the owned host | `None` (no branch) | callable-with-context (`curr_host`, just-compromised) |

**`ENUM_HOST` is the dispatcher, not an oracle.** Its `bool` distinguishes an
already-owned host (loop) from a fresh target (attack); it is not a
success/failure verdict for any tactic. It selects *which host* the verdict-
bearing verbs act on. It maps to **no CTI tactic** (anatomy §5.1: internal
target selection, no ATT&CK counterpart) and appears in the map only as the
gate that sets `curr_host` for the four chain-bound verbs.

---

## 3. The tactic → action influence map (M5)

**The relation is many-to-many and concentrated.** Reading "which actions does
each tactic influence" (M5's framing, not the superseded one-action-per-tactic
C2 *binding*): one verb realises several tactics (`EXPLOIT_VULN` spans four),
and six of the fifteen tactics have any verb at all. The action-bearing six are
exactly the get-in-and-spread band the anatomy's ATT&CK coverage isolates
(§5.2); the other nine are **dwell-only** — no substrate verb prices them, and
R5 sanctions leaving them as pure dwell (the token still traverses them; the net
carries their duration from the catalogue).

### 3.1 The matrix

`✓` = the tactic influences (is realised by) the verb. `·` = no influence.
`ENUM_HOST` is omitted — it realises no tactic (§2).

| Tactic (TA) | `SCAN_HOST` | `SCAN_PORT` | `EXPLOIT_VULN` | `BRUTE_FORCE` | `SCAN_NEIGHBOR` | Band |
|---|:--:|:--:|:--:|:--:|:--:|---|
| reconnaissance (TA0043) | ✓ | ✓ | · | · | · | prep / discovery |
| resource-development (TA0042) | · | · | · | · | · | prep — dwell-only |
| initial-access (TA0001) | · | ‣ | ✓ | · | · | get-in |
| execution (TA0002) | · | · | · | · | · | dwell-only |
| persistence (TA0003) | · | · | · | · | · | dwell-only |
| privilege-escalation (TA0004) | · | ‣ | ✓ | · | · | get-in |
| stealth / defense-evasion (TA0005) | · | · | · | · | · | dwell-only |
| defense-impairment (TA0112) | · | · | · | · | · | dwell-only |
| credential-access (TA0006) | · | · | ✓ | ✓ | · | spread |
| discovery (TA0007) | ✓ | ✓ | · | · | ✓ | spread |
| lateral-movement (TA0008) | · | · | ✓ | ✓ | ✓ | spread |
| collection (TA0009) | · | · | · | · | · | objective — dwell-only |
| command-and-control (TA0011) | · | · | · | · | · | objective — dwell-only |
| exfiltration (TA0010) | · | · | · | · | · | objective — dwell-only |
| impact (TA0040) | · | · | · | · | · | objective — dwell-only |

`‣` = **precursor context, not a mapped influence.** `SCAN_PORT` populates
`curr_ports`, which `EXPLOIT_VULN` requires; for initial-access and
privilege-escalation the *verdict-bearing* act is the exploit, and the port scan
is the context `ENUM_HOST`→`SCAN_PORT` synthesises before it. `SCAN_PORT` is a
mapped influence only where the scan *is itself* the tactic (reconnaissance,
discovery — service enumeration).

### 3.2 Per-pair justification (the twelve influenced pairs)

Each justification cites the tactic profile's §5 block and carries the anatomy
callability constraint. Group labels are the profile `group_hypothesis`.

**reconnaissance × `SCAN_HOST`, × `SCAN_PORT`** — scan-shaped (§5: "the
substrate prices reconnaissance as an active scan verb", ×1.0 of the scan
anchor, Tier 1). The opening `SCAN_HOST` from the ingress is recon-shaped
(anatomy §5.1: T1595/T1018); `SCAN_PORT` is the service-enumeration pass
(T1046). Callable-as-is / callable-with-context. The patient off-network recon
the literature reports is a recorded *tempo* divergence, not a metered dwell.

**initial-access × `EXPLOIT_VULN`** — exploit-shaped (§5: server-side entry is
"exactly what complexity-scaled `exploit_time` prices", ×1.0, Tier 1, not
tuned). `EXPLOIT_VULN` against an exposed endpoint is T1190. Callable-with-
context (`curr_host` = an exposed host, `curr_ports` from `SCAN_PORT`). The
phishing/watering-hole delivery-wait is outside the metered action (§2 shape
divergence).

**privilege-escalation × `EXPLOIT_VULN`** — exploit-shaped (§5: canonical
instance is vuln exploitation the substrate prices via `exploit_time`, ×1.0,
Tier 1). Same verb, local-exploit reading (T1068). Callable-with-context. The
token/valid-account variant is a faster reuse-of-material path the substrate
does not separately price (within-group skew).

**credential-access × `EXPLOIT_VULN`, × `BRUTE_FORCE`** — exploit-shaped for the
dumping path (§5: OS Credential Dumping T1003 is substrate-priceable, ×1.0, Tier
1). `EXPLOIT_VULN` abstracts the on-host dump; `BRUTE_FORCE` is Credential Access
→ Brute Force, specifically T1110.004 credential stuffing (reuses the harvested
pool; anatomy §5.1). Both callable-with-context. This is the **survivor pole**
of the reset axis — the harvested credential is a standing possession no shuffle
resets (§5, [[09_credential-access]]).

**discovery × `SCAN_HOST`, × `SCAN_PORT`, × `SCAN_NEIGHBOR`** — scan-shaped (§5:
"internal enumeration priced as the substrate scan verb", ×1.0, Tier 1).
Reconnaissance's interior twin: `SCAN_NEIGHBOR` is the post-foothold discovery
engine (T1018), `SCAN_PORT` the interior service scan (T1046), `SCAN_HOST` the
foothold-grown host discovery. Callable-as-is / callable-with-context. Purely
reset-*vulnerable* — a position shuffle invalidates the map wholesale (§3).

**lateral-movement × `EXPLOIT_VULN`, × `BRUTE_FORCE`, × `SCAN_NEIGHBOR`** —
exploit-shaped (§5: dominant form is a remote-service login/exploit the
substrate prices, ×1.0, Tier 1, wide sweep). The **per-modality split** the
thesis turns on: `EXPLOIT_VULN` is the scan-hop (T1210, reset-vulnerable),
`BRUTE_FORCE` the credential-hop (T1110.004, reset-survivor), `SCAN_NEIGHBOR`
the discovery that finds the next hop target. Callable-with-context. Which
modality dominates is objective-conditioned ([[11_lateral-movement]]).

### 3.3 The nine dwell-only tactics (explicit no-action rows)

Each has **no substrate verb** (anatomy §5.2: the post-ingress objective tactics
are absent as techniques). The token dwells for the catalogue duration and
advances on the net's base forward weight (M2 unconditioned — no outcome oracle
to condition it). R5 sanctions this.

- **resource-development** — off-clock (§5: ×0, "the adversary arrives already
  equipped"). Dwell-only; the M6 join gives it its only net edge (§6).
- **execution** — no verb prices "run a payload" (§5: group genuinely unsettled,
  ×0.5, Tier 3). `EXPLOIT_VULN` *abstracts over* execution (anatomy §5.1) but
  does not model it as a distinct act; the R2 execution-success hook attaches
  here later (§5).
- **persistence** — no verb prices "maintain a foothold" (§5: ×1.0, Tier 3);
  survives via rate contest (FlipIt), not a metered act.
- **stealth / defense-evasion** — detection is culled project-wide (§5: Tier 3,
  "nothing to evade in-sim"); value is tempo, which the dwell already carries.
- **defense-impairment** — the substrate models no defensive-control state (§5:
  widest sweep, Tier 3); effect declared as future work only.
- **collection** — no verb prices "gather data" (§5: ×1.0, Tier 2); a real dwell
  floor; pre-objective capability for the steal profiles.
- **command-and-control** — no verb prices a channel (§5: un-priceable by CVE
  data, Ling & Ekstedt; Tier 3); objective for `infrastructure_setup`. In code,
  Brown's "assume C2" is merely `update_reachable_compromise` (anatomy §5.2).
- **exfiltration** — terminal data-theft act, no verb (§5: Tier 2); objective
  for `pure_steal` + `double_extortion`; objective-read success.
- **impact** — terminal payload, no verb (§5: Tier 2); objective for
  `pure_impediment` + `double_extortion`; expressed structurally (absent from
  espionage nets) rather than as a zero duration.

### 3.4 Parameterisation (where the affordance register exposes a legitimate tunable)

Actions and parameters are both controller vocabulary. The scan-shaped and
exploit-shaped tactics can be invoked at a class-specific **tempo** via
`ATTACK_DURATION`, and the exploit-shaped tactics carry a **persistence** lever
via `ATTACKER_THRESHOLD` (anatomy §4.1). **Hard limitation:** every one of these
is *module-global* — set once, it applies uniformly across the run; per-tactic
invocation-time parameterisation is not expressible without a further carve
(anatomy §4.2, the wanted-but-absent register). So a per-tactic tempo profile is
a *specified intent* the map records, not a capability the current surface
delivers within one run. This is the honest ceiling the ch4 design constraint
and ch6 future work inherit.

---

## 4. The binary verdict per tactic (the M2/M4 oracle contract)

When the live net's token sits at an **action-bearing** tactic, the driver calls
the mapped verb via `step()` and reads the `_do_*` outcome as the M2 binary
verdict: **success → forward weight set live; failure → forward zeroed,
retry/backward live** (M2/M3). The verdict is defined per tactic below. For the
nine dwell-only tactics there is no oracle call — the token dwells and advances
on the base weights unconditioned (§3.3).

| Tactic | Success event (forward) | Failure event (retry/back) | Interrupt (MTD) |
|---|---|---|---|
| reconnaissance | `SCAN_HOST`/`SCAN_PORT` completes with a non-empty reachable/port set | empty set — nothing left to discover (`host_stack` empty) | `network`-layer mutation → back to `SCAN_HOST` (map lost) |
| initial-access | `EXPLOIT_VULN → EXPLOIT_COMPROMISED` (foothold on exposed host; Σ impact > 7) | `EXPLOIT_UNCOMPROMISED` (no vuln landed) | `EXPLOIT_HALTED` — `application`-layer mutation resets the working set |
| privilege-escalation | `EXPLOIT_VULN → EXPLOIT_COMPROMISED` (local exploit lands) | `EXPLOIT_UNCOMPROMISED` | `EXPLOIT_HALTED` |
| credential-access | `EXPLOIT_VULN → EXPLOIT_COMPROMISED` (dump) **or** `BRUTE_FORCE → True` (stuff) | both fail | `EXPLOIT_HALTED` on the exploit path; brute-force is uninterrupted |
| discovery | `SCAN_NEIGHBOR`/`SCAN_PORT` completes with a new reachable set | empty new set | `network` mutation → back to `SCAN_HOST` |
| lateral-movement | `EXPLOIT_VULN → EXPLOIT_COMPROMISED` (scan-hop) **or** `BRUTE_FORCE → True` (cred-hop) — new foothold | neither lands | `EXPLOIT_HALTED` on the scan-hop; the cred-hop survives (survivor modality) |

The interrupt column is read from the substrate's own reset model (anatomy §2.4;
primer §(e)): a `network`-layer mutation throws position-dependent tactics back
to host discovery; an `application`-layer mutation resets the surface-dependent
exploit working set on the same still-owned host; a credential/user mutation
raises no interrupt (the survivor modalities do not reset). MTD-interrupt
recovery for a *driven* run is still routed through the native `_handle_interrupt`
(anatomy §3 banner / `step()` scope note) — wiring it to the driver is the
feedback-net design's job, not this map's.

---

## 5. No double-counting, and the R2 hook

**The verdict is read, never re-rolled (M4).** For every action-bearing tactic
the success/failure event in §4 is the `_do_*` return of the substrate's own
mechanism — the per-vuln `random.random() < complexity` roll and the
`Σ impact > 7` threshold for the exploit verbs, `compromise_with_users`'s
credential-footprint roll for brute force, deterministic enumeration for the
scans (§2). The net supplies *movement* (which tactic, which direction); the
substrate supplies *outcome*. No new probability is layered on top of these,
which is the double-counting trap the retired operationalisation handoff flagged
— avoided by construction because the oracle *is* the substrate dice.

**Where R2 would act, if it arrives (hook, not design).** The R2 per-action
success-rate axis (register R2: "tuned higher in execution actions for APTs")
would attach as a **gate or scale on entry to the verb**, upstream of the native
roll — e.g. a per-class multiplier on the effective complexity for
`EXPLOIT_VULN`, or a Bernoulli gate deciding whether the driver attempts the verb
at all — and, for execution (the tactic R2 names), a declared success draw at the
otherwise dwell-only place (§3.3). This is named so the seam is known; it is
**not** designed here (R2 is post-first-numbers, an open handoff). The map and
the verdicts stand without it.

---

## 6. The M6 pre-intrusion synthetic join (applied 2026-07-21)

**The gap.** The corpus is blind to pre-intrusion tactics, so reconnaissance and
resource-development can be **detached islands** in the built nets. The situation
is profile-specific — confirmed by inspecting the shipped structural nets
(`data/ogasp/petri/*_structural.json`) and the existing prefix-gap probe
([`analysis.py`](../../../../src/mtdsim/l3_simulation/petri/analysis.py)
`_prefix_gap_probe`; `EXPECTED_RECON_REACHES_IA` in
[`tests/l3_simulation/test_petri.py`](../../../../tests/l3_simulation/test_petri.py)):

| Profile | recon → initial-access reachable? | resource-development connectivity |
|---|---|---|
| `aggregate` | **yes** — bridged by a real corpus edge | out-edges present (real flows) |
| `pure_steal` | **yes** — bridged by a real corpus edge | out to initial-access (real) |
| `pure_impediment` | **yes** — bridged | out to C2/execution, none to initial-access |
| `double_extortion` | **no — island** (recon has no out-edge) | fully detached (no in/out) |
| `infrastructure_setup` | **no — island** (recon has in-edges but no out) | fully detached |

M6 (register): connect the pre-intrusion tactics **manually** at the front —
recon enables initial access ("if you cannot recon anything, you can't gain
initial access") — defensible because nothing detects pre-intrusion activity.

**The applied curation — the overlay-object shape.** Marc's go-ahead
(2026-07-21) resolved the gate, and the application pass sharpened the seam in
one respect: rather than persisting `synthetic_transitions` inside regenerated
`*_structural.json` artefacts, the join ships as a **separate overlay artefact
composed at net construction** —
[`data/ogasp/petri/prefix_join_overlay.json`](../../../../data/ogasp/petri/prefix_join_overlay.json),
built by
[`petri/prefix_join.py`](../../../../src/mtdsim/l3_simulation/petri/prefix_join.py).
The observed structural JSONs are untouched (byte-identical — no regeneration),
which dissolves the review-gating cost the originally specified seam carried,
and separates CTI-derived structure from synthetic curation at the *artefact*
level, not just the field level.

- **Edges.** One synthetic `reconnaissance → initial-access` transition per
  profile where the observed net does not bridge the pair —
  `double_extortion` and `infrastructure_setup`; the guard leaves the three
  bridged profiles untouched (and catches any future class that regresses).
- **Guard rule (uniform across profiles).** A synthetic edge is added only
  where recon cannot reach initial-access over the observed net, and only out
  of a place with **no observed out-transitions**: an observed edge is never
  overwritten and observed weight distributions are never renormalised, so the
  D3 flow-proportion layer is never perturbed. A profile where recon had
  observed out-edges yet missed initial-access would *raise* — that shape needs
  a new declared decision, not a silently invented weight.
- **Weight treatment.** A synthetic edge has **no backing flow**, so the W-A
  regime (D3) does not apply; it carries a **declared manual weight of 1.0** as
  the sole out-transition of its source place (per-place out-weights still sum
  to 1). `weights.py` is unmodified — the declared weight lives on the
  synthetic spec and in the overlay artefact, never in the flow-proportion
  layer.
- **Provenance flag.** Every synthetic spec carries `synthetic: true` + the M6
  provenance string, so it is never mistaken for corpus structure
  ([`provenance.md`](../../provenance.md), M6 row).
- **The invariant is preserved, not broken.** The overlay lives in a
  `StructuralNet.synthetic_transitions` field, never folded into
  `transitions`; `test_no_synthesis_invariant` runs on the observed-only build
  with unchanged assertions, and a new test section pins the overlay (exact
  edges, weight 1.0, flags, composed reachability for all five profiles,
  artefact freshness) —
  [`tests/l3_simulation/test_petri.py`](../../../../tests/l3_simulation/test_petri.py)
  §7.
- **Composition.** `build_all_profiles` / `build_all` compose the overlay **by
  default** (`with_prefix_join=True`); observed-only is the explicit opt-out
  used by the artefact emitter and the invariant tests.
  `prefix_join.apply_prefix_join` is the single-net entry point the live
  feedback runner uses. Reachability (`analysis._place_adjacency`) unions the
  overlay, and the prefix-gap probe reports **"BRIDGED synthetically"** on
  composed island nets. **Overlay off + an `initial-access` seed remains the D8
  comparison arm** — the entry-point experiment becomes a toggle, not a second
  code path.

**The open judgement — resolved: (b), resource-development stays a documented
island.** The application pass surfaced a structural fact the specification
missed: the specified `resource-development → initial-access` edge alone would
have been **dead structure** — in both island profiles resource-development has
no in-edges and the single token seeds at `reconnaissance`, so a place nothing
flows into is never visited. Genuinely joining resource-development requires
the chain `reconnaissance → resource-development → initial-access`
(kill-chain-correct: recon = CKC reconnaissance, resource-development =
weaponisation) with a declared split at recon. Since resource-development is
off-clock (×0 dwell, no mapped action — §3.3), that chain adds a pass-through
place that changes no number, so option (b) is taken: recon-only join,
resource-development documented as an island in the overlay artefact. The chain
shape remains a small declared extension of `prefix_join.py` if later wanted.

---

## 7. The ledger

The revised ledger is [`../../../../data/ogasp/tactic_action_map.csv`](../../../../data/ogasp/tactic_action_map.csv)
— **long-form, one row per influenced (tactic, action) pair plus one explicit
dwell-only row per no-action tactic** (12 + 9 = 21 rows). Columns, decided by
this record:

`tactic, attack_tactic_id, action, influence, callability, context_required,
native_dice, success_event, failure_event, parameterisation, kill_chain_band,
profile_group, profile_ref, justification`.

**Relationship to the prior ledger.** The earlier
[`../../../../data/ogasp/timeline/tactic_action_map.csv`](../../../../data/ogasp/timeline/tactic_action_map.csv)
is the **per-tactic C2-binding** ledger of the *superseded* binding
investigation ([`binding_design_space.md`](binding_design_space.md), "DECIDED
OVER" banner) — one row per tactic, one `bound_action` each, C2 capability
columns. Its framing was decided over (M2/M4/M5); it is **not** renamed or
extended here. It is retained in place as that investigation's historical
artefact (still cited by [`binding_signoff_summary.md`](binding_signoff_summary.md)),
and this record's ledger is the differently-shaped M5 deliverable at the hoisted
path. Its rationale column was folded in as raw material and re-derived under
M5's "which tactics does each action influence" framing, not inherited.

---

## 8. What this establishes, where it connects, and when to update

This record turns "map the tactics onto the actions" into: a seam-level action
inventory with the native dice named (§2), a complete many-to-many influence
matrix with per-pair justification carrying the post-carve callability
constraint (§3), the M2/M4 binary verdict per tactic as the oracle contract the
feedback net consumes (§4), a no-double-counting statement with the R2 hook
located (§5), and the M6 pre-intrusion join **applied** as a separate composed
overlay (§6). Its practical output: the feedback-net design has its verdict
contract and a connected net to consume — `build_all_profiles()` returns the
composed nets, with the observed record and the D8 comparison arm one flag away.

**Validation-gate status** (handoff):
1. ✅ every action inventoried with state effect, pricing, native chance, readable outcome (§2).
2. ✅ all 15 tactics have a complete row set — mapped actions or explicit dwell-only, per-pair justification citing profile §5, defined binary verdict (§3, §4, ledger).
3. ✅ **applied (2026-07-21, Marc's go-ahead)** — M6 edges, weight, provenance flag regenerate through the build code as a separate composed overlay artefact; the observed `*_structural.json` are byte-untouched and the no-synthesis invariant is unchanged (§6).
4. ✅ no double-counting stated per tactic; R2 hook named not designed (§5).
5. ⏳ **awaiting Marc's review** of this map before the feedback-net design consumes it (the M6 go-ahead reviewed §6's shape; the M5 matrix and §4 verdicts remain to sign off).
6. ✅ no simulator behaviour changed — the M6 code touches the L3 net-build (`src/mtdsim/l3_simulation/petri/`), not `mtdnetwork/`.

- **Consumes:** [`action_layer_anatomy.md`](action_layer_anatomy.md) (inventory,
  callability, ATT&CK coverage); the 15 [`tactic_profiles/`](../../../notes/ch3_design/tactic_profiles/)
  §5 blocks; [`supervisor_decision_register.md`](supervisor_decision_register.md)
  §M1–M8, D3/D4, R2/R5.
- **Feeds:** the feedback-net design
  ([`../../../handoffs/2026-07-15_l3_feedback_net_design.md`](../../../handoffs/2026-07-15_l3_feedback_net_design.md))
  — the verdict contract (§4) and the M6 overlay (§6); the profiled-attacker
  build and first-numbers downstream of it.
- **When to update:** ~~if the M6 overlay is applied~~ — happened 2026-07-21
  (item 3 ✅; §6 records the as-applied overlay-object shape, and the island
  table still describes the *observed* nets, which the overlay leaves
  untouched); if the chain shape (recon → resource-development →
  initial-access) is ever wanted, §6's resolved judgement reopens; if R2 lands
  (§5 hook becomes a design); if the action layer's tail-calls or native dice
  change (§2/§4 re-walked — this is a code snapshot, dated in the frontmatter).
