# GAP enrichment datasets

Vendored snapshots used to attach motivation, region, and alias metadata to
MITRE intrusion-sets. All joins are keyed on the MITRE external group ID
(e.g. `G0007`) or a case-insensitive name/alias match.

## Files

### `misp_threat_actor.json`

- **Source**: https://github.com/MISP/misp-galaxy (CC0-licensed)
- **Upstream URL**: https://raw.githubusercontent.com/MISP/misp-galaxy/main/clusters/threat-actor.json
- **Retrieved**: 2026-04-15
- **Fields consumed**: `value` (primary name), `meta.synonyms`, `meta.country`,
  `meta.cfr-type-of-incident`, `meta.refs` (parsed for `attack.mitre.org/groups/G####/`
  to resolve MITRE IDs).

To refresh:

```bash
curl -fsSL -o src/mtdsim/attacker/gap/enrichment/data/misp_threat_actor.json \
    https://raw.githubusercontent.com/MISP/misp-galaxy/main/clusters/threat-actor.json
```

### `etda_threat_groups.json` (optional)

Not currently vendored — ETDA Threat Group Cards (https://apt.etda.or.th/) are
served as HTML and require scraping. Drop a JSON snapshot here with the shape
`{"groups": [{"mitre_id": "G####", "motivation": "<ETDA 4-cat>", ...}, ...]}`
and it will be picked up automatically.

### `overrides.yaml`

Hand-curated MITRE group → motivation mapping using the ETDA 4-category
taxonomy. Takes precedence over MISP-derived values. Edit freely during
research; commit changes so reviewers can audit attribution calls.

Taxonomy (ETDA):
- `information_theft_espionage`
- `financial_gain`
- `financial_crime`
- `sabotage_destruction`
