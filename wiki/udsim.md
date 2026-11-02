---
title: "UDSim"
summary: "UDS (Unified Diagnostic Services) ECU simulator and fuzzer for discovering and testing UDS services."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/zombieCraig/UDSim"
status: maintenance
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "UDS (Unified Diagnostic Services) ECU simulator and fuzzer for discovering and testing UDS services."
related: [uds-server, icsim, can-utils, simulation-and-test-doubles]
license: "GPL-3.0"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/zombieCraig/UDSim"
    retrieved: 2026-10-31
---

UDS (Unified Diagnostic Services) ECU simulator and fuzzer for discovering and testing UDS services.

## What it is

UDSim — a graphical UDS simulator and fuzzer by zombieCraig (Craig
Smith). The README states it is "a complete rewrite of uds-server."
GPL-3.0.

## How it works

A C++/SDL GUI run against a CAN interface, with three modes.
**Learning:** passively discovers UDS-capable modules from live traffic
(or from a candump log via `-l`) over ISO-TP — no prior vehicle
knowledge needed — and saves what it learned as an INI-style config
(sections keyed by hex CAN ID, responder/positive/negative IDs,
recorded packets in can-utils format). **Simulation:** replays the
learned modules so diagnostic tools behave as if attached to the real
car; per-module "Fake Responses" synthesises standard-UDS replies
(default or random values) for requests never observed, and "Ignore"
silences a module. **Attack:** a built-in response fuzzer (levels 0–4,
only 0 and 1 functional) plus export of learned data to Peach Fuzzer
(`fuzz_can.xml`).

## Where it fits

Learning a real vehicle's UDS behaviour once, then re-simulating that
vehicle on the bench — training, tool testing, and repeatable attack
demos without the car. Where [uds-server](uds-server.md) is hand-coded
per ECU, UDSim is record-and-replay; where
[doip-sim-ecu-dsl](doip-sim-ecu-dsl.md) is declarative, UDSim is
observational.

## Limits and notes

The README's own caveats: simulation "won't make up traffic it has
never seen"; "consider the Attack mode very alpha"; fuzz levels 2–4
are TBD and some UI fuzzing widgets "currently do not do anything"; a
documented Mono bug in the CAN publisher can mark the socket unwritable
(a 0-byte write check), which is why the Peach export path is "in a
hold state." Status `maintenance`: fully documented, but no pushes
since 2022-12-10 in the checked sources.

## Related

- [uds-server](uds-server.md) — its predecessor, hand-coded simulation.
- [ICSim](icsim.md) — the cluster-side simulator from the same author.
- [can-utils](can-utils.md) — the capture format its learning mode reads.
