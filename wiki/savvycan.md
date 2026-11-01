---
title: "SavvyCAN"
summary: "Cross-platform Qt-based CAN bus reverse engineering and capture tool with DBC file loading, UDS scanning, and fuzzing support."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/collin80/SavvyCAN"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Cross-platform Qt-based CAN bus reverse engineering and capture tool with DBC file loading, UDS scanning, and fuzzing support."
related: [can-utils, lindwurm, canalyzat0r, cantools]
license: MIT
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/collin80/SavvyCAN"
    retrieved: 2026-10-31
  - url: "https://www.savvycan.com/docs/uds_scanner.html"
    retrieved: 2026-10-31
---

Cross-platform Qt-based CAN bus reverse engineering and capture tool with DBC file loading, UDS scanning, and fuzzing support.

## What it is

A Qt-based cross-platform CAN analysis tool for visualisation, reverse
engineering, debugging, and capture, by Collin Kidder (`collin80`),
MIT-licensed. It is now Qt6-based.

## How it works

A central frame list/model holds captured or loaded frames in many
formats: GVRET native, CRTD, BusMaster, Microchip, Vector trace, IXXAT,
CAN-DO, and Vehicle Spy, plus read-only candump/Kayak, PCAN, and
Wireshark PCAP. Capture hardware is either GVRET devices (CANDue
recommended) or any Qt SerialBus driver (SocketCAN, Vector, PeakCAN,
TinyCAN); capture hardware is optional for file work. DBC files can be
loaded and edited so frames expand into decoded signals in the main view.

Specialist windows include a **sniffer** (only actively-updating IDs,
byte/bit change colouring, and "notching" to mute known-changing bits —
the docs explicitly liken it to a graphical cansniffer), graphing and
signal viewers, a frame sender, playback, and a **UDS scan window** that
sweeps request IDs (default 0x7E0–0x7E7, reply offset +8) with scan types
ReadByID/ReadByAddress, Session Control, ECU Reset, Security Access,
Tester Present, and a Wildcard service fuzz.

## Where it fits

GUI-driven reverse-engineering sessions: finding which ID and bits change
with a physical action, decoding with a DBC once one is known, quick UDS
surface discovery, and working across log formats produced by different
tools — the [can-utils](can-utils.md) logs from a Linux bench open here
directly.

## Limits and notes

The README describes Qt6 support as "approximately beta quality," with a
dependency floor of Qt 5.14+/SerialBus and a minimum display resolution
of 1024×768. The UDS docs warn the Wildcard scan "can take a VERY long
time if you aren't careful," and that the Security Access scan will find
supported levels but is "unlikely to actually unlock them" —
challenge/response is out of its scope, and the docs point to scripting
for anything deeper (see [UDS seed/key](concepts/uds-seed-key.md)).

## Related

- [can-utils](can-utils.md) — produces the candump logs it reads.
- [Lindwurm](lindwurm.md) — pentest-workflow tracing and fuzzing.
- [CANalyzat0r](canalyzat0r.md) — project-based protocol RE.
- [cantools](cantools.md) — programmatic DBC decode/encode.
