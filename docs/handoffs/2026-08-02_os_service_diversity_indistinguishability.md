---
status: open
created: 2026-08-02
---

# Classify two substrate behaviours that make OS Diversity and Service Diversity the same mechanism against this attacker — and decide what the defence family's true cardinality is

**This is a classification-and-disposition brief, not a fix brief.** Two
behaviours were found while cross-examining the axis-6 redesign. Both are
`documented-nowhere` candidates under the intent spec's §c procedure, which makes
them *candidate* divergences and nothing more — **only Marc's disposition makes
either a bug**, and neither has been touched. What is not in doubt is the
measured consequence, which is recorded below and reproduces in two independent
data sets.

The reason this earns a brief rather than a line in an audit is the second half
of the title. If the two diversity mechanisms are one mechanism, the defence
family the project reports over has four members and two distinct effects, and
that bears on the headline result.

## 1. State of play — what was found, and what is certain

### 1.1 OS Diversity's selectivity is inert (certain, verified live)

`ServicesGenerator.service_is_compatible_with_os` (`services.py:387-402`) is:

```python
return service in list(self.os_services[os_type][os_version].keys())
```

The dictionary's keys are service **name strings** (`gen_services`,
`services.py:404-420`); `service` is a `Service` **instance**; and
`Service.__eq__` (`services.py:304-307`) returns `False` for any non-`Service`
operand. The membership test therefore evaluates `Service == str` and can never
be true.

Verified by running it rather than by reading it: a service drawn from
`get_random_service(os, version)` tested against **its own** OS and version
returns `False`, and returns `False` against all four OS types at every version.

The consequence is in `osdiversity.py:31-45`: the branch guarded by
`if not service_is_compatible_with_os(...)` always fires, so OS Diversity
replaces **every** non-target service on **every** non-endpoint host, every time
it runs. It is not doing nothing — **it is doing a complete service shuffle**,
plus an OS relabel, and the direction is *more* aggressive than the intent
describes rather than less.

### 1.2 The OS relabel reaches this attacker through nothing (certain)

Two routes exist by which a host's OS could matter to exploitation, and neither
is live for the movement attacker.

**The success gate is commented out.** `Vulnerability.network(host=...)`
(`services.py:132-155`) is passed the host — `attack_operation.py:487` supplies
`adversary.get_curr_host()` — and then ignores it, because the gate that would
act on it is inherited commented-out code:

```python
# if self.has_os_dependency and host is not None:
#     if host.os_type not in self.vuln_os_list:
#         return 0.0
```

So whether an exploit succeeds depends on `complexity` alone. With
`VULN_PROB_DEPENDS_ON_OS = 0.8`, most vulnerabilities carry a populated
`vuln_os_list` that is never consulted for success.

**The one live coupling is a time effect, and the movement layer declines it by
design.** `exploit_time` (`services.py:106-124`) applies `×2.5` when the
vulnerability is OS-dependent and the host's OS is not in its list. But `step()`
— the movement layer's entry point — calls
`_do_exploit_vuln(..., driven=True, charge_time=False)`
(`attack_operation.py:747`), and that method's own docstring already states the
consequence:

> what goes is the substrate's own pricing of the attempt, along with the
> mechanisms that only ever expressed themselves through that price (the
> complexity scaling, the OS-mismatch multiplier, and the per-instance
> re-exploit discount, ATK-04). Those are MTDSim's model of what an exploit
> costs, and a driving layer that supplies its own durations is declining to
> use it.

This second point is **not a candidate divergence** — it is the S3-R seam
working exactly as documented. It is recorded here because it is half the reason
the OS relabel is inert, and because of §1.4.

### 1.3 The measured consequence — the two mechanisms are one (certain)

The prediction from §1.1 and §1.2 is that OS Diversity should behave as Service
Diversity does. It does, in both available data sets.

**Experiment 2's own recorded rows** (movement arm, 200 s, `interval_report`
over distinct hosts) place them as an **unseparated adjacent pair**:

| condition | hosts | 95 % CI |
|---|--:|--:|
| complete_topology | 0.640 | ± 0.200 |
| ip_shuffle | 0.720 | ± 0.202 |
| os_diversity | 3.460 | ± 0.502 |
| service_diversity | 3.700 | ± 0.588 |
| none | 5.240 | ± 0.495 |

`unseparated_adjacent_pairs` returns exactly two pairs:
`(complete_topology, ip_shuffle)` and `(os_diversity, service_diversity)`.

**The iterated-cost-model family sub-study** (2026-08-02, 50 runs per cell,
`v2_partial`) reproduces it independently across three arms:

| arm | condition | hosts | blocked fraction | interrupts |
|---|---|--:|--:|--:|
| ablation | os_diversity | 2.42 | 0.223 | 39.0 |
| ablation | service_diversity | 2.64 | 0.219 | 39.4 |
| declared | os_diversity | 1.76 | **0.307** | 39.0 |
| declared | service_diversity | 1.58 | **0.307** | 39.0 |
| AB | os_diversity | 1.92 | 0.229 | 34.7 |
| AB | service_diversity | 2.04 | 0.227 | 35.0 |

Blocked fraction agreeing to three decimal places over 50 runs each, with
interrupt counts identical, is what two labels on one mechanism look like.

**The good news for the record's integrity: no recorded conclusion separates
them.** The pair is unseparated in experiment 2's own interval report, so nothing
that was claimed depended on the distinction. This is a finding about what the
defence family *is*, not a correction to a claim.

### 1.4 The other pair, which has a different cause and the same effect

`(complete_topology, ip_shuffle)` is also unseparated, and the enumeration sweep
found the mechanism: **`IPShuffle` assigns each non-endpoint host a fresh random
IP, and no attacker path reads `host.ip`** — the attacker works entirely on node
ids. Its entire measured effect is the interrupt plus the network-layer cursor
clear, both of which Complete Topology Shuffle also delivers.

So the four-mechanism defence family resolves to **two distinct effects, each
appearing twice**, and both pairings are explained by code rather than by
coincidence. That is the substantive finding of this brief.

### 1.5 What is at stake, stated carefully

**The E5 ranking inversion survives, and its statistic is weaker than four points
suggests.** The headline (`experiment_02_findings.md` §9) reports
ρ = −0.893 over four mechanisms. The *claim* — that the position-destroying
family and the diversity family swap places between the two attackers — is a
family-level 2 × 2 contrast, and both families are genuinely represented, so the
result stands. What does not stand unqualified is the impression that four
independent mechanisms produced it. If two of the four points are duplicates,
the effective degrees of freedom behind that correlation are lower than the
number of rows implies, and the record should say so.

**No re-run is implied.** Every recorded figure is a record of the substrate as
it is, per the standing precedent. This brief asks for a classification and a
disposition, and — if the disposition is to change anything — a decision about
what happens to the family's cardinality in the reporting.

## 2. Classification status — what the intent spec already says

Run the §c procedure against
[`../implementation/mtdsim_intent_spec.md`](../implementation/mtdsim_intent_spec.md)
before forming any view. What is already on record:

- **IS-MTD-06** (OS Diversity): *"randomly change the OS on each host; services
  **incompatible with the new OS** are also randomly changed"* — Brown §III-B(6),
  Zhang §4.3.1.4. The audit
  ([`../implementation/intent_conformance_audit.md`](../implementation/intent_conformance_audit.md)
  line 83) marks it **CONFORMS (delta)** and lists three deltas: latest-version
  replacement (since fixed by D-05), exposed hosts exempted, and OS version index
  preserved.

  **"The compatibility test can never return true, so all services are always
  replaced" is not among them.** It is absent from the spec row and absent from
  the audit's delta list, which by the §c procedure makes it
  `documented-nowhere` — a *candidate*, and the audit row's CONFORMS verdict was
  reached without it in view.

- **IS-TIM-06** already records the `×2.5` OS-mismatch multiplier as a
  **beyond-paper term**, so that half is on the record as an inherited addition
  rather than an omission.

- The commented-out `network()` gate is **not** covered by an IS-ID. The audit's
  line 218 discusses OS-dependent vulnerabilities generally. Whether the gate is
  separately dispositionable is an open question, not a settled one.

**Precedent worth reading before deciding: IS-MTD-05.** The sibling row is
recorded as `DIVERGES-DOCUMENTED-NOWHERE` and was described as
"deliberate-looking, self-consistent — candidate design choice, not obviously a
bug", and Marc later ruled it a fix (D-05, 2026-07-29, goldens re-baselined).
That is the closest analogue to the decision this brief asks for, including its
cost.

## 3. Recommended approach

**Classify first, in three separate decisions, because they are independent and
have different costs.**

**Decision A — the compatibility test.** This is the cheapest and the most
clear-cut. A `Service` compared against a list of `str` cannot be a design
choice in any reading; the question is only whether the *behaviour it produces*
(always replace) is one. Note that the fix direction is not obvious: repairing
the comparison would make OS Diversity **less** aggressive than it is today, and
would move every recorded MTD figure that includes it. Options are (i) repair the
comparison so the mechanism becomes selective as IS-MTD-06 describes, (ii) leave
it and record the behaviour as a documented divergence, since "replace all
services" is exactly IS-MTD-05's operative reading and the mechanism is
self-consistent under it, or (iii) repair it and accept the golden re-baseline.

**Decision B — the commented-out OS gate.** Uncommenting it would make OS
Diversity meaningful against exploitation for the first time, which would give
the diversity family a genuine second channel and could separate it from Service
Diversity. But it changes the substrate's exploit semantics for **both** arms and
would move every golden. The literature basis needs checking before this is even
a candidate: the spec must be read for whether OS-dependent exploitation failure
is *intended*, or whether the `×2.5` time penalty is the intended expression of
OS mismatch and the gate was an abandoned alternative. **Do not uncomment it on
the strength of this brief.**

**Decision C — the family's cardinality in the reporting.** Independent of A and
B, and actionable now at zero risk: decide whether the defence family is reported
as four mechanisms or as two effects with two members each. The recommendation is
**two effects, four members, stated explicitly**, with the unseparated pairs
named and the mechanism for each pairing given — because that is what the
interval report already says, and stating it converts an unexamined presentation
into a finding.

**Why C first if only one is taken.** It is free, it strengthens the record
rather than perturbing it, and it is the one that bears on the headline result.
A and B both cost goldens and neither changes a recorded conclusion.

### Alternatives considered

- **Treat this as an axis-6 input and fold it into the redesign.** Rejected as
  the primary framing: the redesign consumes the answer but does not need to own
  the question, and a substrate classification should not be decided inside a
  movement-layer design brief. It is recorded as a consumer in §5.
- **Add a validation test and move on without a disposition.** Rejected: a test
  pinning current behaviour would freeze an unclassified divergence, which is the
  failure mode the intent-spec procedure exists to prevent.
- **Re-run experiment 2 with a corrected mechanism.** Rejected under the standing
  precedent that recorded experiments stand as records of the model and substrate
  they ran under.

## 4. Validation gate

The work is done when:

1. Each of A, B and C carries a **written disposition from Marc**, recorded in
   the intent-conformance audit (A, B) and in the experiment-2 findings record
   (C).
2. `intent_conformance_audit.md`'s **IS-MTD-06 row is corrected either way** —
   either its CONFORMS verdict is re-argued with the always-replace behaviour in
   view, or the row is re-classified. The current row reaches a verdict without
   the behaviour in view, and that is true regardless of the disposition.
3. If C is taken: `experiment_02_findings.md` §9 carries the cardinality
   qualification, and the two unseparated pairs are named with their causes.
4. If A or B is taken: the fix lands with goldens re-baselined per
   `baseline/CHANGELOG.md`, the full suite green, and the spec/audit rows moved
   to `fixed` with the dated disposition — the D-05 procedure, followed exactly.
5. A regression test exists for whatever A settles on. If the comparison is
   repaired, it must assert `service_is_compatible_with_os` returns **True** for a
   service against its own OS and version — the assertion whose absence let this
   survive.

## 5. Hard constraints

- **"Bug" is a verdict, not a first impression.** Classify against
  `mtdsim_intent_spec.md` §c before forming a view; `documented-nowhere` makes a
  behaviour a *candidate* only, and **only Marc's disposition makes it a bug**.
  Never fix from a paper-code mismatch.
- **No recorded experiment is re-run** under a changed substrate. The frontier,
  experiment 2 and the axis sweeps stand as records of what they ran under.
- **Goldens.** A and B both move them. Follow the D-05 procedure: re-baseline
  deliberately, log in `baseline/CHANGELOG.md`, and never `--no-verify`.
- **Determinism (SIM-05)** across any substrate change.
- **The axis-6 redesign is a consumer and must not pre-empt this.** A time-free
  effort term cannot distinguish OS Diversity from Service Diversity on the
  current substrate, and any candidate model claiming to price them differently
  is modelling something MTDSim does not do. That is a falsifier for the axis-6
  design work, and it should be stated there rather than resolved here.
- Australian English; branch per session; commit locally; **never push**.

## 6. Reading list

- `mtdnetwork/component/services.py` — `service_is_compatible_with_os`
  (387-402), `gen_services` (404-420), `Service.__eq__` (304-307),
  `Vulnerability.network` (132-155), `Vulnerability.exploit_time` (106-124).
- `mtdnetwork/mtd/osdiversity.py` and `mtdnetwork/mtd/servicediversity.py` — the
  two mechanisms side by side; the difference is the OS relabel and the guard.
- `mtdnetwork/operation/attack_operation.py` — `_do_exploit_vuln` (423-500,
  especially the `charge_time` docstring) and the `step()` call site at 747.
- [`../implementation/mtdsim_intent_spec.md`](../implementation/mtdsim_intent_spec.md)
  IS-MTD-05, IS-MTD-06, IS-TIM-06 — the yardstick, to be audited against by
  IS-ID rather than from paper memory.
- [`../implementation/intent_conformance_audit.md`](../implementation/intent_conformance_audit.md)
  lines 82-83 and 218 — the existing verdicts, and the IS-MTD-05 precedent for
  how a sibling divergence was dispositioned.
- [`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
  §9 — the headline the cardinality question bears on.

## 7. Out of scope (explicitly)

- **Uncommenting the OS gate on this brief's authority.** Decision B is a
  question to be answered, not an action to be taken.
- **Any change to `PortShuffle`, `UserShuffle` or `HostTopologyShuffle`**, which
  are commented out of the default strategy set and unreachable in every
  experiment. They are noted in the enumeration sweep as relevant to a different
  question.
- **The axis-6 utility redesign itself.** This brief supplies it an input and a
  falsifier; it does not design it.
- **Re-running or re-analysing experiment 2**, beyond adding the cardinality
  qualification if decision C is taken.
- Dissertation prose.
