---
tactic: <kebab-case-name>          # must match the place name in data/ogasp/ exactly
attack_id: <TA0000>                # ATT&CK Enterprise v19.1 external id
attack_url: https://attack.mitre.org/tactics/<TA0000>/
attack_version: 19.1               # the pinned bundle; note pre-split literature uses "defense-evasion"
status: stub                       # stub | drafted | reconciled
group_hypothesis: <scan-shaped | exploit-shaped | stealth-low-and-slow | objective-execution | prep-off-network>
tier_hypothesis: <1 substrate | 2 literature | 3 declared>
---

# <Tactic Name> — APT × adversary-simulation × MTD dwell profile

> **Purpose of this file (read once):** a *reconciled synthesis* that terminates
> in exactly two claims the simulator needs — **(a) dwell character** (how long /
> how low-and-slow) and **(b) MTD disruption** (does an MTD action invalidate
> progress here, forcing repeat or wait). Everything else is context. A sentence
> that changes neither *how long* nor *whether the attacker repeats it* is trim.
> Keep it to 1–2 pages. Method + bar:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../operational_validation.md).
> Structure + groups: [`README.md`](README.md). The filled §5 feeds
> [`../../data/ogasp/tactic_durations.json`](../../../../data/ogasp/tactic_durations.json).

## 1. Tactic & role

One paragraph. What the tactic is (paste/condense the ATT&CK definition, cite the
`attack_url`) and where it sits in an APT campaign narrative. If this is a
v19.1-split tactic (stealth / defense-impairment), say what it inherited from the
old `defense-evasion` and what the sibling took.

## 2. APT relevance — the group-assignment argument

Is this tactic inherently **low-and-slow** or **fast** for an APT actor? Argue it
from the literature (CTI, breach narratives, the precedent survey). This is the
qualitative claim the literature *can* support even where numbers don't exist,
and it decides which timing **group** the tactic joins (frontmatter
`group_hypothesis` → confirm or overturn here). Do **not** land a point number.

## 3. MTD interaction — reasoned from mechanism (declared, not evidence-backed)

Which MTD action — **IP/topology shuffle**, **service/OS diversity**,
**redundancy** — disturbs progress in this tactic, and how? Be explicit that this
is argued from the *semantics of the MTD mechanism* (there are no public logs of
MTD→attacker effect — the genuine unknown,
[`../notes/2026-06-18_cti_to_executable_behaviour.md`](../structure_to_behaviour_binding.md) §5).
The output is (i) a **reset verdict** — does a shuffle invalidate a gain here
(e.g. a foothold) or survive it (e.g. a stolen credential)? — which feeds the
declared MTD-reset parameter and the L3b binding
([`../handoffs/2026-07-03_l3_binding_scoping.md`](../../../handoffs/2026-07-03_l3_binding_scoping.md)),
and (ii) the **sweep-width** it justifies (more uncertainty → wider range).

## 4. Timing evidence

Small table. Most rows will legitimately be "no direct value" — that *is* the gap
evidence, record it, don't force a number. Papers are claims: flag `[fetched]`
vs `[search]`, cite the locator, never guess ([`../specs/guardrails.md`](../../../workflows/guardrails.md)).

| Source | Claim (value / behaviour) | How adapted to this tactic | Confidence |
|---|---|---|---|
| ATT&CK `<TA0000>` page | <definition / technique list; no timing> | — | [fetched] |
| <in-corpus extraction §ref> | <e.g. "no per-tactic timing"> | <inference or none> | [fetched] |
| <external, if any> | <e.g. M-Trends / Sophos milestone> | <mapped onto this tactic> | [search] |

## 5. Catalogue inputs — the only section that feeds `tactic_durations.json`

- **Group:** <one of the five; confirms/overturns `group_hypothesis`>
- **Relative multiplier:** <×k of the group anchor — a ratio, not an absolute time>
- **Sweep range:** <e.g. ×½ / ×2, wider if §3 uncertainty is high>
- **Tier:** <1 | 2 | 3> + one-line why
- **Justification (one paragraph):** the synthesis of §2–§4 that makes the group
  + multiplier non-arbitrary. This paragraph *is* the deliverable, not the number.
