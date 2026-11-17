---
uid: 01a1aba1-8842-7176-bc66-9e2e7bf83d37
title: "Automotive Ethernet"
summary: "Matheus and Königseder, Cambridge University Press 2021. The standard reference on automotive Ethernet, covering PHYs, TSN, and security concepts for…"
type: entity
category: "Books"
url: "https://books.google.com/books?vid=ISBN9781108841955"
status: published
last_checked: 2026-11-17
created: 2026-11-05
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 082afab
list_summary: "Matheus and Königseder, Cambridge University Press 2021. The standard reference on automotive Ethernet, covering PHYs, TSN, and security concepts for in-vehicle networks."
related:
  - a-comprehensible-guide-to-controller-area-network
  - eth-ws-someip
  - tow-ids-automotive-ethernet-intrusion-dataset
  - vsomeip
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-05
  - url: "https://books.google.com/books?vid=ISBN9781108841955"
    retrieved: 2026-11-17
facets: [ethernet, learning]
---

Matheus and Königseder, Cambridge University Press 2021. The standard reference on automotive Ethernet, covering PHYs, TSN, and security concepts for in-vehicle networks.

## What it is

*Automotive Ethernet*, third edition, by Kirsten Matheus and Thomas Königseder, published by Cambridge University Press on 22 April 2021, 414 pages, ISBN 9781108841955. It is the fully revised reference on the technology, with about 20% new material and greater technical depth than the earlier editions. The authors write from the industry side: Matheus is a communications engineer responsible for establishing Ethernet-based communication at BMW (previously Volkswagen, NXP and Ericsson) and received the IEEE-SA Standards Medallion in 2019; Königseder is CTO of Technica Engineering and was responsible at BMW for launching the first car with an Ethernet connection in 2008.

## How it works

The expanded coverage in this edition includes detailed explanations of the new PHY technologies — 10BASE-T1S including multidrop, and 2.5, 5 and 10GBASE-T1 — alongside EMC interference models and the new TSN standards for automotive use. It also covers security concepts, power-saving possibilities, functional safety in the Automotive Ethernet context, test strategies and lessons learned. The stated audience is engineers, technical managers and researchers designing in-car electronics, and those interested in the strategy of introducing a new technology.

The table of contents shows the book's arc: a history of Ethernet from a car manufacturer's perspective, Automotive Ethernet and power supply, a history of in-vehicle networking and of Automotive Ethernet, the automotive environment, automotive physical-layer technologies, references, and Ethernet in automotive system development. Recurring topics in the index include BroadR-Reach, 100/1000 Mbps operation, unshielded twisted-pair cabling, PLCA, SOME/IP, VLANs, IP, service discovery, network architecture, switching, QoS, wake-up, EMC and OPEN Alliance. Industry pioneers contribute the technical and non-technical decisions behind Automotive Ethernet's adoption.

## Where it fits

This is the physical-layer and network-architecture reference that complements the CAN-focused material in the KB. [A comprehensible guide to controller area network](a-comprehensible-guide-to-controller-area-network.md) is the equivalent plain-language CAN text. On the protocol side, [eth-ws-someip](eth-ws-someip.md) and [vsomeip](vsomeip.md) cover the SOME/IP stack that runs over these networks, and [TOW-IDS](tow-ids-automotive-ethernet-intrusion-dataset.md) is the intrusion dataset for Automotive Ethernet. Readers coming from CAN bus security should note that the attack surface changes substantially once switched Ethernet, IP and service discovery enter the car.

## Limits and safety notes

This is a book, not a tool or a freely available paper. The description here is drawn from the publisher's Google Books listing, which offers a limited preview and a visible table of contents rather than full text; specific claims about individual chapters therefore reflect the publisher's summary. Nothing here was independently verified against the book's technical content, and no security testing was performed. The book is a 2021 third edition, so standards that have evolved since then need current specifications.

## Status and sources

Checked 2026-11-17. **Published** — Cambridge University Press, third edition, 2021.

- [Publisher listing via Google Books](https://books.google.com/books?vid=ISBN9781108841955)

## Related

- [A comprehensible guide to controller area network](a-comprehensible-guide-to-controller-area-network.md)
- [eth-ws-someip](eth-ws-someip.md)
- [TOW-IDS: automotive ethernet intrusion dataset](tow-ids-automotive-ethernet-intrusion-dataset.md)
- [vsomeip](vsomeip.md)
