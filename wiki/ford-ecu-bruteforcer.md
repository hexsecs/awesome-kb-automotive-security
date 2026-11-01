---
title: "Ford-ECU-Bruteforcer"
summary: "Security access brute-force tool for pre-2011 Ford ECUs with 3-byte seed and 5-byte key."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/jakka351/Ford-ECU-Bruteforcer"
status: maintenance
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Security access brute-force tool for pre-2011 Ford ECUs with 3-byte seed and 5-byte key."
related: [uds-seed-key, udsoncan, gallia]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/jakka351/Ford-ECU-Bruteforcer"
    retrieved: 2026-10-31
---

Security access brute-force tool for pre-2011 Ford ECUs with 3-byte seed and 5-byte key.

## What it is

A Windows GUI tool (C#, shipped with a prebuilt executable) that
brute-forces UDS SecurityAccess (0x27) on Ford ECUs, by jakka351 /
Tester Present. The README notes a paid, actively developed
"enterprise grade" version covering most Ford, Mazda, and JLR
controllers.

## How it works

Instead of implementing a seed/key algorithm, the tool uses "the keybag
from the Ford Hack" — a set of known keys, augmented with keys
extracted from FORScan via Ghidra — trying keys against the ECU's seed
until one unlocks it. That works because the affected ECUs derive keys
from a small, shared key space, the exact weakness the
[UDS seed/key](concepts/uds-seed-key.md) page describes. Mid-speed or
high-speed CAN and the diagnostic session are selectable; the attempt
aborts on 0x7F negative responses. It was developed against an OBDxPro
FT J2534 interface, and a May 2024 update added 18 V FEPS on OBD pin 13
so PCMs requiring FEPS voltage can hypothetically be unlocked. The
author reports success on an Audio Control Module, Audio Interface
Module, and Instrument Cluster.

## Where it fits

Regaining SecurityAccess to pre-2011 Ford modules (3-byte seed /
5-byte key) whose key sits in the known-key set, when no seed/key
algorithm is available — a concrete, worked example of seed/key failure
in the field, alongside the seed collection in
[Gallia](gallia.md) and the seed-randomness tooling in
[CaringCaribou](caringcaribou.md).

## Limits and notes

The README states it "should work on any Ford ECU that is pre 2011,
assuming it is a 3 Byte Seed and a 5 Byte Key" — that seed/key geometry
is a hard precondition. The open-source version is feature-limited
relative to the enterprise version, and full J2534 support is an
enterprise feature. Licence terms are unverified (GitHub reports
"Other (NOASSERTION)"). Status `maintenance`: the repository is not
archived, but the latest dated README update is 17/10/2024.

## Related

- [UDS seed/key](concepts/uds-seed-key.md) — the weakness this tool operationalises.
- [udsoncan](udsoncan.md) — standards-based SecurityAccess workflows.
- [Gallia](gallia.md) — the research-grade UDS/DoIP framework.
