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
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python package to read and write CAN database formats, converting between DBC, ARXML, KCD, SYM, LDF, ODX, and more."
related:
  - cantools
  - kayak
  - busmaster
  - cangaroo
  - dbc-semantic-layer
license: BSD-2-Clause
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/ebroecker/canmatrix"
    retrieved: 2026-10-31
  - url: "https://canmatrix.readthedocs.io/en/latest/cli.html"
    retrieved: 2026-11-17
facets: [can, tools]
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

The [CLI manual](https://canmatrix.readthedocs.io/en/latest/cli.html),
checked with the repository on 2026-11-17, gives
`canconvert source.arxml target.dbc` as the basic migration shape.
An ARXML file can contain multiple CAN databases, so conversion can emit
one DBC per bus with the bus name prefixed to the requested output name.
Container-PDU frames are converted to multiplexed frames by default;
the documented ignore-container option instead drops those frames.
Choosing that policy is a semantic decision, not merely changing a file
extension.

Conversion also supports selective extraction and modification:
`--ecus=REAR_ECU` keeps the frames the named ECU sends or receives,
while `--frames=...` selects frames with their required ECUs and
attributes. `--merge=second.dbc` combines matrices; rename/delete options
operate on ECUs, frames, signals and attributes. Separate DBC import
and export encodings for units and comments help preserve text across
toolchains. `--recalcDLC=max` only enlarges a stored length when needed;
`force` replaces it with the calculated length. These transformations
should be deliberate, particularly before regenerating a database used
to interpret security-test captures.

A review workflow is to preserve the input, convert into a fresh output,
inspect any per-bus files and transformation choices, and use
`cancompare file1.dbc file2.dbc` to examine database differences.
The comparison tool accepts different supported input formats, so it
can help review migrations as well as revisions within one format.

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

Import and export format lists are not symmetric: reading LDF or ODX
does not imply writing those formats or executing LIN schedules and
diagnostic sessions. Nor does a successful conversion establish lossless
preservation of every source-specific attribute. In particular, review
container-PDU handling, text encoding and any requested DLC/layout
changes before treating the output as an equivalent wire contract.

## Related

- [cantools](cantools.md) — decode/encode against a database, live or offline.
- [Kayak](kayak.md) — KCD is Kayak's native format.
- [BUSMASTER](busmaster.md) — DBF is BUSMASTER's database format.
- [DBC as the CAN semantic layer](concepts/dbc-semantic-layer.md)
