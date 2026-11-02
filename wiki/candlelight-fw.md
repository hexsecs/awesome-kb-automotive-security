---
title: "candleLight_fw"
summary: "Open firmware for low-cost STM32 USB to CAN adapters such as CANable, cantact, and candleLight that implements the mainline Linux gs_usb interface, turning…"
type: entity
category: "Hardware Interfaces"
url: "https://github.com/candle-usb/candleLight_fw"
status: active
last_checked: 2026-11-01
created: 2026-10-31
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

Open firmware that makes inexpensive STM32-based USB-CAN adapters speak **gs_usb** — the USB protocol the mainline Linux kernel's `gs_usb` driver implements. Flash it onto a supported board and the adapter appears to Linux as a native SocketCAN interface, usable by the whole CAN toolchain (candump, Wireshark, python-can) with no vendor driver. It is a firmware project, not hardware: it runs on other projects' boards. Licence hygiene is layered, and worth stating precisely: the candleLight sources themselves are MIT, the STM32 HAL is BSD, and the ST USB library is under ST's SLA0044 terms (the repository's recorded licence resolves to NOASSERTION for exactly this reason).

## How it works

The README's supported list covers the candleLight board itself, [CANtact](cantact.md), CANable (and CANable Pro, with a "use with caution" note), several STM32 development and breakout boards, and a set of named community designs (Entreé, CanDIYmore, and others). Distribution is through **CI artifacts** — the only GitHub release is v2.0 (2022-04-19) — and binaries are flashed over DFU. Two silicon boundaries are explicit upstream: the STM32F103 **cannot** work (its USB and CAN peripherals conflict), and G0B1 and G431 devices are **not yet supported** by the mainline firmware — CAN FD support is in progress (an m_can pull request was merged in July 2026). On its currently supported boards, candleLight_fw is therefore a **classic-CAN** solution; CAN FD today means different hardware (see [CFUC](cfuc.md) and [SuperCAN](supercan.md), whose own protocols are not gs_usb).

## Where it fits

candleLight_fw is the standardisation move for the cheap-adapter ecosystem: instead of each dongle inventing a serial protocol (CANtact's original firmware speaks SLCAN), one firmware gives many boards the same kernel-native interface, which is why it is the firmware most of these devices end up running for Linux work. [CANtact](cantact.md) hardware is dual-natured in exactly this sense — SLCAN with its own firmware, gs_usb with this one — and the CANtact Book's modern setup path requires candleLight firmware.

## Limits and safety notes

Scope is bounded by the board list and, for now, the classic-CAN peripheral; a board not in the README's list is an unverified port, and the F103 exclusion and pending G0B1/G431 support are hard upstream statements, not gaps to improvise around. Flashing is a one-way door if done carelessly — the README's DFU procedure is the recovery story, and unsupported-clone boards are a recurring source of "it flashed but doesn't enumerate" reports the project cannot test against. The mixed licence stack (MIT / BSD / SLA0044) matters for commercial redistribution.

## Status and sources

Checked 2026-11-01. **Active**: the repository is not archived and development continues — most recent push 2026-10-02, with commits through September 2026 and FD work landing (the m_can PR merged 2026-07-17). The release cadence is misleading if read alone: v2.0 (2022-04-19) is the only GitHub release because distribution runs through CI artifacts. That records observed activity, not a promise of support. Documentation claims above come from the following primary sources; no hardware was flashed for this page.

- [Upstream repository](https://github.com/candle-usb/candleLight_fw)
- [Upstream README](https://github.com/candle-usb/candleLight_fw/blob/master/README.md)

## Related

- [CANtact](cantact.md)
- [CFUC](cfuc.md)
- [SuperCAN](supercan.md)
