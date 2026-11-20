---
uid: 01a19d3c-af6f-7dff-a1c9-8cf0e3927076
title: "Shared, default, and global secrets: the break-once pattern"
summary: "The decisive failure is rarely cipher strength — it is one secret shared by a fleet or a type, or a default nobody changed. Break one, break all."
type: concept
cluster: boundary
created: 2026-11-01
updated: 2026-11-17
depth: deep
related:
  - lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems
  - beneath-the-bonnet-a-breakdown-of-diagnostic-security
  - experimental-security-analysis-of-a-modern-automobile
  - gone-in-360-seconds-hijacking-with-hitag2
  - dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer
  - uds-seed-key
  - secure-firmware-updates
  - adventures-in-automotive-networks-and-control-units
  - firmware-acquisition
  - v2x-credential-management
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity16/presentation/garcia"
    retrieved: 2026-11-01
  - url: "https://www.usenix.org/legacy/events/sec10/tech/full_papers/Koscher.pdf"
    retrieved: 2026-11-01
  - url: "https://files.usenix.org/s3fs-public/cdn/sec16_paper_garcia.pdf"
    retrieved: 2026-11-17
  - url: "https://www.autosec.org/pubs/cars-oakland2010.pdf"
    retrieved: 2026-11-17
  - url: "https://illmatics.com/car_hacking.pdf"
    retrieved: 2026-11-17
facets: [authentication, attack]
---

The break-once pattern is a failure of **compromise containment**: a credential recovered from one ECU, transponder, or workshop program authorises operations on other units. Strong encryption cannot distinguish the rightful holder from an attacker who possesses the same key. But shared secrets, defaults, weak keys, and constant challenges are not interchangeable findings. This synthesis separates their mechanisms and evidence; it does not claim that every automotive cipher survives, or that every recovered key unlocks a fleet.

## Mechanism: the credential's scope sets the blast radius

For a challenge-response implementation, write the response abstractly as `r = F(K, seed)`. If every ECU of a type uses the same `K` and public algorithm `F`, extraction from one unit gives responses to fresh challenges from the others. Random seeds stop replay of old responses, **not computation with a stolen key**. Conversely, a fixed seed permits reuse of a corresponding response even without learning `K`, provided no other session-specific input is checked. These are different paths to the same loss of authentication.

The attacker's cost has two parts: an initial reverse-engineering or extraction cost and a per-target access cost. Sharing amortises the first across the credential's acceptance domain. It does not remove the second: the attacker may still need a target radio transmission, a CAN foothold, proximity to a transponder, or access behind a gateway. "Break all" means reusable authority within that domain, not instantaneous control of every car.

[Firmware acquisition](firmware-acquisition.md) explains why the cheapest accessible unit matters. A secret used by an expensive ECU can be exposed through another ECU or a dealer executable holding the same authority. Protection must be evaluated across **all copies**, not only the strongest storage location.

## OEM-wide keys: the VW RKE evidence

[Lock It and Still Lose It](../lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md), §§3–3.5, provides the clearest global-key case. Firmware analysis recovered the receiving ECUs' algorithms and keys. VW-2 and VW-3 use AUT64 with a single worldwide master key for each scheme; VW-4 uses XTEA with another worldwide key. No per-vehicle key diversification is used in those schemes. After recovering the appropriate key, an adversary needs one target rolling-code transmission to learn the target identity and counter and generate new codes.

This is not an attack on XTEA's nominal key length. Nor is it one universal key for every Volkswagen product: the paper distinguishes schemes, leaves VW-5–VW-7 unanalysed, and treats VW-1 separately as an obfuscated LFSR without cryptographic protection. A remote's unique identifier is not diversification when it accompanies messages protected by the same global key.

The paper cites almost 100 million VW Group sales in 2002–2015 and strong indications that the vast majority were vulnerable. That is a scope estimate, not 100 million individually tested vehicles. Its practical demonstration includes a model-year-2016 Audi Q3. The manufacturer statement about newer platforms using individual keys is reported, not independently verified by the authors. RKE compromise permits entry; this result alone does not defeat the separate immobilizer required to start the vehicle.

## Type-shared secrets and hardcoded authority

[Beneath the Bonnet](../beneath-the-bonnet-a-breakdown-of-diagnostic-security.md), §§3–4, is the diagnostic counterpart. Its evidence covers firmware from 13 ECUs across eight models, not an industry census. The KB's entity account records reused per-type secrets, weak proprietary seed/key constructions, and diagnostic download paths that execute a secondary loader in RAM. Algorithm recovery therefore becomes reusable diagnostic authority where the same constants and implementation recur.

The scope must remain implementation-specific. The Ford/Volvo construction and Fiat examples differ; the VW Group bytecode programs vary in strength. Sharing a public algorithm is not itself a vulnerability: standard cryptography deliberately shares algorithms. The problem is shared secret material, insufficient entropy, or a transformation whose supposed secret can be recovered cheaply. The Audi gateway's hardcoded alternative response is a stronger failure still: a fixed accepted value bypasses the ordinary challenge-dependent calculation. That observation should not be promoted to an OEM-wide backdoor without evidence of its distribution.

The paper's level-collapse result also depends on composition: level-1 access enables extraction of firmware containing higher-level secrets. It is not proof that all UDS security levels everywhere are equivalent. [UDS seed/key](uds-seed-key.md) owns the protocol and attempt-limiting details; this page tracks how authority propagates between units and levels.

The independently rechecked [Miller and Valasek 2013 report](https://illmatics.com/car_hacking.pdf), filed as [Adventures in Automotive Networks and Control Units](../adventures-in-automotive-networks-and-control-units.md), supplies a second extraction location. Ford's dealer software contains a bag of keys and the calculation code; Toyota's Calibration Update Wizard similarly exposes per-ECU secrets. Hardcoding is a storage/provisioning property, not automatically a fleet scope: a unique hardcoded key compromises one unit, while a model-wide constant compromises its acceptance domain.

## Default credentials: two immobilizer cases

[Gone in 360 Seconds](../gone-in-360-seconds-hijacking-with-hitag2.md), §7.4, says **at least half of the tested cars used default or predictable transponder passwords**. It does not say half of all Hitag2 cars used one datasheet value. Section 7.2 gives a concrete Korean-model example with the default password and a patterned cryptographic key. The password and the 48-bit cipher key are distinct credentials; learning or guessing one does not establish that the other is globally shared.

The same study demonstrates independent cipher/protocol attacks and instances of missing key read protection. Thus changing a default password addresses one shortcut, not the complete Hitag2 threat model. Its experiments involved more than 20 vehicles; the product's presence in hundreds of models is not evidence that every model had the same provisioning mistake.

[Dismantling Megamos Crypto](../dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md), §§2 and 5, documents transponders with unlocked memory or a publicly known default PIN. That grants write access to key blocks. Non-atomic partial key updates then provide a way to recover the original key through repeated authentication tests. The authors demonstrated the roughly 30-minute attack on several vehicles.

Their proposed lock-bit and random-PIN fix closes that write-access route. It does not repair the paper's independent cryptanalytic attack or weak-key patterns. A default PIN is therefore not synonymous with "the immobilizer encryption key is public." The first removes a protective gate; the second would directly supply the authority being protected.

## Debug leftovers and static challenge-response

The Escape parking-assist module in Miller and Valasek's report randomises a challenge, then overwrites both its stored copy and outgoing buffer with a constant. The authors describe debugging code left behind as the **presumed explanation**. That is evidence of a debug-like constant-seed path, not proof that a formally designated development key was shipped across the entire manufacturer's fleet.

[Koscher et al. 2010](../experimental-security-analysis-of-a-modern-automobile.md), §IV-C, reports a telematics challenge/response hardcoded and common to similar units, alongside the standard's prohibition on equal seeds for units sharing a part number. More fundamentally, its implementation did not use the exchange's result. The static credential and absent enforcement are independent failures; attributing the demonstrated access solely to secret reuse would misdescribe the experiment.

These cases justify auditing debug credentials and alternate authentication branches, but not inventing an additional measured category of fleet-wide "debug keys." The evidence here establishes constants, hardcoded exceptions, and inferred debug leftovers. A fresh-looking seed exchange on a protocol diagram does not establish freshness in deployed code.

## Containment, rotation, and remaining limits

The defensive deductions follow the mechanisms rather than one universal fix:

- **Diversify per vehicle, ECU, and purpose.** Independent random keys, or sound derivation with separated contexts, prevent a recovered leaf key from authorising another device. An identifier alone is not a secret; derivation fails fleet-wide if every ECU also contains the derivation master.
- **Separate verification from signing authority.** A public verification key may safely be identical across a fleet. It is not a shared secret: extracting it does not create signatures. Symmetric authentication instead gives every key holder the ability to compute authenticators.
- **Remove defaults and development exceptions.** Provisioning must verify completed configuration, including memory locks and alternate acceptance paths. A unique main key does not help if a shared fallback remains accepted.
- **Rotate through a trusted path.** Replacing a compromised shared key limits future exposure only when old authority is revoked and the attacker cannot learn or select its replacement. Updating every unit to another shared key recreates the same blast radius.

[V2X credential management](v2x-credential-management.md) illustrates per-device authority and revocation, but certificate issuance brings its own privacy and operational constraints. [Secure firmware updates](secure-firmware-updates.md) explains Uptane's separate repository roles and vehicle-bound instructions: these contain particular update-system compromises, not every leaked ECU key.

Per-device secrets therefore change the economics, not necessarily the exploitability of a vulnerable implementation. An automated extraction flaw may still be repeatable on each vehicle. Likewise, HSM storage can prevent key export while compromised authorised software retains a signing-oracle capability. The useful audit question is both **which units accept this credential?** and **what can compromised code do without exporting it?**

## Verification and source limits

Checked 2026-11-17: the original Garcia presentation URL and legacy Koscher PDF URL returned HTTP 404; both are preserved in frontmatter. The corrected USENIX presentation and linked Garcia PDF, AutoSec's Koscher PDF, Miller/Valasek report, and USENIX Hitag2 and Megamos records and PDFs were reachable; PDFs were downloaded and text-extracted for the cited passages. The Birmingham *Beneath the Bonnet* PDF could not be reread: webfetch cannot render that PDF and a direct download returned HTTP 403. Its detailed findings above remain attributed to the existing entity's prior full-text account, not represented as newly verified research. No vehicle or ECU was tested for this synthesis.
