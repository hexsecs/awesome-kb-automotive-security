---
uid: 01a1d439-cc56-7624-9f5f-2638c2058ac0
title: "Automotive Flash Bootloaders: Exposing Automotive ECU Updates"
summary: "Lapczynski, DEF CON 26 Car Hacking Village 2018. Walks through how UDS programming sessions, seed-key exchange, and flash routines expose ECU firmware…"
type: entity
category: "Conference Presentations"
url: "https://infocon.org/cons/DEF%20CON/DEF%20CON%2026/DEF%20CON%2026%20villages/DEF%20CON%2026%20villages%20captions/DEF%20CON%2026%20-%20CAR%20HACKING%20VILLAGE%20-%20Philip%20Lapczynski%20-%20Automotive%20Flash%20Bootloaders%20Exposing%20automotive%20ECU%20updates.eng.txt"
status: published
last_checked: 2026-11-17
created: 2026-11-13
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 6a8b17c
list_summary: "Lapczynski, DEF CON 26 Car Hacking Village 2018. Walks through how UDS programming sessions, seed-key exchange, and flash routines expose ECU firmware updates to attack."
related:
  - car-hacking-village
  - uds-firmware-extraction
  - zephyr-reference-ecu
  - openvehiclediag
  - bootloader-stages
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-13
  - url: "https://infocon.org/cons/DEF%20CON/DEF%20CON%2026/DEF%20CON%2026%20villages/DEF%20CON%2026%20villages%20captions/DEF%20CON%2026%20-%20CAR%20HACKING%20VILLAGE%20-%20Philip%20Lapczynski%20-%20Automotive%20Flash%20Bootloaders%20Exposing%20automotive%20ECU%20updates.eng.txt"
    retrieved: 2026-11-17
---

Lapczynski, DEF CON 26 Car Hacking Village 2018. Walks through how UDS programming sessions, seed-key exchange, and flash routines expose ECU firmware updates to attack.

## What it is

A DEF CON 26 Car Hacking Village talk by Philip Lapczynski, a senior staff engineer at Renesas, explaining what an automotive bootloader is, how a diagnostic tester drives one through a firmware update, and why that path is a rich attack surface. The talk is from 2018, so its "industry is moving towards" remarks should be read as a snapshot of that period rather than a current state.

## How it works

A bootloader owns the reset vector: on reset it decides whether the application is valid and either jumps to it, or — on deeply embedded devices — accepts a reprogramming request. Access is through the OBD connector (mandatory from 2008) onto CAN. CAN's 8-byte frames are too small for a firmware image, so ISO 15765 segmentation provides payloads up to about 4 KB, and ISO 14229 [UDS](uds.md) defines the client/server service API on top, including OEM- and supplier-specific services and tiered diagnostic sessions. Session 2 is the programming session; session 3 is the extended diagnostic session. The bootloader is normally a separately compiled executable, and the application hands over by setting flags and resetting.

The talk walks the three phases. **Pre-programming**: enter the extended session, disable DTCs (otherwise other ECUs log faults while a node is quiet) and disable non-diagnostic communication, possibly with security access. **Programming**: UDS service 0x27 seed/key challenge-response unlocks the bootloader — ISO does not define the algorithm, so it is OEM-specific and, historically, sometimes a weak secret algorithm with poor seed entropy. A WriteDataByIdentifier call may record a programming fingerprint or tester serial. Many OEMs then download a secondary bootloader containing the flash routines into RAM, so those routines are not resident in the ECU normally. Transfer uses 0x34 RequestDownload (address and length, or logical block IDs), 0x36 TransferData in ~4 KB chunks, and 0x37 TransferDataExit, where a checksum, integrity check or code-signing check may run, often through a RoutineControl. **Post-programming**: re-enable DTCs and normal communication, return to the default session and reset into the new application.

## Attack surface

The talk's core point is that a bootloader is a powerful separate application, so getting into it is itself useful. Keeping the application from running stops its legitimate CAN messages, letting an attacker spoof them on unauthenticated CAN. Subverting the validity check can run unsigned code. RequestUpload (0x35) can exfiltrate firmware if an OEM implemented it; ReadDataByIdentifier (0x22) may expose DIDs that exist only in the bootloader; ReadMemoryByAddress (0x23) and WriteMemoryByAddress give direct access where range checks are missing. The programming sequence can be recorded or man-in-the-middled — firmware is often unencrypted on the bus even when encrypted at rest — and valid sequences replayed. The programming tool itself is a softer target: it holds the images, the proprietary sequence details and possibly the symmetric keys. The 0x27 exchange is described as a "blind butler": once the door is unlocked anyone can walk through, so a valid session can be hijacked. A bootloader trojan can overwrite the bootloader with a persistent replacement. Over-the-air programming turns all of this into remote code execution, with added repository, rollback, freeze and denial-of-service attacks.

Defences discussed are code signing, secure boot chains (hard in an SoC with a long chain and divided key ownership), hardware security modules — SHE, EVITA levels, NXP's CSE, Infineon and Arm TrustZone — true random number generation for seeds, protected key storage, JTAG locking, tamper protection that erases keys, per-car keys and authenticated CAN via AUTOSAR.

## Where it fits

This is the conceptual foundation for [UDS firmware extraction](uds-firmware-extraction.md) and for [Zephyr-Reference-ECU](zephyr-reference-ecu.md), which implements the same 0x27/0x34/0x36/0x37 sequence with CMAC SecurityAccess and a signed-image check you can inspect end to end. [OpenVehicleDiag](openvehiclediag.md) is a client that drives real programming sessions, and [Car Hacking Village](car-hacking-village.md) is the venue series the talk belongs to.

## Limits and safety notes

This is a conference transcript, not a how-to: no OEM-specific algorithm, DID map or exploit is given — the speaker repeatedly notes those details are under NDA — and the defence discussion is from 2018. The bootloader and OTA mechanisms described are powerful and can brick an ECU or change safety-critical behaviour; any hands-on work needs a bench, a recovery path and authorisation. This page summarises the transcript; no programming session was performed for it.

## Status and sources

Checked 2026-11-17. **Published** — the talk was given at DEF CON 26 (2018) and the caption transcript is archived; it is a historical reference, not a live project.

- [Caption transcript](https://infocon.org/cons/DEF%20CON/DEF%20CON%2026/DEF%20CON%2026%20villages/DEF%20CON%2026%20villages%20captions/DEF%20CON%2026%20-%20CAR%20HACKING%20VILLAGE%20-%20Philip%20Lapczynski%20-%20Automotive%20Flash%20Bootloaders%20Exposing%20automotive%20ECU%20updates.eng.txt)

## Related

- [Car Hacking Village](car-hacking-village.md)
- [UDS firmware extraction](uds-firmware-extraction.md)
- [Zephyr-Reference-ECU](zephyr-reference-ecu.md)
- [OpenVehicleDiag](openvehiclediag.md)
- [Bootloader stages and bootstrap entry](concepts/bootloader-stages.md)
