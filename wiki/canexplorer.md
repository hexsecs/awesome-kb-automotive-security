---
uid: 01a1bfa1-b3b0-7ecc-85ee-6561d00cb2bb
title: "CANExplorer"
summary: "Cross-platform CAN, CAN FD, and LIN analysis GUI with reverse-engineering tools, UDS discovery and fuzzing, DoIP and SOME/IP support, and SecOC decoding."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/AKJ7/CANExplorer"
status: active
last_checked: 2026-11-17
created: 2026-11-09
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 40ccbae
list_summary: "Cross-platform CAN, CAN FD, and LIN analysis GUI with reverse-engineering tools, UDS discovery and fuzzing, DoIP and SOME/IP support, and SecOC decoding."
related:
  - ecubus-pro
  - savvycan
  - automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps
  - uds
  - autofuze
  - scapy
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-09
  - url: "https://github.com/AKJ7/CANExplorer"
    retrieved: 2026-11-17
  - url: "https://raw.githubusercontent.com/AKJ7/CANExplorer/master/README.md"
    retrieved: 2026-11-17
  - url: "https://api.github.com/repos/AKJ7/CANExplorer"
    retrieved: 2026-11-17
---

Cross-platform CAN, CAN FD, and LIN analysis GUI with reverse-engineering tools, UDS discovery and fuzzing, DoIP and SOME/IP support, and SecOC decoding.

## What it is

CANExplorer is a Python Qt/QML desktop workbench for monitoring, analysing, diagnosing, simulating and testing vehicle buses. Its core (`can_explorer/core`) is Qt-independent asyncio code with a QML GUI adapter, and it runs on any interface supported by python-can 4.6 — or with no hardware on a virtual bus. The project is MIT-licensed, distributes Windows installers, Linux AppImage/`.deb`/snap and a macOS Apple-silicon `.dmg`, and had 180 stars at this check.

## How it works

The upstream README documents a deliberately broad stack:

- **Trace and reverse engineering** — live view with bus load, error frames and busiest IDs; per-ID cycle times and changed-byte highlighting; bit and byte statistics; automatic detection of counters, checksums and multiplexers; matching fields against DBC signals, CSV/GPS logs or polled OBD-II values; frame-interval and per-byte timing plots. Frames older than a threshold are paged to disk for million-frame sessions.
- **Recording and replay** — ASC, BLF, CSV, candump, TRC, SQLite, MF4 and gzipped text, with triggered recording on signal conditions, 0.25×–10× replay, breakpoints and single-stepping onto a real bus, camera/GPS sync, multi-bus timelines and two-log comparison.
- **Databases** — DBC, BUSMASTER DBF, AUTOSAR ARXML (including container PDUs), Kayak KCD, PCAN SYM and LIN LDF, with live **AUTOSAR E2E and SecOC** checks on ARXML PDUs.
- **Diagnostics** — UDS over ISO-TP and LIN transport with sessions, DIDs, routines, user-supplied seed/key algorithms, CDD/ODX descriptions and flashing; OBD-II; UDS **discovery** (enumeration of services, DIDs, subfunctions and routines) and mutation fuzzing that watches for hangs and crashes; DoIP over ISO 13400-2 with TLS routing activation; SOME/IP-SD discovery; XCP/CCP measurement and calibration from A2L.
- **Security and automation** — a password-protected key store for SecOC keys, TLS/IPsec/MACsec material and seed/key algorithms, with replay/forgery tests, UDS Authentication (0x29) and decrypted capture inspection; Python simulated ECUs, restbus simulation and `can-test` headless ECU tests with HTML/JUnit/Markdown reports; `can-server` for remote buses and `can-mcp` to expose a bus to an AI agent behind permission tiers.

## Where it fits

Where [CAN Playground](can-playground.md) is a log viewer and [SavvyCAN](savvycan.md) a reverse-engineering GUI, CANExplorer aims to be the whole bench: signal RE, diagnostics, Ethernet protocols, simulation and CI-test execution in one workspace. That makes it a useful reference point for [UDS](uds.md) discovery workflows and for [automated reverse engineering of CAN commands from mobile apps](automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps.md), where the trace-to-signal pipeline matters. Its SecOC and authentication work is the applied side of the bus-authentication design space.

## Limits and safety notes

Breadth is the trade-off: the installer does not bundle every optional extra (MF4, MQTT, EtherCAT, USB I/O and some vendor drivers are source-install extras), FlexRay and some interfaces are marked experimental, and SecOC/E2E checks require the matching ARXML and keys rather than working from CAN frames alone. "Millions of frames", "automatic detection" and the MCP feature set are upstream self-descriptions; this page records what the README claims, not independently reproduced results. UDS discovery/fuzzing, ECU flashing and replay onto a real bus change live ECU state — use an isolated, authorised bench. The README's `can-mcp` permission tiers are a deliberate guardrail, not a substitute for bench safety. No hardware execution was performed for this page.

## Status and sources

Checked 2026-11-17. **Active** at this check: public, not archived, default branch pushed 2026-11-15, 180 stars, 19 forks, four open issues, MIT. Repository activity is not a support guarantee.

- [Upstream README](https://raw.githubusercontent.com/AKJ7/CANExplorer/master/README.md)
- [Repository metadata](https://api.github.com/repos/AKJ7/CANExplorer)
- [Project documentation](https://akj7.github.io/CANExplorer/)

## Related

- [ECU-BUS Pro](ecubus-pro.md)
- [SavvyCAN](savvycan.md)
- [Automated cross-platform reverse engineering of CAN bus commands from mobile apps](automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps.md)
- [UDS](uds.md)
- [Autofuze](autofuze.md)
- [Scapy](scapy.md)
