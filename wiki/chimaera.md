---
uid: 01a19d3c-af57-74a4-9a6c-54c6eb3faec9
title: "Chimaera"
summary: "Research framework for IVI (In-Vehicle Infotainment) firmware reverse engineering and exploitation targeting Hyundai/Kia Gen5W_L systems."
type: entity
category: "Infotainment and IVI"
url: "https://link.springer.com/article/10.1007/s11416-024-00522-4"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Research framework for IVI (In-Vehicle Infotainment) firmware reverse engineering and exploitation targeting Hyundai/Kia Gen5W_L systems."
related: [gen5fw, secure-firmware-updates, ivi-update-trust]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://link.springer.com/article/10.1007/s11416-024-00522-4"
    retrieved: 2026-11-01
  - url: "https://api.crossref.org/works/10.1007%2FS11416-024-00522-4"
    retrieved: 2026-11-01
---

Research framework for IVI (In-Vehicle Infotainment) firmware reverse engineering and exploitation targeting Hyundai/Kia Gen5W_L systems.

## What it is

Chimaera is the name of an academic attack — and the two Python tools built to execute it — published as a peer-reviewed paper: Costantino, De Vincenzi & Matteucci (CNR, Italy), "A vehicle firmware security vulnerability: an IVI exploitation", *Journal of Computer Virology and Hacking Techniques* 20(4), published online 2024-05-08, DOI 10.1007/s11416-024-00522-4 (full text open access). The work is a vulnerability assessment of the **Gen5W_L** IVI firmware — the LG Electronics–based widescreen head units fitted across Hyundai, Kia and Genesis since 2016 — carried out on one unit from a Hyundai IONIQ EV running a named firmware version (~27 GB, obtained via Hyundai's free Navigation Updater). It ends with fully customised firmware installed on the unit and post-exploitation control reaching the car's CAN buses. Responsible disclosure to Hyundai Motor Group produced four CVEs: **CVE-2023-26243, CVE-2023-26244, CVE-2023-26245, CVE-2023-26246**. The same team's earlier Gen5 work produced CVE-2020-8539 and the KOFFEE exploit; Chimaera is the Gen5W successor study, not the same artefact. One precision on the list wording: the paper presents Chimaera as the attack and names two scripts as its tooling — neither the paper nor the publisher page links a public code repository, and none was found, so the tools are described here as *described in the paper*, not as downloadable software.

## How it works

Each firmware file is content + a terminator string + a SHA-256 + a digital signature, all encrypted; the install-time work is done by the binaries `DecryptToPIPE` (decryption during installation) and `AppDMClient`/`AppUpgrade` (installation checks, including signature verification). The break is a **format-string flaw in the statically linked MbedTLS library inside `DecryptToPIPE`**: by patching and executing the binary, the team made it print its own secrets from memory — the AES-CBC-128 key — and from there reconstructed the full decryption flow, recovered the RSA public key and wrapped-key handling, and discovered the IV-generation algorithm, so they could reproduce both decryption *and* encryption of any firmware file exactly as the installer performs it. Rather than forge signatures, they patched the signature check out of the installer binaries, so customised files are accepted by the modified installer carried in the custom firmware itself. The two tools (§12 of the paper): `chimaera_build` automates re-encryption, using two Docker containers hosting the *patched* `DecryptToPIPE` as an oracle to leak the correct IV and SHA-256 for a file, then encrypting with the generated values; `chimaera_image` converts UI images to and from the firmware's .astc formats, including a double-compressed variant whose custom header the team reverse-engineered. Installation is through the normal USB/SD update path. Post-exploitation: the head unit sits on the multimedia bus with the instrument cluster and its processes intercommunicate over D-Bus; the team forged CAN frames into the M, B and C buses — triggering services as if from the Bluelink telematics app — and took control of the head unit's cellular connection, routing Internet traffic through the car's modem.

## Where it fits

The section's academic anchor for Hyundai/Kia. [gen5fw](gen5fw.md) is the community-tooling counterpart for the *Standard-class Gen5* (Mobis) units — a different hardware/software platform — while Chimaera is the peer-reviewed, CVE-producing study of the *Gen5W_L* (LG) units; the two pages cross-link precisely on that platform split, and neither covers the other's head units. Thematically it is the offensive mirror of [secure firmware updates](concepts/secure-firmware-updates.md): an update chain with real cryptography (AES-CBC + RSA + SHA-256 + signatures) that still fell, because the decryption binary leaked its own keys through a format-string flaw and the signature check lived in a patchable binary. It also pairs with the team's own predecessor (KOFFEE / CVE-2020-8539 on Gen5) as the same-team, next-platform-generation data point.

## Limits and safety notes

Target scope is exact: one LG Gen5W_L unit and firmware version (EUR region). The authors themselves state the limitation — the approach leans on a vulnerability class in the MbedTLS library, but the exploitation and installation are specifically targeted at a Hyundai Motor Group IVI system and procedures "may vary significantly" for other brands. Whether any given production firmware still contains the flaws is outside the paper; the attack is not presented here as current against patched units. The ordering matters and is kept explicit: the work required the physical unit and its firmware image, and the CAN/cellular post-exploitation starts *after* custom firmware is installed (or via a separate 1-day) — nothing in the paper is a remote-only exploit of an unmodified car. The mapping of the four CVEs to the individual flaws is not itemised in the paper portions read, so the CVEs are listed without an invented per-CVE mapping.

## Status and sources

Checked 2026-11-01. **Unknown**: the artefact is a finished, peer-reviewed publication of May 2024 with no associated public code repository in the sources checked — a completed research output with no ongoing project state observable, the same reasoning this KB records for Simos18_SBOOT. Bibliographic facts were verified two ways (the Springer article page and the Crossref record for the DOI). Documentation claims above come from the following primary sources; no head unit was modified for this page.

- [The paper (Springer, open access)](https://link.springer.com/article/10.1007/s11416-024-00522-4)
- [Crossref record](https://api.crossref.org/works/10.1007%2FS11416-024-00522-4)

## Related

- [gen5fw](gen5fw.md)
- [Secure firmware updates](concepts/secure-firmware-updates.md)
- [IVI update-path trust](concepts/ivi-update-trust.md)
