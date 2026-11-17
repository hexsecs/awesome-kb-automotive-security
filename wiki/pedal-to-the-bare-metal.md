---
uid: 01a1ba7a-e34b-754f-ab71-cefd5ac002b8
title: "Pedal to the Bare Metal"
summary: "Scharnowski and Covic, Black Hat USA 2026. Demonstrates rehosting and fuzzing the Tesla Wall Connector firmware to trigger a worm spreading via SWCAN."
type: entity
category: "Conference Presentations"
url: "https://i.blackhat.com/BH-USA-26/Presentations/US-26-Scharnowski-Pedal_to_the_Bare_Metal.pdf"
status: published
last_checked: 2026-11-17
created: 2026-11-08
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 825c8e5
list_summary: "Scharnowski and Covic, Black Hat USA 2026. Demonstrates rehosting and fuzzing the Tesla Wall Connector firmware to trigger a worm spreading via SWCAN."
related:
  - hotwire-real-world-impersonation-and-discharge-attacks-on-electric-vehicle-charging-systems
  - low-energy-to-high-energy-hacking-nearby-ev-chargers-over-bluetooth
  - a-survey-of-remote-automotive-attack-surfaces
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-08
  - url: "https://i.blackhat.com/BH-USA-26/Presentations/US-26-Scharnowski-Pedal_to_the_Bare_Metal.pdf"
    retrieved: 2026-11-17
---

Scharnowski and Covic, Black Hat USA 2026. Demonstrates rehosting and fuzzing the Tesla Wall Connector firmware to trigger a worm spreading via SWCAN.

## What it is

A Black Hat USA 2026 briefing by Tobias Scharnowski and Kristian Covic of fuzzware.io, subtitled *Rehosting and Fuzzing the Tesla Wall Connector to Start a Worm*. The talk retraces the path from "bare-metal firmware is unfuzzable" to scalable rehosting, uses the **Tesla Universal Wall Connector** as the worked example, and ends with a wormable exploit chain. The target was also an EV Charger category target at Pwn2Own Automotive '26, with a $40,000 prize and add-on prizes for a charge-connector attack.

## How it works

The Wall Connector combines an **AW-CU300** module (ARM Cortex-M4, Wi-Fi) with an **STM32**; the charge-port CP line carries **SWCAN**. The firmware is split across Boot ROM, Boot2 and two flash application slots, with more than 40 RTOS tasks. Because peripherals and hardware dependencies make it "unfuzzable" in place, the team rehosted it in three stages: get basic boot working, optimise coverage, then triage crashes. Coverage work involved skipping the `uds_get_raw_can_frame` call that reads real CAN frames, replacing the task launcher, and focusing the fuzzer on the **UDS task** rather than chasing complete coverage — a vendor-vs-attacker trade-off between completeness and efficiency.

The exploit entry point is **UDS over ISO-TP** (CAN ID `0x604`), a general-purpose diagnostic protocol with a complex firmware-upload sequence. A captured, valid transaction provided the starting point; the talk shows the frame `604 [5] 043101ff00` among the upload traffic. The bug they found is an **arbitrary write before the signature validation**, which lets them load unsigned code in place of Boot2, hook the Tesla firmware so updates cannot remove the implant, and take over the STM32 for full hardware control.

For wormability, the chain is: an attacker reaching the initial charger **via the charge plug** compromises a vehicle's infotainment unit **wirelessly**, and that infotainment unit then compromises further chargers **wirelessly**. The hardware demonstration spans multiple vendors — a Tesla Wall Connector, an Autel MaxiCharger and a ChargePoint Home Flex — and cites CVE-2025-8480, CVE-2024-23958 and CVE-2024-23959, with an Alpine iLX-F511 head unit as the Wi-Fi IVI hop and Bluetooth as the charger vector. The recommended countermeasures are scalable security testing plus hardening: disable unused interfaces, minimise the pre-authentication surface, secure boot, enforce user interaction and add exploit mitigations, so that fully autonomous "drive-by" hops are broken.

## Where it fits

This is the hardware-and-firmware end of the EV charging material. [HotWire](hotwire-real-world-impersonation-and-discharge-attacks-on-electric-vehicle-charging-systems.md) attacks the DIN 70121 protocol layer and [Low Energy to High Energy](low-energy-to-high-energy-hacking-nearby-ev-chargers-over-bluetooth.md) the Bluetooth path into chargers; [A Survey of Remote Automotive Attack Surfaces](a-survey-of-remote-automotive-attack-surfaces.md) is the broader context for the wireless hops. The rehosting method is also relevant well beyond charging hardware.

## Limits and safety notes

The source is the **official Black Hat slide deck**; exploit addresses are partly redacted and the CVE-to-device mapping is presented at a high level, so this page does not reproduce the toolchain or payload. The speakers are explicit about scope: they **demonstrated** the complete autonomous chain, multiple devices and vendors, infrastructure-to-vehicle hops, no manual steps after launch, and real devices in a lab — but **did not** demonstrate internet-wide prevalence of vulnerable versions, unrestricted propagation across arbitrary vehicles or chargers, grid destabilisation, or deployment outside the lab. The deck's own summary is "No public chargers hurt in our experiments." No charger, vehicle or firmware was tested for this page.

## Status and sources

Checked 2026-11-17. **Published** — Black Hat USA 2026; official briefing slides.

- [Black Hat USA 26 briefing slides](https://i.blackhat.com/BH-USA-26/Presentations/US-26-Scharnowski-Pedal_to_the_Bare_Metal.pdf)

## Related

- [HotWire: Real-World Impersonation and Discharge Attacks on Electric Vehicle Charging Systems](hotwire-real-world-impersonation-and-discharge-attacks-on-electric-vehicle-charging-systems.md)
- [Low Energy to High Energy: hacking nearby EV chargers over Bluetooth](low-energy-to-high-energy-hacking-nearby-ev-chargers-over-bluetooth.md)
- [A Survey of Remote Automotive Attack Surfaces](a-survey-of-remote-automotive-attack-surfaces.md)
