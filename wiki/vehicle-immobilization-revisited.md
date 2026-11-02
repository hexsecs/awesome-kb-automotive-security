---
uid: 01a19d3c-aff5-73c9-b99a-e7b70f791641
title: "Vehicle Immobilization Revisited"
summary: "Bokslag, 36C3 2019. Studies three vehicles and shows the immobilizer transponder talks to the body control module rather than the ECM, so weak…"
type: entity
category: "Conference Presentations"
url: "https://media.ccc.de/v/36c3-11020-vehicle_immobilization_revisited"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Bokslag, 36C3 2019. Studies three vehicles and shows the immobilizer transponder talks to the body control module rather than the ECM, so weak authentication at either link allows an unauthorised start."
sources:
  - url: "https://media.ccc.de/v/36c3-11020-vehicle_immobilization_revisited"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer
  - gone-in-360-seconds-hijacking-with-hitag2
---

Bokslag, 36C3 2019. Studies three vehicles and shows the immobilizer transponder talks to the body control module rather than the ECM, so weak authentication at either link allows an unauthorised start.

A 36C3 (2019) talk by Wouter Bokslag, from his academic work on vehicle immobilizers. Most immobilizer research targets the key transponder; Bokslag examines the overlooked second link. In the three vehicles he investigated — from the Peugeot, Fiat, and Opel groups — the security transponder does not authenticate to the engine control module (ECM) directly, but to the body control module (BCM), which then authenticates itself to the ECM to release the immobilizer. He identified the immobilizer messages in CAN traffic, dumped ECM and BCM firmware (via existing software functions and JTAG/BDM debug access), and reverse-engineered those BCM–ECM protocols: two of the three are completely broken, and the third is derived directly from a 1995 security transponder design. Either weakness — transponder or BCM–ECM link — therefore allows an unauthorised start, and both attacks run through the standardised OBD-II connector; the same protocols are used across many models of each manufacturer group, including then-current production.

What you get: the full talk video and slides on media.ccc.de — a methodical walk from CAN trace analysis to protocol breakage. It pairs naturally with the classic transponder breaks (Hitag2, Megamos) as the "other half" of the immobilizer story, and its pattern — the in-vehicle authentication hop being weaker than the credential it carries — keeps recurring in later work. Caveats: the case studies are 2010s European volume brands; treat the specific protocols as history and the structural lesson as current.

## Status and sources

Status: **published** — 36C3, December 2019; recording and slides public. Verified against the talk page and abstract at [media.ccc.de](https://media.ccc.de/v/36c3-11020-vehicle_immobilization_revisited) (the stub's resource), 2026-11-01.

## Related

- [Dismantling Megamos Crypto](dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md) — the transponder-side break; this talk is about the link behind the transponder
- [Gone in 360 Seconds: Hijacking with Hitag2](gone-in-360-seconds-hijacking-with-hitag2.md) — the other classic transponder case study
