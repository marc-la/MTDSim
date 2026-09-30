# Verify A: Table 4.3, three rows (relative tactic occurrence, distinct attack paths, attack actions blocked)

Read-only check, 2026-09-30. Every quote below is re-read from the source text: the markdown in `docs/sources/lit_review/` and, for page numbers, the PDF text layer of `docs/sources/lit_review/original/*.pdf` (pypdf; Brown Fig. 4 rendered as an image and read). The extracts were used only as pointers.

Dissertation text read from §4.5 of `docs/thesis/dissertation.tex` at commit 36999e59 (the live-text extract) (ll. 22-47, 155-163) and `docs/thesis/tables/tab_4-5a_metrics.tex` (the Source column cites all three rows bare: `\citep{rodriguez2024}`, `\citep{hong2018}`, `\citep{brown2023}`). "Interrupt" is read from dissertation.tex §4.4.1 (l. 5190-5202).

---

## 1. Relative tactic occurrence -> rodriguez2024

**Source's name (verbatim).** None as a metric. It is a column head in ProM's log summary: "**Occur. (rel.)**" beside "**Occur. (abs.)**", rows headed "**class**" (Table 3 "Log Summary (ProM)", §4.4.1, PDF p. 8; md l. 358-384). The same columns recur in Table 5 (Team 12, md l. 425-446). No sentence in the paper names or defines the quantity. The only prose reference: "Additionally, the frequency with which these tactics occur is provided in the information contained in the analyzed log." (§4.3, md l. 321 + l. 298; the PDF column order splits the sentence.)

**What the column is (from the table itself).**
- Header rows: "Total number of process instances: 21", "Total number of events: 7265", "Total number of classes: 14".
- Row: "execution | 3270 | 45.01%". 3270 / 7265 = 45.01 %. So rel. = a class's events / **all events in the log, pooled over the 21 process instances** (a ratio of sums, not a mean of per-trace shares, not per trace).
- The denominator includes ProM's artificial "Start | 21 | 0.29%" and "End | 21 | 0.29%" classes (0.58 % of events).
- An event is one labelled Sysmon detection: "The log is exported as a CSV file, each row representing an event with columns containing event attributes, including the case ID, activity name, and timestamp." (§3.1.3, md l. 169) and "the attacker's techniques and tactics are considered the activities performed" (§3.1.3, md l. 173). Repeats are kept: "In our domain, cases may include repeated activities in sequence or duplicate tasks with the same taxonomy signature." (§3.2, md l. 181).
- Used in prose as a share of activity: "Almost 79.88% of the activity is concentrated in 3 types of events: execution, defense_evasion, persistence." (§4.4.1, md l. 348).

**Dissertation.** "Relative tactic occurrence is the percentage of an attacker's steps taken in each tactic, the quantity Rodr\'{\i}guez et al. tabulate for the tactics of an attack log \citep[Table~3]{rodriguez2024}. A step is one tactic executed by the Petri net ... The baseline attacker has no tactics: its step is one action, with consecutive repeats of an action counted once ... Counting over every run, relative tactic occurrence(p) = 100 x steps in tactic p / all steps."

**Verdict: adapted-but-unstated (minor).** The operation is Rodríguez's exactly (count per tactic over the pooled total, as a percentage), and "tabulate" is honest (it does not claim they define it). The unit is not: their count is sensor events, so one tactic executed can contribute many rows in a row; a step counts a tactic once per execution, and the baseline's consecutive repeats are collapsed, the opposite of Rodríguez's practice. "The quantity Rodríguez et al. tabulate" silently equates events with steps. The earlier drafted version (extract `s45_metric_definitions/01_*.md`) stated this difference; the current text dropped it. The name "relative tactic occurrence" is the dissertation's, built from the column head; that is acceptable and should not be presented as Rodríguez's name.

**Source an examiner expects?** Yes, acceptably: a peer-reviewed ATT&CK attacker-profiling paper tabulating this share per tactic from attack logs. It is a descriptive relative frequency, so no "originating" metric paper exists to be missed. Checked alternatives: Rodríguez's own Table 4 relays Cisco (Nahorney 2020) "% of IoCs seen" per tactic (md l. 391-405), an industry figure whose shares do not sum to 100 %, so worse. A search of the held corpus for tactic-frequency or tactic-prevalence metrics (grep across `docs/sources/`) found nothing better (only Ferraz 2024 and the DFIR Report, neither defining a share). The ProM relative occurrence comes from process mining (van der Aalst 2016, cited by Rodríguez); it is not needed.

**Confidence: high.** The table arithmetic is checked, and the absence of a definition was checked by grep ("Occur" appears only in Tables 3 and 5).

**Smallest fix.** Add one clause stating the unit: e.g. "...the share Rodríguez et al. tabulate for the logged events of each tactic [Table 3]; they count every logged event, so one tactic executed can count many times, where a step counts it once." Optionally make the table cell "adapted from \citep{rodriguez2024}" if the table's source grammar still distinguishes adapted from bare.

**Bib check.** `rodriguez2024` DOI 10.5753/jisa.2024.3902 resolves (HTTP 302 to the SBC article page). The PDF's own header prints "2023, 15:1, doi: 10.5753/jisa.2023.3902", which 404s, and "Published: 01 August 2024". Bib year 2024 and DOI are right. The PDF header is a typo; do not copy it. Pages 212-232 were not checked.

---

## 2. Distinct attack paths -> hong2018

**Source's names (verbatim).** Hong 2018 has no metric called "distinct attack paths" or "number of attack paths". Its path metrics:
- **Attack path variation (APV)**, §5.1.1 "Scanning: path variation", p. 39: "the attack path variation (APV) measures the shift in attack paths as the network changes when MTD techniques are deployed ... That is, APV captures the change in the set of attack paths between the network states." Eq. (1): ΔAP_{i,i-1} = |AP_i − AP_{i-1}| / |AP_i|; Eq. (2): APV = Σ_{i=1}^{|S|} ΔAP_{i,i-1} / (|S| − 1). (Both checked against the PDF text layer, p. 39.)
- **APN**, §5.1.2 "Scanning: path number", p. 40: "Eq. (5) shows the computation of APN metric that measures the differences between the numbers of attack paths for all network states." Eq. (3): 1 − (|AP_i| − |AP_{i-1}|)/|AP_i|; Eq. (4): the max(·, 0) form; Eq. (5): APN = Σ Δ|AP| / (|S| − 1). The acronym is never expanded. Fig. 1 (p. 36) labels the category "Path Number".
- The count |AP_i| appears only as an ingredient: "Increasing the number of attack paths can negatively impact the network security, as it reveals more choices to be taken by the attacker" (§5.1.2, p. 39). In the worked example: "the set of attack paths in s0 with the cardinality value of AP0 = 5" (§5.3.1, p. 42, md l. 406) and "the number of attack paths for each network state is five, giving the APN value of one" (§5.3.2, p. 42, md l. 425).

**What Hong's attack path is.** It is a sequence of **hosts** in the upper-layer attack graph of the network's HARM, from the attacker to the target. Def. 2 (p. 37) says: "U_ti is an upper layer using an Attack Graph that captures only the reachability of hosts that establishes attack paths". The worked example (p. 42) gives "AP0 = {(A, h1, h4, h7), (A, h1, h5, h6, h7), ...}". Table 1: "AP | A set of attack paths". Paths are computed analytically per network state, not observed from a running attacker.

**Dissertation.** "An attacker's attack path in a run is the sequence of steps the run takes. Distinct attack paths is the number of different attack paths an attacker's runs take, compared over their first k steps; it counts the paths the runs realise, not the paths the attack graph allows: distinct attack paths(k) = number of different first-k-step sequences. ... Hong et al. count the attack paths a network offers \citep{hong2018}; here the paths are the ones an attacker takes." (Equation label still `eq:apv`, which is invisible to the reader.)

**Verdict: adapted, and only partly stated. The Table 4.3 cell reads as misattribution.**
- Stated: realised paths versus the paths the attack graph allows. The last sentence is accurate: Hong does count |AP_i| per network state.
- Unstated: (a) Hong's attack path is a host sequence to the target; the dissertation's is a sequence of **steps** (tactics, or actions for the baseline). The thesis redefines Hong's term without saying so. (b) The dissertation compares a k-step prefix, not a whole path. (c) Hong's metrics are change-across-network-states ratios in [0, 1] (APV, APN), not a count. No Hong metric is a count of distinct paths.
- The prose cites Hong only for "count the attack paths a network offers", which is defensible. But Table 4.3 puts `\citep{hong2018}` alone in the Source column for "Distinct attack paths", and a reader, above all Hong himself, will look there for a metric of that name and not find one. Hong is first author and the supervisor.

**Source an examiner expects?** Not as the metric's source. Hong 2018 is the right MTD-lineage paper for the attack-path concept. The quantity, a count of distinct realised sequences in a set of runs, is what process mining calls trace variants (van der Aalst 2016, *Process Mining*, not held). Rodríguez mentions "selecting process variants for deeper analysis" (§3.2, md l. 185) but never counts them. A named count of attack paths does exist in Hong's group: NAP, "number of attack paths", in Enoch, Ge, Hong, Alzaid & Kim, *Computer Networks* 2018 (DOI 10.1016/j.comnet.2018.07.028). The census file `metric_census/F_web_open_access.md` l. 111 records it as read on the web, but it is **not held locally** and I did not verify it. It is still the network-offered count, not the realised one.

**Confidence: high** on what Hong 2018 defines and does not define (text layer checked, Eqs. 1-5 and Def. 2). **Medium** on NAP as an alternative, because the source is not held.

**Smallest fix.** Two edits. (1) Table cell: "this dissertation, after \citep{hong2018}", the same grammar as the time-lost row. (2) Replace the last sentence with one that names both differences, e.g. "Hong et al.'s attack path is a sequence of hosts through the network's attack graph, and they count the paths each network state offers \citep[Sec.~5.1.2]{hong2018}; here a path is a run's sequence of steps, and only the paths runs take are counted." Raise the name with Dr Hong before submission (the 02_apv extract already recommended this for the APV name).

---

## 3. Attack actions blocked -> brown2023

**Authors.** Brown, Lee and **Jin B. Hong** (PDF p. 1; bib l. 126-134). The supervisor is a co-author.

**Source's name (verbatim).** Brown uses three forms:
- The §IV-A heading "Attack Actions Blocked" (p. 5).
- In the §IV text: "we evaluate the total actions blocked and also the average attempts required to compromise ... We look at these two metrics as the simplest form of metrics when considering multiple attack scenarios" (p. 5).
- The Fig. 4 caption "Total actions blocked using different MTDs", with the y-axis "No. of Actions Blocked" (p. 6, rendered and read). The "None" bars are empty (zero).

**Source's definition.** There is no equation or formal definition. What "blocked" means is given by:
- §III-D, p. 4: "It is important to understand the different scenarios that the attacker is placed in when the attacker is blocked by an MTD technique and what actions they will perform." The three cases:
  - (1) "Connection to Host is Lost: IP Shuffle and Host Topology Shuffle ... This would result in the attacker's connection to the host being terminated or timed out ... forced to re-perform the host discovery phase";
  - (2) "Connection to Service is Lost: Service and Operating System Diversity, and Port Shuffle ... This would block the attacker from compromising the vulnerability and force them to re-perform a port scan";
  - (3) "User Access Has Changed: ... This would only block the attack if the attacker was performing a credential stuffing attack".
- §III-B, p. 3, per mechanism: "interrupting any attacker performing operations using an incorrect IP Address" (IP shuffle); "interrupting any attacker performing operations using an incorrect port number" (port shuffle); "disconnects any connections to the service, interrupting any attack that is still ongoing" (service diversity).
- §IV-B, p. 6: "when the attacker is blocked, the attacker simply needs to reconnect and then exploit the same vulnerabilities."
- §V-A, p. 7: "giving a time penalty whenever the attacker is blocked due to an MTD and forces them to re-scan the network".

So a blocked action is an attacker operation that a deployment cuts off while it is under way (connection or credential lost). It is a **count** ("total", "No. of"). The aggregation is unstated: Brown gives no run count, so per-run versus summed is unknown. `evaluation_conventions.md` §i: "No run count at all (Brown) — the most-cited paper in the lineage does not say how many times anything was run."

**Dissertation.** "Attack actions blocked is Brown's count of the attacker's actions that MTD blocks \citep[Sec.~IV-A]{brown2023}: here, the actions a deployment interrupts (Section~\ref{subsec:runtime-mechanics}). attack actions blocked = mean over runs (actions a deployment interrupts)." In §4.4.1: "if MTD interrupts the attacker, then whatever action it is on fails ... A deployment that lands during a dwell-only tactic cuts the dwell short ... but there was no action in flight to lose".

**Verdict: faithful, with one natural adaptation (per-run mean) that Brown's silence makes unfalsifiable.** "Interrupted in flight" matches Brown's §III-B/§III-D/§IV-B/§V-A wording: connection terminated, "interrupting any attack that is still ongoing". It also matches Brown's own code lineage: `mtdnetwork/operation/mtd_operation.py` `_interrupt_adversary` increments `add_total_attack_interrupted()`. This is implementation corroboration, not the source. The analyser (`data/results/ch5_defended/time_lost.py` l. 8-13, 57-75) counts MTD_INTERRUPT records and excludes dwell-only interrupts, consistent with §4.4.1. Brown's case (3) is honoured in the substrate: the reserve-layer interrupt applies only to BRUTE_FORCE (mtd_operation.py l. 248-255, citing IS-INT-03). The zero under no MTD matches Brown's empty "None" bars. This resolves the earlier dispute recorded in the table's comment ("Brown's metric is our interrupt"), which counted precondition failures and read 0.24 with no MTD.

**Source an examiner expects?** Yes. It is the originating paper for this simulator's metric, under the same name.

**Confidence: high** on name, count and in-flight meaning. **Medium-high** on the per-run reading, since Brown never states it.

**Smallest fix.** Cite the definition's locator as well as the heading: `\citep[Secs.~III-D, IV-A]{brown2023}`. Optional: "Brown reports a total; here it is averaged per run." Housekeeping, not in the reader's text: `docs/sources/extractions/mtd_metric_catalogue.md` l. 36 still describes the retired precondition-failure share ("a share rather than a count ... these include failures with no defence running (0.24)"), and `tab_4-5a_metrics.tex`'s "CUT 2026-09-25 ... ATTACK ACTIONS BLOCKED" comment is stale against the current table.

---

## To download / verify (not held)
- Enoch, Ge, Hong, Alzaid, Kim 2018, *Computer Networks*, DOI 10.1016/j.comnet.2018.07.028: NAP (number of attack paths). Only needed if the distinct-attack-paths row wants a named path-count antecedent.
- van der Aalst 2016, *Process Mining: Data Science in Action* (Springer): trace variants and relative event-class occurrence. Optional antecedent for rows 1 and 2.

## What an examiner expects of metric citations
- A metric is defined at its site with name, equation and direction, and a canonical name is never reused with different semantics silently. From `literature_conventions.md` §d.2: "**Never reuse a canonical name with divergent semantics silently** ... a named divergence is a defensible choice, an unnamed one reads as an error."
- A concept is cited to its origin. From `literature_conventions.md` §f: "a concept is cited to its origin, not to whichever survey mentioned it". For Hong's term "attack path", the thesis must either keep his meaning (host sequences) or say it changed it.
- The field's metric prescription asks for "common security mechanisms and terminology ... making it understandable even to people who are not experts in the MTD field" (Jalowski, via `evaluation_conventions.md` §g). A bespoke count should be named for what it counts, which "distinct attack paths" does.
- `evaluation_conventions.md` §f2 says a phase-resolved measure with a published antecedent "should cite it rather than introduce itself as novel". The mirror duty applies too: a quantity that is not the cited paper's must not borrow that paper's authority in a bare Source cell.
- In practice, for this table, a bare citation will be read as "defined there, as here". Row 3 meets that. Rows 1 and 2 each need one stated difference, and row 2 needs "after" in its cell, because its author will examine the claim first-hand.
