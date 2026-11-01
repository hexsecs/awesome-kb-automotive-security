---
title: "pwnobd"
summary: "Offensive cybersecurity toolkit for vulnerability analysis of OBD-II devices presented at Black Hat Europe 2024."
type: entity
category: "Penetration Testing"
url: "https://github.com/Nnubes256/pwnobd"
status: maintenance
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Offensive cybersecurity toolkit for vulnerability analysis of OBD-II devices presented at Black Hat Europe 2024."
related: [donglescope, car-toolkit, autofuze]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/Nnubes256/pwnobd"
    retrieved: 2026-11-01
  - url: "https://github.com/Nnubes256/pwnobd/tree/main/src/pwnobd/modules"
    retrieved: 2026-11-01
  - url: "https://github.com/Nnubes256/pwnobd/blob/main/src/pwnobd/modules/attacks/elm327.py"
    retrieved: 2026-11-01
---

Offensive cybersecurity toolkit for vulnerability analysis of OBD-II devices presented at Black Hat Europe 2024.

## What it is

A Python penetration-testing toolkit whose target is not the vehicle but the OBD-II device plugged into it — the cheap diagnostic dongle treated as the attack surface. It is a research artefact with an unusual paper trail: presented at Black Hat Europe 2024 (Arsenal) and JNIC 2024, and published as a peer-reviewed paper in IEEE Access 13 (July 2025), pp. 126925–126934 (doi:10.1109/ACCESS.2025.3589867). The shipped code concentrates on Bluetooth ELM327 dongles. Licence: MIT.

## How it works

An interactive Python CLI (installed with pipx from the repository) whose functionality is modular and dynamically registered through decorators — `@attack`, `@device("name")`, `@scanner("name")` — so dropping a Python file into the module tree registers it at startup. The attack lifecycle is explicit in the README: `precheck` parameter validation, constructor parameter ingestion from a typed `OPTIONS` dict, async `setup`, and async `run(ctx, devices)` with devices handed over pre-locked; each attack declares `DEVICE_REQUIREMENTS` validated before instantiation. Device drivers subclass a core `Device` class plus capability interfaces, and scanners come in two kinds — general building-block scanners and leaf scanners whose results can instantiate a driver directly during recon. The shipped modules include Bluetooth support built on bleak, recon, a capture module, and exactly one device driver (Bluetooth ELM327) and one concrete attack: a **replay attack** that parses a PCAP for Bluetooth traffic to a device named "OBDII", reconstructs the AT-command conversation segmented on `ATZ` resets, and replays it against a real Bluetooth ELM327 device with original inter-packet timing corrected for measured round-trip latency.

## Where it fits

The offensive counterpart to [DongleScope](donglescope.md) in the same section: DongleScope automates vulnerability *detection* in wireless OBD-II dongles (USENIX Security 2020 research); pwnobd is a hands-on exploitation and replay framework aimed at the same device class, with an extension API for new attacks and drivers. Its CAN-side sending goes through the dongle under test, so it complements rather than overlaps the bus-side toolkits ([Car Toolkit](car-toolkit.md), [AutoFuze](autofuze.md)).

## Limits and safety notes

Scope is the dongle, not the car: the only shipped device driver and the only concrete attack target Bluetooth ELM327 devices. Support for other OBD-II device families exists only as an extension API — a user must write the driver. The README documents the framework mechanics thoroughly but ships no safety or authorisation guidance of its own; the framing is vulnerability research on devices the tester owns. A very small history (three commits) and a single early release mark it as published research code, not a maintained product.

## Status and sources

Checked 2026-11-01. **Maintenance**: the repository is not archived; created 2024-07-07, it has three commits in total with the latest on 2025-09-23, and one release, 0.1.0 (2024-08-28). The IEEE Access paper followed in July 2025. Sporadic by any measure, but research code that still shows occasional life. Documentation claims above come from the following primary sources; no dongle was attacked for this page.

- [Upstream repository](https://github.com/Nnubes256/pwnobd)
- [Module tree](https://github.com/Nnubes256/pwnobd/tree/main/src/pwnobd/modules)
- [Shipped ELM327 replay attack](https://github.com/Nnubes256/pwnobd/blob/main/src/pwnobd/modules/attacks/elm327.py)

## Related

- [DongleScope](donglescope.md)
- [Car Toolkit](car-toolkit.md)
- [AutoFuze](autofuze.md)
