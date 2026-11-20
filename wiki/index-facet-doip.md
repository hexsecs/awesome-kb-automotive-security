# Facet: DoIP

Diagnostics over IP and its discovery/routing boundary.

Generated from page frontmatter by tools/ingest.py; 14 pages (entities and concepts). Do not edit by hand.

## CAN Bus Analysis

- [CANExplorer](canexplorer.md) — Cross-platform CAN, CAN FD, and LIN analysis GUI with reverse-engineering tools, UDS discovery and fuzzing, DoIP and SOME/IP support, and SecOC decoding.
- [CANarchy](canarchy.md) — Stream-first CAN and J1939 toolkit that emits structured JSONL for automation, with live capture, DBC/ARXML/KCD decoding, J1939 PGN/SPN and DM1 fault…
- [CanLab](canlab.md) — PyQt6 desktop application for offline CAN capture reverse engineering, combining automated counter and checksum detection with entropy-based signal boundary…

## Diagnostic Tools

- [EcuBus-Pro](ecubus-pro.md) — Cross-platform open-source ECU tool with UDS, CAN-TP, DoIP, LIN, and SOME/IP support, DBC and LDF databases, TypeScript scripting in the style of CAPL, and…
- [OpenSOVD Classic Diagnostic Adapter](opensovd-classic-diagnostic-adapter.md) — Eclipse OpenSOVD bridge in Rust that translates SOVD (ISO 17978) requests into UDS over DoIP for legacy ECUs, with a security plugin architecture.
- [doip-sim-ecu-dsl](doip-sim-ecu-dsl.md) — Kotlin DSL for scripting simulated DoIP ECUs, reachable over Ethernet, CAN with ISO-TP, or both at once, for exercising diagnostic clients against UDS error…
- [gallia](gallia.md) — Extendable automotive pentesting framework from Fraunhofer AISEC focused on UDS, with DoIP and ISO-TP transports and structured logging for reproducible scans.
- [python-doipclient](python-doipclient.md) — Pure Python DoIP (ISO 13400) client that plugs into udsoncan as a transport layer for diagnostics over automotive Ethernet.

## Firmware and ECU Reverse Engineering

- [Zephyr-Reference-ECU](zephyr-reference-ecu.md) — Forkable body control module on Zephyr with UDS diagnostics over CAN and DoIP, SecurityAccess with AES-128-CMAC, and signed firmware update, runnable with…

## Automotive Ethernet

- [ProtoCrawler](protocrawler.md) — Intelligent protocol fuzzer for SOME/IP, DoIP, UDS, and Ethernet AVB satisfying ISO/SAE 21434 testing requirements.
- [Scapy](scapy.md) — Python packet manipulation library with support for DoIP, SOME/IP, AUTOSAR PDUs, SecOC, CAN-FD, and FlexRay protocols.

## Penetration Testing

- [AutoFuze](autofuze.md) — Python toolkit for fuzzing and penetration testing ECUs over UDS, XCP, SOME/IP, and OBD, across CAN, DoIP, USB, and SPI transports.
- [NullSec CarFuzz](nullsec-carfuzz.md) — Rust fuzzer for CAN, UDS, OBD-II, and DoIP with grammar-aware test generation and coverage tracking.

## Concepts

- [DoIP moves diagnostics onto the network](concepts/doip.md) — DoIP replaces the physical OBD port with a routable endpoint; discovery and routing activation become the new trust boundary.
