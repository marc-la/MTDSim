# ch4_implementation — notes feeding the Implementation chapter

## What this chapter does

The implementation chapter carries the **realisation detail the methodology chapter deliberately excludes**: how the design became running code against the inherited simulator, and the engineering decisions that were forced along the way. Implementation challenges are themselves contribution — turning a defined-but-unbuilt model into something executable is exactly where comparable work stops — so the chapter's job is to make the realisation *reproducible and credible*, not to re-argue the design. Its natural shape follows the pipeline (corpus ingestion → graph construction → profiles → binding → execution), and its honest companion is the record of what was inherited unchanged versus built fresh. (Whole-document guidance: [`../_writing_guide.md`](../_writing_guide.md).)

Placeholder — no notes yet. What lands here: prose-worthy *arguments about how the design was realised* — e.g. why the attacker binding was implemented alongside (not inside) the inherited attacker, what the pipeline's staging buys, engineering tradeoffs an examiner would probe. Rubric-gated like every chapter dir ([`../../workflows/notes_rubric.md`](../../workflows/notes_rubric.md)).

Most implementation detail is **not** notes material: schemas, dispositions, and investigation records belong in [`../../implementation/`](../../implementation/) (see the placement criterion in [`../../workflows/docs_map.md`](../../workflows/docs_map.md)). A note earns a place here only when the *reasoning* about the implementation is itself dissertation prose. Expect this dir to stay thin until the chapter is drafted.
