# Facet: Hardware

Debug ports, boards, adapters and bench interfaces.

Generated from page frontmatter by tools/ingest.py; 11 pages (entities and concepts). Do not edit by hand.

## CAN Bus Analysis

- [CANgaroo](cangaroo.md) — Open-source CAN bus analyzer for Linux and Windows with DBC and LDF decoding, CAN FD, Python scripting, SocketCAN, PEAK, Kvaser, Vector, and candlelight…

## Infotainment and IVI

- [idrive7-8-ssh-root](idrive7-8-ssh-root.md) — Enable root SSH on BMW iDrive 7/8 MGU head units over ENET via debug image flash and persistent SSH without B7F8E5 DTC, for head unit reverse engineering.

## Hardware Interfaces

- [CANtact](cantact.md) — Open-source hardware CAN interface and desktop app supporting live tracing, frame transmission, ISO-TP, JavaScript scripting, and candump-format traces.
- [candleLight_fw](candlelight-fw.md) — Open firmware for low-cost STM32 USB to CAN adapters such as CANable, cantact, and candleLight that implements the mainline Linux gs_usb interface, turning…
- [panda](panda.md) — Open-source CAN and CAN FD interface firmware from comma.ai running on an STM32H725, with Python bindings for full read/write access to vehicle buses.

## Penetration Testing

- [SecOC Key Extractor](secoc-key-extractor.md) — Scripts to extract SecOC (Secure On-Board Communication) keys from Toyota vehicles using comma.ai panda hardware.

## Conference Presentations

- [Abusing CAN Bus Protocol Specification for Denial of Service in Embedded Systems](abusing-can-bus-protocol-specification-for-denial-of-service-in-embedded-systems.md) — Petran, DEF CON 31 Car Hacking Village 2023. Shows how an out-of-range CAN data length code reaches firmware unchecked and overflows a buffer, demonstrated…
- [Vehicle Immobilization Revisited](vehicle-immobilization-revisited.md) — Bokslag, 36C3 2019. Studies three vehicles and shows the immobilizer transponder talks to the body control module rather than the ECM, so weak…

## Learning Resources

- [Bypassing Debug Password Protection on the RH850 Family](bypassing-debug-password-protection-on-the-rh850-family.md) — Quarkslab walkthrough of defeating the 16-byte IDCODE debug lock on Renesas RH850 ECU microcontrollers with crowbar voltage glitching, using a ChipWhisperer…

## Related Awesome Lists

- [Awesome Embedded Security](awesome-embedded-security.md) — Tools and knowledge for embedded security research.

## Concepts

- [IVI runtime privilege and service exposure](concepts/ivi-runtime-privilege.md) — The head unit's failures that are not on the update path: declared-but-unenforced permissions, unchecked service callers, and designed-in debug surfaces.
