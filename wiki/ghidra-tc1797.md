---
title: "ghidra-tc1797"
summary: "Ghidra processor specification and language definitions for the Infineon TriCore TC1797, used to label memory regions when disassembling MED17 and similar…"
type: entity
category: "Firmware and ECU Reverse Engineering"
url: "https://github.com/christianobora/ghidra-tc1797"
status: unknown
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Ghidra processor specification and language definitions for the Infineon TriCore TC1797, used to label memory regions when disassembling MED17 and similar ECU firmware."
related: [ghidra-v850, medc17-checksum-tool, tc1791-can-bsl]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/christianobora/ghidra-tc1797"
    retrieved: 2026-11-01
  - url: "https://github.com/christianobora/ghidra-tc1797/blob/master/README.md"
    retrieved: 2026-11-01
---

Ghidra processor specification and language definitions for the Infineon TriCore TC1797, used to label memory regions when disassembling MED17 and similar ECU firmware.

## What it is

A Ghidra processor specification (GPL-3.0) for one chip: the Infineon TriCore TC1797, the AudoNG-generation microcontroller inside Bosch MED17-family engine ECUs. Stock Ghidra ships a generic TriCore definition; this module replaces it with a TC1797-specific one — most importantly a memory map of the chip's regions (program/data flash, boot ROM, scratchpad and peripheral space, external bus) as named overlay blocks, so a raw firmware dump lands in labelled address space instead of an undifferentiated blob.

## How it works

The repository is the SLEIGH language definition set for the chip (`tc1797.slaspec` and companions: processor spec, context and register definitions) plus a sample loader for raw TC1797 flash binaries. The author imported the language files into Ghidra 9.1.2 and used the overlay-based memory model to place MEDC17 firmware regions; the README is explicit that it "is not working perfectly, but it's enough to begin reversing MEDC17 firmware" and lists disassembly of PCP (Peripheral Control Processor) coprocessor code as unimplemented. The repository also deliberately excludes generated PCP C files that were, in the author's words, mostly empty.

## Where it fits

This is the first hour of a MED17 firmware project: before any function can be understood, the dump needs the right processor semantics and a truthful memory map. It pairs naturally with [medc17-checksum-tool](medc17-checksum-tool.md), which handles the same ECU family's checksum blocks once code is identified, and it is the Ghidra-side counterpart to [ghidra_v850](ghidra-v850.md) for the Renesas families. The Simos18 work elsewhere in this section targets a sibling TriCore part (the TC1791 in [TC1791_CAN_BSL](tc1791-can-bsl.md)) — a different chip and memory map, so this spec does not transfer directly.

## Limits and safety notes

Single-chip scope is the point and the limit: applying TC1797 overlays to another TriCore variant will silently mislabel regions. The author flags the definition as imperfect and PCP code as unsupported, so disassembly around coprocessor interactions needs manual verification against the chip's user manual. The README's single tested Ghidra version is 9.1.2 (2020-era); compatibility with current Ghidra releases is not stated upstream — unverified at this check.

## Status and sources

Checked 2026-11-01. **Unknown**: the repository is not archived, but it was created on 2020-08-20, contains two commits, and has had no pushes since its creation day; there are no releases. A 2020 snapshot with no track record to classify. That records the observable state, not a judgement on the definitions' quality. Documentation claims above come from the following primary sources; no firmware was disassembled for this page.

- [Upstream repository](https://github.com/christianobora/ghidra-tc1797)
- [Upstream README](https://github.com/christianobora/ghidra-tc1797/blob/master/README.md)

## Related

- [ghidra_v850](ghidra-v850.md)
- [medc17-checksum-tool](medc17-checksum-tool.md)
- [TC1791_CAN_BSL](tc1791-can-bsl.md)
