# Mendonça 2023 — extraction notes

> J. Mendonça, J.-H. Cho, T. J. Moore, F. F. Nelson, H. Lim, D. D. Kim.
> "Performance impact analysis of services under a time-based moving target
> defense mechanism." *Journal of Defense Modeling and Simulation: Applications,
> Methodology, Technology*, vol. 20, no. 1, pp. 41–58, 2023.
> doi:10.1177/15485129211036937.
> Source file: `docs/sources/added_mendonca2023.md` (gitignored).
> Relevance to this thesis: the **closest published precedent** for the L3 OGASP
> Petri-net workstream — an analytical Petri-net model that *evaluates and
> compares* **time-based** MTD strategies (= the SDR scheduling this thesis
> evaluates), authored by the **Dongseong Kim** group that MTDSim descends from.
> The contrast that licenses the thesis's contribution: Mendonça models the
> **defender/service** with *no attacker*; this thesis puts a **CTI-grounded
> attacker** in the net.

## Bibliographic anchor

- **Citation key**: `mendonca2023`
- **DOI / URL**: 10.1177/15485129211036937
- **Pages cited from**: full text (§2.3, §3, §4; Tables 4–6; Figs 2–6)

## Extraction policy

Quote sparingly, paraphrase liberally; fair-use blockquotes carry a section/line
locator into the source markdown. Cross-links to spec rows / notes carry a
`→ [`...`]` pointer.

## Relevance class

**L — Load-bearing on methodology.** This is the methodological exemplar the L3
Petri-net feasibility study
([`../notes/2026-06-18_l3_petri_feasibility.md`](../../implementation/pipeline/ogasp/petri_feasibility.md))
points to for *analytical Petri-net evaluation and comparison of time-based MTD*.
It anchors the "why a Petri net" case (§2 of the study) and the four-classes-as-
four-parameterisations comparison apparatus (§5/§7), and it supplies the
**DSPN-not-CTMC** refinement (below) that the study's pure-SPN/CTMC framing had
missed.

## Relevant artefacts

### Concept 1 — DSPN is the right variant when the MTD trigger is a *deterministic period*

**Source locator:** §2.3 (lines 243–286); §3.2.2 (lines 445–477, the `TMTDi`
deterministic transition); Table 4 (`MTDi = 300 s`, line 1030).

**Paraphrase:** The authors use a **deterministic and stochastic Petri net
(DSPN)** — Petri nets with *two* transition kinds: **timed** transitions with
exponentially-distributed delays (job arrival, service, vIP-update) and
**deterministic** transitions with a *fixed* delay. The MTD trigger `TMTDi` is a
**deterministic** transition firing at a constant interval (300 s default),
because a *time-based* MTD shuffles on a fixed schedule, not on an exponential
clock. Immediate transitions (zero delay) model the job-drop logic (`Td1`–`Td3`)
gated by guard functions. The models are solved by **numerical analysis** (and
simulation) in the TimeNET tool — "other tools such as Mercury or SHARPE can be
used similarly" (§4.1, line 723).

**Quote (essential — the variant choice):**
> "This paper adopts an extension of Petri nets called *deterministic and
> stochastic Petri net* (DSPN) for evaluating services with or without an MTD
> mechanism deployed in SDN environments. Note that DSPN modeling allows the
> analysis of systems through numerical solution and simulation methods." (§2.3,
> lines 261–266)

**Maps to:** [`../notes/2026-06-18_l3_petri_feasibility.md`](../../implementation/pipeline/ogasp/petri_feasibility.md)
§2 (why a Petri net), §6.1 (tractability) and §6.3 (Markov semantics). **The
load-bearing refinement:** the study assumed an SPN with *exponential* firing so
the reachability graph is a clean CTMC (`τ = −Q_T⁻¹·1`). But the SDR scheduling
this thesis evaluates is **periodic** — so a *faithful* MTD-reset transition is
**deterministic**, which makes the substrate a **DSPN, not a pure CTMC**, and the
closed-form solve needs DSPN machinery (embedded Markov chain / supplementary
variables, as TimeNET implements), not just a matrix inverse. The baseline may
*approximate* the MTD reset as exponential to keep the clean CTMC (and declare
the approximation), or adopt a DSPN and accept the harder solve. Mendonça shows
the faithful choice is DSPN.

### Concept 2 — the comparison apparatus: one net per strategy, solve each, compare a metric panel

**Source locator:** §3 (five scenarios, lines 297–339); §4.3 + Table 6
(lines 901–917, 1191–1214); Fig. 9 (MTD-interval sweep, lines 982–1002).

**Paraphrase:** Five DSPN models are built — *No MTD*, *With MTD* (default,
shuffling breaks in-flight jobs), *undefined waiting* (finish jobs first, block
new), *defined waiting* (a fixed grace period, then shuffle), and *switchover*
(two servers shuffled alternately so jobs never break). Each is solved
independently and the *same eight-metric panel* (throughput, response time,
utilisation, blocking probability, blocked/dropped jobs, job-completion
probability, cost) is read off and **compared across strategies**; the MTD
interval is *swept* (100–600 s) to show its effect (Fig. 9). Switchover wins on
response time, job loss, completion and cost. This "one net per configuration →
common metric panel → compare, and sweep the MTD interval" is exactly the L4
shape this thesis needs.

**Maps to:** [`../notes/2026-06-18_l3_petri_feasibility.md`](../../implementation/pipeline/ogasp/petri_feasibility.md)
§5/§7 (the four GASP classes as four parameterisations of one shared net, solved
and compared) and [`../specs/architecture.md`](../../implementation/architecture.md) §(g) (the
L4 matrix: MTD mechanism × profile × interval — Mendonça sweeps the interval
axis). **Contrast:** Mendonça's five "configurations" are five *MTD strategies*
(defender side); this thesis's four are four *attacker profiles* (the GASP
classes). Same apparatus, opposite axis of variation.

### Concept 3 — honest parameterisation: ground what the literature gives, *declare* the rest

**Source locator:** §4.1 (lines 724–730); Table 4 (lines 1021–1042, the `?`-marked
rows).

**Paraphrase:** Input rates are sourced from prior work (Hu et al., Kim et al.,
Machida et al.; cost parameters from Chen / Elnozahy), and the parameters that
could not be sourced are **explicitly flagged** ("input parameters marked with ?
were reasonably estimated, as they were not found in the literature or product
specifications"). So the model grounds the rates it can and *marks the rest as
estimated* rather than implying they are measured.

**Quote (essential — the parameterisation honesty):**
> "The input parameters for the DSPN models were based on some previous work …
> The input parameters marked with ? were reasonably estimated, as they were not
> found in the literature or product specifications." (§4.1, lines 725–730)

**Maps to:** [`../notes/2026-06-18_l3_petri_feasibility.md`](../../implementation/pipeline/ogasp/petri_feasibility.md)
§6.2 (rate grounding) and [`../specs/provenance.md`](../../implementation/provenance.md). This
is the **template for the thesis's rate problem**: ground the *structure* from
CTI, and treat the un-groundable timing parameters the way Mendonça treats his
estimated rows — *declared notional, swept for sensitivity*, never presented as
measured. Note the asymmetry the thesis cannot escape: Mendonça's groundable
parameters are *defender/service* rates (arrival, service time, MTD interval),
for which a literature exists; the thesis's un-groundable parameters are
*attacker* rates, for which — as Bland 2020 and this survey confirm — **no
frequency-grounded source exists at all** ([`./bland2020.md`](./bland2020.md);
the GAP's `observation_count` is a recurrence count, not a rate, per
[`../specs/metrics_semantics.md`](../../implementation/metrics_semantics.md) §(f)).

### Concept 4 — the metric panel is *performance/QoS*, not security; the attacker is absent

**Source locator:** §3.1 (lines 354–357, the one-line attacker mention); §4.2
(metrics, lines 744–899); §4.4 (limitations, lines 1074–1077).

**Paraphrase:** The model has **no attacker structure**. An attacker is mentioned
once as motivation ("a scenario in which an attacker can compromise a specific
server") but never modelled; the limitation section concedes "we did not consider
security aspects in our model." Every metric is a **performance/QoS** quantity
(throughput, response time, job loss, cost), computed from stationary/transient
DSPN marking probabilities (`P{marking}`, `E{#place}`). There is no MTTC, no ASR,
no attack-success metric.

**Quote (essential):**
> "We did not consider security aspects in our model. We plan to enhance our
> models to analyze the services' performance and security aspects in an
> integrated way." (§4.4, lines 1074–1077)

**Maps to:** [`../notes/2026-06-18_l3_petri_feasibility.md`](../../implementation/pipeline/ogasp/petri_feasibility.md)
§2/§3 (the defender-vs-attacker inversion that *is* the thesis's contribution).
**This is the precise contrast boundary:** the established SPN/GSPN/SRN/DSPN-for-
MTD lineage (Mendonça, and the works it surveys — Cai, Connell, Maleki, ElMir,
Carroll, §5 lines 1112–1177) models the **defender/MTD system performance** with
an abstract-or-absent attacker; this thesis encodes the **attacker** (the CTI-
derived GASP) and reads **security** metrics (MTTC, ASR) off the net. The
metrics do *not* transfer (theirs are QoS, ours are attack outcomes); the
*apparatus* (analytical Petri-net, one-net-per-configuration comparison, interval
sweep) does.

### Concept 5 — a citable map of the analytic-MTD-modelling neighbourhood

**Source locator:** §5 Related work (lines 1112–1177).

**Paraphrase:** Mendonça's related-work section is a compact survey of *analytic*
MTD-evaluation models, several of which are the primer's missing anchors or
adjacent to them: **Cai et al.** (a "generalized performance evaluation and
comparison model for existing MTDs through DSPNs" — note Mendonça characterises
Cai as *DSPN*, where the primer's reference list called it GSPN; the variant
label is worth checking if Cai is ever obtained); **Maleki et al.** (a Markov-
model framework introducing "security capacity" as an MTD-effectiveness measure,
computing attack-success probability and attack cost — the *security*-metric
analogue this thesis wants); **Connell et al.** (analytic availability/performance
of generic MTD); **Carroll et al.** (network-address-shuffling analysis — limited
protection, connection-loss trade-off); **ElMir et al.** (cloud VM-migration
MTD). Useful as a literature-usage map for the lit review's MTD-evaluation
strand, and as a pointer to **Maleki** as the security-metric (attack-success/
cost) precedent that complements Mendonça's performance-only panel.

**Maps to:** [`../sources/LIT_REVIEW.md`](../lit_review/LIT_REVIEW.md) §IV/§V
(MTD-evaluation methods) and
[`../notes/2026-06-18_l3_petri_feasibility.md`](../../implementation/pipeline/ogasp/petri_feasibility.md)
§3 (literature-usage review).

## Disposition for this thesis

**Contrasted-against, as the methodological precedent.** The *apparatus* is
adopted as the model for the L3/L4 Petri-net workstream — analytical Petri-net
evaluation, one-net-per-configuration comparison, MTD-interval sweep, declared-
and-swept parameterisation. Three things are **contrasted, not inherited**:

1. *Modelling target.* Mendonça models the **defender/service performance** with
   no attacker; this thesis models the **CTI-grounded attacker** with MTD
   exogenous. The metrics invert (QoS vs MTTC/ASR).
2. *Variant.* Mendonça's **DSPN** (deterministic MTD-interval transition) is the
   faithful choice for *periodic* MTD and a refinement of the study's pure-SPN/
   CTMC framing — but it costs the clean closed-form (DSPN needs supplementary-
   variable / embedded-Markov solution). The thesis adjudicates DSPN-faithful vs
   CTMC-approximate explicitly (study §6.1/§6.3).
3. *Tooling.* Mendonça solves in **TimeNET / Mercury / SHARPE**; the study's
   baseline plan is SNAKES + custom `scipy.sparse` (or a PNML export). TimeNET/
   Mercury are a credible alternative path for the DSPN solve and a credibility
   hedge.

## Used in lit review

Not yet cited in [`../sources/LIT_REVIEW.md`](../lit_review/LIT_REVIEW.md) (the paper
was added to `docs/sources/` on 2026-06-18). Candidate placements: §IV/§V MTD-
evaluation-methods strand (analytic Petri-net evaluation of time-based MTD), and
as the methodological-precedent anchor the L3 Petri-net workstream is built
against — the same role architecture §(j) gives Rodríguez for the profiling
strand.

## Open questions / things to verify

- **DSPN vs CTMC for the MTD reset — design decision, flagged.** A faithful
  periodic-MTD transition is *deterministic* → DSPN → no clean `τ = −Q_T⁻¹·1`.
  Whether the thesis takes the DSPN-faithful route (TimeNET/Mercury) or the
  exponential-CTMC approximation (SNAKES + custom solve, declared approximation)
  is open and belongs to the L3 build (handoff Stage 1).
- **Cai variant label.** Mendonça (§5) calls Cai et al. a **DSPN** model;
  external search called it GSPN. Cai 2016 is **off-limits** (cannot be obtained),
  so this stays unresolved and Cai is cited only second-hand via Mendonça's and
  the primer's characterisations — flagged so no first-hand claim is made about
  Cai's formalism.
- **Maleki et al.** (security-capacity, attack-success/cost) is the *security*-
  metric precedent absent from Mendonça's performance-only panel; worth pulling
  if the security-metric grounding (MTTC/ASR-as-reward) needs a published anchor.

## Out of scope for this thesis

- The SDN/OpenFlow service-performance modelling (job queues, switch forwarding,
  vIP shuffling mechanics) — Mendonça's subject, not this thesis's; only the
  *modelling methodology* transfers.
- The QoS/cost metric panel (throughput, response time, job loss) — this thesis
  reads *security* metrics (MTTC, ASR), not performance.
