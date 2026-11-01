---
title: "Key-fob relay attacks"
summary: "Two attackers relay a genuine key's radio exchange, so the car sees a valid key 'nearby' — encryption doesn't help, because nothing was forged, only forwarded."
type: concept
updated: 2026-10-31
related: [relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars, fast-furious-and-insecure-passive-keyless-entry-and-start-systems-in-modern-supercars, dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer]
sources:
  - url: "https://www.ndss-symposium.org/ndss2011/relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars/"
    retrieved: 2026-10-31
  - url: "https://tches.iacr.org/index.php/TCHES/article/view/8289"
    retrieved: 2026-10-31
  - url: "https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/verdult"
    retrieved: 2026-10-31
---

A relay attack defeats passive keyless entry and start (PKES) without
breaking any cryptography. Two attackers bridge the distance between car
and key: one stands by the car with a relay device, the other near the
owner's real key — outside a front door, or in a café. The car's
low-frequency wake-up and challenge are forwarded to the real key; the
key's genuine, correctly encrypted response is forwarded back. Both
endpoints behave exactly as designed. The lie is purely about *distance*.

## Why the design is vulnerable

PKES authenticates the *key*, but infers *proximity* from signal presence
and strength — there is no secure distance measurement. Cryptography
cannot help: relaying forwards valid ciphertext and valid responses, and
is independent of modulation, protocol, and authentication strength.
Francillon, Danev, and Čapkun demonstrated this at NDSS 2011 against ten
models from eight manufacturers; relaying only the car-to-key leg
sufficed, at up to 50 metres.

The same pattern applies to phone-as-key: NCC Group demonstrated a
link-layer Bluetooth Low Energy relay against Tesla Model 3/Y phone key
in 2022, forwarding encrypted traffic with roughly 8 ms of added latency —
 inside normal timing variation, which defeats latency-bounding and
link-encryption mitigations.

## Relay is not cloning

Keep this distinct from *cloning* attacks, which break the cryptography
itself: the Megamos immobiliser cipher was broken outright (Verdult,
Garcia & Ege, USENIX Security 2015), and one widely used PKES system used
a 40-bit proprietary cipher with no mutual authentication, allowing a fob
to be cloned from a few seconds of proximity (Wouters et al., IACR
TCHES 2019). Relay needs no such break — it works against correctly implemented
crypto.

## Papers in this KB

- [Relay Attacks on Passive Keyless Entry and Start Systems in Modern Cars](../relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars.md) — the NDSS 2011 demonstration.
- [Fast, Furious and Insecure](../fast-furious-and-insecure-passive-keyless-entry-and-start-systems-in-modern-supercars.md) — the DST40 cloning break (TCHES 2019).
- [Dismantling Megamos Crypto](../dismantling-megamos-crypto-wirelessly-lockpicking-a-vehicle-immobilizer.md) — the immobiliser cipher break (USENIX Security 2015).

## Detection and mitigation

- **Secure ranging / distance bounding** (UWB-based digital-key designs)
  is the only mitigation class that addresses the root cause; it requires
  hardware support at both ends, and coverage differs sharply by brand
  and model year.
- **User-presence proof** for start (PIN-to-drive, deliberate phone
  interaction) and **motion-sensing fobs** that sleep when stationary;
  letting owners disable passive entry entirely.
- **Key hygiene:** Faraday storage at home blunts the
  attacker-near-the-door variant.
- **Weak defences, labelled as such:** RSSI heuristics and coarse latency
  checks are partial at best — the NCC work shows a link-layer relay sits
  inside normal timing variation.
- **Detection is intrinsically hard** because the exchange is genuine;
  vehicle-side logging of entry events and owner notifications are the
  realistic detective controls.
