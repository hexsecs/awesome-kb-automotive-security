---
title: "RAMN"
summary: "Resistant Automotive Miniature Network, a four-ECU CAN/CAN FD testbed on a single board with KiCad sources, CARLA closed-loop simulation, and use as the Car…"
type: entity
category: "Hardware Interfaces"
url: "https://github.com/ToyotaInfoTech/RAMN"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Resistant Automotive Miniature Network, a four-ECU CAN/CAN FD testbed on a single board with KiCad sources, CARLA closed-loop simulation, and use as the Car Hacking Village CTF platform."
related: [panda, owasp-automotive-emb-60, can-daq]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/ToyotaInfoTech/RAMN"
    retrieved: 2026-11-01
  - url: "https://github.com/ToyotaInfoTech/RAMN/blob/main/README.md"
    retrieved: 2026-11-01
  - url: "https://github.com/ToyotaInfoTech/RAMN/releases/tag/v2.3"
    retrieved: 2026-11-01
---

Resistant Automotive Miniature Network, a four-ECU CAN/CAN FD testbed on a single board with KiCad sources, CARLA closed-loop simulation, and use as the Car Hacking Village CTF platform.

## What it is

Toyota InfoTech's open testbed for automotive security research (Apache-2.0): not an interface to a car, but a miniature car network on one PCB — **four ECUs** (three STM32H723ZG-based ECUs playing powertrain/body roles, plus an STM32F407VG driving a display) wired onto real CAN and CAN FD buses, with a "resistant" firmware posture that makes the network a harder target than a naive bench. Hardware sources are KiCad, firmware and tooling are in the repository, and per the project it serves as a Car Hacking Village CTF platform — a network you are explicitly invited to attack.

## How it works

Each ECU runs its own firmware with realistic vehicle functions and inter-ECU traffic over both classic CAN and CAN FD. A host connects over USB (the boards present a serial/SlCAN-style path for tools like SavvyCAN-class software), and an expansion board path closes the loop with the CARLA simulator, so simulated vehicle state drives the physical ECUs and their responses feed back — hardware-in-the-loop without a vehicle. Releases are versioned (the current line is named after vehicle codenames; v2.3 "Marlow" is the latest at this check), and the repository includes build/flash tooling for all four ECUs.

## Where it fits

RAMN answers the section's standing problem — everything else here plugs into a real vehicle, where experiments have consequences — by being the vehicle, in miniature and on purpose. It is the natural target for the CAN-section tooling (injection, fuzzing, diagnostic probing) and the constructive counterpart to [panda](panda.md): panda polices what may be sent to a real car; RAMN exists so you can send anything to a fake one. The [OWASP Automotive EMB 60](owasp-automotive-emb-60.md) aimed at an adjacent teaching-platform niche with far less momentum.

## Limits and safety notes

A testbed is a model: four ECUs and two buses resemble a vehicle network without reproducing any real vehicle's message set, gateway rules, or safety interlocks, so results transfer as technique, not as vehicle findings. You supply the hardware — boards must be fabricated/assembled or obtained through the project's channels, and four-ECU flashing is a small production line of its own. "Resistant" is the project's design goal for its firmware, not a certification; treat its hardness as a research variable, not a guarantee.

## Status and sources

Checked 2026-11-01. **Active**: the repository is not archived, the latest release is v2.3 (2026-07-31), and commits continue into mid-2026. This records observed project activity, not a promise of support. Documentation claims above come from the following primary sources; no hardware was built or run for this page.

- [Upstream repository](https://github.com/ToyotaInfoTech/RAMN)
- [Upstream README](https://github.com/ToyotaInfoTech/RAMN/blob/main/README.md)
- [Release v2.3](https://github.com/ToyotaInfoTech/RAMN/releases/tag/v2.3)

## Related

- [panda](panda.md)
- [OWASP Automotive EMB 60](owasp-automotive-emb-60.md)
- [CAN-DAQ](can-daq.md)
