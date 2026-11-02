---
title: "TruckDevil"
summary: "Framework for assessing heavy-vehicle ECUs that communicate over J1939, with ECU discovery, message reading and sending, and a J1939 fuzzer, running on a…"
type: entity
category: "Penetration Testing"
url: "https://github.com/LittleBlondeDevil/TruckDevil"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Framework for assessing heavy-vehicle ECUs that communicate over J1939, with ECU discovery, message reading and sending, and a J1939 fuzzer, running on a Macchina M2 or any python-can interface."
related: [nullsec-carfuzz, canarchy, expanding-the-attack-scenarios-of-sae-j1939-a-comprehensive-analysis-of-established-and-novel-vulnerabilities-in-transport-protocol, diagnostic-fuzzing]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/LittleBlondeDevil/TruckDevil"
    retrieved: 2026-11-01
---

Framework for assessing heavy-vehicle ECUs that communicate over J1939, with ECU discovery, message reading and sending, and a J1939 fuzzer, running on a Macchina M2 or any python-can interface.

## What it is

A Python framework for interacting with and assessing ECUs on heavy vehicles — trucks and other SAE J1939 equipment — over CAN. Where most of this KB's tooling assumes passenger-car diagnostics, TruckDevil is built around J1939's PGN addressing and the heavy-duty world: it provides an interactive shell, a small set of built-in assessment modules, and a plugin system for adding vehicle- or test-specific modules. Licence: GPL-3.0.

## How it works

An interactive CLI (`truckdevil`) or single-shot command-line invocation: devices are added with `add_device`, modules run with `run_module`, and the same commands chain in one invocation for scripted use. Built-in modules are `ecu_discovery`, `read_messages`, `send_messages`, and `j1939_fuzzer`. Message display can be upgraded with the optional `pretty_j1939` integration, rendering decoded PGN, source and destination fields from a J1939 database JSON. Hardware: built on python-can, so any python-can-supported interface works (SocketCAN included); the recommended interface is the Macchina M2 (Under-the-Dash), which needs the repository's `m2_sketch` firmware flashed via Arduino IDE. An OBD-II-to-J1939 Deutsch 9-pin adapter or splitter may also be needed to physically reach the bus. A virtual CAN device supports hardware-free use, and the test suite runs on vcan with no hardware required. Extensibility is first-class, in three forms: built-in modules, user modules dropped into a config directory, and installed Python packages registering the `truckdevil.modules` entry point, all over a documented `j1939.py` API. Distribution is via `uv tool install truckdevil` / `pip install truckdevil` per the README, or from a git clone.

## Where it fits

The heavy-vehicle anchor of the section, and of the KB: J1939 appears elsewhere mostly as research literature (e.g. [expanding-the-attack-scenarios-of-sae-j1939-a-comprehensive-analysis-of-established-and-novel-vulnerabilities-in-transport-protocol](expanding-the-attack-scenarios-of-sae-j1939-a-comprehensive-analysis-of-established-and-novel-vulnerabilities-in-transport-protocol.md)), while TruckDevil is the runnable tooling. Its fuzzer overlaps one mode of [NullSec CarFuzz](nullsec-carfuzz.md) — which lists J1939 in its USAGE.md only — but is purpose-built for PGN semantics rather than generic frames. For J1939 message decoding and general CAN work on the analysis side it complements [CANarchy](canarchy.md).

## Limits and safety notes

J1939 only: nothing here addresses passenger-car UDS/OBD-II workflows beyond sharing a CAN bus, and the framework assumes the tester can physically connect to the truck's diagnostic connector. The README carries no safety or authorisation section; the framework sends arbitrary messages and fuzzes production-bus protocols, so the bench-vs-vehicle judgement is the operator's, and the fuzzer's own technique is not described beyond its existence as a module. Release hygiene is loose: there are no GitHub releases or tags, so the installable package state has to be taken from the package index rather than GitHub.

## Status and sources

Checked 2026-11-01. **Active**: the repository is not archived; created 2020-02-20, it has 134 commits with the latest on 2026-09-05 — under two months before this check — with recent work visibly modernising packaging (uv support, `pyproject.toml`, plugin entry points, CI workflows). There are no GitHub releases or tags. Documentation claims above come from the following primary sources; no truck was connected for this page.

- [Upstream repository](https://github.com/LittleBlondeDevil/TruckDevil)

## Related

- [NullSec CarFuzz](nullsec-carfuzz.md)
- [CANarchy](canarchy.md)
- [expanding-the-attack-scenarios-of-sae-j1939-a-comprehensive-analysis-of-established-and-novel-vulnerabilities-in-transport-protocol](expanding-the-attack-scenarios-of-sae-j1939-a-comprehensive-analysis-of-established-and-novel-vulnerabilities-in-transport-protocol.md)
