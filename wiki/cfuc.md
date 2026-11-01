---
title: "CFUC"
summary: "Open hardware and firmware ISO CAN FD to USB dongle built on the STM32G431, presenting as a native SocketCAN or gs_usb interface with a bundled python-can…"
type: entity
category: "Hardware Interfaces"
url: "https://github.com/ucandevices/CFDC_embedded"
status: maintenance
last_checked: 2026-11-01
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

The firmware repository (this page's listed URL) for UCANdevices' CANableFD-family dongles — the CFUC/CFDC USB-to-**CAN FD** adapters built on the STM32G431's FDCAN peripheral. Where the classic adapters in this section top out at CAN 2.0, these are single-channel ISO CAN FD devices, and the firmware implements the **gs_usb** USB protocol, the same kernel-facing interface as [candleLight_fw](candlelight-fw.md) but on FD-capable silicon.

## How it works

The G431's FDCAN controller provides one FD channel; the firmware bridges it to USB as a gs_usb device. Two host paths exist, and the distinction corrects the list summary's phrasing: on Linux the dongle works with the kernel's gs_usb driver (a true SocketCAN device); the project's own Python path is its `ucanbus` python-can plugin, and its `ucanclient` daemon bridges the device to a socketcand-style TCP service that a remote SocketCAN stack can consume — SocketCAN by bridge, not by a native kernel driver of its own. The organisation's repositories split the work: this embedded repo for firmware, a separate python-can library repo, and the client daemon.

## Where it fits

CFUC/CFDC is the FD step up from the candleLight generation: same gs_usb host model, modern peripheral, FD data rates. [SuperCAN](supercan.md) is the other open FD answer, with its own USB protocol and official Windows support — the trade is gs_usb/Linux nativeness (this) versus a maintained cross-platform stack (that). Against [CANtact](cantact.md)-class hardware it is two CAN generations ahead.

## Limits and safety notes

Single channel. There are **no tagged releases** in the firmware repository — users build from a moving tree or take binaries from the project, and the firmware repository carries **no licence file** (the organisation's Python library is GPL-3.0, but licences do not transfer between repositories by implication; treat the firmware's terms as unstated). Vendor-published hardware availability and pricing live outside the primary sources checked here and are unverified on this page.

## Status and sources

Checked 2026-11-01. **Maintenance**: the firmware repository is not archived and receives irregular commits (most recent 2026-05-17, adding board support), but with no releases, no tags, and long quiet gaps it reads as tended-when-needed rather than actively developed. That records observed activity, not a promise of support. Documentation claims above come from the following primary sources; no hardware was run for this page.

- [Upstream firmware repository](https://github.com/ucandevices/CFDC_embedded)
- [Upstream README](https://github.com/ucandevices/CFDC_embedded/blob/master/README.md)

## Related

- [candleLight_fw](candlelight-fw.md)
- [SuperCAN](supercan.md)
- [CANtact](cantact.md)
