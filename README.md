# MTDSimTime

A time-based simulator used for evaluating Moving Target Defence (MTD) techniques.

## Getting Started:

1. Installing [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. Creating conda environment
   - `conda env create -f environment.yml`
   - `conda config --add channels conda-forge`
3. Activating the environment
   - `conda activate mtdsimtime`
4. Updating the environment
   - `conda env update --name mtdsimtime --file environment.yml --prune`

## Features

1. Network graph generation
<p>
  <img alt="" src="output/network.png" width="1080"/>
</p>

2. Attack Operation

<p>
  <img alt="" src="output/attack_record.png" width="720"/>
</p>


3. MTD Operation

<p>
  <img alt="" src="output/mtd_record.png" width="755"/>
</p>


4. Snapshot

5. Evaluation based on MTTC


## System Architecture
The system uses the 3-layer HARM model to represent the network. This is a representation of the network, with the lowest levels on the bottom and the highest levels on the top:

| layer           | Description                                                                                                                              |
|-----------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Network         | Made up of all the Hosts, connected in an Attack Graph, with exposed and un-exposed hosts that attackers will attempt to compromise      |
| Host            | Made up of several services (internal and external) in an Attack Graph.  The host is compromised when an internal service is compromised |
| Services        | An attack tree of vulnerabilities. A service is compromised when the sum of the exploited vulnerabilities' impact scores exceeds **7** (`SERVICE_COMPROMISED_THRESHOLD`). |
| Vulnerabilities | Generated with a set Attack Complexity (∈ [0.4, 1]) and Impact (∈ **[0, 10]** in this codebase — see note below).                          |

> **Note on Impact range.** Brown 2023 Table I quotes vulnerability impact on a `[0, 1]` scale. This codebase uses **`[0, 10]`** (`services.py`: `self.impact = random.random() * 10`), and the service-compromise threshold of `7` is calibrated against that wider range. The `[0, 10]` form is the inherited reality of MTDSim; the Brown-paper `[0, 1]` form is recorded as a documentation-only delta in [`docs/specs/mtdsim_spec.md`](docs/specs/mtdsim_spec.md) (Conflict C3, NET-13). No code change.

For the original upstream MTD parameter reference, see the unmodified MTDSimTime repository at https://github.com/MoeBuTa/MTDSimTime.

## Documents

see [docs](https://github.com/MoeBuTa/MTDSimTime/blob/main/docs/) for all related documents.






## Setup the previous works only

switch to another branch (MTDSim / New-Attack-Method) or go directly to:

[MTDSim](https://github.com/Ccamm/MTDSim)

[MTDSimTze](https://github.com/tzewenlee99/MTDSimTze)



This was all run on Python 3.9.13 64 Bit. In the root directory in terminal, run the following commands in your virtual environment to setup the environment:

- Setup virtualenv
   - `python -m pip install virtualenv venv`
   - `python -m virtualenv venv`
- Activate environemnt
   - `source venv/bin/activate`
- Install dependencies
   - `python setup.py install`
   - `pip install -r requirements.txt`
- Run an example: The following is only an example of how the function can be made, reference the run.py file or use the –help command to understand the parameters.
   - For New-Attack-Method: 
     - `python batchrun.py`
   - For MTDSim: 
     - `python -m mtdnetwork.run -m IPShuffle -n 50 -e 10 -s 5 -l 3 results.json`


