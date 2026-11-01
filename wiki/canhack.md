---
title: "CANHack"
summary: "Ken Tindell's proof-of-concept toolkit of low-level CAN protocol attacks such as Janus frames, bit-banged from a Raspberry Pi Pico on the CANPico board…"
type: entity
category: "Penetration Testing"
url: "https://github.com/kentindell/canhack"
status: maintenance
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Ken Tindell's proof-of-concept toolkit of low-level CAN protocol attacks such as Janus frames, bit-banged from a Raspberry Pi Pico on the CANPico board, with a Sigrok decoder for observing the attacks on a logic analyser."
related: [piccante, can-injection, savvycan]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/kentindell/canhack"
    retrieved: 2026-11-01
  - url: "https://github.com/kentindell/canhack/blob/master/README.md"
    retrieved: 2026-11-01
  - url: "https://kentindell.github.io/categories"
    retrieved: 2026-11-01
---

Ken Tindell's proof-of-concept toolkit of low-level CAN protocol attacks such as Janus frames, bit-banged from a Raspberry Pi Pico on the CANPico board, with a Sigrok decoder for observing the attacks on a logic analyser.

## What it is

Canis Labs' proof-of-concept toolkit of low-level CAN protocol attacks — attacks on the CAN protocol itself, executed by bit-banging rather than through a CAN controller. Part of the "Yes We CAN" project, it ships as portable C source (`src/canhack.c`, `src/canhack.h`), a MicroPython API baked into the firmware for Canis Labs' Pico-based boards, a Python tool for constructing CAN frame bitstreams (`src/canframe.py`, including Janus attack frames), and the `can2` Sigrok/PulseView protocol decoder for observing the attacks' effects on a logic analyser. Licence: MIT.

## How it works

A normal CAN controller enforces protocol rules — arbitration, CRC, error signalling — that make malformed-frame attacks impossible to launch. CANHack instead emulates "the minimal parts of the CAN protocol required" (author's blog) in software, driving the bus bit-by-bit so it can violate those rules deliberately. The documented centrepiece is the **Janus attack**: one frame whose bit-level construction makes a targeted receiver sample a different payload than every other receiver — a single CAN frame containing two different payloads. The author's writing covers further protocol attacks beyond Janus (blog posts on "three new CAN protocol hacks" and an ASRG webinar demonstrating five); the full catalogue lives in the blog posts and the MicroPython SDK reference manual in `docs/`, not the README. Hardware: the toolkit is built into the Canis Labs MicroPython firmware for the Raspberry Pi Pico / Pico W on the CANPico board, the dedicated CANHack board, and the Car Hacking Village DEF CON 30 badge. The bundled `can2` decoder lets PulseView decode CAN 2.0 and flag exceptional low-level protocol events.

## Where it fits

The protocol-layer attack entry of the section: where most other pages attack ECUs, services or radios, CANHack attacks the bus protocol's own assumptions — related to, but distinct from, frame-level impersonation in the [CAN injection](concepts/can-injection.md) concept. Its closest sibling is [PiCCANTE](piccante.md): same Pico host platform, opposite intent — PiCCANTE is a well-behaved CAN interface, CANHack exists to misbehave precisely. The `can2` decoder half overlaps the CAN Bus Analysis section's tooling at a lower level: [SavvyCAN](savvycan.md) works at frame level, `can2` at bit level.

## Limits and safety notes

Explicitly a proof-of-concept, not a maintained pentest product: the attacks demonstrate the viability of protocol-level abuse on bench hardware. It requires the named Pico-based boards and firmware — it is not a SocketCAN tool and does not run against arbitrary CAN interfaces. The README carries no safety warnings; the attacks are by construction disruptive to a live bus, so bench use is the implied context.

## Status and sources

Checked 2026-11-01. **Maintenance**: the repository is not archived; its latest commit is 2024-04-01, following activity from 2020 to 2024, and there are no releases. The surrounding project (Canis Labs blog, CANPico hardware) remains the author's public work, but the repository itself has had no commits in roughly the last 19 months. Documentation claims above come from the following primary sources; no CAN bus was connected for this page.

- [Upstream repository](https://github.com/kentindell/canhack)
- [Upstream README](https://github.com/kentindell/canhack/blob/master/README.md)
- [Author's blog](https://kentindell.github.io/categories)

## Related

- [PiCCANTE](piccante.md)
- [CAN injection](concepts/can-injection.md)
- [SavvyCAN](savvycan.md)
