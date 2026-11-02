---
title: "CanCat"
summary: "Firmware for Arduino CAN shields and Macchina M2 boards paired with a Python client for sniffing and injecting CAN traffic, running UDS and CCP sessions…"
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/atlas0fd00m/CanCat"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Firmware for Arduino CAN shields and Macchina M2 boards paired with a Python client for sniffing and injecting CAN traffic, running UDS and CCP sessions, and placing a device in the middle of a CAN link."
related: [caringcaribou, canarchy, savvycan]
license: BSD-2-Clause
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/atlas0fd00m/CanCat"
    retrieved: 2026-10-31
---

Firmware for Arduino CAN shields and Macchina M2 boards paired with a Python client for sniffing and injecting CAN traffic, running UDS and CCP sessions, and placing a device in the middle of a CAN link.

## What it is

A two-part CAN experimentation tool: firmware for Arduino-class CAN
transceivers plus a Python client/library (`cancatlib`). Maintained by
atlas0fd00m; the README acknowledges collaboration with GRIMM (SMFS)
researchers Matt Carpenter and Tim Brom. BSD-2-Clause.

## How it works

Supported hardware is Arduino + Seeed Studio CAN shield, Arduino Due +
Togglebit CAN shield, and Macchina M2 (under-dash and under-hood
variants). Once flashed and the baud rate is set, the device auto-captures
into an in-memory session that the user drives interactively, IPython-style:
ping, snapshot, bookmarks and comments on message ranges, filtering,
transmit, replay, and session save/load; captures can also be re-analysed
offline with no device attached.

Protocol modules sit on top: a **UDS module** (ReadDID/WriteDID, session
control, SecurityAccess with a user-supplied seed→key override, memory
read/write, download/upload, ECU reset) that reduces UDS-server and DID
scanning to a short script; a **CCP module** (leader/follower, parse and
generate per command); a **J1939 tool** (J1939Cat); format converters
(cancat ↔ candump/pcap); and `canmap`, a scanner built on the UDS class
that enumerates ECUs (default probe: ReadDID 0xF190, the VIN), DIDs, and
diagnostic sessions, saving resumable YAML scan configs.

## Where it fits

Low-cost, scriptable ECU and UDS discovery and session-level analysis;
isolating one device's traffic via the CAN-in-the-middle setup; and the
J1939 and CCP niches few other open tools cover. For broader exploration
workflows, compare [CaringCaribou](caringcaribou.md).

## Limits and notes

Captures live only in the session — unsaved messages are lost when the
session ends, and the README warns to save periodically. CCP gaps are
stated plainly: leader-side event/DAQ parsing is unimplemented, follower
DAQ functions are untested, and CCP endianness is implementation-specific.
CAN-in-the-middle requires physically modifying a shield (cutting the CS
trace and bridging it to D10). ECU scanning defaults to a 0.2 s timeout
versus the UDS-standard 3 s, so slow ECUs can be missed unless the timeout
is raised.

## Related

- [CaringCaribou](caringcaribou.md) — the other scriptable exploration tool.
- [CANarchy](canarchy.md) — event-stream analysis with UDS/DoIP workflows.
- [SavvyCAN](savvycan.md) — GUI capture analysis and UDS scanning.
