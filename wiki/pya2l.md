---
title: "pyA2L"
summary: "Python parser for ASAM MCD-2 MC (A2L) description files, exposing the characteristic, measurement, and memory-layout metadata needed to make sense of ECU…"
type: entity
category: "Firmware and ECU Reverse Engineering"
url: "https://github.com/christoph2/pya2l"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Python parser for ASAM MCD-2 MC (A2L) description files, exposing the characteristic, measurement, and memory-layout metadata needed to make sense of ECU calibration data during firmware analysis."
related: [pyxcp, medc17-checksum-tool]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/christoph2/pya2l"
    retrieved: 2026-11-01
  - url: "https://github.com/christoph2/pya2l/blob/master/README.md"
    retrieved: 2026-11-01
  - url: "https://github.com/christoph2/pya2l/releases/tag/v0.15.2"
    retrieved: 2026-11-01
---

Python parser for ASAM MCD-2 MC (A2L) description files, exposing the characteristic, measurement, and memory-layout metadata needed to make sense of ECU calibration data during firmware analysis.

## What it is

A Python library (GPLv3) for ASAM MCD-2 MC files — the **A2L** format. An A2L file is the calibration engineer's map of an ECU: it names every measurement and adjustable characteristic, gives its address in ECU memory, its data type, and the conversion formulas that turn raw bytes into physical values. pyA2L imports an A2L file into a queryable SQLite database (via SQLAlchemy) and exposes the result through a Python API — project metadata, ASAP2 elements, interface descriptors (IF_DATA), memory segments, and the rest of the standard's data model.

## How it works

A2L itself is defined by two grammars — the ASAP2 language for the file body and AML for the machine-readable interface descriptions — and pyA2L's README describes ANTLR-based tooling for them (it generates AML parsers from the meta-model). Importing an A2L produces a database the library's higher-level API queries: find a characteristic by name, get its address and record layout, follow its conversion method. (The list summary calls pyA2L a "parser"; upstream's own description centres on A2L import into the database — the distinction matters because repeated queries run against the DB, not the text file.) The same author's [pyXCP](pyxcp.md) is the natural consumer: an XCP slave's A2L describes exactly the memory pyXCP then measures and calibrates.

## Where it fits

Calibration literacy is half of ECU reverse engineering. A firmware dump tells you where code is; an A2L tells you what the data *means* — which map is a torque limit, which scalar is an injection quantity, and what units a value has. For security work that distinction is load-bearing: seed/key routines, diagnostic limits, and safety thresholds are usually characteristics with names. Leaked or extracted A2L files are therefore sensitive artefacts in their own right, and pyA2L is the open tool for mining them programmatically instead of in a commercial calibration suite.

## Limits and safety notes

A2L files are only as truthful as their generator: a mismatched A2L/firmware pair yields confident, wrong addresses, and nothing in the format authenticates the pairing. The README is brief about supported ASAM version coverage, so edge constructs (vendor IF_DATA variants are notorious) should be verified against the standard or a reference tool before results are trusted. The README also lists cython-a2l, a related experiment, as not production-ready — do not confuse the two.

## Status and sources

Checked 2026-11-01. **Active**: the repository is not archived, the latest release is v0.15.2 (2026-10-21, on PyPI as pya2l 0.15.2), and commits continue into late October 2026. This records observed project activity, not a promise of support. Documentation claims above come from the following primary sources; no A2L files were processed for this page.

- [Upstream repository](https://github.com/christoph2/pya2l)
- [Upstream README](https://github.com/christoph2/pya2l/blob/master/README.md)
- [Release v0.15.2](https://github.com/christoph2/pya2l/releases/tag/v0.15.2)

## Related

- [pyXCP](pyxcp.md)
- [medc17-checksum-tool](medc17-checksum-tool.md)
