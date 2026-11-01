---
title: "TC1791_CAN_BSL"
summary: "CAN bootstrap loader for Infineon TriCore AudoMAX parts such as the TC1791, giving arbitrary flash and RAM read/write on Simos18 and related ECUs without…"
type: entity
category: "Firmware and ECU Reverse Engineering"
url: "https://github.com/bri3d/TC1791_CAN_BSL"
status: unknown
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "CAN bootstrap loader for Infineon TriCore AudoMAX parts such as the TC1791, giving arbitrary flash and RAM read/write on Simos18 and related ECUs without desoldering."
related: [simos18-sboot, ghidra-tc1797]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/bri3d/TC1791_CAN_BSL"
    retrieved: 2026-11-01
  - url: "https://github.com/bri3d/TC1791_CAN_BSL/blob/master/README.md"
    retrieved: 2026-11-01
---

CAN bootstrap loader for Infineon TriCore AudoMAX parts such as the TC1791, giving arbitrary flash and RAM read/write on Simos18 and related ECUs without desoldering.

## What it is

A small published implementation of the Infineon TriCore **CAN bootstrap loader (BSL)** protocol for the TC1791 (AudoMAX family), by the author of [Simos18_SBOOT](simos18-sboot.md). TriCore chips carry a factory boot-strap-loader mode that accepts code over CAN (or UART) before any application runs; this repository is a working loader for that mode — the delivery mechanism that gets a researcher's own mini-loader running on the chip.

## How it works

The repository pairs a TriCore-side loader stub with host tooling organised as send/receive helpers plus mode-specific scripts (`Generic` and `Simos18` modes), with the load address adjusted per target. In the SBOOT workflow the README of that project describes, the BSL stage runs after the bootloader session is established: the operator switches the ECU into its BSL path and this loader transfers the follow-on code. The README here is terse — it identifies the artefact as a CAN BSL implementation for use "in conjunction with the Tricore CAN BSL protocol" and does not document an operating procedure, prerequisites, or the bench setup.

Two framings in circulation go beyond this primary source, and this page does not repeat them as fact: the list summary's "arbitrary flash and RAM read/write … without desoldering" end-state is the *workflow's* outcome as described in the SBOOT material, not a claim this repository's README makes; and SBOOT's README links its companion as "TC1767_CAN_BSL" — a different chip in the name than this listed repository's TC1791. Whether the two are the same code under a renamed repository could not be verified from primary sources at this check.

## Where it fits

BSL access is the hinge between "we can talk to the bootloader" and "we can run code": in the Simos18 chain it is the stage that turns an authenticated session into arbitrary code execution on the ECU, which is why a small, old, single-purpose loader earns a section slot next to the exploit writeup it serves. For TriCore firmware analysis more broadly it complements [ghidra-tc1797](ghidra-tc1797.md) — the loader gets code and dumps off the chip; the processor spec makes them readable.

## Limits and safety notes

Documentation is the limit: one README paragraph, no releases, no stated licence, no test or compatibility list, and chip scope in the name only (TC1791/AudoMAX) with load addresses that must be adapted per target. Reaching BSL mode at all is target-specific and, in the Simos18 case, depends on the upstream SBOOT work — this loader alone does not open a locked production ECU. Running arbitrary code on an engine ECU is destructive if mishandled; bench units and recovery paths first.

## Status and sources

Checked 2026-11-01. **Unknown**: the repository is not archived, but it is a single commit dated 2020-12-06 with no releases and no activity since — a published snapshot with no track record to classify. Documentation claims above come from the following primary sources; no ECU was connected for this page.

- [Upstream repository](https://github.com/bri3d/TC1791_CAN_BSL)
- [Upstream README](https://github.com/bri3d/TC1791_CAN_BSL/blob/master/README.md)

## Related

- [Simos18_SBOOT](simos18-sboot.md)
- [ghidra-tc1797](ghidra-tc1797.md)
