---
title: "medc17-checksum-tool"
summary: "Analyses and corrects CRC32, ADD32, and ADD16 checksums in Bosch MED17 and EDC17 firmware, resolving CRC values algebraically rather than by brute force and…"
type: entity
category: "Firmware and ECU Reverse Engineering"
url: "https://github.com/ConnorHowell/medc17-checksum-tool"
status: unknown
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Analyses and corrects CRC32, ADD32, and ADD16 checksums in Bosch MED17 and EDC17 firmware, resolving CRC values algebraically rather than by brute force and regenerating RSA signatures after modification."
related: [ghidra-tc1797, pya2l]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/ConnorHowell/medc17-checksum-tool"
    retrieved: 2026-11-01
  - url: "https://github.com/ConnorHowell/medc17-checksum-tool/blob/main/README.md"
    retrieved: 2026-11-01
---

Analyses and corrects CRC32, ADD32, and ADD16 checksums in Bosch MED17 and EDC17 firmware, resolving CRC values algebraically rather than by brute force and regenerating RSA signatures after modification.

## What it is

A single-file Python script for post-edit survival on Bosch MED17/EDC17 engine ECUs: those firmwares carry internal checksum blocks, and the ECU refuses or faults an image whose checksums no longer match its contents. After any modification — the tuning and research workflows this section supports — the checksums must be corrected, and that is all this tool does: analyse an image, report its checksum blocks, and rewrite them to match.

## How it works

The README names seven supported MED17/EDC17 variants and three checksum algorithms — CRC32, ADD32, and ADD16 — used in different block layouts across those variants. Its distinctive claim is method: instead of flipping bytes and re-testing, the tool solves the CRC correction algebraically (GF(2) polynomial arithmetic — computing the exact patch value that forces the target checksum), which is instant and exact where brute force would be neither. It works from the command line on a firmware file and prints an analysis of the blocks it finds before correcting them.

One part of the list summary does **not** survive contact with the primary source: the summary says the tool regenerates "RSA signatures after modification", but the README states the opposite boundary — the RSA private keys are not public, so signatures cannot be regenerated with this tool. The checksum correction is real; signature forgery is explicitly out of scope upstream. This page follows the README.

## Where it fits

The companion step to understanding the firmware: [ghidra-tc1797](ghidra-tc1797.md) gets a MED17 image disassembled, calibration literacy comes from files parsed by tools like [pyA2L](pya2l.md), and this tool is what makes a modified image internally consistent again. It is also a clean illustration of a general ECU-security fact: plain checksums are integrity checks against corruption, not authenticity controls — they yield to algebra. Authenticity is what signatures (and frameworks like Uptane, in the update path) are for.

## Limits and safety notes

Variant scope is the hard limit: seven named MED17/EDC17 variants, three checksum algorithms; a variant with a different block layout is out of scope and a forced correction would produce a confidently wrong image. There is no test suite, example firmware, or input-format documentation in the repository, so first use on a new variant needs independent verification before anything is flashed. The repository carries **no licence file** — default copyright applies, which matters for redistribution. A checksum-corrected image is still an unsigned-modified image wherever the ECU verifies signatures; see the RSA note above.

## Status and sources

Checked 2026-11-01. **Unknown**: the repository is not archived, but at this check it consists of a single commit (2025-08-12) adding the script and README, with no releases and no subsequent activity — a published snapshot with no track record to classify. That records the observable state, not a judgement on the code. Documentation claims above come from the following primary sources; no firmware was processed for this page.

- [Upstream repository](https://github.com/ConnorHowell/medc17-checksum-tool)
- [Upstream README](https://github.com/ConnorHowell/medc17-checksum-tool/blob/main/README.md)

## Related

- [ghidra-tc1797](ghidra-tc1797.md)
- [pyA2L](pya2l.md)
