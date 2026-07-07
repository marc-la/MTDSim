---
tactic: defense-impairment
attack_id: TA0112
attack_url: https://attack.mitre.org/tactics/TA0112/
attack_version: 19.1
status: stub
group_hypothesis: stealth-low-and-slow
tier_hypothesis: 3 declared
---

# Defense Impairment — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

> **v19.1 note:** `defense-impairment` (TA0112) is the *disabling/degrading-defences*
> half split out of the old `defense-evasion` in v19.1; the *hiding/evasion* half
> is `stealth` (TA0005). Pre-split "defense-evasion" literature must be allocated
> between the two — capture only the disabling-defences portion here.

## 1. Tactic & role

Defense Impairment is defined in the pinned v19.1 bundle as the phase where "the
adversary is trying to break security mechanisms, pipelines, and tooling so defenders
can't see or trust what's happening": techniques that degrade, disable, or undermine the
effectiveness and trustworthiness of security controls and monitoring, characterised by
"direct interference with defensive systems", with the goal of reducing defenders'
ability to detect, interpret, or respond
([TA0112](https://attack.mitre.org/tactics/TA0112/)).

**The v19.1 split.** This is the newly-created half (new id TA0112) of the former Defense
Evasion tactic, split out in ATT&CK v19 (28 April 2026). Where its sibling Stealth covers
hiding from intact defences, Defense Impairment covers actively breaking them — MITRE's
shorthand is "Stealth is about hiding from your defenses; Impair Defenses is about
breaking them", a distinction that maps to different defensive responses (behavioural
analytics vs tamper protection)
([Defense Evasion Split: A Tale of Two Tactics](https://medium.com/mitre-attack/defense-evasion-split-a-tale-of-two-tactics-5d533545fa32)).
It inherited the **interference** half: disabling or tampering with security tooling
(Disable or Modify Tools T1685 — its dominant technique at 188 procedures, Disable or
Modify System Firewall T1686, Safe Mode Boot T1688), subverting trust and authentication
controls (Subvert Trust Controls T1553, Modify Authentication Process T1556), tampering
with configuration and policy (Modify Registry T1112, Domain or Tenant Policy
Modification T1484, File and Directory Permissions Modification T1222), suppressing
logging (Prevent Command History Logging T1690), network-device and cloud-infrastructure
weakening (Weaken Encryption T1600, Modify System Image T1601, Network Boundary Bridging
T1599, Modify Cloud Compute Infrastructure T1578, Modify Cloud Resource Hierarchy T1666),
and dedicated exploitation/downgrade (Exploitation for Defense Impairment T1687, Downgrade
Attack T1689). MITRE notes some behaviours are deliberately mapped to *both* tactics where
intent is mixed — Modify Registry T1112 and Modify Authentication Process T1556 appear
here and in Persistence/Credential Access.

Positionally it is the eighth tactic, adjacent to Stealth. It is markedly smaller than
its sibling (18 parent techniques, 38 subs, 632 procedures across 252 malware): its
most-attributed procedures involve taking down the defensive surface directly — disabling
event logging, killing EDR and backup services — a higher-privilege, higher-signal act
than concealment, which sets up the group-assignment question in §2.

## 2. APT relevance — group-assignment argument

Defense Impairment is the second tactic (with [[04_execution]]) where the profile
**questions its `stealth-low-and-slow` hypothesis.** The v19.1 split makes the tension
visible: where Stealth hides from intact defences, Defense Impairment *breaks* them — "a
higher-privilege, higher-signal act than concealment" (§1). Alshamrani, whose APT is defined
by evasion, is notably thin on *disabling* defences: its adversary "keep[s] low to go
undetected" and evades signature-based AV rather than tearing down the logging pipeline
([`alshamrani2019`](../extractions/alshamrani2019.md) §II-A, §IV-A) [fetched] — so the
paper's abundant defense-evasion evidence allocates to [[07_stealth]], and Defense Impairment
inherits little of it. That near-absence is itself the finding: the low-and-slow APT the
corpus documents prefers to *avoid* defences rather than *disable* them.

Where disabling does occur it reads as punctuated and decisive — killing EDR, disabling
event logging, stopping backup services — often immediately before a noisy objective (the
ransomware pattern), not as a low-and-slow dwell. This pulls Defense Impairment toward the
fast / objective-adjacent end rather than the stealth group. The profile therefore **does
not confirm** `stealth-low-and-slow`: it records the group as genuinely uncertain — an
evasion-avoidant APT rarely visits it, and when a smash-and-grab or ransomware actor does it
is a brief decisive act — and flags the **widest sweep in the set** until §5 and the runner
resolve whether it belongs with stealth, with objective-execution, or as its own near-exploit
act. No point number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

Disabling a defensive control (killed EDR, disabled Event Log, stopped backup service, a loaded
BYOVD driver, firewall/registry tamper) is **host-local software state, not network position or
knowledge** — so under the reset model it patterns with the *capability/conquest* side and
**survives** a network-layer mutation. An IP or topology shuffle re-addresses and re-links the
host but leaves the killed control exactly as the attacker left it; no re-disable is required.
This is the opposite verdict from [[01_reconnaissance]]/[[10_discovery]] and it is confirmed at
the code level: the substrate's `ipshuffle`/`portshuffle`/`*topologyshuffle` operations mutate
network position only and never touch host compromise or host software state. The *only* MTD
modality that would invalidate the gain is one that **rebuilds the host from a clean image** —
the software-rejuvenation analogue, closest to `OSDiversity` read as a reprovision — which
restores the control as a byproduct. So the reset is modality-split: **survives shuffle,
invalidated only by reimage/reprovision.**

A second durability axis, orthogonal to the shuffle, is worth stating because it makes the gain a
*maintained, decaying* capability rather than a one-shot conquest like a harvested credential:
process-kill is transient and needs an active watchdog to stay down; a registry `Start=4` disable
survives reboot but is reboot-gated and tamper-protected; only kernel-level BYOVD reliably
defeats tamper protection (real-world dwell of ~15 days on a persistent vulnerable-driver
technique). So survival against the network shuffle is *total*, but the gain's intrinsic
half-life against a host refresh varies by technique. **Reset verdict: survivor under shuffle,
reset only by reprovision; sweep width widest in the set** — compounded by the group-uncertainty
already flagged in §2 (an evasion-avoidant APT rarely disables; a ransomware actor does it fast
and hard).

What is **not captured** — and this is the dominant caveat: the substrate **represents no
defensive-control state on hosts at all** (detection/IDS is culled —
[substrate primer](../specs/substrate_primer.md) §(f)), so there is nothing for the attacker to
disable and nothing for a reprovision to restore. The survivor verdict above is therefore a
*conceptual/thesis-level* verdict — the direction the interaction *would* take were defences
modelled — not something the simulator computes today. Impair-Defenses also shows up in the data
as **prevalence, not dwell** (measured as %-of-cases; a punctuated, objective-adjacent act before
a noisy payload), which is why the tactic stays Tier-3 declared with the widest sweep. The formal
precedent for treating "defences the attacker must bypass" as a modelled gate with declared
per-step effort is MAL/coreLang ([`timed_attack_models`](../extractions/timed_attack_models.md)),
should defences ever be restored to the substrate.

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0112 page | New v19.1 tactic; Disable or Modify Tools T1685 dominant (188 procedures); **no timing** | Disabling defences directly; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-A, §IV-A | APT *evades* (signature-AV) rather than disables; defense-evasion evidence is hiding → allocated to [[07_stealth]] | Documented near-absence — the low-and-slow APT rarely disables; supports the group-uncertainty finding | [fetched] |
| [`he2025`](../extractions/he2025.md) §IV | MTD-AD = decision-boundary perturbation vs adversarial-ML *detector evasion*; adaptive attacker aware of the defence | Nearest analogue is detector-evasion (a stealth/impairment concept), not APT network compromise; no per-tactic dwell | [fetched] |
| [`selmanaj2024`](../extractions/selmanaj2024.md) Ch. 4 (Defense Evasion) | The *disabling* half — "uninstalling or disabling security software to prevent it from detecting malicious actions" — allocates here; Selmanaj's lead example (Duqu token-theft) is a *stealth* behaviour, not a disable | Confirms the v19.1 disable-scope allocation and the Step-B finding that the evasion-avoidant APT rarely *disables* defences (genuinely unsettled group); no number | [fetched] |
| [`ling2023`](../extractions/ling2023.md) Appendix A (Inhibit Response Function) | The ICS analogue of disabling defences maps predominantly to *Denial of Service* (Alarm Suppression, Service Stop, Block-Command), but is mixed (Manipulate I/O Image → Memory) | Nearest empirical shape for defence-degradation is DoS-like; still no dwell — Tier-3 declared, widest sweep | [fetched] |
| [`ransomware_timing`](../extractions/ransomware_timing.md) (Talos 2025; Huntress 2025) | Talos: ransomware dwell **17–44 d**, Interlock 17 d access→encryptor; **100% of ransomware orgs lacked/bypassed MFA**, EDR missing/misconfigured >25% — Impair Defenses (T1562) is measured as **%-of-cases, not a duration**. Huntress: access→deploy avg **~17 h**, fastest **~4 h**, ~18 pre-payload actions | Direct evidence that defence-disabling is a *prevalence* phenomenon, not a per-phase dwell — confirms the gap-documenting result and the **widest sweep**; the whole-chain timing is bimodal (hours↔weeks) | [fetched] |
| [`timed_attack_models`](../extractions/timed_attack_models.md) (coreLang 2020) | MAL models *defenses* as gating entities that block attack steps when TRUE, and assigns each attack step a **declared probability distribution** for the effort to complete it | Formal precedent for treating "defences the attacker must bypass" as a modelled gate + declaring per-step effort — legitimises Tier-3 declared for this tactic; no dwell value | [fetched] |
| — (no in-corpus per-tactic timing) | No extraction assigns a defense-impairment duration | Documented negative; Tier-3 declared, widest sweep | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn stealth-low-and-slow>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 3 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
