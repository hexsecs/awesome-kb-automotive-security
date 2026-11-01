---
title: "UnlockECU"
summary: "Free seed-key unlocking tool for Bosch, Continental, Delphi, Daimler, and Marquardt ECUs without proprietary DLLs."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/jglim/UnlockECU"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Free seed-key unlocking tool for Bosch, Continental, Delphi, Daimler, and Marquardt ECUs without proprietary DLLs."
related: [uds-seed-key, udsoncan]
license: "MIT"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/jglim/UnlockECU"
    retrieved: 2026-10-31
---

Free seed-key unlocking tool for Bosch, Continental, Delphi, Daimler, and Marquardt ECUs without proprietary DLLs.

## What it is

A free, open-source ECU seed-key unlocking tool by jglim: a .NET 5 C#
application (`VisualUnlockECU.exe`, plus an in-browser version) with a
portable class library at its core. MIT-licensed. The README stresses
it includes no copyrighted or proprietary files — all security
functions and definitions were reverse-engineered and reimplemented.

## How it works

Offline key computation, not a bus tool: feed it a seed for a chosen ECU
and access level, and it returns the key. Definitions live in `db.json`
(ECU name, seed/key lengths, provider, parameters such as tables and
masks). Roughly 25 security providers are built in — the DaimlerStandard
family, PowertrainBoschConti 1/2, PowertrainDelphi, VolkswagenSA2,
EsLibEd25519, XorAlgo, and more — heavily Daimler-weighted. It is a
concrete catalogue of the algorithms whose failure modes the
[UDS seed/key](concepts/uds-seed-key.md) page analyses.

## Where it fits

Computing a SecurityAccess key for a supported — especially
Mercedes/Daimler — ECU when your diagnostic client cannot unlock it
itself: [udsoncan](udsoncan.md) asks for the key, UnlockECU computes it.

## Limits and notes

From the README's own notes: definitions exist only where they could
be reverse-engineered from DLLs/SMR-D files, so some ECUs are
unavailable (high-level instrument-cluster definitions, for example);
if you already have a DLL-based generator it "does not offer much more"
beyond a few modern targets; and `DaimlerStandardSecurityAlgo` is
usually for firmware flashing and "might not unlock other capabilities
such as variant-coding." No vehicle-safety warning is stated.

## Related

- [UDS seed/key](concepts/uds-seed-key.md) — the algorithms it implements, and why they fall.
- [udsoncan](udsoncan.md) — the client that consumes the computed key.
