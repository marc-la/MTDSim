---
status: open — design inventory; Marc's rulings owed before any tex change
created: 2026-09-08
topic: "§4.3 is titled a formalism and carries none. Every element of the executed net, the standard GSPN tuple it maps onto, and the one genuine extension (verdict-conditioned immediate weights), inventoried from the code and the records so the formal definition can be written in Marc's words and the sensitivity analysis keyed to its symbols."
---

# §4.3 — the elements of the GSPN formalism, and what this net extends

## The ask (Marc, 2026-09-08)

A section titled "generalised stochastic Petri-net formalism" that does not
state a formalism reads as deceitful. Paragraph 2 of §4.3 should become the
formal definition; the amendments (dwell times, mapping, failure matrix, the
runtime re-weighting) should be defined in that definition's language; the
sensitivity analysis in ch5/ch6 then reads as bounds on the definition's
parameters, and the method's assumptions become an explicit register.
Design first, no tex change yet: this file is the element inventory.

Everything below was read off the **code** (`src/mtdsim/l3_simulation/`) and
the **data artefacts** (`data/ogasp/`) first, then reconciled against the
records. Where a record and the code disagree, the code wins and the
disagreement is listed in §9.

## 1. The reference definition the section must cite

The standard GSPN (Ajmone Marsan, Conte and Balbo 1984; the 1995 book) is the
tuple

    GSPN = (P, T, Π, I, O, H, W, M0)

with `P` places, `T = T_timed ∪ T_imm` transitions, `Π` priorities (immediate
transitions pre-empt timed ones), `I` / `O` input and output arcs, `H`
inhibitor arcs, `W` the rate of each timed transition and the weight of each
immediate one, `M0` the initial marking. A marking with an enabled immediate
transition is *vanishing*; one with only timed transitions enabled is
*tangible*. Marsan's definition already allows `W` to be **marking-dependent**;
that is the hook §4 hangs on.

**Bib gap.** No Marsan entry exists in `references.bib`; the only Petri source
cited is `cai2016` (the MTD precedent) and the records cite Murata 1989 for
the SPN–CTMC isomorphism. A definition needs its own source. Per the
paper-acquisition division this is Marc's to download (the 1995 book, or the
1984 ACM TOCS paper). Stub the key `marsan1995gspn` with a VERIFY note when the
prose is drafted, not before.

## 2. The representational choice the definition must make first

The code puts the dwell "on the place" and the routing choice "on the
transitions" (`timing.py` docstring: "a place's dwell is a timed transition
with exponential firing, and the verdict-conditioned routing choice among its
out-edges is a weighted immediate transition"). In standard GSPN terms that is
a two-transition gadget per tactic:

    p  ──τ_p (timed, rate 1/μ_p)──▶  p̂  ──t_{pq} (immediate, weight w)──▶  q

`p` is the tangible tactic place, `p̂` its vanishing *decision* place, `τ_p`
the tactic's execution (the dwell **is** the dispatched action, S3-R), and
`t_{pq}` the choice of the next tactic. Marc's P2 sentence "the transitions
are tactic–tactic pairs" names `t_{pq}`; the dwell sentence names `τ_p`.

Ruling owed (R1): state the gadget explicitly (honest, and what an examiner
who knows GSPNs will look for), or define places = tactics and say once that
each tactic carries one timed transition and its out-edges are its immediate
transitions. Recommendation: the explicit gadget, drawn once (a five-node
figure), because the extension in §4 lives entirely on the immediate
transitions and the figure makes that visible.

## 3. The static net — element by element

One net per profile `c ∈ C = {exfiltration, impact, exfiltration+impact,
no realised objective}` plus the aggregate; same construction, different
`P_c` and `W_c` ("one shared structure, four parameterisations",
`petri_feasibility.md:173-179`).

| Symbol | Standard element | This work | Value / artefact | Anchor |
|---|---|---|---|---|
| `P_c` | tangible places | the ATT&CK Enterprise tactics present in profile `c` (v19.1 pin, `data/gap/_attack/`) | 15 / 13 / 14 / 13 (aggregate 15); `stealth` = TA0005 Defense Evasion, `defense-impairment` = TA0112 are project relabels | `*_structural.json` `places`; `tactic_durations.json` |
| `P̂_c` | vanishing places | one decision place per tactic (the gadget) | implicit in the code (`_route`) | §2 |
| `T_timed` | timed transitions | `τ_p`, one per tactic; **immediate** when `μ_p = 0` (`resource-development`) | rate `λ_p = 1/μ_p` | `timing.py:66-87` |
| `T_imm` | immediate transitions | `t_{pq}`, the tactic-pair transitions; **no self-loops** (dropped at build; dwell carries in-tactic time) | 108 / 76 / 69 / 54 (aggregate 122) non-null | `*_structural.json` `transitions`; `weights.py` docstring |
| `I, O` | arcs | `I(τ_p)=p, O(τ_p)=p̂, I(t_{pq})=p̂, O(t_{pq})=q`; all multiplicity 1 | — | §2 |
| `H` | inhibitor arcs | **none** | — | records silent; code has none |
| `Π` | priorities | immediate > timed only; no priority among immediates | — | standard |
| `W(τ_p)` | firing rate | `1/μ_p`, `μ_p` the declared per-tactic mean (§5) | catalogue | `tactic_durations.json` |
| `W(t_{pq})` | base weight `w_c(p,q)` | out-normalised **flow proportion** (D3, W-A): distinct flows in `c` drawing a technique edge `p→q`, over flows drawing any out-edge of `p`; `operator_dedup` corpus (n = 29) primary, `raw` (n = 38) the robustness column | Σ_q w_c(p,q) = 1 | `weights.py:1-40`; `metrics_semantics.md:448-476` |
| synthetic overlay | added immediate transitions | `recon→resdev`, `resdev→initial-access`, `initial-access→recon`, added only where recon cannot reach initial-access; share `s = 1.0` out of an island place, `s = 0.1` otherwise with observed mass scaled to `1−Σs` | exfiltration+impact: 1.0 / 1.0 / 0.1; none/C2: 1.0 / 0.1 / 0.1; exfiltration, impact, aggregate: none | `net.py:163-195`; `synthetic_overlay.json` |
| `M0` | initial marking | one token at `reconnaissance` (overlay arm) or `initial-access` (observed-only arm) | 1-safe by construction | `net.py:198-212` |
| sinks | places with no out-transition | exfiltration: `impact`; impact: `collection`; exfil+impact: `credential-access`; none/C2: `privilege-escalation` (overlay on) | handled by retrace (§4.5) | `sink_retrace_design.md:44-49` |
| absorbing place | — | **none.** No place ends the run; termination is the environment's (§6) | — | records silent, code confirms |

Closed-world assumption, stated once with `W`: the observed out-set at `p` is
the complete choice set (`metrics_semantics.md:466-469`). Weights are
workflow recurrence, never efficacy or actor likelihood (survivorship
framing, `:470-473`).

## 4. The extension — what the runtime does to the net

### 4.1 The statement in one line

The structure `(P, T, I, O)` never changes during a run. What changes is the
weight vector of the immediate transitions out of the current decision place,
recomputed at every firing of `τ_p` from a signal the environment returns.
Formally, `W(t_{pq})` is not a constant but a function

    W(t_{pq} | v, h)  ∝  w_c(p,q) · F_v(p,q) · Π_m  m(p,q | h)

renormalised over the out-set of `p`, where `v` is the verdict the
environment returned for `τ_p`'s firing and `h` is the run's own history.
(`outcome.py:114-157`; `state.py:1-16`; `modulator_composition.md:27-31`.)
Marsan's marking-dependent weights depend on the marking; here the marking
is one token's position, so the dependence is on an **exogenous** signal.
That is the honest name for the extension: a GSPN whose immediate-transition
weights are conditioned on an environment verdict. Candidate names for Marc's
ruling (R2): "verdict-conditioned GSPN", "GSPN with environment-conditioned
routing", "open GSPN". The records' own phrase is "verdict-conditioned
re-weighting" (§4.4.2 of the tex already uses it).

### 4.2 The environment and the two functions that couple to it

| Element | Definition | Value | Anchor |
|---|---|---|---|
| `E` | the environment: MTDSim, network + defender, on the shared SimPy clock | — | `run.py` |
| `A` | the action set | the six inherited verbs `{SCAN_HOST, ENUM_HOST, SCAN_PORT, EXPLOIT_VULN, BRUTE_FORCE, SCAN_NEIGHBOR}` | `controller.py:45-54` |
| `φ` | tactic-to-verb mapping, `φ: P → A ∪ {⊥}`, partial, at most one verb per tactic, `⊥` = dwell-only | `v2_partial`: 8 mapped, 7 dwell-only (persistence, stealth, defense-impairment, collection, exfiltration, impact, resource-development); `v1_ckc_total` is the total mapping of experiment 1 | `mappings/v2_partial.csv` |
| `V` | verdict alphabet | `{success, failure, none}` | `outcome.py:53`; `attacker.py:371` |
| `ν` | verdict function, read off the environment's own outcome, never re-rolled | per verb: `EXPLOIT_VULN` compromised/uncompromised; `SCAN_HOST`, `BRUTE_FORCE` the bool; `ENUM_HOST`, `SCAN_PORT`, `SCAN_NEIGHBOR` success unless the fresh-host contract's state-delta rows fire (`ENUM_EXHAUSTED`, `SCAN_PORT_EMPTY`, `NEIGHBORS_NONE_FRESH`) | `verdict.py` |
| — | unmet precondition | `failure`, decided in-layer (`PRECONDITION_UNMET`); the dwell is still charged | `attacker.py:894-903` |
| — | MTD interrupt | `failure`, whatever the verb | `verdict.py:83` |
| — | dwell-only place | `none`: no verb, no verdict; `F_none ≡ 1`, the token routes on `w_c` | `attacker.py:585-636` |

### 4.3 The conditioning factor `F_v`

    F_success ≡ 1        (v4_failure_only: the corpus is the success policy)
    F_none    ≡ 1
    F_failure(p,q) = R(p,q) · d(Δ(p,q))        over all 210 ordered pairs

`R` is the rule kernel: nine declared values, first match wins, in the
rules file's order (`rules.py:259-282`; letters from
`failure_weight_decomposition.md:83-92`):

| Key | Rule | Value | Fires on |
|---|---|---|---|
| A | ia_gate_foothold | 0.02 | initial-access failed → any foothold-dependent destination |
| B | recon_gate_initial_access | 0.4 | reconnaissance failed → initial-access |
| C | recon_gate_deep | 0.05 | reconnaissance failed → any foothold-dependent destination |
| D | preintrusion_damper | 0.25 | post-intrusion source falling back to a pre-foothold destination |
| E | execution_damper | 0.35 | any backward move into execution |
| F | backward | 0.9 | else backward |
| G | lateral | 0.7 | else within-stage |
| H | forward_from_foothold | 0.35 | else forward, source post-intrusion |
| I | forward_from_prep | 0.3 | else forward, source pre-foothold |

`d` is the lifecycle-distance kernel on the signed stage offset
`Δ = s(q) − s(p)` over the four consensus stages
(preparation {recon, resdev}; intrusion {initial-access, execution};
post-intrusion {persistence, privilege-escalation, stealth,
defense-impairment, credential-access, discovery, lateral-movement, C2};
objective {collection, exfiltration, impact}):

    d(Δ) = 1                 Δ = 0
         = γ^(Δ−1)           Δ ≥ 1
         = δ^(|Δ|−1)         Δ ≤ −1
    d < z  reads as exactly 0 (strict comparison, applied to d, before composition)

Declared `γ = δ = 0.25`, `z = 0.1` (`lifecycle_consensus.json`
`declared_parameters`; `rules.py:81-111`; note the code's dataclass default
`delta_ratio = 0.5` is v2's value and the registry entry overrides it to
0.25 for v3/v4). Fourteen distinct cell values, twelve exact zeros.

Semantics of a cell: present with value 0 removes the edge under that
verdict; a pair absent from the table passes through at 1 (this is what makes
`none` and the verdict-blind ablation arm identities). If every out-edge is
suppressed the walk **stalls** and ends; no profile reaches that at any swept
point, and that is checked, not assumed (`weight_sensitivity_study.md` §3).

### 4.4 The history term `Π_m`

In the **reported configuration the product is empty** (`Π_m = 1`): the
freeze pins the headline arm to modulators null (`model_scope_freeze.md:296-308`).
Every capability is a further multiplicative factor with its own declared
parameter and a null value at which the run is bit-identical:

| Factor | Rule | Parameter (declared; band) | Status |
|---|---|---|---|
| learning (axis 7) | `m = Q(q)^κ`, `Q(q) = (s_q+1)/(s_q+f_q+2)`, counts decayed by `(1−ρ)` on each MTD interrupt | κ = 1 {0,0.5,1,2,4}; ρ = 0.5 {0,0.25,0.5,1} | built, DESIGNED, ablation arm |
| incentive (axis 6) | `m = (u(q)/ū)^λ`, `u = benefit/max(cost, floor)` | λ = 1 {0,0.5,1,2,4}; floor 4.5 s | built, DESIGNED, closed 2026-08-02 |
| FSM succession | `m = 1` if `q`'s verb is FSM-licensed next, else `1−α` | α = 0 [0,1] | concession, negative result, off |
| FSM alignment | distance-to-productive-action dial | α = 0 | retired as instrument |

Two things in the driver are history-dependent but are **not** factors:
the sink retrace (§4.5) and the fresh-host contract (a host-selection
invariant in dispatch, on by default, reweights nothing). The token-hold
rule (T1) is off: H1′ not met, not layered onto the reported configuration
(`fsm_token_hold_findings.md:280-290`).

Ruling owed (R3): does the definition show the general `Π_m` slot (one
symbol, then "empty in every reported run; each ablation arm names its
factor") or only `F_v`? Recommendation: show the slot. It is one symbol, it
is how the records already write the rule, and it is what makes ch6's
ablation arms definable in the same language rather than as prose
exceptions.

### 4.5 Sink retrace — the one new policy, stated as a rule

When the token's routing at `s` yields nothing **and** `s` has no base
out-transition, the token returns to the place `p` it came from, visits it
in the ordinary way (a fresh `τ_p` firing, a fresh verdict), and the edge
`(p, s)` is removed from that one selection at `p` only; if that leaves `p`
with no positive mass the retrace walks one further step up the visited
chain, and an exhausted chain ends the run (`SINK_EXHAUSTED`). No budget;
retraces are under 1 % of steps in every measured cell
(`attacker.py:1171-1219`; `sink_retrace_design.md:78-93, 177-205`). A
**stall** (every out-edge suppressed at a place that has base edges) is a
different condition and is not retraced. In the definition this is a
history-dependent restriction of the enabled set at `p̂`, not a weight.

## 5. Timing semantics — what the standard gives and what this work commits

| Element | This work | Anchor |
|---|---|---|
| firing time of `τ_p` | `Exponential(mean μ_p)`; `μ_p = 0` → immediate, no draw | `timing.py:83-87` |
| `μ_p` | `anchor_g(p) × m_p`: four anchors (scan-shaped 35 s, exploit-shaped 4.5 s, low-and-slow 45 s, objective-execution 36 s; prep 0 s) times a per-tactic multiplier; fifteen values, four free anchors | `tactic_durations.json`; tex Table 4.4 |
| what the firing is | the dispatched action itself: `step(verb, duration = draw)` — the movement layer supplies every unit of attacker time (S3-R); the substrate's own `ATTACK_DURATION` and `exploit_time` are not consumed on this arm | `attacker.py:18-36, 908` |
| pre-emption | an MTD mutation is an exogenous event that pre-empts `τ_p` mid-firing: the partial time served is recorded, the confusion penalty is paid, the verdict is `failure`; a network-layer mutation also clears the host cursor | `attacker.py:905-937, 978-1021` |
| the race | with exponential firing the residual after a pre-emption is distributed as a fresh draw, so no partial-service state is carried; shape re-enters through this channel (a long dwell is likelier to be interrupted) — the madan2004 leak already argued in App. C.2 | `stochastic_timing_design.md:406-412, 522-525` |
| confusion penalty | substrate-side, not a net element: `20 + Exp(0.5)` s under the inherited shifted regime, one charge per interrupt | `constants.py:147`; `time_generator.py:39-42` |
| MTD trigger | not in the net; the environment's process. Under the inherited "shifted" regime the interval is `200 + Exp(0.5)` s, i.e. near-deterministic; a true `Exp(200)` is the D-08 regime input | `constants.py:110-114`; `run.py:281, 364-375` |
| clock | one shared SimPy clock; the net holds no clock ("the movement layer supplies the time; SimPy spends it") | `stochastic_timing_design.md:183-196` |
| RNG | four isolated streams: token sampler (run seed), dwell (`seed ^ "TIME"`), state (`seed ^ "STAT"`), substrate global | `timing.py:51`; `state.py:81` |

The claim is explicitly **not** that attacker dwell is exponential: a
tractable, precedented family whose mean is the load-bearing quantity, with
the Erlang-4 same-mean substitution as the shape check (App. C.2).

## 6. The run as a process — and what ends it

One run is the joint trajectory of (marking, environment state). Per step:
`τ_p` fires for its drawn time (the verb runs in `E`, or nothing does) →
`ν` returns `v` → the weights at `p̂` are composed → one `t_{pq}` is
sampled → the token moves. Termination is never a place:

| Terminal | Condition | Tag |
|---|---|---|
| objective | the environment's compromise criterion, 80 % of hosts (or a target host under the targeted objective) | `SIM_END` via `end_event` |
| horizon | 15 000 s | `SIM_END` |
| stall | every out-edge suppressed under `v` | (no tag; `next_place = None`) |
| sink, retrace off / exhausted | §4.5 | sink / `SINK_EXHAUSTED` |
| backstop | 50 000 events | `MAX_EVENTS` |

The reported configuration, for the record the definition describes:
profile net with synthetic overlay, seed at reconnaissance; `v2_partial`
mapping; `v4_failure_only` overlay; S3 exponential timing; retrace on;
fresh-host contract on; token hold off; modulators null; general objective;
horizon 15 000 s; MTD interval 200 s (shifted regime); geometry 50/5/8/4.

## 7. Parameters and assumptions, for ch5/ch6

### 7.1 The parameter register (candidate V6 table rows)

| Symbol | Meaning | Declared | Band | Tier | Swept? |
|---|---|---|---|---|---|
| `μ_g` scan-shaped | anchor | 35 s | ×[0.5, 2] | 1 substrate-fixed | yes (inert) |
| `μ_g` exploit-shaped | anchor | 4.5 s | ×[0.5, 2] / [0.25, 4] | 1 | yes (inert) |
| `μ_g` low-and-slow | anchor | 45 s | ×[0.25, 4] (execution, defense-impairment ×0.5 base, [0.1, 4]) | 3 | yes — the only anchor that moves an outcome |
| `μ_g` objective-execution | anchor | 36 s | ×[0.5, 2] (impact [0.1, 5]) | 2 | yes (inert) |
| `μ` resource-development | off-clock | 0 s | fixed | 3 | no |
| dwell family | shape | exponential | Erlang-4 same-mean | — | yes (one corner separates) |
| `γ` | forward decay | 0.25 | [0.1, 0.5] | attested-pattern / declared-magnitude | yes (fixed-dwell regime; re-sweep owed under S3-R) |
| `δ` | backward decay | 0.25 | [0.1, 0.5] | declared-judgement | partly (δ = 0.1 unswept) |
| `z` | floor | 0.1 | {0, 0.05, 0.1} | declared-judgement | yes (inert by corpus structure) |
| A–I | rule kernel | nine values | — | declared | **no, by rule** (argued magnitudes, not a parameterised term) |
| `s` | synthetic share | 0.1 (island 1.0) | — | declared | no |
| `φ` | mapping | v2_partial | v1_ckc_total | selected input | yes (two versions; App. B.7) |
| `F_success` | success treatment | identity | v3's success table | ruled 2026-08-19 | measured before ruling |
| corpus variant | base weights | operator_dedup (29) | raw (38) | — | robustness column |
| uniform weights | preference floor | off | on | ablation | yes (plural_preference) |
| verdict-blind | adaptive loop | off | on | ablation (axis 4) | yes |
| κ, ρ, λ, α | modulators | 1, 0.5, 1, 0 | see §4.4 | declared | yes, as labelled arms |
| penalty | confusion | 20 s | — | substrate invariant (Brown) | no |
| MTD interval | environment | 200 s | 1 600 s boundary noted | substrate | yes (tempo sweep) |
| horizon, geometry, seeds | environment | 15 000 s; 50/5/8/4; 10-seed studies | — | — | — |

### 7.2 The assumption register (candidate ch5 list; each is a sentence the
definition licenses)

1. **A1 exponential firing.** Dwell is `Exp(μ_p)`; the mean is the claim, the
   shape a tractability choice (App. C.2 carries the defence).
2. **A2 closed world.** The observed out-set at each tactic is the complete
   choice set; a different corpus gives different `T_imm` and `W`.
3. **A3 recurrence, not likelihood.** `w_c` is how often analysts drew the
   edge; success-only reporting (survivorship) is why `F_failure` exists.
4. **A4 success passthrough.** The corpus is the success policy (`F_success ≡ 1`).
5. **A5 binary verdict.** `ν` collapses every outcome to success/failure;
   an interrupt and an unmet precondition are both failure.
6. **A6 dwell-only opacity.** A mutation during a dwell-only place is felt in
   cost, not routing.
7. **A7 one token.** The AND structure Attack Flow preserves is vacuous
   under a single token; a constraint on parameters, not the formalism.
8. **A8 consensus staging.** `s(·)` and hence `Δ` are imported from five
   lifecycle models; ATT&CK itself imposes no order.
9. **A9 synthetic pre-intrusion structure.** Three declared edges, share `s`.
10. **A10 retrace.** A structural dead end is retraced; a stall is not.
11. **A11 substrate invariants.** Penalty, interval, and the six verbs are the
    environment's, held fixed across arms.
12. **A12 no cross-run memory; no scheme awareness.** `h` is within-run.

## 8. Proposed shape for §4.3 paragraph 2 (scaffold, not prose)

- **Definition 1 (profile net).** The tuple of §3, one display, with `P_c`,
  `T_timed`, `T_imm`, `W`, `M0` named in Marc's words; the gadget figure
  beside it (R1).
- **Definition 2 (timing).** `τ_p ~ Exp(μ_p)`, `μ_p = 0` immediate; one
  sentence that the firing is the action and the environment spends the time.
- **Definition 3 (verdict-conditioned routing).** The one display equation
  of §4.1, then `F_v` named (identity on success and none; `R · d` on failure)
  with a forward pointer to §4.4.1 for the values and to App. B.6 for the
  kernels. The general `Π_m` slot if R3 rules it in.
- **The extension sentence.** One sentence saying what departs from Marsan:
  structure fixed, immediate weights conditioned on an exogenous verdict,
  a timed transition pre-emptible by the environment, one history rule
  (retrace). That sentence is what makes the section's title honest.
- **Notation table** (symbols → meaning → where declared), either in the
  section or as the head of App. B; this is also the sensitivity table's key.
- What P2 currently says survives as prose around the definitions: places
  are tactics, transitions are pairs, self-loops dropped, one token, built
  before execution, "plug and play" (= `W` and `P_c` vary, the construction
  does not).
- §4.4's three inputs then re-key: dwell catalogue = `μ`; mapping = `φ`;
  failure matrix = `F_failure = R · d`; §4.4.2's loop = the process of §6.
  No new content, symbols only.

Budget: roughly 120–150 words of new definitional prose plus two displays
and a notation table (tables are word-cheap). The L3 unit is at ~370 words
against 1; the overdraft is the ledger's to reconcile at assembly.

## 9. Record inconsistencies to resolve before the prose is written

1. `architecture.md:534-536` says S3 replicates the confusion penalty "as a
   net place"; `stochastic_timing_design.md:534-540` rules no penalty place
   and the code agrees. Amend architecture.
2. `modulator_composition.md:44` names `v3_persistent_backward` as factor 2;
   the ruled version is `v4_failure_only` (2026-08-19). Amend the register.
3. `rules.py:98` defaults `delta_ratio = 0.5` (v2's value); every registered
   version from v3 on overrides it to 0.25. Harmless, but a reader of the
   code alone gets the wrong declared value — a comment, or the default
   moved to 0.25 with the registry as authority.
4. `sink_policy.md` (superseded) says the default is `censor`; the code's
   `retrace_sinks=False` default plus experiment 2 naming it on is the live
   rule. No action; cite `sink_retrace_design.md` only.

## Rulings owed (Marc)

- **R1** gadget explicit (recommended) or implicit.
- **R2** the extension's name.
- **R3** show the `Π_m` slot (recommended) or `F_v` only.
- **R4** the Marsan citation: which edition; on the download list.
- **R5** whether §4.4's prose is re-keyed to the symbols in the same pass or
  left for the integration check.
- **R6** the sensitivity section's key: is §7.1 the V6 table's row set, and
  is the assumption register §7.2 a ch5 unit or a ch4 closing paragraph.

## Validation gate

Marc has ruled R1–R6; a cue card for P2 exists (noun stubs only, per the
drafting pipeline) and Marc has dictated against it; the definition's
symbols are the ones §4.4, App. B and the ch5/ch6 sensitivity table use, with
no symbol defined twice.

## Hard constraints

- Drafting pipeline: no session-written prose in the tex; the definition is
  Marc's dictation against a cue card, the displays and notation table are
  the mechanical part a session may typeset.
- Numbers in the tex come from artefacts (generated tables), never typed
  (the notation table may be typed; it carries symbols, not values).
- The criterion's badge ceiling is untouched by any of this.

## Reading list

- `src/mtdsim/l3_simulation/movement/attacker.py` — the walk (§6), the
  interrupt and retrace paths.
- `src/mtdsim/l3_simulation/controller/outcome.py` + `rules.py` — `compose`
  and the `R · d` compiler.
- `src/mtdsim/l3_simulation/movement/net.py`, `timing.py`, `state.py` —
  `W`, `τ_p`, `Π_m`.
- `docs/implementation/pipeline/ogasp/stochastic_timing_design.md` §3 — the
  GSPN ruling and the SPN/DSPN rejections (already in the tex).
- `docs/implementation/pipeline/ogasp/success_failure_overlay_design.md` §1,
  `failure_weight_decomposition.md` §1–2, `lifecycle_consensus.md` §6.
- `docs/implementation/pipeline/ogasp/modulator_composition.md` — the
  factor register (amend item 2 of §9 there).

## Out of scope

The analytical (D1/CTMC) track in `petri_feasibility.md` — a different net,
solved not executed. The definition here is of the executed net; if the
section wants the CTMC isomorphism sentence, it is one clause with Murata
1989 and stops.
