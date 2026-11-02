---
title: "Artery"
summary: "OMNeT++ simulation framework pairing the Vanetza ITS-G5 stack with SUMO traffic, providing the environment that most misbehavior-detection and V2X attack…"
type: entity
category: "V2X Security"
url: "https://github.com/riebl/artery"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "OMNeT++ simulation framework pairing the Vanetza ITS-G5 stack with SUMO traffic, providing the environment that most misbehavior-detection and V2X attack studies are built on."
related: [vanetza, veins, f2md, van3twin, misbehavior-detection]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/riebl/artery"
    retrieved: 2026-11-01
  - url: "https://artery.v2x-research.eu/"
    retrieved: 2026-11-01
---

OMNeT++ simulation framework pairing the Vanetza ITS-G5 stack with SUMO traffic, providing the environment that most misbehavior-detection and V2X attack studies are built on.

## What it is

An OMNeT++ simulation framework for ETSI ITS-G5 vehicular networking: it couples the SUMO road-traffic simulator with a per-vehicle ITS-G5 protocol stack so cooperative ITS services (CAM, DENM, collective perception) can be simulated at scale with realistic vehicle movement. The ITS-G5 stack itself is not Artery's code — Artery wraps the separate [Vanetza](vanetza.md) implementation (GeoNetworking, BTP, congestion control, security) as OMNeT++ modules and adds the simulation scaffolding around it: a per-vehicle middleware equipping each vehicle with a configurable set of services, common facilities, an environment/sensor model, and scripted scenario control. It began as an extension of the [Veins](veins.md) framework. Licence: GPL-2.0. (The characterisation of Artery as the environment most misbehavior-detection studies build on is the list's framing of its role in the literature; neither repo's own docs make that claim, and it is kept attributed to the list here.)

## How it works

SUMO reads the road network and traffic demand; the OMNeT++ runtime runs the network simulation; a global TraCI manager module launches SUMO and talks to it over TCP, pulling each vehicle's position, speed and heading per step and creating/updating/deleting the matching OMNeT++ vehicle modules. The stack is Vanetza, shipped as a git submodule and wrapped as OMNeT++ modules — the GeoNetworking router, DCC congestion control, and the ETSI security entity. Each vehicle's central module is the *Middleware*, which instantiates service modules from an XML configuration, so different vehicles can carry different application sets in one run: the Cooperative Awareness service (CAM), the Decentralized Environmental Notification service (DENM), RSU and pedestrian variants, a Local Dynamic Map facility, and a Collective Perception service fed by the environment model, which gives vehicles simulated sensor objects to perceive and report. Sudden scenario changes (accidents, weather, breakdowns) are scripted in Python through the storyboard feature — condition/effect pairs evaluated at runtime, and the hook most often used to trigger events, benign or malicious, mid-run. Artery provides **no radio model of its own** — its architecture doc says so plainly; it employs the IEEE 802.11 model of Veins or of INET, INET being the one the team mostly uses nowadays, so Artery can run without Veins. An LTE path and a Simulte fork exist in the tree, but the headline scope remains ITS-G5; the LTE/C-V2X path is present but secondary in the sources read.

## Where it fits

The simulation substrate of this section. Precisely: [Vanetza](vanetza.md) is Artery's protocol stack consumed as a submodule — same maintainer on both repositories — and is also usable standalone, which is why it is a separate entry. [Veins](veins.md) is Artery's ancestor: it started as a Veins extension, still ships Veins as a submodule and can use its 802.11 model, but no longer requires it; Veins remains the WAVE/802.11p-centred framework, Artery the ITS-G5 counterpart built out of it. [F2MD](f2md.md) has **no code dependency with Artery in either direction** — it is built on a forked Veins; the two are parallel OMNeT++/SUMO environments whose relationship is topical: F2MD supplies the misbehavior-detection chain a plain Artery setup does not ship. [VaN3Twin](van3twin.md) shares the Vanetza stack but couples it to a different simulator lineage (ns-3).

## Limits and safety notes

Simulation only: Artery models the stack and the traffic, and results are bounded by the borrowed radio models (Veins or INET 802.11) and by SUMO's traffic model; nothing here transmits or touches a real vehicle. There are **no versioned releases** — zero GitHub releases ever and a single tag from 2015 — so studies pin a commit, not a version; that reproducibility caveat is part of the record. The documentation website lags the code (its footer reads August 2023 while the code is developed into 2026); the repository is the live source. The security entity Artery exposes is Vanetza's ETSI security implementation; Artery itself adds no attack or detection tooling — attacks in Artery-based studies are the study authors' own services and storyboards.

## Status and sources

Checked 2026-11-01. **Active**: not archived; 2,646 commits with the latest on 2026-07-30 — multiple feature and fix commits plus merged pull requests that month, roughly three months before this check. It has never made a versioned release, so activity is judged on commit flow, which is current. Documentation claims above come from the following primary sources; no simulation was run for this page.

- [Upstream repository](https://github.com/riebl/artery)
- [Project documentation site](https://artery.v2x-research.eu/)

## Related

- [Vanetza](vanetza.md)
- [Veins](veins.md)
- [F2MD](f2md.md)
- [VaN3Twin](van3twin.md)
