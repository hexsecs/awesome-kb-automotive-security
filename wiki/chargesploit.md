---
title: "ChargeSploit"
summary: "Security testing framework for ISO 15118-2 and DIN SPEC 70121 that emulates either the charger or the vehicle, with TLS support and extensible handlers for…"
type: entity
category: "EV Charging Security"
url: "https://github.com/konicst1/ChargeSploit"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Security testing framework for ISO 15118-2 and DIN SPEC 70121 that emulates either the charger or the vehicle, with TLS support and extensible handlers for injecting non-compliant behaviour at any step of a session."
related: [acccs, pyplc, dsv2gshark, wwcp-iso15118]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/konicst1/ChargeSploit"
    retrieved: 2026-11-01
  - url: "https://github.com/konicst1/ChargeSploit/commit/9d80027a4b05a94ad6b97fa7c95c1653bbe0c176"
    retrieved: 2026-11-01
  - url: "https://github.com/konicst1/ChargeSploit/blob/9d80027a4b05a94ad6b97fa7c95c1653bbe0c176/README.md"
    retrieved: 2026-11-01
---

Security testing framework for ISO 15118-2 and DIN SPEC 70121 that emulates either the charger or the vehicle, with TLS support and extensible handlers for injecting non-compliant behaviour at any step of a session.

## What it is

A security-testing framework for the vehicle-to-charger V2G communication stack. The upstream README documents ISO 15118-2 and DIN SPEC 70121, EVSE and EVCC roles, and TLS using a supplied certificate set. It is a programmable session peer rather than a packet-only decoder.

## How it works

A controller owns discovery, transport sockets, and the session loop. UDP carries SECC Discovery Protocol (SDP), TCP or TLS carries the V2G conversation, V2GTP supplies framing, and a Java EXI codec is called from Python through py4j. Message handlers decode, dispatch, and encode responses built from JSON templates. Subclassing a handler and registering it lets a test change one response while reusing the rest of the session. Discovery behaviour is separately extensible through SDP modes.

## Where it fits

Choose it for controlled negative tests or state-machine experiments against an authorised peer when the transport and discovery path are already available. It requires Python 3.9+, Java 11+, and an interface with IPv6 link-local addressing; the README notes that elevated privileges are normally needed. [AcCCS](acccs.md) and [pyPLC](pyplc.md) also address hardware/PLC integration; [dsV2Gshark](dsv2gshark.md) helps inspect the resulting exchanges. [WWCP_ISO15118](wwcp-iso15118.md) offers a separate codec and session implementation for comparison.

## Limits and safety notes

The checked README does not establish ISO 15118-20 support or complete Plug & Charge certificate-chain, authorisation, and revocation behaviour. A TLS option is not evidence of that entire workflow, nor is a handler named normal proof of certification. Upstream explicitly warns that abnormal voltage/current fields or illegal state transitions belong on a low-voltage bench against authorised hardware, with the DC source confirmed low-voltage first. This page does not verify operation against physical equipment.

## Status and sources

Checked 2026-11-01. **Active** at this check: the repository is not archived and its latest default-branch commit is dated 2026-08-08. This records observed project activity, not a promise of support or protocol completeness. See the [checked commit](https://github.com/konicst1/ChargeSploit/commit/9d80027a4b05a94ad6b97fa7c95c1653bbe0c176). Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream README](https://github.com/konicst1/ChargeSploit/blob/9d80027a4b05a94ad6b97fa7c95c1653bbe0c176/README.md)

## Related

- [AcCCS](acccs.md)
- [pyPLC](pyplc.md)
- [dsV2Gshark](dsv2gshark.md)
- [WWCP_ISO15118](wwcp-iso15118.md)
