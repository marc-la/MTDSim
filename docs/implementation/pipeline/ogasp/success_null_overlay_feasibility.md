---
status: durable
created: 2026-08-19
updated: 2026-08-19
topic: "Feasibility of collapsing the outcome overlay to a failure-only matrix (success = pass-through on the base flow proportions): the premise made precise, the static test of what the success column does to the base, the rule-generated success-null variant, a three-arm paired dry run on the experiment-2 grid, the evidence-tier inversion weighed, the blast radius priced, and the ruling slot"
---

# The failure-only overlay — is the success column doing work the corpus does not already do?

**Status:** durable. Executes
`docs/handoffs/2026-08-19_failure_only_overlay_feasibility.md` (deleted in the
commit that ships this record). **This is feasibility and evidence, not
adoption**: §8 carries the ruling slot, and nothing keyed on
`v3_persistent_backward` is touched until Marc rules.

**The premise, in Marc's words** (L4 pass 4 dictation, 2026-08-19, now in
§4.2.4 of the tex): "*failure is not something that is just encoded: the CTI
that we're using naturally encodes success, because these are well-known
successful incidents that have resulted in impact and were worth writing about,
so the failures are not encoded, and that is what we're trying to encode
here.*" The consequence he drew from it in the same pass: one declared matrix
— the failure matrix — is more defendable than two, so the success table should
go, and a success verdict should route on the base flow proportions unchanged.

**The counter-argument the handoff told this record to weigh honestly:** the
design record's evidence-tier asymmetry runs the other way
([`success_failure_overlay_design.md`](success_failure_overlay_design.md) §4):
the *success* table is the better-attested half (MITRE `enables` semantics and
the DFIR get-in/spread patterns) and the failure table the declared-judgement
half. A failure-only overlay keeps the declared half and drops the attested
one. Both the defensibility gain and this inversion are in the verdict (§7).

**Reproduce.** Workspace `data/results/success_null_feasibility/` (gitignored
by design — regenerable). Three scripts: `static_analysis.py` (§2),
`run_grid.py` (§4–§5; 2 400 + 1 600 runs, ~75 min at 7 workers), `kernel_only.py` (§5.8), `analyse.py`
(`numbers/`). The variant itself is compiled by the tracked generator (§3).

```
PYTHONPATH=src python data/results/success_null_feasibility/static_analysis.py
PYTHONPATH=src python data/results/success_null_feasibility/run_grid.py --workers 7
PYTHONPATH=src python data/results/success_null_feasibility/analyse.py
```

---

## 1. The premise made precise — three layers, not two

The outcome-conditioned walk composes three things at a routing decision:

| layer | what it is | where it comes from | tier |
|---|---|---|---|
| **base** `base(a→b)` | the D3 out-edge-normalised flow proportion | the Attack Flow corpus — sequences of techniques that *worked* | corpus-grounded |
| **success column** `overlay_success(a→b)` | a per-pair factor in [0, 1] multiplied onto the base on a success verdict | 5 rules: `enabled` 1.0 (MITRE semantics + AAR get-in/spread), `forward` 0.6, `lateral` 0.5, `backward` 0.25, `backward_to_prep` 0.1, × the distance kernel | 1 rule attested-pattern, 4 declared-judgement |
| **failure column** `overlay_failure(a→b)` | the same, on a failure verdict | 9 rules: two foothold gates and a recon gate (attested-pattern/declared-magnitude), two dampers and the relationship ladder (declared-judgement), × the distance kernel | 3 rules attested-pattern/declared-magnitude, 6 declared-judgement |

Marc's premise is a claim about the first two rows: the base *is already* the
success-conditioned routing, because the corpus it is taken from is a
survivorship sample of successful campaigns. On that reading the success column
is a **second encoding of the same thing** — a declared re-weighting laid over
an attested one — and the failure column is the *only* layer encoding anything
the corpus cannot. That is exactly the genesis epistemics of the overlay thread
(research record #28, 2026-07-21: "we know a lot about successful patterns as
that's what the campaigns/incident reports tell us, but not a lot about the
failure components"), and the design record itself half-says it
([`success_failure_overlay_design.md`](success_failure_overlay_design.md) §2.2:
"the base weights already encode success-biased observed workflow, and the
`enables` boost sharpens the specific next-steps the AARs attest"). What is new
is the inference that the sharpening is therefore redundant rather than merely
better-grounded.

So the question is not "is the success column well-grounded?" (it is, relative
to the failure column) but "**does it do work the base does not already
do?**" — statically (does it change the distribution?) and behaviourally (does
that change reach any measured outcome?). §2 answers the first, §5 the second.

**The evidence-tier inversion, re-read under the premise.** Per the ledger
([`../../declared_value_provenance.md`](../../declared_value_provenance.md);
`outcome_rules.json`), the success table is attested-pattern on 69 of 210 cells
(the `enabled` tier) and declared-judgement on 141; the failure table is
attested-pattern/declared-magnitude on 25 cells (the three gates) and
declared-judgement on 185. On the 115 pairs that actually carry base mass in
some profile net the split is 57 attested / 58 declared for success and 12 /
103 for failure. Two things follow. (i) The handoff's counter-argument is
right as stated: dropping the success column drops the better-attested table.
(ii) But half of what it drops on the routed pairs is declared-judgement
anyway (the 0.6 / 0.5 / 0.25 / 0.1 ladder), and the attested half — the
`enables` relations — is attested *by the same kind of source the base is
built from* (incident reports of what worked next). Under the premise, the
`enables` tier is not independent evidence the base lacks; it is the same
survivorship evidence, re-declared as a coarse 1.0-or-less factor on top of
proportions the corpus already measured. What the failure-only overlay keeps
is the one layer no corpus could supply. The inversion is therefore real at
the level of tiers and dissolves at the level of *what the tiers are evidence
of*: both concessions stay on the page, and the verdict (§7) states them in
that order.

---

## 2. The static test — the success column is not a pass-through

If the base already encoded success routing, `compose(success)` would be close
to the renormalised base at every place. It is not. Under `v2_partial` eight
tactics hold a verdict; at those places, over the five profile nets
(synthetic overlay on), the total-variation distance between the
success-conditioned out-distribution and the base out-distribution is:

| profile | verdict-bearing multi-out places | mean TV(success, base) | mean TV(failure, base) | mean TV(success, failure) | places with TV(success, base) < 0.05 |
|---|--:|--:|--:|--:|--:|
| `aggregate` | 8 | 0.199 | 0.253 | 0.202 | 0 / 8 |
| `objective_exfiltration` | 8 | 0.144 | 0.192 | 0.196 | 1 / 8 |
| `objective_impact` | 6 | 0.146 | 0.118 | 0.085 | 1 / 6 |
| `objective_exfiltration_impact` | 6 | 0.128 | 0.230 | 0.219 | 2 / 6 |
| `objective_none_c2` | 6 | 0.175 | 0.212 | 0.254 | 0 / 6 |

So the success column moves 13–20 % of the out-mass at a typical
verdict-bearing place — the same order as the failure column does everywhere
except `initial-access`, where the foothold gate moves 61–73 %. Three places
are exactly pass-through — not the single-out-edge point masses (those are
excluded from the table) but places whose every destination takes the same
factor, so renormalisation cancels it; the largest single departure is
`aggregate / reconnaissance`
(TV 0.44: the `enabled` tier lifts `→ initial-access` from 33 % to 77 % of the
success mass at the expense of the two Δ = +2 siblings — the same mechanism the
sweep study §2 recorded on the pre-2026-08-17 nets, where the base share was
45 %).

**Where it moves the mass.** Pooled across the verdict-bearing places, the net
shift between destination *classes* is small — to dwell-only destinations
−0.05 to +0.02, to objective-band destinations −0.06 to +0.01 — so the success
column does not systematically change the action/dwell mix or the objective
pull; it redistributes *within* classes, toward `enabled` action-bearing
destinations and away from their siblings (`lateral-movement → discovery`
+0.30 in `objective_exfiltration_impact`; `execution → impact` −0.21 in
`objective_impact`; `command-and-control → stealth` −0.05 to −0.12 in four
nets). Per-place table: `static_places.json`.

**What this settles and what it does not.** Statically the premise is false as
a statement about the *distributions* — the success column is a real
perturbation of the corpus routing, comparable in size to the failure column's
— and true as a statement about *provenance* (§1). Whether a perturbation of
this size reaches any outcome is the behavioural question, and the prior is
informative: experiment 2's verdict-blind control, which removes *both*
columns, was indistinguishable from the conditioned arm across 1 600 paired
runs ([`experiment_02_findings.md`](experiment_02_findings.md) §11). A
success-null arm removes less, so the expected behavioural cost is bounded
above by a contrast already measured as null.

---

## 3. The variant — rule-generated, reproducible, in memory

No value was hand-set. The generator gained one compilation switch,
`RuleSpec.success_passthrough` (`src/mtdsim/l3_simulation/controller/rules.py`):
with it set, every success cell compiles to `{"v": 1.0, "rule": "passthrough"}`
— the multiplicative identity, so composition on a success verdict returns the
base out-set renormalised — and the failure table compiles exactly as the spec
otherwise says. The five success rules are not edited; they are not consulted.
The variant used here is v3's registered spec with the flag on, held in memory
via `OutcomeOverlay.from_values(compile_values(...))` — the same seam the
sensitivity sweep and the verdict-blind arm use — and it is **not registered**:
the registry binds a version only once a published run consumes it, and none
has. Four tests pin it (`tests/l3_simulation/test_controller_rules.py`): the
success table is the identity on all 210 cells; the failure table equals v3's
cell for cell; at every place of every net a success verdict composes to the
blind arm's distribution and a failure verdict to the pinned arm's; and no
registered version carries the flag. The reproduction check still reports
0 of 420 differing cells per registered version.

Deliberately **without** the distance term on the success side. The premise is
that on success the walk *is* the corpus's routing; multiplying a declared
distance kernel back onto it would re-introduce exactly the declared layer the
variant removes. (A "distance-only success" point between the two is
representable — `success_passthrough=False` with the rule values set to 1.0 —
but it is not what the premise asks for, and it was not run.)

**The kernel-only arms are built in the workspace, not in `src/`.** The
handoff's third arm arrived with a "sync with Marc's concurrent session before
building anything" instruction, and nothing from that session had landed in
the repo when this study ran. So the two kernel-only overlays are constructed
in `kernel_only.py` from the tracked compiler's public seams alone — a
`RuleSet` with the nine failure rule values neutralised to 1.0 (so the
compiled failure cell is the bare kernel factor), `success_passthrough=True`,
and either the declared kernel form or a one-line subclass with the
adjacency-penalising form — and held in memory like `verdict_blind`. Nothing
was added to the generator for them; if the idea is taken up, the form becomes
a `RuleSpec` option and the ledger gains a row, which is a build that should
follow the concurrent session's own record, not precede it.

---

## 4. The dry run — design, declared before the numbers

| | |
|---|---|
| **arms** | `conditioned` (v3, both tables — the pinned arm) · `success_null` (v3 failure table, success pass-through) · `verdict_blind` (both tables absent — experiment 2's axis-4 control) · **the handoff's third arm, in two parameterisations** (§5.8): `kernel_asdeclared` and `kernel_adjacent` — failure encoded *purely* as the distance kernel with asymmetric decay, no failure semantic rules, success pass-through |
| **everything else** | experiment 2's declared inputs, regenerated on the current code so the three arms are paired on one implementation: mapping `v2_partial`, `retrace_sinks=True` (the landed S5), S3-R timing, horizon 15 000 s, the standard geometry, the eight defence conditions, intervals 200 s and 2 000 s, seeds 0–9 |
| **matrix** | 3 × 5 × 8 × 2 × 10 = **2 400 runs**, plus 2 × 800 = **1 600** for the two kernel-only arms, run after the first three had been analysed (stated so the sequence is on record; the kernel-only parameterisations were fixed before their runs existed) |
| **primary contrast** | paired per-seed difference in **distinct hosts compromised** (the axis-4 primary measure), `success_null − conditioned`; the pre-registered axis-4 bar is borrowed as the separation criterion: CI-separated in ≥ 2 profiles **and** ≥ 2 defence conditions at an interval |
| **secondary** | successes, attempted actions, blocked fraction, retraces, distinct places, visits, failure-routing rate; terminal-mode mix; share of routing decisions taken on each branch; realised success-branch routing per place (TV between arms) |
| **headline directionality** | E1's per-mechanism breadth suppression and E3's per-profile best-suppressor, per arm — does the ranking the chapter reports change when the success column is removed? |
| **not powered for** | any ordering of profiles; a mechanism league table (the exp-2 caveats carry over); anything ASR-shaped at 200 s |
| **caveat** | D-29: seed-matched arms share the substrate's RNG streams, so once walks diverge the "paired" difference is between independent draws; reported as experiment 2 reported it |

---

## 5. What moved

4 000 runs, zero errored cells. Every run terminated at the horizon — no
objective reach on any arm at either interval (the rate study's degenerate
region at 200 s; at 2 000 s the substrate objective was not reached in these
10 seeds either) — except the 47 stalls on the `kernel_adjacent` arm, §5.8.
Numbers: `analysis.txt`, `numbers/`.

### 5.1 The primary contrast — `success_null − conditioned`, distinct hosts

| | cells | CI > 0 | CI < 0 | mean of cell differences |
|---|--:|--:|--:|--:|
| hosts (primary) | 80 | **9** | **6** | +0.30 |
| successes | 80 | 2 | 12 | −0.85 |
| attempted actions | 80 | 0 | 25 | −7.8 |
| visits | 80 | 0 | 28 | −8.3 |
| distinct places | 80 | 20 | 2 | +0.17 |
| retraces | 80 | 3 | 2 | −0.25 |
| blocked fraction | 80 | 12 | 2 | −0.003 |

Fifteen of eighty host cells separate (four would by chance), and they are
**not noise: they sort by profile and by sign.** Removing the success column
*raises* breadth in `objective_none_c2` (8 cells, +1.3 to +2.9 hosts, seven of
them at 2 000 s) and in one `objective_impact` cell, and *lowers* it in
`objective_exfiltration_impact` (4 cells, −1.7 to −2.0) and `objective_exfiltration`
(2 cells, −0.6 to −0.9); `aggregate` never separates. Borrowing the axis-4 bar
(positive and CI-separated in ≥ 2 profiles and ≥ 2 conditions): **met at
2 000 s** (2 profiles × 6 conditions) and **not met at 200 s** (1 × 2) — and
met *in the other direction* nowhere, because the losing profiles never reach
two. So the success column is neither free nor uniformly useful: it is a
**profile-signed** effect of one to three hosts, as large as anything the
whole overlay has ever been shown to do.

Per-arm breadth, no-MTD / pooled over the seven MTD conditions:

| profile | interval | conditioned | success_null | verdict_blind |
|---|--:|---|---|---|
| `aggregate` | 200 | 6.10 ± 0.74 / 2.77 ± 0.56 | 6.50 ± 1.38 / 2.79 ± 0.58 | 6.40 ± 0.89 / 2.54 ± 0.44 |
| `objective_exfiltration` | 200 | 5.30 ± 1.01 / 2.33 ± 0.36 | 5.40 ± 0.93 / 2.11 ± 0.34 | 5.20 ± 0.64 / 1.80 ± 0.35 |
| `objective_impact` | 200 | 5.90 ± 1.19 / 2.09 ± 0.45 | 7.30 ± 0.97 / 2.29 ± 0.50 | 6.60 ± 1.06 / 2.27 ± 0.48 |
| `objective_exfiltration_impact` | 200 | 7.50 ± 1.68 / 2.56 ± 0.69 | 5.80 ± 1.20 / 1.93 ± 0.52 | 6.50 ± 1.41 / 1.96 ± 0.51 |
| `objective_none_c2` | 200 | 4.10 ± 1.74 / 1.09 ± 0.34 | 5.40 ± 2.07 / 1.81 ± 0.48 | 5.80 ± 1.57 / 2.06 ± 0.47 |
| `aggregate` | 2 000 | 6.10 / 5.97 ± 0.48 | 6.50 / 5.99 ± 0.38 | 6.40 / 6.10 ± 0.45 |
| `objective_exfiltration` | 2 000 | 5.30 / 5.13 ± 0.40 | 5.40 / 4.97 ± 0.34 | 5.20 / 4.64 ± 0.30 |
| `objective_impact` | 2 000 | 5.90 / 5.60 ± 0.43 | 7.30 / 6.46 ± 0.37 | 6.60 / 5.87 ± 0.41 |
| `objective_exfiltration_impact` | 2 000 | 7.50 / 6.29 ± 0.77 | 5.80 / 6.10 ± 0.54 | 6.50 / 6.71 ± 0.57 |
| `objective_none_c2` | 2 000 | 4.10 / **3.09 ± 0.45** | 5.40 / **5.50 ± 0.58** | 5.80 / **5.51 ± 0.49** |

### 5.2 The mechanism — the `enables` tier is substrate-coupled, in both directions

The realised success-branch routing (pooled, `success_branch_routing_tv.json`)
says where the hosts come from. In `objective_none_c2` the conditioned arm
routes `lateral-movement → execution` at 12 % of its success mass against the
corpus's 31 %, because the `enables` tier lifts the C2-hub arms
(`→ command-and-control` 43 %, `→ credential-access` 21 %) over it; `execution`
is `EXPLOIT_VULN` under `v2_partial`, the one verb that takes a host. Remove
the column and the corpus's own preference for exploiting after moving acts:
breadth under MTD at 2 000 s goes 3.09 → 5.50, which is exactly the blind
arm's 5.51 — so the whole of the conditioned arm's deficit in that profile
(experiment 2 saw the same sign on the old nets, §11: 4.10 against 5.40) was
the *success* column's doing, not the failure column's. In
`objective_exfiltration_impact` the same tier runs the other way:
`lateral-movement → discovery` at 78 % against the corpus's 51 % puts
`SCAN_PORT` before `EXPLOIT_VULN`, which is the substrate's own precondition
chain (`curr_ports` must be populated), so the column *helps* there (7.50
against 5.80 without MTD). The `enables` relations are attested knowledge about
adversaries; whether acting on them pays is a property of the *mapping*, and
on this mapping it pays in some nets and costs in others. That is the
H-coupling story of experiment 1's finding 1, now visible as a success-column
effect.

### 5.3 What the failure column does on its own — `success_null − verdict_blind`

| | CI > 0 | CI < 0 | mean |
|---|--:|--:|--:|
| hosts | 10 | 1 | +0.04 |
| successes | 44 | 2 | +9.8 |
| attempted actions | 57 | 0 | +13.2 |
| distinct places | 0 | 34 | −0.25 |
| retraces | 11 | 32 | −0.89 |
| blocked fraction | 10 | 21 | −0.011 |

With the success table out of the way this is the cleanest reading the failure
column has had. It does measurable **process** work — ten more successful
actions and thirteen more attempts per run, fewer retraces (the IA → recon
fall-back keeps the token off the sinks), fewer distinct places (the walk is
more concentrated), a slightly lower blocked fraction — and almost no
**outcome** work: +0.04 hosts on average, ten cells separated positive and one
negative, the axis-4 bar met at both intervals on the borrowed criterion but on
half-host effects (+0.5 to +1.5). The failure column is the half that
"reacts"; the host count it reacts into is essentially the blind arm's.

### 5.4 The whole overlay against the blind arm — `conditioned − verdict_blind`, regenerated

Hosts: 5 cells CI > 0, **15 CI < 0**, mean −0.27; successes +10.7 and attempts
+21.0 (49 and 59 cells positive). Thirteen of the fifteen negative cells are
`objective_none_c2` (the §5.2 mechanism), the other two
`aggregate / simultaneous_multi`. On the borrowed bar the conditioned arm beats the blind arm at 200 s
(2 profiles × 4 conditions, all of them `objective_exfiltration` and
`objective_exfiltration_impact` under application-class or multi schemes) and
nowhere at 2 000 s. **Flag, not actioned (out of this handoff's scope):** this
is experiment 2's E2 contrast regenerated on the 2026-08-17 rebuilt nets and
the landed retrace implementation, and its shape differs from §11 of the
experiment-2 record — more separated cells, most of them negative, and the
200 s bar technically met in the positive direction. The axis-4 badge was
decided on the old nets; whether it is re-examined is a ruling for that
record's owner, and nothing here moves it.

### 5.5 The experiment-2 headlines, per arm

- **E1 (per-mechanism breadth suppression) holds on all three arms, with the
  same shape.** At 200 s the network-class pair and the simultaneous scheme
  suppress breadth to 0.1–1.5 hosts against 4–7.5 without MTD, in every profile
  under every arm; the application-class pair suppresses weakly (to 2.7–7.1),
  and the random and alternative schemes sit between — the 2 × 2 family
  contrast the boundary programme named, unchanged by the arm. At 2 000 s
  suppression is largely gone on every arm (0–2 hosts, `ip_shuffle` and
  `simultaneous_multi` the only consistent suppressors). The arm does not
  change whether, or which class of, MTD suppresses.
- **E3's interaction holds on all three arms, and its *identities* do not.**
  On every arm the best-suppressing mechanism differs by profile (4–5 distinct
  of 5), so "the ranking is not the same for every profile" survives the arm
  change. But which mechanism is best for which profile changes between
  `conditioned` and `success_null` in four of five profiles at each interval —
  and between `conditioned` and `verdict_blind` too. Ten seeds do not separate
  mechanisms that differ by 0.1–0.9 hosts, which is the caveat experiment 2
  already carries ("not powered for a mechanism league table"); this study
  sharpens it: the *identity* of a profile's best suppressor is arm-sensitive
  and must not be reported as a property of the profile.

### 5.6 Which column fires, and how often

Pooled over every cell, the share of routing decisions taken on each branch
(a precondition-blocked dispatch carries a failure verdict and routes on the
failure column — `attacker.py`, `_UNACTIONABLE_VERDICT`):

| arm | success column | failure column (unblocked + blocked) | base (dwell-only) |
|---|--:|--:|--:|
| `conditioned` | 30.0 % | 34.2 % (8.6 + 25.6) | 35.8 % |
| `success_null` | 30.1 % | 33.2 % (8.0 + 25.2) | 36.6 % |
| `verdict_blind` | 28.5 % | 32.9 % (7.9 + 25.0) | 38.6 % |

Two things for the chapter. The success column conditions three in ten
routing decisions and the failure column one in three — so a failure-only
overlay leaves seven in ten decisions on the corpus proportions, which is the
premise realised in numbers. And three-quarters of the failure column's
firings are **precondition blocks**, not substrate failures: the "failure"
the declared failure matrix mostly conditions is the movement layer's own
coupling to the action layer (anatomy §6, H-coupling), not an MTD interrupt or
a failed exploit. That is already on record; it bears restating beside any
claim about what the failure matrix encodes.

### 5.7 The CTI-independence statement

No value was selected on these numbers. The variant is a declared construct
— the multiplicative identity on the success side — fixed before a run
existed; the failure table is v3's unchanged; the grid and the borrowed bar
were stated in §4 before `analyse.py` was written against the complete
`runs.jsonl`. The profile-signed host effect in §5.1 is reported as an output,
and it must **not** become a reason to adopt or decline: adopting the
failure-only overlay *because* it raises `objective_none_c2`'s breadth would
be fitting the policy to the nets, the violation the design forbids. The
reasons to adopt or decline are the §1 provenance argument and the §6 cost;
§5 says only what the choice moves.

### 5.8 The third arm — failure as the distance kernel alone, asymmetric decay

The handoff's item 4 (added 2026-08-19 after this study began): encode failure
*purely* as the distance kernel with a backward decay that differs from the
forward one — no failure semantic rules — so the whole declared layer is one
mechanism. Two parameterisations were fixed before their runs, both from
numbers already on the registry's record (γ = 0.25 declared; δ = 0.5, the
backward value before the persistence ruling; floor 0.1), success pass-through
on both (§3, `kernel_only.py`):

- `kernel_asdeclared` — the declared kernel *form* (`γ^(Δ−1)`, `δ^(|Δ|−1)`),
  which leaves adjacent travel unpenalised. With the rules neutralised, a
  failure verdict is therefore **pass-through at |Δ| ≤ 1** and bites only at
  Δ = ±2 (factor 0.25 forward, 0.5 backward) and ±3 (zero). Statically its
  failure column sits at TV 0.02–0.07 from the base and **0.05–0.20 from
  v3's failure column**.
- `kernel_adjacent` — the adjacency-penalising form (`γ^Δ`, `δ^|Δ|`) the
  sibling record costs as the candidate re-declaration
  ([`failure_weight_decomposition.md`](failure_weight_decomposition.md) §4):
  forward one stage 0.25, backward one stage 0.5, within-stage 1.0, two
  stages 0.0625 → 0 under the floor. It *does* encode direction at one stage
  — backward twice forward — but the ordering it can express is
  lateral > backward > forward, where v3's failure rules say
  backward 0.9 > lateral 0.7 > forward 0.35; and it **hard-suppresses 15
  corpus edges** on failure (every Δ = +2 edge), where v3 suppresses none.

**What neither can express, now in numbers.** The foothold gate. On a failed
`initial-access`, v3 routes **65–83 %** of the mass back to `reconnaissance`
(the 0.02 gate against the 0.9 bridge); both kernel-only arms route **4–11 %**
— the base share of the synthetic bridge edge, because a per-offset factor
gives every destination at the same offset the same number and cannot
prefer the bridge over the foothold-dependent destinations. The destination-
aware behaviour the failure rules were written for is unreachable from any
kernel, symmetric or not.

**And one thing the adjacent form breaks.** It stalls: at
`objective_exfiltration / reconnaissance` both base out-edges are Δ = +2, so a
failure verdict there (an MTD interrupt at 120–130 s in, read as failure)
zeroes the whole out-set and the walk ends — **47 of 160 runs** on that profile
terminated that way (`terminal_mode = sink`, the stall path), every one at
200 s under an MTD condition. `objective_impact / resource-development` would
stall the same way and does not only because it is dwell-only. v3's "0 stalls
at every swept point" guarantee (`weight_sensitivity_study.md` §2) does not
survive the adjacent form on these nets — the same 28 corpus edges the
sibling record warned the re-declaration would hard-suppress.

**Behaviourally** (paired per seed; 80 cells):

| contrast | hosts CI>0 / CI<0 / mean | successes mean | attempted mean | retraces mean | axis-4 bar |
|---|---|--:|--:|--:|---|
| `kernel_asdeclared − success_null` | 7 / 1 / +0.15 | −6.2 (31 cells <0) | −7.1 | +0.35 | not met 200 s; met 2 000 s (3 × 2) |
| `kernel_adjacent − success_null` | 13 / 9 / +0.28 | −0.3 | −5.3 | −0.17 | met both (profile-signed again: `objective_none_c2` +, `objective_exfiltration` −) |
| `kernel_asdeclared − verdict_blind` | 5 / 2 / +0.19 | +3.6 | +6.1 | −0.54 | met both (2 × 3, 2 × 2) |
| `kernel_adjacent − verdict_blind` | 7 / 0 / +0.32 | +9.5 | +7.9 | −1.05 | met both (2 × 2, 4 × 4) |

Read against §5.3: the failure *rules* are what produce the failure column's
process work — neutralising them costs six successful actions per run against
`success_null` — and the kernel alone recovers some of it only in the
adjacent form, at the price of the stall. On hosts the kernel-only arms are
again within a fraction of a host of everything else, signed by profile.

**Verdict on the third arm.** *Representable, and it does not do the job.* A
kernel-only failure layer is one mechanism, which is the attraction; but the
declared form makes failure a pass-through at the adjacent step (so it
encodes almost nothing), the adjacent form encodes the wrong ordering
(lateral above backward), both lose the foothold gate entirely (4–11 % against
65–83 % back to reconnaissance), and the adjacent form stalls the walk on one
profile. The behaviours the failure rules exist for are destination-aware and
a per-offset decay is destination-blind by construction; that is not a
parameter problem. If the one-mechanism story is wanted, the honest version is
the §7 one — one *declared matrix* (nine rules × one kernel, the decomposition
the sibling record draws) — not one kernel.

---

## 6. Blast radius — what adoption would re-open

Every published movement-arm number since 2026-07-29 is keyed on
`v3_persistent_backward`. The recorded workspaces that name it and their run
counts: experiment 2 (2 760), the axis-4 structural probe (800), the axis-7
learning sweep (2 400), the disruption frontier (960), FSM alignment (2 080),
FSM succession (2 080), learning readiness (4 600), progress credit (7 000),
predictability (1 600 + 600), plural preference (1 100), profile divergence
(500), exploit-learning disengagement (450); the retired iterated-cost sweep
(3 400) does not re-run. **≈ 27 000 runs, ≈ 22 CPU-hours, roughly 3–4 hours
wall at 7 workers** — the compute is not the cost. The cost is that each of
those records carries a findings section and several carry badge verdicts
(axes 1, 3, 4, 6, 7) and figures; adopting a new overlay version would mean
either (a) re-running and re-deriving every one of them under `v4`, or (b)
publishing the chapter on `v3` and reporting the failure-only variant as a
**measured ablation** beside it. Option (b) is what this study already is.

---

## 7. Verdict

**Feasible, not free, and the premise holds on provenance, not on behaviour.**

1. **Statically, the success column does real work** (§2): it moves 13–20 % of
   the out-mass at a typical verdict-bearing place, the same order as the
   failure column outside the foothold gate. "Success is already encoded in
   the base" is false as a claim about the distributions.
2. **Behaviourally, that work is profile-signed and substrate-coupled** (§5.1,
   §5.2): one to three hosts up in one profile, one to two down in two others,
   through the `enables` tier's interaction with the mapping's precondition
   chain. It is not the clean "approximately free" the handoff hoped for; it
   is also not a reason to keep the column, because the sign depends on the
   net.
3. **The premise is right about provenance** (§1): the success column is a
   declared re-weighting (half its routed cells declared-judgement, the other
   half an `enables` tier attested by the same survivorship sources the base
   is measured from) laid over a corpus-grounded layer that already encodes
   what successful campaigns did next. The failure column is the only layer
   encoding what no corpus records. A failure-only overlay is one declared
   object with one provenance story — *the corpus routes success; the
   declared matrix routes failure* — and that is the defensibility gain Marc
   named, realised exactly.
4. **The evidence-tier inversion is real and must be stated** (§1): adoption
   drops the better-attested table. The honest sentence is that it drops a
   *re-declaration* of attested knowledge, not the attested knowledge — which
   stays in the base — and keeps the declared half because the declared half
   is the one with no alternative source.
5. **The failure column alone is the reacting half** (§5.3, §5.6): more
   actions, fewer retraces, a host count indistinguishable from the blind arm;
   it conditions one routing decision in three, three-quarters of those on
   precondition blocks. Whatever axis 4 says about the overlay, it says about
   this half.
6. **The headline claims survive the choice** (§5.5): MTD suppresses breadth
   on every arm; the mechanism × profile interaction exists on every arm; no
   profile ordering and no mechanism league table was powered before and is
   not now. What the choice moves is the per-profile breadth magnitudes every
   published record quotes — which is the §6 cost.
7. **The kernel-only third arm is representable and does not do the job**
   (§5.8): it loses the foothold gate by construction, encodes the wrong
   one-stage ordering in the only form that encodes any, and stalls a profile.
   The one-mechanism simplification the handoff hoped for is not available
   from a kernel; it is available as one declared *matrix*.

**One-sentence bottleneck:** the decision is a provenance-versus-re-derivation
trade — a cleaner declared layer against ≈ 27 000 re-run rows and a dozen
re-written findings — and the behavioural evidence does not break the tie in
either direction, because it is signed by profile; the kernel-only shortcut
is off the table on expressiveness, not on cost.

---

## 8. The ruling slot

**Question for Marc (one question, with a recommendation):** adopt the
failure-only overlay as the reported configuration (register `v4_failure_only`,
re-key every published movement-arm record — §6), keep `v3` as the reported
configuration and carry this study as the **ablation** that prices the success
column, or decline the idea?

**Recommendation: keep `v3` as the reported configuration; carry this study
as the ablation; write the chapter's overlay paragraph on the premise.** The
premise is the better *argument* and it can be made on the page without
re-keying anything: the dissertation says the base encodes the corpus's
success routing, the failure matrix encodes what the corpus cannot, and the
success table is a declared sharpening whose removal was *measured* — a
profile-signed effect of one to three hosts, the §5.2 mechanism named — and
found not to change any headline. That is a stronger position than either
"two declared matrices" or "one declared matrix, untested", and it costs no
re-run. If Marc wants the reported configuration itself to be failure-only,
the price is §6 and it should be paid once, as `v4`, with every record's
findings section re-derived — not by editing `v3` (the registry's immutability
rule; the pinned arm stays reproducible).

| ruling | date | by |
|---|---|---|
| *pending* | | Marc |

---

## 9. What this gives the chapter (content points, no prose)

For the owed §4.2.4 paragraph on how failure was encoded (Marc dictates):

- The three-layer statement: corpus proportions carry success; the failure
  matrix carries what incident reports do not record; the success table is a
  declared sharpening of the corpus, kept in the reported configuration and
  priced by ablation.
- The size of the sharpening: 13–20 % of the out-mass at a conditioned place,
  three in ten routing decisions conditioned; and its measured effect — one to
  three hosts, signed by profile, through the `enables` tier's interaction with
  the substrate's precondition chain (the H-coupling mechanism), no headline
  moved.
- The failure matrix's firing profile: one routing decision in three,
  three-quarters of those on precondition blocks rather than MTD interrupts or
  failed exploits.
- The evidence-tier sentence, in the order §7 item 4 gives it.
- Why failure is not the kernel alone: the foothold gate is destination-aware
  and a per-offset decay is destination-blind (4–11 % against 65–83 % back to
  reconnaissance); the adjacent form stalls one profile — so the one declared
  object is a matrix of nine rules times one kernel, not a kernel.
- Ties to the sibling provenance handoff: the decomposition presentation
  (failure kernel × distance kernel → aggregated matrix) is unchanged by this
  ruling if `v3` stays; if `v4` is adopted the success panel of that figure
  becomes a constant and the presentation is of one matrix.

## 10. Where this connects, and when to update

- **Consumes:** [`success_failure_overlay_design.md`](success_failure_overlay_design.md)
  §1–§4 (the composition rule, the rules, the tier asymmetry);
  [`weight_sensitivity_study.md`](weight_sensitivity_study.md) (the registry and
  v3); [`experiment_02_findings.md`](experiment_02_findings.md) §2, §11 (the
  grid, the blind control); [`demonstration_arms_prereg.md`](demonstration_arms_prereg.md)
  §5 (the axis-4 bar borrowed here);
  [`../../declared_value_provenance.md`](../../declared_value_provenance.md)
  (the tiers); [`../../research_record/threads/outcome_overlay.md`](../../research_record/threads/outcome_overlay.md)
  (the genesis epistemics); the §4.2.4 dictation in `docs/thesis/dissertation.tex`.
- **Feeds:** the §4.2.4 failure-encoding paragraph; the sibling provenance
  handoff (`2026-08-19_failure_weight_provenance.md`, deliverable 1's shape);
  [`../../../notes/ch4_methods/outcome_overlay_directionality.md`](../../../notes/ch4_methods/outcome_overlay_directionality.md)
  (its asymmetry paragraph should carry the §1 re-reading once Marc rules).
- **Code:** `src/mtdsim/l3_simulation/controller/rules.py`
  (`RuleSpec.success_passthrough`, `PASSTHROUGH_RULE`);
  `tests/l3_simulation/test_controller_rules.py` (four pins).
- **When to update:** when Marc rules (§8 table; if `v4`, register it in
  `overlays/manifest.json` with `success_passthrough: true`, bump the ledger,
  and open the re-key handoff); if the axis-4 record is re-examined on the
  rebuilt nets (§5.4 flag); if the nets are rebuilt again (§2 and §5 are on
  the 2026-08-17 nets).
