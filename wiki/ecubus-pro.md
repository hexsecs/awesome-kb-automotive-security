---
uid: 01a19d3c-af82-708f-b3be-4177fe48fdd1
title: "EcuBus-Pro"
summary: "Cross-platform open-source ECU tool with UDS, CAN-TP, DoIP, LIN, and SOME/IP support, DBC and LDF databases, TypeScript scripting in the style of CAPL, and…"
type: entity
category: "Diagnostic Tools"
url: "https://github.com/ecubus/EcuBus-Pro"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Cross-platform open-source ECU tool with UDS, CAN-TP, DoIP, LIN, and SOME/IP support, DBC and LDF databases, TypeScript scripting in the style of CAPL, and a command-line interface."
related:
  - udsoncan
  - odxtools
  - python-can
  - opensovd-classic-diagnostic-adapter
  - canexplorer
  - dbc-semantic-layer
  - doip
  - lin-bus
license: "Apache-2.0"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/ecubus/EcuBus-Pro"
    retrieved: 2026-10-31
  - url: "https://app.whyengineer.com/docs/um/script/script.html"
    retrieved: 2026-11-17
facets: [can, diagnostics, doip, lin, someip, tools]
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

The [scripting manual](https://app.whyengineer.com/docs/um/script/script.html),
checked with the repository on 2026-11-17, shows how bus work becomes
repeatable automation. Scripts execute in a Node.js environment;
TypeScript checks syntax and esbuild creates the build in `.ScriptBuild`.
Build errors appear in the application's Message window. `Util.Init()`
registers startup work, `Util.OnCan(id, callback)` handles a chosen CAN ID
(or `true` for all CAN traffic), and `Util.OnKey()` attaches actions to
keyboard input. CAN message objects carry an ID, direction, data buffer
and flags such as standard/extended ID, CAN FD and bit-rate switching,
rather than just a payload string.

Diagnostic scripts can listen for configured tester/service send and
receive events using `Util.On()`. The `runUdsSeq` API imported from `ECB`
runs a named `Tester.Sequence`; an optional progress callback reports
enabled items as they start and finish, and a sequence-stopping failure
rejects the promise. A useful workflow is therefore to configure and
exercise the diagnostic sequence interactively, add event handlers and
assertions around it, then reuse the automation rather than manually
clicking through each request.

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

The README's database feature labels are deliberately asymmetric: DBC
viewing is not a claim of full DBC editing or ODX-driven diagnostic
generation. Likewise, "like CAPL" describes the scripting role, not
source compatibility with CAPL; the documented runtime and API are
TypeScript/JavaScript and Node.js. Vendor and bus support must be checked
per adapter rather than inferred from the desktop operating-system list.
Node.js timers and scripted CAN output do not by themselves establish
hard-real-time scheduling guarantees, and a transmitted diagnostic
sequence still depends on the ECU's sessions and access controls.

## Related

- [udsoncan](udsoncan.md) — the Python UDS client library.
- [odxtools](odxtools.md) — database-driven diagnostics from ODX.
- [python-can](python-can.md) — the transport layer under much of this section.
- [DBC as the CAN semantic layer](concepts/dbc-semantic-layer.md)
- [DoIP moves diagnostics onto the network](concepts/doip.md)
- [LIN as the trusted subordinate bus](concepts/lin-bus.md)
