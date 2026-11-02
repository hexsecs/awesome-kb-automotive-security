---
uid: 01a19d3c-af25-74f7-a2fd-69719c058eb0
title: "AcCCS"
summary: "Idaho National Laboratory test platform on a Raspberry Pi that emulates either the vehicle or the charger in a CCS session, driving the J1772 control pilot…"
type: entity
category: "EV Charging Security"
url: "https://github.com/IdahoLabResearch/AcCCS"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Idaho National Laboratory test platform on a Raspberry Pi that emulates either the vehicle or the charger in a CCS session, driving the J1772 control pilot, HomePlug Green PHY SLAC, and DIN 70121 exchange so either side can be tested without the other present."
related: [pyplc, open-plc-utils, chargesploit, dsv2gshark]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/IdahoLabResearch/AcCCS"
    retrieved: 2026-11-01
  - url: "https://github.com/IdahoLabResearch/AcCCS/commit/1ff96ff0a2446c9432d3a0000d3f1e943730edcf"
    retrieved: 2026-11-01
  - url: "https://github.com/IdahoLabResearch/AcCCS/blob/1ff96ff0a2446c9432d3a0000d3f1e943730edcf/README.md"
    retrieved: 2026-11-01
---

Idaho National Laboratory test platform on a Raspberry Pi that emulates either the vehicle or the charger in a CCS session, driving the J1772 control pilot, HomePlug Green PHY SLAC, and DIN 70121 exchange so either side can be tested without the other present.

## What it is

Access Capabilities for CCS is Idaho National Laboratory's hardware-and-software test platform for emulating an electric vehicle communications controller (EVCC) or supply equipment communications controller (SECC). Its purpose is to keep a CCS peer connected long enough to investigate its network interface, without needing the other real endpoint. The upstream README describes a Raspberry Pi 4, Green PHY evaluation boards, and a control-pilot/relay board.

## How it works

The documented stack combines J1772 pilot-state emulation, HomePlug Green PHY SLAC pairing, UDP SECC discovery, and TCP over IPv6 link-local addresses. Python scripts use Scapy for packets and smbus for I2C relay control. The README describes EV and EVSE roles and basic endpoint port-scanning support. The pilot hardware and the Green PHY modem are required parts of this setup; Ethernet software alone does not reproduce the physical connection.

## Where it fits

Useful for a controlled lab where the test requires both pilot signalling and a PLC connection. [pyPLC](pyplc.md) provides another research implementation of the vehicle/charger roles; [open-plc-utils](open-plc-utils.md) addresses the underlying modem and SLAC layer. Capture the resulting session with [dsV2Gshark](dsv2gshark.md); use [ChargeSploit](chargesploit.md) when the focus is extensible application-message handling.

## Limits and safety notes

The README says the original code was primarily developed against the older DIN 70121 schema, tested with few vehicles/chargers, and is not a finished product. It labels the MIM script **not implemented**. Its EVSE description calls ISO 15118-2/-20 future work, while later sections describe newer entry points and Plug & Charge certificate generation. That inconsistency remains unresolved at this check: certificate instructions alone do not establish working ISO 15118-2/-20, TLS, or Plug & Charge interoperability. Verify the selected implementation before relying on those features. Pilot/relay emulation interacts with charging hardware; use an isolated, authorised bench and independently enforce electrical safety.

## Status and sources

Checked 2026-11-01. **Active** at this check: the repository is not archived and its latest default-branch commit is dated 2026-03-30. This records observed project activity, not a promise of support or protocol completeness. See the [checked commit](https://github.com/IdahoLabResearch/AcCCS/commit/1ff96ff0a2446c9432d3a0000d3f1e943730edcf). Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream README](https://github.com/IdahoLabResearch/AcCCS/blob/1ff96ff0a2446c9432d3a0000d3f1e943730edcf/README.md)

## Related

- [pyPLC](pyplc.md)
- [open-plc-utils](open-plc-utils.md)
- [ChargeSploit](chargesploit.md)
- [dsV2Gshark](dsv2gshark.md)
