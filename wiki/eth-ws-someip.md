---
title: "eth-ws-someip"
summary: "Wireshark LUA dissectors for Automotive Ethernet SOME/IP and SOME/IP-SD protocols (Autosar 4.2)."
type: entity
category: "Automotive Ethernet"
url: "https://github.com/jamores/eth-ws-someip"
status: maintenance
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Wireshark LUA dissectors for Automotive Ethernet SOME/IP and SOME/IP-SD protocols (Autosar 4.2)."
related: [vsomeip, scapy, ics-cap, someip-protocol-fuzzer]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/jamores/eth-ws-someip"
    retrieved: 2026-11-01
  - url: "https://github.com/jamores/eth-ws-someip/blob/master/README.md"
    retrieved: 2026-11-01
---

Wireshark LUA dissectors for Automotive Ethernet SOME/IP and SOME/IP-SD protocols (Autosar 4.2).

## What it is

A set of four Wireshark dissectors written in Lua that decode SOME/IP and SOME/IP Service Discovery (SOME/IP-SD) traffic inside Wireshark. It is a passive analysis aid only: it parses and labels traffic someone else captured — it does not implement SOME/IP, generate traffic, or talk to an ECU. The repository is small and MIT-licensed: four `.lua` files plus the bundled AUTOSAR specification PDFs and a packet-format cheat sheet.

## How it works

The four files split the work: `someip.lua` dissects the SOME/IP header; `sd.lua` the SD header; `sd_entries.lua` and `sd_options.lua` the two SD arrays. The SOME/IP dissector decodes the fixed 16-byte header — Message ID (split into Service ID and Method/Event ID, the high bit distinguishing method from event), Length, Request ID (Client + Session), Protocol and Interface Versions, Message Type, Return Code — with a message-type table covering the base types (request, notification, response, error and their ACK variants) **and** the SOME/IP-TP segment types, dissecting the TP header (offset, more-segments flag) when the TP bit is set. It registers on UDP and TCP ports 30490, 30491 and 30501–30504, uses Wireshark's TCP reassembly so PDUs split across segments are handled, and loops to dissect multiple SOME/IP PDUs packed in one packet. When the Message ID is the SD identifier (`0xFFFF8100`), the payload passes to the SD chain: flags, entries (Find Service, Offer Service, Subscribe, Subscribe Ack — with TTL = 0 reinterpreted as the stop/nack forms, and the entry type written into Wireshark's Info column) and options (configuration, load balancing, IPv4/IPv6 endpoint, multicast and SD-endpoint, with L4 protocol and port). Installation is manual — copy or symlink the four files into Wireshark's personal plugins folder. Anything past the SOME/IP header that is not SD falls through to Wireshark's generic `data` dissector: there is no payload/serialisation decoding. The README's "Extras" section points traffic-generation readers to the author's separate Scapy-based `eth-scapy-someip` project (not a KB entry).

## Where it fits

The passive-observation end of this section: what you load when you already have a capture — from [ICS CAP](ics-cap.md), a mirror/TAP, or [vsomeip](vsomeip.md) test traffic — and need SOME/IP and SD exchanges readable in Wireshark. The pairings are complementary, not competing: vsomeip creates and endpoints the traffic, these dissectors only decode it; [Scapy](scapy.md) crafts and sends packets (its contrib layer covers SOME/IP) where this is the read-side counterpart; and on the icscap capture path, a Lua dissector like this one is exactly the gap-filler for SOME/IP header/SD visibility. It is also the tool you would watch active testing with — [someip-protocol-fuzzer](someip-protocol-fuzzer.md) or [AutoFuze](autofuze.md) traffic — rather than a testing tool itself.

## Limits and safety notes

The AUTOSAR generation wording differs across the primary sources, and this page preserves that rather than resolving it: the repository description (and the list) say "Autosar 4.2", while the current README frames the dissectors as "AUTOSAR CP & AP, Foundation 1.5.0"; the bundled specs are the AUTOSAR PRS documents. Which exact AUTOSAR release the code was validated against is **not stated** anywhere in the repository — there are no test captures, CI, or conformance claims. Header + SD only: service payloads are opaque bytes, so field-level meaning of a method's arguments needs service definitions and a different toolchain. The README's worked install example is Wireshark 2.4.4-era; behaviour on current Wireshark versions is not documented in the repo. And because there has been no release since 2019 (see Status), installing today means installing `master` — the 2025 fix is in no release. The tool itself has no safety surface: passive dissectors, no transmission.

## Status and sources

Checked 2026-11-01. **Maintenance**: the repository is not archived; development and releases ended in October 2019 (latest release v1.5.1, 2019-10-22), but a substantive dissector bug fix landed on master on 2025-06-22 after a ~5½-year gap — sporadic life rather than abandonment, with no release carrying that fix. Documentation claims above come from the following primary sources; no traffic was captured for this page.

- [Upstream repository](https://github.com/jamores/eth-ws-someip)
- [Upstream README](https://github.com/jamores/eth-ws-someip/blob/master/README.md)

## Related

- [vsomeip](vsomeip.md)
- [Scapy](scapy.md)
- [ICS CAP](ics-cap.md)
- [someip-protocol-fuzzer](someip-protocol-fuzzer.md)
