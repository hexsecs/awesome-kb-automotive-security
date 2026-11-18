---
uid: 01a19d3c-afa0-7cae-af68-9dc5b2f6ee55
title: "ICSim"
summary: "Instrument Cluster Simulator for safe CAN bus security testing with virtual dashboard controls."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/zombieCraig/ICSim"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Instrument Cluster Simulator for safe CAN bus security testing with virtual dashboard controls."
related:
  - can-utils
  - carpunk
  - cantoolz
  - caringcaribou
  - simulation-and-test-doubles
  - uds-server
  - udsim
  - opengarages
  - car-toolkit
  - can-commander
  - canalyzat0r
  - candevstudio
  - cantot
  - can-injection
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/zombieCraig/ICSim"
    retrieved: 2026-10-31
facets: [can, simulation, tools]
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

The [README](https://github.com/zombieCraig/ICSim), checked 2026-11-17,
documents a Linux virtual-bus setup: load the CAN and vcan modules,
create `vcan0`, and bring the interface up. Both applications receive
that interface name as an argument. With default settings, `./icsim vcan0`
and `./controls vcan0` share hard-coded mappings, so no physical CAN
adapter or vehicle is needed to observe the relationship between controls,
frames, and display changes. Keep the controls window focused for input.

A useful training progression is to confirm that default controls work,
capture a baseline, and then change only one control while watching the
traffic. Replay the supplied generic recording to add unrelated frames,
then repeat with randomisation enabled. Preserve the printed seed with
the capture: it ties a particular exercise's mappings to the matching
controls invocation. At difficulty level 2, additional changing data
shares the target arbitration ID, so identifying the ID alone no longer
isolates the meaningful bytes. The exercise is about discriminating
relevant payload changes, not merely spotting a new identifier.

The current README documents a Meson build after installing SDL
dependencies. Its training path uses recorded CAN traffic and canplayer,
not a DBC-based vehicle model or a diagnostic service description.
An observed dashboard response supplies immediate feedback for an
injection experiment, while a saved capture supports repeating the
same analysis later.

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

This is a deliberately small training target, not evidence of real ECU
timing, physical-layer faults, gateway policy, or UDS behaviour. Success
against its dashboard does not validate a technique against a vehicle,
and virtual-bus results do not measure hardware arbitration or bus load
under real electrical conditions.

## Related

- [can-utils](can-utils.md) — capture and replay against it.
- [Carpunk](carpunk.md) — menu-led exercises that target it safely.
- [CANToolz](cantoolz.md) — analysis framework with VIRCar as its own variant.
- [CaringCaribou](caringcaribou.md) — discovery workflows to practise on it.

[Simulation and test doubles](concepts/simulation-and-test-doubles.md)
explains that fidelity boundary; [CAN injection](concepts/can-injection.md)
places replay and crafted frames within the broader attack model.
