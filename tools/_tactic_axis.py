"""The shared tactic axis — read from the pinned ATT&CK bundle, not typed.

`figure_table_conventions.md` §b6 makes the tactic order a cross-figure
contract: tactics are never reordered between figures. That contract is only
worth as much as its single source, so this module derives the axis from the
bundle under `data/gap/` rather than restating it:

* **order** — the Enterprise matrix's own `tactic_refs` sequence, which is the
  reading order `fig:l1-graph` uses (it agrees row-for-row with the GAP's
  `tactic_layer`, checked at build time by `check_against`);
* **labels** — the bundle's tactic names, down-cased to the sentence case the
  figure family sets. US spelling inside an ATT&CK proper name is therefore
  *looked up, not translated* — the 2026-08-20 Australianisation ruling
  (`figure_table_conventions.md` §i);
* **version** — the collection object's `x_mitre_version`, for the §b5 pin
  every derived float states in its caption.

Two orders are legal, and a figure declares which it takes. `matrix_order` is
the raw ATT&CK reading order (`fig:l1-graph`). `stage_grouped_order` sorts by
consensus lifecycle stage first, keeping the matrix order inside a stage
(`fig:failure-weight-matrix`, and any figure that draws stage bands); the two
differ only in that stage grouping lifts command and control above collection.

Not wired into the two generators that predate it — they carry their own copies
of the label map. Rewiring them would regenerate shipped figures for no visual
change, so it is left as a follow-up; this module is the single source for
anything built after it.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUNDLE = REPO / "data" / "gap" / "_attack" / "enterprise-attack-19.1.json"
LIFECYCLE = REPO / "data" / "ogasp" / "controller" / "lifecycle_consensus.json"

# Words that stay capitalised when a Title Case ATT&CK name is folded to the
# sentence case the figures set. Empty today — no v19.1 tactic name contains a
# proper noun — and present so that a future bundle carrying one ("Active
# Directory") is a one-line fix rather than a silent mis-case.
KEEP_CAPITALISED: frozenset[str] = frozenset()


def _sentence_case(name: str) -> str:
    """"Command and Control" -> "Command and control". First word keeps its
    capital; the rest lower unless listed in KEEP_CAPITALISED."""
    head, *rest = name.split(" ")
    return " ".join([head] + [w if w in KEEP_CAPITALISED else w.lower() for w in rest])


class TacticAxis:
    """The pinned tactic set: order, display names, and the version pin."""

    def __init__(self, order: list[str], label: dict[str, str], version: str):
        self.matrix_order = order          # ATT&CK reading order
        self.label = label                 # shortname -> sentence-case name
        self.version = version             # e.g. "19.1", for the §b5 caption pin

    def __len__(self) -> int:
        return len(self.matrix_order)

    def stage_grouped_order(self, stage_of: dict[str, int]) -> list[str]:
        """Consensus stage first, matrix order within a stage.

        The same rule `failure_weight_decomposition_figure.stage_grouped_order`
        applies, so the two figures' axes agree: the four stage blocks become
        visible and within-block order still asserts nothing, which is what the
        consensus wants — it declares the post-intrusion middle unordered.
        """
        return sorted(
            self.matrix_order,
            key=lambda t: (stage_of[t], self.matrix_order.index(t)),
        )

    def check_against(self, order: list[str]) -> None:
        """Fail loudly if another artefact's tactic set has drifted from the pin.

        The axis is a contract; a mismatch means a figure would be drawn against
        a tactic set the bundle does not carry, which is exactly the silent
        failure the single-source rule exists to prevent."""
        if list(order) != self.matrix_order:
            raise SystemExit(
                "tactic axis mismatch against the pinned bundle:\n"
                f"  bundle: {self.matrix_order}\n"
                f"  other:  {list(order)}"
            )


def load_axis(bundle: Path = BUNDLE) -> TacticAxis:
    """Read order, labels and version from the pinned ATT&CK bundle."""
    doc = json.loads(bundle.read_text())
    objects = doc["objects"]

    by_id = {o["id"]: o for o in objects if o.get("type") == "x-mitre-tactic"}
    matrices = [o for o in objects if o.get("type") == "x-mitre-matrix"]
    if len(matrices) != 1:
        raise SystemExit(f"{bundle.name}: expected exactly one matrix, found {len(matrices)}")

    order, label = [], {}
    for ref in matrices[0]["tactic_refs"]:
        tactic = by_id[ref]
        shortname = tactic["x_mitre_shortname"]
        order.append(shortname)
        label[shortname] = _sentence_case(tactic["name"])

    collections = [o for o in objects if o.get("type") == "x-mitre-collection"]
    if not collections:
        raise SystemExit(f"{bundle.name}: no collection object, so no version to pin")
    return TacticAxis(order, label, str(collections[0]["x_mitre_version"]))


def load_stages(path: Path = LIFECYCLE) -> tuple[dict[str, int], dict[int, str]]:
    """The lifecycle-consensus staging: `tactic -> stage`, and `stage -> name`.

    Stage names are shortened to the form the figure family prints — the
    consensus spells stage 2 "post-intrusion operations", which is a caption
    phrase, not a band label.
    """
    doc = json.loads(path.read_text())
    stage_of = dict(doc["stage_of"])
    stage_name = {int(k): v.split(" (")[0] for k, v in doc["stages"].items()}
    stage_name = {k: ("post-intrusion" if v.startswith("post-intrusion") else v)
                  for k, v in stage_name.items()}
    return stage_of, stage_name
