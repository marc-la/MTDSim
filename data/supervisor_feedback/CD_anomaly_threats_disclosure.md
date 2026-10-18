# C + D: the anomaly, the threats and the disclosures (items 4, 5, 8, 9)

**Status (2026-10-18).**
- **Applied** (commit `2a984e44`):
  - **Item 9.** §4.2: "…did neither, so $c_4$ is a mixed group, not a single objective: three attackers…".
  - **Item 8.** Appendix A's label: "…After submission, work on the defender was ruled out of scope, so this dissertation pursues only the first of the proposal's four aims, ``a more sophisticated adversarial module'', and runs MTDShield as released, with no IDS." The label is raised into the top margin, clear of the proposal's title (rendered and checked).
- **Open:** item 4 (wording approved; Marc's question below), and item 5 (T4 v3 below).

---

## Item 4: why the first deployment helps the baseline attacker. Bug, or design worth keeping?

**Wording (Marc: "very clear … well integrated").** Inserted in §5.3.1 after "…204 to 232 s forward.". One fix against the ch5 gate: no "With no MTD" opener ahead of the subject.
> The first deployment disrupts the baseline attacker while it exploits its first exposed endpoint, and sends it straight back to that endpoint. It otherwise returns there only after its list of hosts runs out (Section~\ref{subsec:attacker-model}).

**Marc's question.** How do we tell this from a bug, and why keep it?

**1. Every rule that produces it is one the MTDSim papers describe.** The test the thesis uses (guardrails; `mtdsim_intent_spec.md` §c) is this: a behaviour is a bug candidate only if no source documents it, and only Marc's disposition makes it a bug. Each step was traced on three seeds, and each run matched its corpus row exactly:

| Step | Source (intent spec) |
|---|---|
| An MTD deployment interrupts the attack action in progress, and the attacker restarts its procedure "regardless of prior progress" | IS-INT-01, IS-INT-05, IS-INT-07 (Brown §III-D, §V-A; Zhang §4.4.2) |
| The restart rebuilds its list of hosts, with the exposed endpoints first | IS-PRC-01 |
| Vulnerabilities it has already exploited stay exploited, so a new port scan reaches the services behind them | IS-PRC-02 |
| With no MTD, a failed host is left until the list runs out | IS-PRC-06, IS-PRC-07, IS-SCN-04 |

No paper states the outcome (an earlier return to the first host), but every rule behind it is documented. The 2026-10-06 classification was `conforms`, and the record of that ruling (ch5 redraft handoff §8–9) says so.

**2. Why keep it.**
- **It is the yardstick.** The baseline attacker is the attacker every MTDSim study used (Brown, Zhang, Ho, Tay), and the one MTDShield was trained against. The thesis claims that MTD measures differently against the APT attacker model *than against that baseline*. Changing the baseline changes the comparison the thesis exists to make.
- **Changing it now would be post hoc.** Altering the comparator after seeing a result it produces is the reverse-fitting the thesis guards against everywhere else: marks fixed before scoring, values declared before results, criteria fixed before runs.
- **It does not favour either layer.** The 204–232 s comes under *every* host-layer and service-layer mechanism alike (service diversity included), so it shifts both of the baseline attacker's layers together, not one against the other. After the first deployment, each later host-layer deployment costs it 18–32 s, as the paper's penalty predicts. The first-deployment split (ch5 record §8, point 4) keeps the direction of time lost in both subsets.
- **It is a plausible attacker.** An attacker knocked off its target retries the most promising one first, and a service it has already exploited stays exploited. Neither is unrealistic. Only the timing, the first deployment arriving mid-exploit, makes it visible.
- **It is what Jin asked for.** "If it is how MTDSim is designed to behave, explain it in section 5.3.1."

**What the case does not claim.**
- It does not say the effect is negligible on every number. It shapes the baseline attacker's time lost, and it may feed T4's sign flips (more targets reached under some host-layer mechanisms). That link is measured, not attributed, so T4 does not claim it.

**Ruling owed:** keep and explain (recommended), or flag in T1 as unexplained (not recommended, because it *is* explained).

---

## Item 5: extend T4 (v3)

**Connecting the dots (Marc: "I'm not connecting the dots").**
1. NCR counts the hosts compromised **by the end of the run**.
2. A baseline-attacker run **ends the moment it compromises a target host**. That is the targeted attack scenario's stopping rule.
3. So if an MTD mechanism gets the baseline attacker to a target host **sooner**, its runs **end sooner**. It has had less time to compromise other hosts, so its NCR is **lower** under that mechanism, while **more** runs reach a target, so its ASP is **higher**.
4. NCR reduction is then positive ("MTD helped the defender") while ASP reduction is negative ("MTD helped the attacker"). The same runs give opposite verdicts.
5. The APT attacker model rarely reaches a target, and 91 % of its runs end at the time limit, so its NCR is counted over the whole run and the effect does not arise. That is why every sign flip is the baseline attacker's.

Points 2–4 are the sentence round 1 compressed into "can therefore raise NCR reduction by ending the attacker's runs sooner". v3 states step 3 as plain facts, in the order they happen.

**Numbers (checked against `numbers_reported.json` and Tables D.3 and D.5).**

| Baseline attacker | NCR reduction | ASP reduction |
|---|---|---|
| IP shuffle 500 / 1 000 / 2 000 s | 0.39 / 0.30 / 0.19 | −0.09 / −0.11 / −0.10 |
| complete topology shuffle 500 s | 0.09 | −0.23 |
| OS diversity 500 s | 0.04 | −0.11 |

- Every cell's 95 % interval excludes zero.
- How runs end with no MTD: 66 % of the baseline attacker's runs at a target host; 91 % of the APT attacker model's at the time limit.

**v3, in place (bold = new; the rest is on disk as ratified).**
> NCR reduction, our main metric, only partially measures how MTD performs: it counts the hosts an attacker compromises, whether or not it reaches a target host in the targeted attack scenario. **With no MTD, 66 % of the baseline attacker's runs end at their first target host compromised, and 91 % of the APT attacker model's at the time limit. When an MTD mechanism brings the baseline attacker to a target host sooner, more of its runs reach one, and each ends with fewer hosts compromised. Its NCR reduction is positive and its ASP reduction negative under IP shuffle at 500 to 2 000 s, and under complete topology shuffle and OS diversity at 500 s (Tables D.3 and D.5).** To mitigate this threat, we also computed ASP reduction, and it orders the two layers as NCR reduction does, for both attackers, at every deployment interval (Table D.5). The threat remains for rank 1 against the APT attacker model up to 200 s, where ASP reduction ties every host-layer mechanism at 1 and only NCR reduction orders them.

**Why this shape.**
- **One thought, in the order it happens:** how runs end (the two stopping rules, one per attacker); what an earlier target does (more targets, fewer hosts); then where it shows (the cells).
- **Fixes against Marc's round-1 notes.** No "It counts them when the run ends:" colon lead-in, and no "The threat remains where the two disagree in sign, all for the baseline attacker:" closing. The sign flips are now part of the threat, and the existing mitigation answers them: the layer order holds on ASP reduction. The residual stays rank 1, as ratified.
- **No causal claim about these cells.** Sentence 3 says what an earlier target does; sentence 4 reports the cells. The reader can join them, and T4 attributes nothing it did not measure.
- "Its" in sentence 4 refers to the baseline attacker (the subject of sentence 3's main clause).

**Net:** about +80 words. That is more than round 2's +66, because v3 keeps the "so what" Marc needed, and less than round 1's +100.

**Alternatives, if the band forces one:**
- (a) Drop sentence 3 (−22 words). This is round 2: the cells follow the run endings with no mechanism, which is the version whose dots did not connect.
- (b) Drop OS diversity from the list (−3 words). This matches Jin's list exactly, but then the list reads as complete when it is not.

---

**Repo record owed when items 4 and 5 are applied:** `docs/implementation/disruption_mechanism.md` §9 has three stale points: the §6.2 pointer; "an attempt it would not otherwise have had", which should be "an earlier one"; and D-23 omitted.

---

## Round 3 (Marc 2026-10-18): the defence in one sentence; NCR as a function of time

**Marc.**
- Item 4: no appendix entry; defend it within the sentence by the four sourced rules.
- T4: the missing dot is that NCR is, in effect, a function of time.

**What changes.** §2.2.3 already states every rule, cited:
- the restarts, back to scanning hosts or to the same host's ports [brown2023, zhang2023];
- the list rebuilt when it runs out [brown2023];
- "a deployment never takes back a compromised host [zhang2023] … the attacker loses only the progress it must repeat".

So the §5.3.1 sentence names *its procedure* and points to §2.2.3, and T4 grounds the time dot in the same rule. Nothing is re-cited.

**Item 4 v3 (§5.3.1, after "…204 to 232 s forward."). PROPOSE**
> The first deployment disrupts the baseline attacker while it exploits its first exposed endpoint, and its procedure sends it straight back to that endpoint, keeping the progress it made there (Section~\ref{subsec:attacker-model}). It otherwise returns there only after its list of hosts runs out.

**T4 v4. APPLY ON RULING**
> NCR reduction, our main metric, only partially measures how MTD performs: it counts the hosts an attacker compromises, whether or not it reaches a target host in the targeted attack scenario. With no MTD, 66\,\% of the baseline attacker's runs end at their first target host compromised, and 91\,\% of the APT attacker model's at the time limit. A run's NCR only rises while the run lasts, because a deployment never takes back a compromised host (Section~\ref{subsec:attacker-model}). An MTD mechanism that brings the baseline attacker to a target host sooner therefore ends those runs with fewer hosts compromised, raising its ASP while lowering its NCR. The baseline attacker's NCR reduction is positive and its ASP reduction negative under IP shuffle at 500 to 2\,000\,s, and under complete topology shuffle and OS diversity at 500\,s (Tables~\ref{tab:eff-interval-values} and~\ref{tab:eff-interval-values-asp}). To mitigate this threat, … *(unchanged)*

Net: item 4 about +40 words; T4 about +100.
