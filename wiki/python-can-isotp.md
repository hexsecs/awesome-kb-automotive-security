---
uid: 01a19d3c-afc6-7e42-9e30-adc7d5647e70
title: "python-can-isotp"
summary: "ISO-TP (ISO 15765) transport for Python on top of python-can or Linux SocketCAN, the segmentation layer that UDS and OBD-II diagnostics run over."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/pylessard/python-can-isotp"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "ISO-TP (ISO 15765) transport for Python on top of python-can or Linux SocketCAN, the segmentation layer that UDS and OBD-II diagnostics run over."
related: [python-can, savvycan, caringcaribou]
license: MIT
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/pylessard/python-can-isotp"
    retrieved: 2026-10-31
  - url: "https://can-isotp.readthedocs.io"
    retrieved: 2026-10-31
---

ISO-TP (ISO 15765) transport for Python on top of python-can or Linux SocketCAN, the segmentation layer that UDS and OBD-II diagnostics run over.

## What it is

A Python implementation of the ISO-TP (ISO 15765-2) transport protocol,
MIT-licensed, from the `pylessard/python-can-isotp` repository. Current
documentation is the v2.x series.

## How it works

Two layers: a pure-Python user-space stack that may or may not be coupled
to [python-can](python-can.md), and a simplified wrapper around the Linux
SocketCAN ISO-TP kernel module. In v2, the transport layer's timing runs
in an internal thread (no periodic `process()` calls), the CAN receive
function is expected to be blocking, and blocking sends let a UDS layer
manage its P2/P2* versus P6 timeouts properly. `CanStack` variants
include `NotifierBasedCanStack`, which consumes frames via python-can's
Notifier instead of draining the receive queue itself (fixing starvation
of other modules); asymmetric TX/RX addressing and generator-based
sending for large payloads are supported.

## Where it fits

Building UDS and OBD-II diagnostic clients in Python — anywhere payloads
exceed one CAN frame and segmentation, flow control, and reassembly are
needed. It is the layer under the diagnostic workflows in
[CaringCaribou](caringcaribou.md) and the UDS tooling in the Diagnostic
Tools section, and pairs with python-can backends or the kernel module on
Linux. The security relevance is direct: UDS services — including
SecurityAccess — reach ECUs over this transport; see
[UDS seed/key](concepts/uds-seed-key.md).

## Limits and notes

v2 has documented breaking API changes from v1 (parameters renamed or
removed, `isotp.socket` timeout behaviour changed, the error handler is
now called from a different thread). Non-blocking receive functions are
possible, but the stack is then throttled by sleeps, "possibly degrading
overall timing" (a busy-wait option exists for more precise timing). The
kernel-module path is Linux/SocketCAN-only by definition; the user-space
stack is the portable option.

## Related

- [python-can](python-can.md) — the bus layer underneath.
- [SavvyCAN](savvycan.md) — GUI analysis, including UDS scanning.
- [CaringCaribou](caringcaribou.md) — diagnostics-driven exploration tool.
