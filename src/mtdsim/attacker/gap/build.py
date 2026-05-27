"""Top-level GAP build: corpus STIX + ATT&CK -> per-flow extracts + aggregate.

Reads the gitignored inputs acquired by ``scripts/fetch_gap_corpus.py``,
produces the committed artefacts:

- ``data/gap/flows/<flow_id>.yaml`` — one lossless per-flow extract per flow.
- ``data/gap/gap_v<version>.json`` — the aggregated GAP.

Library entry points: :func:`build_gap` / :func:`persist_extracts` /
:func:`persist_gap`. The CLI runner lives at ``scripts/build_gap.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

from mtdsim.attacker.gap.aggregate import aggregate_gap
from mtdsim.attacker.gap.attack_flow_parser import parse_flow_file
from mtdsim.attacker.gap.attack_stix import load_attack_taxonomy, load_attack_techniques
from mtdsim.attacker.gap.schema import GeneralisedAttackProfile, PerFlowExtract

# --- pinned provenance (mirrors scripts/fetch_gap_corpus.py) -----------------
VERSION = "0.5"
CORPUS_REF = "attack-flow@v3.1.1 (pkg 3.2.0); STIX 2.0.0 extension; CTID published export"
ATTACK_SOURCE = "enterprise-attack-19.1"

_REPO_ROOT = Path(__file__).resolve().parents[4]
CORPUS_STIX_DIR = _REPO_ROOT / "data" / "gap" / "_corpus_stix"
ATTACK_DIR = _REPO_ROOT / "data" / "gap" / "_attack"
FLOWS_OUT_DIR = _REPO_ROOT / "data" / "gap" / "flows"
GAP_OUT_PATH = _REPO_ROOT / "data" / "gap" / f"gap_v{VERSION}.json"


def _resolve_attack_bundle(attack_path) -> Path:
    if attack_path is not None:
        return Path(attack_path)
    found = sorted(ATTACK_DIR.glob("enterprise-attack-*.json"))
    if not found:
        raise FileNotFoundError(
            f"No ATT&CK bundle in {ATTACK_DIR}. Run scripts/fetch_gap_corpus.py first."
        )
    return found[-1]


def build_gap(
    corpus_stix_dir=CORPUS_STIX_DIR,
    attack_stix_path=None,
    *,
    version: str = VERSION,
    corpus_ref: str = CORPUS_REF,
    attack_source: str = ATTACK_SOURCE,
) -> tuple[list[PerFlowExtract], GeneralisedAttackProfile]:
    """Parse every corpus flow + aggregate. Returns (extracts, gap)."""
    corpus_stix_dir = Path(corpus_stix_dir)
    attack_bundle = _resolve_attack_bundle(attack_stix_path)

    with open(attack_bundle) as f:
        attack_obj = json.load(f)
    taxonomy = load_attack_taxonomy(attack_obj)
    attack_meta = load_attack_techniques(attack_obj, taxonomy)

    flow_files = sorted(corpus_stix_dir.glob("*.json"))
    if not flow_files:
        raise FileNotFoundError(
            f"No corpus flows in {corpus_stix_dir}. Run scripts/fetch_gap_corpus.py first."
        )
    extracts = [
        parse_flow_file(p, tactic_id_to_name=taxonomy.id_to_name) for p in flow_files
    ]

    schema_versions = {e.schema_version for e in extracts}
    af_schema = sorted(schema_versions)[0] if schema_versions else "2.0.0"

    gap = aggregate_gap(
        extracts,
        attack_meta,
        taxonomy,
        version=version,
        corpus_ref=corpus_ref,
        attack_source=attack_source,
        attack_flow_schema_version=af_schema,
    )
    return extracts, gap


def persist_extracts(extracts: list[PerFlowExtract], flows_dir=FLOWS_OUT_DIR) -> None:
    flows_dir = Path(flows_dir)
    flows_dir.mkdir(parents=True, exist_ok=True)
    for ex in extracts:
        (flows_dir / f"{ex.flow_id}.yaml").write_text(ex.to_yaml())


def persist_gap(gap: GeneralisedAttackProfile, gap_path=GAP_OUT_PATH) -> None:
    Path(gap_path).parent.mkdir(parents=True, exist_ok=True)
    gap.to_json(gap_path)
