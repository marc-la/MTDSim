---
status: open                  # standing context for dictating ch2 §2.2.2; retire when the unit is through pass 6
created: 2026-08-27
---

# §2.2.2 Defence mechanisms — the academic context for the dictation, as it stood before and after the 2026-08-27 pool changes

**Mode note.** Marc dictates the unit; a session scaffolds and scrutinises
([`../workflows/draft_scrutiny.md`](../workflows/draft_scrutiny.md)). Nothing
below is a sentence for the chapter. It is the content spine, the points Marc
has already argued elsewhere in the record, the facts each sentence must
carry, and the traps — refreshed so a session that did not live through the
2026-08-27 changes can brief the unit without inheriting either the old
four-mechanism picture or a lopsided account of the new one.

Companions, authoritative on shape and craft:
[`2026-08-21_ch2_background_context.md`](2026-08-21_ch2_background_context.md)
(budget, skeleton, boundaries — Part 2 (d) gives this unit ~300 words),
[`2026-08-21_ch2_lineage_description_precedents.md`](2026-08-21_ch2_lineage_description_precedents.md)
(precedents 9–12 and the anti-pattern board), and
[`../notes/ch2_background/README.md`](../notes/ch2_background/README.md)
(the two placement tests). Facts: the pool-restoration brief (retired 2026-08-30; `git show d127f443:docs/handoffs/2026-08-27_mtd_pool_restoration.md`)
(the ruling trail and the traced verification), [`../implementation/mtd_write_surfaces.md`](../implementation/mtd_write_surfaces.md),
[`../implementation/substrate_primer.md`](../implementation/substrate_primer.md) §(c)/(e).

---

## 1. What changed on 2026-08-27, in one table

The context brief of 2026-08-21 and the first scaffold of this session (same
day, morning) were written against the *four-mechanism* pool. The afternoon's
rulings changed the roster and one mechanism's nature. A future session must
describe the platform **as it is now**, and must not describe the old state as
the platform's design — but it should know what moved, because the lineage
papers and every record before 2026-08-27 describe the old state.

| Before (what the 2026-08-21 brief and the lineage describe) | After (ruled 2026-08-27) | Where recorded |
|---|---|---|
| Four reported mechanisms (Zhang's selection of Brown's pool): IP shuffle, complete topology shuffle, OS diversity, service diversity; four latent, defective or unexercised | **Seven working mechanisms** — the four plus host topology shuffle (D-31 repaired), user shuffle (D-32/D-26 repaired), port shuffle (activated as-is). Two named pools: `lineage` (the four, default — every recorded experiment, Tay's action space) and `full` (seven) | pool handoff; `mtd_scheme.py` `MTD_POOLS` |
| OS diversity assignment (Zhang's DAP variant) latent and broken | **Withdrawn** by ruling D-17(c): solver never coupled, the idea presupposes a server class the untargeted arm lacks, and (then) an unpriced OS axis | audit §n banner |
| OS diversity = service diversity plus a dead relabel (guard inert, D-18; OS success gate commented out, D-19) | **OS diversity is a distinct mechanism**: the guard repaired (redraws only the services the new OS makes incompatible, by (name, version)); the OS-gated exploit success channel reinstated (an OS-dependent vulnerability fails on a host whose OS it does not cover; the refused attempt counts) | audit D-18/D-19 rows; provenance rows |
| Two landings for the layer-reading: shuffles rewrite the host layer, diversity the service layer | **Three landings**: shuffles → host layer (position); diversity → service layer (surface); **user shuffle → credentials** (Brown's third interaction class, neither layer) | pool handoff "Consequences" |
| Exposed endpoints exempt from IP/OS/service mechanisms; user shuffle touched every host | Endpoints exempt from **all seven** (R2 applied to user shuffle; CTS moves endpoint adjacency but never the endpoint hosts) | write surfaces §(b)1, §(c) |
| The terrain: exploit success on complexity alone | **Exploit success now also requires the host OS to be in the vulnerability's OS list** (~40 % of vulnerabilities carry one: cross-platform services × 0.8). Fires with or without a defence — a terrain fact, so every baseline moved | provenance "OS-gated exploit success" |

Everything else in the 2026-08-21 brief stands: budget, the §2.1 → §2.2.2
wiring, the execution schemes, the reactive selector [→ MTDShield, classified hybrid; ruled 2026-09-02], the metrics-to-ch4
ruling, the no-figure-in-this-unit ruling (Figure 2.1 is the preamble's).

## 2. The unit's job, as ruled (unchanged)

- ~300 words; the dense unit — the ~125 words freed by folding the opener and
  *Prior work* into the §2.2 preamble were spent here.
- Three things in the order Figure 2.1 draws them, left to right: **roster →
  execution scheme → reactive selector [→ MTDShield, classified hybrid; ruled 2026-09-02]**. Opens on the defence box.
- **§2.1's vocabulary must be cashed in the first two sentences** or it was
  decoration (README rule; Zhang taught-never-used and Ho used-never-taught are
  the two failures it repairs). Each mechanism arrives wearing its class; the
  schemes are *proactive*; the selector *reactive*.
- **The honest scope note lands here**: shuffle and diversity only, no
  redundancy. §2.1 defined redundancy so its absence could be stated; ch6 leans
  on it. Tay teaches redundancy and never says the platform lacks it.
- Descriptive register: describe and stop. No fairness verdicts, no
  description-by-limitation (Ho's "can only deploy…"), no lineage headlines.
- Nothing enters that ch4/ch5 does not lean on. Leaned on: the layer-landing
  reading (reset model, disruption-channel results), scheme/interval as the
  *when* axis (timing results), the no-op selector as an L4 arm, the
  no-redundancy note (ch6), and now the two pools (ch4 comparability: family-1
  re-runs use `lineage`, the fresh evaluation `full`). Not leaned on: priority
  numbers, queue mechanics, durations, Tay's architecture, the withdrawn DAP
  beyond one clause.

## 3. The content spine (post-update)

**0. Opening (two sentences).** Shuffle and diversity only, no redundancy. The
two families as attacker-effect, echoing §2.1 S7/S8: shuffles rename or
relocate a resource without changing what it can do; diversity changes the
software stack so a vulnerability already found no longer applies.

**1. The roster — seven, in Brown's pool, wearing labels (~110 w).** Brown
built the pool; Zhang ran four of it; this thesis restores the pool with the
three latent mechanisms repaired (attribution as clauses, never a section).
- *Shuffles — rewrite the host layer*: **IP shuffle** reassigns every internal
  host's address; **complete topology shuffle** regenerates the graph, host
  instances and their compromise state kept; **host topology shuffle** swaps
  hosts' positions within a level of depth (same-level constraint is Brown's;
  the level is the `layer` attribute, i.e. depth, not the subnet).
- *Diversity — rewrite the service layer*: **service diversity** redraws every
  non-target service on internal hosts; **OS diversity** changes each internal
  host's operating system (version index kept) and redraws only the services
  the new OS cannot run — and, because exploits are OS-specific, the
  vulnerabilities the attacker knew on surviving services may no longer apply.
- *Port shuffle* (a shuffle on the service layer's addressing): moves every
  non-target service's port; services and vulnerabilities untouched.
- *User shuffle* (credentials): redraws each internal host's user accounts from
  the network's pool; a harvested credential stays valid wherever that account
  re-seats (Brown's mechanism, ruled R1).
- One clause, if the budget allows: the DAP-optimised variant is withdrawn.

**2. The organising reading (1–2 sentences; what ch4/ch5 collect on).** Sort by
*which layer of the terrain each mechanism rewrites and therefore which attacker
gain it threatens*: the shuffles move where things are and what reaches what
(the attacker's *map*); the diversity mechanisms change what an exploit must
match on a host already reached (the *exploit working set*); user shuffle
changes which credentials are valid. Brown §III-D is the precedent (connection
to host lost / connection to service lost / user access changed); Figure 2.1's
accented arrows draw the first two. Wear *host layer / service layer /
credentials*; not "direct/indirect", not OSI.

**3. The uniform exemption profile (one sentence).** Across all seven: exposed
endpoints are never rewritten (back-reference §2.2.1, do not re-explain); what
the attacker has compromised persists; a service redraw changes what is *at*
an address, never the address. This is the reset-model pre-install — describe,
do not argue.

**4. The execution schemes — *when*, proactive (Zhang; ~70 w).** All
time-triggered on a periodic signal, §2.1's proactive regime by name. What
differs is what registers on each signal: *random* (one mechanism drawn at
random — what Brown effectively ran), *alternative* (one, by fixed rotation),
*simultaneous* (all; contention on a shared layer resolved by priority and a
suspension queue), and *single* (one fixed mechanism — what this thesis's
experiments run). Interval drawn exponentially (Zhang's replacement of Brown's
uniform), one clause; values to ch4. Resource rule in one clause: two
mechanisms serving the same layer cannot deploy concurrently. Do not lift
Zhang's worked example — it mis-places complete topology shuffle on the
application layer.

**5. The reactive selector [→ MTDShield, classified hybrid; ruled 2026-09-02] — *when*, reactive (Tay; ~60 w).** The review's
cleanest port (`LIT_REVIEW.md:87`): a DDQN reading network security metrics at
each evaluation tick and selecting one of **five actions**, the lineage four
plus **no operation**. Marc's point, already made: the fifth action encodes
*restraint as a policy choice rather than a global interval parameter* — the
reactive regime's answer to *when not to move*. Deploys through the same
MTD-operation path, an alternative feeding the same slot as the schemes. Its
action space is the lineage pool, not the full one (a ch4 sentence, not this
unit's). Architecture and V3 (as-is, no retraining) stay out.

**6. Closer (optional, ≤1 sentence).** Which mechanisms, under which scheme, at
what interval are parameters of a run, not properties of the simulator — the
axis the evaluation varies.

## 4. Points Marc has already argued, which this unit carries or protects

- *Describe once; attribution as clause.* "The execution schemes Zhang added",
  "the selector Tay added", "the pool Brown built" — never a lineage paragraph.
- *Position versus surface needs "what to move" posed first* — §2.1 did that;
  this unit collects on it.
- *Brown's per-mechanism template* (real-world grounding → implemented-as →
  what it interrupts), compressed to a sentence each and opened with its class;
  when cutting, keep *what it invalidates for the attacker*.
- *The pool is restored, not extended* — no novel defender (architecture
  decision); the contribution on the defence side is fidelity to the four
  papers, so "which mechanisms dominate, and is that stable across the
  lineage's own conditions" is answerable over more rows.
- *The OS label must reach the attack operation* (Marc, 2026-08-27): moving the
  OS should disrupt the attacker implicitly through exploit applicability, not
  only through a service redraw. That is what the reinstated gate does; the
  chapter states it as what OS diversity *is*, not as a repair.
- *Port shuffle is a pure interrupt mechanism by Brown's own reading* (§V:
  "the attacker simply needs to reconnect and then exploit the same
  vulnerabilities") — ch2 describes it; the pairing with IP shuffle as the two
  interrupt classes is ch6's ([`../notes/ch7_discussion/pure_interrupt_pair.md`](../notes/ch7_discussion/pure_interrupt_pair.md)).

## 5. Traps — the standing warning, updated

*Facts from the records, not the papers; every behavioural claim traceable.*

- **Do not describe the pre-2026-08-27 state as the design.** Every record
  dated earlier, the 2026-08-02 family sub-study, experiment 2's diversity
  numbers, and the first scaffold of this session say OSD ≡ SD and the pool is
  four. They are superseded and annotated; the chapter describes the platform
  as it is. Equally, do not narrate the repairs in ch2 — that the guard was
  inert or the gate commented out is ch4 comparability material (one sentence
  there), not background.
- **Intent verbs are Brown's design, not measured behaviour.** "Interrupts any
  attacker using a stale IP" is the paper; against the movement attacker IP
  shuffle writes nothing the attacker reads and reaches it only through the
  network-class interrupt (D-20). Ch2 states what each mechanism does *to the
  network*; the interrupt semantics and class-level pricing are ch4's.
- **The OS gate is terrain, not a mechanism.** It fires in undefended runs
  too. If the unit mentions it, it is as the reason OS diversity bites (exploits
  are OS-specific), not as something the defence does.
- **Ports do not move when services do** (a redraw changes what is *at* an
  address); worth one clause because ch4's reset discussion leans on it.
- **Priority ordering and durations exist in code, not in any paper**
  (IS-SCH-06, IS-TIM-03); declared in provenance; no numbers in ch2.
- **Host topology shuffle's visibility consequence**: a swapped foothold stays
  compromised but can leave the attacker's visible subgraph if its new position
  has no compromised neighbour — the substrate's visibility model (CTS has it
  too). State it in ch2 if a sentence is spare; ch4 leans on it.
- **User shuffle's explicit channel is rare by design** (blocks only
  mid-brute-force, IS-INT-03); its effect is mostly implicit through
  credential reuse. Describe the mechanism, not its rarity.
- **Zhang's resource-layer worked example** places CTS on the application
  layer; the code and IS-MTD-09 put it on the network layer.
- **Vocabulary**: *no operation* / *no-op* — pick one (the tex's §2.1 comment
  says "no-op", the review "no operation"); reserve the word for the selector
  (a non-firing user shuffle is not a "no-op"). Registry rows still unratified:
  the seven mechanism names in lower case (*IP shuffle*, *complete topology
  shuffle*, *host topology shuffle*, *port shuffle*, *user shuffle*, *OS
  diversity*, *service diversity*), *execution scheme*, *the selector* vs
  *Tay's agent*, *pool* (*lineage pool* / *full pool*).

## 6. Precedents to reuse, and the corpus's bar (unchanged; see the precedents brief)

Brown's per-mechanism template and §III-D grouping (items 9–10); Zhang's
schemes by distinguishing action, one clause each (11); the Tay-paragraph shape
for the selector (12). Anti-patterns to sweep against: vocabulary taught but
never cashed, description by limitation, the prose flowchart, frameworks
over-taught, and describing the papers' intent as the code's behaviour — the
last now with a second instance (the OS gate *was* Brown's stated intent and
was not the code's behaviour until 2026-08-27).

## 7. Downstream consequences already booked (not this unit's to draft)

Figure 2.1's roster box (seven entries; a credential landing for user shuffle;
regenerate via `tools/mtdsim_model_figure.py` — its validation reads
`_mtd_strategies`, which is now the *lineage* list; decide whether the figure
draws the lineage pool or the full one, and say which in the caption); Table
2.1's Brown row (*what this thesis inherits* widens to the full pool); the ch4
comparability sentence (two pools; the OS gate moves every baseline; pre-ruling
diversity numbers not comparable); the seeded per-mechanism measurement over
the full pool before any ranking is quoted.

## 8. Budget pressure

Seven mechanisms × (class + what it rewrites + what it invalidates) ≈ 160 w,
schemes ≈ 70, selector ≈ 60, opening + scope note + exemption sentence ≈ 40 —
about 330 against 300. The disruption-channel grouping is where the
compression lives: describe the three shuffles as a group and the two diversity
mechanisms as a group, name port and user shuffle once each by what they move.
If it still overflows, the closer goes first, then the DAP clause.
