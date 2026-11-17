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
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: ed4fb66
list_summary: "ETAS synthetic CAN benchmark with continuous, plateau, playback, suspension, and flooding attacks in the signal space, for comparing IDS that work on decoded signals rather than raw arbitration IDs."
sources:
  - url: "https://github.com/etas/SynCAN"
    retrieved: 2026-11-01
  - url: "https://raw.githubusercontent.com/etas/SynCAN/master/README.md"
    retrieved: 2026-11-17
  - url: "https://ieeexplore.ieee.org/document/9044377"
    retrieved: 2026-11-17
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - car-hacking-dataset
  - gem-can
  - survival-analysis-dataset
  - in-vehicle-intrusion-detection
  - simulation-and-test-doubles
facets: [can, simulation, ids, attack, datasets]
---

ETAS synthetic CAN benchmark with continuous, plateau, playback, suspension, and flooding attacks in the signal space, for comparing IDS that work on decoded signals rather than raw arbitration IDs.

SynCAN is ETAS's synthetic CAN dataset, released as supplementary material for the CANet paper (IEEE Access 2020): simulated traffic for ten message IDs carrying twenty physical signals between them, provided already decoded into signal values rather than raw frames. That is its niche — it benchmarks IDS that operate on signals (the input a production signal-based detector actually sees), where real-car datasets mostly offer raw IDs and payloads and leave decoding to you. Four training files contain only normal traffic for unsupervised training; six test files cover normal driving and five attack types — plateau, continuous drift, playback, suppression (an ID silenced), and flooding — each row labelled 0/1 with ID, timestamp in milliseconds, and that ID's signal values.

The data is distributed as zip files in the GitHub repository. Caveats: it is synthetic — no real vehicle, bus timing, or error behaviour behind it — and the terms are restrictive: the licence in the repository allows non-commercial use for research, teaching, and personal experimentation, explicitly not field use.

## How it works

**The paper and its benchmark.** The dataset is supplementary material for Hanselmann, Strauss, Dormann and Ulmer, *CANet: An Unsupervised Intrusion Detection System for High Dimensional CAN Bus Data*, IEEE Access 8 (2020), pp. 58194–58205. The experimental design follows from that title: train an unsupervised model on normal traffic, then measure its detection on labelled anomalies. This is why the training files carry no positive labels at all — the evaluation is deliberately about novelty detection, not supervised classification.

**The schema is the point.** Every file is a table with the columns `Label, ID, Time, Signal1_of_ID, … Signal4_of_ID`:

- `Label` is 0 for normal and 1 for intrusion. In the training data it is always 0; the column exists only so training and test files share one representation.
- `Time` is a millisecond timestamp of the current message.
- `ID` is one of `id1` … `id10` — ten simulated message IDs.
- The `SignalN_of_ID` columns hold decoded signal values. Different IDs carry different numbers of signals — the counts across `id1` … `id10` are (2, 3, 2, 1, 2, 2, 2, 1, 1, 4), twenty in total — and signal 1 of one ID is not signal 1 of another.

Because the values are already decoded, an IDS can be compared on the representation a production signal-based detector would consume, without a DBC or a reverse-engineering step. That is the deliberate trade against the raw-frame datasets in the KB's [in-vehicle intrusion detection](concepts/in-vehicle-intrusion-detection.md) family.

**Train/test split.** Four training archives (`train_1.zip` … `train_4.zip`) must be concatenated to form the full normal-training set. The six test files are:

| File | Condition |
|---|---|
| `test_normal.zip` | entirely normal traffic — a false-positive baseline |
| `test_plateau.zip` | a signal is overwritten with a constant for a period |
| `test_continuous.csv` | a signal drifts slowly away from its true value |
| `test_playback.zip` | a signal is overwritten with a recorded time series of that same signal |
| `test_suppress.zip` | an ECU is stopped, so its ID disappears from traffic (suspension) |
| `test_flooding.zip` | an existing ID is sent at high frequency |

In the five attack files, multiple attacks of that type are injected, each followed by several seconds of normal traffic; an attack targets one signal or one ID over a time interval, and during that interval **the label of all IDs is set to 1**, not just the attacked one. That labelling rule matters for scoring: a detector is judged on whether it flags the interval, not on whether it attributes the anomaly to the correct ID.

## Where it fits

SynCAN is the synthetic, signal-space benchmark — the controlled counterpart to [Car Hacking Dataset](car-hacking-dataset.md) (real vehicle, raw frames), [GEM-CAN](gem-can.md) (small real-vehicle set) and [Survival Analysis Dataset](survival-analysis-dataset.md). It is also a natural fixture for the KB's [simulation and test doubles](concepts/simulation-and-test-doubles.md) theme: the traffic is generated, so the ground truth is exact and the five attack types can be replayed deterministically. Use it to compare detectors on signal-level semantics; do not use it to claim performance on a real bus.

## Limits and safety notes

The traffic is synthetic: there is no real vehicle, bus timing, electrical behaviour or ECU implementation behind it, so detection thresholds learned here do not transfer to CAN frame timing or error frames. The licence is restrictive — free to academic and non-academic entities for non-commercial purposes such as research, teaching, scientific publication or personal experimentation/simulation, **not in the field**, explicitly because the dataset has not been tested for field use. The repository is archived on GitHub (last push 2020) and remains downloadable as-is; the IEEE paper was metadata-checked at the 2026-11-17 recheck but its full text was not re-read for this page. No archive was downloaded and no detector was run.

## Status and sources

Status: **archived** — ETAS has archived the GitHub repository; the release is final (last push 2020) and remains downloadable as-is. Source: the [GitHub repository](https://github.com/etas/SynCAN), checked 2026-11-01; README and CANet record re-checked 2026-11-17.

## Related

- [Car Hacking Dataset](car-hacking-dataset.md) — the real-vehicle raw-frame counterpart
- [GEM-CAN](gem-can.md) — a small real-vehicle dataset for lightweight IDS benchmarking
- [Survival Analysis Dataset](survival-analysis-dataset.md)
- [In-vehicle intrusion detection and ECU fingerprinting](concepts/in-vehicle-intrusion-detection.md)
- [Simulation and test doubles for vehicle networks](concepts/simulation-and-test-doubles.md)
