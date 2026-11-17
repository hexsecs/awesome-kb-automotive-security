# Glossary

Acronyms and standards used across this KB, with the page that explains each one. Generated from tools/taxonomy.py; do not edit by hand.

- **CAN** — Controller Area Network. See [CAN injection](concepts/can-injection.md) — The in-vehicle bus whose frames carry no sender identity.
- **CAN FD / CAN XL** — CAN with Flexible Data-rate / extra Long. See [A Formal Security Analysis of CAN XL](a-formal-security-analysis-of-can-xl.md) — Faster and larger-frame generations of CAN; the security substrate is unchanged.
- **ECU** — Electronic Control Unit. See [Bootloader stages and bootstrap entry](concepts/bootloader-stages.md) — A vehicle's embedded computer — the unit whose firmware and boot chain are in scope.
- **UDS** — Unified Diagnostic Services (ISO 14229). See [UDS seed/key (SecurityAccess)](concepts/uds-seed-key.md) — The highest-privilege diagnostic service set; 0x27 gates privileged access.
- **SecurityAccess** — UDS service 0x27 (seed/key). See [UDS seed/key (SecurityAccess)](concepts/uds-seed-key.md) — The challenge-response gate in front of privileged diagnostics.
- **ISO-TP** — ISO 15765-2 transport protocol. See [ISO-TP: the stateful transport under diagnostics](concepts/iso-tp.md) — Reassembles multi-frame diagnostic payloads on CAN; its flow control is attackable.
- **DoIP** — Diagnostics over Internet Protocol. See [DoIP moves diagnostics onto the network](concepts/doip.md) — Moves diagnostics from the OBD port to a routable endpoint.
- **OBD-II** — On-Board Diagnostics II. See [Diagnostic-service abuse](concepts/diagnostic-service-abuse.md) — The legally mandated diagnostic port and its service set.
- **DBC** — Database CAN. See [DBC as the CAN semantic layer](concepts/dbc-semantic-layer.md) — The file that names CAN IDs and decodes signals — a human claim, not ground truth.
- **XCP** — Universal Measurement and Calibration Protocol. See [The calibration plane (XCP/A2L)](concepts/calibration-plane.md) — Direct memory access into a running ECU, described by an A2L file.
- **A2L** — ASAM MCD-2 MC description file. See [The calibration plane (XCP/A2L)](concepts/calibration-plane.md) — Names the memory objects XCP can reach.
- **SOME/IP** — Scalable service-Oriented MiddlewarE over IP. See [SOME/IP and SOME/IP-SD](concepts/someip.md) — AUTOSAR's service middleware; service discovery is its trust root.
- **J1939** — SAE J1939. See [J1939 transport security](concepts/j1939.md) — Heavy-vehicle CAN application and transport layer with its own attackable state.
- **LIN** — Local Interconnect Network. See [LIN as the trusted subordinate bus](concepts/lin-bus.md) — A cheap subordinate bus often treated as trusted because it sits behind a gateway.
- **SecOC** — Secure Onboard Communication. See [CAN message authentication: the retrofit design space](concepts/can-message-authentication.md) — AUTOSAR's authenticated CAN framing; freshness and key scope still matter.
- **MACsec** — Media Access Control Security. See [What is Automotive MACsec?](what-is-automotive-macsec.md) — Link-layer encryption/authentication for Automotive Ethernet.
- **IDS** — Intrusion Detection System. See [In-vehicle intrusion detection and ECU fingerprinting](concepts/in-vehicle-intrusion-detection.md) — Detects in-vehicle anomalies via timing, skew, voltage or learned models.
- **IVI** — In-Vehicle Infotainment. See [IVI runtime privilege and service exposure](concepts/ivi-runtime-privilege.md) — The head unit and the apps/services it hosts.
- **OTA** — Over-the-Air update. See [Secure firmware updates (Uptane)](concepts/secure-firmware-updates.md) — Remote software delivery; Uptane is the reference design for securing it.
- **Uptane** — A compromise-resilient update framework. See [Secure firmware updates (Uptane)](concepts/secure-firmware-updates.md) — Two repositories and per-vehicle signed instructions for automotive OTA.
- **TARA** — Threat Analysis and Risk Assessment. See [TARA methodology: the ISO/SAE 21434 artefact chain](concepts/tara-methodology.md) — The ISO/SAE 21434 artefact chain from item definition to risk treatment.
- **ISO/SAE 21434** — Road vehicles — Cybersecurity engineering. See [TARA methodology: the ISO/SAE 21434 artefact chain](concepts/tara-methodology.md) — The process standard whose artefacts a TARA produces.
- **UNECE R155** — UN regulation on vehicle cybersecurity. See [Automotive Cybersecurity: An Introduction to ISO/SAE 21434](automotive-cybersecurity-an-introduction-to-iso-sae-21434.md) — Requires a certified CSMS for type approval in many markets.
- **OCPP** — Open Charge Point Protocol. See [OCPP and charging attacks](concepts/ocpp-charging-attacks.md) — Links chargers to backends; weak transport and shared identities enable fraud.
- **ISO 15118** — Vehicle-to-Grid communication interface. See [The EV–EVSE charging trust chain (ISO 15118 / DIN 70121)](concepts/charging-trust-chain.md) — The EV–EVSE protocol behind Plug & Charge.
- **DIN 70121** — German DC charging communication profile. See [The EV–EVSE charging trust chain (ISO 15118 / DIN 70121)](concepts/charging-trust-chain.md) — The predecessor profile to ISO 15118 for DC charging.
- **V2G** — Vehicle-to-Grid. See [OpenV2G](openv2g.md) — Bidirectional energy and communication between vehicle and charger.
- **CCS** — Combined Charging System. See [The EV–EVSE charging trust chain (ISO 15118 / DIN 70121)](concepts/charging-trust-chain.md) — The dominant DC charging connector and communication stack.
- **V2X** — Vehicle-to-Everything. See [V2X credential management](concepts/v2x-credential-management.md) — Vehicle communication with other vehicles, infrastructure and pedestrians.
- **SCMS** — Security Credential Management System. See [V2X credential management](concepts/v2x-credential-management.md) — The US split-knowledge issuer of pseudonymous V2X tickets.
- **CCMS** — Cooperative Credential Management System. See [V2X credential management](concepts/v2x-credential-management.md) — The European equivalent of the SCMS.
- **RKE / PKE** — Remote / Passive Keyless Entry. See [Key-fob relay attacks](concepts/key-fob-relay-attacks.md) — The fob-to-car link targeted by relay and rolling-code attacks.
- **Rolling code** — A hopping code tied to receiver counter state. See [Rolling-code failure classes](concepts/rolling-code-failure-classes.md) — Trust lives in the counter's state, so attacks target windows, resync and blocking.
- **TPMS** — Tire Pressure Monitoring System. See [Security and Privacy Vulnerabilities of In-Car Wireless Networks: A Tire Pressure Monitoring System Case Study](security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study.md) — A wireless sensor network inside the vehicle with its own attack surface.
- **SIL / HIL** — Software-/Hardware-in-the-Loop. See [Simulation and test doubles for vehicle networks](concepts/simulation-and-test-doubles.md) — Simulation rungs that trade physical fidelity for repeatability.
- **OEM** — Original Equipment Manufacturer. See [IVI update-path trust](concepts/ivi-update-trust.md) — The vehicle maker; Tier-1 suppliers build many of the components.
