"""Back-compat shim: the visualiser moved to ``viz/``.

Kept so notebooks importing ``from mtdsim.attacker.gap.visualiser import
MITRETechniqueDependencyVisualiser`` continue to work. Delete in a future
release once downstream call sites are updated.
"""

from mtdsim.attacker.gap.viz.renderer import MITRETechniqueDependencyVisualiser

__all__ = ["MITRETechniqueDependencyVisualiser"]
