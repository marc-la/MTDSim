# Apply brief: everything left in the clausing check (Marc approved all, 2026-10-18)

Apply every item below to `docs/thesis/dissertation.tex`, and to generators and generated floats where a caption lives there. Cluster F is already applied, so do not redo it.

## What to apply

1. **`data/clausing_check/clusters/C_colons.md`:** all proposals.
   - C.28 is the merged version (it includes D.7).
   - The §3.3.2 property walk is kept, per the recommended option (a).
   - Citations stay grouped exactly as written, for example `\citep{hongkim2012harm, brown2023}`. Never split a `\citep`.
2. **`clusters/A1_commas_ch1-4.md`** and **`clusters/A2_commas_ch5-app.md`:** all proposals, taking the main *after* and not the Alt.
   - **Exception:** A2.14 (L9845) is already applied as "maps eight of the 15 tactics". Skip it.
3. **`clusters/D_words.md`:** all proposals except D.7 (merged into C.28).
   - **D.3 is changed:** Kim's "stages" becomes **"tasks"**, not "steps", at all three sites. *Step* is now reserved for attack-flow steps.
4. **The calibration ledger:** items 1–18 in `docs/handoffs/2026-10-18_final_register_pass.md`, recommended options. Item 19 is kept as written.
   - **Item 5, D.2:** use the title **"Values of attack actions blocked and time lost"** (cluster F's correction).
   - **Item 8:** also remove the arrow label "deeper into the network" in `tools/ch2_fig22_network_model.html`, *if* the figure can be re-rendered by an existing script. Otherwise skip the label and report it.
   - **Item 13:** edit through the generator `tools/ch2_lineage_configurations_table.py`.
   - **Skip any item cluster F already changed:** check with `git diff HEAD`.

## Rules

- **Line numbers have drifted.** Locate each passage by its text.
- **Keep all LaTeX as written:** maths (`$c_1$`), `\citep`, `\ref`, `~`, `\,` and `\emph`. The cluster files show the plain text.
- **Edits are exact word changes only.** Add nothing beyond the item.
- **If items overlap on one sentence,** apply both when they are compatible. Otherwise apply the later cluster's and report the conflict.
- **Write files safely:** read, use exact-match replacements, assert each is unique, write a temp file, then `os.replace`.
- **Generated floats:** change the generator, then re-run it. If a generator fails, hand-edit the generated `.tex` and report it.
- **Rebuild:** `pdflatex`, then `bibtex`, then `pdflatex` twice in `docs/thesis`. The log must have 0 lines starting with `!`, no new undefined references, and no new overfull prose lines.
- **Do not commit.**

## Report (at most 10 lines)

- Counts applied per cluster.
- Every item not applied exactly, with the reason.
- Generators re-run, or generated files hand-edited.
- The build result: pages and errors.
- **Also:** after calibration item 4, update the F.19 and F.20 short captions to the new Appendix C titles (cluster F left them pending).
