---
title: "ghidra_v850"
summary: "Ghidra processor module for Renesas V850E2 and V850E3/RH850 microcontrollers, the core families behind many ECUs, for disassembling and decompiling their…"
type: entity
category: "Firmware and ECU Reverse Engineering"
url: "https://github.com/esaulenka/ghidra_v850"
status: maintenance
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Ghidra processor module for Renesas V850E2 and V850E3/RH850 microcontrollers, the core families behind many ECUs, for disassembling and decompiling their firmware."
related: [ghidra-tc1797]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/esaulenka/ghidra_v850"
    retrieved: 2026-11-01
  - url: "https://github.com/esaulenka/ghidra_v850/blob/master/README.md"
    retrieved: 2026-11-01
  - url: "https://github.com/esaulenka/ghidra_v850/releases/tag/v0.0.9"
    retrieved: 2026-11-01
---

Ghidra processor module for Renesas V850E2 and V850E3/RH850 microcontrollers, the core families behind many ECUs, for disassembling and decompiling their firmware.

## What it is

A Ghidra processor module (Apache-2.0) that teaches Ghidra the Renesas V850E2, V850E3, and RH850 instruction sets — the 32-bit core families that sit inside a very large share of automotive ECUs (body, chassis, powertrain, and gateway controllers across Japanese and European makes). Without a processor module, Ghidra cannot disassemble these firmware images at all; with it, both disassembly and decompilation to C-like pseudocode become available.

## How it works

The module ships as a built Ghidra extension: download the release ZIP matched to your Ghidra version, install it via Ghidra's extension manager, restart, and import firmware selecting the V850E2, V850E3, or RH850 language variant. Support is uneven by design and the README says so per family: V850E3/RH850 is the most complete (the README claims full floating-point instruction and register support there), V850E2 has full base-integer support with fewer floating-point instructions, and RH850 SIMD instructions are explicitly unimplemented. Decompiler output depends on the SLEIGH semantics being right, and the commit history shows the maintenance pattern — individual P-code fixes for specific instructions (multiply-accumulate, saturating arithmetic, conversion helpers) as users hit them.

## Where it fits

The Renesas counterpart to [ghidra-tc1797](ghidra-tc1797.md)'s TriCore work: between them, the two modules cover the two dominant legacy ECU silicon families a firmware analyst meets first. V850/RH850 images typically arrive from a bench read or an update package; this module is what makes the subsequent work — finding diagnostic handlers, seed/key routines, and update logic — possible in a free tool.

## Limits and safety notes

Per-variant gaps are real: floating-point coverage differs between E2 and E3, RH850 SIMD is absent, and a wrong variant choice produces plausible-looking but wrong disassembly. Release ZIPs are built per Ghidra version (the release line runs 9.2 through 10.3), so a current Ghidra may need a from-source build; the README's installation path assumes a matching prebuilt extension. Coprocessor and peripheral behaviour are outside a processor module's scope entirely.

## Status and sources

Checked 2026-11-01. **Maintenance**: the repository is not archived and still receives occasional fixes (most recent commit 2025-04-27, a P-code correction), but packaged releases stopped at v0.0.9 (2023-02-12) and commit cadence is sparse — a mature, slowly tended module rather than an actively developed one. That records observed activity, not a promise of support. Documentation claims above come from the following primary sources; no firmware was disassembled for this page.

- [Upstream repository](https://github.com/esaulenka/ghidra_v850)
- [Upstream README](https://github.com/esaulenka/ghidra_v850/blob/master/README.md)
- [Release v0.0.9](https://github.com/esaulenka/ghidra_v850/releases/tag/v0.0.9)

## Related

- [ghidra-tc1797](ghidra-tc1797.md)
