# MTD address-shuffle / decoy disruption of scanning-shaped tactics (extraction notes)

> A themed bundle of MTD-effect papers extracted **for §3 (MTD interaction) and
> the sweep-width of the scan-shaped tactics** — reconnaissance
> ([`01_reconnaissance`](../tactic_profiles/01_reconnaissance.md)) and discovery
> ([`10_discovery`](../tactic_profiles/10_discovery.md)) — plus the shared
> reset-vs-dwell *ratio* mechanism that governs every tuned tactic. These are the
> closest the literature comes to the genuine unknown
> ([`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md) §5):
> how a defensive move perturbs an attacker. **All timing here is declared /
> modelled, not empirical APT dwell** — they price the *effect of a shuffle
> interval*, which is exactly what §3's reset verdict + sweep need.
> Source files (gitignored): `1_recon/Analysis_of_network_address_shuffling…md`,
> `1_recon/2808475.2808480.md`, `1_recon/Parameterizing_Moving_Target_Defenses.md`,
> `1_recon/sec21-ferguson-walter.md`,
> `1_recon/How_to_Disturb_Network_Reconnaissance…DRL.md`,
> `1_recon/Software_Rejuvenation_Meets_Moving_Target_Defense…md`,
> `10_disc/3560828.3564006.md`, `10_disc/An_Effective_Address_Mutation…md`,
> `10_disc/file.md`, `10_disc/wang2016_mtd_network_reconnaissance_sdn_isc16.md`.

### Relevance class

**M** (MTD-mechanism / attacker-effect) — the reset-verdict + sweep-width
evidence for §3. Not per-tactic dwell; the *shape* of how attacker scan-success
falls as the shuffle interval shortens relative to the attacker's action time.

### Used in lit review

Recon/discovery §3 (declared reset verdict) + §4 (MTD-effect rows); the
reset-vs-dwell ratio argument that underwrites the whole tuned-group sweep
([`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md)).

## Bibliographic anchor

- **Citation keys**: `carroll2014` (Carroll, Crouse, Fulp, Berenhaut, *Analysis
  of Network Address Shuffling as a MTD*, IEEE ICC 2014); `crouse2015` (Crouse,
  Prosser, Fulp, *Probabilistic Performance Analysis of MT and Deception
  Reconnaissance Defenses*, MTD'15); `anderson2016` (Anderson, Mitchell, Chen,
  *Parameterizing Moving Target Defenses*, IFIP NTMS 2016); `fergusonwalter2021`
  (Ferguson-Walter, Major, Johnson, Muhleman, *Examining the Efficacy of
  Decoy-based and Psychological Cyber Deception*, USENIX Security 2021 — Tularosa
  Study); `reti2022` (Reti, Elzer, Fraunholz, Schneider, Schotten, *Evaluating
  Deception and MTD with Network Attack Simulation*, MTD'22); `wang2016_sdn`
  (Wang, Wu, *MTD Against Network Reconnaissance with SDN*, ISC 2016);
  `zhang2023_drl` (Zhang et al., *How to Disturb Network Reconnaissance: a DRL
  MTD Approach*, IEEE TIFS 2023); `torquato2022` (Torquato, Maciel, Vieira,
  *Software Rejuvenation Meets MTD: Time-Based VM Migration*, ISSRE 2022);
  `jafarian2015_rhm` (Jafarian, Al-Shaer, Duan, *An Effective Address Mutation
  Approach for Disrupting Reconnaissance*, IEEE TIFS 2015).
- **Pages cited from**: full text (Carroll, Crouse, Anderson, Reti, Wang);
  §6 results (Ferguson-Walter); value sections (Jafarian, Zhang-DRL, Torquato).

## Relevant artefacts

### Carroll 2014 — the urn model: perfect shuffling caps attacker success at e⁻¹

**Source locator:** §III (urn models); §IV-A/B/E (analysis + empirical)

**Paraphrase:** the foundational analytical result [fetched]. Model a network as
an urn of *n* addresses with *v* vulnerable hosts; the attacker draws *k* probes.
Under **perfect shuffling** (remap after every probe) with one vulnerable host
and *k = n* probes, attacker success converges to **e⁻¹ ≈ 0.63** as the network
grows — a **37% reduction** vs static addressing. The load-bearing conditions:
shuffling **only helps when the vulnerable population is sparse in a large
address space** (as *v/n* rises, the benefit collapses; with many vulnerable
hosts, static and shuffled are near-identical). Cost: legitimate connection loss
rises with shuffle rate (climbs sharply past a ~0.85 normalised rate ≈ shuffle
every 38 probes). Cites the DARPA/DYNAT figure that **"an attacker can be
expected to spend upwards of 45% of their time performing reconnaissance"** and
Rowe & Goh that **attackers can wait up to a day before acting on recon**, so a
few shuffles a day suffice.

**Quote:**
> "perfect shuffling reduces the probability of attacker success by 37% as
> compared to using static addresses." (§IV-A)

> **VERIFY (expression, flagged 2026-07-09):** "e⁻¹ ≈ 0.63" is internally
> inconsistent — e⁻¹ ≈ 0.37. The stated value (0.63) and the quoted "37%
> reduction" agree with each other and imply the intended expression is
> **1 − e⁻¹ ≈ 0.632**. Confirm against Carroll §IV-A before citing the
> *expression* anywhere; the dissertation (§3.1 tactic profiles) cites the
> value only ("roughly 63%"). Same expression is propagated in
> `01_reconnaissance.md` (§3/§4/§5) — correct there too once confirmed.

**Maps to:** [`01_reconnaissance`](../tactic_profiles/01_reconnaissance.md) /
[`10_discovery`](../tactic_profiles/10_discovery.md) §3 (a shuffle *invalidates*
recon/discovery gains — reset verdict = re-discovery forced) and §4; the
"sparse-vulnerable" condition bounds *how much* a shuffle bites (sweep width);
the 45%-of-time-on-recon anchor supports recon as a large-share, low-and-slow
activity (§2).

**Disposition for this thesis:** verified [fetched] — analytical upper bound.
Declared/modelled, not empirical dwell; the e⁻¹ ceiling and the sparse-vulnerable
condition are the shape §3 encodes.

---

### Crouse 2015 — reset depends on shuffle-interval ÷ attacker-wait-time ratio

**Source locator:** §3.3 (shuffling model); §5.1 Foothold Scenario (Fig. 9); §5.3

**Paraphrase:** extends Carroll with honeypots, and — load-bearing for us —
models a two-phase attack: **reconnaissance → wait (attack-wait-time) → attack**,
and shows attacker success is governed by the **ratio of inter-shuffle time to
attack-wait-time** [fetched]. When the shuffle interval exceeds the attack-wait
time, the shuffle rarely fires between recon and exploitation and its benefit
collapses (attacker success rises to the no-shuffle line); when it is shorter,
recon knowledge is invalidated before it can be used. This *ratio*, not the
absolute interval, is the reset mechanism — directly the project's "shuffle
interval vs tactic dwell" punchline
([`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md) §6).
Connection-drop cost ~0.04 when inter-shuffle = wait time. Confirms honeypots
(deception) often beat shuffling alone; combination best.

**Maps to:** [`01_reconnaissance`](../tactic_profiles/01_reconnaissance.md) §3
(reset = invalidation *if* shuffle interval < recon-to-exploit gap; the sweep
width is the uncertainty in that gap);
[`10_discovery`](../tactic_profiles/10_discovery.md) §3; the ratio game is the
operational-validation calibration lever for every tuned group.

**Disposition for this thesis:** verified [fetched]. The reset verdict is
*conditional on the interval ratio* — this is why §3 declares a verdict + a
sweep, not a point.

---

### Anderson 2016 — SPN churn-interval exemplar; "churn faster than completion ⇒ attack never succeeds"

**Source locator:** §III (closed-form + SPN models); §IV (results, Figs 3–10)

**Paraphrase:** two cross-validated models (closed-form + Stochastic Petri Net)
for dynamic-platform MTD over a **6-phase attack** (survey, tool, implant, pivot,
damage/exfil, cleanup — mirrors the substrate's scripted attacker) [fetched].
The reset mechanism stated plainly: for attacks that must restart after a churn,
**"the attack can never succeed if the churn rate is faster than the completion
rate"** (§III). Declared parameter values (the *precedent* for Tier-3
declare-and-sweep): churn time *h* = **30 / 60 / 240 minutes**; cyber-attack
length *c* = **8 / 24 / 48 h** (and the guidance to use "months" for nation-state,
"hours" for recreational); implants required *i* = *c/h × o/2*. Two emergent
cautions: **(1) a mis-parameterised MTD can make the system *less* secure**
(attacker has an exploit for one platform but not others — below a breakeven
configuration count MTD *helps* the attacker); **(2) longer campaigns are
*less* likely to succeed** under churn (more re-implants ⇒ more detection
chances), inverting the naïve "APT patience always wins".

**Maps to:** all tuned tactics' §3/§5 sweep (the churn-vs-completion ratio =
reset condition); the declared churn intervals (30–240 min) are a *precedent* for
declaring a tactic dwell + sweeping it, not a value to transplant.

**Disposition for this thesis:** verified [fetched] — method precedent
(declare-and-sweep) + the reset-ratio mechanism. Its ICS/DPT framing means the
numbers are exemplars, not APT dwell.

---

### Ferguson-Walter 2021 (Tularosa Study) — measured red-team forward-progress under decoys

**Source locator:** §4 (design); §6.1 Forward Progress (Target Selection,
EternalBlue, Data Exfiltration, Delay); §6.1.2 (Resources)

**Paraphrase:** the rare thing — **measured human-attacker effect** of a
defensive perturbation. 123 professional red-teamers, full-day pen-test, 2×2
(decoys Present/Absent × Informed/Uninformed), network of 25 Win + 25 Linux real
hosts (+25+25 decoys) [fetched]. Decoys impede forward progress at **every**
kill-chain stage:
- **Exfiltration:** Absent mean 3.86 files (n=13 participants) vs Present 1.52
  (n=6) — roughly halved.
- **EternalBlue:** module loads Absent 17.3 vs Present 4.6; self-reported exploit
  successes Absent 6.5 vs Present 1.4.
- **Real hosts targeted:** Absent 31.98 vs Present 22.78; 35% of packets and 52%
  of IP-bearing commands in Present conditions were wasted on decoys.
- **Time-to-first-real-target (via Metasploit RHOST):** Uninformed 128.6 min vs
  Informed 174.6 min; first decoy interaction 11.7–20.6 min.
- **Every** Present participant tripped a decoy alert *before* any successful
  exploitation of a real host.
- **Key emergent finding:** deception is effective **even when the attacker knows
  it is present** (H2 supported; Present-Informed most affected) — counter to the
  "deception must be hidden" folklore.

**Maps to:** [`01_reconnaissance`](../tactic_profiles/01_reconnaissance.md) /
[`10_discovery`](../tactic_profiles/10_discovery.md) §3 (a defensive perturbation
bites hardest at the recon/discovery stage — wasted effort, delayed forward
progress) and §4 (real human minutes-to-target).

**Disposition for this thesis:** verified [fetched] — the strongest measured
attacker-effect datum in the corpus. **Scope caveat:** decoys/deception are *not*
the SDR MTD mechanisms the substrate models (shuffle/diversity/redundancy); the
relevance is the *shape* of recon-stage disruption + the human timing anchors,
not a deployable mechanism (deception/IDS are culled from the thesis' defender
set — [`../specs/project_context.md`](../specs/project_context.md)).

---

### Reti 2022 — NASim honeypot+MTD sim: short mutation interval drives scan-agent success to 0

**Source locator:** §3.1 (three attacker agents); §4.2 (MTD = address mutation);
§6.1/§6.3 (results, Figs 1–6)

**Paraphrase:** the closest analogue to *this thesis's own substrate* [fetched] —
a network-attack simulator (NASim) with three **rule-based** agents (careful =
full horizontal scan first; standard = vertical, one host at a time; aggressive =
worm-like, exploits all hosts with no scan) over phases scan → service/OS/vuln
scan → exploit/privesc → wiretapping. MTD = **address mutation every N time-steps**
(N ∈ {25, 50, 75, 100}); after a mutation "the agent does not know which hosts
were already exploited" — **the reset forces re-discovery** and the scan-based
agent restarts from phase 1. Results:
- **At mutation interval 25 the careful (scan-first) agent's win probability is
  0** — "the IP mutation is happening before the agent chooses to attack." Win
  probability rises monotonically with the interval.
- The **aggressive (worm) agent is *least* hurt** by short intervals (it doesn't
  rely on a scan that gets invalidated) — outperforms the scan agents for
  intervals < 60.
- Compromising **all** sensitive hosts stays < 1% at interval 25; the **one-host**
  goal never falls below 40% for any interval — MTD bites the *thorough* attacker,
  not the opportunist.
- Larger network lowers success (48% at 50 hosts vs 78% at 10 hosts, interval 25).

**Maps to:** [`10_discovery`](../tactic_profiles/10_discovery.md) §3 (a shuffle
invalidates the internal map → forced re-discovery; the effect scales with the
mutation-interval ÷ scan-cadence ratio) and §4;
[`11_lateral-movement`](../tactic_profiles/11_lateral-movement.md) §3 (the
worm-agent's *resistance* to shuffling — scan-free spread survives address
mutation better than scan-based movement).

**Disposition for this thesis:** verified [fetched] — a directly comparable
DES result; the interval-25→0 finding is the sharpest illustration of the
reset-vs-cadence ratio in a substrate like ours. Simulation, declared costs
(all actions cost 1 step) — a *shape* result, not a dwell.

---

### Wang 2016 (Sniffer Reflector) — SDN obfuscation invalidates the recon result

**Source locator:** §3–§5 (architecture, evaluation, Tables 1–2)

**Paraphrase:** an SDN MTD that reflects scan traffic to a **shadow network**, so
the attacker's nmap scan returns *forged* ports/OS (e.g. real host's 22/23/80/443
replaced by decoy 53/135/139/445/3389) [fetched]. The recon *result* is
invalidated — the attacker cannot collect effective network information, so
"the following attack steps will not succeed." Cites that **">70% of network
scans are connected with attack activities"** and port scan is "the initial step
of the cyber attack routine." No dwell (scan still completes in ~14 s; decoy
latency 0.015 s vs real 0.00015 s), but qualitatively a clean reset of recon
gains via obfuscation rather than address churn.

**Maps to:** [`01_reconnaissance`](../tactic_profiles/01_reconnaissance.md) §3
(diversity/obfuscation reset — recon result made false) and §4 (recon-as-precursor
statistic).

**Disposition for this thesis:** verified [fetched]. Prototype, no dwell;
qualitative reset evidence + the recon-precursor statistic. Obfuscation is
diversity-flavoured, adjacent to the substrate's service-diversity MTD.

### Jafarian 2015 (RHM) — deterrence ratio = attack-completion delay; restart-per-interval

**Source locator:** §I (RHM scheme); §V (effectiveness: deterrence/detectability
ratios, game-theoretic scanning analysis)

**Paraphrase:** Random Host Address Mutation, two-level (low- + high-frequency
eIP mutation), adaptive to observed scanning [fetched]. Defines the two metrics
we care about: **deterrence ratio = T_RHM / T_static** (attack-completion
duration under mutation ÷ static — the *delay* imposed) and **detectability ratio
= C_RHM / C_static** (scans forced). Mechanism: "after each mutation interval,
the attacker is forced to restart his scan" — a clean reset of recon/discovery
progress every interval. Game-theoretic result: RHM forces the rational attacker
onto *uniform* scanning, which is easy to detect; miss probability > **e⁻¹** if
the attacker scans less than the full space (e.g. half the space ⇒ e⁻¹ᐟ² missed)
— corroborating Carroll's e⁻¹ ceiling. Focuses on **low-rate scanners/worms**
(fast scanning is easy to detect) — the APT-relevant regime.

**Maps to:** [`10_discovery`](../tactic_profiles/10_discovery.md) /
[`01_reconnaissance`](../tactic_profiles/01_reconnaissance.md) §3 (restart-per-interval
= the reset verdict; the deterrence ratio is the *delay multiplier* a shuffle
imposes — directly a sweep input) and §4;
[`11_lateral-movement`](../tactic_profiles/11_lateral-movement.md) §3 (worm
slowdown).

**Disposition for this thesis:** verified [fetched] — the cleanest statement of
"mutation forces re-discovery per interval" + the deterrence-ratio framing.
Declared/analytical, not empirical dwell.

---

### Wang 2017 (RDAM) — 96.2% scanner miss; effect set by scan-rate ÷ mutation-rate

**Source locator:** §5.1 (evaluation, Figs 5–6; Mininet/POX simulation)

**Paraphrase:** Random Domain-name And address Mutation — mutates *both* the
domain name and IP, enlarging the scan space beyond the address space [fetched].
Simulation (12,000 internal / 6,000 public hosts, Class-B space): **RDAM causes
96.2% of hosts to be missed** by internal+external scanners scanning domain
names; an internal IP-scanner "cannot hit any host"; external IP-scanning misses
37% (no time-window) up to 80% (tuned window). Load-bearing mechanism: define
**r = attacker-scan-rate ÷ defender-mutation-rate**; miss probability *rises as r
falls* (mutate faster than the scan ⇒ more misses), and **when r ≥ k the mutation
offers no benefit over static** (mutation slower than the scan) — the same
ratio-governs-reset law as Crouse, now on the scan/mutation timescale.
Explicitly defends worm propagation by enlarging the scan space.

**Maps to:** [`10_discovery`](../tactic_profiles/10_discovery.md) /
[`01_reconnaissance`](../tactic_profiles/01_reconnaissance.md) §3 (reset strength
= f(mutation-rate ÷ scan-rate); the sweep spans r<1 "strong reset" to r≥1 "no
benefit") and §4;
[`11_lateral-movement`](../tactic_profiles/11_lateral-movement.md) §3 (worm).

**Disposition for this thesis:** verified [fetched] — quantifies the ratio law
with a concrete miss curve. Simulation, declared rates.

---

### Zhang 2023 (ID-HAM) — DRL host mutation: −25% scanning hits, +26–58.7% scan time

**Source locator:** abstract; §I; §IV (analysis, Eqs 21–24)

**Paraphrase:** an RL (advantage actor-critic) host-address-mutation scheme that
*learns from* scanning behaviour [fetched]. Headline: **decreases scanning hits
by up to 25%** vs prior HAM, and **prolongs scanning time by 26%** (adversary
unaware of the scheme) to **58.7%** (adversary aware) over static IP. Cites the
Panjwani figure that **up to 70% of cyber attacks are preceded by scanning**. The
adaptive angle answers jalowski2026's point that APTs "learn mutation patterns" —
an RL defender that co-adapts.

**Maps to:** [`01_reconnaissance`](../tactic_profiles/01_reconnaissance.md) /
[`10_discovery`](../tactic_profiles/10_discovery.md) §3 (magnitude of the scan-time
penalty a mutation imposes — 26–59% longer; feeds the sweep) and §4.

**Disposition for this thesis:** verified [fetched] — quantified scan-time
penalty. RL-defender, simulation; the numbers are the *shape* of the deterrence,
not APT dwell.

---

### Torquato 2022 — VM-migration SPN: >40% attack-success reduction, availability/security trade-off

**Source locator:** abstract; §I (RQ1–3); §V (results)

**Paraphrase:** SPN model of **time-based VM migration** serving *both* software
rejuvenation and diversity-based MTD [fetched]. A migration relocates the VM
(optionally onto a different hypervisor version), which resets a **host-based**
foothold. Result: MTD "reduce[s] the probability of attack success by more than
40%" in the best scenarios; availability+security improvement "surpasses 50%".
Central finding = an explicit **availability-vs-security trade-off in the
migration interval** — shorter interval ⇒ more security, less availability — i.e.
the MTD-cost side of the same ratio dial (mirrors Carroll's connection-loss cost).

**Maps to:** [`05_persistence`](../tactic_profiles/05_persistence.md) /
[`04_execution`](../tactic_profiles/04_execution.md) §3 (a migration *invalidates*
a host-based foothold — reset verdict for the on-host tactics, not just recon) +
the method precedent (SPN interval sweep with a declared cost).

**Disposition for this thesis:** verified [fetched] — cross-tactic (host-foothold
reset) + the availability-cost of short intervals. Cloud/VM domain; SPN-modelled,
not APT dwell. (Filed under recon in Step D, but its reset target is the
persistence/execution foothold.)

## Open questions / things to verify

- Every reset verdict here is **modelled/declared**, never a logged real-world
  MTD→APT effect (that log does not exist — the genuine unknown). The consistent
  *shape* across analytical (Carroll/Crouse), SPN (Anderson), DES (Reti), and
  human-subject (Ferguson-Walter) evidence is the argument; the *magnitude* is
  swept.
- Ferguson-Walter §7–appendix (kill-chain stage tables, cognitive-bias
  discussion) read at §6 granularity; if a specific appendix number is later
  cited, pull the exact table first.
- `jafarian2015_rhm`, `zhang2023_drl`, `torquato2022` rows are added below after
  their value-section reads (RHM mutation-interval-vs-scan-success curves).

## Out of scope for this thesis

Honeypot/decoy *deployment optimisation* (how many, where — Reti/Crouse's main
contribution); SDN implementation detail (VDESwitch, Snort rules); cyberpsychology
theory (Ferguson-Walter H3/H4); DPT taxonomy (Anderson §II). Deception and IDS as
*defender mechanisms* are culled from the thesis — used here only as
attacker-effect *shape* evidence.
