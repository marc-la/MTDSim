#!/usr/bin/env bash
# The five redrawn partitions (redraw_partition_control.py, 2026-10-07) at 1 000 seeds, into
# their own stream; the original rows of these partitions stay in runs_partition_control.jsonl
# and partition_control.py drops them. Resumable. Launch detached:
#   setsid nohup data/results/ch5_defended/run_partition_control_redraw.sh >/dev/null 2>&1 &
# Stop: kill -- -"$(cat data/results/ch5_defended/run_partition_control_redraw.pgid)"
cd "$(dirname "$0")/../../.." || exit 1
export PYTHONPATH=src TF_CPP_MIN_LOG_LEVEL=3
D=data/results/ch5_defended
echo $$ > "$D/run_partition_control_redraw.pgid"
F='^(WARNING: All log|I0000|E0000|W0000|To enable)'
{
  echo "commit $(git rev-parse HEAD) ($(git branch --show-current)), started $(date -Is)"
  SEEDS=1000 PARTITIONS=0,1,3,7,9 OUT="$D/runs_partition_control_redraw.jsonl" WORKERS="${WORKERS:-7}" \
    nice python "$D/run_partition_control.py" 2> >(grep --line-buffered -v -E "$F" >&2)
  echo "seeds 1000 exit $? $(date -Is)"
} >> "$D/run_partition_control_redraw.log" 2>&1
