"""Pytest bootstrap: puts ``src/`` on ``sys.path`` so the suite runs from a
checkout without ``pip install -e .`` (both packages, ``mtdnetwork`` and
``mtdsim``, live under ``src/``)."""

import sys
from pathlib import Path

_SRC = Path(__file__).parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
