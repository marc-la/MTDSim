# Additive integration — wrap, never modify; the inherited path stays bit-identical

**Span:** 2026-04-22 → standing. **Prompts:** #2, #39; echoed throughout.

The principle predates almost everything else in the repo. The April demo plan
(#2, 2026-04-22) specified a `SubgraphAttackerProfile` that **wraps** the
inherited `AttackerProfile` rather than inheriting from it, behind a profile-type
flag, with an acceptance test that the legacy path produce **byte-identical**
attack-stats output — "if a run with `AttackerProfile.default()` produces
different output than `main`, the integration is wrong". Explicit April
non-goals: no DDQN retraining, no MTD-interruption changes, no Caldera, no new
defender observations.

**What it became.** The same commitment, matured: the golden-oracle baseline
(`baseline/golden/`), the substrate seam (movement layer added *beside* the
six-phase attacker, both kept internally consistent —
[`../../architecture.md`](../../architecture.md)), bit-identical ablation arms as
the standard for every modulator, and the note arguing the build-beside choice
([`../../../notes/ch4_methods/inherited_attacker_flowchart_vs_machine.md`](../../../notes/ch4_methods/inherited_attacker_flowchart_vs_machine.md)).
The April non-goals held with remarkable fidelity: the DDQN was never retrained
(V3, 2026-08-11 — used as-is), the interruption model was inherited not
reinvented, Caldera stayed rejected (#16).

**Negative space.** Nothing on this thread was reversed — which is itself the
finding: it is the longest-held design commitment in the corpus, made under
demo-day pressure and never relitigated. The one descendant decision: `main`
was rebuilt (2026-07-27, #39) as a standalone, cleaned MTDSim for an incoming
student — the deliberate dev/main divergence — so the "legacy path" now has two
custodians.
