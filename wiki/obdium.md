---
title: "OBDium"
summary: "Rust-based OBD-II diagnostic tool with modern Tauri GUI supporting live data, DTC analysis, and offline VIN decoding."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/provrb/obdium"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Rust-based OBD-II diagnostic tool with modern Tauri GUI supporting live data, DTC analysis, and offline VIN decoding."
related: [opendbc, savvycan, python-can-isotp]
license: GPL-3.0
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/provrb/obdium"
    retrieved: 2026-10-31
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

## Related

- [opendbc](opendbc.md) — programmatic vehicle state and DBC corpus.
- [SavvyCAN](savvycan.md) — raw-bus analysis beneath the OBD-II layer.
- [python-can-isotp](python-can-isotp.md) — the transport diagnostics ride on.
