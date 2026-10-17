"""Scott-Knott ESD: rank treatments into groups, ties shared (Marc 2026-09-25:
"ranking with ties ... what's conventional, what's defensible"; guidance in
docs/handoffs/2026-09-20_ch5_s52_s54_results_context.md §8j-4).

Two steps, as Tantithamthavorn, McIntosh, Hassan & Matsumoto (2017, IEEE TSE
43(1):1-18) describe the ESD test:

1. **Scott & Knott (1974, Biometrics 30(3):507-512).** Sort the treatment
   means; split the set where the between-groups sum of squares is largest,
   and keep the split only if the likelihood-ratio statistic lambda exceeds
   the chi-square critical value at ``alpha`` on g/(pi-2) degrees of freedom;
   recurse into both halves. A line-for-line port of ``MaxValue`` from the
   ScottKnott R package 1.2-7 (J. C. Faria), written as a recursion (the R
   function walks the same tree pre-order).
2. **The ESD merge.** Adjacent groups whose difference is negligible,
   |Cohen's d| < 0.2 on the two groups' pooled observations (pooled standard
   deviation, as effsize::cohen.d), are merged, the smallest first, until no
   adjacent pair is negligible.

Note: ScottKnottESD 2.0.3 on CRAN drops step 1's test and splits on effect
size alone; this module keeps it, so a split must be both significant and
non-negligible. Groups are ranked densely from the highest mean (1, 2, 2, 3):
treatments in one group share a rank.

Assumes equal replicates per treatment (asserted) and uses the one-way ANOVA
residual mean square, as the R package does.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.stats import chi2

NEGLIGIBLE = 0.2


def cohen_d(a: np.ndarray, b: np.ndarray) -> float:
    """(mean a - mean b) / pooled standard deviation."""
    na, nb = len(a), len(b)
    s = math.sqrt(((na - 1) * np.var(a, ddof=1) + (nb - 1) * np.var(b, ddof=1)) / (na + nb - 2))
    diff = float(np.mean(a) - np.mean(b))
    if s == 0.0:
        return 0.0 if diff == 0.0 else math.copysign(math.inf, diff)
    return diff / s


def _partition(means: np.ndarray, mmse: float, dfr: int, alpha: float) -> tuple[list[list[int]], list[dict]]:
    """Scott-Knott on means sorted high to low; groups as index lists, and a
    record of every node's test."""
    tests: list[dict] = []

    def split(lo: int, hi: int) -> list[list[int]]:
        g = hi - lo + 1
        if g == 1:
            return [[lo]]
        best, b0 = lo, -1.0
        for k1 in range(lo, hi):
            t1, t2 = means[lo:k1 + 1].sum(), means[k1 + 1:hi + 1].sum()
            ss = t1 ** 2 / (k1 - lo + 1) + t2 ** 2 / (hi - k1) - (t1 + t2) ** 2 / g
            if ss > b0:  # the first maximiser, as R's order(..., decreasing=TRUE)[1]
                best, b0 = k1, ss
        m = means[lo:hi + 1]
        si02 = (float(np.sum((m - m.mean()) ** 2)) + dfr * mmse) / (g + dfr)
        lam = (math.pi / (2 * (math.pi - 2))) * b0 / si02
        crit = float(chi2.ppf(1 - alpha, g / (math.pi - 2)))
        tests.append({"lo": lo, "hi": hi, "cut": best, "lambda": lam, "critical": crit, "split": lam > crit})
        if lam <= crit:
            return [list(range(lo, hi + 1))]
        return split(lo, best) + split(best + 1, hi)

    return split(0, len(means) - 1), tests


def sk_esd(samples: dict[str, np.ndarray], alpha: float = 0.05, *, best: str = "high") -> dict:
    """``samples``: treatment -> observations (equal counts). ``best``: "high"
    ranks the largest mean first, "low" the smallest (hosts compromised: fewer
    is better). Returns the dense rank per treatment, the final groups, the
    Scott-Knott groups before the merge, the merges with their d, and the ANOVA
    terms; ``means`` are in the observations' own sign."""
    assert best in ("high", "low")
    if best == "low":  # the test is symmetric in sign: negate, rank, restore
        out = sk_esd({c: -np.asarray(v, dtype=float) for c, v in samples.items()}, alpha, best="high")
        out["means"] = {c: -m for c, m in out["means"].items()}
        out["best"] = "low"
        return out
    names = list(samples)
    ns = {len(v) for v in samples.values()}
    assert len(ns) == 1, f"unequal replicates {ns}"
    n = ns.pop()
    order = sorted(names, key=lambda c: -float(np.mean(samples[c])))
    means = np.array([float(np.mean(samples[c])) for c in order])
    sse = sum(float(np.sum((samples[c] - np.mean(samples[c])) ** 2)) for c in order)
    dfr = len(order) * (n - 1)
    mse = sse / dfr
    idx_groups, tests = _partition(means, mse / n, dfr, alpha)
    groups = [[order[i] for i in grp] for grp in idx_groups]
    sk_groups = [list(g) for g in groups]
    merges = []
    while len(groups) > 1:
        ds = [abs(cohen_d(np.concatenate([samples[c] for c in groups[j]]),
                          np.concatenate([samples[c] for c in groups[j + 1]]))) for j in range(len(groups) - 1)]
        j = int(np.argmin(ds))
        if ds[j] >= NEGLIGIBLE:
            break
        merges.append({"upper": groups[j], "lower": groups[j + 1], "d": ds[j]})
        groups[j:j + 2] = [groups[j] + groups[j + 1]]
    rank = {c: r + 1 for r, grp in enumerate(groups) for c in grp}
    return {"rank": rank, "groups": groups, "sk_groups": sk_groups, "merges": merges,
            "tests": [{**t, "cut_after": order[t["cut"]], "treatments": order[t["lo"]:t["hi"] + 1]} for t in tests],
            "alpha": alpha, "negligible_d": NEGLIGIBLE, "n_per_treatment": n, "mse": mse, "df_residual": dfr,
            "order": order, "means": dict(zip(order, means.tolist())), "best": "high"}
