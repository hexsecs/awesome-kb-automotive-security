---
title: "Simos18_SBOOT"
summary: "Documented exploit chain against the VW Simos18 supplier bootloader, chaining PWM entry, a weak Mersenne Twister seed/key, and a CRC bounds-check flaw into…"
type: entity
category: "Firmware and ECU Reverse Engineering"
url: "https://github.com/bri3d/Simos18_SBOOT"
status: unknown
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Documented exploit chain against the VW Simos18 supplier bootloader, chaining PWM entry, a weak Mersenne Twister seed/key, and a CRC bounds-check flaw into arbitrary flash read."
related: [tc1791-can-bsl, uds-seed-key, secure-firmware-updates, ivi-update-trust]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/bri3d/Simos18_SBOOT"
    retrieved: 2026-11-01
  - url: "https://github.com/bri3d/Simos18_SBOOT/blob/master/README.md"
    retrieved: 2026-11-01
---

Documented exploit chain against the VW Simos18 supplier bootloader, chaining PWM entry, a weak Mersenne Twister seed/key, and a CRC bounds-check flaw into arbitrary flash read.

## What it is

A fully documented exploit chain — writeup plus Python implementation — against SBOOT, the supplier bootloader in Continental Simos18.1–18.6 engine ECUs (Infineon TriCore TC1791) as fitted to VW/Audi EA888 Gen 3 vehicles such as the Mk7 Golf R and Audi S3 8V. SBOOT is the second, supplier-controlled boot stage whose whole job is to verify signed firmware before the application runs; the repository demonstrates defeating SBOOT's boot password and, through the companion BSL tooling, reading the ECU's flash despite it. It is the most complete public worked example in this section of how a production secure-boot chain fails in practice.

## How it works

The README documents the weaknesses composed into a chain. **Entry**: SBOOT keeps a backdoor open for a PWM calibration signal on an ECU pin — documented as a by-design feature for load-dump conditions, not a bug. Reaching it is bench work: the documented prerequisites include opening the ECU and soldering or probing the board vias, with a Raspberry Pi's GPIO generating the PWM signal. **Mode switch**: with a valid PWM input, an undocumented UDS routine switches the ECU from its locked ASW bootloader into SBOOT. **Seed/key**: SBOOT's challenge-response uses what appears to be a non-cryptographic PRNG (the writeup identifies Mersenne Twister characteristics) with a fallback seed value per variant, shrinking the search from 2^128 to roughly 2^20 candidates — the [UDS seed/key](concepts/uds-seed-key.md) failure class at its most concrete. **Erase logic**: a "passive" mode accepts erasure of flash already marked invalid, and a partially erased block revalidates. **The break**: a CRC bounds-check flaw lets the boot password be recovered by CRC back-calculation, using the reset/BSL trick and the `crchack` tool — the documented end state of the SBOOT stage itself is **boot-password recovery**, and flash read follows from it through the companion [TC1791_CAN_BSL](tc1791-can-bsl.md) workflow. Precision matters here: the writeup does **not** claim arbitrary unsigned code execution through SBOOT, and this page does not upgrade password recovery into a direct flash-read primitive.

## Where it fits

This is the section's anchor case study: the Ghidra work ([ghidra-tc1797](ghidra-tc1797.md) is the adjacent-chip analogue), the seed/key concept, and checksum analysis all converge here. Its companion piece is [TC1791_CAN_BSL](tc1791-can-bsl.md) by the same author — the SBOOT README links it by exactly that name as the follow-on stage the SBOOT session enables. Note also what the chain attacks: SBOOT was the *less* protected stage (the ASW bootloader carries the HSM-backed cryptography) — layered boot only helps if every layer holds.

## Limits and safety notes

Scope is narrow and dated by construction: Simos18.1–18.6 with SBOOT on the named hardware, physical bench access (opened ECU, soldered or probed vias, Pi GPIO for PWM), and per-variant seed values the writeup says took "quite a long time" to extract for two variants. The README flags the erase step as untested territory ("partially erased blocks" behaviour was inferred, not fully characterised), so the chain's middle is less certain than its ends. The repository carries no licence file. None of this generalises to other ECU families without redoing the research — which is precisely the page's defensive value: every link in the chain is a named, checkable design decision.

## Status and sources

Checked 2026-11-01. **Unknown**: the repository is not archived; its commits end at 2022-03-18 (a documentation polish) and there are no releases. It is a finished research artefact rather than a maintained tool — the status vocabulary has no "complete" value, and "unknown" records that no ongoing project state can be observed. Documentation claims above come from the following primary sources; no ECU was connected for this page.

- [Upstream repository](https://github.com/bri3d/Simos18_SBOOT)
- [Upstream README and exploit writeup](https://github.com/bri3d/Simos18_SBOOT/blob/master/README.md)

## Related

- [TC1791_CAN_BSL](tc1791-can-bsl.md)
- [Secure firmware updates](concepts/secure-firmware-updates.md)
- [UDS seed/key](concepts/uds-seed-key.md)
- [IVI update-path trust](concepts/ivi-update-trust.md)
