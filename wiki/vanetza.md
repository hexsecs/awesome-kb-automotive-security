---
title: "Vanetza"
summary: "Open-source ETSI C-ITS protocol stack covering GeoNetworking, BTP, DCC, and the security layer, widely used as the reference implementation for V2X…"
type: entity
category: "V2X Security"
url: "https://github.com/riebl/vanetza"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source ETSI C-ITS protocol stack covering GeoNetworking, BTP, DCC, and the security layer, widely used as the reference implementation for V2X experimentation."
related: [artery, van3twin, veins, misbehavior-detection]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/riebl/vanetza"
    retrieved: 2026-11-01
  - url: "https://www.vanetza.org"
    retrieved: 2026-11-01
  - url: "https://github.com/riebl/vanetza/blob/master/vanetza/security/README.md"
    retrieved: 2026-11-01
---

Open-source ETSI C-ITS protocol stack covering GeoNetworking, BTP, DCC, and the security layer, widely used as the reference implementation for V2X experimentation.

## What it is

An open-source C++ implementation of the ETSI C-ITS protocol suite — a set of libraries, not a simulator. It implements GeoNetworking, the Basic Transport Protocol (BTP), Decentralized Congestion Control (DCC), the ETSI security layer, and ASN.1 facilities messages (CAM, DENM, CPM, IVIM, MAPEM, SPATEM, RTCMEM, SREM, SSEM), and it runs both inside simulations and on real V2X hardware. Development started as a research project at Technische Hochschule Ingolstadt (CARISSMA Car2X lab); since 2024, nfiniity GmbH sponsors active development, with maintenance coordinated by Raphael Riebl. Licence: LGPLv3.

## How it works

Component libraries cover access (IEEE 802.11 PHY/MAC helpers), asn1 (generated code and wrappers), btp, dcc (cross-layer DCC algorithms), facilities (helpers to generate and evaluate ITS messages), geonet (geographical routing), gnss, net (socket API and packet handling), rpc, and security (sign and verify packets) — built with CMake, also packaged via Conan, with unit tests in CI on the three latest Ubuntu LTS versions. It is designed for ITS-G5 over IEEE 802.11p, but the README states the components "can be combined with other communication technologies as well, e.g. GeoNetworking over IP multicast or C-V2X", and the repo ships CMake toolchains for real hardware — Cohda MK5 and Autotalks Craton. The `socktap` tool runs most of the stack on Linux packet sockets or Cohda LLC sockets; `certify` generates and handles security certificates and authorization tickets; a benchmark tool measures signing/verification throughput. The security module is the deep part: it implements the **ETSI TS 103 097** security extension of GeoNetworking in two namespaces (v1.2.1 and v1.3.1), with encap/decap services that sign outgoing and verify incoming secured messages, ECDSA-256 signatures with SHA-256, OpenSSL and Crypto++ backends, CAM/DENM security profiles, incoming-certificate validation, and requesting certificates of unknown stations from peers. The ASN.1 set also ships the surrounding trust machinery's definitions — TS 103 097, IEEE 1609.2, and TS 102 941 (enrolment, authorization, trust lists, CA messages) — and an experimental `certify-pqc` tool generates ECC/FN-DSA post-quantum certificate chains. The module README states the implementation "has been verified to work correctly by interoperability tests with other implementations" (the project's own claim).

## Where it fits

The reusable ETSI stack that other things embed. The project site's Deployments page states this section's key relationship verbatim: [Artery](artery.md) "is a V2X simulation framework based on OMNeT++; Vanetza is used in this network simulation as (quite detailed) model of ITS-G5 protocols" — so in the OMNeT++ world, Artery supplies the framework and Vanetza supplies the protocol stack, including its security layer. The same page lists non-simulation deployments: communication units in the CARISSMA Car2X lab, prototype motorcycles of the Connected Motorcycle Consortium, and nfiniity's *cube* V2X ecosystem. Against the siblings: [VaN3Twin](van3twin.md) implements its own ETSI stack inside ns-3 instead of reusing Vanetza, and [Veins](veins.md) core ships no ETSI facilities/security stack at all — Vanetza is where a researcher goes for the stack itself, on a bench or inside Artery.

## Limits and safety notes

A library: it brings no channel model, no mobility and no simulation engine; on its own it does not produce a network study. The security gaps are the module's **own list**, kept verbatim in substance: **no CA revocation (CRL) checks**, incomplete region checks, and no support "to request authorization tickets from an authorization authority or to do an enrolment" — it is the message-security layer, not a PKI client, and any statement about PKI behaviour must stop at certificate handling and ticket generation via `certify`. One precision this page enforces: the IEEE 1609.2 ASN.1 definitions ship in the repo, but no source read states the security entity processes US-style 1609.2 secured data end-to-end — the documented implementation target is TS 103 097, and the ASN.1 presence is not upgraded into a 1609.2 implementation claim. The depth of ETSI Release 2 support was not enumerated in the sources read.

## Status and sources

Checked 2026-11-01. **Active** — the strongest activity signal in this section: not archived; a release cadence of roughly two to three releases per year (latest v26.09, 2026-09-08), a sponsored maintainer since 2024, and a head commit dated the day of checking (2026-11-01). Documentation claims above come from the following primary sources; no stack was run for this page.

- [Upstream repository](https://github.com/riebl/vanetza)
- [Project site](https://www.vanetza.org)
- [Security module README](https://github.com/riebl/vanetza/blob/master/vanetza/security/README.md)

## Related

- [Artery](artery.md)
- [VaN3Twin](van3twin.md)
- [Veins](veins.md)
