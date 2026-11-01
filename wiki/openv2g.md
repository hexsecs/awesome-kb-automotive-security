---
title: "OpenV2G"
summary: "C implementation of the ISO 15118 and DIN 70121 vehicle-to-grid interface with an EXI codec, widely reused as the encoding engine behind other V2G analysis…"
type: entity
category: "EV Charging Security"
url: "https://github.com/Martin-P/OpenV2G"
status: maintenance
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "C implementation of the ISO 15118 and DIN 70121 vehicle-to-grid interface with an EXI codec, widely reused as the encoding engine behind other V2G analysis tooling."
related: [pyplc, v2gdecoder, wwcp-iso15118, open-plc-utils]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/Martin-P/OpenV2G"
    retrieved: 2026-11-01
  - url: "https://github.com/Martin-P/OpenV2G/commit/733d4f43cb6579c705d59c7386786ce12a0a0026"
    retrieved: 2026-11-01
  - url: "https://github.com/Martin-P/OpenV2G/blob/733d4f43cb6579c705d59c7386786ce12a0a0026/README.txt"
    retrieved: 2026-11-01
  - url: "https://github.com/uhi22/pyPLC/blob/be5139bc6e66ba3b3bfa502666f494d3e157968b/readme.md"
    retrieved: 2026-11-01
---

C implementation of the ISO 15118 and DIN 70121 vehicle-to-grid interface with an EXI codec, widely reused as the encoding engine behind other V2G analysis tooling.

## What it is

A Siemens-origin C implementation of basic ISO/IEC 15118 vehicle-to-grid functionality and EXI encoding/decoding. The checked README identifies release 0.9.6, dated 2025-01-14, under LGPL-3.0-or-later. It records ISO 15118-2 schema tracks and DIN support, along with AC/DC message-sequence examples.

## How it works

Schema-specific C codecs encode and decode the charging message structures. The README distinguishes ISO1 (15118-2-2013), ISO2 (15118-2-2016), and DIN tracks; those internal names do not mean ISO 15118-1 versus -2. DIN support and XML signature/fragment functionality have build-time deployment switches, so a particular binary's capabilities depend on its configuration. The history also records the application handshake and V2GTP framing.

## Where it fits

Useful as a codec/reference implementation beneath experimental tooling. [pyPLC](pyplc.md) documents using its OpenV2Gx fork to expose a command-line codec to Python; this is a fork relationship, not a claim that the upstream repository itself supplies pyPLC's wrapper. Compare with [V2Gdecoder](v2gdecoder.md), which uses the Java RISE-V2G library, and [WWCP_ISO15118](wwcp-iso15118.md), which separates C# codecs from session logic. [open-plc-utils](open-plc-utils.md) serves the lower modem layer.

## Limits and safety notes

The README does not establish ISO 15118-20 support, a complete modern Plug & Charge deployment, or a production-ready charging controller. XML signature encoding support is only one component of certificate-based authorisation. Versions 0.9.5 and 0.9.6 fixed possible memory corruption and large-integer decoding overflow respectively; check the actual vendored version rather than assuming a downstream fork includes those fixes. Treat arbitrary captured inputs as untrusted. The maintenance classification below reflects the checked mirror's sparse update history, not an upstream end-of-life announcement.

## Status and sources

Checked 2026-11-01. **Maintenance** is an editorial assessment: the repository is not archived, but the latest default-branch commit is the 2025-11-12 import/merge of release 0.9.6. The README records bug fixes rather than a current feature roadmap; no upstream retirement announcement was found in these checked sources. See the [checked commit](https://github.com/Martin-P/OpenV2G/commit/733d4f43cb6579c705d59c7386786ce12a0a0026). Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream README](https://github.com/Martin-P/OpenV2G/blob/733d4f43cb6579c705d59c7386786ce12a0a0026/README.txt)

- [pyPLC upstream README: integration and modem visibility](https://github.com/uhi22/pyPLC/blob/be5139bc6e66ba3b3bfa502666f494d3e157968b/readme.md)

## Related

- [pyPLC](pyplc.md)
- [V2Gdecoder](v2gdecoder.md)
- [WWCP_ISO15118](wwcp-iso15118.md)
- [open-plc-utils](open-plc-utils.md)
