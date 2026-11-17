---
uid: 01a19d3c-af2b-7f8a-bac6-a17df9763765
title: "AutoHack"
summary: "Multi-bus CAN dataset from a real vehicle covering C-CAN, P-CAN, and B-CAN, with physically verified fuzzing, spoofing, replay, DoS, and UDS-based attacks."
type: entity
category: "Datasets"
url: "https://zenodo.org/records/19661006"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Multi-bus CAN dataset from a real vehicle covering C-CAN, P-CAN, and B-CAN, with physically verified fuzzing, spoofing, replay, DoS, and UDS-based attacks."
related:
  - can-mirgu
  - road
  - car-hacking-dataset
  - vasp
  - in-vehicle-intrusion-detection
sources:
  - url: "https://zenodo.org/records/19661006"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.5281/zenodo.20321379"
    retrieved: 2026-11-17
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
facets: [can, diagnostics, simulation, ids, attack, datasets]
---

Multi-bus CAN dataset from a real vehicle covering C-CAN, P-CAN, and B-CAN, with physically verified fuzzing, spoofing, replay, DoS, and UDS-based attacks.

AutoHack is a CAN intrusion-detection dataset recorded simultaneously from three buses of a real vehicle — chassis (C-CAN), powertrain (P-CAN), and body (B-CAN) — by Korea University and Kookmin University researchers. Most public CAN datasets capture a single bus; recording three at once lets IDS work test whether an attack visible on one bus correlates with effects on the others, and the attack set is broader than the usual injection trio: alongside fuzzing, spoofing, replay, and DoS it includes UDS-based diagnostic attacks, all physically verified in the vehicle rather than spliced into benign traffic offline.

What you get is a Zenodo download: a ~309 MB dataset archive plus a small (~31 kB) benchmark archive. The record is versioned (v3 is current). Caveats: the vehicle is a single, unnamed model, the dataset is an appendix to a paper the record describes as submitted to USENIX VehicleSec 2026 (so the accompanying analysis is not yet a published paper), and no licence was stated on the record page when checked.

## How it works

**Artifact and provenance.** The Zenodo record is a dataset publication (DOI 10.5281/zenodo.20321379, version v3, published 20 April 2026, metadata modified 21 May 2026). Six named contributors are split across two institutions: Korea University (Song, Baek, Kim as data collectors/curator) and Kookmin University (Ahn and Kim as annotators, Jeon as curator). That division is visible in the record's role labels — collection, annotation, curation are credited separately rather than to a single author list. The record associates the dataset with the 4th USENIX Symposium on Vehicle Security and Privacy (Baltimore, MD, 10–11 August 2026), names USENIX VehicleSec2026 as publisher, is indexed in OpenAIRE, and declares Python as the programming language for the accompanying material.

**The two-file delivery.** `Autohack2025_Dataset.zip` (309.1 MB) is the capture corpus; `AutoHack-Benchmark.zip` (31.5 kB) is the small benchmark bundle. The size asymmetry is the design: the heavy artifact is raw multi-bus traffic, and the benchmark is a compact, distributable slice for repeatable scoring. Both are Open Access on Zenodo; the record reports 680 views and 317 downloads (all versions) at the time of the 2026-11-17 check.

**Why three buses matter.** A single-bus capture cannot show whether a diagnostic request on one segment produces a visible reaction on another. Capturing C-CAN, P-CAN and B-CAN together makes cross-bus correlation a measurable property instead of an assumption — an IDS can be evaluated on whether an attack that starts as a UDS request on one bus shows up as an actuation or fault signature on another. This is the dataset's distinguishing shape against the KB's [Car Hacking Dataset](car-hacking-dataset.md) (one bus) and [ROAD](road.md) (one bus, dynamometer).

**The attack taxonomy.** Five classes, all physically executed in the vehicle:

- **Fuzzing** — malformed or random traffic to provoke unexpected ECU behaviour.
- **Spoofing** — impersonating a legitimate sender.
- **Replay** — re-injecting previously recorded frames.
- **DoS** — denying bus service, the layer-2 counterpart covered in [CAN availability](concepts/can-availability.md).
- **UDS-based attacks** — misuse of unified diagnostic services, the class the KB treats in [Diagnostic service abuse](concepts/diagnostic-service-abuse.md).

Including UDS is the notable choice: most public CAN IDS sets stop at injection primitives. A diagnostic-session attack is both harder to spot on rate statistics and more closely tied to a legitimate maintenance workflow.

## Where it fits

AutoHack fills the multi-bus, physically-verified niche in the KB's [in-vehicle intrusion detection](concepts/in-vehicle-intrusion-detection.md) family. [CAN-MIRGU](can-mirgu.md) is the moving-vehicle counterpart with a narrower attack set; [ROAD](road.md) supplies masquerade attacks on a dynamometer; [Car Hacking Dataset](car-hacking-dataset.md) is the single-bus baseline; and [SynCAN](syncan.md) is the synthetic, signal-space benchmark. AutoHack is the one to reach for when the research question is "what happens on the other buses?" rather than "can I detect an injected ID?"

## Limits and safety notes

The vehicle is a single unnamed model, so the three-bus topology is one example, not a fleet sample. The attacks are physically verified but the accompanying analysis was described as a submitted paper at the 2026-11-01 check; the record's conference association and 2026 publication date were confirmed on 2026-11-17, but the paper text was not read for this page. Licensing needs care: the earlier pointer recorded no licence on the record page, while the current record shows Creative Commons Attribution 4.0 — verify the terms on the record itself before reuse and do not assume the earlier observation is stale without checking. No archive was downloaded or traffic analysed for this page; all claims come from the Zenodo record metadata and the file inventory it exposes.

## Status and sources

Status: **published** — a finished, versioned archival release on Zenodo (v3, April 2026; record updated May 2026), not a living project. Source: the dataset's [Zenodo record](https://zenodo.org/records/19661006), checked 2026-11-01; DOI and file inventory re-checked 2026-11-17.

## Related

- [CAN-MIRGU](can-mirgu.md) — physically verified attacks from a moving vehicle
- [ROAD](road.md) — the dynamometer dataset with verified masquerade attacks
- [Car Hacking Dataset](car-hacking-dataset.md) — the single-bus HCRL baseline
- [In-vehicle intrusion detection and ECU fingerprinting](concepts/in-vehicle-intrusion-detection.md)
