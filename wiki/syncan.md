---
uid: 01a19d3c-afe3-72c1-afd7-b11131ce54fd
title: "SynCAN"
summary: "ETAS synthetic CAN benchmark with continuous, plateau, playback, suspension, and flooding attacks in the signal space, for comparing IDS that work on…"
type: entity
category: "Datasets"
url: "https://github.com/etas/SynCAN"
status: archived
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "ETAS synthetic CAN benchmark with continuous, plateau, playback, suspension, and flooding attacks in the signal space, for comparing IDS that work on decoded signals rather than raw arbitration IDs."
sources:
  - url: "https://github.com/etas/SynCAN"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - car-hacking-dataset
  - gem-can
---

ETAS synthetic CAN benchmark with continuous, plateau, playback, suspension, and flooding attacks in the signal space, for comparing IDS that work on decoded signals rather than raw arbitration IDs.

SynCAN is ETAS's synthetic CAN dataset, released as supplementary material for the CANet paper (IEEE Access 2020): simulated traffic for ten message IDs carrying twenty physical signals between them, provided already decoded into signal values rather than raw frames. That is its niche — it benchmarks IDS that operate on signals (the input a production signal-based detector actually sees), where real-car datasets mostly offer raw IDs and payloads and leave decoding to you. Four training files contain only normal traffic for unsupervised training; six test files cover normal driving and five attack types — plateau, continuous drift, playback, suppression (an ID silenced), and flooding — each row labelled 0/1 with ID, timestamp in milliseconds, and that ID's signal values.

The data is distributed as zip files in the GitHub repository. Caveats: it is synthetic — no real vehicle, bus timing, or error behaviour behind it — and the terms are restrictive: the licence in the repository allows non-commercial use for research, teaching, and personal experimentation, explicitly not field use.

## Status and sources

Status: **archived** — ETAS has archived the GitHub repository; the release is final (last push 2020) and remains downloadable as-is. Source: the [GitHub repository](https://github.com/etas/SynCAN), checked 2026-11-01.

## Related

- [Car Hacking Dataset](car-hacking-dataset.md) — the real-vehicle raw-frame counterpart
- [GEM-CAN](gem-can.md) — a small real-vehicle dataset for lightweight IDS benchmarking
