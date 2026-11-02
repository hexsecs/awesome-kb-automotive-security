---
title: "uds-firmware-extraction"
summary: "Tool for extracting ECU firmware from UDS flash traffic following ISO-14229 standard."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/honinb0n/uds-firmware-extraction"
status: unknown
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Tool for extracting ECU firmware from UDS flash traffic following ISO-14229 standard."
related: [can-utils, udsoncan, conescan]
license: "GPL-2.0"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/honinb0n/uds-firmware-extraction"
    retrieved: 2026-10-31
---

Tool for extracting ECU firmware from UDS flash traffic following ISO-14229 standard.

## What it is

A small Python tool that extracts ECU firmware from captured UDS flash
traffic, by Honinbon. GPL-2.0.

## How it works

Offline and log-driven: the input is a standard candump logfile; you
pass `--flash_id` (the diagnostic ID used for flashing) and the tool
reassembles the firmware transferred in the UDS (ISO 14229)
flash/download traffic in that log. Output is a binary (`firmware.bin`
by default, `-o` to rename) and optionally an S19 file (`-s`); `--split`
sets the separator between CAN ID and data in the input file (default
`#`).

## Where it fits

Recovering a flashable firmware image from a previously recorded
dealer or own flashing session — no live vehicle interaction. It is
the read-side counterpart to the download workflows in
[ConeScan](conescan.md) and the flashing toolchains in this section,
fed by [can-utils](can-utils.md) captures.

## Limits and notes

No limits or safety warnings are stated in the checked sources. Status
`unknown`: the repository has only 2 commits, all on its creation day
(2024-03-04), with one release and no activity since to judge upkeep
by.

## Related

- [can-utils](can-utils.md) — produces the candump logs it consumes.
- [udsoncan](udsoncan.md) — the live-session side of the same UDS transfers.
- [ConeScan](conescan.md) — download-direction tooling on the same services.
