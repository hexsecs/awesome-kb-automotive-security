---
uid: 01a19d3c-afe2-7fcd-9894-194d2eb5a0bf
title: "Survival Analysis Dataset"
summary: "HCRL CAN captures from a Hyundai YF Sonata, Kia Soul, and Chevrolet Spark with labelled flooding, fuzzy, and malfunction attacks."
type: entity
category: "Datasets"
url: "https://ocslab.hksecurity.net/Datasets/survival-ids"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "HCRL CAN captures from a Hyundai YF Sonata, Kia Soul, and Chevrolet Spark with labelled flooding, fuzzy, and malfunction attacks."
sources:
  - url: "https://ocslab.hksecurity.net/Datasets/survival-ids"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - car-hacking-dataset
  - syncan
---

HCRL CAN captures from a Hyundai YF Sonata, Kia Soul, and Chevrolet Spark with labelled flooding, fuzzy, and malfunction attacks.

The Survival Analysis Dataset is HCRL's multi-vehicle companion to its Car Hacking Dataset: normal and attacked CAN traffic from three different cars — a Hyundai YF Sonata, a Kia Soul, and a Chevrolet Spark — collected to develop an intrusion detector based on survival analysis of CAN ID cycle times. Three attack scenarios are covered: flooding (the bus dominated with ID 0x000), fuzzy (random IDs and payloads injected every 0.3 ms), and malfunction (a vehicle-specific target ID — 0x316, 0x153, and 0x18E respectively — whose data field is manipulated so the vehicle reacts abnormally). Attack traffic was injected for five seconds in every twenty.

The format matches the Car Hacking Dataset — timestamp, CAN ID, DLC, eight data bytes, and a T/R flag for injected versus normal frames — split into an attack-free dataset and an attack dataset per vehicle, with a summary PDF on the page. Who it is for: anyone who needs the HCRL style of data across more than one vehicle. Caveats: the fixed five-in-twenty-seconds injection rhythm is itself a learnable artefact, each vehicle contributes a single bus, and — as with the Car Hacking Dataset — no formal licence is stated; HCRL offers it for academic use with citation.

## Status and sources

Status: **published** — a finished static release, hosted unchanged on HCRL's dataset pages. Source: the [HCRL dataset page](https://ocslab.hksecurity.net/Datasets/survival-ids), checked 2026-11-01.

## Related

- [Car Hacking Dataset](car-hacking-dataset.md) — HCRL's single-vehicle predecessor and the field's default baseline
- [SynCAN](syncan.md) — the synthetic alternative for signal-space IDS work
