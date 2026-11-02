---
title: "VulCAN: Efficient Component Authentication and Software Isolation for Automotive Control Networks"
summary: "Van Bulck, Muhlberg, and Piessens, ACSAC 2017. Combines message authentication with trusted-computing isolation, defending against an adversary running…"
type: entity
category: "Research Papers"
url: "https://vanbulck.net/files/acsac17-vulcan.pdf"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Van Bulck, Muhlberg, and Piessens, ACSAC 2017. Combines message authentication with trusted-computing isolation, defending against an adversary running arbitrary code on a participating ECU."
sources:
  - url: "https://vanbulck.net/files/acsac17-vulcan.pdf"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1145/3134600.3134623"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - vatican-vetted-authenticated-can-bus
  - leia-a-lightweight-authentication-protocol-for-can
  - can-injection
  - can-message-authentication
---

Van Bulck, Muhlberg, and Piessens, ACSAC 2017. Combines message authentication with trusted-computing isolation, defending against an adversary running arbitrary code on a participating ECU.

## What it is

Jo Van Bulck, Jan Tobias Mühlberg, and Frank Piessens, imec-DistriNet, KU Leuven. *Annual Computer Security Applications Conference (ACSAC) 2017*, pp. 225–237. DOI: [10.1145/3134600.3134623](https://doi.org/10.1145/3134600.3134623) (printed in the paper's own ACM Reference Format block and confirmed via Crossref). A **design/architecture** paper, not a new wire protocol. VulCAN implements the two existing AUTOSAR-compliant CAN authentication protocols — **vatiCAN and LeiA** (identified in-paper as, to the authors' knowledge, the only two proposed to date) — on **Sancus**, an open-source protected-module architecture extending the openMSP430: hardware-enforced isolated Protected Modules (PC-based access control, single entry point), a three-level key hierarchy (node master key → vendor key → module key derived from module identity = code contents + section addresses), and hardware authenticated encryption (SpongeWrap/spongent). The generic protocol shape follows vatiCAN/LeiA: a symmetric **128-bit key per CAN ID**, a 64-bit MAC over (ID | payload | counter), the MAC sent as a **separate frame on ID i+1**, backwards-compatible with legacy transceivers. Requirements beyond the protocol properties (P1–P4) are system-level: real-time compliance, component isolation, component attestation, dynamic key update, and legacy integration (S1–S5).

**Adversary model (the paper's headline strengthening).** The adversary has **arbitrary message manipulation *and* arbitrary code execution on every ECU in the network** — all software, including privileged OS code, is compromised **except** the Sancus-protected components. Denial of service is explicitly out of scope (broadcast bus), as are physical/side-channel key-extraction attackers. As the paper frames it, prior CAN-authentication proposals assume the adversary has *not* compromised the ECU whose packets she fakes; VulCAN removes that assumption — key secrecy and processing integrity survive full ECU compromise because messages are constructed and verified inside the protected module and keys never leave its private data section.

**System elements.** An in-vehicle **Attestation Server (AS)** holds every module's key and runs load-time challenge–response attestation at ignition; session keys (fresh random 128-bit per connection) are distributed **at every car start**, piggybacked on attestation. The paper proposes wiring ignition to the AS so the **car can refuse to start if attestation fails**. ECU replacement by an untrusted repair shop is handled via the car vendor as Sancus infrastructure provider. **Legacy shielding:** a Sancus gateway ECU — with the CAN driver itself inside a protected module owning the transceiver — authenticates on behalf of unmodified legacy ECUs and forwards only authenticated messages onto a private bus. Persistent tamper-resistant storage is needed **only on the AS node** (a higher-end TEE such as TrustZone/SGX is suggested for it) — a stated relaxation versus prior proposals. **One protocol change:** their vulcanised vatiCAN **omits vatiCAN's global Nonce Generator** and uses LeiA-style session keys (epoch + counter, refreshed on overflow), because of the replay finding below.

## What it showed

- **Novel finding — a practical replay attack on vatiCAN's nonce renewal** (Appendix A). vatiCAN's Nonce Generator broadcasts a fresh random 32-bit global nonce every 50 ms, resetting all counters. By the (generalised) birthday problem, nonce reuse reaches 90% probability after 135,000 renewals and 99% after 199,000 (2–3 hours); counting *near*-collisions (within k, which the attacker can skip/wait through) advances this sharply — at k=15, 99% certainty after 36,000 renewals. **As little as 30 minutes of recorded bus traffic can suffice to replay a previously authenticated message**, defeating vatiCAN authentication for a 50 ms window (extendable by destroying renewal messages with custom transceiver hardware).
- **Evaluation platform:** FPGA testbench — six Xilinx Spartan-6 FPGAs, Sancus openMSP430 cores at **20 MHz**, MCP2515 transceivers, 500 kbit/s bus. The paper presents the **first-ever implementation of LeiA**. The Attestation Server itself was **not implemented** (future work).
- **MAC cost:** Sancus hardware computes the MAC in **4,222 cycles = 0.21 ms** (LeiA variant 4,049 cycles = 0.20 ms) — **over 11× faster** than software-only vatiCAN's reported 47,600 cycles ≈ 2.95 ms (Keccak on a 16 MHz ATmega). Framed as travel distance at 100 km/h: ≈8 cm (software) vs ≈0.6 cm (VulCAN).
- **Message overhead (send one authenticated message):** legacy baseline 0.41 ms; Sancus+vatiCAN protected 0.80 ms (**+97%**); Sancus+LeiA protected 0.96 ms (**+136%**); extrapolated software-only vatiCAN 2.95 ms (+625%). Round-trip: legacy 1.01 ms; protected vatiCAN 1.82 ms (+80%); protected LeiA 2.18 ms (+115%). **Isolation itself costs only ~5–6%** over the unprotected Sancus build. The paper concedes the ~100%+ overheads "may be prohibitive for some existing real-world applications".
- **TCB:** **147 lines of trusted code (vatiCAN) / 212 lines (LeiA)**, versus 322 lines for the authors' own unprotected CAN driver alone and >670 for the Arduino CAN shield library. Bus congestion from the added authentication frames (~3%) is cited from vatiCAN, not re-measured.
- **Application scenario (hardware-in-the-loop):** two off-the-shelf **2014 Seat Ibiza** instrument clusters plus six Sancus ECUs; one cluster unprotected on the bus, the other shielded behind a Sancus gateway. An attacker keypad running arbitrary unprotected code on the central ECU spoofs commands that move the unprotected cluster but are **rejected by the protected ECUs and not forwarded to the shielded cluster** (the gateway lights a warning indicator instead).

## Where it fits

VulCAN treats [vatiCAN](vatican-vetted-authenticated-can-bus.md) and [LeiA](leia-a-lightweight-authentication-protocol-for-can.md) as the two AUTOSAR-compliant baselines and implements both rather than proposing a third protocol. Its protocol-level criticism is directed solely at vatiCAN's nonce renewal (above); it proves nothing new about LeiA, noting LeiA's security was formally proven under MAC unforgeability. Its delta over both 2016 designs is system-level: both assume the sending/receiving ECU software is uncompromised; VulCAN's guarantees are stated to hold when it is not. It also supplies the first implementation and measurements of LeiA, which the LeiA paper itself lacked. The attack class the authentication addresses is the KB's [CAN injection](concepts/can-injection.md) concept.

## Limits and safety notes

- The Attestation Server — the component that attests ECUs and distributes session keys — was **not implemented**; attestation and key distribution are design, not measurement.
- DoS and physical/side-channel attackers are out of scope by construction; real-time compliance is claimed for benign conditions.
- Participating ECUs need Sancus-capable hardware — not a pure software retrofit; only legacy ECUs behind a gateway avoid modification.
- Headline comparisons cross platforms (20 MHz FPGA Sancus cores vs the 16 MHz ATmega figures reported for software vatiCAN).

## Status and sources

Status: **published** (finished 2017 publication). The author PDF was read in full for this page, including Appendix A; code and hardware are public at distrinet.cs.kuleuven.be/software/vulcan. Pp. 225–237 rest on the Crossref record.

## Related

- [vatiCAN](vatican-vetted-authenticated-can-bus.md) — one of the two protocols VulCAN implements; target of its nonce-renewal replay finding
- [LeiA](leia-a-lightweight-authentication-protocol-for-can.md) — the other protocol VulCAN implements; VulCAN is its first implementation
- [CAN injection](concepts/can-injection.md) — the attack class message authentication addresses
