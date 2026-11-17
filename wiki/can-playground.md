---
uid: 01a1de8a-a621-7640-91b6-87b69fab5d55
title: "CAN Playground"
summary: "Local-first Tauri desktop app for viewing, decoding, and capturing CAN bus traffic, with DBC import, signal annotation, and bit-level change timelines."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/numbpill3d/can-playground"
status: active
last_checked: 2026-11-17
created: 2026-11-15
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 87fdec8
list_summary: "Local-first Tauri desktop app for viewing, decoding, and capturing CAN bus traffic, with DBC import, signal annotation, and bit-level change timelines."
related:
  - canarchy
  - security-in-automotive-bus-systems
  - canlab
  - cangaroo
  - cantools
  - obdium
  - dbc-semantic-layer
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-15
  - url: "https://github.com/numbpill3d/can-playground"
    retrieved: 2026-11-17
  - url: "https://raw.githubusercontent.com/numbpill3d/can-playground/master/README.md"
    retrieved: 2026-11-17
  - url: "https://api.github.com/repos/numbpill3d/can-playground"
    retrieved: 2026-11-17
---

Local-first Tauri desktop app for viewing, decoding, and capturing CAN bus traffic, with DBC import, signal annotation, and bit-level change timelines.

## What it is

CAN Frame Playground is a desktop log viewer and light reverse-engineering aid built with Tauri v2: a Rust backend for native work (including live capture), a vanilla HTML/CSS/JavaScript frontend, and Chart.js for plots. The upstream README describes it as local-first — no network requests and no telemetry — and distributes 0.1.0-era `.deb`, `.rpm` and AppImage binaries for Linux. Windows and macOS builds are possible from source, but live capture is Linux-only. The repository is MIT-licensed and was created 2026-03-01.

## How it works

Logs enter as candump lines, bare `ID#payload` lines (synthetic sequential timestamps), Vector `.asc`, or PCAN `.trc` (v1.1 and v2.x), pasted or dragged in. Parsed frames feed four linked views:

- **Hex Dump** — a virtualised byte table for 100k+ frame logs, with delta-from-previous or delta-from-baseline highlighting, byte-order-aware signal overlays, per-cell hex/decimal/binary tooltips, byte-condition filters (`B0>0x80`, `B2==0xFF`), and right-click copy as candump line, bytes literal, C array or CSV.
- **Delta Graph** — Chart.js plots of byte values, decoded signals, or message rate, with zoom/pan and an overlay mode for comparing several IDs on one timebase.
- **Bit Map** — a canvas-rendered per-bit timeline across frames; static bits are muted and toggling bits coloured per byte, with automatic subsampling for large logs.
- **Stats** — per-byte min/max/mean/stdev/unique-count/change-rate plus frame-rate and inter-frame-interval timing.

Signal annotations are defined by start bit, length, byte order (Intel little-endian or Motorola big-endian), type, scale, offset and unit; a DBC import populates matching IDs, and annotations round-trip as JSON in saved sessions. Live capture connects to a named SocketCAN interface (`can0`, `vcan0`, `any`) and streams through the Rust backend, which invokes `candump` from `can-utils`.

## Where it fits

This is a log-triage and bit-level inspection tool, not a protocol stack: it helps you see *which bytes and bits move* before you know what they mean. It sits between raw `candump` output and the heavier decoding environments — [Cangaroo](cangaroo.md) or [SavvyCAN](savvycan.md) for broader GUI work, [cantools](cantools.md) when the DBC is already authoritative. For diagnostic sessions, [CANarchy](canarchy.md) covers the interactive side; for the bus-security context these traces feed, see [Security in automotive bus systems](security-in-automotive-bus-systems.md) and [CAN Lab](canlab.md).

## Limits and safety notes

The upstream release line is still 0.1.0-era and the interface list is short: capture requires Linux, an up SocketCAN interface and `candump`; Windows/macOS users can only parse logs unless they build locally. The README itself warns that DBC signals decode incorrectly when byte-order or start-bit conventions differ between tools — verify imported annotations against a known frame. There is no UDS, J1939 or XCP protocol decode: DBC annotations are the only semantic layer, so "decoded" here means signals you defined, not vehicle semantics inferred by the tool. No hardware execution was performed for this page; feature descriptions come from the upstream README. Joining a live bus still requires the correct bitrate and an authorised bench.

## Status and sources

Checked 2026-11-17. **Active** at this check: the repository is public, not archived, and its default branch was pushed 2026-11-01; 13 stars, MIT, zero open issues. This records observed repository activity, not a promise of maintenance or release cadence.

- [Upstream README](https://raw.githubusercontent.com/numbpill3d/can-playground/master/README.md)
- [Repository metadata](https://api.github.com/repos/numbpill3d/can-playground)

## Related

- [CANarchy](canarchy.md)
- [Security in automotive bus systems](security-in-automotive-bus-systems.md)
- [CAN Lab](canlab.md)
- [Cangaroo](cangaroo.md)
- [cantools](cantools.md)
- [OBDium](obdium.md)
- [DBC as the CAN semantic layer](concepts/dbc-semantic-layer.md)
