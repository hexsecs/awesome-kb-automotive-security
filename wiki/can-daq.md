---
uid: 01a19d3c-af3f-751e-897a-a5f027402dfe
title: "CAN-DAQ"
summary: "Open hardware ESP32-S3 CAN data-capture device with DBC-driven real-time plotting and SQLite logging, published in HardwareX as a sub-$25 alternative to…"
type: entity
category: "Hardware Interfaces"
url: "https://github.com/eccentricOrange/can-daq"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open hardware ESP32-S3 CAN data-capture device with DBC-driven real-time plotting and SQLite logging, published in HardwareX as a sub-$25 alternative to commercial CAN loggers."
related: [ramn, cantact]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/eccentricOrange/can-daq"
    retrieved: 2026-11-01
  - url: "https://github.com/eccentricOrange/can-daq/blob/main/README.md"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1016/j.ohx.2026.e00743"
    retrieved: 2026-11-01
---

Open hardware ESP32-S3 CAN data-capture device with DBC-driven real-time plotting and SQLite logging, published in HardwareX as a sub-$25 alternative to commercial CAN loggers.

## What it is

An open-hardware CAN bus data-acquisition device (CC-BY-4.0) built around an ESP32-S3: custom PCB, firmware, and host software, published as a peer-reviewed HardwareX paper (vol. 25, e00743, 2026) as well as a repository. It captures classic CAN traffic, decodes it against a DBC file, plots signals live, and stores everything to a local SQLite database for analysis. The cost claim upstream is "less than INR 2000" for the device as manufactured by the authors — the list summary's "sub-$25" is a currency conversion of that figure, not a price the project itself states.

## How it works

The ESP32-S3's built-in TWAI controller talks to the bus through an external transceiver — the main README names the **MCP2561** (sub-READMEs in the repository inconsistently say "MCP2561FD" and "MCP2651FD"; this page follows the main README and flags the inconsistency rather than resolving it). Classic CAN 2.0 only (TWAI has no CAN FD), at up to 1 Mbps, with a maximum sampling rate of 1 kHz. The host link is **wired**: a USB-UART connection (micro-B, up to 3 Mbit/s) to the PC software that plots and logs. WiFi is **not** used in the current design. Nor is the device passive-only: the firmware can transmit frames sent from the PC, so it can act on a bus, not just observe one. The documented validation is a bench loopback described in the HardwareX paper; the repository does not document on-vehicle test results.

## Where it fits

CAN-DAQ occupies the cheap, self-contained end of data capture: where the other devices in this section are USB peripherals that make a laptop into a CAN node, this one packages capture, DBC decoding, plotting, and logging into one small published design. For teaching and fleet-style logging that is the appeal; [RAMN](ramn.md) is the same open-hardware spirit aimed at a whole miniature network rather than one bus tap.

## Limits and safety notes

Classic CAN only, single channel, 1 kHz maximum sampling — busy-bus behaviour at high load is bounded by those numbers, and the documented validation is a bench loopback, not a vehicle. The cost figure assumes the authors' manufacturing route in India; fabricating one board elsewhere will differ. Because the firmware transmits as well as receives, it belongs on bench buses first, like every active interface in this section.

## Status and sources

Checked 2026-11-01. **Unknown**: the repository is not archived; its entire history is two commits (the initial commit, 2025-04-13, and a citation commit, 2026-02-10) with one release (v1.0.0, 2025-04-13). The design reads as publication-complete with low ongoing activity, and the HardwareX paper gives it a fixed, citable reference point — but two commits are too little record to classify further. Documentation claims above come from the following primary sources; no hardware was built or run for this page.

- [Upstream repository](https://github.com/eccentricOrange/can-daq)
- [Upstream README](https://github.com/eccentricOrange/can-daq/blob/main/README.md)
- [HardwareX paper](https://doi.org/10.1016/j.ohx.2026.e00743)

## Related

- [RAMN](ramn.md)
- [CANtact](cantact.md)
