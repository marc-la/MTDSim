#!/usr/bin/env bash
# The ratio-fix pipeline (handoff §14): re-run and splice, then every analyser
# that reads the two reported ledgers. Niced, 3 workers, so the machine stays usable.
cd "$(dirname "$0")/../../.." || exit 1
export PYTHONPATH=src TF_CPP_MIN_LOG_LEVEL=3 CORPUS=reported
F="grep --line-buffered -v -E ^(WARNING:|I0000|E0000|W0000|To.enable)"
LOG=data/results/ratio_fix/ratio_fix.log
{
  echo "commit $(git rev-parse HEAD), started $(date -Is)"
  WORKERS=3 nice -n 19 python data/results/ratio_fix/rerun_ratio_fix.py 2> >($F >&2) || { echo "rerun FAILED $(date -Is)"; exit 1; }
  for s in data/results/ch5_s531_unopposed/analyse.py data/results/ch5_defended/analyse.py \
           data/results/ch5_defended/time_lost.py data/results/ch5_defended/time_lost_first_deployment.py; do
    echo "$s start $(date -Is)"
    nice -n 19 python "$s" 2> >($F >&2)
    echo "$s exit $? $(date -Is)"
  done
  echo "pipeline done $(date -Is)"
} >> "$LOG" 2>&1
