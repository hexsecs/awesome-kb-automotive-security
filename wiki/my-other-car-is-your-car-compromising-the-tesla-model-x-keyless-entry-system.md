---
uid: 01a19d3c-afb0-7b17-8e93-5d8243b01d09
title: "My Other Car is Your Car: Compromising the Tesla Model X Keyless Entry System"
summary: "Wouters, Gierlichs, and Preneel, CHES 2021. Chains a BLE firmware downgrade and a key fob update flaw into unlocking and driving away a Tesla Model X."
type: entity
category: "Research Papers"
url: "https://tches.iacr.org/index.php/TCHES/article/view/9063"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Wouters, Gierlichs, and Preneel, CHES 2021. Chains a BLE firmware downgrade and a key fob update flaw into unlocking and driving away a Tesla Model X."
sources:
  - url: "https://tches.iacr.org/index.php/TCHES/article/view/9063"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.46586/tches.v2021.i4.149-172"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - fast-furious-and-insecure-passive-keyless-entry-and-start-systems-in-modern-supercars
  - sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it
  - relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars
  - key-fob-relay-attacks
---

Wouters, Gierlichs, and Preneel, CHES 2021. Chains a BLE firmware downgrade and a key fob update flaw into unlocking and driving away a Tesla Model X.

## What it is

Lennert Wouters, Benedikt Gierlichs, and Bart Preneel — imec-COSIC, KU Leuven. *IACR Transactions on Cryptographic Hardware and Embedded Systems* 2021, issue 4, pp. 149–172 (CHES 2021 Best Paper Award). A practical security evaluation of the Tesla Model X keyless entry system — and a deliberate contrast with the same lab's [Fast, Furious and Insecure](fast-furious-and-insecure-passive-keyless-entry-and-start-systems-in-modern-supercars.md) (2019), whose Model S system relied on the 40-bit DST40 cipher: the Model X system instead uses standardised symmetric- and public-key cryptography in a Common Criteria EAL5+ certified Secure Element (Infineon SLM97), present in both the key fob and the Body Control Module (BCM). The fob carries three processors: a TI CC2541 BLE SoC (plus CC2590 range extender) for car communication, a Maxim MAX2153E 22 kHz LF transponder receiver, an accelerometer (motion-based sleep), and the Secure Element, which computes every RKE token and PKES challenge response. The BCM mirrors it (Freescale SPC5605B, three CC2541s, same Secure Element). Its thesis: the Secure Element itself is never attacked — the way it is used is.

## What it showed

**The fob's BLE surface.** The fob becomes a connectable BLE peripheral only briefly — after a power cycle, or when the BCM wakes it with an LF packet. It then exposes three services: device information; TI's Over-Air-Download (OAD) firmware update service; and an APDU service relaying smart-card commands to the Secure Element (the pairing channel). The CC2541 firmware filters the APDU service with a blocklist on the APDU instruction byte — blocking, among others, the unlock-token command.

**The firmware update accepts unauthenticated images.** The fob firmware (v1.5.1; copies ship in the Toolbox software and the car's infotainment filesystem) is distributed in plaintext — header with a 16-bit CRC, the code, a SHA-1 digest, a magic value — no signature or MAC the fob acts on. The authors changed the advertised device name ("Tesla Keyfob"), recomputed CRC and SHA-1, pushed the image via OAD, and the fob accepted and ran it. Only later (§7.2) did the root cause surface: the CC2541 *was* asking the Secure Element to verify the firmware's signature — and ignoring the error status words the Secure Element returned. Anyone who can BLE-connect to a fob can thus run arbitrary code on its BLE SoC. Removing the APDU blocklist took brute-force binary patching — flipping JNZ (0x70) instructions to JZ/SJMP one at a time, flashing, testing — until the target APDU went through (hours; the patched image keeps all stock functionality).

**Waking the victim's fob.** The BCM's UDS interface (diagnostic connector) was enumerated on the bench: 54 RoutineControl routines, among them the LF wake-up transmitter and an APDU pass-through to the BCM's own Secure Element. The wake-up packet carries a 2-byte car identifier derived from the VIN — which is readable through the windshield. A modified BCM can thus wake any Model X fob paired to a chosen VIN from a few metres away, making it advertise as connectable on demand.

**The pairing protocol never checks the fob's credentials.** Pairing has two phases. In *provisioning*, the Toolbox and Tesla's backend HSM load the Tesla Root and APP CA certificates into Secure Element slots 0–1 and obtain HSM-signed certificates for fob-generated 2048-bit RSA keypairs (slots 2–4), binding VIN, Secure Element ID, and public key; the slots are then locked. In *pairing*, the Toolbox relays between the two Secure Elements: the BCM SE issues a 16-byte challenge; the fob SE signs challenge ‖ SE ID ‖ slot-3 public key with its slot-2 private key (RSA-PSS-SHA256); the BCM SE verifies the signature, generates five 128-bit AES keys, and returns them RSA-OAEP-encrypted to the slot-3 key; both sides then confirm key agreement with AES-ECB blocks around a fixed `key_auth` string. The flaw is structural: **the certificates created in provisioning are never sent to the car during pairing, so the BCM cannot verify the authenticity of the fob being paired** — provisioning can simply be skipped. The authors replaced the Secure Elements in a fob and a BCM with UART-bridged simulations (CP2102N, Python on a Raspberry Pi): their simulated fob pairs to any car — no Tesla account, no HSM, no genuine certificate — and can be re-paired indefinitely. (Fob RSA keys were also checked against ROCA — none vulnerable.)

**The chained attack (§6).** A backpack device (~USD 250: Raspberry Pi 3B+, CAN shield, the modified BCM, battery) executes: (1) wake the target car's fob by LF using its VIN; (2) BLE-connect and push the malicious firmware (~1.5 minutes, at BLE range); (3) request a valid RKE unlock token from the Secure Element through the now-unfiltered APDU service; (4) broadcast the token and unlock the car; (5) connect to the diagnostic port inside and run the pairing protocol with the simulated-Secure-Element fob; (6) drive off — the attacker's fob is now paired and starts the car anytime. The authors stress this is **not a relay attack**: no genuine fob needs to be near, or used again. PIN to Drive (disabled by default) would still block driving off — not access or pairing.

**Disclosure and the fix.** Disclosed to Tesla in August 2020; Tesla confirmed within days and paid a USD 5,000 bounty. The 2020.48 update (November 2020) pushed new fob firmware automatically, while driving. The new image carries a 256-byte signature, verified by the Secure Element (SHA-256 over the SHA-1 digest, RSA-PSS under the Tesla Root key in slot 0) — and the CC2541 now honours the result; the authors confirmed their image is rejected after the update. Residuals: the scheme still rests on a SHA-1 digest, so a chosen-prefix SHA-1 collision (Leurent–Peyrin) could revive the update flaw; the pairing protocol and the wake-up functionality were, to the authors' knowledge, unchanged; and any future code-execution bug in the CC2541 or TI's BLE stack reopens the token oracle, because the Secure Element cannot attest the software running on the chip that interfaces with it.

## Where it fits

The sequel-in-spirit to [Fast, Furious and Insecure](fast-furious-and-insecure-passive-keyless-entry-and-start-systems-in-modern-supercars.md). There, the cryptography itself was the failure — a 40-bit cipher, cloned from two elicited challenge–response pairs. Here, the cryptography is standardised, certified, and unbroken, and the failure is composition: an update path whose signature verdict was computed and then ignored, and a pairing protocol that authenticates a keypair but never the certificates that were supposed to vouch for it. The [Stealing Cars SoK](sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it.md) files this break in one line — unsigned fob firmware over BLE chained with a pairing protocol that never sends certificates — under its new-technology class; this page is the primary source behind that line, and adds the third act the SoK compresses away: Tesla's fix, which works by honouring a check that existed all along. Against the KB's [key-fob relay attacks](concepts/key-fob-relay-attacks.md) framing, the end state is neither relay (no live exchange is forwarded) nor cloning (no key material is recovered): it is *enrolment abuse* — the attacker ends with a legitimately paired fob of their own, because the enrolment protocol's authentication step is vacuous. The generalisable lesson is the paper's own: a Secure Element's guarantees end at its interface — whoever controls the interfacing chip can spend the Secure Element's authority, here requesting RKE tokens at will once the blocklist is gone.

## Limits and safety notes

As the paper bounds them: **Proximity is required twice** — the LF wake-up works over a few metres with the standard antenna, and the ~1.5-minute firmware push needs BLE range of the victim's fob; the fob attacked must be that car's paired fob. **The update flaw is patched**: 2020.48 (November 2020) closed the OAD hole, and the authors verified the closure — this page should not be read as describing a currently open path into a patched fob. The pairing-protocol flaw and the wake-up vector were *not* fixed in that update, per the paper, but exploiting pairing still needs the car's diagnostic connector (evil-maid/evil-valet access) or a fresh route to fob code execution. **Scope: Model X only**; other models' phone-as-key systems are not analysed. Testing used the authors' own equipment and a consenting owner's car; a fuzzing side-quest (Appendix C) found only a BCM denial-of-service.

## Status and sources

Status: **published**. *IACR Transactions on Cryptographic Hardware and Embedded Systems* 2021(4), pp. 149–172. DOI [10.46586/tches.v2021.i4.149-172](https://doi.org/10.46586/tches.v2021.i4.149-172), verified against Crossref (record's title, all three authors, venue, and page range match the paper), 2026-11-01. Full text read in full from the authors' open repository copy of the TCHES version, 2026-11-01.

## Related

- [Fast, Furious and Insecure](fast-furious-and-insecure-passive-keyless-entry-and-start-systems-in-modern-supercars.md) — the same lab's Model S break: weak cipher there, broken composition here
- [SoK: Stealing Cars Since Remote Keyless Entry Introduction](sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it.md) — files this break under new-technology attacks
- [Relay Attacks on Passive Keyless Entry and Start Systems in Modern Cars](relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars.md) — the attack class this paper explicitly is not
- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md) — the concept page; this break is enrolment abuse, a third outcome
