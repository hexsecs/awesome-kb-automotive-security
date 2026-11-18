---
uid: 01a19d3c-af4d-7148-8900-80dc28d1a18d
title: "cantools"
summary: "Python library for CAN bus diagnostics, DBC parsing, and message decoding/encoding."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/cantools/cantools"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python library for CAN bus diagnostics, DBC parsing, and message decoding/encoding."
related:
  - python-can
  - canmatrix
  - canarchy
  - kayak
  - opendbc
  - canlab
  - savvycan
  - can-playground
  - dbc-semantic-layer
  - canalyse
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/cantools/cantools"
    retrieved: 2026-10-31
  - url: "https://cantools.readthedocs.io/en/latest/"
    retrieved: 2026-10-31
facets: [can, diagnostics, tools]
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

The [API documentation](https://cantools.readthedocs.io/en/latest/) and
[repository examples](https://github.com/cantools/cantools), checked
2026-11-17, make the data boundary concrete.
`cantools.database.load_file('vehicle.dbc')` returns a database;
`get_message_by_name()` retrieves a message whose `encode()` method
takes a dictionary of signal names and values and returns payload bytes.
At receive time, `db.decode_message(frame_id, data)` returns a dictionary
of decoded signals. Frame identifiers and extended-frame flags come from
the message definition; the caller builds the actual python-can message
and owns transmission.

Signal definitions carry bit positions, lengths, byte order, signedness,
scaling, offsets, units, and named choices. Simple and extended
multiplexing let different signal layouts share a message according to a
selector. By default, strict database validation raises an exception for
overlapping signals or signals that do not fit their message. This checks
layout consistency, not whether the database describes the vehicle being
observed.

For offline work, the CLI can read `candump` output from standard input
and append decoded signal values, or plot selected signals with wildcard
selection and separate axes. `dump` exposes bit layouts and the signal
tree; `list` provides less decorative output suitable for scripts.
The C generator emits header/source files containing message structs,
pack/unpack functions, signal conversion functions, and frame metadata.
Its options control floating-point representation and can restrict
generated pack/unpack paths to a named node.

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

Neither the decoder nor generated codecs infer missing signal meanings
from a capture. A successful decode is only as trustworthy as the supplied
database; DID encoding support is also not a complete diagnostic transport
or UDS session manager.

## Related

- [python-can](python-can.md) — the transport layer in its live-bus examples.
- [canmatrix](canmatrix.md) — format conversion between databases.
- [CANarchy](canarchy.md) — builds its DBC workflows on cantools.
- [Kayak](kayak.md) — KCD is Kayak's native format.
- [DBC as the CAN semantic layer](concepts/dbc-semantic-layer.md)
- [CANalyse](canalyse.md)
