---
title: "Car Hacking Dataset"
summary: "HCRL captures from a Kia Soul with labelled DoS, fuzzing, and RPM and gear spoofing injections, the most widely cited baseline in CAN intrusion detection…"
type: entity
category: "Datasets"
url: "https://ocslab.hksecurity.net/Datasets/car-hacking-dataset"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "HCRL captures from a Kia Soul with labelled DoS, fuzzing, and RPM and gear spoofing injections, the most widely cited baseline in CAN intrusion detection papers."
sources:
  - url: "https://ocslab.hksecurity.net/Datasets/car-hacking-dataset"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - survival-analysis-dataset
  - can-train-and-test
  - road
---

HCRL captures from a Kia Soul with labelled DoS, fuzzing, and RPM and gear spoofing injections, the most widely cited baseline in CAN intrusion detection papers.

The Car Hacking Dataset, from Korea University's Hacking and Countermeasure Research Lab (HCRL), is the dataset the CAN intrusion-detection literature grew up on: CAN traffic logged through the OBD-II port of a real vehicle while message-injection attacks were performed against it. It ships as four attack datasets — DoS (ID 0x0000 injected every 0.3 ms), fuzzy (random IDs and payloads), and spoofing of the RPM gauge and of the drive gear — each containing 300 injection episodes of 3–5 seconds within 30–40 minutes of traffic.

Each record gives timestamp, CAN ID, DLC, the eight data bytes, and a flag marking the frame as injected (T) or normal (R), which makes it trivially easy to load — one reason it became the default baseline. The honest caveat is the flip side of that fame: the attacks are simple, periodic, and easy to detect, the traffic comes from a single vehicle, and strong results on this dataset alone say little about performance on stealthier attacks. HCRL asks users to cite the associated paper; no formal licence is stated on the page.

## Status and sources

Status: **published** — a finished static release, hosted unchanged by HCRL for years and still served from the lab's dataset pages. Source: the [HCRL dataset page](https://ocslab.hksecurity.net/Datasets/car-hacking-dataset), checked 2026-11-01.

## Related

- [Survival Analysis Dataset](survival-analysis-dataset.md) — HCRL's three-vehicle follow-up
- [can-train-and-test](can-train-and-test.md) — multi-vehicle captures for generalisation testing
- [ROAD](road.md) — the harder, verified-attack successor benchmark
