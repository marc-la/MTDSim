# Mean-Time-to-Compromise lineage — TTC refinements + Markov-MTD (extraction notes)

> Three sources extending the **McQueen time-to-compromise** family, extracted as
> the **per-state declared-dwell precedent** for the exploit-shaped tactics and as
> §3 MTD-effect evidence. They corroborate the corpus
> [`mcqueen2006`](mcqueen2006.md) anchor (1-day easy-exploit compromise), refine
> its skill model, and — Maleki — relate MTD strength to attacker time/cost.
> Feeds [`06_privilege-escalation`](../../notes/ch3_design/tactic_profiles/06_privilege-escalation.md)
> (and the exploit-shaped group generally).
> Source files (all `docs/sources/tactic_profiles/step_d/6_privesc/`, gitignored):
> `Estimating_a_Systems_Mean_Time-to-Compromise.md`,
> `The_-Time-to-Compromise_Metric_for_Practical_Cyber_Security_Risk_Estimation.md`,
> `2995272.2995273.md`.

### Relevance class

**C** (calibration) + **M** (MTD-mechanism). TTC-lineage per-state declared dwell
(the field's dominant declare-a-time precedent) + a Markov MTD success-vs-time
model.

### Used in lit review

Privilege-escalation §4 (per-state declared dwell corroboration); the method
note's "declare-and-sweep is the field norm" (TTC is the exemplar); §3 MTD-effect
(Maleki).

## Bibliographic anchor

- **Citation keys**: `leversage2008` (Leversage & Byres, *Estimating a System's
  Mean Time-to-Compromise*, IEEE S&P 6(1), 2008); `zieger2018` (Zieger, Freiling,
  Kossakowski, *The β-Time-to-Compromise Metric*, IEEE IMF 2018); `maleki2016`
  (Maleki, Valizadeh, Koch, Bestavros, van Dijk, *Markov Modeling of MTD Games*,
  MTD'16).
- **Pages cited from**: Leversage §"Process 1" (t₁ = 1 day; skill model); Zieger
  Abstract + §I–IV (β-TTC); Maleki Abstract + §1 (security capacity).

## Relevant artefacts

### Leversage & Byres 2008 — Process-1 mean = 1 day, skill-conditioned

**Source locator:** §"Process 1" ("mean time of one day, t₁ = 1 day"); §"skills
indicator"

**Paraphrase:** a McQueen-lineage MTTC method [fetched]. **Process 1 (attacker
has a known vulnerability *and* an exploit on hand) has a mean time of 1 day
(t₁ = 1 day)** — directly corroborating [`mcqueen2006`](mcqueen2006.md)'s
easy-exploit figure. Adds a **skill model**: a continuous skills indicator ∈ [0,1]
(0 = beginner, 1 = highly skilled) scaling the number of readily-available
exploits (m = 450, McQueen's value from public exploit sites). So the declared
per-state dwell is skill-parameterised, not a single point.

**Maps to:** [`06_privilege-escalation`](../../notes/ch3_design/tactic_profiles/06_privilege-escalation.md)
/ [`03_initial-access`](../../notes/ch3_design/tactic_profiles/03_initial-access.md) §4 (the 1-day
easy-exploit dwell, independently restated; the skill axis supports a *range*
around the anchor) + method (per-state *declared* dwell — the precedent our Tier-3
tactics follow).

**Disposition for this thesis:** verified [fetched] — corroborates McQueen's
declared 1-day value; the skill model justifies a swept range.

---

### Zieger 2018 — β-TTC: continuous, CVSS-informed, β-distributed skill

**Source locator:** Abstract; §III (continuous TTC); §IV (β-skill); §VI (exploit
complexity)

**Paraphrase:** a formal refinement of McQueen's TTC [fetched]. Embeds the metric
in the continuous domain, folds in **CVSS vectors** and models **attacker skill as
a β-distributed random variable** (β-TTC), validated on a national-CERT
vulnerability database — "more realistic predictions than the original TTC" while
staying simple. Reinforces that TTC "has evolved into one of the most successful
cybersecurity metrics in practice" — i.e. declaring a per-state compromise time
*and refining it with CTI* is the mainstream method, exactly the register the
method note claims.

**Maps to:** [`06_privilege-escalation`](../../notes/ch3_design/tactic_profiles/06_privilege-escalation.md)
§4 (a CVSS-informed refinement of the exploit-shaped dwell) + the method note
(declare-and-refine precedent; supports a distribution over the anchor, not a
point).

**Disposition for this thesis:** verified [fetched] — method precedent; a
technique/CVE-level TTC (not per-ATT&CK-tactic), consistent with the survey's gap
finding that empirical timing exists only at CVE granularity.

---

### Maleki 2016 — Markov MTD: adversary success rises with time/cost; "security capacity"

**Source locator:** Abstract; §1; §3 (framework); §4 (IP-hopping / hiding
applications)

**Paraphrase:** a Markov framework for MTD analysis [fetched]. Provides "general
theorems about how the **probability of a successful adversary defeating an MTD
strategy is related to the amount of time/cost spent by the adversary**", and
defines **security capacity** — a measure of MTD strength depending on
MTD-specific + system parameters. Multi-level MTD compositions analyse by
combining per-strategy analyses. Applied to IP-hopping and single/multiple-target
hiding.

**Maps to:** [`06_privilege-escalation`](../../notes/ch3_design/tactic_profiles/06_privilege-escalation.md)
§3 (MTD-effect: attacker success is a rising function of time-under-MTD → a faster
reset caps success; the sweep axis is the MTD parameter) and the tuned-group §3
generally.

**Disposition for this thesis:** verified [fetched] — §3 mechanism (success vs
time-under-MTD); analytical, not a per-tactic dwell.

## Open questions / things to verify

- TTC-lineage values are **technique/CVE-granularity** declared per-state dwells,
  not per-ATT&CK-*tactic* — they are the *precedent* our tactic layer generalises,
  and the 1-day figure is a corroborated anchor, not a transplant.
- Leversage/Zieger exact skill-curve parameters were read at definitional
  granularity; if a specific per-skill day-count is cited in §5, pull the figure.

## Out of scope for this thesis

McQueen's original 3-process TTC derivation (already in [`mcqueen2006`](mcqueen2006.md));
Zieger's CVSS-DAF format details and CERT-database evaluation; Maleki's security-capacity
proofs and IP-hopping numerics.
