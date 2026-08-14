# Axis 8 — the smart-APT vision, the Tay retrain ambition, and the kill on calibration circularity

**Span:** 2026-08-05 → 2026-08-11 (killed). **Prompts:** #68, #70–#76, #77, #94,
#104. The exclusion is recorded
([`../../apt_model_criterion.md`](../../apt_model_criterion.md) axis 8; register
V3); the *vision that was killed* is recorded nowhere but here.

**The rise.** Over 2026-08-05/06 a unifying design formed — the most ambitious
in the corpus. Vulnerability memory plus "swift mode" (a knowledge-rich attacker
blitzing a network it has already mapped, #68, #71); detectability used as a
loss function ("the attacker … intuitively knows what actions will likely be
picked up … so times its verbs smartly to maximise likelihood of progress in
the progress/effort calculus", #70); and side-channel MTD awareness — the
attacker deduces the MTD-AI's decision boundaries from the network metrics it
moves, acts *below* the no-op threshold, and strikes "before its information
set is invalidated" (#72, #76). One mechanism was to span axes 5, 6, 7 and 8 at
once — "well integrated and covered a cross section of the axes" (#70).

**The dependency that broke it.** The vision needed an event-based,
metrics-driven defence to side-channel, and the only one is Tay's MTD-AI. #73–#74
record the reintegration attempt: the archived weights doubted ("trained
improperly … non-standard hyperparameters", trained locally rather than on
Kaya), the reward function hunted through the paper, a Kaya retrain offered —
gated on "95 % confident that this model does what Tay said". The 11-Aug meeting
closed the gate: **do not retrain, use the model as-is** (V3, third-party ruling
paraphrased). Without a trustworthy reactive defence there is nothing for
scheme-awareness to exploit.

**The kill, in Marc's own words (#77, 2026-08-09; #94).** "I am killing axis 8
on the grounds of no event-based MTD mechanisms to exploit" — and the reason a
substitute trigger was refused is the thread's best sentence: "Any simple
event-based MTD orchestration added to MTDSim would involve calibration, which
**effectively defeats the purpose of the exercise**." Building the defence
yourself and then side-channelling it is circular; the axis dies rather than be
demonstrated against a strawman. Axes 4 and 8 are thereafter "recorded
failures … pushed into future work" (#94). #104 (2026-08-13) probes the last
crack — could the current attacker exploit knowledge of mutation timing at
all — and feeds the pivot-kernel design the criterion records as declined with
a named reopening condition (a genuinely reactive defender).

**What survives:** vulnerability memory (as the axis-7 exploit-learning
mechanism, reframed from evasion to learning); the detectability reader (axis 5,
shipped as a measurement); the reactive-defender evaluation as the named
successor programme
([`../../../notes/ch7_future_work/successor_programme.md`](../../../notes/ch7_future_work/successor_programme.md)).
