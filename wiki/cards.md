---
title: "CarDS"
summary: "ACSAC 2025 dataset of over nine hours of traffic from a 2020 electric vehicle with 10 CAN buses and 6 automotive Ethernet buses, covering benign driving and…"
type: entity
category: "Datasets"
url: "https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/5080"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "ACSAC 2025 dataset of over nine hours of traffic from a 2020 electric vehicle with 10 CAN buses and 6 automotive Ethernet buses, covering benign driving and attack scenarios."
sources:
  - url: "https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/5080"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - tow-ids-automotive-ethernet-intrusion-dataset
  - road
---

ACSAC 2025 dataset of over nine hours of traffic from a 2020 electric vehicle with 10 CAN buses and 6 automotive Ethernet buses, covering benign driving and attack scenarios.

CarDS (Controller Area Network and Automotive Ethernet Realistic Data Set) is, as of its ACSAC 2025 release, the broadest public capture of a whole in-vehicle network: 9 hours 7 minutes of traffic from a modern commercial electric vehicle from 2020, spanning all 10 of its CAN buses (CAN CC and CAN FD, in a domain architecture) and 6 automotive Ethernet buses in a star topology with four VLANs. It holds roughly 397 million CAN and 181 million Ethernet messages in 258 traces, organised into nine scenarios — one benign, seven of CAN-based attacks, and one of automotive Ethernet penetration testing.

The dataset is deposited at TU Darmstadt's TUdatalib repository, with the authors' artifact repository documenting composition and validation. Who it is for: IDS researchers who need multi-bus, multi-protocol data from one coherent vehicle rather than single-bus excerpts. Caveats: it is very large (the authors warn against casually downloading the complete artifact), the vehicle model is anonymised, and it is a single vehicle — breadth of networks, not of fleet.

## Status and sources

Status: **published** — a finished dataset release accompanying the ACSAC 2025 paper, deposited in an institutional repository. Sources: the [TUdatalib record](https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/5080) and the authors' artifact README, checked 2026-11-01.

## Related

- [TOW-IDS Automotive Ethernet Intrusion Dataset](tow-ids-automotive-ethernet-intrusion-dataset.md) — the earlier, testbed-scale Ethernet dataset
- [ROAD](road.md) — single-bus but physically verified dynamometer attacks
