---
title: "Securing Vehicular Ad Hoc Networks"
summary: "Raya and Hubaux, Journal of Computer Security 2007. Threat analysis and security architecture for VANETs that set the direction for most later V2X security…"
type: entity
category: "Research Papers"
url: "https://infoscience.epfl.ch/entities/publication/2976e5d8-215b-4465-834e-875efe55844f"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Raya and Hubaux, Journal of Computer Security 2007. Threat analysis and security architecture for VANETs that set the direction for most later V2X security work."
sources:
  - url: "https://doi.org/10.3233/JCS-2007-15103"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - secure-vehicular-communication-systems-design-and-architecture
  - v2x-credential-management
  - misbehavior-detection
  - pseudonym-schemes-in-vehicular-networks-a-survey
---

Raya and Hubaux, Journal of Computer Security 2007. Threat analysis and security architecture for VANETs that set the direction for most later V2X security work.

## What it is

Maxim Raya and Jean-Pierre Hubaux, Laboratory for Computer Communications and Applications (LCA), EPFL. *Journal of Computer Security* 15(1):39–68, 2007. DOI: [10.3233/JCS-2007-15103](https://doi.org/10.3233/JCS-2007-15103) (verified via Crossref). The journal paper extends the authors' ACM SASN 2005 paper of the same programme. Verification note: the JCS full text is paywalled, so the mechanism detail below rests on the openly available SASN 2005 full text (the paper's own conference version, read in full) plus the JCS abstract and record; any elaboration unique to the journal extension is unverified here.

## What it showed

**Attacker model in three dimensions** — insider vs. outsider, malicious vs. rational, active vs. passive — and a five-class attack taxonomy: (1) *bogus information* (colluding insiders diffuse false data to manipulate other drivers, e.g. clearing a road for themselves); (2) *cheating with positioning information* (falsified position or speed to escape liability after an accident); (3) *ID disclosure* (the "Big Brother" tracking scenario, by a global passive observer); (4) *denial of service* (jamming, dummy-message injection); (5) *masquerade*. The requirements set follows: authentication, verification of data consistency, availability, non-repudiation (with event data recording for liability-related messages), privacy, and real-time constraints.

**The architecture** is a PKI with per-message digital signatures and **no confidentiality for safety messages** — authentication, not encryption, is what standalone broadcast messages need; session establishment and group keys are explicitly rejected because they would destroy non-repudiation. Keys and signing live in a **tamper-proof device** per vehicle, with its own battery and secure clock, renewed at the periodic vehicle checkup.

**Two-tier identity:** a long-term **Electronic License Plate (ELP)** issued by a government authority (alternatively an Electronic Chassis Number from the manufacturer), plus sets of **anonymous key pairs** — CA-certified pseudonym keys carrying no publicly discoverable link to the ELP. Certification authorities can be governmental transportation authorities or vehicle manufacturers; the paper weighs both.

**Conditional anonymity:** anonymity holds against observers but is revocable for liability and law enforcement — and the disclosure capability is itself distributed among multiple authorities (police need a judge's permission; secret sharing is proposed to enforce this technically), so no single authority can unilaterally de-anonymize. **Revocation comes two ways:** signed revocation messages to the tamper-proof device when all of a vehicle's material is compromised, and for individual keys **revocation by expiration** — short certificate lifetimes (around one day) instead of CRL distribution, at the cost of large key sets.

**Quantified privacy:** a speed-adaptive key-changing algorithm. An observer can correlate keys over a vulnerability window, which bounds the key-change interval; the worked example at 100 km/h changes keys roughly every 55 seconds — about 184 messages per key, ≈43,800 keys per year, ≈21 MB of key material (derivation of the whole set from a master key shared with the authority is proposed to cut storage). The paper is explicit that tracking of a single isolated target is trivial despite any anonymity measures; correlation resistance needs at least two neighbouring vehicles under observation.

**Bogus information is answered data-centrically:** *verification by correlation* — rate the correctness of the data, not the reputation of the source, because neighbourhoods change too fast for source reputation to form. DoS is mitigated by switching channels or communication technologies, with graceful shutoff of VANET features as the fallback. The performance case for public-key cryptography compares RSA, ECDSA and NTRUSign (ECDSA signature 28 bytes vs RSA 256) under two worst-case highway scenarios with per-message processing budgets of 2.5 ms and 2.78 ms, both assessed achievable, backed by ns-2 simulations — the paper's conclusion that public-key cryptography is fit for vehicular networks, and its claim to the first systematic, quantified treatment of vehicular network security.

## Where it fits

The V2X counterpart to [Wolf 2004](security-in-automotive-bus-systems.md) in this batch: where Wolf secured the in-vehicle buses, Raya and Hubaux defined the security problem for vehicle-to-everything communication before any of it was deployed. The ELP-plus-anonymous-keys model is the direct ancestor of the enrolment-credential / Authorization Ticket split the KB's [V2X credential management](concepts/v2x-credential-management.md) concept page documents in the ETSI CCMS and US SCMS, and its bogus-information class plus verification-by-correlation is the first statement of the problem the [misbehavior detection](concepts/misbehavior-detection.md) concept page treats. The [SeVeCom paper](secure-vehicular-communication-systems-design-and-architecture.md) is its direct continuation by an overlapping author set.

## Limits and safety notes

A design and analysis paper: the architecture was not implemented or deployed by the paper, and the efficiency case rests on era hardware figures (Pentium II 400 MHz benchmarks) and simulation, not a running system. Limits the paper itself states: availability "can never be totally guaranteed" (outsiders retain jamming); anonymity degrades under key correlation and fails for an isolated target; anonymity revocation depends on authorities cooperating as designed; secure positioning is left as an open problem (GPS spoofing and jamming acknowledged, no vehicular solution available). The tracking model deliberately excludes cameras, physical pursuit, and radio fingerprinting — real-world tracking is easier than the model suggests.

## Status and sources

Status: **unknown** — a finished 2007 publication. Sources: the journal record (EPFL Infoscience) and DOI, verified 2026-11-01; the SASN 2005 open full text, read in full 2026-11-01; the list.

## Related

- [Secure Vehicular Communication Systems: Design and Architecture](secure-vehicular-communication-systems-design-and-architecture.md)
- [V2X credential management](concepts/v2x-credential-management.md)
- [Misbehavior detection in V2X](concepts/misbehavior-detection.md)
