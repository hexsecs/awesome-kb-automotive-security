---
title: "F2MD"
summary: "Simulation framework recreating the whole misbehavior detection chain for ITS-G5 and C-V2X, with plausibility checks, machine learning detectors, and both…"
type: entity
category: "V2X Security"
url: "https://github.com/josephkamel/F2MD"
status: maintenance
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Simulation framework recreating the whole misbehavior detection chain for ITS-G5 and C-V2X, with plausibility checks, machine learning detectors, and both local and global attack implementations."
related: [artery, veins, v2verifier]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/josephkamel/F2MD"
    retrieved: 2026-11-01
---

Simulation framework recreating the whole misbehavior detection chain for ITS-G5 and C-V2X, with plausibility checks, machine learning detectors, and both local and global attack implementations.

## What it is

A framework for misbehavior detection (MD) research in vehicular networks, built on OMNeT++: it simulates the whole ETSI misbehavior-handling chain — local detection on the vehicle, reporting, and global investigation by a misbehavior authority — together with the attacks those mechanisms are meant to catch, for both ITS-G5 and C-V2X. F2MD is, to this KB's knowledge, the only ITS framework that includes an institutional model of the misbehavior authority alongside the detection chain. Its anchoring publication is Kamel et al., "A Misbehavior Detection Framework for Cooperative Intelligent Transport Systems", *IEEE Transactions on Vehicular Technology* (2020; citation from the repository's own README).

## How it works

A chain of OMNeT++ module families recreates the ETSI model end to end. **Detection (local):** `mdChecks` modules run plausibility checks on incoming beacons (position/speed consistency, sudden-appearance and overlap classes), with three check sets selectable in the implementation; detected messages flow to `mdApplications` node-level investigation modules — threshold-based, aggregation-based, behavioural, cooperative C2C and machine-learning variants — which produce detections. **Reporting:** `mdReport` modules package a detection plus the offending beacons as a misbehavior report to the misbehavior authority, in two generations (the original XML report path and a newer binary ETSI-format report). **Authority:** a Python misbehavior-authority server receives reports on a closed port, runs global investigation over a pluggable "ideal detector" slot, and broadcasts resolution information; pseudonym change policies are co-simulated as part of the interaction between reports and pseudonymous certificates. **Attack side:** `mdAttacks` modules — a local attack manager hosting roughly twenty attack classes (constant position, offset, position jump, random position and heading, speed shifter, beacon denial-of-service, and combinations on beacons and CAM/DENM data), plus global attacks (Sybil, replay, denial of service) — launchable in real time via an attack server, so attack timing is decoupled from simulation configuration; machine-learning support runs through a separate ML server coupled over HTTP. The radio side is dual: ITS-G5 (IEEE 802.11p with DCC) through a **forked [Veins](veins.md)**, and C-V2X Sidelink (PC5 Mode 4) through a **forked Simulte**, with INET as a submodule and SUMO coupled via TraCI. The implementation reuses Veins' beaconing with the beacons carrying a vehicular pseudonym — consistent with F2MD's own argument, argued in its paper, that C-ITS beacons are BSM-equivalent.

## Where it fits

The section's detection-chain entry: where F2MD exists, the other simulators mostly don't — [Artery](artery.md) ships no detection tooling, [Veins](veins.md) core ships no security layer at all, and [V2Verifier](v2verifier.md) is the over-the-air counterpart rather than a simulator. There is **no code dependency between F2MD and Artery in either direction** (parallel OMNeT++ lineage, both ultimately Veins-descended), a precision this page keeps because the two are often conflated. F2MD is the environment for evaluating detectors against attacks with ground truth — attack types are configurable, reports and resolutions are observable, and the authority side is simulated rather than assumed.

## Limits and safety notes

Simulation only: detectors here are evaluated against simulated attacks in simulated traffic, and the authority's "ideal detector" slot is a research scaffold, not a deployed MA design. The toolchain is pinned and old — the README's requirements are OMNeT++ 5.6.1, SUMO 1.5.0, and forked Veins/Simulte at their 2020 state, with an installer the README describes as tested on Debian 9 / Ubuntu 18.04 — so running it today means running a period toolchain. Two provenance gaps are recorded, not filled: the repository carries **no licence file**, so reuse terms are unstated; and the individual attack names/threshold details in the anchoring IEEE paper could not be verified against its full text (not readable in the sources checked), so this page rests on module-level code evidence, which is sufficient for the mechanism claims but not for paper-only parameters.

## Status and sources

Checked 2026-11-01. **Maintenance**: not archived, but the substantive code work ends in September 2022 (submodule updates), followed by README-only commits in September 2023 and November 2025 — sporadic touches on a completed 2020 research framework, with zero releases and zero tags. Documentation claims above come from the following primary sources; no simulation was run for this page.

- [Upstream repository](https://github.com/josephkamel/F2MD)

## Related

- [Artery](artery.md)
- [Veins](veins.md)
- [V2Verifier](v2verifier.md)
