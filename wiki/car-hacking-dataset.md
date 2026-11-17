---
uid: 01a19d3c-af50-7c6f-8d58-906ea9d6e173
title: "Car Hacking Dataset"
summary: "HCRL captures from a Kia Soul with labelled DoS, fuzzing, and RPM and gear spoofing injections, the most widely cited baseline in CAN intrusion detection…"
type: entity
category: "Datasets"
url: "https://ocslab.hksecurity.net/Datasets/car-hacking-dataset"
status: published
last_checked: 2026-11-17
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "HCRL captures from a Kia Soul with labelled DoS, fuzzing, and RPM and gear spoofing injections, the most widely cited baseline in CAN intrusion detection papers."
related:
  - survival-analysis-dataset
  - can-train-and-test
  - road
  - autohack
  - on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems
  - gem-can
  - a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset
sources:
  - url: "https://ocslab.hksecurity.net/Datasets/car-hacking-dataset"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
  - url: "https://arxiv.org/html/2308.04972v1"
    retrieved: 2026-11-17
---

HCRL captures from a Kia Soul with labelled DoS, fuzzing, and RPM and gear spoofing injections, the most widely cited baseline in CAN intrusion detection papers.

## What it is

The Car-Hacking Dataset is published by the **Hacking and Countermeasure Research Lab (HCRL)** at Korea University. It is CAN traffic logged through the OBD-II port of a real vehicle while message-injection attacks were performed against it, released specifically to foster car security research. HCRL describes CAN as the de facto in-vehicle network and message injection as the representative attack type — fabricated messages that deceive original ECUs or cause malfunctions.

It became the dataset the CAN intrusion-detection literature grew up on: a later survey in the [can-train-and-test](can-train-and-test.md) paper records it, citing Rajapaksha et al., as the most widely used dataset for evaluating CAN IDSs.

## How it works

The release comprises four attack datasets plus an attack-free capture:

- **DoS** — messages with CAN ID `0x000` injected every **0.3 ms**; HCRL notes `0000` is the most dominant ID.
- **Fuzzy** — messages with totally random CAN ID and DATA values injected every **0.5 ms**.
- **Spoofing the drive gear** — messages on the CAN ID related to gear information injected every **1 ms**.
- **Spoofing the RPM gauge** — messages on the CAN ID related to RPM information injected every **1 ms**.
- **Attack-free (normal)** — baseline traffic.

Each dataset contains **300 intrusions**, each lasting **3–5 seconds**, within **30–40 minutes** of total CAN traffic. Every record has twelve attributes: timestamp (seconds), CAN ID (hex, e.g. `043f`), DLC (0–8), the eight data bytes `DATA[0]`–`DATA[7]`, and a **Flag** of `T` for an injected message or `R` for a normal one. That per-frame flag is what makes the dataset trivially loadable for supervised IDS work.

HCRL asks academic users to cite the associated paper. Two are listed: Song, Woo and Kim, *In-vehicle network intrusion detection using deep convolutional neural network*, Vehicular Communications 21 (2020), 100198; and Seo, Song and Kim, *GIDS: GAN based Intrusion Detection System for In-Vehicle Network*, PST 2018 — with a note that errors were found in Table 2 of the original PST version and corrected in the arXiv version. The lab's contact for the dataset is Huy Kang Kim.

## Where it fits

This is the baseline that later datasets were designed to improve on. [Survival Analysis Dataset](survival-analysis-dataset.md) is HCRL's own three-vehicle follow-up; [can-train-and-test](can-train-and-test.md) supplies equivalent attacks across four vehicles specifically so generalisation can be measured; [ROAD](road.md) supplies physically verified attacks against a vehicle on a dynamometer. [A Comprehensive Guide to CAN IDS Data and Introduction of the ROAD Dataset](a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset.md) grades this dataset alongside the others, and [on the real-world applicability of automotive CAN intrusion detection systems](on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems.md) asks whether strong IDS results on data like this transfer to practice. [AutoHack](autohack.md) and [GEM-CAN](gem-can.md) are other entries in the same IDS-tooling neighbourhood.

## Limits and safety notes

The attacks are simple, periodic and easy to detect, and all traffic comes from a **single vehicle** — strong results here say little about stealthier injections or other car models. The can-train-and-test survey records that the vehicle was **parked with the engine running** during collection, which limits fidelity for driving-state detection. There is also a source discrepancy worth flagging: the KB summary and much secondary literature describe the vehicle as a Kia Soul, while the can-train-and-test survey's comparison table records the HCRL Car-Hacking Dataset as using a Hyundai YF Sonata; HCRL's own page does not name the vehicle, so this page does not resolve it. HCRL says the data is released "for academic purposes" and asks for a citation, but states **no formal licence**. No attacks were reproduced for this page.

## Status and sources

Checked 2026-11-17. **Published** — a static release hosted by HCRL for years and still served from its dataset pages.

- [HCRL Car-Hacking Dataset page](https://ocslab.hksecurity.net/Datasets/car-hacking-dataset)
- [Lampe and Meng, can-train-and-test (survey of datasets and collection conditions)](https://arxiv.org/html/2308.04972v1)

## Related

- [Survival Analysis Dataset](survival-analysis-dataset.md) — HCRL's three-vehicle follow-up
- [can-train-and-test](can-train-and-test.md) — multi-vehicle captures for generalisation testing
- [ROAD](road.md) — the harder, verified-attack successor benchmark
- [AutoHack](autohack.md)
- [On the real-world applicability of automotive CAN intrusion detection systems](on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems.md)
- [GEM-CAN](gem-can.md)
- [A Comprehensive Guide to CAN IDS Data and Introduction of the ROAD Dataset](a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset.md)
