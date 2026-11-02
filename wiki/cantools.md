---
title: "cantools"
summary: "Python library for CAN bus diagnostics, DBC parsing, and message decoding/encoding."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/cantools/cantools"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python library for CAN bus diagnostics, DBC parsing, and message decoding/encoding."
related: [python-can, canmatrix, canarchy, kayak]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/cantools/cantools"
    retrieved: 2026-10-31
  - url: "https://cantools.readthedocs.io/en/latest/"
    retrieved: 2026-10-31
---

Python library for CAN bus diagnostics, DBC parsing, and message decoding/encoding.

## What it is

A Python 3 library and command-line toolkit centred on CAN database
files. The repository sits under the `cantools` GitHub organisation;
package metadata names Erik Moqvist as author.

## How it works

Load a DBC, KCD, SYM, ARXML 3/4, or CDD database into message and signal
objects, then encode signal values into frame data or decode a frame ID
and payload back into physical values. The database layer is deliberately
separate from bus transport: the documented live-bus examples use
[python-can](python-can.md) to send and receive through SocketCAN. CLI
commands decode or plot `candump` streams, dump and list a database,
monitor traffic, and generate C pack/unpack code. It also supports
diagnostic DID encoding/decoding and a node tester.

## Where it fits

Programmatic DBC/KCD work, log decoding, signal plotting, automated node
testing, and generating embedded C codecs from a CAN database. It is the
decode engine inside [CANarchy](canarchy.md) and [opendbc](opendbc.md),
and the usual partner to python-can in scripts. Where
[canmatrix](canmatrix.md) converts between database formats, cantools is
the library for working against one database at a time.

## Limits and notes

The C generator documents a maximum signal size of 64 bits. Plotting
requires the optional Matplotlib installation. No vehicle-safety warning
is stated in the checked project documentation.

## Related

- [python-can](python-can.md) — the transport layer in its live-bus examples.
- [canmatrix](canmatrix.md) — format conversion between databases.
- [CANarchy](canarchy.md) — builds its DBC workflows on cantools.
- [Kayak](kayak.md) — KCD is Kayak's native format.
