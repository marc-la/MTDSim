"""CLI for L0 corpus acquisition — ``python -m mtdsim.l0_cti``.

See :mod:`mtdsim.l0_cti.fetch` for the library entry point. Acquires the
gitignored inputs under ``data/gap/_corpus_stix/`` and ``data/gap/_attack/``.
"""

from __future__ import annotations

import argparse
import sys

from mtdsim.l0_cti.fetch import (
    ATTACK_DIR,
    ATTACK_VERSION,
    CORPUS_DIR,
    CORPUS_REF,
    FLOW_NAMES,
    fetch_corpus,
)


def main() -> int:
    ap = argparse.ArgumentParser(prog="python -m mtdsim.l0_cti", description=__doc__)
    ap.add_argument("--force", action="store_true", help="re-download existing files")
    args = ap.parse_args()

    print(f"GAP corpus acquisition\n  corpus_ref:   {CORPUS_REF}\n"
          f"  attack:       enterprise-attack-{ATTACK_VERSION}\n"
          f"  -> {CORPUS_DIR}\n  -> {ATTACK_DIR}\n")

    report = fetch_corpus(args.force)
    counts = report["corpus"]
    print(f"Attack Flow corpus: {counts['ok']} downloaded, "
          f"{counts['skip']} cached, {counts['fail']} failed "
          f"(of {len(FLOW_NAMES)})")
    for name, status in report["failures"]:
        print(f"  FAIL {name}: {status}")

    attack = report["attack"]
    print(f"ATT&CK Enterprise: {attack['status']} ({attack['size_mb']:.1f} MB)")

    ok = counts["fail"] == 0 and not attack["status"].startswith("fail")
    print("\nDone." if ok else "\nDone with errors.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
