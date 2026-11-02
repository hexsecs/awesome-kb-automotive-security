---
title: "medc17-checksum-tool"
summary: "Analyses and corrects CRC32, ADD32, and ADD16 checksums in Bosch MED17 and EDC17 firmware, resolving CRC values algebraically rather than by brute force and…"
type: entity
category: "Firmware and ECU Reverse Engineering"
url: "https://github.com/ConnorHowell/medc17-checksum-tool"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Analyses and corrects CRC32, ADD32, and ADD16 checksums in Bosch MED17 and EDC17 firmware, resolving CRC values algebraically rather than by brute force and regenerating RSA signatures after modification."
related: [ghidra-tc1797, pya2l, secure-firmware-updates]
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

A Python tool (MIT licence — a LICENSE file is present in the repository) for post-edit survival on Bosch MED17/EDC17 engine ECUs: those firmwares carry internal checksum blocks, and the ECU refuses or faults an image whose checksums no longer match its contents. After any modification — the tuning and research workflows this section supports — the checksums must be corrected, and that is what this tool does: analyse an image, report its checksum blocks, and rewrite them to match. It also corrects **CVN** (Calibration Verification Number) values, the calibration-identity numbers diagnostic testers read out.

## How it works

The README names the supported MED17/EDC17 variants — support has grown across versions to multiple variants — and the checksum algorithms used in different block layouts across them: CRC32, ADD32, and ADD16. Its distinctive claim is method: instead of flipping bytes and re-testing, the tool solves the CRC correction algebraically (GF(2) polynomial arithmetic — computing the exact patch value that forces the target checksum), which is instant and exact where brute force would be neither. It works from the command line on a firmware file, prints an analysis of the blocks it finds before correcting them, and offers a JSON output mode for scripted use.

On signatures, precision matters in both directions. The README's feature list **does** include the bullet "Generates valid Bleichenbacher signatures" — so the list summary's signature claim has a primary-source basis — but the README gives no method detail for it: no key handling, no explanation of how the signature is produced. This page therefore records the bullet as an upstream claim with an undocumented mechanism, neither endorsed nor denied here.

## Where it fits

The companion step to understanding the firmware: [ghidra-tc1797](ghidra-tc1797.md) gets a MED17 image disassembled, calibration literacy comes from files parsed by tools like [pyA2L](pya2l.md), and this tool is what makes a modified image internally consistent again. It is also a clean illustration of a general ECU-security fact: plain checksums are integrity checks against corruption, not authenticity controls — they yield to algebra. Authenticity is what signatures (and frameworks like Uptane, in the update path) are for.

## Limits and safety notes

Variant scope is the hard limit: the named MED17/EDC17 variants and their checksum algorithms; a variant with a different block layout is out of scope and a forced correction would produce a confidently wrong image. The Bleichenbacher-signature bullet is undocumented beyond its one line (see above), so no workflow should be planned around it without independent verification. A checksum-corrected image is still a modified image wherever the ECU verifies signatures through other means.

## Status and sources

Checked 2026-11-01. **Active**: the repository (created 2025-11-20) is not archived and receives continuing development — commits through 2026-08-27 adding multi-variant support, CVN reporting, and a JSON mode. That records observed project activity, not a promise of support. Documentation claims above come from the following primary sources; no firmware was processed for this page.

- [Upstream repository](https://github.com/ConnorHowell/medc17-checksum-tool)
- [Upstream README](https://github.com/ConnorHowell/medc17-checksum-tool/blob/main/README.md)

## Related

- [ghidra-tc1797](ghidra-tc1797.md)
- [pyA2L](pya2l.md)
- [Secure firmware updates](concepts/secure-firmware-updates.md)
