---
uid: 01a19d3c-afe7-7c5d-82fb-1cf8c38ee57a
title: "The Car Hacker's Handbook"
summary: "Craig Smith, No Starch Press 2016. The foundational practical guide to vehicle security, covering threat modelling, CAN reverse engineering, and ECU…"
type: entity
category: "Books"
url: "https://www.opengarages.org/handbook/"
status: published
last_checked: 2026-11-17
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Craig Smith, No Starch Press 2016. The foundational practical guide to vehicle security, covering threat modelling, CAN reverse engineering, and ECU exploitation; free to read online via Open Garages."
related:
  - opengarages
  - hacking-connected-cars
  - a-comprehensible-guide-to-controller-area-network
  - automotive-cybersecurity-roadmap
sources:
  - url: "https://www.opengarages.org/handbook/"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
---

Craig Smith, No Starch Press 2016. The foundational practical guide to vehicle security, covering threat modelling, CAN reverse engineering, and ECU exploitation; free to read online via Open Garages.

## What it is

*The Car Hacker's Handbook: A Guide for the Penetration Tester*, by Craig Smith of Theia Labs and a founder of OpenGarages, published by No Starch Press in March 2016 (304 pages, ISBN 978-1-59327-703-1). It grew out of the 2014 OpenGarages publication and is described by its publisher as the standard first stop for anyone "curious about automotive security" who wants to "hack a two-ton computer". OpenGarages hosts the full text free to read online and as an `htmlz` download, under a **Creative Commons Attribution-Noncommercial-ShareAlike** licence.

## How it works

The book's structure follows a learn-by-doing arc. It begins with vulnerabilities and detailed explanations of CAN bus communications and communication between devices and systems, then moves to intercepting data and performing specific hacks. The publisher's list of what the reader will be able to do is a good summary of the coverage:

- Build an accurate **threat model** for a vehicle.
- **Reverse engineer the CAN bus** to fake engine signals.
- Exploit vulnerabilities in **diagnostic and data-logging systems**.
- Hack the **ECU and other firmware and embedded systems**.
- Feed exploits through **infotainment and vehicle-to-vehicle communication** systems.
- Override factory settings with **performance-tuning** techniques.
- Build **physical and virtual test benches** to try exploits safely.

The tooling is deliberately low-cost and open source: **Metasploit, Wireshark, Kayak, can-utils and ChipWhisperer** are named on the book's site. That combination — canonical CAN workflow plus cheap hardware — is why it remained the standard first recommendation for newcomers long after publication. No Starch also sells the print edition; translations are listed for Simplified Chinese, Korean, Italian and Japanese.

## Where it fits

This is the practical entry point of the corpus. [OpenGarages](opengarages.md) is the community project the book grew out of and the host of the free edition; [A Comprehensible Guide to Controller Area Network](a-comprehensible-guide-to-controller-area-network.md) is the protocol reference underneath the CAN chapters; [Hacking Connected Cars](hacking-connected-cars.md) is the field manual for the telematics side this book touches more lightly; [Automotive Cybersecurity Roadmap](automotive-cybersecurity-roadmap.md) is the structured self-study path that uses it. [Car Hacking Village](car-hacking-village.md) is the in-person setting where the same skills are practised.

## Limits and safety notes

This is a **2016 book**. Tooling and vehicle architectures have moved on: there is no ISO/SAE 21434 or UNECE R155 process material, nothing on software-defined vehicles, and no coverage of the newer Ethernet, sensor-attack and EV-charging material that makes up much of this KB. The CAN reverse-engineering workflow it teaches is still the canonical one, but readers should treat specific tool versions and vehicle examples as historical. The free edition is CC BY-NC-SA, so commercial reuse and remixing carry conditions. This page is based on the book's own publisher/OpenGarages page; the technical chapters were not re-verified against the text for these claims. No vehicle or ECU was used.

## Status and sources

Checked 2026-11-17. **Published** — Craig Smith, No Starch Press, March 2016; free online edition via OpenGarages.

- [OpenGarages handbook page (free online edition)](https://www.opengarages.org/handbook/)

## Related

- [OpenGarages](opengarages.md) — the community project the book grew out of, which hosts the free edition
- [Hacking Connected Cars](hacking-connected-cars.md) — the field manual for the telematics side this book touches lightly
- [A Comprehensible Guide to Controller Area Network](a-comprehensible-guide-to-controller-area-network.md) — the protocol reference underneath this book's CAN chapters
- [Automotive Cybersecurity Roadmap](automotive-cybersecurity-roadmap.md)
