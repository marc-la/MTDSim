# Detector conventions: rate or threshold-over-window alarms (κ and θ)

Research record, 2026-09-29. Read-only on the repo. Every quote below was fetched or read in this session. Local copies are in `docs/sources/s45_fetched/` (gitignored) (`scan_v5.0.0.zeek`, `simple_scan.zeek`, `ss.zeek`, `ps_module.cc`, `ps_detect.cc`, `snort_defaults.lua`, `sfportscan.txt`, `snort_df.txt`, `suri_thr.txt`, `w.txt`, `tw.txt`, `trw.txt`, `cisar.txt`, `sp.txt`). PDF page numbers are *PDF p.*, printed page numbers are *p.*

---

## 1. Production IDS defaults

### Zeek (Bro), `policy/misc/scan.zeek`
URL: https://raw.githubusercontent.com/zeek/zeek/v5.0.0/scripts/policy/misc/scan.zeek. The file is identical at v3.0.0, v4.0.0 and v5.0.0 and is still present at v6.0.0. It is **absent from v7.0.0 on**. Zeek's NEWS says: "The ``misc/scan.zeek`` script has been marked for removal in Zeek 6.1. Use github.com/ncsa/bro-simple-scan instead." (https://raw.githubusercontent.com/zeek/zeek/master/NEWS, l.3609–3610.)

- l.32–35: "Failed connection attempts are tracked over this time interval for the address scan detection. A higher interval will detect slower scanners, but may also yield more false positives." `const addr_scan_interval = 5min &redef;`
- l.40: `const port_scan_interval = 5min &redef;` (same comment)
- l.42–44: "The threshold of the unique number of hosts a scanning host has to have failed connections with on a single port." `const addr_scan_threshold = 25.0 &redef;`
- l.46–48: "The threshold of the number of unique ports a scanning host has to have failed connections with on a single victim host." `const port_scan_threshold = 15.0 &redef;`
- **What it counts:** the number of *unique* failed-connection destinations (hosts, or ports) per scanner, using `SumStats::UNIQUE` (l.56, 81). It does not count the number of events.
- **Window shape:** the window is a SumStats *epoch*, a tumbling window that resets, not a sliding one. SumStats `main.zeek` v5.0.0, l.96–101: "The interval at which this sumstat should be "broken" and the *epoch_result* callback called. The results are also reset at this time so any threshold based detection needs to be set to a value that should be expected to happen within this epoch."
- **Replacement** (ncsa/bro-simple-scan, `scripts/scan.zeek`, https://raw.githubusercontent.com/ncsa/bro-simple-scan/master/scripts/scan.zeek). l.56–59: "Failed connection attempts are tracked until not seen for this interval. A higher interval will detect slower scanners, but may also yield more false positives." `const scan_timeout = 15min &redef;`. l.67: `const scan_threshold = 25` (unique host+port for a remote scanner). l.71: `local_scan_threshold = 250`. This is an idle timeout, not a fixed window.
- **Older Bro default**, per Jung et al. 2004 (§2, PDF p.3; see §2 below): "By default, Bro sets N = 100 addresses … However, the sites from which our traces came used N = 20 instead." That detector used a count with no window.

### Snort 3 `port_scan` (the successor to sfPortscan)
Source: `lua/snort_defaults.lua` at snort3 master (commit 14aeb09f), https://raw.githubusercontent.com/snort3/snort3/master/lua/snort_defaults.lua.
- l.1094–1102 `default_hi_port_scan`: `tcp_window = 600`, `udp_window = 600`, `ip_window = 600`, `icmp_window = 600`
- l.1122–1130 `default_med_port_scan`: all windows `90`
- l.1150–1158 `default_low_port_scan`: all windows `60`
- The per-type count thresholds are at l.1045–1092. For example `tcp_low_ports = { scans = 0, rejects = 5, nets = 25, ports = 5 }`, `tcp_med_ports = { scans = 200, rejects = 10, nets = 60, ports = 15 }` and `tcp_hi_ports = { scans = 200, rejects = 5, nets = 100, ports = 10 }`. `ps_module.cc` l.48–58 gives the meanings: `scans` "scan attempts"; `rejects` "scan attempts with negative response"; `nets` "number of times address changed from prior attempt"; `ports` "number of times port (or proto) changed from prior attempt". `tcp_window` is described as "detection interval for all TCP scans" (l.128–129).
- **Window shape** (`ps_detect.cc` l.451–459): `if (pkt_time > proto->window) { *proto = {}; proto->window = pkt_time + interval; }`. The window is tumbling and resets, and the units are seconds (packet time).
- **Snort 2 sfPortscan README** (https://www.snort.org/faq/readme-sfportscan, "sense_level"): ""Low" alerts are only generated on error packets sent from the target host … This setting is based on a static time window of 60 seconds, afterwhich this window is reset." ""High" alerts continuously track hosts on a network using a time window to evaluate portscan statistics for that host. A "High" setting will catch some slow scans because of the continuous monitoring, but is very sensitive to active hosts." The README does not state the medium and high window lengths. The Snort 3 defaults above (90 s and 600 s) are the numeric source for them.
- **Snort 2.0.2 portscan2 defaults**, per Jung et al. 2004 (§6, PDF p.11): "We use Snort's default settings, for which it flags a source IP address that has sent connections to 5 different IP addresses within 60 seconds. (We ignore Snort's rule for 20-different-ports-within-60-seconds …)" and "It can also be easily evaded by a scanner who probes a network no faster than 5 ad[dresses/minute]" (the sentence completes on PDF p.12: "…dresses/minute.").

### Snort 3 `detection_filter` (rate on a rule)
Source: https://docs.snort.org/rules/options/post/detection_filter. "Rule writers use this option to define a rate (count per seconds) that must be exceeded by a source or destination host before a rule can generate an event." The documented example is "# this rule looks for 30 SSH login attempts occurring # in 60 seconds from a single source IP … detection_filter:track by_src,count 30,seconds 60;"

### Suricata `threshold` / `detection_filter`
Source: https://docs.suricata.io/en/latest/rules/thresholding.html, §8.49, Suricata 9.0.0-dev docs.
- §8.49.1.1: "If seconds is specified, an alert is generated when count matches have occurred within N seconds." The example is `threshold: type threshold, track by_src, count 10, seconds 60;`, with the gloss "This signature generates an alert if there are 10 or more inbound emails from the same server within one minute."
- §8.49.1.2: `threshold: type limit, track by_src, seconds 180, count 1;`
- §8.49.1.3: `threshold: type both, track by_src, count 5, seconds 360;`
- §8.49.2 `detection_filter` examples:
  - `detection_filter: track by_dst, count 10, seconds 60, unique_on dst_port;`, labelled "Vertical scan: >=10 distinct dst ports in 60s"
  - `count 20, seconds 30, unique_on src_port`
  - `detection_filter:track by_src,count 15,seconds 2;`, with the gloss "This rule will generate alerts after 15 or more matches have occurred within 2 seconds."
- These are rule examples, not engine defaults. Suricata has **no default window**, because `seconds` is set per rule.

**Pattern across production tools.** Every tool is a count within a window of W seconds against a count threshold. **W = 60 s is the modal documented value**: the Snort 3 low default, the Snort 2 sfPortscan low default, the portscan2 default (5 hosts per 60 s), the Snort detection_filter documentation example (30 per 60 s) and the Suricata threshold and vertical-scan examples (10 per 60 s). The longer windows (90 s, 300 s, 600 s, 15 min) are the "sensitive" settings. Zeek and the Snort README both state them as a trade: a longer window catches slower scanners at more false positives. The implemented windows are **tumbling** (Snort, Zeek SumStats). None is exponential.

---

## 2. Academic rate-based detectors

### Williamson 2002, "Throttling Viruses" (ACSAC 2002; open: https://www.acsac.org/2002/papers/97.pdf)
The PDF's math glyphs are font-encoded (for example "/D2" = n), so the symbols are read as the text renders them.
- §3, PDF p.2: "Newness is determined by comparing the destination of the request to a short list of recently made connections. The length of this list or "working set" [n] can be varied so altering the sensitivity of the system." It "restricts connections to new hosts to one per timeout period."
- §4, PDF p.4: "In all cases the maximum frequency is low … and most of the traffic is concentrated at low frequencies e.g. 1–2 cps. This suggests that a reasonable value for the allowed rate should be 1–2 cps." And: "The data suggests that reasonable performance would be obtained with an allowed rate of 0.5–1 cps."
- §6, PDF p.7: "showing that the rate limit can be set as low as 1 cps without causing undue delay."
- **How the value was set:** the rate limit is set **from the distribution of benign traffic** (a histogram of normal users' local frequency), measured by "sliding a time window along the sequence" (PDF p.4).

### Twycross and Williamson 2003, "Implementing and testing a virus throttle" (USENIX Security 2003; open: https://www.usenix.org/legacy/events/sec03/tech/full_papers/twycross/twycross.pdf)
- p.288: "under normal usage often no more than one connection to a target not recently connected to is made per second". "The working set can hold up to 5 such addresses." "Once every second the delay queue is processed".
- p.288: "From observation of the normal behaviour of a range of users we saw that the delay queue rarely grew bigger than a handful of packets … In our throttle we set this upper limit on the delay queue size to 100 packets."
- The alarm is the delay-queue length, set from observed benign behaviour. **The time scale is 1 s**, which suits worms. It is far too fast for a κ on APT actions.

### Jung, Paxson, Berger and Balakrishnan 2004, Threshold Random Walk (IEEE S&P 2004; open: https://www.icir.org/vern/papers/portscan-oak04.pdf)
- §2, PDF p.3, **the canonical statement of the window convention and its weakness:** "Historically most scan detection has been in the simple form of detecting N events within a time interval of T seconds. The first such algorithm in the literature was that used by the Network Security Monitor (NSM) [2], which had rules to detect any source IP address connecting to more than 15 distinct destination IP addresses within a given time window. Such approaches have the drawback that once the window size is known it is easy for attackers to evade detection by simply increasing their scanning interval."
- §2, PDF p.3: "In general, choosing a good threshold is important: too low, and it can generate excessive false positives, while too high, and it will miss less aggressive scanners."
- **TRW avoids a window.** §1, PDF p.2: "In terms of time, we aim to detect scans that might be spread over intervals ranging up to hours … and we do not consider the particular rate at which a remote host attempts to make connections." And §1, PDF p.2: "'quickly' here is in terms of the amount of subsequent activity by the scanner: the activity itself can occur at a very slow rate". TRW is a sequential likelihood-ratio test on connection outcomes (success or failure), with no time scale. Listing "considering the rate at which a remote host makes connection attempts" as future work (§7, PDF p.12) confirms that time plays no part.
- **Threshold framing.** §3, PDF p.6: "We use the detection probability, PD, and the false positive probability, PF, to specify performance conditions of the detection algorithm. In particular, for user-selected values α and β, we desire that: PF ≤ α and PD ≥ β (3)", "where typical values might be α = 0.01 and β = 0.99" (PDF p.7). Table 3 uses "PD = 0.99, PF = 0.01, θ1 = 0.2, and θ0 = 0.8".
- **Relevance.** This is the one fetched source that sets a *detection-probability target on attacker traffic* as part of the threshold design. The target is β = 0.99, and it is always paired with a false-positive bound α set on benign traffic.

### Ye, Borror and Zhang 2002, EWMA for intrusion detection (QREI 18(6):443–451, doi:10.1002/qre.493)
**Paywalled (Wiley returns 403). To download.** Nothing is quoted from it. Čisar et al. 2010 also cite Ye et al. [5], "Computer Intrusion Detection Through EWMA for Autocorrelated and Uncorrelated Data" (IEEE Trans. Reliability). **Also to download.**

### Čisar, Bošnjak and Maravić Čisar 2010, "EWMA Algorithm in Network Practice" (IJCCC 5(2):160–170; open: https://univagora.ro/jour/index.php/ijccc/article/download/2471/938)
- Abstract, p.160: "Because of the ability of exponentially weighted moving average (EWMA) control charts to monitor the rate of occurrences of events based on their intensity, this technique is appropriate for implementation in control limits based algorithms."
- Eq. 1, p.160: "EWMA_t = λY_t + (1 − λ)EWMA_{t−1} … 0 < λ ≤ 1 is a constant that determines the depth of memory of the EWMA."
- **λ convention, p.161:** "The value of λ is usually set between 0.2 and 0.3 [2] although this choice is somewhat arbitrary. Lucas and Saccucci [3] have shown that although the smoothing factor λ used in an EWMA chart is usually recommended to be in the interval between 0.05 to 0.25, in practice the optimally designed smoothing factor depends not only on the given size of the mean shift δ, but also on a given in-control Average Run Length (ARL)." [2] is Hunter 1986 (J. Quality Technology 18:203–210). [3] is Lucas and Saccucci 1990 (Technometrics 32:1–29).
- **Their own λ** (§2, p.163) is fitted by minimum squared error on real traffic: "the authors suggest for the overall optimal parameter λopt to accept the average of all the partial results (in this particular case it is 0.75)."
- **Sampling interval** (p.165): MRTG "Daily - with calculation of 5-minute average; Weekly - 30-minute average; Monthly - 2-hour average."
- **Alarm level** (Eq. 3, p.161): "UCL = EWMA_0 + kσ_EWMA … where the factor k is either set equal 3 (the 3-sigma control limits) or chosen using the Lucas and Saccucci tables (ARL = 370)." EWMA_0 is "the mean of historical data (target)". **The limit is set on normal history, for a benign false-alarm rate.**
- p.164: "Generally, the smoothing constant should not be too small, so that a short-term trend in the intensity of events in the recent past can be detected."
- **Converting λ to κ.** The conversion is κ = −Δ / ln(1−λ) for sampling interval Δ. With Δ = 5 min: λ = 0.2 gives κ ≈ 22 min; λ = 0.3 gives κ ≈ 14 min; λ = 0.75 gives κ ≈ 3.6 min. **λ is dimensionless.** It fixes κ only relative to a sampling interval Δ, and no source fixes that interval for APT actions. **So Čisar cannot give κ = 60 s.**

### Stafford and Li 2010, "Behavior-based worm detectors compared" (RAID 2010, LNCS 6307:38–57)
This is Jafarian 2015's ref. [4], the source for "fast scanning is easy to detect". It is **paywalled** (Springer), and no author copy was found. **To download.** It is the best candidate for a cited comparison of rate or window detector parameters.

### Sommer and Paxson 2010, "Outside the Closed World" (IEEE S&P 2010; open: https://www.icir.org/robin/papers/oakland10-ml.pdf)
- §III-B, PDF p.3: "A false positive requires spending expensive analyst time … As argued by Axelsson, even a very small rate of false positives can quickly render an NIDS unusable [23]."
- §V, PDF p.7–8: "limiting false positives must be a top priority for any anomaly detection system."
- **Axelsson 2000** (base-rate fallacy, ACM TISSEC): the RAID'99 PDF URL is dead. **To download.**

---

## 3. What the repo's sources say (`/home/marc/GitHub/MTDSim/docs/sources/`)

**Jafarian 2015** has no `jafarian2015.md`. The file is `tactic_profiles/step_d/10_disc/An_Effective_Address_Mutation_Approach_for_Disrupting_Reconnaissance_Attacks.md`.
- l.289 (§VII; PDF p.10 = p.2571): "In our analysis, we focus on scanners/worms with low scanning rates, since fast scanning is easy to detect [4]." **Correction to `extractions/s45_metric_definitions/04_attack_confidentiality.md` row 7.** That row says this sentence "is missing from the `.md` conversion". It is present at l.289.
- l.289: "deployment of RHM in a network will force a rational attacker to commit to uniform scanning, which is highly susceptible to detection [4]."
- l.25: "these reactive defense methods (e.g., intrusion detection techniques) could be evaded by careful selection of attack parameters [4]."
- l.51: "stealthy reconnaissance and scanning attacks which may evade intrusion detection systems."
- The paper gives **no detection window or rate number**. It defers everything to [4], Stafford and Li. In Jafarian, θ is the mutation rate, so it does not collide in the thesis.

**Ward 2018** (`methodology/ward2018_mit_survey.md`):
- l.11796 (§5.18 Düppel, p.234): "If the number of preemptions exceeds 10 per millisecond, Düppel assumes a side-channel attack … is in progress"
- l.11892–11894 (p.236): "Finally, Düppel's preemption detection threshold is arbitrary. An attacker could avoid triggering Düppel to switch from sentinel to battle mode by slowing the rate of attack. This causes loss of precision, but is likely preferable to triggering the defense." **The survey itself calls a rate threshold "arbitrary".** This is useful cover for declaring κ and θ openly.
- l.13737–13740 (AVANT-GUARD): "traffic-rate-based, which uses a 22-bit condition that specifies the traffic rate (i.e., packets per second [PPS], bits per second [BPS], or raw count), a comparator, and a value to compare the current rate against"
- l.13857–13860: "This technique alone does not prevent an attacker from sending a malicious payload in a flow that stays below the traffic-rate trigger conditions"
- l.14802–14805 (§6.16 NetControl/Bro, p.296): "an attacker who is able to stay under the radar of the IDS could evade the system entirely. It is possible that administrators would set less aggressive thresholds for event detection in the framework, since false positives resulting in sudden, incorrect connectivity loss could significantly impede benign network operations." (This is the false-positive-driven threshold framing.)
- l.8976–8977: "A stealthy attacker could avoid detection and carry out their attack without extra hindrance."
- No time window for any network IDS is given.

**Hong 2018** (`lit_review/1_2_hong2018dynamic.md`):
- l.307 (§5.1.5, p.40): "the longer the attack takes, the more likely it will be detected." This is the opposite direction, already used as the bound. There is **no rate, threshold or window**.
- l.80 mentions Lei et al. 2016 "change-point detection in real time", which is not a detector window.

**Zaffarano 2015** (`lit_review/zaffarano2015.md`):
- l.344–345: "Attack Confidentiality is a measure of how much attacker activity may be visible by detection mechanisms".
- l.398: "is visible in plaintext in network traffic."
- There is **no rate, window or threshold** anywhere. The grep for stealth, low-and-slow, threshold, window, rate and per-second returned nothing else.
- **None of the four uses "low-and-slow".** That phrase is in Alshamrani 2019 (see the 04 record, row 8).

---

## 4. Setting the alarm threshold: conventions

- **Dominant convention: set θ on benign or reference-normal traffic for a target false-alarm rate.** Williamson and Twycross set the allowed rate and queue limit from normal users. Čisar sets UCL = mean + 3σ of historical traffic, or in-control ARL = 370. Zeek's and Snort's docs frame their windows and thresholds as a false-positive trade. Ward (l.14803–14805) and Sommer and Paxson (§V) put false positives first.
- **Evaluation framing: detection probability, or true-positive rate, at an operating point.** Jung 2004 writes this as "PF ≤ α and PD ≥ β", with typical α = 0.01 and β = 0.99. Sweeping θ traces the ROC (PD against PF). Jung is the one fetched source that puts a PD target on *attacker* traffic in the threshold design, and it is β = 0.99 jointly with an α on benign traffic.
- **Setting θ to flag a fixed share (50 %) of a reference attacker, with no benign traffic, was *not* found attested** in any fetched IDS source. A web search for attacker-referenced calibration returned only conformal-prediction papers (2026 arXiv), which were not read and not relied on.
- **Honest framing for the thesis.** θ is a *relative* operating point: the detection rate on the reference (baseline) attacker is fixed at 0.5, and each APT profile is read at that same θ. Since MTDSim has no benign traffic, no false-positive rate can be computed. Say so, and move the operating point (the appendix sweep already moves the flagged share). That makes the figure an ROC-style reading across θ, which is the conventional framing. **Do not present 0.5 as a cited convention.**
- **Arithmetic flag.** With the index-form self count, a steady rate r gives E[D] = 1 + rκ; this was checked by simulation for Poisson arrivals at 1, 3 and 12 per minute. θ ≈ 2.95 therefore corresponds to about **2 prior actions a minute, or 3 within the last minute counting the flagged one**. The draft's gloss "about three actions a minute" holds only in the counting-itself sense. The same identity gives E[count in the last 60 s, inclusive] = 1 + r·60.

---

## Conclusions

**(a) κ.** The best-cited candidate is **κ = 60 s, justified as equal to the modal production window W = 60 s**. Sources: the Snort 3 `default_low_port_scan` (all windows 60); the Snort 2 sfPortscan low "static time window of 60 seconds"; the Snort portscan2 default of 5 hosts in 60 s (via Jung 2004 p.11); the Snort detection_filter documentation example (30 in 60 s); and the Suricata examples (10 in 60 s). An exponential kernel with time constant κ has the same area as a box window W = κ. So at a steady rate the mean of D equals the mean count in a 60 s window (1 + rκ in both cases, checked numerically). Longer defaults exist for "sensitive" settings: Snort medium 90 s and high 600 s, Zeek 5 min, simple-scan 15 min. They bracket the appendix sweep. Čisar's λ 0.2–0.3 cannot fix κ without a sampling interval.

**(b) θ.** The best-cited framing is **operating point, meaning detection probability at a threshold, with θ varied to trace the curve** (Jung 2004's PF ≤ α, PD ≥ β; Čisar's control limit set on normal history). "Flag half of the baseline attacker" should be stated as a declared relative operating point (PD = 0.5 on the reference attacker), justified because the simulator has no benign traffic for a false-positive calibration. It should be backed by the sweep, not by a citation. Ward l.11892 ("threshold is arbitrary") supports declaring it openly.

**(c) A simpler detector.** Yes. **A count of actions in a window of W = 60 s against a count threshold N is the more conventional detector.** Jung calls it the historical form ("N events within a time interval of T seconds"), and it is what Snort, Zeek and Suricata implement, all with tumbling windows. The exponential kernel is conventional only in family, through EWMA or control charts (Čisar; Ye paywalled). Switching would need:
1. a window-count code path (sliding or tumbling; pick sliding and say so, since tumbling adds phase dependence);
2. an integer N, where N = 3 in 60 s matches the current θ in mean;
3. a statement of whether the window counts the current action;
4. a tie-breaking rule on equal start times (the 37 tied baseline actions);
5. a re-run of the confidentiality numbers, because integer counts put many actions at exactly N, so "flags half" can no longer hold exactly and the median rule needs a stated ≥ versus > convention;
6. citations to Jung 2004 §2 plus the Snort and Suricata docs, instead of Čisar.

---

## To download (paywalled or unreachable; nothing quoted)
- Ye, Borror and Zhang 2002, QREI 18(6):443–451, doi:10.1002/qre.493
- Ye et al., "Computer intrusion detection through EWMA for autocorrelated and uncorrelated data", IEEE Trans. Reliability (Čisar ref. [5])
- Stafford and Li 2010, RAID, LNCS 6307:38–57 (Jafarian ref. [4])
- Axelsson 2000, "The base-rate fallacy and the difficulty of intrusion detection", ACM TISSEC 3(3)
- Lucas and Saccucci 1990, Technometrics 32:1–29; Hunter 1986, J. Quality Technology 18:203–210 (the λ-range primaries)
