---
uid: 01a19d3c-afcd-7453-9cd8-09c4a286f844
title: "ROAD"
summary: "Real ORNL Automotive Dynamometer CAN intrusion dataset with verified fuzzing, targeted ID, masquerade, and accelerator attacks captured on a dynamometer."
type: entity
category: "Datasets"
url: "https://0xsam.com/road/"
status: published
last_checked: 2026-11-17
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Real ORNL Automotive Dynamometer CAN intrusion dataset with verified fuzzing, targeted ID, masquerade, and accelerator attacks captured on a dynamometer."
related:
  - a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset
  - can-train-and-test
  - cross-vehicle-generalisation-benchmark
  - can-mirgu
  - autohack
  - car-hacking-dataset
  - cards
  - in-vehicle-intrusion-detection
sources:
  - url: "https://0xsam.com/road/"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1371/journal.pone.0296879"
    retrieved: 2026-11-17
---

Real ORNL Automotive Dynamometer CAN intrusion dataset with verified fuzzing, targeted ID, masquerade, and accelerator attacks captured on a dynamometer.

## What it is

ROAD — the **Real ORNL Automotive Dynamometer** CAN intrusion dataset — was built to fix the field's fidelity problem. The project site bills it as the first open dataset featuring real, physically verified, advanced attacks on a vehicle's CAN bus. Instead of injecting attacks into synthetic traffic or a parked car, the team ran a real passenger vehicle on a **four-wheel rolling dynamometer at Oak Ridge National Laboratory** and verified every attack physically. The site's headline numbers are **3.5 hours of CAN data, 33 attack captures, 12 ambient captures, about 30 minutes of attack duration and about 3 hours of ambient duration**.

## How it works

The taxonomy covers the three primary CAN attack categories with real and simulated variants across multiple stealth levels:

- **Fuzzing (fabrication)** — random arbitration-ID injection with maximum payload; high volume, low stealth, useful as a baseline detection test.
- **Targeted ID (fabrication)** — single-frame injection between ambient messages using "flam" delivery; the project calls this the most stealthy fabrication possible in public data.
- **Correlated signal** — four false wheel-speed values injected, causing loss of accelerator control and requiring a vehicle restart in some instances.
- **Max speedometer** — the speedometer signal set to `0xFF`, producing a false maximum-speed reading on the cluster.
- **Max engine coolant** — coolant temperature set to maximum, triggering a false overheating warning.
- **Reverse light** — a non-critical signal manipulated to demonstrate unintended light activation.
- **Accelerator (disclosed vulnerability)** — a newly discovered vulnerability enabling accelerator disabling; a real, non-simulated advanced attack unique to ROAD.
- **Masquerade (simulated)** — spoofed frames sent in place of suspended legitimate ones; the hardest detection challenge in the set.

Downloads come in two forms. Raw CAN is provided as standard **SocketCAN `.log`** files with timestamp, interface, arbitration ID and payload (for example `(1364236952.554636) vcan0 0B4#00000813000013FC`). Many captures also include **decoded physical-signal time series** — wheel speed, temperature, speedometer and so on — so signal-level IDS research does not first require reverse-engineering the car's DBC.

The authors are Miki E. Verma, Michael D. Iannacone, Robert A. Bridges, Samuel C. Hollifield, Pablo Moriano, Steven C. Hespeler, Bill Kay and Frank L. Combs. The companion paper is Verma et al., *A comprehensive guide to CAN IDS data and introduction of the ROAD dataset*, PLOS ONE (2024), DOI 10.1371/journal.pone.0296879, also on arXiv as 2012.14600. The dataset is under **Creative Commons Attribution**, produced under US Department of Energy contract DE-AC05-00OR22725, and distributed via Zenodo.

## Where it fits

ROAD is the harder successor benchmark to the [Car Hacking Dataset](car-hacking-dataset.md). [A Comprehensive Guide to CAN IDS Data and Introduction of the ROAD Dataset](a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset.md) is that companion paper at full depth in this KB, and also surveys and grades the other public CAN IDS datasets. [can-train-and-test](can-train-and-test.md) organises multi-vehicle captures for generalisation testing, and the [Cross-Vehicle Generalisation Benchmark](cross-vehicle-generalisation-benchmark.md) uses ROAD as its hardest held-out domain. [CAN-MIRGU](can-mirgu.md) and [AutoHack](autohack.md) are IDS tooling in the same space; [CARDS](cards.md) is another dataset entry.

## Limits and safety notes

The fidelity gain has boundaries: the data comes from **one anonymised vehicle**, driven on a dynamometer rather than on the road, and the masquerade variants are **simulated** rather than executed. The companion survey by Lampe and Meng records the raw ROAD logs as **unlabelled**, so detection work requires deriving labels from the attack descriptions or the decoded signal series. The attack count is also easy to misread: the project reports 33 attack *captures*, while survey papers count a smaller number of *unique attack types* by grouping variants. Neither the attacks nor the vehicle setup were reproduced for this page.

## Status and sources

Checked 2026-11-17. **Published** — a finished static release under CC BY, distributed from the project site and Zenodo.

- [ROAD project site](https://0xsam.com/road/)
- [Verma et al., PLOS ONE 2024](https://doi.org/10.1371/journal.pone.0296879)

## Related

- [A Comprehensive Guide to CAN IDS Data and Introduction of the ROAD Dataset](a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset.md) — the companion paper, at full depth
- [can-train-and-test](can-train-and-test.md) — multi-vehicle captures for generalisation testing
- [Cross-Vehicle Generalisation Benchmark](cross-vehicle-generalisation-benchmark.md) — uses ROAD as its hardest held-out domain
- [CAN-MIRGU](can-mirgu.md)
- [AutoHack](autohack.md)
- [Car Hacking Dataset](car-hacking-dataset.md)
- [CARDS](cards.md)
- [In-vehicle intrusion detection and ECU fingerprinting](concepts/in-vehicle-intrusion-detection.md)
