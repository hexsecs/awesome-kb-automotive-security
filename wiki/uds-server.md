---
title: "uds-server"
summary: "UDS ECU simulator and fuzzer for use alongside ICSim, for practising diagnostic command discovery and fuzzing scan tools."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/zombieCraig/uds-server"
status: maintenance
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "UDS ECU simulator and fuzzer for use alongside ICSim, for practising diagnostic command discovery and fuzzing scan tools."
related: [udsim, icsim, caringcaribou, simulation-and-test-doubles]
license: "GPL-2.0"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/zombieCraig/uds-server"
    retrieved: 2026-10-31
---

UDS ECU simulator and fuzzer for use alongside ICSim, for practising diagnostic command discovery and fuzzing scan tools.

## What it is

A CAN UDS ECU simulator and fuzzer, written as a companion to ICSim for
training, by Craig Smith (zombieCraig) / OpenGarages. GPL-2.0.

## How it works

A single C program run against a SocketCAN interface (`vcan0` for
training, `can0` for real tools). It plays the vehicle/ECU: answers
TesterPresent with generic OKs, serves VIN reads (with a correctly
calculated VIN checksum) and DTCs, and handles some OEM-specific
services — the examples show GM Read Data by ID and Device Control,
which is how the README demonstrates extracting a door-unlock command
from a GM TechII. Fuzzing is graduated: repeated `-z` raises the level,
from randomised VINs/DTCs up to oversized/binary VINs and hundreds of
DTCs; `-c` limits fuzzing to data (not ISO-TP), `-F` disables flow
control and functional addressing, `-V` sets the reported VIN. For
dealership-tool work the README describes a bench "ODB GW" — a two-port
OBD-II bridge putting the tool and the simulator on one small CAN
network.

## Where it fits

Training and bench work where a fake ECU must satisfy — or deliberately
missatisfy — a real dealership or scan tool: reversing what the tool
sends, and fuzzing the tool's input validation. It pairs with
[ICSim](icsim.md) as that simulator's diagnostic half, and
[CaringCaribou](caringcaribou.md) is the natural client to point at it.

## Limits and notes

In the README's own words, this version "is still considered 'alpha'";
the fuzzing "is still in a Proof of Concept (PoC) stage"; new ECU
modules "need to be added by hand" in the C code, with configuration
and debug still hard-coded. Status `maintenance`: not archived, but
only a handful of commits since 2015. [UDSim](udsim.md) is its
author's rewrite.

## Related

- [UDSim](udsim.md) — the graphical rewrite of this simulator.
- [ICSim](icsim.md) — the cluster simulator it was written to accompany.
- [CaringCaribou](caringcaribou.md) — discovery tooling to exercise against it.
