---
uid: 01a19d3c-af75-78d6-8e95-26da78baef80
title: "conescan"
summary: "Automotive ECU hacking supertool for firmware dumping and manipulation via J2534 OBD interfaces."
type: entity
category: "Diagnostic Tools"
url: "https://github.com/ConnorRigby/conescan"
status: maintenance
last_checked: 2026-11-17
status_note: "GitHub repo not archived; last push 2022-11-11."
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Automotive ECU hacking supertool for firmware dumping and manipulation via J2534 OBD interfaces."
related:
  - atlas
  - udsoncan
  - uds-firmware-extraction
  - firmware-acquisition
  - openvehiclediag
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/ConnorRigby/conescan"
    retrieved: 2026-10-31
  - url: "https://github.com/ConnorRigby/conescan/tree/main/src"
    retrieved: 2026-11-17
  - url: "https://github.com/ConnorRigby/conescan/blob/main/docs/build.md"
    retrieved: 2026-11-17
facets: [diagnostics, firmware, tools]
---

Automotive ECU hacking supertool for firmware dumping and manipulation via J2534 OBD interfaces.

## What it is

An "Automotive ECU Hacking supertool" (the repository's own
description) by Connor Rigby, in C/C++. **This page is deliberately
cautious: the repository's README is empty (0 bytes) and its one doc
file, previously unavailable, was retrieved on 2026-11-17 but is also
empty (0 bytes), so the feature list below
rests on the source tree, not on documentation.**

## How it works

From the source tree itself: a GUI application (layout, shader,
table-editor, console, and file-dialog sources), ECU definition parsing
(`definition.cpp`, `definition_parse.cpp`), a database component
(`conescan_db.cpp`, with a shipped `conescan.db`), and a UDS module
named `uds_request_download.cpp` — evidence of a UDS RequestDownload
component, not proof of a complete flashing workflow. It has a Makefile
and a Visual Studio solution; an `emscripten/` directory exists but its
purpose is unverified.

The [source directory](https://github.com/ConnorRigby/conescan/tree/main/src)
was accessible on 2026-11-17 and still exposes these separate components.
That supports a narrow architectural reading: definitions and their
parser describe the data being edited, the table editor provides an
editing surface, and layout, console, history, and file-dialog code
support the surrounding application. The shipped database is an artifact
to inspect alongside definitions; its presence alone does not establish
which ECU families or firmware versions are supported. No definition
schema, command-line API, or documented input/output contract was
established by this check.

The list describes J2534 OBD interfaces, but the empty documentation
does not provide a verified adapter matrix, driver requirements, or an
end-to-end connection procedure. Likewise, the UDS filename is a useful
starting point for source inspection, not evidence that session setup,
security access, transfer sequencing, checksums, and recovery are all
implemented for a particular ECU. A RequestDownload component should not
be read as proof of firmware *readout*: transferring an image to an ECU
and extracting one from it are different workflows.

Before treating it as an operational tool, establish a reproducible build,
identify the exact definition and image formats in the parser, and trace
the download component's callers and transport backend. These are
evaluation requirements, not steps claimed by an upstream manual.
The [build document](https://github.com/ConnorRigby/conescan/blob/main/docs/build.md)
currently supplies no instructions to resolve them.

## Where it fits

By the tree evidence: ECU definition/table editing and UDS download
workflows — the same neighbourhood as [Atlas](atlas.md), with far less
documentation to judge it by. Treat this page as a pointer with
evidence attached, not a recommendation.

## Limits and notes

None stated in the checked sources — the README is empty, so no
warnings could be read. The preserved maintenance assessment records a
last push of 2022-11-11; repository accessibility does not establish current
upkeep. A LICENSE file exists but GitHub classifies
it as "Other" (NOASSERTION); the licence is unverified.

## Related

- [Atlas](atlas.md) — the documented calibration counterpart.
- [udsoncan](udsoncan.md) — the UDS layer its download module speaks.
- [UDS Firmware Extraction](uds-firmware-extraction.md) — the reverse direction of its download path.

See [firmware acquisition](concepts/firmware-acquisition.md) for the
distinction between obtaining an image and manipulating a calibration.
These sibling tools provide context, not a verified compatibility or
interchange promise for conescan's undocumented formats.
