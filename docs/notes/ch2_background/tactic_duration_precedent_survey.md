---
status: durable
created: 2026-07-04
updated: 2026-07-05
topic: precedent survey — does anyone assign per-ATT&CK-tactic durations, and where do timed-APT-model numbers come from
---

> **Step-C reconciliation (2026-07-05):** the survey's known-but-unextracted
> sources and macro calibration targets are now dissected into
> [`../extractions/`](../extractions/) and reconciled from **[search]** to
> **[fetched]** — Ling & Ekstedt 2023, McQueen 2006, Xiong 2021 (both the SoSyM
> and CSIMQ papers), Selmanaj 2024, Syed 2025, Che Mat 2024, and the four macro
> vendor bundles (M-Trends, CrowdStrike GTR, Sophos AAR, DFIR). The gap verdict
> is **unchanged and strengthened**; edits below are inline.

# Nobody assigns justified per-ATT&CK-*tactic* durations — the gap is real, and the field norm is "declare and sweep"

## Why this is worth recording

The state-duration catalogue
([`../../data/ogasp/tactic_durations.json`](../../data/ogasp/tactic_durations.json))
rests on Hong's claim that **no ready-made resource maps MITRE tactics to
durations** — the justification for defining them ourselves (D4). That claim is
now checked, not assumed. This note is the landscape survey behind the gap
statement in the methodology chapter and the citable answer to "did you look?".
The headline: the gap is real at the *tactic* level, and — more useful — the
survey turned up the **precedents that legitimise the method we're proposing**
(declare-and-sweep is the field norm; face-validation of declared numbers has
prior art). That converts operational validation
([`./2026-07-04_operational_validation_the_bar.md`](./2026-07-04_operational_validation_the_bar.md))
from "our workaround" into "the field's standard practice, which we extend". The
survey was run as four parallel web-research agents on 2026-07-04; every claim
below carries a confidence flag (**[fetched]** = verified by fetching the primary
source, **[search]** = search-snippet/secondary only — reconcile before thesis
citation, per [`../specs/guardrails.md`](../specs/guardrails.md)).

## The substance

### The verdict, in one line

**Per-ATT&CK-*tactic* durations with justification: NO precedent exists.** The one
tactic-level ATT&CK Petri-net model (Rodríguez 2024) is *untimed*; every timed
APT model that carries ATT&CK labels attaches timing at the *technique/CVE* level
or declares its rates outright. So the layer we are building — a justified,
tiered, calibrated tactic→duration catalogue — is genuinely open ground. Hong is
right.

### Where timed-APT-model numbers actually come from (the crux)

The dominant practice is **(b) assume/declare, usually paired with (d)
sensitivity analysis** over the assumed values — the standard defence is "we
don't know the true rate, so we sweep it". Genuine empirical timing **(a)** is
the exception and lives only at *vulnerability/exploit* granularity (CVSS/NVD or
testbed measurement), never at the tactic level. Calibration-to-observed-
behaviour **(c)** is essentially absent. This is the single most important
finding for our framing: **our plan (Tier-1 substrate anchor + declared Tier-3
estimates + sweep ranges) already matches the field norm, and the operational-
validation calibration step goes *further* than the norm, not less far.**

The load-bearing precedents:

- **Bland et al. 2020** (SPN + RL, *Computers & Security* 92:101738) — the closest
  executed-SPN precedent [our extraction:
  [`../extractions/bland2020.md`](../extractions/bland2020.md)]. **Firing rates
  are declared placeholders**: the dissertation says verbatim "*For the purpose
  of the example arbitrary rates are used and would later have to be determined
  by subject matter experts.*" Crucially, the net *structure* was **face-validated
  by 14 cybersecurity SMEs** — a structured validation of a declared model. This
  is direct prior art for our Tier-3 "declared + justified" values and for
  face-validation as an acceptable standard. **[fetched]** (UAH dissertation full
  text).
- **McQueen et al. 2006** "Time-to-Compromise Model" — the MTTC lineage. Openly a
  blend of expert elicitation, thin empirical anchoring, and **admitted
  arbitrariness**: one sub-process mean set "*somewhat arbitrarily*" at 8 hours,
  another anchored empirically at 5.8 days (vuln-announcement→exploit-code). The
  canonical citation for "declare a stage time, justify it in prose, move on".
  **[fetched]** — now dissected full-text (OSTI 911165) into
  [`../extractions/mcqueen2006.md`](../extractions/mcqueen2006.md) (Step C,
  2026-07-05). New finding: the model's Process-3 dwell is a **declared per-skill
  constant** — 21 d (expert) → 193 d (novice) to compromise a component with *no
  known vulnerability* — the closest thing in the lineage to a declared
  per-stage dwell, and an order-of-magnitude envelope for stealth-tactic dwell.
  The paper also states TTC "*decreases over time* unless there is constant
  effort" — near-direct MTD relevance.
- **Mendonça 2023** (DSPN MTD performance model, *J. Defense Modeling & Sim.*) —
  our Tier-2 analytical-MTD precedent [extraction:
  [`../extractions/mendonca2023.md`](../extractions/mendonca2023.md)]. Full text
  paywalled; **[search]** inference is that MTD-trigger interval and service/
  arrival rates are analyst-set inputs, swept — i.e. (b)+(d). A *sister* paper
  (Mendonça et al., PRDC, MTD in SDN, **[fetched]** pre-print) is a rare
  partial-empirical case: recon/exploit times measured on an SDN testbed (Nmap,
  sqlmap, Patator), "other parameters reasonably estimated" — (a)+(b)+(d). Note
  the empirical part is again *exploit-level*, mirroring our substrate's
  `exploit_time`.
- **Rodríguez et al. 2024** (process-mining ATT&CK Petri nets, *JISA*) — our
  tactic-level-structure precedent [extraction:
  [`../extractions/rodriguez2024.md`](../extractions/rodriguez2024.md)]. The
  Inductive-Miner nets are **untimed control-flow**: log timestamps only *order*
  events into runs; no transition rates or dwells. Tactic-level, but zero timing.
  **[fetched]** (open predecessor PDF).

### The one per-technique "yes", and why it doesn't close our gap

- **Ling & Ekstedt 2023** "Estimating Time-To-Compromise for ICS Attack
  Techniques Through Vulnerability Data" (*SN Computer Science* 4:318) — the clean
  positive case: TTC assigned to **ATT&CK-for-ICS *techniques***, justified from
  **empirical CVE data** (2,740 ICS vulns, CVSS exploitability, Metasploit
  exploit-availability→skill, mean-time-between-vulnerabilities from advisory
  dates, RAND exploit-dev times). Worked output: MITM-on-HMI ≈ 2501 days novice /
  6 days expert. **[fetched]** (Springer). But it is *per-technique from CVE data*,
  ICS-specific, and formalism-agnostic — it does **not** give per-tactic dwells,
  and its method needs real CVEs (the vuln-instance binding our substrate can't
  do, per [`./2026-06-18_cti_to_executable_behaviour.md`](./2026-06-18_cti_to_executable_behaviour.md)
  §4 level 3 / BRON). It's the citation for "the frontier of putting numbers on
  ATT&CK stops at technique/CVE level" — which is exactly the gap boundary we sit
  just past. **[fetched]** — now dissected into
  [`../extractions/ling2023.md`](../extractions/ling2023.md) (Step C). New
  findings: under an **expert (APT) assumption the per-technique method
  degenerates to a shared 6-day floor** (empirical support for group anchors over
  15 per-tactic values); and CVE-based timing **structurally cannot price**
  command-and-control or the hiding half of evasion ("not exploiting a
  vulnerability") — those tactics are free parameters in *any* model.
- **Xiong et al. 2021** — **two distinct papers, both now [fetched] and
  reconciled (Step C):** (a) the **SoSyM enterpriseLang** paper
  ([`../extractions/xiong2021.md`](../extractions/xiong2021.md)) ships
  **untimed** — the MAL machinery *supports* per-step TTC distributions but the
  published language does not assign them (equal-width edges "owing to the lack
  of probability distributions"; distributions deferred to future work). So the
  flagship ATT&CK-wide simulation language corroborates the gap rather than
  filling it. (b) The **CSIMQ companion** (Xiong, Hacks & Lagerström 2021, 26:55–77)
  is the one that assigns distributions — **corrected characterisation:** not raw
  "expert-declared defaults" but a **systematic literature review with
  credibility assessment** ("we assess their quality by credibility assessment …
  interpret and convert information into probability distributions"), explicitly
  an improvement on the prior "rely on security experts" norm — still (b)-class
  (qualitative→quantitative conversion, not empirically fitted rates). The
  earlier **[search]** "expert-declared" flag is resolved.

### Corpora: sequence yes, timing no

- **AbSamad99/APTsDataset** (the repo Marc flagged) — its paper is **Syed et al.
  2025** (IEEE Networking Letters), now dissected into
  [`../extractions/syed2025.md`](../extractions/syed2025.md) (Step C): **23
  Caldera-executed campaigns across 12 APTs**, 83 techniques / ~290 abilities
  over 14 tactics, captured via ELK. The curated `Sequence.json` is a pure
  ordered technique-sequence, **no adversary-tempo timing**; the Caldera ability
  timestamps measure *testbed execution latency*, not dwell. The raw `logs.7z`
  holds ELK `@timestamp`s — timing *derivable* but not curated (same heavy
  sourcing-decision class as DARPA OpTC/TC). **[fetched]** (paper + repo).
- **Attack Flow** (CTID) — its `attack-action` schema **defines optional
  `execution_start` / `execution_end` timestamps** — the exact intended home for
  per-technique timing — but the **public corpus leaves them empty** (built from
  breach reports that rarely give machine-usable timestamps). The schema admits
  what the data doesn't supply. **[fetched]** schema / **[search]** on corpus
  emptiness (grep the corpus JSON to confirm).
- **ATT&CK Campaigns** = coarse whole-campaign `first_seen`/`last_seen` at
  month/year granularity only. **Groups** = no timing. APTnotes = PDF index, prose
  timing only. Emulation plans = prescriptive, not observational. All **[search]**.
- **The only genuinely per-stage-timed sources are raw provenance datasets** —
  **DARPA OpTC** (≈8.7B host events; red-team ground-truth PDF with a timestamped
  action timeline) and **DARPA Transparent Computing E3/E5** (ground-truth IoCs +
  timestamps spanning the full lifecycle). Per-ATT&CK-tactic timing is
  *derivable* by binning timestamped ground-truth actions into tactics — a real
  but heavy empirical option, and a new sourcing category the specs don't yet
  classify (flag for a decision if pursued). **[fetched/search]**.

### Adversary-emulation frameworks: no per-phase dwell anywhere

None of Caldera, Atomic Red Team, CTID Emulation Library, Prelude Operator,
VECTR, Stratus Red Team, Atomic Operator, Infection Monkey attaches a **per-phase
dwell/duration/time-budget** to its phase→ability mapping. Every temporal field
found is one of: **C2 beacon cadence** (Caldera jitter, default 2–8 s check-in),
a **per-command kill-timer** (Caldera ability `timeout`, default 60 s),
**whole-operation scheduling** (Prelude), or **post-hoc recorded timestamps**
(VECTR). Caldera and Atomic Red Team verified by fetching the ability/YAML
schema; the other six **[search]**. So Marc's design — a Caldera-style per-phase
ability catalogue that *additionally* assigns a dwell to each phase — has **no
identified public analogue**. That absence is itself worth stating in the thesis.

### Empirical macro-timing: only whole-campaign or single-transition, never per-tactic

Confirmed: **no vendor breach/IR report publishes a per-ATT&CK-tactic duration
breakdown.** They give either whole-campaign aggregates or single named
transitions. The usable calibration targets (reconcile figures against primary
PDFs before citing — several are **[search]**):

| Source | Latest figure | Metric | Granularity |
|---|---|---|---|
| Mandiant M-Trends | **14 days** (2026 ed.); espionage/DPRK 122 d; BRICKSTORM ~400 d; access→hand-off 8 h (2022)→22 s (2025) **[fetched]** | global median dwell + splits | whole-intrusion (detection-source split: 26 d external / 5 d adversary / 10 d internal) |
| CrowdStrike GTR | **29 min avg / 27 s fastest** (2026 ed.); 48 min / 51 s (2025); one case exfil +4 min **[fetched]** | breakout time | single transition: initial-access → lateral-movement |
| Sophos Active Adversary | dwell 2–3 d; **access→AD ~3.4 h (2026) / 11 h (2025)**; **access→exfil ~73–79 h**; exfil→detection ~2 h **[fetched]** | multi-milestone chain | **best industry granularity — named milestones** |
| The DFIR Report | **per-case TTR 2 h / 118 h / 328 h**; Mimikatz +20 min; lateral +10 min–2 h post-access **[fetched]** | per-incident timestamps | **per-technique but per-case, not aggregate** |
| Secureworks | ~28 h median ransomware dwell (2024) **[search]** | whole-campaign dwell | whole-campaign (bimodal) |
| IBM X-Force | <4 d access→ransomware (2023; later unconfirmed) **[search]** | single transition | single transition |
| Unit 42 | median exfil ~2 d (2025) **[search]** | single transition | whole-campaign |
| DARPA OpTC / TC | datasets (2018–2020) | timestamped red-team ground truth | **per-action → derivable per-tactic** |

The four top rows are **reconciled to primary sources (Step C, 2026-07-05)** and
consolidated in [`../extractions/breach_reports_macro_timing.md`](../extractions/breach_reports_macro_timing.md);
Secureworks/IBM/Unit 42 remain **[search]** (not re-fetched — the four fetched
vendors already span the fast↔slow envelope). Cross-report comparability is weak
(each vendor defines dwell/breakout and its start/end anchors differently, over
different populations) — treat them as independent calibration points, not one
consistent timeline. This *reinforces* the shape-not-scale decision in the
operational-validation note: the honest use of these is to set *relative*
structure and a plausibility envelope, not absolute per-tactic times.

## How it connects

- **To the method note:** this is the evidence base for
  [`./2026-07-04_operational_validation_the_bar.md`](./2026-07-04_operational_validation_the_bar.md).
  Bland/McQueen/MAL = the "declare + justify + (face-)validate + sweep" precedent
  that legitimises Tier 3; the empirical table = the calibration targets; the
  "no per-tactic breakdown" finding = why calibration is of *shape*, not scale.
- **To the catalogue:** grounds the tier hierarchy in
  [`../../data/ogasp/tactic_durations.json`](../../data/ogasp/tactic_durations.json)
  — Tier 2's first stops (Bland, Mendonça) confirmed as *declared*, not empirical,
  so most non-substrate tactics land in Tier 3 with the sweep discipline.
- **To the lit review:** existing extractions (bland2020, mendonca2023,
  rodriguez2024) confirmed and characterised for *parameter sourcing*
  specifically. **New extraction candidates — all now dissected (Step C,
  2026-07-05):** [`ling2023`](../extractions/ling2023.md) (the one per-technique
  empirical case), [`mcqueen2006`](../extractions/mcqueen2006.md) (MTTC lineage),
  [`xiong2021`](../extractions/xiong2021.md) (enterpriseLang — ships untimed) +
  the CSIMQ companion flag settled; plus [`selmanaj2024`](../extractions/selmanaj2024.md)
  (adversary-emulation textbook — per-tactic MO + smash-and-grab/slow-and-deliberate
  cadence), [`syed2025`](../extractions/syed2025.md) (Caldera APT corpus —
  sequence-no-timing), [`chemat2024`](../extractions/chemat2024.md) (APT-behaviour
  SLR), and the [`breach_reports_macro_timing`](../extractions/breach_reports_macro_timing.md)
  bundle. The **[search]** macro figures are reconciled to primary sources; only
  Secureworks/IBM/Unit 42 remain unreconciled (not needed).
- **To open sourcing decisions:** DARPA OpTC/TC as an empirical per-tactic-timing
  source is a *new sourcing category* — heavy, and not yet classified by the
  specs. Flag for a decision rather than assuming it's in scope.

## When this would need updating

- If a **per-tactic timed ATT&CK model** surfaces (the survey is broad but not
  exhaustive; it is web-search-bounded, not a systematic review) — the gap
  statement weakens to "near-absent" and reframes as positioning.
- If we **decide to mine DARPA OpTC/TC** for empirical inter-tactic timing — a new
  Tier promotes some tactics from declared to empirically-anchored, and the
  sourcing-category decision must be recorded first.
- If the **substrate adopts real CVEs** — Ling & Ekstedt's per-technique CVE
  method becomes directly applicable and the frontier moves.
- If any **[search]**-flagged figure fails primary-source reconciliation — drop or
  correct it; do not let an unreconciled number harden into a calibration target.
