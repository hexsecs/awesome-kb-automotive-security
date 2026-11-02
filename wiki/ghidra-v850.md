---
title: "ghidra_v850"
summary: "Ghidra processor module for Renesas V850E2 and V850E3/RH850 microcontrollers, the core families behind many ECUs, for disassembling and decompiling their…"
type: entity
category: "Firmware and ECU Reverse Engineering"
url: "https://github.com/esaulenka/ghidra_v850"
status: maintenance
last_checked: 2026-11-01
created: 2026-10-31
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
---

Ghidra processor module for Renesas V850E2 and V850E3/RH850 microcontrollers, the core families behind many ECUs, for disassembling and decompiling their firmware.

## What it is

A Ghidra processor module (MIT licence) that teaches Ghidra the Renesas V850E2, V850E3, and RH850 instruction sets — the 32-bit core families that sit inside a very large share of automotive ECUs (body, chassis, powertrain, and gateway controllers across Japanese and European makes). Without a processor module, Ghidra cannot disassemble these firmware images at all; with it, both disassembly and decompilation to C-like pseudocode become available. The language definitions themselves are version 0.1 — early, and the README says so in its own TODO list.

## How it works

There are **no releases or tags** — distribution is source-only: copy the module into `$(GHIDRA_HOME)\Ghidra\Extensions\` and restart Ghidra, then import firmware selecting the V850E2, V850E3, or RH850 language variant. The README's TODO list is candid about maturity — literally "fix a lot of bugs" and "complete RH850 support" — so coverage claims should be read as work in progress, not a finished matrix; this page does not repeat per-variant floating-point coverage figures, because the README does not support them. Decompiler output depends on the SLEIGH semantics being right, and the commit history shows the maintenance pattern — individual P-code fixes for specific instructions as users hit them (most recently a `rotl` fix).

## Where it fits

The Renesas counterpart to [ghidra-tc1797](ghidra-tc1797.md)'s TriCore work: between them, the two modules cover the two dominant legacy ECU silicon families a firmware analyst meets first. V850/RH850 images typically arrive from a bench read or an update package; this module is what makes the subsequent work — finding diagnostic handlers, seed/key routines, and update logic — possible in a free tool.

## Limits and safety notes

Version 0.1 language definitions with an upstream TODO that includes fixing "a lot of bugs": expect wrong P-code on edge instructions, and a wrong variant choice produces plausible-looking but wrong disassembly. There is no packaged build to install — a source copy into the Ghidra tree is the only path, so the module's behaviour can vary with the Ghidra version it is dropped into. Coprocessor and peripheral behaviour are outside a processor module's scope entirely.

## Status and sources

Checked 2026-11-01. **Maintenance**: the repository is not archived and still receives occasional fixes (most recent commit 2025-08-14, a `rotl` P-code correction), but there have never been releases or tags and commit cadence is sparse — a mature, slowly tended module rather than an actively developed one. That records observed activity, not a promise of support. Documentation claims above come from the following primary sources; no firmware was disassembled for this page.

- [Upstream repository](https://github.com/esaulenka/ghidra_v850)
- [Upstream README](https://github.com/esaulenka/ghidra_v850/blob/master/README.md)

## Related

- [ghidra-tc1797](ghidra-tc1797.md)
