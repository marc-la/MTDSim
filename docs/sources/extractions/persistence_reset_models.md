# Persistence reset models — FlipIt & self-cleansing (extraction notes)

> The game-theoretic and system models of **periodic reset vs a stealthy,
> persistent foothold** — extracted for §3 of the durability tactics
> ([`05_persistence`](../../notes/ch4_methods/tactic_profiles/05_persistence.md),
> [`07_stealth`](../../notes/ch4_methods/tactic_profiles/07_stealth.md),
> [`13_command-and-control`](../../notes/ch4_methods/tactic_profiles/13_command-and-control.md)). These
> answer the core §3 question directly: *when does a defender's periodic move
> invalidate a persistent gain, and how fast must it move?* All three price the
> **reset-rate ÷ compromise-rate ratio** — the same lever as the scan-shuffle
> papers, applied to a held foothold.
> Source files (all `docs/sources/tactic_profiles/step_d/5_persist/`, gitignored):
> `s00145-012-9134-5.md` (FlipIt), `Incorruptible_system_self-cleansing…md`
> (SCIT), `TSP_CMC_64849.md` (Sun, Stackelberg-FlipIt).

### Relevance class

**M** (MTD-mechanism / attacker-effect). The reset-verdict + sweep-width evidence
for the persistence/stealth/C2 group.

### Used in lit review

Persistence/stealth/C2 §3 (declared reset verdict + the move-rate sweep); the
reset-vs-dwell ratio for the tuned groups.

## Bibliographic anchor

- **Citation keys**: `vandijk2013_flipit` (van Dijk, Juels, Oprea, Rivest,
  *FlipIt: The Game of "Stealthy Takeover"*, J. Cryptology 26(4), 2013);
  `huang2006_scit` (Huang, Arsenault, Sood, *Incorruptible System Self-Cleansing
  for Intrusion Tolerance* (SCIT), IEEE IPCCC 2006); `sun2025_flipit` (Sun, Fei,
  Zhu, Guo, *MARL for MTD Temporal Decision-Making (Stackelberg-FlipIt)*, CMC
  84(2), 2025).
- **Pages cited from**: FlipIt Abstract + §1 + §4 (renewal-game results); SCIT
  §1–§5 (garbled OCR — mechanism read, exact figures `[parse-uncertain]`); Sun
  §1–§4.

## Relevant artefacts

### FlipIt 2013 — the stealthy-takeover game: move-rate ÷ cost decides control fraction

**Source locator:** Abstract; §1 (model); §4.3 (renewal-game Theorem 4)

**Paraphrase:** the canonical APT-reset model [fetched]. Two players share a
resource (a key, a password, "an entire infrastructure"); each can "move" (take
control / reset) at any time for a **move cost**, and — the stealth feature — **a
player learns the resource's state only when they themselves move**. Benefit =
fraction of time controlling the resource − average move cost. This is *exactly*
persistence: the attacker holds a foothold, the defender's MTD move re-takes
control, neither sees the other's moves. Key results: at the periodic-game Nash
equilibrium **the player with the higher move cost has benefit 0**; a **periodic
strategy with a random phase strongly dominates all renewal strategies** of the
same rate. Practical reading: whoever can move *faster and cheaper* controls the
resource more of the time — so a cheap, frequent MTD reset erodes a persistent
foothold's control fraction, and an expensive/rare one cedes it.

**Maps to:** [`05_persistence`](../../notes/ch4_methods/tactic_profiles/05_persistence.md) /
[`07_stealth`](../../notes/ch4_methods/tactic_profiles/07_stealth.md) §3 (reset verdict: a periodic
move *does* contest a persistent gain, but the outcome is set by the move-rate ÷
move-cost ratio — so the reset is partial and rate-dependent, not clean → a wide
sweep) and the group anchor.

**Disposition for this thesis:** verified [fetched] — the foundational
persistence-reset model. Game-theoretic/analytical, not a per-tactic dwell; it
supplies the *mechanism and the ratio*, the sweep supplies the magnitude.

---

### SCIT 2006 — cleansing cycle bounds the undetected-compromise window

**Source locator:** §1–§2 (basics); §4 (primitives; "longest cleansing cycle")

**Paraphrase:** periodic server **self-cleansing/rotation** (a redundancy MTD)
restores a server to a known-clean state on a fixed cycle, "restricting would-be
attackers to short time windows to breach the system before restoration"
[fetched]. The cleansing-cycle length *is* the maximum window an attacker holds
the system; a faster cycle → shorter window. Caveat the paper raises: an attacker
can target the cleansing process itself (Trojaned utilities, tampered boot) — so
the reset is not unconditionally clean. **The md is OCR-garbled — no exact cycle
figures cited; mechanism only, exact numbers `[parse-uncertain]`.**

**Maps to:** [`05_persistence`](../../notes/ch4_methods/tactic_profiles/05_persistence.md) §3
(redundancy/rotation MTD periodically invalidates a foothold — the attacker must
re-establish persistence each cycle; the reset is periodic, bounded, and itself
attackable).

**Disposition for this thesis:** verified [fetched] for the mechanism; exact
timing `[parse-uncertain]` (garbled OCR). A defender-cycle bound, not attacker
dwell.

---

### Sun 2025 (Stackelberg-FlipIt) — "when to move" is the optimised quantity

**Source locator:** §1 (contributions); §2 (when-to-move taxonomy); §4 (IP-hopping
case study)

**Paraphrase:** extends FlipIt with a Stackelberg leader-follower structure and
multi-agent RL (WoLF-PHC) to *learn* the MTD move timing [fetched]. States the
sweep-relevant trade-off plainly: "**insufficiently reactive MTD intervals grant
attackers extended time windows to analyze system patterns, exploit
vulnerabilities, or escalate privileges**", while overly aggressive intervals
cause instability/overhead. Validated on IP-address dynamic hopping against
scanning. Confirms "when to move" (the reset interval) is *the* decision variable
and is adversary-conditioned.

**Maps to:** [`05_persistence`](../../notes/ch4_methods/tactic_profiles/05_persistence.md) /
[`07_stealth`](../../notes/ch4_methods/tactic_profiles/07_stealth.md) §3 (the reset interval is the
swept parameter; too-slow reset cedes the foothold) + method (FlipIt-lineage
declare-and-optimise).

**Disposition for this thesis:** verified [fetched] — corroborates FlipIt's
ratio result and frames the reset interval as the sweep axis. RL/game-theoretic,
not a dwell.

## Open questions / things to verify

- All three are *models of the defender's reset*, not logs of an APT's persistence
  dwell — they price *what a reset does to a held foothold*, which is precisely §3
  (the genuine unknown), and consistently say the reset is **partial and
  rate-dependent** (never a clean wipe). The magnitude is swept.
- SCIT exact cleansing-cycle figures need the clean PDF (md OCR-garbled).

## Out of scope for this thesis

FlipIt's full strategy hierarchy and equivalence proofs; SCIT's DNS-cluster
implementation detail; Sun's WoLF-PHC algorithm internals and convergence proofs.
The mechanism (reset contests a foothold, rate-dependently) is the load-bearing
part.
