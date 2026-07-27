# Mandiant 2013 (APT1 report) — extraction notes

> Mandiant. "APT1: Exposing One of China's Cyber Espionage Units." Mandiant
> (Alexandria, VA), 2013, 76 pp. (Cited elsewhere in this repo's channels as
> D. McWhorter, per Alshamrani's ref [1].)
> Source file: `docs/sources/lit_review/mandiant-apt1-report.pdf` (+ `.md`
> text conversion, gitignored; supplied by Marc 2026-07-27).
> Relevance to this thesis: the **primary source for the Mandiant attack
> lifecycle** — model L3 of the S1 lifecycle-consensus overlay
> ([`../../implementation/pipeline/ogasp/lifecycle_consensus.md`](../../implementation/pipeline/ogasp/lifecycle_consensus.md)),
> previously cited only via Alshamrani's channel. Read for the lifecycle
> structure only; the APT1 attribution case is out of scope.

## Bibliographic anchor

- **Citation key**: `mandiant2013`
- **DOI / URL**: no DOI (industry report); widely mirrored — cite the report itself
- **Pages cited from**: pp. 27–28 (Figure 14 + lifecycle section opening); pp. 63–65 (Appendix B, per-stage definitions)

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### Relevance class

**L — Load-bearing on methodology** (for the consensus overlay only). The
lifecycle's stage set, its per-stage behavioural definitions, and the
explicit statement that the post-foothold middle is unordered and cyclic are
direct inputs to the consensus ordering that grounds the tactic-to-tactic
distance model.

---

### The Attack Lifecycle model — eight stages in the figure, seven in the prose

**Source locator:** Figure 14 "Mandiant's Attack Lifecycle Model", p. 27;
"APT1: Attack Lifecycle" section pp. 27–40; Appendix B "APT and the Attack
Lifecycle", pp. 63–65.

**Paraphrase:** Figure 14 depicts **eight** stages: Initial Recon → Initial
Compromise → Establish Foothold → Escalate Privileges → Internal Recon →
Move Laterally → Maintain Presence → Complete Mission (drawn as a cycle —
the middle four loop). The **prose**, however — both the main-body walkthrough
(which opens at "The Initial Compromise", p. 28) and Appendix B's per-stage
overview — describes **seven** stages, beginning at Initial Compromise;
*Initial Recon appears in the figure only and receives no section of its
own*. This reconciles the secondary channels: Alshamrani's seven-stage
listing ([`alshamrani2019`](alshamrani2019.md) §II-C) tracks the prose, while
the eight-node rendering commonly reproduced elsewhere tracks the figure.
Both are faithful to different parts of the primary.

**Maps to:** [`../../implementation/pipeline/ogasp/lifecycle_consensus.md`](../../implementation/pipeline/ogasp/lifecycle_consensus.md)
model L3 (upgraded from secondary channel to primary-verified, 2026-07-27).
The figure-level Initial Recon stage is consistent with the consensus's
preparation stage (s0) preceding intrusion — it does not change any seat.

**Disposition for this thesis:** *adopted-as-evidence.* Record the model as
"eight stages by figure, seven by prose"; when a stage-by-stage enumeration
is needed, use the prose's seven (the channel-verified form) and note the
figure's prefix stage.

---

### The middle is unordered — and cyclic

**Source locator:** Appendix B opening, p. 63.

**Paraphrase:** The report states directly that the stages between Establish
Foothold and Complete Mission (i.e. Escalate Privileges, Internal Recon,
Move Laterally, Maintain Presence) need not occur in the listed order, and
goes further than any-order: once established, APT groups repeat a
recon → identify → move-laterally → steal cycle indefinitely until evicted.
This is the primary form of the caveat Alshamrani reports as "stages 3
through 6 happening in any order" — confirmed, and strengthened from
*permutable* to *cyclic and repeating*, with even "completing mission"
recurring within a single campaign.

**Quote (essential — the load-bearing ordering caveat, now primary):**
> "The stages between 'Establish Foothold' and 'Complete Mission' do not have to occur in this order every time. In fact, once established within a network, APT groups will continually repeat the cycle of conducting reconnaissance, identifying data of interest, moving laterally to access that data, and 'completing mission' by stealing the data." (Appendix B, p. 63)

**Maps to:** [`../../implementation/pipeline/ogasp/lifecycle_consensus.md`](../../implementation/pipeline/ogasp/lifecycle_consensus.md)
§4 (the weakly-ordered middle — this is now its strongest evidence) and §6
(the within-stage distance of 1.0: the literature not only declares no order
in the middle, it attests *repeated traversal* there).

**Disposition for this thesis:** *adopted-as-baseline* for the consensus's
weakly-ordered stage 2. Note the nuance: Complete Mission recurring inside
the cycle blurs the middle/objective boundary *within a campaign*; the
consensus keeps the objective stage terminal because every model (including
this one's own stage listing) still places mission completion as the
campaign's end-state, and the cyclic re-entry is verdict/behaviour
machinery (the overlay's failure/retry routing), not stage ordering.

---

### Per-stage behavioural definitions (Appendix B) — the mapping cells, primary-grounded

**Source locator:** Appendix B, pp. 63–65 (each stage's paragraph).

**Paraphrase, stage by stage, with the ATT&CK-tactic reading used by the
consensus mapping:**

- **Initial Compromise** (p. 63): penetration methods — spear phishing
  (attachment / link), strategic web compromise, webshells on vulnerable
  Internet-facing servers. → `initial-access`; the user-triggered payload
  reading also supports `execution`.
- **Establish Foothold** (p. 63): backdoors (public, underground, custom)
  that "establish an outbound connection from the victim network to a
  computer controlled by the attackers", giving shell/GUI control. →
  `persistence` **and** `command-and-control`, both from the definition —
  resolves the cell previously flagged `verify` under the name-only channel.
- **Escalate Privileges** (p. 64): "Most often this consists of obtaining
  usernames and passwords" — hash dumping (preferably from Domain
  Controllers), cracking, pass-the-hash, harvesting PKI certificates and VPN
  credentials. → `privilege-escalation` **and** `credential-access`, both
  from the definition — resolves the second `verify` cell.
- **Internal Reconnaissance** (p. 64): built-in OS commands, share/directory
  listings, keyword and extension searches to identify data of interest. →
  `discovery`.
- **Move Laterally** (p. 64): compromised credentials / pass-the-hash with
  PsExec and the Task Scheduler to execute commands and install malware on
  remote systems. → `lateral-movement`.
- **Maintain Presence** (pp. 64–65): *new* backdoors distinct from the
  foothold's, multiple malware families, "a variety of command and control
  addresses, presumably for redundancy", plus non-backdoor access (valid
  PKI/VPN credentials, circumventing two-factor). → `persistence` and
  `command-and-control` again — persistence and C2 are each seated **twice**
  in this model, confirming the non-unique seating the consensus resolves by
  rule R-1.
- **Complete Mission** (p. 65): pack files of interest into (usually
  password-protected) RAR/ZIP archives, then transfer out via FTP, custom
  tools, or existing backdoors. → `collection` and `exfiltration`, from the
  definition. **`impact` is not attested here** — APT1's mission is data
  theft; the consensus's stage-3 seat for `impact` rests on the CKC
  (integrity/availability violations) and Alshamrani (impediment), not on
  this model.

**Maps to:** [`../../implementation/pipeline/ogasp/lifecycle_consensus.md`](../../implementation/pipeline/ogasp/lifecycle_consensus.md)
§3 (the L3 mapping table).

**Disposition for this thesis:** *adopted-as-evidence.* All previously
`verify`-flagged L3 cells are resolved from the primary; no consensus seat
changes.

---

## Open questions / things to verify

- None for the lifecycle use. The venue/author string ("D. McWhorter" vs the
  corporate "Mandiant" byline — the report itself carries no individual
  byline) should follow the dissertation's citation policy for industry
  reports when the bibliography is finalised.

## Out of scope for this thesis

- The APT1/PLA Unit 61398 attribution case, the malware family appendices
  (WEBC2 etc.), the indicators appendix, and the per-victim statistics —
  everything except the lifecycle model and its stage definitions.
