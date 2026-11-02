---
title: "SOME/IP and SOME/IP-SD"
summary: "AUTOSAR's service-oriented middleware over IP: how services are offered, found and invoked — and why discovery is the trust root of every SOME/IP conversation."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [vsomeip, eth-ws-someip, scapy, someip-protocol-fuzzer, protocrawler, ics-cap, autofuze]
sources:
  - url: "https://github.com/jamores/eth-ws-someip/tree/master/specs"
    retrieved: 2026-11-01
  - url: "https://www.autosar.org/fileadmin/standards/R20-11/FO/AUTOSAR_PRS_SOMEIPProtocol.pdf"
    retrieved: 2026-11-01
  - url: "https://www.autosar.org/fileadmin/standards/R23-11/FO/AUTOSAR_FO_PRS_SOMEIPProtocol.pdf"
    retrieved: 2026-11-01
  - url: "https://www.autosar.org/fileadmin/standards/R20-11/FO/AUTOSAR_PRS_E2EProtocol.pdf"
    retrieved: 2026-11-01
  - url: "https://github.com/COVESA/vsomeip/blob/master/documentation/vsomeipConfiguration.md"
    retrieved: 2026-11-01
---

Modern vehicle Ethernet backbones do not exchange fixed CAN-style frames; they offer **services**. SOME/IP — AUTOSAR's "Scalable service-Oriented MiddlewarE over IP" — is the middleware protocol those services run on, specified once in the AUTOSAR Foundation for Classic and Adaptive platforms alike. Its companion, SOME/IP-SD, is how providers announce services and consumers find and subscribe to them. That split is the security centre of gravity: **SD is the trust root of every SOME/IP conversation** — a client learns where a service lives from discovery messages — and neither specification defines authentication, encryption or access control.

## How SOME/IP works

A **service** combines **methods** (RPCs on the provider), **events** (data sent cyclically or on change) and **fields** (status values with a getter, setter and/or notifier — a notifier also sends the current value on subscription, where a bare event does not). Subscription granularity is the **eventgroup**: per eventgroup, never per event.

Every message carries a fixed 16-byte header (network byte order): **Message ID** (Service ID 16 bit + a method/event bit + Method/Event ID 15 bit); **Length** (counted *from the Request ID*); **Request ID** (Client ID + Session ID); **Protocol/Interface Version**; **Message Type** — REQUEST 0x00, REQUEST_NO_RETURN 0x01 (fire-and-forget, which by specification never returns an error), NOTIFICATION 0x02, RESPONSE 0x80, ERROR 0x81, plus SOME/IP-TP segment types (TP flag set); and a **Return Code**.

The **payload is not self-describing**: serialisation is fixed by the interface specification and configuration — byte order is configured per interface, dynamic length fields count **bytes, not elements**, optional members exist only in the tagged (TLV) form. Without the interface definition *and* its configuration, payload bytes cannot be decoded unambiguously. Transports are UDP or TCP; UDP payloads cap at **1400 bytes** — the stated reason is headroom "to allow for future changes to protocol stack (e.g. changing to IPv6 or adding security means)" — and larger messages use **SOME/IP-TP** segmentation. **No port numbers are assigned by the specification** — endpoints are configuration; the family's only well-known port belongs to SD.

## How discovery works (SOME/IP-SD)

SD is itself a SOME/IP message (Service 0xFFFF, Method 0x8100) over UDP to **port 30490** by default. Its multicast address is a configuration parameter; the specification fixes no numeric value. Messages pack **entries** referencing **options** by index:

- **Find Service** (0x00): sent only while a service's state is unknown; wildcards (Instance 0xFFFF, Major 0xFF) do the searching; a Find references *no* endpoint options.
- **Offer Service** (0x01): announces one instance and **must reference at least one IPv4/IPv6 Endpoint Option**. **Stop Offer** is the same entry with TTL 0 — there is no stop message type.
- **Subscribe Eventgroup** (0x06): carries the *client's* endpoint options. **Stop Subscribe** is TTL 0. **Ack/Nack** share type 0x07 — Ack echoes the TTL; Nack is TTL 0.

**TTL** is a 24-bit lifetime in seconds (0xFFFFFF = "until next reboot"), so offers and subscriptions are **soft state**, refreshed or silently gone. Options include **Load Balancing** (Priority/Weight "like the DNS-SRV records": highest priority wins). Startup runs three phases: **Initial Wait** → **Repetition** (delay *doubling* each round; a client that gets its Offer stops finding) → **Main** (servers Offer cyclically; **no cyclic Finds are allowed**). **Reboot detection** is mandatory; receivers discard state built on a rebooted peer's old incarnation.

## The security surface

The absence claim: a full-text read of the FO 1.5.0 SOME/IP Protocol Specification finds **no security mechanism and no occurrence of authentication, encryption or access control as protocol features**. The SD specification contains exactly one security requirement, §6.1 [PRS_SOMEIPSD_00656] — the protocol's entire specified defence:

> "Received SOME/IP-SD messages shall be checked that the IP Addresses received in Endpoint options and SD Endpoint options are topological correct (reference IP Addresses in the IP subnet for which SOME/IP-SD is used) and shall ignore IP Addresses that are not topological correct as well as the entries referencing those options."

It validates that an advertised address belongs to the local subnet — not that the sender is entitled to advertise it. The consequences follow from the specified mechanics:

- **Rogue Offer / discovery spoofing.** Any host reaching the SD multicast group can Offer any Service/Instance ID. Clients are specified to act on Offers — adopting the advertised endpoint values (*overwriting preconfigured addresses and ports* is a mandatory behaviour) and the advertiser-controlled Load Balancing priority.
- **Forged Stop Offer as a one-packet kill.** Withdrawal is an Offer with TTL 0 and no proof of ownership; a forged one is indistinguishable on the wire, and processing one deletes **all subscriptions for that instance on both sides**.
- **Unauthorised subscription.** The specified Nack reasons are existence, transport and resource problems — **none is an authorisation decision**. Any reachable host may subscribe to any offered eventgroup and name its own delivery endpoint.
- **Method invocation by any reachable host.** Requests are answered on addressing alone (Message ID + the endpoint learned via SD); the protocol defines no client identity to check.

Scope: the claim is made about the FO 1.5.0 texts read firsthand (cross-checked against R20-11/R23-11). Whether any later AUTOSAR release adds SOME/IP-native authentication is **not established**. DoIP (ISO 13400) is a separate diagnostics protocol, deliberately out of scope.

## What exists around it

**E2E protection** is the mechanism most often mistaken for SOME/IP security. E2E profiles can protect SOME/IP payloads with an unkeyed CRC, a sequence/alive counter and a configured Data ID. It is a *functional-safety* mechanism (ISO 26262 fault model): its "masquerading" detection means a frame from the *wrong configured source* fails expectations — protection against misdelivery, not against a deliberate injector, since both the published CRC polynomial and the configured Data ID are reproducible by anyone on the bus. **E2E provides no authentication, authorisation or confidentiality.**

**SecOC**'s boundary is worth stating exactly, because "SecOC is not for SOME/IP" is too absolute. Per AUTOSAR's Secure Onboard Communication specification (CP SWS, R24-11), SecOC provides MAC authentication and freshness at the **PDU level** through the COM/PduR stack; its §4.2 states SecOC "can only be used to secure **the whole SomeIpTp message**" — but SecOC has no SOME/IP-native mechanism and does not authenticate SD at all.

**Implementation-level access control** exists in exactly one place in this KB's evidence: [vsomeip](../vsomeip.md)'s opt-in `security` configuration — off unless a `security` node exists, inert until `check_credentials: true` (otherwise "Audit Mode": violations "logged but allowed"). It is UNIX-credential allow/deny over **local** Unix-domain sockets, local only by design; `allow_remote_clients` defaults to allowing **all** remote requests/subscriptions, and no wire encryption is described.

Version traps: TP_RESPONSE/TP_ERROR are **0xA0/0xA1** (the FO 1.5.0 table's 0x23/0x24 contradict its own flag rule); **ACK types** (0x40…) appear in no PRS message-type table checked — implementation extensions.

## Related

- [vsomeip](../vsomeip.md)
- [eth-ws-someip](../eth-ws-someip.md)
- [Scapy](../scapy.md)
- [someip-protocol-fuzzer](../someip-protocol-fuzzer.md)
- [ProtoCrawler](../protocrawler.md)
- [ics-cap](../ics-cap.md)
- [AutoFuze](../autofuze.md)

Checked 2026-11-01 against the AUTOSAR PRS texts in the frontmatter (FO 1.5.0, with R20-11/R23-11 cross-checks).
