---
title: "F2MD"
summary: "Simulation framework recreating the whole misbehavior detection chain for ITS-G5 and C-V2X, with plausibility checks, machine learning detectors, and both…"
type: entity
category: "V2X Security"
url: "https://github.com/josephkamel/F2MD"
status: maintenance
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Simulation framework recreating the whole misbehavior detection chain for ITS-G5 and C-V2X, with plausibility checks, machine learning detectors, and both local and global attack implementations."
related: [artery, veins, v2verifier, misbehavior-detection, v2x-credential-management]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/josephkamel/F2MD"
    retrieved: 2026-11-01
---

Simulation framework recreating the whole misbehavior detection chain for ITS-G5 and C-V2X, with plausibility checks, machine learning detectors, and both local and global attack implementations.

## What it is

A framework for misbehavior detection (MD) research in vehicular networks, built on OMNeT++: it simulates the whole ETSI misbehavior-handling chain — local detection on the vehicle, reporting, and global investigation by a misbehavior authority — together with the attacks those mechanisms are meant to catch, for both ITS-G5 and C-V2X. F2MD is, to this KB's knowledge, the only ITS framework that includes an institutional model of the misbehavior authority alongside the detection chain. Its anchoring publication is Kamel et al., "Simulation Framework for Misbehavior Detection in Vehicular Networks", *IEEE Transactions on Vehicular Technology* 69(6), pp. 6631–6643 (2020), DOI 10.1109/TVT.2020.2984878 — the title as the repository's own README cites it; the paper's full text is openly available (HAL hal-02527873) and was read for this page's 2026-11-01 correction pass.

## How it works

A chain of OMNeT++ module families recreates the ETSI model end to end. **Detection (local):** `mdChecks` modules run plausibility checks on incoming beacons (position/speed consistency, sudden-appearance and overlap classes), with three check sets selectable in the implementation; detected messages flow to `mdApplications` node-level investigation modules — threshold-based, aggregation-based, behavioural, cooperative C2C and machine-learning variants — which produce detections. **Reporting:** `mdReport` modules package a detection as a misbehavior report following the three-container design (header / source / evidence) of the authors' VNC 2018 reporting protocol, in four forms of increasing weight — check results only; the single offending beacon; an evidence history of up to 30 beacons; and a protocol form pairing beacons with their check results — serialised as JSON to the authority (XML serialisers also exist in the code), with a report enforcer throttling repeats to one report per pseudonym per behaviour window while evidence accumulates. Two detector configurations run in parallel on the same scenario — V1 and V2, each with its own check set, application and authority instance — for head-to-head comparison; they are configurations, not report-format generations, and no binary ETSI encoding exists in the code read. **Authority:** a Python misbehavior-authority server collects each chain's reports; its decision rule is deliberately minimal — the paper calls it "a simple non intelligent method that has a threshold on the number of reports": a pseudonym is predicted a local attacker past five reports, and reaction levels escalate with prediction count through warning, ticket, passive revocation and active revocation (the paper's levels 0–4). The server returns no resolution into the simulation — the report POST is answered with the literal string `"False"`. Pseudonyms here are synthetic integers minted by six change policies (periodical, disposable, distance-based, random, C2C-style, and none): there is **no PKI or certificate handling anywhere in the artefact**, and the paper lists adding a PKI module as future work. All three layers key on the pseudonym — check history, behavioural trust, authority report counts — and the paper's own pseudonym-change experiment shows frequent changes starving the count-based authority of the reports it needs, which is why the chain is summarised as a concept at [Misbehavior detection in V2X](concepts/misbehavior-detection.md). **Attack side:** `mdAttacks` modules — a local attack manager hosting nineteen misbehavior types in code, matching the paper's taxonomy of nine faulty behaviours (fixed and random position and speed, each with and without offsets, plus stale messages) and six attacks (DoS, disruptive replay of overheard beacons, data replay, eventual stop, congestion Sybil, and MA Stress), with the code splitting DoS variants and adding Sybil hybrids — plus one global attack, MA Stress, which files fabricated reports at the authority rather than transmitting beacons — launchable in real time via an attack server, so attack timing is decoupled from simulation configuration; machine-learning support runs through a separate ML server coupled over HTTP. The radio side is dual: ITS-G5 (IEEE 802.11p with DCC) through a **forked [Veins](veins.md)**, and C-V2X Sidelink (PC5 Mode 4) through a **forked Simulte**, with INET as a submodule and SUMO coupled via TraCI. The implementation reuses Veins' beaconing with the beacons carrying a vehicular pseudonym — consistent with F2MD's own argument, argued in its paper, that C-ITS beacons are BSM-equivalent.

## Where it fits

The section's detection-chain entry: where F2MD exists, the other simulators mostly don't — [Artery](artery.md) ships no detection tooling, [Veins](veins.md) core ships no security layer at all, and [V2Verifier](v2verifier.md) is the over-the-air counterpart rather than a simulator. There is **no code dependency between F2MD and Artery in either direction** (parallel OMNeT++ lineage, both ultimately Veins-descended), a precision this page keeps because the two are often conflated. F2MD is the environment for evaluating detectors against attacks with ground truth — attack types are configurable, reports and resolutions are observable, and the authority side is simulated rather than assumed.

## Limits and safety notes

Simulation only: detectors here are evaluated against simulated attacks in simulated traffic, and the authority's count-threshold decision rule is a placeholder its own authors describe as such, not a deployed MA design. The toolchain is pinned and old — the README's requirements are OMNeT++ 5.6.1, SUMO 1.5.0, and forked Veins/Simulte at their 2020 state, with an installer the README describes as tested on Debian 9 / Ubuntu 18.04 — so running it today means running a period toolchain. One provenance gap is recorded, not filled: the repository carries **no licence file**, so reuse terms are unstated. (An earlier version of this page carried a second caveat — that the anchoring paper's full text had not been read — and three mechanism errors that came with it: a wrong paper title, a "binary ETSI-format report" that the code does not contain, and an "ideal detector" authority. The 2026-11-01 correction pass read the paper's full text and the report/authority code firsthand and fixed all four; the mechanism claims now rest on both.)

## Status and sources

Checked 2026-11-01. **Maintenance**: not archived, but the substantive code work ends in September 2022 (submodule updates), followed by README-only commits in September 2023 and November 2025 — sporadic touches on a completed 2020 research framework, with zero releases and zero tags. Documentation claims above come from the following primary sources; no simulation was run for this page.

- [Upstream repository](https://github.com/josephkamel/F2MD)
- [Anchoring paper, DOI 10.1109/TVT.2020.2984878](https://doi.org/10.1109/TVT.2020.2984878) (open full text: HAL hal-02527873)

## Related

- [Artery](artery.md)
- [Veins](veins.md)
- [V2Verifier](v2verifier.md)
