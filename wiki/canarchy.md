---
uid: 01a19d3c-af42-746e-a703-76c70cb65e7b
title: "CANarchy"
summary: "Stream-first CAN and J1939 toolkit that emits structured JSONL for automation, with live capture, DBC/ARXML/KCD decoding, J1939 PGN/SPN and DM1 fault…"
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/hexsecs/canarchy"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-11-14
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Stream-first CAN and J1939 toolkit that emits structured JSONL for automation, with live capture, DBC/ARXML/KCD decoding, J1939 PGN/SPN and DM1 fault parsing, UDS and DoIP support, constrained fuzzing, and an MCP server for agent-driven workflows."
related: [can-utils, cantools, python-can, pretty-j1939]
license: GPL-3.0
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/hexsecs/canarchy"
    retrieved: 2026-10-31
---

Stream-first CAN and J1939 toolkit that emits structured JSONL for automation, with live capture, DBC/ARXML/KCD decoding, J1939 PGN/SPN and DM1 fault parsing, UDS and DoIP support, constrained fuzzing, and an MCP server for agent-driven workflows.

## What it is

A CLI-first CAN/CAN-FD and J1939 toolkit for security research and
AI-agent use, by hexsecs (PyPI package `canarchy`, Python 3.11+). GPL-3.0.
hexsecs' own toolkit — it is also the project this KB's maintainer works on
directly, which is worth knowing when weighing this page's enthusiasm.

## How it works

The stable contract is a typed event schema: every command emits the same
JSON envelope as `--json`/`--jsonl`/`--text`, designed to be piped
(`| jq`) or consumed by an agent through the built-in MCP server. Live
transport rides on [python-can](python-can.md) backends (SocketCAN,
virtual, UDP multicast), plus a deterministic no-hardware "scaffold"
backend for trying the contract offline.

Command families: capture/stats/compare; DBC/ARXML/KCD decode-encode and
provider-backed DBC discovery and caching (via [cantools](cantools.md));
first-class J1939 — PGN/SPN decode from a bundled SAE catalog, transport
reassembly, DM1 fault parsing; UDS and DoIP diagnostic workflows;
reverse-engineering helpers (signal/counter/entropy ranking, anomaly
diffing against a baseline); and a full-screen TUI.

## Where it fits

Automation and agent-driven analysis; heavy-vehicle and J1939 work (SPN
lookups, DM1 faults) without dropping to raw IDs; capture diffing and
anomaly detection inside scripts and pipelines built on
[can-utils](can-utils.md) logs.

## Limits and notes

Active workflows are gated by a documented active-transmit safety model:
`--dry-run` is the safe planning path, and MCP active-transmit tools
require an explicit acknowledgement, so an agent cannot put frames on a
live bus by accident.

## Related

- [can-utils](can-utils.md) — the SocketCAN command-line base layer.
- [cantools](cantools.md) — the DBC engine CANarchy builds on.
- [python-can](python-can.md) — the transport library underneath.
- [pretty_j1939](pretty-j1939.md) — the other J1939-first tool in this section.
