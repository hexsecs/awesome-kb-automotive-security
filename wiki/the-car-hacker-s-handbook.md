---
uid: 01a19d3c-afe7-7c5d-82fb-1cf8c38ee57a
title: "The Car Hacker's Handbook"
summary: "Craig Smith, No Starch Press 2016. The foundational practical guide to vehicle security, covering threat modelling, CAN reverse engineering, and ECU…"
type: entity
category: "Books"
url: "https://www.opengarages.org/handbook/"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Craig Smith, No Starch Press 2016. The foundational practical guide to vehicle security, covering threat modelling, CAN reverse engineering, and ECU exploitation; free to read online via Open Garages."
sources:
  - url: "https://www.opengarages.org/handbook/"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - opengarages
  - hacking-connected-cars
  - a-comprehensible-guide-to-controller-area-network
---

Craig Smith, No Starch Press 2016. The foundational practical guide to vehicle security, covering threat modelling, CAN reverse engineering, and ECU exploitation; free to read online via Open Garages.

The foundational hands-on book of the field (subtitle: *A Guide for the Penetration Tester*), by Craig Smith of Theia Labs, a founder of OpenGarages. Expanded from the 2014 OpenGarages publication, it teaches by doing: understanding threat models, reverse engineering the CAN bus, attacking ECUs and firmware, infotainment and wireless systems — built around low-cost, open-source tools such as can-utils, Wireshark, Kayak, Metasploit, and ChipWhisperer. The full text is free to read online via OpenGarages, which keeps it the standard first recommendation for newcomers.

For beginners and intermediate practitioners who want to start touching a bus. Caveats: it is a 2016 book — tooling and vehicle architectures have moved on (no ISO/SAE 21434 or UNECE R155 era process material, nothing on software-defined vehicles), but the CAN reverse-engineering workflow it teaches is still the canonical one. 304 pages.

## Status and sources

Status: **published** — Craig Smith, No Starch Press, March 2016. ISBN 978-1-59327-703-1. Book's own site (free online edition): https://www.opengarages.org/handbook/ (checked 2026-11-01).

## Related

- [OpenGarages](opengarages.md) — the community project the book grew out of, which hosts the free edition
- [Hacking Connected Cars](hacking-connected-cars.md) — the field manual for the telematics side this book touches lightly
- [A Comprehensible Guide to Controller Area Network](a-comprehensible-guide-to-controller-area-network.md) — the protocol reference underneath this book's CAN chapters
