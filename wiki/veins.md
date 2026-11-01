---
title: "Veins"
summary: "Open-source vehicular network simulation framework coupling OMNeT++ and SUMO, used as the testbed for VANET and V2X security and attack studies."
type: entity
category: "V2X Security"
url: "https://github.com/sommer/veins"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source vehicular network simulation framework coupling OMNeT++ and SUMO, used as the testbed for VANET and V2X security and attack studies."
related: [artery, van3twin, f2md, vanetza]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/sommer/veins"
    retrieved: 2026-11-01
  - url: "https://veins.car2x.org"
    retrieved: 2026-11-01
---

Open-source vehicular network simulation framework coupling OMNeT++ and SUMO, used as the testbed for VANET and V2X security and attack studies.

## What it is

An open-source framework for running vehicular network simulations, built on bidirectional online coupling of two established simulators: OMNeT++ runs the network simulation and SUMO runs the road traffic simulation, each able to influence the other during a run — a network-triggered warning can reroute SUMO traffic, whose new positions then change the network. Its roots are a 2006-era research project; the canonical citation the project itself asks for is Sommer, German & Dressler, "Bidirectionally Coupled Network and Road Traffic Simulation for Improved IVC Analysis", *IEEE Transactions on Mobile Computing* 10(1), 2011. Licence: GPL-2.0-or-later for most parts (per-file licences).

## How it works

SUMO is launched and driven through TraCI by OMNeT++ modules, and the simulations run online and bidirectionally. The radio model is an IEEE 802.11p NIC — `Mac1609_4` (the IEEE 1609.4-style multi-channel MAC) over an 802.11p PHY with MiXiM-derived analogue models for interference, and obstacle-shadowing models for buildings **and** vehicles; the project's stated goal is validated, computationally inexpensive channel models. Example application modules (beaconing, warning-style demos) are what researchers extend — Veins supplies the framework and models, not a catalogue of ITS services. The `veins_inet` subprojects in the tree let Veins mobility drive the INET framework's TCP/IP stack, and an "Instant Veins" prebuilt VM is offered for the tutorial. Version lockstep is a recurring theme: the 5.4 release notes are dominated by compatibility (OMNeT++ 6.4, SUMO 1.23–1.28, INET 4.6/4.7).

## Where it fits

The incumbent OMNeT++ simulation baseline for VANET/V2X studies. Within this section: [Artery](artery.md) is the OMNeT++ alternative when the study needs the ETSI ITS-G5 stack (facilities, GeoNetworking, security) — Artery gets that stack from [Vanetza](vanetza.md), which Veins core does not include; [VaN3Twin](van3twin.md) is the ns-3 counterpart and additionally covers C-V2X/NR-V2X, which core Veins does not model; [F2MD](f2md.md) is a misbehavior-detection framework built on a forked Veins. Veins' security content is a **verified absence**, and stating it precisely is this page's security claim: a full-tree search finds no IEEE 1609.2 or ETSI TS 103 097 security implementation — the only "1609" component is the 1609.4 MAC (channel coordination, a different standard from 1609.2 security); there is no signing, no certificate handling, no GeoNetworking/BTP/DCC and no facilities services in the core tree. Its role in security research is exactly what the list description says: the **testbed** — researchers implement attackers, plausibility checks and countermeasures in its application layer or in frameworks layered on it, because its traffic/network coupling lets an attack's effect on traffic be measured, not just its packet counts.

## Limits and safety notes

Simulation only, and 802.11p-centric: no C-V2X/5G sidelink model and no ETSI facilities/security stack in the core tree (both verified against the tree at check time) — studies needing them must add frameworks or choose another base; the external subproject ecosystem was not inventoried for this page, so the claim is about core Veins only. Validity is bounded by its models: results inherit the accuracy of the 802.11p PHY/analogue and obstacle-shadowing models and of the SUMO traffic fed in. Version lockstep with OMNeT++/SUMO/INET releases is a recurring cost. One minor source note: at check time the project homepage still headlined release 5.3 although 5.4 shipped on GitHub on 2026-10-29 — the website lags the repo; the repo is the status source of truth.

## Status and sources

Checked 2026-11-01. **Active**: not archived; release veins-5.4 was published three days before checking (2026-10-29) with the version-bump commit as repository head, following two further releases earlier in 2025 — a cadence that resumed after a 2022–2024 gap. Documentation claims above come from the following primary sources; no simulation was run for this page.

- [Upstream repository](https://github.com/sommer/veins)
- [Project site](https://veins.car2x.org)

## Related

- [Artery](artery.md)
- [VaN3Twin](van3twin.md)
- [F2MD](f2md.md)
- [Vanetza](vanetza.md)
