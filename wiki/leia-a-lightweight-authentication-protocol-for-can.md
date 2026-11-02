---
title: "LeiA: A Lightweight Authentication Protocol for CAN"
summary: "Radu and Garcia, ESORICS 2016. Backwards-compatible per-ID authentication that fits CAN's timing and bandwidth limits, compartmentalising ECUs so a…"
type: entity
category: "Research Papers"
url: "https://pure-oai.bham.ac.uk/ws/portalfiles/portal/29342174/leia.pdf"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Radu and Garcia, ESORICS 2016. Backwards-compatible per-ID authentication that fits CAN's timing and bandwidth limits, compartmentalising ECUs so a compromised head unit cannot actuate the powertrain."
sources:
  - url: "https://pure-oai.bham.ac.uk/ws/portalfiles/portal/29342174/leia.pdf"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1007/978-3-319-45741-3_15"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - can-injection
  - lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems
  - vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks
---

Radu and Garcia, ESORICS 2016. Backwards-compatible per-ID authentication that fits CAN's timing and bandwidth limits, compartmentalising ECUs so a compromised head unit cannot actuate the powertrain.

## What it is

A design-and-proof paper by Andreea-Ina Radu and Flavio D. Garcia, School of Computer Science, University of Birmingham. *21st European Symposium on Research in Computer Security* (ESORICS 2016), Heraklion, Greece, September 2016, Proceedings Part II, LNCS 9879, pp. 283–300. LeiA is a message authentication protocol for the CAN bus that adds source authentication — the property whose absence underlies the published CAN attack literature the paper surveys (Koscher, Checkoway, Miller & Valasek) — under CAN's real constraints (8-byte payloads, tight latency, broadcast semantics, no new infrastructure). The authors present it as the first AUTOSAR-compliant lightweight authentication protocol in the literature, designed against the AUTOSAR 4.2 SecOC specification.

## What it showed

**Construction — per-ID keys, epoch-derived session keys.** Every CAN identifier that carries authenticated traffic gets its own key material, held by the broadcasting ECU and every legitimate receiver of that ID: a 128-bit long-term key, a 56-bit **epoch**, and a 16-bit **counter**. The epoch increments at every vehicle start-up and whenever the counter overflows. The session key is derived, not distributed: session key = MAC(long-term key, epoch), computed locally by sender and receivers alike — which is why LeiA needs neither the key server of MaCAN nor its time server (counters replace timestamps as the freshness source). To send, the sender increments the counter and transmits the data, then a 64-bit MAC computed over (counter, data) under the current session key. A receiver accepts only if the received epoch‖counter is strictly greater than its stored value — older values are discarded as replays — and the MAC verifies. Consequences the paper draws out: a session key authenticates at most 2^16 messages, and a compromised session key is useful only until the epoch rolls (2^16 messages or the next vehicle restart, whichever comes first); the long-term key itself never MACs traffic directly.

**Framing — the counter rides in the identifier, not the payload.** LeiA runs on CAN 2.0B extended (29-bit) frames: the 16-bit counter and a 2-bit command code are placed in the 18-bit extended-identifier field, so no payload bytes are spent on freshness. The *data channel* (command 00) carries the ordinary frame. The *authentication channel* carries the MAC in a separate frame on a nearby ID (the paper suggests data ID + 1, to stay close in arbitration order), with command codes distinguishing MAC-of-data (01), an epoch value (10), and a MAC of an epoch (11). Each node also has an *authentication error channel* carrying a two-frame AUTH FAIL signal. Resynchronisation is first-class because receivers overwrite stale buffers and nodes join at different times, so desynchronisation — not attack — is the expected cause of MAC failures: on AUTH FAIL the sender broadcasts its current epoch plus a MAC over (epoch, counter), and receivers adopt the values only if they verify and are newer.

**Claims, as the paper makes them.** *Backwards compatible:* extended frames coexist with standard 11-bit frames on the same bus, arbitration priority is still decided by the base identifier, and no transceiver or controller changes are required — the explicit contrast with CANAuth and LiBrA-CAN, which need CAN+ and replacement transceivers, and CaCAN, which needs a modified monitor controller in every car. *AUTOSAR-aligned:* 128-bit keys, a 64-bit MAC (the SecOC recommended minimum for truncated MACs, and exactly one 8-byte CAN payload), freshness by counter, and the MAC bound to the identifier (via the per-ID session key) as the specification requires. *Compartmentalisation:* keys are per identifier, so a fully compromised ECU can forge valid MACs only for the IDs it legitimately sends or receives — the paper's motivating example is that a compromised CD player cannot thereby accelerate the vehicle; reaching the powertrain requires the powertrain IDs' keys. *Security:* the paper proves LeiA's authentication security by reduction to the unforgeability of the underlying MAC under chosen-message attack (UF-CMA), against a Dolev-Yao network adversary — with one extra assumption stated in plain sight: the MAC's outputs must be indistinguishable from random, because the same MAC algorithm doubles as the key-derivation function for session keys.

**Overhead — design accounting, not measurement.** This paper contains no implementation and no measurements; its overhead statements are arithmetic, and they are presented as such. Authenticating every message costs one extra frame per data frame — the frame count doubles where full authentication is applied. For nodes not involved in safety-critical functions, the protocol can instead send one MAC after every *n* messages, letting manufacturers pick their own security/bandwidth trade-off per ID. The counter itself costs no payload (it sits in the extended identifier).

## Where it fits

LeiA is the protocol-design answer to the attack class documented across this section: every CAN exploitation paper in the KB works because receivers cannot tell who sent a frame. The KB's [CAN injection](concepts/can-injection.md) concept page names "message authentication with freshness — AUTOSAR SecOC" as the defence class; LeiA is the 2016 academic design that implements exactly that class within unmodified CAN hardware constraints, and it is explicit about the two deployment traps it was designed around: schemes that need new transceivers or extra servers do not survive automotive cost review. Garcia is the connecting author to this batch's [Lock It and Still Lose It](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md), which LeiA cites as the RKE-cloning result: the same research programme breaking key systems on one side and designing bus authentication on the other.

## Limits and safety notes

As the paper states them: **denial of service is explicitly out of scope** — LeiA authenticates; it cannot stop an attacker from flooding or destroying frames on a shared bus (unauthenticated frames are dropped unparsed, and all prior CAN authentication proposals share the DoS exposure). A fully compromised ECU unavoidably forges its own IDs — "not a problem of our protocol but an inherent limitation of using symmetric key cryptography": compartmentalisation bounds the blast radius, it does not eliminate it. Key management is assumed, not solved: provisioning and replacing long-term keys "should require direct physical access… by an authorised repairs shop" and is declared beyond the paper's scope. And the honest framing for the whole design: it is a specification with a proof, published without an implementation, vehicle trial, or measured bus-load figures — its backwards-compatibility and overhead claims are argued from the CAN standard's frame coexistence rules and frame arithmetic, not demonstrated on a vehicle.

## Status and sources

Status: **unknown** — a finished 2016 publication; a protocol design, not a maintained artefact. Bibliographic record: ESORICS 2016, Proceedings Part II, LNCS 9879, Springer, pp. 283–300. DOI: [10.1007/978-3-319-45741-3_15](https://doi.org/10.1007/978-3-319-45741-3_15) — verified via the Birmingham portal's citation page and the Crossref record. Full text openly available from the Birmingham portal; read in full 2026-11-01.

## Related

- [CAN injection](concepts/can-injection.md)
- [Lock It and Still Lose It: On the (In)Security of Automotive Remote Keyless Entry Systems](lock-it-and-still-lose-it-on-the-in-security-of-automotive-remote-keyless-entry-systems.md)
- [VulCAN](vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks.md) — LeiA's first implementation, on Sancus protected modules
