---
status: open
created: 2026-08-13
related: 2026-08-11_fsm_hosted_learning_control_arm.md
---

# Instrument *where* the compound-exploit learner's bought successes land on the movement attacker — a within-run, within-arm ledger that shows the mechanism operating and locates why it converts no outcome, without ever comparing two attackers

> **Sibling of the FSM-hosted control arm
> ([`2026-08-11_fsm_hosted_learning_control_arm.md`](2026-08-11_fsm_hosted_learning_control_arm.md)).**
> That handoff discriminates the exploit-learning null by *changing the host*
> (movement → native FSM) and pays for a cross-attacker counterfactual. This one
> stays **entirely on the movement attacker** and changes only *what is measured*:
> it shows the learner operationalising and shows, event by event, where its
> bought successes go. The two are sequenced, not alternatives — see
> § Relationship to the FSM arm. Read both to avoid conflating them.

## State of play

The compound-exploit learner returned a **measured negative** on the movement
attacker ([`../implementation/pipeline/ogasp/exploit_learning_findings.md`](../implementation/pipeline/ogasp/exploit_learning_findings.md)):
the mechanism operates (successful exploits rise monotonically with λ; the
constrained pool drives cross-host re-encounters as designed) but moves no
outcome. The findings already carry the *aggregate* reasons — breadth is
exploit-insensitive (a perfect exploit adds ≈ 0 hosts, §(a)1), tempo-limited
(§(a)2), and capped by the profiled attacker's **89 % re-compromise churn**
(§(a)3) from the tactic→verb mapping running the inherited FSM's phases out of
dependency order (§(c)). Axis 7 holds at DESIGNED; Marc's disposition is that the
churn is a concession of the envelope, with fidelity-fights-the-FSM as the
thesis-grade finding.

**What is not yet on record is the mechanism-level *demonstration* of that
absorption on the movement attacker itself.** The findings infer it from
run-total aggregates (a perfect-exploit ceiling; a 24/27 re-compromise count at
one seed). Nothing shows, per learning-bought success, *what that success
yielded* — a fresh host or a host already owned — resolved across the swept λ
band. That per-event picture is the exhibit this handoff builds, and it is the
strongest honest thing the movement attacker alone can say about its own learner.

**Why this matters for the write-up, in Marc's own framing (2026-08-13).** The
FSM control arm carries a framing hazard: reported carelessly it reads as *we had
to demonstrate on the old attacker because ours is worse*, which invites a ranking
of the two attackers the model is not allowed to make. A movement-only exhibit
sidesteps that line entirely — it never mentions a second attacker. It shows the
capability working **on the model's own attacker** and locates the null's cause
**on that same attacker**, so the sentence the chapter needs ("the learner
operationalises; the substrate absorbs its gains into churn") is made without a
cross-attacker comparison at all. This is the primary exhibit; the FSM arm becomes
the backup that answers a *narrower* residual question (see below).

## The instrument — one ledger, plainly

**Name it in prose, not as a noun-stack.** The thing being built is *a ledger of
what each learning-bought exploit yields*. Call it the **yield ledger** as a short
handle and describe it as a sentence wherever it appears; do **not** write
"marginal success yield ledger" or any four-noun pile-up into the record or the
chapter (Marc, 2026-08-13).

**What it records.** The learner works by consulting a boosted success threshold
at the single roll site and banking a prior-success on a fresh `False→True`
transition ([`../implementation/pipeline/ogasp/exploit_learning.md`](../implementation/pipeline/ogasp/exploit_learning.md)
§(b); the consult-and-bank is
[`attack_operation.py:555-560`](../../mtdnetwork/operation/attack_operation.py#L555-L560)).
At exactly that site the two probabilities the attribution needs are already in
hand: the **base** threshold `c = vuln.complexity` and the **boosted** threshold
`p_eff` returned by `adversary.effective_exploit_prob(vuln)`
([`adversary.py:184-214`](../../mtdnetwork/component/adversary.py#L184-L214)). For
every roll where the boost is active (`p_eff` not `None`, i.e. `p_eff > c`), log:
`c`, `p_eff`, whether the roll succeeded (`vuln.is_exploited()` after the call),
and — the yield classification — **whether `curr_host` was already compromised at
the moment of the roll** (`adversary.get_curr_host().check_compromised()` read
*before* the roll, or equivalently host membership in the compromised set).

**Attribution by probability mass, not by captured draw — this is the
determinism-safe core.** Do not try to capture the RNG draw; that would touch the
roll and risk SIM-05. Instead attribute at the level of expectation. A roll that
succeeded under the boost drew `u < p_eff`; that same `u` would also have
succeeded at base iff `u < c`. So, conditional on a boosted success, the
probability it was *bought by learning* (would have failed at base) is
`1 − c / p_eff`. Summing `(1 − c / p_eff)` over all successful boosted rolls in a
run gives the **expected number of learning-attributable successes**, computed
from quantities already at the consult site, consuming **no RNG** and changing
**no control flow** — byte-identity and the four safety properties
([`exploit_learning.md`](../implementation/pipeline/ogasp/exploit_learning.md)
§(e)) are untouched by construction, because the ledger only *reads*. Split that
attributable mass by the yield flag into a **fresh-host** bucket and a
**re-compromise** bucket.

*(Exact per-event attribution — success iff the draw falls in the window
`(c, p_eff]` — is available as an alternative only if `Vulnerability.network` is
made to report its draw. It is strictly more code at the roll site for a sharper
but not different story; the mass method is the recommendation precisely because
it needs no roll-site change. Note either way that this is event-level
attribution, not a trajectory counterfactual: after the first bought success the
run's state diverges from what λ = 0 would have produced, so the ledger says
"these successes the boost bought, and here is what each yielded", while the
**λ = 0 ablation arm remains the trajectory-level comparator". State both.)*

**A companion read that costs almost nothing: the targeting denominator.** From
the same event stream, the fraction of exploit attempts aimed at an
already-compromised host, resolved by λ. This is the run-total the findings quote
at one seed (24/27) turned into a swept curve. It carries the one-sentence causal
story: **learning improves the shot; the tactic ordering picks the target.**
Include it — it is the mechanism behind whatever the yield ledger shows.

## Recommended approach

1. **Extend the movement tracer / sweep collector, do not write a new script.**
   The yield fields attach at the consult site; the sweep already runs the cells
   and reads `adversary._exploit_type_counts`
   ([`tools/exploit_learning_sweep.py`](../../tools/exploit_learning_sweep.py)
   `one_cell`, lines 63-90). Add the per-run aggregates — attributable mass,
   fresh-host bucket, re-compromise bucket, attempts-on-owned-host fraction — as
   new columns on the same cell dict. The prereg's §(i) tracer-extension task
   (surface `n(id)` / `p_eff` at the roll site) is the natural home; fold the
   ledger into it rather than beside it. Living tools get extended, not cloned
   ([`../implementation/trace_tool.md`](../implementation/trace_tool.md)).

2. **Pre-register before any swept output exists**, reusing the committed regime —
   λ band, pools, seeds, `aggregate`, `v2_partial`, horizon 15 000 — verbatim from
   [`../implementation/pipeline/ogasp/exploit_learning_prereg.md`](../implementation/pipeline/ogasp/exploit_learning_prereg.md).
   **No new value, and none because it improves an outcome.** Commit two predictions:
   - **Structural (confirmatory):** the learning-attributable mass concentrates
     overwhelmingly in the **re-compromise** bucket, and the **fresh-host**
     attributable count is **flat in λ** (breadth is exploit-insensitive, so the
     bought successes cannot be landing on new hosts). The targeting denominator is
     **invariant in λ** (learning changes success-given-a-target, never which
     target the ordering selects).
   - **Null branch (committed, not feared):** if attributable mass lands on fresh
     hosts *yet breadth stays flat*, that is a **different and more interesting
     absorption channel** than churn — report it plainly; it would mean fresh
     compromises are being undone downstream rather than never made. Finding it is
     the honest point of instrumenting per-event rather than trusting the aggregate.

3. **Run within the already-executed grid.** The λ sweep, pool sweep and
   ablation arm already exist in the prereg; this adds columns, not cells. If the
   generated outputs from the shipped sweep are still on disk under `data/ogasp/`
   (gitignored), a re-run at the same seeds reproduces them bit-for-bit and the
   ledger columns come for free; otherwise re-run the committed cells.

4. **Report and amend.** A findings section beside
   [`exploit_learning_findings.md`](../implementation/pipeline/ogasp/exploit_learning_findings.md)
   (or a new sibling record) carrying one committed verdict: *the movement
   attacker's learner operationalises and its bought successes are absorbed into
   `<bucket>`*. This executes §(d)'s "the mechanism's real axis is effort / RoA,
   not breadth" sentence at event granularity. Delete this handoff in the shipping
   commit.

**Alternatives considered.** (i) *Re-encounter effort curve* — attempts-to-success
on familiar types falling with λ (the FSM-arm handoff's alternative ii). Honest and
cheap, but it demonstrates per-action improvement without saying where the
successes *go*, so it cannot show the absorption; the yield ledger subsumes it.
Keep it only as a secondary panel if a per-action improvement figure is wanted.
(ii) *Exact draw-window attribution* — sharper per-event, but needs a roll-site
change; declined for the mass method above unless the draw is exposed for another
reason. (iii) *Skip straight to the FSM arm* — that pays for a cross-attacker
counterfactual to answer a question this on-host exhibit largely retires; do this
first (see below).

## What the package licenses, and what it does not

**Sayable after this ships (movement attacker only, no second attacker named):**
the compound-exploit learner **operationalises** on the movement attacker, and its
learning-attributable successes are delivered **almost entirely to hosts already
compromised** because the CTI tactic ordering selects targets independently of
exploit capability — so no exploit-success mechanism, of any strength (the
perfect-exploit ceiling, §(a)1, is the magnitude bound), could convert to breadth
on this host. That is a **located, demonstrated structural absorption**, not an
apology and not a comparison.

**Not sayable, and this is the residual the FSM arm still owns:** the *global*
deflationary form — "perhaps no attacker on this substrate converts exploit
capability to outcomes". The yield ledger shows the gains are absorbed *here*; it
cannot show a differently-ordered attacker would convert them. The examiner
exposure shrinks from "you demonstrated on the old attacker because yours is worse"
to "might the substrate be exploit-insensitive for everyone?" — a *question*, not a
weakness, and exactly what the FSM control arm tests if it is ever wanted.

## Relationship to the FSM arm — sequencing

Build this **first**. It is strictly safe: it touches only the movement path, adds
no knob to any attacker, and its exhibit stands whether or not the FSM arm is ever
built. If the FSM arm's step-0 ceiling pilot fails its gate (no headroom even at a
perfect exploit on the native FSM,
[`2026-08-11_fsm_hosted_learning_control_arm.md`](2026-08-11_fsm_hosted_learning_control_arm.md)
step 0), the FSM arm retires by evidence and this ledger is the *only* exhibit
anyone could have built — so building it first spends no effort that a failed FSM
pilot would waste. The FSM arm then remains available as the **backup discriminator**
for the narrower global-deflationary residual, framed permanently as a measurement
instrument, never a named attacker.

Note also the **movement-objectives handoff**
([`2026-08-11_movement_objectives.md`](2026-08-11_movement_objectives.md)) *cures*
the churn this ledger *measures*: this instrument quantifies the terrain that the
objective layer would change. They are complementary and should cite each other;
this ledger is a measurement of the current envelope, not a competitor to the fix.

## Validation gate

Done when the following exist **in commit order**:

1. The pre-registration, committed **before any ledger output exists**, carrying
   the structural prediction and the committed null branch, reusing the shipped
   λ band / pools / seeds with no new value.
2. The ledger columns on the sweep collector, with a proof that they are
   **read-only**: full suite green, the movement goldens and the ATK-04
   exact-integer pins untouched, no golden re-baselined, the four safety
   properties in `exploit_learning.md` §(e) still holding. (The mass method
   consumes no RNG and changes no control flow — this should be zero test churn.)
3. The findings record, committed, with **one verdict sentence** naming which
   bucket the learning-attributable successes concentrate in, and the targeting
   denominator's λ-dependence.
4. `grep -ri "smart attacker\|better attacker"` over the diff returns nothing, and
   no sentence ranks the movement attacker against the native FSM.

A null result (attributable mass on fresh hosts, or a moving denominator) **passes
this gate** — it is a finding. A result produced by changing any committed value
does not.

**The qualification the validation must carry, stated as Marc framed it
(2026-08-13):** the **mechanism is measured** — it operationalises, and the ledger
shows it — but the **outcome in the simulator is not clear-cut**, because three
measured mitigating factors sit between the mechanism and any breadth gain:
- **X — breadth is exploit-insensitive:** a perfect exploit adds ≈ 0 hosts at every
  horizon (the ceiling, findings §(a)1), so no exploit-success capability can move
  breadth regardless of strength;
- **Y — breadth is tempo-limited, not capped:** it scales with runtime, so a longer
  run gives bigger numbers and the identical learning gap (findings §(a)2);
- **Z — the profiled attacker re-compromises hosts it already owns 89 % of the
  time**, because the CTI tactic→verb mapping runs the inherited FSM's phases out
  of dependency order (findings §(a)3, §(c)).
The write-up states the measured mechanism operation and the qualified outcome
together; it never reports the operation as a breadth or ASR gain.

## Hard constraints

- **Instrument, not product.** No new named attacker; no "smart attacker" / "better
  attacker" anywhere; no performance ranking of the movement attacker against the
  native FSM. The exhibit is *mechanism × terrain*, on one attacker.
- **Axis 7's badge does not move on this evidence**, in either direction. Any badge
  change is Marc's adjudication, separately, against the criterion.
- **No value chosen because it improves an outcome.** λ band, pools, seeds are the
  shipped pre-registration's. The mechanism's compounding form
  ([`exploit_learning.md`](../implementation/pipeline/ogasp/exploit_learning.md)
  §(c)) is frozen as shipped.
- **Read-only instrumentation.** No RNG consumed at or around the roll; no control
  flow changed; determinism / SIM-05 and default-off / λ = 0 bit-identity intact;
  no ATK-04 restoration.
- **Within-arm / within-family only.** No time-denominated comparison that crosses
  the movement/native pricing asymmetry (S3-R); the whole exhibit is on the
  movement arm, so the asymmetry does not arise, and no sentence may reach across
  it. Attribution is in success counts (mass), not seconds.
- **No MTD-crossed claims beyond the prereg's Dimension 3 as already committed** —
  the ledger reports within the existing grid; it does not open new cells.
- Branch / commit / push rules from
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md); never push.
- Australian English.

## Reading list

- [`../implementation/pipeline/ogasp/exploit_learning_findings.md`](../implementation/pipeline/ogasp/exploit_learning_findings.md)
  — §(a) the three absorbers (X/Y/Z above); §(c) the churn diagnosis; §(d) the
  "real axis is effort / RoA, not breadth" sentence this executes at event level.
- [`../implementation/pipeline/ogasp/exploit_learning.md`](../implementation/pipeline/ogasp/exploit_learning.md)
  — §(b) the consult-and-bank roll site the ledger reads; §(e) the four safety
  properties that must keep holding; §(f) the RoA-first headroom caveat, which
  bounds how much mass any boosted roll can carry.
- [`../implementation/pipeline/ogasp/exploit_learning_prereg.md`](../implementation/pipeline/ogasp/exploit_learning_prereg.md)
  — the committed λ band, pools, seeds, and §(i) the tracer-extension task to fold
  the ledger into.
- [`mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  lines 549-560 — the consult-and-bank; the yield read attaches here.
- [`mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py)
  lines 184-214 — `effective_exploit_prob`; source of `c` and `p_eff` for the
  attribution.
- [`2026-08-11_fsm_hosted_learning_control_arm.md`](2026-08-11_fsm_hosted_learning_control_arm.md)
  — the sibling; read its § State of play and its step-0 gate for the sequencing.

## Out of scope (explicitly)

- Any change to the movement attacker or its mechanism; the credit-assignment
  redesign; any FSM-succession revival; the movement-objectives churn *fix* (this
  measures the terrain the fix would change — it does not build it).
- The FSM-hosted control arm (the sibling handoff owns it).
- The routing-belief learner and the scale-dependence sweep (a separate handoff).
- Capturing the RNG draw for exact attribution unless independently warranted.
- Re-grading axis 7; dissertation prose.

## Return format

The default thesis-framed return, plus explicitly: **which bucket the
learning-attributable successes concentrate in** (re-compromise vs fresh-host), the
**λ-dependence of the targeting denominator**, and the one sentence now sayable in
the evaluation chapter — the movement attacker's learner *operationalises and is
structurally absorbed on its own terrain*, stated with the X/Y/Z qualification and
without any second attacker in view. Point at the committed records for the detail.
