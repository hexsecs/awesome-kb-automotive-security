---
title: "CANtact"
summary: "Open-source hardware CAN interface and desktop app supporting live tracing, frame transmission, ISO-TP, JavaScript scripting, and candump-format traces."
type: entity
category: "Hardware Interfaces"
url: "https://github.com/linklayer/cantact-app"
status: maintenance
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source hardware CAN interface and desktop app supporting live tracing, frame transmission, ISO-TP, JavaScript scripting, and candump-format traces."
related: [candlelight-fw, panda, can-daq]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/linklayer/cantact-app"
    retrieved: 2026-11-01
  - url: "https://github.com/linklayer/cantact-fw"
    retrieved: 2026-11-01
  - url: "https://linklayer.github.io/cantact/"
    retrieved: 2026-11-01
---

Open-source hardware CAN interface and desktop app supporting live tracing, frame transmission, ISO-TP, JavaScript scripting, and candump-format traces.

## What it is

One of the original open-source hardware CAN interfaces: a small USB-to-CAN board (STM32F042-class) with open hardware designs, open firmware (cantact-fw), and a cross-platform desktop application (cantact-app — this page's listed URL) for interacting with a bus. CANtact's historical importance is that it made a hackable, documented CAN interface cheap and reproducible years before the current adapter crowd; its documentation site (linklayer.github.io/cantact) still describes the full stack.

## How it works

The board is a single-channel **classic CAN** interface — the F042's bxCAN peripheral sets the ceiling, so no CAN FD. With its own firmware, the device speaks SLCAN (the serial-line CAN protocol) to the host; flash [candleLight_fw](candlelight-fw.md) instead and the same hardware becomes a gs_usb/SocketCAN device. The desktop app (Java) provides the interactive surface the list summary names: live frame tracing, frame transmission, ISO-TP transport support, JavaScript scripting of the interface, and candump-format trace import/export — the feature set that made it a teaching tool for CAN basics.

## Where it fits

CANtact is the reference point this section grew from: [candleLight_fw](candlelight-fw.md) exists largely because of boards like it, and modern FD adapters ([CFUC](cfuc.md), [SuperCAN](supercan.md)) are answers to its classic-CAN limit. Against [panda](panda.md) it is the simpler instrument — one bus, no safety model, everything manual.

## Limits and safety notes

Classic CAN only, one channel, and USB-serial-class throughput. The project state needs care (see Status): the listed app repository is archived, so new users should start from the successor the README names rather than treating the archived app as the current software story. Clones and derivative boards vary in quality and are not this project's hardware. As with every transmitting interface here, an unsuspecting bus is not a lab: bench first.

## Status and sources

Checked 2026-11-01. **Maintenance** — a split picture, recorded in full: the listed repository, cantact-app, was **archived by its owner on 2025-04-06**, and its README states that development moved to a successor Rust application (linklayer/cantact, actively pushed as of late 2025), which is a different resource from the one listed. The firmware repository (cantact-fw) is not archived but has been quiet since 2024-05-24. The hardware designs and documentation remain published and usable; the original software line is in upkeep-by-successor rather than development. Documentation claims above come from the following primary sources; no hardware was run for this page.

- [Listed repository (cantact-app, archived)](https://github.com/linklayer/cantact-app)
- [Firmware repository (cantact-fw)](https://github.com/linklayer/cantact-fw)
- [Project documentation](https://linklayer.github.io/cantact/)

## Related

- [candleLight_fw](candlelight-fw.md)
- [panda](panda.md)
- [CAN-DAQ](can-daq.md)
