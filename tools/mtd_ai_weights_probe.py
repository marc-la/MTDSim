"""Forensic probe over the archived Tay/Ho DDQN weights.

Answers three questions about a directory of `.h5` MTDShield checkpoints,
without running the simulator:

1. **shape**  — what state/time-series/action signature does each model expect?
   This decides which models the live `get_state_and_time_series` can feed at all.
2. **steps**  — how many gradient updates did each model actually receive?
   `mtd_ai_training` calls `model.fit(...)` on a *single* sample, so every
   BatchNormalization layer on the dense path sees a batch variance of exactly 0
   and its `moving_variance` decays as `momentum ** n` (Keras default 0.99).
   Inverting that gives a direct step count — and `moving_variance == 1.0`
   proves the model never trained at all.
3. **policy** — is the greedy policy degenerate? Sampling plausible states and
   counting the argmax distribution separates "a model that discriminates" from
   "a constant-action deployer".

Usage:

    PYTHONPATH=. python tools/mtd_ai_weights_probe.py mtdsim-weights-archive/
    PYTHONPATH=. python tools/mtd_ai_weights_probe.py mtdsim-weights-archive/ --filter gamma_ epsilon_

Read-only: it loads checkpoints and never writes one back.
"""

from __future__ import annotations

import argparse
import collections
import glob
import math
import os
import sys

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import numpy as np  # noqa: E402

# Keras default BatchNormalization momentum. `create_network` never overrides it.
BN_MOMENTUM = 0.99

# The probe's sampling ranges for the 8-static / 3-time-series signature that
# every one of Tay's own sweep checkpoints carries. Order is the one produced by
# the commented-out `get_state_and_time_series` in `mtd_ai_operation.py`.
STATIC_RANGES = [
    ("host_compromise_ratio", 0.0, 1.0),
    ("exposed_endpoints", 1.0, 20.0),
    ("attack_path_exposure", 0.0, 10.0),
    ("overall_asr_avg", 0.0, 1.0),
    ("roa", 0.0, 50.0),
    ("shortest_path_variability", 0.0, 2.0),
    ("risk", 0.0, 10.0),
    ("attack_type", 1.0, 7.0),
]
TIME_RANGES = [
    ("mtd_freq", 0.0, 0.05),
    ("overall_mttc_avg", 0.0, 500.0),
    ("time_since_last_mtd", 0.0, 3000.0),
]


def _sample_states(n, state_size, time_size, seed=0):
    rng = np.random.default_rng(seed)

    def draw(ranges, width):
        cols = []
        for i in range(width):
            _, lo, hi = ranges[i] if i < len(ranges) else ("pad", 0.0, 1.0)
            cols.append(rng.uniform(lo, hi, n))
        return np.column_stack(cols).astype("float32")

    static = draw(STATIC_RANGES, state_size)
    series = draw(TIME_RANGES, time_size).reshape(n, time_size, 1)
    return static, series


def _gradient_steps(model, keras):
    """Invert `moving_variance = momentum ** n` on the first dense-path BN layer.

    Returns (moving_variance, steps) where steps is 0 for an untrained layer and
    `math.inf` once float32 has underflowed (roughly n > 10 300).
    """
    bns = [l for l in model.layers if isinstance(l, keras.layers.BatchNormalization)]
    if not bns:
        return None, None
    mv = float(np.median(np.asarray(bns[0].moving_variance.numpy())))
    if mv >= 1.0:
        return mv, 0
    if mv <= 0.0:
        return mv, math.inf
    return mv, math.log(mv) / math.log(BN_MOMENTUM)


def _policy_entropy(model, n_samples, seed):
    state_size = int(model.inputs[0].shape[-1])
    time_size = int(model.inputs[1].shape[1])
    static, series = _sample_states(n_samples, state_size, time_size, seed=seed)
    q = model.predict([static, series], verbose=0)
    argmax = np.argmax(q, axis=1)
    counts = collections.Counter(argmax.tolist())
    dist = [counts.get(i, 0) / n_samples for i in range(q.shape[1])]
    p = np.array([d for d in dist if d > 0])
    entropy = float(-(p * np.log2(p)).sum())
    ordered = np.sort(q, axis=1)
    gap = float(np.mean(ordered[:, -1] - ordered[:, -2]))
    return dist, entropy, gap


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", help="directory of .h5 checkpoints")
    parser.add_argument(
        "--filter",
        nargs="*",
        default=None,
        help="only probe files whose basename contains one of these substrings",
    )
    parser.add_argument("--samples", type=int, default=400)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--no-policy",
        action="store_true",
        help="skip the policy probe (much faster; shapes and step counts only)",
    )
    args = parser.parse_args(argv)

    import keras

    paths = sorted(glob.glob(os.path.join(args.archive, "*.h5")))
    if args.filter:
        paths = [p for p in paths if any(f in os.path.basename(p) for f in args.filter)]
    if not paths:
        print(f"no checkpoints matched under {args.archive}", file=sys.stderr)
        return 1

    signatures = collections.Counter()
    degenerate = untrained = 0

    header = f"{'model':<52} {'signature':<26} {'steps':>10}"
    if not args.no_policy:
        header += f" {'entropy':>8} {'argmax distribution':<24}"
    print(header)

    for path in paths:
        name = os.path.basename(path)[:52]
        try:
            model = keras.models.load_model(path, compile=False)
        except Exception as exc:  # noqa: BLE001 — a load failure is a result here
            print(f"{name:<52} LOAD FAILED: {type(exc).__name__}")
            continue

        sig = (
            f"{int(model.inputs[0].shape[-1])}/"
            f"{int(model.inputs[1].shape[1])} -> {int(model.outputs[0].shape[-1])}"
        )
        signatures[sig] += 1

        _, steps = _gradient_steps(model, keras)
        if steps == 0:
            steps_str = "NEVER"
            untrained += 1
        elif steps == math.inf:
            steps_str = ">1e4"
        else:
            steps_str = f"{steps:.0f}"

        row = f"{name:<52} {sig:<26} {steps_str:>10}"
        if not args.no_policy:
            dist, entropy, _gap = _policy_entropy(model, args.samples, args.seed)
            if entropy < 0.5:
                degenerate += 1
            row += f" {entropy:8.3f} {' '.join(f'{d:.2f}' for d in dist):<24}"
        print(row)

    print()
    print(f"{len(paths)} checkpoints probed")
    for sig, count in signatures.most_common():
        print(f"  {count:>4}  signature {sig}")
    print(f"  {untrained:>4}  never received a gradient step (moving_variance == 1.0)")
    if not args.no_policy:
        print(f"  {degenerate:>4}  degenerate policy (entropy < 0.5 bits over sampled states)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
