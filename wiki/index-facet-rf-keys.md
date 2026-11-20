# Facet: RF & keys

Key fobs, RKE/PKE, rolling codes, TPMS and radio tooling.

Generated from page frontmatter by tools/ingest.py; 27 pages (entities and concepts). Do not edit by hand.

## CAN Bus Analysis

- [CAN Commander](can-commander.md) — Flipper Zero application and companion ESP32 CAN board for reverse engineering vehicle networks, with sniffing, DBC decoding, replay, and injection profiles…

## RF and Key Fob Analysis

- [Flipper Zero](flipper-zero.md) — Handheld multi-tool with Sub-GHz capabilities for reading, saving, and transmitting key fob signals with automotive database.
- [Flipper-ARF](flipper-arf.md) — Automotive-focused firmware fork for Flipper Zero supporting Keeloq, rolling codes, and VAG protocol analysis.
- [KeyFob Analysis Toolkit (KAT)](keyfob-analysis-toolkit-kat.md) — Toolkit for analyzing, decoding, and retransmitting key fob signals with support for HackRF, RTL-SDR, and Flipper Zero.
- [Proxmark3](proxmark3.md) — Industry-standard RFID/NFC research tool for reading, cloning, and emulating immobilizer transponders at 125kHz and 13.56MHz.
- [Universal Radio Hacker (URH)](universal-radio-hacker-urh.md) — Open-source suite for wireless protocol investigation with native SDR support and easy signal demodulation.
- [rtl_433](rtl-433.md) — Generic ISM band receiver for decoding TPMS sensors and key fobs at 315/433/868/915 MHz with RTL-SDR.

## Penetration Testing

- [tesla-opener](tesla-opener.md) — Open-source tool to open Tesla charging port using HackRF and WebUSB with ASK/OOK RF transmission.

## Datasets

- [VeReMi Extension](veremi-extension.md) — Simulated V2X misbehavior detection dataset generated with F2MD over the Luxembourg SUMO scenario, labelling position, speed, timing, replay, DoS, and Sybil…

## Research Papers

- [BLE Theft Auto: Evaluating the Security of Aftermarket BLE-based Automotive Remote Control Systems](ble-theft-auto-evaluating-the-security-of-aftermarket-ble-based-automotive-remote-control-systems.md) — Yu et al., USENIX Security 2026. Shows three of six aftermarket Bluetooth vehicle remote-control systems have critical pairing and authentication flaws…
- [Brokenwire: Wireless Disruption of CCS Electric Vehicle Charging](brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging.md) — Kohler, Baker, Strohmeier, and Martinovic, NDSS 2023. Aborts CCS rapid-charging sessions wirelessly from tens of metres with off-the-shelf radio hardware…
- [Dismantling Megamos Crypto: Wirelessly Lockpicking a Vehicle Immobilizer](dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md) — Verdult, Garcia, and Ege, USENIX Security 2015. Reverse engineers the Megamos immobilizer used by Audi, Fiat, Honda, Volkswagen, and Volvo; famously…
- [Fast, Furious and Insecure: Passive Keyless Entry and Start Systems in Modern Supercars](fast-furious-and-insecure-passive-keyless-entry-and-start-systems-in-modern-supercars.md) — Wouters et al., CHES 2019. Breaks the DST40-based PKES used by Tesla and others, cloning a key fob from a few seconds of proximity.
- [Gone in 360 Seconds: Hijacking with Hitag2](gone-in-360-seconds-hijacking-with-hitag2.md) — Verdult, Garcia, and Balasch, USENIX Security 2012. Breaks the Hitag2 immobilizer transponder, then fitted to over 200 car models, recovering the key by…
- [Lock It and Still Lose It: On the (In)Security of Automotive Remote Keyless Entry Systems](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md) — Garcia, Oswald, Kasper, and Pavlides, USENIX Security 2016. Recovers shared global keys covering most Volkswagen Group vehicles sold over two decades, and…
- [My Other Car is Your Car: Compromising the Tesla Model X Keyless Entry System](my-other-car-is-your-car-compromising-the-tesla-model-x-keyless-entry-system.md) — Wouters, Gierlichs, and Preneel, CHES 2021. Chains a BLE firmware downgrade and a key fob update flaw into unlocking and driving away a Tesla Model X.
- [Relay Attacks on Passive Keyless Entry and Start Systems in Modern Cars](relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars.md) — Francillon, Danev, and Capkun, NDSS 2011. Demonstrates the relay attack that still underpins most keyless vehicle theft today, against ten PKES systems from…
- [RollBack: A New Time-Agnostic Replay Attack Against the Automotive Remote Keyless Entry Systems](rollback-a-new-time-agnostic-replay-attack-against-the-automotive-remote-keyless-entry-systems.md) — Csikor et al., Black Hat USA 2022. Replaying already-invalid rolling codes in sequence triggers a resynchronisation rollback, unlocking a vehicle…
- [Security and Privacy Vulnerabilities of In-Car Wireless Networks: A Tire Pressure Monitoring System Case Study](security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study.md) — Rouf et al., USENIX Security 2010. Shows TPMS sensors are unauthenticated and trackable at roughly 40m, the first published wireless in-car network attack.
- [SoK: Stealing Cars Since Remote Keyless Entry Introduction and How to Defend From It](sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it.md) — Bianchi et al., USENIX VehicleSec 2025. Systematization of RKE and passive keyless entry and start systems, covering their history, the attacks against…

## Conference Presentations

- [How I Discovered and Hacked Learning Codes of the Key Fob of a Car Assembled in My Country](how-i-discovered-and-hacked-learning-codes-of-the-key-fob-of-a-car-assembled-in-my-country.md) — Erazo, DEF CON 32 Car Hacking Village 2024. Breaks the learning-code key fob of a locally assembled car with replay, a receiver backdoor, and a brute-force…
- [Passive and Active Attacks on TPMS Systems](passive-and-active-attacks-on-tpms-systems.md) — Yago Lizarribar, DEF CON 33 Car Hacking Village 2025. Slides on long-term passive tracking of tire pressure sensors and active spoofing, both with commodity…
- [Vehicle Immobilization Revisited](vehicle-immobilization-revisited.md) — Bokslag, 36C3 2019. Studies three vehicles and shows the immobilizer transponder talks to the body control module rather than the ECM, so weak…

## Concepts

- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md) — Two attackers relay a genuine key's radio exchange, so the car sees a valid key 'nearby' — encryption doesn't help, because nothing was forged, only forwarded.
- [Physical-channel sensor attacks](concepts/physical-channel-sensor-attacks.md) — Attacks that manufacture the measurement itself — in acoustics, optics, RF, and heat — where no digital interface is touched and the output is faithfully wrong.
- [Rolling-code failure classes](concepts/rolling-code-failure-classes.md) — Rolling codes move trust from the code's secrecy to the receiver's counter state; the failure classes attack that state: windows, resync, harvesting, blocking.
- [The vehicle's external attack surface: remote entry and the telematics pivot](concepts/external-attack-surface.md) — Compromise repeatedly begins at a boundary interface and pivots through the unit crossing it: connectivity units are most exposed and most privileged.
