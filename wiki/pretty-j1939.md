---
title: "pretty_j1939"
summary: "NMFTA's Python library and CLI that decodes J1939 traffic from candump logs using the SAE J1939 Digital Annex, with transport protocol reassembly…"
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/nmfta-repo/pretty_j1939"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "NMFTA's Python library and CLI that decodes J1939 traffic from candump logs using the SAE J1939 Digital Annex, with transport protocol reassembly, filtering, JSON output, and a live terminal view."
related: [canarchy, can-utils, python-can]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/nmfta-repo/pretty_j1939"
    retrieved: 2026-10-31
---

NMFTA's Python library and CLI that decodes J1939 traffic from candump logs using the SAE J1939 Digital Annex, with transport protocol reassembly, filtering, JSON output, and a live terminal view.

## What it is

A Python library and CLI for decoding J1939 traffic, published under the
`nmfta-repo` GitHub organisation (the project pages do not expand the
NMFTA acronym; the expansion to National Motor Freight Traffic
Association comes from general sources).

## How it works

Two halves: `create_j1939db-json` converts the SAE J1939 Digital Annex
(`.xls`/`.xlsx`) into a `J1939db.json`, and the `pretty_j1939` CLI/library
decodes candump logs — or live capture via [python-can](python-can.md) —
against it, emitting JSON with PGN/SPN names, source/destination
addresses, and physical values, pipeable to `jq`. It reassembles J1939
transport (BAM, RTS/CTS) and ISO-TP multi-packet messages, filters and
highlights by PGN/SA/DA, generates a Mermaid network summary of controller
applications, and offers a curses live viewer. Database lookup order:
`--da-json`, the current directory, the user config directory, then the
bundled fallback.

## Where it fits

Heavy-vehicle and J1939 log analysis and scripting: decoding truck
candump captures produced by [can-utils](can-utils.md) into named PGN/SPN
data, mapping which ECUs talk to which, and embedding J1939 decoding in
other Python tools. [CANarchy](canarchy.md) covers the same J1939 ground
inside a broader event-stream toolkit with its own bundled catalog.

## Limits and notes

Full decoding requires buying the Digital Annex from SAE; the bundled
default database is explicitly "very limited," built only from freely
available information. The README also notes that some Digital Annex
editions regress (the 201611 edition has fewer SPNs than 201311) or
contain bugs the converter works around, and that isobus.net exports omit
almost all commercial-vehicle SPNs/PGNs.

## Related

- [CANarchy](canarchy.md) — J1939-first analysis in an event-stream toolkit.
- [can-utils](can-utils.md) — produces the candump logs it decodes.
- [python-can](python-can.md) — its live-capture path.
