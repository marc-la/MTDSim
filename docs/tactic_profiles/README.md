# `docs/tactic_profiles/` — per-tactic APT × adversary-sim × MTD dwell profiles

One file per tactic in the L3a place-union — a **reconciled synthesis** of what
an APT actor does in this tactic, how long (dwell character), and how an MTD
system disrupts it. The files are the **evidence layer** the state-duration
catalogue (`data/ogasp/tactic_durations.json`) and the L3b binding draw on; they
are not the catalogue itself.

- **Method / the bar these files must clear:** [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md)
  — operational validation: calibrate unobservable per-tactic dwells so the
  *emergent timeline shape* matches literature-reported campaign patterns; badge
  every value's validity; sweep it.
- **Why the gap is real (precedent survey):** [`../notes/2026-07-04_tactic_duration_precedent_survey.md`](../notes/2026-07-04_tactic_duration_precedent_survey.md)
  — nobody assigns justified per-ATT&CK-*tactic* durations; the field norm is
  declare-and-sweep, which these profiles execute.
- **How to fill a file (mechanical research protocol):** [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
- **Template:** [`_template.md`](_template.md).

## The 15 tactics — ATT&CK Enterprise v19.1

The place-union across the five L3a nets is **15**, not the classic 14, because
**ATT&CK v19.1 split `defense-evasion` (TA0005) into `stealth` (TA0005, reused
id) + `defense-impairment` (TA0112, new)**. The pinned bundle is
[`../../data/gap/_attack/enterprise-attack-19.1.json`](../../data/gap/_attack/enterprise-attack-19.1.json).
**Research consequence:** most existing literature predates the split and says
"defense-evasion" — allocate those claims across `stealth` (hiding/evasion) vs
`defense-impairment` (disabling/degrading defences), don't map them to one.

Kill-chain order; `group_hypothesis` is a *starting bet* each file must confirm
or overturn. Tier-1 groups (scan/exploit-shaped) are substrate-anchored and **not
tuned**; the tuned groups are stealth-low-and-slow and objective-execution.

| # | Tactic (place name) | ATT&CK | Group hypothesis | Tier hyp. |
|--:|---|---|---|:--:|
| 1 | `reconnaissance` | [TA0043](https://attack.mitre.org/tactics/TA0043/) | scan-shaped | 1 |
| 2 | `resource-development` | [TA0042](https://attack.mitre.org/tactics/TA0042/) | prep-off-network | 3 |
| 3 | `initial-access` | [TA0001](https://attack.mitre.org/tactics/TA0001/) | exploit-shaped | 1 |
| 4 | `execution` | [TA0002](https://attack.mitre.org/tactics/TA0002/) | stealth-low-and-slow | 3 |
| 5 | `persistence` | [TA0003](https://attack.mitre.org/tactics/TA0003/) | stealth-low-and-slow | 3 |
| 6 | `privilege-escalation` | [TA0004](https://attack.mitre.org/tactics/TA0004/) | exploit-shaped | 1 |
| 7 | `stealth` | [TA0005](https://attack.mitre.org/tactics/TA0005/) | stealth-low-and-slow | 3 |
| 8 | `defense-impairment` | [TA0112](https://attack.mitre.org/tactics/TA0112/) | stealth-low-and-slow | 3 |
| 9 | `credential-access` | [TA0006](https://attack.mitre.org/tactics/TA0006/) | exploit-shaped | 1 |
| 10 | `discovery` | [TA0007](https://attack.mitre.org/tactics/TA0007/) | scan-shaped | 1 |
| 11 | `lateral-movement` | [TA0008](https://attack.mitre.org/tactics/TA0008/) | exploit-shaped | 1 |
| 12 | `collection` | [TA0009](https://attack.mitre.org/tactics/TA0009/) | objective-execution | 2/3 |
| 13 | `command-and-control` | [TA0011](https://attack.mitre.org/tactics/TA0011/) | stealth-low-and-slow | 3 |
| 14 | `exfiltration` | [TA0010](https://attack.mitre.org/tactics/TA0010/) | objective-execution | 2/3 |
| 15 | `impact` | [TA0040](https://attack.mitre.org/tactics/TA0040/) | objective-execution | 2/3 |

## The five timing groups

You calibrate ~4 **group anchors**, not 15 independent dwells (identifiability —
see the method note). Each file assigns its tactic to a group + a relative
multiplier within it.

- **scan-shaped** — substrate-priced (`ATTACK_DURATION` scan verbs). Tier 1, not tuned.
- **exploit-shaped** — substrate-priced (`exploit_time`, complexity-scaled). Tier 1, not tuned.
- **stealth-low-and-slow** — the primary *tuned* group; anchored at k× the exploit median.
- **objective-execution** — collection/exfil/impact; its own tuned anchor.
- **prep-off-network** — resource-development and any tactic with no in-network
  action; candidate for near-zero in-sim dwell. Group boundary is itself a
  finding to record.

## Status

All 15 files are `status: stub` at creation — header + empty sections only.
Lifecycle: `stub` → `drafted` (sections filled) → `reconciled` (`[search]` claims
confirmed against primary sources, ready to feed the catalogue).
