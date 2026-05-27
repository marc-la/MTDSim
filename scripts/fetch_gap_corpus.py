#!/usr/bin/env python3
"""Acquire the gitignored upstream inputs for the L1 GAP build.

Per ``docs/specs/01_gap_schema.md`` Decision 4, the upstream corpora are
consumed from a gitignored local copy; only the distilled per-flow extracts +
the aggregated GAP are committed. This script materialises those inputs
reproducibly:

1. The 40 MITRE CTID Attack Flow corpus flows, as **STIX 2.1 bundles**, taken
   from CTID's own published lossless export (the corpus ships only ``.afb``
   Builder files; CTID exports them to STIX for its docs site). Pinned to the
   v3.1.1 release content.
2. The MITRE ATT&CK Enterprise STIX bundle (node metadata: technique names,
   tactics, platforms), pinned to a specific ATT&CK version.

Both land under ``data/gap/_corpus_stix/`` and ``data/gap/_attack/`` (gitignored).
Idempotent: existing non-empty files are skipped unless ``--force`` is given.

Usage::

    python scripts/fetch_gap_corpus.py [--force]

Network access required. Apache-2.0 (Attack Flow) / ATT&CK Terms of Use —
attribution preserved in data/gap/README.md.
"""

from __future__ import annotations

import argparse
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# --- Pinned provenance -------------------------------------------------------

# Attack Flow corpus: latest release tag is v3.1.1 (the python package version
# string is 3.2.0; the STIX extension schema is 2.0.0). CTID publishes the
# STIX export of each corpus flow at this base URL.
CORPUS_REF = "attack-flow@v3.1.1 (pkg 3.2.0); STIX 2.0.0 extension"
CORPUS_BASE_URL = (
    "https://center-for-threat-informed-defense.github.io/attack-flow/corpus/"
)

# ATT&CK Enterprise STIX (node metadata). Latest in attack-stix-data at pin time.
ATTACK_VERSION = "19.1"
ATTACK_URL = (
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/"
    f"master/enterprise-attack/enterprise-attack-{ATTACK_VERSION}.json"
)

# The 40 corpus flow names (filename stems of corpus/*.afb at v3.1.1). Pinned
# explicitly so the build is reproducible without cloning the upstream repo.
FLOW_NAMES = [
    "Black Basta Ransomware",
    "CISA AA22-138B VMWare Workspace (Alt)",
    "CISA AA22-138B VMWare Workspace (TA1)",
    "CISA AA22-138B VMWare Workspace (TA2)",
    "CISA Iranian APT",
    "Cobalt Kitty Campaign",
    "Conti CISA Alert",
    "Conti PWC",
    "Conti Ransomware",
    "DFIR - BumbleBee Round 2",
    "Equifax Breach",
    "Example Attack Tree",
    "FIN13 Case 1",
    "FIN13 Case 2",
    "Gootloader",
    "Hancitor DLL",
    "Ivanti Vulnerabilities",
    "JP Morgan Breach",
    "MITRE NERVE",
    "Maastricht University Ransomware",
    "Mac Malware Steals Crypto",
    "Marriott Breach",
    "Muddy Water",
    "NotPetya",
    "OceanLotus",
    "OpenClaw",
    "REvil",
    "Ragnar Locker",
    "SWIFT Heist",
    "SearchAwesome Adware",
    "Shamoon",
    "SolarWinds",
    "Sony Malware",
    "Target Breach",
    "Tesla Kubernetes Breach",
    "ToolShell Vulnerability in Sharepoint",
    "Turla - Carbon Emulation Plan",
    "Turla - Snake Emulation Plan",
    "Uber Breach",
    "WhisperGate",
]

_REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = _REPO_ROOT / "data" / "gap" / "_corpus_stix"
ATTACK_DIR = _REPO_ROOT / "data" / "gap" / "_attack"


def _download(url: str, dest: Path, force: bool) -> str:
    """Fetch ``url`` to ``dest``; return 'ok' | 'skip' | 'fail: ...'."""
    if dest.exists() and dest.stat().st_size > 0 and not force:
        return "skip"
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url, timeout=120) as resp:
            data = resp.read()
        dest.write_bytes(data)
        return "ok"
    except Exception as exc:  # noqa: BLE001 — report, don't abort the batch
        return f"fail: {type(exc).__name__}: {exc}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="re-download existing files")
    args = ap.parse_args()

    print(f"GAP corpus acquisition\n  corpus_ref:   {CORPUS_REF}\n"
          f"  attack:       enterprise-attack-{ATTACK_VERSION}\n"
          f"  -> {CORPUS_DIR}\n  -> {ATTACK_DIR}\n")

    # 1. Attack Flow corpus (STIX export)
    counts = {"ok": 0, "skip": 0, "fail": 0}
    failures = []
    for name in FLOW_NAMES:
        url = CORPUS_BASE_URL + urllib.parse.quote(name) + ".json"
        status = _download(url, CORPUS_DIR / f"{name}.json", args.force)
        key = "fail" if status.startswith("fail") else status
        counts[key] += 1
        if key == "fail":
            failures.append((name, status))
    print(f"Attack Flow corpus: {counts['ok']} downloaded, "
          f"{counts['skip']} cached, {counts['fail']} failed "
          f"(of {len(FLOW_NAMES)})")
    for name, status in failures:
        print(f"  FAIL {name}: {status}")

    # 2. ATT&CK Enterprise STIX
    attack_dest = ATTACK_DIR / f"enterprise-attack-{ATTACK_VERSION}.json"
    status = _download(ATTACK_URL, attack_dest, args.force)
    size_mb = attack_dest.stat().st_size / 1e6 if attack_dest.exists() else 0
    print(f"ATT&CK Enterprise: {status} ({size_mb:.1f} MB)")

    ok = counts["fail"] == 0 and not status.startswith("fail")
    print("\nDone." if ok else "\nDone with errors.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
