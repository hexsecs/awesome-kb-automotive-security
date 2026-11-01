---
title: "OpenSOVD Classic Diagnostic Adapter"
summary: "Eclipse OpenSOVD bridge in Rust that translates SOVD (ISO 17978) requests into UDS over DoIP for legacy ECUs, with a security plugin architecture."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/eclipse-opensovd/classic-diagnostic-adapter"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Eclipse OpenSOVD bridge in Rust that translates SOVD (ISO 17978) requests into UDS over DoIP for legacy ECUs, with a security plugin architecture."
related: [odxtools, udsoncan, ecubus-pro]
license: "Apache-2.0"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/eclipse-opensovd/classic-diagnostic-adapter"
    retrieved: 2026-10-31
---

Eclipse OpenSOVD bridge in Rust that translates SOVD (ISO 17978) requests into UDS over DoIP for legacy ECUs, with a security plugin architecture.

## What it is

The Classic Diagnostic Adapter (CDA) of the Eclipse OpenSOVD project:
a Rust service that bridges legacy diagnostics to the SOVD
(Service-Oriented Vehicle Diagnostics) architecture. Apache-2.0.

## How it works

The CDA translates SOVD REST calls into UDS-over-DoIP exchanges with
real ECUs, driven by MDD diagnostic databases produced from ODX via the
separate eclipse-opensovd odx-converter. In the ODX-to-SOVD mapping, a
DiagLayerContainer short name becomes a component path
(`/vehicle/v15/components/<ecu>`); services map by SID — 0x22/0x2E
(Read/WriteDataByIdentifier) to `/data` (the varcoding functional class
to `/configurations`), 0x31 RoutineControl to `/operations` — with
configurable affix stripping of service names. It is a modular Cargo
workspace (CAN, DoIP, and UDS communication crates, a transport router,
security/lock-priority plugins), serves a REST API on port 20002 with
Swagger UI, and selects its DoIP variant via `--protocol-name`
(DoIP-DOBT in-vehicle by default, plain DoIP offboard). Stated goals:
async I/O performance, low footprint, fast startup.

## Where it fits

Exposing classic UDS ECUs behind a modern SOVD/REST interface — on a
gateway ECU or a test bench — where an MDD/ODX description of the ECUs
exists. It is the serving counterpart to [odxtools](odxtools.md)'s
parsing, and the bridge between this section and the
service-oriented diagnostics world.

## Limits and notes

The README's prerequisites require at least one `.mdd` file before the
adapter can run. The repository has 0 releases and 0 tags — there is no
stable release yet; it builds from source (Rust ≥ 1.88 / Bazel).
Status `active`, but pre-release.

## Related

- [odxtools](odxtools.md) — the ODX parsing layer its databases derive from.
- [udsoncan](udsoncan.md) — UDS client semantics it re-exposes over REST.
- [EcuBus-Pro](ecubus-pro.md) — interactive diagnostic tooling across the same protocols.
