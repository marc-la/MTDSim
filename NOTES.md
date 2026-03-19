# INTERNAL DOCUMENTATION OF MTD SIMULATOR 

This is for my own personal understanding of the model. Will append stuff in here.

---

This is a annotated tree from prompting/scanning the codebase. 

```bash
.
├── NOTES.md        # ME
├── README.md       # Deprecated README, needs updating.
├── docs            # Theses and manuals
│   ├── manual
│   │   ├── Document.pdf
│   │   ├── MTD Parameters.pdf
│   │   └── logs.md
│   ├── notes.md
│   └── thesis
│       ├── ... (deleted theses)
├── environment.yml
├── experiments         # Lots and lots of data
│   ├── .DS_Store
│   ├── AI_model
│   │   ├── .DS_Store
│   │   ├── models_joo_kai
│   │   └── models_will
│   │       ├── .DS_Store
│   │       ├── new_models
│   │       │   ├── ... (deleted)
│   │       └── new_models.zip
│   ├── archive
│   │   ├── data_visualisation.ipynb
│   │   └── simulation.ipynb
│   ├── dap_mtd.py          # ALT:  Runs diversity-assignment variant experiments.
│   ├── experimental_data
│   │   ├── .DS_Store
│   │   ├── plots
│   │   └── results
│   │       ├── .DS_Store
│   │       ├── final_trials
│   │       │   ├── (deleted trial variants)
│   │       ├── other_schemes
│   │       ├── other_schemes_other
│   │       ├── overall_trials
│   │       │   ├── (deleted trial variants)
│   ├── experiments.ipynb
│   ├── model_training
│   │   ├── mtd_ai_training.ipynb
│   │   ├── mtd_ai_training_will.ipynb
│   │   ├── training_will.py    # Training launcher.
│   │   └── training_will_2.py  # Variant of above.
│   ├── multiple_mtd.py     # ALT: Pairwise strategy combinations under random/alternative/simultaneous schemes.
│   ├── run.py              # MAIN ORCHESTRATION API FOR BASELINE: End-to-end execution where experiments create a SimPy environment and loads snapshots.
│   ├── run_trials
│   │   ├── run_experiment.ipynb
│   │   ├── run_experiment.py
│   │   ├── run_trials.py
│   │   └── run_trials_2.py
│   ├── single_mtd.py       # Batch single-strategy plus no-MTD runs.
│   ├── snapshots
│   └── visualization
│       ├── final_report_visualisation.ipynb
│       ├── presentation_plots.ipynb
│       ├── radar_plots.py
│       ├── radar_plots_final.ipynb
│       └── stacked_plots.py
└── mtdnetwork              # Simulator world model. A generated enterprise network of hosts and services, with vulnerabilities and users
    ├── .DS_Store
    ├── __init__.py
    ├── component
    │   ├── __init__.py
    │   ├── adversary.py    # Stateful attacker process loop scanning, enumerating, port-scanning, exploiting, and brute-forcing. (attacker state container)
    │   ├── host.py         # CORE (Per-host internal service graph, compromise logic, port/vuln traversal)
    │   ├── mtd_scheme.py   # Schedules and executes MTD actions with resource locks and attacker interruption. (Strategy registration and scheduling policy.)
    │   ├── network.py      # CORE (graph generation, topology, host placement, exposure/path scoring hooks)
    │   ├── services.py     # CORE (Vulnerability and service generators, exploitability/risk/ROA dynamics)
    │   ├── target_network.py   # Targeted-attack flavour of network.
    │   ├── time_generator.py   # Distribution helpers.
    │   └── time_network.py # CORE (runtime network with queues and compromise stop criteria)
    ├── data
    │   ├── __init__.py
    │   ├── constants.py
    │   ├── first-names.txt
    │   └── words.txt       
    ├── mtd                 # MTD operations exist here. 
    │   ├── __init__.py
    │   ├── completetopologyshuffle.py      # COMPLETE TOPOLOGY SHUFFLE:        Regenerates full topology while preserving host objects
    │   ├── hosttopologyshuffle.py          # HOST TOPOLOGY SHUFFLE:            Host topology shuffling strategy.
    │   ├── ipshuffle.py                    # IP SHUFFLE:                       Changes host IPS
    │   ├── osdiversity.py                  # OS DIVERSITY:                     Changes host OS and reassigns incompatible services
    │   ├── osdiversityassignment.py        # OS DIVERSITY ASSIGMENT:           Optimisation-based OS assigment (Python Linear Programming used)
    │   ├── portshuffle.py                  # PORT SHUFFLE:                     Port randomisation strategy.
    │   ├── servicediversity.py             # SERVICE DIVERSITY:                Service mutation MTD. 
    │   └── usershuffle.py                  # USER SHUFFLE:                     User placement/account perturbation strategy.
    ├── mtdai               # Network architecture, epsilon-greedy action choice, replay and reward function
    │   └── mtd_ai.py       # DDQN-like policy over static plus time features to choose next MTD action.
    ├── operation                   # HELPER PACKAGE
    │   ├── __init__.py             
    │   ├── attack_operation.py     # Works with component/advserary.py
    │   ├── mtd_ai_operation.py     # Works with mtdai/mtd_ai.py
    │   ├── mtd_ai_training.py      # Works with mtdai/mtd_ai.py
    │   └── mtd_operation.py        # Works with component/mtd_scheme.py
    ├── snapshot        # Snapshot/pickle state of network/adversary/base paths
    │   ├── __init__.py
    │   ├── adversary_snapshot.py
    │   ├── network_snapshot.py
    │   └── snapshot_checkpoint.py
    └── statistic                   # Attack and MTD traces become derived metrics like ASR, MTTC-like measures, risk/ROA
        ├── __init__.py
        ├── attack_statistics.py    # CORE
        ├── evaluation.py           # CORE
        ├── mtd_statistics.py       # CORE
        ├── scorer.py               # CORE    
        ├── security_metric_evaluations.py
        ├── security_metric_statistics.py
        └── utils.py
```

---

# CORE MTD SYSTEM

