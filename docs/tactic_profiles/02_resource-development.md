---
tactic: resource-development
attack_id: TA0042
attack_url: https://attack.mitre.org/tactics/TA0042/
attack_version: 19.1
status: stub
group_hypothesis: prep-off-network
tier_hypothesis: 3 declared
---

# Resource Development — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Resource Development is defined in the pinned v19.1 bundle as the phase where "the
adversary is trying to establish resources they can use to support operations":
creating, purchasing, or compromising/stealing the infrastructure, accounts, and
capabilities that back an intrusion ([TA0042](https://attack.mitre.org/tactics/TA0042/)).
The bundle makes the downstream links concrete — purchased domains support Command and
Control, email accounts enable phishing for Initial Access, stolen code-signing
certificates aid Defense Evasion (the pre-split label the description still carries).

Positionally it is the second tactic in the matrix and the second **pre-compromise** /
`PRE` tactic (with Reconnaissance); all 9 parent techniques are platform `PRE`, staged
*off* the victim network before and alongside the intrusion. In the campaign narrative
it is preparatory and largely invisible to the target: the adversary is building or
acquiring its own kit, so most activity leaves no trace inside the victim estate. It is
the tactic least coupled to the substrate's on-network model, which is why its
`group_hypothesis` is `prep-off-network`.

The v19.1 technique surface (9 parent, 41 sub-techniques) is organised as
acquire-vs-compromise pairs — infrastructure (Acquire Infrastructure T1583, Compromise
Infrastructure T1584), accounts (Establish Accounts T1585, Compromise Accounts T1586),
and capabilities (Develop Capabilities T1587, Obtain Capabilities T1588) — plus staging
(Stage Capabilities T1608), buying pre-existing access (Acquire Access T1650), and a
v19-era content-generation technique (Generate Content T1683) whose top procedures
reflect AI-assisted persona and content creation. It is the most heavily
group-/campaign-attributed pre-compromise tactic (563 procedure examples across 115
groups and 48 campaigns) with negligible malware attribution — again operator tradecraft
rather than on-host code. No technique crosses into another tactic.

## 2. APT relevance — group-assignment argument

The literature **confirms `prep-off-network` decisively.** Alshamrani describes the tail
of the reconnaissance phase as the point where "once APT actors have collected enough
information, they construct an attacking plan and prepare the necessary tools" — tool and
malware development, and the identification of vulnerabilities to weaponise, all conducted
*off* the victim network before the foothold exists
([`alshamrani2019`](../extractions/alshamrani2019.md) §I, §II-C Stage 1) [fetched]. The
ATT&CK surface agrees structurally: all nine parent techniques are platform `PRE`, and the
tactic is the most heavily group-/campaign-attributed pre-compromise stage with negligible
malware attribution — operator tradecraft staged externally, not on-host code (§1).

The consequence for the catalogue is the sharpest group boundary in the set: this tactic
has **no in-network observable the substrate can meter.** Whatever real-world weeks or
months tool-building consumes happen before the simulator's clock starts, so its in-sim
dwell is a candidate for **near-zero** — the adversary arrives already equipped. The group
boundary is itself the finding (per the README's "prep-off-network … boundary is itself a
finding to record"): resource-development is present in the place-union for completeness
but is the tactic least coupled to the on-network timeline. No point number here (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

Resource development is the profile's **inert** tactic (rubric crit. 7), and the honest §3 is a
*null verdict* stated plainly rather than a reset story forced onto a tactic that has none. Its
gain — infrastructure, accounts, tooling — is built and held **off the victim network**, before
the simulator's clock starts and outside anything an MTD mechanism can touch: mutation protects
the interior of the estate, not the adversary's own kit
([substrate primer](../specs/substrate_primer.md) §(c)), and resource development "takes place
outside of the company's protection and control … preventive measures may not be effective"
([`selmanaj2024`](../extractions/selmanaj2024.md) Ch. 4). No IP/topology shuffle, service/OS
diversity, or credential rotation reaches it.

**Reset verdict: null — reset-immune (off-network, pre-clock); no sweep** (the tactic carries a
near-zero in-sim dwell to begin with, §2). This is a *negative* contribution to the thesis's
novel object: resource development sits on neither the survivor nor the vulnerable pole of the
axis because it is never on the terrain the axis describes. It is present in the place-union for
completeness, and the honest move is to record that it contributes nothing to the MTD-interaction
finding rather than manufacture a verdict.

What is **not captured**: everything about resource development is outside the substrate's model
by construction — there is no off-network stage for the simulator to represent, and no
attacker-side gain here for a mutation to invalidate or spare. The tactic's whole value to the
model is as the documented boundary of where the MTD interaction *begins*.

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0042 page | 9 parent techniques, all `PRE`; acquire/compromise pairs; **no timing** | Confirms off-network staging; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §I, §II-C Stage 1 | Tool/plan/malware prep happens off-network before the foothold ("construct an attacking plan and prepare the necessary tools") | Supports near-zero *in-sim* dwell — the work precedes the simulator's clock | [fetched] |
| [`selmanaj2024`](../extractions/selmanaj2024.md) Ch. 4 (Resource Development) | Resource development "takes place outside of the company's protection and control. As a result, preventive measures may not be effective"; infrastructure is agile ("quickly provision, modify, and shut down … abort a mission and move on") | Emulation-textbook confirmation of the off-network verdict → near-zero *in-sim* dwell + reset-immune (an MTD shuffle can't touch it); no per-tactic number | [fetched] |
| [`syed2025`](../extractions/syed2025.md) §IV-A | Caldera adversary profiles were hand-built off-network from CTI ("we were not able to find playbooks … referred to multiple CTI sources"); prep precedes execution | Corroborates prep-off-network; the dataset's timestamps are execution latency, not prep dwell — documented gap | [fetched] |
| [`resource_dev_timing`](../extractions/resource_dev_timing.md) (RAND 2017; Bompos 2020) | **Median 22 days to develop a 0-day exploit**; 0-day average life **6.9 years** | Off-network capability-development dwell — weeks-scale, precedes the foothold; supports near-zero *in-sim* dwell (the work is done before the clock) | [fetched] |
| [`resource_dev_timing`](../extractions/resource_dev_timing.md) (Lidestri 2022 Table 1) | Creation→disclosure median **~3.7 yr**; disclosure→**exploit-published +1 day**; exploits perishable | The *obtain*-capability path is near-instant (grab a published exploit ~1 day post-disclosure) vs RAND's *develop* path (22 d) — the two ends of resource-dev tempo | [fetched] |
| [`resource_dev_timing`](../extractions/resource_dev_timing.md) (Hao 2011 Findings 4.1/5.2; Interisle 2021) | Malicious domains registered "just in time" — **>55% used ≥1 day after registration**, lookups peak in **3–4 days**; 65% of phishing domains maliciously registered, used within days | Infrastructure-prep (Acquire Infrastructure T1583) is hours-to-days, off-network — the agile, fast end; still pre-clock → near-zero in-sim | [fetched] |
| — (no in-corpus per-tactic timing) | No extraction assigns a duration to resource-development | Documented negative — this is the gap, and here it coincides with a near-zero in-network verdict | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** prep-off-network — **confirmed decisively;** this tactic *defines* the group boundary and is its sole member.
- **Relative multiplier:** ×0 (near-zero in-sim) — the adversary arrives already equipped; the real weeks-to-months of tool/infrastructure prep precede the simulator's clock.
- **Sweep range:** 0 → a small nominal floor (degenerate) — there is no in-sim dwell to sweep; a token nonzero transit is allowed only if the runner needs the place visibly traversed.
- **Tier:** 3 — declared; no substrate verb, and near-zero is a modelling decision (off-clock), not a literature-calibrated dwell.
- **Justification (one paragraph):** Resource-development is the **inert null** of the set. §2 confirms prep-off-network decisively — all nine parents are `PRE`, heavily operator-attributed, with no in-network observable the substrate can meter — and §4's timing evidence (RAND's 22-day 0-day development, days-scale malicious-domain registration) is uniformly *pre-clock*, so the in-sim dwell is near-zero (×0): the adversary is already equipped when the simulation begins. §3's reset verdict is a **null** — the gain is built and held off the victim network, reset-immune, sitting on neither pole of the survivor-vs-vulnerable axis. It receives a catalogue entry only for place-union completeness (validation gate), badged Tier-3 declared near-zero, and its honest contribution is as the documented boundary of *where the MTD interaction begins* rather than a dwell that shapes the timeline.
