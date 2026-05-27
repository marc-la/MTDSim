# Bland 2020 — extraction notes

> J. A. Bland, M. D. Petty, T. S. Whitaker, K. P. Maxwell, W. A. Cantrell. "Machine Learning Cyberattack and Defense Strategies." *Computers & Security*, vol. 92, art. 101738, 2020.
> Source file: `docs/sources/4_bland2020machine.md` (gitignored).
> Relevance to this thesis: cross-cutting reference for §V — a relatively early example of *attacker-side* ML, the kind of asymmetry-reversing modelling that Cho et al.'s critique calls for and that MTD evaluation seldom adopts.

## Bibliographic anchor

- **Citation key**: `bland2020`
- **DOI / URL**: 10.1016/j.cose.2020.101738
- **Pages cited from**: full text

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### TODO — Pass 2

(awaiting Pass-2 deep extraction)

Sections to lift in Pass 2:
- The ML-attacker formulation — what learning signal, what action space.
- The defender-side counterpart (the paper proposes both) — and whether the joint game asymmetry is genuinely balanced.
- The simulation environment used — relate to MTDSim's substrate.

---

## Open questions / things to verify

- Whether this paper's "learning attacker" rises to the **behavioural** rung of the fidelity descriptor (Table II) or remains at procedural.
- Confirm placement in §V — Marc may use this as a supporting reference rather than a placement on Table II.

## Out of scope for this thesis

- The defender-side ML details, unless they illuminate the attacker's learning regime.
