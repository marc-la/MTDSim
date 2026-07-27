# Alshamrani 2019 — extraction notes

> A. Alshamrani, S. Myneni, A. Chowdhary, D. Huang. "A Survey on Advanced Persistent Threats: Techniques, Solutions, Challenges, and Research Opportunities." *IEEE Communications Surveys & Tutorials*, vol. 21, no. 2, pp. 1851–1877, 2019.
> Source file: `docs/sources/lit_review/2_3_alshamrani2019survey.md` (gitignored; path corrected 2026-07-27 — the extraction previously pointed at the pre-refactor top-level location).
> Relevance to this thesis: defining survey of APTs (lit review §III-C) — three-property framing (advanced / persistent / threat), five-phase lifecycle (reconnaissance → foothold → lateral movement → exfiltration-or-impediment → cleanup), commodity-vs-APT contrast.

## Bibliographic anchor

- **Citation key**: `alshamrani2019`
- **DOI / URL**: 10.1109/COMST.2019.2891891
- **Pages cited from**: full text

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### Relevance class

**S — Supporting-argument.** Alshamrani 2019 anchors the APT adversary class in lit review §III-C — three-property definition, NIST behavioural framing, five-phase lifecycle, and the commodity-vs-APT contrast — but does not drive any L0→L4 methodology decision in [`../specs/architecture.md`](../../implementation/architecture.md). It establishes *what an APT is* so that subsequent sections (Cho's four characteristics at §IV-B framing, the fidelity ladder at §IV-B, the GASP motivation set at architecture §(e)) inherit a defensible adversary definition. The paper is rhetorical scaffolding, not a methodology source.

### Used in lit review

- [`../sources/LIT_REVIEW.md:123`](../lit_review/LIT_REVIEW.md#L123) — opens §III-C with the three-property framing (*advanced* tooling, *persistent* low-and-slow tempo, *threat* defined by objective) and the NIST behavioural restatement (pursues objectives repeatedly, adapts to defender resistance, sustains the interaction needed) — all cited to [8] = Alshamrani.
- [`../sources/LIT_REVIEW.md:123`](../lit_review/LIT_REVIEW.md#L123) (same paragraph) — anchors the commodity-attacker contrast ("single-run, smash-and-grab operations that neither hide nor adapt and end at first detection") to Alshamrani.
- [`../sources/LIT_REVIEW.md:125`](../lit_review/LIT_REVIEW.md#L125) — anchors the five-phase APT lifecycle (reconnaissance → foothold → lateral movement → exfiltration-or-impediment → cleanup) and the invariant-vs-contingent split (phases 1–2 invariant; 3–5 contingent on the three NIST-derived objectives) to Alshamrani.
- [`../sources/LIT_REVIEW.md:165`](../lit_review/LIT_REVIEW.md#L165) — §IV-B framing prose pivots Cho's *persistent* characteristic into APT multi-stage operations ("multi-stage APT operations [8]") — cross-attribution flagged below in *Maps to*.

---

### APT class definition — three properties + NIST behavioural framing

**Source locator:** §II-A "What Is APT?", p. 1853.

**Paraphrase:** Alshamrani defines APT as the conjunction of three properties. *Advanced* names the tooling: well-funded attackers with access to multi-vector methods, including custom malware that signature-based detection does not catch. *Persistent* names the tempo: a "low and slow" approach with evasive techniques to elude IDS, sustained for as long as the funding source requires. *Threat* names the objective: sensitive-data loss or impediment of mission-critical components, against organisations whose missions or data warrant the investment. The paper then restates the same profile behaviourally via NIST: an APT actor (i) pursues its objectives repeatedly over an extended period, (ii) adapts to defenders' efforts to resist it, and (iii) is determined to maintain the level of interaction needed to execute its objectives — exfiltration of information, or undermining/impeding critical aspects of a mission or program, through multiple attack vectors. The "What Is NOT APT?" subsection (§II-B, p. 1853) sharpens the boundary: an attack that could have been prevented with minimal countermeasures, did not require adaptation against defender resistance, or exhibited no novelty in its variants is a targeted breach rather than an APT — the operational definition of the commodity-attacker contrast.

**Quote (if essential):**
> "An APT attacker: (i) pursues its objectives repeatedly over an extended period of time; (ii) adapts to defenders efforts to resist it; and (iii) is determined to maintain the level of interaction needed to execute its objectives." (§II-A, p. 1853, paraphrasing NIST)

**Maps to:** [`../specs/architecture.md`](../../implementation/architecture.md) §(e) L2 GASP motivation set `{espionage, disruption, financial}` — the NIST objective triad (exfiltration / impediment / position-for-future, §II-C, p. 1854) is the documented source the GASP motivation categories trace back to via ATT&CK group descriptions. Also underwrites the §IV-B framing in [`../sources/LIT_REVIEW.md:163-166`](../lit_review/LIT_REVIEW.md#L163) where Cho's *persistent* and *adaptive* characteristics align with NIST clauses (i) and (ii) — the cross-reference is via [[cho2020]], not by quoting Cho here.

**Disposition for this thesis:** *adopted-as-baseline.* This is the adversary definition the dissertation inherits. The behaviourally-grounded adversarial profiles the thesis motivates are built precisely against the class Alshamrani defines — the GASP motivation set at L2 is the NIST objective triad in different clothing, and the §IV-B fidelity ladder is calibrated to discriminate threat models that capture the NIST clauses from threat models that do not (parametric/scripted rungs fail clause (ii), procedural+ rungs begin to engage it).

---

### Five-phase APT lifecycle — invariant prefix and objective-conditioned suffix

**Source locator:** §II-C "APT Attack Model", p. 1854 (five-stage enumeration); also §II-C, p. 1854–1859 (per-stage detail).

**Paraphrase:** Alshamrani consolidates Mandiant's seven-stage and Ussath's three-stage lifecycles into a five-phase model: (1) Reconnaissance — extensive passive information-gathering about target IT infrastructure and personnel before any exploit, distinguishing APT reconnaissance from the active scanning a commodity attacker would perform; (2) Establish Foothold — successful entry, typically via spear-phishing, watering-hole, known-vulnerability exploitation, or zero-day; (3) Lateral Movement / Stay Undetected — credential dumping, pass-the-hash, privilege escalation through the network in search of target resources; (4) Exfiltration or Impediment — split by objective: data exfiltration to C&C servers (often batched and IP-diversified to evade ingress-only filtering), or disabling/destroying critical components; (5) Post-Exfiltration / Post-Impediment — sustained operations, log scrubbing, and clean exit. The paper makes a structural claim that matters for the dissertation's adversary modelling: stages 1–2 are invariant across all APT operations, while stages 3–5 are *conditioned on the attacker's objective*. The "position for future" objective in particular does not enter stages 4–5 at all, instead extending stage 3 indefinitely as the attacker silently observes and maps the environment.

**Maps to:** [`../specs/architecture.md`](../../implementation/architecture.md) §(f) L3 OGASP — the inherited 6-phase attacker module ([`../../mtdnetwork/component/adversary.py`](../../../mtdnetwork/component/adversary.py)) is the substrate's procedural baseline for this lifecycle; the graph-driven attacker that traverses GASP within MTDSim is the design intent for encoding the objective-conditioned suffix. Also maps to [`../specs/architecture.md`](../../implementation/architecture.md) §(e) — the motivation-subgraphing transformation at L2 is the structural correlate of Alshamrani's "stages 3–5 are objective-conditioned" claim: different motivations select different terminal regions of the underlying GAP.

**Disposition for this thesis:** *adopted-as-baseline.* The lifecycle frames the lit review's APT adversary class and is the conceptual ancestor of both the 6-phase substrate attacker (procedural baseline) and the L2 GASP motivation-conditioned subgraph (behavioural-fidelity target). The dissertation does not implement Alshamrani's five phases directly — the substrate inherits a six-phase enumeration, and the GASP traversal will resolve to ATT&CK technique-level granularity rather than phase-level — but the load-bearing structural claim (invariant prefix, objective-conditioned suffix) is preserved.

---

### The consolidated lifecycles — Mandiant's seven stages and Ussath's three (secondary channel; added 2026-07-27 for the S1 consensus overlay)

**Source locator:** §II-C "APT Attack Model: How APT Attacks Are Made?",
p. 1854 (source markdown lines 87–89). Alshamrani is the **channel**, not the
primary source: Mandiant's model is the paper's ref [1] (D. McWhorter, *APT1:
Exposing One of China's Cyber Espionage Units*, Mandiant, 2013); Ussath's is
ref [7] (M. Ussath, D. Jaeger, F. Cheng, C. Meinel, "Advanced persistent
threats: Behind the scenes", *Proc. CISS 2016*, pp. 181–186).

**Paraphrase:** Before presenting its own five-phase model, the paper records
the two lifecycles it consolidates. **Mandiant's** APT attack life cycle has
seven stages — Initial Compromise (1), Establish Foothold (2), Escalate
Privileges (3), Internal Reconnaissance (4), Move Laterally (5), Maintain
Presence (6), Complete Mission (7) — **"with stages 3 through 6 happening in
any order"**. **Ussath's** three-stage model, focusing only on the
representative characteristics of an APT attack, is Initial Compromise (1),
Lateral Movement (2), Command & Control Activity (3). Alshamrani's own verdict
on the model family: "all these attack models are similar in terms of the
operations involved in APT attacks, they are either too generalized or too
specific" — which is the paper's motivation for its own five stages.

**Quote (essential — the any-order caveat is load-bearing for the consensus):**
> "Mandiant has discussed it's APT attack life cycle model consisting of 7 stages - Initial Compromise (1), Establish Foothold (2), Escalate Privileges (3), Internal Reconnaissance (4), Move Laterally (5), Maintain Presence (6) and Complete Mission (7) with stages 3 through 6 happening in any order." (§II-C, p. 1854)

**Maps to:** [`../../implementation/pipeline/ogasp/lifecycle_consensus.md`](../../implementation/pipeline/ogasp/lifecycle_consensus.md)
(models L3 and L4). The any-order caveat is the strongest direct evidence that
the post-foothold middle of the campaign is only weakly ordered — it is what
stops the consensus asserting a finer-than-stage ordering there.

**Disposition for this thesis:** *adopted-as-evidence via secondary channel;
Mandiant half primary-verified 2026-07-27.* The stage names and the any-order
caveat are used exactly as Alshamrani reports them. Flags, both resolved for
the Mandiant model: (a) ~~the APT1 lifecycle figure is commonly depicted with
an initial reconnaissance stage this seven-stage listing omits~~ — primary
acquired ([`mandiant2013`](mandiant2013.md)): **both readings are faithful** —
the report's prose describes seven stages beginning at Initial Compromise
(what Alshamrani reports), while its Figure 14 depicts eight including
Initial Recon; (b) ~~name-only mapping cells flagged `verify`~~ — resolved
from the primary's Appendix B definitions. The **Ussath** model remains
channel-only (primary unread; on the to-download list if ever load-bearing
beyond its consensus vote).

---

### Per-tactic dwell character, MTD-effect, and the synthetic-model caveat (Step B, 2026-07-04)

**Source locator:** §II-C Stages 1–5; §II-D (C&C); §III-C/§III-D/§III-E (Stuxnet, RSA,
Carbanak case studies); §IV-A (monitoring — Villeneuve & Bennett, Shalaginov, Virvilis &
Gritzalis); §IV-B (detection); §IV-C-1-A (Johnson & Hogan); §IV-C-2-B (Moving Target
Defense); §V (evaluation methodologies).

**Paraphrase:** This paper is the **backbone behavioural source** for the per-tactic dwell
profiles ([`../tactic_profiles/`](../tactic_profiles/)); the following per-tactic claims are
mined for §2 (group-assignment) and §4 (timing evidence) of those files. *Reconnaissance*
(TA0043) is "passive" in the sense of *non-exploitative*, yet includes active port/service
scanning, WHOIS/BGP and fingerprinting — low-and-slow in *tempo*, not modality (§II-C
Stage 1). *Resource-development* (TA0042) tooling/planning is off-network, before the
foothold (§I, §II-C Stage 1) → near-zero in-sim dwell. *Initial-access* (TA0001) is mostly
*known*-vuln exploitation + spear-phishing (most common); the attacker then "patiently
wait[s]" for user-triggered execution (§II-C Stage 2, §VIII). *Execution* (TA0002) "keep[s]
low to go undetected"; fileless/in-memory (Duqu 2.0) is evasive (§II-C Stage 2, §IV-A).
*Persistence* (TA0003) is durable/sticky ("very difficult to push out"); pre-OS bootkits
"loaded even before the OS" survive reimaging (§II-C Stage 3, §I). *Privilege-escalation*
(TA0004) is exploit-driven on demand (Stuxnet 2 Windows 0-days → "full control"; §II-C
Stage 3, §III-C). *Stealth* (TA0005, post-split) is the defining "low and slow" behaviour;
the evasion set (rootkit, obfuscation, steganography, in-memory, fake certs; §IV-A) is
*hiding* → allocates to `stealth`, **not** `defense-impairment`, which the paper barely
addresses. *Credential-access* (TA0006): "stolen legitimate credentials"; mimikatz/WCE/LSA;
"dumping most common for lateral movement" (§II-C Stage 3, §VIII). *Discovery* (TA0007) is
internal scanning; the "position for future" objective makes it an indefinite passive watch
(§II-A, §II-C). *Lateral-movement* (TA0008) spans slow human pass-the-hash to Stuxnet's
fast worm-style auto-propagation (LNK/print-spooler/Step7 password; §II-C Stage 3, §III-C);
modelled as graph reachability by Johnson & Hogan (§IV-C-1-A). *Collection*/*Exfiltration*
(TA0009/TA0010): data "compressed and encrypted" then exfiltrated over FTP (RSA, §III-D),
"intelligently split … into batches and to servers with different IP addresses" to evade
ingress-only filtering (§II-C Stage 4). *C&C* (TA0011) is a "long-term connection" over
HTTP (blends), beaconing "at given intervals" / "several times per day" with fast-flux URL
rotation "every couple of minutes" (§II-D, §IV-A, §IV-B). *Impact* (TA0040) is
disabling/destroying components (Stuxnet); the dwell ceiling is sponsor-bounded — "ends when
… the funding organization gets all the data it needs" (§II-C Stage 4/5, §I).

**MTD-effect (feeds §3 / Step E, recorded here now):** §IV-C-2-B is the load-bearing
sentence — "The APT scenarios rely on exploration of cloud system or network in order to
create exploitation plan. **The rearrangement of network or software components renders the
exploratory knowledge of the attacker useless.**" i.e. shuffle/diversity invalidates
reconnaissance/discovery ("exploratory knowledge"), and the paper does *not* extend that to
established footholds. Crouse et al. [82] (§IV-C-2-B) frame MTD as denying the "static and
long-term assumptions" recon relies on, but caveat that a small number of honeypots *beat*
defence-by-movement in their foothold-establishment / minimum-to-win scenarios. The NIST
definition (§II-A) that an APT "adapts to defenders' efforts to resist it" implies MTD
provokes re-adaptation rather than permanent denial.

**Methodological caveat (feeds the op-validation note):** §V warns that a synthetic model is
"based on simplified attack scenarios … where no realistic noise is involved … one of the
major points APT attackers consider to stay undetected and move low and slow", and that the
field "lacks data sets from realistic attack scenarios" — a direct limit on reading dwell
character off a synthetic substrate, reinforcing shape-not-scale and the modest-claim
discipline.

**Maps to:** all fifteen [`../tactic_profiles/`](../tactic_profiles/) files (§2/§4);
the MTD-effect paragraph feeds their §3 (Step E) and
[`../notes/2026-07-04_operational_validation_the_bar.md`](../../notes/ch3_design/operational_validation.md).

**Disposition for this thesis:** *adopted-as-evidence.* No per-tactic *duration* is taken
from this paper (it publishes none — that is the gap); the per-tactic *behaviour/dwell
character* is the qualitative input to the group-assignment argument, and the MTD-effect and
synthetic-model caveats are recorded for §3 and the validity rationale respectively.

---

## Open questions / things to verify

- The "according to NIST" framing at §II-A (p. 1853) carries reference [3] in Alshamrani's bibliography. The lit review currently cites Alshamrani [8] for the NIST behavioural restatement rather than NIST SP 800-39 directly; for the dissertation bibliography, decide whether to (a) keep the indirect citation through Alshamrani as the *secondary source where this triad becomes load-bearing for APT framing*, or (b) chase the NIST primary source (SP 800-39 / SP 800-30) and cite it directly. Defer to lit-review citation policy.
- Alshamrani §II-A also references Chen et al. [4] for the APT-vs-traditional comparison table (Table I, §II-A, p. 1853) — confirm whether the commodity-vs-APT contrast at [`../sources/LIT_REVIEW.md:123`](../lit_review/LIT_REVIEW.md#L123) intends to inherit Alshamrani's framing exclusively, or whether Chen's table is a complementary anchor worth surfacing.

## Out of scope for this thesis

- The detailed enumeration of APT groups; the dissertation references named groups (APT29, Lazarus, Volt Typhoon) via ATT&CK G-IDs, not via this paper's catalogue.
