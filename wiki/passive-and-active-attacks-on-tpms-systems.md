---
title: "Passive and Active Attacks on TPMS Systems"
summary: "Yago Lizarribar, DEF CON 33 Car Hacking Village 2025. Slides on long-term passive tracking of tire pressure sensors and active spoofing, both with commodity…"
type: entity
category: "Conference Presentations"
url: "https://media.defcon.org/DEF%20CON%2033/DEF%20CON%2033%20villages%20and%20creators/DEF%20CON%2033%20-%20Car%20Hacking%20Village%20-%20Yago%20Lizarribar%20-%20Passive%20and%20Active%20Attacks%20on%20TPMS%20Systems.pdf"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Yago Lizarribar, DEF CON 33 Car Hacking Village 2025. Slides on long-term passive tracking of tire pressure sensors and active spoofing, both with commodity SDR hardware."
sources:
  - url: "https://media.defcon.org/DEF%20CON%2033/DEF%20CON%2033%20villages%20and%20creators/DEF%20CON%2033%20-%20Car%20Hacking%20Village%20-%20Yago%20Lizarribar%20-%20Passive%20and%20Active%20Attacks%20on%20TPMS%20Systems.pdf"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study
  - rtl-433
---

Yago Lizarribar, DEF CON 33 Car Hacking Village 2025. Slides on long-term passive tracking of tire pressure sensors and active spoofing, both with commodity SDR hardware.

A DEF CON 33 Car Hacking Village talk by Yago Lizarribar (IMDEA Networks; now armasuisse). Direct TPMS sensors broadcast pressure readings together with a fixed, unique sensor ID, in clear text and without authentication — and the talk works through both consequences. Passively: a tracking infrastructure built from inexpensive commodity SDR receivers can re-identify and follow individual cars over the long term purely from their tyre sensors. Actively: the talk presents a tool for crafting custom TPMS messages and spoofing the TPMS ECUs of different cars. Lizarribar's related measurement study ("Can't Hide Your Stride," WONS 2026) puts scale on the passive half: a roadside network of ~$100 receivers captured, over ten weeks, millions of TPMS messages from over 20,000 vehicles — enough to infer presence, vehicle type, load, and movement patterns — while current vehicle cybersecurity regulation still does not address TPMS.

What you get: the slide deck on media.defcon.org and the recorded talk (posted by DEF CON under the title "Uncovering the Secrets of Tire Pressure Monitoring Systems"). It updates the classic 2010 TPMS case study with modern SDR economics, and is the pointer for privacy researchers and regulators as much as for car hackers. Caveats: sensor transmission behaviour varies by brand — some sensors transmit frequently even when the car is parked, others rarely — so tracking yield is fleet-dependent; and the large-scale numbers come from the companion paper, with the talk deck as the summary artefact.

## Status and sources

Status: **published** — DEF CON 33, Car Hacking Village, August 2025; slides and recording public. Deck is the stub's resource on [media.defcon.org](https://media.defcon.org/DEF%20CON%2033/DEF%20CON%2033%20villages%20and%20creators/DEF%20CON%2033%20-%20Car%20Hacking%20Village%20-%20Yago%20Lizarribar%20-%20Passive%20and%20Active%20Attacks%20on%20TPMS%20Systems.pdf); recording description and the companion paper (OrbiLu record) verified, 2026-11-01.

## Related

- [Security and Privacy Vulnerabilities of In-Car Wireless Networks: A TPMS Case Study](security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study.md) — the 2010 paper that founded this threat model; this talk is its modern sequel
- [rtl_433](rtl-433.md) — the commodity-SDR receiver software class used for this kind of passive collection
