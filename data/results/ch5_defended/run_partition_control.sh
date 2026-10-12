#!/usr/bin/env bash
# The size-matched, label-blind partition control (run_partition_control.py):
# K = 10 random partitions x 4 groups x 5 cells, 100 seeds first, then 1 000.
# Seed-major and resumable: re-run this script after a kill and it carries on.
# Launch in its own process group, detached:
#   setsid nohup data/results/ch5_defended/run_partition_control.sh >/dev/null 2>&1 &
# Stop the whole group:
#   kill -- -"$(cat data/results/ch5_defended/run_partition_control.pgid)"
cd "$(dirname "$0")/../../.." || exit 1
export PYTHONPATH=src TF_CPP_MIN_LOG_LEVEL=3
D=data/results/ch5_defended
echo $$ > "$D/run_partition_control.pgid"
F='^(WARNING: All log|I0000|E0000|W0000|To enable)'
{
  echo "commit $(git rev-parse HEAD) ($(git branch --show-current)), started $(date -Is)"
  if ! grep -q "^seeds 100 exit 0" "$D/run_partition_control.log" 2>/dev/null; then
    SEEDS=100 WORKERS="${WORKERS:-7}" python "$D/run_partition_control.py" 2> >(grep --line-buffered -v -E "$F" >&2)
    echo "seeds 100 exit $? $(date -Is)"
  fi
  SEEDS=1000 WORKERS="${WORKERS:-7}" python "$D/run_partition_control.py" 2> >(grep --line-buffered -v -E "$F" >&2)
  echo "seeds 1000 exit $? $(date -Is)"
} >> "$D/run_partition_control.log" 2>&1
