---
status: durable
created: 2026-07-28
updated: 2026-07-29
---

# MTDSim Intent Spec — the literature-only yardstick

**What this is.** A unified specification of what the MTDSim lineage simulator is *documented to do*, derived exclusively from the four lineage papers. **No code was consulted in building this document** — no locators, no dispositions, no "the code does X". Where the papers are vague, that vagueness is recorded as a spec fact rather than resolved from implementation knowledge.

**Why it exists.** The standing risk in this project is conflating three different things when "fixing bugs": (1) genuine bugs (unintended behaviour with no paper basis), (2) documented design choices (paper-intended behaviour, however odd), and (3) undocumented inherited divergences (the code's reality, absent from every paper). The existing [`mtdsim_spec.md`](mtdsim_spec.md) is a *conformance* record — paper claims already entangled with code evidence and dispositions — so it cannot serve as an independent instrument. This file can: it is the paper side alone, built one paper per pass, and it is what the current implementation gets audited against.

**Primary source:** Brown 2023 (the foundational MTDSim paper) — every extractable spec and nuance, section by section. **Secondary sources:** Zhang 2023 (MTDSimTime), Ho 2024, Tay 2024 — included only where they modify or extend the core simulator. Brown's *experimental numbers are not endorsed* (per Marc: they may be wrong); what is normative here is the documented design, not the reported results.

---

## a) Sources and their standing

| Source | Artefact | Role | Conversion caveats |
|---|---|---|---|
| Brown 2023, *Evaluating Moving Target Defenses against Realistic Attack Scenarios* (EnCyCriS) | `docs/sources/lit_review/brown2023.md` | **Primary.** Foundational MTDSim: network model, 6 techniques, 2 scenarios, attack procedure, interaction classes, Table I | Fig 1 (HARM) and Fig 2 (host layer) remain omitted images. **Fig 3 (attack-procedure flowchart) recovered 2026-07-29** — supplied directly by Marc, transcribed in full at the head of §j and normative there |
| Zhang 2023, *Evaluating Multiple MTD in the Time Domain* (masters thesis) | `docs/sources/lit_review/zhang2023.md` | Secondary. Time-domain refactor (MTDSimTime): SimPy, execution schemes, resource occupation, exponential time, MTTC/NCR, adversary profile dimensions | **Eqs 1–2 (`T_Aphase2`), Fig 1 (structure), Fig 4 (execution-scheme flow) and Fig 7 (attack action flow) recovered 2026-07-29** — supplied by Marc; folded into IS-TIM-06/07, IS-ARC-01, IS-SCH-01 and §j. Figs 3, 5–6 still omitted |
| Ho 2024, *Using AI to Automate the Deployment of MTD Operation* (honours) | `docs/sources/lit_review/ho2024.md` | Secondary. 11-metric suite, Static Degrade Factor, DDQN action space, evaluation pipeline | Most formula images omitted; prose definitions survive and are used here |
| Tay 2024, *Using AI to Automate the Deployment of MTD Operations* (honours, MTDShield) | `docs/sources/lit_review/tay2024.md` | Secondary. Reactive plugin contract, 5-action set, detection-rate feed | Eq 1 and Figs omitted; prose survives |

The source markdown files are the citable artefacts (gitignored; read in-session). Per-paper extraction notes in [`../sources/extractions/`](../sources/extractions/) were used only to confirm the Zhang Eq 1–2 gap, not as a content source.

## b) Precedence rule — how to read the lineage

Brown 2023 → Zhang 2023 → Ho 2024 → Tay 2024 is an evolution, not four competing specs. When auditing the *current* substrate (an MTDSimTime descendant):

1. Where a later paper **explicitly documents a change** to an earlier behaviour (e.g. Zhang replaces Brown's uniform MTD trigger with exponential — IS-TIM-01/02), the later paper's version is the operative intent, and matching Brown instead is itself a divergence.
2. Where a later paper is **silent**, Brown's intent stands.
3. Where papers **conflict without either acknowledging the other** (§m), neither wins here — the conflict is recorded and the disposition is Marc's.

## c) The classification procedure (use this when auditing code)

For each spec row, the audit classifies the code's behaviour as exactly one of:

- **CONFORMS** — matches the operative intent under the precedence rule.
- **CONFORMS-SUPERSEDED** — matches an earlier lineage intent that a later paper documentedly replaced (e.g. Brown-era behaviour surviving under Zhang's refactor). Not a bug; a lineage-lag design fact to parameterise or document.
- **DIVERGES-DOCUMENTED-NOWHERE** — matches no paper's documented intent. *Candidate bug* — but only Marc's disposition makes it one. Evidence for "bug": violates an invariant the papers state, or entered via an unexplained commit. Evidence for "undocumented design choice": deliberate-looking, self-consistent, load-bearing.
- **UNTESTABLE** — the spec row is design-intent prose with no observable code surface (tagged `[intent]` below).

A "fix" is legitimate only against rows classified as bugs *after* disposition — never directly from a paper-code mismatch, because the mismatch may be the design (guardrail: papers are claims to reconcile with the code, not ground truth about it).

**Test-surface tags** used below: `[behav]` observable in a run/trace; `[config]` a constant or table checkable statically; `[struct]` architectural shape; `[intent]` design rationale only.

---

## d) Architecture and modules

| ID | Intended behaviour | Source | Notes |
|---|---|---|---|
| **IS-ARC-01** | The simulator comprises three modelled entities: the **System** (network), the **Attacker**, and the **Defense** (MTD) | Brown §III; Zhang Fig 1 | Zhang §4.1 restates as Simulated Network / MTD Techniques / Adversary modules, with MTD Operation and Attack Operation as their action surfaces. Tay §4 (Fig 1) restates the same three, labelled Network (b), MTD (c), Attacker (a). **Zhang Fig 1 recovered 2026-07-29**, and names the three couplings between them: `MTD Techniques → MTD Operation`, which *"retrieve/release resource for reconfiguration"* against the Simulated Network; `Adversary → Attack Operation`, which *"discover/compromise hosts"* on the same network; and a direct `MTD Operation → Attack Operation` edge labelled ***"interrupt attack actions"***. The interruption path is thus architectural, not incidental — it is one of only three labelled edges in the structure diagram. `[struct]` |
| **IS-ARC-02** | The System is captured as a **3-layer HARM**: Hosts, Services, Vulnerabilities — one graph generated per component. Extends Alavizadeh's 2-layer HARM by adding the **service layer**, added specifically to model realistic attack behaviour | Brown §III-A, Fig 1 | Zhang §4.2.1 names the layers: `AGn` (host attack graph), `AGh` (services-on-host graph), `ATs` (service attack tree). The "3 layers" are the *representation*, not the network's topological depth (cf. IS-PRM-01, which is a separate concept). `[struct]` |
| **IS-ARC-03** | The Attacker is a "theoretically intelligent adversary" following a **logical flowchart** inspired by the Cyber Kill Chain and MITRE ATT&CK | Brown §III, §III-C(2), Fig 3 | **Fig 3 recovered 2026-07-29** and transcribed at the head of §j — the flowchart is now the normative statement of the procedure, with IS-PRC-01..08 as its prose gloss. `[struct]` |
| **IS-ARC-04** | The framework exists to evaluate **combinations** of MTD techniques (single through triple in Brown; pairwise in Zhang) against multiple attack scenarios; other techniques are explicitly pluggable | Brown §III-B intro; Zhang §5.2 | `[intent]` |
| **IS-ARC-05** | Simulation is **discrete-event in the time domain** on SimPy — Zhang's headline refactor. Brown's original modelled time only as the MTD interval and ignored MTD execution time; Zhang documents this as the deficiency being fixed | Zhang §1, §3.3, §4.5 | Zhang's critique of Brown (§3.3) is itself spec-relevant: the *refactored* simulator must model both MTD interval **and** MTD execution duration. `[struct]` |

## e) Network model

| ID | Intended behaviour | Source | Notes |
|---|---|---|---|
| **IS-NET-01** | Inter-host topology generated with the **Barabási–Albert** model, "to generate small subnets in each level of depth", mimicking real-world network characteristics | Brown §III-A; Zhang §4.2.1 (`AGn`) | `[behav]` |
| **IS-NET-02** | Service connections on a host generated with the **Watts–Strogatz** model, representing "the regular nature of how services are connected on a host" | Brown §III-A; Zhang §4.2.1 (`AGh`) | `[behav]` |
| **IS-NET-03** | Host layer inputs: **total number of hosts**, of which some are **exposed hosts**, and a **number of levels** of depth (e.g. public, DMZ, application, database). The **first level consists only of exposed hosts**; all remaining hosts are **randomly assigned** to the other levels | Brown §III-A | `[behav]` |
| **IS-NET-04** | Each host is generated with its **own operating system, an ID, and services**; the OS decides which services can be found on the host; the host then randomly selects **3–11 compatible services** | Brown §III-A; Table I `[3, 11]` | `[behav]` `[config]` |
| **IS-NET-05** | The host's **ID decides the location** it can be found on the network | Brown §III-A | Underspecified in the paper (no mapping rule given) — vagueness is a spec fact. `[behav]` |
| **IS-NET-06** | Services are generated **per operating system** with a **50 % chance of being compatible with other operating systems** (cross-platform). Brown footnote 1: the 0.5 is arbitrary (no empirical study exists), explicitly intended to be user-replaceable | Brown §III-A + fn 1; Table I; Zhang §4.2.3 ("half of the newly created services") | `[config]` |
| **IS-NET-07** | Each service carries a **version number in [1, 99]**; **older versions have more vulnerabilities**. Brown footnote 2: 99 chosen as a reasonable upper bound (public repos rarely exceed version 20) | Brown §III-A + fn 2; Zhang §4.2.3 | Zhang adds: services have unique names; **same-name services may share vulnerabilities**. `[behav]` |
| **IS-NET-08** | Vulnerability lifecycle per version: each version has **a chance of introducing a new vulnerability**, which is **patched ~10 versions later on average** (removing it) | Brown §III-A | The per-version introduction probability itself is **not stated** — only the patch horizon. `[behav]` |
| **IS-NET-09** | **Version 99 always carries a vulnerability**, representing zero-days and ensuring the attacker can compromise **any** service | Brown §III-A | The stated *purpose* (every service compromisable) is normative, not just the mechanism. `[behav]` |
| **IS-NET-10** | Vulnerabilities carry an **attack complexity** (difficulty of exploiting, randomly generated in **[0.4, 1]**) and an **impact** (reward for compromise, randomly generated in **[0, 1]**), both derived from the CVSS scoring system | Brown §III-A; Table I | **Conflicts with Zhang on both counts** — see IS-CFL-01 (complexity range) and note that Zhang nowhere restates the impact range, leaving Brown's `[0, 1]` the only documented one. `[config]` |
| **IS-NET-11** | Each host has **5 user accounts**; each account has a **5 % chance of password reuse** across the network (deliberately modest vs. the >50 % reuse reported in the cited study), existing to enable credential-stuffing | Brown §III-B(3); Zhang §4.2.2 | Brown documents this under the User-Access-Shuffle section, but it is a *network-generation* fact. `[config]` |
| **IS-NET-12** | **Four OS types**: Ubuntu, CentOS, Windows, FreeBSD — each with its own set of services | Zhang §4.2.2 | Zhang addition (Brown names no OS list). `[config]` |
| **IS-NET-13** | Each host is assigned a **unique IP address** at network setup; the IP is what lets adversaries locate and pivot to the host | Zhang §4.2.2 | `[behav]` |
| **IS-NET-14** | Generation-parameter values are **placeholders** chosen to be plausible and to demonstrate the workflow; in practice users substitute real host/system values | Brown §III-A closing | `[intent]` — but it licenses the audit to treat parameter deltas as less severe than rule deltas. |

## f) MTD techniques (defence behaviours)

Brown documents **six** techniques. Zhang states the inherited codebase had **seven** implemented (see IS-CFL-06), selects four, and adds a new fifth (DAP). Semantics below are per the documenting paper.

| ID | Intended behaviour | Source | Notes |
|---|---|---|---|
| **IS-MTD-01** | **IP Shuffle**: randomly change **all internal hosts'** (virtual) IP addresses when triggered; interrupts any attacker operating with a stale IP | Brown §III-B(1); Zhang §4.3.1.2 | Zhang phrasing: "each involved host". `[behav]` |
| **IS-MTD-02** | **Port Shuffle**: randomly reassign the ports of **all exposed services** (virtual ports — service unaffected); interrupts any attacker using a stale port | Brown §III-B(2) | Brown-only; not in Zhang's selected set. `[behav]` |
| **IS-MTD-03** | **User Access Shuffle**: randomly change the user accounts on each host; defeats credential-stuffing (see IS-NET-11 for the account model) | Brown §III-B(3) | Brown-only. `[behav]` |
| **IS-MTD-04** | **Host Topology Shuffle**: swap **all** hosts with another host **within the same network layer** (VM-migration-like). Same-layer constraint is justified by assumed similar purpose → minimal disruption | Brown §III-B(4) | Brown-only. The same-layer constraint is explicit intent, not incidental. `[behav]` |
| **IS-MTD-05** | **Service Diversity**: replace **all services running on the host** — Brown: disconnects connections to the service, interrupting ongoing attacks; Zhang: randomly re-configure services **with different versions** (the 99-version pool is the diversity space) | Brown §III-B(5); Zhang §4.3.1.3 | Zhang's re-statement is more specific (version re-roll); treat Zhang's as operative for the time-domain substrate. `[behav]` |
| **IS-MTD-06** | **OS Diversity**: randomly change the OS on each host; services **incompatible with the new OS are also randomly changed** | Brown §III-B(6); Zhang §4.3.1.4 | Zhang: new OS drawn randomly from the four types. `[behav]` |
| **IS-MTD-07** | **Complete Topology Shuffle**: entirely regenerate the network's topology, changing every involved host's connection status with other hosts | Zhang §4.3.1.1 | First *documented* by Zhang (generalisation of SDN topology-shuffling literature); Ho §3.3.3 adds "**preserving the hosts** from the previous network". `[behav]` |
| **IS-MTD-08** | **DAP-optimised OS Diversity**: instead of random OS assignment, solve the Diversity Assignment Problem — **maximise network connectivity** under optimal OS-variant assignment. Abstraction for solving: a single endpoint host and single database host represent their classes; intermediate hosts are routing nodes; objective + constraint functions taken from the cited DAP literature (Newell et al.) | Zhang §4.3.1.5, Fig 3 | Zhang's one *new* technique. `[behav]` |
| **IS-MTD-09** | Techniques are classed by the **resource they serve**: network layer (IP Shuffle, Complete Topology Shuffle) vs application layer (Service Diversity, OS Diversity). This classing drives both scheduling contention (IS-SCH-04) and attacker-interaction semantics (IS-INT-*) | Zhang §4.3.3, §4.4.2 | Brown's equivalent classing is the three interaction classes (IS-INT-01..03), which additionally place Port Shuffle with the service-level class and User Shuffle in its own class. `[struct]` |

## g) MTD execution schemes and scheduling (Zhang)

Brown's only documented trigger model is a single global timer (IS-TIM-01). Everything in this section is Zhang's extension.

| ID | Intended behaviour | Source | Notes |
|---|---|---|---|
| **IS-SCH-01** | All schemes are **time-based proactive**: a periodic triggering signal drives a **register/trigger queue**: on signal, register a new MTD instance into a queue or trigger an existing one; the **highest-priority** instance is popped and deployed if there is no suspension issue; suspended instances are held in a **suspension queue** whose members have **higher pop priority than the main queue** | Zhang §4.3.2, Fig 4 | **Fig 4 recovered 2026-07-29** — the decision order is exactly: `Triggering Signal → [MTD queue empty?] —yes→ Register new MTD(s) → [Suspension queue empty?]`; `—no→ [Suspension queue empty?]` directly. Then `[Suspension queue empty?] —yes→ Trigger MTD(s) in MTD queue`, `—no→ Trigger MTD(s) in suspension queue`. Registration is therefore **conditional on the main queue being empty**, and the suspension queue's precedence is a branch, not a priority number. `[behav]` |
| **IS-SCH-02** | **Random execution**: on each signal, register one MTD selected at random from all techniques; trigger a single instance. Documented as the scheme the previous work (Brown) effectively used | Zhang §4.3.2.1 | `[behav]` |
| **IS-SCH-03** | **Alternative execution**: register/trigger one MTD at a time, selected **by fixed rotation based on the previously registered instance** (not randomly) | Zhang §4.3.2.2 | `[behav]` |
| **IS-SCH-04** | **Simultaneous execution**: trigger **all** techniques at each signal; among those contending for the same resource, the highest-priority deploys first; lower-priority ones go to the suspension queue and execute in the next cycle. Explicitly more resource-consuming at equal interval | Zhang §4.3.2.3 | `[behav]` |
| **IS-SCH-05** | **Resource occupation**: a triggered MTD must acquire the resource it serves (network layer / application layer); if occupied by an unfinished MTD, it is **suspended until the resource frees**. Worked example: IPShuffle and CompleteTopologyShuffle mutually exclude (both network-layer); ServiceDiversity deploys any time (application layer) | Zhang §4.3.3, Fig 6 | `[behav]` |
| **IS-SCH-06** | MTD priority exists as a concept (queue pop order, contention winner). **The priority ordering itself is never specified** in any lineage paper | Zhang §4.3.2–4.3.3 | Underspecification recorded as spec fact. Any concrete ordering in code is an undocumented choice, not a divergence from a documented one. `[struct]` |

## h) Time model

| ID | Intended behaviour | Source | Notes |
|---|---|---|---|
| **IS-TIM-01** | *(Brown, superseded)* MTD ("defense") trigger time ~ **Uniform(1000, 5000) ms**, E[T] = 3000 ms — randomises timing while keeping trigger frequency similar between trials | Brown §IV; Table I | Operative only for a Brown-faithful arm. `[config]` |
| **IS-TIM-02** | *(Zhang, operative)* The MTD interval is modelled with an **exponential distribution** — an explicit, documented replacement of Brown's uniform, argued as more realistic | Zhang §4.3.4 | The interval means (per scheme) are **not** in the thesis text beyond the tested 50–200 s range (IS-PRM-03). `[behav]` |
| **IS-TIM-03** | Each MTD technique has its own **execution duration**, sensitivity-selected: CompleteTopologyShuffle **110 s**, IPShuffle **100 s**, OSDiversity **80 s**, DAP_OSDiversity **80 s**, ServiceDiversity **70 s** — each with standard deviation **0.5** | Zhang §4.3.4, Table 3 | `[config]` |
| **IS-TIM-04** | The **exponential distribution is the primary PDF** for both (a) inter-event times (e.g. the MTD interval) and (b) action durations; µ is the historical average elapsed time (empirical study + sensitivity analysis) | Zhang §4.5, Eqs 3–4 | `[behav]` |
| **IS-TIM-05** | Attack-action timing by phase: **Phase 1 (port scan + credential stuffing) is constant time** (scan speed constant under a fixed strategy); **Phase 3 (brute force) has a specific time limit**; **Phase 2 (exploit) is variable** | Zhang §4.4.3 | `[behav]` |
| **IS-TIM-06** | Phase-2 duration over the service's vulnerability list `V = V_unexploited + V_exploited` **(Eq 1)** is **(Eq 2)**: `T_Aphase2 = [ Σ_{vi ∈ V_unexploited} (1 − AC_vi) + Σ_{vj ∈ V_exploited} (1 − AC_vj)/2 ] · T_Aexploit` | Zhang §4.4.3, Eqs 1–2 | **Recovered 2026-07-29** (Marc supplied the equation images; §q gap 1 closed). Now-exact normative content: phase-2 cost is a **sum over the whole vulnerability list**, each term linear in `(1 − AC_v)`, scaled by a common `T_Aexploit`, with **already-exploited vulnerabilities contributing at half weight**. Two things the prose alone did not pin: (a) `V_exploited` terms are *included in* the phase-2 cost, not skipped; (b) linearity in `(1 − AC_v)` fixes the polarity — higher `ACv` ⇒ *cheaper*, confirming IS-CFL-01's reading of Zhang's inverted semantics. `T_Aexploit` is §4.5's exponential time value. `[behav]` |
| **IS-TIM-07** | **Adversary learning**: exploitation time is **halved** for vulnerabilities that were **exploited in previous attack operations conducted on previous hosts** | Zhang §4.4.3 + Eq 2 | Prose implies a cross-host, per-vulnerability rule; per-instance vs per-type is not pinned by the text. **Eq 2 (recovered 2026-07-29) locates the mechanism**: the halving *is* the `/2` on Eq 2's `V_exploited` sum — the same rule as IS-TIM-06 rather than a separate discount elsewhere. The scope of `V_exploited` (per-host list vs global memory) remains unstated. `[behav]` |
| **IS-TIM-08** | **Confusion penalty**: the adversary takes a **time penalty each time an attack event is interrupted or stopped by MTD** | Zhang §4.4.3; Brown §V-A | Brown's original: time penalty on every block **plus forced re-scan** of the network. Both halves are intent. `[behav]` |
| **IS-TIM-09** | **Time-unit incoherence across the lineage** (recorded, not resolved): Brown quotes trigger times in **ms**; Zhang quotes durations/intervals in **seconds** (70–110 s, 50–200 s); Ho quotes the SDF in **ms** (2000 ms) while running finish-time 15 000 (unit unstated) | Brown Table I; Zhang Tables 2–3; Ho Table 2 | Any audit comparing code constants to paper values must resolve the unit convention first. `[config]` |

## i) Attacker model — scenarios and profile

| ID | Intended behaviour | Source | Notes |
|---|---|---|---|
| **IS-SCN-01** | Two attack scenarios with **identical capabilities, different goals, on identical initial networks** (same generated HARM for both) | Brown §III-C, §IV | `[struct]` |
| **IS-SCN-02** | **Scenario 1 (General / takeover)**: compromise the whole network; **prioritise the weakest host** to compromise as quickly/easily as possible, increasing the chance of credential reuse and known-vuln exploitation | Brown §III-C(1) | **Fig 3 (recovered 2026-07-29) contradicts this prose.** Box 2 is "Pick a Target Host from Priority Stack", annotated: *"Prioritises internal hosts that minimise the time it takes for the adversary to move to a compromised host to target it."* So the **implemented** priority is proximity to the attacker's foothold, not host weakness. Brown's §III-C(1) prose ("weakest host") and his own Fig 3 (nearest host) describe different rules; the figure is the one labelled "the attack procedure implemented in MTDSim". This also means Zhang's distance-based selection (IS-LIM-04) is **not a simplification of Brown but a restatement of him**. `[behav]` |
| **IS-SCN-03** | **Scenario 2 (Targeted / APT-style)**: compromise a specific target host; the attacker can identify target characteristics. Strategy: if the target is found during scanning → **attack only the target**; if not found → prioritise hosts **on the same level** as the target; else attack hosts that **appear to be on a different level**, to move toward the target's level | Brown §III-C(1) | `[behav]` |
| **IS-SCN-04** | **Give-up rule**: move on after **10 failed exploitation attempts** on the currently selected host — but in Scenario 2 the attacker **never gives up on the target node** | Brown §V-C; Table I (10) | `[behav]` |
| **IS-SCN-05** | Attacker skill is **uniform** — exploitation skill is not differentiated across adversaries (explicit limitation, deferred to future work) | Brown §V-C | `[intent]` |
| **IS-SCN-06** | *(Zhang)* Only **Scenario 1** is refactored into MTDSimTime (explicitly for time reasons); the targeted scenario is **out of the documented time-domain scope** | Zhang §4.4.1.1 | If targeted-scenario code exists in an MTDSimTime descendant, no lineage paper documents its time-domain semantics. `[struct]` |
| **IS-ADV-01** | Adversary profile has four documented dimensions: **attack objectives**, **exploiting vulnerabilities**, **command-and-control capabilities**, **user-credential exploitation** | Zhang §4.4.1 | The profile is a *description*, not a configurable parameterisation, in every lineage paper. `[struct]` |
| **IS-ADV-02** | **Host-compromise criterion**: "when **enough services** on a host have been compromised, the host is considered compromised" | Zhang §4.4.1.2 | "Enough" is never quantified in any lineage paper — the threshold is an undocumented choice wherever it lives. `[behav]` |
| **IS-ADV-03** | **C2 capability**: pivot from compromised hosts; form an attack path of compromised hosts to reach new hosts | Zhang §4.4.1.3; Brown §III-C(2) ("assume command and control functionality") | `[behav]` |
| **IS-ADV-04** | **Compromise persistence** — two documented versions: **Brown §V-B**: MTD that disrupts an attack path revokes the attacker's control of compromised hosts (monotonicity deliberately broken), with **instant re-recognition and re-control** if a network path to a previously compromised host is regained (justified: unchanged config → trivial re-exploit). **Zhang §4.4.1.3**: compromised hosts **always stay compromised** and are instantly recognised on regained access, *regardless of MTD changes* | Brown §V-B; Zhang §4.4.1.3 | See IS-CFL-02. Zhang's is the operative time-domain version under the precedence rule, but Zhang does not *acknowledge* the change — so this stays listed as a conflict for disposition, not silently resolved. `[behav]` |
| **IS-ADV-05** | **Credential exploitation**: compromising a host yields **all of its users**; these fuel credential-stuffing on other hosts; a successful stuff compromises the target host **without exploiting any vulnerability** | Zhang §4.4.1.4; Brown §III-C(2) | `[behav]` |

## j) Attacker model — procedure

Brown §III-C(2) prose **plus Fig 3 (recovered 2026-07-29)**, refined by Zhang §4.4.2 **plus Fig 7 (recovered 2026-07-29)**.

**Brown Fig 3, transcribed** (the ten boxes and every arrow — this is the normative
procedure, superseding the prose-only reconstruction the rows below were built from):

1. Host Discovery → 2
2. Pick a Target Host from Priority Stack *(annotation: prioritises internal hosts that
   minimise the adversary's movement time from a compromised host)* → 3
3. Port Scan → 4
4. Check if a Compromised User has Reused Credentials on Host *(annotation: the adversary
   collects user credentials from hosts it has compromised)* → 5
5. Find Vulnerabilities on Services → 6
6. Try to Exploit Vulnerabilities → 7
7. Check if the Host Has Been Compromised — **Success** → 9 · **Failure** → 8
8. Try To Brute Force A Login — **Success** → 9 · **Failure** → 10
9. Scan for Neighbors to the Recently Compromised Host → **2**
10. Check if there is another Host to Target — *"There is Another Host"* → 2 ·
    *"There is not Another Host"* → **1**

Two structural facts the prose did not carry: **9 returns to 2, not to 10** (a fresh
compromise re-enters target selection directly), and **10 is the only route back to 1**
(host discovery re-runs only when the stack is exhausted). Note also that Fig 3 draws
**4 → 5 unconditionally** — it has no success branch out of the credential check, whereas
§III-C(2)'s prose says exploitation is reached *only on stuffing's failure*. Prose is the
more specific statement; the tension is recorded, not resolved.

**Zhang Fig 7, transcribed** (the time-domain action flow, and the interruption scoping
that IS-INT-04/05 describe in words):

- Action chain: `Scan Host → Enum Host → Scan Port & Exploit User Credential (Phase 1) →
  Exploit Vulnerabilities (Phase 2) → Brute Force (Phase 3)`; a **host-compromised** edge
  runs from Phase 2 / Phase 3 to `Scan Neighbour`, and `Scan Neighbour → Enum Host`.
- **Network-layer MTD** (green) encloses **every** action — Scan Host through Scan
  Neighbour — and returns to **Scan Host**.
- **Application-layer MTD** (orange) encloses **only Phases 1–3** — it does *not* reach
  Scan Host, Enum Host or Scan Neighbour — and returns to **Phase 1**.

The two enclosures are the figure-level statement of the conditional-interrupt rule: the
scoping is by action class, and the recovery point differs by layer.

| ID | Intended behaviour | Source | Notes |
|---|---|---|---|
| **IS-PRC-01** | **Host discovery** first: scan the network to discover **all exposed hosts**; internal hosts are visible **only if a path exists through a compromised or exposed internal host** | Brown §III-C(2) | Zhang names the actions "Scan Host" and "Enum Host" (reconnaissance), ending in selection of a target host. `[behav]` |
| **IS-PRC-02** | **Host reconnaissance** next: port scans discover **exposed services**, or internal services connected to an already-compromised service | Brown §III-C(2) | `[behav]` |
| **IS-PRC-03** | **Credential stuffing is attempted first**, using user-account information from previously compromised hosts — Zhang folds this into **Phase 1 "Scan Port & Exploit User Credential"**; only on its failure does the adversary proceed to exploitation | Brown §III-C(2); Zhang §4.4.2 | `[behav]` |
| **IS-PRC-04** | **Exploit selection**: a service from the scan is selected; the vulnerabilities from **all scanned services** are placed into a **priority stack ordered by RoA** (return on attack) | Brown §III-C(2) | Zhang's Phase 2 "Exploit Vulnerabilities" targets the services discovered in Phase 1 but does not restate the RoA stack — Brown's ordering rule stands per precedence. `[behav]` |
| **IS-PRC-05** | **On successful compromise**: assume C2 functionality — internal services and hosts connected to the compromised host become visible. Zhang names this **"Scan Neighbour"**, performed after every successful attack event | Brown §III-C(2); Zhang §4.4.2 | `[behav]` |
| **IS-PRC-06** | **On exploit failure**: commence a **brute-force attack** (Zhang: Phase 3, brute-forcing a user login, time-limited). Success in any phase compromises the host | Brown §III-C(2); Zhang §4.4.2, §4.4.3 | `[behav]` |
| **IS-PRC-07** | **If all attack options fail**: choose another host to exploit | Brown §III-C(2) | Interacts with the give-up rule IS-SCN-04 and the interruption threshold IS-INT-06. `[behav]` |
| **IS-PRC-08** | The attacker **always** follows the procedure to decide its next move — no off-flowchart behaviour | Brown §V-A | `[struct]` |

## k) MTD–attacker interaction

Brown defines three interaction classes by what the attacker loses; Zhang recasts them as network-layer blocking vs application-layer interruption.

| ID | Intended behaviour | Source | Notes |
|---|---|---|---|
| **IS-INT-01** | **Connection-to-host lost** (IP Shuffle, Host Topology Shuffle): the attacker's connection terminates/times out; being uncertain of host status, the attacker is **forced to re-perform host discovery** to find new paths | Brown §III-D(1) | `[behav]` |
| **IS-INT-02** | **Connection-to-service lost** (Service Diversity, OS Diversity, Port Shuffle): ports or services (and hence vulnerabilities) change; the attacker is **blocked from compromising the vulnerability** and forced to **re-run a port scan** | Brown §III-D(2) | `[behav]` |
| **IS-INT-03** | **User access changed** (User Shuffle): blocks the attack **only if the attacker is mid-credential-stuffing**; the attacker is then forced to look for vulnerabilities on the host instead | Brown §III-D(3) | The narrow blocking condition is explicit intent. `[behav]` |
| **IS-INT-04** | *(Zhang)* **Network-layer MTD** (IP Shuffle, Complete Topology Shuffle) deployment makes the attack event **fail immediately** upon the adversary's discovery of a host — connection paths/IPs changed, adversary blocked from connecting | Zhang §4.4.2 | Time-domain recast of IS-INT-01. `[behav]` |
| **IS-INT-05** | *(Zhang)* **Application-layer MTD** (OS Diversity, Service Diversity) **cannot block** attack actions (topology unaffected) but **interrupts** them; the adversary must **restart from Phase 1 regardless of prior progress** | Zhang §4.4.2 | `[behav]` |
| **IS-INT-06** | *(Zhang)* Each attack action has a **limited number of attempts**; if interruptions by application-layer MTD reach a **threshold**, the attack event fails and the adversary shifts to other hosts | Zhang §4.4.2 | Threshold value unstated by Zhang. Distinct trigger from Brown's 10-failed-exploits rule (IS-SCN-04): one counts MTD interruptions, the other failed attempts. Both are documented intent. `[behav]` |
| **IS-INT-07** | Every MTD block/interrupt carries the **confusion cost**: time penalty + forced re-scan (see IS-TIM-08) | Brown §V-A; Zhang §4.4.3 | `[behav]` |

## l) Parameters and configuration tables

| ID | Intended behaviour | Source | Notes |
|---|---|---|---|
| **IS-PRM-01** | Brown Table I baseline: total hosts **200**; exposed hosts **20**; layers **5**; subnets **20**; services/host **[3, 11]**; vuln cross-platform **0.5**; attack complexity **[0.4, 1]**; impact **[0, 1]**; attack attempts before giving up **10**; defense trigger **Uniform(1000, 5000) ms** | Brown Table I | "Layers = 5" is network *depth*, a different concept from the 3-layer HARM representation (IS-ARC-02). `[config]` |
| **IS-PRM-02** | Zhang Table 2 network geometries: nodes/density/endpoints/layers = **25/0.093/3/4**, **50/0.052/5/4**, **75/0.040/7/4**, **100/0.043/10/4** | Zhang §5, Table 2 | `[config]` |
| **IS-PRM-03** | Zhang evaluation protocol: MTD intervals **50–200 s** (four values); terminating condition **NCR = 0.8**; **100 runs** per variable set | Zhang §5 | NCR = compromised hosts / total hosts, used as the simulation checkpoint. `[config]` |
| **IS-PRM-04** | Ho simulator settings: start **0**, finish **15 000**; total nodes **150**; Static Degrade Factor **2000 ms**. Ho distinguishes a "**Network Size**" parameter (100/150/200) from "Number of Nodes" (held at 150) — network size varies while node count stays fixed, to vary **density** | Ho Tables 2, 6, 7; §3.3.1, §4.2.3 | The Network-Size-vs-nodes distinction implies a documented **size/area parameter independent of node count** in the network generator. `[config]` |
| **IS-PRM-05** | Ho/Tay learning defaults: γ **0.95**, ε **1.0**, ε_min **0.01**, ε-decay **0.995**, training start **1000** samples, **100** episodes. Tay's tuned bests: γ ∈ **[0.75, 0.90]** (best 0.85), ε **0.5** with decay **0.99**, train start **2000** | Ho Table 1; Tay §5.2, §6.1–6.3 | Plugin-side. `[config]` |

## m) Metrics and evaluation semantics

| ID | Intended behaviour | Source | Notes |
|---|---|---|---|
| **IS-MET-01** | Brown's two metrics: **total attack actions blocked** and **average attempts required to compromise** — chosen as the simplest metrics valid across multiple scenarios (cost/RoA/P(success) excluded as dependent on external factors) | Brown §IV | `[behav]` |
| **IS-MET-02** | **MTTC** is Zhang's headline metric; Ho's formula: **mean duration of `SCAN_PORT`, `EXPLOIT_VULN`, `BRUTE_FORCE` events for all relevant hosts**; 0 if no attack events | Zhang §3.4, §5; Ho §3.3.2 (#8) | `[behav]` |
| **IS-MET-03** | **NCR** (network compromise ratio) = compromised / total hosts; **0.8 is the terminating checkpoint** for Zhang's evaluations | Zhang §5 | `[behav]` |
| **IS-MET-04** | Ho's 11-feature metric suite, with prose definitions: **APE** (mean new-vulnerability-percent over hosts on the shortest attack path; V_new(h)=0 if none), **Risk** = CSP(h)·AI(h), **RoA** = Risk / AC with **AC defined as time-to-exploit**, **HCR** = C_t / T_host, **Attack Stage** (integer enum, `SCAN_PORT`…`BRUTE_FORCE`, default value when no attack), **ASR** = compromised / attempted where attempts count `SCAN_PORT` + `EXPLOIT_VULN` + `BRUTE_FORCE` (0 if no compromises), **MEF** = N_MTD / (finish_last − start_first) (0 if none), **MTTC** (IS-MET-02), **TSLM** = now − time of last MTD execution, **SAPV** (set difference of consecutive shortest-path sets), **NAV** (address changes normalised by state size, ∈ [0, 1]) | Ho §3.3.2, Table 3 | Exact formula images omitted; prose fully pins all but the SAPV/NAV set constructions, which are pinned to their cited T-HARM lineage. `[behav]` |
| **IS-MET-05** | Ho evaluation pipeline: **five checkpoints per trial → mean per trial → median across trials**; final score = **equal-weighted sum of ASR, ROA, APE, Risk**, each **normalised against a no-MTD baseline run** (minimised metrics scaled baseline/value; maximised value/baseline); larger = better | Ho §3.4.1–3.4.2; Tay §5.1 | Tay's baseline normalisation adds MTTC to the five reported metrics. `[behav]` |

## n) Reactive/AI extension contract (Ho + Tay — the plugin seam)

Included because these papers extend the *core simulator's* surface: a reactive trigger path, a forced-trigger clock, and an attacker-information feed.

| ID | Intended behaviour | Source | Notes |
|---|---|---|---|
| **IS-AI-01** | **MTDShield is a plugin** that converts the time-based simulator to a **reactive** one: it receives network-posture information in real time from the network module, decides whether triggering an MTD would improve posture, selects the technique, and deploys it **via the existing MTD operations module** | Tay §4, Fig 1 | The deployment path *through* the core MTD module (not around it) is part of the contract. `[struct]` |
| **IS-AI-02** | **Static Degrade Factor (SDF)**: if (now − last MTD trigger) exceeds the SDF (default **2000 ms**), the system **forces a random MTD** (within the selected deployment type) and resets the interval counter; the check runs **before** network metrics are fed to the AI model | Ho §3.1.2, Fig 2 | Core-touching: requires the simulator to track last-MTD-trigger time. `[behav]` |
| **IS-AI-03** | **Action space — two documented versions**: Ho §3.2.3: singles + **pairwise combinations** + Null; Tay §4.1/§4.1.4: exactly **five actions** — IP Shuffle, OS Diversity, Service Diversity, Complete Topology Shuffle, no-deploy — with a 5-unit Q-output layer | Ho §3.2.3; Tay §4.1.4 | See IS-CFL-05. `[struct]` |
| **IS-AI-04** | **Model architecture** (joint Ho/Tay): static branch Dense-128 → ReLU → BN → Dense-64 → ReLU → BN → 30 % dropout; time-series branch LSTM-64 (return sequences) → ReLU → BN → LSTM-32 → ReLU → BN → 30 % dropout; fusion = concat → Dense-64 → ReLU → BN → 30 % dropout → Q-output. Double DQN (main + periodically-copied target network) with experience replay | Tay §4.1.1–4.1.4, §4.2; Ho §3.2.2 | Static-branch inputs (Tay): HCR, number of vulnerabilities, number of **exposed** vulnerabilities, APE score. Time-series inputs: MTTC variation, MTD deployment intervals, **downtime/operational impact for node replacement**, TSLM. `[struct]` |
| **IS-AI-05** | **Reward** = f(N_{t+1}) − f(N_t) over the selected features; multi-metric rewards are a **weighted sum with w_i = ±1 by feature direction**, features **min-max normalised against in-memory history** per calculation; learning begins only after the training-start sample count | Ho §3.2.4 | `[behav]` |
| **IS-AI-06** | **Attacker detection rate (IDS-sensitivity) feed**: the model can be fed a fraction (0–100 %) of information about the attacker's actions during training; performance degrades marginally from 1.0 down to 0.7, then a **cutoff at ≈ 0.7** below which performance decorrelates from the detection rate | Tay §5.3, §6.4 | Core-touching: requires the simulator to expose attacker-action information at a configurable rate. `[behav]` |

## o) Explicit non-features and declared simplifications

Documented *absences* — code implementing these is beyond-paper behaviour, not conformance.

| ID | Declared limitation | Source |
|---|---|---|
| **IS-LIM-01** | No modelling of attacker skill levels (uniform capability) | Brown §V-C |
| **IS-LIM-02** | Randomness-of-confusion is approximated by penalty + re-scan only; better confusion models deferred | Brown §V-A |
| **IS-LIM-03** | MTD reconfiguration applies to **all nodes**; selective/critical-node deployment explicitly not implemented | Zhang §6.4 |
| **IS-LIM-04** | Target selection is **by distance to discovered hosts** — acknowledged as a simplification (no difficulty-aware selection) | Zhang §6.3 · cf. Brown Fig 3 box 2 |
| **IS-LIM-05** | Suspension-mechanism/deployment-frequency relationship not investigated; deployment frequency does **not** necessarily rise with shorter intervals due to resource occupation | Zhang §6.1 |
| **IS-LIM-06** | One adversary type only in the AI-era simulator; no adaptive/intelligent attackers | Ho §5.1; Tay §7 |
| **IS-LIM-07** | No QoS/performance-side modelling (downtime cost is a *feature input*, not a simulated effect) | Zhang §6.4; Ho §5.2 |

## p) Inter-paper conflicts — record only, disposition is Marc's

| ID | Conflict | Positions | Notes |
|---|---|---|---|
| **IS-CFL-01** | **Attack-complexity range** | Brown Table I: **[0.4, 1]** · Zhang §4.4.3: **ACv ∈ [0, 1]** (0 = unexploitable, 1 = easiest) | Zhang also inverts the *semantics* (Brown: complexity = difficulty; Zhang: higher = easier). Both range and polarity need disposition before any "fix". |
| **IS-CFL-02** | **Compromise persistence under MTD** | Brown §V-B: MTD disrupting the path revokes control (+ instant re-control on path regain) · Zhang §4.4.1.3: always stay compromised regardless of MTD | Precedence favours Zhang for the time-domain substrate, but Zhang never flags the change — treat as undocumented simplification pending disposition. |
| **IS-CFL-03** | **Trigger distribution** | Brown §IV: Uniform(1000, 5000) ms · Zhang §4.3.4: exponential | *Documented* replacement (Zhang cites and rejects the uniform) — resolved by precedence; listed for completeness. |
| **IS-CFL-04** | **Scenario scope** | Brown: two scenarios are a headline contribution · Zhang §4.4.1.1: only Scenario 1 refactored | Documented narrowing, resolved by precedence; the targeted scenario has **no** time-domain spec. |
| **IS-CFL-05** | **AI action space** | Ho §3.2.3: singles + pairwise + Null · Tay §4.1.4: 5 actions (4 singles + no-op) | Same jointly-developed model described incompatibly. Unresolvable from the papers. |
| **IS-CFL-06** | **Technique count in the inherited codebase** | Brown documents **6** techniques · Zhang §4.3.1: "seven MTD techniques were implemented" in the previous work | The seventh is undocumented by Brown; Zhang's Complete Topology Shuffle (IS-MTD-07) is the likely candidate but the thesis never says so. Verify. |
| **IS-CFL-07** | **Impact range** | Brown Table I: **[0, 1]** · no later paper restates it | Not an inter-paper conflict strictly — recorded because the only documented range is Brown's, so any other scale found in code is `DIVERGES-DOCUMENTED-NOWHERE`. |

## q) Known extraction gaps (unrecoverable from the source conversions)

**Four of the five gaps closed 2026-07-29** — Marc supplied the missing images (Brown
Fig 3; Zhang Figs 1, 4, 7; Zhang Eqs 1–2). Their content is folded into the rows above and
transcribed in §j; this list records what remains.

1. ~~**Zhang Eqs 1–2** — the exact `T_Aphase2` / `T_Aexploit` formula (IS-TIM-06).~~
   **CLOSED 2026-07-29.** Equation folded into IS-TIM-06; it also settles IS-TIM-07's
   mechanism and independently confirms IS-CFL-01's polarity reading.
2. ~~**Brown Fig 3** — the attack-procedure flowchart.~~ **CLOSED 2026-07-29.** All ten
   boxes and every arrow transcribed at the head of §j. It **contradicts Brown's own
   §III-C(1) prose** on host priority (see IS-SCN-02) — the one place where recovering the
   figure changed an intent, rather than merely confirming one.
3. **Partially closed.** ~~Zhang Figs 4, 7~~ and ~~Zhang Fig 1~~ recovered (IS-SCH-01,
   IS-INT-04/05 + §j, IS-ARC-01). Still unrecovered: **Zhang Figs 5–6** (execution-scheme
   and resource-occupation flows — prose descriptions used, IS-SCH-02..05), **Zhang Fig 3**
   (the DAP abstraction, IS-MTD-08), **Ho Figs 1–4**, **Tay Figs 1–2**.
4. **Brown Figs 4–5 / Zhang Figs 8–14 / Ho–Tay results figures** — experimental results;
   deliberately out of scope (results are not endorsed as spec).

---

## Audit protocol for the next session (the intended consumer)

1. Work one section at a time (d → n); for each row, locate the code surface(s) and classify per §c. Cite code locators in the *audit record*, never back into this file — this file stays literature-only.
2. Rows tagged `[config]` first (cheap static checks), then `[behav]` via the trace tooling (`python -m mtdnetwork.trace`), then `[struct]`.
3. Where this spec and [`mtdsim_spec.md`](mtdsim_spec.md) disagree about what a paper says, **this file wins for the paper side** (it was built without code contamination) — but flag the delta rather than editing either silently.
4. Output: a conformance table keyed by IS-IDs with the four-way classification, feeding a disposition list for Marc. Only after Marc's dispositions do any classifications become "bugs to fix".
