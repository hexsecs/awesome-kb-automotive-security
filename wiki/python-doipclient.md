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
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Pure Python DoIP (ISO 13400) client that plugs into udsoncan as a transport layer for diagnostics over automotive Ethernet."
related:
  - udsoncan
  - uds
  - doip-sim-ecu-dsl
  - autofuze
  - scapy
  - doip
  - diagnostic-service-abuse
  - python-can-isotp
license: "MIT"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/jacobschaer/python-doipclient"
    retrieved: 2026-10-31
  - url: "https://python-doipclient.readthedocs.io/en/latest/"
    retrieved: 2026-10-31
facets: [diagnostics, doip, ethernet, tools, standards]
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

The [API reference](https://python-doipclient.readthedocs.io/en/latest/),
checked with the repository on 2026-11-17, separates network location from
diagnostic identity: `DoIPClient(ecu_ip_address, ecu_logical_address)`
needs both. Discovery returns an address and announcement object, from
which the caller obtains the logical address. IPv4 and IPv6 are supported;
`client_ip_address` selects the source address when a machine has several
network interfaces. The tester also has its own configurable logical
address. Routing activation normally happens during construction and can
be disabled or explicitly requested with a chosen activation type.

At the lower API level, `send_diagnostic()` accepts raw UDS bytes and
`receive_diagnostic()` returns a `bytearray`; DoIP negative
acknowledgements raise `IOError`, while a missing diagnostic response can
raise `TimeoutError`. These are transport outcomes, distinct from UDS
negative responses interpreted by udsoncan. In the higher-level workflow,
wrap the client in `DoIPClientUDSConnector`, pass that connection to
udsoncan's `Client`, and supply the vehicle-specific service configuration
there. After an ECU reset, allow the ECU to restart before reconnecting
and reactivating routing. Close the DoIP socket explicitly, or configure
the connector to close it with the UDS client.

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

This is a client-side transport, not an ECU simulator, a complete UDS
service implementation or a source of OEM security algorithms and DID
codecs. Successful discovery and routing activation do not establish that
the ECU authorises a privileged diagnostic service.

## Related

- [udsoncan](udsoncan.md) — the client it was built to carry.
- [py-uds](uds.md) — message-level UDS work over the same transports.
- [doip-sim-ecu-dsl](doip-sim-ecu-dsl.md) — a programmable server-side
  test double for exercising client responses without a vehicle.
- [DoIP moves diagnostics onto the network](concepts/doip.md)
- [Diagnostic-service abuse](concepts/diagnostic-service-abuse.md) — the
  service/session permission boundary remains above the Ethernet transport.
