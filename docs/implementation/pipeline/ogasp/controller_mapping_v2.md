---
status: durable
created: 2026-07-28
updated: 2026-07-28
topic: "L3 controller — mapping version 2, the experiment-2 partial map: each of the fifteen tactics decided on its merits against what the verb actually does, seven declared dwell-only, with the per-row reason and the two at-a-glance figures"
lineage: successor value to controller.md's version-1 map; executes step 1 of docs/handoffs/2026-07-27_controller_v2_partial_mapping.md (S4)
---

# Controller mapping version 2 — the experiment-2 partial map

**Status:** durable, **ratified by Marc 2026-07-28**, and **built** — the mapping
is selectable data that the controller layer reads. It is registered as
`v2_partial` in
[`../../../../data/ogasp/controller/mappings/`](../../../../data/ogasp/controller/mappings/),
loadable by name, and demonstrated end to end in a seeded run. It is **not the
default**, deliberately: see §4.

**Why a second version exists at all.** The controller is *the application layer
the experiments vary* — an input parameter, not a recovered truth
([`controller.md`](controller.md)). Supervisor ruling **S4** relaxed the property
version 1 was built to guarantee: a tactic maps to **[0, 1]** verbs, several
tactics may share a verb, and a tactic for which no verb's real effect is a
defensible stand-in becomes a **dwell-only** tactic that consumes simulated time
without dispatching anything. Version 1 stays registered and immutable so
experiment 1's numbers remain reproducible; this is a change of a parameter's
value, not the correction of a wrong one.

---

## 1. The construction — no mediating layer

Version 1 composed **transitively through the Cyber Kill Chain**: each verb owned
one CKC phase by Brown's Fig-3 flow position, each tactic took the verb of its own
or the nearest covered phase. Complete coverage fell out by construction, at the
price of six objective-band tactics all firing the same placeholder
neighbour-reveal.

Version 2 has **no mediating layer**. Each row was decided directly against what
the verb does and what it requires
([`attacker_phase_catalogue.md`](attacker_phase_catalogue.md)), and the reason is
recorded per row. Position in the kill chain decides nothing; where no verb's
effect fits, the answer is none. One consequence is worth stating up front: the
verb column and the substrate's own call order **no longer agree**, which is
visible in the figure as the verb column being ordered by the tactics it serves.

Row order below is the shipped lifecycle-consensus staging
([`lifecycle_consensus.md`](lifecycle_consensus.md);
[`../../../../data/ogasp/controller/lifecycle_consensus.json`](../../../../data/ogasp/controller/lifecycle_consensus.json)),
not the ATT&CK matrix order. Stage 2 asserts no internal order, so the tactics
inside it keep the `controller.csv` order.

## 2. The map (the 15 rows)

| Tactic | Stage | v1 | **v2** | Reason |
|---|---|---|---|---|
| reconnaissance | preparation | `SCAN_HOST` | `SCAN_HOST` | Builds the queue of attackable hosts from everything reachable from the current foothold — the substrate's only survey act. Unchanged. |
| resource-development | preparation | `ENUM_HOST` | **dwell-only** | Acquires infrastructure and capability off-target; MTDSim models no world outside the victim network. Also resolves a standing inconsistency: the synthetic overlay already treats this as a zero-dwell structural waypoint with no mapped action ([`synthetic_overlay.md`](synthetic_overlay.md) §2) while v1 dispatched `ENUM_HOST` from it. *A future action would need an out-of-network capability store gating which exploits are available later.* |
| initial-access | intrusion | `SCAN_PORT` | **`EXPLOIT_VULN`** | The most criticised cell in v1, where initial-access fired a port scan and could never take a foothold on its own merits. `EXPLOIT_VULN` is the only verb whose deliberate effect converts a host the attacker does not own into one it does, and ATT&CK's initial-access is dominated by exploiting a public-facing service. The credential-reuse hit inside `SCAN_PORT` is an incidental side effect of scanning, not a modelled access technique. |
| execution | intrusion | `EXPLOIT_VULN` | `EXPLOIT_VULN` | Applies a vulnerability's effect to a host's service — the substrate's only act of running something on a target. Unchanged. |
| persistence | post-intrusion | `BRUTE_FORCE` | **dwell-only** | Once compromised, a host stays compromised unconditionally: there is no access artefact to plant, lose, or maintain. v1 dispatched `BRUTE_FORCE` here on kill-chain position, which made persistence a second credential-guessing tactic. *A future action would need revocable per-host access that an MTD mutation can strip and the attacker re-assert.* |
| privilege-escalation | post-intrusion | `EXPLOIT_VULN` | `EXPLOIT_VULN` | The substrate has **no privilege dimension** — a host is compromised or not, with no user or administrator level. The stand-in is the exploit verb's accumulation of exploited impact toward the threshold at which a host falls: escalation of control, if not of privilege. Kept mapped because the verb's real effect is a defensible approximation; the missing privilege model is the caveat that rides with the row. |
| stealth (defense-evasion) | post-intrusion | `EXPLOIT_VULN` | **dwell-only** | Nothing observes the attacker, so there is no state evasion could alter and no verb whose effect is becoming less visible. v1's exploit dispatch was position, not effect, and made concealment indistinguishable from attack. This is the model's stealth gap (criterion axis 5) made explicit rather than papered over. |
| defense-impairment | post-intrusion | `EXPLOIT_VULN` | **dwell-only** | MTD scheduling is a defender-side process the attacker can neither observe nor touch, and no verb degrades a defensive component. *A future action would have to suppress or delay an MTD trigger — defender-side, and outside the freeze.* |
| credential-access | post-intrusion | `SCAN_NEIGHBOR` | **`BRUTE_FORCE`** | `BRUTE_FORCE` attempts a login against the current host from the pool of compromised usernames, which is ATT&CK T1110 with no interpretation required. The cleanest single row in the map. |
| discovery | post-intrusion | `SCAN_NEIGHBOR` | **`SCAN_PORT`** | Enumerates the open ports reachable on the current host — network service discovery (T1046). Two consequences named rather than hidden: the credential-reuse auto-compromise rides inside this verb, so discovery can occasionally compromise a host outright; and the verb populates `curr_ports`, which is what lets a later initial-access or execution run at all. |
| lateral-movement | post-intrusion | `SCAN_NEIGHBOR` | **`ENUM_HOST`** | Pops the next host, makes it current, and sets the pivot — the substrate's act of moving to a remote system. See §3. |
| command-and-control | post-intrusion | `SCAN_NEIGHBOR` | `SCAN_NEIGHBOR` | The one row where the inherited design states the mapping itself: Brown describes this verb as command and control revealing connected hosts. Unchanged, and now the sole tactic dispatching it rather than one of seven. |
| collection | objective | `SCAN_NEIGHBOR` | **dwell-only** | The substrate has no data — hosts carry services and vulnerabilities, nothing gatherable. *A future action needs modelled data at rest.* |
| exfiltration | objective | `SCAN_NEIGHBOR` | **dwell-only** | Neither half exists: nothing to take, nowhere to send it. v1's placeholder made the attacker's terminal act indistinguishable from its spreading act — precisely the uninterpretability S4 removes. |
| impact | objective | `SCAN_NEIGHBOR` | **dwell-only** | No verb destroys, encrypts, or denies anything. Declaring it dwell-only means an objective-band walk spends time at its objective instead of firing a spread verb that misrepresents what it is doing. |

**Shape of the result.** Eight tactics dispatch a verb; seven are dwell-only.
**All six verbs stay reachable**, and only `EXPLOIT_VULN` carries more than one
tactic (three). Eleven of fifteen rows change value from version 1, which spread
six verbs over all fifteen tactics with seven of them on the neighbour-reveal.

**No silent rows.** Every tactic above states mapped-to-verb or dwell-only with a
written reason, which is the relaxed invariant S4 asks for: silence stays an
error, declared absence becomes legal.

## 3. The two decisions that carry the most weight

**`lateral-movement` → `ENUM_HOST` is the deliberate answer to experiment 1's
churn.** The substrate spreads by revealing neighbours and *then* enumerating one;
version 1 routed seven tactics onto the neighbour-reveal and none onto the
enumeration, so the profiles fired the first without ever firing the second and
the attack never pivoted ([`experiment_01_findings.md`](experiment_01_findings.md)
Finding 1). Pairing `command-and-control` → `SCAN_NEIGHBOR` with
`lateral-movement` → `ENUM_HOST` lets that pair occur whenever a net routes
between those two tactics.

**The H-coupling is left visible, not mapped around.** Two of the new rows inherit
real preconditions: `EXPLOIT_VULN` needs `curr_ports`, so initial-access and
execution block unless a discovery step ran first; `ENUM_HOST` needs a non-empty
host stack, so lateral-movement blocks until reconnaissance or the
neighbour-reveal has run. Those are genuine dependencies of the substrate and
blocking on them is a result to report, not a defect to hide — a mapping that
routed around every unmet precondition would suppress the finding
([`runtime_verification.md`](runtime_verification.md) §P4).

## 4. How it is wired — the mapping as an input, not a layer

The reason this took a registry rather than an edited CSV: the experiment's
choice of mapping had been sitting *inside* the pipeline. `controller.csv` was
one file at one path, the loader read exactly that path, and a test asserted the
properties of that one mapping. Trying a different mapping therefore meant
editing the pipeline's data in place — which loses the old value, moves the
experiment that consumed it, and makes "which mapping produced these numbers"
unanswerable after the fact.

The seam now runs the other way. Every mapping tried is a **named version** in
[`../../../../data/ogasp/controller/mappings/`](../../../../data/ogasp/controller/mappings/)
— one file per version plus a manifest carrying each version's rationale, what it
produced, and which experiment consumed it — and the controller layer reads
whichever version it is handed:

```python
load_controller()                      # the manifest's default
load_controller(version="v2_partial")  # an explicit selection
run_movement(profile, mapping_version="v2_partial", ...)
```

**The default is version 1, and stays there.** Promoting the newest version to
default would re-bake an experiment's choice into the pipeline, which is the
coupling the registry exists to remove; it would also silently change what every
existing run, tool, and test reproduces. So an unqualified load still resolves
experiment 1's mapping, and experiment 2 names `v2_partial` at its own seam. This
is a deliberate deviation from the S4 handoff's gate item 6, which asked for the
controller record to describe version 2 as "the live value": there is no longer a
single live value, which is the better outcome. Both versions are live and
selectable; the experiment decides.

Two files hold version 1 —
[`../../../../data/ogasp/controller.csv`](../../../../data/ogasp/controller.csv),
retained because experiment 1's record cites it, and the registry's
`v1_ckc_total.csv`, which is where the loader now reads from. A test pins the two
equal row-for-row so neither can drift.

**Dwell-only at runtime.** `Controller.phase_for` returns `None` for a dwell-only
tactic, and the movement driver serves that place without dispatching: time
advances, no verb fires, no verdict is produced, and the token routes on the base
weights. The per-event record carries `place_class` (`action-bearing` /
`dwell-only`) with an empty verb and verdict, so an analysis can tell "spent time
thinking" from "did nothing" — without it the action-budget decomposition would
count every dwell-only step as a failed action. Two consequences are decided
rather than left implicit:

- **An MTD mutation during a dwell-only dwell is felt in cost, not in routing.**
  The substrate's interrupt price is paid and the interrupt is recorded, but no
  verdict is fabricated, because no verb ran and there is no substrate outcome to
  read. This is the scope boundary
  [`success_failure_overlay_design.md`](success_failure_overlay_design.md) §5
  already stated. Paying the price matters: the alternative makes dwell-only
  places cost-free under MTD, which would flatter the attacker for a reason that
  has nothing to do with its behaviour.
- **The adversary's `curr_process` reads as a `DWELL` sentinel** while the token
  sits on a dwell-only place, rather than keeping the last verb. The defender's
  application-layer interrupt gate reads that field, and a stale verb would have
  it judging something that finished steps ago. The sentinel is judged
  surface-dependent, which is the conservative reading — a dwell-only place is
  not a free hiding spot from MTD.

**The validation gate, discharged.** Every tactic states mapped-or-dwell-only
with a reason (§2); the registry holds two versions with provenance and switching
is a data selection; the relaxed invariant is test-pinned — a tactic resolving to
nothing *and* not declared dwell-only still raises at load; a dwell-only place is
demonstrated end to end in a seeded run; and determinism holds per version. The
tests are
[`../../../../tests/l3_simulation/test_controller.py`](../../../../tests/l3_simulation/test_controller.py)
(the registry and the invariant) and
[`../../../../tests/l3_simulation/test_controller_mapping_versions.py`](../../../../tests/l3_simulation/test_controller_mapping_versions.py)
(the end-to-end behaviour). Version 1 produces no dwell-only records at all, so
the new path is dormant under it and experiment 1's numbers are untouched.

**The figures**, regenerable by `data/misc/_viz/controller_mapping/controller_mapping_v2_viz.py`,
which reads both versions from the registry rather than restating them:

- `data/misc/_viz/controller_mapping/controller_mapping_v2.png` — the version-2 map in the same
  visual language as version 1's figure: verbs on the left, the fifteen tactics on
  the right banded by lifecycle stage with the reason per row, and dwell-only rows
  terminating in a "no verb" gutter rather than reaching the verb column.
- `data/misc/_viz/controller_mapping/controller_mapping_versions.png` — both versions side by side,
  which is the registry's comparability point made visible.

Both live in `data/misc/_viz/`, which is **gitignored** — as version 1's figure and
generator already are. They are regenerable from the script, and this record is the
tracked statement of what they draw. One palette slot was re-stepped for the new
figures (`BRUTE_FORCE` from `#c8102e` to `#d6336c`) because the version-1 hues
failed adjacent-pair deuteranopia separation against `EXPLOIT_VULN`; the other five
slots are unchanged.

**What this version has not yet done is run.** `consumed_by` is empty in the
manifest and `produced` reads "not yet run", which is why the version is still
marked mutable: it becomes immutable the moment an experiment consumes it. Two
things should be expected to change when experiment 2 runs against it, and
neither is a defect to fix in advance:

- **The dwell-only tactics change the action budget's denominator.** Seven of
  fifteen places now emit an event without an action, so events-per-run and
  actions-per-run are no longer the same quantity. Any per-action metric compared
  against experiment 1 has to say which it means.
- **Blocking will move, not vanish.** `EXPLOIT_VULN` on initial-access and
  `ENUM_HOST` on lateral-movement both carry real preconditions (§3), so the
  H-coupling should still be visible — in different places, and for better
  reasons, than under version 1.

## 5. Relationship to the rest of L3

- **Consumes:** [`attacker_phase_catalogue.md`](attacker_phase_catalogue.md) (what
  each verb does and requires — the input to every row);
  [`lifecycle_consensus.md`](lifecycle_consensus.md) (the stage ordering the map is
  presented in); [`experiment_01_findings.md`](experiment_01_findings.md) §3 (the
  two failure modes this version is trying not to reproduce).
- **Feeds:** the stochastic-timing design handoff, which needs the dwell-only
  tactic set as its input — that set is §2's seven rows; and experiment 2, which
  runs against this version.
- **Unchanged from version 1:** §4 of [`controller.md`](controller.md), the
  per-verb verdict semantics. The controller still owns only *which verb*; timing,
  outcome, and net routing are owned elsewhere.
- **Criterion impact:** none of the eight axes in
  [`../../apt_model_criterion.md`](../../apt_model_criterion.md) re-scores on a
  mapping change alone. Scores move on evidence, and the evidence is experiment 2.
