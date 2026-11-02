---
title: "Automated Cross-Platform Reverse Engineering of CAN Bus Commands From Mobile Apps"
summary: "Wen, Zhao, Chen, and Lin, NDSS 2020. Recovers CAN command syntax and semantics for 360 car models from companion mobile apps alone, without touching a vehicle."
type: entity
category: "Research Papers"
url: "https://www.ndss-symposium.org/ndss-paper/automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps/"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Wen, Zhao, Chen, and Lin, NDSS 2020. Recovers CAN command syntax and semantics for 360 car models from companion mobile apps alone, without touching a vehicle."
sources:
  - url: "https://www.ndss-symposium.org/ndss-paper/automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps/"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.14722/ndss.2020.24231"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - canvas-fast-and-inexpensive-automotive-network-mapping
  - plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles
  - donglescope
  - canalyzat0r
  - can-injection
---

Wen, Zhao, Chen, and Lin, NDSS 2020. Recovers CAN command syntax and semantics for 360 car models from companion mobile apps alone, without touching a vehicle.

## What it is

Haohuang Wen, Qingchuan Zhao, and Zhiqiang Lin (The Ohio State University) and Qi Alfred Chen (University of California, Irvine). *Network and Distributed System Security Symposium* (NDSS 2020), San Diego, CA, February 23–26, 2020. The paper presents CANHUNTER, the first cost-effective (no real car needed) and automatic (no human intervention) system for reverse engineering CAN bus commands — both their syntactics (identifier, structure, format, concrete bytes) and their semantics (what the command does) — from car companion mobile apps alone. The state of the art it displaces is dynamic testing with real cars: trigger a physical action and watch the bus, or inject candidate messages and watch the car — hardware-hungry and error-prone, one model at a time. Companion apps change the artefact available: to offer diagnosis or remote control, an app must contain the logic to construct the CAN commands for every vehicle it supports. That embedded logic, across hundreds of apps, is a fleet-scale corpus of the manufacturers' private command sets. CANHUNTER is implemented for both platforms (≈3,000 lines of Android code, ≈2,000 of iOS); code and the recovered command set were released.

## What it showed

**How it works.** Three stages. (1) *Backward slicing*: every app must finally send its commands through the standard low-level network APIs (BLE, Bluetooth, Wi-Fi/socket, HTTP), so CANHUNTER slices backward from those APIs — data- and control-dependent, context-sensitive and interprocedural, over Soot IR for Android and IDA-Pro-decompiled code for iOS — to recover each command-generation path. Backward beats forward-from-UI on precision and also finds commands no UI element triggers. (2) *Dynamic forced execution*: the generation code normally sits behind network connections and user/vehicle authentication (a valid VIN, a paired dongle), contexts that cannot be prepared without a car — but the construction itself is independent of those inputs, because commands are embedded constants end users cannot type. CANHUNTER therefore force-executes just the sliced paths on a real phone (Frida/Cycript instrumentation, with automatic crash restart), bypassing the context checks, and logs whatever reaches the network APIs as the command syntactics. (3) *Semantics recovery*: with no car and no traffic traces, prior trace-based methods do not apply, so CANHUNTER mines code-level clues — the text of the UI element whose trigger function generated the command (running example: a button labelled "Engine Controls" in Carly for Toyota), and function-argument association, where a command constant and a meaning string are passed to the same call (present in ≈30% of apps with commands, apparently a logging/debugging habit). The same mining recovers which car model each command belongs to. Native libraries are handled by stitching JNI/virtual-call edges so the call graph stays complete.

**Scale.** Applied to all 236 free car companion apps the authors collected from Google Play and the Apple App Store in April 2019 (122 Android, 114 iOS; 146 dongle apps, 90 IVI apps), CANHUNTER extracted **182,619 syntactically unique CAN bus commands from 107 apps, 157,296 of them (86.1%) with semantics**, covering **over 360 car models from 21 manufacturers**; car-model information was recovered for 161,819 commands (88.6%). The semantics resolve to 3,439 distinct meanings — 1,309 control (door locking, horn, comfort functions) and the rest diagnosis. About 15% of the recovered commands are the standardised OBD PIDs; the other 85% are the manufacturers' private commands the paper is after. It also recovered, as by-catch, 41 unique AT commands and 267 interpreted commands (below).

**Where the commands live — the ecosystem finding.** Of the 107 productive apps, 104 are dongle apps and only 3 are IVI apps, and the asymmetry is the paper's structural result. Dongle apps construct CAN commands on the phone, in the clear: 104 of 146 dongle apps (71.2%) yielded commands directly. IVI apps mostly do not: 82 of 90 (91.1%) send *interpreted commands* — human-readable strings such as "UNLOCK" — to a cloud server or the IVI unit, which translates them into CAN commands the analyst never sees; 22 dongle apps use the same indirection inside their dongles. The 3 IVI apps that did yield CAN commands had integrated them *accidentally*, in code that can never be triggered — dead code, like the further commands found with no UI correlation anywhere, judged debugging leftovers that should have been removed before release. The remaining 20 dongle apps defeated the slicing through obfuscation.

**Correctness.** Ground truth for private commands barely exists, so validation is three-legged: public resources, cross-platform and cross-app consistency, and real-car testing — together validating 130,011 commands (71.2%). Cross-platform: 129,266 commands (70.8%) from 15 dual-platform apps matched in syntactics, with no inconsistency among the 128,200 pairs where both sides carried semantics. Cross-app: 745 overlapping pairs across 22 models and 6 apps, no inconsistency. Against public resources, 38 of 69 collected ground-truth commands matched syntactics; of 33 with recovered semantics, 30 matched — the 3 mismatches (1.2% of the 241 manually validated commands) traced to mistakes in the apps' own semantics strings, not to CANHUNTER. Real-car testing ran the Carista app's commands against a 2014 Toyota RAV4 (88 commands) and a 2014 Toyota Corolla (84): every intercepted command matched, and the corresponding physical behaviours (e.g., disabling wireless door locking) were observed.

## Where it fits

CANHUNTER inverts the direction of the KB's other CAN reverse-engineering paper. [CANvas](canvas-fast-and-inexpensive-automotive-network-mapping.md) (USENIX Security 2019) works from the bus inward — a real car, an OBD-II tap, clock offsets and forced bus-off isolation — and recovers *topology*: which ECU transmits and which receive each ID, with no payload semantics. CANHUNTER works from the software outward — no car at all — and recovers *syntax and semantics*: the exact command bytes and what they do, with no topology. Together they are the structural and the semantic half of knowing a vehicle's command set (comparison is this page's, not either paper's). Against the manual capture-and-correlate workflow of the CAN Bus Analysis tools ([CANalyzat0r](canalyzat0r.md) and its peers — do an action, watch which bits change), CANHUNTER automates the same goal from a different artefact, at a different granularity: whole commands with function labels, not bit-level signal boundaries, scalings, or DBC definitions for periodic broadcast traffic, which it does not produce. The dongle half of its corpus is the same ecosystem the lead author's [Plug-N-Pwned](plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles.md) (USENIX Security 2020, cited here as in-press) audits from the device side — the apps CANHUNTER mines are the phone half of that attack surface, and its [DongleScope](donglescope.md) tooling is the sibling artefact. For the [CAN injection](concepts/can-injection.md) concept, the paper measures how widely precise, semantics-labelled command knowledge — injection's prerequisite — was already distributed in 2019: in free apps anyone could download.

## Limits and safety notes

As the paper states them: the analysis **assumes unobfuscated apps** — control-flow obfuscation breaks backward slicing, and 20 of 146 dongle apps were already lost that way in 2019; it covers only commands sent through the APIs it slices from, so false negatives are possible by construction. The validation ceiling is honest: just over 70% of commands could be validated by any method available, cross-validation assumes independent implementations do not share the same developer mistakes (the 3 known false positives are exactly that failure, inherited from the apps), and real-car ground truth covers two Toyota models from one app. Paid apps (71) were not collected; the corpus is an April 2019 snapshot. On the dual-use side, the authors' framing is that these commands were already effectively public — shipped in free apps — and their discussion is a countermeasure section: interpreted commands (keep the CAN bytes server- or firmware-side, as the IVI ecosystem does) and anti-analysis techniques (encrypt the embedded commands, obfuscate control flow). This page likewise treats the corpus as a fact about exposure, and reproduces no command tables.

## Status and sources

Status: **published** — *Proceedings of NDSS 2020*, Internet Society, ISBN 1-891562-61-4. **DOI: 10.14722/ndss.2020.24231 — verified against Crossref (2026-11-01): the record's title, all four authors, venue (NDSS 2020, San Diego), and publisher match the paper**, and its primary resource is the official PDF read here in full, 2026-11-01. Tool and recovered commands: github.com/OSUSecLab/CANHunter, as cited in the paper.

## Related

- [CANvas: Fast and Inexpensive Automotive Network Mapping](canvas-fast-and-inexpensive-automotive-network-mapping.md) — the bus-side counterpart: topology without semantics, to this paper's semantics without topology
- [Plug-N-Pwned](plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles.md) — the same lab's audit of the dongle devices whose apps supply most of CANHUNTER's corpus
- [DongleScope](donglescope.md) — the sibling OSU SecLab tool for the dongle half of this ecosystem
- [CANalyzat0r](canalyzat0r.md) — the manual capture-and-correlate workflow CANHUNTER automates from a different artefact
- [CAN injection](concepts/can-injection.md) — the concept whose prerequisite knowledge this paper measures in the wild
