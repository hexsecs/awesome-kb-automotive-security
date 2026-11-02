---
uid: 01a19d3c-afcd-7453-9cd8-09c4a286f844
title: "ROAD"
summary: "Real ORNL Automotive Dynamometer CAN intrusion dataset with verified fuzzing, targeted ID, masquerade, and accelerator attacks captured on a dynamometer."
type: entity
category: "Datasets"
url: "https://0xsam.com/road/"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Real ORNL Automotive Dynamometer CAN intrusion dataset with verified fuzzing, targeted ID, masquerade, and accelerator attacks captured on a dynamometer."
sources:
  - url: "https://0xsam.com/road/"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset
  - can-train-and-test
  - cross-vehicle-generalisation-benchmark
---

Real ORNL Automotive Dynamometer CAN intrusion dataset with verified fuzzing, targeted ID, masquerade, and accelerator attacks captured on a dynamometer.

ROAD (Real ORNL Automotive Dynamometer) is the CAN intrusion dataset built to fix the field's fidelity problem: instead of attacks simulated in synthetic traffic or injected into a parked car, every attack was executed against a real passenger vehicle running on a four-wheel rolling dynamometer at Oak Ridge National Laboratory and physically verified — the accelerator attack, from a vulnerability the team discovered, genuinely disabled the accelerator. The taxonomy spans fabrication (fuzzing, and targeted-ID "flam" injections), signal-level attacks (false wheel speeds, maximum speedometer and coolant readings, reverse-light activation), and masquerade attacks, in real and simulated variants at several stealth levels.

Downloads from the project site come as raw SocketCAN log files, and for many captures also as decoded physical-signal time series, so signal-level IDS work does not first require reverse-engineering the car's DBC. The dataset is released under Creative Commons Attribution. Caveats: one anonymised vehicle, driven on a dynamometer rather than the road, and the masquerade variants are simulated rather than performed. The companion guide paper — which also surveys and grades the other public CAN IDS datasets — has its own full page in this KB.

## Status and sources

Status: **published** — a finished static release under CC BY, distributed from the project site. Sources: the [ROAD project site](https://0xsam.com/road/) and Verma et al., PLOS ONE 2024 (DOI 10.1371/journal.pone.0296879), checked 2026-11-01.

## Related

- [A Comprehensive Guide to CAN IDS Data and Introduction of the ROAD Dataset](a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset.md) — the companion paper, at full depth
- [can-train-and-test](can-train-and-test.md) — multi-vehicle captures for generalisation testing
- [Cross-Vehicle Generalisation Benchmark](cross-vehicle-generalisation-benchmark.md) — uses ROAD as its hardest held-out domain
