---
title: "pyXCP"
summary: "Python implementation of the ASAM MCD-1 XCP protocol over CAN, Ethernet, and USB, with seed-and-key access handling, for measuring, calibrating, and…"
type: entity
category: "Firmware and ECU Reverse Engineering"
url: "https://github.com/christoph2/pyxcp"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python implementation of the ASAM MCD-1 XCP protocol over CAN, Ethernet, and USB, with seed-and-key access handling, for measuring, calibrating, and flashing ECUs."
related: [pya2l, uds-seed-key, calibration-plane]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/christoph2/pyxcp"
    retrieved: 2026-11-01
  - url: "https://github.com/christoph2/pyxcp/blob/master/README.md"
    retrieved: 2026-11-01
  - url: "https://github.com/christoph2/pyxcp/releases/tag/v0.28.0"
    retrieved: 2026-11-01
---

Python implementation of the ASAM MCD-1 XCP protocol over CAN, Ethernet, and USB, with seed-and-key access handling, for measuring, calibrating, and flashing ECUs.

## What it is

A Python implementation (LGPL-3.0 licence) of **XCP**, the ASAM MCD-1 "Universal Measurement and Calibration Protocol" — the vendor-neutral successor to CCP that production ECUs expose for development and calibration. pyXCP is the master (client) side: a `Master` object over a pluggable transport that can connect to an XCP slave and read/write its memory directly. The same author maintains [pyA2L](pya2l.md), and the pairing is the point — the slave's A2L file names and locates everything pyXCP can touch; pyXCP's A2L integration runs through that package (`pya2ldb`).

## How it works

Transports cover CAN (via python-can, including Vector/PEAK-class interfaces), Ethernet (UDP/TCP), USB, and a serial/SxI framing. Once connected, the documented command surface includes synchronous measurement and memory access — `upload`/`download` and their block and short forms, address setting, checksums over memory ranges — plus the DAQ/STIM machinery for timestamped cyclic measurement and stimulation (event channels, ODT entries, start/stop, presets saved to files for cyclic jobs). The calibration-memory model is implemented faithfully: RAM/flash page switching (`setCalPage`, `copyCalPage`), page freezing, and XCP's **seed-and-key** resource protection, which upstream describes as pluggable seed-to-key resolution — pyXCP calls a user-supplied seed/key implementation to unlock resources, the same protection pattern as [UDS seed/key](concepts/uds-seed-key.md) at the calibration layer instead of the diagnostic layer. Persistence features (DAQ resume, parameter files) round out a tool aimed at real calibration benches.

## Where it fits

XCP is the development interface that sometimes survives into production vehicles, and when it does, it is one of the deepest access paths an ECU offers: direct memory read/write and calibration changes without going through diagnostic services at all. For security assessment, pyXCP answers the practical questions — is XCP reachable, which resources does its seed/key actually protect, and how strong is the deployed algorithm — with a scriptable open client instead of a commercial calibration suite.

## Limits and safety notes

Precision about "flashing" matters: the README documents programming support as **building blocks** — helpers for program/erase/write flows — rather than a turnkey flash routine, so a real flash workflow (sector erase order, bootloader cooperation, verification) is still the user's code assembled on top of them. Seed/key support likewise means pyXCP can *call* your algorithm; it does not supply or recover any manufacturer's algorithm. XCP writes go straight to ECU memory — a wrong address or page state can brick a calibration or worse, so bench hardware and a recovery path come first.

## Status and sources

Checked 2026-11-01. **Active**: the repository is not archived, the latest release is v0.28.0 (2026-03-01), and commits continue to 2026-10-31. This records observed project activity, not a promise of support. Documentation claims above come from the following primary sources; no ECU was connected for this page.

- [Upstream repository](https://github.com/christoph2/pyxcp)
- [Upstream README](https://github.com/christoph2/pyxcp/blob/master/README.md)
- [Release v0.28.0](https://github.com/christoph2/pyxcp/releases/tag/v0.28.0)

## Related

- [pyA2L](pya2l.md)
- [UDS seed/key](concepts/uds-seed-key.md)
