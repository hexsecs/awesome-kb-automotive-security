---
uid: 01a19d3c-af90-7583-a351-c1e70b393d6e
title: "Flipper-ARF"
summary: "Automotive-focused firmware fork for Flipper Zero supporting Keeloq, rolling codes, and VAG protocol analysis."
type: entity
category: "RF and Key Fob Analysis"
url: "https://github.com/D4C1-Labs/Flipper-ARF"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Automotive-focused firmware fork for Flipper Zero supporting Keeloq, rolling codes, and VAG protocol analysis."
related: [flipper-zero, keyfob-analysis-toolkit-kat, rolling-code-failure-classes]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/D4C1-Labs/Flipper-ARF"
    retrieved: 2026-11-01
  - url: "https://github.com/D4C1-Labs/Flipper-ARF/blob/main/README.md"
    retrieved: 2026-11-01
---

Automotive-focused firmware fork for Flipper Zero supporting Keeloq, rolling codes, and VAG protocol analysis.

## What it is

An independently developed [Flipper Zero](flipper-zero.md) firmware fork (GPL-3.0), based on Unleashed Firmware but heavily modified: it removes the stock firmware's general-purpose functions and focuses exclusively on automotive research — in its README's words, a "high-compatibility, protocol-focused build" aimed at "automotive remote protocols, rolling code behavior, and keyfob ecosystem compatibility". Where official firmware deliberately restricts rolling-code handling, this fork's design philosophy is "clean and accurate protocol implementation, controlled rolling counter handling, automotive-specific encoder accuracy".

## How it works

The substance is a protocol table far broader than stock firmware's Sub-GHz set, with encoder and decoder support marked per system. Automotive families with both encoder and decoder include VAG Group, Porsche, PSA (with a README showcase of built-in PSA XTEA decryption), Ford V0/V1, Fiat, Mazda Siemens, Kia/Hyundai V0–V7, Subaru, Suzuki, Mitsubishi, Honda (including a static variant), Star Line, Scher-Khan (including Magic Code), Sheriff, and Chrysler/Dodge/Jeep FOBIK. A few are decode-only (Fiat Marelli/Delphi, Renault Marelli). KeeLoq sits in a separate Gate/Access group alongside Nice, CAME, FAAC SLH, Somfy, and other gate remotes, with general static/rolling protocols (Princeton, Linear, Security+ 1.0/2.0, MegaCode, and more) retained. Showcase screenshots name a Sub-GHz scanner, a KeeLoq key manager, and a counter brute-force scene. It builds and flashes with the standard Flipper `fbt` tooling. Its README positions it against the published RKE cryptanalysis literature (the KeeLoq breaks, RollJam/RollBack/Rolling-PWN) as a research companion to that work.

## Where it fits

Flipper-ARF is what official [Flipper Zero](flipper-zero.md) firmware declines to be: a single build whose whole surface is keyfob/alarm/gate protocol emulation and analysis, trading away the general-purpose app ecosystem. The relationship runs downstream, too — the [KeyFob Analysis Toolkit (KAT)](keyfob-analysis-toolkit-kat.md) ports several Flipper-ARF protocols into its own decoder set. Scope as documented is Sub-GHz remote/RKE only: the README shows no OBD, CAN, UDS, or transponder functionality, so immobiliser work still belongs to near-field tools such as [Proxmark3](proxmark3.md).

## Limits and safety notes

The README's table is a support claim, not a test report: no vehicle test matrix or success rates are published, several entries lack CRC, and effectiveness against a specific vehicle is unverified from primary sources. There is no stable release channel — every published build is a `dev-*` build, so treat builds as snapshots of a moving tree. Rolling-code emulation and counter brute-forcing are exactly the capabilities official firmware withholds; the README's disclaimer restricts use to educational, research, and interoperability purposes with explicit permission, "AS IS" without warranty. Emulating a fob you do not own, or probing a vehicle you may not test, is outside both the disclaimer and the law in most jurisdictions.

## Status and sources

Checked 2026-11-01. **Active**: the repository is not archived, its latest push is dated 2026-10-30, and dev builds publish continuously (the latest, dev-7e3d1081, is dated 2026-10-30). Commit messages are terse ("update 5"), so activity is verifiable while the content of individual changes is not described. This records observed project activity, not a promise of support. Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream repository](https://github.com/D4C1-Labs/Flipper-ARF)
- [Upstream README](https://github.com/D4C1-Labs/Flipper-ARF/blob/main/README.md)

## Related

- [Flipper Zero](flipper-zero.md)
- [KeyFob Analysis Toolkit (KAT)](keyfob-analysis-toolkit-kat.md)
