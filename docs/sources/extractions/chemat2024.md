# Che Mat et al. 2024 — extraction notes

> Nur Ilzam Che Mat, Norziana Jamil, Yunus Yusoff, Miss Laiha Mat Kiah, "A
> systematic literature review on advanced persistent threat behaviors and its
> detection strategy", *Journal of Cybersecurity* 10(1):tyad023, 2024 (open
> access).
> Source file: `docs/sources/tactic_profiles/step_c/APTProfiling_SLRAPTProfiling_2024Mat.md`
> (+ `.pdf`, gitignored).
> Relevance to this thesis: a PRISMA SLR (45 studies: 35 academic + 10
> industry, academic window Jan 2015–Apr 2020/2022) of **APT detection based on
> multi-stage attack behaviour**. Detection is culled from this thesis
> (lit-review §1.3 only), so the SLR's core taxonomy is out of scope — what it
> contributes is behaviour-breadth evidence (18 APT groups × kill-chain-phase
> TTP matrix) and one more independent confirmation that the timing gap holds
> on the detection side too.

### Relevance class

**S** (supporting) — behavioural corroboration for §2-type claims plus
detection-side gap evidence; no timing values anywhere.

### Used in lit review

Tactic-profile §4/§2 evidence (Step C, 2026-07-05); candidate for lit-review
§1.3 (detection, culled thread) if ever needed.

## Bibliographic anchor

- **Citation key**: `chemat2024`
- **DOI / URL**: https://doi.org/10.1093/cybsec/tyad023
- **Pages cited from**: full text (18 pp)

## Relevant artefacts

### Dwell character, one line — months to years

**Source locator:** §Introduction, para 4

**Paraphrase:** the framing claim: an APT "can remain undetected within the
target network for **months and even years**", staging tools consecutively
through the attack stages; and (via Trend Micro/Report [5]) the APT "selects a
target regardless of its defenses and persists until it breaches them" —
persistence-of-intent, not opportunism. Whole-campaign and qualitative; no
per-stage numbers anywhere in the review (45 studies surveyed and no stage
duration surfaces — detection-side corroboration of the timing gap).

**Maps to:** consistent with the alshamrani2019 backbone (no new number);
precedent-survey gap statement (detection literature likewise carries no
per-tactic timing).

**Disposition for this thesis:** verified [fetched].

---

### Table 5 — 18 APT groups × kill-chain phase, TTP prevalence

**Source locator:** §Discussion "Behavior analysis", Table 5 (pp. 13–14 of
print; table parse partially garbled)

**Paraphrase:** for 18 named groups (APT1, APT3, APT12, APT15, APT16, APT17,
APT28, APT29, APT30, CopyKitten, Molerats, Silent Chollima, Emissary Panda,
Olympic Game, Energetic Bear, Lotus Blossom, Desert Falcon, Snake), the review
tabulates which CKC-phase TTPs each uses. Tick counts recoverable from the
parse (out of 18): **social-engineering reconnaissance 18; spear-phishing
delivery 18; HTTPS(S) command-and-control 18; registry-key-modification
installation 18; data exfiltration 18** — i.e. near-universal per-phase
staples — vs host-based weaponisation 17, known-vuln exploitation 15, 0-day
exploitation 13, watering hole 12, network-based weaponisation 7, rogue
software 5. Per-group attribution of the sparser TTPs is `[parse-uncertain]`
(the tick columns lost alignment); the counts themselves are legible.

**Maps to:** [`13_command-and-control`](../../notes/ch3_design/tactic_profiles/13_command-and-control.md)
(§2/§4: web-protocol C2 as the universal channel) ·
[`05_persistence`](../../notes/ch3_design/tactic_profiles/05_persistence.md) (registry-key
persistence universal) · [`03_initial-access`](../../notes/ch3_design/tactic_profiles/03_initial-access.md)
(spear-phish ubiquity) · [`14_exfiltration`](../../notes/ch3_design/tactic_profiles/14_exfiltration.md)
(exfiltration present in all 18 profiles' behaviour set).

**Disposition for this thesis:** verified [fetched] — breadth corroboration
only; frequencies of *use across groups*, not rates or durations (and not
corpus `observation_count` — different provenance, same prohibition on
reading it as timing).

---

### The C&C-optionality caveat — attack models break on Stuxnet

**Source locator:** §Discussion "Multi-stage attack behavior" (Table 4
discussion)

**Paraphrase:** phase models (CKC and its derivatives — Dell SecureWorks,
LogRhythm, Mandiant, Lancaster, BSI, all sharing the three-part
foothold→remote-access→objectives skeleton, Table 4) "may be invalidated if
unanticipated actions are carried out, or the order in which the actions are
performed is disrupted. Attackers may not always follow well-known
techniques, such as using C&C to monitor their attacks. For instance, the APT
Stuxnet can autonomously carry out specific activities without needing to
communicate through the C&C server."

**Maps to:** [`13_command-and-control`](../../notes/ch3_design/tactic_profiles/13_command-and-control.md)
§2/§4 — independent corroboration of the Step B Stuxnet finding (C&C dwell is
conditional on connectivity; air-gapped campaigns route around it) ·
supports wide sweep on the C&C profile.

**Disposition for this thesis:** verified [fetched].

## Open questions / things to verify

- Table 5 per-group tick attribution `[parse-uncertain]` — recover from the
  PDF only if a per-group claim is ever needed (counts suffice for the
  profiles).
- The "months and even years" dwell cites the review's ref [8] — second-hand;
  the M-Trends/Sophos macro reports are the quantitative versions and
  supersede it as calibration targets.

## Out of scope for this thesis

The entire detection-method taxonomy (similarity / causal-correlation /
structural / case-based themes and their 45 constituent studies); the
proposed 4-module vulnerability-weighted detection architecture (Fig. 7);
vendor tooling assessment (Table 1); AI/SOAR future-work discussion. Detection
is a culled thread — recorded here so nobody re-reads 18 pages to rediscover
that.
