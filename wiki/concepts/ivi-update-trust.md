---
uid: 01a19d3c-af66-77c1-b415-16df9b0b7742
title: "IVI update-path trust"
summary: "How head-unit update trust anchors fail across six IVI platforms: absent checks, a public test key, a fleet-wide key, CRC-only integrity, patchable verifiers."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [byd-dolphin-hacking, chimaera, gen5fw, ic1101, mmi3g-toolkit, q50-reverse-engineering, secure-firmware-updates, simos18-sboot, secv-securing-connected-vehicles-with-hardware-trust-anchors, ivi-runtime-privilege]
sources:
  - url: "https://github.com/wheregoes/byd-dolphin-hacking/blob/master/README.md"
    retrieved: 2026-11-01
  - url: "https://link.springer.com/article/10.1007/s11416-024-00522-4"
    retrieved: 2026-11-01
  - url: "https://github.com/rgerganov/gen5fw/blob/master/README.md"
    retrieved: 2026-11-01
  - url: "https://github.com/librick/ic1101/blob/main/README.md"
    retrieved: 2026-11-01
  - url: "https://github.com/dspl1236/MMI3G-Toolkit/blob/main/README.md"
    retrieved: 2026-11-01
  - url: "https://github.com/oneezeeroo/Q50-Reverse-Engineering/blob/main/README.md"
    retrieved: 2026-11-01
---

Every head unit in this KB's IVI section decides what code it will run by trusting something on its update or package path: a signature, a key, a permission check, a checksum. Six platforms document that decision point — and in five of them the anchor did not bind. The failures are almost never broken cryptography: they are anchors that were missing, public, shared fleet-wide, unkeyed, or implemented in software the attacker could rewrite or interrogate — plus one platform, the Q50, where the anchor has not been located at all. This page is the taxonomy of those failures.

## The failure classes

Each class names where the trust decision lived and why it did not bind — not the technique used against it. Platforms span classes (Chimaera 5 + 6; gen5fw 3 + 4; MMI 4 + 5 on different anchors). Scoped to these six documented platforms.

1. **No check at the gate** — no authorisation decision at the entry point, or verification shipped disengaged. (BYD)
2. **The trusted key is public** — verification sound and enforced, but the trusted key is a published test key. (Honda)
3. **One key for the whole fleet** — one symmetric key/IV in every unit; one extraction breaks the fleet. (Gen5)
4. **Integrity without authenticity** — the only integrity mechanism is an unkeyed, recomputable checksum (CRC32). (Gen5, MMI)
5. **The check is patchable in the trusted binary** — a real signature check whose verifier is mutable software in the domain it verifies. (Gen5W_L, MMI)
6. **The trusted binary leaks its own key** — the secret's holder discloses it under exploitation. (Gen5W_L)
7. **Verification boundary unmapped** *(open case)* — format and encryption documented; whether verification gates installation is not established. (Q50)

## The platforms

**[BYD Dolphin](../byd-dolphin-hacking.md)** (DiLink 3, Android 10). Delivery: three OTA paths (cloud COTA, FOTA with mutual TLS, USB OTG) plus the on-device `upgrade_server` Binder service, which performs **no permission check** and accepts firmware-update calls from the shell UID, given a valid signed package — nothing decides *who may invoke it*. Above it, the bootloader ships **unlocked** from the factory (verified-boot state "orange"). Both gates stand open on the caller side.

**[Chimaera — Hyundai/Kia Gen5W_L](../chimaera.md)** (LG). Delivery: the normal USB/SD update path. Anchor: each file carries a SHA-256 and a digital signature verified at install time. Failure, twice over: a format-string flaw in the statically linked MbedTLS inside the decryption binary `DecryptToPIPE` made the binary **print its own AES key** from memory; and rather than forge signatures, the team **patched the signature check out of the installer binaries**, the modified installer carried in the custom firmware. (Four CVEs followed.)

**[gen5fw — Hyundai/Kia Standard Gen5](../gen5fw.md)** (Mobis). Delivery: USB drive in a hidden recovery flow. The firmware encryption is a **single hardcoded AES-128-CBC key and IV shared by every unit**; the `file_info` manifest guarding integrity is **CRC32s only**; there are no per-device keys and no signature gate on the recovery path as documented. The `update_package.zip` password is likewise *derived from static `build.prop` properties*.

**[ic1101 — Honda Civic 2016–2021](../ic1101.md)** (Mitsubishi Electric, Android). Delivery: an update file on a USB drive; the headunit reboots into recovery and applies it. Anchor: Android's update signature verification, working exactly as designed. Failure: the key it trusts is the **widely known AOSP test key**, so a self-built package signed with it passes the check and executes. Sound cryptography, failed key management.

**[MMI3G-Toolkit — Audi/VW MMI 3G / 3G+](../mmi3g-toolkit.md)** (Harman Becker, QNX). Delivery: the manufacturer's own SD-card script-execution mechanism. FSC activation codes are RSA-verified by the head-unit application, and a **2-byte patch** replaces the call to the RSA signature-decrypt routine with a constant success return (a patch to the user's own unit binary, not key recovery); and in the firmware update format, **every integrity check is CRC32**.

**[Q50 Reverse Engineering — Infiniti Q50 InTouch](../q50-reverse-engineering.md)** (Connexis/YGOMI). Delivery: a service watches USB media and parses EPK packages. Mapped: the EPK v2 format and its hybrid encryption (a 256-byte RSA-wrapped key field, AES-CBC payloads). Not mapped: the **signature/verification boundary in the install path is explicitly not yet mapped**. Q50 cannot be assigned to any failure class — nor cleared of them.

## The same anchors, on the ECU side

The KB's clearest ECU-side case is [Simos18 SBOOT](../simos18-sboot.md): a supplier boot stage defeated without breaking any signature — its boot password rests on a weak PRNG seed/key, and a CRC bounds-check flaw lets the password be recovered by CRC back-calculation (password recovery, not code execution). It also holds the KB's one clear **working control**: the application (ASW) bootloader above SBOOT carries HSM-backed cryptography and, as documented, *held* — the chain routes around it through the weaker stage. [VW_Flash](../vw-flash.md) ships the patchable-verifier class for engine ECUs (RSA-bypass patches enabling unsigned code) — whose own limit is the axis's other end: other Simos units are flashable only if RSA validation "has already been disabled". Anchors grade out as present-and-holding, present-but-patchable, or absent-or-public; a strong stage beside a weak parallel path is a system failure with a component success inside it.

## The delivery vector

Removable media is the delivery vector in **five of the six** platforms — and in those cases it is **manufacturer-provided functionality**: the normal update path (Gen5W_L), a built-in script mechanism (MMI), a stock media-watcher service (Q50), the platform's own recovery flow (Gen5, Honda). In the sixth (BYD), USB is one of three paths and the failure lives at an on-device service gate instead. The medium is not where the platforms differ — the anchor is. The ECU side differs again: in this KB's evidence, ECU flashing runs over the **diagnostic bus** (UDS, KWP2000), gated where gated by seed/key — two update surfaces, sharing anchor classes, failing at different gates.

## The open case

Q50 earns its row because **encryption is not verification**: its package encryption is fully mapped while its verification boundary is explicitly unmapped. Classification requires a *located* anchor; until the boundary is mapped, absence of a known bypass is absence of a map, not evidence of a sound anchor. When it is established, Q50 moves into one of classes 1–6 — or becomes the taxonomy's first documented sound IVI anchor. (It ships no installer or keys by deliberate choice.)

The defensive answer exists in the KB as [secure firmware updates](secure-firmware-updates.md): authenticity needs a secret the attacker does not hold — signatures over hashes, with keys distributed, thresholded and revocable. Each class above is a way a production platform shipped without one of those properties. The honest caveat rides with it: that design answer (Uptane) has **no named production deployment**, and the KB's working controls appear only as asides inside failure write-ups — the positive side of this record is thin.

## Related

- [BYD Dolphin hacking](../byd-dolphin-hacking.md)
- [Chimaera](../chimaera.md)
- [gen5fw](../gen5fw.md)
- [ic1101](../ic1101.md)
- [MMI3G-Toolkit](../mmi3g-toolkit.md)
- [Q50 Reverse Engineering](../q50-reverse-engineering.md)
- [Secure firmware updates](secure-firmware-updates.md)
- [Simos18 SBOOT](../simos18-sboot.md)
- [VW_Flash](../vw-flash.md)

Checked 2026-11-01 against the KB's full entity pages cited; no claim here goes beyond what those pages establish.
