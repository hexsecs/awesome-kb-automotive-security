---
title: "CAN injection"
summary: "Attacker taps exposed CAN wiring and impersonates a trusted ECU: classic CAN frames carry no sender authentication, so fake 'key valid' messages are believed."
type: concept
created: 2026-10-31
updated: 2026-11-01
related: [canflict, canter, carpunk, canalyzat0r, can-utils, security-in-automotive-bus-systems, experimental-security-analysis-of-a-modern-automobile, comprehensive-experimental-analyses-of-automotive-attack-surfaces, adventures-in-automotive-networks-and-control-units, remote-exploitation-of-an-unaltered-passenger-vehicle, error-handling-of-in-vehicle-networks-makes-them-vulnerable, leia-a-lightweight-authentication-protocol-for-can, vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks, fast-and-vulnerable-a-story-of-telematic-failures]
sources:
  - url: "https://plaxidityx.com/blog/blog-post/what-oems-can-do-to-prevent-can-injection-car-theft/"
    retrieved: 2026-10-31
---

CAN injection is the attack behind a wave of keyless car thefts: the
attacker taps CAN wiring reachable from outside the cabin and transmits
frames that impersonate a trusted ECU. Classic CAN frames carry no sender
authentication, so a forged status claim — "a valid key is present" — is
believed by the ECUs that act on it.

## Attack model

The best-documented case is the theft of Ian Tabor's Toyota RAV4,
analysed by Ken Tindell of Canis Labs. The attackers reached the bus
through the headlight wiring, because the headlight ECU sits on the same
CAN segment as the smart-key ECU. A small concealed device transmitted
frames as if it were the smart-key ECU announcing a validated key; a
gateway forwarded that state to the powertrain segment, the immobiliser
disengaged, and the doors unlocked. No key, fob, or cryptographic secret
is involved — the attack forges a *status claim*, not a credential. Some
injector devices also electrically dominate or flood the bus to suppress
legitimate ECUs, which is why the RAV4 logged a storm of diagnostic
trouble codes during the theft.

## Access paths

The theft above is this concept's core case, not its whole extent.
The substrate claim — frames carry no sender identity, so any
transmitter is believed — is one concept, but *how the transmitter
gets on the bus* varies, and the mitigations below do not bind every
path equally. The KB's pages use at least four entries:

1. **External tap** (the theft model): a concealed device on exposed
   exterior wiring. Segmentation of externally reachable segments and
   gateway forwarding policy bind this path directly.
2. **Diagnostic-port attachment:** the assumed-access research model —
   [Koscher 2010](../experimental-security-analysis-of-a-modern-automobile.md)'s
   laptop on the OBD-II port, and Miller & Valasek 2013's ECOM cable
   likewise. No concealed device and no key-validation forgery; what
   binds here is physical access control and diagnostic-session
   gating, not harness segmentation.
3. **Compromised or bridged ECU:** an ECU already inside the network
   becomes the injector — Checkoway 2011's exploited media player
   sending arbitrary CAN packets; the Jeep's reflashed V850 bridge
   chip in Miller & Valasek 2015; Koscher's telematics unit
   reprogrammed from the low-speed bus to relay onto the high-speed
   bus. Segmentation of *external* segments does nothing against a
   dual-homed unit already inside both subnets; only message
   authentication binds this path fully.
4. **Data-link-layer crafting from an unmodified MCU:**
   [CANflict](../canflict.md) forges frames below the controller's
   own checks, from inside a legitimate node.

Only message authentication with freshness binds all four; every
other mitigation is path-specific, and a defence argued from the
theft model alone silently leaves paths 2–4 open.

## Why the design is vulnerable

Classical CAN (ISO 11898) was designed for a closed, trusted network. A
frame's arbitration ID identifies the *message type*, not the sender;
there is no source authentication, no integrity protection beyond a link
CRC, no freshness, and no encryption. Any node that can transmit can
claim any identity, and receivers — including gateways bridging
segments — act on ID plus payload. Security therefore rests entirely on
the physical inaccessibility of the harness, an assumption modern body
electronics breaks: headlights, bumpers, and external sensors now sit on
security-relevant segments. [CANflict](../canflict.md) shows the same
trust problem at the data-link layer, from inside an unmodified
microcontroller.

## Detection and mitigation

- **Message authentication with freshness** on security-critical frames —
  AUTOSAR SecOC (MAC plus freshness counter, keys held in HSMs) is the
  standardised answer.
- **Segmentation:** externally reachable segments must never carry
  key-validation state, and gateways should refuse to forward security
  state arriving from exposed segments.
- **Plausibility interlocks:** Tindell's suggested short-term fix —
  inhibit smart-key unlock/start when recent CAN error or DTC anomalies
  indicate bus disturbance.
- **Intrusion detection:** per-ID timing and frequency anomaly detection
  and ECU fingerprinting; [CANter](../canter.md) targets the
  drop-and-spoof variant specifically. Telematics alerts on DTC bursts
  catch the noisy injector variants.
- **Physical:** harness routing and protection, tamper evidence on
  exterior connectors.

## Tools in this KB

- [Carpunk](../carpunk.md) — an injection toolkit; the offensive side of this page.
- [CANalyzat0r](../canalyzat0r.md) and [can-utils](../can-utils.md) — the capture and analysis bench used to study injected traffic.
- [CANflict](../canflict.md) — data-link-layer frame crafting from an unmodified MCU.
- [CANter](../canter.md) — IDS research aimed at this attack class.

Per-model susceptibility varies widely: segment topology and gateway
policy are decisive, and no fleet-wide measurement exists.
