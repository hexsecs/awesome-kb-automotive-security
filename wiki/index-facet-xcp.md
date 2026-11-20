# Facet: XCP / A2L

Measurement and calibration, XCP and A2L description files.

Generated from page frontmatter by tools/ingest.py; 10 pages (entities and concepts). Do not edit by hand.

## CAN Bus Analysis

- [CanLab](canlab.md) — PyQt6 desktop application for offline CAN capture reverse engineering, combining automated counter and checksum detection with entropy-based signal boundary…
- [pycangui](pycangui.md) — Graphical CAN bus tool with live trace and plots, transmit, CANopen, UDS, J1939, and XCP/CCP support on any python-can adapter, with Python scripting and…

## Diagnostic Tools

- [Atlas](atlas.md) — Open-source ECU calibration application for reverse engineering and recalibrating Subaru, Toyota, and Honda ECUs, with an integrated Ghidra bundle for…

## Firmware and ECU Reverse Engineering

- [pyA2L](pya2l.md) — Python parser for ASAM MCD-2 MC (A2L) description files, exposing the characteristic, measurement, and memory-layout metadata needed to make sense of ECU…
- [pyXCP](pyxcp.md) — Python implementation of the ASAM MCD-1 XCP protocol over CAN, Ethernet, and USB, with seed-and-key access handling, for measuring, calibrating, and…

## Penetration Testing

- [AutoFuze](autofuze.md) — Python toolkit for fuzzing and penetration testing ECUs over UDS, XCP, SOME/IP, and OBD, across CAN, DoIP, USB, and SPI transports.

## Datasets

- [Cross-Vehicle Generalisation Benchmark](cross-vehicle-generalisation-benchmark.md) — Leave-one-vehicle-out benchmark unifying ROAD, CIDv2, and can-train-and-test into 217 captures across eight vehicles for evaluating whether CAN IDS models…

## Related Awesome Lists

- [Awesome EV Charging](awesome-ev-charging.md) — Curated specifications, tools, and resources for EV charging protocols including OCPP, ISO 15118, OCPI, and Eichrecht.

## Concepts

- [Firmware acquisition: the read-side channels](concepts/firmware-acquisition.md) — Before analysis comes acquisition: the channels the corpus documents for getting an ECU's image out — by bus, by bootstrap, by bench, by log, by package.
- [The calibration plane (XCP/A2L)](concepts/calibration-plane.md) — Beside diagnostics sits a second access plane into production ECUs: XCP's direct memory access and the A2L maps that name everything it can touch.
