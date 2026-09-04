# The research question and the document — from "is the idea right?" to capture / model / evaluate

**Span:** 2026-07-09 → 2026-08-12. **Prompts:** #8, #12, #26, #82, #85–#87,
#91, #93, #100–#103, #106. Heavily recorded — the supervisor decision register
(V-series), [`../../../notes/_writing_guide.md`](../../../notes/_writing_guide.md),
`dissertation.tex` — so this thread keeps only the evolution and its inflection
points.

**July: the framing found its values before its words.** #8 set the reader
contract (write for a general CS-honours reader, decouple from internal
machinery) that became the notes rubric; #12 built the two-consumer docs system
around the dissertation's chapters; #16 stated the value criterion that
outlasted every framing draft: "you can make a really strong attack model by
bumping up the success rate … and say 'we made an APT attacker', but that's not
the goal … It's what insights do we get from this research from the results."

**August: the question crystallised in one meeting.** The 11-Aug workshop (#85)
went in with a draft ("how does a CTI-grounded APT attack model affect MTD
mechanism evaluation") and Marc's own proposal that the sub-questions act as the
experiment's *criterion*, parallel to the APT criterion's role for the model.
The meeting (#91/#93, third-party rulings paraphrased in the register) returned
the ratified form: RQ "How does MTD perform against APT attackers?", decomposed
into **capture / model / evaluate** — methodological sub-questions, not
sub-problems, preserving the single-RQ decision. #86 records a posture shift
worth remembering when drafting: transparent about ranking benchmarks, and
"whatever we can justify selling upwards (charitable interpretation of my own
work) should be adopted from now forth" — the counterweight to the record's
otherwise relentless self-deflation.

**The document followed the question.** The background-chapter ruling (the
inherited simulator is *not* methodology — V-series) produced the current
structure: intro / background / lit review / method / results / discussion /
future work / conclusion (#100–#101), the unit ledger ("a subsection is the
base unit … ~250 words … ~60 units", #102), and the anti-vacuity rules (#87:
barebones sections, no vacuous splits; #81's metric-naming standard — "I would
rather a well thought out metric that returns a negative result at first than
an AI-slop import metric"). #103 added the critique protocol for reviewing
Marc's own drafts without flattening his voice. #106 (2026-08-14) remapped the
notes tree onto the ratified chapters and commissioned this record's Stages 1–3.

**Superseded framings, recorded as such:** sub-RQs as testable hypotheses
(#85, replaced by the criterion-shaped sub-questions); the ~44-subsection
methodology coverage map (killed by the unit ledger); "predictability" as the
plurality metric's name (V2 — retired for the MTD-venue collision, reframed as
effective behavioural breadth).

**September: the document's shape followed the literature review (2026-09-04).**
Porting the review into ch3 exposed a duplication the skeleton had carried since
the 11-Aug workshop: ch4 §4.1.1 ("The threat model MTD evaluation omits") was
ch3 §3.3's verdict restated, and §4.1.2 ("A fidelity criterion from the APT
literature") was the criterion ch3 §3.3.2 derives — the port plan's CONFIRM 2 had
already moved the derivation to ch3 and left §4.1.2 as a half-unit adoption stub.
Marc's ruling took it to the end point: §4.1 is cut outright and the research gap
hands off directly ("the literature does not formally define its attacker models;
building one is Chapter 4"); the former §4.2 "The movement attacker" *is* the
chapter, its preamble the chapter preamble and its four L-subsections now §4.1–§4.4;
the former §4.3 "Experimental setup" is its own chapter, structure unchanged
("keep the structure as is for now"). The document is now intro / background /
lit review / **APT attacker model** / **experimental setup** / results /
discussion / future work / conclusion (nine chapters; the notes dirs were
renumbered to match, and a `ch5_experimental_setup/` dir took the three
experimental-design notes). Two things §4.1 owed were re-homed rather than lost:
this project's commitments (proof-of-concept boundary; attacker-only scope) are
two sentences owed to the ch4 preamble, and the scoring discipline (the badge
vocabulary; axes fixed before the model was scored) opens the discussion chapter's
fidelity verdict. Two naming rulings rode with it. The chapter is titled **"APT
attacker model"**: *attacker model* is the own-voice term (Marc rejected *threat
model definition* — "means different things to different people"), *definition*
was dropped as redundant with the chapter's position, and **"movement attacker"
is the model's name and lives in the prose, not in headings** — "a rhetorical
flourish that should live in the content itself" — which supersedes the
2026-08-09 keep-"movement attacker"-in-headings preference. Ledger: methodology
11 → attacker model 6 + experimental setup 3, the cut §4.1's two units back to
the float (now 4). Capture / model / evaluate is untouched; evaluate simply gains
its own methodological chapter. The four-chapter spine matrix in the writing
guide gained a column.
