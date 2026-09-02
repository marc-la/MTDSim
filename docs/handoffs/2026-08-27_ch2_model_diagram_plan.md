---
status: open                  # Figure 2.1 built and wired 2026-08-27; retire once Marc's voice pass on the caption and the preamble reference sentence land
created: 2026-08-27
---

# Figure 2.1 — the MTDSim model diagram: purpose, placement, content, and build plan

**Ruling recorded (Marc, 2026-08-27):** ch2 §2.2 carries a model diagram in
its preamble. This does not overturn an earlier ruling — the two "no figure"
decisions on record were about the *pipeline ladder* (ch4's, context brief
Part 2 open question 4) and an *attacker flowchart* for §2.2.3 (precedents
brief item 14). A three-module simulator diagram was never ruled on. Floats
sit outside the word budget; the ledger is untouched.

Companions: [`2026-08-21_ch2_background_context.md`](2026-08-21_ch2_background_context.md)
(shape, budget), [`2026-08-21_ch2_lineage_description_precedents.md`](2026-08-21_ch2_lineage_description_precedents.md)
(craft). Facts here come from the implementation records, per the standing
warning in the precedents brief — never from the lineage papers.

---

## 1. Purpose — what the figure is for

**One line:** *the reader sees the whole simulator once, so that the three
subsections can each describe one part of a picture already held.*

Three jobs, in order of weight:

1. **Frame the subsections.** §2.2.1 / §2.2.2 / §2.2.3 each describe one box
   of the figure. Every structural noun a subsection uses (host, service,
   vulnerability, mechanism, scheme, selector, phase) is visible in the figure
   before it is read. The figure is the table of contents of §2.2 drawn as a
   system.
2. **Pre-install the interaction reading ch4 and ch5 use.** The defence writes
   the network *per layer* (position-mutating mechanisms touch the network
   layer, surface-mutating ones the host layer); the attacker reads a
   *visible subgraph* of the network and writes compromise into it. Drawn as
   arrows into specific layers, the position-versus-surface reading arrives
   free, and ch4's reset model and ch5's disruption-channel results can point
   back at it.
3. **Pin the seam the rest of the document stands on.** The ch4 figures
   (`fig:pipeline`, `fig:movement-dataflow`) already draw "the action layer,
   inherited from MTDSim" as a grey three-box glyph (attacker / network /
   defender). Figure 2.1 is that glyph opened up. The reader who meets the
   grey box in ch4 has already seen its insides here.

**What it is not:** a lineage diagram (Table 2.1's job), a procedure diagram
(no attacker phases as a flowchart, no scheme timelines — prose owns those),
and not the pipeline (ch4's ladder).

## 2. Placement — how it sits in §2.2

The preamble (~120 w) currently has two jobs: say what MTDSim is, then the
lineage's shape over Table 2.1. The figure slots between them:

> sentence 1–2: what MTDSim is (discrete-event simulator over a three-layer
> HARM) → **"Figure 2.1 shows its three modules and how they act on one
> another"** → sentence 3–4: the lineage's shape, over Table 2.1 → subsections.

Float order on the page: **figure first, table second.** The figure is the
frame; the table is the seam. Both are referenced from the preamble; neither
is referenced from §2.1.

Each subsection opens on its box. §2.2.1 opens on the network module's three
layers; §2.2.2 on the defence module (roster → scheme → selector, left to
right as the figure draws them); §2.2.3 on the attacker module. This is what
"a reader can follow the rest of the document" cashes out as: the subsections
never introduce a component the figure did not show.

Sizing: `\textwidth` float, portrait, natural-size inclusion (bare
`\includegraphics`, per the figure-pipeline rule), labels at
`\footnotesize`/`\small` so nothing prints under the 8pt floor. Not landscape:
this is a three-box diagram, not an edge-dense graph.

## 3. Content — what goes in, boiled down

The primer's "three durable objects" are the whole figure: **a network (the
terrain), a set of MTD mutations (terrain change), an attacker (an agent
moving over the terrain)**. Three modules, and the arrows between them. The
discipline: *a component is drawn only if a subsection describes it and a
later chapter leans on it.*

### 3.1 Network module — the centre of the figure

The three-layer HARM, drawn top-down as three stacked bands inside one box:

| Layer | What is drawn | Fact source |
|---|---|---|
| **Host layer** (was "network layer"; ruled 2026-08-27) | a small node-link graph of hosts; a few marked as **exposed endpoints** (the ingress); reachability as edges | primer §(b); write surfaces (b)1 — endpoints are fixed in ip/os/service space, deliberately (D-23) |
| **Service layer** (ruled name, 2026-08-27 M1 — the three layers are host / service / vulnerability, the network is the container; figure labels must match §2.2.1) | one host expanded: its internal **service graph** with an internal target node | primer §(b) — Watts–Strogatz service graph; the compromise-critical services are those adjacent to the internal target |
| **Vulnerability layer** | one service expanded: its **vulnerabilities**, each priced (a CVSS/complexity value sets success probability and exploit time). ~~some gated by a precondition~~ — **dropped 2026-08-27**: §2.2.1 cut preconditions (nothing later leans on them; in code it is a single-hop companion-presence gate on 10 % of vulns, not a tree), so the figure draws none | primer §(b).2–3; synthetic, no real CVEs |

Drawn as a *zoom*: network → one host → one service → its vulnerabilities.
Three levels of magnification, connected by thin zoom lines. This is Brown's
Fig. 1 genre (HARM overview) in our greys.

**Deliberately not drawn:** a designated target host. The primer says "there
is a designated target", but the write-surface census verified `target_node`
is `None` in the time-domain arm every experiment runs in (network type 1);
the attacker's objective in that arm is network-wide compromise. Drawing a
fixed target would put a fact in the figure the code contradicts — the
standing-warning failure mode. §2.2.3 states the scenario in prose instead.
Also not drawn: subnets, layer counts, node counts (constants → ch4's
parameter table).

### 3.2 Defence module — left of the network, writing into it

Three things, in the order §2.2.2 describes them, left-to-right or stacked:

1. **The mechanism roster** — the four reported mechanisms, each wearing its
   §2.1 label: *IP shuffle* (S), *complete topology shuffle* (S), *OS
   diversity* (D), *service diversity* (D). No redundancy — the honest scope
   note is stated in the caption, not drawn as an empty slot.
2. **The execution scheme** — one box between roster and network: *which
   mechanism fires, when* (simultaneous / random / alternating / single).
   Zhang's contribution; the proactive/time-triggered regime of §2.1.
3. **The reactive selector** — the DDQN choosing among the four plus no-op,
   drawn as an alternative feeding the same scheme slot. Tay's contribution;
   the reactive regime of §2.1.

**The arrows that carry the figure's argument:** the roster writes the
network, and the arrows land on *layers*, not on the box:

- IP shuffle, topology shuffle → **network layer** (position-mutating: they
  change where things are and what reaches what)
- OS diversity, service diversity → **host layer** (surface-mutating: they
  change what an exploit must match on a host already reached)

Two arrows, two landing layers. That is the position-versus-surface reading
drawn once. Fact source: write surfaces §(a) — verified diffs: IP shuffle
moves `host.ip` on internal hosts only; CTS regenerates adjacency; OSD/SD
redraw service nodes on internal hosts, ports untouched.

The exposed-endpoint exemption (mutation protects the interior, not the
perimeter) is a caption sentence, not a drawn element — it matters to ch4
but does not need geometry.

### 3.3 Attacker module — right of the network, reading and writing it

The inherited procedural attacker, drawn as a box with **what it holds**, not
what it does:

- **the visible subgraph** — exposed endpoints, compromised hosts, their
  neighbours (what it can see; grows outward from footholds)
- **compromised hosts and harvested credentials** — what it keeps (survives
  mutation — the reset model, ch4)
- its **six-phase loop** named in one line of small text inside the box
  (scan hosts → enumerate host → scan ports → exploit vulnerability /
  brute-force → discover neighbours → repeat), **not** as a flowchart.

Two arrows: **reads** the network (the visible subgraph — a read arrow from
the network layer), **writes** compromise into it (exploits at the
vulnerability layer, credentials reused network-wide). Drawn to the layers
the actions touch, the reads/writes are the mirror of the defence's writes —
which is exactly the interaction the thesis is about: what the defence
rewrites is what the attacker had read.

**Not drawn:** exploit ordering (RoA over CVSS — prose), the two scenarios
(prose), the reset penalty (ch4), any ATT&CK / kill-chain attribution (prose,
named not taught).

### 3.4 What makes it a simulation — the frame

A thin outer frame labelled **discrete-event simulation**, with one small
clock/time-axis emblem: the defender fires on a schedule; the attacker's
actions consume simulated time; the run yields time-to-compromise. This is
the metrics forward-clause drawn as one emblem, no more. It also gives the
scheme box its *when* — the schedule is the frame's, not the roster's.

### 3.5 Accent — the one thing the figure is about

The accent (RGB 31,84,140) goes on **the arrows between modules** — the
interactions — with the boxes and their contents in greys. The figure is
about how the three parts act on each other; the accent says so. Alternative
considered and rejected: accenting the attacker box (it is what this thesis
replaces) — that is ch4's story, and in ch2 the attacker is inherited like
everything else.

## 4. The reading, in one pass

Left to right: *the defence picks a mechanism by a scheme (or a learned
selector) and rewrites a layer of the network; the attacker reads the network
outward from the ingress and writes compromise into it; the simulation clock
runs both.* One sentence. If the figure cannot be read in that sentence, it
has too much in it.

## 5. Caption (decodes every encoding, per conventions §b2)

Session-drafted for Marc's voice pass. Short form: *The three modules of
MTDSim.*

> The three modules of MTDSim. The network is a three-layer hierarchical
> attack representation model, shown as three magnifications: hosts and
> their reachability, one host's internal service graph, and one service's
> priced vulnerabilities. The defence module selects a mechanism through an
> execution scheme or the learned selector and rewrites the network; accented
> arrows show which layer each mechanism rewrites --- the shuffles move the
> network layer, the diversity mechanisms the host layer. Exposed endpoints
> are never rewritten. The attacker module reads the network outward from
> the endpoints and writes compromise into it; what it has compromised
> survives every rewrite. The simulator carries shuffle and diversity
> mechanisms only; no redundancy mechanism is implemented.

## 6. Build plan

1. **Generator:** `tools/mtdsim_model_figure.py`, style block copied from
   `tools/gap_appendix_figures.py` (canonical since 2026-08-20). Emits
   `docs/thesis/figures/mtdsim_model.tex` (12pt standalone TikZ) + `.pdf`.
   Packs to the page box; prints natural size and effective type size.
2. **No values on the face**, so nothing is loaded from artefacts — but the
   generator *validates its claims* the way `movement_dataflow_figure.py`
   does: reads the default reported family from `mtd_scheme.py` and asserts
   the roster it draws is exactly that set (mechanism-not-exception: a roster
   change in code fails the build, not silently ships a stale figure).
3. **Geometry:** three columns (defence | network | attacker) under one
   frame; network column ~45 % of width for the three-level zoom; the zoom
   drawn as nested boxes with thin connecting lines, hosts as small circles,
   services as small squares, vulnerabilities as a short list with one
   precondition edge.
4. **Wire into the tex:** `\begin{figure}[tp]` under `\section{MTDSim}`,
   label `fig:mtdsim-model`, bare `\includegraphics`, caption from §5.
   Preamble reference sentence is Marc's to dictate.
5. **Consistency check against the ch4 glyph:** the action-layer box in
   `movement_dataflow` reads attacker / network / defender; Figure 2.1's
   three columns must use the same three names in the same order-of-mention
   so the reader recognises the glyph. (Order on the page differs — defence
   left, attacker right — because the reading runs defence → network →
   attacker; the names are what must match.)
6. **Record:** ch2 README "Deliberately absent → No figure" line rewritten;
   context brief open question 4 annotated; `figure_table_conventions.md`
   §d gains the HARM-overview genre note if the zoom form works.

## 7. Open for Marc (rule once, then build)

- **O1 — the zoom form for the network.** Three magnifications (network →
  host → service) versus three flat stacked bands. Recommendation: **zoom** —
  it shows *why* it is called hierarchical, and the vulnerability layer is
  otherwise a list with nothing to attach to. Cost: more drawing, slightly
  busier centre.
- **O2 — the latent mechanisms.** Four other mechanisms exist in code but are
  in no recorded experiment (port shuffle, user shuffle, host topology
  shuffle, OS diversity assignment). Recommendation: **not drawn** — ch2
  describes what the evaluation uses; the latent set is ch4's if anywhere.
- **O3 — the selector's presence.** Drawing the DDQN as an alternative feed
  into the scheme slot commits the figure to Tay's arm being part of the
  described platform. Recommendation: **drawn, small** — V3 keeps it as a
  benchmark, §2.2.2 describes it, and it is the only reactive-regime
  instance §2.1's vocabulary can point at.
- **O4 — where the accent goes** (§3.5). Recommendation: interaction arrows.


---

## 8. Rulings and state (2026-08-27, same day)

**Marc's rulings:** the target host **is** drawn — the targeted scenario (a
target such as a database the attacker is trying to reach) is the one this
work uses, so the §3.1 "deliberately not drawn" entry is overturned and the
attacker module carries an *Objective* panel ("compromise the target host").
O1 zoom form: adopted. O2 latent mechanisms: not drawn. O3 selector: drawn
small and dashed, de-emphasised (not used in this work). O4 accent: the
inter-module arrows.

**Discrepancy to carry, not resolve here:** the write-surface census verified
`target_node` is `None` in the time-domain arm (network type 1). If the
evaluation runs targeted, the arm that sets a target is the one to use, and
ch4's setup states it; the figure now describes the targeted platform Marc
says the work uses. Flag for the ch4 experimental-setup unit.

**Built:** `tools/mtdsim_model_figure.py` → `docs/thesis/figures/mtdsim_model.{tex,pdf}`,
15.9 × 11.6 cm natural, footnotesize/scriptsize printed at 10/8pt (natural
inclusion). Roster validated against `mtd_scheme.py` at build. Wired as
`fig:mtdsim-model` under `\section{MTDSim}` with the §5 caption (extended to
decode the endpoint / target / internal-target fills). Six iterations on the
rendered preview; the reading sentence of §4 holds on the final.

**Owed by Marc:** the preamble sentence referencing the figure; the voice
pass on the caption.


## 9. Redesign (2026-08-27, evening) — pictograms, not labels

Marc's verdict on the TikZ draft: correct as a model diagram, not doing the
job of *visualising* — too many words, not scannable, the LaTeX medium was
constraining the drawing. Ruling: draw it in whatever medium is natural
(HTML/SVG), keep the research-paper conventions, keep only component names
as words, replace the rest with symbolism.

**What changed.** The drawing now lives in `tools/mtdsim_model_figure.html`
(hand-authored SVG); `tools/mtdsim_model_figure.py` is the build step —
roster validation against `mtd_scheme.py`, the 8 pt floor check on every
`font-size` in the SVG at the 16 cm print width, and the PDF print through
headless Chromium (Playwright). Latin Modern is picked up from the system
fonts, so the figure sets in the document face. The TikZ generator and
`fig_2-2a_mtdsim_model.tex` are gone.

Content moves: module pictograms (shield / network / hooded attacker); a
per-mechanism glyph (host + swap for IP shuffle, rewired quad for topology
shuffle, host with an OS badge for OS diversity, service square for service
diversity), clock + dice for the scheme's *when / which*, a chip for the
selector; the **attack trace** as a dashed accented path across the network
layer (entry → owned hosts → target database) continuing into the host
layer (to the internal target) and the vulnerability layer (the exploited
bug ringed); the attacker's objective as crosshair + database, knowledge as
an eye over a seen/unseen mini-graph, capability as owned hosts + a key,
and the procedure as a five-step vertical loop with a loop-back arc. The
S/D badges were dropped — each name already carries its class — and the
caption decodes every fill and the trace.

Words left on the face: the three module names, the three layer names, the
four mechanism names, the four attacker panel names, and twelve small
labels (when, which, entry, target, internal target, precondition, the
complexity line, reach target, reads, exploits, the five loop steps).

**Pipeline note for the figure-conventions file:** this is the first
dissertation figure built HTML → Chromium PDF rather than TikZ. The
greys + one accent rule, the caption-decodes-everything rule and the 8 pt
floor all still apply and are checked in the tool; the difference is
authoring medium only.


## 10. Network module redesign (2026-08-27, late) — Marc's clarity checklist

Marc's questions, each now answered on the face: three HARM layers (three
magnified panels, shaded zoom wedges between them); scale-free network
(labelled Barabási–Albert); hosts as computers, reachability as cables;
depth left→right with the exposed endpoints as the first column and the
target database at the end; the attacker entering at the endpoints
(accented *enters* arrow) and its foothold glowing; the exposed column
pinned and labelled *exposed, fixed*; the visible subgraph as a dashed
accented perimeter (endpoints + footholds + neighbours), unseen hosts drawn
faint; one host magnified with OS / IP chips, a users-and-credentials
glyph, and services on a small-world ring (labelled Watts–Strogatz) with an
internal target; one service magnified as an attack tree with OR / AND
gates, the exploited vulnerability ringed, CVSS complexity named as the
price. Column order flipped to attacker | network | defence so the entry
arrow lands where the foothold is. OS versions not drawn (Marc: maybe not
important). Caption rewritten to decode every encoding.


## 11. Verification pass (2026-08-27) — Marc's dictated claims against the code

Marc flagged that some of what he dictated for §10 was wrong and asked for
every claim to be verified. Each row is checked in `mtdnetwork/` (locators
given), not in the primer or the papers.

| Claim on the face | Verdict | Evidence | Fix |
|---|---|---|---|
| Layers named network / host / vulnerability | **wrong** | Brown 2023 §III-A names them **Host / Service / Vulnerability**; the code's `Host.gen_internal_network` is the service graph | panels relabelled Host layer / Service layer / Vulnerability layer; caption + rewrite-arrow sentence updated (shuffles → host layer, diversity → service layer) |
| Vulnerabilities form an attack tree with AND/OR gates | **wrong** | `Vulnerability.has_dependent_vulns` (p = 0.1, `constants.py:86`) keys **one** dependency by a shared `dependent_vuln_id`; `can_exploit_with_dependent_vuln` needs one other vuln with that id (`services.py:34-37, 88-105`). No gates anywhere | drawn as a chain: one *requires* arrow between two vulnerabilities |
| CVSS sets success chance and exploit time | **half-right** | success: `random() < self.complexity` (`services.py:160`); time: `EXPLOIT_VULN × (1 − complexity)` (`services.py:112`). `cvss` is computed but consumed only by `roa()` for ordering (`services.py:188, 248`) | label reads *complexity sets success chance, exploit time*; CVSS not named on the face |
| OS dependency | **missing, now drawn** | `VULN_PROB_DEPENDS_ON_OS = 0.8` (`constants.py:85`); an OS-dependent vuln on the wrong OS costs 2.5× time (`services.py:113-114`) | one vulnerability carries an OS chip |
| A single target host | **wrong in mechanism, right in substance** | `target_node` is unconstructable on the shipped geometry (`network.py:215`, `network_type` hardcoded 1) — `targeted_objective_probe.md` §1. The located objective this work uses is the **database set** `get_database()`, the last `total_database` nodes, all at the deepest layer (`network.py:55`) | two database hosts drawn as the deepest column; attacker objective reads *database* |
| Scale-free (Barabási–Albert) network | **right, per subnet** | `nx.barabasi_albert_graph` per subnet per layer (`network.py:180`), inter-layer edges with p = 0.4 | corner label *subnets Barabási–Albert* |
| Layer 0 = all exposed endpoints, never mutated | **right** | `exposed_endpoints = range(total_endpoints)` (`network.py:52`), layer 0 holds exactly them (`network.py:143`); reported family skips them (write-surface census) | pin + *exposed, fixed* stands |
| Visible subgraph = endpoints + compromised + their neighbours | **right** | `get_hacker_visible_graph` (`network.py:957-970`) | perimeter stands |
| Host has one OS (type + version), an IP, users with credentials, 3–11 services on a Watts–Strogatz graph | **right** | `host.py:43-56, 486-493, 542`; `HOST_SERVICES_MIN/MAX = 3/11`, `USER_TOTAL_FOR_EACH_HOST = 5` | chips stand; versions not drawn (Marc: not important) |
| Host compromised when an exploited service is adjacent to the internal target | **right** | `check_compromised` (`host.py:417-426`) | internal target stands; caption states the rule |
| Attacker loop | **incomplete** | verbs are SCAN_HOST, ENUM_HOST, SCAN_PORT, EXPLOIT_VULN, BRUTE_FORCE, SCAN_NEIGHBOR (`constants.py:140-146`) | *exploit, or brute-force* and *neighbours* steps added |

One fact not on the figure but worth carrying to ch4: the time-domain
arm terminates at `terminate_compromise_ratio = 0.8` (`time_network.py:55`)
— the general scenario — and crown-jewel reach is a read-only measurement
over it, not a termination condition. The figure draws the objective as the
databases because that is what the located-objective work scores against.


## 12. Marc's rulings on §11, applied (2026-08-27)

- Layers: Host / Service / Vulnerability — applied.
- Vulnerabilities: a **chain**, nothing more; complexity / success chance /
  exploit time are implementation detail and leave the face. Drawn as
  service → vulnerability → vulnerability → vulnerability → host
  compromised (glow), labelled *vulnerability chain* only.
- Single target host: **stays** as an abstraction (the database-set
  operationalisation is §11's note for ch4, not the figure's).
- Service layer: redrawn as a zoom **into the computer** — the OS box holds
  the IP and the users' credentials, and the OS runs the services (arrow to
  the Watts–Strogatz ring). The OS → services link is what makes the OS
  dependency of services and vulnerabilities legible without a chip.
- Procedure: a **six-state machine** — scan hosts → enumerate → scan ports
  → exploit → brute-force → neighbours, with the three loop-backs drawn:
  brute-force fails → enumerate; neighbours discovered → enumerate; exploit
  succeeds → neighbours (accented, skipping brute-force). Transition names
  are in the caption, not on the face.

## 13. Proposal — encoding the baseline attacker into the Attacker module (2026-08-27)

Marc's brief: the Attacker module must carry the inherited scripted attacker
as a **closed six-state finite-state machine** (the artefact at
`data/misc/_viz/attacker_fsm/attacker_fsm_dependencies.png` is the
reference), show what it *holds* and that holdings persist, show it
*advancing* through reachability into compromise into an expanded
reachable set, and show **MTD disruption pushing it back to a recovery
state**. Targeted scenario only; general goes to the caption. This section
is the proposal, not the build — Marc rules, then it is drawn.

### 13.1 What the code says the machine is (facts, with locators)

- Six states: SCAN_HOST → ENUM_HOST → SCAN_PORT → EXPLOIT_VULN →
  BRUTE_FORCE; SCAN_NEIGHBOR. ENUM_HOST is the hub — four verbs need the
  `curr_host` it sets (`attacker_phase_catalogue.md` §"Reliance on
  preceding phases").
- Forward motion is compromise only: SCAN_PORT (credential-reuse hit),
  EXPLOIT_VULN (compromised) and BRUTE_FORCE (success) all go to
  SCAN_NEIGHBOR; every failure falls back (EXPLOIT fail → BRUTE_FORCE;
  BRUTE_FORCE fail → ENUM_HOST; SCAN_NEIGHBOR always → ENUM_HOST).
- Two terminals: STOP (nothing discoverable) and END (network owned) —
  the *general* scenario's terminal, which the figure does not show.
- **MTD interrupt** (`mtd_operation.py:217-264`): a **network-layer**
  mechanism interrupts *any* timed verb and restarts at **SCAN_HOST**; an
  **application-layer** mechanism interrupts only SCAN_PORT / EXPLOIT_VULN /
  BRUTE_FORCE and restarts at **SCAN_PORT**; both pay a confusion penalty
  (`PENALTY = 20`, exponential draw, `attack_operation.py:171-197`).
- **Holdings**: compromised hosts and harvested credentials survive every
  mutation (primer §(e), verified in the write-surface census — no
  mechanism writes `compromised_hosts`); the visible subgraph is
  endpoints + compromised + neighbours (`network.py:957`).

### 13.2 The proposal, in one picture

Replace the four stacked attacker panels with **two**: a *holdings* panel
and a *state-machine* panel, with the state machine given ~70 % of the
column.

**(a) Holdings (top, ~110 px).** Three glyphs in a row, no words beyond
the panel title *Holds*: crosshair + database (objective), the eye over
the seen/unseen mini-graph (visible subgraph), shaded hosts + key
(compromised hosts, credentials). A small **lock** glyph on the shaded
hosts and the key encodes *persistence* — these are the holdings no
mutation takes away. Caption decodes the lock. (Alternative considered:
drawing a rewrite arrow that bounces off the holdings — too much ink for
one fact.)

**(b) The machine (below, ~430 px).** The six states in a **ring**, not a
column — the loop *is* the attacker, and a ring reads as a closed cycle
at a glance where a column reads as a checklist. Layout, clockwise from
the top: SCAN HOSTS (12 o'clock) → ENUMERATE (2) → SCAN PORTS (4) →
EXPLOIT (6) → BRUTE-FORCE (8) → NEIGHBOURS (10) → back to ENUMERATE
through the centre. The hub role of ENUMERATE is then visible: three
edges converge on it (from scan hosts, from neighbours, from brute-force
fail). Edge grammar:

- grey solid: the forward chain and fall-backs;
- **accented**: the three *compromise* edges into NEIGHBOURS (from scan
  ports, exploit, brute-force) — the only forward motion, drawn in the
  figure's one accent so the reading "the only way forward is a
  compromise" is visual;
- a compromise edge continues **out of the module** as the existing
  *exploits* arrow into the network, and NEIGHBOURS has the *enters* /
  reads relationship — i.e. the module's external arrows attach to
  specific states, not to the box.

Words on the face: the six state names (icons inside each state as now),
nothing else. Success/fail labels are decoded in the caption.

**(c) MTD disruption — the recovery edges.** Two **dashed** edges from a
small shield glyph inside the machine panel (the defence acting *on the
attacker*, not on the network): one to SCAN HOSTS labelled by a tiny
host-layer glyph (a network-layer rewrite throws it back to host
discovery, from any state) and one to SCAN PORTS labelled by a tiny
service glyph (a service-layer rewrite throws it back to port scanning,
from the three application-level states). Drawn dashed grey, arrowheads
into the two recovery states, so the reader sees *where the attacker
lands* after each kind of move. The penalty (a clock glyph on the dashed
edges) is optional — recommend **omit**: the figure describes structure,
the penalty is ch4's timing material.

This is also the figure's payoff for ch4/ch5: the two recovery states are
the position-versus-surface reading on the attacker side (host-layer
mutation resets the map; service-layer mutation resets the working set on
a still-owned host), and it is now drawn once, in the same figure that
draws which layer each mechanism rewrites.

**(d) Advancing through the network.** Already encoded in the network
module (trace from entry to foothold, vulnerability chain ending in *host
compromised*, the perimeter that grows from footholds). The state machine
adds the *loop* view of the same thing; the two are tied by the external
arrows attaching to states (b). No new network-side element is proposed.

**(e) Targeted only.** Nothing changes on the face; the ENUM heuristic
(prefer hosts on the target's layer) and the general scenario's END
terminal go to the caption in one clause each.

### 13.3 What I would not draw, and why

- STOP / END terminals — clutter; the machine is closed for the reader's
  purposes and the terminals are one caption clause.
- Per-state durations, the give-up threshold (`ATTACKER_THRESHOLD = 10`),
  the 20 s penalty — ch4's parameter table.
- The credential-reuse check inside SCAN PORTS — it is why SCAN PORTS has
  a compromise edge; the edge carries it, the mechanism stays in prose.

### 13.4 Rulings needed

- **R1** ring versus column for the six states (recommend ring).
- **R2** the disruption edges: from a shield glyph *inside* the attacker
  panel (recommend), or as two long dashed arrows from the Defence module
  across the whole figure (rejected: they would cross the network column).
- **R3** persistence of holdings: lock glyph (recommend) or nothing
  drawn, caption only.
- **R4** penalty clock on the recovery edges: omit (recommend) or draw.
- **R5** the column budget: the machine needs ~430 px; the Objective /
  Knowledge / Capability panels merge into one *Holds* row to pay for it.


## 14. §13 built as recommended (2026-08-27)

R1 ring, R2 shield inside the panel, R3 lock, R4 no penalty clock, R5
Holds row — all applied. Column widened to 300 px (canvas 1100 px, type
raised to 20 px so the 8 pt floor holds at 16 cm). Ring of radius 100,
states at 11/1/3/5/7/9 o'clock; three accented compromise edges into
*neighbours*; two grey fall-backs into *enumerate*; two dashed recovery
edges from a shield above the ring into *scan hosts* (host-layer rewrite)
and *scan ports* (service-layer rewrite), glyph-free — the caption decodes
them. The *exploits* arrow now leaves from the exploit state. Labels that
the recovery edges pass behind carry a panel-coloured halo. The output
stem became `fig_2-2a_mtdsim_model` from outside this session (tool +
tex include both renamed; consistent). Caption re-decoded, including the
targeted-only clause.


## 15. Defence column brought to the full pool (Marc, 2026-08-30)

Verified against `2026-08-27_ch2_defence_mechanisms_context.md` §3: the
figure drew the lineage four. Ruling: draw the **full pool**. Roster now
seven, grouped by landing (three shuffles → host layer; OS and service
diversity and port shuffle → service layer; user shuffle → credentials —
a third accented arrow into the OS box's credentials compartment).
Tool validates against `MTD_POOLS['full']`; caption names the pool and
that the lineage's experiments and the selector use the first four.


## 16. Glyph standard and the selector's place (Marc, 2026-08-30)

Glyphs standardised to recognisable, brand-free symbols: **gear** = service
(ring, roster, chain head; filled gear = target service), **four-pane
window** = OS (chip and OS-diversity glyph), **socket/plug** = port (port
shuffle, the scan-ports state), computer = host, key = credential, user =
account, bug = vulnerability, database = target. No white squares remain.

Selector: `mtd_ai_operation.py` wraps an `MTDScheme`, draws the same
exponential trigger interval (200 t/u default) and chooses which mechanism,
or none. So the learned selector is drawn **inside the execution scheme**
as the alternative for *which* (dice *or* chip), not as a separate box
feeding the roster. The dashed selector panel is gone. Caption updated.


## 17. Conventions audit (2026-08-30) — against `figure_table_conventions.md` and general CS/infosec diagram practice

| Check | Result |
|---|---|
| §b1 caption below, short caption for the list | ✔ |
| §b2 every encoding decoded in the caption | ✔ after this pass (pin, faint hosts, perimeter, shaded hosts, **trace**, lock, gear / window / socket, accented transitions, dashed recoveries, dice-or-chip, three defence landings) |
| §b6 lifecycle order | ✔ ring runs scan → enumerate → ports → exploit → brute-force → neighbours |
| §d genre grammar | framework figure with per-stage content boxes (Rodriguez-style, no icons-as-clip-art); FSM as circles + labelled-by-caption transitions; HARM overview as magnifications ✔ |
| §g anti-patterns | no code identifiers, no tool junk, no clip-art, no sub-8 pt glyph, nothing undecoded ✔ |
| §h sizing | natural-size inclusion, 16 cm; smallest type 8.3 pt (tool-enforced); titles 10.8 pt < 12 pt body ✔ |
| greys + one accent | ✔; accent arrows at 3 px so they separate from grey by weight in greyscale (proofed) |
| one meaning per visual variable | accent = attacker gain / defence rewrite (the two interactions); dashed grey = MTD recovery; dashed accent = trace / perimeter; faint = unseen. Two dashed meanings, separated by hue and weight; decoded ✔ |
| one label per meaning | duplicate "target" removed from the service ring (filled gear + caption) ✔ |
| referenced from prose | `\ref{fig:mtdsim-model}` at two places in §2.2.3 ✔ |
| residual | caption ≈ 380 words — long, but the convention (§b2) requires the decode; Marc's voice pass may compress. Confidence the figure conforms: ~95 %. |
