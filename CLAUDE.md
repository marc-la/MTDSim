# CLAUDE.md

Durable context for this repo. **Task-specific scope and step lists live in the prompt I paste per session** — this file is the always-true background and the rules that hold across every session. Phase-specific constraints from a task prompt (e.g. "audit only, don't change code") refine but never relax anything here.

## Project
- Repo: a fork of **MTDShield** (`main`), a discrete-event simulator for evaluating Moving Target Defence (MTD).
- Owner: Marc Labouchardiere — UWA honours (CSSE), supervised by Dr Jin Hong. Project: *Adaptive MTD for dynamic networks*.
- Goal: a more capable adversary module grounded in CTI / MITRE ATT&CK.

## Codebase lineage (so cross-paper overlap reads as evolution, not contradiction)
Brown 2023 (foundational MTDSim) → Zhang 2023 (MTDSimTime: time domain, MTTC, MTD execution schemes, adversary profiles) → Ho 2024 (metrics suite + RL) → Tay 2024 (MTDShield: reactive RL plugin). Brown is the reference implementation; the rest are systematic updates to it.

## Always-on guardrails
- **Git:** work on a dedicated branch; never commit to `main`; commit locally for my review; **never push** without asking; never run destructive git (`reset --hard`, `clean -fd`, force-push).
- **Scope:** stay inside the task's defined scope. *Flag* out-of-scope findings — don't action them. Prefer small, reviewable, line-level diffs over wholesale rewrites; ask before expanding scope or restructuring.
- **Do not merge `feat/replay-viz`** into baseline/spec work — its fixes are deliberate later cherry-picks.

## Working standards
- **Papers are claims to reconcile with the code, not ground truth about it.** When a paper and the code disagree, record both; correct neither.
- **Never guess** a disposition or a locator. If you can't verify it, mark `unverified` / `verify` and state why.
- Don't assert that a paper is wrong (or that one paper contradicts another) — flag it "to verify" for me to resolve.
- When working across multiple papers, extract **one paper per pass** before merging, to prevent cross-attribution.
- Keep **inherited artefacts** distinct from **my own editorial choices**; track them separately.

## Repo conventions
- `docs/sources/` — source papers + my lit review. **Gitignored** (copyright); read from here, never commit them.
- `docs/spec/MTDSIM_SPEC.md` — the conformance spec; verify-and-extend, provisional until dispositioned against the baseline.
- `docs/spec/_notes_*.md` — per-paper extraction notes.
- `baseline/BASELINE.md` + `baseline/golden/` — the running baseline and its seeded golden outputs (the behavioural oracle for faithfulness).
- Australian English throughout.

## Environment
- Conda env `mtdsimtime` from `environment.yml` (`conda activate mtdsimtime`); originally Python 3.9.13. Fallback: venv + `python setup.py install` + `requirements.txt`. **Record any deviation needed to build — it's a Phase-0 finding, not a silent fix.**