# Alshamrani 2019 — extraction notes

> A. Alshamrani, S. Myneni, A. Chowdhary, D. Huang. "A Survey on Advanced Persistent Threats: Techniques, Solutions, Challenges, and Research Opportunities." *IEEE Communications Surveys & Tutorials*, vol. 21, no. 2, pp. 1851–1877, 2019.
> Source file: `docs/sources/2_3_alshamrani2019survey.md` (gitignored).
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

**S — Supporting-argument.** Alshamrani 2019 anchors the APT adversary class in lit review §III-C — three-property definition, NIST behavioural framing, five-phase lifecycle, and the commodity-vs-APT contrast — but does not drive any L0→L4 methodology decision in [`../specs/architecture.md`](../specs/architecture.md). It establishes *what an APT is* so that subsequent sections (Cho's four characteristics at §IV-B framing, the fidelity ladder at §IV-B, the GASP motivation set at architecture §(e)) inherit a defensible adversary definition. The paper is rhetorical scaffolding, not a methodology source.

### Used in lit review

- [`../sources/LIT_REVIEW.md:123`](../sources/LIT_REVIEW.md#L123) — opens §III-C with the three-property framing (*advanced* tooling, *persistent* low-and-slow tempo, *threat* defined by objective) and the NIST behavioural restatement (pursues objectives repeatedly, adapts to defender resistance, sustains the interaction needed) — all cited to [8] = Alshamrani.
- [`../sources/LIT_REVIEW.md:123`](../sources/LIT_REVIEW.md#L123) (same paragraph) — anchors the commodity-attacker contrast ("single-run, smash-and-grab operations that neither hide nor adapt and end at first detection") to Alshamrani.
- [`../sources/LIT_REVIEW.md:125`](../sources/LIT_REVIEW.md#L125) — anchors the five-phase APT lifecycle (reconnaissance → foothold → lateral movement → exfiltration-or-impediment → cleanup) and the invariant-vs-contingent split (phases 1–2 invariant; 3–5 contingent on the three NIST-derived objectives) to Alshamrani.
- [`../sources/LIT_REVIEW.md:165`](../sources/LIT_REVIEW.md#L165) — §IV-B framing prose pivots Cho's *persistent* characteristic into APT multi-stage operations ("multi-stage APT operations [8]") — cross-attribution flagged below in *Maps to*.

---

### APT class definition — three properties + NIST behavioural framing

**Source locator:** §II-A "What Is APT?", p. 1853.

**Paraphrase:** Alshamrani defines APT as the conjunction of three properties. *Advanced* names the tooling: well-funded attackers with access to multi-vector methods, including custom malware that signature-based detection does not catch. *Persistent* names the tempo: a "low and slow" approach with evasive techniques to elude IDS, sustained for as long as the funding source requires. *Threat* names the objective: sensitive-data loss or impediment of mission-critical components, against organisations whose missions or data warrant the investment. The paper then restates the same profile behaviourally via NIST: an APT actor (i) pursues its objectives repeatedly over an extended period, (ii) adapts to defenders' efforts to resist it, and (iii) is determined to maintain the level of interaction needed to execute its objectives — exfiltration of information, or undermining/impeding critical aspects of a mission or program, through multiple attack vectors. The "What Is NOT APT?" subsection (§II-B, p. 1853) sharpens the boundary: an attack that could have been prevented with minimal countermeasures, did not require adaptation against defender resistance, or exhibited no novelty in its variants is a targeted breach rather than an APT — the operational definition of the commodity-attacker contrast.

**Quote (if essential):**
> "An APT attacker: (i) pursues its objectives repeatedly over an extended period of time; (ii) adapts to defenders efforts to resist it; and (iii) is determined to maintain the level of interaction needed to execute its objectives." (§II-A, p. 1853, paraphrasing NIST)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(e) L2 GASP motivation set `{espionage, disruption, financial}` — the NIST objective triad (exfiltration / impediment / position-for-future, §II-C, p. 1854) is the documented source the GASP motivation categories trace back to via ATT&CK group descriptions. Also underwrites the §IV-B framing in [`../sources/LIT_REVIEW.md:163-166`](../sources/LIT_REVIEW.md#L163) where Cho's *persistent* and *adaptive* characteristics align with NIST clauses (i) and (ii) — the cross-reference is via [[cho2020]], not by quoting Cho here.

**Disposition for this thesis:** *adopted-as-baseline.* This is the adversary definition the dissertation inherits. The behaviourally-grounded adversarial profiles the thesis motivates are built precisely against the class Alshamrani defines — the GASP motivation set at L2 is the NIST objective triad in different clothing, and the §IV-B fidelity ladder is calibrated to discriminate threat models that capture the NIST clauses from threat models that do not (parametric/scripted rungs fail clause (ii), procedural+ rungs begin to engage it).

---

### Five-phase APT lifecycle — invariant prefix and objective-conditioned suffix

**Source locator:** §II-C "APT Attack Model", p. 1854 (five-stage enumeration); also §II-C, p. 1854–1859 (per-stage detail).

**Paraphrase:** Alshamrani consolidates Mandiant's seven-stage and Ussath's three-stage lifecycles into a five-phase model: (1) Reconnaissance — extensive passive information-gathering about target IT infrastructure and personnel before any exploit, distinguishing APT reconnaissance from the active scanning a commodity attacker would perform; (2) Establish Foothold — successful entry, typically via spear-phishing, watering-hole, known-vulnerability exploitation, or zero-day; (3) Lateral Movement / Stay Undetected — credential dumping, pass-the-hash, privilege escalation through the network in search of target resources; (4) Exfiltration or Impediment — split by objective: data exfiltration to C&C servers (often batched and IP-diversified to evade ingress-only filtering), or disabling/destroying critical components; (5) Post-Exfiltration / Post-Impediment — sustained operations, log scrubbing, and clean exit. The paper makes a structural claim that matters for the dissertation's adversary modelling: stages 1–2 are invariant across all APT operations, while stages 3–5 are *conditioned on the attacker's objective*. The "position for future" objective in particular does not enter stages 4–5 at all, instead extending stage 3 indefinitely as the attacker silently observes and maps the environment.

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(f) L3 OGASP — the inherited 6-phase attacker module ([`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py)) is the substrate's procedural baseline for this lifecycle; the graph-driven attacker that traverses GASP within MTDSim is the design intent for encoding the objective-conditioned suffix. Also maps to [`../specs/architecture.md`](../specs/architecture.md) §(e) — the motivation-subgraphing transformation at L2 is the structural correlate of Alshamrani's "stages 3–5 are objective-conditioned" claim: different motivations select different terminal regions of the underlying GAP.

**Disposition for this thesis:** *adopted-as-baseline.* The lifecycle frames the lit review's APT adversary class and is the conceptual ancestor of both the 6-phase substrate attacker (procedural baseline) and the L2 GASP motivation-conditioned subgraph (behavioural-fidelity target). The dissertation does not implement Alshamrani's five phases directly — the substrate inherits a six-phase enumeration, and the GASP traversal will resolve to ATT&CK technique-level granularity rather than phase-level — but the load-bearing structural claim (invariant prefix, objective-conditioned suffix) is preserved.

---

## Open questions / things to verify

- The "according to NIST" framing at §II-A (p. 1853) carries reference [3] in Alshamrani's bibliography. The lit review currently cites Alshamrani [8] for the NIST behavioural restatement rather than NIST SP 800-39 directly; for the dissertation bibliography, decide whether to (a) keep the indirect citation through Alshamrani as the *secondary source where this triad becomes load-bearing for APT framing*, or (b) chase the NIST primary source (SP 800-39 / SP 800-30) and cite it directly. Defer to lit-review citation policy.
- Alshamrani §II-A also references Chen et al. [4] for the APT-vs-traditional comparison table (Table I, §II-A, p. 1853) — confirm whether the commodity-vs-APT contrast at [`../sources/LIT_REVIEW.md:123`](../sources/LIT_REVIEW.md#L123) intends to inherit Alshamrani's framing exclusively, or whether Chen's table is a complementary anchor worth surfacing.

## Out of scope for this thesis

- The detailed enumeration of APT groups; the dissertation references named groups (APT29, Lazarus, Volt Typhoon) via ATT&CK G-IDs, not via this paper's catalogue.
