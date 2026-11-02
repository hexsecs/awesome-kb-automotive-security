---
title: "ICSim"
summary: "Instrument Cluster Simulator for safe CAN bus security testing with virtual dashboard controls."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/zombieCraig/ICSim"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Instrument Cluster Simulator for safe CAN bus security testing with virtual dashboard controls."
related: [can-utils, carpunk, cantoolz, caringcaribou, simulation-and-test-doubles]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/zombieCraig/ICSim"
    retrieved: 2026-10-31
---

Instrument Cluster Simulator for safe CAN bus security testing with virtual dashboard controls.

## What it is

A SocketCAN instrument-cluster simulator attributed in its README to
OpenGarages; the repository is `zombieCraig/ICSim`. It is the safe
practice target several other tools in this section point at.

## How it works

Two C programs cooperate over the same CAN interface. `controls` emits
frames corresponding to game-controller-style inputs, while `icsim`
listens for the relevant frames and updates an SDL-rendered dashboard.
For training, the supplied sample traffic provides background bus noise.
Starting the simulator with `-r` randomises the target arbitration IDs
and payload positions and prints a seed; passing the same seed to
`controls -s` keeps the pair synchronised. Difficulty level 2 adds
further randomisation within the target arbitration ID.

## Where it fits

Safe CAN-training exercises: learning to identify control frames among
background traffic, and providing a repeatable target for sniffing,
replay, and for tools like [CaringCaribou](caringcaribou.md),
[CANToolz](cantoolz.md), or [Carpunk](carpunk.md) — all on `vcan0`, with
no vehicle involved. [CANdevStudio](candevstudio.md) is the step up when
the simulated ECU needs custom behaviour rather than a dashboard.

## Limits and notes

Building requires SDL2, SDL2_Image, and [can-utils](can-utils.md); the
README's troubleshooting section specifically covers missing `canplayer`,
controller-window focus, architecture-mismatched `lib.o`, and SDL-related
"Bad address" failures. Randomised exercises do not work as intended
unless the simulator and controls receive the same seed.

## Related

- [can-utils](can-utils.md) — capture and replay against it.
- [Carpunk](carpunk.md) — menu-led exercises that target it safely.
- [CANToolz](cantoolz.md) — analysis framework with VIRCar as its own variant.
- [CaringCaribou](caringcaribou.md) — discovery workflows to practise on it.
