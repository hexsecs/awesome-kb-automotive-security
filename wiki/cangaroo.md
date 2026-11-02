---
uid: 01a19d3c-af48-762b-8865-0cb932783113
title: "CANgaroo"
summary: "Open-source CAN bus analyzer for Linux and Windows with DBC and LDF decoding, CAN FD, Python scripting, SocketCAN, PEAK, Kvaser, Vector, and candlelight…"
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/Schildkroet/CANgaroo"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source CAN bus analyzer for Linux and Windows with DBC and LDF decoding, CAN FD, Python scripting, SocketCAN, PEAK, Kvaser, Vector, and candlelight interfaces, and Vector ASC, MDF4, candump, and PCAP export."
related: [savvycan, canmatrix, can-utils]
license: GPL-2.0
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/Schildkroet/CANgaroo"
    retrieved: 2026-10-31
---

Open-source CAN bus analyzer for Linux and Windows with DBC and LDF decoding, CAN FD, Python scripting, SocketCAN, PEAK, Kvaser, Vector, and candlelight interfaces, and Vector ASC, MDF4, candump, and PCAP export.

## What it is

A Qt 6 open-source CAN bus **analyser** for Linux and Windows. This
repository is a fork (GitHub marks it as such): the original is by Hubert
Denkmair, with further development by Ethan Zonca, WeAct Studio,
Schildkroet (this repo), Wikilift, and OpenAutoDiagLabs. GPL-2.0.

## How it works

A measurement-centric GUI: pick an interface, run a measurement, and
decode live CAN/CAN-FD/LIN frames against multiple loaded DBC (CAN) or
LDF (LIN) files; graph signals as time series, scatter plots, and gauges;
filter live; log and export. The interface matrix is wide: SocketCAN,
PEAK PCAN, Kvaser, Vector (Windows), TinyCAN, Candlelight/CANable/gs_usb,
SLCAN, CANblaster (UDP), and GrIP, plus LIN adapters. Extras include
embedded Python scripting (pybind11) to send, receive, and decode; a CAN
gateway forwarding between two interfaces with per-message filters; trace
replay (ASC, candump, PCAP/PCAPng); and exports to ASC, MDF4, candump, and
PCAP(NG). The repo also ships STM32G4 reference adapter firmware.

## Where it fits

Interactive live-bus analysis and decoding on cheap gs_usb/CANable-class
hardware; mixed CAN+LIN benches; and scripted measurement automation. Its
closest neighbour is [SavvyCAN](savvycan.md); CANgaroo leans further into
measurement and graphing, SavvyCAN into reverse engineering.

## Limits and notes

Configuring SocketCAN interfaces needs `CAP_NET_ADMIN` (a polkit rule or
password prompt handles it; not needed if the interface is configured by
the OS). Several drivers are build-time options needing vendor SDKs or
DLLs (PEAK, Kvaser, Vector XL). The README carries an explicit "use
entirely at your own risk" disclaimer.

## Related

- [SavvyCAN](savvycan.md) — the other cross-platform analysis GUI.
- [canmatrix](canmatrix.md) — CANgaroo's README points ARXML users to its converter.
- [can-utils](can-utils.md) — the command-line base on Linux benches.
