---
uid: 01a19d3c-af2b-7f8a-bac6-a17df9763765
title: "AutoHack"
summary: "Multi-bus CAN dataset from a real vehicle covering C-CAN, P-CAN, and B-CAN, with physically verified fuzzing, spoofing, replay, DoS, and UDS-based attacks."
type: entity
category: "Datasets"
url: "https://zenodo.org/records/19661006"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Multi-bus CAN dataset from a real vehicle covering C-CAN, P-CAN, and B-CAN, with physically verified fuzzing, spoofing, replay, DoS, and UDS-based attacks."
sources:
  - url: "https://zenodo.org/records/19661006"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - can-mirgu
  - road
  - car-hacking-dataset
---

Multi-bus CAN dataset from a real vehicle covering C-CAN, P-CAN, and B-CAN, with physically verified fuzzing, spoofing, replay, DoS, and UDS-based attacks.

AutoHack is a CAN intrusion-detection dataset recorded simultaneously from three buses of a real vehicle — chassis (C-CAN), powertrain (P-CAN), and body (B-CAN) — by Korea University and Kookmin University researchers. Most public CAN datasets capture a single bus; recording three at once lets IDS work test whether an attack visible on one bus correlates with effects on the others, and the attack set is broader than the usual injection trio: alongside fuzzing, spoofing, replay, and DoS it includes UDS-based diagnostic attacks, all physically verified in the vehicle rather than spliced into benign traffic offline.

What you get is a Zenodo download: a ~309 MB dataset archive plus a small (~31 kB) benchmark archive. The record is versioned (v3 is current). Caveats: the vehicle is a single, unnamed model, the dataset is an appendix to a paper the record describes as submitted to USENIX VehicleSec 2026 (so the accompanying analysis is not yet a published paper), and no licence was stated on the record page when checked.

## Status and sources

Status: **published** — a finished, versioned archival release on Zenodo (v3, April 2026; record updated May 2026), not a living project. Source: the dataset's [Zenodo record](https://zenodo.org/records/19661006), checked 2026-11-01.

## Related

- [CAN-MIRGU](can-mirgu.md) — physically verified attacks from a moving vehicle
- [ROAD](road.md) — the dynamometer dataset with verified masquerade attacks
- [Car Hacking Dataset](car-hacking-dataset.md) — the single-bus HCRL baseline
