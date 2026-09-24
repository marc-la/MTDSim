#!/usr/bin/env python3
"""§5.3.1 Response to disruption: the reads Figure 5.3 draws, on both attackers
by one rule (rebuild ruled by Marc 2026-09-24; record: results context handoff
§8g-5, with the review rounds that shaped every choice below).

Why a separate reader: analyse.py caches per-run summaries keyed on its own
mtime, and these reads need each deployment's landing time, which the summaries
do not carry. Reading the corpus directly (prefiltered, ~20 s) keeps the cache
intact. Output: ``disruption_numbers.json`` beside the corpus.

THE ANCHOR. A deployment rewrites the network when it COMPLETES (verified on
the records: the baseline attacker's interrupted record ends at the completion
exactly; the APT attacker model's ends 20 s later, its record carrying the
confusion penalty). Both attackers are aligned on the completion of every
deployment, whether or not the record flags an interrupt: flagging selects each
attacker on the state it happened to be in, and a deployment that misses is
part of what the defence does. Only deployments with a full 750 s before them
count (the first lands about 100 s into a run, before anything is compromised,
and its "before" is empty).

THE WINDOW. 750 s before to 1 250 s after. At the 2 000 s interval the 750 s
before one deployment are the 1 250-2 000 s after the previous one, so the
window stops at 1 250 s: beyond it, "back to its level before" would be true
by construction.

(a) COMPROMISE RATE AROUND A DEPLOYMENT (NCR growth rate). Hosts compromised
    per unit of live time, in 125 s bins, as a percentage of the same
    attacker's rate in the 750 s before (its own level, so a slower attacker
    does not read as a damaged one). Live time: a bin counts only the part of
    it before the run ended, so a run that took its target does not read as a
    stalled one; the compromise that ends a run is counted. Kept per mechanism,
    per layer and pooled; the placebo (the same read on the same seed's
    no-defence run at the same moments) beside each.
(b) TIME LOST PER DEPLOYMENT, per mechanism: the area of (a)'s dip, over the
    1 250 s after, as seconds at the attacker's own pace (a deployment that
    stopped it dead for 300 s and then let it resume at full pace reads 300),
    LESS the same area on the placebo (not zero: the attacker's own pace drifts
    within a run). Can be negative: a catch-up above its level cancels a dip.
    Interval: seeded bootstrap, runs resampled with their placebo pairs. Also
    reported in hosts per deployment (seconds x the rate before), for the
    reader who asks what the normalisation by pace does.

Rejected estimators, 2026-09-24 (numbers in the record): the per-event wait to
the next compromise (drops the deployments never followed by a compromise, a
third of the model's under IP shuffle); the same wait against the same seed's
no-defence run at the same clock time (the defended attacker is behind its
twin; flipped the sign of the baseline's topology-shuffle cost); a
progress-matched half-gap reference (positive for every mechanism, biased).

Usage: python data/results/ch5_defended/disruption.py [--intervals 2000,200]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs.jsonl"
OUT = HERE / "disruption_numbers.json"
COMPROMISE = {("BRUTE_FORCE", "TRUE"), ("SCAN_PORT", "TRUE"), ("EXPLOIT_VULN", "EXPLOIT_COMPROMISED")}
HOST = ("ip_shuffle", "complete_topology", "host_topology")
SERVICE = ("port_shuffle", "os_diversity", "service_diversity")
MECHANISMS = HOST + SERVICE + ("user_shuffle",)
EDGES = np.arange(-750, 1251, 125)
PRE = EDGES[:-1] < 0
N_BOOT = 2_000
SEED = 20260924


def load(intervals: set[int]) -> list[dict]:
    """Targeted, core, quasi-periodic runs of the four profiles and the baseline
    attacker, no defence and the single mechanisms, at the given intervals."""
    out = []
    with RUNS.open() as f:
        for line in f:
            head = line[:400]
            if '"group": "core"' not in head or '"regime": "shifted"' not in head or '"objective": "targeted"' not in head:
                continue
            r = json.loads(line)
            if r["profile"] == "aggregate":
                continue
            if r["condition"] != "none" and (r["condition"] not in MECHANISMS or r["interval"] not in intervals):
                continue
            if r["arm"] == "movement":
                comp = [x[8] for x in r["records"] if (x[1], x[2]) in COMPROMISE]
            else:
                comp = [x[2] for x in r["records"] if x[3] is not None]
            T = r["termination_time"]
            out.append({
                "arm": r["arm"], "profile": r["profile"], "seed": r["seed"], "cond": r["condition"],
                # clamp to T: 116 of the model's runs log the last compromise up to 5e-7 s past it
                "interval": r["interval"], "T": T, "comp": np.sort(np.minimum(np.array(comp, float), T)),
                "landings": [e[2] for e in r["mtd_executions"] if -EDGES[0] <= e[2] < T],
                "durations": [e[3] for e in r["mtd_executions"]],
            })
    return out


def _sums(r: dict, src: dict) -> tuple[np.ndarray, np.ndarray]:
    """Compromises and live seconds by bin around each of ``r``'s deployments,
    read on ``src``: ``r`` itself, or its seed's no-defence run (the placebo)."""
    num = np.zeros(len(EDGES) - 1)
    den = np.zeros(len(EDGES) - 1)
    c, T = src["comp"], src["T"]
    for t in r["landings"]:
        if t >= T:
            continue
        lo = np.clip(t + EDGES[:-1], 0, T)
        hi = np.clip(t + EDGES[1:], 0, T)
        den += hi - lo
        # a compromise at the run's last instant is counted in the bin that ends
        # there, and only there: bins wholly after the run (lo == hi == T) count
        # nothing (round-2 review, 2026-09-24: the first form re-counted it in
        # every later bin, +20..40 s on the model's time lost)
        upto = np.where(hi >= T, np.searchsorted(c, hi, "right"), np.searchsorted(c, hi, "left"))
        cnt = upto - np.searchsorted(c, lo, "left")
        num += np.where(hi > lo, cnt, 0)
    return num, den


def _stack(runs: list[dict], none: dict | None) -> tuple[np.ndarray, np.ndarray]:
    num = np.zeros((len(runs), len(EDGES) - 1))
    den = np.zeros((len(runs), len(EDGES) - 1))
    for i, r in enumerate(runs):
        src = r if none is None else none[(r["arm"], r["profile"], r["seed"])]
        num[i], den[i] = _sums(r, src)
    return num, den


def _relative(num: np.ndarray, den: np.ndarray) -> np.ndarray:
    pre = num[PRE].sum() / den[PRE].sum()
    return 100 * (num / np.where(den > 0, den, np.nan)) / pre


def _time_lost(num: np.ndarray, den: np.ndarray) -> float:
    pre = num[PRE].sum() / den[PRE].sum()
    post = ~PRE
    rate = num[post] / np.where(den[post] > 0, den[post], np.nan)
    return float(np.nansum((1 - rate / pre) * np.diff(EDGES)[post]))


def read(runs: list[dict], none: dict, rng: np.random.Generator | None) -> dict:
    num, den = _stack(runs, None)
    pnum, pden = _stack(runs, none)
    n, d, pn, pd = num.sum(0), den.sum(0), pnum.sum(0), pden.sum(0)
    pre = n[PRE].sum() / d[PRE].sum()
    out = {"runs": len(runs), "deployments": int(sum(len(r["landings"]) for r in runs)),
           "deployment_seconds_median": float(np.median([x for r in runs for x in r["durations"]])),
           "pre_rate_per_ksec": 1000 * pre,
           "relative_pct": _relative(n, d).tolist(), "placebo_relative_pct": _relative(pn, pd).tolist(),
           "compromises": n.tolist(), "live_seconds": d.tolist()}
    if rng is not None:
        raw, plac = _time_lost(n, d), _time_lost(pn, pd)
        idx = rng.integers(0, len(runs), size=(N_BOOT, len(runs)))
        boots = np.array([_time_lost(num[row].sum(0), den[row].sum(0)) - _time_lost(pnum[row].sum(0), pden[row].sum(0))
                          for row in idx])
        out["time_lost"] = {"seconds": raw - plac, "lo": float(np.percentile(boots, 2.5)),
                            "hi": float(np.percentile(boots, 97.5)), "uncorrected_seconds": raw,
                            "placebo_seconds": plac, "hosts_per_deployment": (raw - plac) * pre}
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--intervals", default="2000,200")
    args = ap.parse_args()
    intervals = {int(x) for x in args.intervals.split(",")}
    runs = load(intervals)
    none = {(r["arm"], r["profile"], r["seed"]): r for r in runs if r["cond"] == "none"}
    rng = np.random.default_rng(SEED)
    out = {"edges": EDGES.tolist(), "anchor": "deployment completion (the rewrite lands)",
           "pooled": "four profiles for the APT attacker model; single-mechanism conditions",
           "reads": {}, "none_rate_per_ksec": {}}
    for arm in ("movement", "baseline"):
        nr = [r for r in runs if r["arm"] == arm and r["cond"] == "none"]
        out["none_rate_per_ksec"][arm] = 1000 * sum(len(r["comp"]) for r in nr) / sum(r["T"] for r in nr)
    for iv in sorted(intervals):
        per_deployment = iv >= EDGES[-1] - EDGES[0]  # else the window spans several deployments
        for arm in ("movement", "baseline"):
            for key, group in (("all", MECHANISMS), ("host", HOST), ("service", SERVICE)) + tuple((m, (m,)) for m in MECHANISMS):
                rs = [r for r in runs if r["arm"] == arm and r["cond"] in group and r["interval"] == iv]
                out["reads"][f"{arm}|{key}|{iv}"] = read(rs, none, rng if (per_deployment and key in MECHANISMS) else None)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"wrote {OUT.relative_to(HERE.parents[2])}")
    for iv in sorted(intervals):
        print(f"\n== interval {iv} s ==")
        for key in ("all", "host", "service") + MECHANISMS:
            for arm in ("movement", "baseline"):
                c = out["reads"][f"{arm}|{key}|{iv}"]
                line = (f"  {arm:9s} {key:18s} dep {c['deployments']:6d} pre {c['pre_rate_per_ksec']:.2f}/ks  "
                        + " ".join(f"{v:4.0f}" for v in c["relative_pct"]))
                tl = c.get("time_lost")
                if tl:
                    line += (f"\n  {'':28s} placebo " + " ".join(f"{v:4.0f}" for v in c["placebo_relative_pct"])
                             + f"\n  {'':28s} time lost {tl['seconds']:5.0f} s [{tl['lo']:5.0f}, {tl['hi']:5.0f}]  "
                             f"(uncorrected {tl['uncorrected_seconds']:4.0f}, placebo {tl['placebo_seconds']:4.0f}; "
                             f"{tl['hosts_per_deployment']:.3f} hosts)")
                print(line)


if __name__ == "__main__":
    main()
