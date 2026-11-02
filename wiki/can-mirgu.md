---
title: "CAN-MIRGU"
summary: "CAN bus attack dataset from a modern vehicle driven on real roads over six days, with physically verified masquerade, suspension, and real attacks."
type: entity
category: "Datasets"
url: "https://github.com/sampathrajapaksha/CAN-MIRGU"
status: maintenance
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "CAN bus attack dataset from a modern vehicle driven on real roads over six days, with physically verified masquerade, suspension, and real attacks."
sources:
  - url: "https://github.com/sampathrajapaksha/CAN-MIRGU"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - road
  - autohack
  - can-train-and-test
---

CAN bus attack dataset from a modern vehicle driven on real roads over six days, with physically verified masquerade, suspension, and real attacks.

CAN-MIRGU is a CAN attack dataset collected from a modern vehicle with autonomous-driving capability while it was actually being driven: benign traffic spans six days of real-road driving, and the attacks were executed and physically verified in the moving vehicle. That distinguishes it from the many datasets whose attacks were injected on a bench or merged into parked-car traffic. The attack side is organised into masquerade attacks (e.g. a brake-warning masquerade), suspension attacks against specific IDs, and "real" attacks, each with a metadata file describing the runs.

The data itself is not in the GitHub repository — the repo is a landing page with a sample, an analysis PDF, and a link to the full dataset on Google Drive. Files are CAN log files plus an `Attacks_metadata.json`. Caveats: the vehicle model is not named, no licence is stated anywhere in the repository (so reuse terms are unclear), and the dataset accompanies the authors' VehicleSec 2024 paper, which is the citation they ask for.

## Status and sources

Status: **maintenance** — the dataset is complete and the repository is live but only occasionally updated (last push September 2025); it is a distribution page, not an archived release. Source: the dataset's [GitHub repository](https://github.com/sampathrajapaksha/CAN-MIRGU), checked 2026-11-01.

## Related

- [ROAD](road.md) — verified attacks, but captured on a dynamometer
- [AutoHack](autohack.md) — verified multi-bus attacks from a real vehicle
- [can-train-and-test](can-train-and-test.md) — labelled captures from four vehicles
