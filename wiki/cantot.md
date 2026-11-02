---
uid: 01a19d3c-af4e-7a10-9dfc-8e166692edaf
title: "canTot"
summary: "Metasploit-style CAN bus exploitation framework built on sploitkit, packaging published vehicle-specific CAN attacks as selectable modules."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/shipcod3/canTot"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Metasploit-style CAN bus exploitation framework built on sploitkit, packaging published vehicle-specific CAN attacks as selectable modules."
related: [caringcaribou, carpunk, cantoolz, icsim]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/shipcod3/canTot"
    retrieved: 2026-10-31
---

Metasploit-style CAN bus exploitation framework built on sploitkit, packaging published vehicle-specific CAN attacks as selectable modules.

## What it is

A Python, Sploitkit-based console for applying already-known CAN attacks
and vehicle-specific effects. The README names Jay Turla as author and
says the project was made by Car Hacking Village Philippines.

## How it works

The workflow deliberately resembles Metasploit: `show modules`,
`use <module>`, `show options`, set values such as arbitration ID and CAN
interface, then `run`. The sample session uses `vcan0` by default. Beyond
the README's sample catalogue, the current `modules/` directory includes
candump, UDS fuzzing and Security Access, instrument-cluster fuzzers and
movers for several models, ECU reset/power modules, and vehicle-specific
spoofing or disabling modules.

## Where it fits

Reproducing published, model-specific CAN effects in an authorised lab or
training environment, and learning how exploit-framework organisation
maps to vehicle testing. The author expressly positions it as a
collection of known attacks, not a replacement for general fuzzers,
explorers, or analysers like [CaringCaribou](caringcaribou.md) or
[CANToolz](cantoolz.md).

## Limits and notes

This is the highest-risk tool in this section, and its own README says
why: sample module descriptions include bleeding a moving 2014 Cherokee's
brakes with "significant safety issues," killing a Ford Escape engine at
any speed, steering and engine-kill modules, and a Firehose
bus-denial-of-service module. Treat it as a lab-only artefact for
authorised work against [ICSim](icsim.md)-class targets and owned
vehicles on virtual interfaces — and read the module list as a catalogue
of what unauthenticated CAN access makes possible (see
[CAN injection](concepts/can-injection.md)). The README also says it
works better on Kali and Ubuntu and describes the project as "quick and
dirty."

## Related

- [CaringCaribou](caringcaribou.md) — exploration and discovery, the safer front end.
- [Carpunk](carpunk.md) — a smaller injection toolkit.
- [CANToolz](cantoolz.md) — modular black-box analysis framework.
- [ICSim](icsim.md) — the safe target for practising its workflows.
