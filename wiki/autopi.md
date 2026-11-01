---
title: "AutoPi"
summary: "Open-source core software for the AutoPi dongle, a Raspberry Pi-based OBD-II device for vehicle diagnostics, CAN bus data collection, and automotive IoT…"
type: entity
category: "Diagnostic Tools"
url: "https://github.com/autopi-io/autopi-core"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source core software for the AutoPi dongle, a Raspberry Pi-based OBD-II device for vehicle diagnostics, CAN bus data collection, and automotive IoT applications."
related: [can-utils, caringcaribou, udsoncan]
license: "Apache-2.0"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/autopi-io/autopi-core"
    retrieved: 2026-10-31
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

## Related

- [can-utils](can-utils.md) — the SocketCAN utilities such devices expose.
- [CaringCaribou](caringcaribou.md) — Pi-based CAN exploration, the security-side neighbour.
- [udsoncan](udsoncan.md) — diagnostics over the dongle's data.
