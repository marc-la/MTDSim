---
status: investigation record — pins the one structural baseline the L2 chapter
        cites, and the 2026-08-17 confidence re-audit of the objective
        classification. Tool: tools/gasp_structural_baseline.py; test:
        tests/l2_subgraph/test_structural_baseline.py. The three per-flow
        dispositions of §(d) were ruled by Marc later the same day — §(g):
        membership 19/8/6/5 → 19/7/7/5, L2–L3 rebuilt; 38 / 38 high after
        Marc's read of AA22-138B.
created: 2026-08-17
updated: 2026-08-17
scope: L2 (GASP) — descriptive structural columns and confidence column of the
       audit CSV (§(a)–(f)); then, by Marc's per-flow dispositions, three
       membership changes and the L2/L3 rebuild they forced (§(g)).
---

# The structural baseline the chapter cites, and the confidence re-audit — 2026-08-17

## Why this exists

The §4.2.2 draft ran a number trail — "13 reach exfiltration / 13 reach impact /
3 both" → 19 / 8 / 6 / 5 → "15 of 38 land in a different category than the
terminal tactic alone gives" — whose first and third numbers came from two
different structural readings of the flows (*reach* and *terminal*), and whose
"15" depended on a concordance rule that was recorded in
[`partition_decision.md`](partition_decision.md) but never stated beside the
number. Marc's ruling (2026-08-17): the chapter cites **one** structural
baseline, reproducibly; and the L2 confidence column (30 high / 2 medium / 6
low) is not cited until the composite approach — terminal tactic as primary
evidence, cross-referenced against the CTID blurb, the ATT&CK group page and
the vendor report — has been run to its end on the eight non-high flows.
This record holds both results. It executes the handoff
`2026-08-17_l2_classification_confidence_validation.md`.

## (a) The pinned baseline — definition

**Def A, terminal read, technique-level, via the L1 contraction.** Contract the
flow to its technique graph exactly as L1 does
([`aggregate.contract_flow`](../../../../src/mtdsim/l1_construction/aggregate.py):
technique-bearing action → through operator / condition glue → next
technique-bearing action; an action *without* a technique breaks the chain). A
technique is **terminal** when it has no contracted out-edge to a different
technique. The flow's *terminal tactics* are the tactics of the actions carrying
its terminal techniques. The flow's **terminal read** is then

| terminal tactics include | read |
|---|---|
| `exfiltration` only | exfil |
| `impact` only | impact |
| both | both |
| neither (incl. cyclic flows with no terminal) | neither |

This is P1 of [`partition_decision.md`](partition_decision.md), and it is now
what the audit CSV's `terminal_techniques` / `terminal_tactics` columns hold —
regenerated 2026-08-17 by `tools/gasp_structural_baseline.py --write-descriptive`
(the columns were first populated by an uncommitted in-session script whose
terminal-set rule could not be reproduced technique-for-technique; at the
*objective-read* level the two rules agreed on 36 / 38 flows and swapped two,
`oceanlotus` ↔ `toolshell`, leaving every aggregate number below unchanged).
The `reaches_*` columns reproduced exactly and were rewritten byte-identical.

Why this definition and not another: it is the pipeline's own view of the flow
(the GAP is built from exactly these contracted edges), so the chapter's
"terminal tactic in the dependency graph" is the terminal of the graph the
thesis actually builds — no second algorithm to defend. Two rejected
alternatives, both computed by the tool: (i) a walk over raw action nodes that
does not break at technique-less actions gives 8 / 11 / 1 / 18 (differs on
`toolshell` only); (ii) counting tactic-only (technique-less) actions changes
the read of six flows (three Conti + `muddy_water` → both; `toolshell` →
neither; `uber_breach` → exfil) — see §(c). Neither is what L1 sees.

**Concordance rules against the audit's `stated_objective`** (mapping
`steal_data`↔exfil, `impediment`↔impact, `double_extortion`↔both,
`position_for_future`↔neither):

- **exact** — the 4-way terminal read equals the audit class;
- **any-overlap** — the read shares at least one objective tactic with the
  audit class, or both are empty (the rule behind the record's 23 / 38 = 61 %).

## (b) The numbers (38 flows; `PYTHONPATH=src python tools/gasp_structural_baseline.py --check`)

| reading | 4-way split (exfil / impact / both / neither) | any-count | disagree, exact | disagree, any-overlap |
|---|---|---|--:|--:|
| **terminal (Def A) — pinned** | **7 / 11 / 1 / 19** | 8 exfil, 12 impact, 1 both | **19 / 38** | **15 / 38** |
| reach (any occurrence) | 10 / 10 / 3 / 15 | 13 exfil, 13 impact, 3 both | 14 / 38 | 11 / 38 |

Reconciliation with the record and the draft:

- "13 / 13 / 3" (draft P1) is the **reach** any-count. It reproduces; it is not
  the terminal read.
- "15 / 38" ([`partition_decision.md`](partition_decision.md), [`gasp_schema.md`](gasp_schema.md)
  §(a), draft P5) is the terminal read under **any-overlap**. It reproduces.
- "19 / 38" (the quick re-read in the handoff) is the terminal read under
  **exact**. It also reproduces. The four flows that separate the two rules are
  all ransomware: `conti_cisa_alert`, `conti_pwc`, `conti_ransomware`,
  `ragnar_locker` — terminal on impact alone, audit `double_extortion`.
- The record's 8 : 12 : 20 with 1 overlap was on the 39-flow corpus; minus
  `openclaw` (all-ATLAS, reads neither) it is 8 : 12 : 19 = this table.

**Composition of the 19 exact disagreements** — the fact the chapter is really
after: 14 flows whose terminal read is *silent* (neither) while the report
attests an objective (`black_basta_ransomware`, `cisa_iranian_apt`,
`cobalt_kitty_campaign`, `equifax_breach`, `fin13_case_1`,
`ivanti_vulnerabilities`, `jp_morgan_breach`, `mac_malware_steals_crypto`,
`marriott_breach`, `oceanlotus`, `searchawesome_adware`, `swift_heist`,
`turla_carbon_emulation_plan`, `uber_breach`); 4 ransomware flows terminal on
impact alone whose report attests exfiltration too (the four above); 1
*contradiction* (`muddy_water`: terminal impact via a `confidence: 0` T1486
node, audit exfiltration). Under any-overlap the first and last groups are the
15.

**What the chapter cites — recommendation, Marc's call.** One reading, the
terminal read, in both places: P1 becomes "8 flows terminate on exfiltration,
12 on impact, one on both, 19 on neither"; P5 cites **19 of 38** if the sentence
keeps its literal form ("land in a different category — impact, exfiltration,
both, or neither — than the terminal tactic alone gives" is the exact rule), or
**15 of 38** if it is reworded to "the terminal read is silent or contradicts
the report" with the four impact-only ransomware flows named as the remainder.
The 14 / 4 / 1 composition is the more informative sentence either way: it is
the truncated-report point ([`gasp_schema.md`](gasp_schema.md) (b) D3) with a
number on it. If the reach numbers stay in P1 they must be labelled as reach,
not as the baseline.

## (c) Sensitivity — tactic-only actions are invisible to L1

Twenty-one of the 38 flows carry action nodes with a tactic but no technique
(Attack Flow lets the analyst draw a tactic-level step); in eight of them the
tactic-only step is `exfiltration` (three Conti flows, `mac_malware_steals_crypto`,
`marriott_breach`, `muddy_water`, `target_breach`, `uber_breach`). L1
aggregation drops them by design (no-synthesis: they break the chain and
contribute no GAP node), so both the terminal and the reach columns miss them.
Three of them matter for the re-audit: `mac_malware_steals_crypto` (two `Exfiltration` tactic-only actions),
`uber_breach` (one), `muddy_water` (`Collection` + `Exfiltration`). Their
*analyst-drawn* narrative therefore contains an exfiltration step the structural
read cannot see — which is exactly the "high-fidelity, low-coverage" point the
chapter makes, and is why those three re-grade on the flow narrative below.
Including tactic-only actions would move the terminal split to 7 / 7 / 5 / 19
and the reach split to 13 / 6 / 7 / 12; recorded here, not adopted.

## (d) The confidence re-audit — eight non-high flows under the composite approach

Method: for each flow — terminal read (§(a)) → CTID `example_flows/` blurb →
the CTID `.afb` flow file's per-node analyst narrative (fetched from the
`center-for-threat-informed-defense/attack-flow` corpus; a source the May round
did not use — the local YAMLs carry names and tactics but not the analyst's
node descriptions) → ATT&CK G-page → the most authoritative vendor URL. CISA
was 403 at the network edge for this session (Akamai, all routes, and the
Internet Archive was offline); the two advisory sentences quoted below were
located by exact-phrase search indexed against the `cisa.gov` page and are
`verify`-marked for Marc to confirm on the page.

| flow | class | before | **after** | deciding source(s) |
|---|---|---|---|---|
| `cisa_aa22_138b_vmware_workspace_ta1` | exfiltration | low | **high** | terminal T1041; flow narrative "script collects sensitive files … stored in a tar ball" → "sensitive data stored in tar ball is exfiltrated by GET request"; advisory: *"TA1 downloaded a malicious shell script, which they used to collect and exfiltrate sensitive data"* (verify) |
| `cisa_aa22_138b_vmware_workspace_ta2` | none_c2 | low | **high** | terminal C2; flow narrative = Godzilla + Dingo J-spy webshells, `/etc/passwd`+`/etc/shadow` viewed, reverse SOCKS proxy — no exfil / impact action; advisory: *"TA2 interacted with the server (without automation or scripts) and installed multiple webshells and a reverse secure socket (SOCKS) proxy"*, GET requests "to upload webshells for persistence" (verify) |
| `cisa_aa22_138b_vmware_workspace_alt` | none_c2 | low | **low** (disposition needed) | flow narrative = credential TAR *staged*, C2 to 20.232.97.189, MoneroOcean miner and JSP webshell downloads *attempted*; no exfil / impact action. **But** the tooling overlaps TA1's — `fd86ald0.pem`, `20.232.97.189`, the CVE-2022-22960 `horizon`→sudo escalation — so the flow reads as the advisory's analysis of TA1's script drawn without the exfil step. If so, `none_c2` is a truncation artefact of the flow cut, and the class definition (pre-payload, *not* truncated breach) points at exfiltration or at a duplicate-encoding drop. Membership change or corpus edit either way → Marc. |
| `mac_malware_steals_crypto` | exfiltration | low | **medium** | flow narrative encodes **two** exfiltration actions (Safari cookies; Chrome credentials + wallet keys — tactic-only, §(c)) and the miner as T1105 tool transfer, not as impact; Unit 42 leads with theft (*"more efficient way to generate profits than outright cryptocurrency mining"*). Residual: dual monetisation at malware level ([`gasp_schema.md`](gasp_schema.md) (h)3). High needs one ruling: dominant-objective classification for dual-monetisation malware. |
| `toolshell_vulnerability_in_sharepoint` | exfiltration | low | **high** | **the flow file contains no ransomware / impact action** — the 4L4MD4R half exists only in vendor coverage; blurb: "leads to remote code execution and credential theft"; flow narrative: MachineKey extraction → Exfiltration Over C2 Channel (×3) → ViewState persistence; Unit 42 attributes the MachineKey exfil to CL-CRI-1040. The (h)1 flow-split premise is falsified: the flow does not conflate two actors, the vendor report does. Terminal read is now exfil (§(a)). |
| `muddy_water` | exfiltration | medium | **high** | flow narrative "Collects intellectual property data from private entities, universities, and research labs" → "Exfiltrate intellectual property" (tactic-only, §(c)); the T1486 node carries `confidence: 0`; ATT&CK G0069 = cyber-espionage; Talos: *"no encryption, wiping, or ransom demands"*. The capability-aggregating scope caveat stays in the per-flow record; it is not a source disagreement. |
| `uber_breach` | exfiltration | medium | **high** | flow narrative "Attacker exfiltrated internal Slack messages and information from a finance tool used to manage invoices" (tactic-only, §(c)); ATT&CK G1004: social engineering and extortion, *"including destructive attacks without the use of ransomware"*; Uber: *"downloaded some internal Slack messages, as well as accessed or downloaded information from an internal tool our finance team uses to manage some invoices"*, no production / user data, no encryption. Attribution stays `G1004?`; the objective does not depend on it. |
| `searchawesome_adware` | impact | low | **low** (named misfit) | flow narrative: root certificate, AitM, mitmproxy, malvertising, JS injection, C2, self-delete — **no impact-tactic and no exfiltration action**; Malwarebytes: *"doesn't directly exfiltrate user data"*. No source attests impact; `impediment` is by analogy only. Disposition needed: accept as the one named misfit, or drop as non-adversary-objective adware (a new criterion — the openclaw / example_attack_tree drop was "not analyst-curated CTI of a real operation", which SearchAwesome *is*). |

**Tally: 30 / 2 / 6 → 35 high / 1 medium / 2 low.** Applied to
`data/gasp/metadata_audit.csv` (`metadata_confidence`, `source_used`, `notes`
only) and carried through to `data/gasp/classification.csv` by the L2 rebuild;
the four class subgraphs are byte-identical (membership unchanged; the L2 gate
`tests/l2_subgraph/` passes).

**What 38 / 38 would require — three rulings, none the session's to make:**

1. `mac_malware_steals_crypto` → high: rule that dual-monetisation malware is
   classified by its dominant, analyst-encoded objective (closes (h)3 for this
   flow without a fifth class).
2. `cisa_aa22_138b_vmware_workspace_alt` → high *or* re-class *or* drop: read
   AA22-138B and decide whether the "alternative method" section is a distinct
   intrusion (→ high as none_c2) or TA1's script analysis (→ exfiltration by
   the class definition, or a duplicate-encoding drop; both re-open L2 / L3).
3. `searchawesome_adware`: accept as the named misfit at low, or drop with a
   stated criterion. **36 / 38 high with two named misfits is the honest
   sentence today**; 38 / 38 is reachable only through rulings 1–3.

## (e) Spot-check of the thirty highs (stratified, all four classes)

Read the same way (flow narrative + existing vendor citation). All confirmed;
two flags, no re-grades:

- exfiltration: `equifax_breach` (exfil over encrypted web protocols, log
  wiping), `turla_carbon_emulation_plan` ("SSH credentials are collected and
  exfiltrated"), `cobalt_kitty_campaign` (DNS / mail exfil), `swift_heist` —
  **flag**: the flow's realised objective is fraudulent SWIFT payment orders
  (financial theft), neither exfiltration nor impact; `objective_exfiltration`
  is by the recorded analogy. Not a source disagreement; a scheme-fit note
  already in the per-flow record.
- impact: `cisa_iranian_apt` (XMRig miner deployed — the corpus reads
  cryptomining as impact when the analyst encodes it), `sony_malware` (T1485 /
  T1561 wipe).
- double extortion, all three non-Conti flows: `black_basta_ransomware`
  encodes T1567 exfil, T1486, **and** T1657 "leverages double extortion";
  `ragnar_locker` — T1567 "steals files and uploads them … in case the victim
  refuses to pay" + T1486; `revil` — T1041 + T1486 + T1485. Plus one Conti:
  `conti_ransomware` — **flag**: the flow's only exfiltration node is beacon
  telemetry ("computer name and OS version … sent via encoded cookie values");
  the flow's own evidence for the exfiltration half is weak; the class rests
  on the operator-level (DFIR / CISA) double-extortion characterisation. High
  stands on the vendor source, as recorded; noted for the operator-concentration
  discussion.
- none_c2: `hancitor_dll` (Cobalt Strike + Ficker Stealer staged; DFIR:
  evicted before completing the mission).

## (f) Artefacts

- Tool: [`tools/gasp_structural_baseline.py`](../../../../tools/gasp_structural_baseline.py)
  — `--check` (numbers + column reproduction), `--write-descriptive` (regenerate
  the four descriptive columns), `--tex` (appendix tables).
- Test: [`tests/l2_subgraph/test_structural_baseline.py`](../../../../tests/l2_subgraph/test_structural_baseline.py)
  — pins 7 / 11 / 1 / 19, 19 exact / 15 any-overlap, per-flow column
  reproduction, and the 35 / 1 / 2 tally with the named low / medium flows.
- Appendix tables: [`docs/thesis/tables/objective_classification_audit.tex`](../../../thesis/tables/objective_classification_audit.tex)
  — four booktabs tables (one per class: flow, terminal read, terminal tactics,
  source, confidence), generated, `\input`-ready, no new packages; labels
  `tab:objective-audit-{exfiltration,impact,exfiltration-impact,none-c2}`.
- CSV: `data/gasp/metadata_audit.csv` (descriptive + confidence columns),
  `data/gasp/classification.csv` (carried-through confidence).
- Per-flow trail: [`per_flow_justifications.md`](per_flow_justifications.md)
  § *Verification round 2 (2026-08-17)*.


## (g) Marc's rulings on the three flows, and what they moved (2026-08-17, later)

Marc's dispositions (dictated; the per-flow reasoning is his, the record is
the session's):

| flow | ruling | class after | confidence |
|---|---|---|---|
| `mac_malware_steals_crypto` | *"monetisation … two different methods to extract money from the person, so logically it would fall into double extortion"* — two monetisation channels (credential / cookie / wallet-key theft; XMRig/Koto mining = resource hijacking, the corpus's own reading of XMRig in `cisa_iranian_apt`) in one flow → the class defined as *both impact and exfiltration in the same flow* | `objective_exfiltration_impact` | high |
| `cisa_aa22_138b_vmware_workspace_alt` | *"threat actor one is known for data exfiltration … it's a truncated exfiltration flow"* — the flow is TA1's script analysis drawn without the exfil step (§(d)); the class definition excludes truncated breach reports | `objective_exfiltration` | high — Marc read AA22-138B (2026-08-17): it states TA1 deployed `80b6ae2cea.sh`, which overwrites `publishCaCert.hzn` using `fd86ald0.pem` to enable credential theft, and identifies the script's purpose as exfiltration of sensitive system data. Was medium for the hour between the ruling and the read |
| `searchawesome_adware` | *"no realised objective category with high confidence, we have systematically ruled the other three"* — no exfiltration action, no impact-tactic action, hence not both; the residual by elimination | `objective_none_c2` | high |

Two notes the record must carry with the rulings. (i) The Mac ruling is
consistent with the chapter's *definition* of the compound class and with the
tactic label; it is not "extortion" in the ransom sense, so the chapter's name
for the class should follow the definition (double extortion is what six of
its seven members are). (ii) The Alt truncation is the CTID analyst's — the
`.afb` file itself has no exfiltration node — not an L1 excision (Alt's two
technique-less nodes are C2 and discovery). SearchAwesome is the one
`objective_none_c2` member there by elimination rather than pre-payload
structure: it realises ad injection, which is not an objective tactic.

**Result.** Partition **19 / 7 / 7 / 5**; confidence **38 / 38 high** (Alt was
medium until Marc's read of the advisory the same day). Structural baseline unchanged (7 / 11 / 1 / 19; 19
exact / 15 any-overlap — Alt moved from agree to disagree and SearchAwesome the
other way; the exact-disagreement composition is now 14 silent + 4 impact-only
ransomware + 1 contradiction with `cisa_…_alt` in and `searchawesome_adware` out
of the silent group). Mean technique JSD 0.429 → 0.443 bits.

**What the rebuild moved (all regenerated, all tests re-pinned):**

- L2: `classification.csv`, four class subgraphs — exfiltration 96 n / 408 e,
  impact 59 / 246, exfiltration+impact 59 / 229, none 39 / 141.
- L3a Petri: places 15 / 13 / 14 / 13 (impact lost `defense-impairment`, which
  only SearchAwesome carried), transitions 109 / 76 / 72 / 57, inter-tactic
  edges 358 / 217 / 205 / 130, self-loops dropped 50 / 29 / 24 / 11; divergence
  report and README regenerated. `objective_impact` now carries a structural
  sink (`collection` lost its only out-edge with SearchAwesome); `objective_none_c2`'s
  sink moved from `defense-impairment` to `privilege-escalation`, and — the
  consequential one — its `resource-development` place is no longer an island
  (SearchAwesome's malvertising draws `resource-development → command-and-control
  / execution`), so the M6 synthetic overlay's forward edge
  `resource-development → initial-access` had to merge into an observed
  out-distribution. **Marc's ruling: improve the mechanism, not exempt one
  profile** — the overlay now applies one share rule to every synthetic edge
  (island source → the whole out-mass; source with observed out-edges →
  `MERGE_SHARE` 0.1, observed rescaled to 1 − Σs), which is what the backward
  bridge already did ([`../ogasp/synthetic_overlay.md`](../ogasp/synthetic_overlay.md)
  §3–4; register §M6 addendum). Only `objective_none_c2`'s
  `resource-development → initial-access` edge changes share (1.0 → 0.1) under
  the rule today.
- L3b timeline: report, example and figures regenerated. Median net
  time-to-objective ranking (primary cell): aggregate < none < impact <
  exfiltration < exfiltration+impact; survives the sweep extremes; weighted vs
  uniform not stable (as before — check `timeline_report.md`).
- Movement (behavioural, not artefacts): `objective_none_c2` walks now strand
  at `privilege-escalation` early on most seeds (seed 0: t ≈ 106 of a 3 000
  horizon) unless retrace is on — a real profile change worth a sentence
  wherever the none profile's walks are described; `objective_impact` now
  retraces (both arms); every class retraces with the overlay on. Test pins
  moved accordingly (`test_movement_retrace.py`, the seeded fixture in
  `test_movement_measures.py` → seed 11).
- L2 statistics ([`tactic_profile_statistics.md`](tactic_profile_statistics.md)
  §10): verdicts unchanged qualitatively; gate pins 0.499 / 0.532 bits; the
  exfiltration-vs-impact what-next pair no longer clears 0.05.
- Chapter numbers to move: every 19 / 8 / 6 / 5; "half of double extortion is
  Conti" → three of seven; the two-misfits concession → gone (38 / 38 high); the
  class name follows the definition.

Not touched, flagged: [`../../../notes/ch4_methods/objective_partition_findings.md`](../../../notes/ch4_methods/objective_partition_findings.md)
carries the pre-ruling numbers in prose (banner added, body left for the
drafting session); [`partition_decision.md`](partition_decision.md) and
[`tactic_resolution_restatement.md`](tactic_resolution_restatement.md) are
investigation history and are left as written. The L3 records that
state the pre-ruling sink facts (`objective_impact` sinkless; `objective_none_c2`
sink at `defense-impairment`) — [`../ogasp/sink_retrace_design.md`](../ogasp/sink_retrace_design.md),
[`../ogasp/demonstration_arms_prereg.md`](../ogasp/demonstration_arms_prereg.md),
[`../ogasp/demonstration_arms_cross_examination.md`](../ogasp/demonstration_arms_cross_examination.md),
[`../ogasp/experiment_02_findings.md`](../ogasp/experiment_02_findings.md) — are
dated designs and results on the 19 : 8 : 6 : 5 nets and are left as written;
any re-run of those experiments on the 19 : 7 : 7 : 5 nets must re-derive its
sink/sinkless arms from `load_routing_net(...).is_sink` (only the aggregate is
sinkless now) and re-capture its own goldens, as the `*_retrace` goldens were
here (the 15 retrace goldens on `objective_exfiltration_impact` moved; the 39
aggregate-profile goldens are byte-identical, so no defender-side behaviour
drifted).
