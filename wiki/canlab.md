---
title: "CanLab"
summary: "PyQt6 desktop application for offline CAN capture reverse engineering, combining automated counter and checksum detection with entropy-based signal boundary…"
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/Sherin-SEF-AI/CanLab"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "PyQt6 desktop application for offline CAN capture reverse engineering, combining automated counter and checksum detection with entropy-based signal boundary analysis, a visual DBC builder, and UDS/OBD-II/J1939/XCP/DoIP diagnostic support."
related: [savvycan, cantools, opendbc]
license: MIT
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/Sherin-SEF-AI/CanLab"
    retrieved: 2026-10-31
---

PyQt6 desktop application for offline CAN capture reverse engineering, combining automated counter and checksum detection with entropy-based signal boundary analysis, a visual DBC builder, and UDS/OBD-II/J1939/XCP/DoIP diagnostic support.

## What it is

A PyQt6 desktop "workstation" for reverse-engineering CAN captures, with
CLI and MCP-server front ends over the same analysis. A single-author
project by Sherin Joseph Roy, MIT-licensed, and self-described as beta.

## How it works

An offline-first workflow in five workspaces (CAPTURE, EXPLORE, DETECT,
DEFINE, BUS; 16 tabs): load a capture → automated detection proposes
counters, checksums (with algorithm identification), and entropy-based
signal boundaries → define signals in a visual DBC builder that *verifies
definitions against real frames* → export DBC, openpilot, and Wireshark
dissectors. It is built on [python-can](python-can.md) and
[cantools](cantools.md), holds frames in a capped ring buffer, and also
speaks UDS/ISO-TP/J1939/OBD-II/XCP/DoIP. All transmit paths — inject,
replay, fuzz, gateway, diagnostics — route through one gated function.

## Where it fits

Turning an unknown capture into a verified DBC, especially where counter
and checksum structure is the hard part of the reverse-engineering
problem. [SavvyCAN](savvycan.md) is the established GUI for the same
capture-first workflow without the automated detection layer.

## Limits and notes

The README's safety section is unusually explicit: use CanLab **only on
isolated bench setups** (`vcan0`, benchtop ECU, lab hardware) — injecting
on a live vehicle bus "can interfere with braking, steering and airbag
systems." Guards include a first-launch warning, a global ARM TX switch
disarmed by default (disarming halts in-flight fuzz/replay), and a
blocked-ID list refused even when armed. Its limitations section is
equally plain: the analysis is heuristic — it suggests candidates, and its
confidence is a match fraction, not proof; it is not validated across many
vehicles; CAN FD was tested only on a virtual bus; diagnostics were tested
against scripted responders, not a real ECU; and the MCP server is
unauthenticated unless a token is set, so keep it on loopback.

## Related

- [SavvyCAN](savvycan.md) — its sniffer/GVRET behaviour follows SavvyCAN's.
- [cantools](cantools.md) — the DBC library in its stack.
- [opendbc](opendbc.md) — source of checksum algorithms it adapts.
