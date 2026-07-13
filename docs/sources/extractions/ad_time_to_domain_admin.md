# Active Directory time-to-Domain-Admin — decoys, immunization, pen-test timeline (extraction notes)

> Three sources on the **privilege-escalation → Domain-Admin** race inside Active
> Directory, extracted for [`06_privilege-escalation`](../../notes/ch3_design/tactic_profiles/06_privilege-escalation.md)
> and [`11_lateral-movement`](../../notes/ch3_design/tactic_profiles/11_lateral-movement.md) (the two
> tactics AD attack-graphs interleave). They price the *structure* of the race to
> DA and how a graph-level defence slows it — §3/§4 evidence, not a metered dwell.
> Complements the macro race-to-AD anchor (Sophos ~3–16 h,
> [`breach_reports_macro_timing`](breach_reports_macro_timing.md)).
> Source files (all `docs/sources/tactic_profiles/step_d/6_privesc/`, gitignored):
> `ngo2024_ad_decoys_response_time_gecco_arxiv.md`,
> `herranz2023_surgical_immunization_ad_jnca.md`,
> `munaiah2019_cptc_attacker_behavior_esem.md`.

### Relevance class

**M** (MTD/deception mechanism) + **C** (calibration, structural). AD-graph
defence effect + an executed ATT&CK-timed campaign; no per-tactic rate.

### Used in lit review

Privesc/lateral §3 (structural AD defence slows the race to DA) + §4 (executed
ATT&CK timeline — gap-confirming: ordering, not dwell).

## Bibliographic anchor

- **Citation keys**: `ngo2024` (Ngo, Guo, Nguyen, *Optimizing Cyber Response
  Time on Temporal AD Networks Using Decoys*, GECCO'24; arXiv:2403.18162);
  `herranz2023` (Herranz-Oliveros et al., *Surgical immunization against lateral
  movement in AD*, JNCA 222, 2023); `munaiah2019` (Munaiah et al.,
  *Characterizing Attacker Behavior in a Pen-Testing Competition* (CPTC'18),
  ESEM'19).
- **Pages cited from**: Ngo Abstract + §"response time" defn; Herranz Abstract +
  §1–§2; Munaiah Abstract + §II–IV.

## Relevant artefacts

### Ngo 2024 — "response time" = first-decoy-trigger → DA compromise

**Source locator:** Abstract; §"response time" definition

**Paraphrase:** models decoy placement in AD as a Stackelberg game on **temporal**
attack graphs, and defines a metric squarely relevant to §3: **response time = the
duration from when attackers trigger the first decoy to when they compromise
Domain Admin** [fetched]. The defender maximises this over worst-case attack paths
(NP-hard; solved with evolutionary diversity optimisation). It is a *defender
detection-to-DA window*, i.e. how much time a decoy buys before privesc completes.

**Maps to:** [`06_privilege-escalation`](../../notes/ch3_design/tactic_profiles/06_privilege-escalation.md)
§3 (deception/decoys extend the privesc→DA window — a delay, not a reset) and §4
(the race-to-DA is a real, structured duration).

**Disposition for this thesis:** verified [fetched] — a defender response-time
metric, not attacker dwell. Deception (decoys) is out of the substrate's SDR MTD
set (scope caveat, per [`../specs/project_context.md`](../../workflows/project_context.md));
used for the *shape* of the privesc→DA race.

---

### Herranz 2023 — AD lateral movement as an infection; immunization slows spread

**Source locator:** Abstract; §1 (lateral movement = precursor); §2 (graph model)

**Paraphrase:** models AD lateral movement as an **infection (SIR-type) process**
on the trust/reachability graph, and shows that **immunizing a very small set of
high-centrality nodes** effectively slows spread [fetched]. The load-bearing
framing for us: "the time gained enables the opportunity to detect the attack,
mitigate its impact and/or track its source" — a graph-structure defence buys
*time* against privesc/lateral movement, and network structure governs how fast
the movement progresses.

**Maps to:** [`11_lateral-movement`](../../notes/ch3_design/tactic_profiles/11_lateral-movement.md) /
[`06_privilege-escalation`](../../notes/ch3_design/tactic_profiles/06_privilege-escalation.md) §3
(redundancy/structure-based mitigation slows the spread — a rate reduction, not a
reset) and §2 (structure governs movement speed).

**Disposition for this thesis:** verified [fetched] — structural (graph-immunization)
mitigation; a rate-slowing, not a per-tactic dwell. Epidemiological model, cf. the
worm cluster ([`worm_propagation_models`](worm_propagation_models.md)).

---

### Munaiah 2019 (CPTC'18) — an ATT&CK-timed pen-test campaign (ordering, not rate)

**Source locator:** Abstract; §II–IV (CPTC'18 dataset; ATT&CK codification)

**Paraphrase:** codifies one team's CPTC'18 campaign as a **chronological sequence
of MITRE ATT&CK tactics/techniques** — 44 events across 7 vulnerabilities, from
>500M logged events [fetched]. Demonstrates that an executed campaign *can* be
rendered as a timestamped ATT&CK tactic/technique sequence — but the contribution
is the *ordering/feasibility*, and the timing is anecdotal (a single competition
run), not a rate.

**Maps to:** [`06_privilege-escalation`](../../notes/ch3_design/tactic_profiles/06_privilege-escalation.md)
§4 (a real ATT&CK-timed campaign exists, but gives *sequence*, not per-tactic
dwell — gap-confirming, like [`rodriguez2024`](rodriguez2024.md)).

**Disposition for this thesis:** verified [fetched] — gap-confirming: even a
timestamped, ATT&CK-mapped campaign yields ordering, not a per-tactic rate. A
controlled competition, not APT.

## Open questions / things to verify

- Ngo/Herranz are *defence-placement optimisations* — the transferable finding is
  the **shape** (decoys/immunization *delay* privesc/lateral, they don't reset it),
  aligning with FlipIt's "reset is partial". Decoys are deception (out of SDR
  scope) — used for shape only.
- Munaiah's 44-event timeline has per-event timestamps in the underlying dataset;
  if a specific privesc→DA duration is needed, the CPTC'18 dataset (not this paper)
  would have to be mined — flagged, out of Step-D scope.

## Out of scope for this thesis

Ngo's EDO algorithm and NP-hardness proof; Herranz's centrality-metric comparison
and immunization-budget experiments; Munaiah's attacker-mindset pedagogy and
dataset-curation detail.
