---
title: "CANalyzat0r"
summary: "Security analysis toolkit for proprietary car protocols with graphical sniffing, fuzzing, packet comparison, background-noise filtering, and UDS fuzzing."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/schutzwerk/CANalyzat0r"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Security analysis toolkit for proprietary car protocols with graphical sniffing, fuzzing, packet comparison, background-noise filtering, and UDS fuzzing."
related: [icsim, savvycan, cantoolz]
license: GPL-3.0
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/schutzwerk/CANalyzat0r"
    retrieved: 2026-10-31
---

Security analysis toolkit for proprietary car protocols with graphical sniffing, fuzzing, packet comparison, background-noise filtering, and UDS fuzzing.

## What it is

A GUI security-analysis toolkit for proprietary car protocols. It
originated as Philipp Schmied's bachelor's thesis at SCHUTZWERK in
collaboration with Aalen University and is hosted under the schutzwerk
organisation. GPLv3.

## How it works

A single tabbed Qt GUI over SocketCAN — it can load kernel modules and
manage physical and virtual SocketCAN devices itself, supports multiple
interfaces, and handles CAN FD. Work is organised into database-backed
projects (findings, dumps, and known packets per project; projects
import/export as human-readable JSON, and all actions are logged).
Analysis tabs run threaded sniffing, sending, and fuzzing. The distinctive
mechanisms are background-noise filtering to isolate action-specific
packets, binary packet filtering with randomisation, dump comparison, and
basic UDS fuzzing. All SocketCAN adapters should work in general; it is
tested with 8devices USB2CAN (CAN) and PEAK PCAN-USB Pro FD (CAN FD).

## Where it fits

Structured protocol-reversing engagements on an unknown bus — especially
the "do an action, find which packets changed" workflow — with findings
managed per project. The README itself suggests [ICSim](icsim.md) as the
safe practice target.

## Limits and notes

The application must run as superuser (its troubleshooting section is
explicit, including the `sudo -E` environment-preservation workaround);
the Docker build is the currently recommended install route. No
usage-safety disclaimer was found in the README.

## Related

- [ICSim](icsim.md) — the safe practice target the README recommends.
- [SavvyCAN](savvycan.md) — capture analysis and RE without the project layer.
- [CANToolz](cantoolz.md) — modular black-box analysis framework.
