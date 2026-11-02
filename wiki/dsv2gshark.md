---
uid: 01a19d3c-af81-7c14-942c-7eb8e62caff0
title: "dsV2Gshark"
summary: "Wireshark plugin that dissects ISO 15118 and DIN 70121 traffic, decoding EXI-encoded V2G payloads and SLAC handshakes into readable fields."
type: entity
category: "EV Charging Security"
url: "https://github.com/dspace-group/dsV2Gshark"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Wireshark plugin that dissects ISO 15118 and DIN 70121 traffic, decoding EXI-encoded V2G payloads and SLAC handshakes into readable fields."
related: [acccs, chargesploit, pyplc, v2gdecoder, wwcp-iso15118, everest, checkocpp]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/dspace-group/dsV2Gshark"
    retrieved: 2026-11-01
  - url: "https://github.com/dspace-group/dsV2Gshark/commit/cde7bebec6b7194c314323d3d091fa11b5d48223"
    retrieved: 2026-11-01
  - url: "https://github.com/dspace-group/dsV2Gshark/blob/cde7bebec6b7194c314323d3d091fa11b5d48223/README.md"
    retrieved: 2026-11-01
---

Wireshark plugin that dissects ISO 15118 and DIN 70121 traffic, decoding EXI-encoded V2G payloads and SLAC handshakes into readable fields.

## What it is

dSPACE's Wireshark plugin for analysing EV-to-EVSE communication. The upstream README lists V2GTP, Supported App Protocol (SAP), SECC Discovery Protocol (SDP), DIN 70121, ISO 15118-2, and preliminary ISO 15118-20 decoding. It also provides XSD validation, Plug & Charge certificate details, HomePlug diagnostic analysis, and example charging captures.

## How it works

Packets reach Wireshark through a PLC sniffer or a direct development Ethernet interface. The plugin decodes EXI-backed V2G messages, can detect schemas when discovery/negotiation packets are absent, and adds filters, colouring, and graphs. EXI decoding is based on cbExiGen. For instrumented TLS tests it can consume disclosed session secrets; the README distinguishes TLS 1.2 master-secret disclosure from TLS 1.3 traffic-secret records.

## Where it fits

A first choice for inspecting captures from [AcCCS](acccs.md), [ChargeSploit](chargesploit.md), [pyPLC](pyplc.md), [WWCP_ISO15118](wwcp-iso15118.md), or [EVerest](everest.md). Certificate display helps investigate Plug & Charge exchanges, without establishing that a contract was authorised. [V2Gdecoder](v2gdecoder.md) instead exposes explicit XML/EXI conversion; [CheckOCPP](checkocpp.md) inspects charger-to-backend traffic.

## Limits and safety notes

ISO 15118-20 is explicitly not fully supported. Wireshark 4.4+ requires plugin 1.4.2 or later; the plugin is 64-bit only and incompatible with other V2G dissector plugins. Linux/macOS installation and profile setup need manual steps. TLS decryption requires secrets disclosed by a compatible test endpoint; upstream says ordinary production TLS sessions cannot simply be decrypted. Lost capture packets can corrupt TCP/TLS analysis, so separate a capture problem from a protocol violation. Protect captures containing certificates or disclosed session secrets.

## Status and sources

Checked 2026-11-01. **Active** at this check: the repository is not archived and its latest default-branch commit is dated 2026-10-28. This records observed project activity, not a promise of support or protocol completeness. See the [checked commit](https://github.com/dspace-group/dsV2Gshark/commit/cde7bebec6b7194c314323d3d091fa11b5d48223). Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream README](https://github.com/dspace-group/dsV2Gshark/blob/cde7bebec6b7194c314323d3d091fa11b5d48223/README.md)

## Related

- [AcCCS](acccs.md)
- [ChargeSploit](chargesploit.md)
- [pyPLC](pyplc.md)
- [V2Gdecoder](v2gdecoder.md)
- [WWCP_ISO15118](wwcp-iso15118.md)
- [EVerest](everest.md)
- [CheckOCPP](checkocpp.md)
