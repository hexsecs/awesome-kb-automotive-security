---
title: "uds"
summary: "Python package for ISO 14229 UDS in both client and server roles over CAN, Ethernet, LIN, FlexRay, and K-Line, usable for simulation, testing, and decoding…"
type: entity
category: "Diagnostic Tools"
url: "https://github.com/mdabrowski1990/uds"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python package for ISO 14229 UDS in both client and server roles over CAN, Ethernet, LIN, FlexRay, and K-Line, usable for simulation, testing, and decoding UDS traffic."
related: [udsoncan, python-can, python-can-isotp]
license: "MIT"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/mdabrowski1990/uds"
    retrieved: 2026-10-31
  - url: "https://uds.readthedocs.io/en/stable/"
    retrieved: 2026-10-31
---

Python package for ISO 14229 UDS in both client and server roles over CAN, Ethernet, LIN, FlexRay, and K-Line, usable for simulation, testing, and decoding UDS traffic.

## What it is

A Python package for UDS (ISO 14229) communication by Mateusz
Dabrowski, published as py-uds. MIT-licensed. Its stated design goal is
a common API across buses (CAN, Ethernet, LIN, FlexRay, K-Line,
extensible to custom transports) and across *both* communication sides,
where existing packages focus on a single bus or on client-only use.

## How it works

Layered on the OSI model: `uds.message` (diagnostic messages),
`uds.translator` (build/interpret), `uds.packet` and
`uds.segmentation` (bus-specific packets, segmentation and
desegmentation), `uds.transport_interface`, bus handling delegated to
external packages (python-can for CAN), and `uds.client` for client
simulation. Per its docs' status tables, implemented today are
message/packet send-receive, segmentation, the message translator, the
logger, and client simulation — with CAN the only bus at "Full."

## Where it fits

Message-level UDS simulation and test work: building, sending,
receiving, and decoding UDS traffic and simulating a client against an
ECU, with [python-can](python-can.md) underneath. Where
[udsoncan](udsoncan.md) is the finished session client, py-uds is the
packet-level workbench beneath that abstraction.

## Limits and notes

Its own docs state: "The package is currently in the early development
phase, therefore only a few features are currently available" —
server simulation and the UDS sniffer are planned, not present, and
FlexRay, Ethernet, K-Line, and LIN support are planned only. No
vehicle-safety warning is stated in the checked sources.

## Related

- [udsoncan](udsoncan.md) — the session-level client one layer up.
- [python-can](python-can.md) and [python-can-isotp](python-can-isotp.md) — its CAN transports.
