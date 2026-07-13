# Al-Sada 2024 — extraction notes

> B. Al-Sada, A. Sadighian, G. Oligeri. "MITRE ATT&CK: State of the Art and Way Forward." *ACM Computing Surveys*, vol. 57, no. 1, art. 12, October 2024, 37 pp.
> Source file: `docs/sources/2_1_al-sada2024MITRE.md` (gitignored).
> Relevance to this thesis: survey of ATT&CK as a knowledge base / lingua franca for adversary behaviour (lit review §III-A); used to substantiate the four-level hierarchy (tactic / technique / sub-technique / procedure) and the three-matrix structure (Enterprise / Mobile / ICS).

## Bibliographic anchor

- **Citation key**: `al-sada2024`
- **DOI / URL**: 10.1145/3687300
- **Pages cited from**: full text

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### Relevance class

**S — Supporting-argument.** Al-Sada is a survey that establishes the ATT&CK vocabulary the dissertation inherits at L1 (nodes = ATT&CK techniques, per [`../specs/architecture.md`](../specs/architecture.md) §(d)). It anchors the lit review's §III-A descriptive paragraph on the four-level hierarchy and the three-matrix structure, but does not drive a methodological choice — the architecture would adopt the same vocabulary if cited via any other reasonable secondary source. The load-bearing rhetoric is "what ATT&CK is", not a specific Al-Sada claim about how to use it.

### Used in lit review

- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 22 — cited as `[3]` to attribute MITRE ATT&CK's 2013 origin as a behavioural vocabulary parallel to the Pyramid of Pain.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 97 — cited as `[3]` for the framework's origin in MITRE's 2013 Fort Meade Experiment (the four-level-hierarchy paragraph's opening claim; the per-level definitions in that paragraph are then attributed to Rodríguez `[7]`, not Al-Sada).
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 99 — cited as `[3]` for the three-matrix structure (Enterprise / Mobile / ICS) and Enterprise being the most heavily populated.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 101 — cited as `[3]` for the catalogue of named adversary groups, software, and campaigns at technique resolution.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 101 — co-cited as `[3]` (with `[14]` Jalowski) for "ATT&CK has become the *lingua franca* for adversary behaviour" and the comparison to the phase-level Cyber Kill Chain and category-level STRIDE.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 127 — cited as `[3]` for ATT&CK cataloguing attributed APT operations at technique resolution (APT29, Lazarus, Volt Typhoon).

### Four-level hierarchy: tactics, techniques, sub-techniques, procedures

**Source locator:** §2 "Background on MITRE ATT&CK Framework", pp. 12:2–12:3; Fig. 1 (matrix layout, p. 12:3); Table 1 (WannaCry tactics-techniques mapping, p. 12:4).

**Paraphrase:** ATT&CK organises adversary behaviour as a hierarchy: a *tactic* is the short-term objective, a *technique* is the means the adversary adopts to achieve that objective, a *sub-technique* is a more specific variant of a technique, and a *procedure* is a particular implementation. Techniques are grouped into tactics, sub-techniques refine techniques, and procedures populate sub-techniques — e.g., Encrypted Channel (T1573) splits into Symmetric Cryptography (T1573.001) and Asymmetric Cryptography (T1573.002), the latter with 55 catalogued procedures. The matrix layout (Fig. 1) places tactics as columns and techniques as rows, ordered left-to-right by typical attack progression, though Al-Sada is explicit that the matrix does not itself encode the sequence of malicious activities — only the techniques observed.

**Quote (if essential):**
> "an APT achieves its objective by implementing a sequence of malicious activities that can be modelled as a sequence of Tactics, Techniques, and Procedures (TTPs)." (§2, p. 12:3)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(d) L1 GAP (nodes = ATT&CK techniques) · [`../specs/architecture.md`](../specs/architecture.md) §(c) L0 raw CTI (ATT&CK Campaigns input).

**Disposition for this thesis:** *adopted-as-baseline* for the L1 node namespace. The architecture's L1→L4 pipeline takes techniques as the node-level abstraction; sub-techniques and procedures sit below the granularity at which GAP edges are inferred (edges come from Attack Flow's inter-technique dependencies, per [`../specs/architecture.md`](../specs/architecture.md) §(d), not from procedure-level decomposition). Tactics are present as a labelling layer the L2 motivation-subgraphing step can use for terminal-node identification. Al-Sada's own observation that the matrix does not reflect attack sequence is precisely the gap Attack Flow and Ferraz [[ferraz2025]] address — Al-Sada itself notes the gap descriptively but does not propose a fix.

---

### Three matrices and the cataloguing of groups, software, and campaigns

**Source locator:** §2.1 "Technology Domains", pp. 12:3–12:5; §2 second WannaCry passage (S0366 ↔ G0032 Lazarus Group linkage), p. 12:3.

**Paraphrase:** ATT&CK is partitioned into three technology-domain matrices: *Enterprise* (191 techniques, 385 sub-techniques across Windows, Linux, macOS, Cloud, Network, Containers — the only domain to include preparatory-activity tactics such as Reconnaissance and Resource Development), *Mobile* (66 techniques, 41 sub-techniques), and *Industrial Control Systems* (78 techniques, no sub-techniques; captures IT→OT pivots from Spearphishing Attachment through to physical-world impacts like Damage to Property and Loss of Safety). Enterprise is the most heavily populated because of its longer observational legacy and broader platform coverage. Beyond the matrices themselves, each malicious software entry (e.g., `S0366` WannaCry) is linked to the named adversary groups observed deploying it (e.g., `G0032` Lazarus Group), and each technique is cross-linked to suggested mitigations (M-IDs) and detection data sources (DS-IDs).

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(c) L0 raw CTI (ATT&CK Campaigns / ATT&CK group descriptions as inputs) · [`../specs/architecture.md`](../specs/architecture.md) §(e) L2 motivation specifier (drawn from primary motivation categories surfaced across ATT&CK group descriptions).

**Disposition for this thesis:** *adopted-as-baseline* for the Enterprise-matrix scope. The architecture's L0 corpus draws on ATT&CK Campaigns and ATT&CK group descriptions, both of which live in the Enterprise bundle — the choice to centre on Enterprise (not Mobile, not ICS) is consistent with Al-Sada's observation that Enterprise carries the richest legacy of observed campaigns. The G-ID / S-ID / C-ID cataloguing is what makes APT behaviour reconstructable into a reusable adversarial profile rather than a single-incident replay (the argument the lit review attaches to APTs at §III-C, line 127). Mobile and ICS matrices are out of scope for this thesis.

---

## Open questions / things to verify

- Al-Sada reports the Enterprise matrix size as "191 techniques and 385 sub-techniques" (§2.1, p. 12:4) as of the survey's late-2023 / early-2024 writing window. The matrix has since grown — the architecture spec should not pin to those counts, and any reference to "current Enterprise size" in downstream prose needs to source the count from the live ATT&CK release used at extraction time, not from Al-Sada.
- The lit review's "STIX 2.1 records *which* but not *how*" observation (line 103) is attributed to Ferraz `[13]`, not Al-Sada — Al-Sada notes the framework "does not reflect the sequence of malicious activities" (§2, p. 12:3) but does not develop the STIX-serialisation argument at the depth the lit review uses. The Pass-1 stub's "Sections to lift in Pass 2" hint listed STIX as an Al-Sada lift, which appears to be a stub-authoring error; the load-bearing STIX argument lives in [[ferraz2025]]. Worth a quick cross-check when the Ferraz extraction is fleshed in this same batch.

## Out of scope for this thesis

- Detection-engineering / SOC use-cases for ATT&CK.
