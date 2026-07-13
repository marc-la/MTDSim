# Evans, Nguyen-Tuong & Knight 2011 — Effectiveness of Moving Target Defenses (extraction notes)

> The foundational analytical model of MTD effectiveness (Chapter 2 of the
> Springer *Moving Target Defense* volume — the book the whole field cites).
> Extracted **for §3 (MTD interaction) across every tactic** and as the canonical
> statement of the reset-vs-attacker-race mechanism. Its load-bearing message —
> *MTD's benefit is "often much less significant than one would expect", and is
> conditional on the attack class and the re-randomisation rate* — directly
> disciplines the §3 reset verdicts (not every shuffle invalidates every gain)
> and the sweep widths.
> Source file: `docs/sources/tactic_profiles/step_d/4_exec/978-1-4614-0977-9.md`
> (gitignored; the full edited volume — Chapter 2 is the value section, pp. 29–46).

### Relevance class

**M** (MTD-mechanism / attacker-effect). The reference model behind Anderson,
Carroll, Crouse; the per-attack-class taxonomy of *when a shuffle helps*.

### Used in lit review

§3 reset-verdict reasoning for all tuned tactics (esp.
[`04_execution`](../../notes/ch3_design/tactic_profiles/04_execution.md)); the method note's
"declared MTD-effect is the genuine unknown" — Evans supplies the *mechanism*,
not a per-tactic number.

## Bibliographic anchor

- **Citation key**: `evans2011`
- **DOI / URL**: https://doi.org/10.1007/978-1-4614-0977-9_2 (Springer AIS 54)
- **Pages cited from**: Chapter 2, §2.3–2.6 (pp. 33–46).

## Relevant artefacts

### The model — the attacker races to exploit before re-randomisation

**Source locator:** §2.3 (Model); §2.5.4 (Probing)

**Paraphrase:** two players; the attacker knows a vulnerability, the defender
runs a key-dependent transform `STk` re-randomised over time. **`te` = time from
starting the exploit to compromise; an exploit constructed at t₁ fails if it can
only be launched at t₂ after a re-randomisation** [fetched]. This *is* the
reset-vs-dwell race in its original form. Crucial realism check: for probing
attacks the exploit "can be constructed automatically based on the probe
information, so the time between the probe and attack launch is effectively just
the network latency for two round trips" — i.e. the re-randomisation must beat a
*very* short window to help.

**Maps to:** §3 of every tuned tactic — the reset verdict is "does the shuffle
fire inside the attacker's te?" ([`mtd_scan_disruption`](mtd_scan_disruption.md)
Crouse's interval-ratio is the same idea).

**Disposition for this thesis:** verified [fetched] — the canonical mechanism.

---

### The per-attack-class taxonomy — MTD helps only sometimes (Table 2.1)

**Source locator:** §2.4 (attack strategies); §2.5 + Table 2.1 (Impact of Dynamic
Diversity)

**Paraphrase:** dynamic diversity's benefit depends entirely on the attack class
[fetched]:
- **Circumvention** (ROP/return-to-libc, higher-level SQL/logic attacks that
  don't depend on the randomised property): **No advantage.**
- **Deputy** (repurpose the program's own de-randomisation code): **No advantage.**
- **Brute-force / entropy-reduction** (NOP sled, heap spray): **at most doubles
  expected attack time** (+1 bit — sampling without→with replacement).
- **Probing**: only a "very high rate of re-randomisation may thwart" (window ≈ 2
  round-trips).
- **Incremental** (many probes, one key-fragment each): **may provide significant
  advantage** — the one class MTD strongly disrupts.

**Emergent (load-bearing for §3):** the *modality* of the attacker action decides
whether a shuffle resets it. For **execution**, this is decisive — **fileless /
script / living-off-the-land execution (the APT-preferred mode, per
[`alshamrani2019`](alshamrani2019.md)) is a *circumvention/higher-level* attack →
MTD gives no advantage**, whereas memory-corruption code-injection *is* disrupted
by ASLR/ISR re-randomisation. This directly reconciles execution's "unsettled
group": the low-and-slow script-execution the corpus describes is *reset-immune*
to the memory-diversity MTD, arguing against a strong reset and for a wide sweep.

**Maps to:** [`04_execution`](../../notes/ch3_design/tactic_profiles/04_execution.md) §3 (script
execution circumvents memory-MTD → weak reset, wide sweep) + §2 (the group
reconciliation); §3 of any tactic where the attacker uses stolen material vs a
fresh exploit.

**Disposition for this thesis:** verified [fetched] — the sharpest available
argument that a reset verdict must be *per-modality*, not blanket.

---

### The re-randomisation rate dominates — 6 orders of magnitude

**Source locator:** §2.5.5 (Incremental Attacks, Fig. 2.2)

**Paraphrase:** for the incremental case, re-randomising **every 4th vs every
100th probe spans ~6 orders of magnitude** in attack-success probability
[fetched]. Re-randomising only every 50th/100th probe → attack success "quickly
exceeds 90%" (MTD effectively useless); only very fast re-randomisation (every
~4–25 probes) helps. Achievable in some implementations (ISR XOR-key
re-randomisation every 100 ms at ~14% overhead), but "prohibitively costly" as a
general network-message-rate defence. Shacham's brute-force on PaX ASLR succeeds
in ~216 s on average.

**Maps to:** the **sweep-width justification** for every tuned tactic — MTD
effect is hypersensitive to the shuffle-interval ÷ attacker-action-time ratio, so
a wide sweep on that ratio is mandatory, not optional
([`../notes/2026-07-04_operational_validation_the_bar.md`](../../notes/ch3_design/operational_validation.md)).

**Disposition for this thesis:** verified [fetched] — quantifies why §3 declares
a verdict *and a wide range*, never a point.

## Open questions / things to verify

- Evans models *low-level memory diversity* (ASLR/ISR/data randomisation), not
  network address shuffle. The transferable finding is the **attack-class
  conditionality** and the **rate-sensitivity**, not the specific memory
  mechanism. The substrate's MTD is network/service SDR — map the *shape* (which
  attacker actions a diversity move resets), not the memory specifics.
- The "no advantage against circumvention" result is the strongest single
  argument for a *per-modality* reset verdict; worth foregrounding in Step E.

## Out of scope for this thesis

The ASLR/ISR/data-randomisation implementation surveys (§2.2); composition and
N-Variant Systems (§2.6) — defence-design, not attacker dwell; the rest of the
edited volume (other chapters are separate MTD techniques, not read here).
