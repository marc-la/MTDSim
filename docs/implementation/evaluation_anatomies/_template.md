# <bibkey> — evaluation-section anatomy

Source read: <path(s)>. Locators are page numbers (PDF) or line numbers (md) — every claim below carries one.
Paper's own research question / purpose (one sentence, so its conventions are read against its purpose, not ours):

## A. Skeleton of the evaluation portion
Verbatim headings (section numbers + titles) from the first setup/experiment heading through the discussion/limitations, each with page/line. Note which are setup vs results vs discussion, and whether setup and results are one section or two.

## B. Setup — what is declared before any result
- Network configuration(s): size, topology, how many configurations, how chosen.
- Attacker model / scenarios: how many, how named, how defined (bold-defined once?).
- Defence conditions: mechanisms, strategies/schedulers, parameters, a "no defence" baseline (yes/no).
- Parameter table: yes/no; what is in it (columns); distributions declared?
- Replications: runs / seeds / episodes per cell; horizon; termination rule; how stated.
- Statistics: mean / std / CI / min-max / significance tests; what is reported and how.
- Anything else declared (hardware, implementation, versions).

## C. Results — how the numbers are shown
- Order of results (what comes first, and why it seems to).
- Every figure in the evaluation portion: number, chart type, x, y, series, facets, caption gist.
- Every table: number, rows × columns, what it compares.
- How the baseline/no-defence condition appears in each.
- How comparisons are stated in prose: magnitude ("reduced by 40%"), ordering ("A outperforms B"), recommendation ("A is the best choice when …").

## D. Narrative — the claims, in order
The sequence of claims the results section makes from the data (quote or close paraphrase + locator). Separately: does the paper make any claim about the ATTACKER's properties from the data (as opposed to the defence's)? If so, how.

## E. Sensitivity / parameter analysis
Present? Which parameters, over what ranges, one-at-a-time or grid/factorial, how the ranges were justified, how reported (figure/table), where it sits (own section / inside results / appendix), and what claim it is used to support.

## F. Discussion / limitations
Is discussion a separate section or folded into results? What it contains (interpretation, threats to validity, attacker-realism concessions, comparability caveats). Verbatim limitation sentences worth quoting, with locator.

## G. Transferable vs purpose-specific
Two short lists: conventions that transfer to an honours dissertation evaluating existing MTD mechanisms against a new attacker model on a simulator; conventions that are artefacts of this paper's own purpose/venue.
