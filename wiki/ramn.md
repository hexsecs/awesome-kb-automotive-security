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
  - url: "https://github.com/ToyotaInfoTech/RAMN/releases/tag/v1.0.3"
    retrieved: 2026-11-01
---

Resistant Automotive Miniature Network, a four-ECU CAN/CAN FD testbed on a single board with KiCad sources, CARLA closed-loop simulation, and use as the Car Hacking Village CTF platform.

## What it is

Toyota InfoTech's open testbed for automotive security research: not an interface to a car, but a miniature car network on one PCB — **four ECUs built on STM32L5 microcontrollers** (L562CET6 / L552x family) wired onto real CAN and CAN FD buses, with KiCad hardware sources, firmware and tooling in the repository, and use as a Car Hacking Village CTF platform — a network you are explicitly invited to attack. The four ECUs have fixed roles: **A** is the gateway/USB ECU (the display is a SCREENS *expansion* attached to it, not a dedicated screen ECU), **B** is chassis, **C** is powertrain, and **D** is body. The licence picture is mixed: the repository records NOASSERTION — the non-software material is CC BY-SA 4.0 and the firmware carries its own LICENSE.md.

## How it works

Each ECU runs its own firmware with realistic vehicle functions and inter-ECU traffic over both classic CAN and CAN FD. A host connects over USB through ECU A: the classic-CAN path is slcan, a `vcand` script covers CAN FD, and release v1.0.3 added gs_usb support (alongside J1939/J1979 work) — so current firmware can also appear as a native SocketCAN device. An expansion path closes the loop with the CARLA simulator, so simulated vehicle state drives the physical ECUs and their responses feed back — hardware-in-the-loop without a vehicle. One documented safety property deserves emphasis: **the board's terminated bus cannot be connected to a real car** — the project's own documentation says so; RAMN is a standalone network, not an in-vehicle peripheral.

## Where it fits

RAMN answers the section's standing problem — everything else here plugs into a real vehicle, where experiments have consequences — by being the vehicle, in miniature and on purpose. It is the natural target for the CAN-section tooling (injection, fuzzing, diagnostic probing) and the constructive counterpart to [panda](panda.md): panda polices what may be sent to a real car; RAMN exists so you can send anything to a fake one. The [OWASP Automotive EMB 60](owasp-automotive-emb-60.md) aimed at an adjacent teaching-platform niche with far less momentum. On the name: the documentation does **not** explain "Resistant" as a firmware-hardening posture — the closest upstream text is about automotive-grade components and resistance to harsh environments — so this page records the expansion (Resistant Automotive Miniature Network) without inventing a rationale for it.

## Limits and safety notes

A testbed is a model: four ECUs and two buses resemble a vehicle network without reproducing any real vehicle's message set, gateway rules, or safety interlocks, so results transfer as technique, not as vehicle findings. You supply the hardware — boards must be fabricated/assembled or obtained through the project's channels, and four-ECU flashing is a small production line of its own. And the terminated-bus warning above is a hard limit, not boilerplate: do not wire this network into a vehicle.

## Status and sources

Checked 2026-11-01. **Active**: the repository is not archived and was most recently pushed 2026-09-04; the release line runs v1.0.0 through **v1.0.3** (2026-06-08, which added gs_usb and J1939/J1979 support). This records observed project activity, not a promise of support. Documentation claims above come from the following primary sources; no hardware was built or run for this page.

- [Upstream repository](https://github.com/ToyotaInfoTech/RAMN)
- [Upstream README](https://github.com/ToyotaInfoTech/RAMN/blob/main/README.md)
- [Release v1.0.3](https://github.com/ToyotaInfoTech/RAMN/releases/tag/v1.0.3)

## Related

- [panda](panda.md)
- [OWASP Automotive EMB 60](owasp-automotive-emb-60.md)
- [CAN-DAQ](can-daq.md)
