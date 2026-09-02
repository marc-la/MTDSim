---
status: durable
chapter: ch1_introduction
created: 2026-09-02
updated: 2026-09-02
---

# The authoritative Volt Typhoon advisory answers a knowledge-durability campaign without ever naming moving target defence

## Position in the dissertation

Chapter 1 — the motivating case study. The introduction can open on (or pivot
through) Volt Typhoon as the live instance of the attacker class this thesis
evaluates MTD against, and the observation below is the introduction's hook:
the defence class whose stated mechanism most directly targets what this
campaign banks is absent from the authoritative public response to it.

## The idea

In February 2024, nine agencies across four countries — CISA, the NSA and the
FBI, co-sealed by, among others, the Australian Signals Directorate's ACSC —
published a joint advisory on Volt Typhoon, a PRC state-sponsored actor that
had compromised critical infrastructure organisations across multiple sectors
(CISA, 2024, AA24-038A). The advisory's headline facts describe an attacker
whose entire value proposition rests on the durability of what it steals and
holds. The actors maintained access and footholds within some victim IT
environments for at least five years. They harvested the Active Directory
credential store from three of one victim's domain controllers over a
four-year period — refreshing their credential material to keep it current,
rather than spending it. After credential theft they went largely silent,
performing discovery but not bulk exfiltration; the agencies assess with high
confidence that the behaviour is "not consistent with traditional cyber
espionage" and that the actors are pre-positioning on IT networks to enable
future disruption of operational technology. The mechanism of the five
undiscovered years is living off the land and valid accounts: no malware to
detect, only legitimate credentials exercised through native tools.

Everything this campaign banks is static defender state. Harvested
credentials remain valid for years; network topology knowledge remains
accurate; footholds remain where they were left. Moving target defence is the
defence class whose stated mechanism is the invalidation of exactly that
asset class — rotating addresses, services, and credentials so that
accumulated attacker knowledge decays instead of compounding. Yet the
advisory's mitigation guidance answers the campaign entirely with static
hardening and detection: patching, multi-factor authentication, logging,
behavioural baselining and hunting. Nowhere in the advisory does a
moving-target approach appear. That absence is the observation this thesis's
introduction can be built on: the attacker class for which MTD's value
proposition is strongest — long-dwell, credential-anchored, pre-positioned —
is publicly answered without it, and the literature evaluating MTD has not
supplied the evidence that would change this, because (as the literature
review argues) it evaluates MTD against attackers with no accumulated
knowledge to lose.

Two scope boundaries keep the claim honest. First, the inference is this
thesis's, not the advisory's: the agencies do not consider and reject MTD,
they simply do not name it, and this note verifies the absence against the
advisory's text only — the stronger claim that *nobody* in the Volt Typhoon
discourse has proposed MTD would need a wider, dated literature check before
the introduction asserts it. Second, the campaign functions in this thesis as
motivation and as a worked example of behaviour capture (the literature
review reconstructs a machine-readable attack flow from this advisory), not
as an evaluated scenario: the evaluation's attacker profiles derive from an
independent analyst-curated corpus that does not contain this campaign, and
the introduction must not imply that MTD was scored against Volt Typhoon.

The case generalises beyond one campaign. Current incident-response
reporting places the global median intrusion dwell at 14 days but the
espionage-class tail at 122 days (Mandiant M-Trends 2026) — an
order-of-magnitude divergence in pacing by objective, of which Volt Typhoon's
five years is the documented extreme. The introduction can therefore move
from the statistic (long-dwell attackers exist as a class) to the exemplar
(this is what one looks like, and this is how it was answered) to the thesis
question (what would an MTD evaluation have to look like for its answer to
bear on this attacker at all).

## Evidence and repo anchors

- `docs/sources/extractions/cisaaa24038a.md` — Concepts 2–4 carry the quoted
  dwell, pacing and objective facts with section locators; all quotes
  fetch-verified 2026-09-02 against the ASD ACSC republication.
- `docs/sources/extractions/breach_reports_macro_timing.md` — the M-Trends
  2026 dwell figures (14 d global median; 122 d cohort is cyber-espionage +
  DPRK-IT-worker, so prose should say "espionage-class").
- The MTD-absence claim: text search of the full ACSC republication
  (2026-09-02) returns zero occurrences of "moving target" or "MTD",
  including the Mitigations section. The companion joint guide *Identifying
  and Mitigating Living Off the Land Techniques* was not checked.
- `data/gap/hand_curated/README.md` — the hand-authored Attack Flow built
  solely from this advisory (outside the corpus by Decision 6; the ch3
  §3.1.2 exemplar figure is its induced subset). This is why the case study
  is load-bearing rather than decorative: the campaign is in the thesis's
  evidence chain.
- Bib keys: `cisaaa24038a` (active), `mtrends2026` (activated 2026-09-02),
  `nist2011sp80039` (the objective-triad definition the pre-positioning
  behaviour instantiates).
- Ch3 §3.1.1 gap G5 introduces the campaign in the survey; this note is the
  ch1 use of the same material.

## Revisit conditions

- If a Volt Typhoon profile is ever admitted to the corpus (a membership
  ruling reserved for Marc), the "not an evaluated scenario" boundary
  inverts and the introduction may claim more.
- If later advisories or major vendor guidance begin recommending
  moving-target approaches for this actor class, the absence claim must be
  re-dated or dropped.
- The absence is verified against AA24-038A only; before the introduction
  strengthens "the advisory does not name it" to "nobody proposes it", run
  the wider discourse check.
