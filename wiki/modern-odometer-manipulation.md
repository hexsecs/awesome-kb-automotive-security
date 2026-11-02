---
uid: 01a19d3c-afaf-7121-b5bc-e7c687a9fcf3
title: "Modern Odometer Manipulation"
summary: "collin and oblivion, DEF CON 33 Car Hacking Village 2025. Slides reverse engineering a device that alters a message before it reaches the instrument…"
type: entity
category: "Conference Presentations"
url: "https://media.defcon.org/DEF%20CON%2033/DEF%20CON%2033%20villages%20and%20creators/DEF%20CON%2033%20-%20Car%20Hacking%20Village%20-%20collin%20%26%20oblivion%20-%20Modern%20Odometer%20Manipulation.pdf"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "collin and oblivion, DEF CON 33 Car Hacking Village 2025. Slides reverse engineering a device that alters a message before it reaches the instrument cluster, using a glitching bypass of flash read protection."
sources:
  - url: "https://media.defcon.org/DEF%20CON%2033/DEF%20CON%2033%20villages%20and%20creators/DEF%20CON%2033%20-%20Car%20Hacking%20Village%20-%20collin%20%26%20oblivion%20-%20Modern%20Odometer%20Manipulation.pdf"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - back-in-the-driver-s-seat-recovering-critical-data-from-tesla-autopilot-using-voltage-glitching
  - can-injection
---

collin and oblivion, DEF CON 33 Car Hacking Village 2025. Slides reverse engineering a device that alters a message before it reaches the instrument cluster, using a glitching bypass of flash read protection.

A DEF CON 33 (2025) talk by collin and oblivion: a teardown and firmware analysis of a commercial odometer-manipulation device — the kind of multi-brand tool sold to commit odometer fraud by making a car report lower mileage than it has driven. The speakers examine the device hardware, extract its firmware from a locked STM32 by bypassing the chip's flash read protection with voltage glitching, and analyse how the device sits in-line on the vehicle's network and rewrites the CAN messages bound for the instrument cluster so the displayed mileage is altered. The talk also explains the broader fraud problem and shows an example of detecting that such a device was used even after it has been removed from the car.

What you get: the slide deck on media.defcon.org and a video recording of the talk. It is most useful to anti-fraud and anti-tamper practitioners — OEM engineers, insurers, used-car platforms, and forensic examiners — because its centre of gravity is detection and attribution rather than the manipulation itself. Caveats: a single device family is dissected, so specific message details do not transfer directly to other tools or brands; and the technical core (defeating read protection on a locked MCU) will be familiar from the fault-injection literature — the novelty is its application to fraud-device forensics.

## Status and sources

Status: **published** — DEF CON 33, August 2025; slides and recording public. Deck is the stub's resource on [media.defcon.org](https://media.defcon.org/DEF%20CON%2033/DEF%20CON%2033%20villages%20and%20creators/DEF%20CON%2033%20-%20Car%20Hacking%20Village%20-%20collin%20%26%20oblivion%20-%20Modern%20Odometer%20Manipulation.pdf); talk listing verified on the DEF CON 33 schedule and the recorded-talk description, 2026-11-01.

## Related

- [Back in the Driver's Seat](back-in-the-driver-s-seat-recovering-critical-data-from-tesla-autopilot-using-voltage-glitching.md) — voltage glitching used the same way: to get firmware/data out of a locked automotive chip
- [CAN injection](concepts/can-injection.md) — the device is a commercialised in-line message-rewriting instance of this attack class
