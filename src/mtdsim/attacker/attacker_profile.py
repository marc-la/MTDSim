import yaml
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from mtdsim.data.constants import ATTACK_DURATION, ATTACKER_THRESHOLD


@dataclass
class AttackerProfile:
    """
    Parameterised attacker profile derived from MITRE ATT&CK campaign data.

    Each profile modifies the baseline attacker behaviour via:
    - attack_duration_multipliers: speed modifiers per attack phase (0.5–1.0, lower = faster)
    - exploit_success_bonus: additive bonus to vulnerability exploit probability (0.0–0.15)
    - brute_force_multiplier: multiplier on brute-force success probability (1.0–3.0)
    - attack_threshold: max attempts per host before giving up (default 10, higher = more persistent)
    """
    name: str
    campaign_id: str
    description: str = ""
    attack_duration_multipliers: Dict[str, float] = field(default_factory=dict)
    exploit_success_bonus: float = 0.0
    brute_force_multiplier: float = 1.0
    attack_threshold: int = ATTACKER_THRESHOLD
    capability_profile: Dict[str, float] = field(default_factory=dict)
    techniques: List[dict] = field(default_factory=list)

    @classmethod
    def default(cls) -> 'AttackerProfile':
        """Returns the baseline profile — all multipliers at 1.0, no bonuses.
        Produces behaviour identical to the original hardcoded constants."""
        return cls(
            name="default",
            campaign_id="default",
            description="Baseline attacker with default parameters",
            attack_duration_multipliers={phase: 1.0 for phase in ATTACK_DURATION},
            exploit_success_bonus=0.0,
            brute_force_multiplier=1.0,
            attack_threshold=ATTACKER_THRESHOLD,
            capability_profile={
                'SCAN_HOST': 0.0, 'ENUM_HOST': 0.0, 'SCAN_PORT': 0.0,
                'EXPLOIT_VULN': 0.0, 'BRUTE_FORCE': 0.0, 'SCAN_NEIGHBOR': 0.0,
            },
            techniques=[],
        )

    @classmethod
    def from_yaml(cls, path: str) -> 'AttackerProfile':
        """Load an attacker profile from a YAML file."""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(
            name=data.get('campaign_name', 'unknown'),
            campaign_id=data.get('campaign_id', 'unknown'),
            description=data.get('description', ''),
            attack_duration_multipliers=data.get('attack_duration_multipliers', {}),
            exploit_success_bonus=data.get('exploit_success_bonus', 0.0),
            brute_force_multiplier=data.get('brute_force_multiplier', 1.0),
            attack_threshold=data.get('attack_threshold', ATTACKER_THRESHOLD),
            capability_profile=data.get('capability_profile', {}),
            techniques=data.get('techniques', []),
        )

    def get_attack_duration(self, phase: str) -> float:
        """Return the modified attack duration for a given phase."""
        base = ATTACK_DURATION[phase]
        multiplier = self.attack_duration_multipliers.get(phase, 1.0)
        return base * multiplier

    def to_yaml(self, path: str):
        """Save this profile to a YAML file."""
        data = {
            'campaign_id': self.campaign_id,
            'campaign_name': self.name,
            'description': self.description,
            'techniques': self.techniques,
            'capability_profile': self.capability_profile,
            'attack_duration_multipliers': self.attack_duration_multipliers,
            'exploit_success_bonus': round(self.exploit_success_bonus, 4),
            'brute_force_multiplier': round(self.brute_force_multiplier, 4),
            'attack_threshold': self.attack_threshold,
        }
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
