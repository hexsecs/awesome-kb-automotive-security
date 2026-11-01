---
title: "automotive-security-research"
summary: "Published reverse engineering results for two production vehicles including CAN matrices, extracted ECU security access keys, and UDS scanning…"
type: entity
category: "Penetration Testing"
url: "https://github.com/ps1337/automotive-security-research"
status: unknown
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Published reverse engineering results for two production vehicles including CAN matrices, extracted ECU security access keys, and UDS scanning proof-of-concepts."
related: [uds-seed-key, simos18-sboot, q50-reverse-engineering]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/ps1337/automotive-security-research"
    retrieved: 2026-11-01
  - url: "https://github.com/ps1337/automotive-security-research/blob/master/README.md"
    retrieved: 2026-11-01
---

Published reverse engineering results for two production vehicles including CAN matrices, extracted ECU security access keys, and UDS scanning proof-of-concepts.

## What it is

A published research-results repository: the artefacts of one researcher's reverse engineering of two production car models from a single manufacturer. The repository deliberately does not name the manufacturer — its description reads "…for a few specific car models of a very specific car manufacturer. Please don't sue." It is a data and proof-of-concept dump, not a tool: partial CAN matrices, CAN dumps, extracted ECU security-access keys, and two small Python proof-of-concepts, accompanied by the author's BSides Stuttgart 2019 slides and a redacted paper.

## How it works

The README indexes the contents. `helpers/` holds two simple Python PoCs: reading CAN data, and scanning a CAN bus for UDS security access — the seed/key service whose weaknesses are this KB's [UDS seed/key](concepts/uds-seed-key.md) concept. `keys/` holds ECU keys extracted from manufacturer software using IDA; the README notes the manufacturer is guessable from the file names. `misc/` holds the partial CAN matrix of various cars and CAN protocol information. `model-6/` and `model-8/` hold per-model data sets for the two models: code to set the displayed speed on the speedometer via CAN, various CAN dumps, and a wiring diagram. `paper.pdf` is a redacted version of a car-hacking paper (German only, per the README); `slides_bsidesSTR_2019.pdf` is the BSides Stuttgart 2019 talk.

## Where it fits

The section's worked-example counterpart to documented research like [Simos18_SBOOT](simos18-sboot.md): real extracted SecurityAccess keys and a UDS security-access scanner make the seed/key failure class concrete on production vehicles, and the CAN matrices and dumps pair with the CAN Bus Analysis section's reverse-engineering pages (compare [q50-reverse-engineering](q50-reverse-engineering.md), another published single-vehicle RE dump). It is evidence, not tooling — nothing here is packaged for reuse against other vehicles.

## Limits and safety notes

Everything is specific to the two unnamed models, and the CAN matrix is explicitly "partial". The `keys/` directory publishes real extracted ECU keys for those vehicles — that is the repository's content and its sensitivity, stated plainly. The paper is redacted and German-only. The manufacturer and models are not named in the source, and this page does not name them either.

## Status and sources

Checked 2026-11-01. **Unknown**: the repository is not archived, but its commits end at 2019-05-26 ("add BSides STR 2019 slides") and there are no releases. It is a finished 2018–2019 research artefact; no ongoing project state is observable. Documentation claims above come from the following primary sources.

- [Upstream repository](https://github.com/ps1337/automotive-security-research)
- [Upstream README](https://github.com/ps1337/automotive-security-research/blob/master/README.md)

## Related

- [UDS seed/key](concepts/uds-seed-key.md)
- [Simos18_SBOOT](simos18-sboot.md)
- [q50-reverse-engineering](q50-reverse-engineering.md)
