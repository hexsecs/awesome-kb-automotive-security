---
title: "SuperCAN"
summary: "Open-source USB to CAN FD adapter firmware for the ATSAME51 and several other supported boards, giving a low-cost interface for capturing and injecting CAN…"
type: entity
category: "Hardware Interfaces"
url: "https://github.com/jgressmann/supercan"
status: maintenance
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source USB to CAN FD adapter firmware for the ATSAME51 and several other supported boards, giving a low-cost interface for capturing and injecting CAN and CAN FD traffic."
related: [cfuc, candlelight-fw, cantact]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/jgressmann/supercan"
    retrieved: 2026-11-01
  - url: "https://github.com/jgressmann/supercan/blob/main/README.md"
    retrieved: 2026-11-01
  - url: "https://github.com/jgressmann/supercan/releases/tag/v1.2.3"
    retrieved: 2026-11-01
---

Open-source USB to CAN FD adapter firmware for the ATSAME51 and several other supported boards, giving a low-cost interface for capturing and injecting CAN and CAN FD traffic.

## What it is

Open-source firmware (with matched host software) that turns supported microcontroller boards into USB-to-**CAN FD** adapters — capture and injection of classic CAN and CAN FD traffic from a low-cost dev board instead of a commercial interface. The flagship target is Microchip's ATSAME51 (the firmware is built with Microchip's MPLAB Harmony tooling), and the README's official device list names the supported boards; anything not on that list is not an official target.

## How it works

SuperCAN deliberately does **not** implement gs_usb: it defines its own USB protocol, with the project's own driver/app stack providing official Windows support and a Linux user-space path (the README notes SocketCAN reachability via cannelloni rather than a native kernel driver). A scope warning the sources force: an older, unrelated same-name Windows driver circulates for CANtact/candleLight-class hardware — the SuperCAN *firmware* documented here does not support that hardware, and the two should not be conflated. Protocol documentation lives in the repository for anyone implementing against it.

## Where it fits

SuperCAN and [CFUC](cfuc.md) are the two open CAN FD adapter answers in this section, split by host philosophy: CFUC bets on gs_usb and the Linux kernel; SuperCAN bets on its own protocol and a maintained Windows story. Both exist because the [candleLight_fw](candlelight-fw.md) generation is classic-CAN only. For a researcher on Windows, or already holding a supported SAME51 board, SuperCAN is the shorter path.

## Limits and safety notes

Board scope is the list in the README — no CANtact/CANable support despite the historical name collision, and no promise for unlisted SAME51 variants. Linux users trade the kernel-native experience the gs_usb devices get for a user-space bridge. Development has slowed (see Status), so the protocol and board set should be treated as settled rather than expanding.

## Status and sources

Checked 2026-11-01. **Maintenance**: the repository is not archived, but the latest release is v1.2.3 (January 2025) and the most recent push is dated 2025-01-14, closing a 2020–2025 run of steady releases. That records observed activity, not a promise of support. Documentation claims above come from the following primary sources; no hardware was run for this page.

- [Upstream repository](https://github.com/jgressmann/supercan)
- [Upstream README](https://github.com/jgressmann/supercan/blob/main/README.md)
- [Release v1.2.3](https://github.com/jgressmann/supercan/releases/tag/v1.2.3)

## Related

- [CFUC](cfuc.md)
- [candleLight_fw](candlelight-fw.md)
- [CANtact](cantact.md)
