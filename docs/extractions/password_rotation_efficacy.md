# Password-rotation efficacy — does a reset revoke a captured credential? (extraction notes)

> Two studies that answer the **credential-access §3 reset-verdict question
> directly**: when the defender rotates a password (a credential-level "reset"),
> does it actually revoke an attacker who has *already captured* the old one? Both
> conclude **largely not** — which, with the location-independence of a stolen
> credential, makes credential-access the archetypal **reset-survivor**.
> Extracted for [`09_credential-access`](../tactic_profiles/09_credential-access.md) §3.
> Source files (both `docs/sources/tactic_profiles/step_d/9_cred_access/`,
> gitignored): `1866307.1866328.md`, `s10623-015-0071-9.md`.

### Relevance class

**M** (MTD/reset-mechanism). The §3 reset-verdict evidence for credential-access —
the one tactic where the "does the gain survive a reset" question has a direct
empirical answer.

### Used in lit review

Credential-access §3 (reset verdict: stolen auth material survives both a topology
shuffle and a credential rotation → reset-survivor, narrow-to-moderate sweep).

## Bibliographic anchor

- **Citation keys**: `zhang2010_expiration` (Zhang, Monrose, Reiter, *The
  Security of Modern Password Expiration*, ACM CCS 2010); `chiasson2015`
  (Chiasson, van Oorschot, *Quantifying the Security Advantage of Password
  Expiration Policies*, Designs Codes & Cryptography 77(2–3), 2015).
- **Pages cited from**: Zhang §1 + §"results" (41%/17%/63% figures); Chiasson §5
  (concluding remarks).

## Relevant artefacts

### Zhang, Monrose & Reiter 2010 — rotation revokes a captured password in only a minority of cases

**Source locator:** §1 (high-order results); §"online attack" (Fig. 5/7)

**Paraphrase:** the first large-scale test (**7,700 accounts**) of whether
password expiration achieves its purpose — revoking access to an attacker who has
*captured* a password [fetched]. Using a transform-based search (users modify
their old password in systematic ways), the attacker breaks the *new* password
from the old in:
- **41% of accounts offline** (expected effort < 3 s/account),
- **17% of accounts online** (fewer than 5 guesses; 13% with certainty in 5, 18%
  in 10),
- **63% of accounts** among those with a prior history of using transforms.

Conclusion: the study "calls into question the merit of continuing the practice
of password expiration" — **rotation fails to revoke a captured credential in a
large fraction of cases.**

**Maps to:** [`09_credential-access`](../tactic_profiles/09_credential-access.md)
§3 (a credential-rotation "reset" is *leaky* — a captured credential survives it
17–41% of the time; combined with location-independence (survives an IP/topology
shuffle), credential-access is a strong reset-survivor → **narrow sweep on the
reset**).

**Disposition for this thesis:** verified [fetched] — the direct empirical answer
to the §3 reset question for this tactic. Population = one institution's defunct
accounts; the *shape* (rotation is leaky) transfers, the exact % is context-bound.

---

### Chiasson & van Oorschot 2015 — the security benefit of expiration is "partial and minor"

**Source locator:** §5 (Concluding remarks)

**Paraphrase:** a formal analysis of the defensive advantage of password
expiration [fetched]. Conclusion: "the security benefit of password aging
policies are at best **partial and minor**." Load-bearing for §3: expiration
"provides little help against numerous other attacks, including those which upon
first access immediately … install keystroke-logging software or **other
persistent malware to render ineffective subsequent password changes**" — i.e.
**once a stolen credential is used to establish persistence, rotation is moot**
(the [`05_persistence`](../tactic_profiles/05_persistence.md) "adapt around a
periodic reset" link, from the credential side).

**Maps to:** [`09_credential-access`](../tactic_profiles/09_credential-access.md)
§3 (rotation's benefit is minor; a credential that has bootstrapped persistence is
reset-immune) and [`05_persistence`](../tactic_profiles/05_persistence.md) §3.

**Disposition for this thesis:** verified [fetched] — corroborates Zhang et al.
analytically; reinforces the reset-survivor verdict.

## Open questions / things to verify

- Both concern *password* rotation specifically; the substrate's MTD is
  IP/topology/service SDR, which a stolen credential *also* survives (not
  location-bound). Together they make credential-access the clearest reset-survivor
  — the reset verdict is "survives", with only a modest sweep for the leaky-minority
  case.
- Zhang's exact break-rates are institution-specific; the *direction* (rotation is
  leaky) is the transferable finding.

## Out of scope for this thesis

Zhang's transform-tree search algorithm (Bemts/orderBemts) and password-strength
correlations; Chiasson's cryptographic key-search base analysis. The load-bearing
part is the verdict: rotation does not reliably revoke a captured credential.
