---
title: "PiCCANTE"
summary: "Dirt-cheap CAN bus exploration tool built on Raspberry Pi Pico as an open-source hardware/software solution."
type: entity
category: "Penetration Testing"
url: "https://github.com/Alia5/PiCCANTE"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Dirt-cheap CAN bus exploration tool built on Raspberry Pi Pico as an open-source hardware/software solution."
related: [savvycan, can-utils, canhack, cantact, panda, donglescope]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/Alia5/PiCCANTE"
    retrieved: 2026-11-01
  - url: "https://github.com/Alia5/PiCCANTE/blob/main/Readme.md"
    retrieved: 2026-11-01
---

Dirt-cheap CAN bus exploration tool built on Raspberry Pi Pico as an open-source hardware/software solution.

## What it is

PiCCANTE ("Pi Controller Area Network Tool for Exploration") is an open-source hardware + firmware CAN exploration tool built on Raspberry Pi Pico boards — any model: RP2040 Pico/Pico W or RP2350 Pico 2/Pico 2 W. The design goal is a dead-simple, inexpensive, readily available vehicle-research interface: a Pico plus one to three CAN transceivers, with open KiCad hardware designs (perfboard build or manufactured PCB, OBD-II dongle form factor with a 3D-printable case) and prebuilt firmware distributed as GitHub releases. Licence: GPL-3.0.

## How it works

The Pico has no native CAN controller; PiCCANTE uses the PIO-based **can2040** implementation, which is why it speaks **CAN 2.0B only** — the FAQ attributes the lack of CAN FD/XL to can2040's scope, and support via an external controller such as MCP2518FD is invited but not implemented. Boards expose up to 2 CAN buses on RP2040 and 3 on RP2350. To the host it presents up to four driverless USB-CDC interfaces: one combined command CLI + **GVRET** (binary) interface, SavvyCAN-compatible, and up to three **SLCAN** interfaces, one per bus, SocketCAN-compatible on Linux via `slcand`. Pico W models add Wi-Fi (AP or client mode, with the command/GVRET interface also exposed as a Telnet server), a web configuration/monitoring interface, and Bluetooth. A partially implemented **ELM327 emulator** supports PID request/response with 11/29-bit addressing and multi-frame ISO-TP, with gaps the README flags itself. A CLI configures bitrates, buses, Wi-Fi and LEDs, settings persist to flash, and the board auto-sleeps on idle and wakes on CAN activity.

## Where it fits

The current low-cost-hardware entry of the section: a DIY alternative to commercial CAN interfaces that plugs straight into the standard analysis workflow — [SavvyCAN](savvycan.md) over GVRET, [can-utils](can-utils.md) over SLCAN/SocketCAN. It is the well-behaved-interface counterpart to [CANHack](canhack.md) (same Pico platform, protocol-attack intent), overlaps [CANtact](cantact.md) and [panda](panda.md) as an open CAN adapter — cheaper and CAN-2.0-only where panda is a finished product — and its ELM327 emulation makes it a bench stand-in for the dongles that [DongleScope](donglescope.md) tests.

## Limits and safety notes

Hard protocol limit: CAN 2.0B only — no CAN FD or XL. Several headline features are roadmap items, marked 🔜 in the README and **not** implemented: MITM mode, SD-card data logging, software CAN filters, web-UI live monitoring. The ELM327 emulator is partial by the author's own account, and the CAN bus must be configured beforehand ("this is a hacking-tool"). Hardware is DIY: the README warns that most transceiver breakout boards carry a 120 Ω termination resistor that must be removed when connecting to an already-terminated vehicle bus, and opens with "Always exercise caution when connecting to vehicle systems."

## Status and sources

Checked 2026-11-01. **Active**: the repository is not archived; created 2025-03-29, it has 291 commits with the latest on 2026-01-26, and firmware releases including v0.0.1 (2025-05-03) and a rolling dev-latest (updated 2026-01-26). Documentation claims above come from the following primary sources; no hardware was built for this page.

- [Upstream repository](https://github.com/Alia5/PiCCANTE)
- [Upstream README](https://github.com/Alia5/PiCCANTE/blob/main/Readme.md)

## Related

- [SavvyCAN](savvycan.md)
- [can-utils](can-utils.md)
- [CANHack](canhack.md)
- [CANtact](cantact.md)
- [panda](panda.md)
- [DongleScope](donglescope.md)
