---
uid: 01a19d3c-afc7-7e1d-a9f7-5a36949840ea
title: "python-doipclient"
summary: "Pure Python DoIP (ISO 13400) client that plugs into udsoncan as a transport layer for diagnostics over automotive Ethernet."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/jacobschaer/python-doipclient"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Pure Python DoIP (ISO 13400) client that plugs into udsoncan as a transport layer for diagnostics over automotive Ethernet."
related: [udsoncan, uds]
license: "MIT"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/jacobschaer/python-doipclient"
    retrieved: 2026-10-31
  - url: "https://python-doipclient.readthedocs.io/en/latest/"
    retrieved: 2026-10-31
---

Pure Python DoIP (ISO 13400) client that plugs into udsoncan as a transport layer for diagnostics over automotive Ethernet.

## What it is

A pure-Python DoIP client (ISO 13400) by jacobschaer, for diagnostics
over automotive Ethernet. MIT-licensed. Its stated primary use case is
to serve as the transport layer for [udsoncan](udsoncan.md).

## How it works

It implements "the majority of ISO-13400 (2019) from the perspective of
a short-lived synchronous client." Discovery works via a Vehicle
Identification Request (`get_entity()`) or by awaiting the power-up
Vehicle Announcement broadcast (`await_vehicle_announcement()`); then
routing activation, entity status, alive check, diagnostic power mode,
and raw diagnostic payload send/receive over TCP (UDP for discovery),
on port 13400 (3496 for TLS). `DoIPClientUDSConnector` adapts it to
udsoncan's `Client`; a `reconnect()` supports post-ECU-reset flows,
with an `auto_reconnect_tcp` option.

## Where it fits

Giving a Python UDS stack — above all udsoncan — a DoIP/Ethernet
transport to a modern ECU. It is the Ethernet counterpart to
[python-can-isotp](python-can-isotp.md)'s CAN transport role.

## Limits and notes

The docs state that only the majority of ISO 13400-2:2019 is
implemented, and that parts of the spec requiring threaded operation to
maintain time-based state are not maintained ("in practice these are
rarely important"); the TLS option (`use_secure`, port 3496) is
documented as "Untested." No vehicle-safety warning is stated in the
checked sources.

## Related

- [udsoncan](udsoncan.md) — the client it was built to carry.
- [py-uds](uds.md) — message-level UDS work over the same transports.
