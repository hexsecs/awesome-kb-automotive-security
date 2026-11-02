---
uid: 01a19d3c-af4c-7ce0-9420-9fe597997417
title: "cannelloni"
summary: "Tunnels SocketCAN interfaces over UDP, TCP, or SCTP, bridging a vehicle bus to a remote analysis machine and letting bench setups share one physical CAN…"
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/mguentner/cannelloni"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Tunnels SocketCAN interfaces over UDP, TCP, or SCTP, bridging a vehicle bus to a remote analysis machine and letting bench setups share one physical CAN adapter."
related: [candevstudio, can-utils]
license: GPL-2.0
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/mguentner/cannelloni"
    retrieved: 2026-10-31
---

Tunnels SocketCAN interfaces over UDP, TCP, or SCTP, bridging a vehicle bus to a remote analysis machine and letting bench setups share one physical CAN adapter.

## What it is

A small C++11 daemon that tunnels SocketCAN frames over Ethernet (UDP,
TCP, or SCTP), by Maximilian Güntner. GPL-2.0. Also described in a 2015
IEEE SIES paper.

## How it works

One instance runs per machine, each bound to a local (often virtual) CAN
interface; frames are aggregated into Ethernet frames — multiple CAN
frames per packet, IPv4/IPv6, CAN FD where the interface supports it.
UDP/SCTP buffer until the buffer fills or a timeout fires (default
100 ms, with per-ID timeout files for high-priority frames); TCP sends
immediately with no buffering or sorting. An optional sort orders frames
by ID inside each Ethernet frame so high-priority frames hit the
receiving bus first. Undeliverable frames are dropped after a staleness
timeout (default 2 s) instead of flushing a stale backlog when a broken
bus recovers.

## Where it fits

Remote and bench access to a physical bus — the [CANdevStudio](candevstudio.md)
no-hardware setup uses it — sharing one physical adapter across machines,
and virtualised embedded setups. Pair with [can-utils](can-utils.md)'s
`cangw` when the tunnelled interface needs pre-filtering.

## Limits and notes

The README's "Important Usage Notice" is prominent: **not suited for
production**; use only where packet loss is tolerable; there is **no
guarantee frames arrive at all, or in the right order**, on any transport.
A `vcan` end can vastly outpace a physical ≤1 Mbit/s bus — the README
advises rate-limiting the vcan interface, which adds latency. There is no
built-in filtering: bridge a pre-filtered `vcan` via `cangw` instead.

## Related

- [CANdevStudio](candevstudio.md) — ships a cannelloni plugin for remote simulation.
- [can-utils](can-utils.md) — `cangw` provides the filtering cannelloni lacks.
