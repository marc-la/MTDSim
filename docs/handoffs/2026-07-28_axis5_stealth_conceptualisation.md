---
status: open
created: 2026-07-28
---

# Conceptualise stealth for a substrate with no detector — settle what the stealth state *is*, what it buys, and what it costs, before any of it is built

**Chain position: wave 5, design-only, and the one item on this chain that ends in a
question rather than a build.** It can start immediately and in parallel with everything
else, because its deliverable is a design record and a decision request. Its *build* half
depends on `2026-07-28_attacker_state_seam.md` and on a ruling from Marc, and should not be
opened until both exist.

**Read this handoff as a brief to think, not a brief to implement.** Several of the
questions below have no obviously right answer and at least one of them is genuinely
Marc's to decide with the supervisor. A session that produces a well-argued design record
and a clean list of resolved and unresolved questions has succeeded; a session that ships a
stealth mechanism without settling question 1 has not.

## State of play

**The idea, as Marc framed it.** The Petri net contains a `stealth` place. When the token
lands there, the attacker becomes more stealthy — a stealth level on the attacker model —
and that level feeds back into the success/failure weight sets at runtime. The direction is
right and the place exists in **all five profile nets**, which is unusually good coverage
for a mechanism of this kind. What the idea does not yet contain is an answer to what
stealth *does*, and that is the whole difficulty.

**The crux, stated bluntly: there is nothing to be stealthy against.** The substrate has no
detection model in either direction. There is no alert, no attacker-noise concept, no
defender observation of attacker activity anywhere in `mtdnetwork/`. The MTD interrupt is a
blind collision — the defender mutates on a schedule and interrupts the attacker only if
its current process happens to be one of the surface-dependent verbs. IDS is culled from
the research threads by standing project direction, which says in terms: **do not build
IDS/detection features**. Tay's detection-sensitivity machinery is retained only as an
inherited benchmark defence to replicate, never to extend, and deferred to the ablation
phase. So the ordinary meaning of stealth — reducing the probability of being detected — has
no referent here, and any mechanism that quietly assumes one is unbuildable.

**The project has already written this down, in the tactic profile itself.**
`docs/notes/ch3_design/tactic_profiles/07_stealth.md` §3: *"detection is culled from the
substrate, where 'caught' means MTD invalidated progress, never an IDS saw you… Because
there is no detector to hide from, stealth's gain has no direct substrate representation…
This is the honest frame: a stealth tactic gets a time, not a detection model."* And the
criterion's axis 5 says the same from the other side: movement through evasion-named tactics
exists but carries no stealth semantics, and *tempo alone is still not evasion*. Any design
that contradicts these two statements has to argue against them explicitly, not around them.

**The half that is already built, and is stronger than the criterion currently records.**
The criterion describes S3's timing regime as the nearest open direction, "CONJECTURED:
ruled, with design and build handoffs open". Both of those handoffs have since shipped.
Each tactic's dwell is now a draw about a declared mean; `stealth` carries a mean of 45 s,
the longest tier alongside persistence and command-and-control, on the widest sweep band and
the weakest evidence tier; under the `v2_partial` mapping it is **dwell-only**, so a stealth
visit today consumes 45 seconds of simulated time and dispatches nothing at all. The model
therefore already has a tempo axis. What it does not have is any consequence attached to it.

**And the rate study found that this dial is the most consequential parameter in the whole
model.** Of the four timing group anchors swept, **only `stealth-low-and-slow` moves any
outcome**: pooled host breadth runs from 7.82 ± 1.21 at a quarter of its declared value down
to 1.78 ± 0.36 at four times it, both ends separated from the centre, while the scan,
exploit and objective anchors are inert across their bands. The stealth tempo dial is
already, empirically, where this model's behaviour lives. That is the strongest possible
starting point for a stealth design and it should be the record's opening argument.

**What the CTI corpus can and cannot ground.** It carries genuine per-tactic *qualitative*
observability evidence — passive reconnaissance is "the least risky… characteristic of an
APT behavior" while active reconnaissance is "generally a sign of an ongoing attack";
command-and-control is a "persistent, low-signal channel… mimicking normal, expected
traffic"; defence-impairment is a "higher-privilege, higher-signal" act preceding a noisy
payload; credential access makes the adversary "harder to detect"; impact is the fast, noisy
objective mode. That is enough to rank the fifteen tactics on an ordinal exposure axis. It
carries **no magnitudes at all** — no per-tactic detection probability anywhere. The only
quantitative anchors in reach are Jafarian's detectability ratio (defender-side
detectability of scanning) and Outkin's ATT&CK-Evaluations-fitted per-step detection
probabilities, and the extraction for the latter explicitly records it as **not transferable
to SDR-family MTD without a calibration step that does not exist in the public record**.

## The open questions

These are the deliverable. Answer them in the record; escalate the ones marked as Marc's.

**1. What is stealth against? — the crux, and partly Marc's call.** Three candidate
semantics, in the order they should be evaluated:

- **(a) Stealth as tempo, with exposure reported as a metric.** The stealth state slows the
  attacker (raises dwell means) and lowers a reported *exposure* figure — attack events per
  unit simulated time, dwell fraction in non-action places, tempo response to MTD frequency,
  which is precisely the criterion's own M8b candidate list. Nothing in the simulation
  responds to exposure; it is an observable, not a mechanism. **Recommended baseline**, and
  the honest ceiling it implies must be stated: this moves axis 5 from NOT ADDRESSED to
  DESIGNED, and cannot reach DEMONSTRATED, because a metric nothing responds to has not been
  shown to change an outcome.
- **(b) Stealth with teeth, via a reactive defender.** Tay's reactive selection agent is the
  only existing coupling in this codebase where attacker activity could plausibly feed
  defender behaviour. If it does, then including it unchanged as one of experiment 2's
  defence families makes exposure consequential **without building any detector**. Two things
  gate this: **verify what Tay's agent actually keys on** before proposing it — the state of
  play above suggests the substrate offers no attacker-activity signal at all, in which case
  this option collapses — and then get a ruling, because Tay's machinery is deferred to the
  ablation phase and the "replicate, never extend" boundary is narrow. **This is Marc's
  decision, and it is the one worth asking about**, because it is the difference between
  axis 5 reaching DESIGNED and reaching DEMONSTRATED.
- **(c) Stealth as a success-rate buff.** Rejected, and the record should say why: with no
  detector, stealth raising the probability that an action succeeds is a free bonus with no
  mechanism behind it. Nothing in the model would explain why an attacker would ever choose
  *not* to be stealthy, and choosing the buff's magnitude so that stealth "matters" is
  reverse-engineering a benefit — the exact thing the declared-value guardrails forbid.

**2. What does stealth cost, and is the trade real?** A stealth state that only confers
advantage is incoherent. The defensible cost is **time**: stealth is low-and-slow, so a
higher stealth level raises dwell means. That makes the trade real and, crucially, makes it
interact with the defence *without a detector at all* — MTD's temporal churn taxes exactly
the time budget stealth spends, so a stealthier attacker eats more mutations. This is the
one genuine stealth-versus-MTD mechanism available on this substrate and the record should
develop it carefully. Cho's framing supports it directly: the stealthy attacker "trades
speed for observation time", which is "precisely the budget MTD's temporal churn is supposed
to tax".

**3. Does a movement-layer stealth state violate the S2 freeze?** S2 forbids adding attacker
states. The argument that a movement-layer state is not an MTDSim attacker state belongs to
`2026-07-28_attacker_state_seam.md`; this handoff should not re-derive it, but must not
proceed as though it is settled either. Flag it once, point at the seam handoff, and move on.

**4. Does stealth modulate routing, dwell, both, or neither?** Routing means the stealth
level changes which move comes next; dwell means it changes how long each takes. These are
different claims with different evidence. Dwell is the better-grounded of the two (the tempo
argument above); routing is what Marc's original framing described. If routing, note that
under `v2_partial` the `stealth` place is **dwell-only and therefore never calls `compose`**,
so the seam handoff's dwell-only routing change is a hard prerequisite.

**5. How does the stealth level rise and fall?** Does it accrue on every visit to `stealth`
and decay with time, or with each noisy action taken? Is it bounded, and where? The corpus's
ordinal noisiness ranking is the natural source for which tactics spend stealth, but ranking
is not magnitude — whatever is chosen is declared judgement and must be swept.

**6. Is exposure a metric or a mechanism?** This is question 1 restated in the criterion's
own vocabulary, and it decides the badge ceiling. Answer it explicitly rather than letting
the implementation decide it by accident.

**7. How do three modulators compose?** Stealth, learning and incentive all multiply into
the same routing composition. A stealth level that slows the attacker interacts with a
utility factor whose cost term *is* duration — a slower attacker makes every tactic look
more expensive, which is either a nice emergent coupling or a hidden double-count. Work out
which before both are switched on together, and say what the sweep has to cross.

**8. What does the distribution-shape corner mean for a mechanism that raises dwell?** The
rate study found the mean-is-load-bearing defence has a boundary: at long stealth dwells
under mutation pressure, a same-mean Erlang-4 costs the attacker roughly two-thirds of what
little breadth it had. A stealth mechanism that raises dwell means moves the model **into
exactly that corner**, where the exponential's mode-at-zero — the least realistic feature of
the timing choice, and the one quietly working in the attacker's favour — stops being
inert. Any stealth design that raises dwell has to address the distribution family rather
than wave it through on the mean.

## Recommended approach

1. **Verify before designing.** Establish what Tay's reactive agent keys on. Question 1(b)
   lives or dies on it, and the answer is a few hours of reading.
2. **Write the design record**, structured on the eight questions, in the shape the outcome
   overlay's own design record uses: the semantics, the composition rule, the declared
   values with tiers, the alternatives named and killed, the honest caveats. Its deliverable
   is a decision, not code.
3. **Take the tempo baseline (1a) as the default** unless the Tay verification opens 1(b).
   Build it on the seam once that lands: a stealth level rising on `stealth` visits, scaling
   the dwell means, with an ordinal per-tactic exposure weight rule-generated from the
   corpus's qualitative ranking and swept.
4. **State the badge ceiling in the record.** Under (a), axis 5 reaches DESIGNED and no
   further. Writing that down before building is what stops it being quietly over-claimed
   later, and it is the constraint the criterion's own "does not promise the world"
   requirement imposes.
5. **Put the unresolved questions to Marc as a short list**, with a recommendation on each.
   Question 1(b) is the only one that needs the supervisor.

**Alternatives considered.** *Build a minimal detector so stealth has a referent* —
rejected, and firmly: it is forbidden by standing project direction, it would need a fresh
comparability argument against every baseline, and Outkin is the only pipeline that could
ground per-step detection probabilities while its own extraction records it as
non-transferable to this defence family. *Reuse the evasion-named places as stealth without a
state* — that is what exists now, and the criterion already scores it as carrying no stealth
semantics. *Defer axis 5 entirely to future work alongside axis 8* — defensible, and the
record should say why it was not taken: the tempo half is already built and is empirically
the model's most consequential parameter, so leaving it unclaimed understates what the model
does.

## Validation gate

Done when:

1. A design record exists under `docs/implementation/pipeline/ogasp/` answering all eight
   questions, marking each as resolved or escalated, with the alternatives named and killed.
2. The Tay verification is on record with a yes-or-no answer and its evidence.
3. The badge ceiling implied by the chosen semantics is stated explicitly.
4. A short decision request is written for Marc, with a recommendation on each open item.
5. **If, and only if, a build follows:** the null configuration reproduces the current record
   stream field for field; the exposure weights are rule-generated, tiered and swept; the
   distribution-family question (8) is addressed rather than assumed.

## Hard constraints

- **No IDS, no detector, no detection features.** Standing project direction, not a
  preference. This is the constraint the whole design must route around.
- **Tay's machinery is replicate-never-extend** and deferred to the ablation phase. Using it
  unchanged as a defence arm may be sanctioned; extending it is not, and neither is assumed.
- **Do not choose a stealth benefit magnitude so that stealth "matters".** That is
  reverse-engineering, and on this axis it is the obvious temptation.
- **The S2 freeze question is open**, not settled. Flag it; do not build through it.
- **Envelope, not actor.** A stealth level is a declared behavioural parameter, never a claim
  about how a real adversary hides.
- Determinism / SIM-05; within-substrate comparability only; Australian English; branch and
  commit rules from [`../workflows/session_workflow.md`](../workflows/session_workflow.md);
  never push.

## Reading list

- `docs/notes/ch3_design/tactic_profiles/07_stealth.md` — the project's own position, §3 in
  particular; read this before anything else, because it already answers part of question 1.
- `docs/implementation/apt_model_criterion.md` §(d) axis 5 — the literature framing, the
  NOT ADDRESSED reasoning, and the M8b candidate measurements.
- `docs/implementation/pipeline/ogasp/rate_feasibility_study.md` §8 and §10 — the stealth
  anchor as the only anchor that moves an outcome, and the distribution-shape corner that
  question 8 turns on.
- `docs/implementation/pipeline/ogasp/stochastic_timing_design.md` §3.1–§3.2 — the tempo
  regime, the exponential's weakness for the low-and-slow group, and the mean-is-load-bearing
  defence with its stated leak.
- `docs/notes/ch3_design/tactic_profiles/01_reconnaissance.md`, `08_defense-impairment.md`,
  `13_command-and-control.md` — the qualitative observability evidence an ordinal exposure
  ranking would be built from.
- `docs/workflows/project_context.md` — the IDS culling and the Tay boundary, stated as
  standing direction.

## Out of scope (explicitly)

- Building anything before questions 1 and 3 are answered.
- Any detection model, alert, or attacker-visibility mechanism in the substrate.
- Extending Tay's agent in any way.
- Fitting a stealth parameter to make the attacker perform better.
- The measurement suite's exposure metrics — those are listed there but must not be built on
  an assumed stealth semantics, which is precisely what this handoff exists to settle first.
- Dissertation prose.
