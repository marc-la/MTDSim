---
status: parked-reference (pick up during the dissertation write-up, after first numbers)
created: 2026-07-23
topic: "Drafting brief — the dissertation section that DEFENDS the outcome-overlay's declared-value methodology. Defines the full-marks dimensions, the argument spine, where every piece of evidence lives in the codebase, the figures/examples needed, and the examiner challenges + answers. Written so a cold-start session can pull it all together and draft the section."
---

# Brief: drafting the declared-value / outcome-overlay **defence** section

The L3 success/failure outcome overlay finished its adversarial scrutiny at **certified
82% confidence**, and every review round agreed the **82 → 95% remainder is not value
uncertainty — it is the written defence of the reasoning** (the dissertation making the
case an examiner accepts). This brief is the specification for that section: what it must
accomplish for full marks, and the map to pull the evidence together. It is deliberately
parked here, not on the forward chain — revive it during write-up.

Its subject is a hard problem the dissertation must own head-on: **a load-bearing set of
numbers that is declared, not measured.** Handled well, that is a methodological
contribution; handled by apology, it bleeds marks. This section is where it is handled well.

---

## 0. PREREQUISITE (do this first, or the section cannot make its central claim)

The section's strongest argument is **reproducibility** — "the values are rule-generated
and a deterministic generator reproduces the table 0/123 before any edit." But **the
generator, the composed-net validator, the stepping harness, and the routing/evidence
artefacts currently live only in the session scratchpad and are volatile — they will not
exist when the section is written.** Before drafting, **persist them into the repo** so the
claim is citable and re-runnable by an examiner:

- the rule generator (reproduces the table; `--mode fold-r2`),
- the composed-net validator (routed mass on `build_all_profiles(with_synthetic_overlay=True)`),
- the stepping harness (walks the real nets, MTDSim verdict stubbed),
- the routing digest / evidence pack / a representative trace set.

A natural home is a `tools/` or `src/mtdsim/l3_simulation/petri/` module + a committed
`data/ogasp/controller/_evidence/` directory, each with a one-line provenance to
[`../../implementation/declared_value_provenance.md`](../../implementation/declared_value_provenance.md).
**Without this, the reproducibility pillar is an unbacked assertion.** This is the single
highest-leverage prerequisite.

---

## 1. What the section is, and where it lands

It is a **methodology-defence**, not a results section. It argues that a declared-plausibility
policy layer is a legitimate, rigorous research object whose specific magnitudes, though
CTI-unvalidated by construction, are **defensible** — and it converts that into marks by
being explicit, evidenced, illustrated, and critically self-aware.

It is not one block of prose; it threads three chapters (write once, cross-reference):
- **ch4_methods** — the model and the declared-knowledge stance (why declared, the three
  factors, the composition contract). The *what and why*.
- **ch6_results** — the validation-by-scrutiny methodology and its outputs (the CTI-
  independence proof, the composed-net validation, the stepwise simulation, the confidence
  trajectory). The *how we know it holds*.
- **ch7_discussion** — the honest limitations, the inherent ceiling, and the methodological
  contribution. The *what it costs and what it gives*.

The through-line question the section must answer for the examiner: **"why should I believe
these numbers?"** — answered not with "they were measured" (they weren't) but with a chain
of *reproducibility + evidence-tiering + adversarial survival + honest limits*.

---

## 2. The full-marks dimensions (the rubric to write against)

A distinction-grade methodology defence hits all of these. Treat each as a subsection or a
paragraph the section must contain; a missing dimension is where marks leak.

1. **Epistemic framing done positively.** Name the object — a *declared-plausibility
   envelope, not a recovered actor* — and defend the stance as a deliberate methodological
   choice, before any number. The failure mode is defensiveness ("we couldn't get data,
   so…"); the full-marks move is to argue the envelope is the *correct* object for the
   research question and that treating it as declared is more honest than a false-precision fit.
2. **Non-circularity / independence, proven not asserted.** Show the overlay never
   reverse-engineers the CTI layer it conditions: `make_rules` reads only bands/enables/
   foothold; the base is *failure-blind* (so the failure side cannot be circular by
   construction — the decisive structural fact); the enables set is provably not a
   subset/superset/threshold of the base flow graph.
3. **Reproducibility.** The values follow from a small model, not per-pair hand-setting;
   a generator reproduces them deterministically (0/123 before edits). Requires §0.
4. **Evidence-tiering, stated not hidden.** Every value carries a tier (`attested-pattern`
   vs `declared-judgement`); the success/failure asymmetry is presented as a *finding* about
   what incident reports do and don't record, not a weakness.
5. **Construct validity.** The numbers produce *plausible behaviour* on the real deployment
   surface: the composed-net validation (routing lands where the semantics say) and the
   stepwise simulation (per-step option-sets an operator would choose) are the evidence.
6. **Validation-by-adversarial-scrutiny as method.** Present the multi-round cross-examination
   (fan-out review → adversarial refute → generalising fold → re-scrutinise → confidence
   panel) as a *reproducible validation protocol* for declared values — this is the section's
   originality claim, and it must be framed as a contribution, with its convergence (final
   finetune synthesis = zero changes) as evidence the process terminated, not stopped.
7. **Critical self-awareness / threats to validity.** State the caveats and the inherent
   ceiling plainly (see §7). Examiners reward the candidate who raises the objection first.
8. **Literature positioning.** Locate the approach among how the field handles unvalidated
   parameters: expert elicitation, envelope/interval methods, sensitivity analysis,
   plausibility modelling. This is currently the **thinnest** part of the evidence base and
   needs sourcing work — flag it.
9. **Evidence made visible.** Figures and worked examples throughout (see §5). The prior
   lit-review lost marks specifically for *missing images/examples* — do not repeat it.
10. **Voice.** The prose must clear [`../../workflows/voice.md`](../../workflows/voice.md).
    The same lit-review lost marks for *AI-flattened voice*; this section, of all sections,
    must read as authored argument, not generated summary.

---

## 3. The argument spine (the logical order that convinces)

Draft to this skeleton; each step discharges the one before:

1. *The research needs a policy layer* — structure (the nets) gives legal moves; something
   must say which move fires on which verdict. (Sets up necessity.)
2. *Measuring it is impossible and undesirable here* — no corpus records post-failure
   behaviour; a fitted value would be false precision. So it is **declared**. (Justifies the stance.)
3. *Declared need not mean arbitrary* — it is generated from a stated model (bands + enables
   + foothold) by fixed rules, reproducibly. (Reproducibility.)
4. *And it is independent* — it conditions the CTI base, never re-derives it; the base is
   failure-blind. (Non-circularity.)
5. *And it is honestly tiered* — attested-pattern vs declared-judgement, labelled. (Evidence tiers.)
6. *And it behaves plausibly* — composed-net routing + stepped traces confirm the numbers move
   the token the way the semantics claim. (Construct validity.)
7. *And it survived adversarial attack* — N rounds, ~90 independent critics, converging to
   zero further changes. (Validation-by-scrutiny.)
8. *Here is exactly what it cannot claim* — CTI-unvalidated magnitudes; only within-source
   ratios; the named caveats. (Limits.)
9. *Therefore* — the values are defensible as a plausibility envelope, and the scrutiny
   protocol is a reusable contribution. (The claim the examiner accepts.)

---

## 4. Evidence inventory — where every piece lives (the pull-together map)

A cold session drafts from these. All paths repo-relative.

| Claim to support | Artefact |
|---|---|
| The model + rules + per-rule provenance ledger | `data/ogasp/controller/outcome_rules.json` (rules, tiers, changelog, scrutiny) |
| The complete 210-pair values | `data/ogasp/controller/{success,failure}.json` (compiled views) |
| The design rationale, R2 ladder, caveats | `docs/implementation/pipeline/ogasp/success_failure_overlay_design.md` §1–§2.5 |
| The provenance/scrutiny **precedent** (the method, generalised) | `docs/implementation/declared_value_provenance.md` |
| Non-circularity anchor (base is failure-blind, "conditions not re-derives") | `docs/implementation/metrics_semantics.md` §(f); design §1 (rejects "solving the nets") |
| The decisions (M2/M3, C2-hub kept, enabled-flat, finalisation) | `docs/implementation/pipeline/ogasp/supervisor_decision_register.md` |
| Reproducibility, composed-net validation, stepwise traces | the persisted tooling from §0 (**must be relocated first**) |
| The scrutiny narrative (rounds, findings, convergence, confidence 82%) | distilled in design §2.5 + the ledger `ledger_meta.review_history`; **the raw workflow transcripts are volatile — cite the distilled records, not the transcripts** |
| Substrate/verdict/interrupt mechanics the overlay keys on | `src/mtdsim/l3_simulation/controller/{outcome.py,verdict.py}`; `controller.md` §4 |

**Caution for the drafter:** the workflow agent transcripts under
`…/subagents/workflows/` are session-volatile and were never meant to be cited directly.
The durable record of the scrutiny is the design doc §2.5 and the ledger. If a specific
figure is wanted (e.g. the recon-bridge 50→83% shift), regenerate it from the persisted
tooling (§0), do not quote a transcript.

---

## 5. Figures and worked examples the section must carry

Marks were lost before for their absence. Each of these earns its place:

- **The rule ladder** — success/failure values as a compact decision tree (enabled → 1.0;
  forward/lateral/backward; the gates + dampers). Makes "rule-generated" visible at a glance.
- **A composed routing distribution, before/after a fix** — e.g. `initial-access` on failure:
  the recon-bridge share moving **50% → 83%** when `ia_gate` goes 0.1 → 0.02. The single most
  persuasive "diagnosis → semantic re-reading → validation" illustration.
- **A stepped trace** — one attacker walk through a real net with the stubbed verdicts and the
  per-step option-set, annotated with which rule fired. Shows the policy *behaving*.
- **The scrutiny funnel** — rounds × agents → findings raised → survived refutation → folded,
  ending at "zero changes." Evidences convergence, not just effort.
- **The evidence-tier map** — which rules are attested-pattern vs declared-judgement, over the
  15×15 grid. Makes the honesty structural, not rhetorical.
- **A worked pair** — carry `command-and-control → execution` or `lateral-movement →
  credential-access` end to end (semantics → rule → value → composed routing), so the reader
  sees one number fully justified.

Keep to the diagnostic-viz house style (no accentuation/arrows on evidence figures — let the
cells/bars speak); reserve emphasis for genuinely dissertation-facing figures.

---

## 6. The gates the prose must clear

- **Voice contract** — [`../../workflows/voice.md`](../../workflows/voice.md), loaded in full
  before drafting. This section is the highest-risk place for AI-flattening because it is
  argument-dense; write it as a defence *you* would mount in a viva.
- **Notes rubric** — [`../../workflows/notes_rubric.md`](../../workflows/notes_rubric.md) if any
  part lands as a `docs/notes/` note en route to the chapters.
- **AI-use declaration** — the scrutiny was AI-run; the AI-Use Declaration must describe it
  accurately (the adversarial cross-examination is part of the method and should be disclosed
  as such, framed as a tool the candidate directed and owns).

---

## 7. Examiner challenges — anticipate and pre-answer

The section should surface these before the viva does. Prepared answers exist in the artefacts:

- **"Why *this* magnitude and not a neighbouring one?"** — the honest, winning answer: only
  *within-source ratios* are claimed (the composition renormalises); the magnitudes are a
  declared soft ordering, and the ratios are what were scrutinised. Do not overclaim point precision.
- **"Isn't this circular with your CTI data?"** — no: `make_rules` never reads the base; the
  base is failure-blind; the enables set is provably not derived from the base graph.
- **"Isn't AI-run scrutiny just the model agreeing with itself?"** — address directly:
  independent adversarial lenses *tasked to refute*, findings only counted after survival,
  every claim re-run against routed mass/traces (evidence, not opinion), and the process
  changed real values (the R2 folds) before converging. Frame it as structured disagreement,
  and state its limits.
- **"Your confidence is 82%, not higher — why ship it?"** — because the residual is defence,
  not defect: the finetune synthesis returned zero changes; what remains is exactly this
  written argument. Say so.
- **"How would this generalise / is it reusable?"** — point to the precedent doc: the ledger +
  the scrutiny protocol are the transferable contribution, not just this one overlay.

---

## 8. What separates full marks from a pass

- **Pass:** describes the overlay, lists the values, admits they are declared, notes it was reviewed.
- **Full marks:** *argues* the declared stance is correct for the question; *proves* non-circularity
  and reproducibility with re-runnable artefacts; *shows* plausible behaviour with figures and a
  worked trace; *frames* the adversarial scrutiny as a validation contribution with evidence of
  convergence; *raises the examiner's objections first* and answers them; and reads in an authored
  voice throughout. The difference is almost entirely: **evidence made visible + objections owned +
  contribution claimed**, not more numbers.

---

## Connections

- The finalised artefacts and their scrutiny: `success_failure_overlay_design.md` §2.5,
  `declared_value_provenance.md`, `outcome_rules.json` (`ledger_meta`).
- Decisions: `supervisor_decision_register.md` (M2/M3 + the 2026-07-23 finalisation resolution).
- Sequencing: draft **after** first numbers ([`../2026-07-15_l3_first_numbers.md`](../2026-07-15_l3_first_numbers.md)),
  so the evaluation chapter can weave the overlay's behaviour into the actual results, and
  **after** the §0 tooling is persisted.
