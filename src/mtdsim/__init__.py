"""mtdsim — the contribution pipeline, organised by architecture level (L0→L4).

Each stage is an ``lN_`` package (``l0_cti``, ``l1_construction``,
``l2_subgraph``, ``l3_simulation``, ``l4_evaluation``); ``README.md`` carries the
canonical cross-walk. On this branch (``feat/gap-schema``) L0–L1 are built and
self-contained — they import nothing from the simulator substrate, so they build
and test in isolation — while L2 is a stub and L3–L4 are seam pointers into the
inherited ``mtdnetwork/`` substrate. A parallel *role*-based restructure of the
substrate lives on ``feat/attacker-profiling`` and is a separate reconciliation.
"""
