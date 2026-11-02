---
title: "Proxmark3"
summary: "Industry-standard RFID/NFC research tool for reading, cloning, and emulating immobilizer transponders at 125kHz and 13.56MHz."
type: entity
category: "RF and Key Fob Analysis"
url: "https://proxmark.com/"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Industry-standard RFID/NFC research tool for reading, cloning, and emulating immobilizer transponders at 125kHz and 13.56MHz."
related: [flipper-zero, dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://proxmark.com/"
    retrieved: 2026-11-01
  - url: "https://proxmark.com/proxmark-3-hardware/proxmark-3-rdv4"
    retrieved: 2026-11-01
  - url: "https://github.com/RfidResearchGroup/proxmark3"
    retrieved: 2026-11-01
  - url: "https://github.com/RfidResearchGroup/proxmark3/releases/tag/v4.23346"
    retrieved: 2026-11-01
---

Industry-standard RFID/NFC research tool for reading, cloning, and emulating immobilizer transponders at 125kHz and 13.56MHz.

## What it is

A hardware-plus-firmware platform — the official site calls it "an RFID swiss-army tool" and "the industry standard tool for RFID Analysis" — for low-level interaction with contactless tags at two near-field bands: LF 125 kHz and HF 13.56 MHz. The current hardware is the Proxmark3 RDV4, designed and manufactured by RRG (RfidResearchGroup), whose Iceman-fork repository is also where active firmware development lives; the older Proxmark/proxmark3 repository's own README says it is no longer maintained and points to the Iceman fork. (A newer Proxmark 5 generation also exists; it is a different device and not this page's subject.)

## How it works

Everything is centimetre-scale: the RDV4's quoted antenna performance is 70 mm at LF and 88 mm at HF, with the tag presented to the device. The command set covers reading/searching (`lf search`, `hf search`), sniffing a reader↔tag exchange, emulation (the Proxmark itself impersonates a tag from emulator memory), cloning (dump a source tag and write/restore it to a blank — T5577 rewrites and MIFARE restores are the documented sequences), and key-checking/cracking commands. The automotive surface is the LF transponder families the firmware documents in depth: a full **Hitag** command family (Hitag 2, Hitag S, Hitag µ — read, dump, sniff, simulate, and `crack2`/`chk` key tools), **EM4x70** — the firmware's own doc heads it "EM4x70 (aka ID48, aka Megamos)" — with auth, write, unlock, and partial-key brute-force commands, and PCF7931 read/write. One honesty note: the primary sources document this *chip-family support*; they do not themselves use the word "immobilizer" — that framing is the list summary's, and the chip-to-vehicle mapping is the [Megamos research](dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md) in this KB, not a proxmark.com claim.

## Where it fits

Proxmark3 is the near-field half of this section: everything else here works over the air at Sub-GHz, while the transponder in a key head talks at 125 kHz across a few centimetres — a physically different conversation (typically the start-authorisation check, versus the fob's remote-entry transmission). A [Flipper Zero](flipper-zero.md) also reads LF tags, at hobbyist depth; Proxmark3 is the research instrument. Its three operations must not be conflated: **cloning** copies a tag's data onto another tag, **emulation** impersonates a tag, and neither is **relaying** — no relay function is documented in the primary sources, and the [key-fob relay attack](concepts/key-fob-relay-attacks.md) is a separate mechanism with separate equipment.

## Limits and safety notes

Range is the physics: millimetres-to-centimetres, tag in hand or reader in reach — nothing here reaches a fob in someone's house. Hardware choice matters more than usual: the official site warns that grey-market clones have "poor performance and lifespan", the Iceman README lists supported platforms (RDV1–RDV4, RDV3 Easy and its many clones, and others) and explicitly unsupported ones (Proxmark Evolution, Ryscorp Proxmark3 Pro — unknown pin assignments), and 256 KB generic devices must compile with reduced functionality. The firmware describes itself as bleeding-edge: "do expect significant changes to code layout on a regular basis."

## Status and sources

Checked 2026-11-01. **Active**: the canonical RfidResearchGroup/proxmark3 repository is not archived, its latest push is dated 2026-10-30 with merged PRs the same week, and the latest release is v4.23346 (2026-09-17). This records observed project activity, not a promise of support. Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Official site](https://proxmark.com/)
- [Proxmark3 RDV4 hardware page](https://proxmark.com/proxmark-3-hardware/proxmark-3-rdv4)
- [Canonical firmware repository (Iceman fork)](https://github.com/RfidResearchGroup/proxmark3)
- [Release v4.23346](https://github.com/RfidResearchGroup/proxmark3/releases/tag/v4.23346)

## Related

- [Flipper Zero](flipper-zero.md)
- [Dismantling Megamos Crypto](dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md)
- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md)
