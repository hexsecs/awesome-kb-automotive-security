# Facet: Standards & specs

ISO, SAE, AUTOSAR, UNECE and published specifications.

Generated from page frontmatter by tools/ingest.py; 48 pages. Do not edit by hand.

## CAN Bus Analysis

- [pretty_j1939](pretty-j1939.md) — NMFTA's Python library and CLI that decodes J1939 traffic from candump logs using the SAE J1939 Digital Annex, with transport protocol reassembly…
- [python-can-isotp](python-can-isotp.md) — ISO-TP (ISO 15765) transport for Python on top of python-can or Linux SocketCAN, the segmentation layer that UDS and OBD-II diagnostics run over.

## Diagnostic Tools

- [OpenSOVD Classic Diagnostic Adapter](opensovd-classic-diagnostic-adapter.md) — Eclipse OpenSOVD bridge in Rust that translates SOVD (ISO 17978) requests into UDS over DoIP for legacy ECUs, with a security plugin architecture.
- [iso14229](iso14229.md) — Dependency-free C implementation of a UDS (ISO 14229) server and client with built-in ISO-TP, for building embedded ECU targets and test tools.
- [odxtools](odxtools.md) — Python toolkit for parsing ODX/PDX (ISO 22901) diagnostic databases and encoding, decoding, and snooping ECU diagnostic sessions.
- [python-doipclient](python-doipclient.md) — Pure Python DoIP (ISO 13400) client that plugs into udsoncan as a transport layer for diagnostics over automotive Ethernet.
- [uds-firmware-extraction](uds-firmware-extraction.md) — Tool for extracting ECU firmware from UDS flash traffic following ISO-14229 standard.
- [uds](uds.md) — Python package for ISO 14229 UDS in both client and server roles over CAN, Ethernet, LIN, FlexRay, and K-Line, usable for simulation, testing, and decoding…
- [udsoncan](udsoncan.md) — Python implementation of the ISO 14229 UDS protocol covering session control, security access, data identifiers, and routine control.

## Firmware and ECU Reverse Engineering

- [ghidra-tc1797](ghidra-tc1797.md) — Ghidra processor specification and language definitions for the Infineon TriCore TC1797, used to label memory regions when disassembling MED17 and similar…

## Automotive Ethernet

- [ProtoCrawler](protocrawler.md) — Intelligent protocol fuzzer for SOME/IP, DoIP, UDS, and Ethernet AVB satisfying ISO/SAE 21434 testing requirements.
- [Scapy](scapy.md) — Python packet manipulation library with support for DoIP, SOME/IP, AUTOSAR PDUs, SecOC, CAN-FD, and FlexRay protocols.
- [eth-ws-someip](eth-ws-someip.md) — Wireshark LUA dissectors for Automotive Ethernet SOME/IP and SOME/IP-SD protocols (Autosar 4.2).

## EV Charging Security

- [ChargeSploit](chargesploit.md) — Security testing framework for ISO 15118-2 and DIN SPEC 70121 that emulates either the charger or the vehicle, with TLS support and extensible handlers for…
- [EVerest](everest.md) — Linux Foundation Energy full-stack open-source EV charging firmware implementing OCPP 1.6/2.0.1/2.1, ISO 15118-2/-3/-20, IEC 61851, and DIN SPEC 70121…
- [OCPPuzz](ocppuzz.md) — Specification-driven fuzzer for OCPP charging station management systems that extracts message rules and state transitions from the specification with a…
- [OpenV2G](openv2g.md) — C implementation of the ISO 15118 and DIN 70121 vehicle-to-grid interface with an EXI codec, widely reused as the encoding engine behind other V2G analysis…
- [V2Gdecoder](v2gdecoder.md) — Encodes and decodes EXI-compressed V2G messages on the fly, turning captured ISO 15118 exchanges into editable XML for replay and fuzzing.
- [WWCP_ISO15118](wwcp-iso15118.md) — ISO 15118 implementation covering SLAC, SDP, V2GTP, -2 and -20, explicitly shipping attack vectors and penetration-testing workflows for the individual…
- [dsV2Gshark](dsv2gshark.md) — Wireshark plugin that dissects ISO 15118 and DIN 70121 traffic, decoding EXI-encoded V2G payloads and SLAC handshakes into readable fields.
- [pyPLC](pyplc.md) — Python toolkit for CCS charging research that can pose as vehicle or charger, sniff HomePlug Green PHY traffic, and walk the SLAC, DIN 70121, and ISO 15118…

## Security Analysis

- [AVCDL](avcdl.md) — Motional's open-sourced Versatile Cybersecurity Development Lifecycle with process definitions and templates mapped to ISO/SAE 21434, ISO 24089, and UN…
- [AutoTARA](autotara.md) — Web-based TARA (Threat Analysis and Risk Assessment) framework for ISO/SAE 21434 that models systems as attack graphs and applies MITRE's CTSA/CRRA…
- [Security AutoDesigner](security-autodesigner.md) — Automated TARA platform for creating ISO 21434 and UNR 155 compliant threat analysis reports.

## Research Papers

- [Automating Function-Level TARA for Automotive Full-Lifecycle Security](automating-function-level-tara-for-automotive-full-lifecycle-security.md) — Yang et al., NDSS 2026. DefenseWeaver, a multi-agent LLM system that automates function-level ISO/SAE 21434 threat analysis and risk assessment, reported as…
- [Charge It to My Neighbor: A Relay Attack on ISO 15118 Plug and Charge Payment](charge-it-to-my-neighbor-a-relay-attack-on-iso-15118-plug-and-charge-payment.md) — Löw et al., USENIX VehicleSec 2026. Relays Plug and Charge authentication so the attacker charges their own car while the victim is billed, exploiting…
- [Losing the Car Keys: Wireless PHY-Layer Insecurity in EV Charging](losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging.md) — Baker and Martinovic, USENIX Security 2019. Recovers ISO 15118 charging messages from the unintentional wireless emissions of CCS power-line communication…

## Conference Presentations

- [Abusing CAN Bus Protocol Specification for Denial of Service in Embedded Systems](abusing-can-bus-protocol-specification-for-denial-of-service-in-embedded-systems.md) — Petran, DEF CON 31 Car Hacking Village 2023. Shows how an out-of-range CAN data length code reaches firmware unchecked and overflows a buffer, demonstrated…
- [Expanding the Attack Scenarios of SAE J1939: A Comprehensive Analysis of Established and Novel Vulnerabilities in Transport Protocol](expanding-the-attack-scenarios-of-sae-j1939-a-comprehensive-analysis-of-established-and-novel-vulnerabilities-in-transport-protocol.md) — Lee, Lee, Jun, and Kim, escar USA 2024. Presents 14 attack scenarios against the J1939 protocol used in commercial vehicles, seven of them new.
- [One Modem to Brick Them All: Exploiting Vulnerabilities in the EV Charging Communication](one-modem-to-brick-them-all-exploiting-vulnerabilities-in-the-ev-charging-communication.md) — Berens, Szakaly, and Kohler, DEF CON 33 Car Hacking Village 2025. Slides on attacking the CCS charging communication modem, from the authors of the USENIX…

## Books

- [A Comprehensible Guide to Controller Area Network](a-comprehensible-guide-to-controller-area-network.md) — Wilfried Voss, Copperhill 2005. The standard plain-language reference on CAN itself, covering frame formats, arbitration, error handling, and timing that…
- [Automotive Cyber Security](automotive-cyber-security.md) — Shiho Kim and Rakesh Shrestha, Springer 2020. Academic introduction to connected and autonomous vehicle security, threats, and the standardisation landscape.
- [Automotive Cybersecurity Engineering Handbook](automotive-cybersecurity-engineering-handbook.md) — Ahmad MK Nasser, Packt 2023. Practitioner's guide to building cyber-resilient vehicles, covering threat analysis, hardware security, and ISO/SAE 21434…
- [Automotive Cybersecurity: An Introduction to ISO/SAE 21434](automotive-cybersecurity-an-introduction-to-iso-sae-21434.md) — David Ward and Paul Wooderson, SAE International 2021. Short introduction to ISO/SAE 21434 covering cybersecurity basics, setting up a company process, and…
- [Automotive Cybersecurity: Protecting Connected and Autonomous Vehicles](automotive-cybersecurity-protecting-connected-and-autonomous-vehicles.md) — Alfred Basta and Sam Hana, Kendall Hunt 2026. Textbook covering threats from ECU networks and sensor spoofing to OTA patching, EV charging breaches, and…
- [Automotive Threat Analysis and Risk Assessment in Practice](automotive-threat-analysis-and-risk-assessment-in-practice.md) — Rodrigo do Carmo and Alexander Schlensog, Springer 2024. Practitioner's guide to threat analysis and risk assessment (TARA) following ISO/SAE 21434, with…
- [Cybersecurity for Commercial Vehicles](cybersecurity-for-commercial-vehicles.md) — Gloria D'Anna, SAE International 2018. Covers heavy vehicle and fleet security, how it differs from passenger cars, SAE J3061, platooning, and breach forensics.

## Learning Resources

- [Automotive Cybersecurity Roadmap](automotive-cybersecurity-roadmap.md) — Structured learning path from CAN and UDS fundamentals through TARA, firmware reverse engineering, and hardware hacking into specialized career tracks.
- [Automotive-Networking-Security](automotive-networking-security.md) — Automotive networking security standards and solutions overview.
- [OWASP Automotive Security Cheat Sheet](owasp-automotive-security-cheat-sheet.md) — OWASP cheat sheet covering threat modeling, message authentication, secure boot, and update verification for vehicle ECUs and connected services.

## Related Awesome Lists

- [Awesome EV Charging](awesome-ev-charging.md) — Curated specifications, tools, and resources for EV charging protocols including OCPP, ISO 15118, OCPI, and Eichrecht.

## Concepts

- [DoIP moves diagnostics onto the network](concepts/doip.md) — DoIP replaces the physical OBD port with a routable endpoint; discovery and routing activation become the new trust boundary.
- [ISO-TP: the stateful transport under diagnostics](concepts/iso-tp.md) — ISO 15765-2 reassembles multi-frame diagnostic payloads on CAN; its flow-control state machine is an attacker-controllable resource.
- [J1939 transport security](concepts/j1939.md) — Heavy-vehicle J1939 has its own request and transport semantics; TP.CM/TP.DT state is attackable in ways generic CAN IDS misses.
- [SOME/IP and SOME/IP-SD](concepts/someip.md) — AUTOSAR's service-oriented middleware over IP: how services are offered, found and invoked — and why discovery is the trust root of every SOME/IP conversation.
- [TARA methodology: the ISO/SAE 21434 artefact chain](concepts/tara-methodology.md) — How an automotive TARA is actually assembled: the ISO/SAE 21434 artefact chain, the layers the KB's tools occupy, and where automation helps and lies.
- [The EV–EVSE charging trust chain (ISO 15118 / DIN 70121)](concepts/charging-trust-chain.md) — The vehicle–charger link's trust is a chain — association, transport, contract authorisation — whose links fail independently and are measured failing.
- [UDS seed/key (SecurityAccess)](concepts/uds-seed-key.md) — UDS SecurityAccess (0x27) gates privileged diagnostics behind a seed/key exchange; weak seeds, reused secrets and simple algorithms defeat it.
