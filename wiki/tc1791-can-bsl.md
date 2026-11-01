---
title: "TC1791_CAN_BSL"
summary: "CAN bootstrap loader for Infineon TriCore AudoMAX parts such as the TC1791, giving arbitrary flash and RAM read/write on Simos18 and related ECUs without…"
type: entity
category: "Firmware and ECU Reverse Engineering"
url: "https://github.com/bri3d/TC1791_CAN_BSL"
status: maintenance
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

A published implementation of the Infineon TriCore **CAN bootstrap loader (BSL)** protocol for the TC1791 (AudoMAX family), by the author of [Simos18_SBOOT](simos18-sboot.md). TriCore chips carry a factory boot-strap-loader mode that accepts code over CAN (or UART) before any application runs; this repository is a working loader for that mode — the delivery mechanism that gets a researcher's own mini-loader running on the chip. The repository's own description claims "arbitrary read/write as well as compressed read" for the loader, so the list summary's end-state framing does come from the project itself. The repository records **no licence** (no LICENSE file, none recorded upstream), so default copyright applies.

## How it works

The repository pairs a TriCore-side loader stub with host tooling organised as send/receive helpers plus mode-specific scripts (`Generic` and `Simos18` modes), with the load address adjusted per target. Contrary to a terse-README impression, the README **does** document the bench setup in full: a Raspberry Pi 2/3/4 with a Seeed CAN hat, the HWCFG pin wired to GPIO 24 and RST to GPIO 23, HWCFG-based entry into BSL mode, and the SPRAM load address at `C0000000`. In the SBOOT workflow that project's README describes, the BSL stage runs after the bootloader session is established and the boot password recovered: the operator switches the ECU into its BSL path and this loader transfers the follow-on code.

## Where it fits

BSL access is the hinge between "we can talk to the bootloader" and "we can run code": in the Simos18 chain it is the stage that turns a recovered boot password into arbitrary code execution on the ECU, which is why a small, single-purpose loader earns a section slot next to the exploit writeup it serves. For TriCore firmware analysis more broadly it complements [ghidra-tc1797](ghidra-tc1797.md) — the loader gets code and dumps off the chip; the processor spec makes them readable.

## Limits and safety notes

Chip scope is in the name (TC1791/AudoMAX) with load addresses that must be adapted per target, and there are no releases — users build from the tree. Reaching BSL mode at all is target-specific and, in the Simos18 case, depends on the upstream SBOOT work — this loader alone does not open a locked production ECU. Running arbitrary code on an engine ECU is destructive if mishandled; bench units and recovery paths first.

## Status and sources

Checked 2026-11-01. **Maintenance** (intermittently active): the repository (created 2020-12-19) is not archived and, after a long quiet gap from 2022, received a January 2026 commit and further pushes on 2026-08-02 ("migrate to UV", "pass ruff") — an old artefact its author still touches, not a one-shot snapshot. There are no releases. That records observed activity, not a promise of support. Documentation claims above come from the following primary sources; no ECU was connected for this page.

- [Upstream repository](https://github.com/bri3d/TC1791_CAN_BSL)
- [Upstream README](https://github.com/bri3d/TC1791_CAN_BSL/blob/master/README.md)

## Related

- [Simos18_SBOOT](simos18-sboot.md)
- [ghidra-tc1797](ghidra-tc1797.md)
