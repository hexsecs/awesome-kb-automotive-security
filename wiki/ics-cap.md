---
uid: 01a19d3c-af9f-7cee-bda4-5fce542a9fc5
title: "ICS CAP"
summary: "Free Wireshark plugin for monitoring Automotive Ethernet, CAN, CAN FD, LIN, and FlexRay networks."
type: entity
category: "Automotive Ethernet"
url: "https://intrepidcs.com/products/software/ics-cap/"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Free Wireshark plugin for monitoring Automotive Ethernet, CAN, CAN FD, LIN, and FlexRay networks."
related: [eth-ws-someip, scapy, vsomeip, someip]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://intrepidcs.com/products/software/ics-cap/"
    retrieved: 2026-11-01
  - url: "https://guide.intrepidcs.com/brochures/icsusa/icscap.pdf"
    retrieved: 2026-11-01
  - url: "https://cdn.intrepidcs.net/icscap/"
    retrieved: 2026-11-01
---

Free Wireshark plugin for monitoring Automotive Ethernet, CAN, CAN FD, LIN, and FlexRay networks.

## What it is

icscap (the vendor's styling; part number ICSCAP) is a free, closed-source Wireshark plugin from Intrepid Control Systems that turns Intrepid vehicle-network interface hardware into Wireshark capture interfaces, so Automotive Ethernet, CAN, CAN FD, LIN and FlexRay traffic can be captured live and inspected at packet level in Wireshark's ordinary UI. On its own it is a capture bridge, not an analysis suite: signal decoding, stateful protocol tracking and transmission live in Intrepid's paid companion, Vehicle Spy — the vendor's own page draws that line explicitly.

## How it works

The chain is Intrepid hardware → Intrepid drivers → icscap plugin → Wireshark. The vendor's install flow starts with updating drivers and configuring the hardware (baud rates, Ethernet PHY settings) before Wireshark ever sees an interface; the plugin is not a software-only capture source and cannot reach a vehicle bus without the hardware. What standalone icscap does, per the product page and brochure: capture Automotive Ethernet, CAN, CAN FD, LIN and FlexRay traffic with real-time packet-level visibility for debugging, validation and compliance testing; inspect raw packets in Wireshark; extend Wireshark with **Lua scripts** to interpret proprietary messages or complex traffic — the page's own examples are Protobuf and SOME/IP — and capture for offline analysis, regression testing, replay, or teaching. Builds ship for Windows (zip + installer) and Linux (x86_64 and aarch64); no macOS build is listed. The vendor points to its open-source device library `libicsneo` for the supported-hardware list (neoVI, RAD and ValueCAN families).

What requires **icscap + Vehicle Spy** — a separate feature list on the same product page, credited to the pair, never to icscap alone: tracking SOME/IP, DoIP, UDS and other multi-frame/stateful protocols with sequence and system-level context; injecting messages and replaying traffic; CCP, XCP and UDS operations; latency/jitter/throughput measurement; test sequences and stress-testing ECUs with malformed or randomised messages; and native interpretation of DBC, ARXML and FIBEX files.

## Where it fits

The capture front-end of this section — and, unusually, of the CAN/LIN/FlexRay world too, since one plugin fronts all five network types through one hardware vendor. Stock Wireshark cannot see CAN, FlexRay or Automotive Ethernet PHYs at all without an interface like this, which is the plugin's entire reason to exist. It complements [eth-ws-someip](eth-ws-someip.md): icscap delivers Automotive Ethernet frames into Wireshark, and Lua dissectors like eth-ws-someip make SOME/IP and SD readable once there — the icscap page itself advertises exactly that Lua hook. It complements [Scapy](scapy.md) at the opposite workflow end (Scapy crafts and sends from a normal NIC; icscap is receive-side capture from specialised interfaces, with transmit gated behind Vehicle Spy), and pairs with [vsomeip](vsomeip.md) traffic the same way any capture path does. In the vendor's framing it is a development/validation tool; its place in this KB is as the observation point during assessments.

## Limits and safety notes

Hardware-gated: no Intrepid interface, no capture — the plugin alone, Wireshark alone, and a standard Ethernet NIC do not reproduce it, so the hardware is a budget and workflow prerequisite. The standalone scope limit is vendor-drawn: packet level only, with signal decoding, stateful SOME/IP/DoIP tracking, transmission, diagnostics and any fuzzing belonging to the Vehicle Spy pairing. The plugin is closed source with no public repository or changelog; its licence terms, Wireshark version compatibility range, and the exact per-device support subset are not stated in the vendor sources (the vendor's hardware pointer is libicsneo's broader list). The vendor sources state no safety warnings; in standalone form the tool is passive, and the active capabilities belong to the pairing.

## Status and sources

Checked 2026-11-01. **Active**: the vendor's own download index shows eight versioned releases in eleven months, the latest 26.2.1 dated 2026-05-08 (Windows and Linux x86_64/aarch64 builds), with the product page live and a brochure revision dated November 2025. A currently shipped and maintained product. Documentation claims above come from the following vendor sources; no hardware was connected for this page.

- [Product page](https://intrepidcs.com/products/software/ics-cap/)
- [Vendor brochure (Rev. 20251113)](https://guide.intrepidcs.com/brochures/icsusa/icscap.pdf)
- [Download index](https://cdn.intrepidcs.net/icscap/)

## Related

- [eth-ws-someip](eth-ws-someip.md)
- [Scapy](scapy.md)
- [vsomeip](vsomeip.md)
- [SOME/IP and SOME/IP-SD](concepts/someip.md)
