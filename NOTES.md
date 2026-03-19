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

I generated playground to play around with the codebase. By running it, I find the following:

![30 node network](output/playground/network_30n.png)
![100 node network](output/playground/network_100n.png)

This is the network of 30 and 100 nodes. Program runs so slowly.

```bash
(mtdsimtime) marc@marc:/mnt/c/Users/marcl/OneDrive/Documents/GitHub/MTDSim (learning/mtd-ai-walkthrough)$ time python playground.py network --nodes 30   
/home/marc/miniconda3/envs/mtdsimtime/lib/python3.9/site-packages/simpy/__init__.py:11: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  from pkg_resources import get_distribution
2026-03-19 09:45:07.962683: I tensorflow/core/util/port.cc:110] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2026-03-19 09:45:08.107566: I tensorflow/tsl/cuda/cudart_stub.cc:28] Could not find cuda drivers on your machine, GPU will not be used.
2026-03-19 09:45:08.908576: I tensorflow/tsl/cuda/cudart_stub.cc:28] Could not find cuda drivers on your machine, GPU will not be used.
2026-03-19 09:45:08.911229: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2026-03-19 09:45:12.344417: W tensorflow/compiler/tf2tensorrt/utils/py_utils.cc:38] TF-TRT Warning: Could not find TensorRT
/mnt/c/Users/marcl/OneDrive/Documents/GitHub/MTDSim/playground.py:60: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
  plt.tight_layout()
Saved network plot: output/playground/network_30n.png

real    0m20.459s
user    0m9.441s
sys     0m4.068s
```

Lazy loading of imports (e.g. preventing large ML libraries importing) seemed to fix it. Also fixed deprecated `pkg_resources`.

```bash
(mtdsimtime) marc@marc:/mnt/c/Users/marcl/OneDrive/Documents/GitHub/MTDSim (learning/mtd-ai-walkthrough)$ time python playground.py network --nodes 100
Saved network plot: output/playground/network_100n.png

real    0m6.848s
user    0m3.643s
sys     0m1.822s
```

