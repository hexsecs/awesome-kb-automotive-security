---
title: "VW_Flash"
summary: "Flashing tools for VW AG control units over UDS supporting Simos18.1/6/10 and DQ250-MQB."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/bri3d/VW_Flash"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Flashing tools for VW AG control units over UDS supporting Simos18.1/6/10 and DQ250-MQB."
related: [odxtools, pq-flasher, udsoncan, uds-seed-key, ivi-update-trust]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/bri3d/VW_Flash"
    retrieved: 2026-10-31
---

Flashing tools for VW AG control units over UDS supporting Simos18.1/6/10 and DQ250-MQB.

## What it is

A flashing toolchain for VW AG control units over ISO-TP/UDS, by bri3d.

## How it works

A Python CLI (`VW_Flash.py`) plus a wxPython GUI. It supports full
custom reflash of Continental/Siemens Simos 18.1/6 and 18.10 engine
ECUs (MQB), Temic DQ250-MQB and Bosch DQ381-MQB DSG gearboxes, and Gen5
Haldex4Motion — handling compression, encryption, and checksums
(including the ECM2→ECM3 monitoring checksums) as part of flashing. It
ships RSA-bypass/"unlock" patches for Simos 18.1/6 (SC8) and 18.10
(SCG) enabling unsigned code and calibration, plus a bench toolchain
(TC1791 CAN BSL and a Simos18 SBOOT password-recovery exploit).
Components include `sa2-seed-key`, an implementation of VW's SA2
programming-session seed/key algorithm — SA2 bytecode from the ODX
flash container is executed against the SecurityAccess seed to derive
the key (see [UDS seed/key](concepts/uds-seed-key.md)) — and
`extractodx.py`, which decrypts/decompresses Simos ODX containers
("AUDI AES" / "AUDI LZSS", and the DQ250 scheme), plus an FRF container
extractor. Interfaces: J2534 (Macchina A0/BridgeLEG, Tactrix OpenPort
2.0) and SocketCAN on Linux.

## Where it fits

Reflashing and tuning supported MQB Simos and DSG/Haldex units with
modified calibration or application software, including unlocking
RSA-protected Simos18 ECUs. [pq-flasher](pq-flasher.md) is the older,
narrower PQ-platform counterpart; VW_Flash is the maintained MQB one.

## Limits and notes

The README states J2534 support is limited to devices supporting the
STMIN_TX IOCTL and that "clones and counterfeits have mixed results";
other Simos ECUs are flashable only if RSA validation "has already been
disabled." No broader safety disclaimer appears in the checked README.
The repository carries a LICENSE file but GitHub reports its terms as
"Other (NOASSERTION)" — treat the licence as unverified.

## Related

- [odxtools](odxtools.md) — ODX work adjacent to its flash containers.
- [pq-flasher](pq-flasher.md) — PQ35 EPS flashing, the older platform.
- [udsoncan](udsoncan.md) — the UDS session layer it builds on.
- [UDS seed/key](concepts/uds-seed-key.md) — the SA2 algorithm's attack class.
- [IVI update-path trust](concepts/ivi-update-trust.md)
