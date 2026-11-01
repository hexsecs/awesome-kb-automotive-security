---
title: "EcuBus-Pro"
summary: "Cross-platform open-source ECU tool with UDS, CAN-TP, DoIP, LIN, and SOME/IP support, DBC and LDF databases, TypeScript scripting in the style of CAPL, and…"
type: entity
category: "Diagnostic Tools"
url: "https://github.com/ecubus/EcuBus-Pro"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Cross-platform open-source ECU tool with UDS, CAN-TP, DoIP, LIN, and SOME/IP support, DBC and LDF databases, TypeScript scripting in the style of CAPL, and a command-line interface."
related: [udsoncan, odxtools, python-can]
license: "Apache-2.0"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/ecubus/EcuBus-Pro"
    retrieved: 2026-10-31
---

Cross-platform open-source ECU tool with UDS, CAN-TP, DoIP, LIN, and SOME/IP support, DBC and LDF databases, TypeScript scripting in the style of CAPL, and a command-line interface.

## What it is

A cross-platform (Windows/Linux/macOS) open-source ECU development and
diagnostic tool from the ecubus project (whyengineer), positioned as an
open alternative to commercial CANoe-class tooling. Apache-2.0.

## How it works

An Electron/TypeScript desktop app plus a CLI. Per the README it covers
UDS (ISO 14229), CAN-TP (ISO 15765-2), DoIP (ISO 13400), LIN, and
SOME/IP. It offers TypeScript scripting "like CAPL," a hardware-in-the-
loop test framework, a drag-and-drop panel builder, real-time signal
graphing, and DBC viewing plus LDF edit/export. Hardware support spans
PEAK, Kvaser, Vector, ZLG, and Toomoss interfaces (CAN/CAN-FD/LIN),
SLCAN and GS_USB/candleLight (CAN/CAN-FD), and the project's own
EcuBus-LinCable.

## Where it fits

Interactive ECU development and testing plus scripted diagnostic
sessions across CAN, DoIP, and LIN in one GUI+CLI tool — the closest
open-source shape to a commercial diagnostic workstation in this
section. Where [udsoncan](udsoncan.md) is a library you build on,
EcuBus-Pro is the finished application; where
[odxtools](odxtools.md) works from an ODX database, EcuBus-Pro works
interactively against the bus.

## Limits and notes

No limits or safety warnings are stated in the checked sources.

## Related

- [udsoncan](udsoncan.md) — the Python UDS client library.
- [odxtools](odxtools.md) — database-driven diagnostics from ODX.
- [python-can](python-can.md) — the transport layer under much of this section.
