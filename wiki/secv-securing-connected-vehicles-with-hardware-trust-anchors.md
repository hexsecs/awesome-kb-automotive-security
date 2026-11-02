---
title: "SECV: Securing Connected Vehicles with Hardware Trust Anchors"
summary: "Kayondo et al., NDSS 2026. Mediates external-network control messages inside a TEE backed by an EVITA-compliant HSM, so the gateway can verify them even…"
type: entity
category: "Research Papers"
url: "https://www.ndss-symposium.org/ndss-paper/secv-securing-connected-vehicles-with-hardware-trust-anchors/"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Kayondo et al., NDSS 2026. Mediates external-network control messages inside a TEE backed by an EVITA-compliant HSM, so the gateway can verify them even when the external network manager is compromised, at 6.5 percent transmission overhead."
sources:
  - url: "https://www.ndss-symposium.org/ndss-paper/secv-securing-connected-vehicles-with-hardware-trust-anchors/"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.14722/ndss.2026.240106"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - remote-exploitation-of-an-unaltered-passenger-vehicle
  - secure-firmware-updates
  - uptane
  - ivi-update-trust
---

Kayondo et al., NDSS 2026. Mediates external-network control messages inside a TEE backed by an EVITA-compliant HSM, so the gateway can verify them even when the external network manager is compromised, at 6.5 percent transmission overhead.

## What it is

SecV (stylised SECV) is a runtime security mechanism for the boundary between a vehicle's extra-vehicle network (EVN) platform — the connected, full-OS side hosting infotainment, telematics, and OTA functions — and its in-vehicle network (IVN), by Kayondo, You, Kim, Seo, and Paek, NDSS 2026. The problem is an architectural assumption connected platforms silently broke. A traditional IVN gateway enforces static routing and filtering over fixed-function ECUs, using the fixed ID-to-ECU mapping to attribute every message. The EVN manager is not fixed-function: it runs a full OS and many applications, any of which can transmit through the gateway — and the gateway cannot see *which application* sent a message or under what authority. A compromised EVN OS or application can therefore emit control messages satisfying every static filter while violating the OEM's actual policy. SecV moves the trust decision to where the context exists: a trusted enforcement module in a TEE on the EVN platform (SSMe) mediates *all* EVN-to-IVN traffic, enforces per-application policies, and signs what it authorizes; a counterpart at the gateway (SSMi), anchored in an EVITA-compliant HSM, verifies the signatures before the gateway applies its existing filters. Static filtering is preserved — SecV adds the provenance layer it never had.

## What it showed

**The threat is a demonstrated pattern, not a hypothesis.** The design is derived from five real attack examples, each mapped to the requirement whose absence enabled it: Keen Lab vs Mercedes-Benz (Wi-Fi to head-unit code execution, root, impersonation injecting CAN messages past the gateway; 2021); Cai et al. vs BMW (cellular TCU, WebKit overflow, TOCTOU to root, unchecked messages through weak filtering; 2019); Miller & Valasek's Jeep Cherokee (TCU foothold, SPI pivot, malicious gateway firmware; 2015); Keen Lab vs Tesla Model S (browser/kernel chain to reconfiguring gateway filters, then — after Tesla added signing in 2017 — an update-logic bypass running unsigned apps; 2016–17); Synacktiv vs Tesla Model 3 (Wi-Fi, Bluetooth, LTE entries, 2022–2024, ending in unfiltered injection or malicious gateway firmware). The paper's generalizations: the pattern is constant across vendors over a decade, the gateway is always the single chokepoint, and in the Tesla cases the EVN manager alone sufficed. Five requirements follow (RQ1–RQ5): explicit per-application transmission permissions, protected against modification; only attested firmware/software executing on both platforms; keys securely stored and use-controlled; consistent gateway verification of every EVN-originated message.

**The design answers three stated challenges.** (1) *TEE–HSM trust establishment:* the HSM cannot inspect TEE firmware or export its keys, so SecV combines measured boot with cross-domain attestation, anchored in OEM-provisioned key pairs; a three-phase attestation and channel setup derives an ephemeral root key (SKR) from HSM-supplied entropy, then a runtime key (SKC), and discards SKR. (2) *Real-time mediation without TCB bloat:* the Secure World must own the communication peripherals (Normal World access revoked via TZPC/TZASC), but porting full drivers into the TEE would import their vulnerability history — so drivers are *split*: minimal "driverlets" in the Secure World implement only the authorization-critical Tx/Rx path and whitelist expected control-register sequences, while Normal World drivers delegate via SMC requests; polling, batching, and zero-copy shared buffers bound the world-switch cost. (3) *Attribution under a compromised OS:* provenance cannot ride on metadata the untrusted OS supplies, so it is bound physically — applications load through a hardened Linux IMA flow: each binary is bundled with its transmission policy *encrypted* under an OEM key (MEK) held in the HSM, the bundle hashed and signed; a minimal trusted "inner kernel" (Hilps-based intra-kernel isolation via the ARM64 TxSZ field) verifies the bundle at load and has SSMe allocate a per-process secure buffer pool recorded in a PID–MID map the Normal World cannot see. A message's sender *is* its buffer's address; the outer kernel holds those buffers read-only, and copy-to-user paths are hooked so only the inner kernel can write them. At send time the driverlet resolves the buffer to a policy, checks the message ID, signs with SKC, and transmits — anything else is dropped. TCB is small by construction (≈2.0k isolation lines, 2.7k SSMe, 1.2k secure monitor).

**Measured on real automotive hardware.** The prototype runs on an NXP S32G3 (eight Cortex-A53 cores hosting the EVN manager; four Cortex-M7 MCUs hosting the IVN gateway; automotive HSE as the HSM), OP-TEE 4.0, ARM Trusted Firmware 2.10, Linux 6.6.52, over FlexCAN. Headline costs: **6.5% geometric-mean transmission overhead** and **1.5% additional message loss**, the loss concentrated in zero-gap bursts of small (8-byte) frames (an unprioritized long queue lost over 20%; fixed by priority handling plus SSMe rate limiting). Trust establishment adds 5.83 ms at boot (under 1%). Application load latency rises 23× (0.0256 ms to 0.593 ms), a one-time cost of verification and PID–MID setup. With cryptography live on 32-byte messages at a realistic 1 ms gap, HMAC adds 181 µs mean round-trip latency and 8.61% gateway CPU (offloaded to the HSM); AES-GCM adds 247 µs and 13.99%. Real-trace replay (CAN-MIRGU, OTIDS — neither has sub-1 ms gaps) showed no degradation or frame loss; memory cost is a fixed 30 MB reservation. The security evaluation is qualitative: each threat-model attack fails at a named check (IMA appraisal, PID–MID lookup, buffer bitmap, peripheral revocation, boot attestation), several converting into denial of service — a deliberate safety-preserving trade-off.

## Where it fits

SecV is the KB's first full page for a *runtime* gateway-trust design, and its position relative to the KB's update-security material needs one clear line: **Uptane secures delivery; SecV secures provenance of live control traffic.** The [secure firmware updates](concepts/secure-firmware-updates.md) concept and the Uptane pages address who may push software to a vehicle and how that delivery survives server and key compromise; SecV assumes software is already installed and asks instead: when an installed, connected platform emits a control message, can the gateway tell *which application* sent it, and whether it was allowed to? The two meet at attestation (RQ3, the hardened-IMA load path), and its Jeep example (AE3) is the KB's Miller & Valasek 2015 chain retold as a requirements derivation — that paper's reflashed gateway chip is, in SecV's vocabulary, a gateway whose firmware attestation and EVN-side mediation were both absent. SecV also sharpens the [IVI update-trust](concepts/ivi-update-trust.md) concept from an unexpected direction: its Tesla Model S example records the 2017 signing bypass (an update-*logic* flaw, not a key failure) as an RQ3 violation — a worked instance of that concept's gate-logic failure class on the execution side rather than the installation side. Against the gateway literature it positions itself versus hypervisor-based IVI containment (Harness — larger TCB, higher overhead, no HSM acceleration) and TEE network filters (TEEFilter, TrustedGateway — no automotive constraints or per-application attribution); its claimed novelty is the *combination*: TEE and HSM as joint anchors with cross-domain attestation.

## Limits and safety notes

The threat model is explicit about its edges, and the page keeps them attached. The TEE itself is trusted (Secure World attacks are out of scope; listed hardening options are future work), as are physical attacks (fault injection, side channels). A hijacked *legitimately permissioned* application can still send anything inside its own policy; the mitigation is rate limiting and bounded buffers, which bounds volume, not semantic abuse — the same compromised-sender limit the CAN-authentication literature concedes, one layer up. Availability is deliberately subordinated: failed attestation halts communication, so several attacks convert into denial of service rather than being prevented outright. Engineering limits are stated in the paper: driver splitting is manual (the mainline CAN/SPI families' Tx/Rx/IRQ paths align, vendor interrupt handling being the main divergence); the evaluation is a single platform (S32G3) with the IVN side lightly modified; and the Automotive Ethernet extension is a *proposed* kernel-bypass redesign — the CAN stack traversal does not transfer — so no Ethernet result should be read as measured. This page records a defensive design and its evaluation, reproducing no attack procedure beyond the pattern level at which the paper states them.

## Status and sources

Status: **published**. Network and Distributed System Security Symposium (NDSS) 2026, 23–27 February 2026, San Diego, CA, USA; ISBN 979-8-9919276-8-0. **DOI 10.14722/ndss.2026.240106 — verified against Crossref for this page**: the record's title, author list (Kayondo, You, Kim, Seo, Paek), venue (NDSS 2026, Internet Society), and primary resource URL (the exact NDSS PDF read) all match the paper.

## Related

- [Remote Exploitation of an Unaltered Passenger Vehicle](remote-exploitation-of-an-unaltered-passenger-vehicle.md) — the Jeep chain as a requirements derivation
- [Secure firmware updates](concepts/secure-firmware-updates.md) — delivery security; SecV is the runtime-provenance counterpart
- [Uptane](uptane.md) — the delivery-side design SecV complements
- [IVI update trust](concepts/ivi-update-trust.md) — SecV's Tesla example instances its gate-logic failure class
