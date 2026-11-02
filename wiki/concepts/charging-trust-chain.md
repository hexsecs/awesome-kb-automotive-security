---
uid: 01a19d3c-af5f-7345-a8e2-1d04ca6c743d
title: "The EV–EVSE charging trust chain (ISO 15118 / DIN 70121)"
summary: "The vehicle–charger link's trust is a chain — association, transport, contract authorisation — whose links fail independently and are measured failing."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging, current-affairs-a-security-measurement-study-of-ccs-ev-charging-deployments, charge-it-to-my-neighbor-a-relay-attack-on-iso-15118-plug-and-charge-payment, race-to-charge-concurrency-bugs-and-state-integrity-violations-in-ev-charging-infrastructure, openv2g, pyplc, everest, ocpp-charging-attacks]
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity25/presentation/szakaly"
    retrieved: 2026-11-01
  - url: "https://www.usenix.org/conference/usenixsecurity19/presentation/baker"
    retrieved: 2026-11-01
---

Charging a vehicle is a negotiation between two computers that have never met, over a power cable, ending in money moving. The KB's charging coverage splits across two links: the charger↔backend link, owned by the [OCPP concept](ocpp-charging-attacks.md), and the **vehicle↔charger link** — ISO 15118 and its predecessor DIN 70121, running over power-line communication (HomePlug Green PHY) on the CCS connector. This page covers that second link. Its organising fact, established jointly by the KB's tool and paper pages, is that "the charging session is secure" is not one property but a **chain of independent links** — physical association, transport protection, and contract authorisation — and the corpus documents every link failing separately, including in sessions where the other links held.

## Link 1: association (SLAC) — pairing without authentication

Before any ISO 15118 message exists, the vehicle and charger must associate at the PLC layer via SLAC (Signal Level Attenuation Characterisation), which pairs them and derives the network membership key (NMK) for their shared HomePlug network. SLAC in its deployed form is unauthenticated and its key exchange runs in the clear: [Losing the Car Keys](../losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging.md) (USENIX Security 2019) showed the single-ended CCS wiring radiates this exchange beyond the cable — from 54 sessions at 14 sites, a neighbouring parking bay recovered session traffic, and plaintext SLAC handed over the NMK in 31 sessions, after which the "private" vehicle–charger network is simply joinable. The tooling pages ([pyPLC](../pyplc.md), [open-plc-utils](../open-plc-utils.md), [dsv2gshark](../dsv2gshark.md)) are the working substrate of this layer. A physical-layer companion, [Brokenwire](../brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging.md), starves the same medium by preamble alone. Association security is the chain's foundation link, and in the deployed fleet it is the weakest.

## Link 2: transport (TLS) — optional, and mostly absent

ISO 15118 adds TLS above the association for the application session — for Plug & Charge it is mandatory in the specification; for the older DIN 70121 profile there is no TLS at all, and plain EXI-encoded XML runs over the (already compromised) PLC network. The deployment measurement is [Current Affairs](../current-affairs-a-security-measurement-study-of-ccs-ev-charging-deployments.md) (USENIX Security 2025), the first charger-side census: 325 chargers, 26 manufacturers, 4 countries — **only 12% offer TLS, 6% standards-compliant, zero mutual TLS, zero ISO 15118-20**. The implementations in this KB ([OpenV2G](../openv2g.md), [v2gdecoder](../v2gdecoder.md), [wwcp-iso15118](../wwcp-iso15118.md), [everest](../everest.md)) each carry pieces of the stack; EVerest's page also records what a production stack's own code does under concurrency ([Race to Charge](../race-to-charge-concurrency-bugs-and-state-integrity-violations-in-ev-charging-infrastructure.md): 11 CVE-assigned thread-safety flaws in its core). The link's verdict: transport protection is specified, rarely deployed, and never mutual in the measured fleet — the vehicle authenticates nothing about the charger in practice.

## Link 3: Plug & Charge authorisation — signatures that don't bind the session

Plug & Charge replaces the RFID card with a certificate chain: the vehicle presents a contract certificate, the charger validates the chain to a root, checks revocation, and bills the contract. Each of those is a separate link — chain validation, revocation freshness, and the binding between the authenticated certificate and *this* physical session. [Charge It to My Neighbor](../charge-it-to-my-neighbor-a-relay-attack-on-iso-15118-plug-and-charge-payment.md) (VehicleSec 2026) broke the binding link specifically: the PnC signature covers the challenge alone, not the session context, so three relayed application-layer messages make a victim's contract pay for a stranger's charge — with every signature valid and every certificate genuine. Chain validation also presumes the revocation link works in an offline charger, which the corpus treats as an open operational question rather than a solved one. [Chargesploit](../chargesploit.md) works this surface from the testing side.

## The chain property

The three links fail independently, and partial security composes badly: TLS over a compromised association still authenticates a channel the attacker shares; a valid contract certificate relayed into the wrong session bills the wrong party; a correct association and transport with a DIN 70121 profile has no authorisation link at all. The measurement papers are what elevate this from architecture commentary to fact — Losing the Car Keys measured link 1 failing in the wild in 2019, Current Affairs measured link 2's absence across the deployed fleet in 2025, and Charge It to My Neighbor demonstrated link 3's binding flaw against the strongest configuration the standard offers. A charging-security claim that names only one link's status is, on this corpus's evidence, a claim about a third of the chain.

This page synthesizes the KB's own full entity pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source.

## Related

- [Losing the Car Keys](../losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging.md) — link 1 measured failing: radiated SLAC, plaintext NMK
- [Current Affairs](../current-affairs-a-security-measurement-study-of-ccs-ev-charging-deployments.md) — link 2's census: 12% TLS, zero mutual
- [Charge It to My Neighbor](../charge-it-to-my-neighbor-a-relay-attack-on-iso-15118-plug-and-charge-payment.md) — link 3's binding flaw, against valid signatures
- [OCPP charging attacks](ocpp-charging-attacks.md) — the companion concept for the charger↔backend link
- [EVerest](../everest.md) and [pyPLC](../pyplc.md) — the open implementations of this link's stack
