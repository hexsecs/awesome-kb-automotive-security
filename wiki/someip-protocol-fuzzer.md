---
title: "someip-protocol-fuzzer"
summary: "Black-box SOME/IP fuzzer that mutates user-defined protocol fields with radamsa and uses a ping heartbeat to detect when the target service stops responding."
type: entity
category: "Automotive Ethernet"
url: "https://github.com/cfanatic/someip-protocol-fuzzer"
status: unknown
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Black-box SOME/IP fuzzer that mutates user-defined protocol fields with radamsa and uses a ping heartbeat to detect when the target service stops responding."
related: [protocrawler, autofuze, scapy, vsomeip, eth-ws-someip]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/cfanatic/someip-protocol-fuzzer"
    retrieved: 2026-11-01
---

Black-box SOME/IP fuzzer that mutates user-defined protocol fields with radamsa and uses a ping heartbeat to detect when the target service stops responding.

## What it is

A small proof-of-concept black-box fuzzer for SOME/IP services, written in Python on top of Scapy — the README calls it a proof-of-concept in its first paragraph. It takes seed values for operator-selected protocol fields from a template derived from captured traffic, mutates them with the external radamsa fuzzer, sends the mutated values to a target SOME/IP service, and runs a periodic ping/pong heartbeat against the same service, stopping the run when the heartbeat fails — i.e. when the target appears to have crashed or hung. Licence: MIT.

## How it works

The documented setup spans two VMs. The target VM runs a SOME/IP service built with **vsomeip 3.1.20** from the author's companion `vsomeip-fuzzing` repository; the fuzzer VM runs Python 3.7.6 with **Scapy pinned to 2.4.5** and radamsa 0.6. The template path: `template.py` reads a pcapng trace with Scapy, walks each packet's layers, and builds a JSON template recording, per layer (SOMEIP or SD) and direction, each field's observed values and type, with a `"fuzzer": null` marker. The operator edits the template to set `"fuzzer": "radamsa"` on the field(s) to mutate — the README's worked example fuzzes the payload field. (As committed, `main.py` only *imports* a pre-generated template; the generation function exists in the code but is never invoked by it.) The send loop runs one thread per targeted field on a 1-second cadence: pick a random seed value, pipe it through the radamsa subprocess, and send the result with Scapy's `sr1` as the payload of a SOME/IP request — the envelope in the committed code is fixed (service 0x1234, method 0x0421, client 0x1313, session 0x0010), and with history enabled the mutated output becomes the next round's seed. The heartbeat thread sends a `ping` payload every 3 seconds and requires a response ending in `pong`; a missing or wrong response raises an exception that propagates and terminates the run. Running requires sudo, which the code surfaces as its own error.

## Where it fits

The worked-example end of SOME/IP fuzzing in this KB: small, readable, and tied to a concrete reproducible target, where [ProtoCrawler](protocrawler.md) is a commercial model-based fuzzer and [AutoFuze](autofuze.md) covers SOME/IP inside a broader multi-protocol toolkit (AutoFuze's page already lists this entry as related; the link is reciprocated here). It is simultaneously a consumer of two other entries — built on [Scapy](scapy.md), whose SOME/IP layer does all packet construction, and aimed at [vsomeip](vsomeip.md), its documented target stack. It complements [eth-ws-someip](eth-ws-someip.md): the README itself has the operator analyse SOME/IP traffic in Wireshark first to learn the target's addresses and ports.

## Limits and safety notes

The README's own "Improvements" section is the authoritative limit list: the approach is black-box (a grey-box improvement would need a state machine to pass the target's trivial checks first), and the heartbeat should ideally be checked after *each* input so the exact mutated input that caused an anomaly can be identified — as shipped, the periodic 3-second heartbeat cannot attribute a failure to one specific input. The dependency matrix is generation-locked and old: Scapy 2.4.5 (whose SOME/IP API differs from current Scapy), Python 3.7.6, radamsa 0.6, a vsomeip 3.1.20 target; nothing in the repo indicates it has been run against current versions of either stack, so porting is part of using it. The target shape as committed is narrow — one hard-coded service/method pair, per-run manual template editing, no service discovery or enumeration — and the `live` mode offered in the config is an unimplemented stub; only replay mode does anything. Safety posture: this is an active fuzzer whose success signal is the target service *stopping responding*; the README's setup confines it to two VMs on a private 192.168.0.0 network, and the repo provides no safeguards for use against a service that matters.

## Status and sources

Checked 2026-11-01. **Unknown**: the repository is not archived, but it has had no commit, release or tag since April 2022 (20 commits total, January–April 2022) — a finished proof-of-concept artefact rather than a maintained tool, with no ongoing project state observable. The API's `updated_at` (a metadata timestamp) is not code activity; `pushed_at` is, and it is 2022. Documentation claims above come from the following primary sources; no service was fuzzed for this page.

- [Upstream repository](https://github.com/cfanatic/someip-protocol-fuzzer)

## Related

- [ProtoCrawler](protocrawler.md)
- [AutoFuze](autofuze.md)
- [Scapy](scapy.md)
- [vsomeip](vsomeip.md)
- [eth-ws-someip](eth-ws-someip.md)
