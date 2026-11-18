---
uid: 01a19d3c-afb2-7b37-9897-673b12cbb4ef
title: "OBDium"
summary: "Rust-based OBD-II diagnostic tool with modern Tauri GUI supporting live data, DTC analysis, and offline VIN decoding."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/provrb/obdium"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Rust-based OBD-II diagnostic tool with modern Tauri GUI supporting live data, DTC analysis, and offline VIN decoding."
related:
  - opendbc
  - savvycan
  - python-can-isotp
  - can-playground
  - diagnostic-service-abuse
  - simulation-and-test-doubles
license: GPL-3.0
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/provrb/obdium"
    retrieved: 2026-10-31
facets: [diagnostics, tools]
---

Rust-based OBD-II diagnostic tool with modern Tauri GUI supporting live data, DTC analysis, and offline VIN decoding.

## What it is

A desktop OBD-II diagnostic application: Rust backend with a Tauri/web
frontend, GPL-3.0, cross-platform (macOS, Windows 10/11, Linux). The repo
owner is the GitHub account `provrb`; the README states no person or
organisation name beyond that.

## How it works

OBDium connects over a serial port to an ELM327 adapter. A central `OBD`
struct issues service/PID requests (for example `0105` for coolant
temperature), receives hex-encoded responses, and evaluates the standard
byte equations (A, B, C…; e.g. `A - 40`). Features include live PID
dashboards and graphs, DTC reading across Powertrain/Body/Chassis/Network
with descriptions, I/M readiness, custom PIDs, and offline VIN decoding
via a custom parser over a SQLite database derived from NHTSA's vPIC
data. Everything runs fully offline. A demo mode replays a recorded
`requests.json` — responses can be recorded from a real vehicle — to
simulate a car without hardware.

The [project README](https://github.com/provrb/obdium), checked
2026-11-17, describes connection configuration through a serial-port
selector, an OBD-II protocol setting, and a baud-rate setting. Port
discovery can be refreshed from the Connection panel. This is an
ELM327-mediated request/response workflow, not direct SocketCAN frame
capture; the adapter and selected protocol sit between the app and
the vehicle's diagnostic interface.

Once connected, the OBD Dashboard displays tracked metrics, the Graphs
panel visualises live data, and the DTC panel presents fault codes.
Clicking a metric card stops tracking it; it can be resumed from the
bottom of the dashboard. The PID List provides an index and lets the
user add a custom PID. Readiness reporting covers compression- and
spark-ignition engines. VIN decoding is a separate local lookup/parsing
path, so decoding a VIN should not be confused with discovering which
diagnostic requests a particular ECU actually supports.

For repeatable UI evaluation, enable **Record OBD Responses** in Settings
while connected to capture the app's response data. The README places
the default recording in a `data` subdirectory and allows its location
to be changed. Supplying an OBDium `requests.json` recording and choosing
**DEMO MODE** as the serial port replays those exchanges locally.
That file is an application-specific replay fixture, not a raw CAN
capture or a vehicle database. It lets a bug report or demonstration
reuse observed responses without maintaining a live hardware connection.

## Where it fits

End-user and technician OBD-II diagnostics and live-data viewing without
proprietary scan-tool software; offline VIN decoding; and evaluating the
app via demo mode before connecting hardware. It sits at the
diagnostics end of this section, a layer above the raw-bus tools like
[SavvyCAN](savvycan.md).

## Limits and notes

Manufacturer-specific PIDs are stated as planned, not present — current
decoding is the standard PID set. No safety warnings are stated in the
README.

The custom-PID entry feature should not be conflated with built-in
manufacturer-specific coverage. Similarly, displaying Body, Chassis,
or Network DTC descriptions does not demonstrate access to every
manufacturer's control modules. Demo replay validates handling of the
recorded responses, not adapter reliability or full vehicle behaviour.

## Related

- [opendbc](opendbc.md) — programmatic vehicle state and DBC corpus.
- [SavvyCAN](savvycan.md) — raw-bus analysis beneath the OBD-II layer.
- [python-can-isotp](python-can-isotp.md) — the transport diagnostics ride on.
- [Diagnostic-service abuse](concepts/diagnostic-service-abuse.md)
- [Simulation and test doubles](concepts/simulation-and-test-doubles.md) —
  why recorded responses exercise the app without reproducing a whole ECU.
