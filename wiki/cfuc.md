---
title: "CFUC"
summary: "Open hardware and firmware ISO CAN FD to USB dongle built on the STM32G431, presenting as a native SocketCAN or gs_usb interface with a bundled python-can…"
type: entity
category: "Hardware Interfaces"
url: "https://github.com/ucandevices/CFDC_embedded"
status: maintenance
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open hardware and firmware ISO CAN FD to USB dongle built on the STM32G431, presenting as a native SocketCAN or gs_usb interface with a bundled python-can plugin."
related: [candlelight-fw, supercan, cantact]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/ucandevices/CFDC_embedded"
    retrieved: 2026-11-01
  - url: "https://github.com/ucandevices/CFDC_embedded/blob/master/README.md"
    retrieved: 2026-11-01
---

Open hardware and firmware ISO CAN FD to USB dongle built on the STM32G431, presenting as a native SocketCAN or gs_usb interface with a bundled python-can plugin.

## What it is

UCANdevices' CANableFD-family dongles — the CFUC/CFDC USB-to-**CAN FD** adapters built on the STM32G431's FDCAN peripheral. This repository (the page's listed URL) holds **both** the hardware (the KiCad PCB design) and the firmware for the dongles, under an LGPL-3.0 licence. Where the classic adapters in this section top out at CAN 2.0, these are single-channel ISO CAN FD devices, with data-phase rates up to 5 Mbit/s. The README carries a vendor price claim of about $22 on Tindie — recorded here as a vendor claim, not an independently verified price.

## How it works

The G431's FDCAN controller provides one FD channel, and the device runs **one of two firmware flavours** — you flash one or the other, they are not simultaneous modes. The native flavour presents a USB CDC device and is driven from the host by the project's `cfuc` plugin for python-can, cross-platform (Windows, macOS, Linux). The alternative is a **gs_usb firmware port** (the "budgetcan" build), which is what gives native Linux SocketCAN through the kernel's gs_usb driver. That two-flavour split is the accurate version of the list summary's "native SocketCAN or gs_usb" phrasing: SocketCAN arrives via the gs_usb flavour, and the cross-platform Python path via the CDC flavour. Releases are published from this repository (latest `slcan_1`, 2024-05-02).

## Where it fits

CFUC/CFDC is the FD step up from the candleLight generation: FD-capable silicon, with a choice between a gs_usb/Linux-native build and a python-can build for other platforms. [SuperCAN](supercan.md) is the other open FD answer, with its own USB protocol and a separate out-of-tree SocketCAN driver — the trade is firmware choice and python-can reach (this) versus a single maintained protocol stack (that). Against [CANtact](cantact.md)-class hardware it is two CAN generations ahead.

## Limits and safety notes

Single channel. The firmware choice is exclusive — a device flashed with the CDC flavour is not a SocketCAN device until reflashed with the gs_usb port, and vice versa — so "which firmware is on this dongle" is the first question for any setup problem. Code activity has gone quiet (see Status), so treat the feature set as settled. Vendor pricing and availability claims live in the README and are unverified beyond it.

## Status and sources

Checked 2026-11-01. **Maintenance**: the repository is not archived; the last *code* commit is from July 2023, and the May 2026 repository activity was README-only — dormant code with an occasionally tended front page, rather than active development. Releases exist (latest `slcan_1`, 2024-05-02). That records observed activity, not a promise of support. Documentation claims above come from the following primary sources; no hardware was run for this page.

- [Upstream repository (hardware and firmware)](https://github.com/ucandevices/CFDC_embedded)
- [Upstream README](https://github.com/ucandevices/CFDC_embedded/blob/master/README.md)

## Related

- [candleLight_fw](candlelight-fw.md)
- [SuperCAN](supercan.md)
- [CANtact](cantact.md)
