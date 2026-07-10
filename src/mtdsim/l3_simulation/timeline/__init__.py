"""L3b — the standalone timeline runner (D2's v1 execution model).

A seeded single-token walk over the committed weighted tactic-place nets
(``data/ogasp/petri/<profile>_structural.json``) with per-state dwell from the
v0 duration catalogue (``data/ogasp/tactic_durations.json``): the net runs
**independently** of the simulator, and the output is a library of timed
attacker-state sequences (cumulative timelines) that the replay attacker
later feeds into MTDSim. Also delivers D1's standalone-examination half —
the behavioural verification report over the timeline library.

Contract artefacts (committed): ``data/ogasp/timeline/timeline_schema.md``
(the ``ogasp-timeline/v1`` record schema the replay attacker pins to),
``timeline_example.jsonl``, ``timeline_report.md``/``.json``. Bulk timelines
live under the gitignored ``data/ogasp/timeline/_timelines/`` and the
awareness figures under ``data/ogasp/timeline/_viz/`` (both regenerable).
Entry point: ``PYTHONPATH=src python -m mtdsim.l3_simulation.timeline``.

The runner never imports ``mtdnetwork`` (D2: independent execution) and
never fires a transition absent from the committed nets (no-synthesis,
tested in ``tests/l3_simulation/test_timeline.py``).
"""

from mtdsim.l3_simulation.timeline.matrix import (
    Cell,
    N_RUNS,
    POLICY_ARMS,
    TIMELINES_DIR,
    build_matrix,
    entries_for,
    generate_cell,
    generate_library,
    seed_for,
)
from mtdsim.l3_simulation.timeline.report import (
    EXAMPLE_PATH,
    REPORT_JSON,
    REPORT_MD,
    build_report,
    cell_stats,
    write_example,
    write_report_md,
)
from mtdsim.l3_simulation.timeline.walk import (
    AGGREGATE,
    CLASS_NAMES,
    DURATION_VARIANTS,
    MAX_STEPS,
    OBJECTIVE_RULES,
    OGASP_DIR,
    PETRI_DIR,
    PROFILE_NAMES,
    SCHEMA_VERSION,
    TIMELINE_DIR,
    Net,
    Transition,
    dwell_table,
    load_catalogue,
    load_net,
    serialise,
    walk,
)

__all__ = [
    "AGGREGATE",
    "CLASS_NAMES",
    "Cell",
    "DURATION_VARIANTS",
    "EXAMPLE_PATH",
    "MAX_STEPS",
    "N_RUNS",
    "Net",
    "OBJECTIVE_RULES",
    "OGASP_DIR",
    "PETRI_DIR",
    "POLICY_ARMS",
    "PROFILE_NAMES",
    "REPORT_JSON",
    "REPORT_MD",
    "SCHEMA_VERSION",
    "TIMELINE_DIR",
    "TIMELINES_DIR",
    "Transition",
    "build_matrix",
    "build_report",
    "cell_stats",
    "dwell_table",
    "entries_for",
    "generate_cell",
    "generate_library",
    "load_catalogue",
    "load_net",
    "seed_for",
    "serialise",
    "walk",
    "write_example",
    "write_report_md",
]
