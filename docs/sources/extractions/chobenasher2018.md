# Cho & Ben-Asher 2018 — extraction notes

> J.-H. Cho and N. Ben-Asher. "Cyber defense in breadth: Modeling and analysis
> of integrated defense systems." *Journal of Defense Modeling and Simulation:
> Applications, Methodology, Technology*, vol. 15, no. 2, pp. 147–160, 2018.
> doi:10.1177/1548512917699725. (Special issue article; © The Author(s) 2017.)
> Source file: `docs/sources/lit_review/chobenasher2018.md` (gitignored source
> tree; the header/DOI above are transcribed from it verbatim).
> Relevance to this thesis: the SRN/SPN-for-MTD-effectiveness anchor the L3
> feasibility study named "pending extraction" — an **analytical Stochastic
> Petri Net** (SPNP v6, Markov/semi-Markov) of an *integrated defence system*
> (IDS + honeypot deception + MTD platform migration), where MTD's effect is
> modelled as **prolonging the attacker's reconnaissance dwell**. It is cited in
> the dissertation's methodology §4.2.3 as precedent for stochastic-Petri-net
> modelling in the MTD-evaluation space, alongside Cai 2016 and Mendonça 2023.

## Bibliographic anchor

- **Citation key**: `chobenasher2018`
- **DOI**: 10.1177/1548512917699725
- **Pages cited from**: abstract; §1 (contributions, source ll. 108–144); §3.1
  attack model (ll. 442–480); §4.1 SPN description (ll. 557–660); §5.2 setup
  (ll. 805–835); §6 conclusion (ll. 1074–1104).

## Extraction policy

Quote sparingly, paraphrase liberally; locators are line numbers into the
source markdown. Written 2026-08-17 for the §4.2.3 precedent cite — a
*targeted* extraction, not a full dissection.

## What the paper does (paraphrase)

- **Formalism.** "We develop a Stochastic Petri Nets (SPN) model in which the
  underlying mode is Markov or semi-Markov" (§1 contribution 2, l. 120),
  solved with the Duke SPNP package v6 (Trivedi; §4.1, l. 562). Places are
  system states; a transition "refers to a transition rate a system changes
  from one state to another" (l. 573). Analytical, not executed.
- **What is modelled.** The *defence system* — four variants: IDS only,
  IDS+deception (honeypot), IDS+MTD (platform migration), IDS+MTD+HP (§5.1).
  Metrics: attack success probability and attack cost (attacker side); defence
  cost and **mean time to security failure (MTTSF)** (defender side) —
  MTTSF is their derivation of a reliability metric with attacker success as
  the failure condition (ll. 124–130).
- **The attacker.** An abstract attacker with a finite exploit set, perfect
  vulnerability knowledge on access, a deception-detection probability
  `Pad`, learning from failure that *shortens* time to success, and — the
  MTD-relevant clause — a **longer reconnaissance period under MTD**
  ("the attacker has to spend a significantly more time to identify the
  target's new configurations", ll. 464–472). No campaign structure, no
  ATT&CK vocabulary; the attacker is a rate vector.
- **MTD's mechanism in the net.** MTD fires with rate `Pm/Tm` (l. 645) and
  its effect is expressed through the dwell in the RECON place, which both
  delays attack success and gives IDS more time to detect (ll. 647–660).
- **Rate provenance.** Design parameters (Table 2) and transition rates
  (Table 3) are *set* to "reflect a particular system condition"; the authors
  state that varying them changes the time-evolution "to some extent" while
  "the overall behavior across times remain the same" (ll. 820–834). No
  literature sourcing of attacker rates is claimed — the same declare-and-
  argue stance as Bland 2020 and Mendonça 2023.

## What transfers to this thesis, and the trap

- **Transfers:** SPN/SRN as an accepted apparatus for *comparing* MTD
  configurations analytically; MTD-as-dwell-extension (an attacker's
  reconnaissance time is where MTD bites) — consonant with this thesis's
  place-holds-time reading; MTTSF as a first-passage/absorption metric.
- **Trap:** the *defender* is what is modelled, with an abstract attacker;
  IDS is out of scope here (architecture §(a)); the net is solved, not
  executed. Cite for *precedent in the MTD-evaluation space*, not for the
  attacker side, and not as an executed-net precedent (that is Bland 2020).
- The L3 feasibility study's §3 row for this paper (written before
  extraction) is confirmed: SPN, SPNP, analytical, system/defender
  parameters, MTD = longer attacker reconnaissance.
