---
uid: 01a19d3c-af92-72d3-a43f-50759978a861
title: "gallia"
summary: "Extendable automotive pentesting framework from Fraunhofer AISEC focused on UDS, with DoIP and ISO-TP transports and structured logging for reproducible scans."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/Fraunhofer-AISEC/gallia"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Extendable automotive pentesting framework from Fraunhofer AISEC focused on UDS, with DoIP and ISO-TP transports and structured logging for reproducible scans."
related: [udsoncan, iso14229, caringcaribou]
license: "Apache-2.0"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/Fraunhofer-AISEC/gallia"
    retrieved: 2026-10-31
---

Extendable automotive pentesting framework from Fraunhofer AISEC focused on UDS, with DoIP and ISO-TP transports and structured logging for reproducible scans.

## What it is

An extendable pentesting framework focused on the automotive domain,
from Fraunhofer AISEC. Its scope is pentests "from a single ECU up to
whole cars," with the main focus on the UDS interface. Apache-2.0;
partly funded by BMBF/BMWE projects (SecForCARs, ATLAS-L4).

## How it works

Python and asyncio-based, CLI-driven via the `gallia` command, with
defaults taken from a `gallia.toml` (generatable with `--template`).
Targets are URIs that select a transport — verified schemes:
`isotp://` (Linux kernel ISO-TP over SocketCAN, with CAN-FD options),
`can-raw://`, `doip://` (gateway plus routing activation), `hsfz://`,
and `tcp-lines://` (a hex-line test transport). Commands are organised
as UDS primitives and scanners (the quickstart shows
`gallia primitive uds dtc read`); a generic logging interface is a core
design point, implementing reproducible tests and post-processing. It
is the framework counterpart to [CaringCaribou](caringcaribou.md)'s
module CLI in the CAN section, one diagnostic layer up.

## Where it fits

Reproducible, logged UDS penetration tests and scans against an ECU or
a whole vehicle, over CAN or DoIP — the research-grade option in this
section, where [udsoncan](udsoncan.md) is the production client and
[iso14229](iso14229.md) the embedded library.

## Limits and notes

The README carries an explicit warning: "this project is intended for
research and development usage only! Inappropriate usage might cause
irreversible damage to the device under test. We do not take any
responsibility for damage caused by the usage of this tool."

## Related

- [udsoncan](udsoncan.md) — the production UDS client.
- [iso14229](iso14229.md) — the embedded C implementation, server and client.
- [CaringCaribou](caringcaribou.md) — CAN-layer exploration, the layer below.
