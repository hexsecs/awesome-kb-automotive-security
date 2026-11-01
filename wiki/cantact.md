---
title: "CANtact"
summary: "Open-source hardware CAN interface and desktop app supporting live tracing, frame transmission, ISO-TP, JavaScript scripting, and candump-format traces."
type: entity
category: "Hardware Interfaces"
url: "https://github.com/linklayer/cantact-app"
status: unknown
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

One of the original open-source hardware CAN interfaces: a small USB-to-CAN board (STM32F042-class) with open hardware designs, open firmware (cantact-fw), and a cross-platform desktop application (cantact-app — this page's listed URL) for interacting with a bus. CANtact's historical importance is that it made a hackable, documented CAN interface cheap and reproducible years before the current adapter crowd; its documentation site (linklayer.github.io/cantact) still describes the full stack. The firmware's licence picture is mixed (the repository records NOASSERTION; the sources are MIT alongside ST libraries).

## How it works

The board is a single-channel **classic CAN** interface — the F042's bxCAN peripheral sets the ceiling, so no CAN FD. With its own firmware, the device speaks SLCAN (the serial-line CAN protocol) to the host; flash [candleLight_fw](candlelight-fw.md) instead and the same hardware becomes a gs_usb/SocketCAN device — the CANtact Book (cantact.io) in fact requires candleLight firmware for its modern setup path. The desktop app (Java) provides the interactive surface the list summary names: live frame tracing, frame transmission, ISO-TP transport support, JavaScript scripting of the interface, and candump-format trace import/export — the feature set that made it a teaching tool for CAN basics.

## Where it fits

CANtact is the reference point this section grew from: [candleLight_fw](candlelight-fw.md) exists largely because of boards like it, and modern FD adapters ([CFUC](cfuc.md), [SuperCAN](supercan.md)) are answers to its classic-CAN limit. Against [panda](panda.md) it is the simpler instrument — one bus, no safety model, everything manual. Its living continuation is split across successors (see Status): the Rust `linklayer/cantact` application, candleLight firmware on the same hardware, and the CANtact Book documentation.

## Limits and safety notes

Classic CAN only, one channel, and USB-serial-class throughput. The project state needs care (see Status): the original app and firmware repositories are dormant — neither is archived, but neither has seen code in years — so new users should start from the successor application and candleLight firmware rather than treating the 2016-era app as the current software story. Clones and derivative boards vary in quality and are not this project's hardware. As with every transmitting interface here, an unsuspecting bus is not a lab: bench first.

## Status and sources

Checked 2026-11-01. **Unknown** — a split record, stated in full: **neither** repository is archived. The listed cantact-app repository's HEAD commit is dated 2016-06-01 (repository last pushed 2020-04-13), and its last release is v0.3.0-alpha (2016); cantact-fw's HEAD commit is 2017-06-09 (repository last pushed 2023-06-30), with no releases. The original line is dormant, not formally ended. The living continuation lives elsewhere: the successor Rust application `linklayer/cantact` (pushed 2024-08-26), candleLight_fw running on CANtact hardware (pushed 2026-10-02), and the CANtact Book. "Unknown" records that the listed repositories themselves show no classifiable ongoing project state. Documentation claims above come from the following primary sources; no hardware was run for this page.

- [Listed repository (cantact-app)](https://github.com/linklayer/cantact-app)
- [Firmware repository (cantact-fw)](https://github.com/linklayer/cantact-fw)
- [Project documentation](https://linklayer.github.io/cantact/)

## Related

- [candleLight_fw](candlelight-fw.md)
- [panda](panda.md)
- [CAN-DAQ](can-daq.md)
