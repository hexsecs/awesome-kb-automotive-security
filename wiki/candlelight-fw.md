---
title: "candleLight_fw"
summary: "Open firmware for low-cost STM32 USB to CAN adapters such as CANable, cantact, and candleLight that implements the mainline Linux gs_usb interface, turning…"
type: entity
category: "Hardware Interfaces"
url: "https://github.com/candle-usb/candleLight_fw"
status: maintenance
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open firmware for low-cost STM32 USB to CAN adapters such as CANable, cantact, and candleLight that implements the mainline Linux gs_usb interface, turning them into native SocketCAN devices without a vendor driver."
related: [cantact, cfuc, supercan]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/candle-usb/candleLight_fw"
    retrieved: 2026-11-01
  - url: "https://github.com/candle-usb/candleLight_fw/blob/master/README.md"
    retrieved: 2026-11-01
---

Open firmware for low-cost STM32 USB to CAN adapters such as CANable, cantact, and candleLight that implements the mainline Linux gs_usb interface, turning them into native SocketCAN devices without a vendor driver.

## What it is

Open firmware (BSD-3-Clause components under a GPL-2.0 umbrella) that makes inexpensive STM32-based USB-CAN adapters speak **gs_usb** — the USB protocol the mainline Linux kernel's `gs_usb` driver implements. Flash it onto a supported board and the adapter appears to Linux as a native SocketCAN interface, usable by the whole CAN toolchain (candump, Wireshark, python-can) with no vendor driver. It is a firmware project, not hardware: it runs on other projects' boards.

## How it works

The README's supported list covers the candleLight board itself, [CANtact](cantact.md), CANable (and CANable Pro, with a "use with caution" note), several STM32 development and breakout boards, and a set of named community designs (Entreé, CanDIYmore, and others) — all built around STM32F042/F072-class parts with bxCAN classic-CAN controllers, plus USB. Prebuilt binaries are published per board (`candleLight_fw/build/candle.bin` and siblings) and flashed over DFU. The critical capability boundary is the silicon: F042/F072 bxCAN is classic CAN only, so candleLight_fw on its listed boards is a **classic-CAN** solution — CAN FD requires different hardware (see [CFUC](cfuc.md) and [SuperCAN](supercan.md), whose own protocols are not gs_usb).

## Where it fits

candleLight_fw is the standardisation move for the cheap-adapter ecosystem: instead of each dongle inventing a serial protocol (CANtact's original firmware speaks SLCAN), one firmware gives many boards the same kernel-native interface, which is why it is the firmware most of these devices end up running for Linux work. [CANtact](cantact.md) hardware is dual-natured in exactly this sense — SLCAN with its own firmware, gs_usb with this one.

## Limits and safety notes

Scope is bounded by the board list and the classic-CAN peripheral; a board not in the README's list is an unverified port. Flashing is a one-way door if done carelessly — the README's DFU procedure is the recovery story, and unsupported-clone boards are a recurring source of "it flashed but doesn't enumerate" reports the project cannot test against. Licence hygiene is mixed (BSD-3-Clause code with GPL-2.0 glue), which matters for commercial redistribution.

## Status and sources

Checked 2026-11-01. **Maintenance**: the repository is not archived and still receives occasional attention (most recent push 2025-06-20, a CI fix), but the latest release is from October 2021 and feature development has been quiet for years — a mature firmware in upkeep, not growth. That records observed activity, not a promise of support. Documentation claims above come from the following primary sources; no hardware was flashed for this page.

- [Upstream repository](https://github.com/candle-usb/candleLight_fw)
- [Upstream README](https://github.com/candle-usb/candleLight_fw/blob/master/README.md)

## Related

- [CANtact](cantact.md)
- [CFUC](cfuc.md)
- [SuperCAN](supercan.md)
