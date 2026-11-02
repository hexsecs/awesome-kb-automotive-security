---
uid: 01a19d3c-af4d-7c6a-9ed9-01f6ad837cfd
title: "CANter"
summary: "Intrusion detection system for CAN and CAN-FD that detects drop-and-spoof attacks using frequency analysis of frame intervals."
type: entity
category: "CAN Bus Analysis"
url: "https://ceur-ws.org/Vol-3962/paper69.pdf"
status: unknown
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Intrusion detection system for CAN and CAN-FD that detects drop-and-spoof attacks using frequency analysis of frame intervals."
related: [canflict, canalyzat0r, cantot, can-availability, in-vehicle-intrusion-detection]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://ceur-ws.org/Vol-3962/paper69.pdf"
    retrieved: 2026-10-31
---

Intrusion detection system for CAN and CAN-FD that detects drop-and-spoof attacks using frequency analysis of frame intervals.

## What it is

A research intrusion detection system — a paper (ITASEC/SERICS 2025, CEUR
Vol-3962 paper 69), not a released tool. By Stefano Longari, Gregorio
Galletti, and Stefano Zanero (Politecnico di Milano) and Jan Holle (ETAS
GmbH). The paper links no public code repository; it describes a
proof of concept only, which is why this page's status stays `unknown`.

## How it works

CANter is a stand-alone monitoring node (the proof of concept uses a
Nucleo L552ZE-Q with an MCP2557FD transceiver) with two modules:

- An **FSM module** implements a custom CAN/CAN-FD controller that parses
  the bus bit by bit, follows frame-format and fault-confinement rules,
  and tracks the protected ECU's Transmit Error Counter to recognise
  bus-off (TEC = 256) and subsequent spoofed frames.
- A **frequency-analysis module** catches attackers who hide the victim's
  passive error flag (the CopyCAN evasion the paper demonstrates): it
  assumes periodic frames, watches for inter-arrival times below half the
  mean period, tests the "late-early" pattern against a 3σ Gaussian bound,
  and accumulates a TEC-like counter (over 64 means attack).

It is the defensive answer to the attack class implemented by
[CANflict](canflict.md) — see also the
[CAN injection](concepts/can-injection.md) concept page.

## Where it fits

Detecting drop-and-spoof and bus-off attacks on CAN and CAN FD without
modifying ECUs or bus topology — the niche where payload- and
timing-only IDSs are blind because the spoofed frames are well-formed.

## Limits and notes

The frequency module requires the protected ECU's frames to be periodic.
The FSM tracks TEC only (receive-error-counter rules are deliberately
excluded), and one scenario in the paper is stated to be not detectable
by CANter. Evaluation is a single bench testbed with 50 repetitions per
test — no in-vehicle validation is claimed. The paper reports all test
attacks detected with no false positives in its tests and ReCAN
evaluation; treat those as paper-reported results, not independently
verified ones.

## Related

- [CANflict](canflict.md) — the attack implementation used in CANter's own evaluation.
- [CANalyzat0r](canalyzat0r.md) — analysis tooling for the same buses.
- [canTot](cantot.md) — packaged CAN attack modules of the kind CANter aims to detect.
