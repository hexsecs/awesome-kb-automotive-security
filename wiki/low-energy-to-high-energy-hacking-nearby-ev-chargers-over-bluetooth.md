---
uid: 01a19d3c-afac-7abf-8bce-67c99028ba65
title: "Low Energy to High Energy: Hacking Nearby EV-Chargers Over Bluetooth"
summary: "Alkemade and Nassar, Black Hat USA 2024. Bluetooth attacks on three EV chargers, built from exploits demonstrated at Pwn2Own Automotive 2024."
type: entity
category: "Conference Presentations"
url: "https://citation.thinkst.com/talk/89711"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Alkemade and Nassar, Black Hat USA 2024. Bluetooth attacks on three EV chargers, built from exploits demonstrated at Pwn2Own Automotive 2024."
sources:
  - url: "https://citation.thinkst.com/talk/89711"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - pwn2own-automotive-2026-day-three-results-and-the-master-of-pwn
  - ocpp-charging-attacks
  - brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging
---

Alkemade and Nassar, Black Hat USA 2024. Bluetooth attacks on three EV chargers, built from exploits demonstrated at Pwn2Own Automotive 2024.

A Black Hat USA 2024 briefing by Alkemade and Nassar of Computest Sector 7, unpacking the team's exploits from the first Pwn2Own Automotive (ZDI, Tokyo, January 2024). At the contest, Sector 7 demonstrated vulnerabilities in three different EV chargers, each exploitable to arbitrary code execution with a single prerequisite: being close enough to connect over Bluetooth. The talk explains the vulnerabilities found and the exploits developed, and draws out the general IoT-security lessons — the authors note the bugs were mostly easy to find once the charger firmware was extracted, and that a lack of binary-exploitation mitigations made writing reliable exploits equally straightforward.

What you get: the recorded briefing video. Watch it alongside ZDI's Pwn2Own Automotive 2024 results coverage for the contest framing; the talk itself is the technical follow-up the contest format doesn't allow. It is aimed at charger vendors, embedded/IoT practitioners, and anyone evaluating Bluetooth as an attack surface on high-power equipment. Caveats: a 2024 snapshot of three specific charger targets and their then-current firmware — the vulnerabilities went through ZDI's coordinated disclosure to the vendors before the talk, so treat the details as a case study in charger firmware hygiene rather than a current exposure list.

## Status and sources

Status: **published** — Black Hat USA 2024 briefing; recording public. Abstract verified at [citation.thinkst.com/talk/89711](https://citation.thinkst.com/talk/89711) (the stub's resource) and against Black Hat's USA 2024 briefing announcement, 2026-11-01.

## Related

- [Pwn2Own Automotive 2026: Day Three Results and the Master of Pwn](pwn2own-automotive-2026-day-three-results-and-the-master-of-pwn.md) — the later edition of the contest this talk grew out of
- [OCPP charging attacks](concepts/ocpp-charging-attacks.md) — the concept page for the charger/backend attack surface
- [Brokenwire](brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging.md) — the other proximity attack on charging equipment in this KB
