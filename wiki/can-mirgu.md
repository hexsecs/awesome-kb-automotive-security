---
uid: 01a19d3c-af40-7db3-bfd8-5bec8e291721
title: "CAN-MIRGU"
summary: "CAN bus attack dataset from a modern vehicle driven on real roads over six days, with physically verified masquerade, suspension, and real attacks."
type: entity
category: "Datasets"
url: "https://github.com/sampathrajapaksha/CAN-MIRGU"
status: maintenance
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: ed4fb66
list_summary: "CAN bus attack dataset from a modern vehicle driven on real roads over six days, with physically verified masquerade, suspension, and real attacks."
sources:
  - url: "https://github.com/sampathrajapaksha/CAN-MIRGU"
    retrieved: 2026-11-01
  - url: "https://raw.githubusercontent.com/sampathrajapaksha/CAN-MIRGU/main/README.md"
    retrieved: 2026-11-17
  - url: "https://www.ndss-symposium.org/ndss-paper/auto-draft-482/"
    retrieved: 2026-11-17
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - road
  - autohack
  - can-train-and-test
  - in-vehicle-intrusion-detection
---

CAN bus attack dataset from a modern vehicle driven on real roads over six days, with physically verified masquerade, suspension, and real attacks.

CAN-MIRGU is a CAN attack dataset collected from a modern vehicle with autonomous-driving capability while it was actually being driven: benign traffic spans six days of real-road driving, and the attacks were executed and physically verified in the moving vehicle. That distinguishes it from the many datasets whose attacks were injected on a bench or merged into parked-car traffic. The attack side is organised into masquerade attacks (e.g. a brake-warning masquerade), suspension attacks against specific IDs, and "real" attacks, each with a metadata file describing the runs.

The data itself is not in the GitHub repository — the repo is a landing page with a sample, an analysis PDF, and a link to the full dataset on Google Drive. Files are CAN log files plus an `Attacks_metadata.json`. Caveats: the vehicle model is not named, no licence is stated anywhere in the repository (so reuse terms are unclear), and the dataset accompanies the authors' VehicleSec 2024 paper, which is the citation they ask for.

## How it works

**The README is a manifest, not the data.** It gives three outbound links: the full dataset on Google Drive, the companion paper (listed under the NDSS symposium domain as "auto-draft-482"), and a demonstration video. Reproduction therefore depends on an external Google Drive folder; the GitHub repository holds only the structure description and sample material. The required citation is explicit: Rajapaksha, Madzudzo, Kalutarage, Petrovski and Al-Kadri, *CAN-MIRGU: A Comprehensive CAN Bus Attack Dataset from Moving Vehicles for Intrusion Detection System Evaluation*, Symposium on Vehicles Security and Privacy, Internet Society, 2024 — the VehicleSec paper attached to NDSS 2024.

**Two trees, one naming convention.** The folder structure encodes the benchmarking split:

- `Benign/Day_1/` through `Benign/Day_6/` — six days of normal traffic, each day split into numbered log files (`Benign_day1_file1.log`, …). This is the unsupervised-training pool; multiple days let an IDS be trained on normal variation rather than a single trace.
- `Attacks/` — a single `Attacks_metadata.json` plus three labelled subdirectories:

| Directory | Attack class | Example file |
|---|---|---|
| `Masquerade_attacks/` | a legitimate ID impersonated by a malicious sender | `Break_warning_masquerade_attack.log` |
| `Suspension_attacks/` | a specific ECU's messages stopped | `ID_07F_suspension_attack.log` |
| `Real_attacks/` | direct attacks on a target function | `Break_warning_attack.log` |

The metadata file is the key to supervised evaluation: it is where the run boundaries and ground truth for each attack log are recorded. A reproducible result requires pairing each `.log` with its metadata entry, not just running a detector over the whole directory.

**Why "moving vehicles" is the claim.** The paper's title and the README both stress that captures came from a car in real-world driving scenarios, with attacks physically verified — the injected frame was checked to have the intended effect on the running vehicle. That is the point of contrast with [ROAD](road.md), whose verified masquerade attacks were recorded on a dynamometer, and with [SynCAN](syncan.md), which is synthetic. The brake-warning pair is illustrative of the design: a masquerade version and a "real" attack version of the same function, so a detector can be tested on both a spoofed sender and a direct actuation.

## Where it fits

CAN-MIRGU is the moving-vehicle, real-road entry in the KB's [in-vehicle intrusion detection](concepts/in-vehicle-intrusion-detection.md) family. [AutoHack](autohack.md) is the multi-bus counterpart with a broader attack taxonomy including UDS; [ROAD](road.md) provides the controlled dynamometer setting; [can-train-and-test](can-train-and-test.md) supplies labelled captures from four vehicles; and [Car Hacking Dataset](car-hacking-dataset.md) is the single-bus HCRL baseline. Choose CAN-MIRGU when the evaluation question is whether an IDS holds up against physically verified attacks in traffic recorded while driving.

## Limits and safety notes

The vehicle model is not named anywhere in the repository, so the ID set and physical response characteristics cannot be generalised to a specific platform. No licence is stated in the repository, which leaves reuse terms unclear — check the Google Drive distribution before building on it. The full data lives on Google Drive rather than a versioned archive, so long-term availability and integrity are weaker than a DOI-backed release. The paper's link uses an `auto-draft-482` slug under the NDSS domain, which suggests a submission-stage record; the paper text was not read for this page, and the "physically verified" claim is the authors' rather than an independently reproduced result. The repository was last pushed in September 2025 and is a distribution page, not an actively maintained project.

## Status and sources

Status: **maintenance** — the dataset is complete and the repository is live but only occasionally updated (last push September 2025); it is a distribution page, not an archived release. Source: the dataset's [GitHub repository](https://github.com/sampathrajapaksha/CAN-MIRGU), checked 2026-11-01; README and companion-paper link re-checked 2026-11-17.

## Related

- [ROAD](road.md) — verified attacks, but captured on a dynamometer
- [AutoHack](autohack.md) — verified multi-bus attacks from a real vehicle
- [can-train-and-test](can-train-and-test.md) — labelled captures from four vehicles
- [In-vehicle intrusion detection and ECU fingerprinting](concepts/in-vehicle-intrusion-detection.md)
