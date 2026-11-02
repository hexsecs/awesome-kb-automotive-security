---
title: "Universal Radio Hacker (URH)"
summary: "Open-source suite for wireless protocol investigation with native SDR support and easy signal demodulation."
type: entity
category: "RF and Key Fob Analysis"
url: "https://github.com/jopohl/urh"
status: archived
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source suite for wireless protocol investigation with native SDR support and easy signal demodulation."
related: [keyfob-analysis-toolkit-kat, rtl-433, flipper-zero]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/jopohl/urh"
    retrieved: 2026-11-01
  - url: "https://github.com/jopohl/urh/blob/master/README.md"
    retrieved: 2026-11-01
  - url: "https://github.com/jopohl/urh/releases/tag/v2.10.0"
    retrieved: 2026-11-01
---

Open-source suite for wireless protocol investigation with native SDR support and easy signal demodulation.

## What it is

A cross-platform (Windows, Linux, macOS) GPL-3.0 suite for investigating wireless protocols you do not already understand. Where most tools in this section decode a known signal, URH starts from a raw recording and walks you to a decoded, labelled, re-generatable protocol — the manual reverse-engineering workbench of the section. It comes from published research (Pohl & Noack, *Universal Radio Hacker: A Suite for Analyzing and Attacking Stateful Wireless Protocols*, USENIX WOOT '18).

## How it works

The documented workflow has four phases, with results transferable between them. **Interpretation** records or imports a signal (spectrum analyser to find it first), demodulates it automatically, and lets you tune noise threshold, bit length, centre, and error tolerance, with a spectrogram view for finding structure. **Analysis** aligns the resulting messages for comparison; you assign protocol fields and labels (or let rule-based inference propose them), attach checksums with generic CRC verification, and build decodings as chains of primitives — including CC1101-style data whitening. **Generation** turns the recovered protocol back into signals: checksums recalculate on edit, and a fuzzing component aimed at stateless protocols varies field values in successive, concurrent, or exhaustive modes. **Simulation** models stateful exchanges as a flow graph with rules, counters, and live or formula-driven label values — the stateful-attack counterpart to the fuzzer. Recording and sending use native C-extension backends where available (HackRF, bladeRF, LimeSDR, PlutoSDR, USRP, RTL-SDR receive-only, and others); [Flipper Zero](flipper-zero.md) is supported only via `.sub` files, with transmit limited to the Generator.

## Where it fits

URH is the tool for a fob or sensor protocol that nothing else decodes yet: [rtl_433](rtl-433.md) applies a fixed library of known decoders and stops there, and the [KeyFob Analysis Toolkit (KAT)](keyfob-analysis-toolkit-kat.md) models known fob families directly. URH's output is the understanding those tools presuppose — once a protocol is worked out in URH, a decoder or a dedicated script can follow. For the passive-keyless attack model these investigations feed into, see [key-fob relay attacks](concepts/key-fob-relay-attacks.md) — noting that relaying needs no protocol break at all, URH or otherwise.

## Limits and safety notes

URH is protocol-agnostic and ships no automotive-specific decoders: the demodulation is assisted, but field boundaries, checksums, and semantics are the analyst's work, and the fuzzer targets stateless protocols (stateful work needs the Simulator). The linked User Guide is v1.1, written for URH v2.0, and predates the final release by several versions, so guide details can be dated. The offensive capability is the documented purpose (the paper's title says "attacking"), so the usual rule applies with force: transmit, replay, and fuzzing only against your own or authorised equipment on permitted frequencies. And see Status — the project is over; factor end-of-life into any workflow built on it.

## Status and sources

Checked 2026-11-01. **Archived**: the owner archived the repository on 2026-03-29 and it is now read-only. The final release is v2.10.0 (2025-12-17) and the last commit is dated 2025-12-19. No further fixes should be expected. Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream repository](https://github.com/jopohl/urh)
- [Upstream README](https://github.com/jopohl/urh/blob/master/README.md)
- [Release v2.10.0](https://github.com/jopohl/urh/releases/tag/v2.10.0)

## Related

- [KeyFob Analysis Toolkit (KAT)](keyfob-analysis-toolkit-kat.md)
- [rtl_433](rtl-433.md)
- [Flipper Zero](flipper-zero.md)
- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md)
