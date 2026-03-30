"""
Generate AttackerProfiles from MITRE ATT&CK Campaign data.

Uses mitreattack-python to parse the Enterprise ATT&CK STIX bundle,
extract campaigns and their techniques, and derive simulation parameters.

Tactic-to-Phase Mapping
-----------------------
The 14 ATT&CK tactics are collapsed into MTDSim's 6 attack phases based on
functional equivalence in the cyber kill chain:

    SCAN_HOST      <- Reconnaissance, Discovery
    ENUM_HOST      <- Resource Development, Collection
    SCAN_PORT      <- Initial Access, Execution
    EXPLOIT_VULN   <- Privilege Escalation, Defense Evasion, Persistence
    BRUTE_FORCE    <- Credential Access
    SCAN_NEIGHBOR  <- Lateral Movement, Command and Control, Exfiltration, Impact

Parameter Derivation
--------------------
From the normalised capability profile C[phase] in [0, 1]:

    duration_multiplier[phase] = 1.0 - ALPHA * C[phase]       (ALPHA = 0.5, max 50% speedup)
    exploit_success_bonus      = MAX_EXPLOIT_BONUS * C[EXPLOIT_VULN]   (max 0.15)
    brute_force_multiplier     = 1.0 + BF_FACTOR * C[BRUTE_FORCE]     (BF_FACTOR = 2.0, max 3x)
    attack_threshold           = int(BASE_THRESHOLD * (1.0 + PERSIST_FACTOR * C[SCAN_NEIGHBOR]))
"""

import os
import yaml
from typing import List, Dict, Optional
from mtdsim.data.constants import ATTACK_DURATION, ATTACKER_THRESHOLD
from mtdsim.attacker.attacker_profile import AttackerProfile


# --- Mapping from ATT&CK tactics to MTDSim phases ---

TACTIC_TO_PHASE = {
    'reconnaissance': 'SCAN_HOST',
    'discovery': 'SCAN_HOST',
    'resource-development': 'ENUM_HOST',
    'collection': 'ENUM_HOST',
    'initial-access': 'SCAN_PORT',
    'execution': 'SCAN_PORT',
    'privilege-escalation': 'EXPLOIT_VULN',
    'defense-evasion': 'EXPLOIT_VULN',
    'persistence': 'EXPLOIT_VULN',
    'credential-access': 'BRUTE_FORCE',
    'lateral-movement': 'SCAN_NEIGHBOR',
    'command-and-control': 'SCAN_NEIGHBOR',
    'exfiltration': 'SCAN_NEIGHBOR',
    'impact': 'SCAN_NEIGHBOR',
}

PHASES = ['SCAN_HOST', 'ENUM_HOST', 'SCAN_PORT', 'EXPLOIT_VULN', 'BRUTE_FORCE', 'SCAN_NEIGHBOR']

# --- Tuning constants ---
ALPHA = 0.5              # Max duration speedup factor
MAX_EXPLOIT_BONUS = 0.15 # Max additive exploit probability bonus
BF_FACTOR = 2.0          # Brute-force multiplier scaling
PERSIST_FACTOR = 0.5     # Attack threshold scaling
BASE_THRESHOLD = ATTACKER_THRESHOLD


def extract_campaigns(mitre_data) -> List[dict]:
    """
    Extract all campaigns and their techniques from MitreAttackData.

    Parameters
    ----------
    mitre_data : mitreattack.stix20.MitreAttackData
        Loaded MITRE ATT&CK data object.

    Returns
    -------
    list of dict
        Each dict contains campaign metadata and a list of techniques with tactics.
    """
    campaigns = mitre_data.get_campaigns()
    result = []

    for campaign in campaigns:
        campaign_id = campaign.get('external_references', [{}])[0].get('external_id', 'unknown')
        campaign_name = campaign.get('name', 'unknown')
        description = campaign.get('description', '')
        # Truncate description for YAML readability
        if len(description) > 300:
            description = description[:297] + '...'

        techniques_used = mitre_data.get_techniques_used_by_campaign(campaign['id'])
        technique_list = []
        for rel in techniques_used:
            tech = rel.get('object', None)
            if tech is None:
                continue
            tech_id = tech.get('external_references', [{}])[0].get('external_id', '')
            tech_name = tech.get('name', '')
            tactics = []
            for phase in tech.get('kill_chain_phases', []):
                if phase.get('kill_chain_name') == 'mitre-attack':
                    tactics.append(phase.get('phase_name', ''))
            technique_list.append({
                'id': tech_id,
                'name': tech_name,
                'tactics': tactics,
            })

        result.append({
            'campaign_id': campaign_id,
            'campaign_name': campaign_name,
            'description': description,
            'techniques': technique_list,
        })

    return result


def compute_capability_profile(techniques: List[dict]) -> Dict[str, float]:
    """
    Compute a normalised capability profile from a campaign's technique list.

    Counts how many techniques contribute to each MTDSim phase, then normalises
    by dividing by the maximum count across all phases (so the strongest phase = 1.0).

    Parameters
    ----------
    techniques : list of dict
        Each with 'tactics' key listing ATT&CK tactic names.

    Returns
    -------
    dict
        Phase name -> float in [0, 1].
    """
    phase_counts = {phase: 0 for phase in PHASES}
    for tech in techniques:
        for tactic in tech.get('tactics', []):
            phase = TACTIC_TO_PHASE.get(tactic)
            if phase:
                phase_counts[phase] += 1

    max_count = max(phase_counts.values()) if phase_counts.values() else 1
    if max_count == 0:
        max_count = 1

    return {phase: round(count / max_count, 4) for phase, count in phase_counts.items()}


def derive_profile_params(capability: Dict[str, float]) -> dict:
    """
    Derive simulation parameters from a capability profile.

    Returns
    -------
    dict with keys: attack_duration_multipliers, exploit_success_bonus,
                    brute_force_multiplier, attack_threshold
    """
    duration_mults = {}
    for phase in ATTACK_DURATION:
        c = capability.get(phase, 0.0)
        duration_mults[phase] = round(1.0 - ALPHA * c, 4)

    return {
        'attack_duration_multipliers': duration_mults,
        'exploit_success_bonus': round(MAX_EXPLOIT_BONUS * capability.get('EXPLOIT_VULN', 0.0), 4),
        'brute_force_multiplier': round(1.0 + BF_FACTOR * capability.get('BRUTE_FORCE', 0.0), 4),
        'attack_threshold': int(BASE_THRESHOLD * (1.0 + PERSIST_FACTOR * capability.get('SCAN_NEIGHBOR', 0.0))),
    }


def build_attacker_profile(campaign_data: dict) -> AttackerProfile:
    """
    Build an AttackerProfile from raw campaign data.
    """
    capability = compute_capability_profile(campaign_data['techniques'])
    params = derive_profile_params(capability)

    return AttackerProfile(
        name=campaign_data['campaign_name'],
        campaign_id=campaign_data['campaign_id'],
        description=campaign_data['description'],
        attack_duration_multipliers=params['attack_duration_multipliers'],
        exploit_success_bonus=params['exploit_success_bonus'],
        brute_force_multiplier=params['brute_force_multiplier'],
        attack_threshold=params['attack_threshold'],
        capability_profile=capability,
        techniques=campaign_data['techniques'],
    )


def generate_all_profiles(
    mitre_data,
    output_dir: Optional[str] = None,
    min_techniques: int = 3,
) -> List[AttackerProfile]:
    """
    Generate AttackerProfiles for all MITRE ATT&CK campaigns.

    Parameters
    ----------
    mitre_data : mitreattack.stix20.MitreAttackData
        Loaded MITRE ATT&CK data object.
    output_dir : str, optional
        If provided, save YAML files here.
    min_techniques : int
        Minimum techniques per campaign to include (default 3).

    Returns
    -------
    list of AttackerProfile
    """
    campaigns = extract_campaigns(mitre_data)
    profiles = []

    for campaign_data in campaigns:
        if len(campaign_data['techniques']) < min_techniques:
            continue
        profile = build_attacker_profile(campaign_data)
        profiles.append(profile)

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            safe_name = campaign_data['campaign_id'].replace('/', '_')
            filepath = os.path.join(output_dir, f"{safe_name}_{campaign_data['campaign_name'].replace(' ', '_')}.yaml")
            profile.to_yaml(filepath)

    # Write index file
    if output_dir and profiles:
        index = []
        for p in profiles:
            index.append({
                'campaign_id': p.campaign_id,
                'name': p.name,
                'num_techniques': len(p.techniques),
            })
        index_path = os.path.join(output_dir, '_index.yaml')
        with open(index_path, 'w') as f:
            yaml.dump(index, f, default_flow_style=False, sort_keys=False)

    return profiles
