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
  - url: "https://pypi.org/project/pya2ldb/"
    retrieved: 2026-11-01
---

Python parser for ASAM MCD-2 MC (A2L) description files, exposing the characteristic, measurement, and memory-layout metadata needed to make sense of ECU calibration data during firmware analysis.

## What it is

A Python library for ASAM MCD-2 MC files — the **A2L** format. An A2L file is the calibration engineer's map of an ECU: it names every measurement and adjustable characteristic, gives its address in ECU memory, its data type, and the conversion formulas that turn raw bytes into physical values. pyA2L imports an A2L file into a queryable SQLite database (via SQLAlchemy) and exposes the result through a Python API — project metadata, ASAP2 elements, interface descriptors (IF_DATA), memory segments, and the rest of the standard's data model. Two naming facts matter for anyone installing it: the PyPI package is **`pya2ldb`**, not `pya2l` (the PyPI project named `pya2l` belongs to a different author), and the licence record is conflicted at the source — the repository metadata and `pyproject` say **GPL-2.0**, while the README badge says LGPL v3+. This page states the conflict rather than resolving it.

## How it works

A2L itself is defined by two grammars — the ASAP2 language for the file body and AML for the machine-readable interface descriptions. pyA2L's parser machinery is ANTLR-based; an AML parser exists in the source tree, though the README does not document it — the documented surface is the import-and-query flow: importing an A2L produces a database the library's higher-level API queries (find a characteristic by name, get its address and record layout, follow its conversion method). The distinction matters because repeated queries run against the DB, not the text file. The same author's [pyXCP](pyxcp.md) is the natural consumer: an XCP slave's A2L describes exactly the memory pyXCP then measures and calibrates, and pyXCP's A2L integration runs through this package (`pya2ldb`).

## Where it fits

Calibration literacy is half of ECU reverse engineering. A firmware dump tells you where code is; an A2L tells you what the data *means* — which map is a torque limit, which scalar is an injection quantity, and what units a value has. For security work that distinction is load-bearing: seed/key routines, diagnostic limits, and safety thresholds are usually characteristics with names. Leaked or extracted A2L files are therefore sensitive artefacts in their own right, and pyA2L is the open tool for mining them programmatically instead of in a commercial calibration suite.

## Limits and safety notes

A2L files are only as truthful as their generator: a mismatched A2L/firmware pair yields confident, wrong addresses, and nothing in the format authenticates the pairing. Versioning needs care: GitHub Releases are stale (the latest there is 1.0.316, from 2021-12-04), while the living distribution is PyPI's `pya2ldb`, at version 1.0.355 as of 2026-10-15 — install and cite from PyPI, not from the GitHub release page. The README is brief about supported ASAM version coverage, so edge constructs (vendor IF_DATA variants are notorious) should be verified against the standard or a reference tool before results are trusted. The README also lists cython-a2l, a related experiment, as not production-ready — do not confuse the two.

## Status and sources

Checked 2026-11-01. **Active**: the repository is not archived, commits continue, and the current PyPI release of `pya2ldb` is 1.0.355 (2026-10-15). This records observed project activity, not a promise of support. Documentation claims above come from the following primary sources; no A2L files were processed for this page.

- [Upstream repository](https://github.com/christoph2/pya2l)
- [Upstream README](https://github.com/christoph2/pya2l/blob/master/README.md)
- [PyPI package (pya2ldb)](https://pypi.org/project/pya2ldb/)

## Related

- [pyXCP](pyxcp.md)
- [medc17-checksum-tool](medc17-checksum-tool.md)
