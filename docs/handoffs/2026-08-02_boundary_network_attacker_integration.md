---
status: open
created: 2026-08-02
---

# Boundary review 1 of 3 — NETWORK / ATTACKER: is the attacker meaningfully coupled to every network component the defence family can move?

**Programme framing (shared by the three boundary briefs).** The project's
comparative MTD evaluation is only as good as the integration it runs on: a
mechanism's measured effect must flow through channels the attacker actually
exercises, or the evaluation compares *integration depths* rather than *defence
ideas*. The 2026-08-02 indistinguishability finding
([`2026-08-02_os_service_diversity_indistinguishability.md`](2026-08-02_os_service_diversity_indistinguishability.md))
is the proof this failure mode is live: both unseparated pairs in experiment 2
are integration artefacts, not defence facts — the OS relabel is written and
never read; `host.ip` is written and read by **nothing in the repository**
(verified at repo scope, 2026-08-02: written at `host.py:45` and
`ipshuffle.py:22`, zero readers). Marc has directed a systematic review of the
three component boundaries, one session each:

1. **NETWORK / ATTACKER** (this brief) — what the attacker reads.
2. **NETWORK / DEFENDER**
   ([`2026-08-02_boundary_network_defender_integration.md`](2026-08-02_boundary_network_defender_integration.md))
   — what each mechanism writes, and whether it is the whole surface in its
   purview.
3. **ATTACKER / DEFENDER**
   ([`2026-08-02_boundary_attacker_defender_integration.md`](2026-08-02_boundary_attacker_defender_integration.md))
   — the direct couplings that bypass network state.

Ownership rule, to prevent double-work: this brief owns the **read side** of
the coupling matrix (§2). A component the attacker never reads is this brief's
finding even if a mechanism moves it; a component moved partially is brief 2's;
a signal that reaches the attacker without passing through network state is
brief 3's. Each brief runs its own Part A / Part B cycle and its own confidence
gate; the matrix skeleton lives here because reads define what "meaningful"
means for the other two.

## 1. Goal

Establish, at 95 % confidence (§6), that every network component inside the
defence family's purview is coupled to the attacker through at least one live,
verified channel — **per arm** — or carries a Marc-dispositioned record of why
its dead coupling is acceptable for comparative evaluation. Where the coupling
is dead and undispositioned, classify it under the intent spec's §c procedure
and put it to Marc; where Marc rules a change, implement it under the D-05
procedure. The purpose is a fair contest: after this brief closes, no
mechanism's measured rank should be attributable to an unexamined read-gap.

## 2. State of play — the coupling matrix, seeded with what is already verified

The attacker's entire perceptual surface, per verb (native six-verb FSM;
the movement arm drives the same cores through `step()`):

| Verb | What it reads (code-verified locators) |
|---|---|
| SCAN_HOST | `get_hacker_visible_graph()`, neighbours of compromised hosts, `get_path_from_exposed` distances, exposed endpoints — **node ids and adjacency only** (`attack_operation.py:250-303`) |
| ENUM_HOST | host stack order, per-host attempt counter, host instance handle |
| SCAN_PORT | node attrs `"port"` and `"service"` on the host's internal graph; phase-1 credential-reuse check against host users |
| EXPLOIT_VULN | per-service vulnerability lists (top-5 RoA), `complexity`; `vuln.network(host)` receives the host and ignores it (gate commented out, `services.py:146-148` → D-19) |
| BRUTE_FORCE | host users vs network user list (reuse probability) |
| SCAN_NEIGHBOR | current host's neighbours in the host graph |

Components already known **read**: topology/adjacency, node ids, services,
ports (as identifiers), vulnerabilities, users/credentials, exposed endpoints,
path distances. Components already known **written by a mechanism but never
read**:

- **`host.ip`** — zero readers repo-wide. IPShuffle's entire measured effect is
  brief 3's channels (interrupt + penalty + cursor clear), which is why
  `(complete_topology, ip_shuffle)` is unseparated in every data set.
- **`host.os_type` / `os_version`** — two channels exist and both are dead for
  the movement arm, one dead for both arms: the success gate is inherited
  commented-out code (`services.py:146-148`, D-19, no IS-ID covers it); the
  ×2.5 exploit-time multiplier (`services.py:116-117`, beyond-paper per
  IS-TIM-06) is live for the **native arm only** — the movement layer declines
  all substrate pricing by design (`charge_time=False`, S3-R,
  `attack_operation.py:445-454`).

**Marc's hypothesis, reviewed.** The hypothesis was that OS Diversity sits on
its own layer because it was a later addition never integrated into the attack
operation. The conclusion is right; the history detail is not quite: OS
Diversity is Brown-era (§III-B(6), IS-MTD-06), and the un-integration is
inherited — the gate arrived commented-out, and the OS-dependency machinery
(`VULN_PROB_DEPENDS_ON_OS = 0.8`) is beyond-paper throughout (audit §l item 1).
Nothing in the lineage ever wired OS into exploitation success. The review
below must therefore treat "was it ever intended to be read?" as an open
classification question, not assume a regression.

**The generalisation that makes this systematic rather than anecdotal.** The
S3-R seam means the two arms have **different read surfaces**: any substrate
mechanism that expresses itself *only through time* (complexity scaling,
OS-mismatch multiplier, re-exploit discount ATK-04) is structurally invisible
to the movement attacker. So every cell of the matrix must carry a per-arm
verdict, and "live for the native arm" must never be silently read as "live".

## 3. Recommended approach — Part A (review / cross-examination; no code changes)

1. **Complete the coupling matrix.** Rows: every mutable network component —
   topology edges, host identity (node id), `ip`, `os_type`/`os_version`,
   service identity, service version, vulnerability set (incl. exploited
   flags), ports, users/credentials, target node, exposed endpoints, and the
   derived structures (`get_hacker_visible_graph`, path caches, scorer feeds).
   Columns: read-by (verb, arm), written-by (mechanism — cross-filled from
   brief 2), liveness verdict, evidence locator. Every cell carries a code
   locator; no cell is filled from memory of the papers or of prior audits.
2. **Live-verify every load-bearing cell.** A "read" claimed live must be
   demonstrated in a run — use the tracers (`python -m mtdnetwork.trace`;
   `PYTHONPATH=src python -m mtdsim.l3_simulation.trace`), extending them
   rather than print-debugging (they are living tools per `trace_tool.md`). A
   "dead" claim must be verified the way this session verified the
   compatibility test: by executing, not only reading (the 0-of-600 check is
   the template).
3. **Review the attack phases against the matrix** (Marc's explicit ask):
   for each of the six verbs, state what network state it *should* plausibly
   consult for the interaction to be "realistic" for research purposes, what it
   does consult, and classify each gap per §c
   (`mtdsim_intent_spec.md`): CONFORMS / CONFORMS-SUPERSEDED /
   DIVERGES-DOCUMENTED-NOWHERE / UNTESTABLE. **"Bug" is a verdict, not a first
   impression** — a dead coupling documented in no paper is a *candidate*, and
   only Marc's disposition makes it fixable.
4. **Produce the findings table**: every dead or partial coupling, classified,
   with costed options (repair / keep-and-document / re-scope the mechanism
   out of the reported family), golden impact stated per option, and a
   recommendation. D-18 and D-19 are already-open members of this table —
   consume their rulings, do not re-litigate them.
5. **Deliverable**: an implementation record
   (`docs/implementation/` per the placement criterion — this is
   codebase-shaped truth), plus the disposition requests appended to the
   intent-conformance audit's list (next free: D-20).

## 4. Part B (implementation; only after Marc's dispositions)

- Implement exactly the dispositioned changes, one logical unit per commit.
- The D-05 procedure, followed exactly: goldens re-baselined deliberately,
  logged in `baseline/CHANGELOG.md`, never `--no-verify`; SIM-05 determinism
  re-verified; full suite green.
- Each change lands with a regression test asserting the *repaired* coupling
  (template: gate 5 of the indistinguishability brief — assert the property
  whose absence let the defect survive).
- **No recorded experiment is re-run.** Changes create a new substrate version
  for future comparative runs; the comparability boundary is recorded in
  `metrics_semantics.md` terms (which recorded results remain internally
  comparable, which cross a substrate version).

## 5. The A/B cycle and the confidence gate (Marc's standing instruction for this programme)

After **every** Part A / Part B cycle, run a written **confidence evaluation**
before closing:

- **The question:** "Are we ≥ 95 % confident that no undispositioned dead,
  partial, or arm-asymmetric coupling remains at this boundary that could
  change a comparative MTD ranking?"
- **How it is answered — evidence, not vibes.** The confidence figure is a
  structured judgement against a checklist, not a computed statistic, and the
  evaluation must say so. It passes only if: (i) every matrix cell has a
  locator and a per-arm verdict; (ii) every live verdict has a run-level
  demonstration; (iii) every dead verdict has either a disposition or an open
  D-number; (iv) for every mechanism pair the recorded data leaves
  unseparated, a code-level cause is on record; and (v) an **adversarial
  pass** — a fresh look (fresh session or explicit red-team pass) that
  actively hunts for a coupling the matrix missed — found nothing new.
- **The residual-doubt rule.** The evaluation names its residual doubts
  explicitly. Any doubt that could plausibly move a ranking fails the gate.
- **If the gate fails:** open the next A/B iteration **scoped to exactly the
  named doubts**, update this handoff with the cycle's record (what was
  checked, what changed, what remains), and repeat. The handoff is deleted
  only when a cycle's confidence evaluation passes and Marc has seen it.

## 6. Validation gate

1. The coupling matrix exists as an implementation record, complete per
   §5(i)–(iii), with per-arm verdicts.
2. Every finding carries Marc's written disposition; Part B changes (if any)
   landed under the D-05 procedure with regression tests.
3. The verb-by-verb attack-phase review (Marc's ask) is on record, including
   the OS-layer question answered with its classification.
4. A passed confidence evaluation, written into this handoff's final update,
   naming residual doubts and why each is tolerable.

## 7. Hard constraints

- Classify before judging: `mtdsim_intent_spec.md` §c; only Marc's disposition
  makes anything a bug. Never fix from a paper–code mismatch.
- No recorded experiment is re-run under a changed substrate.
- Goldens move only via the D-05 procedure. Determinism (SIM-05) throughout.
- Two arms, two read surfaces: every claim states which arm it is about.
- D-18/D-19 are open and owned by the indistinguishability brief — consume
  their rulings here, do not duplicate them.
- Australian English; branch per session; commit locally; **never push**.

## 8. Reading list

- `mtdnetwork/operation/attack_operation.py` — the six `_do_*` cores
  (250-612), `step()` (684-770), the `charge_time` docstring (445-454).
- `mtdnetwork/component/adversary.py`, `mtdnetwork/component/host.py`
  (node attrs, users, `get_hacker_visible_graph` consumers),
  `mtdnetwork/component/network.py` (visible graph, path-from-exposed).
- `docs/implementation/intent_conformance_audit.md` — §j (procedure rows),
  §l (beyond-paper behaviours), the disposition list (D-18/D-19).
- `docs/implementation/substrate_primer.md` — the attacker's-eye terrain view.
- `docs/implementation/trace_tool.md` — the verification instrument.
- [`2026-08-02_os_service_diversity_indistinguishability.md`](2026-08-02_os_service_diversity_indistinguishability.md)
  — the lead finding and the verification template.

## 9. Out of scope (explicitly)

- The write side of the matrix (brief 2) and the direct attacker/defender
  channels (brief 3), beyond cross-filling shared cells.
- Building attacker capabilities (axis-8 scheme awareness is ruled out;
  `adversary.observed_changes` stays unwired).
- Re-running or re-analysing recorded experiments.
- Dissertation prose.
