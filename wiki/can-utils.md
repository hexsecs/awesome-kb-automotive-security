---
title: "can-utils"
summary: "Linux-CAN SocketCAN userspace utilities including cansniffer, candump, cansend, canplayer, and cangen for CAN bus analysis."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/linux-can/can-utils"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Linux-CAN SocketCAN userspace utilities including cansniffer, candump, cansend, canplayer, and cangen for CAN bus analysis."
related: [python-can, cannelloni, pretty-j1939]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/linux-can/can-utils"
    retrieved: 2026-10-31
---

Linux-CAN SocketCAN userspace utilities including cansniffer, candump, cansend, canplayer, and cangen for CAN bus analysis.

## What it is

The Linux-CAN project's userspace utilities for SocketCAN — the standard
command-line toolkit that ships with the Linux CAN subsystem, maintained
under the linux-can GitHub organisation.

## How it works

A suite of small single-purpose C programs over the kernel's SocketCAN
sockets, grouped by function:

- **Basic traffic** — candump, cansend, canplayer, cangen, cansequence,
  and cansniffer (which highlights payload differences between successive
  frames);
- **Network access** — canlogserver, bcmserver, socketcand;
- **Gatewaying** — cangw, configuring the in-kernel CAN gateway;
- **Measurement and test** — canbusload, canfdtest, canerrsim, and a
  bit-timing calculator;
- **ISO-TP** — isotpsend, isotprecv, isotpsniffer, isotpdump, isotpserver,
  isotpperf, isotptun;
- **J1939 / ISOBus** — j1939spy, j1939cat, j1939sr, an address-claim
  daemon, and an ISOBus file server;
- **Log conversion** — asc2log, log2asc, log2long; plus slcan
  line-discipline setup.

## Where it fits

Scripted capture, replay, and generation on any Linux bench — and the
candump log format it produces is the interchange format most other tools
in this section consume, including [python-can](python-can.md) pipelines
and [pretty_j1939](pretty-j1939.md) decoding. Remote benches pair it with
[cannelloni](cannelloni.md) tunnels.

## Limits and notes

Linux/SocketCAN only; there is no Windows or macOS path. The README states
no usage-safety guidance. Note that cangen generates random traffic by
design — it is an active-transmit tool, not a passive listener.

## Related

- [python-can](python-can.md) — the library form of the same SocketCAN world.
- [cannelloni](cannelloni.md) — tunnels SocketCAN interfaces over IP networks.
- [pretty_j1939](pretty-j1939.md) — decodes J1939 traffic from candump logs.
