---
title: "Atlas"
summary: "Open-source ECU calibration application for reverse engineering and recalibrating Subaru, Toyota, and Honda ECUs, with an integrated Ghidra bundle for…"
type: entity
category: "Diagnostic Tools"
url: "https://github.com/kylehulscher/atlas"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source ECU calibration application for reverse engineering and recalibrating Subaru, Toyota, and Honda ECUs, with an integrated Ghidra bundle for analysing tables and emulating ROM machine code."
related: [conescan, udsoncan, uds-firmware-extraction]
license: "AGPL-3.0"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/kylehulscher/atlas"
    retrieved: 2026-10-31
---

Open-source ECU calibration application for reverse engineering and recalibrating Subaru, Toyota, and Honda ECUs, with an integrated Ghidra bundle for analysing tables and emulating ROM machine code.

## What it is

An open-source ECU calibration and tuning application for
reverse-engineering and recalibrating modern ECUs, by Kyle Hulscher.
AGPL-3.0.

## How it works

A cross-platform Java application (Windows/macOS/Linux, including
SteamOS). It talks to the car over J2534 (CAN) hardware, with a native
in-app driver for the Tactrix OpenPort 2.0 over serial/COM. It bundles
the Ghidra SRE framework to analyse tables and emulate ROM code, and
provides 2D/3D OpenGL table and gauge visualisation, a 1–2D table
editor, a value-scaling UI, RAM memory-parameter notes, and a
datalogger/gauges with CSV export, in a single-file composite project
format. It began as a 2022 Subaru WRX ECU project.

## Where it fits

A free, full recalibration workflow — from ROM analysis to a tuned
flash — on supported Subarus. Nothing else in this section covers the
calibration end of diagnostics; [ConeScan](conescan.md) is the closest
neighbour in shape, and [udsoncan](udsoncan.md) is the protocol layer
such tools sit above.

## Limits and notes

The README's own warning: "Messing with your ECU is dangerous. You can
'brick'/permanently ruin an ECU… anything you do with Atlas is done at
your own risk." The project refuses to provide definitions for legally
regulated (emissions) systems. Support is narrow: only the 2022 USDM
WRX (manual) is listed as "Supported"; most other vehicles and maps are
Planned or In Progress, and supported vehicles "may not be complete."

## Related

- [ConeScan](conescan.md) — the other calibration-oriented tool here.
- [udsoncan](udsoncan.md) — UDS client work beneath calibration tools.
- [UDS Firmware Extraction](uds-firmware-extraction.md) — recovering the images calibration starts from.
