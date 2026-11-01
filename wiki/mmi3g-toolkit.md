---
title: "MMI3G-Toolkit"
summary: "SD-card-based toolkit for Audi/VW MMI3G head units covering boot-image extraction, reverse-engineered GEMMI protocol details, and an FSC signature-bypass…"
type: entity
category: "Infotainment and IVI"
url: "https://github.com/dspl1236/MMI3G-Toolkit"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "SD-card-based toolkit for Audi/VW MMI3G head units covering boot-image extraction, reverse-engineered GEMMI protocol details, and an FSC signature-bypass technique alongside CAN diagnostic and variant-dumping tools."
related: [ic1101, q50-reverse-engineering, secure-firmware-updates, uds-seed-key, ivi-update-trust]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/dspl1236/MMI3G-Toolkit"
    retrieved: 2026-11-01
  - url: "https://github.com/dspl1236/MMI3G-Toolkit/blob/main/README.md"
    retrieved: 2026-11-01
---

SD-card-based toolkit for Audi/VW MMI3G head units covering boot-image extraction, reverse-engineered GEMMI protocol details, and an FSC signature-bypass technique alongside CAN diagnostic and variant-dumping tools.

## What it is

A modular toolkit — 26 selectable modules, a Python SD-card builder, and a browser-based web app for choosing modules — that extends and analyses Audi/VW Harman Becker MMI 3G, MMI 3G+ and VW RNS-850 head units through the units' built-in SD-card script-execution mechanism. The head units run QNX on the SH4 processor family. Modules install custom screens into the Green Engineering Menu (GEM) and helper scripts into flash storage, are removable without trace per the README, and need no permanent modification or soldering. Beyond the modules, the repository carries a deep research corpus (40+ analysis documents) covering the firmware update format, the IFS boot image, the GEMMI (Google Earth) protocol, and the FSC (feature activation code) signature check — including a working 2-byte patch that defeats that check. Licence: MIT.

## How it works

The execution vector is the MMI's own SD-card script mechanism: the builder assembles chosen modules into a ready SD card (handling the `copie_scr.sh` encoding automatically), and scripts run on the head unit's QNX system. One hard prerequisite sits outside the SD path: the GEM enable bit must first be set with VCDS/ODIS — the README explains why an SD script cannot do it (the value lives in module 5F's persistent memory, writable only over UDS, and QNX ships no UDS client binary). The tested core modules include system-info (full state dump to SD), a gauges dashboard, DTC checking, GEMMI binary extraction, a password finder (stored Wi-Fi/hotspot passwords, Bluetooth keys, Audi Connect credentials), variant dumping and a nav-database parser; readier/alpha additions include a CAN scanner, CAN diagnostics, a UDS diag tool and a game loader for the MMI's J9 JVM.

The research centrepiece is **GEMMI / Google Earth restoration**: reverse engineering found Google's tile server still alive while the authentication endpoint was removed, and the restoration path is staged (probe → enable → deploy → clean restore), with GEMMI payloads shipped as release assets. The **FSC signature bypass**: FSC activation codes gate paid features and maps and are RSA-verified by the head-unit application; a **2-byte patch** at a documented file offset replaces the call to the RSA signature-decrypt routine with a constant success return, forcing the check to pass — a patch to the application binary on the user's own unit, not a key recovery or forgery method. The firmware pipeline (since April 2026) extracts and rebuilds complete MMI3G+ firmware — flash filesystem, LZO-compressed QNX boot image, wrapped binaries — through a documented repack chain in which **every integrity check in the format is CRC32**, and whose LZO recompression is byte-identical to Harman's own output. Engineering access is similarly built from shipped parts: the firmware already contains telnet and network services plus a USB-Ethernet driver, and a few added lines in a startup script yield a root shell over a USB-Ethernet adapter.

## Where it fits

The section's QNX/Harman counterpart to [ic1101](ic1101.md)'s Android/Honda work: same era of IVI, opposite operating system and vendor, and the same structural story — a removable-media execution path the manufacturer built in, integrity anchored on CRC32 plus one RSA check that falls to a 2-byte patch. It is simultaneously a user-facing modification toolkit (dashboards, splash screens, restored Google Earth) and the deepest public research corpus on this platform. Its CAN modules touch the CAN Bus Analysis section's territory from the head-unit side rather than a bench interface, and its GEM-enable prerequisite is a small worked instance of the [UDS seed/key](concepts/uds-seed-key.md) era's diagnostic-access model. Concept link: [secure firmware updates](concepts/secure-firmware-updates.md) — CRC-only integrity plus a bypassable signature check is that page's failure taxonomy in one platform.

## Limits and safety notes

Platform scope is the README's table: MMI 3G High 2008–2012, MMI 3G+ 2012–2018, VW RNS-850 2011–2018 — nothing outside the Harman MMI 3G family, and feature availability varies by variant. Maturity is uneven by the README's own labels — the module table mixes Tested, Ready, Alpha, Design and Planned, the Google Earth restoration chain is Alpha, and some modules are design-only or planned; this page does not flatten those labels into blanket capability. The vendor-flagged verification gap: the `usb-net` module is beta — validated on a Porsche PCM 3.1 (same QNX driver ABI) and, in the README's words, still needs confirmation on an Audi/VW bench unit; MMI 3G High lacks the USB-Ethernet driver entirely. GEM-screen modules are inert until the one-time VCDS/ODIS adaptation change is made. Two facts are **not stated** in the sources and are not guessed here: the QNX version, and the exact SH4 SoC part number.

## Status and sources

Checked 2026-11-01. **Active**: created 2026-04-14, it has 360 commits in under six months with the latest on 2026-09-24 (about five weeks before this check), three April 2026 releases shipping the GEMMI payloads, and merged PRs into late September — a young project in continuous development. Documentation claims above come from the following primary sources; no head unit was modified for this page.

- [Upstream repository](https://github.com/dspl1236/MMI3G-Toolkit)
- [Upstream README](https://github.com/dspl1236/MMI3G-Toolkit/blob/main/README.md)

## Related

- [ic1101](ic1101.md)
- [Q50 Reverse Engineering](q50-reverse-engineering.md)
- [Secure firmware updates](concepts/secure-firmware-updates.md)
- [UDS seed/key](concepts/uds-seed-key.md)
- [IVI update-path trust](concepts/ivi-update-trust.md)
