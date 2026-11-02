---
title: "OWASP Automotive EMB 60"
summary: "OWASP incubator project with open hardware and software for a single-board computer that acts as a CAN-to-USB interface through SocketCAN for penetration…"
type: entity
category: "Hardware Interfaces"
url: "https://owasp.org/www-project-automotive-emb-60/"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "OWASP incubator project with open hardware and software for a single-board computer that acts as a CAN-to-USB interface through SocketCAN for penetration testing."
related: [ramn, cantact]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://owasp.org/www-project-automotive-emb-60/"
    retrieved: 2026-11-01
  - url: "https://github.com/OWASP/www-project-automotive-emb-60"
    retrieved: 2026-11-01
---

OWASP incubator project with open hardware and software for a single-board computer that acts as a CAN-to-USB interface through SocketCAN for penetration testing.

## What it is

An OWASP **incubator-stage** project documenting an automotive security test board. The documented design is a **custom board built around a Microchip ATSAME70N21B** with **two MCP2562FD CAN FD transceivers** — a 2-channel CAN FD interface with a single D-Sub 9 connector, a 40-pin Raspberry-Pi-like expansion header, and the SAME70's security peripherals in play (MPU, TRNG, hardware AES and SHA). That is the design the project's own documentation specifies; earlier guesses built on contributor repositories (an Allwinner F1C100s / Lichee Pi SBC plus a separate STM32 CAN board) do not match it, and this page does not repeat them.

## How it works

The documentation goes beyond the interface itself: it specifies a **secure bootloader** for the board — firmware updates delivered over ISO-TP/UDS, update distribution protected with AES-128-GCM, secure boot verified with HMAC-SHA256, and key material protected by the MPU. The caveat is availability: **no firmware or hardware source repository could be found** for this project. The only GitHub repository is the OWASP website repository (`OWASP/www-project-automotive-emb-60`, no licence recorded), and its code-repository link is a placeholder. So the design — board and bootloader alike — is documented but unverified: there is nothing public to build from or audit.

## Where it fits

EMB 60 is the standards-body attempt at what [RAMN](ramn.md) later did with manufacturer backing: a reference platform a pentester or student can use to learn vehicle-network testing. Against a plain [CANtact](cantact.md) it aimed higher — CAN FD channels and a secure-boot story of its own. Its lasting value in this KB is as the documented baseline of that idea, and as a caution about the distance between a documented design and a obtainable one (see Status).

## Limits and safety notes

Incubator stage means exactly what it says, and here it also means *documentation only*: no source repository, no releases, no board to buy or build from the project's own artefacts. The secure-bootloader design is a specification, not reviewed code — none of its properties (key storage, update authentication) can be checked against an implementation, because none is public. Anyone wanting a working platform today should start from RAMN or a candleLight-class adapter; EMB 60 is a reference to read, not a device to deploy.

## Status and sources

Checked 2026-11-01. **Unknown**: the project is still listed as an OWASP Incubator project, but every substantive content commit in its website repository dates from March 2021, and no implementation repository has surfaced since. The honest verdict is a **dormant incubator**: documented, never visibly shipped, and not formally ended by its owners. Documentation claims above come from the following primary sources; no hardware was built for this page.

- [OWASP project page](https://owasp.org/www-project-automotive-emb-60/)
- [OWASP website repository](https://github.com/OWASP/www-project-automotive-emb-60)

## Related

- [RAMN](ramn.md)
- [CANtact](cantact.md)
