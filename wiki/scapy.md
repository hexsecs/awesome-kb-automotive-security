---
title: "Scapy"
summary: "Python packet manipulation library with support for DoIP, SOME/IP, AUTOSAR PDUs, SecOC, CAN-FD, and FlexRay protocols."
type: entity
category: "Automotive Ethernet"
url: "https://scapy.net/"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python packet manipulation library with support for DoIP, SOME/IP, AUTOSAR PDUs, SecOC, CAN-FD, and FlexRay protocols."
related: [vsomeip, someip-protocol-fuzzer, eth-ws-someip, autofuze, python-doipclient]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/secdev/scapy"
    retrieved: 2026-11-01
  - url: "https://github.com/secdev/scapy/releases/tag/v2.8.0"
    retrieved: 2026-11-01
  - url: "https://scapy.readthedocs.io/en/latest/layers/automotive.html"
    retrieved: 2026-11-01
---

Python packet manipulation library with support for DoIP, SOME/IP, AUTOSAR PDUs, SecOC, CAN-FD, and FlexRay protocols.

## What it is

Scapy is a general-purpose Python packet-manipulation program and library: it forges and decodes packets for a wide range of protocols, sends and captures them on the wire, reads and writes pcap files, and matches requests against replies — usable as an interactive shell or imported as a library. It is not an automotive tool. Its place in this section is the automotive contrib area (`scapy/contrib/automotive/`, plus the CAN layer), which implements the Ethernet-era automotive stack — DoIP, SOME/IP and SOME/IP-SD, AUTOSAR PDUs, SecOC — alongside the CAN-side stack (CAN/CAN-FD, ISO-TP, UDS, GMLAN, OBD, CCP/XCP) in a single scriptable toolkit. That breadth in one Python API is why other entries in this KB are built on it. Licence: GPL-2.0.

## How it works

Everything is a composable `Packet` layer: layers stack with `/` (e.g. `IP()/UDP()/SOMEIP()`), build to bytes or dissect from bytes, and move through Scapy sockets. Contrib layers load explicitly (`load_contrib('automotive.someip')`, etc.). The automotive pieces:

- **SOME/IP + SOME/IP-SD** — a `SOMEIP` class (service ID, method/event sub-ID distinguished at 0x8000, length, client/session IDs, versions, the full message-type set including SOME/IP-TP segment types, and the AUTOSAR return-code enum) binding over UDP and TCP on ports 30490–30504; Service Discovery is a separate `SD` packet (service 0xFFFF, method 0x8100) with service and eventgroup entries and IPv4/IPv6 endpoint, multicast, configuration and load-balance options.
- **DoIP** (ISO 13400) — a `DoIP` packet class covering the payload-type table (vehicle identification over UDP, routing activation, alive check, diagnostic messages 0x8001 over TCP with UDS bound as payload), plus a working client: `DoIPSocket` opens TCP (port 13400; TLS port 3496), sends a routing-activation request on connect, and upgrades to TLS when the entity's response requires a secure socket; `UDS_DoIPSocket` wraps it so UDS packets are encapsulated transparently.
- **AUTOSAR PDU** — `PDU` (32-bit PDU ID + length + payload) and `PDUTransport` bound under UDP port 60000, citing the AUTOSAR Classic 22-11 IPDU Multiplexer specification; the payload is deliberately left free to interpret — Scapy provides the multiplexing envelope, the user supplies the semantics.
- **SecOC** — dissect, build, verify and authenticate SecOC messages as AUTOSAR PDUs or CAN-FD frames: AES-128 CMAC over payload + freshness value, with a 1-byte truncated freshness value and 3-byte truncated MAC in the implementation classes. Protected PDU IDs must be registered so the dissector can tell SecOC and non-SecOC PDUs apart.
- **CAN-FD** — a first-class `CANFD` layer (64-byte maximum data) usable through SocketCAN/python-can sockets, and the carrier for the SecOC CAN-FD form.

## Where it fits

The general-purpose packet forge underneath much of this section: where [vsomeip](vsomeip.md) is a stack you run, Scapy is the crafting/dissecting toolkit you script — hand-building one SOME/IP request or SD Offer, replaying or mutating captured traffic, prototyping a DoIP/UDS exchange. Scapy's own automotive docs make the pairing explicit: their Raspberry Pi SOME/IP test setup uses a vsomeip service/client as the peer. Directly downstream, [someip-protocol-fuzzer](someip-protocol-fuzzer.md) is built on Scapy's SOME/IP layer. It complements [eth-ws-someip](eth-ws-someip.md) (passive dissection in a capture tool vs active craft/send/receive — the two overlap on SOME/IP/SD decoding), overlaps [AutoFuze](autofuze.md) on Python SOME/IP/UDS coverage (AutoFuze is the purpose-built ECU-testing toolkit, Scapy the broader substrate), and for DoIP is the broad alternative to the focused [python-doipclient](python-doipclient.md).

## Limits and safety notes

One list claim needs qualifying in the body: the list description's **FlexRay** support is **not corroborated as a dedicated automotive layer** by the primary sources — the `scapy/contrib/automotive/` tree has no FlexRay module; FlexRay appears only as an AVTP encapsulation header in `scapy/contrib/ieee1722.py` (FlexRay frames carried over Ethernet AVB) and as transport context in the docs. Native FlexRay bus support is therefore not claimed here. SecOC is a framework, not a turnkey implementation: three functions (payload, key, freshness value) must be customised per target — OEM SecOC data IDs and freshness values must be known and tracked by the user — and if the `cryptography` package is absent, the module loads with CMAC calculation disabled. The automotive docs state their own protocol caveat: DoIP, like ISO-TP, "does not specify special security measures" — secured communication is the application layer's problem, and Scapy will happily build the unprotected form. Automotive features work best on Linux (SocketCAN and the can-isotp kernel module), and contrib APIs change between releases — downstream tools pin versions for a reason. By design this is an active tool: the README advertises sending invalid frames and combining injection techniques, which against a live vehicle network is probing, not passive analysis.

## Status and sources

Checked 2026-11-01. **Active**: the repository is not archived; the latest release, v2.8.0 (2026-10-02), carries automotive changes (SAE J1939 added, standalone UDS/KWP/OBD/GMLAN packets, CAN/ISO-TP socket robustness), and the head commit is dated the day of checking. A continuously developed project whose automotive area gained features in the current release. Documentation claims above come from the following primary sources; no packets were sent for this page.

- [Upstream repository](https://github.com/secdev/scapy)
- [v2.8.0 release notes](https://github.com/secdev/scapy/releases/tag/v2.8.0)
- [Scapy automotive documentation](https://scapy.readthedocs.io/en/latest/layers/automotive.html)

## Related

- [vsomeip](vsomeip.md)
- [someip-protocol-fuzzer](someip-protocol-fuzzer.md)
- [eth-ws-someip](eth-ws-someip.md)
- [AutoFuze](autofuze.md)
- [python-doipclient](python-doipclient.md)
