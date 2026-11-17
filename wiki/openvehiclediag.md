---
uid: 01a1e6dc-fe7f-75c9-ba7d-460057a2c159
title: "OpenVehicleDiag"
summary: "Rust ECU diagnostics and reprogramming application over J2534 pass-through adapters and Linux SocketCAN, with UDS and KWP2000 sessions and a converter that…"
type: entity
category: "Diagnostic Tools"
url: "https://github.com/rnd-ash/OpenVehicleDiag"
status: maintenance
last_checked: 2026-11-17
created: 2026-11-15
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: a570090
list_summary: "Rust ECU diagnostics and reprogramming application over J2534 pass-through adapters and Linux SocketCAN, with UDS and KWP2000 sessions and a converter that turns Mercedes CBF diagnostic databases into its own JSON format."
related:
  - python-can-isotp
  - automotive-flash-bootloaders-exposing-automotive-ecu-updates
  - pq-flasher
  - uds
  - conescan
  - zephyr-reference-ecu
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-15
  - url: "https://github.com/rnd-ash/OpenVehicleDiag"
    retrieved: 2026-11-17
  - url: "https://raw.githubusercontent.com/rnd-ash/OpenVehicleDiag/main/README.md"
    retrieved: 2026-11-17
  - url: "https://api.github.com/repos/rnd-ash/OpenVehicleDiag"
    retrieved: 2026-11-17
facets: [can, diagnostics, tools]
---

Rust ECU diagnostics and reprogramming application over J2534 pass-through adapters and Linux SocketCAN, with UDS and KWP2000 sessions and a converter that turns Mercedes CBF diagnostic databases into its own JSON format.

## What it is

OpenVehicleDiag (OVD) is a Rust ECU diagnostic platform using the J2534-2 pass-through protocol and, on Linux, SocketCAN. The upstream README states its goal plainly: make a car's diagnostic functions explorable through an API so an ECU can be reprogrammed without a dealer-only tool, and identifies it as the author's university final-year project at the University of Reading. It is GPL-3.0, with 1,034 stars and 108 forks at this check — popularity far above the pace of recent development.

## How it works

The repository is split into three parts, per the README: `app_rust` is the diagnostic application, `CBFParser` converts Mercedes CBF diagnostic databases into OVD's own ECU JSON (format documented in `SCHEMA.md`), and `Common` is shared library code. That converter is the practical entry point: you supply a CBF database for the target ECU, convert it, and the application uses the resulting JSON to name and address diagnostic functions over a J2534-2 adapter or SocketCAN. The README describes the goal of ECU reprogramming but does not enumerate a supported-vehicle matrix or a verified protocol feature list; treat the CBF pipeline and the J2534/SocketCAN transports as the documented core, and verify a specific vehicle before assuming coverage.

## Where it fits

OVD is the open-source answer to "I have a pass-through cable and want diagnostic/reprogram access without the dealer tool", strongest where a CBF database exists. It pairs naturally with [UDS](uds.md) and the seed/key material in [UDS seed/key (SecurityAccess)](concepts/uds-seed-key.md), with [python-can-isotp](python-can-isotp.md) for the transport, and with bench targets such as [Zephyr reference ECU](zephyr-reference-ecu.md). For firmware-side alternatives see [PQ-Flasher](pq-flasher.md) and [Automotive flash bootloaders](automotive-flash-bootloaders-exposing-automotive-ecu-updates.md); [Conescan](conescan.md) covers a different, discovery-first workflow.

## Limits and safety notes

**Status is the main caveat.** The repository is not archived, but its default branch was last pushed 2025-07-25 and the newest tagged release is v1.0.5 from 2021-05-15; 25 issues were open at this check. This is a maintained-looking but slow-moving project, not an actively developed tool — hence `maintenance`. The README also records that the `SMRParser` component was **removed following a DMCA takedown notice**; do not expect that parser in a current checkout. Its origins as a final-year project and the thin upstream documentation mean vehicle/adapter support claims should not be generalised. Reprogramming an ECU can brick it or change safety-critical behaviour: use a bench, a recovery path, and authorisation for the specific vehicle.

## Status and sources

Checked 2026-11-17. **Maintenance** at this check: public, not archived, 1,034 stars / 108 forks, last default-branch push 2025-07-25, latest release v1.0.5 (2021-05-15), GPL-3.0. No build or hardware execution was performed.

- [Upstream README](https://raw.githubusercontent.com/rnd-ash/OpenVehicleDiag/main/README.md)
- [Repository metadata](https://api.github.com/repos/rnd-ash/OpenVehicleDiag)
- [ECU JSON schema](https://github.com/rnd-ash/OpenVehicleDiag/blob/main/SCHEMA.md)

## Related

- [python-can-isotp](python-can-isotp.md)
- [Automotive flash bootloaders: exposing automotive ECU updates](automotive-flash-bootloaders-exposing-automotive-ecu-updates.md)
- [PQ-Flasher](pq-flasher.md)
- [UDS](uds.md)
- [Conescan](conescan.md)
- [Zephyr reference ECU](zephyr-reference-ecu.md)
