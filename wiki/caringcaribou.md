---
title: "CaringCaribou"
summary: "Python automotive security exploration tool designed as the nmap of CAN bus with fuzzing, ECU discovery, and attack modules."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/CaringCaribou/caringcaribou"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python automotive security exploration tool designed as the nmap of CAN bus with fuzzing, ECU discovery, and attack modules."
related: [python-can, python-can-isotp, cantoolz, canalyzat0r]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/CaringCaribou/caringcaribou"
    retrieved: 2026-10-31
---

Python automotive security exploration tool designed as the nmap of CAN bus with fuzzing, ECU discovery, and attack modules.

## What it is

A Python automotive-security exploration system designed to be placed on
an unfamiliar CAN network and discover what is there — it began in the
HEAVENS research project, funded by VINNOVA. The README lists many
contributors but does not identify one primary maintainer.

## How it works

A central CLI dispatches to drop-in modules in `caringcaribou/modules`;
shared utilities implement CAN actions, ISO-TP (ISO 15765-2), and UDS
(ISO 14229-1), using [python-can](python-can.md) underneath. The typical
documented workflow starts with `listener` to enumerate active
arbitration IDs, then uses UDS discovery and service/subservice
enumeration, followed by DID dumping, Security Access seed collection,
reset, memory-read, or fuzzing modules. Separate modules cover raw
dump/send/replay, CAN fuzzing strategies, UDS seed-randomness and delay
fuzzing, DoIP, and XCP discovery, information retrieval, and memory
dumping. The seed-collection and seed-randomness work speaks directly to
the weaknesses on the [UDS seed/key](concepts/uds-seed-key.md) page.

## Where it fits

Zero-knowledge CAN reconnaissance, UDS/DoIP/XCP attack-surface
enumeration, diagnostic-service testing, seed-randomness evaluation, and
extensible assessments where writing a new Python module is the natural
next step. [CanCat](cancat.md) is the closest alternative shape —
firmware plus interactive session instead of a module CLI.

## Limits and notes

Requirements are a CAN interface, Python 3.7 or later, python-can, and a
fairly modern Linux kernel; the documentation's worked physical example
uses a Raspberry Pi with PiCAN. The legacy `dcm` module is explicitly
deprecated in favour of `uds`. No explicit operational-safety warning was
verified in the README or usage guide checked.

## Related

- [python-can](python-can.md) and [python-can-isotp](python-can-isotp.md) — its transport stack.
- [CANToolz](cantoolz.md) — the other modular framework in this section.
- [CANalyzat0r](canalyzat0r.md) — GUI counterpart for protocol RE.
