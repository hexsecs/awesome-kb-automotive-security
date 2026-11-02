---
title: "Back in the Driver's Seat: Recovering Critical Data from Tesla Autopilot Using Voltage Glitching"
summary: "Kuhnapfel, Werling, and Jacob, 37C3 2023. Voltage-glitching attack that gives root on Tesla Autopilot hardware and recovers protected data."
type: entity
category: "Conference Presentations"
url: "https://media.ccc.de/v/37c3-12144-back_in_the_driver_s_seat_recovering_critical_data_from_tesla_autopilot_using_voltage_glitching"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Kuhnapfel, Werling, and Jacob, 37C3 2023. Voltage-glitching attack that gives root on Tesla Autopilot hardware and recovers protected data."
sources:
  - url: "https://media.ccc.de/v/37c3-12144-back_in_the_driver_s_seat_recovering_critical_data_from_tesla_autopilot_using_voltage_glitching"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - modern-odometer-manipulation
  - secoc-key-extractor
---

Kuhnapfel, Werling, and Jacob, 37C3 2023. Voltage-glitching attack that gives root on Tesla Autopilot hardware and recovers protected data.

A 37C3 (2023) talk by Niclas Kühnapfel, Christian Werling, and Hans Niklas Jacob. The team demonstrates a voltage-glitching attack on Tesla's arm64-based Autopilot computer that yields root privileges, letting them extract arbitrary code and user data from the system — including the onboard camera and sensor data that third parties (for example, crash investigators) are normally locked out of — plus, among other cryptographic material, a hardware-unique key that Autopilot uses to authenticate itself to Tesla's servers. The talk also walks through Autopilot's security architecture and recaps the group's earlier voltage-glitching jailbreak of Tesla's AMD-based infotainment platform (Black Hat USA 2023), which enabled root-filesystem modification and temporary activation of paid features.

What you get: the full talk video on media.ccc.de, with subtitles, translated audio tracks, and slides. Read/watch it if you work on automotive hardware security, fault injection, or vehicle forensics — it is one of the clearest public accounts of taking a locked-down automotive SoC from glitch to data extraction. Caveats: this is a lab attack requiring physical access and glitching equipment, demonstrated on the Autopilot hardware generation current in 2023; no exploit code is released, and details track Tesla's hardware revisions, so expect specifics to age.

## Status and sources

Status: **published** — 37C3, December 2023; recording public. Verified against the talk page and abstract at [media.ccc.de](https://media.ccc.de/v/37c3-12144-back_in_the_driver_s_seat_recovering_critical_data_from_tesla_autopilot_using_voltage_glitching) (the stub's resource), 2026-11-01.

## Related

- [Modern Odometer Manipulation](modern-odometer-manipulation.md) — the same technique family: glitching past STM32 flash read protection
- [SecOC key extractor](secoc-key-extractor.md) — fault-injection key extraction from an automotive ECU
