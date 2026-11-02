---
uid: 01a19d3c-af5e-7711-a7da-b8fc246900a9
title: "CAN message authentication: the retrofit design space"
summary: "Two complete academic designs and the standardised answer, compared on freshness, key scope, frame cost, and evidence — plus the two limits they all share."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [vatican-vetted-authenticated-can-bus, leia-a-lightweight-authentication-protocol-for-can, vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks, can-injection, can-availability]
sources:
  - url: "https://doi.org/10.1007/978-3-662-53140-2_6"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1007/978-3-319-45741-3_15"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1145/3134600.3134623"
    retrieved: 2026-11-01
---

CAN frames carry no proof of who sent them — the gap [CAN injection](can-injection.md) exploits. The retrofit question is how to add that proof to a bus designed in the 1980s: 8-byte classical payloads, broadcast delivery, ECUs that cannot be recalled for new hardware, and hard real-time deadlines. This KB holds two complete academic answers at full depth, built in the same year from opposite directions, and the standardised third answer they both predate in deployment. Comparing them exposes the design space itself: every choice trades frame space, key-management burden, and what a failed check actually *does*.

## The designs

**vatiCAN** (Nürnberger & Rossow, CHES 2016) adds a **second frame** after each protected message carrying a truncated HMAC-SHA256 over the data, keyed per message group. Freshness comes from a **global nonce** distributed by a dedicated trusted ECU — each nonce encrypted to its recipient under a per-ECU device key, a group key shared by all participants of an ID, and a shared broadcast value. Its failure semantics are detection-grade: a receiver that sees an invalid checksum floods an alarm and moves the suspect sender toward error state rather than silently dropping the frame. It is a **measured prototype** — real ECUs, Vector hardware, published latencies.

**LeiA** (Radu & Garcia, ESORICS 2016) spends no extra frames. It works on CAN with **extended identifiers**, carving the 29-bit ID into the arbitration ID, a session field, and a counter field, so freshness rides *inside* the frame's own header; a truncated MAC occupies payload bytes. Keys are **pairwise per ID** (a message ID's key shared by its sender and receivers), provisioned as long-term keys from which per-session keys are derived by a KDF, with a two-phase epoch synchronisation to recover from counter drift. Its evidence type is the mirror of vatiCAN's: a design with a **formal security proof** in the UC model — and **no implementation and no measurements**, a fact its page states plainly. Detection versus prevention is a configuration choice: receivers can drop unauthenticated frames or merely flag them.

**AUTOSAR SecOC** is the industry's standardised answer and the one that ships: a MAC computed over the PDU plus a **freshness value** (a counter/timestamp hybrid managed by a Freshness Manager), truncated to a profile-chosen length, keys provisioned into HSMs. Verification failure means the PDU is discarded — prevention semantics by default. SecOC's constraint is deployment scope rather than cryptography: it authenticates configured PDUs on buses whose ECUs implement it, which makes it a new-platform answer, not a retrofit for the fleets the research papers attack.

## The comparison axes

- **Freshness.** A nonce service (vatiCAN: fresh, but needs a trusted distributor ECU and per-recipient encryption) vs. counters in-band (LeiA: no extra frames, but synchronisation becomes a protocol of its own) vs. managed counter/timestamp freshness (SecOC: standardised, but the Freshness Manager is infrastructure).
- **Key scope.** Group keys per ID (vatiCAN) are cheap to provision and mean any group member can forge any other member's frames. Pairwise per-ID keys (LeiA) narrow the blast radius to the ID's participants. SecOC leaves key scope to the OEM's provisioning — the standard specifies the mechanism, not the trust topology.
- **Frame and bandwidth cost.** vatiCAN doubles the protected traffic (an extra frame per message plus nonce distribution). LeiA spends identifier bits and payload bytes instead. SecOC spends payload bytes on MAC and freshness truncation. On a loaded classical bus each cost is real; none of the three is free.
- **Failure semantics.** Detection-and-alarm (vatiCAN), configurable drop-or-flag (LeiA), drop (SecOC). On a safety bus the choice is not cosmetic: dropping a genuine frame whose counter desynchronised is itself an availability event.
- **Evidence.** A measured prototype, a formal proof with no implementation, and a deployed standard whose public record is specification text rather than evaluation. The three evidence types do not rank each other; a retrofit decision needs all three questions answered and each design answers a different one best.

## The two shared limits

**Availability.** Authentication verifies frames that arrive; it cannot make frames arrive. Flooding, fault-confinement abuse, physical dominance, and silencing all act below or beside the layer these designs defend — the [CAN availability](can-availability.md) page owns that half, and any authentication deployment claim that prices injection but not removal is incomplete.

**The compromised sender.** Symmetric keys authenticate a *key holder*, not an honest ECU: a fully compromised legitimate sender produces perfectly authentic malicious frames under every design above. [VulCAN](../vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks.md) (ACSAC 2017) is the corpus's answer to exactly this gap — it pairs its authentication protocol with **software isolation** (library-OS compartmentalisation of the sending stack) and remote attestation, arguing authentication is only meaningful if the thing holding the key is itself constrained. Its own limit is recorded on its page: the attestation-server half is design-only. The design space's frontier, in this corpus, is not stronger MACs — it is bounding what a key holder can do.

This page synthesizes the KB's own full entity pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source.

## Related

- [vatiCAN](../vatican-vetted-authenticated-can-bus.md) — second-frame HMAC, nonce service, measured prototype
- [LeiA](../leia-a-lightweight-authentication-protocol-for-can.md) — in-ID freshness, pairwise keys, proof without implementation
- [VulCAN](../vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks.md) — authentication plus isolation, aimed at the compromised sender
- [CAN injection](can-injection.md) — the attack class these designs answer
- [CAN availability](can-availability.md) — the limit none of them answers
