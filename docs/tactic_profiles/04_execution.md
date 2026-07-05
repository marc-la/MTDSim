---
tactic: execution
attack_id: TA0002
attack_url: https://attack.mitre.org/tactics/TA0002/
attack_version: 19.1
status: stub
group_hypothesis: stealth-low-and-slow
tier_hypothesis: 3 declared
---

# Execution — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Execution is defined in the pinned v19.1 bundle as the phase where "the adversary is
trying to run malicious code": techniques that result in adversary-controlled code
running on a local or remote system
([TA0002](https://attack.mitre.org/tactics/TA0002/)). The definition itself stresses the
tactic's cross-cutting character — execution techniques are "often paired with techniques
from all other tactics" (the bundle's example: a remote-access tool running a PowerShell
script that performs Remote System Discovery).

Positionally it is the fourth tactic, immediately post-foothold, but functionally a
**recurring, cross-cutting** tactic rather than a single stage — code execution underlies
most on-host actions throughout the intrusion. In the narrative it is less a place the
attacker *dwells* than the verb by which other tactical goals are achieved, which is what
makes its dwell character (the `stealth-low-and-slow` `group_hypothesis`) a genuine
question for §2 rather than a substrate-priced given.

The v19.1 technique surface is large (20 parent, 44 sub-techniques) and dominated by
Command and Scripting Interpreter T1059 (1,017 procedure examples — the largest
single-technique count in this study), followed by User Execution T1204, Native API
T1106 and Scheduled Task/Job T1053, then a broad spread across service, IPC, container,
serverless/cloud and CI-CD execution surfaces (System Services T1569, Inter-Process
Communication T1559, Container Administration Command T1609, Serverless/Cloud
Administration T1648/T1651, ESXi Administration Command T1675, Poisoned Pipeline
Execution T1677). It is the most heavily instrumented tactic overall (2,317 procedure
examples across 565 malware families). Its cross-tactic mappings are extensive —
Scheduled Task/Job T1053 (also Persistence, Privilege Escalation), Hijack Execution Flow
T1574 (also Stealth), Software Deployment Tools T1072 (also Lateral Movement), BITS Jobs
T1197 (also Stealth, Persistence) — reflecting that "run code" is the shared mechanism
beneath many other tactics.

## 2. APT relevance — group-assignment argument

The hypothesis is `stealth-low-and-slow`, but execution is the one tactic where the profile
**flags the group as genuinely unsettled.** Alshamrani couples execution directly to
concealment — "once the attackers get control of the system through the malware execution …
they keep low to go undetected to the next phase" — and notes that fileless, in-memory
execution (Duqu 2.0) is chosen precisely to evade
([`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 2, §IV-A) [fetched]; both
read as low-and-slow. cho2020's advanced-attacker model agrees in spirit — stealthy
attackers "stay stealthy until the time comes"
([`cho2020`](../extractions/cho2020.md) §V-A) [fetched]. Yet mechanically execution is a
brief, cross-cutting *verb*: "run code" completes in moments and, as §1 notes, underlies
most other tactics rather than occupying a dwell of its own.

The reconciliation the profile records for §5 is that execution's low-and-slow character is
inherited from the **stealth wrapper and the inter-execution spacing** — an APT paces its
on-host actions to stay quiet — not from the execution act itself, which is fast. That
leaves two defensible readings: keep execution `stealth-low-and-slow` if the modelled state
represents the *paced cadence* of on-host action, or move it toward a fast/near-zero verb if
it represents only the *act*. The literature supports the former, the mechanism the latter.
This is an unresolved group boundary, and the honest consequence is a **wide sweep** on
execution's multiplier until the runner shows which reading the timeline needs. No point
number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0002 page | Command/Scripting Interpreter T1059 dominant (1,017 procedures); cross-cutting; **no timing** | Confirms execution is a verb beneath other tactics; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 2, §IV-A | Execution "keep[s] low to go undetected"; fileless/in-memory (Duqu 2.0) chosen to evade | Qualitative stealth-coupling (paced cadence), but the act itself is fast — no per-tactic number | [fetched] |
| [`bland2020`](../extractions/bland2020.md) §2.1 | CAPEC-modelled attack steps carry transition rates "notional … randomly selected between one and ten" | Declare-and-sweep precedent for step-level execution timing | [fetched] |
| [`cho2020`](../extractions/cho2020.md) §IV-A-8 | OS-rotation "exposure window" = "duration of an OS being exposed and vulnerable" | A defender-side window, not attacker execution dwell — no per-tactic value | [fetched] |
| [`selmanaj2024`](../extractions/selmanaj2024.md) Ch. 4 (Execution) | A fast enabling verb — "Once the attacker has successfully executed their code, they can start to carry out their malicious goals" (fileless/in-memory PowerShell) | Frames execution as the quick pivot, not a dwell — supports the "fast verb in a stealth wrapper" reading flagged unsettled in Step B; no number | [fetched] |
| [`ling2023`](../extractions/ling2023.md) Appendix A | Execution techniques map to code/command-injection vuln categories (Command-Line Interface → Direct Shell Command; Native API → Command Injection) | Per-technique CVE shape exists for execution, unlike C&C/hiding; still no dwell (empirical method needs real CVEs) | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn stealth-low-and-slow>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 3 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
