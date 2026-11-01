---
title: "vsomeip"
summary: "COVESA reference implementation of SOME/IP and SOME/IP-SD, used both as the target in automotive Ethernet fuzzing research and as a client for crafting…"
type: entity
category: "Automotive Ethernet"
url: "https://github.com/COVESA/vsomeip"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "COVESA reference implementation of SOME/IP and SOME/IP-SD, used both as the target in automotive Ethernet fuzzing research and as a client for crafting service calls against production ECUs."
related: [someip-protocol-fuzzer, scapy, eth-ws-someip, autofuze]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/COVESA/vsomeip"
    retrieved: 2026-11-01
  - url: "https://github.com/COVESA/vsomeip/releases/tag/3.7.6"
    retrieved: 2026-11-01
---

COVESA reference implementation of SOME/IP and SOME/IP-SD, used both as the target in automotive Ethernet fuzzing research and as a client for crafting service calls against production ECUs.

## What it is

vSomeIP is a C++ implementation of SOME/IP (Scalable service-Oriented MiddlewarE over IP) and its Service Discovery protocol, SOME/IP-SD, maintained under COVESA on GitHub (copyright BMW AG; licence MPL-2.0). It is middleware, not a security tool: applications link it to offer and consume services on an automotive Ethernet network, with a per-node routing manager arbitrating local and remote communication. Its security relevance — and its list framing — is dual: it is the SOME/IP stack fuzzing research most readily targets (this KB's [someip-protocol-fuzzer](someip-protocol-fuzzer.md) documents exactly that setup), and the same library serves as a ready-made standards-speaking client/service peer for probing other SOME/IP implementations. Two list framings are the list's own wording, not upstream's: upstream sources do not call it a "reference implementation", and no primary source checked names a production-ECU deployment.

## How it works

Four shared libraries compose the stack: `libvsomeip3` (SOME/IP core), `libvsomeip3-cfg` (configuration), `libvsomeip3-sd` (service discovery) and `libvsomeip3-e2e` (E2E protection). One application per node acts as routing manager — either the first vsomeip application started (autoconfiguration) or the dedicated minimal daemon `routingmanagerd`; local applications register with it over local sockets (default base path /tmp), and the routing manager owns external endpoints and forwards between local clients and remote services. Applications interact through callbacks — state, availability, message and event handlers — as the user guide's hello-world client/service example walks through. Configuration is JSON (default `/etc/vsomeip.json` or the `VSOMEIP_CONFIGURATION` variable) declaring the unicast address, applications and client IDs, services/instances and endpoint ports, and service-discovery settings. The protocol surface is SOME/IP request/response and subscribe/notify over UDP and TCP, SOME/IP-SD offer/find/subscribe over multicast, SOME/IP-TP segmentation for oversized payloads, plus nPDU timing/debouncing and selective broadcast in the configuration docs. Ships with examples, a command-line sender (`vsomeip_ctrl` sends a hex SOME/IP message to a service/instance and prints a response arriving within 5 s), and a Wireshark Lua dissector for vsomeip's *internal* routing communication — not for SOME/IP on the wire. Build: C++20, CMake, Boost ≥ 1.75, with instructions for Linux, Android and Windows.

## Where it fits

The section's infrastructure entry: the thing other tools talk *to* or *through*. The documented pairings inside this KB are concrete — someip-protocol-fuzzer's README builds its target service with vsomeip 3.1.20 (plus the author's companion target repo), and [Scapy](scapy.md)'s automotive docs use vsomeip services/clients as the peer in their Raspberry Pi SOME/IP test setup. It complements [eth-ws-someip](eth-ws-someip.md) (dissection of the traffic vsomeip generates — vsomeip's own shipped dissector covers only its internal routing protocol). It overlaps [AutoFuze](autofuze.md), which carries its own Python SOME/IP + SD implementation — a scripting-level alternative when a C++ stack is unnecessary. As a client it is the heavyweight counterpart to Scapy's crafted-packet approach: a real stack with real SD and routing behaviour, versus single hand-built messages.

## Limits and safety notes

Security is opt-in and off by default — the configuration documentation states it plainly: "As long as no `security` node exists, the security implementation is switched off." When enabled, the built-in mechanism is UNIX-credentials based: a local client presents UID/GID with its client ID, the routing manager matches them against configured allow/deny policies, and a mismatch closes the socket; remote clients must be explicitly allowed. That is access control for local IPC and service use — the configuration docs describe no SOME/IP wire encryption. The user guide warns that client-ID autoconfiguration "isn't meant to be used together with vsomeip Security": a dynamically assigned ID cannot have matching credentials configured in advance. E2E protection is configurable CRC, not authentication — profiles 01 (CRC8), 04, 07 and a custom CRC32, applied per event; it detects corruption and is not a MAC (contrast Scapy's SecOC, the AUTOSAR mechanism that does provide message authentication). Documentation lags the code: the in-repo user guide states it was generated for vSomeIP 3.5 while the code is at 3.7.6. And it is a production-shaped stack with a production-shaped CVE surface — the 3.7.6 changelog is dominated by robustness and security fixes (an integer overflow in a payload deserializer, a TP reassembly over-read, a routing SIGSEGV, an Android logging vulnerability) — which is precisely why it serves as a fuzzing target, and why version currency matters when it is one.

## Status and sources

Checked 2026-11-01. **Active**: the repository is not archived, with five releases in the six months before checking (3.7.2 in April through 3.7.6 on 2026-09-17) — a maintained stack on a roughly monthly release rhythm. (Head commits arrive as batched release imports, so the activity claim rests on the release cadence, not commit dates.) Documentation claims above come from the following primary sources; no ECU was probed for this page.

- [Upstream repository](https://github.com/COVESA/vsomeip)
- [3.7.6 release notes](https://github.com/COVESA/vsomeip/releases/tag/3.7.6)

## Related

- [someip-protocol-fuzzer](someip-protocol-fuzzer.md)
- [Scapy](scapy.md)
- [eth-ws-someip](eth-ws-someip.md)
- [AutoFuze](autofuze.md)
