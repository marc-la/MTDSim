#!/usr/bin/env bash
# §5.4's two run ablations to 1 000 seeds with the vulnerability memory and the
# failure matrix on wherever they are not the component removed (Marc 2026-10-02).
# Seed-major and resumable: re-run this script after a kill and it carries on.
#   1. failure matrix: both arms, memory on -> runs_ablation_memory.jsonl (40 000 runs)
#   2. vulnerability memory: off and on arms extended to 1 000 seeds
#      -> runs_memory.jsonl (the every-exploit-succeeds arm stays at 100 seeds)
cd "$(dirname "$0")/../../.." || exit 1
export PYTHONPATH=src TF_CPP_MIN_LOG_LEVEL=3
D=data/results/ch5_defended
echo $$ > "$D/run_ablations_1000.pgid"
F='^(WARNING: All log|I0000|E0000|W0000|To enable)'
{
  echo "commit $(git rev-parse HEAD) ($(git branch --show-current)), started $(date -Is)"
  if ! grep -q "^failure exit 0" "$D/run_ablations_1000.log" 2>/dev/null; then
    ABLATION=1 MEMORY=1 SEEDS=1000 WORKERS=7 python "$D/run_corpus.py" 2> >(grep --line-buffered -v -E "$F" >&2)
    echo "failure exit $? $(date -Is)"
  fi
  RESUME=1 SEEDS=1000 PERFECT_SEEDS=100 WORKERS=7 python "$D/run_memory_ablation.py" 2> >(grep --line-buffered -v -E "$F" >&2)
  echo "memory exit $? $(date -Is)"
} >> "$D/run_ablations_1000.log" 2>&1
