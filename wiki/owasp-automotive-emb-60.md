---
title: "OWASP Automotive EMB 60"
summary: "OWASP incubator project with open hardware and software for a single-board computer that acts as a CAN-to-USB interface through SocketCAN for penetration…"
type: entity
category: "Hardware Interfaces"
url: "https://owasp.org/www-project-automotive-emb-60/"
status: unknown
last_checked: 2026-11-01
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
  - url: "https://github.com/PhilippSchmitt/emb60"
    retrieved: 2026-11-01
---

OWASP incubator project with open hardware and software for a single-board computer that acts as a CAN-to-USB interface through SocketCAN for penetration testing.

## What it is

An OWASP **incubator-stage** project that specifies a small, cheap automotive pentest appliance: a single-board computer (the project documentation names an Allwinner F1C100s board, pictured as a Lichee Pi Nano-class board) paired with a custom STM32-based CAN board, so the combination presents a CAN interface to its Linux host stack through SocketCAN for penetration testing of vehicles and components.

## How it works

The architecture is two boards: the SBC runs the Linux environment and tooling, and the CAN board (STM32-based — project issue history discusses F042/F072-class parts; the checked READMEs do not pin an exact part number, so this page does not either) bridges the vehicle bus to the SBC. The project page and the founding repository (Philipp Schmitt's emb60, from which the OWASP project grew; a second contributor repository covers CAN-board hardware revision work) describe the goal as a reproducible, documented, low-cost platform rather than a product — parts lists and setup documentation over finished firmware.

## Where it fits

EMB 60 is the standards-body attempt at what [RAMN](ramn.md) later did with manufacturer backing: a reference platform a pentester or student can build to learn vehicle-network testing without improvising hardware. Against a plain [CANtact](cantact.md) it adds the standalone-computer appliance idea (the SBC *is* the test host). Its lasting value in this KB is as the documented baseline of that idea — and as a caution about incubator-stage momentum (see Status).

## Limits and safety notes

Incubator stage means exactly what it says: no graduated-project assurance, no releases, and documentation over deliverables. The hardware definition is less pinned than the list summary implies — SBC identity rests on a README image caption and contributor repos rather than a normative spec, and the CAN board's exact MCU is not fixed in the primary sources checked. Anyone building one today is doing archaeology as much as assembly; RAMN or a candleLight-class adapter will reach a working bus faster.

## Status and sources

Checked 2026-11-01. **Unknown**: the OWASP project page's own metadata shows it last updated 2022-03-12 at incubator stage, and the founding repository's last push is 2022-08 with no releases and no commits since. Nothing in the primary sources marks the project archived or formally ended, so "unknown" — not archived — is the honest call: dormant since 2022, status unconfirmed by its owners. Documentation claims above come from the following primary sources; no hardware was built for this page.

- [OWASP project page](https://owasp.org/www-project-automotive-emb-60/)
- [Founding repository](https://github.com/PhilippSchmitt/emb60)

## Related

- [RAMN](ramn.md)
- [CANtact](cantact.md)
