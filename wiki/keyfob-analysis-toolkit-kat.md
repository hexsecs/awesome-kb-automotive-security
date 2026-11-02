---
title: "KeyFob Analysis Toolkit (KAT)"
summary: "Toolkit for analyzing, decoding, and retransmitting key fob signals with support for HackRF, RTL-SDR, and Flipper Zero."
type: entity
category: "RF and Key Fob Analysis"
url: "https://github.com/KaraZajac/KAT"
status: maintenance
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Toolkit for analyzing, decoding, and retransmitting key fob signals with support for HackRF, RTL-SDR, and Flipper Zero."
related: [universal-radio-hacker-urh, rtl-433, flipper-zero, flipper-arf]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/KaraZajac/KAT"
    retrieved: 2026-11-01
  - url: "https://github.com/KaraZajac/KAT/blob/main/README.md"
    retrieved: 2026-11-01
  - url: "https://github.com/KaraZajac/KAT/releases/tag/v1.3.0"
    retrieved: 2026-11-01
---

Toolkit for analyzing, decoding, and retransmitting key fob signals with support for HackRF, RTL-SDR, and Flipper Zero.

## What it is

A terminal-based RF analysis tool for automotive key fobs, written in Rust with a real-time text UI. Where the other tools in this section are general radio instruments, KAT is fob-specific end to end: live capture, decoding against a built-in library of named OEM fob protocols, matching captures against a built-in database of published fob vulnerabilities, and — with transmit hardware — encoding and sending lock/unlock/trunk/panic commands or replaying a capture. Its protocol decoders are aligned with the ProtoPirate reference implementation, and its v1.3.0 release also ports protocols from [Flipper-ARF](flipper-arf.md).

## How it works

Hardware support needs care, because the list summary overstates one leg. A **HackRF One** (or compatible) gives full receive and transmit. An **RTL-SDR** dongle is receive-only — capture and decode work, transmit commands are disabled and shown as "(no TX)". **Flipper Zero is not capture/transmit hardware for KAT**: it appears only as the `.sub` file format KAT imports and exports (KAT's own captures are its versioned `.fob` JSON). With no device attached, KAT still opens for viewing and converting captures. The demodulator is AM/OOK only — envelope detection with adaptive thresholding; there is **no FM/2FSK demodulation**, though FM-tagged protocols may decode when a strong signal produces a usable envelope. The v1.3.0 release notes put the decoder count at **32 protocols** (Kia, Ford, Chrysler, Honda, Toyota/Lexus, Land Rover, Fiat, Mazda, Mitsubishi, BMW CAS4, Porsche, Subaru, Suzuki, VAG, PSA, Scher-Khan, Star Line, and more), exposing encoding, serial, counter, key data, and CRC. Cryptographic support includes KeeLoq (with a fallback that tries every manufacturer key in an embedded keystore), AES-128, and TEA-family ciphers. Capture metadata (year/make/model/region) is matched against a built-in CVE list — the README names the RollBack and Honda replay CVEs — and flagged in a vulnerability panel.

## Where it fits

KAT is the key-fob specialist: [Universal Radio Hacker (URH)](universal-radio-hacker-urh.md) makes you derive a protocol from raw signal before anything decodes, and [rtl_433](rtl-433.md) decodes fob-shaped traffic only as one family among hundreds of ISM devices — KAT starts from the fob and its known protocol families, and adds the CVE context neither of the others carries. Its retransmission is about testing a protocol's own acceptance rules (counter handling, replay windows) on the bench; that is a different mechanism from [key-fob relay attacks](concepts/key-fob-relay-attacks.md), which forward a genuine key's live exchange and break no cryptography.

## Limits and safety notes

AM/OOK demodulation only; Ford V3, Toyota (Lexus), and BMW CAS4 are named decode-only; transmit needs a HackRF. Captures are held in memory and lost unless exported. The README's own rule is explicit: use KAT only on systems and vehicles you own or have explicit written permission to test — capturing, decoding, or transmitting vehicle-access signals without authorisation may breach computer-misuse and radio law. The licence is also non-standard: BSD-3-Clause with an added no-military/no-government restriction, which GitHub classifies as "Other" — read it before reuse.

## Status and sources

Checked 2026-11-01. **Maintenance**: the repository is not archived and development was brisk from its creation (2026-02-14) through the v1.3.0 release (2026-06-24, the latest of eight releases), but there have been no commits since 2026-06-24. That records observed activity, not a promise of support. Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream repository](https://github.com/KaraZajac/KAT)
- [Upstream README](https://github.com/KaraZajac/KAT/blob/main/README.md)
- [Release v1.3.0](https://github.com/KaraZajac/KAT/releases/tag/v1.3.0)

## Related

- [Universal Radio Hacker (URH)](universal-radio-hacker-urh.md)
- [rtl_433](rtl-433.md)
- [Flipper Zero](flipper-zero.md)
- [Flipper-ARF](flipper-arf.md)
- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md)
