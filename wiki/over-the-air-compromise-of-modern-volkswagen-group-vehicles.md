---
uid: 01a1b552-f07f-7977-ac32-f29fcc38966a
title: "Over the Air: Compromise of Modern Volkswagen Group Vehicles"
summary: "Ivachev and Parnishchev, Black Hat Europe 2024. Bluetooth attack chain against Volkswagen Group MIB3 infotainment yielding persistent code execution…"
type: entity
category: "Conference Presentations"
url: "https://i.blackhat.com/EU-24/Presentations/EU-24-Parnishchev-OverTheAirVW.pdf"
status: published
last_checked: 2026-11-17
created: 2026-11-07
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 6ab6e98
list_summary: "Ivachev and Parnishchev, Black Hat Europe 2024. Bluetooth attack chain against Volkswagen Group MIB3 infotainment yielding persistent code execution, microphone recording, GPS tracking, and contact exfiltration across 1.4 million vehicles."
related:
  - back-connect-to-the-connected-car-search-for-vulnerabilities-in-the-vw-electric-car
  - drivethru-car-hacking-fast-food-faster-data-breach
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
  - low-energy-to-high-energy-hacking-nearby-ev-chargers-over-bluetooth
  - lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems
  - pwnobd
  - potential-cyberattacks-on-automated-vehicles
  - external-attack-surface
  - ivi-update-trust
  - ivi-runtime-privilege
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-07
  - url: "https://i.blackhat.com/EU-24/Presentations/EU-24-Parnishchev-OverTheAirVW.pdf"
    retrieved: 2026-11-17
facets: [firmware, ivi, sensors, attack, research]
---

Ivachev and Parnishchev, Black Hat Europe 2024. Bluetooth attack chain against Volkswagen Group MIB3 infotainment yielding persistent code execution, microphone recording, GPS tracking, and contact exfiltration across 1.4 million vehicles.

## What it is

A Black Hat Europe 2024 briefing by Artem Ivachev and Danila Parnishchev of PCA, with Mikhail Evdokimov, Aleksei Stennikov, Polina Smirnova, Radu Motspan and Abdellah Benotsmane. The target is the **Preh MIB3** infotainment unit — the talk uses a Skoda Superb 3 (B8, produced 2015–2023), with MIB3 appearing from 2021 and spanning many Volkswagen Group models. The source-list summary cites more than **1,400,000 cars sold in 2022** for the affected range. The research chains a Bluetooth-adjacent memory corruption bug into privileged, persistent code execution and remote control through a manufacturer backend.

## How it works

The team first tried the unit's UART without luck and moved to Bluetooth. They emulated a phone with a **Raspberry Pi 4** and NCC Group's **nOBEX** tool to implement the PBAP and HFP profiles, generating the HFP response file from captured traffic between the head unit and a real phone. This reached a **heap overflow in `picserver`'s libjpeg handling**: by placing a libjpeg object pool after the scan line and controlling the overflow's length and content, they achieved code execution using **JOP+ROP**.

Privilege escalation rode on MIB3's own architecture. A **custom IPC mechanism** on the Renesas R-CAR M3 SoC lacks access control, and the Networking service exposes an RPC (including `initCarPlayInterface`) with a **shell injection**. That service runs with **`CAP_SYS_MODULE`** while kernel module signature verification is disabled on MIB3's Linux, so the attackers could load an arbitrary kernel module and obtain root.

Persistence required defeating secure boot. MIB3 uses Renesas ARM Trusted Firmware with a proprietary image-compression feature; the vulnerability they found is in proprietary **BL2** code (not in Renesas's ATF). Content appended after decompression is not covered by the signature check, letting them modify the boot image and keep root across reboots. With that foothold they demonstrated microphone recording, GPS tracking, exfiltration of the contact database (a SQLite DB under `/var/lib/tsd.bt.phone.mib3/`) and photos, access to CAN, and **remote control over the internet** via the backend.

The deck lists twelve 2023 CVEs: CVE-2023-28902 (DoS via integer underflow in picserver), 28903 (DoS via integer overflow in picserver), 28904 (secure boot bypass in BL2), 28905 (heap buffer overflow in picserver), 28906 (command injection in networking service), 28907 (lack of access restrictions in CARCOM memory), 28908 (integer overflow in non-fragmented phone-service data), 28909 (integer overflow leading to MTU bypass), 28910 (disabled abortion flag), 28911 (arbitrary channel disconnection DoS), 28912 (clear-text phonebook information) and 29113 (lack of access control in custom IPC). The summary describes nine of the vulnerabilities as published in 2023 and twelve further findings disclosed at the conference, a 21-issue body of work. Disclosure ran from **07.03.2023** (report to `vulnerability@volkswagen.de`) through VW's clarification requests and a first meeting on 22.06.2023 where findings were confirmed, fixes communicated around end of 2023/early 2024, and public disclosure at Black Hat EU on **12.12.2024**.

## Where it fits

This is the connected-infotainment compromise case that matches the taxonomy in [Potential Cyberattacks on Automated Vehicles](potential-cyberattacks-on-automated-vehicles.md) and the remote-sensor concerns in [Remote attacks on automated vehicles' sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md). [Back to the connected car](back-connect-to-the-connected-car-search-for-vulnerabilities-in-the-vw-electric-car.md) is the earlier VW-side research; [DriveThru](drivethru-car-hacking-fast-food-faster-data-breach.md) and [PwnOBD](pwnobd.md) cover adjacent vehicle-data and diagnostic surfaces, and [Low Energy to High Energy](low-energy-to-high-energy-hacking-nearby-ev-chargers-over-bluetooth.md) is another Bluetooth-to-vehicle case. [Lock it and still lose it](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md) covers the RKE boundary rather than infotainment.

## Limits and safety notes

This page is drawn from the **official Black Hat slide deck**, not independent testing. The initial trigger requires Bluetooth proximity to the head unit; "over the air" here describes the eventual internet-controlled persistence, not a long-range radio exploit. The CVE-to-capability mapping in the deck is a chain across several distinct bugs, and the vehicle counts and affected-model scope are the speakers'/source-list figures rather than an independently verified VW advisory. The issues were responsibly disclosed and patched — this is a historical case of a coordinator-disclosed chain, not a live exploitation guide. No exploit code, vehicle or head unit was used for this page.

## Status and sources

Checked 2026-11-17. **Published** — Black Hat Europe 2024, December 2024; official briefing slides.

- [Black Hat EU 24 briefing slides](https://i.blackhat.com/EU-24/Presentations/EU-24-Parnishchev-OverTheAirVW.pdf)

## Related

- [Back to the connected car: search for vulnerabilities in the VW electric car](back-connect-to-the-connected-car-search-for-vulnerabilities-in-the-vw-electric-car.md)
- [DriveThru: car hacking, fast food, faster data breach](drivethru-car-hacking-fast-food-faster-data-breach.md)
- [Remote attacks on automated vehicles' sensors: experiments on camera and LiDAR](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md)
- [Low Energy to High Energy: hacking nearby EV chargers over Bluetooth](low-energy-to-high-energy-hacking-nearby-ev-chargers-over-bluetooth.md)
- [Lock it and still lose it: on the (in)security of automotive remote keyless entry systems](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md)
- [PwnOBD](pwnobd.md)
- [Potential Cyberattacks on Automated Vehicles](potential-cyberattacks-on-automated-vehicles.md)
- [The vehicle's external attack surface: remote entry and the telematics pivot](concepts/external-attack-surface.md)
- [IVI update-path trust](concepts/ivi-update-trust.md)

## Connections

- [IVI runtime privilege](concepts/ivi-runtime-privilege.md) — missing IPC access control and a networking service with module-loading capability turn the initial Bluetooth foothold into root execution before the separate persistence step.
