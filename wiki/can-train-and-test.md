---
uid: 01a19d3c-af41-7093-9e2b-aae8dc4840e7
title: "can-train-and-test"
summary: "Labelled CAN captures from four vehicles across two manufacturers with nine attack types, split into known and unknown vehicle and attack test subsets for…"
type: entity
category: "Datasets"
url: "https://bitbucket.org/brooke-lampe/can-train-and-test/src/master/"
status: published
last_checked: 2026-11-17
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Labelled CAN captures from four vehicles across two manufacturers with nine attack types, split into known and unknown vehicle and attack test subsets for evaluating IDS generalisation."
related:
  - cross-vehicle-generalisation-benchmark
  - car-hacking-dataset
  - road
  - a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset
  - can-mirgu
  - on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems
sources:
  - url: "https://bitbucket.org/brooke-lampe/can-train-and-test/src/master/"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
  - url: "https://arxiv.org/html/2308.04972v1"
    retrieved: 2026-11-17
---

Labelled CAN captures from four vehicles across two manufacturers with nine attack types, split into known and unknown vehicle and attack test subsets for evaluating IDS generalisation.

## What it is

`can-train-and-test` is a curated CAN intrusion dataset by Brooke Lampe and Weizhi Meng of the Technical University of Denmark, published in *Computers & Security* 140 (2024), 103777, with an open arXiv version. It packages CAN traffic from **four vehicles across two manufacturers** into a train/test structure designed to answer a question most CAN datasets cannot: does an IDS trained on one car still work on a different car, and on attack types it never saw? The authors' motivation is lowering the barrier to entry for IDS research when a test vehicle is unavailable; they explicitly catalogue seven shortcomings of earlier public datasets — insufficient attack-free data, attack variation, vehicle variation, fidelity, severity, modernity and labels.

## How it works

The vehicles are a **2011 Chevrolet Impala** (sedan), **2011 Chevrolet Traverse** (full-size SUV), **2016 Chevrolet Silverado** (pickup) and **2017 Subaru Forester** (compact SUV). Test drivers were varied by age and gender. Traffic was logged at the OBD-II port; many attacks, especially spoofing ones, were performed during **live on-the-road experiments** with known physical impacts, and attacks were adapted to evade modern enhancements (the 2016 Silverado, for example, ejected the researchers from the bus when too many spoofed frames were sent too quickly, while the 2011 Impala rarely did).

There are **nine unique attack types**: denial of service; combined spoofing (double and triple); fuzzing; gear spoofing; interval; RPM spoofing (driving and accessory modes); speed spoofing (driving and accessory modes); standstill; and systematic. Because attack types can be held out, researchers can train on a subset and test on unseen attacks.

The release contains **236 CSV files, 193,241,081 lines and about 7.5 GB**, split into four sub-datasets (`set_01`–`set_04`, roughly 1.7–2.2 GB each). Each sub-dataset has one training subset and four test subsets:

- `train_01` — train the model.
- `test_01_known_vehicle_known_attack` — the easy case.
- `test_02_unknown_vehicle_known_attack` — tests cross-vehicle generalisation.
- `test_03_known_vehicle_unknown_attack` — tests unseen-attack generalisation.
- `test_04_unknown_vehicle_unknown_attack` — both held out.

Every frame is labelled **0 (attack-free) or 1 (attack)**; the attack type is carried by the file name rather than a per-frame label. Replayable `.log` files as well as labelled and unlabelled `.csv` files are provided. The dataset was curated from the authors' earlier `can-dataset`, `can-log` and `can-ml` repositories, with validation steps covering log-file validation and standardisation, conversion to CSV, CSV standardisation and labelling, and sub-dataset curation. The paper includes a benchmark of **seven model families and eighteen models**, spanning supervised/unsupervised and traditional/deep learning.

## Where it fits

This is the generalisation-testing dataset, sitting between the single-vehicle [Car Hacking Dataset](car-hacking-dataset.md) and the physically verified [ROAD](road.md). The [Cross-Vehicle Generalisation Benchmark](cross-vehicle-generalisation-benchmark.md) builds an eight-vehicle corpus partly on this data. [A Comprehensive Guide to CAN IDS Data and Introduction of the ROAD Dataset](a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset.md) surveys and grades it alongside the other public datasets; [CAN-MIRGU](can-mirgu.md) is IDS tooling in the same area, and [on the real-world applicability of automotive CAN intrusion detection systems](on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems.md) asks the practical-transfer question.

## Limits and safety notes

The binary per-frame labels mean **attack-type evaluation is per-file, not per-frame**: the type comes from the filename, so mixing attack files changes what a label means. Only **two manufacturers**, both US-market vehicles, are represented, so "unknown vehicle" results are a narrow test of generalisation. Because the data is repackaged from older collections, their collection quirks are inherited rather than re-documented here. The Bitbucket repository itself did not render text when checked, so the structural and quantitative details above come from the authors' primary arXiv paper rather than the repository README. No frames were replayed or models trained for this page.

## Status and sources

Checked 2026-11-17. **Published** — a finished, curated static release; the Bitbucket repository is the distribution point and is not presented as an ongoing collection.

- [Dataset repository on Bitbucket](https://bitbucket.org/brooke-lampe/can-train-and-test/src/master/)
- [Lampe and Meng, arXiv:2308.04972](https://arxiv.org/html/2308.04972v1)

## Related

- [Cross-Vehicle Generalisation Benchmark](cross-vehicle-generalisation-benchmark.md) — builds its eight-vehicle corpus partly on this dataset
- [Car Hacking Dataset](car-hacking-dataset.md) — the single-vehicle baseline this generalisation split reacts against
- [ROAD](road.md) — the other source corpus for cross-vehicle work
- [A Comprehensive Guide to CAN IDS Data and Introduction of the ROAD Dataset](a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset.md)
- [CAN-MIRGU](can-mirgu.md)
- [On the real-world applicability of automotive CAN intrusion detection systems](on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems.md)
