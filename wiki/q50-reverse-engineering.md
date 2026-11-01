---
title: "Q50 Reverse Engineering"
summary: "Independent reverse-engineering research into the Infiniti Q50 infotainment platform's Linux/Android environment, documenting its EPK firmware package…"
type: entity
category: "Infotainment and IVI"
url: "https://github.com/oneezeeroo/Q50-Reverse-Engineering"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Independent reverse-engineering research into the Infiniti Q50 infotainment platform's Linux/Android environment, documenting its EPK firmware package format, code-signing process, and USB app-installation flow."
related: [ic1101, mmi3g-toolkit, secure-firmware-updates]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/oneezeeroo/Q50-Reverse-Engineering"
    retrieved: 2026-11-01
  - url: "https://github.com/oneezeeroo/Q50-Reverse-Engineering/blob/main/README.md"
    retrieved: 2026-11-01
---

Independent reverse-engineering research into the Infiniti Q50 infotainment platform's Linux/Android environment, documenting its EPK firmware package format, code-signing process, and USB app-installation flow.

## What it is

Independent, single-author reverse-engineering research into the Infiniti Q50's infotainment (InTouch) platform — a hybrid Linux/Android IVI system whose application layer is supplied by Connexis/YGOMI. The repository documents the platform's architecture and its EPK application-package format — envelope layout, hybrid RSA/AES encryption, and the USB app-installation flow — from decompiled software, one known working community package, and small reproduction tools. It is deliberately research-only: the author publishes no proprietary firmware, no device keys, and no working install pipeline. Licence: MIT.

## How it works

The Q50 image has a Linux-oriented side and a modified **Android 2.3** environment (the app layer targets Android API 10); Connexis/YGOMI components provide the application-management stack, including versioned EPK parsers, and the stock HomeScreen itself reads IVI application metadata. The USB install path is traced: a service watches removable media, parses EPK packages found there, and passes normal payload files toward the IVI package manager — USB media is the app-delivery vector, structurally the same entry pattern as the other platforms in this section. The **EPK v2 format** is mapped from the samples: a 268-byte envelope with big-endian numeric fields before typed payload blocks (the known working community package was EPK v2, payload type 2, carrying one APK block). Encryption is **hybrid**: temporary key material RSA-wrapped (a 256-byte wrapped-key field) with AES-CBC payload encryption. The README is careful to separate EPK payload encryption from APK signing — the reference APK carries a normal developer-style JAR certificate — and the exact signature/verification boundary in the install path is explicitly listed as **not yet mapped**. Vehicle data does not reach apps as raw CAN: the reference app reads it through Android `SensorManager` with an IVI-specific permission (`IVI_CAN_READ`), and the repo's sensor map documents observed mappings (sensor type 13 = RPM, plus temperatures, speed, throttle, torque, G-force, gear, power, TPMS). The shipped tooling is deliberately minimal: `epk_inspect.py`, a read-only inspector that reports an EPK file's structure without decrypting payloads and contains no device keys, and a source-only example app skeleton that — the README stresses — cannot simply be copied to USB and installed. Findings are graded in the README as Confirmed / Observed in specific reference material / Still being tested, and this page mirrors that grading.

## Where it fits

The section's documentation-first entry: where [ic1101](ic1101.md) ships an exploit-capable toolchain and [MMI3G-Toolkit](mmi3g-toolkit.md) ships a working modification toolkit, this repo's deliverable is a verified architecture and format model of a platform nobody else in the KB covers, with the install path's trust boundary honestly marked as the open question. Its EPK analysis belongs to the same family as the other two entries' package work (Honda update files, the MMI update format) — three IVI packaging systems with three different trust designs. The planned next phase (passive CAN capture of drive-mode and tune switching) would extend it toward the CAN sections, but that work is a roadmap, not a result. Concept link: [secure firmware updates](concepts/secure-firmware-updates.md) — the EPK envelope is another instance of package encryption being present while the verification story is the part that decides security.

## Limits and safety notes

Sample-bound by the author's own framing: findings "describe the samples and software revisions examined" and are not claims that every Q50 revision behaves identically. Explicitly unmapped, and kept unmapped here: differences across model years, trims and engines; the complete meaning of EPK payload-type values; the exact signature and verification boundary; required permissions and sensor indexes in practice; and the final Linux/Android boundary of the USB install flow. No capability is shipped — no installer, no keys, no firmware, no recovered third-party APKs — by deliberate authorial choice, repeatedly stated; citing this entry as a Q50 app-installation method would misread it. The CAN-capture/tune-switching phase is a documented roadmap (October 2026) with no results yet. The README's responsible-research framing is standard: test only owned/authorised hardware; incompatible packages can leave a unit unstable or unusable. Two facts are **not stated** in the sources: the underlying SoC/hardware platform, and which Q50 model years the examined software came from. The repo also discloses that agentic AI assisted parts of the research and editing — worth knowing when weighing its prose, though its findings are graded and sample-bound.

## Status and sources

Checked 2026-11-01. **Active**: created 2026-09-15, it has 25 commits with the latest on 2026-10-24 — eight days before this check — adding a next-phase roadmap the author describes as ongoing; the README badges the project "active research". A young, currently worked-on research project; no releases exist, which is normal for a six-week-old documentation repo. Documentation claims above come from the following primary sources; no head unit was modified for this page.

- [Upstream repository](https://github.com/oneezeeroo/Q50-Reverse-Engineering)
- [Upstream README](https://github.com/oneezeeroo/Q50-Reverse-Engineering/blob/main/README.md)

## Related

- [ic1101](ic1101.md)
- [MMI3G-Toolkit](mmi3g-toolkit.md)
- [Secure firmware updates](concepts/secure-firmware-updates.md)
