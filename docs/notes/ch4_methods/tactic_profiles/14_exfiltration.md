---
tactic: exfiltration
attack_id: TA0010
attack_url: https://attack.mitre.org/tactics/TA0010/
attack_version: 19.1
status: reconciled
group_hypothesis: objective-execution
tier_hypothesis: 2 literature
---

# Exfiltration — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../operational_validation.md).
> Catalogue (the §5 distillation): [`../../data/ogasp/tactic_durations.json`](../../../../data/ogasp/tactic_durations.json).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Exfiltration is defined in the pinned v19.1 bundle as the phase where "the adversary is
trying to steal data": techniques for removing data from the network, often after
packaging it (compression, encryption) to avoid detection, typically over the
command-and-control channel or an alternate channel and sometimes with transfer-size
limits ([TA0010](https://attack.mitre.org/tactics/TA0010/)).

Positionally it is the fourteenth tactic; a **terminal objective** tactic (with Impact)
that consumes the output of Collection and rides the Command-and-Control channel. In a
data-theft campaign it is the endpoint the whole intrusion serves, which is why its
`group_hypothesis` is `objective-execution` (Tier 2 — a candidate for
literature-calibrated timing, since the breach literature reports access→exfil milestones
even though it reports no per-tactic dwell).

The v19.1 technique surface is one of the smallest in the matrix (9 parent, 10
sub-techniques), and channel choice dominates it: Exfiltration Over C2 Channel T1041 (201
procedures — over half the tactic's total), Exfiltration Over Alternative Protocol T1048,
Exfiltration Over Web Service T1567, Exfiltration Over Other Network Medium T1011,
Exfiltration Over Physical Medium T1052, and Transfer Data to Cloud Account T1537 — plus
shaping/automation techniques (Automated Exfiltration T1020, Scheduled Transfer T1029, Data
Transfer Size Limits T1030). It has no cross-tactic mappings — exfiltration techniques are
exfiltration-only — but is tightly semantically coupled to C2 (T1041 exfiltrates over the
same channel as T1071/T1105). 396 procedures across 215 malware families, a smaller
footprint than the enabling tactics.

## 2. APT relevance — group-assignment argument

The literature **confirms `objective-execution`** with a distinctive stealth-shaped spread.
Exfiltration is the terminal act of a data-theft campaign, and Alshamrani describes its
behaviour precisely: because "most IDS/IPS do ingress filtering and not outgress filtering",
exfiltration often succeeds, and a careful attacker "intelligently split[s] the data
exfiltration into batches and to servers with different IP addresses"
([`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §II-C Stage 4) [fetched]. The RSA
intrusion exfiltrated over FTP after compressing and encrypting the data
([`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §III-D) [fetched]. So the tactic is
objective-execution — it acts on the goal — but its *shape* is deliberately paced and
fragmented to stay under detection thresholds.

That gives exfiltration a dual character: a terminal objective (like impact) whose execution
is spread low-and-slow (like stealth). It joins collection and impact in the tuned
`objective-execution` group / Tier 2 — the group the breach literature can calibrate, since it
reports access→exfil milestones even though it publishes no per-tactic dwell (per the
[precedent survey](../../ch2_background/tactic_duration_precedent_survey.md)). The batched,
IP-diversified spread argues its multiplier should admit a **wide range** (fast bulk transfer
vs slow trickle). No point number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

Exfiltration is the act of moving already-collected data out over the command-and-control
channel, so its reset verdict is **inherited from [[13_command-and-control]]**: because
Exfiltration Over C2 Channel T1041 rides the C2 route, a position-mutating shuffle that disturbs
that route interrupts an *in-progress* transfer (forcing re-establishment and resume) — a
**partial reset**, blunted by C2's architected resilience. The two gains either side of the
transfer, though, survive: the **data already staged/collected** is a capability possession the
shuffle does not touch ([substrate primer](../../../implementation/substrate_primer.md) §(e)), and the
destination infrastructure is off-network.

Crucially, exfiltration's own tradecraft is *itself* an adaptation to channel disruption: the
careful attacker "intelligently split[s] the data exfiltration into batches and to servers with
different IP addresses" (Alshamrani §II-C Stage 4) and schedules transfers to blend in
([`selmanaj2024`](../../../sources/extractions/selmanaj2024.md) Ch. 4). Batching across servers/IPs means a
single shuffle resets at most one batch, not the campaign — the design blunts the reset. The MTD
action that bites is therefore the position-mutating shuffle acting on the C2 route, weakly.
**Reset verdict: partial (inherits C2's architected survival; staged data survives; batching
blunts it); sweep width wide** — spanning a fast bulk burst to a slow, fragmented trickle, with a
throughput floor (exfil "cannot go any faster … data throughput … rigid time frames").

What is **not captured**: the substrate models neither data-at-rest as resettable state nor the
C2 channel's fallback resilience, so exfiltration's modelled reset is simply the C2 route
interruption applied to the transfer window — the batched, IP-diversified spread that would blunt
it in reality is an attacker-side behaviour the L3b binding must encode, not a substrate
primitive.

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0010 page | Small (9 parents); Exfiltration Over C2 Channel T1041 (201, >half); size-limit/scheduled-transfer shaping; **no timing** | Terminal objective; no duration to inherit | [fetched] |
| [`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §II-C Stage 4, §III-D | Batched + IP-diversified to evade ingress-only filtering; RSA compress+encrypt→FTP | Objective-execution with a stealth-shaped spread → wide range; no per-tactic number | [fetched] |
| [`breach_reports_macro_timing`](../../../sources/extractions/breach_reports_macro_timing.md) (Sophos AAR) | Attack start → **exfiltration: median 72.98 h (2025 ed.) / 78.83 h (2026 ed.)**; exfil → detection ~1.9–2.7 h; exfil "cannot go any faster … human activity, data throughput … rigid time frames" (a dwell floor) | Tier-2 macro calibration target for the objective-execution anchor and the *held-out* milestone check (access→exfil); reconciled [search]→[fetched] from the primary reports | [fetched] |
| [`breach_reports_macro_timing`](../../../sources/extractions/breach_reports_macro_timing.md) (DFIR cases) | Time-to-Ransomware spans **2 h → 118 h → 328 h** across three cases; exfil (Rclone→MEGA/SFTP) lands late in the chain, often after a multi-day dwell gap | Per-case tempo spread the objective-execution sweep must span; exfil timing is late and paced, not a burst — corroborates the batched-low-and-slow reading | [fetched] |
| [`selmanaj2024`](../../../sources/extractions/selmanaj2024.md) Ch. 4 (Exfiltration — Scheduled Transfer T1029) | Attackers "schedule a specific time or interval … during peak business hours … If data is being exfiltrated at random intervals, it can look suspicious" | Direct support for the *deliberately paced* (batched low-and-slow) end of the exfil width flagged in Step B; behaviour, not a number | [fetched] |
| [`collection_exfil_timing`](../../../sources/extractions/collection_exfil_timing.md) (GAO Equifax; Nadler 2019; Unit42 2026) | Equifax exfil **ran ~76 days, ~9,000 queries** in small increments to evade; low-throughput DNS-exfil is **slow by design** (data volume → stealth duration); but fastest quartile exfil **1.2 h** | Spans the exfil width: a fast eCrime burst (hours) ↔ a low-and-slow espionage extraction (months) — the objective-execution sweep + the throughput floor | [fetched] |

> **§4 note — operational-validation outer envelope.** The whole-chain macro-milestone rows
> above (breakout, access→AD, access→exfil, campaign dwell, time-to-ransomware) are an
> *operational-validation outer envelope*, not per-tactic timing or reset targets: each is
> defined by *when detection caught the intrusion*, and detection/IDS is culled from this
> substrate ([substrate primer](../../../implementation/substrate_primer.md) §(f)), so they bound the emergent
> timeline's *shape/plausibility*, never an absolute per-tactic dwell. Only the rows that resolve
> dwell-character or reset-verdict feed §3/§5.

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** objective-execution — **confirmed**, with a stealth-shaped spread (terminal objective, but deliberately paced/fragmented to stay under thresholds).
- **Relative multiplier:** ×1.0 of the objective-execution anchor — the terminal data-theft act; throughput-bound with a floor.
- **Sweep range:** ×0.25–×4 (wide) — spans a fast bulk burst to a slow, fragmented trickle (Equifax ~76 days ↔ fastest quartile 1.2 h, as the outer envelope), with a throughput floor at the bottom.
- **Tier:** 2 — literature-calibratable: the breach literature reports access→exfil milestones (Sophos ~73–79 h) as a held-out calibration/plausibility check.
- **Justification (one paragraph):** Exfiltration is the terminal act of a data-theft campaign with a dual character — an objective (like [[15_impact]]) executed low-and-slow (like [[07_stealth]]) — so §2 places it in the tuned objective-execution group at the reference multiplier (×1.0), and its Tier is 2 because access→exfil is one of the few milestones the breach literature reports (a held-out observable for operational validation, per the method note's anti-circularity rule 3). The wide sweep is earned by the batched, IP-diversified spread §2 documents: the modelled band spans a fast bulk burst to a slow fragmented trickle, while acknowledging the real-world span (hours ↔ months) as an outer envelope that shape-not-scale deliberately does not match absolutely. §3's reset is **inherited from [[13_command-and-control]]** — Exfiltration Over C2 Channel T1041 rides the C2 route, so a position-mutating shuffle interrupts an *in-progress* transfer (partial reset, blunted by C2's architected resilience), while the already-staged data survives and the destination is off-network; crucially the tactic's own tradecraft (batching across servers/IPs) *is* an adaptation to disruption, so a single shuffle resets at most one batch. The reset fraction (partial, blunted) feeds the binding; the wide duration band feeds the catalogue.
