# Facet: Authentication & keys

Message authentication, SecOC, key management and shared secrets.

Generated from page frontmatter by tools/ingest.py; 37 pages. Do not edit by hand.

## CAN Bus Analysis

- [CANExplorer](canexplorer.md) — Cross-platform CAN, CAN FD, and LIN analysis GUI with reverse-engineering tools, UDS discovery and fuzzing, DoIP and SOME/IP support, and SecOC decoding.

## Automotive Ethernet

- [Scapy](scapy.md) — Python packet manipulation library with support for DoIP, SOME/IP, AUTOSAR PDUs, SecOC, CAN-FD, and FlexRay protocols.

## Penetration Testing

- [SecOC Key Extractor](secoc-key-extractor.md) — Scripts to extract SecOC (Secure On-Board Communication) keys from Toyota vehicles using comma.ai panda hardware.

## Datasets

- [TOW-IDS Automotive Ethernet Intrusion Dataset](tow-ids-automotive-ethernet-intrusion-dataset.md) — HCRL captures of AVTP, gPTP, and CAN-over-UDP traffic on an automotive Ethernet network, split into normal driving and five labelled attack scenarios.

## Research Papers

- [A Formal Security Analysis of CAN XL](a-formal-security-analysis-of-can-xl.md) — Tang et al., USENIX Security 2026. First formal security analysis of the CAN XL standard, showing it retains all known classic CAN MAC sub-layer flaws and…
- [BLE Theft Auto: Evaluating the Security of Aftermarket BLE-based Automotive Remote Control Systems](ble-theft-auto-evaluating-the-security-of-aftermarket-ble-based-automotive-remote-control-systems.md) — Yu et al., USENIX Security 2026. Shows three of six aftermarket Bluetooth vehicle remote-control systems have critical pairing and authentication flaws…
- [Charge It to My Neighbor: A Relay Attack on ISO 15118 Plug and Charge Payment](charge-it-to-my-neighbor-a-relay-attack-on-iso-15118-plug-and-charge-payment.md) — Löw et al., USENIX VehicleSec 2026. Relays Plug and Charge authentication so the attacker charges their own car while the victim is billed, exploiting…
- [Dismantling Megamos Crypto: Wirelessly Lockpicking a Vehicle Immobilizer](dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md) — Verdult, Garcia, and Ege, USENIX Security 2015. Reverse engineers the Megamos immobilizer used by Audi, Fiat, Honda, Volkswagen, and Volvo; famously…
- [LeiA: A Lightweight Authentication Protocol for CAN](leia-a-lightweight-authentication-protocol-for-can.md) — Radu and Garcia, ESORICS 2016. Backwards-compatible per-ID authentication that fits CAN's timing and bandwidth limits, compartmentalising ECUs so a…
- [Pseudonym Schemes in Vehicular Networks: A Survey](pseudonym-schemes-in-vehicular-networks-a-survey.md) — Petit, Schaub, Feiri, and Kargl, IEEE Communications Surveys and Tutorials 2015. Defines the pseudonym lifecycle and categorises the schemes that reconcile…
- [Security and Privacy Vulnerabilities of In-Car Wireless Networks: A Tire Pressure Monitoring System Case Study](security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study.md) — Rouf et al., USENIX Security 2010. Shows TPMS sensors are unauthenticated and trackable at roughly 40m, the first published wireless in-car network attack.
- [Security in Automotive Bus Systems](security-in-automotive-bus-systems.md) — Wolf, Weimerskirch, and Paar, Workshop on Embedded Security in Cars 2004. The first systematic treatment of CAN, LIN, MOST, and FlexRay as security…
- [VulCAN: Efficient Component Authentication and Software Isolation for Automotive Control Networks](vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks.md) — Van Bulck, Muhlberg, and Piessens, ACSAC 2017. Combines message authentication with trusted-computing isolation, defending against an adversary running…
- [vatiCAN: Vetted, Authenticated CAN Bus](vatican-vetted-authenticated-can-bus.md) — Nurnberger and Rossow, CHES 2016. Retrofit authentication for CAN using MACs and a global nonce, a reference point for later SecOC-style designs.

## Conference Presentations

- [Back in the Driver's Seat: Recovering Critical Data from Tesla Autopilot Using Voltage Glitching](back-in-the-driver-s-seat-recovering-critical-data-from-tesla-autopilot-using-voltage-glitching.md) — Kuhnapfel, Werling, and Jacob, 37C3 2023. Voltage-glitching attack that gives root on Tesla Autopilot hardware and recovers protected data.
- [CANdid: A Stealthy Stepping-Stone Attack to Bypass Authentication on ECUs](candid-a-stealthy-stepping-stone-attack-to-bypass-authentication-on-ecus.md) — Kulandaivel, Jain, Guajardo, and Sekar, escar USA 2022. Shows a compromised ECU can authenticate against a safety-critical ECU's SecurityAccess without the…
- [DriveThru Car Hacking: Fast Food, Faster Data Breach](drivethru-car-hacking-fast-food-faster-data-breach.md) — Chen et al., Black Hat Asia 2025. Attack chain against more than 24 dashcam models, delivered through a drive-through ordering flow, with an accompanying tool.
- [Fast and Compromised: Automotive Security on a Timer](fast-and-compromised-automotive-security-on-a-timer.md) — Ziv and Alfasi, escar USA 2025. Penetration test taking a production electric vehicle from an insecure Wi-Fi network to full compromise in eight working…
- [How API Flaws Led to Admin Access to Over 1k USA Dealers and Control Over Your Car](how-api-flaws-led-to-admin-access-to-over-1k-usa-dealers-and-control-over-your-car.md) — Eaton Zveare, DEF CON 33 Car Hacking Village 2025. Slides showing how flaws in an automaker's central dealer platform yielded a national admin account…
- [Passive and Active Attacks on TPMS Systems](passive-and-active-attacks-on-tpms-systems.md) — Yago Lizarribar, DEF CON 33 Car Hacking Village 2025. Slides on long-term passive tracking of tire pressure sensors and active spoofing, both with commodity…
- [Vehicle Immobilization Revisited](vehicle-immobilization-revisited.md) — Bokslag, 36C3 2019. Studies three vehicles and shows the immobilizer transponder talks to the body control module rather than the ECM, so weak…

## Books

- [Securing Electric Mobility](securing-electric-mobility.md) — Aparna Kumari (ed.), Elsevier 2026. Edited volume on the security of electric vehicles and charging infrastructure.

## Learning Resources

- [Automotive-Networking-Security](automotive-networking-security.md) — Automotive networking security standards and solutions overview.
- [Fleet Cyber Challenge](fleet-cyber-challenge.md) — NMFTA's free self-paced capture-the-flag lab for commercial vehicle security, with scenarios on CAN traffic analysis, ELD compromise, GPS spoofing, firmware…
- [OWASP Automotive Security Cheat Sheet](owasp-automotive-security-cheat-sheet.md) — OWASP cheat sheet covering threat modeling, message authentication, secure boot, and update verification for vehicle ECUs and connected services.

## Concepts

- [CAN availability and denial of service](concepts/can-availability.md) — Availability attacks remove or suppress the bus's genuine traffic, below the layer message authentication defends: flooding, bus-off, dominance, silencing.
- [CAN injection](concepts/can-injection.md) — Attacker taps exposed CAN wiring and impersonates a trusted ECU: classic CAN frames carry no sender authentication, so fake 'key valid' messages are believed.
- [CAN message authentication: the retrofit design space](concepts/can-message-authentication.md) — Two complete academic designs and the standardised answer, compared on freshness, key scope, frame cost, and evidence — plus the two limits they all share.
- [IVI update-path trust](concepts/ivi-update-trust.md) — How head-unit update trust anchors fail across six IVI platforms: absent checks, a public test key, a fleet-wide key, CRC-only integrity, patchable verifiers.
- [In-vehicle intrusion detection and ECU fingerprinting](concepts/in-vehicle-intrusion-detection.md) — The bus's defence literature, organised by observable signal: timing, clock skew, voltage, learned models — and split by detecting an anomaly vs attributing it.
- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md) — Two attackers relay a genuine key's radio exchange, so the car sees a valid key 'nearby' — encryption doesn't help, because nothing was forged, only forwarded.
- [Misbehavior detection in V2X](concepts/misbehavior-detection.md) — Why V2X needs a layer beyond signatures: detecting false content from validly credentialed stations, reporting it, and the authority that decides.
- [Physical-channel sensor attacks](concepts/physical-channel-sensor-attacks.md) — Attacks that manufacture the measurement itself — in acoustics, optics, RF, and heat — where no digital interface is touched and the output is faithfully wrong.
- [SOME/IP and SOME/IP-SD](concepts/someip.md) — AUTOSAR's service-oriented middleware over IP: how services are offered, found and invoked — and why discovery is the trust root of every SOME/IP conversation.
- [Shared, default, and global secrets: the break-once pattern](concepts/shared-and-default-secrets.md) — The decisive failure is rarely cipher strength — it is one secret shared by a fleet or a type, or a default nobody changed. Break one, break all.
- [UDS seed/key (SecurityAccess)](concepts/uds-seed-key.md) — UDS SecurityAccess (0x27) gates privileged diagnostics behind a seed/key exchange; weak seeds, reused secrets and simple algorithms defeat it.
- [V2X credential management](concepts/v2x-credential-management.md) — How vehicles get pseudonymous credentials: split-knowledge issuance in the ETSI CCMS and US SCMS, so linking a ticket to an identity takes a quorum.
