# Facet: IVI

Infotainment and head-unit runtime and update trust.

Generated from page frontmatter by tools/ingest.py; 18 pages (entities and concepts). Do not edit by hand.

## Infotainment and IVI

- [Chimaera](chimaera.md) — Research framework for IVI (In-Vehicle Infotainment) firmware reverse engineering and exploitation targeting Hyundai/Kia Gen5W_L systems.
- [MMI3G-Toolkit](mmi3g-toolkit.md) — SD-card-based toolkit for Audi/VW MMI3G head units covering boot-image extraction, reverse-engineered GEMMI protocol details, and an FSC signature-bypass…
- [Q50 Reverse Engineering](q50-reverse-engineering.md) — Independent reverse-engineering research into the Infiniti Q50 infotainment platform's Linux/Android environment, documenting its EPK firmware package…
- [byd-dolphin-hacking](byd-dolphin-hacking.md) — Reverse engineering of the BYD Dolphin DiLink 3 head unit (Android 10 on a Qualcomm QCM6125), documenting its MCU and CAN interfaces, OTA update paths, and…
- [gen5fw](gen5fw.md) — Python tools for decrypting, patching, and redeploying firmware on Mobis Gen5 navigation head units in Hyundai, Kia, and Genesis vehicles, including…
- [ic1101](ic1101.md) — Open research project for reverse engineering 10th generation Honda Civic infotainment systems (Android-based, NVIDIA Tegra 3).
- [idrive7-8-ssh-root](idrive7-8-ssh-root.md) — Enable root SSH on BMW iDrive 7/8 MGU head units over ENET via debug image flash and persistent SSH without B7F8E5 DTC, for head unit reverse engineering.

## Research Papers

- [LeiA: A Lightweight Authentication Protocol for CAN](leia-a-lightweight-authentication-protocol-for-can.md) — Radu and Garcia, ESORICS 2016. Backwards-compatible per-ID authentication that fits CAN's timing and bandwidth limits, compartmentalising ECUs so a…

## Conference Presentations

- [Back in the Driver's Seat: Recovering Critical Data from Tesla Autopilot Using Voltage Glitching](back-in-the-driver-s-seat-recovering-critical-data-from-tesla-autopilot-using-voltage-glitching.md) — Kuhnapfel, Werling, and Jacob, 37C3 2023. Voltage-glitching attack that gives root on Tesla Autopilot hardware and recovers protected data.
- [Back-connect to the Connected Car. Search for Vulnerabilities in the VW Electric Car.](back-connect-to-the-connected-car-search-for-vulnerabilities-in-the-vw-electric-car.md) — Serdyuk, Kondikov, Razmakhnin, and Sakr, Black Hat Europe 2022. Maps the attack surface of the VW ID.3 across Wi-Fi, Bluetooth, V2X, cellular, CAN, and…
- [Meet Salinas: The First Ever SMS-Commanded Car Infotainment RAT](meet-salinas-the-first-ever-sms-commanded-car-infotainment-rat.md) — Regalado, DEF CON 26 Car Hacking Village 2018. Shows how a production infotainment unit can be infected with malware that exfiltrates the driver's data…
- [Over the Air: Compromise of Modern Volkswagen Group Vehicles](over-the-air-compromise-of-modern-volkswagen-group-vehicles.md) — Ivachev and Parnishchev, Black Hat Europe 2024. Bluetooth attack chain against Volkswagen Group MIB3 infotainment yielding persistent code execution…
- [Pwn2Own Automotive 2026: Day Three Results and the Master of Pwn](pwn2own-automotive-2026-day-three-results-and-the-master-of-pwn.md) — Zero Day Initiative, Tokyo 2026. Final results of the contest, where $1,047,000 was awarded for 76 unique zero-days in infotainment systems and EV chargers.

## Books

- [Automotive Cybersecurity: Protecting Connected and Autonomous Vehicles](automotive-cybersecurity-protecting-connected-and-autonomous-vehicles.md) — Alfred Basta and Sam Hana, Kendall Hunt 2026. Textbook covering threats from ECU networks and sensor spoofing to OTA patching, EV charging breaches, and…
- [Hacking Connected Cars](hacking-connected-cars.md) — Alissa Knight, Wiley 2020. Tactics, techniques, and procedures for penetration testing, threat modelling, and risk assessment of telematics control units…

## Concepts

- [Firmware acquisition: the read-side channels](concepts/firmware-acquisition.md) — Before analysis comes acquisition: the channels the corpus documents for getting an ECU's image out — by bus, by bootstrap, by bench, by log, by package.
- [IVI runtime privilege and service exposure](concepts/ivi-runtime-privilege.md) — The head unit's failures that are not on the update path: declared-but-unenforced permissions, unchecked service callers, and designed-in debug surfaces.
- [IVI update-path trust](concepts/ivi-update-trust.md) — How head-unit update trust anchors fail across six IVI platforms: absent checks, a public test key, a fleet-wide key, CRC-only integrity, patchable verifiers.
