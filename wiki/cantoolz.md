---
title: "CANToolz"
summary: "Black-box CAN network analysis framework also known as YACHT with modular architecture for fuzzing and ECU discovery."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/CANToolz/CANToolz"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Black-box CAN network analysis framework also known as YACHT with modular architecture for fuzzing and ECU discovery."
related: [caringcaribou, canalyzat0r, icsim, savvycan]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/CANToolz/CANToolz"
    retrieved: 2026-10-31
---

Black-box CAN network analysis framework also known as YACHT with modular architecture for fuzzing and ECU discovery.

## What it is

A modular framework for black-box CAN analysis, also called **YACHT —
Yet Another Car Hacking Tool**. The README identifies Alexey Sintsov as
creator.

## How it works

A configuration loads I/O and processing modules and chains them through
numbered **pipes**. I/O modules cover USBtin, CANBus Triple,
LAWICEL/Seeed-style serial hardware, Linux CAN sockets, and TCP
tunnelling. Frames then pass through analysis, ping/discovery, replay,
firewall, printing, or single-byte proxy-fuzzing modules. The `analyze`
module keeps traffic in buffers and supports statistics, capture diffing,
ISO-TP/UDS detection, and experimental STATCHECK profiling to isolate
action frames. It can run through a web interface, and its VIRCar
configuration simulates a virtual car for exercises.

## Where it fits

Finding control and status frames by comparing captures, UDS and ISO-TP
discovery, man-in-the-middle filtering, replay, chained test scenarios,
and ECU prototyping — with [ICSim](icsim.md)-class simulators and VIRCar
as safe targets. [CaringCaribou](caringcaribou.md) covers the
reconnaissance end of the same work with a tighter module model.

## Limits and notes

The README explicitly calls it "very early-uber-alpha," says bugs remain,
and instructs users to use it as-is. Its replay documentation warns that
inadequate inter-frame delay can cause a CAN-bus denial of service. The
documented physical-hardware set is narrower than python-can's backend
range.

## Related

- [CaringCaribou](caringcaribou.md) — modular exploration, reconnaissance-first.
- [CANalyzat0r](canalyzat0r.md) — GUI-driven protocol analysis projects.
- [ICSim](icsim.md) — a safe practice target.
- [SavvyCAN](savvycan.md) — capture analysis and UDS scanning.
