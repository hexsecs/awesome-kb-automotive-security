---
uid: 01a19d3c-af4e-7cad-ad2c-003196045198
title: "CANToolz"
summary: "Black-box CAN network analysis framework also known as YACHT with modular architecture for fuzzing and ECU discovery."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/CANToolz/CANToolz"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Black-box CAN network analysis framework also known as YACHT with modular architecture for fuzzing and ECU discovery."
related:
  - caringcaribou
  - canalyzat0r
  - icsim
  - savvycan
  - diagnostic-fuzzing
  - cantot
  - carpunk
  - can-injection
  - can-availability
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/CANToolz/CANToolz"
    retrieved: 2026-10-31
facets: [can, attack, tools]
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

The [repository README](https://github.com/CANToolz/CANToolz), reachable
on 2026-11-17, documents `cantoolz -g w -c examples/can_sniff.py` as a
starting configuration, with the web interface on localhost port 4444.
The configuration is the experiment: choose an I/O module for the bus,
then compose processing stages rather than treating discovery, filtering
and replay as unrelated programs. `firewall` blocks frames by ID, `ping`
generates chosen IDs for ECU/service discovery, and `analyze` exports
statistics as CSV as well as attempting UDS/ISO-TP detection. A changed
capture or detected service is an analysis lead, not an OEM signal
definition or proof of an exploitable ECU.

The documented VIRCar exercise uses two processes. `examples/car_config.py`
hosts the simulated car and its web interface on port 5555; after starting
it, `examples/car_hacker.py` connects through `hw_TCP2CAN` to its OBD2 and
CABIN buses. This separates a target configuration from the analysis
configuration while exercising the same module chaining used with
hardware. It is useful for learning filtering and frame-generation
workflows before involving a physical network.

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

The README identifies the Python 2.7 release as a separate historical
branch; old examples and dependencies should therefore be checked
against the chosen checkout. The CAN socket module is Linux-only,
whereas TCP tunnelling provides a different I/O path. Neither modularity
nor VIRCar implies complete vehicle emulation, universal adapter support
or production-grade protocol conformance. Scanning, proxy fuzzing and
replay actively transmit: begin with a virtual or isolated bench target,
and control frame timing rather than equating successful replay with
safe replay.

## Related

- [CaringCaribou](caringcaribou.md) — modular exploration, reconnaissance-first.
- [CANalyzat0r](canalyzat0r.md) — GUI-driven protocol analysis projects.
- [ICSim](icsim.md) — a safe practice target.
- [SavvyCAN](savvycan.md) — capture analysis and UDS scanning.
- [CAN injection](concepts/can-injection.md) — why generated and replayed
  frames can impersonate legitimate traffic.
- [CAN availability](concepts/can-availability.md) — why replay rate and
  discovery traffic are operational limits, not just performance settings.
