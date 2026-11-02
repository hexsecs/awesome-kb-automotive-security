---
title: "CANdevStudio"
summary: "Flow-based graphical CAN simulation environment that wires senders, receivers, DBC decoders, and signal viewers together to stand in for missing ECUs on a…"
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/GENIVI/CANdevStudio"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Flow-based graphical CAN simulation environment that wires senders, receivers, DBC decoders, and signal viewers together to stand in for missing ECUs on a bench."
related: [cannelloni, busmaster, icsim, simulation-and-test-doubles]
license: MPL-2.0
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/GENIVI/CANdevStudio"
    retrieved: 2026-10-31
---

Flow-based graphical CAN simulation environment that wires senders, receivers, DBC decoders, and signal viewers together to stand in for missing ECUs on a bench.

## What it is

A Qt-based (C++/Qt 5, CMake) desktop tool for CAN bus *simulation*,
positioned as a cost-effective alternative to commercial CAN simulation
frameworks. Hosted under the GENIVI GitHub organisation. MPL-2.0.

## How it works

A component/node-graph model: a project is built by drag-and-drop, wiring
components together — CanDevice for the bus backend, CanRawView, CanSignalData
as the DBC signal database, and so on — then starting the simulation. Bus
access goes through Qt's CAN backends (SocketCAN, PEAK, Vector, Microchip,
PassThruCAN/J2534, and more). DBC is the supported signal-database format.
Since v1.1 it supports QML scripting loaded dynamically, for custom GUIs
and time- and message-triggered actions. It works with no hardware via
Linux `vcan`, or remotely via [cannelloni](cannelloni.md) — a dedicated Qt
cannelloni plugin ships with it.

## Where it fits

Bench simulation of missing ECUs and signal behaviour — ignition, doors,
and reverse gear are its own examples — and HMI/infotainment development
without a vehicle. [BUSMASTER](busmaster.md) covers the rest-bus
simulation end of the same problem with a different, window-based model;
[ICSim](icsim.md) is the narrower, single-purpose cluster simulator.

## Limits and notes

Legacy compilers (gcc 5.3, VS2015, MinGW) were dropped as of v1.2.0, and
the prebuilt Linux packages are built on ubuntu-latest, which the README
warns may hit library mismatches on other distributions. No safety
warnings are stated.

## Related

- [cannelloni](cannelloni.md) — the tunnel its remote setups use.
- [BUSMASTER](busmaster.md) — rest-bus simulation from Bosch/ETAS.
- [ICSim](icsim.md) — a single virtual instrument cluster, ready-made.
