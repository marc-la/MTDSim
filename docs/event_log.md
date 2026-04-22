# Simulation event log

Shared data contract between the simulator and the replay visualiser.

## Schema

Each event is a flat JSON dict:

```json
{
  "schema_version": "1.0",
  "t": 123.4,
  "type": "phase_started",
  "host_id": 5,
  "phase": "EXPLOIT_VULN",
  "technique_id": "T1486",
  "tactic": null,
  "meta": {}
}
```

| Field            | Type                  | Description                                                     |
|------------------|-----------------------|-----------------------------------------------------------------|
| `schema_version` | str                   | Event-log schema version. Loaders fail fast on unknown values.  |
| `t`              | float                 | Simulation time in seconds (`env.now + proceed_time`).          |
| `type`           | str                   | One of the event types below.                                   |
| `host_id`        | int \| null           | Target / compromised host id (nullable for global events).      |
| `phase`          | str \| null           | MTDSim phase (`SCAN_HOST`, `ENUM_HOST`, …).                     |
| `technique_id`   | str \| null           | MITRE ATT&CK technique id when sampled from a subgraph profile. |
| `tactic`         | str \| null           | ATT&CK tactic; reserved for future use.                         |
| `meta`           | dict                  | Free-form payload per event type.                               |

The authoritative schema is [docs/schemas/event_log.schema.json](schemas/event_log.schema.json).

## Event types

| Type                 | Emitted where                                        | Key `meta` fields                            |
|----------------------|------------------------------------------------------|----------------------------------------------|
| `sim_started`        | Notebook wrapper before `env.run`                    | `profile`, `selector_tag`, `scheme`, `seed`  |
| `sim_ended`          | Notebook wrapper after `env.run`                     | `compromise_ratio`, `duration`               |
| `phase_started`      | `AttackOperation._scan_host` etc., after dispatch    | —                                            |
| `phase_completed`    | `AttackOperation._execute_attack_action` bottom, and `_execute_exploit_vuln` per-vuln; also `_handle_interrupt` | `interrupted: bool`, optional `vuln_id`      |
| `host_compromised`   | `AttackOperation.update_compromise_progress`         | `cumulative_compromised`                     |
| `mtd_deployed`       | `MTDOperation._mtd_execute_action` / `MTDAIOperation`| `mtd_name`, `resource_type`                  |
| `mtd_completed`      | Same methods, after execution timeout                | `mtd_name`, `resource_type`, `duration`      |
| `attack_interrupted` | `AttackOperation._handle_interrupt`                  | `interrupted_by` (MTD name)                  |

## Persistence

Events are held in memory on the `EventLogger` and written out via:

- `EventLogger.to_jsonl(path)` — newline-delimited JSON (preferred for the replay viewer and incremental reads).
- `EventLogger.to_json(path)` — single JSON array (convenient for ad-hoc inspection).

Notebook runs save to `notebooks/gap_out/events/{tag}_{seed}.jsonl`. The `gap_out/` directory is gitignored.
