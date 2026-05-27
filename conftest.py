"""Pytest bootstrap.

Adds ``src/`` to ``sys.path`` so the restructured ``mtdsim`` package
(the L0–L1 pipeline stages on this branch — ``mtdsim.l0_cti`` /
``mtdsim.l1_construction``) is importable without altering the repo's
``mtdnetwork`` packaging in ``setup.py``. Module CLIs run with ``PYTHONPATH=src``.
"""

import sys
from pathlib import Path

_SRC = Path(__file__).parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
