---
uid: 01a19d3c-afe9-7979-9886-6d4b05e6997f
title: "TOW-IDS Automotive Ethernet Intrusion Dataset"
summary: "HCRL captures of AVTP, gPTP, and CAN-over-UDP traffic on an automotive Ethernet network, split into normal driving and five labelled attack scenarios."
type: entity
category: "Datasets"
url: "https://ocslab.hksecurity.net/Datasets/tow-ids-automotive-ethernet-intrusion-dataset"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "HCRL captures of AVTP, gPTP, and CAN-over-UDP traffic on an automotive Ethernet network, split into normal driving and five labelled attack scenarios."
sources:
  - url: "https://ocslab.hksecurity.net/Datasets/tow-ids-automotive-ethernet-intrusion-dataset"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - cards
  - survival-analysis-dataset
---

HCRL captures of AVTP, gPTP, and CAN-over-UDP traffic on an automotive Ethernet network, split into normal driving and five labelled attack scenarios.

TOW-IDS is HCRL's automotive Ethernet intrusion dataset, built to support the lab's Three Overlapped Wavelets IDS paper (IEEE Transactions on Information Forensics and Security, 2022). It captures three kinds of traffic off a 100BASE-T1 switched network by port mirroring: AVTP audio/video streams, gPTP time-synchronisation traffic, and CAN messages encapsulated in UDP — so it covers the timing and streaming protocols that CAN-only datasets never see. The captures divide into a normal-driving dataset and an abnormal dataset built from five labelled scenarios: frame injection, PTP sync attack, switch MAC flooding, CAN DoS, and CAN replay, with label names defined on the download page.

You get pcap files, via Dropbox from the HCRL page or from IEEE DataPort (DOI 10.21227/bz0w-zc12). Who it is for: anyone working on Ethernet-side in-vehicle IDS rather than CAN. Caveats: the traffic comes from the lab's Ethernet testbed environment rather than a production vehicle's network, the attack set is small and fixed, and HCRL offers it for academic purposes with a citation to the paper requested.

## Status and sources

Status: **published** — a finished static release, hosted by HCRL and mirrored as a citable IEEE DataPort record. Sources: the [HCRL dataset page](https://ocslab.hksecurity.net/Datasets/tow-ids-automotive-ethernet-intrusion-dataset) and the DataPort record, checked 2026-11-01.

## Related

- [CarDS](cards.md) — the 2025 whole-vehicle successor: real CAN and Ethernet buses in one capture
- [Survival Analysis Dataset](survival-analysis-dataset.md) — HCRL's CAN-side multi-vehicle dataset
