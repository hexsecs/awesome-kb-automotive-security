---
uid: 01a19d3c-afc0-7892-92c3-285d32826893
title: "Pseudonym Schemes in Vehicular Networks: A Survey"
summary: "Petit, Schaub, Feiri, and Kargl, IEEE Communications Surveys and Tutorials 2015. Defines the pseudonym lifecycle and categorises the schemes that reconcile…"
type: entity
category: "Research Papers"
url: "https://oparu.uni-ulm.de/items/b215d57b-06e1-4f27-a67e-a6ecaf3b45d2"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Petit, Schaub, Feiri, and Kargl, IEEE Communications Surveys and Tutorials 2015. Defines the pseudonym lifecycle and categorises the schemes that reconcile V2X message authentication with driver privacy."
related: [securing-vehicular-ad-hoc-networks, secure-vehicular-communication-systems-design-and-architecture, v2x-credential-management, misbehavior-detection]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://doi.org/10.1109/COMST.2014.2345420"
    retrieved: 2026-11-01
  - url: "https://ris.utwente.nl/ws/files/5314057/Petit_Pseudonym_schemes.pdf"
    retrieved: 2026-11-01
---

Petit, Schaub, Feiri, and Kargl, IEEE Communications Surveys and Tutorials 2015. Defines the pseudonym lifecycle and categorises the schemes that reconcile V2X message authentication with driver privacy.

## What it is

Jonathan Petit, Michael Feiri and Frank Kargl (University of Twente; Kargl also University of Ulm) and Florian Schaub (University of Ulm; then Carnegie Mellon University). *IEEE Communications Surveys & Tutorials* 17(1):228–255, First Quarter 2015. DOI: [10.1109/COMST.2014.2345420](https://doi.org/10.1109/COMST.2014.2345420) (verified via Crossref; also printed on the authors' manuscript). The full text was read from the authors' accepted manuscript (University of Twente repository copy). The problem it surveys: cooperative vehicles broadcast beacons (CAM in Europe, BSM in the US) at 1–10 Hz carrying position, speed and heading; safety requires those messages to be authenticated, but an authenticated broadcast is a tracking feed — the survey treats beacon content as personal data outright. The field's answer is pseudonymity, and the survey's contribution is to give that answer a common skeleton — an **abstract pseudonym lifecycle** — and a four-way categorization of every scheme proposed against it.

## What it showed

**Definitions and adversary model.** A digital pseudonym (after Chaum; Pfitzmann & Hansen) is a unique identifier usable for authentication that carries no personally identifying information; actions under one pseudonym are linkable to each other, unlinkability comes from *changing* pseudonyms. Anonymity in deployed systems can only be **conditional**: a privileged authority must be able to resolve a pseudonym to an identity under stated conditions (misbehaviour, law enforcement), which separates pseudonymity from anonymity proper. The adversary model is adopted explicitly from Raya & Hubaux: global vs. local, active vs. passive, internal vs. external — with the **global passive adversary** as the design case for tracking, and a local passive adversary as the realistic one. Attacks catalogued: location tracking, context linking, and — for active adversaries — the **pseudonym depletion attack** (force changes until the victim's pool empties).

**Requirements.** Five privacy requirements (after Schaub et al.): minimum disclosure, conditional anonymity, unlinkability, **distributed resolution authority** (no single authority may resolve alone), and perfect forward privacy. Pseudonyms must be time-limited, unique, always available, blockable (safety sometimes requires *preventing* a change), and changed **together with every other identifier on every layer** — a change that leaves the MAC address standing is trivially linkable.

**The lifecycle.** Five phases: **issuance** (a long-term vehicle identity — the VID, "also referred to as an electronic license plate (ELP)" — authenticates the vehicle to an issuing authority, which issues pseudonym credentials and may retain escrow information for later resolution; validity periods and limited parallel pseudonyms are the Sybil bound), **use** (sign outgoing, verify incoming — with the structural asymmetry that a vehicle verifies roughly *n × r* messages per second from *n* neighbours beaconing at *r* Hz while sending only its own), **change** (only effective with an anonymity context — a lone vehicle changing under observation is linkable anyway), **resolution** (optional; escrow lookup, or split-authority/threshold designs), and **revocation** (optional; revoking all of a vehicle's pseudonyms requires them to be linkable somehow, itself a privacy cost — hence the common retreat to revoking the VID and letting pseudonyms expire, "passive revocation").

**Change strategies** (surveyed mainly for PKI schemes): fixed-time periodic (a known period makes tracking trivial), random, silent period, vehicle-centric (Swing/Swap — change on velocity change, or swap pseudonyms with a neighbour), density-based, and collaborative/synchronous change around **mix zones** — with Buttyán et al.'s bound that mix zones between RSUs fail when an attacker monitors more than 50% of intersections. The survey's verdict: "it remains unclear which strategy is the most effective in practice."

**The four categories.** (1) **Asymmetric/PKI**: the pseudonym is an anonymous public-key certificate; CAs hold long-term identities, separate Pseudonym Providers issue short-term certificates. Privacy-enhanced issuance splits knowledge so no authority can link alone — the CAMP/US design (Registration Authority shuffling requests, CA issuing blind, two Linkage Authorities whose values combine as the certificate's revocation handle), V-tokens, SRAAC. (2) **Identity-based cryptography**: the identifier *is* the public key, so no certificate is attached and overhead drops — but the trusted authority extracts every private key from its master secret, so key escrow is total: a compromised authority "could impersonate any OBU and also resolve arbitrary pseudonymous messages." (3) **Group signatures**: signers are anonymous and unlinkable *within the group*, no routine change needed — but the group manager can open any signature (escrow again), and revoking one member forces re-keying the whole group. (4) **Symmetric cryptography**: (H)MAC authentication is fastest and cheapest, but every verifier holding the key can forge, non-repudiation is unavailable, and in the representative schemes only RSUs can verify — receivers wait for infrastructure confirmation, a delay safety messages cannot afford. The survey's conclusion (§IX): "symmetric schemes have substantial drawbacks and are not practical," group signatures are held back by computation overhead, and **asymmetric and identity-based schemes are "the most viable approaches."** A scale figure anchors the overhead discussion: a worst-case hourly CRL of over 2.2 GB under naive pseudonym-revocation policies, cut to 42 MB by adding a "valid after" field.

**Standardization, as of the survey (§X).** ETSI TS 102 941's split — enrolment authority for long-term identity, authorization authority for short-term pseudonymous certificates — "corresponds to a simple pseudonym scheme with a CA and PP," and at that date the specification "misses important aspects of the pseudonym lifecycle… like pseudonym resolution, protection from misuse by authorities, and even pseudonym change." IEEE 1609.2-2013 contains **no privacy mechanism at all** (§E.9.5, quoted: the working group declined to specify anonymous certificates because requirements were unclear and "revocation and privacy are in conflict"); Japan's ARIB STD-T109 (Dec 2012) does not consider privacy; the CAMP specification is identified as the design expected to shape future US work.

**Open challenges (§XI).** Pseudonym change flushes the whole communication stack and can break applications; there is **no consensus privacy metric**; and privacy mechanisms carry a safety cost — a silent period beginning at a safety-critical moment is a "missed intervention."

## Where it fits

The survey is the research literature underneath the KB's [V2X credential management](concepts/v2x-credential-management.md) concept page — before/after photographs of the same systems. The concept page's ETSI enrolment/authorization split is this survey's "simple pseudonym scheme," documented here in its preliminary state (no resolution, no change strategy, no authority-misuse protection) where the concept page documents the mature TS 102 941 architecture; the concept page's US SCMS is the CAMP design this survey describes in §V-B, linkage values and all, a decade earlier (labelled comparison: the survey's "CA" is the role the SCMS's Pseudonym CA fills). Its adversary model and its ELP are taken directly from Raya & Hubaux, making it the direct continuation of [Securing Vehicular Ad Hoc Networks](securing-vehicular-ad-hoc-networks.md) — same model, same two-tier identity, now with an industry of schemes to organize. And one sentence in its lifecycle explains why the KB needs a second concept page at all: under *use*, the survey notes that "a valid vehicle would still be able to report false data and thus complementary security mechanisms that verify consistency of data are needed" — that complementary layer is what [misbehavior detection](concepts/misbehavior-detection.md) documents (KB-side synthesis, labelled as such).

## Limits and safety notes

A survey, not an experiment: its category verdicts are the authors' analysis of the cited schemes, and its "current state of standardization" is a 2014 snapshot — ETSI and IEEE work has moved substantially since (the concept page records where it landed), so nothing in §X should be quoted as present fact. The full text read for this page is the authors' accepted manuscript, marked "not been fully edited"; wording may differ in small ways from the published version, whose pagination (17(1):228–255) is taken from the OPARU/Crossref records. Its scope is pseudonymous *authentication* for V2X; privacy of other channels is context, not subject.

## Status and sources

Status: **published** — a finished 2015 publication. Sources: the authors' accepted manuscript, University of Twente repository (read in full 2026-11-01 via the Wayback Machine's snapshot; the live file currently 404s); DOI and published pagination verified via Crossref and the Ulm OPARU record, 2026-11-01; the list.

## Related

- [Securing Vehicular Ad Hoc Networks](securing-vehicular-ad-hoc-networks.md) — the adversary model and ELP this survey adopts
- [Secure Vehicular Communication Systems: Design and Architecture](secure-vehicular-communication-systems-design-and-architecture.md) — the PKI category's reference project
- [V2X credential management](concepts/v2x-credential-management.md) — what the survey's ETSI/CAMP schemes became
- [Misbehavior detection in V2X](concepts/misbehavior-detection.md) — the data-consistency layer the survey calls for
