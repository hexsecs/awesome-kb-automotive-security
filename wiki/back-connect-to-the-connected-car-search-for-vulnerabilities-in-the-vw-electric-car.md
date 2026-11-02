---
title: "Back-connect to the Connected Car. Search for Vulnerabilities in the VW Electric Car."
summary: "Serdyuk, Kondikov, Razmakhnin, and Sakr, Black Hat Europe 2022. Maps the attack surface of the VW ID.3 across Wi-Fi, Bluetooth, V2X, cellular, CAN, and…"
type: entity
category: "Conference Presentations"
url: "https://citation.thinkst.com/talk/83581"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Serdyuk, Kondikov, Razmakhnin, and Sakr, Black Hat Europe 2022. Maps the attack surface of the VW ID.3 across Wi-Fi, Bluetooth, V2X, cellular, CAN, and OBD-II entry points."
sources:
  - url: "https://citation.thinkst.com/talk/83581"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - byd-dolphin-hacking
  - experimental-security-analysis-of-a-modern-automobile
  - secure-firmware-updates
---

Serdyuk, Kondikov, Razmakhnin, and Sakr, Black Hat Europe 2022. Maps the attack surface of the VW ID.3 across Wi-Fi, Bluetooth, V2X, cellular, CAN, and OBD-II entry points.

A Black Hat Europe 2022 briefing by Yuriy Serdyuk, Alexey Kondikov, Sergey Razmakhnin, and Khaled Sakr of NavInfo Europe, reporting a full penetration test of a Volkswagen ID.3 Pro. Working across the car's connected surface — Wi-Fi, Bluetooth, V2X, cellular, CAN, OBD-II, automotive Ethernet, USB, telematics, and the mobile app — they reached root in the infotainment and gateway modules, bypassed the digital-signature check in the Automotive Grade Linux update process, exploited an arbitrary-code-execution flaw in a QNX7 network service, extracted keys from the gateway's trust zone, and remotely controlled backdoors installed in the car over Wi-Fi. Per the abstract, the same architectural problems also apply to the ID.4 and ID.5, and the work was disclosed to Volkswagen (three vulnerability reports) before the talk.

What you get: the recorded briefing video (Black Hat's channel) and the full talk transcript; there is no separate paper. It is the natural briefing for anyone assessing VW's MEB platform or AGL/QNX-based in-vehicle architectures, and a good worked example of a whole-car pentest report structure. Caveats: this is a 2022 snapshot of cars then in production — expect the specific flaws to be patched; the talk demonstrates outcomes and demos rather than publishing a reproducible exploit write-up, and some findings required physical access to the vehicle.

## Status and sources

Status: **published** — Black Hat Europe 2022 briefing; recording and transcript public. Abstract verified at [citation.thinkst.com/talk/83581](https://citation.thinkst.com/talk/83581) (the stub's resource) and speaker names/substance cross-checked against the talk transcript (infocon.org Black Hat Europe 2022 captions), 2026-11-01.

## Related

- [BYD Dolphin hacking](byd-dolphin-hacking.md) — another whole-car assessment of a mass-market EV
- [Experimental Security Analysis of a Modern Automobile](experimental-security-analysis-of-a-modern-automobile.md) — the 2010 landmark whole-car study this genre descends from
- [Secure firmware updates](concepts/secure-firmware-updates.md) — the update-signature bypass is one of its failure modes in the wild
