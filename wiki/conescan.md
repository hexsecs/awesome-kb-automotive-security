---
uid: 01a19d3c-af75-78d6-8e95-26da78baef80
title: "conescan"
summary: "Automotive ECU hacking supertool for firmware dumping and manipulation via J2534 OBD interfaces."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/ConnorRigby/conescan"
status: unknown
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Automotive ECU hacking supertool for firmware dumping and manipulation via J2534 OBD interfaces."
related: [atlas, udsoncan, uds-firmware-extraction, firmware-acquisition]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/ConnorRigby/conescan"
    retrieved: 2026-10-31
---

Automotive ECU hacking supertool for firmware dumping and manipulation via J2534 OBD interfaces.

## What it is

An "Automotive ECU Hacking supertool" (the repository's own
description) by Connor Rigby, in C/C++. **This page is deliberately
cautious: the repository's README is empty (0 bytes) and its one doc
file could not be retrieved at check time, so the feature list below
rests on the source tree, not on documentation.**

## How it works

From the source tree itself: a GUI application (layout, shader,
table-editor, console, and file-dialog sources), ECU definition parsing
(`definition.cpp`, `definition_parse.cpp`), a database component
(`conescan_db.cpp`, with a shipped `conescan.db`), and a UDS module
named `uds_request_download.cpp` — i.e. it implements UDS
RequestDownload, the flash-download service. It builds via a Makefile
and a Visual Studio solution; an `emscripten/` directory exists but its
purpose is unverified.

## Where it fits

By the tree evidence: ECU definition/table editing and UDS download
workflows — the same neighbourhood as [Atlas](atlas.md), with far less
documentation to judge it by. Treat this page as a pointer with
evidence attached, not a recommendation.

## Limits and notes

None stated in the checked sources — the README is empty, so no
warnings could be read. Status `unknown`: the repository is not
archived, but its last push was 2022-11-11, weeks after creation, so
upkeep cannot be verified. A LICENSE file exists but GitHub classifies
it as "Other" (NOASSERTION); the licence is unverified.

## Related

- [Atlas](atlas.md) — the documented calibration counterpart.
- [udsoncan](udsoncan.md) — the UDS layer its download module speaks.
- [UDS Firmware Extraction](uds-firmware-extraction.md) — the reverse direction of its download path.
