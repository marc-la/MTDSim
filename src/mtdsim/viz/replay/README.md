# Replay visualiser

Dash app that plays back an MTDSim `events.jsonl` across three SA-aligned
panels: network (SA L1), GAP subgraph (SA L2), intermediary execution (SA
L3, lands in step 6). See [`docs/schemas/event_log.schema.json`](../../../../docs/schemas/event_log.schema.json)
for the log contract.

## Running

```
python -m mtdsim.viz.replay \
  --log notebooks/gap_out/events/A_random_42.jsonl \
  --gap-html notebooks/gap_out/gap.html \
  --port 8050
```

Flags:

- `--log PATH` — events.jsonl. Without it the viewer boots empty.
- `--gap-html PATH` — pre-rendered GAP graph. Without it the SA-L2 panel
  shows a placeholder. Generate one with
  `GapRenderer(gap).render_interactive(path)`.
- `--host`, `--port`, `--debug` — standard Flask flags.

Existing logs under `notebooks/gap_out/events/` predate the
`schema_version` field and are rejected by the loader. Regenerate them
after the step-8 simrunner lands (or amend the notebook's `evlog.emit`
chain to add `schema_version="1.0"`).

## Files it reads / writes

- Reads: `--log`, `--gap-html`, cached layouts under `data/viz_cache/`
  (gitignored).
- Writes: `data/viz_cache/layout_{hash}.json` on first render of a given
  topology; subsequent runs read from the cache.

## Cache key

Layouts are keyed on a SHA-1 of `(sorted_nodes, sorted_edges, seed)`.
Bust the cache by deleting the `data/viz_cache/` directory.

## Steps implemented

- [x] Step 1 — schema lock + `schema_version` stamp.
- [x] Step 2 — Dash skeleton.
- [x] Step 3 — loader + playback state machine.
- [x] Step 4 — network state panel.
- [x] Step 4.5 — postMessage spike (throwaway, gitignored).
- [x] Step 5 — GAP iframe + `app.js` postMessage handler.
- [ ] Step 6 — intermediary execution panel + signal flow sub-panel
      (gated on supervisor decision, see plan §14).
- [ ] Steps 7–10 — catalog, run trigger, compare mode, stats sidebar, polish.
