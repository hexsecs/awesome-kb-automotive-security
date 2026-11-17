---
uid: 01a19d3c-af34-7c4e-a339-d0b0e969bb9b
title: "AutoPi"
summary: "Open-source core software for the AutoPi dongle, a Raspberry Pi-based OBD-II device for vehicle diagnostics, CAN bus data collection, and automotive IoT…"
type: entity
category: "Diagnostic Tools"
url: "https://github.com/autopi-io/autopi-core"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source core software for the AutoPi dongle, a Raspberry Pi-based OBD-II device for vehicle diagnostics, CAN bus data collection, and automotive IoT applications."
related:
  - can-utils
  - caringcaribou
  - udsoncan
  - linusbconverter
  - external-attack-surface
  - dbc-semantic-layer
  - diagnostic-service-abuse
license: "Apache-2.0"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/autopi-io/autopi-core"
    retrieved: 2026-10-31
  - url: "http://docs.autopi.io"
    retrieved: 2026-11-17
  - url: "https://docs.autopi.io/core/"
    retrieved: 2026-11-17
facets: [can, diagnostics, tools]
---

Open-source core software for the AutoPi dongle, a Raspberry Pi-based OBD-II device for vehicle diagnostics, CAN bus data collection, and automotive IoT applications.

## What it is

The on-device software stack for the AutoPi OBD dongle (part of the
AutoPi cloud platform), by the autopi-io organisation. Apache-2.0. The
repository's stated purpose is to expose what commands exist on the
device and how they work.

## How it works

It runs on a Raspberry Pi (Zero or 3) under a lightly modified
Raspbian, and is built on SaltStack: the device runs as a salt minion
against a (possibly virtual) salt master, which is also how it is
provisioned and managed. Full documentation lives at docs.autopi.io,
linked from the README; command-level detail lives there rather than in
the repository.

The [Core introduction](https://docs.autopi.io/core/), checked on
2026-11-17, describes two complementary layers. Background managers own
ongoing work and hardware communication: the OBD manager handles the
vehicle's OBD-II connection, while the Tracking manager collects GNSS
positioning data. Salt execution modules expose commands grouped by
function; the OBD module supplies vehicle-communication commands and EC2X
manages the Quectel cellular/GNSS modem. Commands can be invoked directly
or incorporated into automated workflows, rather than every application
opening hardware independently.

In a deployment workflow, configure the device and its data-collection
tasks, let Core handle local communication and edge logic, and use Cloud
for central device management and automations. The
[platform documentation](http://docs.autopi.io) describes raw and decoded
CAN/CAN-FD/J1939/OBD-II logging, REST and MQTT integrations, OTA management
and on-device Docker workloads. These are platform capabilities, not a
promise that every AutoPi dongle exposes every bus or runs this repository.
For example, the current Core guide covers TMU CM4 and CAN-FD Pro
(including its IP67 variant), and explicitly excludes AutoPi Mini because
it does not run Core. That newer hardware scope should be distinguished
from the Zero/3-era description retained in the repository README.

## Where it fits

Building customisable car projects and telematics on the AutoPi dongle
with an open, inspectable on-device stack — the platform play in this
section, where [can-utils](can-utils.md) is the raw-tool play and
[CaringCaribou](caringcaribou.md) the exploration play on similar
Pi-class hardware.

## Limits and notes

No limits or safety warnings are stated in the checked sources. The
README itself notes the getting-started guide is still "we are working
on" it — documentation is incomplete by the project's own account.

That caveat applies to the repository's guide, not to an absence of
published documentation: the README's `http://docs.autopi.io` link
redirected (301) to `https://docs.autopi.io/` and served the platform
documentation on 2026-11-17. The canonical repository URL is unchanged
and was also reachable. Core is the device-side component; publishing its
source does not make this repository a standalone replacement for the
whole hosted Cloud platform. Treat adapter, device generation and vehicle
protocol support as deployment prerequisites, not as interchangeable
features of a generic Raspberry Pi installation.

## Related

- [can-utils](can-utils.md) — the SocketCAN utilities such devices expose.
- [CaringCaribou](caringcaribou.md) — Pi-based CAN exploration, the security-side neighbour.
- [udsoncan](udsoncan.md) — diagnostics over the dongle's data.
- [The vehicle's external attack surface: remote entry and the telematics pivot](concepts/external-attack-surface.md)
- [DBC as the CAN semantic layer](concepts/dbc-semantic-layer.md) — raw
  logging and meaningful signal interpretation are separate jobs.
- [Diagnostic-service abuse](concepts/diagnostic-service-abuse.md) — remote
  orchestration does not remove the privilege boundary around vehicle commands.
