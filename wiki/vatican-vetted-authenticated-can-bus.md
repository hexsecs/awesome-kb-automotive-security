---
uid: 01a19d3c-aff4-789b-a24a-0356c1d8aeb7
title: "vatiCAN: Vetted, Authenticated CAN Bus"
summary: "Nurnberger and Rossow, CHES 2016. Retrofit authentication for CAN using MACs and a global nonce, a reference point for later SecOC-style designs."
type: entity
category: "Research Papers"
url: "https://christian-rossow.de/publications/vatican-ches2016.pdf"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Nurnberger and Rossow, CHES 2016. Retrofit authentication for CAN using MACs and a global nonce, a reference point for later SecOC-style designs."
sources:
  - url: "https://christian-rossow.de/publications/vatican-ches2016.pdf"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1007/978-3-662-53140-2_6"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - fingerprinting-electronic-control-units-for-vehicle-intrusion-detection
  - error-handling-of-in-vehicle-networks-makes-them-vulnerable
  - vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks
  - can-message-authentication
---

Nurnberger and Rossow, CHES 2016. Retrofit authentication for CAN using MACs and a global nonce, a reference point for later SecOC-style designs.

## What it is

Stefan Nürnberger and Christian Rossow, CISPA, Saarland University, Germany. *Cryptographic Hardware and Embedded Systems — CHES 2016* (18th International Conference, Santa Barbara, CA, August 17–19, 2016), Springer LNCS vol. 9813, pp. 106–124. DOI: [10.1007/978-3-662-53140-2_6](https://doi.org/10.1007/978-3-662-53140-2_6). (The list renders the first author as "Nurnberger"; the paper's byline is Nürnberger.) vatiCAN is a backward-compatible message-authentication retrofit for CAN: it authenticates selected critical messages between upgraded ECUs while leaving legacy ECUs, message payloads, IDs, and CAN transceiver chips completely untouched — security as a pure software/library upgrade, designed around the automotive industry's "never touch a running system" constraint.

## What it showed

**The construction — authentication in a second frame.** The legacy CAN message is sent completely unmodified under its original ID *i*. The sender then transmits one additional CAN frame under ID *j = i + 1* (the smallest possible priority change) carrying a **64-bit HMAC** computed as HMAC(*i* | *m* | *c_j*) — over the legacy sender ID, the payload, and a per-sender counter. The primitive is HMAC over Keccak (SHA-3), parameterized at r = c = 128 to take a 128-bit input block and emit 64 bits; Receivers get the legacy frame immediately but execute the command only when the HMAC frame verifies; a missing or invalid HMAC means discard and optionally warn. Sender and receiver compute the HMAC in parallel, avoiding the wait a signature scheme would impose. Only messages manually selected as critical at development time pay the extra frame — everything else flows exactly as before.

**Replay protection — counters plus a global nonce.** Each sender's counter *c_j* increments with every authenticated message, so identical payloads produce different HMACs. Counters alone would desynchronize when frames are lost or ECUs sleep, so vatiCAN adds the one new component: a **Nonce Generator (NG)** that periodically broadcasts a fresh random global nonce *g*, upon which all ECUs reset their counters to *g*. A 50 ms NG period is suggested, costing ≈1% additional bus utilization at 500 kbit/s. The nonce is not secret — freshness, not unpredictability, is what the construction needs — but the NG must be protected, since impersonating it could desynchronize everyone.

**Keys.** 128-bit keys (exactly one Keccak input block), provisioned per ECU or shared across a logical group of ECUs (e.g. the four wheel-speed sensors) to save flash. Keys are provisioned during production; Diffie–Hellman at ignition is considered and rejected (man-in-the-middle without certificates). Replaced ECUs get new keys via the ordinary OBD software-update path, optionally with signed updates.

**Spoof detection and prevention.** Because CAN is a broadcast bus, every ECU can watch for frames carrying *its own* ID: a frame it did not send is by definition spoofed, and vatiCAN surfaces this in software as an exception. Actual *prevention* — invalidating the spoofed frame mid-flight by destroying its CRC field with dominant bits — is possible only with a modified CAN controller; the paper assumes at least the NG carries such hardware assistance. ECUs that legitimately share a sender ID (e.g. door ECUs) cannot use spoof detection.

**Prototype and measured overhead.** Implemented on ATmega328P (8-bit, 16 MHz) microcontrollers with MCP2515 CAN controllers, a Seat Ibiza instrument cluster as the legacy device, and replayed VW Passat B6 cluster traffic; released as an LGPL v2 Arduino library (2,152 bytes of code total). Measured at 500 kbit/s: one HMAC takes ≈47,600 cycles ≈ **2.95 ms** on the ATmega; the total deferral of a received message until verification completes is **3.3 ms** (the abstract's "less than 4 ms"); a secured request–response round trip takes 4.5 ms vs 1.08 ms legacy. On the Passat cluster bus (560 messages/s, 13.4% utilization), protecting 3 of 13 senders (110 of 560 messages/s) raised utilization to **16.2%**. The ATmega is explicitly a performance *lower bound* — the paper notes common 32-bit automotive MCUs (v850 class) are ≈2.6× faster.

**Security analysis, as stated.** Forging requires the 128-bit key (brute force ≈2¹²⁷ trials on average) or guessing the 64-bit tag (probability 2⁻⁶³ per attempt); the customary birthday-collision shortcut does not apply because the attacker must match one *specific* payload. **Positioning against prior designs (the paper's own 2016 comparisons):** CANAuth shares the HMAC idea but embeds it via CAN+, a physical-layer modification requiring hardware that does not exist; TESLA-style delayed key disclosure violates the real-time requirement; and AUTOSAR's scheme (the SecOC line of designs) appends the MAC at the PDU level, which the paper states is *not* backward compatible with legacy traffic and offers no spoofing prevention — vatiCAN's separate-frame construction is the deliberate opposite choice on both points. This is the paper's characterization of AUTOSAR 4.2-era specifications, carried as such, not a claim about SecOC's current state.

## Where it fits

The reference design for retrofitting authentication onto an unmodified CAN fleet: separate authentication frame, implicit freshness state, group keys, and spoof monitoring — the list summary's "reference point for later SecOC-style designs". Within this batch it is the prevention-side counterpart to [CIDS](fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md) (detection without protocol change) and the direct foil to the [bus-off paper](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md), which argues that error handling operates below authentication, so a MAC scheme alone cannot stop a victim ECU being forced off the bus. Together the three 2016 papers mark the field's pivot from demonstrating CAN attacks to engineering defences under production constraints.

## Limits and safety notes

As the paper states them: **latency is real** — 3.3 ms of verification delay is 0.9 m of travel at 100 km/h, and the conclusion concedes "for highly timing-critical functions, such as brakes, a millisecond delay might be unacceptable"; vatiCAN is offered as fast enough for *most* situations, not all. **Freshness state is fragile:** if frames are lost or an ECU sleeps, its counter desynchronizes and its HMACs are invalid until the NG's next nonce resyncs it. **Spoof *prevention* is not a software feature:** it requires a modified CAN transceiver/controller; unmodified hardware gets detection (an exception) only, and other recipients may already have processed the spoofed frame. **Group keys are a stated trade-off:** one compromised ECU in a key group can forge valid HMACs for every sender in that group. **Multi-frame protocols are out of scope:** authenticating every frame of KWP2000/ISO-TP traffic would induce "impractical bandwidth overhead" (payload-layer signatures are suggested instead, unimplemented). All performance numbers come from an 8-bit ATmega bench prototype with one legacy cluster device and replayed traffic, at one bus speed (500 kbit/s) — no in-vehicle evaluation is claimed.

## Status and sources

Status: **published** — a finished 2016 publication; the Arduino library was released as free software, but there is no maintained product (status follows the publication precedent). Bibliographic record: Springer record for CHES 2016 (LNCS 9813, pp. 106–124); the authors' PDF was read in full 2026-11-01.

## Related

- [Fingerprinting Electronic Control Units for Vehicle Intrusion Detection](fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md)
- [Error Handling of In-Vehicle Networks Makes Them Vulnerable](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md)
- [VulCAN](vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks.md) — implements vatiCAN under a compromised-ECU adversary model, and finds a practical replay attack on its nonce renewal
