# MTD effectiveness against the stealthy adversary (extraction notes)

> Two MTD-effectiveness papers extracted for §3 of the stealth/low-and-slow group
> ([`07_stealth`](../../notes/ch3_design/tactic_profiles/07_stealth.md), and by extension
> [`13_command-and-control`](../../notes/ch3_design/tactic_profiles/13_command-and-control.md) /
> [`14_exfiltration`](../../notes/ch3_design/tactic_profiles/14_exfiltration.md)). They price *how a
> shuffle degrades a stealthy operation* (detector reshuffling vs a stealth
> botnet; MTTC vs shuffle-rate and attacker skill) — §3 reset/sweep evidence, not
> a per-tactic dwell. FlipIt ([`persistence_reset_models`](persistence_reset_models.md))
> is the third stealth-reset source.
> Source files (both `docs/sources/tactic_profiles/step_d/7_stealth/`, gitignored):
> `2995272.2995280.md`, `electronics-14-02205.md`.

### Relevance class

**M** (MTD-mechanism / attacker-effect). §3 reset + sweep for the stealth group.

### Used in lit review

Stealth §3/§4 (MTD-effect rows); the tuned-group sweep (MTTC rises with shuffle
frequency and falls with attacker skill).

## Bibliographic anchor

- **Citation keys**: `venkatesan2016` (Venkatesan, Albanese, Cybenko, Jajodia,
  *A MTD Approach to Disrupting Stealthy Botnets*, MTD@CCS'16); `sharma2025`
  (Sharma, *Evaluating MTD Methods Using TTC and Security Risk Metrics in IoT*,
  Electronics 14(11):2205, 2025).
- **Pages cited from**: Venkatesan Abstract + §1–§2; Sharma Abstract + §1 + §"key
  contributions".

## Relevant artefacts

### Venkatesan 2016 — reshuffling detectors forces the stealthy botnet to re-plan

**Source locator:** Abstract; §1–§2 (stealthy botnets; detector placement)

**Paraphrase:** proposes an MTD that **periodically changes the placement of
network detectors** (centrality-based strategies) to disrupt *stealthy-botnet
data exfiltration* — the "architectural stealth" that routes exfil through relay
bots to avoid monitoring points ("cyber high ground") [fetched]. By creating
uncertainty about detector locations, it "increase[s] the attacker's effort and
likelihood of detection", **forcing botmasters to perform additional actions to
create detector-free paths**. Reduces successful-exfiltration probability
(validated in simulation; a lower-bound detection-probability algorithm given).

**Maps to:** [`07_stealth`](../../notes/ch3_design/tactic_profiles/07_stealth.md) §3 (a topology/
placement shuffle forces the stealthy adversary to *re-plan its route* — a reset
of the concealment gain, imposing re-work) and
[`14_exfiltration`](../../notes/ch3_design/tactic_profiles/14_exfiltration.md) §3.

**Disposition for this thesis:** verified [fetched] — §3 shape evidence.
**Scope caveat:** detector placement is IDS/monitoring-adjacent (IDS is culled
from the thesis defender set); relevance is the *shape* (a shuffle forces the
stealthy adversary to re-route), not a deployable mechanism. No dwell.

---

### Sharma 2025 — MTTC vs shuffle-frequency and attacker skill

**Source locator:** Abstract; §1; §"key contributions" (mean/min/max TTC metrics)

**Paraphrase:** develops **attack-path-based mean-time-to-compromise + security-risk
metrics** to evaluate shuffling/diversity MTD, and — the load-bearing part —
evaluates them "for different attacker skill levels and shuffling frequencies"
[fetched]. Confirms the two sweep axes for the tuned group: **MTTC rises with
shuffle frequency** (a faster shuffle delays compromise) and **falls with attacker
skill**. A McQueen-TTC-lineage metric applied to MTD, echoing
[`mttc_lineage`](mttc_lineage.md) and [`sharma`'s own](mtd_scan_disruption.md)
family.

**Maps to:** [`07_stealth`](../../notes/ch3_design/tactic_profiles/07_stealth.md) §3/§4 (MTD delays
compromise; the shuffle-frequency ÷ attacker-skill plane is the sweep) and the
tuned-group anchor generally.

**Disposition for this thesis:** verified [fetched] — confirms the sweep axes
(shuffle-rate, skill). IoT domain, simulation, TTC-lineage — a *shape* result,
not a per-tactic dwell.

## Open questions / things to verify

- Both are MTD-effectiveness *metrics* on models/simulations, not logs of MTD→APT
  effect. The transferable finding is the **direction and axes** of the effect
  (faster shuffle → longer MTTC / more re-work; higher skill → shorter), which set
  the §3 sweep, not a magnitude.
- Venkatesan's detector-placement is deception/monitoring, adjacent to but not
  identical to the substrate's SDR MTD — use for shape only.

## Out of scope for this thesis

Venkatesan's detector-placement optimisation algorithm and centrality-strategy
comparison; Sharma's IoT-specific security-risk formulation and smart-home case
study. The mechanism (shuffle forces re-work / delays compromise) is the load-bearing
part.
