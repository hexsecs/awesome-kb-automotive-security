---
title: "WWCP_ISO15118"
summary: "ISO 15118 implementation covering SLAC, SDP, V2GTP, -2 and -20, explicitly shipping attack vectors and penetration-testing workflows for the individual…"
type: entity
category: "EV Charging Security"
url: "https://github.com/OpenChargingCloud/WWCP_ISO15118"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "ISO 15118 implementation covering SLAC, SDP, V2GTP, -2 and -20, explicitly shipping attack vectors and penetration-testing workflows for the individual subprotocols."
related: [chargesploit, dsv2gshark, openv2g, v2gdecoder, everest]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/OpenChargingCloud/WWCP_ISO15118"
    retrieved: 2026-11-01
  - url: "https://github.com/OpenChargingCloud/WWCP_ISO15118/commit/e2f9d3e961f136183c171f38a6de3f623468efd1"
    retrieved: 2026-11-01
  - url: "https://github.com/OpenChargingCloud/WWCP_ISO15118/blob/e2f9d3e961f136183c171f38a6de3f623468efd1/README.md"
    retrieved: 2026-11-01
---

ISO 15118 implementation covering SLAC, SDP, V2GTP, -2 and -20, explicitly shipping attack vectors and penetration-testing workflows for the individual subprotocols.

## What it is

OpenChargingCloud's C# implementation of EV-to-charger communication, with codec and session layers and penetration-testing workflows. The README covers SLAC, SDP, V2GTP, ISO 15118-2/-20, and wireless -8 communication. It presents the implementation as a conformance/research peer, not a safe standalone charging station.

## How it works

Build-time source generation turns separately fetched ISO XSDs into EXI codecs. Per-message-set assemblies handle -2 and -20 payloads, with a V2GTP dispatcher and XMLDSig support. The session layer provides EVCC/SECC state machines, discovery, SLAC, TCP/TLS transports, and Plug & Charge flows. The README separates -2 payment/authorisation/signature steps from -20 certificate installation and session resumption. Pure state transitions allow conversation tests without a live socket.

## Where it fits

Useful for inspecting wire-format behaviour and comparing independent protocol peers such as [ChargeSploit](chargesploit.md) or [EVerest](everest.md). [dsV2Gshark](dsv2gshark.md) can inspect captures. [OpenV2G](openv2g.md) and [V2Gdecoder](v2gdecoder.md) supply alternative codec implementations, with different protocol coverage and dependencies.

## Limits and safety notes

ISO schemas are not redistributed: fetching them is subject to ISO's licence. Only the codec solution builds from a standalone clone; the session/CLI layer needs the parent checkout layout and a sibling Hermod project. Upstream explicitly says certificate chains are validated only when trust roots are supplied and revocation is never checked; absent roots, signature checks use the presented leaf. It also documents simplified timeouts, a short simulated charge loop unless configured otherwise, and no electrical safety layer, contactors, pilot control, or isolation monitoring. These restrictions matter directly to Plug & Charge: signature correctness is not a complete decision that a contract is valid. Keep use to controlled conformance/research tests.

## Status and sources

Checked 2026-11-01. **Active** at this check: the repository is not archived and its latest default-branch commit is dated 2026-10-29. This records observed project activity, not a promise of support or protocol completeness. See the [checked commit](https://github.com/OpenChargingCloud/WWCP_ISO15118/commit/e2f9d3e961f136183c171f38a6de3f623468efd1). Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream README](https://github.com/OpenChargingCloud/WWCP_ISO15118/blob/e2f9d3e961f136183c171f38a6de3f623468efd1/README.md)

## Related

- [ChargeSploit](chargesploit.md)
- [dsV2Gshark](dsv2gshark.md)
- [OpenV2G](openv2g.md)
- [V2Gdecoder](v2gdecoder.md)
- [EVerest](everest.md)
