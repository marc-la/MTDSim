#!/usr/bin/env python3
"""Reduced pedagogical exemplar of the Volt Typhoon Attack Flow (ch3 schema figure).

Purpose
-------
The full 67-node flow (`build_volt_typhoon_aa24038a.py`) is the evidence artefact.
THIS is the "keep-it-simple" teaching subset for the ch3 §3.1.2 schema exemplar —
the figure that replaces the 2018 Tesla flow (Marc's ruling, 2026-08-31).

It is a **true induced subgraph of the full flow**: every node and every edge here
also exists in `volt_typhoon_aa24038a.json`, so the figure never diverges from the
evidence artefact. 13 nodes / 14 edges showing the whole Attack Flow grammar on one
legible APT spine:
  - an entry **condition** (unpatched appliance) → the exploit;
  - an **OR operator** (either credential source satisfies the join);
  - **effect edges** carrying precondition semantics along the NTDS.dit procedure
    (RDP-to-DC → vssadmin shadow copy → ntdsutil copy → NTDS.dit → offline crack);
  - a terminal **condition** encoding the restraint finding (pre-positioned, no
    destructive action).

Emits, in this directory:
  volt_typhoon_exemplar.afb    -- Attack Flow Builder file (schema attack_flow_v2).
                                  Open in the Attack Flow Builder, tidy the layout,
                                  and export SVG for the thesis.
  volt_typhoon_exemplar.json   -- the same subset as a STIX 2.1 bundle (validated by
                                  the repo parser; a fallback + round-trip check).

The .afb structure (nodes with 12 angle-anchors; edges as dynamic_line ->
generic_latch pairs sitting in node anchors, each with a generic_handle; layout +
camera) is cloned from the corpus Tesla .afb invariants. It cannot be validated
locally (the Builder is a web app; the AF CLI won't run in this conda env), so it is
best-effort: confirm by opening it in the Builder. The subset STIX bundle IS locally
validated, and the manual build recipe in README covers the fallback.

Run:
    PYTHONPATH=src python3 data/gap/hand_curated/build_volt_typhoon_exemplar.py
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
NS = uuid.uuid5(uuid.NAMESPACE_URL, "mtdsim:hand_curated:volt_typhoon_exemplar")
AF_EXT = "extension-definition--fb9c968a-745b-4ade-9b25-c324172197f4"
TS = "2024-02-08T00:00:00.000Z"

TACTIC_REF = {
    "TA0001": "x-mitre-tactic--ffd5bcee-6e16-4dd2-8eca-7b3beedf33ca",
    "TA0002": "x-mitre-tactic--4ca45d45-df4d-4613-8980-bac22d278fa5",
    "TA0003": "x-mitre-tactic--5bc1d813-693e-4823-9961-abf9af4b0e92",
    "TA0004": "x-mitre-tactic--5e29b093-294e-49e9-a803-dab3d73b77dd",
    "TA0005": "x-mitre-tactic--78b23412-0651-46d7-a540-170a1ce8bd5a",
    "TA0006": "x-mitre-tactic--2558fd61-8c75-4730-94c4-11926db2a263",
    "TA0008": "x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e",
}
TECH_REF = {
    "T1190": "attack-pattern--3f886f2a-874f-4333-b794-aa6075009b1c",
    "T1068": "attack-pattern--b21c3b2d-02e6-45b1-980b-e69051040839",
    "T1552": "attack-pattern--435dfb86-2697-4867-85b5-2fef496c0517",
    "T1078": "attack-pattern--b17a1a56-e99c-403c-8948-561df0cffe81",
    "T1021.001": "attack-pattern--eb062747-2193-45de-8fa2-e62549c37ddf",
    "T1006": "attack-pattern--0c8ab3eb-df48-4b9c-ace7-beacaac81cc5",
    "T1047": "attack-pattern--01a5a209-b94c-450b-b7f9-946497d91055",
    "T1003.003": "attack-pattern--edf91964-b26e-4b4a-9600-ccacd7d7df24",
    "T1110.002": "attack-pattern--1d24cdee-9ea2-4189-b08e-af110bf2435d",
    "T1563": "attack-pattern--5b0ad6f8-6a16-4966-a4ef-d09ea6e2a9f5",
}

# ---------------------------------------------------------------------------
# Subset model: (key, kind, payload, level, col)  -- level/col drive the layout.
# kind: action | condition | operator
# ---------------------------------------------------------------------------
NODES = [
    ("c0", "condition", dict(description="Unpatched public-facing appliance "
        "(e.g. FortiGate 300D, CVE-2022-42475)"), 0, 0),
    ("a1", "action", dict(tid="T1190", tactic="TA0001", name="Exploit Public-Facing Application",
        desc="Exploits a vulnerability in a public-facing network appliance."), 1, 0),
    ("a2", "action", dict(tid="T1068", tactic="TA0004", name="Exploitation for Privilege Escalation",
        desc="Obtains admin credentials via a privilege-escalation vulnerability."), 2, -1),
    ("a3", "action", dict(tid="T1552", tactic="TA0006", name="Unsecured Credentials",
        desc="Obtains a credential insecurely stored on the appliance."), 2, 1),
    ("o1", "operator", dict(operator="OR"), 3, 0),
    ("a4", "action", dict(tid="T1078", tactic="TA0003", name="Valid Accounts",
        desc="Uses valid administrator credentials for persistence and access."), 4, 0),
    ("a5", "action", dict(tid="T1021.001", tactic="TA0008", name="Remote Services: Remote Desktop Protocol",
        desc="Moves laterally to the domain controller over RDP."), 5, 0),
    ("a6", "action", dict(tid="T1006", tactic="TA0005", name="Direct Volume Access",
        desc="Runs vssadmin to create a volume shadow copy on the DC."), 6, 0),
    ("a7", "action", dict(tid="T1047", tactic="TA0002", name="Windows Management Instrumentation",
        desc="Uses WMIC/ntdsutil to copy NTDS.dit from the shadow copy."), 7, 0),
    ("a8", "action", dict(tid="T1003.003", tactic="TA0006", name="OS Credential Dumping: NTDS",
        desc="Extracts the Active Directory database (NTDS.dit) -> full domain compromise."), 8, 0),
    ("a9", "action", dict(tid="T1110.002", tactic="TA0006", name="Brute Force: Password Cracking",
        desc="Cracks the extracted hashes offline."), 9, 0),
    ("a10", "action", dict(tid="T1563", tactic="TA0008", name="Remote Service Session Hijacking",
        desc="Uses recovered access to reach OT-adjacent systems."), 10, 0),
    ("c1", "condition", dict(description="Pre-positioned for OT disruption; "
        "no destructive action executed"), 11, 0),
]
# (source, target, branch)  branch in {None,'True'} -- from a condition uses on_true.
EDGES = [
    ("c0", "a1", "True"),
    ("a1", "a2", None), ("a1", "a3", None),
    ("a2", "o1", None), ("a3", "o1", None), ("o1", "a4", None),
    ("a4", "a5", None), ("a5", "a6", None), ("a6", "a7", None), ("a7", "a8", None),
    ("a8", "a9", None), ("a9", "a10", None), ("a10", "c1", None),
]

NODE = {k: (kind, payload, lvl, col) for k, kind, payload, lvl, col in NODES}

# ===========================================================================
# 1) STIX 2.1 bundle (the parseable form; validated by the repo parser).
# ===========================================================================
def duid(key: str) -> str:
    b = bytearray(uuid.uuid5(NS, key).bytes)
    b[6] = (b[6] & 0x0F) | 0x40
    b[8] = (b[8] & 0x3F) | 0x80
    return str(uuid.UUID(bytes=bytes(b)))

def sid(kind, key):
    return f"{kind}--{duid(kind + ':' + key)}"

ext_block = {AF_EXT: {"extension_type": "new-sdo"}}
stix_id = {}
for k, (kind, *_rest) in NODE.items():
    stix_id[k] = sid({"action": "attack-action", "condition": "attack-condition",
                      "operator": "attack-operator"}[kind], k)

eff = {k: [] for k in NODE}
ontrue = {k: [] for k in NODE if NODE[k][0] == "condition"}
for s, t, br in EDGES:
    if NODE[s][0] == "condition":
        ontrue[s].append(stix_id[t])
    else:
        eff[s].append(stix_id[t])
incoming = {t for _, t, _ in EDGES}
starts = [k for k in NODE if k not in incoming]

objects = []
flow_id = "attack-flow--" + duid("flow")
identity_id = "identity--" + duid("identity")
objects.append({
    "type": "attack-flow", "id": flow_id, "spec_version": "2.1",
    "created": TS, "modified": TS, "extensions": ext_block, "created_by_ref": identity_id,
    "start_refs": [stix_id[k] for k in starts],
    "name": "Volt Typhoon — Attack Flow schema exemplar (AA24-038A subset)",
    "description": ("A 13-node teaching subset of the Volt Typhoon flow: entry condition, "
                    "an OR operator over two credential sources, the NTDS.dit effect-edge "
                    "chain, and a terminal restraint condition. Induced subgraph of the full "
                    "hand-curated flow; source AA24-038A."),
    "scope": "campaign",
    "external_references": [{
        "source_name": "CISA AA24-038A",
        "description": "PRC State-Sponsored Actors Compromise and Maintain Persistent Access to U.S. Critical Infrastructure. 8 Feb 2024.",
        "url": "https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a",
    }],
})
objects.append({"type": "identity", "id": identity_id, "spec_version": "2.1",
                "created": TS, "modified": TS,
                "name": "MTDSim (hand-curated from AA24-038A)", "identity_class": "organization"})
for k, (kind, p, *_r) in NODE.items():
    if kind == "action":
        o = {"type": "attack-action", "id": stix_id[k], "spec_version": "2.1",
             "created": TS, "modified": TS, "extensions": ext_block, "name": p["name"],
             "tactic_id": p["tactic"], "tactic_ref": TACTIC_REF[p["tactic"]],
             "technique_id": p["tid"], "description": p["desc"]}
        if eff[k]:
            o["effect_refs"] = eff[k]
    elif kind == "operator":
        o = {"type": "attack-operator", "id": stix_id[k], "spec_version": "2.1",
             "created": TS, "modified": TS, "extensions": ext_block, "operator": p["operator"]}
        if eff[k]:
            o["effect_refs"] = eff[k]
    else:  # condition
        o = {"type": "attack-condition", "id": stix_id[k], "spec_version": "2.1",
             "created": TS, "modified": TS, "extensions": ext_block, "description": p["description"]}
        if ontrue[k]:
            o["on_true_refs"] = ontrue[k]
    objects.append(o)
objects.append({
    "type": "extension-definition", "id": AF_EXT, "spec_version": "2.1",
    "created": "2022-08-02T19:34:35.143Z", "modified": "2022-08-02T19:34:35.143Z",
    "name": "Attack Flow", "description": "Extends STIX 2.1 with features to create Attack Flows.",
    "created_by_ref": "identity--fb9c968a-745b-4ade-9b25-c324172197f4",
    "schema": "https://center-for-threat-informed-defense.github.io/attack-flow/stix/attack-flow-schema-2.0.0.json",
    "version": "2.0.0", "extension_types": ["new-sdo"],
})
bundle = {"type": "bundle", "id": "bundle--" + duid("bundle"), "spec_version": "2.1",
          "created": TS, "modified": TS, "objects": objects}
json_path = HERE / "volt_typhoon_exemplar.json"
json_path.write_text(json.dumps(bundle, indent=2) + "\n")

# ===========================================================================
# 2) .afb Builder file (schema attack_flow_v2), cloned from Tesla invariants.
# ===========================================================================
# angle -> anchor template (identical for action/operator; conditions drop 240/270/300
# and add branch:True/branch:False, all following the same H/V assignment).
ANGLE_TYPE = {"0": "horizontal_anchor", "30": "horizontal_anchor", "60": "vertical_anchor",
              "90": "vertical_anchor", "120": "vertical_anchor", "150": "horizontal_anchor",
              "180": "horizontal_anchor", "210": "horizontal_anchor", "240": "vertical_anchor",
              "270": "vertical_anchor", "300": "vertical_anchor", "330": "horizontal_anchor"}
COND_ANGLES = ["0", "30", "60", "90", "120", "150", "180", "210", "330"]
COND_BRANCH = {"branch:True": "vertical_anchor", "branch:False": "vertical_anchor"}

DX, DY = 360, 300  # column / level spacing (px), Tesla-scale


def u(key):  # deterministic uuid (plain, .afb 'instance' style)
    return duid("afb:" + key)


afb_objects = []
layout = {}
node_instance = {}
# per-node: the anchor instance ids by angle, and each anchor's latch list.
anchor_inst = {}       # (nodekey, angle) -> anchor instance
anchor_latches = {}    # anchor instance -> list of latch instances
flow_object_ids = []   # nodes (not flow) + lines

def make_node(key, template, props):
    inst = u("node:" + key)
    node_instance[key] = inst
    kind = NODE[key][0]
    angles = (COND_ANGLES + list(COND_BRANCH)) if kind == "condition" else list(ANGLE_TYPE)
    types = dict(ANGLE_TYPE, **COND_BRANCH)
    anchors = {}
    for ang in angles:
        aid = u(f"anchor:{key}:{ang}")
        anchors[ang] = aid
        anchor_inst[(key, ang)] = aid
        anchor_latches[aid] = []
        afb_objects.append({"id": types[ang], "instance": aid, "latches": anchor_latches[aid]})
    obj = {"id": template, "instance": inst, "properties": props, "anchors": anchors}
    afb_objects.append(obj)
    flow_object_ids.append(inst)
    lvl, col = NODE[key][2], NODE[key][3]
    layout[inst] = [col * DX, lvl * DY]

# nodes
for key, (kind, p, lvl, col) in NODE.items():
    if kind == "action":
        props = [["name", p["name"]], ["tactic_id", p["tactic"]],
                 ["tactic_ref", TACTIC_REF[p["tactic"]]], ["technique_id", p["tid"]],
                 ["technique_ref", TECH_REF[p["tid"]]], ["description", p["desc"]],
                 ["confidence", None], ["execution_start", None], ["execution_end", None],
                 ["ttp", [["tactic", p["tactic"]], ["technique", p["tid"]]]]]
        make_node(key, "action", props)
    elif kind == "operator":
        make_node(key, f"{p['operator']}_operator", [["operator", p["operator"]]])
    else:
        make_node(key, "condition", [["description", p["description"]], ["pattern", None],
                                     ["pattern_type", None], ["pattern_version", None], ["date", None]])

# edges: each -> source latch (on source node bottom/branch anchor) + target latch
# (on target node top anchor) + one handle + one dynamic_line.
for s, t, br in EDGES:
    src_ang = ("branch:True" if br == "True" else "90")   # leave from bottom / true-branch
    # arrive at top (270); conditions lack 270, so fall back to a valid top-ish angle.
    tgt_ang = "270" if (t, "270") in anchor_inst else "90"
    src_anchor = anchor_inst[(s, src_ang)]
    tgt_anchor = anchor_inst[(t, tgt_ang)]
    src_latch = u(f"latch:{s}->{t}:src")
    tgt_latch = u(f"latch:{s}->{t}:tgt")
    handle = u(f"handle:{s}->{t}")
    line = u(f"line:{s}->{t}")
    afb_objects.append({"id": "generic_latch", "instance": src_latch})
    afb_objects.append({"id": "generic_latch", "instance": tgt_latch})
    afb_objects.append({"id": "generic_handle", "instance": handle})
    anchor_latches[src_anchor].append(src_latch)
    anchor_latches[tgt_anchor].append(tgt_latch)
    afb_objects.append({"id": "dynamic_line", "instance": line,
                        "source": src_latch, "target": tgt_latch, "handles": [handle]})
    flow_object_ids.append(line)
    # latches carry layout coords near their node (Builder recomputes on open).
    layout[src_latch] = list(layout[node_instance[s]])
    layout[tgt_latch] = list(layout[node_instance[t]])

# flow object (metadata card): no anchors; in layout; NOT in its own objects list.
flow_inst = u("flow")
afb_objects.insert(0, {
    "id": "flow", "instance": flow_inst,
    "properties": [
        ["name", "Volt Typhoon — Attack Flow schema exemplar (AA24-038A subset)"],
        ["description", "Teaching subset of the Volt Typhoon flow reconstructed from CISA AA24-038A."],
        ["author", [["name", "MTDSim (hand-curated from AA24-038A)"], ["identity_class", None],
                    ["contact_information", None]]],
        ["scope", "campaign"],
        ["external_references", [[u("ref:aa24038a").replace("-", ""),
            [["source_name", "CISA AA24-038A"],
             ["description", "PRC State-Sponsored Actors Compromise and Maintain Persistent Access to U.S. Critical Infrastructure. 8 Feb 2024."],
             ["url", "https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a"]]]]],
        ["created", TS],
    ],
    "objects": flow_object_ids,
})
layout[flow_inst] = [-DX * 2, 0]

# camera centred on the spine.
xs = [c[0] for c in layout.values()]; ys = [c[1] for c in layout.values()]
cam = {"x": -(min(xs) + max(xs)) / 2, "y": -(min(ys) + max(ys)) / 2, "k": 0.5}

afb = {"schema": "attack_flow_v2", "theme": "dark_theme",
       "objects": afb_objects, "layout": layout, "camera": cam}
afb_path = HERE / "volt_typhoon_exemplar.afb"
afb_path.write_text(json.dumps(afb, indent=1) + "\n")

# ===========================================================================
# 3) Validate the STIX subset via the repo parser + internal .afb consistency.
# ===========================================================================
import sys
sys.path.insert(0, str(HERE.parents[2] / "src"))
from mtdsim.l1_construction.attack_flow_parser import parse_flow_file  # noqa: E402
from mtdsim.l1_construction.schema import TACTIC_ID_TO_NAME  # noqa: E402
ex = parse_flow_file(json_path, flow_id="vt_exemplar", source="hand_curated",
                     tactic_id_to_name=TACTIC_ID_TO_NAME)
na = sum(1 for n in ex.nodes if n.kind == "action")
nc = sum(1 for n in ex.nodes if n.kind == "condition")
no = sum(1 for n in ex.nodes if n.kind == "operator")
assert (na, nc, no) == (10, 2, 1), (na, nc, no)
assert len(ex.edges) == len(EDGES)
print(f"STIX subset: actions={na} conditions={nc} operators={no} edges={len(ex.edges)} — parser OK")

# .afb internal consistency: every referenced instance exists; latch back-refs hold.
insts = {o["instance"] for o in afb_objects}
missing = []
for o in afb_objects:
    if o["id"] == "dynamic_line":
        for r in [o["source"], o["target"], *o["handles"]]:
            if r not in insts:
                missing.append(r)
    if "anchors" in o:
        for aid in o["anchors"].values():
            if aid not in insts:
                missing.append(aid)
assert not missing, f".afb dangling refs: {missing[:5]}"
# every latch referenced by a line is held by exactly one anchor.
held = {L for o in afb_objects if o["id"] in ("horizontal_anchor", "vertical_anchor") for L in o["latches"]}
line_latches = {r for o in afb_objects if o["id"] == "dynamic_line" for r in (o["source"], o["target"])}
assert line_latches <= held, f"latches not anchored: {line_latches - held}"
assert set(layout) >= (insts - {a for o in afb_objects if o['id'] in ('horizontal_anchor','vertical_anchor','generic_handle','dynamic_line') for a in [o['instance']]}), "layout missing a node/latch"
print(f".afb: objects={len(afb_objects)} lines={len(EDGES)} latches={len(line_latches)} — internally consistent")
print(f"wrote {json_path.name} and {afb_path.name}")
