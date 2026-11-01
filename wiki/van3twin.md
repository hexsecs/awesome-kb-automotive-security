---
title: "VaN3Twin"
summary: "ETSI-compliant multi-stack V2X framework for ns-3 covering ITS-G5, C-V2X, and LTE with SUMO and CARLA co-simulation; the continuation of ms-van3t."
type: entity
category: "V2X Security"
url: "https://github.com/DriveX-devs/VaN3Twin"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "ETSI-compliant multi-stack V2X framework for ns-3 covering ITS-G5, C-V2X, and LTE with SUMO and CARLA co-simulation; the continuation of ms-van3t."
related: [veins, artery, vanetza, f2md, misbehavior-detection]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/DriveX-devs/VaN3Twin"
    retrieved: 2026-11-01
  - url: "https://ms-van3ts-documentation.readthedocs.io/en/master/"
    retrieved: 2026-11-01
---

ETSI-compliant multi-stack V2X framework for ns-3 covering ITS-G5, C-V2X, and LTE with SUMO and CARLA co-simulation; the continuation of ms-van3t.

## What it is

A set of ns-3 modules implementing the ETSI C-ITS stack and a suite of V2X applications, designed so the same facilities and applications can be switched between access technologies: IEEE 802.11p (ITS-G5), LTE, LTE-V2X (3GPP Release 14, PC5 mode 4) and 5G NR-V2X (Release 16). It is the continuation of the ms-van3t framework — the README states VaN3Twin "now integrates the whole ms-van3t framework … just under a new name", with additions such as ray-tracing integration; the ms-van3t name still appears throughout the code and docs while the rename proceeds. Developed by researchers at Politecnico di Torino and Politecnico di Milano. Licence: GPL-2.0.

## How it works

The facilities layer carries basic services for CAM, DENM, IVIM, CPM (collective perception) and VAM (vulnerable road users), plus a Vehicle Data Provider fed by TraCI and a Local Dynamic Map. Networking and transport are GeoNetworking and BTP models, with a DCC model in three flavours (NET, CROSS and ACC, reactive and adaptive). ASN.1 support covers CAM and DENM in both ETSI v1 and v2 encodings (switchable at runtime), CPM, and MCM maneuver-coordination messages used by the bundled FORESEE lane-change model — the head commits at check time are FORESEE/MCM work. Couplings: SUMO via TraCI (tested with SUMO v1.6.0–v1.18.0); an offline module replays collected GNSS traces instead of SUMO mobility; a CARLA extension via OpenCDA pulls CARLA mobility **and sensor perception** into the LDM — its documentation notes the gRPC adapter extends the one from the [Veins](veins.md) ecosystem's CARLA coupling, a real cross-entry link; NVIDIA Sionna ray tracing integrates for the channel. NR-V2X comes from the CTTC module in the project's pinned ns-3-dev fork — the installer downloads that fork, not vanilla ns-3. A sample emulator application sends simulated vehicles' ASN.1 CAMs and DENMs out over a real physical interface (real-time operation) and receives external ones, framed by the docs as a step toward hardware-in-the-loop testing. Security is a single `Security` class for the GeoNetworking layer: signed-data containers with signer digest or certificate chain, to-be-signed certificate containers carrying application permissions (PSID + SSP), and ECDSA P-256 signatures via OpenSSL — with **encryption explicitly not implemented** (the source says so in a comment) and no enrolment/PKI machinery alongside it.

## Where it fits

The ns-3 answer to the OMNeT++ simulation world of [Veins](veins.md)/[Artery](artery.md): a researcher picks VaN3Twin when the study needs several radio stacks in one framework — it is the only one of this section's simulators whose own docs list ITS-G5, LTE, LTE-V2X and NR-V2X side by side, including coexistence studies — or when CARLA perception/digital-twin coupling matters. It implements its own ETSI stack inside ns-3 rather than reusing [Vanetza](vanetza.md), which is the precise contrast with Artery (which wraps Vanetza). Per the README's acknowledgements, the framework's publications are a 2024 *Computer Communications* journal paper and a 2025 main VaN3Twin pre-print.

## Limits and safety notes

Simulation framework: results are bounded by ns-3's channel/PHY models and the SUMO/CARLA mobility fed into it; the only path off the simulator is the sample emulator application. Version brittleness is self-documented: the README warns backward compatibility "is not ensured" with new TraCI versions, requires the specific ns-3-dev fork, and the CARLA extension targets CARLA 0.9.12 on Ubuntu 20.04 with a GPU recommended. The ms-van3t rename is incomplete by the project's own admission. Security scope: signing/verification structures only, encryption unimplemented, and **no TS 103 097 conformance statement exists** in the sources read — the secured-packet containers mirror the 1609.2-style signed-data model as an observation from the source header, not a certified conformance claim, and this page does not upgrade it into one. Nothing in the framework performs misbehavior detection.

## Status and sources

Checked 2026-11-01. **Active**: not archived; head commit dated 2026-10-06 with pushes through 2026-10-17, and the recent work (FORESEE/MCM) is feature development, not upkeep. It has never cut a GitHub release — versioning lives in an in-repo RELEASE_NOTES.md — so activity is judged on commit flow, which is current. Documentation claims above come from the following primary sources; no simulation was run for this page.

- [Upstream repository](https://github.com/DriveX-devs/VaN3Twin)
- [Project documentation](https://ms-van3ts-documentation.readthedocs.io/en/master/)

## Related

- [Veins](veins.md)
- [Artery](artery.md)
- [Vanetza](vanetza.md)
- [F2MD](f2md.md)
