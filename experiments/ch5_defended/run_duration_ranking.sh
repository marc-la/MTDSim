#!/bin/bash
# Threat 2 (Marc 2026-10-08): the 200 s ranking with the 45 s mean duration at
# both band ends, APT arm only. Resumes from runs_duration_ranking.jsonl.
cd "$(dirname "$0")/../.." || exit 1
export PYTHONPATH=src TF_CPP_MIN_LOG_LEVEL=3
{
  echo "commit $(git rev-parse HEAD) ($(git branch --show-current)), started $(date -Is)"
  WORKERS=7 python experiments/ch5_defended/run_duration_ranking.py 2> >(grep --line-buffered -v -E "^(WARNING|I0000|E0000|W0000|To enable|Please report|Cause:|To silence)" >&2)
  echo "duration-ranking exit $? $(date -Is)"
} >> experiments/ch5_defended/run_duration_ranking.log 2>&1
