# Facet: Diagnostics

UDS, OBD, KWP, SecurityAccess and diagnostic services.

Generated from page frontmatter by tools/ingest.py; 57 pages. Do not edit by hand.

## CAN Bus Analysis

- [CANExplorer](canexplorer.md) — Cross-platform CAN, CAN FD, and LIN analysis GUI with reverse-engineering tools, UDS discovery and fuzzing, DoIP and SOME/IP support, and SecOC decoding.
- [CANalyzat0r](canalyzat0r.md) — Security analysis toolkit for proprietary car protocols with graphical sniffing, fuzzing, packet comparison, background-noise filtering, and UDS fuzzing.
- [CANarchy](canarchy.md) — Stream-first CAN and J1939 toolkit that emits structured JSONL for automation, with live capture, DBC/ARXML/KCD decoding, J1939 PGN/SPN and DM1 fault…
- [CanCat](cancat.md) — Firmware for Arduino CAN shields and Macchina M2 boards paired with a Python client for sniffing and injecting CAN traffic, running UDS and CCP sessions…
- [CanLab](canlab.md) — PyQt6 desktop application for offline CAN capture reverse engineering, combining automated counter and checksum detection with entropy-based signal boundary…
- [OBDium](obdium.md) — Rust-based OBD-II diagnostic tool with modern Tauri GUI supporting live data, DTC analysis, and offline VIN decoding.
- [SavvyCAN](savvycan.md) — Cross-platform Qt-based CAN bus reverse engineering and capture tool with DBC file loading, UDS scanning, and fuzzing support.
- [cantools](cantools.md) — Python library for CAN bus diagnostics, DBC parsing, and message decoding/encoding.
- [pycangui](pycangui.md) — Graphical CAN bus tool with live trace and plots, transmit, CANopen, UDS, J1939, and XCP/CCP support on any python-can adapter, with Python scripting and…
- [python-can-isotp](python-can-isotp.md) — ISO-TP (ISO 15765) transport for Python on top of python-can or Linux SocketCAN, the segmentation layer that UDS and OBD-II diagnostics run over.

## Diagnostic Tools

- [AutoPi](autopi.md) — Open-source core software for the AutoPi dongle, a Raspberry Pi-based OBD-II device for vehicle diagnostics, CAN bus data collection, and automotive IoT…
- [EcuBus-Pro](ecubus-pro.md) — Cross-platform open-source ECU tool with UDS, CAN-TP, DoIP, LIN, and SOME/IP support, DBC and LDF databases, TypeScript scripting in the style of CAPL, and…
- [Ford-ECU-Bruteforcer](ford-ecu-bruteforcer.md) — Security access brute-force tool for pre-2011 Ford ECUs with 3-byte seed and 5-byte key.
- [OpenSOVD Classic Diagnostic Adapter](opensovd-classic-diagnostic-adapter.md) — Eclipse OpenSOVD bridge in Rust that translates SOVD (ISO 17978) requests into UDS over DoIP for legacy ECUs, with a security plugin architecture.
- [OpenVehicleDiag](openvehiclediag.md) — Rust ECU diagnostics and reprogramming application over J2534 pass-through adapters and Linux SocketCAN, with UDS and KWP2000 sessions and a converter that…
- [UDSim](udsim.md) — UDS (Unified Diagnostic Services) ECU simulator and fuzzer for discovering and testing UDS services.
- [UnlockECU](unlockecu.md) — Free seed-key unlocking tool for Bosch, Continental, Delphi, Daimler, and Marquardt ECUs without proprietary DLLs.
- [VW_Flash](vw-flash.md) — Flashing tools for VW AG control units over UDS supporting Simos18.1/6/10 and DQ250-MQB.
- [conescan](conescan.md) — Automotive ECU hacking supertool for firmware dumping and manipulation via J2534 OBD interfaces.
- [doip-sim-ecu-dsl](doip-sim-ecu-dsl.md) — Kotlin DSL for scripting simulated DoIP ECUs, reachable over Ethernet, CAN with ISO-TP, or both at once, for exercising diagnostic clients against UDS error…
- [gallia](gallia.md) — Extendable automotive pentesting framework from Fraunhofer AISEC focused on UDS, with DoIP and ISO-TP transports and structured logging for reproducible scans.
- [iso14229](iso14229.md) — Dependency-free C implementation of a UDS (ISO 14229) server and client with built-in ISO-TP, for building embedded ECU targets and test tools.
- [odxtools](odxtools.md) — Python toolkit for parsing ODX/PDX (ISO 22901) diagnostic databases and encoding, decoding, and snooping ECU diagnostic sessions.
- [pq-flasher](pq-flasher.md) — Python tools for reflashing VW PQ35 EPS using TP 2.0 transport layer and KWP2000 diagnostics.
- [python-doipclient](python-doipclient.md) — Pure Python DoIP (ISO 13400) client that plugs into udsoncan as a transport layer for diagnostics over automotive Ethernet.
- [uds-firmware-extraction](uds-firmware-extraction.md) — Tool for extracting ECU firmware from UDS flash traffic following ISO-14229 standard.
- [uds-server](uds-server.md) — UDS ECU simulator and fuzzer for use alongside ICSim, for practising diagnostic command discovery and fuzzing scan tools.
- [uds](uds.md) — Python package for ISO 14229 UDS in both client and server roles over CAN, Ethernet, LIN, FlexRay, and K-Line, usable for simulation, testing, and decoding…
- [udsoncan](udsoncan.md) — Python implementation of the ISO 14229 UDS protocol covering session control, security access, data identifiers, and routine control.

## Firmware and ECU Reverse Engineering

- [Simos18_SBOOT](simos18-sboot.md) — Documented exploit chain against the VW Simos18 supplier bootloader, chaining PWM entry, a weak Mersenne Twister seed/key, and a CRC bounds-check flaw into…
- [Zephyr-Reference-ECU](zephyr-reference-ecu.md) — Forkable body control module on Zephyr with UDS diagnostics over CAN and DoIP, SecurityAccess with AES-128-CMAC, and signed firmware update, runnable with…

## Automotive Ethernet

- [ProtoCrawler](protocrawler.md) — Intelligent protocol fuzzer for SOME/IP, DoIP, UDS, and Ethernet AVB satisfying ISO/SAE 21434 testing requirements.

## Infotainment and IVI

- [MMI3G-Toolkit](mmi3g-toolkit.md) — SD-card-based toolkit for Audi/VW MMI3G head units covering boot-image extraction, reverse-engineered GEMMI protocol details, and an FSC signature-bypass…

## Penetration Testing

- [AutoFuze](autofuze.md) — Python toolkit for fuzzing and penetration testing ECUs over UDS, XCP, SOME/IP, and OBD, across CAN, DoIP, USB, and SPI transports.
- [DongleScope](donglescope.md) — Automated tool for detecting vulnerabilities in wireless OBD-II dongles based on USENIX Security 2020 research.
- [NullSec CarFuzz](nullsec-carfuzz.md) — Rust fuzzer for CAN, UDS, OBD-II, and DoIP with grammar-aware test generation and coverage tracking.
- [automotive-security-research](automotive-security-research.md) — Published reverse engineering results for two production vehicles including CAN matrices, extracted ECU security access keys, and UDS scanning…
- [pwnobd](pwnobd.md) — Offensive cybersecurity toolkit for vulnerability analysis of OBD-II devices presented at Black Hat Europe 2024.

## Datasets

- [AutoHack](autohack.md) — Multi-bus CAN dataset from a real vehicle covering C-CAN, P-CAN, and B-CAN, with physically verified fuzzing, spoofing, replay, DoS, and UDS-based attacks.
- [Cross-Vehicle Generalisation Benchmark](cross-vehicle-generalisation-benchmark.md) — Leave-one-vehicle-out benchmark unifying ROAD, CIDv2, and can-train-and-test into 217 captures across eight vehicles for evaluating whether CAN IDS models…

## Research Papers

- [Beneath the Bonnet: A Breakdown of Diagnostic Security](beneath-the-bonnet-a-breakdown-of-diagnostic-security.md) — Van den Herrewegen and Garcia, ESORICS 2018. Reverse engineers the seed-key ciphers of four manufacturers from ECU firmware and achieves remote code…
- [Fast and Vulnerable: A Story of Telematic Failures](fast-and-vulnerable-a-story-of-telematic-failures.md) — Foster, Prudhomme, Koscher, and Savage, USENIX WOOT 2015. Shows an aftermarket OBD-II telematics dongle exposing SMS-reachable remote control of vehicle CAN…
- [Plug-N-Pwned: Comprehensive Vulnerability Analysis of OBD-II Dongles](plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles.md) — Wen, Chen, and Lin, USENIX Security 2020. Automated analysis of 77 wireless OBD-II dongles, every one of which exposed at least two vulnerability classes.

## Conference Presentations

- [Automotive Flash Bootloaders: Exposing Automotive ECU Updates](automotive-flash-bootloaders-exposing-automotive-ecu-updates.md) — Lapczynski, DEF CON 26 Car Hacking Village 2018. Walks through how UDS programming sessions, seed-key exchange, and flash routines expose ECU firmware…
- [Back-connect to the Connected Car. Search for Vulnerabilities in the VW Electric Car.](back-connect-to-the-connected-car-search-for-vulnerabilities-in-the-vw-electric-car.md) — Serdyuk, Kondikov, Razmakhnin, and Sakr, Black Hat Europe 2022. Maps the attack surface of the VW ID.3 across Wi-Fi, Bluetooth, V2X, cellular, CAN, and…
- [CANdid: A Stealthy Stepping-Stone Attack to Bypass Authentication on ECUs](candid-a-stealthy-stepping-stone-attack-to-bypass-authentication-on-ecus.md) — Kulandaivel, Jain, Guajardo, and Sekar, escar USA 2022. Shows a compromised ECU can authenticate against a safety-critical ECU's SecurityAccess without the…
- [Fast and Compromised: Automotive Security on a Timer](fast-and-compromised-automotive-security-on-a-timer.md) — Ziv and Alfasi, escar USA 2025. Penetration test taking a production electric vehicle from an insecure Wi-Fi network to full compromise in eight working…
- [The Vehicle May Be Sick: Denial of Diagnostic Services by Exploiting the CAN Transport Protocol](the-vehicle-may-be-sick-denial-of-diagnostic-services-by-exploiting-the-can-transport-protocol.md) — Baek, Jeong, and Kim, escar USA 2026. Presents eight ISO-TP attack scenarios that deny or manipulate diagnostic services, validated against aftermarket and…
- [Vehicle Immobilization Revisited](vehicle-immobilization-revisited.md) — Bokslag, 36C3 2019. Studies three vehicles and shows the immobilizer transponder talks to the body control module rather than the ECM, so weak…

## Learning Resources

- [Automotive Cybersecurity Roadmap](automotive-cybersecurity-roadmap.md) — Structured learning path from CAN and UDS fundamentals through TARA, firmware reverse engineering, and hardware hacking into specialized career tracks.

## Related Awesome Lists

- [Awesome CANb IDs](awesome-canb-ids.md) — CAN bus ID reference and documentation.

## Concepts

- [Diagnostic-service abuse](concepts/diagnostic-service-abuse.md) — The diagnostic service set is the highest-privilege surface on the vehicle network: what it actuates, how its gates fail, and the one case where they held.
- [DoIP moves diagnostics onto the network](concepts/doip.md) — DoIP replaces the physical OBD port with a routable endpoint; discovery and routing activation become the new trust boundary.
- [ISO-TP: the stateful transport under diagnostics](concepts/iso-tp.md) — ISO 15765-2 reassembles multi-frame diagnostic payloads on CAN; its flow-control state machine is an attacker-controllable resource.
- [Protocol-aware diagnostic fuzzing](concepts/diagnostic-fuzzing.md) — Fuzzing reaches the deep diagnostic states only when generation is grammar- and state-aware: sessions and SecurityAccess are the fuzzer's real problem.
- [The calibration plane (XCP/A2L)](concepts/calibration-plane.md) — Beside diagnostics sits a second access plane into production ECUs: XCP's direct memory access and the A2L maps that name everything it can touch.
- [UDS seed/key (SecurityAccess)](concepts/uds-seed-key.md) — UDS SecurityAccess (0x27) gates privileged diagnostics behind a seed/key exchange; weak seeds, reused secrets and simple algorithms defeat it.
