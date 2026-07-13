---
tactic: impact
attack_id: TA0040
attack_url: https://attack.mitre.org/tactics/TA0040/
attack_version: 19.1
status: reconciled
group_hypothesis: objective-execution
tier_hypothesis: 2 literature
---

# Impact — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../operational_validation.md).
> Catalogue (the §5 distillation): [`../../data/ogasp/tactic_durations.json`](../../../../data/ogasp/tactic_durations.json).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Impact is defined in the pinned v19.1 bundle as the phase where "the adversary is trying
to manipulate, interrupt, or destroy your systems and data": techniques that disrupt
availability or compromise integrity by manipulating business and operational processes,
including destroying or tampering with data — sometimes as the end goal, sometimes as
cover for a confidentiality breach ([TA0040](https://attack.mitre.org/tactics/TA0040/)).

Positionally it is the fifteenth and last tactic; the other **terminal objective** tactic
(with Exfiltration), where an availability-/integrity-focused campaign (ransomware, wiper,
fraud) delivers its payload. Its `objective-execution` `group_hypothesis` (Tier 2) mirrors
Exfiltration's — it is an end-state action whose timing the ransomware/IR literature
characterises even where per-tactic dwell is unpublished.

The v19.1 technique surface (15 parent, 18 sub-techniques) covers availability destruction
(Data Encrypted for Impact T1486 — 84 procedures, the ransomware-encryption technique;
Data Destruction T1485, Disk Wipe T1561, Firmware Corruption T1495), recovery denial and
service disruption (Inhibit System Recovery T1490, Service Stop T1489, System
Shutdown/Reboot T1529, Account Access Removal T1531), denial-of-service (Network/Endpoint
DoS T1498/T1499, Email Bombing T1667), integrity attacks (Data Manipulation T1565,
Defacement T1491), and objective-level abuse (Resource Hijacking T1496 — cryptomining,
Financial Theft T1657). It has no cross-tactic mappings — impact techniques are terminal by
nature. Its footprint is the smallest of the post-compromise tactics (378 procedures across
36 groups and 8 campaigns), and its most-attributed techniques are the ransomware and
destructive-attack primitives (encryption T1486, recovery inhibition T1490, service stop
T1489).

## 2. APT relevance — group-assignment argument

The literature **confirms `objective-execution`** — impact is the terminal payload of an
availability-/integrity-focused campaign. Alshamrani's Stage 4 covers the impediment case
directly: "when the attackers' goal is to undermine critical components, actions comprising
disabling or destroying the critical components", the canonical instance being Stuxnet's
sabotage of Iran's uranium centrifuges
([`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §II-C Stage 4, §III-C) [fetched].
Unlike the enabling tactics, impact is where the campaign spends its accumulated access, so it
belongs with collection and exfiltration in the tuned objective-execution group.

Its dwell character is the most bimodal in the set, split by actor type. A ransomware or wiper
actor's impact is fast and decisive — encryption or destruction executed in a burst once
positioned (the WannaCry pattern; al-sada2024's per-tactic technique table lists impact as
Data Encrypted for Impact / Inhibit System Recovery / Service Stop,
[`al-sada2024`](../../../sources/extractions/al-sada2024.md) §2 Table 1) [fetched]. An espionage actor with
a "position for future" goal may never reach impact at all
([`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §II-C) [fetched]. And the dwell ceiling
is a *decision*, not a duration — an APT's campaign "ends when … the funding organization gets
all the data it needs" ([`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §I, §II-C Stage
5) [fetched]. The profile confirms `objective-execution` / Tier 2 (the ransomware/IR literature
characterises time-to-impact) with a **wide range** spanning burst-impact to never. No point
number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

Impact is the one tactic where MTD acts as **blast-radius limiting rather than gain
invalidation** — a distinct reset mechanism worth stating in its own right. Impact's gain is an
*irreversible act* (encryption, destruction), not a retained state: a shuffle mid-campaign cannot
"reset" an already-encrypted host. What it can do is limit *how many further hosts* the impact
reaches. Barach's MTD (container mutation + IP hopping + service rotation) contains lateral
ransomware spread mid-attack, cutting encryption reach to **13.2%** with mean-time-to-containment
**91.4 s** ([`ransomware_timing`](../../../sources/extractions/ransomware_timing.md)) — a partial reset of the
impact *reach*, not the impact *act*.

The split maps onto the per-modality axis via *reachability*: once positioned on a host, the
impact act on *that* host is a survivor (fast, decisive — encryption is throughput-bound at
minutes-to-hours); the *spread* to new hosts is reset-vulnerable because it needs the same
reachability/discovery that a position-mutating shuffle invalidates ([[11_lateral-movement]]'s
scan modality). The MTD action that bites is therefore the topology/address shuffle acting on the
*propagation*, not the payload. **Reset verdict: the act on a held host survives; the spread is
reset-vulnerable (blast-radius limiting); sweep width wide** — burst-impact-to-never, the reset
applying to reach not act.

What is **not captured**: the substrate does not model data destruction/encryption as an
irreversible state change, so impact "reach" is proxied entirely by the reachability a topology
shuffle governs — the containment Barach measures is expressible only insofar as the spread rides
the substrate's lateral-movement reachability. Objective-conditioning (crit. 7) is sharp here: an
espionage "position for future" campaign may never reach impact at all
([`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §II-C), so the tactic is inert for some
objective-profiles and decisive for others — a genuine discriminator.

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0040 page | Data Encrypted for Impact T1486 (84); ransomware/destruction primitives; no cross-tactic mappings; **no timing** | Terminal payload; no duration to inherit | [fetched] |
| [`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §II-C Stage 4, §III-C, §I | Disabling/destroying components (Stuxnet); dwell ceiling sponsor-bounded ("ends when the org gets the data it needs") | Objective-execution; burst-impact..never — no per-tactic number | [fetched] |
| [`al-sada2024`](../../../sources/extractions/al-sada2024.md) §2 Table 1 | WannaCry impact = Data Encrypted for Impact / Inhibit System Recovery / Service Stop | Ransomware = fast decisive impact (contrast to espionage never-reaching) — technique map, no timing | [fetched] |
| [`breach_reports_macro_timing`](../../../sources/extractions/breach_reports_macro_timing.md) (DFIR cases) | **Time-to-Ransomware 2 h (Confluence→LockBit) / 118 h (RDP→RansomHub) / 328 h (BlackSuit)** — two orders of magnitude, per-case timestamped | Tier-2 macro anchor for the fast-impact end and the burst↔slow spread the objective-execution sweep must cover; reconciled [search]→[fetched] from primary case reports | [fetched] |
| [`breach_reports_macro_timing`](../../../sources/extractions/breach_reports_macro_timing.md) (M-Trends 2026) | Ransomware evolved into **recovery denial** — operators target backups/identity/hypervisors to make the impact irreversible; espionage never reaches impact | Confirms the impact end as decisive-and-fast for eCrime vs never-reached for espionage — the widest objective-execution sweep; whole-campaign, no per-tactic dwell | [fetched] |
| [`ling2023`](../../../sources/extractions/ling2023.md) Appendix A (Impact) | Impact techniques map to *Denial of Service* (Loss of View) and *Access Control* (Manipulation of View) vuln categories | Per-technique CVE shape for the destructive/impact primitives; no dwell | [fetched] |
| [`ransomware_timing`](../../../sources/extractions/ransomware_timing.md) (Splunk 2022; Secureworks 2024; IBM 2022) | Encryption act **~5m50s (LockBit) → ~1h55m (PYSA)**, overall median **~42m52s**, throughput-bound; ransomware dwell **~7–28 h** (Secureworks), access→deploy 3.85 d–60 d (IBM) | The impact *act* (encryption) is minutes-to-hours with a real floor (disk I/O); the whole-chain is fast-eCrime vs never-for-espionage — the objective-execution anchor + widest sweep | [fetched] |
| [`ransomware_timing`](../../../sources/extractions/ransomware_timing.md) (Barach 2026 MTD) | An MTD (container mutation + IP hopping + service rotation) reports **mean-time-to-containment 91.4 s**, encryption cut to 13.2% by blocking lateral ransomware spread | §3 MTD-vs-impact: shuffling the runtime surface contains lateral spread mid-attack, limiting blast radius — a partial reset of the impact reach (**→§3**) | [fetched] |

> **§4 note — operational-validation outer envelope.** The whole-chain macro-milestone rows
> above (breakout, access→AD, access→exfil, campaign dwell, time-to-ransomware) are an
> *operational-validation outer envelope*, not per-tactic timing or reset targets: each is
> defined by *when detection caught the intrusion*, and detection/IDS is culled from this
> substrate ([substrate primer](../../../implementation/substrate_primer.md) §(f)), so they bound the emergent
> timeline's *shape/plausibility*, never an absolute per-tactic dwell. Keep the ransomware
> *encryption-speed* rows as a real per-act floor; only rows that resolve dwell-character or
> reset-verdict feed §3/§5.

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** objective-execution — **confirmed** (the terminal payload of an availability-/integrity-focused campaign), the most bimodal member of the group.
- **Relative multiplier:** ×1.0 of the objective-execution anchor — the impact *act* (encryption/destruction), throughput-bound at minutes-to-hours.
- **Sweep range:** ×0.1–×5 (**widest**, alongside [[08_defense-impairment]]) — spans a decisive burst to *never-reached*, the "never" handled structurally (some objective-profiles omit impact) rather than by duration alone.
- **Tier:** 2 — literature-calibratable: the ransomware/IR literature characterises time-to-impact (encryption ~6 min–~2 h; time-to-ransomware 2 h–328 h) as an outer envelope.
- **Justification (one paragraph):** Impact is where a campaign spends its accumulated access, so §2 confirms objective-execution (×1.0 anchor), and Tier 2 because the ransomware/IR literature characterises time-to-impact even without a per-tactic dwell — the encryption act itself has a real disk-I/O floor (§4: ~6 min–~2 h). Its dwell is the most bimodal in the set, split by actor type: a ransomware/wiper actor's impact is a fast decisive burst, while an espionage "position for future" campaign may **never reach impact at all** — which is why the sweep is widest and the "never" end is expressed *structurally* (the tactic is simply absent from those objective-nets) rather than as a zero duration. §3 gives impact its own reset mechanism — **blast-radius limiting rather than gain invalidation**: an irreversible act on a held host cannot be "reset", but a mutation limits how many *further* hosts the impact reaches (Barach: encryption cut to 13.2%, mean-time-to-containment 91.4 s), so the reset rides the same reachability a topology shuffle governs and the payload act itself survives. Objective-conditioning is sharpest here (crit. 7): inert for espionage profiles, decisive for ransomware ones — a genuine discriminator, with the blast-radius reset fraction feeding the binding.
