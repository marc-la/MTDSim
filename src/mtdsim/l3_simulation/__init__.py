"""Running the attack profiles as an attacker inside MTDSim (Sections 4.3-4.4).

``petri`` compiles a profile into a Petri net; ``controller`` maps each tactic
to the simulator's attack actions and judges their outcomes; ``movement`` is the
APT attacker model that walks the net inside ``mtdnetwork``; ``timeline`` is an
earlier stand-alone walk of the same nets, kept for its tests; ``trace.py`` is
the event-log tracer for a movement run.
"""
