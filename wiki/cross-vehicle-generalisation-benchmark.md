---
title: "Cross-Vehicle Generalisation Benchmark"
summary: "Leave-one-vehicle-out benchmark unifying ROAD, CIDv2, and can-train-and-test into 217 captures across eight vehicles for evaluating whether CAN IDS models…"
type: entity
category: "Datasets"
url: "https://github.com/obaf/Cross-Vehicle-Generalisation-of-In-Vehicle-Intrusion-Detection"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Leave-one-vehicle-out benchmark unifying ROAD, CIDv2, and can-train-and-test into 217 captures across eight vehicles for evaluating whether CAN IDS models transfer."
sources:
  - url: "https://github.com/obaf/Cross-Vehicle-Generalisation-of-In-Vehicle-Intrusion-Detection"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - road
  - can-train-and-test
---

Leave-one-vehicle-out benchmark unifying ROAD, CIDv2, and can-train-and-test into 217 captures across eight vehicles for evaluating whether CAN IDS models transfer.

This repository is not a new capture but a controlled benchmark built from three public corpora — ROAD, CIDv2, and can-train-and-test — normalised into one frame schema and one attack taxonomy (DoS, fuzzing, spoofing, replay, diagnostic, suspension, masquerade, timing): 217 captures, 91.8 million messages, 13.4 hours, across eight vehicle domains. Its protocol is leave-one-vehicle-out, with detection thresholds calibrated only on the held-out vehicle's benign traffic at a stated false-alarm budget, and it ships the full evaluation — 32 detector configurations, two feature representations, results, and reproduction code — rather than just data.

It is for IDS researchers who suspect, correctly per its findings, that same-vehicle scores near 0.99 say little about transfer. Caveats: labels for some sources are reconstructed (CIDv2's by a count-aware anti-join against benign originals, suspension attacks labelled at window level), ROAD's accelerator captures are excluded for lack of per-message ground truth, and the underlying data remains governed by the source corpora's terms — the repository's own MIT licence covers the benchmark code and packaging.

## Status and sources

Status: **active** — a new, living benchmark repository (created September 2026) with the study's code, cached data, and results. Source: the [GitHub repository](https://github.com/obaf/Cross-Vehicle-Generalisation-of-In-Vehicle-Intrusion-Detection), checked 2026-11-01.

## Related

- [ROAD](road.md) — one of the three source corpora, and its hardest domain
- [can-train-and-test](can-train-and-test.md) — the source corpus supplying four of the eight vehicles
