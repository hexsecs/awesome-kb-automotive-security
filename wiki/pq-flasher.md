---
uid: 01a19d3c-afbd-7065-9a78-29962753261f
title: "pq-flasher"
summary: "Python tools for reflashing VW PQ35 EPS using TP 2.0 transport layer and KWP2000 diagnostics."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/I-CAN-hack/pq-flasher"
status: maintenance
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python tools for reflashing VW PQ35 EPS using TP 2.0 transport layer and KWP2000 diagnostics."
related: [vw-flash, python-can, cancat, firmware-acquisition, secure-firmware-updates]
license: "MIT"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/I-CAN-hack/pq-flasher"
    retrieved: 2026-10-31
---

Python tools for reflashing VW PQ35 EPS using TP 2.0 transport layer and KWP2000 diagnostics.

## What it is

Tools to reflash the electric power steering (EPS) ECU of VW
PQ35-platform cars, by I-CAN-hack (Willem Melching; the README points
to his blog series for reference). MIT-licensed.

## How it works

Three Python scripts form the pipeline: `01_dump.py` dumps firmware and
calibration via CCP (a direct connection to the EPS is required; the
OBD-II gateway blocks the CCP addresses), `02_patcher.py` patches
calibration values (minimum speed 0 km/h, HCA timer) and fixes
checksums after verifying the firmware version string and existing
values, and `03_flasher.py` writes back — by default only the changed
calibration area rather than the whole image. Underneath sit reusable
`tp20.py` (VW TP 2.0 transport) and `kwp2000.py` (KWP2000 diagnostics)
libraries. Transport hardware: a comma.ai panda is required for CAN
communication.

## Where it fits

Patching and reflashing PQ35 EPS calibration (lane-assist/HCA
behaviour is the worked example) on a bench or directly connected
steering ECU, and as a reference TP 2.0/KWP2000 implementation.
[VW_Flash](vw-flash.md) covers the newer MQB platform generation.

## Limits and notes

The README's warnings are explicit and unusually complete: "THIS IS AT
YOUR OWN RISK"; changes "can lose power steering, or the steering motor
may put large amounts of torque on the wheel unexpectedly"; "This may
brick your EPS"; the author tested only on a 2010 VW Golf with 2501
firmware (reports of success on 3501); patches "should be tested on a
spare ECU first"; whole-file flashing is not recommended. Status
`maintenance`: few commits, no releases, no dated activity in the
checked sources since the 2021 creation era.

## Related

- [VW_Flash](vw-flash.md) — the MQB-generation flashing toolchain.
- [python-can](python-can.md) — CAN transport via the panda interface.
- [CanCat](cancat.md) — interactive CAN session work on the same generation of hardware.
