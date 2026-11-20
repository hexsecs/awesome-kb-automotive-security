# Facet: Automotive Ethernet

100/1000BASE-T1, MACsec and in-vehicle IP networking.

Generated from page frontmatter by tools/ingest.py; 24 pages (entities and concepts). Do not edit by hand.

## Diagnostic Tools

- [doip-sim-ecu-dsl](doip-sim-ecu-dsl.md) — Kotlin DSL for scripting simulated DoIP ECUs, reachable over Ethernet, CAN with ISO-TP, or both at once, for exercising diagnostic clients against UDS error…
- [python-doipclient](python-doipclient.md) — Pure Python DoIP (ISO 13400) client that plugs into udsoncan as a transport layer for diagnostics over automotive Ethernet.
- [uds](uds.md) — Python package for ISO 14229 UDS in both client and server roles over CAN, Ethernet, LIN, FlexRay, and K-Line, usable for simulation, testing, and decoding…

## Firmware and ECU Reverse Engineering

- [pyXCP](pyxcp.md) — Python implementation of the ASAM MCD-1 XCP protocol over CAN, Ethernet, and USB, with seed-and-key access handling, for measuring, calibrating, and…

## Automotive Ethernet

- [ICS CAP](ics-cap.md) — Free Wireshark plugin for monitoring Automotive Ethernet, CAN, CAN FD, LIN, and FlexRay networks.
- [ProtoCrawler](protocrawler.md) — Intelligent protocol fuzzer for SOME/IP, DoIP, UDS, and Ethernet AVB satisfying ISO/SAE 21434 testing requirements.
- [eth-ws-someip](eth-ws-someip.md) — Wireshark LUA dissectors for Automotive Ethernet SOME/IP and SOME/IP-SD protocols (Autosar 4.2).
- [vsomeip](vsomeip.md) — COVESA reference implementation of SOME/IP and SOME/IP-SD, used both as the target in automotive Ethernet fuzzing research and as a client for crafting…

## Security Analysis

- [Automotive Threat Modeling Template](automotive-threat-modeling-template.md) — NCC Group stencil set for the Microsoft Threat Modeling Tool, supplying vehicle-specific element types, trust boundaries, and threat rules for ECU and…

## Datasets

- [CarDS](cards.md) — ACSAC 2025 dataset of over nine hours of traffic from a 2020 electric vehicle with 10 CAN buses and 6 automotive Ethernet buses, covering benign driving and…
- [TOW-IDS Automotive Ethernet Intrusion Dataset](tow-ids-automotive-ethernet-intrusion-dataset.md) — HCRL captures of AVTP, gPTP, and CAN-over-UDP traffic on an automotive Ethernet network, split into normal driving and five labelled attack scenarios.

## Research Papers

- [Error Handling of In-vehicle Networks Makes Them Vulnerable](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md) — Cho and Shin, ACM CCS 2016. The bus-off attack, which abuses CAN error handling to force an uncompromised ECU off the bus without any vehicle-specific…
- [GIDS: GAN based Intrusion Detection System for In-Vehicle Network](gids-gan-based-intrusion-detection-system-for-in-vehicle-network.md) — Seo, Song, and Kim, PST 2018. Trains a GAN on normal CAN traffic only, and is a common deep-learning IDS baseline alongside the authors' Car-Hacking dataset.
- [Viden: Attacker Identification on In-Vehicle Networks](viden-attacker-identification-on-in-vehicle-networks.md) — Cho and Shin, ACM CCS 2017. Fingerprints transmitting ECUs by their analogue voltage signature, moving CAN defence from detecting an attack to naming the…

## Conference Presentations

- [Back-connect to the Connected Car. Search for Vulnerabilities in the VW Electric Car.](back-connect-to-the-connected-car-search-for-vulnerabilities-in-the-vw-electric-car.md) — Serdyuk, Kondikov, Razmakhnin, and Sakr, Black Hat Europe 2022. Maps the attack surface of the VW ID.3 across Wi-Fi, Bluetooth, V2X, cellular, CAN, and…
- [Fast and Compromised: Automotive Security on a Timer](fast-and-compromised-automotive-security-on-a-timer.md) — Ziv and Alfasi, escar USA 2025. Penetration test taking a production electric vehicle from an insecure Wi-Fi network to full compromise in eight working…

## Books

- [Automotive Cybersecurity: Protecting Connected and Autonomous Vehicles](automotive-cybersecurity-protecting-connected-and-autonomous-vehicles.md) — Alfred Basta and Sam Hana, Kendall Hunt 2026. Textbook covering threats from ECU networks and sensor spoofing to OTA patching, EV charging breaches, and…
- [Automotive Ethernet](automotive-ethernet.md) — Matheus and Königseder, Cambridge University Press 2021. The standard reference on automotive Ethernet, covering PHYs, TSN, and security concepts for…
- [Hacking Connected Cars](hacking-connected-cars.md) — Alissa Knight, Wiley 2020. Tactics, techniques, and procedures for penetration testing, threat modelling, and risk assessment of telematics control units…
- [Offensive Automotive Cybersecurity](offensive-automotive-cybersecurity.md) — Ahmad MK Nasser and Dennis Kengo Oka, Packt 2026. The two handbook authors together on the offensive side, covering exploitation of modern automotive platforms.

## Learning Resources

- [Automotive Cybersecurity Roadmap](automotive-cybersecurity-roadmap.md) — Structured learning path from CAN and UDS fundamentals through TARA, firmware reverse engineering, and hardware hacking into specialized career tracks.
- [Automotive-Networking-Security](automotive-networking-security.md) — Automotive networking security standards and solutions overview.
- [What is Automotive MACsec?](what-is-automotive-macsec.md) — Video training on Automotive MACsec concepts by Technica Engineering.

## Concepts

- [SOME/IP and SOME/IP-SD](concepts/someip.md) — AUTOSAR's service-oriented middleware over IP: how services are offered, found and invoked — and why discovery is the trust root of every SOME/IP conversation.
