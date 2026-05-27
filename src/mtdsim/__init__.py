"""mtdsim — restructured package root.

On this branch (``feat/gap-schema``) only the L1 GAP subtree
(``mtdsim.attacker.gap``) is materialised; the full ``mtdnetwork`` -> ``mtdsim``
restructure lives on ``feat/attacker-profiling``. The GAP package is
self-contained and imports nothing from the simulator substrate, so it builds
and tests in isolation here.
"""
