---
uid: 01a1ba7a-e336-72d9-9b77-ff600b7bb9e0
title: "LinUSBConverter"
summary: "Open-source USB to LIN bus dongle that operates as master, slave or monitor with optical isolation and SLCAN compatibility for vehicle LIN traffic."
type: entity
category: "Hardware Interfaces"
url: "https://github.com/uCAN-LIN/LinUSBConverter"
status: active
last_checked: 2026-11-17
created: 2026-11-08
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 825c8e5
list_summary: "Open-source USB to LIN bus dongle that operates as master, slave or monitor with optical isolation and SLCAN compatibility for vehicle LIN traffic."
related:
  - security-in-automotive-bus-systems
  - doggie
  - cfuc
  - autopi
  - automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps
  - lin-bus
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-08
  - url: "https://github.com/uCAN-LIN/LinUSBConverter"
    retrieved: 2026-11-17
  - url: "https://raw.githubusercontent.com/uCAN-LIN/LinUSBConverter/master/README.md"
    retrieved: 2026-11-17
  - url: "https://api.github.com/repos/uCAN-LIN/LinUSBConverter"
    retrieved: 2026-11-17
---

Open-source USB to LIN bus dongle that operates as master, slave or monitor with optical isolation and SLCAN compatibility for vehicle LIN traffic.

## What it is

The USB LIN Converter (uLC) is a small open-source dongle (STM32F042, roughly 31 × 18 mm) that lets a PC act as a LIN 2.1 master, slave or passive monitor. It enumerates as a USB CDC virtual COM port and speaks an SLCAN-style ASCII protocol, so no proprietary driver is needed on Windows, Linux or macOS, and it bridges into Linux SocketCAN via `slcand`. The repository ships firmware, KiCad hardware and a Python helper library; the LIN implementation is based on [openLIN](https://github.com/open-LIN). At around $27 it is positioned against commercial LIN analysers that cost hundreds to thousands of euros.

## How it works

The device is controlled by short ASCII commands terminated with CR: `O` opens master mode, `L` slave mode, `l` monitor mode, `C` closes the port, and `S0`/`S2` select 19200/9600 baud. Monitor mode gives full frame reception plus single-frame transmission; master and slave modes each support up to 16 scheduled slots, with explicit per-slot delay and response-wait timing (`T`/`R` commands) for building a schedule table. Checksum style is switchable between classic LIN 1.x and enhanced LIN 2.x (`r31`/`r30`), with diagnostic frames 0x3C/0x3D always using classic. The LIN transceiver is optically isolated from the USB side and powered externally at 4.5–28 V, while software-controlled termination resistors remove the need to rewire the bench. Firmware updates go through the STM32F042's USB DFU bootloader.

A Python package (`ucanlintools`) provides higher-level master/slave/monitor helpers, and a bundled MCP server lets an AI agent sniff and reverse-engineer a LIN bus — capture per-ID periods and changing bits, auto-detect baud and checksum type, and encode/decode signals from an LDF. That server is read-only by default; transmitting and acting as master or slave require `--allow-transmit`.

## Where it fits

LIN is the low-cost subordinate bus behind door modules, seats, climate control and steering-wheel controls, so this dongle fills the gap between a CAN tool and a scope when the target is a LIN node. It sits alongside [Doggie](doggie.md) and [CFUC](cfuc.md) in the hardware-interface tier, and its monitor mode feeds the same trace-to-signal workflow described in [automated reverse engineering of CAN bus commands from mobile apps](automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps.md). [AutoPi](autopi.md) is the always-connected vehicle platform; for the threat model around these buses see [Security in automotive bus systems](security-in-automotive-bus-systems.md).

## Limits and safety notes

This is a generic LIN interface, not an ECU flasher: flashing over LIN depends entirely on the target ECU's own bootloader being documented or already supported. It is a single-bus, 9600/19200-baud dongle — no LIN 2.2 features beyond what the firmware implements, and the host must supply the LIN-side power. Slave simulation and master scheduling are active operations: a wrong schedule or a bad response can drive real actuators, so use a bench and an isolated segment. The upstream test suite is thorough (firmware 3.8 reports 66/66 passes per direction over two dongles), but those are the project's own results, not independently reproduced here. No hardware was exercised for this page, and the MCP transmit path was not used.

## Status and sources

Checked 2026-11-17. **Active** at this check: public, not archived, GPL-3.0, 94 stars / 42 forks / 10 open issues, default branch last pushed 2026-11-03 (firmware 3.8 era). Repository activity is not a support guarantee.

- [Upstream README](https://raw.githubusercontent.com/uCAN-LIN/LinUSBConverter/master/README.md)
- [Repository metadata](https://api.github.com/repos/uCAN-LIN/LinUSBConverter)
- [Product documentation](https://ucandevices.github.io/ulc.html)

## Related

- [Security in automotive bus systems](security-in-automotive-bus-systems.md)
- [Doggie](doggie.md)
- [CFUC](cfuc.md)
- [AutoPi](autopi.md)
- [Automated cross-platform reverse engineering of CAN bus commands from mobile apps](automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps.md)
- [LIN as the trusted subordinate bus](concepts/lin-bus.md)
