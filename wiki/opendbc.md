---
title: "opendbc"
summary: "Python API for your car, bundling community-maintained DBC files with CAN parsing and car interface libraries for reading vehicle state and actuating controls."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/commaai/opendbc"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python API for your car, bundling community-maintained DBC files with CAN parsing and car interface libraries for reading vehicle state and actuating controls."
related: [cantools, python-can, savvycan]
license: MIT
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/commaai/opendbc"
    retrieved: 2026-10-31
---

Python API for your car, bundling community-maintained DBC files with CAN parsing and car interface libraries for reading vehicle state and actuating controls.

## What it is

comma's Python API for reading car state and actuating steering, gas, and
brakes, built primarily to support openpilot's ADAS interfaces. MIT.

## How it works

Four parts: `opendbc/dbc/` (a community DBC file collection),
`opendbc/can/` (parse and build CAN messages from DBCs), `opendbc/car/`
(a high-level per-brand car interface), and `opendbc/safety/`
(functional-safety firmware logic for all supported cars). A car port
lives in `opendbc/car/<brand>/`: `carstate.py` parses the CAN stream via
the DBC, `carcontroller.py` emits actuation messages, `fingerprints.py`
identifies models from ECU firmware versions, plus radar parsing and
values/interface modules. Connection is via a comma four and car harness
(which splits two CAN buses to inject actuation) and a panda interface;
reverse engineering is done from recorded routes in cabana. Decoding is
built on [cantools](cantools.md) and transport on [python-can](python-can.md).

## Where it fits

Adding or maintaining openpilot support for a car; programmatic vehicle
state reading and ADAS actuation on supported models; and as a large,
maintained DBC corpus in its own right — other tools in this KB (for
example [CanLab](canlab.md)) adapt its checksum algorithms.

## Limits and notes

Supportable cars are those with LKAS + ACC — most cars since 2016, per
the README's framing. The safety model is explicit: a panda powers up in
`SAFETY_SILENT` with the buses forced silent; sending requires selecting
a safety mode; `controls_allowed` gates message subsets; and
`SAFETY_ALLOUTPUT` is disabled in release firmware (it requires compiling
and flashing your own build). The safety code is held to MISRA C:2012
checks and 100% line coverage on its unit tests.

## Related

- [cantools](cantools.md) — the DBC decode/encode library in its stack.
- [python-can](python-can.md) — the transport layer underneath.
- [SavvyCAN](savvycan.md) — GUI analysis for the same buses.
