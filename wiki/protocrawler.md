---
title: "ProtoCrawler"
summary: "Intelligent protocol fuzzer for SOME/IP, DoIP, UDS, and Ethernet AVB satisfying ISO/SAE 21434 testing requirements."
type: entity
category: "Automotive Ethernet"
url: "https://cytal.co.uk/"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Intelligent protocol fuzzer for SOME/IP, DoIP, UDS, and Ethernet AVB satisfying ISO/SAE 21434 testing requirements."
related: [someip-protocol-fuzzer, autofuze, eth-ws-someip, ics-cap]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://cytal.co.uk/"
    retrieved: 2026-11-01
  - url: "https://cytal.co.uk/blog/comprehensive-protocol-security-the-industry-spanning-reach-of-protocrawler/"
    retrieved: 2026-11-01
  - url: "https://cytal.co.uk/blog/protocrawler-comprehensive-protocol-support-for-advanced-security-testing-2025/"
    retrieved: 2026-11-01
---

Intelligent protocol fuzzer for SOME/IP, DoIP, UDS, and Ethernet AVB satisfying ISO/SAE 21434 testing requirements.

## What it is

ProtoCrawler™ is a commercial, closed-source, black-box protocol fuzz-testing platform from UK consultancy CyTAL, sold as a standalone software product alongside CyTAL's testing consultancy. It is not automotive-specific: the vendor positions one protocol-aware fuzzing engine across six verticals (telecommunications, smart metering/utilities, ICS/OT, automotive & connected vehicles, medical IoT, networking/security OEMs) with a library the vendor puts at over 70 protocol models. The automotive slice of that library — SOME/IP, DoIP/UDS and Ethernet AVB under ISO/SAE 21434 — is why it sits in this section. There is no public download, repository or trial; access runs through a vendor demo and proof-of-concept process.

## How it works

The engine is model-based rather than blind mutation — the vendor's central claim, stated consistently across its pages: structured protocol models encode message structures, state machines and security mechanisms, and test cases are generated to respect protocol constraints while probing edge cases. The vendor's vertical overview describes automated test generation maximising coverage within those constraints, real-time monitoring with progress tracking, automated analysis using "experience-based scoring matrices" to prioritise high-risk findings, and reporting aimed at remediation and audit evidence. Automotive coverage, per that same vendor post: **SOME/IP** — service discovery, method-call handling, event/field notification mechanisms, and serialisation; **DoIP and UDS as a pair** — authentication mechanisms, diagnostic session management, and command authorisation; **TCP/IP stack, TLS, Ethernet AVB** — network-stack, cryptographic-implementation and audio/video-bridging robustness. The compliance framing is ISO/SAE 21434, with IEC 62443 and UL-2900-1 named alongside it. A dedicated vendor post specifies the CI/CD claim: command-line execution fitting Jenkins, GitLab CI and GitHub Actions pipelines, machine-readable output, and exit codes usable as pass/fail gates. The finding classes the vendor says this testing surfaces — malformed messages causing device resets, invalid authentication data accepted, memory disclosure through error responses, state-machine flaws, missing input validation, specification non-compliances — are its generic cross-protocol claims; no automotive finding, CVE or named target is published in the sources read. The vendor positions ProtoCrawler against Defensics, with dedicated comparison pages — its own competitive framing, recorded here as such.

## Where it fits

The commercial, compliance-driven end of SOME/IP/DoIP fuzzing in this KB. Its direct counterpart is [someip-protocol-fuzzer](someip-protocol-fuzzer.md): same target protocol, opposite philosophy and economics — open-source single-protocol radamsa mutation with a ping heartbeat, versus closed multi-protocol model-based generation with scoring and reporting aimed at certification evidence. It overlaps [AutoFuze](autofuze.md) on SOME/IP fuzzing within a wider protocol set: AutoFuze is an open toolkit a tester runs themselves; ProtoCrawler is a procured platform whose output is scored reports for assurance processes. It complements the passive pair [eth-ws-someip](eth-ws-someip.md) / [ICS CAP](ics-cap.md): ProtoCrawler is purely active, and dissection/capture tooling is how its traffic and the target's responses would be observed.

## Limits and safety notes

The coverage-list discrepancy is the most important caveat on this page. The vendor's formal library page, "ProtoCrawler Supported Protocols 2025", enumerates its 70+ protocols in detail and **does not list SOME/IP, DoIP, UDS or Ethernet AVB anywhere in it**; its automotive-adjacent entries are EV-charging protocols (OCPP, ISO 15118 and relatives) and CAN bus protocols. The SOME/IP/DoIP/UDS/AVB coverage rests solely on the vendor's vertical overview blog post, so this page attributes it to that post specifically; whether the automotive Ethernet models are standard library items, roadmap items, or bespoke/consultancy-delivered is **not established** by the sources. Closed and gated: no public pricing, version number, documentation, system requirements, or target-interface details appear in any primary source read, and no automotive customer or published automotive result is named. Fuzzing is active testing — by the vendor's own findings list, its traffic can reset devices and deny service; the vendor's safety language (rate controls, pausing, safe staging environments) appears in its utilities guidance, not its automotive material, and is not presented here as an automotive feature.

## Status and sources

Checked 2026-11-01. **Active**: CyTAL's site is live, was substantively updated in September 2025, and carries vendor posts dated May 2026, with ProtoCrawler demo booking open — a currently marketed and sold commercial product. No public version or release history exists to cite. Documentation claims above come from the following vendor sources; no target was fuzzed for this page.

- [Vendor homepage](https://cytal.co.uk/)
- [Vendor vertical overview (automotive coverage)](https://cytal.co.uk/blog/comprehensive-protocol-security-the-industry-spanning-reach-of-protocrawler/)
- [Vendor supported-protocols library, 2025](https://cytal.co.uk/blog/protocrawler-comprehensive-protocol-support-for-advanced-security-testing-2025/)

## Related

- [someip-protocol-fuzzer](someip-protocol-fuzzer.md)
- [AutoFuze](autofuze.md)
- [eth-ws-someip](eth-ws-someip.md)
- [ICS CAP](ics-cap.md)
