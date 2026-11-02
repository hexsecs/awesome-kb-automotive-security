---
title: "odxtools"
summary: "Python toolkit for parsing ODX/PDX (ISO 22901) diagnostic databases and encoding, decoding, and snooping ECU diagnostic sessions."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/mercedes-benz/odxtools"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python toolkit for parsing ODX/PDX (ISO 22901) diagnostic databases and encoding, decoding, and snooping ECU diagnostic sessions."
related: [opensovd-classic-diagnostic-adapter, udsoncan, ecubus-pro]
license: "MIT"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/mercedes-benz/odxtools"
    retrieved: 2026-10-31
---

Python toolkit for parsing ODX/PDX (ISO 22901) diagnostic databases and encoding, decoding, and snooping ECU diagnostic sessions.

## What it is

A Python library and CLI utilities for working with ECU diagnostic
descriptions in the ODX standard (ASAM / ISO 22901), by Mercedes-Benz.
MIT-licensed.

## How it works

odxtools parses and internalises ODX/PDX diagnostic databases, then
encodes and decodes diagnostic request/response payloads "in a pythonic
manner" against the database — service objects, CAN receive/send ID
lookup, response decoding against the coded request. CLI subcommands:
`list`, `browse`, `snoop` (live decoding of a diagnostic session),
`find`, `decode`, and `compare` (diffing two database or
diagnostic-layer versions). The package is the description/codec layer;
live ECU interaction means tapping the vehicle's CAN or Ethernet bus
with separate tooling. A "non-strict" mode loads non-conforming
databases with results explicitly undefined.

## Where it fits

Programmatic, database-driven UDS work in Python: exploring an ECU's
services from a PDX file, generating correctly coded requests, decoding
traces, and building tester or calibration tooling on top of ODX data.
It is the description layer beneath tools like the
[OpenSOVD Classic Diagnostic Adapter](opensovd-classic-diagnostic-adapter.md),
whose MDD databases are produced from ODX.

## Limits and notes

The README itself states that some listed use cases are "currently
rather aspirational," and that non-strict mode ignores spec-conformance
problems with undefined results; by default odxtools raises exceptions
when it suspects it cannot fulfil an operation correctly.

## Related

- [OpenSOVD Classic Diagnostic Adapter](opensovd-classic-diagnostic-adapter.md) — serves ODX-derived data over SOVD/REST.
- [udsoncan](udsoncan.md) — the session-level UDS client this complements.
- [EcuBus-Pro](ecubus-pro.md) — interactive counterpart for diagnostic sessions.
