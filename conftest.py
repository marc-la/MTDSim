"""Pytest bootstrap.

Adds ``src/`` to ``sys.path`` so the restructured ``mtdsim`` package
(currently just the ``mtdsim.attacker.gap`` subtree on this branch) is
importable without altering the repo's ``mtdnetwork`` packaging in
``setup.py``. Scripts that need it run with ``PYTHONPATH=src``.
"""

import sys
from pathlib import Path

_SRC = Path(__file__).parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
