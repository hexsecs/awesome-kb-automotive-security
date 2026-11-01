---
title: "doip-sim-ecu-dsl"
summary: "Kotlin DSL for scripting simulated DoIP ECUs, reachable over Ethernet, CAN with ISO-TP, or both at once, for exercising diagnostic clients against UDS error…"
type: entity
category: "Diagnostic Tools"
url: "https://github.com/doip-sim-ecu/doip-sim-ecu-dsl"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Kotlin DSL for scripting simulated DoIP ECUs, reachable over Ethernet, CAN with ISO-TP, or both at once, for exercising diagnostic clients against UDS error and edge cases without hardware."
related: [python-doipclient, uds-server, udsim]
license: "Apache-2.0"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/doip-sim-ecu/doip-sim-ecu-dsl"
    retrieved: 2026-10-31
---

Kotlin DSL for scripting simulated DoIP ECUs, reachable over Ethernet, CAN with ISO-TP, or both at once, for exercising diagnostic clients against UDS error and edge cases without hardware.

## What it is

A Kotlin/JVM domain-specific language and library for quickly writing
DoIP ECU simulations, by the doip-sim-ecu organisation. Apache-2.0.

## How it works

You declare gateways and ECUs with logical/physical addresses and
request→response matchers in the DSL (e.g. `request("11 03") { ack() }`);
`start()` registers the entities on the network interfaces, emits
Vehicle Announcement Messages, and answers UDP/TCP on port 13400 (on a
ktor-network stack). It also simulates ECUs on CAN speaking UDS over
ISO-TP (ISO 15765-2 — segmentation, flow control, and CAN FD escape
encodings implemented in pure Kotlin) via SocketCAN (Linux, optional
javacan dependency) or socketcand over TCP, and `multiTransport` blocks
make one ECU instance dual-homed on DoIP + CAN with shared state. Its
stated purpose: integration and regression tests for DoIP clients,
especially error and edge cases.

## Where it fits

Automated test doubles for DoIP (and CAN/UDS) clients in CI — the only
entry in this section built for programmatic integration testing, and
the natural server-side partner to
[python-doipclient](python-doipclient.md). [UDSim](udsim.md) and
[uds-server](uds-server.md) simulate from recorded behaviour instead of
declarations.

## Limits and notes

The README's stated CAN limitations: CAN FD is not available via
socketcand (the upstream protocol has no FD frame message);
`hardResetEntityFor` is DoIP-only and ignored on CAN; sub-millisecond
STmin values (0xF1–0xF9) are rounded up to 1 ms; and the SocketCAN
transport is Linux-only, needing the optional javacan dependency.

## Related

- [python-doipclient](python-doipclient.md) — the client this simulates for.
- [uds-server](uds-server.md) and [UDSim](udsim.md) — the recorded-behaviour simulators.
