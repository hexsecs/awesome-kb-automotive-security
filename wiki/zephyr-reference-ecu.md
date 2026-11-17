---
uid: 01a1aba1-8833-70fa-bf6d-0f3681d4fcb7
title: "Zephyr-Reference-ECU"
summary: "Forkable body control module on Zephyr with UDS diagnostics over CAN and DoIP, SecurityAccess with AES-128-CMAC, and signed firmware update, runnable with…"
type: entity
category: "Firmware and ECU Reverse Engineering"
url: "https://github.com/Xaloqi/Zephyr-Reference-ECU"
status: active
last_checked: 2026-11-17
created: 2026-11-05
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 082afab
list_summary: "Forkable body control module on Zephyr with UDS diagnostics over CAN and DoIP, SecurityAccess with AES-128-CMAC, and signed firmware update, runnable with no hardware or on a NUCLEO-H753ZI board."
related:
  - vehicle-immobilization-revisited
  - uds-firmware-extraction
  - reversing-a-brake-ecu-firmware-update
  - doip-sim-ecu-dsl
  - automotive-flash-bootloaders-exposing-automotive-ecu-updates
  - openvehiclediag
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-05
  - url: "https://github.com/Xaloqi/Zephyr-Reference-ECU"
    retrieved: 2026-11-17
  - url: "https://raw.githubusercontent.com/Xaloqi/Zephyr-Reference-ECU/main/README.md"
    retrieved: 2026-11-17
  - url: "https://api.github.com/repos/Xaloqi/Zephyr-Reference-ECU"
    retrieved: 2026-11-17
---

Forkable body control module on Zephyr with UDS diagnostics over CAN and DoIP, SecurityAccess with AES-128-CMAC, and signed firmware update, runnable with no hardware or on a NUCLEO-H753ZI board.

## What it is

Zephyr-Reference-ECU is a deliberately forkable Body Control Module application on Zephyr RTOS, with Xaloqi EDS wired in as its diagnostics layer. It boots on `native_sim` with one command and no board or licence, and also runs on a NUCLEO-H753ZI. The point is to give someone learning ECU diagnostics a real firmware target they can clone, read and modify — a "reference ECU" rather than a simulator masquerading as one. The repository's own code is Apache-2.0; EDS itself has a commercial licence boundary for regeneration and for shipping closed-source firmware.

## How it works

The application tracks four doors, a window position and a persisted actuation count, exposing them over ISO 14229 [UDS](uds.md) on CAN/ISO-TP and, in an alternate build, DoIP. Concretely: seven DIDs (VIN, serial, software version, door status, window position, door cycle count, plus a CDA-interop-only identification DID), two DTCs (door-ajar timeout and window-actuation stall), and three RoutineControl entries (`DoorLockAll`, asynchronous `WindowCalibrate`, and a self-test stub). SecurityAccess seeds come from the board's hardware RNG on real silicon (the `native_sim` build falls back to EDS's LFSR), and the unlock uses AES-128-CMAC. The cycle count survives a real hardware reset through an append-only NVM store — the upstream README documents the Zephyr NVS 16-bit sector-size mismatch on STM32H7 that forced the backend change.

DoIP is a separate entry point, never combined with CAN in one image: the README is explicit that EDS deliberately deferred building a safe shared session/security-state architecture. The DoIP build exposes routing activation, DID reads, extended session, CMAC SecurityAccess, RoutineControl and ECUReset (which needed an upstream fix to actually reset rather than just acknowledge 0x51). A secure-boot variant adds MCUboot swap, an image-policy digest gate at 0x37 and MCUboot's RSA-2048-PSS signature check at swap time — the README carefully distinguishes the digest check (catches corruption and naive tampering) from the signature check (the only thing that provides authenticity).

A third build runs the ECU as an AGL SoDeV DomZ Xen guest over DoIP or virtio-CAN. The CI does less than it might appear: the `virtual-campaign` job exercises a small built-in simulator, not this firmware, and no CI job drives the real firmware over a real bus. Every hardware claim in the README was done manually on the bench.

## Where it fits

This is the practice target for the diagnostic and firmware material elsewhere in the KB: [UDS firmware extraction](uds-firmware-extraction.md) and [automotive flash bootloaders](automotive-flash-bootloaders-exposing-automotive-ecu-updates.md) for the update path, [reversing a brake ECU firmware update](reversing-a-brake-ecu-firmware-update.md) for the analysis workflow, [DoIP sim ECU DSL](doip-sim-ecu-dsl.md) for the DoIP side, and [OpenVehicleDiag](openvehiclediag.md) as a real diagnostic client pointed at it. [Vehicle immobilization revisited](vehicle-immobilization-revisited.md) is the defensive counterpart to the SecurityAccess and routine mechanisms modelled here.

## Limits and safety notes

The licence boundary matters: building and running the pre-committed generated C is free, but editing `diagnostics_config.yaml` and regenerating `generated/` needs a commercial EDS licence (GPL-2.0 otherwise constrains closed-source firmware), and real CAN/DoIP transport in the tester needs `xaloqi-tester-pro`. The free virtual campaign's pass is not evidence about this firmware — the README says so directly. Hardware notes are equally specific: DoIP needs JP6/JP7 on, the console may enumerate as `ttyACM2` rather than `ttyACM0`, and firmware over DoIP is capped at 512 KiB including header and TLVs by MCUboot's two-slot layout. Firmware authenticity beyond the MCUboot signature check is an open upstream issue and explicitly out of scope. All of this is from the upstream README; no firmware was built or run for this page.

## Status and sources

Checked 2026-11-17. **Active** at this check: public, not archived, Apache-2.0 for the repository's own code, 2 stars, no forks, no open issues, default branch last pushed 2026-11-15. Activity does not imply a stable release.

- [Upstream README](https://raw.githubusercontent.com/Xaloqi/Zephyr-Reference-ECU/main/README.md)
- [Repository metadata](https://api.github.com/repos/Xaloqi/Zephyr-Reference-ECU)
- [Commercial notice](https://github.com/Xaloqi/Zephyr-Reference-ECU/blob/main/COMMERCIAL_NOTICE.md)

## Related

- [Vehicle immobilization revisited](vehicle-immobilization-revisited.md)
- [UDS firmware extraction](uds-firmware-extraction.md)
- [Reversing a brake ECU firmware update](reversing-a-brake-ecu-firmware-update.md)
- [DoIP sim ECU DSL](doip-sim-ecu-dsl.md)
- [Automotive flash bootloaders: exposing automotive ECU updates](automotive-flash-bootloaders-exposing-automotive-ecu-updates.md)
- [OpenVehicleDiag](openvehiclediag.md)
