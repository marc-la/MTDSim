---
status: open
created: 2026-08-11
related: 2026-08-11_learning_scale_dependence.md
---

# Host the compound-exploit-learning mechanism on the native FSM attacker as a pre-registered positive-control arm — turning "structure blocks conversion" from a diagnosis into a demonstration

> **Sibling, not duplicate (2026-08-11).**
> [`2026-08-11_learning_scale_dependence.md`](2026-08-11_learning_scale_dependence.md)
> sweeps the *routing-belief* learner (axis 7's first mechanism) across host-count
> scale. This handoff takes the *compound-exploit* learner (the second, outcome-wired
> mechanism) and changes its **host attacker**, not its scale. Different learner,
> different question; read both to avoid conflation.

## State of play

The compound-exploit-learning experiment returned a **measured negative**
([`../implementation/pipeline/ogasp/exploit_learning_findings.md`](../implementation/pipeline/ogasp/exploit_learning_findings.md)):
the mechanism operates on the movement attacker (successful exploits rise with λ)
but moves no outcome, because breadth on this substrate is exploit-insensitive (a
*perfect* exploit adds ≈ 0 hosts), tempo-limited, and capped by the profiled
attacker's 89% re-compromise churn — the tactic→verb mapping running the inherited
FSM's phases out of dependency order. Axis 7 holds at DESIGNED, and Marc's
disposition is that the churn is a concession of the envelope, with the
fidelity-fights-the-FSM tension as the thesis-grade finding.

**That null is currently ambiguous between two readings, and nothing on record
discriminates them:**

- **Structural (the recorded diagnosis):** CTI tactic-ordering costs the attacker
  the FSM's operational competence, so no exploit-phase capability can convert to
  an outcome *on that host*. This is the finding the dissertation wants.
- **Deflationary (not yet excluded):** the mechanism is simply too feeble to move
  an outcome on *any* attacker — in which case "fidelity fights the FSM" degrades
  into an implementation apology. The perfect-exploit ceiling that grounds the
  structural reading was measured **on the movement attacker only** (the 6.2→6.0
  figures in findings §(a) are movement-attacker breadth); the native FSM's
  sensitivity to exploit capability has never been measured.

**The positive control that discriminates them:** the same mechanism, same
substrate, hosted on the attacker whose action ordering permits conversion — the
native 6-phase FSM (41/50 breadth, 0% churn, terminates; findings §(c)). If
learning converts to a progress measure there, the structural reading is
*demonstrated*, not asserted: the movement null becomes a controlled result about
what CTI ordering costs. If it converts nowhere, the deflationary reading is
confirmed — also informative, and reported just as plainly.

**The build is small, because the wiring already exists.** The consult-and-bank
sits at the single roll site in `_do_exploit_vuln`
([`attack_operation.py:557-560`](../../mtdnetwork/operation/attack_operation.py#L557-L560)),
which is reached by **all three** exploit paths — native FSM included
([`exploit_learning.md`](../implementation/pipeline/ogasp/exploit_learning.md) §(b)).
The memory and default-off flag live on `Adversary`. What is missing is only an
**enable path on a native-FSM vehicle**: `run_movement` has
`exploit_learning_rate` ([`run.py:357-364`](../../src/mtdsim/l3_simulation/movement/run.py#L357-L364));
no native runner calls `enable_exploit_learning`. First task is verifying the
native path truly reaches the consult (safety property 2's byte-identity argument
implies it does, passing `success_prob=None` while disabled).

**Framing, dispositioned by Marc (2026-08-11).** The arm is a **measurement
instrument** — "the FSM-hosted control arm" — kept permanently in the record as a
control within one experiment, exactly like the λ = 0 ablation and the
perfect-exploit ceiling arms. It is **never** a named attacker: no "smart
attacker" naming anywhere in code, docs, or prose, no persistent third attacker in
the model's public shape. Axis 7's badge cannot move on this evidence in either
direction — the badge scores the movement model, not the substrate baseline.

## Recommended approach

**Step 0 — the kill-cheap ceiling pilot, before any build or pre-registration.**
Run the native FSM (the substrate tracer's `--scheme none` configuration, driven
programmatically) with the perfect-exploit ceiling — a forced `success_prob = 1.0`
at the roll; reconstruct the override the findings used for the movement-attacker
ceiling if it was scratch, and keep it as a declared pilot instrument. No MTD,
~5 seeds, horizon 15 000 to match findings §(c). Measure compromise breadth,
time-to-termination, and attempts-per-compromise against the unmodified native
run. Commit the expectation first: breadth is near-saturated (41/50), so
tempo/attempts are where any headroom lives. **Gate:** if nothing moves outside
seed noise, no exploit-success mechanism can demonstrate on this host either — the
deflationary reading is not excludable by this route. Commit the pilot record,
retire this handoff by evidence, and report; do not proceed to a build that cannot
show anything.

1. **The enable knob.** Thread an `exploit_learning_rate` parameter through the
   native-run vehicle used in step 0, mirroring the movement hook (`None` leaves
   the adversary untouched). Default-off byte-identity must hold with zero test
   churn: full suite green, golden streams and the ATK-04 exact-integer pins
   untouched, no golden re-baselined.
2. **Pre-register before any swept output exists.** Reuse the committed values —
   the λ band and pool sizes from
   [`exploit_learning_prereg.md`](../implementation/pipeline/ogasp/exploit_learning_prereg.md),
   fixed seeds. No new value may be introduced, and none because it improves an
   outcome. Primary measures: **attempts-per-compromise and time-to-termination**;
   breadth is reported but predicted flat (saturation). Commit the confirmatory
   prediction (learning improves the progress measures monotonically in λ against
   the λ = 0 ablation arm on the FSM host) and the null branch (flat in λ ⇒ the
   mechanism-limited reading is confirmed) before running.
   - **Time-denominated comparison is admissible here and the pre-registration
     must say why:** both arms are the same attacker family under identical
     pricing. S3-R's asymmetry binds *cross-family* (movement vs native)
     comparisons, which remain forbidden.
3. **The sweep.** Native FSM, λ = 0 ablation vs the λ band, constrained pool via
   the already-threaded `services_per_os` knob, no MTD. Extend
   [`tools/exploit_learning_sweep.py`](../../tools/exploit_learning_sweep.py) with
   a host-attacker dimension rather than writing a new script.
4. **Report and amend.** A findings record beside `exploit_learning_findings.md`
   (or a new section in it) carrying one committed verdict sentence: which reading
   of the movement-attacker null the control arm excludes. Findings §(d)'s "it
   would have to be shown on an attacker that can realise it" is the sentence this
   work executes — cite it. Delete this handoff in the shipping commit.

**Alternatives considered.** (i) *Ceiling-row-only* — skip the mechanism, report
just the step-0 ceiling as the bound. Cheaper, but it only bounds; Marc's ask is
the mechanism itself, and the enable knob is small because the wiring exists. Keep
this as the fallback if the enable path turns out larger than it looks. (ii)
*Instrument the movement attacker's re-encounter effort instead* (attempts-to-success
on familiar types falling with λ) — complementary, honest, and cheaper, but it
demonstrates per-action improvement without outcome conversion, so it cannot
discriminate the two readings. It pairs with this work; it does not replace it.

## Validation gate

Done when the following exist **in commit order**:

1. The step-0 pilot result, committed, with go/no-go called against the
   pre-committed expectation.
2. If go: the pre-registration, committed before any sweep output exists.
3. The sweep and analysis, committed, with a single verdict sentence naming which
   reading of the movement-attacker null is excluded — or that the
   mechanism-limited reading is confirmed.
4. Default-off byte-identity intact: full suite green, goldens and ATK-04 pins
   untouched, the four safety properties in `exploit_learning.md` §(e) still
   holding.
5. `grep -ri "smart attacker"` over the diff returns nothing.

A null result passes this gate. A positive produced by tuning any value does not.

## Hard constraints

- **Instrument, not product.** No new named attacker class; no performance ranking
  of movement vs native attacker anywhere. The only licensed cross-attacker
  sentence is the structural diagnosis (same mechanism converts on the FSM host,
  cannot on the CTI-ordered host, therefore the ordering is the cause).
- **Axis 7's badge does not move on this evidence**, in either direction; any
  badge change is Marc's adjudication, separately, against the criterion.
- **No value chosen because it improves an outcome.** λ band, pools, seeds are the
  shipped pre-registration's. The mechanism's compounding form (`exploit_learning.md`
  §(c)) is frozen as shipped — no reshaping to flatter the new host.
- **No time-denominated cross-family comparison** (S3-R); within-family is
  admissible with the justification recorded in the pre-registration.
- **Determinism / SIM-05**; default-off and λ = 0 bit-identity; no ATK-04
  restoration — learning stays success-roll-shaped, never exploit-time-shaped.
- **No MTD-crossed cells** — no-MTD isolates the host × learning interaction.
- Branch / commit / push rules from
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md); never push.
- Australian English.

## Reading list

- [`../implementation/pipeline/ogasp/exploit_learning.md`](../implementation/pipeline/ogasp/exploit_learning.md)
  — §(b) the single roll site and the all-three-paths claim this build leans on;
  §(e) the four safety properties that must keep holding; §(f) the 0.77-complexity
  headroom caveat, which binds on this host too.
- [`../implementation/pipeline/ogasp/exploit_learning_findings.md`](../implementation/pipeline/ogasp/exploit_learning_findings.md)
  — §(c) the stark comparison (native 41/50, 0% churn: this handoff's host); §(d)
  the "attacker that can realise it" sentence this executes, and the ruled-out
  disingenuous moves.
- [`../implementation/pipeline/ogasp/exploit_learning_prereg.md`](../implementation/pipeline/ogasp/exploit_learning_prereg.md)
  — the committed λ band, pools, and seeds to reuse.
- [`mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  lines 485–560 — `_do_exploit_vuln` and the consult-and-bank; confirm the native
  path reaches it.
- [`../implementation/trace_tool.md`](../implementation/trace_tool.md) — the
  substrate tracer (`--scheme none`) as the native-run instrument for the pilot.

## Out of scope (explicitly)

- Any change to the movement attacker; the credit-assignment redesign; any
  FSM-succession revival.
- The routing-belief learner and the scale-dependence sweep (the sibling handoff).
- MTD-crossed cells, cross-run memory, defender observation.
- Re-grading axis 7; dissertation prose.

## Return format

The default thesis-framed return, plus, explicitly: **which of the two readings of
the exploit-learning null the control arm excludes**, and the one sentence now
sayable in the evaluation chapter about the measured negative ("demonstrated
structural cost of CTI ordering" vs "mechanism-limited null"). Point at the
committed records for everything else.
