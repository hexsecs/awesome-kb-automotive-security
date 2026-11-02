---
title: "V2Gdecoder"
summary: "Encodes and decodes EXI-compressed V2G messages on the fly, turning captured ISO 15118 exchanges into editable XML for replay and fuzzing."
type: entity
category: "EV Charging Security"
url: "https://github.com/FlUxIuS/V2Gdecoder"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Encodes and decodes EXI-compressed V2G messages on the fly, turning captured ISO 15118 exchanges into editable XML for replay and fuzzing."
related: [openv2g, dsv2gshark, pyplc, wwcp-iso15118]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/FlUxIuS/V2Gdecoder"
    retrieved: 2026-11-01
  - url: "https://github.com/FlUxIuS/V2Gdecoder/commit/2ee5bd94d94d0eaaff8ee693990182f6d6c6c084"
    retrieved: 2026-11-01
  - url: "https://github.com/FlUxIuS/V2Gdecoder/blob/2ee5bd94d94d0eaaff8ee693990182f6d6c6c084/README.md"
    retrieved: 2026-11-01
---

Encodes and decodes EXI-compressed V2G messages on the fly, turning captured ISO 15118 exchanges into editable XML for replay and fuzzing.

## What it is

A Java utility for converting EXI-compressed vehicle-to-grid messages to XML and encoding XML back to EXI. Its README identifies RISE-V2G's shared Java library as the parser foundation. It supplies conversion building blocks for trace inspection or a separate test harness, rather than a complete vehicle/charger emulator.

## How it works

Maven builds an executable JAR. The documented interface accepts string or file input, distinguishes EXI and XML formats, and can write results to an output path. The schemas directory must be present at the tool's root. A web-service mode exposes the same conversion over local TCP port 9000. The README's examples include an ISO 15118-2:2013 response and a SupportedAppProtocol request offering DIN 70121 and ISO 15118-2.

## Where it fits

Useful when a researcher needs readable XML from a captured payload or wants to edit and re-encode a message for an authorised test harness. [dsV2Gshark](dsv2gshark.md) instead integrates decoding with Wireshark's capture/session context. [OpenV2G](openv2g.md) is a separate C codec family, [pyPLC](pyplc.md) a higher-level research stack, and [WWCP_ISO15118](wwcp-iso15118.md) another codec/session implementation.

## Limits and safety notes

The upstream README warns that manufacturers may use old schema definitions, producing decoding problems; schema mismatch is not by itself evidence of a faulty endpoint. Upgrading the RISE-V2G dependency may require source changes. The checked documentation does not establish ISO 15118-20 support, TLS decryption, packet capture, automatic replay, or a fuzzing engine. A decoded XML signature is not proof of Plug & Charge trust/authorisation. Keep the optional conversion service within the lab, and retain original bytes and schema context when interpreting results.

## Status and sources

Checked 2026-11-01. **Active** at this check: the repository is not archived and its latest default-branch commit is dated 2026-07-28. This records observed project activity, not a promise of support or protocol completeness. See the [checked commit](https://github.com/FlUxIuS/V2Gdecoder/commit/2ee5bd94d94d0eaaff8ee693990182f6d6c6c084). Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream README](https://github.com/FlUxIuS/V2Gdecoder/blob/2ee5bd94d94d0eaaff8ee693990182f6d6c6c084/README.md)

## Related

- [OpenV2G](openv2g.md)
- [dsV2Gshark](dsv2gshark.md)
- [pyPLC](pyplc.md)
- [WWCP_ISO15118](wwcp-iso15118.md)
