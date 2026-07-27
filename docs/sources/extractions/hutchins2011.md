# Hutchins, Cloppert & Amin 2011 — extraction notes

> E. M. Hutchins, M. J. Cloppert, R. M. Amin. "Intelligence-Driven Computer
> Network Defense Informed by Analysis of Adversary Campaigns and Intrusion
> Kill Chains." Lockheed Martin Corporation white paper, 2011. (Widely cited
> via the *6th International Conference on Information Warfare and Security*
> (ICIW 2011) — venue `verify`: the white-paper PDF carries no venue imprint,
> so the conference attribution is taken from citation convention, not from
> the artefact itself.)
> Source file: `docs/sources/hutchins2011killchain.md` (+ `.pdf`, gitignored;
> fetched OA from lockheedmartin.com, 2026-07-27).
> Relevance to this thesis: the **primary source for the Cyber Kill Chain** —
> the seven-phase intrusion kill chain that the L3 controller's ATT&CK→CKC
> crosswalk and the S1 lifecycle-consensus overlay both consume. Until this
> extraction, the CKC was cited in-project only via secondary channels
> (Che Mat Table 4; Kim 2026's "seven steps").

## Bibliographic anchor

- **Citation key**: `hutchins2011`
- **DOI / URL**: https://www.lockheedmartin.com/content/dam/lockheed-martin/rms/documents/cyber/LM-White-Paper-Intel-Driven-Defense.pdf
- **Pages cited from**: pp. 1–5 (abstract; §3.2)

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### Relevance class

**L — Load-bearing on methodology.** The seven-phase enumeration and its
sequentiality claim are the primary overlay of the S1 lifecycle-consensus
artefact ([`../../implementation/pipeline/ogasp/lifecycle_consensus.md`](../../implementation/pipeline/ogasp/lifecycle_consensus.md)),
which grounds the tactic-to-tactic distance model the outcome-overlay weights
consume. The ATT&CK→CKC crosswalk already in use
([`../../implementation/pipeline/ogasp/controller.md`](../../implementation/pipeline/ogasp/controller.md) §1)
inherits its phase vocabulary from this paper.

---

### The seven-phase intrusion kill chain

**Source locator:** §3.2 "Intrusion Kill Chain", pp. 4–5.

**Paraphrase:** Hutchins et al. adapt the U.S. military targeting kill chain
(F2T2EA) into a model specifically for network intrusions. The essence of an
intrusion is that the aggressor must develop a payload to breach a trusted
boundary, establish a presence inside a trusted environment, and from that
presence take actions towards their objectives. The seven phases, with their
defining behaviours: (1) *Reconnaissance* — research, identification and
selection of targets (crawling websites, harvesting email addresses and
social relationships); (2) *Weaponization* — coupling a remote-access trojan
with an exploit into a deliverable payload, typically via an automated
weaponizer; (3) *Delivery* — transmission of the weapon to the target
environment (LM-CIRT's three most prevalent APT vectors 2004–2010: email
attachments, websites, USB media); (4) *Exploitation* — the delivered weapon
triggers the intruder's code, usually against an application or OS
vulnerability, or against the user directly; (5) *Installation* — a
remote-access trojan or backdoor is installed, which "allows the adversary to
maintain persistence inside the environment"; (6) *Command and Control* —
compromised hosts beacon outbound to establish a C2 channel giving intruders
"hands on the keyboard" access; (7) *Actions on Objectives* — typically data
exfiltration ("collecting, encrypting and extracting information"), or
violations of data integrity/availability, or using the victim as "a hop
point to compromise additional systems and move laterally inside the
network".

**Quote (essential — the enumeration and the sequentiality claim):**
> "The intrusion kill chain is defined as reconnaissance, weaponization, delivery, exploitation, installation, command and control (C2), and actions on objectives." (§3.2, p. 4)

> "Only now, after progressing through the first six phases, can intruders take actions to achieve their original objectives." (§3.2 phase 7, p. 5)

**Maps to:** [`../../implementation/pipeline/ogasp/lifecycle_consensus.md`](../../implementation/pipeline/ogasp/lifecycle_consensus.md)
(model L1) · [`../../implementation/pipeline/ogasp/controller.md`](../../implementation/pipeline/ogasp/controller.md) §1
(the tactic→CKC→verb construction).

**Disposition for this thesis:** *adopted-as-baseline* as the primary
lifecycle overlay (per the S1 ruling,
[`../../implementation/pipeline/ogasp/supervisor_decision_register.md`](../../implementation/pipeline/ogasp/supervisor_decision_register.md) §S1).
Three cell-level consequences for the ATT&CK mapping, taken from the phase
*definitions* rather than the phase names: Installation is defined as
persistence-establishment (grounds `persistence` → Installation);
C2 is a discrete phase between Installation and Actions on Objectives
(one pole of the C2-placement disagreement the consensus artefact records);
and lateral movement appears *inside* Actions on Objectives (the "hop point"
sentence), not as its own phase.

---

### The chain framing — sequentiality as a defensive premise

**Source locator:** §3.2 opening, p. 4; abstract, p. 1.

**Paraphrase:** The model is called a *chain* because it is "an integrated,
end-to-end process" in which "any one deficiency will interrupt the entire
process" — the defensive value proposition is precisely that phases are
traversed in order, so breaking any early phase denies all later ones. This
is the strongest sequential-ordering claim among the lifecycle models the
consensus artefact overlays; the APT-specific models (Mandiant's stages 3–6
"in any order", via [[alshamrani2019]]) relax it in the post-foothold middle.

**Maps to:** [`../../implementation/pipeline/ogasp/lifecycle_consensus.md`](../../implementation/pipeline/ogasp/lifecycle_consensus.md)
(the invariant-prefix / weakly-ordered-middle consensus shape).

**Disposition for this thesis:** *adopted-as-evidence* for the consensus's
strong ordering at the campaign's ends. Not read as evidence that the
post-intrusion middle is strictly ordered — the CKC compresses the whole
post-foothold campaign into phases 5–7, so it is structurally silent about
ordering *within* what ATT&CK individuates as eight post-intrusion tactics.

---

## Open questions / things to verify

- **Venue imprint** — the white-paper PDF carries no conference imprint; the
  conventional citation is ICIW 2011 (Academic Conferences International).
  Confirm the venue string against the dissertation's citation policy before
  the bibliography is finalised (`verify`).
- The paper's Mandiant reference (§2, p. 3: "the security company Mandiant
  proposes an 'exploitation life cycle'") predates the APT1 report's
  seven-stage lifecycle; the two Mandiant models are related but not the same
  artefact. Keep the citation trails distinct.

## Out of scope for this thesis

- The courses-of-action matrix (§3.3), the campaign-analysis method (§3.4),
  and the three intrusion case studies (§4) — defensive-intelligence
  methodology, not lifecycle structure.
