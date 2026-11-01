---
title: "udsoncan"
summary: "Python implementation of the ISO 14229 UDS protocol covering session control, security access, data identifiers, and routine control."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/pylessard/python-udsoncan"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python implementation of the ISO 14229 UDS protocol covering session control, security access, data identifiers, and routine control."
related: [python-can-isotp, python-doipclient, python-can, uds-seed-key]
license: "MIT"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/pylessard/python-udsoncan"
    retrieved: 2026-10-31
  - url: "https://udsoncan.readthedocs.io/en/latest/"
    retrieved: 2026-10-31
---

Python implementation of the ISO 14229 UDS protocol covering session control, security access, data identifiers, and routine control.

## What it is

A Python 3 implementation of the UDS protocol (ISO 14229): a client
library for building and interpreting UDS payloads and detecting
malformed messages, by pylessard. MIT-licensed.

## How it works

Application layer only: a `Client` talks through a pluggable
`Connection` object — implement `BaseConnection`, or use a built-in.
Built-in connections include `IsoTPSocketConnection` (Linux ISO-TP
socket via can-isotp), `PythonIsoTpConnection` (can-isotp coupled with
python-can), `SyncAioIsotpConnection`, a raw `SocketConnection`, a
`QueueConnection` (in-process queues, for testing), and a
`J2534Connection` (Windows J2534 DLL). DoIP is reached through
[python-doipclient](python-doipclient.md)'s `DoIPClientUDSConnector`.
Client methods cover the standard services — session control,
`unlock_security_access` (0x27; see
[UDS seed/key](concepts/uds-seed-key.md)), read/write data by identifier
with config-defined codecs, ECU reset — and negative or invalid
responses raise typed exceptions.

## Where it fits

Writing a production Python diagnostic tester or test script against an
ECU over CAN/ISO-TP, with DoIP or J2534 available by swapping the
connection. It is the session layer most other Python tooling in this
section either uses or is compared against; [py-uds](uds.md) works one
layer down at message/packet level, and the C library
[iso14229](iso14229.md) covers the embedded side.

## Limits and notes

Its docs state plainly: "this project does not implement any
communication protocol below the UDS layer" — you supply the transport.
The docs also warn that the `SyncAioIsotpConnection` rests on aioisotp,
"no longer actively maintained by its author," with known stream
issues. No vehicle-safety warning is stated in the checked sources.

## Related

- [python-can-isotp](python-can-isotp.md) — its usual ISO-TP transport on Linux.
- [python-doipclient](python-doipclient.md) — the DoIP transport built for it.
- [python-can](python-can.md) — the CAN layer beneath the PythonIsoTp connection.
- [UDS seed/key](concepts/uds-seed-key.md) — what its 0x27 client calls into.
