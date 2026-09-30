#!/bin/bash
# The reported corpora, §5.2 then §5.3 (1 000 seeds, the vulnerability memory
# on; run_corpus.py REPORTED=1). Re-running this script resumes the defended
# corpus from what runs_reported.jsonl already holds; the unopposed corpus
# (about 8 minutes) is re-run only if its log does not say it finished.
cd "$(dirname "$0")/../../.." || exit 1
export PYTHONPATH=src TF_CPP_MIN_LOG_LEVEL=3
U=data/results/ch5_s531_unopposed
D=data/results/ch5_defended
if ! grep -q "^unopposed exit 0" "$U/run_reported.log" 2>/dev/null; then
  {
    echo "commit $(git rev-parse HEAD) ($(git branch --show-current)), started $(date -Is)"
    REPORTED=1 WORKERS=7 python "$U/run_corpus.py"
    echo "unopposed exit $? $(date -Is)"
  } > "$U/run_reported.log" 2>&1
fi
{
  echo "commit $(git rev-parse HEAD) ($(git branch --show-current)), started $(date -Is)"
  REPORTED=1 WORKERS=7 python "$D/run_corpus.py" 2> >(grep --line-buffered -v -E "^(WARNING: All log|I0000|E0000|W0000|To enable)" >&2)
  echo "defended exit $? $(date -Is)"
} >> "$D/run_reported.log" 2>&1
