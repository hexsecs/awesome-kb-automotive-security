---
title: "pyPLC"
summary: "Python toolkit for CCS charging research that can pose as vehicle or charger, sniff HomePlug Green PHY traffic, and walk the SLAC, DIN 70121, and ISO 15118…"
type: entity
category: "EV Charging Security"
url: "https://github.com/uhi22/pyPLC"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python toolkit for CCS charging research that can pose as vehicle or charger, sniff HomePlug Green PHY traffic, and walk the SLAC, DIN 70121, and ISO 15118 state machines."
related: [open-plc-utils, openv2g, acccs, chargesploit, dsv2gshark, everest, v2gdecoder, charging-trust-chain]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/uhi22/pyPLC"
    retrieved: 2026-11-01
  - url: "https://github.com/uhi22/pyPLC/commit/be5139bc6e66ba3b3bfa502666f494d3e157968b"
    retrieved: 2026-11-01
  - url: "https://github.com/uhi22/pyPLC/blob/be5139bc6e66ba3b3bfa502666f494d3e157968b/readme.md"
    retrieved: 2026-11-01
  - url: "https://github.com/uhi22/pyPLC/blob/be5139bc6e66ba3b3bfa502666f494d3e157968b/doc/EvseMode.md"
    retrieved: 2026-11-01
---

Python toolkit for CCS charging research that can pose as vehicle or charger, sniff HomePlug Green PHY traffic, and walk the SLAC, DIN 70121, and ISO 15118 state machines.

## What it is

A Python CCS experimentation toolkit using powerline adaptors. Its README defines ListenMode for observing communication, EvseMode for the charger side, and PevMode for the vehicle side. The project includes state machines, hardware interfaces, captures, log/PCAP conversion helpers, and simulation/fault-injection material.

## How it works

A configured HomePlug modem provides access to the pilot-line PLC network; Python handles SLAC, IPv6 communication, and the higher-level session state. The documented setup uses [open-plc-utils](open-plc-utils.md) to configure adaptors and the OpenV2Gx fork of [OpenV2G](openv2g.md) for EXI conversion. The README's 2026 update describes DIN 70121 plus experimental ISO1 support. Full sniffing depends on suitable transparent firmware; stock TP-Link firmware sees only SLAC/broadcast traffic, while specified QCA7000/QCA7005 firmware and a patched AR7420 build expose more traffic.

## Where it fits

Useful for learning the full CCS communication path, comparing vehicle/charger state transitions, and analysing supplied session traces. [AcCCS](acccs.md) is another hardware-backed test platform; [ChargeSploit](chargesploit.md) emphasises pluggable message handlers. [dsV2Gshark](dsv2gshark.md) provides packet-level analysis and [EVerest](everest.md) a modular charging-stack counterpart.

## Limits and safety notes

Do not read the historical change log as a guarantee that every reported experiment works on every vehicle. The README calls ISO1 experimental and says larger-scale field testing of the AR7420 transparency patch is ongoing. The checked sources do not establish ISO 15118-20 or complete TLS/Plug & Charge support. The EvseMode manual explicitly discusses additional power hardware and vehicle-dependent contactor behaviour. Communication can influence a real energy-transfer system; use simulation or an electrically controlled, authorised bench rather than assuming a communication-only experiment is harmless.

## Status and sources

Checked 2026-11-01. **Active** at this check: the repository is not archived and its latest default-branch commit is dated 2026-10-29. This records observed project activity, not a promise of support or protocol completeness. See the [checked commit](https://github.com/uhi22/pyPLC/commit/be5139bc6e66ba3b3bfa502666f494d3e157968b). Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream README](https://github.com/uhi22/pyPLC/blob/be5139bc6e66ba3b3bfa502666f494d3e157968b/readme.md)
- [EvseMode manual](https://github.com/uhi22/pyPLC/blob/be5139bc6e66ba3b3bfa502666f494d3e157968b/doc/EvseMode.md)

## Related

- [open-plc-utils](open-plc-utils.md)
- [OpenV2G](openv2g.md)
- [AcCCS](acccs.md)
- [ChargeSploit](chargesploit.md)
- [dsV2Gshark](dsv2gshark.md)
- [EVerest](everest.md)
- [V2Gdecoder](v2gdecoder.md)
