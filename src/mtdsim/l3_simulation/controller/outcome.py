"""Load the success/failure outcome-overlay split and compose it (M2).

This module reads the success/failure signal back from the substrate and turns
it into net routing. The loader and the ``compose`` composition rule are both
real; the reconciled numbers are still **provisional** (R2 candidate under
cross-examination — the values, not the mechanism, are gated on Marc's
greenlight):

    docs/handoffs/2026-07-22_l3_controller_success_failure.md
    docs/implementation/pipeline/ogasp/success_failure_overlay_design.md

Data (rule-based notation — see ``data/ogasp/controller/``):
    outcome_rules.json   — the SOURCE OF TRUTH: the model (bands / enables /
        foothold) + the ordered success/failure rules, each carrying its value
        and ONE rationale. Values are rule-generated (first-match-wins).
    success.json / failure.json   — COMPILED VIEWS: the complete directed
        tactic-pair space (210 = 15*14, corpus-agnostic) as
        ``by_source[src][dst] = {"v": value, "rule": rule-id}``. Generated from
        the rules — do NOT hand-edit; regenerate. The rationale for any pair is
        looked up from ``outcome_rules.json`` by its ``rule`` id (stored once per
        rule, never duplicated per pair).

The values are provisional (R2 candidate under cross-examination); finalise once
the numbers are greenlit.

Value semantics (per file ``_meta``):
    overlay_v(src -> dst) in [0, 1] = given the dispatched verb at ``src`` came
    back with verdict ``v``, the conditional likelihood of ``dst`` as the next
    move (0 = will not happen, 1 = the single most likely next course of action).

Composition (M2), implemented in :meth:`OutcomeOverlay.compose`:
    w'(src -> dst) = base(src -> dst) * overlay_v(src -> dst)
                     ------------------------------------------
                     Σ_dst' base(src -> dst') * overlay_v(src -> dst')
    Only within-source ratios are load-bearing; the source out-set renormalises.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

Verdict = str  # "success" | "failure"  (binary outcome only, M2)

_VERDICTS: frozenset[Verdict] = frozenset({"success", "failure"})

# …/src/mtdsim/l3_simulation/controller/outcome.py -> repo root is parents[4].
_DATA_DIR = Path(__file__).resolve().parents[4] / "data" / "ogasp" / "controller"
DEFAULT_FILES: dict[Verdict, Path] = {
    "success": _DATA_DIR / "success.json",
    "failure": _DATA_DIR / "failure.json",
}


@dataclass(frozen=True)
class OutcomeOverlay:
    """The loaded success/failure overlay, indexed ``verdict -> src -> dst -> value``.

    A read-only lookup over the two split files. The runtime composition
    (multiply the base out-weights by these values and renormalise within a
    source's out-set) is deliberately **not** implemented here yet — see
    :meth:`compose`.
    """

    by_verdict: dict[Verdict, dict[str, dict[str, float]]]
    by_rule: dict[Verdict, dict[str, dict[str, str]]]

    def value(self, verdict: Verdict, src: str, dst: str) -> float:
        """The overlay value for one directed pair under one verdict.

        Missing pairs return ``0.0`` — a pair the overlay does not carry is not
        a legal conditioned move under that verdict. (With complete coverage the
        overlay carries every ordered pair, so a miss means an unknown tactic.)
        """
        return self.by_verdict.get(verdict, {}).get(src, {}).get(dst, 0.0)

    def out_values(self, verdict: Verdict, src: str) -> dict[str, float]:
        """All ``dst -> value`` overlay entries for a source under a verdict."""
        return dict(self.by_verdict.get(verdict, {}).get(src, {}))

    def rule_for(self, verdict: Verdict, src: str, dst: str) -> str | None:
        """The id of the rule that generated this pair's value; ``None`` if not
        carried. The rationale lives once in ``outcome_rules.json`` under this id
        — never duplicated per pair."""
        return self.by_rule.get(verdict, {}).get(src, {}).get(dst)

    def compose(
        self,
        src: str,
        verdict: Verdict,
        base_out_weights: dict[str, float],
    ) -> dict[str, float]:
        """Condition the base out-distribution on the verdict and renormalise (M2).

        The rule (``success_failure_overlay_design.md`` §1)::

            w'(src->dst) = base(src->dst) * overlay_v(src->dst) / Σ

        Per destination ``dst`` in ``base_out_weights`` the factor is the overlay
        value for ``(src, dst)`` under this verdict **if that pair is present** in
        the overlay's ``by_source[src]``, **else 1.0** — an absent pair is an
        *unconditioned passthrough* (it keeps its base weight), while a pair
        carried with value ``0`` **hard-suppresses** the edge. This absent-vs-
        present-zero distinction is what makes the composition robust to any
        net/overlay pairing (plug-and-play): the complete-coverage overlay carries
        every ordered tactic pair, but a base net edge the overlay does not name
        (e.g. a self-loop) still routes rather than silently vanishing.

        The source out-set renormalises, so only within-source ratios are
        load-bearing (base proportions are conditioned, never re-derived —
        ``metrics_semantics.md`` §(f)). Returns an empty dict — the **stall**
        (design §3) — if the verdict suppressed every out-edge (Σ == 0); the
        movement driver reads that as walk-termination. With the current numbers
        no verdict zeroes an out-set, so the stall is a guarded edge case, not a
        routine outcome.
        """
        src_overlay = self.by_verdict.get(verdict, {}).get(src, {})
        composed: dict[str, float] = {}
        for dst, base_w in base_out_weights.items():
            factor = src_overlay[dst] if dst in src_overlay else 1.0
            weight = base_w * factor
            if weight > 0:
                composed[dst] = weight
        total = sum(composed.values())
        if total <= 0:
            return {}
        return {dst: weight / total for dst, weight in composed.items()}


def load_outcome_overlay(
    files: dict[Verdict, Path] | None = None,
) -> OutcomeOverlay:
    """Load the success/failure split files into an :class:`OutcomeOverlay`.

    Validation is loud: each file's declared ``verdict`` must match its slot and
    be one of the two binary verdicts, and the ``by_source`` block is required.
    """
    paths = files if files is not None else DEFAULT_FILES
    by_verdict: dict[Verdict, dict[str, dict[str, float]]] = {}
    by_rule: dict[Verdict, dict[str, dict[str, str]]] = {}
    for verdict, path in paths.items():
        if verdict not in _VERDICTS:
            raise ValueError(
                f"unknown verdict {verdict!r}; expected one of {sorted(_VERDICTS)}"
            )
        with Path(path).open(encoding="utf-8") as fh:
            doc = json.load(fh)
        declared = doc.get("verdict")
        if declared != verdict:
            raise ValueError(
                f"{path}: declared verdict {declared!r} != expected {verdict!r}"
            )
        by_source = doc.get("by_source")
        if not isinstance(by_source, dict):
            raise ValueError(f"{path}: missing or malformed 'by_source' block")
        # Compiled-view cell is ``{"v": value, "rule": rule-id}`` (rule-based
        # notation). Tolerate a bare number too, for forward/backward flexibility.
        def _v(cell: object) -> float:
            return float(cell["v"] if isinstance(cell, dict) else cell)

        def _r(cell: object) -> str:
            return str(cell.get("rule", "")) if isinstance(cell, dict) else ""

        by_verdict[verdict] = {
            src: {dst: _v(cell) for dst, cell in dsts.items()}
            for src, dsts in by_source.items()
        }
        by_rule[verdict] = {
            src: {dst: _r(cell) for dst, cell in dsts.items()}
            for src, dsts in by_source.items()
        }
    return OutcomeOverlay(by_verdict=by_verdict, by_rule=by_rule)
