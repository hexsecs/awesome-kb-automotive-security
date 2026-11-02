---
uid: 01a19d3c-af51-7562-ac10-f129fb267ace
title: "Car Toolkit"
summary: "Python-based toolkit for automotive penetration testing with CAN suite, CARAL, and virtual test bench setup."
type: entity
category: "Penetration Testing"
url: "https://github.com/j-schmied/car-toolkit"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python-based toolkit for automotive penetration testing with CAN suite, CARAL, and virtual test bench setup."
related: [caringcaribou, icsim, can-utils, canhack]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/j-schmied/car-toolkit"
    retrieved: 2026-11-01
  - url: "https://github.com/j-schmied/car-toolkit/blob/main/README.md"
    retrieved: 2026-11-01
  - url: "https://github.com/j-schmied/car-toolkit/blob/main/src/can-suite/README.md"
    retrieved: 2026-11-01
  - url: "https://github.com/j-schmied/car-toolkit/blob/main/src/car-analysis/README.md"
    retrieved: 2026-11-01
---

Python-based toolkit for automotive penetration testing with CAN suite, CARAL, and virtual test bench setup.

## What it is

A small Python toolkit for automotive penetration testing, built around a virtual test bench so attacks can be developed against simulated traffic before touching hardware. It bundles two tool groups — the **CAN Suite** (CANAttack, CANReverse, CANBrute, plus a fuzzer-replay helper) and **CARAL**, a machine-learning assistant that correlates bus traffic with driver actions to reverse-engineer what messages mean — and shell scripts that set up the virtual bench and CAN interfaces. Licence: GPL-3.0.

## How it works

Per the repository's own READMEs. **CANAttack** is the offensive module: block the CAN bus (DoS), ECU imitation, replay attack, MITM filter attack (using a second interface as the man-in-the-middle bus), and reading values via OBD. Interfaces are SocketCAN (`vcan`/`can`) by default, python-can in compatibility mode, and PEAK PCAN USB(-FD) dongles, with CAN-FD targets supported via `--fd`. **CANReverse** sanitizes a candump `.log` file and replays it for manual examination. **CANBrute** brute-forces all payloads for a given arbitration ID; its README bounds this itself — suitable for lengths up to 4 bytes, "more will take literally forever". **Fuzzer Replay** replays logged output of the CaringCaribou UDS fuzzer onto an interface. **CARAL** is regression-based analysis: the tester triggers real actions in the car while CARAL records traffic, then regression associates messages with actions to infer meaning and origin ECU; its README labels CAN(-FD) support beta, Automotive Ethernet and LIN work-in-progress, and FlexRay "TbA". The scripts build the bench: `setup_vtb.sh` creates vcan0 with random traffic or the ICSim instrument-cluster simulator, and `setup_can.sh` configures SocketCAN interfaces.

## Where it fits

A bench-workflow entry: its distinguishing piece is the virtual test bench plus CARAL analysis loop rather than any single attack. It overlaps [CaringCaribou](caringcaribou.md) directly — its Fuzzer Replay consumes CaringCaribou's UDS fuzzer output — uses [ICSim](icsim.md) as its simulated cluster, and sits beside the CAN Bus Analysis section's [can-utils](can-utils.md) workflow. CANAttack's MITM and replay functions are the generic versions of techniques [CANHack](canhack.md) implements at bit level.

## Limits and safety notes

The component READMEs are candid about maturity: CARAL's non-CAN protocols and non-SocketCAN hardware are work-in-progress or "TbA", CAN(-FD) support is labelled beta, and CARAL works best under ~10 actions per cycle. CANAttack includes a bus-blocking (DoS) function — the toolkit is for a bench or a test vehicle, and the virtual-bench-first structure is the author's own mitigation. The repository gives no safety guidance beyond that design.

## Status and sources

Checked 2026-11-01. **Unknown**: the repository is not archived and there are no releases, but it was created on 2023-10-29 and all 25 commits land in a single two-day burst ending 2023-10-30. Nothing observable since the initial upload — no ongoing project state can be determined. Documentation claims above come from the following primary sources; no vehicle was connected for this page.

- [Upstream repository](https://github.com/j-schmied/car-toolkit)
- [Upstream README](https://github.com/j-schmied/car-toolkit/blob/main/README.md)
- [CAN Suite README](https://github.com/j-schmied/car-toolkit/blob/main/src/can-suite/README.md)
- [CARAL README](https://github.com/j-schmied/car-toolkit/blob/main/src/car-analysis/README.md)

## Related

- [CaringCaribou](caringcaribou.md)
- [ICSim](icsim.md)
- [can-utils](can-utils.md)
- [CANHack](canhack.md)
