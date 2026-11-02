---
title: "VeReMi Extension"
summary: "Simulated V2X misbehavior detection dataset generated with F2MD over the Luxembourg SUMO scenario, labelling position, speed, timing, replay, DoS, and Sybil…"
type: entity
category: "Datasets"
url: "https://github.com/josephkamel/VeReMi-Dataset"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Simulated V2X misbehavior detection dataset generated with F2MD over the Luxembourg SUMO scenario, labelling position, speed, timing, replay, DoS, and Sybil attacks alongside faulty-sensor behaviour."
sources:
  - url: "https://github.com/josephkamel/VeReMi-Dataset"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - f2md
  - misbehavior-detection
---

Simulated V2X misbehavior detection dataset generated with F2MD over the Luxembourg SUMO scenario, labelling position, speed, timing, replay, DoS, and Sybil attacks alongside faulty-sensor behaviour.

The VeReMi Extension is a simulated dataset for evaluating V2X misbehavior detection — systems that judge whether the position and speed claims in neighbouring vehicles' beacons are plausible. It extends the original VeReMi dataset using the F2MD framework over the Luxembourg SUMO traffic scenario (LuST), adding a much wider misbehavior set: position, speed, and timing falsification, replay, DoS, and Sybil attacks, alongside non-malicious faulty-sensor behaviour, so detectors can be scored on separating attackers from merely broken sensors. Like the original, it provides the received beacons with ground truth about which sender was misbehaving and how.

The GitHub repository is a landing page: the dataset itself is a linked download (MEGA), and the accompanying paper (IEEE ICC 2020) is the citation the authors ask for. Who it is for: misbehavior-detection researchers who need a comparable benchmark with many attacker types. Caveats: everything is simulated — no real radios, vehicles, or channel effects — and results on it do not by themselves establish real-world detection performance; no licence is stated in the repository.

## Status and sources

Status: **published** — a finished dataset release accompanying the ICC 2020 paper; the repository is its standing landing page. Source: the dataset's [GitHub repository](https://github.com/josephkamel/VeReMi-Dataset), checked 2026-11-01.

## Related

- [F2MD](f2md.md) — the framework that generated the dataset
- [Misbehavior detection](concepts/misbehavior-detection.md) — the concept this dataset benchmarks
