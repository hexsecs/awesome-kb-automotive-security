---
uid: 01a19d3c-af5e-7711-a7da-b8fc246900a9
title: "CAN message authentication: the retrofit design space"
summary: "Two complete academic designs and the standardised answer, compared on freshness, key scope, frame cost, and evidence — plus the two limits they all share."
type: concept
cluster: bus
created: 2026-11-01
updated: 2026-11-17
depth: deep
related:
  - vatican-vetted-authenticated-can-bus
  - leia-a-lightweight-authentication-protocol-for-can
  - vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks
  - can-injection
  - can-availability
  - secoc-key-extractor
  - sok-kicking-can-down-the-road-systematizing-can-security-knowledge
  - a-formal-security-analysis-of-can-xl
sources:
  - url: "https://doi.org/10.1007/978-3-662-53140-2_6"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1007/978-3-319-45741-3_15"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1145/3134600.3134623"
    retrieved: 2026-11-01
  - url: "https://icanhack.nl/blog/secoc-key-extraction/"
    retrieved: 2026-11-17
  - url: "https://www.autosar.org/fileadmin/standards/R20-11/FO/AUTOSAR_PRS_SecOcProtocol.pdf"
    retrieved: 2026-11-17
facets: [can, authentication, attack]
---

CAN receivers ordinarily learn a frame's identifier and contents, not the identity of its physical transmitter. An attacker able to transmit can therefore impersonate an expected message ID — the gap [CAN injection](can-injection.md) exploits. Message authentication adds evidence that an authorised key holder generated particular data in an acceptable freshness context. It does not prove that the data are safe, or that the key holder is uncompromised.

## The bus constrains the construction

Classical CAN (CAN CC) offers at most eight payload bytes. The identifier drives arbitration and message selection; it is not an authenticated source address. The frame CRC detects transmission errors, but an injecting controller can generate a valid CRC for invented data. Broadcast delivery also complicates key scope: several receivers may need to verify one sender, yet a symmetric verification key also permits generation.

The framing budget differs across generations. Classical CAN 2.0B supports extended 29-bit identifiers, which LeiA uses for freshness metadata; this is not CAN FD. FD expands payloads to 64 bytes and supports a faster data phase. XL expands them to as much as 2,048 bytes, easing space pressure without automatically authenticating application messages. Neither extra space nor speed establishes secure key provisioning or replay handling.

The [CAN security SoK](../sok-kicking-can-down-the-road-systematizing-can-security-knowledge.md) treats successor-bus transferability as indicative, not experimentally proven. The [CAN XL formal analysis](../a-formal-security-analysis-of-can-xl.md) separately reports inherited CAN CC MAC-sub-layer weaknesses and seven new vulnerabilities validated on commercial controllers. Here **MAC sub-layer means medium access control**, not message authentication code: those findings must not be described as cryptanalysis of a cryptographic MAC.

## Generation, verification and freshness

A useful abstract construction is `tag = MAC(K, context | payload | freshness)`. Context binds the authenticator to the intended message, for example through an identifier or a distinct per-ID key. The receiver reconstructs the same inputs, computes its own tag and compares the transmitted portion before releasing the payload. A valid tag without freshness still permits replay of a recorded valid command.

Counters avoid clocks but create persistent-state and synchronisation requirements. A receiver must reject old values while tolerating legitimate losses; reboot and wraparound must not reuse accepted counter/key combinations. Epoch-derived session keys separate successive counter lifetimes. Timestamp approaches instead require an agreed time basis and acceptance window. Freshness reconstruction from transmitted low bits saves space but depends on the receiver's higher-order state.

Truncation is a security parameter, not merely packing. Under idealised independent guessing, a t-bit tag gives approximately 2^-t success per attempt; the number of accepted attempts matters. Short tags, permissive retry policies and startup exceptions therefore require explicit analysis. Freshness protects against old messages only when its own state and synchronisation messages are protected.

## vatiCAN: preserve the data frame

[vatiCAN](../vatican-vetted-authenticated-can-bus.md), CHES 2016, leaves the original frame unchanged and follows it with a separate 64-bit HMAC frame, typically on ID `i+1`. The construction uses **Keccak**, not SHA-256, over identifier, payload and counter. Upgraded receivers defer execution until authentication succeeds; unchanged legacy recipients receive no such guarantee.

A trusted Nonce Generator periodically broadcasts a random global value to reset counters after loss or sleep. This nonce is public, not a per-recipient encrypted secret. Production-provisioned keys may be per ECU or shared within logical groups. The separate frame preserves existing payloads at the cost of one additional frame per protected message, plus nonce traffic.

The prototype used ATmega328P microcontrollers, MCP2515 controllers, a Seat Ibiza cluster and replayed Passat traffic. Reported verification deferral was 3.3 ms at 500 kbit/s, not a universal deadline guarantee. Software can detect another transmitter using its ID; destroying a spoofed frame before legacy nodes accept it needs additional controller capabilities. Receiver-side rejection and bus-wide prevention are different properties.

VulCAN later identified a replay weakness in vatiCAN's repeated random nonce resets: collisions or near-collisions can recreate authenticating state. Its Appendix A describes scenarios needing as little as 30 minutes of recorded traffic. This is a freshness failure, not an HMAC forgery. Original prototype measurements do not erase the later attack.

## LeiA: per-ID epochs and explicit resynchronisation

[LeiA](../leia-a-lightweight-authentication-protocol-for-can.md), ESORICS 2016, assigns each protected ID a long-term key shared by its sender and legitimate receivers. A 56-bit epoch derives a session key; a 16-bit counter advances per message, with epoch changes at startup and counter overflow. The same MAC primitive serves authentication and derivation, requiring the pseudorandomness assumption stated in the proof as well as MAC unforgeability.

LeiA uses the extended identifier's 18 bits for a 16-bit counter and two-bit command code. Crucially, it **also sends a separate authentication frame**: the counter costs no payload bytes, but the MAC does cost another frame. Command codes distinguish data, data MAC, epoch and epoch MAC. Authenticated epoch exchange recovers synchronisation after an authentication-failure signal.

Thus both designs normally add one authentication frame per data frame; they do not represent extra-frame versus zero-extra-frame alternatives. LeiA permits less frequent authentication as a bandwidth tradeoff. Extended-frame coexistence does not ensure compatibility with every existing identifier allocation or timing budget.

The original paper provides a reduction-based security argument, not vehicle measurements. VulCAN supplies the first implementation and measured timings. Per-ID keys compartmentalise unrelated IDs, but are not pairwise secrets between exactly two ECUs when several receivers share them. A compromised receiver can forge within its key domain. Long-term provisioning and authorised replacement remain assumptions outside LeiA's protocol proof.

## SecOC: configurable PDU protection

[AUTOSAR's R20-11 protocol specification](https://www.autosar.org/fileadmin/standards/R20-11/FO/AUTOSAR_PRS_SecOcProtocol.pdf), §§5.1–5.4, defines authentication over a Data Identifier, the secured payload portion and the complete freshness value. A Freshness Manager supplies counter or timestamp state; only a configured fragment may be transmitted. The Data Identifier is a configured binding, not universally identical to the CAN arbitration ID.

The standard supports authentication information appended to the PDU and separate authentic/cryptographic PDUs. It is therefore misleading to equate SecOC with one fixed frame layout. Profile 1 specifies AES-128 CMAC, 24 transmitted MAC bits and eight freshness bits. Profile 2 explicitly omits freshness when synchronised freshness is unavailable: the name SecOC alone does not guarantee replay resistance.

Successful verification normally permits forwarding; failure handling includes retries, discard conditions and configurable verification-status overrides. Audits must inspect configuration and startup behaviour, not assume unconditional fail-closed operation. Nor does the protocol establish that all keys reside in HSMs. Larger FD/XL payloads ease packing, but application integration, latency and verification enforcement remain deployment work.

## Key management and the compromised component

The [Toyota SecOC key extractor](../secoc-key-extractor.md) demonstrates the distinction between primitive security and key security. The author's 2021 RAV4 Prime EPS investigation recovered firmware through fault injection, reconstructed the update authentication and uploaded an accepted RAM helper that exported keys. AES-CMAC was not broken: software-held keys and a symmetrically authenticated servicing path made valid authenticators available. [Bootloader stages](bootloader-stages.md) owns that execution chain.

The writeup's newer Corolla Cross discussion reports code execution but HSM-protected keys that could not simply be dumped from RAM. Using the HSM as a signing oracle is presented as a theoretical route requiring further investigation, not a reproduced extraction. Neither case establishes one fleet-wide SecOC secret.

[Shared and default secrets](shared-and-default-secrets.md) explains the blast-radius question: which other units accept recovered authority? Provisioning, replacement, rotation and revocation must preserve that boundary. Non-exportable keys help, but compromised authorised software may still invoke permitted cryptographic operations.

[VulCAN](../vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks.md), ACSAC 2017, addresses this stronger adversary with Sancus hardware-isolated components. It implements LeiA and a modified vatiCAN using session-key renewal rather than the global nonce reset. Its FPGA/cluster experiments demonstrate protected processing under hostile surrounding software. The attestation server and session-key provisioning remain design-only; physical and side-channel extraction are excluded.

## Limits and verification

Authentication cannot ensure delivery. Flooding, frame destruction and fault-confinement abuse remain [CAN availability](can-availability.md) problems. Rejecting a genuine but desynchronised message can itself create an availability event; safe fallback requires a system-level argument.

Checked 2026-11-17: all three existing DOI URLs resolved to bibliographic records. Their linked entity pages' primary vatiCAN, LeiA and VulCAN PDFs, and the added AUTOSAR PDF, were downloaded and text-extracted because webfetch cannot render PDFs. The Toyota author writeup and official USENIX CAN XL abstract were reachable. XL findings here are bounded to that abstract; no individual attack chain is inferred. This synthesis combines protocol proofs, bench evaluations, a specification and a particular extraction case, not fleet prevalence measurements, certification or reproduced vehicle testing.
