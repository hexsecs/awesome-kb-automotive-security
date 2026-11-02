---
title: "GEM-CAN"
summary: "Labelled capture of about 143,000 CAN frames from an autonomous GEM e6 platform, with normal operation, DoS floods, and brake and steering-lock…"
type: entity
category: "Datasets"
url: "https://zenodo.org/records/17834775"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Labelled capture of about 143,000 CAN frames from an autonomous GEM e6 platform, with normal operation, DoS floods, and brake and steering-lock data-tampering injections, for benchmarking lightweight on-device IDS."
sources:
  - url: "https://zenodo.org/records/17834775"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - syncan
  - car-hacking-dataset
---

Labelled capture of about 143,000 CAN frames from an autonomous GEM e6 platform, with normal operation, DoS floods, and brake and steering-lock data-tampering injections, for benchmarking lightweight on-device IDS.

GEM-CAN is a small, fully labelled CAN dataset from a GEM e6 low-speed autonomous vehicle driving itself on a closed track, collected via PCAN-USB. Of its roughly 143,000 frames, about 100,000 are nominal driving, about 41,000 are a DoS flood using ID 0x00000000, and about 1,300 are data-tampering injections aimed at brake and steering-lock functions — safety-relevant targets that most datasets, which spoof gauges, do not touch. Each entry carries timestamp, arbitration ID, DLC, payload, and a Normal/Attack label, and a JSON metadata file documents attack windows, bus load, bitrate, and the labelling policy.

You get a 2.4 MB zip from Zenodo — CSV files plus the metadata and a README — which makes it a quick download for benchmarking lightweight or on-device IDS prototypes. Caveats: it is small and from a single low-speed platform, not a production passenger car; the tampering class is a tiny fraction of frames, so per-class metrics rest on few examples; and no licence was stated on the record page when checked.

## Status and sources

Status: **published** — a finished, versioned archival release on Zenodo (v3, March 2026). Source: the dataset's [Zenodo record](https://zenodo.org/records/17834775), checked 2026-11-01.

## Related

- [SynCAN](syncan.md) — the synthetic signal-space benchmark, also aimed at lightweight IDS comparison
- [Car Hacking Dataset](car-hacking-dataset.md) — the larger single-vehicle real-car baseline
