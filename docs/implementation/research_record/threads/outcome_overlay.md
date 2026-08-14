# The outcome overlay — directionality without a kill-chain, and weights that must not be fitted

**Span:** 2026-07-21 → 2026-07-28 (sensitivity study). **Prompts:** #27, #28,
#30, #34, #44. Landed:
[`../../pipeline/ogasp/success_failure_overlay_design.md`](../../pipeline/ogasp/success_failure_overlay_design.md),
[`../../pipeline/ogasp/weight_sensitivity_study.md`](../../pipeline/ogasp/weight_sensitivity_study.md);
distilled for the dissertation in
[`../../../notes/ch4_methods/outcome_overlay_directionality.md`](../../../notes/ch4_methods/outcome_overlay_directionality.md).

**Genesis (#27, 2026-07-21).** Two dictionaries — SUCCESS and FAILURE — over
tactic pairs, multiplied onto the corpus weights at runtime on the substrate's
verdict. The stated point of the design was what it *removed*: an explicit
kill-chain layering had been on the table, and the binary pairing "eliminates
the need for a CKC ordering, because the ordering is implicit in the two sets".
Progression under success and regression under failure emerge from the weights
rather than being imposed as a stage machine — which keeps faith with MITRE's
own no-prescribed-ordering philosophy while still giving the attacker
direction.

**The epistemics (#28), which the design records understate.** Two arguments
rode with the genesis. First, survivorship: "We know a lot about successful
patterns as that's what the campaigns/incident reports tell us, but not a lot
about the failure components" — the overlay's failure half *cannot* be
corpus-derived even in principle, so it is declared knowledge by necessity, not
by laziness. Second, the anti-fitting rule: "This shouldn't be
reverse-engineering the petri nets to produce the mathematically correct set of
weights so that the attacker will move in the right direction … This is
knowledge and real world data working together at runtime to produce a result
that I am here to measure." The overlay is deliberately a *separate* layer from
the CTI-derived nets so that fitting one to the other is a visible violation,
not a tuning knob.

**The verification (#34, 2026-07-23).** With no empirical ground truth
available, the weights were defended by adversarial review instead: a fleet of
independent red-team subagents stress-testing the two dictionaries — including
one bot whose sole job was to detect scope-creep toward reverse-engineering —
iterated "to 95 % confidence". #44 then demanded the distance intuition the
sensitivity study encoded: a persistent attacker does not fall from exfiltration
back to reconnaissance, and recon→impact "should be 0, it defies the sequencing
… of CKC and other papers' APT attack models" — the literature (CKC, Alshamrani
lifecycle) used as a *constraint consensus* on declared values, not as a stage
machine.

**Abandoned on this thread:** the CKC-layer mechanism itself (#27 — dropped
before build); a blanket ban on all forward jumps (#28 — "too rigid" — replaced
by distance-damped weights).
