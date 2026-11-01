---
title: "SuperCAN"
summary: "Open-source USB to CAN FD adapter firmware for the ATSAME51 and several other supported boards, giving a low-cost interface for capturing and injecting CAN…"
type: entity
category: "Hardware Interfaces"
url: "https://github.com/jgressmann/supercan"
status: active
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
  - url: "https://github.com/jgressmann/supercan/releases/tag/v1.0.28"
    retrieved: 2026-11-01
---

Open-source USB to CAN FD adapter firmware for the ATSAME51 and several other supported boards, giving a low-cost interface for capturing and injecting CAN and CAN FD traffic.

## What it is

Open-source firmware (MIT licence, with matched host software) that turns supported microcontroller boards into USB-to-**CAN FD** adapters — capture and injection of classic CAN and CAN FD traffic from a low-cost dev board instead of a commercial interface. The flagship target is Microchip's ATSAME51 (the firmware is built with Microchip's MPLAB Harmony tooling), and the README's device list is broader than the flagship: Feather M4 CAN Express, the D5035 series, CANBED M4, SAM E54 Xplained Pro, NUCLEO-H7A3ZI-Q, STM32F3DISCOVERY, and Teensy 4.x. Anything not on that list is not an official target, and some listed channels are classic-CAN only (Teensy CAN1, the F3's CAN0).

## How it works

SuperCAN deliberately does **not** implement gs_usb: it defines its own USB protocol, with the project's own driver/app stack. Host paths split by platform. On **Windows**, the project ships drivers and apps, and its python-can plugin is Windows-only. On **Linux**, SocketCAN comes from a **separate out-of-tree DKMS kernel driver** (`jgressmann/supercan-linux`) — not from a user-space bridge — and Linux users should use the socketcan interface type rather than the python-can plugin. A scope warning the sources force: an older, unrelated same-name Windows driver circulates for CANtact/candleLight-class hardware — the SuperCAN *firmware* documented here does not support that hardware, and the two should not be conflated. On rates: the project states **no project-wide maximum CAN FD data rate**; the only figure upstream is a hardware claim for one board (the D5035-01, 8 Mbit/s data phase), and this page does not generalise it.

## Where it fits

SuperCAN and [CFUC](cfuc.md) are the two open CAN FD adapter answers in this section, split by host philosophy: CFUC bets on firmware choice (a gs_usb port or a python-can CDC build); SuperCAN bets on its own protocol with a maintained Windows stack and a real (if out-of-tree) Linux kernel driver. Both exist because the [candleLight_fw](candlelight-fw.md) generation is classic-CAN only. For a researcher on Windows, or already holding a supported SAME51 board, SuperCAN is the shorter path.

## Limits and safety notes

Board scope is the list in the README — no CANtact/CANable support despite the historical name collision, and no promise for unlisted SAME51 variants. Per-channel capability varies within the list (some channels are classic-only, above), and the Linux driver is out-of-tree DKMS, so kernel upgrades are the user's maintenance problem. Development is maintenance-paced rather than feature-driven (see Status), so the protocol and board set should be treated as settled rather than expanding.

## Status and sources

Checked 2026-11-01. **Active**, at a maintenance pace: the repository is not archived, its latest commit is dated 2026-10-27, and the latest release is v1.0.28 (2026-02-19) — a long-running project still being tended, with the companion Linux driver repository pushed 2026-05-03. That records observed activity, not a promise of support. Documentation claims above come from the following primary sources; no hardware was run for this page.

- [Upstream repository](https://github.com/jgressmann/supercan)
- [Upstream README](https://github.com/jgressmann/supercan/blob/main/README.md)
- [Release v1.0.28](https://github.com/jgressmann/supercan/releases/tag/v1.0.28)

## Related

- [CFUC](cfuc.md)
- [candleLight_fw](candlelight-fw.md)
- [CANtact](cantact.md)
