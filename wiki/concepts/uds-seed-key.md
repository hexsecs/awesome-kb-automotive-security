---
title: "UDS seed/key (SecurityAccess)"
summary: "UDS SecurityAccess (0x27) gates privileged diagnostics behind a seed/key exchange; weak seeds, reused secrets and simple algorithms defeat it."
type: concept
created: 2026-10-31
updated: 2026-11-01
related: [python-can-isotp, savvycan, cancat, udsoncan, unlockecu, experimental-security-analysis-of-a-modern-automobile, beneath-the-bonnet-a-breakdown-of-diagnostic-security, ford-ecu-bruteforcer]
sources:
  - url: "https://doi.org/10.29354/diag/192162"
    retrieved: 2026-10-31
  - url: "https://pure-oai.bham.ac.uk/ws/portalfiles/portal/50643148/Beneath_the_Bonnet.pdf"
    retrieved: 2026-10-31
  - url: "https://www.autosec.org/pubs/cars-oakland2010.pdf"
    retrieved: 2026-11-01
---

UDS SecurityAccess — service 0x27 of the Unified Diagnostic Services
protocol (ISO 14229) — is the gate in front of privileged diagnostic
operations: reprogramming, sensitive routines, and protected writes. The
ECU issues a "seed," and the tester must return a "key" computed from it
by a secret algorithm. The mechanism is standardised; its strength is
not, and that gap is the vulnerability.

## Attack model

An attacker who reaches a diagnostic channel — the OBD-II port, a
compromised ECU or telematics path, or leaked workshop tooling — attacks
the *implementation* rather than the protocol. If seeds are short or
predictable, or the algorithm is a simple proprietary transform that has
been extracted from one ECU's firmware, valid keys can be computed at
will and the gate opens for the rest of the session.

Peer-reviewed black-box testing (Pełechaty & Konieczny, *Diagnostyka*
2024) found ECUs issuing 2-byte seeds despite up to 4 bytes being
available, weak seed generation, and — critically — the **same
seed-to-key function reused across ECU types from one manufacturer**, so
extracting it once, from a low-value ECU, unlocks others. Independent
work (Sprung, TU Graz 2023) showed such algorithms can even be
synthesised from observed seed/key pairs. The ESORICS 2018 paper
[Beneath the Bonnet](../beneath-the-bonnet-a-breakdown-of-diagnostic-security.md)
reverse engineered the seed-key ciphers of four manufacturers from ECU
firmware and reached remote code execution over CAN through diagnostics
alone.

## The measured baseline

The weakness is not hypothetical, and its arithmetic is on record.
[Koscher et al. 2010](../experimental-security-analysis-of-a-modern-automobile.md)
— this concept's experimental root — measured the production gate of
its era: **16-bit seeds and 16-bit keys**, one key attempt allowed
every 10 seconds, which prices an online brute-force of one ECU at a
little over **7½ days**, or **~3½ days** with power-cycling on the
bench — and the team recovered the brake module's key exhaustively in
**about 1½ days**. Attempt limiting (below) is prescribed against
exactly this baseline. The same paper found the limiting case of
secret management: a telematics unit whose challenge/response was
**hardcoded and common to all units of the part number** — against
the standard's explicit rule that units sharing a part number shall
not share a security seed — compounded by the unit never checking
the exchange's result at all. A second named constant-seed case is
Miller & Valasek 2013's PAM, whose seed is **always the constant
11 22 33** (the firmware randomises, then overwrites it — leftover
debugging code, per the authors). And the small shared key space is
exploited in the field, not only in papers:
[ford-ecu-bruteforcer](../ford-ecu-bruteforcer.md) unlocks pre-2011
Ford modules purely from a bag of known keys.

## Why the design is vulnerable

ISO 14229 standardises the exchange but leaves the algorithm, seed
length, and secret management to each OEM — historically filled with
security-by-obscurity transforms, fleet-wide shared secrets, and no
attempt limiting. The 2020 revision of ISO 14229-1 added a
certificate-based Authentication service (0x29), an implicit
acknowledgement that seed/key alone is thin. Prevalence data comes from
small black-box samples of selected ECUs, not fleet-wide measurement;
treat "typical weakness" claims as generation-dependent.

## Detection and mitigation

- **Cryptographically sound design:** full-length TRNG seeds; keyed
  algorithms with **per-vehicle, per-ECU unique secrets** provisioned
  into HSMs or secure elements — never one fleet-wide secret or a shared
  algorithm across ECU types.
- **Attempt limiting:** enforced delays and lockout after failed keys;
  security levels scoped minimally; privileged services unavailable in
  normal driving states.
- **Channel defence:** authenticated testers, diagnostic gateways and
  firewalls, and migration to 0x29 certificate authentication where
  supported.
- **Detection:** logging and fleet-side alerting on SecurityAccess
  attempts and unlocks, failed-key counters, and unlocks outside service
  contexts; process cover via ISO/SAE 21434 and UNECE R155.

## Tools in this KB

- [python-can-isotp](../python-can-isotp.md) — the ISO-TP transport SecurityAccess runs over.
- [CanCat](../cancat.md) — UDS module with SecurityAccess support and user-supplied seed→key overrides.
- [SavvyCAN](../savvycan.md) — UDS scanning that finds supported security levels (but, per its docs, is unlikely to actually unlock them).
- [udsoncan](../udsoncan.md) and [UnlockECU](../unlockecu.md) — the Diagnostic Tools section's implementations of this layer.
