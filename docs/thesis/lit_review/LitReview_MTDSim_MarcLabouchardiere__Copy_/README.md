# Literature Review — Adaptive MTD for Dynamic Networks

**Author:** Marc Labouchardiere (23857377)
**Supervisor:** Dr Jin B. Hong
**Unit:** CITS4010 (24-point honours)
**Deadline:** 22 May 2026

## What this is

Working draft of the CITS4010 literature review. Submission is iterative per Jin's W9 steer — sections sent for review as they're written, full assembly EOD ~17/18 May, final submission Fri 22 May.

## Structure

```
literature_review/
├── main.tex                      # Top-level: class, packages, \input calls
├── references.bib                # Locked bibliography (19 A*/A entries)
├── README.md                     # This file
└── sections/
    ├── 01_mtd.tex                # §1 Moving Target Defense
    ├── 02_threat_landscape.tex   # §2 Threat Landscape & Adversary Behaviour
    ├── 03_convergence.tex        # §3 Attack Modelling in MTD Evaluation
    ├── 04_gap.tex                # §4 Research Gap & Approach
    └── ai_use_statement.tex      # AI use disclosure (post-bibliography)
```

## Section status (live)

| Section | Words target | Drafted | Sent to Jin |
|---|---|---|---|
| §1.1 MTD Concept & Taxonomy | 350–400 | — | — |
| §1.2 MTD Evaluation Paradigms | 400–450 | — | — |
| §1.3 MTD Orchestration & Adaptive Selection | 450–550 | — | — |
| §2.1 MITRE ATT&CK | 280–320 | — | — |
| §2.2 Pyramid of Pain | 250–300 | — | — |
| §2.3 APTs | 280–320 | — | — |
| §2.4 CTI-derived Attack Profiling | 400–460 | — | — |
| §3.1 Attacker Models in MTD Literature | 500–600 | — | — |
| §3.2 Pyramid of Pain Lens on MTD | 400–500 | — | — |
| §3.3 Adaptive / Behaviour-aware MTD | 500–600 | — | — |
| §4 Research Gap & Approach | 500–700 | — | — |
| **Total (excl. refs and AI statement)** | **4,910–5,800** | — | — |

Spec: 5,000–6,000 words excl. references and AI-use statement; 10–20 references; IEEE referencing style. 10% penalty band starts at 6,600 words.

## Reading guide for Jin

- **Comments are turned on.** Inline comments preferred over track-changes for prose feedback.
- **Section files are independent.** Open `sections/0X_section.tex` directly to read/comment a single section without scrolling main.tex.
- **TODO comments in section files** show what each subsection is meant to argue and which references support it. They will be removed before final submission.
- **Reference tracker** in `references.bib` is comment-tagged by section (`% §1.1, §1.3` etc.) so it's easy to see which references serve which arguments.

## Compilation

Standard pdfLaTeX → BibTeX → pdfLaTeX → pdfLaTeX. Overleaf default settings should work.
