---
tactic: persistence
attack_id: TA0003
attack_url: https://attack.mitre.org/tactics/TA0003/
attack_version: 19.1
status: stub
group_hypothesis: stealth-low-and-slow
tier_hypothesis: 3 declared
---

# Persistence — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Persistence is defined in the pinned v19.1 bundle as the phase where "the adversary is
trying to maintain their foothold": techniques that keep access across restarts, changed
credentials, and other interruptions, via any access, action, or configuration change
that preserves the foothold — replacing or hijacking legitimate code, adding startup
code, and the like ([TA0003](https://attack.mitre.org/tactics/TA0003/)).

Positionally it is the fifth tactic; in the narrative it is established once a foothold
exists and then relied upon continuously, recurring whenever the adversary acquires a new
host or account. It is the **durability layer** beneath the whole post-compromise
campaign — the mechanism by which a gain survives the ordinary churn of a live
environment, which is exactly the property an MTD reset is designed to attack (deferred to
§3), and the reason its dwell character (`stealth-low-and-slow`) is load-bearing for the
timeline.

The v19.1 technique surface is one of the largest in the matrix (22 parent, 91
sub-techniques): autostart/boot-logon mechanisms (Boot or Logon Autostart Execution T1547
— 332 procedures, Boot or Logon Initialization Scripts T1037, Create or Modify System
Process T1543, Event Triggered Execution T1546), scheduled execution (Scheduled Task/Job
T1053), credential/account durability (Valid Accounts T1078, Account Manipulation T1098,
Create Account T1136, Modify Authentication Process T1556), server- and
application-level implants (Server Software Component T1505, Office Application Startup
T1137, Software Extensions T1176), and firmware/image/pre-OS footholds (Pre-OS Boot
T1542, Implant Internal Image T1525, Compromise Host Software Binary T1554). It is the
most cross-wired tactic in the matrix: 7 techniques are shared with Privilege Escalation,
4 with Stealth, plus overlaps into Execution, Initial Access, Credential Access, Defense
Impairment and Command and Control — the bundle notes persistence and privilege-escalation
"often overlap", since an OS feature that lets an adversary persist frequently runs in an
elevated context.

## 2. APT relevance — group-assignment argument

The literature **confirms `stealth-low-and-slow` strongly.** Persistence is the durability
layer whose whole purpose is to outlast time: Alshamrani describes multi-host backdoors plus
valid VPN credentials and observes that once persistence is established "it is very difficult
to completely push out such attacker out of the environment"
([`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 3) [fetched]. FireEye's
M-Trends finding of backdoors "loaded even before the operating system was loaded"
([`alshamrani2019`](../extractions/alshamrani2019.md) §I) [fetched] sharpens the character —
a pre-OS/bootkit foothold is built to survive reboots, reimaging and OS changes. cho2020's
advanced-attacker model frames the same property: stealthy attackers "stay stealthy until
the time comes" ([`cho2020`](../extractions/cho2020.md) §V-A) [fetched], and persistence is
what lets them wait.

The dwell character is therefore long-lived by design, and — unlike the enabling tactics —
persistence is valuable precisely *between* actions rather than during them. cho2020 finds
optimal-defence outcomes hinge on "whether the attacker's goal required a persistent
foothold" ([`cho2020`](../extractions/cho2020.md) §VI-A) [fetched], marking persistence as
the tactic whose dwell most directly drives the MTD comparison. The profile confirms
`stealth-low-and-slow` / Tier 3 (declared) — no substrate verb prices "maintain a foothold".
No point number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

Persistence produces a **foothold** — a capability/conquest possession: a compromised host
stays owned, and "persistent conquest survives everything" in the substrate's reset model
([substrate primer](../specs/substrate_primer.md) §(e)). So the naive verdict is *survivor*.
But persistence is the profile's **open contest** — the reset here is genuinely a *rate
contest*, not a clean survive-or-invalidate, and it should be foregrounded as an open question
rather than resolved. FlipIt frames foothold survival as a game where **the higher-move-cost
player has benefit 0** and whoever moves faster/cheaper controls the resource
([`persistence_reset_models`](../extractions/persistence_reset_models.md)): a periodic MTD move
*contests* a foothold but does not cleanly evict it, an SCIT cleansing cycle bounds the
attacker's hold window, and a too-slow reset "grant[s] attackers extended time windows" (Sun).
There is no fixed answer — the outcome flips on the **defender-move-rate ÷
attacker-re-compromise-rate** ratio, which is why the sweep is wide.

This is also the dwell that most directly drives the MTD comparison (cho2020: optimal defence
hinges on "whether the goal required a persistent foothold"), so getting its verdict *and its
uncertainty* right matters more than for most tactics. The MTD action that bites is any
mechanism that periodically refreshes host state; the substrate, however, implements **no
cleansing/reimaging/redundancy mechanism** ([substrate primer](../specs/substrate_primer.md)
§(c)) — its shuffles and diversity swaps do not clear host compromise — so in the *current*
substrate a foothold is a near-total survivor, and the FlipIt rate-contest is a
**literature-argued verdict that diverges from what the substrate can exercise**. Recording that
divergence is itself a finding (§(e).1): the reset-magnitude sweep encodes the contest the
substrate does not yet run.

What is **not captured**: the eviction mechanism itself (no reimage/rejuvenation op), and the
account-manipulation path by which persistence *adapts around* a periodic credential rotation
(Selmanaj) — the substrate treats the foothold as durable and the credential as never revoked,
so it models persistence at the survivor extreme of the rate contest. **Reset verdict: contested
survivor — foreground as a rate-dependent open question; sweep width wide.**

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0003 page | 22 parents / 91 subs; Valid Accounts T1078, autostart T1547; **no timing** | The durability layer; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 3, §I | Multi-host backdoors + valid creds; "very difficult to push out"; pre-OS bootkits "loaded before the OS" | Long-lived/sticky character; valuable between actions — no per-tactic number | [fetched] |
| [`cho2020`](../extractions/cho2020.md) §V-A, §VI-A | Stealthy attackers "stay stealthy until the time comes"; defence hinges on "whether the goal required a persistent foothold" | Frames persistence as the dwell that drives the MTD comparison; no per-tactic value | [fetched] |
| [`breach_reports_macro_timing`](../extractions/breach_reports_macro_timing.md) (M-Trends 2026) | Espionage/DPRK-IT-worker **median dwell 122 days**; BRICKSTORM edge-implant **dwell ~400 days**, "persistence that routinely survives standard remediation efforts and system reboots" | Tier-2 macro evidence for the long-lived, reset-*surviving* character of persistence — the whole-campaign envelope for the group anchor; not a per-tactic dwell | [fetched] |
| [`selmanaj2024`](../extractions/selmanaj2024.md) Ch. 2 & 4 (Persistence) | The beachhead keeps access "even if the target system is restarted or if security measures are taken"; Account Manipulation "constantly updat[es] the password to avoid … password duration policies"; [`syed2025`](../extractions/syed2025.md) §I: LightBasin undetected **5 years** | Reset-survivor evidence — persistence can *adapt around a periodic reset* (defeating credential rotation); anecdotal whole-campaign dwell, no per-tactic number | [fetched] |
| [`apt_campaign_duration`](../extractions/apt_campaign_duration.md) (Yuldoshkhujaev 2025 §4) | APT campaign duration **1 day → ~5 years, 137 days average** (decade of dossiers); attackers "waiting for an opportune time" | Tier-2 whole-campaign envelope for the reset-*surviving* foothold — the espionage long-tail the group anchor must reach; not a per-tactic dwell | [fetched] |
| [`persistence_reset_models`](../extractions/persistence_reset_models.md) (FlipIt 2013 §4.3; SCIT 2006; Sun 2025) | FlipIt: the higher-move-cost player has **benefit 0**; whoever moves faster/cheaper controls the resource more — reset is **partial, rate-dependent**; SCIT: cleansing cycle bounds the attacker's hold window; Sun: too-slow reset "grant[s] attackers extended time windows" | The §3 reset verdict for persistence: a periodic MTD move *contests* a foothold but does not cleanly wipe it — outcome set by move-rate ÷ compromise-rate → **wide sweep** (**→§3**) | [fetched] |
| — (no in-corpus per-tactic timing) | No extraction assigns a persistence duration | Documented negative (the gap); confirms Tier-3 *declared* | [fetched] |

> **§4 note — operational-validation outer envelope.** The whole-chain macro-milestone rows
> above (breakout, access→AD, access→exfil, campaign dwell, time-to-ransomware) are an
> *operational-validation outer envelope*, not per-tactic timing or reset targets: each is
> defined by *when detection caught the intrusion*, and detection/IDS is culled from this
> substrate ([substrate primer](../specs/substrate_primer.md) §(f)), so they bound the emergent
> timeline's *shape/plausibility*, never an absolute per-tactic dwell. Only the rows that resolve
> dwell-character or reset-verdict feed §3/§5.

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** stealth-low-and-slow — **confirmed strongly** (the durability layer, valuable *between* actions); cho2020 marks it the dwell that most directly drives the MTD comparison.
- **Relative multiplier:** ×1.0 of the stealth anchor — the reference long-lived holding dwell of the group.
- **Sweep range:** ×0.25–×4 (wide) — driven by the FlipIt **rate-contest** uncertainty in §3 (the reset has no fixed answer), not by duration alone.
- **Tier:** 3 — declared; no substrate verb prices "maintain a foothold".
- **Justification (one paragraph):** Persistence is the group's most load-bearing dwell and its clearest **open contest**. §2 confirms the low-and-slow character decisively — the durability layer built to outlast reboots, reimaging and time (pre-OS bootkits, valid-credential backdoors; espionage dwell to months/years as the outer envelope) — so it takes the reference multiplier (×1.0). §3 is where the width comes from: the naive verdict is *survivor* (a compromised host stays owned), but FlipIt frames foothold survival as a rate contest in which the higher-move-cost player has benefit 0, so whether a periodic mutation evicts an entrenched foothold flips on the defender-move-rate ÷ attacker-re-compromise-rate ratio — a genuine "no fixed answer" region that justifies the wide band. The load-bearing divergence to record (substrate-primer §(e).1): the substrate implements **no eviction/reimaging op**, so it currently models persistence at the *survivor extreme* of the contest, and the reset-fraction sweep (feeding the L3b binding) encodes the contest the substrate does not yet run. Tier-3 declared, because no substrate verb and no isolable observable price the tactic.
