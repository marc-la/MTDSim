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
   cost, not routing: the dwell is cut short and the time is spent, but the place
   exercised no capability, so there is no action to lose and the token routes on
   `none` (base proportions) exactly as if the dwell had elapsed. *(Stands.
   A 2026-09-13 "correction" that read D-21's "mid-dwell interrupts are read as a
   failure verdict" as a routing claim was wrong and is withdrawn the same day:
   `movement/attacker.py` routes the dwell-only branch on `VERDICT_NONE`
   regardless of interruption; D-21's wording is the gate's exposure accounting.
   Landed in ch4 §4.4.1 in Marc's framing.)*
7. **A7 one token.** The AND structure Attack Flow preserves is vacuous
   under a single token; a constraint on parameters, not the formalism.
8. **A8 consensus staging.** `s(·)` and hence `Δ` are imported from five
   lifecycle models; ATT&CK itself imposes no order.
9. **A9 synthetic pre-intrusion structure.** Three declared edges, share `s`.
10. **A10 retrace.** A structural dead end is retraced; a stall is not.
11. **A11 substrate invariants.** Penalty, interval, and the six verbs are the
    environment's, held fixed across arms.
12. **A12 no cross-run memory; no scheme awareness.** `h` is within-run.

## 8. The section design — §4.3 in the shape of a formalism section

### 8.1 The convention, read off the corpus

Three of the chapter's own precedents present a Petri-net formalism, and
they agree on the shape:

- **Bland 2020 §2.1** (the exemplar, `docs/sources/lit_review/4_bland2020machine.md:85-130`):
  the standard net stated as a tuple, attributed ("Following Murata 1989 and
  Reisig 2013, a standard Petri net can be formally defined as a 6-tuple
  `PN = (P, T, W, M0, B, L)`, where:"), the elements in an **enumerated
  "where:" list**, one line each; a sentence of firing semantics; a pointer
  ("for more detailed explanations ... see Murata"). Then the paper's own
  formalism **as an extension**: "The PNPSC formalism used in this work is an
  extension of Petri nets", a larger tuple whose **first item is "as defined
  earlier for a standard Petri net"** and whose remaining items are the new
  elements, each defined in one line. Then the nets drawn in the genre
  (`figure_table_conventions.md` §d5: circles = places, bars = transitions,
  IDs on nodes) with **companion ledger tables** (ID | meaning | rate).
- **The ICS GSPN paper** (`docs/sources/tactic_profiles/step_d/0_cross_tactic_timed_models/1-s2.0-S0306454921007404-main.md:290-296`):
  a two-sentence gloss (bipartite graph; immediate vs timed drawn as solid
  vs empty bars), then "Formally, a GSPN = (P, T, A, M0, λ) is defined as a
  5-tuple (Chiola et al., 1993) where …" — the same enumerated form.
- **Mendonça 2023 §2.3** (`docs/sources/lit_review/added_mendonca2023.md:245-286`):
  a background paragraph (places, transitions, immediate vs timed,
  exponential delay, firing semantics) that delegates the full definition
  ("interested readers can be referred to Marsan et al. and Zimmermann").
- The lineage (Zhang 2023 §3.2) names Petri nets in prose only, citing
  Cai 2016 — no tuple. That is the floor the section already sits on.

So the convention is: **attribute, state the standard tuple once, define the
work's own net as an instance or extension with "as defined earlier"
reuse, draw it in the genre, ledger the IDs.** No theorem environment
(none of the three uses one, and the tex loads no `amsthm`); an
enumerated list under a display is the form. Numbered display equations
are already the house rule for definitions (`literature_conventions.md`
rule 1, for metrics) and carry over.

### 8.2 The section, paragraph by paragraph

The existing four-paragraph spine survives; the formalism is inserted as
P2 and the other three paragraphs are re-keyed to its symbols by one
clause each. Marc's sentences are not rewritten — the additions are the
definitional block and the symbol clauses.

**P1 — motivation and the ruled-out structures (exists, ~150 w).** Stays
as dictated. One clause added at the first naming of the GSPN: the
attribution and the pointer, in the corpus's form — "a GSPN
\citep{marsan1984} … ; for the full semantics see \citet{marsan1995}".
The SPN/DSPN rejections and the MTD precedents already stand. This is the
"why this formalism" paragraph every exemplar opens with.

**P2 — the formalism (new; replaces the current P2; ~200 w + two displays +
one enumerated list).** Three moves, in Bland's order:

1. *The standard net, once.* One sentence and the tuple, attributed:
   `GSPN = (P, T_I, T_T, I, O, W, M0)` — places, immediate and timed
   transitions, input and output arcs, the weight/rate function, the
   initial marking; a marking enabling an immediate transition is
   vanishing, otherwise tangible; timed transitions fire after an
   exponential delay, immediate transitions in zero time, with
   priority. Inhibitor arcs and priorities beyond immediate-over-timed are
   named as unused. (Ruling R1 is answered here: the gadget is what makes
   `T_I` and `T_T` both non-empty.)
2. *The profile net, as an instance.* "A profile net is a GSPN
   `N_c = (P_c, T_I, T_T, I, O, W_c, M0)`, where:" and the enumerated list
   in Marc's words — `P_c` the tactics of profile `c` (v19.1); `T_T` one
   timed transition `τ_p` per tactic, rate `1/μ_p`, immediate when
   `μ_p = 0`; `T_I` the tactic-pair transitions `t_{pq}`, one per observed
   pair, no self-loops; the arcs through the decision place; `W_c` the
   flow-proportion weights (Eq. 4.1 as a display: `w_c(p,q) = |F_c(p→q)| /
   Σ_{q'} |F_c(p→q')|`); `M0` one token at reconnaissance. Then the
   sentence the current P2 already carries in prose: "one construction,
   four parameterisations" (plug and play = `P_c`, `W_c` vary, nothing else
   does).
3. *The extension, stated.* "The net departs from a GSPN in one respect."
   The immediate weights are not constants: at each firing of `τ_p` the
   environment returns a verdict `v ∈ {success, failure, none}` and the
   weights out of `p` are recomposed as Eq. 4.2:

       W(t_{pq} | v) = w_c(p,q) · F_v(p,q) / Σ_{q'} w_c(p,q') · F_v(p,q')

   with `F_v` the declared conditioning factor (identity on success and
   none; the failure matrix of §4.4.1 otherwise) and the optional history
   product `Π_m` shown or not per R3. Structure, arcs and marking are
   untouched by it; a timed transition may be pre-empted by the
   environment (the MTD interrupt, §4.4.2). That is the whole extension,
   and it is what the section's title now earns.

**P3 — the pre-intrusion overlay (exists, ~110 w).** Stays. One clause
re-keys it: the overlay is a second immediate-transition set `T_S`
(three transitions, shares `s`), merged into `W_c` by the share rule —
one short display or one sentence (`w = s` out of an island place;
observed weights scaled by `1 − Σs` otherwise). "Sub-Petri-net in its own
right" is then literally true and says which elements it adds.

**P4 — the limits handed to L4 (exists, ~60 w).** Stays. Re-keyed by
naming the symbols: the parameters are `μ` and the exponential family;
the mechanics are `F_v` and the retrace rule, both defined in §4.4 in this
section's language. (The §4.4 re-key itself is Marc's later pass.)

### 8.3 The figure — design (revised 2026-09-08, after Marc's "show the shape" ask)

**Status 2026-09-08 (evening): BUILT.** `tools/gspn_gadget_figure.py` →
`docs/thesis/figures/fig_4-3a_gspn_gadget.{tex,pdf}`, included at natural
size (451 pt of 455.24), Figure 4.2 on body p. 21, build clean. R7 ruled
(a): `T_I` = positive-weight pairs, one sentence added after P2's
enumerate; panel (b) draws eight bars. Words moved out of the panel into
the caption (Marc's ruling); the caption is session-drafted and flagged
for the voice pass. Rows in (b) are in descending `w_c`, axis order within
ties. Remaining: Marc's caption/voice pass; the App. B transition ledger.


`fig:gspn-gadget`, placed after P2. The reader may never have seen a Petri
net, so the figure's job is the **shape** the tuple names: circles, bars,
the token, and the fan of weighted immediate transitions the extension acts
on. Two panels, one generator (`tools/gspn_gadget_figure.py`, to write),
natural size, portrait, `\textwidth` = 455.24 pt; helvet face, greys, one
accent. A prototype was rendered this session (scratchpad only, not in the
repo) and the layout below is what it settled.

**Drawing convention (Marsan's, decoded in an in-figure legend):**

| Element | Symbol | Drawn as |
|---|---|---|
| tangible place (tactic) | `p`, `q` | solid circle; the token dwells here |
| vanishing place (decision) | `p̂` | dashed circle — the same shape, marked as left in zero time (Marsan draws no distinct symbol; the dash is ours and the legend says so) |
| timed transition | `τ_p` | hollow rectangle, label "rate 1/μ_p" |
| immediate transition | `t_pq` | thin solid bar, weight beside it |
| token | — | black dot inside the place; `M_0` = one token |
| arcs | `I`, `O` | grey arrows, weight one so never labelled |

**Panel (a) — generic gadget, the picture of Eq. 4.1 instantiated.** Left to
right: `p` with the token → `τ_p` → `p̂` → fan of `k` bars `t_{pq_1}…t_{pq_k}`
with `w_c(p,q_i)` under each → `q_1…q_k` (with a `⋮`). Legend on the right,
inside the figure (genre convention, alshamrani-style). No accent in (a).

**Panel (b) — the same gadget on one real place.** Ruling recommended:
**initial access in the exfiltration profile**, not collection. Reasons:
(i) it is the entry place of the observed net (`M_0` without the overlay);
(ii) `μ_p = 4.5 s` is a substrate-priced anchor, so the timed transition
carries a number the reader met in §4.2; (iii) under a failure verdict the
foothold-gate rule moves 75 % of the row's mass to reconnaissance (0.062 →
0.750), which is the extension made visible in one line — collection's
failure row only shifts 0.571 → 0.509. The cost is a fan of ten bars; at a
0.76 cm row pitch that is 7.6 cm tall and reads fine at 8 pt.

Layout of (b): gadget on the left as in (a); the ten `t_pq` bars in a
column; the ten destination places in a column with their display names
(shared tactic axis, `_tactic_axis`); then **two ledger columns to the right
of the places**, headed `w_c(p,q)` and `W_c(t_pq | failure)` — the second in
the accent, because the verdict-conditioned column is the one thing the
figure is about (§b2). Order of rows: descending `w_c`, zero-weight rows
last (or the net's own order — Marc's call; prototype used descending).
A short note inside the panel (or the caption) says: ten out-transitions;
two carry base weight 0 under the primary corpus variant and cannot fire;
a failure verdict multiplies by `F_failure(p,q)` and renormalises (Eq. 4.4);
under success the base weights stand.

**Numbers the generator reads, never types** (verified this session):
`data/ogasp/petri/objective_exfiltration_structural.json` initial-access
row, `weights.operator_dedup.weight`: execution .312, persistence .250,
credential-access .125, C2 / discovery / lateral-movement / reconnaissance /
stealth .062 each, collection 0, privilege-escalation 0;
`data/ogasp/controller/overlays/v4_failure_only/failure.json`
`by_source["initial-access"]` (`v` = R·d): reconnaissance 0.9 (rule
`backward`, δ = −1), the eight forward/lateral rows 0.02 (`ia_gate_foothold`,
d = 1), collection 0.005 (d = 0.25); routed (`w·F / Σ`): reconnaissance
.750, execution .083, persistence .067, credential-access .033, the five
.062 rows .017 each, the two zero rows 0. `μ_p` from
`tactic_durations.json` (`initial-access.duration_s`). The generator should
recompute the routed column with the same function the controller uses
(`overlay.compose`), not re-implement Eq. 4.4, so the figure cannot drift
from the runtime.

**Why a transition can carry weight 0 (Marc's question, 2026-09-08, answered
from the code).** The transition set and the weights come from two different
objects. `T_I` is handed down from L2: the GASP is the *surface* subgraph
(gasp_schema.md Decision 4, `l2_subgraph/selector.py:61-88`) — its node set
is every technique used by the profile's flows, and its edge set is every
GAP technique-edge whose **both endpoints** are in that node set, whether or
not a flow of this profile walked the edge. The structural net then keeps
one transition per tactic pair with ≥1 such technique-edge (the
no-synthesis invariant). `w_c` counts only the profile's own flows (distinct,
under the chosen corpus variant). So a transition exists whenever the
profile uses both techniques, and its weight is 0 whenever none of the
profile's counted flows made that move. Two mechanisms, both present in
panel (b):

- **inherited edge** — initial-access → privilege-escalation via
  T1189 → T1068: the only flow that walked it is REvil, which is in the
  exfiltration+impact class; both techniques occur in exfiltration flows, so
  the edge is in the exfiltration GASP with numerator 0 under *both* variants;
- **dedup-removed backing** — initial-access → collection via T1078 → T1005:
  backed by fin13_case_2 alone (raw weight 0.045); operator dedup keeps one
  representative per operator cluster and drops fin13_case_2, so the primary
  numerator is 0 while `raw` gives it mass.

Count across the nets (computed 2026-09-08):

| profile net | transitions | zero under primary | inherited (raw = 0) | dedup-removed (raw > 0) |
|---|---|---|---|---|
| exfiltration+impact | 72 | 22 | 22 | 0 |
| exfiltration | 109 | 34 | 18 | 16 |
| impact | 76 | 33 | 30 | 3 |
| none/C2 | 57 | 15 | 13 | 2 |
| aggregate | 122 | 8 | 0 | 8 |

(The aggregate has no inherited edges by construction: every GAP edge is
walked by some flow of the union.) At runtime a zero-weight transition is
present and never fires (`movement/net.py:223`); every factor is
multiplicative, so no verdict can revive it; only the uniform-weight
ablation prunes to the positive-weight graph, on purpose, to keep both arms
on the same reachable set.

Marc's reading (2026-09-08): "a profile is a subset of the aggregate graph
with the non-existent transitions zeroed rather than removed, so the
aggregate skeleton shows through; an implementation nuance, not a logical
one; I wouldn't do it." Correction: the profile net is *not* the aggregate
skeleton — membership is decided by the profile's own technique set
(exfiltration carries 109 of the aggregate's 122 pairs; the 13 missing
pairs have a technique the profile never uses and are absent, not zero).
Zero weight arises only for pairs where the profile uses both techniques
but none of its counted flows made the move. So: technique membership
decides existence, flow walks decide weight — two objects, and the second
one is the logically meaningful one.

**Ruling owed (R7) — what `T_I` is in the formalism.** Two options:

- **(a) `T_I` = the positive-weight pairs**, `{t_pq : w_c(p,q) > 0}`. The
  formalism is then the logical object Marc would build; the implementation
  carries the wider L2 pair set and lets `w_c = 0` silence the rest. The two
  are behaviourally identical: an immediate transition with weight 0 has
  firing probability 0 in every marking, and every factor multiplies, so no
  verdict or modulator can revive it; the reachable graph, the stall
  condition and the embedded chain are the same. One sentence in P2 states
  the equivalence and the section is honest without reverse-fitting. Costs:
  `T_I` becomes variant-dependent (`raw` has more positive pairs) — fine,
  `N_c` is defined per corpus variant and the reported one is
  `operator_dedup`; and panel (b) draws eight bars, not ten. Consistent with
  the uniform-weight ablation (already the positive-weight graph) and with
  P3 (the overlay adds transitions the observed net lacks, e.g.
  recon → initial-access). **Recommended.**
- **(b) `T_I` = the L2 pair set**, `w_c ≥ 0`. Faithful to the file; needs the
  "may be 0, never fires" clause and the two-mechanism explanation in the
  prose or an appendix; the figure shows the zeros.

Either way the failure-floor zero is a different thing: it zeroes a *factor*
on a transition that exists, for one firing (P2's ruled sentence).

The full profile net is **not** drawn here: the ladder figure
(`fig:pipeline`, L3 rung) already draws one profile's net whole, and a
15-place / 109-transition net at page width was the fig:l1-graph lesson.
The ledger tables the genre pairs with the figure go to App. B: places
(ID | tactic | `μ_p` | anchor) is already Table 4.4 / B.4; transitions
(ID | pair | `w_c` per profile) is a new generated table, one per profile
or one wide table — Marc's call at the appendix pass.

Caption owed (session-drafted, voice pass): decode circles / dashed circle /
hollow bar / solid bar / token, name the profile and place of (b), and say
the accent column is the failure-verdict weight of Eq. 4.4.

### 8.4 The notation table

`tab:gspn-notation`, after the figure or at the head of App. B: Symbol |
Element | Meaning | Declared in. Rows: `P_c, τ_p, μ_p, t_{pq}, w_c, T_S,
s, M0, v, F_v, φ, A, ν, Π_m, γ, δ, z, R`. Typed (symbols, not values);
it is also the key the ch5/ch6 sensitivity table reads from.

### 8.5 Cue card for the P2 dictation (noun stubs only)

- attribute: GSPN, Marsan/Conte/Balbo 1984; full semantics Marsan et al. 1995
- tuple `(P, T_I, T_T, I, O, W, M0)`; tangible / vanishing; immediate zero
  time, priority; timed exponential; no inhibitor arcs used
- profile net `N_c`; `P_c` = tactics present in `c`, v19.1; counts 15/13/14/13
- `τ_p` one per tactic, rate `1/μ_p`; `μ_p = 0` → immediate (resource development)
- `t_{pq}` one per observed pair; no self-loops (dwell carries them)
- decision place `p̂` — the gadget; timed then immediate; the figure
- `w_c(p,q)` flow proportion, distinct flows, out-normalised; operator-dedup
  corpus 29; raw 38 robustness; closed world; recurrence not likelihood
- `M0` reconnaissance (overlay) / initial access (observed-only)
- one construction, four parameterisations (plug and play)
- the extension: verdict `v` from the simulator at each firing; Eq. 4.2;
  `F_success = 1`, `F_none = 1`, `F_failure` = §4.4.1; structure fixed;
  pre-emption by MTD; (`Π_m` if R3)
- forward pointers: §4.4.1 values, §4.4.2 loop, App. B ledgers

### 8.6 Budget

P2 grows from ~110 to ~200 words plus two numbered displays and an
enumerated list (word-cheap); P1/P3/P4 gain one clause each. The section
sits at ~470 against a 1-unit ledger already; the overdraft is claimed
explicitly as the formalism (the writing guide's ledger pass reconciles
at assembly). The figure and notation table are outside the word count.

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
- **R7** what `T_I` is — RULED (a) 2026-09-08: positive-weight pairs; the implementation's zero-weight carrier is stated as equivalent in P2 — §8.3.
- **R6** the sensitivity section's key: is §7.1 the V6 table's row set, and
  is the assumption register §7.2 a ch5 unit or a ch4 closing paragraph —
  RULED 2026-09-13 and APPLIED (assumptions half): **neither a ch5 unit nor a
  closing paragraph; each assumption lives in ch4 prose at the symbol it
  constrains.** A1, A2, A3, A9 were already stated; A4, A5, A6, A7, A8, A10,
  A11, A12 landed as sentences on 2026-09-13 (dated `% [2026-09-13: ...]`
  trails at each anchor), after Marc ruled on a fourteen-item proposal. The
  design's C1 merge (one register, assumptions as held rows) is REVERSED by
  Marc on separation of concerns — see the ch5 design handoff §16. §7.1's
  swept rows become `tab:parameter-register`'s only content (re-cut pending);
  its environment rows go to §5.2's factor tables.

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
