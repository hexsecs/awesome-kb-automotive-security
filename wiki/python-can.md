---
uid: 01a19d3c-afc7-7506-a1c5-08c2ba14e1f4
title: "python-can"
summary: "Python library providing a common interface over many CAN hardware backends with CAN FD support and logging to ASC, BLF, MF4, TRC, CSV, and SQLite."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/hardbyte/python-can"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python library providing a common interface over many CAN hardware backends with CAN FD support and logging to ASC, BLF, MF4, TRC, CSV, and SQLite."
related: [python-can-isotp, cantools, can-utils]
license: LGPL-3.0
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/hardbyte/python-can"
    retrieved: 2026-10-31
---

Python library providing a common interface over many CAN hardware backends with CAN FD support and logging to ASC, BLF, MF4, TRC, CSV, and SQLite.

## What it is

The `can` Python package: hardware-agnostic CAN access for CPython/PyPy
on Linux, macOS, and Windows, LGPL-3.0, hosted at `hardbyte/python-can`.
It is the de-facto base layer much of this section — and much of the
Python CAN ecosystem — is built on.

## How it works

`can.Bus(interface=…, channel=…)` instantiates a backend-specific
`BusABC`; `can.Message` carries arbitration ID, data, and flags, with
normal and extended IDs and CAN FD support. Sending can be one-shot or
periodic; reception is by iteration/`recv()` or via `can.Notifier`, which
runs a thread dispatching frames to `Listener`s (built-ins include
`Printer`, `Logger`, and `BufferedReader`). Log reading, writing, and
playback cover ASC, BLF, MF4, TRC, CSV, SQLite, and canutils formats.
Filtering is done in kernel or hardware where the interface supports it,
configuration can come from files or environment variables, and CLI tools
(logger, viewer, player) are bundled.

## Where it fits

Writing portable Python CAN tooling, test automation, and logging/replay
pipelines that must survive a change of CAN adapter. In this KB it is the
transport under [CANarchy](canarchy.md), [CanLab](canlab.md), and
[python-can-isotp](python-can-isotp.md), and the library counterpart to
[can-utils](can-utils.md) on SocketCAN systems.

## Limits and notes

No safety warnings appear in the README. Two documented caveats from the
project's own docs: virtual buses do not model real CAN arbitration or
throughput throttling, and the `udp_multicast` bus gives up guaranteed
delivery and message ordering.

## Related

- [python-can-isotp](python-can-isotp.md) — the ISO-TP layer built on it.
- [cantools](cantools.md) — the usual pairing for DBC decode/encode.
- [can-utils](can-utils.md) — the C command-line equivalent on Linux.
