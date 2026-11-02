---
uid: 01a19d3c-af88-78f7-bff4-12cd07cf4311
title: "Expanding the Attack Scenarios of SAE J1939: A Comprehensive Analysis of Established and Novel Vulnerabilities in Transport Protocol"
summary: "Lee, Lee, Jun, and Kim, escar USA 2024. Presents 14 attack scenarios against the J1939 protocol used in commercial vehicles, seven of them new."
type: entity
category: "Conference Presentations"
url: "https://zenodo.org/records/18715820"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Lee, Lee, Jun, and Kim, escar USA 2024. Presents 14 attack scenarios against the J1939 protocol used in commercial vehicles, seven of them new."
sources:
  - url: "https://zenodo.org/records/18715820"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - pretty-j1939
  - truckdevil
---

Lee, Lee, Jun, and Kim, escar USA 2024. Presents 14 attack scenarios against the J1939 protocol used in commercial vehicles, seven of them new.

An escar USA 2024 paper by Hwejae Lee, Hyosun Lee, Saehee Jun, and Huy Kang Kim, on the SAE J1939 protocol family used in trucks and other commercial vehicles — a far less picked-over target than passenger-car CAN. The authors catalogue 14 attack scenarios against the J1939 Transport Protocol, which moves multi-packet messages over the bus: seven scenarios carried over from prior research and seven novel ones identified by their analysis. On their real-time testbed, 11 of the 14 scenarios executed successfully; the authors flag that some attacks inject only a single message, which makes them correspondingly hard for an intrusion-detection system to spot.

What you get: the full paper (PDF) on Zenodo — scenario catalogue, testbed design, and per-scenario results — not just slides. It is the natural entry point for heavy-vehicle network security work and for anyone porting CAN IDS thinking to J1939. Caveats: the results are testbed demonstrations, not attacks on a production truck in service, and the scope is the transport protocol layer rather than every J1939 application profile.

## Status and sources

Status: **published** — escar USA 2024; paper PDF public. Verified against the proceedings deposit at [zenodo.org/records/18715820](https://zenodo.org/records/18715820) (the stub's resource), 2026-11-01.

## Related

- [pretty-j1939](pretty-j1939.md) — J1939 tooling for working with the protocol this paper attacks
- [TruckDevil](truckdevil.md) — a research platform for J1939/commercial-vehicle networks
