# RL / simulation security environments — extraction notes (survey-level)

> CyberBattleSim (Microsoft), NASim, CybORG, Yawning Titan and kin. Survey-level
> stub from project documentation and OA papers via web search (July 2026).
> Load-bearing for the binding investigation
> ([`../../implementation/pipeline/ogasp/controller.md`](../../implementation/pipeline/ogasp/controller.md))
> as the precedent for candidate **C3 (net-as-policy-prior over a substrate
> action space)** — the framing that appears in no prior repo document.

## Bibliographic anchor

- **Citation keys**: `cyberbattlesim`, `nasim`, `cyborg`
- **Sources (web, survey-level)**:
  - CyberBattleSim — <https://github.com/microsoft/CyberBattleSim>; MIT MEng
    thesis, "Simulating Network Lateral Movements through the CyberBattleSim Web
    Platform" — <https://dspace.mit.edu/handle/1721.1/143191>
  - "Evaluation of RL for Autonomous Penetration Testing (A3C/Q-learning/DQN)",
    arXiv:2407.15656 (OA) — NASim action model
  - Kim-Hammar, *awesome-rl-for-cybersecurity* — <https://github.com/Kim-Hammar/awesome-rl-for-cybersecurity>
- **Acquisition status**: all OA (GitHub / arXiv / dspace). No paywalled item.

## Extraction policy

Survey-level, paraphrase-only; no fair-use quotation reproduced. Claims
attributed to project docs / OA papers and marked **survey-level**.

## Relevant artefacts

### The attacker as a policy over a typed action space (load-bearing for C3)

- **Claim (survey-level):** CyberBattleSim models the network as a directed
  graph of nodes carrying OS/services/known-vulnerabilities/firewall rules and
  edges as connectivity; the attacker is an RL agent selecting from a **typed
  action space** — local vulnerability exploitation, remote exploitation, and
  **credential-based lateral movement** (an explicit first-class action) — under
  partial observability, with an outcome model that rewards compromise of
  mission-critical nodes more than ordinary hosts. NASim likewise defines a
  declarative action model where each action carries prerequisites, a cost, and
  a success probability; CybORG emphasises the defender side of the same
  action-space idea.
- **Transfer verdict: PARTIALLY TRANSFERS (framing + credential-first action,
  not code).**
  - *What transfers:* the reframing of "attacker" from a *fixed script* to a
    **distribution over an enumerated action space** is exactly candidate C3.
    MTDSim's substrate already has the action space (the six verbs) and the
    typed state (hosts/services/vulns) — so a class-conditioned selection
    distribution over enabled verbs is a natural, precedented binding, and it
    is the structural home for R2 (per-action success) and R3 (styles as
    selection-temperature / reward-shape). The mission-critical-node reward
    asymmetry corroborates that *objective-weighted target selection* is a
    standard, defensible mechanism — useful for reading MTDSim's target node.
  - *What does NOT transfer:* these environments **train** a policy (the agent
    learns); MTDSim's binding does not — the L2 net *is* the policy prior, fixed
    from CTI, not learned. Importing RL training would reintroduce the
    attacker-adaptivity that is explicitly deferred (ATK-04 / primer §f) and
    would break SIM-05 determinism. C3 therefore takes the *action-space
    contract*, not the learning loop: the net supplies the selection weights,
    the substrate samples under a seeded stream.
- **Novelty note:** no existing repo document frames the OGASP net as a *policy
  prior over the substrate's verb action space*; the repo frames it as an
  envelope/script (replay). This is the investigation's first-principles-/
  precedent-sourced candidate that satisfies gate 1's novelty clause.

### Credential handling as the distinguishing modelling choice

- **Claim (survey-level):** CyberBattleSim's noted advance over earlier
  simulators (incl. NASim) is explicit **credential handling** — credentials are
  a first-class, portable capability.
- **Transfer verdict: TRANSFERS (as corroboration).** This independently
  corroborates the substrate primer's §(e) claim that credentials are the
  reset-*survivor* capability — the "key" that is not location-bound. It
  strengthens the C2/C3 case that a *credential-first* class is a behaviourally
  distinct, literature-grounded attacker, not an invention.
  → primer §(e); [`controller.md`](../../implementation/pipeline/ogasp/controller.md) C2.
