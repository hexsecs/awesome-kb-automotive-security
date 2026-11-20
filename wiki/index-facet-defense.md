# Facet: Defense & architecture

Mitigations, secure design, segmentation and standards compliance.

Generated from page frontmatter by tools/ingest.py; 16 pages (entities and concepts). Do not edit by hand.

## CAN Bus Analysis

- [python-can-isotp](python-can-isotp.md) — ISO-TP (ISO 15765) transport for Python on top of python-can or Linux SocketCAN, the segmentation layer that UDS and OBD-II diagnostics run over.

## Research Papers

- [Automating Function-Level TARA for Automotive Full-Lifecycle Security](automating-function-level-tara-for-automotive-full-lifecycle-security.md) — Yang et al., NDSS 2026. DefenseWeaver, a multi-agent LLM system that automates function-level ISO/SAE 21434 threat analysis and risk assessment, reported as…
- [Securing Vehicular Ad Hoc Networks](securing-vehicular-ad-hoc-networks.md) — Raya and Hubaux, Journal of Computer Security 2007. Threat analysis and security architecture for VANETs that set the direction for most later V2X security…
- [SoK: Kicking CAN Down the Road. Systematizing CAN Security Knowledge](sok-kicking-can-down-the-road-systematizing-can-security-knowledge.md) — Serag et al., 2025. Systematization of two decades of CAN security, with a unified taxonomy and assessment model for attackers, attacks, and defences.
- [SoK: Stealing Cars Since Remote Keyless Entry Introduction and How to Defend From It](sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it.md) — Bianchi et al., USENIX VehicleSec 2025. Systematization of RKE and passive keyless entry and start systems, covering their history, the attacks against…
- [The Heat is On: Understanding and Mitigating Vulnerabilities of Thermal Image Perception in Autonomous Systems](the-heat-is-on-understanding-and-mitigating-vulnerabilities-of-thermal-image-perception-in-autonomous-systems.md) — Bhupathiraju et al., NDSS 2026. Shows heat sources degrade thermal-camera pedestrian detection and sensor fusion, including in real driving, and proposes…
- [Viden: Attacker Identification on In-Vehicle Networks](viden-attacker-identification-on-in-vehicle-networks.md) — Cho and Shin, ACM CCS 2017. Fingerprints transmitting ECUs by their analogue voltage signature, moving CAN defence from detecting an attack to naming the…

## Conference Presentations

- [Back in the Driver's Seat: Recovering Critical Data from Tesla Autopilot Using Voltage Glitching](back-in-the-driver-s-seat-recovering-critical-data-from-tesla-autopilot-using-voltage-glitching.md) — Kuhnapfel, Werling, and Jacob, 37C3 2023. Voltage-glitching attack that gives root on Tesla Autopilot hardware and recovers protected data.
- [Fast and Compromised: Automotive Security on a Timer](fast-and-compromised-automotive-security-on-a-timer.md) — Ziv and Alfasi, escar USA 2025. Penetration test taking a production electric vehicle from an insecure Wi-Fi network to full compromise in eight working…
- [Low Energy to High Energy: Hacking Nearby EV-Chargers Over Bluetooth](low-energy-to-high-energy-hacking-nearby-ev-chargers-over-bluetooth.md) — Alkemade and Nassar, Black Hat USA 2024. Bluetooth attacks on three EV chargers, built from exploits demonstrated at Pwn2Own Automotive 2024.

## Learning Resources

- [OWASP Automotive Security Cheat Sheet](owasp-automotive-security-cheat-sheet.md) — OWASP cheat sheet covering threat modeling, message authentication, secure boot, and update verification for vehicle ECUs and connected services.

## Related Awesome Lists

- [Awesome Embedded Security](awesome-embedded-security.md) — Tools and knowledge for embedded security research.

## Concepts

- [CAN availability and denial of service](concepts/can-availability.md) — Availability attacks remove or suppress the bus's genuine traffic, below the layer message authentication defends: flooding, bus-off, dominance, silencing.
- [In-vehicle intrusion detection and ECU fingerprinting](concepts/in-vehicle-intrusion-detection.md) — The bus's defence literature, organised by observable signal: timing, clock skew, voltage, learned models — and split by detecting an anomaly vs attributing it.
- [Physical-channel sensor attacks](concepts/physical-channel-sensor-attacks.md) — Attacks that manufacture the measurement itself — in acoustics, optics, RF, and heat — where no digital interface is touched and the output is faithfully wrong.
- [Rolling-code failure classes](concepts/rolling-code-failure-classes.md) — Rolling codes move trust from the code's secrecy to the receiver's counter state; the failure classes attack that state: windows, resync, harvesting, blocking.
