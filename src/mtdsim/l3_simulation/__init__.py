"""L3 — OGASP (operationalised GASP).  *Substrate seam — holds no code here.*

Stage L3 of the L0->L4 pipeline: a graph-driven attacker traverses the L2 GASP
*inside the MTDSim substrate*, alongside the inherited 6-phase scripted attacker.
That code lives in the substrate (``mtdnetwork/``), not in this package — see
this directory's ``README.md`` and ``docs/specs/architecture.md`` §(f),(i). This
package exists only to mark the pipeline level and point at the seam.
"""
