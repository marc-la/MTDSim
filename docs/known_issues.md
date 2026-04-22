# Known issues

Pre-existing bugs that are not blocking but worth fixing when touching the relevant area.

## `Network.gen_graph` infinite loop with tight subnet/layer ratios

**Where**: [src/mtdsim/network/network.py:119-126](../src/mtdsim/network/network.py#L119-L126)

The while loop populating `subnets_per_layer` only appends when
`total_subnets - (sum + l) > layers - len`. After the hardcoded first entry `[1]`,
this guard becomes unsatisfiable when `total_subnets - total_layers` is too small
(e.g. `total_subnets=3, total_layers=2` → `l < 1`, but `l ∈ [1, max_subnets_per_layer]`).
Result: 100% CPU spin with no progress.

**Observed rule of thumb**: need roughly `total_subnets >= total_layers + 3` for the
guard to be reliably satisfiable.

**Workaround**: use known-good proportions (e.g. the 2026-03-27 notebook's
`total_nodes=100, total_subnets=8, total_layers=4`, or the demo notebook's
`total_subnets=6, total_layers=3`).

**Fix idea**: either (a) relax the strict inequality to `>=`, (b) loosen the check to
accept any `l >= 1` when the remaining layer count can still be satisfied, or
(c) derive `subnets_per_layer` deterministically (`total_subnets // total_layers` with
a remainder distribution).

## `TimeNetwork.is_compromised` ignores `terminate_compromise_ratio`

**Where**: [src/mtdsim/network/time_network.py:47-50](../src/mtdsim/network/time_network.py#L47-L50)

```python
def is_compromised(self, compromised_hosts):
    # 80% compromise ratio
    # return len(compromised_hosts) / self.total_nodes > 0.8
    return len(compromised_hosts) / self.total_nodes > 0.25
```

The constructor accepts `terminate_compromise_ratio` but the method hardcodes
`0.25`. Any experiment that specifies a termination ratio is silently overridden,
which may affect headline results (MTTC, compromise-ratio distributions).

**Fix**: store the constructor arg on `self` and use it in `is_compromised`.
