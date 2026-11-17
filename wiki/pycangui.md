---
uid: 01a1c4c6-ca22-7c29-8482-7221cc23f0a5
title: "pycangui"
summary: "Graphical CAN bus tool with live trace and plots, transmit, CANopen, UDS, J1939, and XCP/CCP support on any python-can adapter, with Python scripting and…"
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/davhodg/pycangui"
status: active
last_checked: 2026-11-17
created: 2026-11-10
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 67533a4
list_summary: "Graphical CAN bus tool with live trace and plots, transmit, CANopen, UDS, J1939, and XCP/CCP support on any python-can adapter, with Python scripting and simulated nodes."
related:
  - cancat
  - python-can
  - cangaroo
  - canarchy
  - uds
  - canalyzat0r
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-10
  - url: "https://github.com/davhodg/pycangui"
    retrieved: 2026-11-17
  - url: "https://raw.githubusercontent.com/davhodg/pycangui/master/README.md"
    retrieved: 2026-11-17
  - url: "https://api.github.com/repos/davhodg/pycangui"
    retrieved: 2026-11-17
---

Graphical CAN bus tool with live trace and plots, transmit, CANopen, UDS, J1939, and XCP/CCP support on any python-can adapter, with Python scripting and simulated nodes.

## What it is

pycangui is a Python 3.12+ desktop application (PySide6/Qt, Apache-2.0) that puts a scriptable GUI on top of [python-can](python-can.md). It is published on PyPI and as a Windows installer, or runnable from a git clone with a self-managed `.venv`. At this check the repository had 7 stars, 10 open issues and a default-branch push on 2026-11-16; the upstream README notes that its release badge reads "no releases found" until the first release, so treat the install paths as the availability signal rather than a release number.

## How it works

- **Adapters and trace** — any python-can interface (PEAK, Vector, Kvaser, IXXAT, ETAS, Intrepid, SocketCAN, SLCAN, gs_usb, UDP multicast, virtual, and others); multi-channel live trace on one timebase including CAN FD; recording to six log formats and replay onto a bus. Two distinct filters: a channel acceptance filter that drops frames before arrival, and a trace filter that hides without discarding.
- **Transmit and signals** — raw frames, DBC messages edited by signal, or CANopen RPDOs, with rolling counters and XOR/sum/CRC-8/CRC-16 or custom checksums; DBC/CANopen/XCP/CCP values into Signals and Plot, with CSV export and MDF/MF4 import.
- **Higher-layer support** — CANopen master (object dictionary, PDO configuration, EMCY, LSS, SYNC, DCF compare, DBC export of PDOs/heartbeats/emergencies), UDS over ISO-TP (sessions, security access, DIDs, DTCs, routines, firmware transfer in either direction), J1939 (address claims, DM1 faults, TP.BAM/TP.CM multi-packet, SPN decode), XCP and CCP over CAN with A2L seed/key and measurement/characteristic access.
- **Extensibility** — Python hooks with hot reload, replaceable CAN interface / ISO-TP transport / XCP-CCP engines, a live console, zip-installed plugins (CANopen firmware download and CiA 402 motor control ship with it), Python simulated nodes and inter-channel gateways, and per-device workspaces holding hooks, EDS files, databases and layout.

An unusual input path: frames decoded by [pyscopegui](https://github.com/davhodg/pyscopegui) from an oscilloscope's channels arrive over UDP multicast and are traced like adapter frames.

## Where it fits

pycangui is the Python-native option for a bench that needs scripting and protocol work in the same window: hooks, replaceable components and simulated nodes make it a good fit when the session is itself a test harness. It overlaps [CANExplorer](canexplorer.md) in breadth but differs in emphasis — pycangui's differentiators are the hot-reload hook system, custom panes built from object dictionaries, and scope-decoded input. For UDS sessions, see [UDS](uds.md); for the underlying adapter abstraction, [python-can](python-can.md); for comparison, [CANalyzat0r](canalyzat0r.md), [Cangaroo](cangaroo.md) and [CANcat](cancat.md).

## Limits and safety notes

The upstream safety notice is explicit and worth keeping: joining at the wrong bitrate makes controllers signal errors on every frame, and transmitting, replaying, writing parameters or downloading firmware change what equipment does, sometimes irreversibly. macOS passes the same test suite on Intel and Apple silicon but has not been exercised on real CAN hardware. On Linux, Qt needs `libxcb-cursor0`; adapter vendor drivers are not bundled. The optional MDF/MF4 reader cannot be installed on Python 3.15 at this check because a dependency lacks a download, and the Windows installer is unsigned (SmartScreen warning; the README points to the pip install as the alternative). Feature descriptions come from the upstream README; no hardware execution was performed.

## Status and sources

Checked 2026-11-17. **Active** at this check: public, not archived, default branch pushed 2026-11-16, PyPI package present, Apache-2.0, 7 stars and 10 open issues. Activity does not imply a stable release line.

- [Upstream README](https://raw.githubusercontent.com/davhodg/pycangui/master/README.md)
- [Repository metadata](https://api.github.com/repos/davhodg/pycangui)
- [Manual](https://github.com/davhodg/pycangui/blob/master/pycangui/help/manual.md)

## Related

- [CANcat](cancat.md)
- [python-can](python-can.md)
- [Cangaroo](cangaroo.md)
- [CANarchy](canarchy.md)
- [UDS](uds.md)
- [CANalyzat0r](canalyzat0r.md)
