---
status: open                  # retire in the commit that records the submitted title and abstract
created: 2026-09-21
companions: ../notes/_title_workshop.md (the dissertation title shortlist, premise now stale, §4), ../notes/ch1_introduction/mtd_absent_from_volt_typhoon_response.md (the hook's evidence), 2026-09-20_ch5_s52_s54_results_context.md (the reader and the workload analogy), ../workflows/voice.md
---

# Seminar title and abstract — the design brief the draft starts from

> **Mode note.** Top-down design at Marc's ask (2026-09-21): audience, genre,
> conventions, claim ceiling, structure. **No sentence of the abstract is
> drafted here.** The slots in §6 are Marc's to dictate (the slot method);
> the title shapes in §5 are shapes, and the choice is his.

## 1. The task, read for what it rewards

Title, presenter, supervisor (Dr Jin B. Hong, UWA), abstract of **at most 200
words**, circulated with the seminar programme. The brief asks for three
things in order: **context** (why it matters), **problem or hypothesis**,
**contributions** ("what you did, what results you will show, *to the extent
known at the time of writing*"). It must be self-contained and readable by a
generalist. The unit outcome it is marked against is *problem formulation* and
*the discourse conventions of computer science*.

Two consequences. First, this is **not the dissertation abstract**: the
writing guide aims that one at an expert and ends it on the single headline
outcome; this one is aimed at a generalist and is allowed, in the brief's own
words, to promise results it does not yet state. Second, the mark is on
*formulating a problem*, so the abstract's strongest move is the reformulation
itself (§3), not the size of the result.

## 2. The reader

A fourth-year computer science student scanning a programme of
abstracts, deciding which sessions to sit in. They choose on the title, then
on the first two sentences.

| They hold | They do not hold |
|---|---|
| networks, hosts, ports, IP addresses, credentials | moving target defence (never met it) |
| "hackers", ransomware, state-sponsored attacks from the news | APT as a term of art; ATT&CK; cyber threat intelligence |
| simulation, benchmarks, test sets, that a benchmark is only as good as its workload | attack graphs, Petri nets, discrete-event simulation of defences |
| a rough sense that a test can be too easy | suppression, dwell time, execution scheme, every thesis-internal noun |

**Jargon budget:** two terms, each defined in the clause that introduces it
(*moving target defence*, *advanced persistent threat*). At most one acronym
carried forward (MTD). Everything else in plain words: "published reports of
real intrusions", not CTI; "stages of an intrusion", not tactics; "scripted
attacker", not baseline attacker; **never** movement attacker, L0–L4, Petri
net, substrate, suppression. The simulator may be named once (MTDSim) or not
at all.

**What hooks this reader,** in the order it works: (1) a concrete, dated,
slightly alarming fact; (2) a problem they can restate to a friend; (3) a
twist (the expected answer is not the answer); (4) a promise of something to
*see* in the talk. What does not: a field survey sentence, a list of methods,
a claim that the topic is important.

## 3. The story, and why Marc's first arc should be bent

Marc's sketch: *APT attackers (Volt Typhoon) are accelerating with AI → we
need proactive tools → MTD is a novel solution → in simulation, MTD thwarts
APT attackers.* Three problems, each with a fix:

1. **"Accelerating with AI" is not in the thesis** and cannot be cited from
   it. It is also the opener half the programme will use, and it is the
   voice contract's banned register (*rapidly evolving*). The thesis already
   owns a better hook that nobody else has: Volt Typhoon held access inside
   critical infrastructure for **at least five years** on stolen but valid
   credentials, and the nine-agency advisory (co-sealed by Australia's ASD)
   answers it without naming MTD once. Dated, concrete, local.
2. **MTD is not novel** (the idea is over a decade old) and *novel* is a
   banned tell. MTD's pitch is not newness; it is that it attacks the one
   thing the long-dwell attacker banks: **knowledge that stays true**.
3. **"MTD thwarts APT attackers" is not what the work shows and not what it
   may claim.** The claim ceiling is *behavioural fidelity changes the
   answer*, never *the defence works* or *the attacker model is true*. On the
   current corpus the defences do not move together: some suppress almost
   everything, one does nothing, one is mildly negative. A blanket "MTD
   works" is both unearned and the less interesting story.

**The story the thesis actually has is the better seminar:** the field has
been testing MTD against an opponent that looks nothing like the attacker
MTD is for; this work builds an opponent from reports of real campaigns, runs
both against the same defences, and the answer changes. That is a
reformulation (from *does MTD work?* to *against whom was it tested?*), which
is what the learning outcome marks.

**The bridge for a non-security reader** is the workload analogy from the
results-context handoff §1: a benchmark ranks systems differently under a
different workload, a classifier scores differently on a different test set;
in a security evaluation *the attacker is the workload*. Not ruled for the
thesis; for this audience it is the single most useful sentence available.

## 4. The claim ceiling — what survives three weeks

The seminar is about three weeks after submission and the thousand-seed runs
are not in. **The dissertation title workshop's premise is stale:** the
ranking inversion (ρ = −0.893, ten seeds) did not reproduce and the tex holds
a hard block on stating it. What the 100-seed defended corpus shows instead
(`docs/thesis/tables/tab_5-3-2a_orderings.tex`; provenance, not values):

| Tier | Claim | Exposure |
|---|---|---|
| 1 | What was built and run: an attacker model derived from published reports of real campaigns, run beside the simulator's scripted attacker against the same defences on the same network | None. True by construction |
| 2 | The defences that look best depend on which attacker they are tested against; one attacker's ordering says almost nothing about the other's (rank correlation near zero at both intervals) | Low. Holds at both intervals; a sensitivity claim, not an inversion |
| 3 | The direction: defences that move the network (address and topology shuffling) dominate against the campaign attacker, defences that change the software (port, OS, service diversity) dominate against the scripted one; the contrast flips sign between attackers, intervals well clear of zero at the short interval | Medium. More seeds will narrow it, not flip it; a code change could (it has before) |
| — | Any number; "inverts"; "MTD defeats APTs"; "realistic", "validated"; anything scored *against Volt Typhoon* (it is motivation, not in the corpus) | Do not write |

**Recommendation: the abstract commits to tier 2, and promises tier 3 as what
the talk will show.** The brief licenses exactly this ("to the extent
known"), the promise is itself the hook (the reader has to come to find out
which defences), and nothing in it can be contradicted by the final runs. If
the thousand-seed corpus lands before submission and tier 3 holds, one clause
of direction may be added.

## 5. The title

**What works in this field and this genre.** Security titles run in four
forms: the descriptive noun phrase (the lineage's own: Brown, Zhang); the
name-colon-subtitle; the finding-bearing sentence; the question. In a
programme the title is the filter, so it needs: the noun a scanner
recognises (*moving target defence*), the opponent (*attacker* or *advanced
persistent threat*, spelled out), a tension or outcome, and no undefined
acronym or codename. About twelve to fifteen words is the ceiling. A chair
reads it aloud, so **M(AP)TD is out for the seminar** whatever the
dissertation does; the seminar title need not match the dissertation's.

**Marc's two instincts are both right and they reconcile.** The placeholder
is too vague (the workshop already rejected the purely descriptive form: no
effect, no outcome). Over-qualification is the opposite failure. The form that
is specific *and* caveat-proof is the workshop's paired-opposition candidate,
which claims sensitivity and therefore survived the inversion's death.

Shapes, in order of recommendation (shapes, not wording):

1. **Topic, colon, finding at tier 2.** *Moving target defence against
   advanced persistent threats: [the best defence depends on the attacker it
   is tested against].* Carries both search nouns and the twist.
2. **Finding alone.** *[Which moving target defence wins depends on the
   attacker it is evaluated against].* Punchier; loses "advanced persistent
   threat" from the title, so the abstract's first sentence must supply it.
3. **Descriptive-plus.** *Evaluating moving target defence against attackers
   modelled on real intrusion campaigns.* The placeholder made specific; safe,
   no twist. The fallback if Marc wants nothing finding-bearing.
4. **Question form.** Attested in the genre and good on a programme, but it
   reads as a tease if the abstract does not answer it. Lowest.

Bars on any candidate: no *novel / robust / framework / realistic*; no
"fidelity" comparatives; "evaluating" is fine (it is the RQ's own verb and
what chapter 5 does).

## 6. The abstract — five moves, slots only

About eight sentences. Budgets are guides; the total is the constraint.

| # | Job | Facts available | Ceiling | ~words |
|---|---|---|---|---|
| S1 | The hook: one concrete case of the attacker class | Volt Typhoon; at least five years inside critical infrastructure; valid credentials, no malware; joint advisory co-sealed by ASD (2024) | An instance of the class. Not "the attacker we evaluated" | 30 |
| S2 | Name the class and what it lives on; introduce MTD as the answer to exactly that | APT defined in a clause; what it banks (addresses, credentials, topology) stays true for years; MTD keeps changing them so stolen knowledge goes stale | MTD's *stated mechanism*, not its proven effect | 35 |
| S3 | The problem: who MTD has been tested against | Simulated evaluations use a scripted attacker (scan, exploit, spread, as fast as possible) with no campaign and nothing to lose; the workload analogy | "Commonly", not "always"; do not name or fault specific papers | 35 |
| S4 | What was done | Attacker model built from published reports of real campaigns; different profiles by attacker objective (steal, disrupt, both, hold access); runs inside an existing MTD simulator; both attackers, same network, same nine defence conditions | "Modelled on", never "realistic" or "validated" | 45 |
| S5 | The result at tier 2, and the promise at tier 3 | §4 | Tier 2 stated; tier 3 promised, not stated | 35 |
| S6 | (optional) The implication, the sentence a reader quotes back | An evaluation's recommendation is only as good as the attacker it assumed | One vivid sentence, per the voice contract; cut first if over 200 | 15 |

**Conventions for the genre:** no citations, no numbers, no section-style
signposting, present tense; one paragraph. First person is normal in a
seminar abstract ("I" or "this talk"); Marc's call, held consistently.

**Voice.** Claim-first; paired opposition where the contrast is load-bearing
(the two attackers are one); one vivid sentence at most; Australian English;
no banned tells. The assessor's note on the literature review (the author's
voice flattened) applies with most force here, because this is the shortest
and most-read thing Marc will submit: he dictates the sentences, the session
repairs and checks the ceiling.

## 7. Open decisions (Marc's)

1. Hook: Volt Typhoon's five years (recommended) or the AI-acceleration
   opener (not supportable from the thesis).
2. Result level in the abstract: tier 2 plus a promise (recommended), or
   tier 3 stated outright.
3. Title shape: 1 (recommended), 2, 3 or 4.
4. Whether the workload analogy appears (recommended: yes, one clause in S3).
5. First person or "this talk".

## Validation gate

A title and an abstract of at most 200 words that (a) a reader with the
left-hand column of §2 only can restate in one sentence, tested cold on a
subagent given nothing else; (b) contain no claim above the chosen tier of
§4; (c) define both budgeted terms at first use and carry no other field
term; (d) pass the voice contract's tell check. Then record the submitted
text and retire this file.

## Out of scope

The slides and the talk itself; the dissertation title and abstract (their
workshop's premise needs its own refresh once §5.3.2 is measured at a
thousand seeds, flagged here, not actioned).
