---
title: "byd-dolphin-hacking"
summary: "Reverse engineering of the BYD Dolphin DiLink 3 head unit (Android 10 on a Qualcomm QCM6125), documenting its MCU and CAN interfaces, OTA update paths, and…"
type: entity
category: "Infotainment and IVI"
url: "https://github.com/wheregoes/byd-dolphin-hacking"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Reverse engineering of the BYD Dolphin DiLink 3 head unit (Android 10 on a Qualcomm QCM6125), documenting its MCU and CAN interfaces, OTA update paths, and NFC digital key, along with permission-bypass and root-level service findings."
related: [can-injection, secure-firmware-updates, ic1101, ivi-update-trust, ivi-runtime-privilege]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/wheregoes/byd-dolphin-hacking"
    retrieved: 2026-11-01
  - url: "https://github.com/wheregoes/byd-dolphin-hacking/blob/master/README.md"
    retrieved: 2026-11-01
---

Reverse engineering of the BYD Dolphin DiLink 3 head unit (Android 10 on a Qualcomm QCM6125), documenting its MCU and CAN interfaces, OTA update paths, and NFC digital key, along with permission-bypass and root-level service findings.

## What it is

A community research repository — documentation plus on-device scripts — that reverse-engineers the infotainment system of the BYD Dolphin (model years 25/26): a DiLink 3.0 head unit running Android 10 on a Qualcomm QCM6125. It is not an exploit kit; it is a worked map of the platform built from ADB exploration, APK decompilation and CAN bus probing, covering the Android↔MCU interface, the instrument cluster, the three OTA update paths, the cloud remote-control path, and the NFC digital key. Its security content is substantial: an unlocked bootloader from the factory, a client-side permission bypass for BYD's vehicle API, an unauthenticated firmware-update Binder service, and CAN frame injection from an unprivileged shell. The repository carries no licence file, so reuse terms are unstated.

## How it works

Access starts with ADB over the car's Wi-Fi, or APK sideloading without root via USB (a universal DiLink 3 master password, printed in the README, gates the USB path; sideloading policy varies by region). The architecture the repo maps: app → BYDAutoManager → Binder → DiCarServer (UID 1000) → `/dev/spidev_ivi` → MCU, with an SPI packet format that carries **no CRC and no HMAC**. The bootloader ships **unlocked** from the factory (verified-boot state "orange"), which is also what makes optional Magisk rooting via fastboot possible — though most findings work without root.

The findings the repo documents, at headline level: most `BYDAUTO_*` vehicle permissions are `protectionLevel=normal`, and `BydPermissionContext` overrides the permission check client-side and auto-grants them — giving a sideloaded app full climate control and more; the bypass fails where the check is server-side. Starting the factory ClusterDebug app and broadcasting `com.byd.cluster.spi` injects raw CAN frames through the MCU from an unprivileged shell — no root, no OBD-II dongle. The `upgrade_server` Binder service performs **no permission check** and accepts firmware-update calls from the shell UID, given a valid signed package. The cloud path is traced end to end (app → BYD Cloud → AES-encrypted TCP → cloudmanager → MCU): the MCU leg itself is unencrypted, and one cloud channel accepts all feature IDs — but remote actuation stops at an MCU GUID gate whose value exists only in a root process's memory. Three OTA paths are documented (cloud COTA, FOTA with mutual TLS, USB OTG), as is the NFC digital key. The README also identifies the bundled root-running AirPlay service as CVE-2025-24132 (the repo's identification, attributed here as such) and notes 13+ BYD services running as root that accept Binder calls from the shell UID. Root, where used, adds direct SPI access past the Java API's size cap, /system writes and full UDS coding.

## Where it fits

The section's only BYD / Chinese-OEM entry and its most complete single-vehicle IVI case study: where [ic1101](ic1101.md) documents a previous-generation Android head unit (Honda/Tegra), this documents a current one, and the Android attack surface — Binder services, permission models, sideloading policy — is the shared thread. Its CAN injection path is a worked instance of the KB's [CAN injection](concepts/can-injection.md) concept reached from the head unit rather than the OBD-II port, and its OTA paths plus the unauthenticated update service belong to the update-integrity theme of [secure firmware updates](concepts/secure-firmware-updates.md), from the attacker's side. It complements the section's firmware-modification tools ([gen5fw](gen5fw.md), [Chimaera](chimaera.md)) by showing the runtime/API layer above the firmware rather than the firmware image itself.

## Limits and safety notes

Scope is one vehicle (BYD Dolphin 25/26) on one tested firmware (`13.1.32.2507250.1`); the README itself warns newer BYD updates "may change or break things — no guarantees", and several findings are region-dependent. The repo's own risk language is explicit and is part of the artefact: unofficial, no BYD affiliation, educational/interoperability purposes, modifying vehicle software may void warranty or violate BYD's terms, authors assume no liability. Documented dead ends are also part of the artefact and are not upgraded here: custom AVAS audio upload is unconfirmed, AVAS volume is MCU-hardcoded, hazard flash is stopped by the MCU GUID gate, and whether the kernel's OverlayFS escalation pair actually works on this unit is unresolved in the repo's own write-up. The CVE-2025-24132 applicability to this head unit is the repo's identification of the bundled AirPlay implementation, not independently confirmed against a BYD or vendor source.

## Status and sources

Checked 2026-11-01. **Active**: not archived; created in May 2026, it accumulated 174 commits in five months with the latest on 2026-10-07 — under four weeks before this check — and the recent work is the author correcting his own earlier unverified claims, i.e. a living research project, not a finished dump. There are no releases. Documentation claims above come from the following primary sources; no vehicle was modified for this page.

- [Upstream repository](https://github.com/wheregoes/byd-dolphin-hacking)
- [Upstream README](https://github.com/wheregoes/byd-dolphin-hacking/blob/master/README.md)

## Related

- [CAN injection](concepts/can-injection.md)
- [Secure firmware updates](concepts/secure-firmware-updates.md)
- [ic1101](ic1101.md)
- [IVI update-path trust](concepts/ivi-update-trust.md)
