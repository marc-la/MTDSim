"""mtdsim — the APT attacker model, built in four stages and run inside MTDSim.

``l0_cti`` fetches the threat intelligence (CTID Attack Flow corpus, MITRE ATT&CK);
``l1_construction`` builds the attack graph (Section 4.1); ``l2_subgraph`` cuts it
into attack profiles by objective (Section 4.2); ``l3_simulation`` compiles each
profile into a Petri net and runs it as the attacker inside the simulator
(``mtdnetwork``) through attack actions (Sections 4.3-4.4). ``README.md`` maps
each package to its dissertation section and data folder.
"""
