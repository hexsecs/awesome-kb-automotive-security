---
title: "CheckOCPP"
summary: "Wireshark dissector for OCPP 1.6 and 2.0.1 that identifies the protocol version and flags messages that do not match the schema."
type: entity
category: "EV Charging Security"
url: "https://github.com/vfg27/CheckOCPP"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Wireshark dissector for OCPP 1.6 and 2.0.1 that identifies the protocol version and flags messages that do not match the schema."
related: [emuocpp, everest, ocpp-charging-attacks, ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations, dsv2gshark]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/vfg27/CheckOCPP"
    retrieved: 2026-11-01
  - url: "https://github.com/vfg27/CheckOCPP/commit/19f5040fd8769d9a62f1af7d5b63074b36fbcf52"
    retrieved: 2026-11-01
  - url: "https://github.com/vfg27/CheckOCPP/blob/19f5040fd8769d9a62f1af7d5b63074b36fbcf52/README.md"
    retrieved: 2026-11-01
---

Wireshark dissector for OCPP 1.6 and 2.0.1 that identifies the protocol version and flags messages that do not match the schema.

## What it is

A passive Wireshark dissector for the JSON form of the Open Charge Point Protocol. Its README lists automatic detection of OCPP 1.6, 2.0, and 2.0.1, schema/message-structure checks, and highlighting of non-compliant packets. This is the charger-to-management-system link covered by [OCPP and charging attacks](concepts/ocpp-charging-attacks.md).

## How it works

Lua dissectors load protocol schemas using lua-cjson. Installation requires configuring the schema paths and choosing either a single OCPP dissector or separate version-specific dissectors. Wireshark then exposes message type, message ID, and payload-validation results; optional colouring makes flagged packets easier to find. Captures from [EmuOCPP](emuocpp.md) provide a natural test input.

## Where it fits

Useful for reviewing readable OCPP captures and triaging malformed or misconfigured messages from a charger or CSMS implementation, including a configured [EVerest](everest.md) deployment. It complements active test inputs and the [OCPPStorm paper](ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations.md). [dsV2Gshark](dsv2gshark.md) covers the other side of a charger, the EV-to-EVSE V2G exchange.

## Limits and safety notes

The upstream limitations are explicit: it validates JSON, not SOAP, and encrypted traffic needs decryption keys. Capturing a TLS connection does not by itself make its OCPP payload visible. Schema conformance does not establish correct authorisation, duplicate-connection handling, transaction state, or resistance to the attacks in the concept page. No support for OCPP 2.1 is established by this README. Handle authorised capture data and any disclosed TLS secrets as sensitive test material.

## Status and sources

Checked 2026-11-01. **Active** at this check: the repository is not archived and its latest default-branch commit is dated 2026-03-22. This records observed project activity, not a promise of support or protocol completeness. See the [checked commit](https://github.com/vfg27/CheckOCPP/commit/19f5040fd8769d9a62f1af7d5b63074b36fbcf52). Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream README](https://github.com/vfg27/CheckOCPP/blob/19f5040fd8769d9a62f1af7d5b63074b36fbcf52/README.md)

## Related

- [EmuOCPP](emuocpp.md)
- [EVerest](everest.md)
- [OCPP and charging attacks](concepts/ocpp-charging-attacks.md)
- [OCPPStorm paper](ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations.md)
- [dsV2Gshark](dsv2gshark.md)
