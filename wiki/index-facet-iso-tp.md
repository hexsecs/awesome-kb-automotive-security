# Facet: ISO-TP

ISO 15765-2 transport, segmentation and flow control.

Generated from page frontmatter by tools/ingest.py; 8 pages (entities and concepts). Do not edit by hand.

## CAN Bus Analysis

- [python-can-isotp](python-can-isotp.md) — ISO-TP (ISO 15765) transport for Python on top of python-can or Linux SocketCAN, the segmentation layer that UDS and OBD-II diagnostics run over.

## Diagnostic Tools

- [doip-sim-ecu-dsl](doip-sim-ecu-dsl.md) — Kotlin DSL for scripting simulated DoIP ECUs, reachable over Ethernet, CAN with ISO-TP, or both at once, for exercising diagnostic clients against UDS error…
- [gallia](gallia.md) — Extendable automotive pentesting framework from Fraunhofer AISEC focused on UDS, with DoIP and ISO-TP transports and structured logging for reproducible scans.
- [iso14229](iso14229.md) — Dependency-free C implementation of a UDS (ISO 14229) server and client with built-in ISO-TP, for building embedded ECU targets and test tools.

## Hardware Interfaces

- [CANtact](cantact.md) — Open-source hardware CAN interface and desktop app supporting live tracing, frame transmission, ISO-TP, JavaScript scripting, and candump-format traces.

## Conference Presentations

- [The Vehicle May Be Sick: Denial of Diagnostic Services by Exploiting the CAN Transport Protocol](the-vehicle-may-be-sick-denial-of-diagnostic-services-by-exploiting-the-can-transport-protocol.md) — Baek, Jeong, and Kim, escar USA 2026. Presents eight ISO-TP attack scenarios that deny or manipulate diagnostic services, validated against aftermarket and…

## Learning Resources

- [Automotive Cybersecurity Roadmap](automotive-cybersecurity-roadmap.md) — Structured learning path from CAN and UDS fundamentals through TARA, firmware reverse engineering, and hardware hacking into specialized career tracks.

## Concepts

- [ISO-TP: the stateful transport under diagnostics](concepts/iso-tp.md) — ISO 15765-2 reassembles multi-frame diagnostic payloads on CAN; its flow-control state machine is an attacker-controllable resource.
