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

## Network "static world"

I generated playground to play around with the codebase. By running it, I find the following:

![30 node network](output/playground/network_30n.png)
![100 node network](output/playground/network_100n.png)
![1000 node network](output/playground/network_1000n.png)

This is the network of 30, 100, 1000 nodes. Program runs so slowly.

GREEN       =   Layer 0 (exposed endpoints/public-facing hosts attacker sees first)
BLUE        =   Layer 1
YELLOW      =   Layer 2
PURPLE      =   Layer 3

Layers are progressively deeper internal parts of the network.

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

## Attacker behaviour

Attacker behaviour without defender interface. This is raw baseline of the a simulated attacker on the network.

Codewise, the simulator starts `attack_operation.py` and does not start MTD. The attacker loop is driven by `attacker_operation.py` and these phases:

Kill Chain: RWDEICA

- SCAN_HOST (recon) (short) (discovers candidate hosts reachable from exposed/compromised nodes and builds host stack ordering.)
- ENUM_HOST (recon) (short) (pops/selects the next host target from that stack and updates pivot/attempt counters.)
- SCAN_PORT (recon) (short) (in real life port scan?)
- EXPLOIT_VULN (longest) (assuming weaponisation, delivery, exfiltration, installation, command and control, some arbitrary action on objective)
- BRUTE_FORCE   
- SCAN_NEIGHBOR (command and control)
- back to ENUM_HOST (???)

### What vulns exploited in `EXPLOIT_VULN`?

Generated synthetic vulns atttached to services during host/service generation. Exploit time is sampled per vulnerability from vulnerability/host properties (not a single fixed normal distribution). Repeated long `EXPLOIT_VULN` streaks are normal as the attacker is "trying" multiple vulns on the current host before deciding success/failure and moving on. What vulns??? or just baked in normal distribution?

### Why is `BRUTE_FORCE` a separate phase?

It is a fallback after exploit attempts fail to compromise the host service graph. It models credential attacks using previously compromised users. It can fail

`BRUTE_FORCE` as a separate phase vs. technically brute forcing in the previous phase. Can brute force fail? are these phases conducted on which hosts/ports?

### Which hosts/ports phases act on

`SCAN_PORT` -> current selected host, discovered exposed/exploitable service ports.

### Wht does flow return from `SCAN_NEIGHBOUR` to `ENUM_HOST`?

The `SCAN_NB` adds newly discovered adjacent hosts to stack. `ENUM_HOSTS` then selects the next host target from the updated stack. This is the pivot loop.

`SCAN_NEIGHBOUR` appears after a successful compromise, meaning attacker pivots and discovers adjacent targets.


```bash
(mtdsimtime) marc@marc:/mnt/c/Users/marcl/OneDrive/Documents/GitHub/MTDSim (learning/mtd-ai-walkthrough)$ python playground.py attack --nodes 50 --finish-time 1200

=== attack_only ===
Total nodes: 50
Compromised hosts: 5 (10.00%)
Attack events: 142
MTD events: 0
Interrupted attack events: 0

# run attacker module again... some randomness.

(mtdsimtime) marc@marc:/mnt/c/Users/marcl/OneDrive/Documents/GitHub/MTDSim (learning/mtd-ai-walkthrough)$ time python playground.py attack --nodes 50 --finish-time 1200

=== attack_only ===
Total nodes: 50
Compromised hosts: 3 (6.00%)
Attack events: 187
MTD events: 0
Interrupted attack events: 0

real    0m18.899s
user    0m9.414s
sys     0m4.159s

# ran attacker for a bit longer to see if more compromises would occur... took 10-15000 seconds

(mtdsimtime) marc@marc:/mnt/c/Users/marcl/OneDrive/Documents/GitHub/MTDSim (learning/mtd-ai-walkthrough)$ time python playground.py attack --nodes 100  --finish-time 11000

=== attack_only ===
Total nodes: 100
Compromised hosts: 97 (97.00%)
Attack events: 1302
MTD events: 0
Interrupted attack events: 0

real    0m17.127s
user    0m13.520s
sys     0m3.382s

# For the diagrams generated below, here are the stats it spat out.

=== attack_only ===
Total nodes: 50
Compromised hosts: 2 (4.00%)
Attack events: 158
MTD events: 0
```

Essentially, the attacker is: Discovering reachable hosts -> selecting one, port scanning it -> trying many vuln exploits ->  brute forcing (if needed) -> repeating until the time limit.

![Attack only attack timeline](output/playground/attack_only_attack_timeline.png)
![Attacker only host compromise ](output/playground/attack_only_host_compromise_progress.png)
![Attacker only compromise network](output/playground/attack_only_host_compromise_map.png)

### What does the CSV show?

It should fixed-duration actions (e.g. `SCAN_HOST`, `ENUM_HOSTS` 5 seconds, `SCAN_PORT` 25s, `BRUTE_FORCE` 20s)

| name | start_time | finish_time | duration | current_host | current_host_uuid | compromise_host | compromise_host_uuid | current_host_attempt | cumulative_attempts | cumulative_compromised_hosts | compromise_users | interrupted_in | interrupted_by |
|------|-----------|------------|----------|--------------|-------------------|-----------------|----------------------|----------------------|----------------------|------------------------------|------------------|----------------|----------------|
| SCAN_HOST | 0.0 | 5.0 | 5.0 | -1 | -1 | None | None | 0 | 0 | 0 | [] | None | None |
| ENUM_HOST | 5.0 | 10.0 | 5.0 | -1 | -1 | None | None | 0 | 0 | 0 | [] | None | None |
| SCAN_PORT | 10.0 | 35.0 | 25.0 | 0 | 56a5c835-8ad3-4ed0-b154-8980bd914f56 | None | None | 1 | 0 | 0 | [] | None | None |
| EXPLOIT_VULN | 35.0 | 35.361361078473614 | 0.3613610784736139 | 0 | 56a5c835-8ad3-4ed0-b154-8980bd914f56 | None | None | 1 | 0 | 0 | [] | None | None |
| EXPLOIT_VULN | 35.361361078473614 | 41.53192920141339 | 6.170568122939777 | 0 | 56a5c835-8ad3-4ed0-b154-8980bd914f56 | None | None | 1 | 1 | 0 | [] | None | None |
| EXPLOIT_VULN | 41.53192920141339 | 48.63905590469397 | 7.107126703280578 | 0 | 56a5c835-8ad3-4ed0-b154-8980bd914f56 | None | None | 1 | 2 | 0 | [] | None | None |
| EXPLOIT_VULN | 48.63905590469397 | 57.47513967971987 | 8.836083775025898 | 0 | 56a5c835-8ad3-4ed0-b154-8980bd914f56 | None | None | 1 | 3 | 0 | [] | None | None |
| BRUTE_FORCE | 57.47513967971987 | 77.47513967971986 | 19.999999999999993 | 0 | 56a5c835-8ad3-4ed0-b154-8980bd914f56 | None | None | 1 | 4 | 0 | [] | None | None |
| ENUM_HOST | 77.47513967971986 | 82.47513967971986 | 5.0 | 0 | 56a5c835-8ad3-4ed0-b154-8980bd914f56 | None | None | 1 | 4 | 0 | [] | None | None |
| SCAN_PORT | 82.47513967971986 | 107.47513967971986 | 25.0 | 1 | 0c20bfd9-ccef-4814-bfbf-85156b21b59d | None | None | 1 | 4 | 0 | [] | None | None |
| EXPLOIT_VULN | 107.47513967971986 | 112.37391858546592 | 4.898778905746056 | 1 | 0c20bfd9-ccef-4814-bfbf-85156b21b59d | None | None | 1 | 4 | 0 | [] | None | None |

...
(rest ommitted)

`EXPLOIT_VULN` durations vary as exploit time is sampled and depends on vuln characteristics. Compromised notes are denoted when `compromise_host` is set:

NOTE: why are there names to compromised users??? shouldn't it be UUID? Can this be visualised?

NOTE 2: Users are basically "first name only", stored in tuples. Hosts have `host_ID` and `host_UUID`. Multiple users on each host.

| name | start_time | finish_time | duration | current_host | current_host_uuid | **compromise_host** | compromise_host_uuid | current_host_attempt | cumulative_attempts | cumulative_compromised_hosts | compromise_users | interrupted_in | interrupted_by |
|------|-----------|------------|----------|--------------|-------------------|-----------------|----------------------|----------------------|----------------------|------------------------------|------------------|----------------|----------------|
| EXPLOIT_VULN | 503.53 | 517.36 | 13.83 | 2 | 45199fdc-9738-4c97-a751-cdc6ac7af9d1 | **2** | 45199fdc-9738-4c97-a751-cdc6ac7af9d1 | 1 | 63 | 0 | ['Perrine', 'Meryl', 'Mia', 'Candace', 'Elaine'] | None | None |


### Limitations to this model

The model is "bursty", as it is host-centric. (pick hst -> do a large batch of exploits in the plot -> short scan/enum transitions).

Limitations include:

- Defensive metrics essentially "fully see" the network (e.g. attack-path stats), going against limited observation assumption.
- Vuln generation/exploitability completely simulator-defined
- Attacker phases are predictable and limited in strategy (defence overfitting attacker behaviour)
- Oversimplification may be present (e.g. phase boundaries; real attacks interleave techniques, cred abuse, and discovery in messier ways)
- Time constraints are fixed duration. Simulation dependent on these parameters.
- Topology generation, endpoint placement, service assignment alter attacker path options. This sort of fluctuation could basically invalidate MTD quality. Possibly produce reproducible networks, and predefined easy, medium, hard networks to crack.


---

## Running MTD operations

Here I attempted to generate some gifs of how each MTD operations operates on the network

### COMPLETE TOPOLOGY SHUFFLE

Method: regenerates the network graph (edges/topology), then reattaches the same host objects to node IDs.
Behavior: strongest effect is structural rewiring; host internals (OS, users, ports, services) mostly stay the same.
Goal: disrupt attacker path planning and shortest paths at the network level.
Tradeoff: very disruptive to connectivity assumptions, but does not inherently diversify host software state.

![Complete topology shuffle](output/playground/inspect_mtd/CompleteTopologyShuffle/animation.gif)


### HOST TOPOLOGY SHUFFLE:           

Method: swaps host objects between node positions, mainly within layers, while avoiding exposed endpoints.
Behavior: from a node-centric view, many fields appear to change at once (IP, OS, ports, users, services) because a different host now occupies that node.
Goal: invalidate attacker mapping between node location and host identity.
Tradeoff: can look similar to many simultaneous changes, but conceptually it is relocation, not internal mutation.
![Host topology shuffle](output/playground/inspect_mtd/HostTopologyShuffle/animation.gif)

### IP SHUFFLE:              
         
Method: reassigns fresh IP addresses to non-exposed hosts.
Behavior: primary change is host addressing; little/no change to OS, ports, users, service set.
Goal: break reconnaissance and cached target addressing.
Tradeoff: lightweight and frequent, but narrow defense scope.

![IP shuffle](output/playground/inspect_mtd/IPShuffle/animation.gif)

### OS DIVERSITY:                     
**GOAL**: Changes host OS and reassigns incompatible services

For each non-exposed host, it randomly picks an OS type, keeps roughy the same version index, and then updates incompatible services. This is quick heterogenity through randonmess. Simple and fast, not globally optimised.

![OS diversity](output/playground/inspect_mtd/OSDiversity/animation.gif)

### OS DIVERSITY ASSIGMENT:           

**GOAL**: Optimisation-based OS assigment (Python Linear Programming used)

This is similar to `OS DIVERSITY` as they do per-host randomisation. However, optimisation-based assignment is used where a Diversity Assignment Problem is constructed over the network graph and computes OS placement to maximise a security objective across attack paths from exposed endpoints to destinations. Goal is for strategic objective across attack paths from exposed endpoints to destinitions. Heavier computational cost.

Explore this more. Does this change its response depending on the way the network is compromised? 

![OS diversity assignment](output/playground/inspect_mtd/OSDiversityAssignment/animation.gif)

### PORT SHUFFLE:       

Method: changes internal service port numbers on non-exposed hosts.
Behavior: service identity remains, but access coordinates (ports) move.
Goal: reduce value of previous scans and scripted exploit attempts tied to old ports.
Tradeoff: targeted obfuscation; does not diversify software stack by itself.

![Port randomisation shuffle](output/playground/inspect_mtd/PortShuffle/animation.gif)

### SERVICE DIVERSITY:  

Method: replaces host services with random latest-version compatible services for that host OS.
Behavior: service composition and vulnerability surface shift significantly; OS/IP usually unchanged.
Goal: alter exploitability landscape by changing what software is present and versions in use.
Tradeoff: can be effective against exploit reuse, but may introduce operational instability in real systems.

![Service diversity](output/playground/inspect_mtd/ServiceDiversity/animation.gif)

### USER SHUFFLE:          

Method: reassigns user sets across hosts.
Behavior: credential-placement landscape changes; host network and software state mostly unchanged.
Goal: disrupt attacker lateral movement paths that rely on harvested credentials and reuse patterns.
Tradeoff: strong effect on credential-based attack steps, limited effect on pure service-exploit paths.

![User shuffle](output/playground/inspect_mtd/UserShuffle/animation.gif)

### Comparison of MTD operations

| label | total_nodes | compromised_hosts | compromise_ratio | attack_events | mtd_events | interrupted_events |
|---|---:|---:|---:|---:|---:|---:|
| compare_nomtd | 50 | 4 | 0.08 | 143 | 0 | 0 |
| compare_CompleteTopologyShuffle | 50 | 1 | 0.02 | 128 | 6 | 6 |
| compare_IPShuffle | 50 | 2 | 0.04 | 143 | 6 | 6 |
| compare_OSDiversity | 50 | 4 | 0.08 | 143 | 6 | 6 |
| compare_ServiceDiversity | 50 | 3 | 0.06 | 119 | 6 | 6 |

Findings 

- Best reduction in compromise ratio is CompleteTopologyShuffle (0.08 to 0.02, 75% reduction vs no MTD).
- IPShuffle improves compromise ratio (0.08 to 0.04, 50% reduction) but does not reduce attack event count in this run.
- ServiceDiversity gives moderate compromise reduction (0.08 to 0.06, 25% reduction) and also reduces attack events (143 to 119).
- OSDiversity shows no improvement in compromise ratio for this run (remains 0.08), suggesting limited short-horizon effect with current parameters.
- All MTD runs report interrupted_events = 6, indicating the scheduler is consistently interrupting attacker actions when MTD executes.
- This is one stochastic run only; conclusions should be based on repeated seeds and confidence intervals, not a single trial.

NOTE: FIndings on very limited dataset (50 nodes, 1200s time, findings are NOT reproducible).

### Limitations of MTD operations

Very modular, multi-layer attack representation (not sure on the differences in the layer generation)

Assumptions
- Attacker model has fixed action primitives and durations (see attack timing in `constants.py`)
- Synthetic network ~ enterprise network? Is the distribution representative enough?
- Are the success probabilities calibrated on anything? Vulnerability complexity/impact/exploitability in `services.py`
- MTD scheduling and execution costs are abstract (see `constant.py`)
- Once an endpoint is exposed, it is hardcoded to be skipped 

Limits
- Realism 
- Attacker diversity
- External validity 
- Host-centric, attacker-centric, network-centric focused studies
- `OSDiversityAssignment` computational overhead

Next steps
- Calibration
- Fidelity of models
- Broader Evaluation
- Reproducibility
- Integration with real network topology/config data

---


