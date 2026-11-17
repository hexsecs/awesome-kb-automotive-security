---
uid: 01a19d3c-af7d-7e42-b216-c58c99234b50
title: "Doggie"
summary: "Modular DIY CAN-to-serial adapter from Faraday Security that speaks slcan over USB, BLE or UART for SocketCAN and python-can, with an EvilDoggie variant…"
type: entity
category: "Hardware Interfaces"
url: "https://github.com/infobyte/doggie"
status: maintenance
last_checked: 2026-11-17
created: 2026-11-02
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: e9533c9
list_summary: "Modular DIY CAN-to-serial adapter from Faraday Security that speaks slcan over USB, BLE or UART for SocketCAN and python-can, with an EvilDoggie variant adding offensive features for automotive research."
related:
  - cfuc
  - linusbconverter
  - supercan
  - owasp-automotive-emb-60
  - python-can
  - can-injection
  - can-availability
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-02
  - url: "https://github.com/infobyte/doggie"
    retrieved: 2026-11-17
  - url: "https://raw.githubusercontent.com/infobyte/doggie/main/README.md"
    retrieved: 2026-11-17
  - url: "https://api.github.com/repos/infobyte/doggie"
    retrieved: 2026-11-17
facets: [can, tools]
---

Modular DIY CAN-to-serial adapter from Faraday Security that speaks slcan over USB, BLE or UART for SocketCAN and python-can, with an EvilDoggie variant adding offensive features for automotive research.

## What it is

Doggie is an open-source, modular project from Faraday Security for building a DIY CAN-to-serial adapter. It was presented at Black Hat Arsenal on 6–7 August 2025 in Las Vegas and is MIT-licensed. One hardware/firmware base has two personalities: **Doggie**, a slcan adapter that behaves like a normal CAN interface, and **evilDoggie**, an offensive firmware variant for automotive security research. The upstream README describes the project as a work in progress.

## How it works

Doggie speaks the slcan (CAN over serial) ASCII protocol, so an assembled board appears as a serial device to Linux [SocketCAN](https://www.kernel.org/doc/html/latest/networking/can.html) through `slcand`, or directly to [python-can](python-can.md). The design is modular rather than tied to one board: supported microcontrollers include RP2040, STM32F103C8 and ESP32, with either a built-in CAN peripheral or an MCP2515 controller, and the host link can be USB, BLE or UART.

evilDoggie keeps the same interface but adds low-level bus behaviour intended for red-team and vulnerability work: dominant-override, bus-off, double-receive and physical-layer overrides, alongside spoofing and custom attacks. These are data-link and physical-layer primitives — the adapter becomes a programmable bus participant rather than a passive listener, which is the point for testing how ECUs react to malformed or adversarial traffic.

## Where it fits

Doggie is a build-your-own counterpart to ready-made slcan adapters: cheap, hackable, and with an offensive firmware option that normal interfaces do not offer. Compare it with [CFUC](cfuc.md) for a CAN FD USB converter or [LinUSBConverter](linusbconverter.md) for the LIN side of the same vehicle; [Supercan](supercan.md) and [python-can](python-can.md) are the broader software contexts. The [OWASP Automotive Embedded Security cheat sheet](owasp-automotive-emb-60.md) is the defensive reference for the behaviours evilDoggie deliberately produces.

## Limits and safety notes

The upstream disclaimer is explicit: the project is for educational and research purposes only, still a work in progress, and any use on real vehicles or production systems is the user's responsibility. Add to that a practical bench rule — dominant-override and bus-off are not passive operations. They can force error states, disrupt other nodes and leave a vehicle undriveable, so use a bench with correct termination and a recovery path, and only on systems you own or have explicit permission to test. Feature descriptions here come from the upstream README and repository metadata; no board was assembled or exercised for this page.

## Status and sources

Checked 2026-11-17. **Maintenance** at this check: public, not archived, MIT, 83 stars / 13 forks / 7 open issues, default branch last pushed 2025-10-27. The Black Hat Arsenal appearance was in 2025. Repository activity is not a support guarantee.

- [Upstream README](https://raw.githubusercontent.com/infobyte/doggie/main/README.md)
- [Repository metadata](https://api.github.com/repos/infobyte/doggie)
- [Project documentation](https://infobyte.github.io/doggie/)

## Related

- [CFUC](cfuc.md)
- [LinUSBConverter](linusbconverter.md)
- [Supercan](supercan.md)
- [OWASP Automotive Embedded Security Cheat Sheet](owasp-automotive-emb-60.md)
- [python-can](python-can.md)

## Connections

- [CAN injection](concepts/can-injection.md) — evilDoggie's spoofing and custom attacks turn the adapter into an adversarial bus participant.
- [CAN availability](concepts/can-availability.md) — dominant-override and bus-off features exercise the physical and error-handling mechanisms that can silence legitimate traffic.
