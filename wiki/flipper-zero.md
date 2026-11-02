---
uid: 01a19d3c-af91-7450-9dd1-1e1a0a73d832
title: "Flipper Zero"
summary: "Handheld multi-tool with Sub-GHz capabilities for reading, saving, and transmitting key fob signals with automotive database."
type: entity
category: "RF and Key Fob Analysis"
url: "https://flipperzero.one/"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Handheld multi-tool with Sub-GHz capabilities for reading, saving, and transmitting key fob signals with automotive database."
related: [flipper-arf, keyfob-analysis-toolkit-kat, rtl-433, universal-radio-hacker-urh, proxmark3]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://flipperzero.one/"
    retrieved: 2026-11-01
  - url: "https://docs.flipper.net/zero/sub-ghz/read"
    retrieved: 2026-11-01
  - url: "https://github.com/flipperdevices/flipperzero-firmware/releases/tag/1.5.1"
    retrieved: 2026-11-01
---

Handheld multi-tool with Sub-GHz capabilities for reading, saving, and transmitting key fob signals with automotive database.

## What it is

A pocket-sized, battery-powered multi-tool built around several radios — a TI CC1101 Sub-GHz transceiver, a 125 kHz RFID reader, a 13.56 MHz NFC front end, infrared, and iButton/GPIO — running open-source firmware. The official site leads with remote-keyless-entry research among its uses, and the Sub-GHz app is the automotive surface in this section: it can receive, save, decode where a protocol is known, and retransmit signals in the 300–348, 387–464, and 779–928 MHz ranges (regional configuration applies).

## How it works

The Sub-GHz radio receives across 300–348, 387–464, and 779–928 MHz (the CC1101's bands; transmit is narrower and region-gated). The official Read documentation describes the workflow: pick the frequency (a Frequency Analyzer finds the strongest candidate) and the modulation — the Flipper is *not* an SDR, so the right modulation must be configured before scanning — then Read decodes known protocols. The documentation draws the key line by protocol class: **static** (unencrypted) remotes can be decoded, saved, and played back; **dynamic** (encrypted/rolling-code) remotes can be decoded, but "for security reasons, the save function is disabled" in official firmware. Unknown protocols fall back to Read RAW captures, stored as `.sub` files — the portable format other tools in this section (such as the [KeyFob Analysis Toolkit (KAT)](keyfob-analysis-toolkit-kat.md)) also consume. The supported alternative to cloning a dynamic remote is Add Manually: pair the Flipper with the receiver as a *new* remote. Custom apps run from the microSD card as FAP packages, usually without firmware changes. [Flipper-ARF](flipper-arf.md) is an automotive-focused firmware fork that builds on this base. The same hardware's LF RFID side overlaps the transponder world of [Proxmark3](proxmark3.md), at hobbyist rather than research depth.

## Where it fits

The Flipper is the handheld first look: walk up, capture, identify, save for the bench. Sustained survey work belongs to [rtl_433](rtl-433.md) on an RTL-SDR, and unknown-protocol reverse engineering to [Universal Radio Hacker (URH)](universal-radio-hacker-urh.md) — but neither fits in a pocket or transmits. It is also the device most often misdescribed in press coverage of "car hacking": what it does to a fob is capture and replay *signals*, which is neither cloning a rolling-code fob nor the real-time forwarding of a [key-fob relay attack](concepts/key-fob-relay-attacks.md).

## Limits and safety notes

Rolling codes are the hard boundary, enforced by the official firmware itself: a dynamic-protocol capture cannot even be saved, let alone replayed as a clone (and a replayed rolling code would fail anyway — the receiver expects the next counter value, and stray replays can desynchronise the genuine fob). Transmit is region-gated: send stays disabled until a firmware update sets the device's region, and the official regional table then unlocks only the civilian bands for that region (e.g. 433.05–434.79 and 868.15–868.55 MHz in the EU/UK; 304.10–321.95, 433.05–434.79, and 915.00–928.00 MHz in the US/Canada group). Transmitting on vehicle bands without authorisation is illegal in most jurisdictions regardless of the tool. Treat third-party "unlock" claims for modern vehicles as unverified unless a primary source demonstrates the specific protocol break — and note that community/fork firmware behaviour is outside the official documentation relied on here.

## Status and sources

Checked 2026-11-01. **Active**: the firmware repository is not archived, its latest push is dated 2026-10-30, and the latest firmware release is 1.5.1 (2026-10-15). This records observed project activity, not a promise of support. Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Official product site](https://flipperzero.one/)
- [Sub-GHz Read documentation](https://docs.flipper.net/zero/sub-ghz/read)
- [Firmware release 1.5.1](https://github.com/flipperdevices/flipperzero-firmware/releases/tag/1.5.1)

## Related

- [Flipper-ARF](flipper-arf.md)
- [KeyFob Analysis Toolkit (KAT)](keyfob-analysis-toolkit-kat.md)
- [rtl_433](rtl-433.md)
- [Universal Radio Hacker (URH)](universal-radio-hacker-urh.md)
- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md)
