---
title: "CAN-DAQ"
summary: "Open hardware ESP32-S3 CAN data-capture device with DBC-driven real-time plotting and SQLite logging, published in HardwareX as a sub-$25 alternative to…"
type: entity
category: "Hardware Interfaces"
url: "https://github.com/eccentricOrange/can-daq"
status: unknown
last_checked: 2026-11-01
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
  - url: "https://doi.org/10.1016/j.ohx.2025.e00700"
    retrieved: 2026-11-01
---

Open hardware ESP32-S3 CAN data-capture device with DBC-driven real-time plotting and SQLite logging, published in HardwareX as a sub-$25 alternative to commercial CAN loggers.

## What it is

An open-hardware CAN bus data-acquisition device (MPL-2.0) built around an ESP32-S3: custom PCB, firmware, and a browser-based GUI, published as a peer-reviewed HardwareX paper (2025) as well as a repository. It is a *logger and viewer*, not a general-purpose interface: it captures classic CAN traffic, decodes it against a DBC file, plots signals live, and stores everything to a local SQLite database for analysis. The bill of materials is costed in the README at roughly US$24 — an author-reported build cost for a self-assembled device, not a product price.

## How it works

The ESP32-S3's built-in TWAI controller talks to the bus through an external SN65HVD230 transceiver (classic CAN only — TWAI has no CAN FD). There is no USB data path: the device runs a WiFi access point, and the user connects a browser to it for live DBC-decoded plotting (a gauge widget is included) and to download prior captures as database files over HTTP. The documented validation is a bench loopback (two ESP32-S3 nodes exchanging frames) described in the HardwareX paper; the repository does not document on-vehicle test results.

## Where it fits

CAN-DAQ occupies the cheap, self-contained end of data capture: where the other devices in this section are USB peripherals that make a laptop into a CAN node, this one removes the laptop — clip it onto a bus, and it logs and visualises on its own. For teaching and fleet-style logging that is the appeal; [RAMN](ramn.md) is the same open-hardware spirit aimed at a whole miniature network rather than one bus tap.

## Limits and safety notes

Classic CAN only, single channel, and the browser-over-WiFi interface is for viewing and retrieval — the README does not document frame transmission, so treat it as a passive capture device unless a primary source says otherwise. The "~$24" figure assumes you fabricate and assemble the board yourself. Repository youth is itself a limit: a small commit history, no releases, and no stated bus-load or throughput figures — load behaviour on a busy production bus is unverified from primary sources.

## Status and sources

Checked 2026-11-01. **Unknown**: the repository (created 2025-05) is not archived, but its history is a handful of commits with the latest dated 2025-05-25 and there are no releases — too little record to classify, though the HardwareX publication gives the design a fixed, citable reference point. Documentation claims above come from the following primary sources; no hardware was built or run for this page.

- [Upstream repository](https://github.com/eccentricOrange/can-daq)
- [Upstream README](https://github.com/eccentricOrange/can-daq/blob/main/README.md)
- [HardwareX paper](https://doi.org/10.1016/j.ohx.2025.e00700)

## Related

- [RAMN](ramn.md)
- [CANtact](cantact.md)
