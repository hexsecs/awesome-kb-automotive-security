---
uid: 01a19d3c-af96-7b26-8a8c-801129f07391
title: "ghidra-tc1797"
summary: "Ghidra processor specification and language definitions for the Infineon TriCore TC1797, used to label memory regions when disassembling MED17 and similar…"
type: entity
category: "Firmware and ECU Reverse Engineering"
url: "https://github.com/christianobora/ghidra-tc1797"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
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

A thin add-on to Ghidra's existing TriCore support for one chip: the Infineon TriCore TC1797, the AudoNG-generation microcontroller inside Bosch MED17-family engine ECUs. Despite the list summary's phrasing, this is **not** a SLEIGH language definition — the repository holds only two files of substance, `tc1797.pspec` (the processor specification: the chip's memory map and register layout) and `tricore.ldefs` (the language-definitions file that registers the TC1797 variant with Ghidra). The compiled language itself (`.sla`) and the compiler specification (`.cspec`) are **not** included; disassembly semantics come from the TriCore support Ghidra already ships. The repository carries **no licence** — no LICENSE file, and none recorded upstream — so default copyright applies.

## How it works

Dropping the pspec and ldefs alongside Ghidra's TriCore module gives an imported TC1797 firmware image the chip's real address-space layout — program/data flash, boot ROM, scratchpad and peripheral space as named regions — instead of an undifferentiated blob, so a raw dump lands in labelled memory. That is the whole mechanism: the project adds chip-specific labelling to a language Ghidra already speaks. The README is minimal: it states the motivation — the author's work on a MED17.1.1 Audi ECU — and gives no installation instructions, no tested Ghidra version, no discussion of the PCP (Peripheral Control Processor) coprocessor, and no completeness caveats. Anything beyond the memory map is Ghidra's stock TriCore behaviour, not this project's claim.

## Where it fits

This is the first hour of a MED17 firmware project: before any function can be understood, the dump needs a truthful memory map. It pairs naturally with [medc17-checksum-tool](medc17-checksum-tool.md), which handles the same ECU family's checksum blocks once code is identified, and it is the Ghidra-side counterpart to [ghidra_v850](ghidra-v850.md) for the Renesas families. The Simos18 work elsewhere in this section targets a sibling TriCore part (the TC1791 in [TC1791_CAN_BSL](tc1791-can-bsl.md)) — a different chip and memory map, so this spec does not transfer directly.

## Limits and safety notes

Single-chip scope is the point and the limit: applying TC1797 regions to another TriCore variant will silently mislabel memory. The artefact is two definition files with a minimal README — no install procedure, no version-compatibility statement, and no upstream caveats to lean on — so correctness of the map against the chip's user manual is on the user. With no licence recorded, redistribution terms are unstated.

## Status and sources

Checked 2026-11-01. **Unknown**: the repository is not archived, but it was created and last pushed on 2024-04-20 (three commits, all that day), with no releases and no activity since — a small dormant snapshot with no track record to classify. That records the observable state, not a judgement on the definitions' quality. Documentation claims above come from the following primary sources; no firmware was disassembled for this page.

- [Upstream repository](https://github.com/christianobora/ghidra-tc1797)
- [Upstream README](https://github.com/christianobora/ghidra-tc1797/blob/master/README.md)

## Related

- [ghidra_v850](ghidra-v850.md)
- [medc17-checksum-tool](medc17-checksum-tool.md)
- [TC1791_CAN_BSL](tc1791-can-bsl.md)
