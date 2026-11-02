---
uid: 01a19d3c-af4b-71ea-90c4-fc2989d1390e
title: "canmatrix"
summary: "Python package to read and write CAN database formats, converting between DBC, ARXML, KCD, SYM, LDF, ODX, and more."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/ebroecker/canmatrix"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python package to read and write CAN database formats, converting between DBC, ARXML, KCD, SYM, LDF, ODX, and more."
related: [cantools, kayak, busmaster]
license: BSD-2-Clause
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/ebroecker/canmatrix"
    retrieved: 2026-10-31
---

Python package to read and write CAN database formats, converting between DBC, ARXML, KCD, SYM, LDF, ODX, and more.

## What it is

A Python library and CLI tools for reading, writing, converting, and
comparing CAN communication databases, maintained in Eduard Bröcker's
`ebroecker` repository. BSD-2-Clause, with documentation on Read the Docs.

## How it works

Everything passes through a format-neutral "Python Can Matrix Object" —
board units, frames, signals, and values — with format plug-ins importing
and exporting around it. Import covers DBC, DBF, KCD, ARXML, YAML, XLS(X),
SYM, FIBEX/CANopen-EDS XML, LDF, ODX, and EDS; export covers DBC, DBF,
KCD, XLS(X), JSON (Canard), ARXML, YAML, SYM, FIBEX, Wireshark Lua
dissectors, and Scapy. It ships `canconvert` (convert between formats)
and `cancompare` (diff two databases), and can also encode and decode
messages.

## Where it fits

Format migration (ARXML→DBC is the classic case), database diffing in CI,
generating Wireshark dissectors, and scripted matrix manipulation. It is
the conversion layer other tools point at — [CANgaroo](cangaroo.md)'s
README sends ARXML users here — while [cantools](cantools.md) is the
library to reach for when the job is decoding traffic against one DBC
rather than moving between formats.

## Limits and notes

ARXML *export* is explicitly a "very basic implementation." It is a
database tool, not a live-bus tool: no capture or analysis workflow is
claimed.

## Related

- [cantools](cantools.md) — decode/encode against a database, live or offline.
- [Kayak](kayak.md) — KCD is Kayak's native format.
- [BUSMASTER](busmaster.md) — DBF is BUSMASTER's database format.
