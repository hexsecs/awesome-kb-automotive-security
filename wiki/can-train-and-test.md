---
uid: 01a19d3c-af41-7093-9e2b-aae8dc4840e7
title: "can-train-and-test"
summary: "Labelled CAN captures from four vehicles across two manufacturers with nine attack types, split into known and unknown vehicle and attack test subsets for…"
type: entity
category: "Datasets"
url: "https://bitbucket.org/brooke-lampe/can-train-and-test/src/master/"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Labelled CAN captures from four vehicles across two manufacturers with nine attack types, split into known and unknown vehicle and attack test subsets for evaluating IDS generalisation."
sources:
  - url: "https://bitbucket.org/brooke-lampe/can-train-and-test/src/master/"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - cross-vehicle-generalisation-benchmark
  - car-hacking-dataset
  - road
---

Labelled CAN captures from four vehicles across two manufacturers with nine attack types, split into known and unknown vehicle and attack test subsets for evaluating IDS generalisation.

can-train-and-test packages CAN traffic from four vehicles — a 2017 Subaru Forester, a 2016 Chevrolet Silverado, a 2011 Chevrolet Traverse, and a 2011 Chevrolet Impala — into four curated sub-datasets (set_01 to set_04), each with one training subset and four test subsets arranged as known/unknown vehicle × known/unknown attack. It exists to answer a question most CAN datasets cannot: does an IDS trained on one car still work on a different car, and on attack types it never saw? The captures are derived from the earlier can-dataset and can-ml collections rather than newly recorded for this release.

You get CSV files in a Bitbucket repository, every frame labelled 0 (attack-free) or 1 (attack); the attack type is carried by the file names rather than a per-frame label. Caveats: the binary labels mean attack-type evaluation is per-file, not per-frame; only two manufacturers are represented, both from the US market; and because the data is repackaged from older collections, its collection quirks are inherited rather than documented here.

## Status and sources

Status: **published** — a finished, curated static release; the repository is the dataset's distribution point and is not presented as an ongoing collection. Source: the dataset's [Bitbucket repository](https://bitbucket.org/brooke-lampe/can-train-and-test/src/master/), checked 2026-11-01.

## Related

- [Cross-Vehicle Generalisation Benchmark](cross-vehicle-generalisation-benchmark.md) — builds its eight-vehicle corpus partly on this dataset
- [Car Hacking Dataset](car-hacking-dataset.md) — the single-vehicle baseline this generalisation split reacts against
- [ROAD](road.md) — the other source corpus for cross-vehicle work
