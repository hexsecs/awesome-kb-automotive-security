---
uid: 01a19d3c-afec-7326-b48c-5c047800ff77
title: "uds-firmware-extraction"
summary: "Tool for extracting ECU firmware from UDS flash traffic following ISO-14229 standard."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/honinb0n/uds-firmware-extraction"
status: maintenance
last_checked: 2026-11-17
status_note: "GitHub repo not archived; last push 2024-03-04."
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Tool for extracting ECU firmware from UDS flash traffic following ISO-14229 standard."
related:
  - can-utils
  - udsoncan
  - conescan
  - firmware-acquisition
  - reversing-a-brake-ecu-firmware-update
  - atlas
  - secoc-key-extractor
  - automotive-flash-bootloaders-exposing-automotive-ecu-updates
  - zephyr-reference-ecu
  - iso-tp
license: "GPL-2.0"
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/honinb0n/uds-firmware-extraction"
    retrieved: 2026-10-31
  - url: "https://raw.githubusercontent.com/Honinb0n/uds-firmware-extraction/main/uds-firmware-extraction.py"
    retrieved: 2026-11-17
facets: [diagnostics, firmware, tools, standards]
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

The [implementation](https://raw.githubusercontent.com/Honinb0n/uds-firmware-extraction/main/uds-firmware-extraction.py),
checked alongside the repository on 2026-11-17, makes the extraction
boundary concrete. It filters the selected hexadecimal CAN ID, recognises
RequestDownload (`0x34`), gathers multi-frame TransferData (`0x36`)
payloads, and checks accumulated byte length against the advertised memory
size at RequestTransferExit (`0x37`). It strips the transfer service and
block-counter bytes rather than writing complete diagnostic messages to
disk. Download data from successive transfers is appended to one binary.

A practical offline workflow is to retain the original candump capture,
identify the tester's flashing ID, and run the script with `-i`, `--flash_id`
and a fresh `-o` filename. It refuses an already-existing binary output.
The optional S19 conversion invokes external `objcopy` with binary input
and S-record output; this is not an independent address-aware reconstruction
of the ECU's memory map.

## Where it fits

Recovering transferred firmware bytes from a previously recorded
dealer or own flashing session — no live vehicle interaction. It is
the read-side counterpart to the download workflows in
[ConeScan](conescan.md) and the flashing toolchains in this section,
fed by [can-utils](can-utils.md) captures.

## Limits and notes

The script reports compression and encryption method nibbles from
RequestDownload, but does not decompress or decrypt transferred bytes.
Consequently, an extracted binary is the observed download payload, not
necessarily a plaintext, complete or directly flashable ECU image. Its
reassembly uses classic CAN ISO-TP frame layouts; it is not a general
DoIP, CAN FD or arbitrary capture-format decoder. Length checks do not
authenticate firmware, and the code does not validate server acceptance
of every transfer or reconstruct missing traffic. No vehicle access,
SecurityAccess bypass or live memory read is performed.

No safety warnings are stated in the checked sources. Status
`unknown`: the repository has only 2 commits, all on its creation day
(2024-03-04), with one release and no activity since to judge upkeep
by.

## Related

- [can-utils](can-utils.md) — produces the candump logs it consumes.
- [udsoncan](udsoncan.md) — the live-session side of the same UDS transfers.
- [ConeScan](conescan.md) — download-direction tooling on the same services.
- [Firmware acquisition](concepts/firmware-acquisition.md) — distinguishes
  recovering a transmitted update from reading all ECU memory.
- [ISO-TP](concepts/iso-tp.md) — explains the segmented transport whose
  payloads must be reassembled before firmware bytes can be recovered.
