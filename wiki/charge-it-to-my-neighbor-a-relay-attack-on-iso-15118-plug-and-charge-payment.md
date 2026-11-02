---
title: "Charge It to My Neighbor: A Relay Attack on ISO 15118 Plug and Charge Payment"
summary: "Löw et al., USENIX VehicleSec 2026. Relays Plug and Charge authentication so the attacker charges their own car while the victim is billed, exploiting…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/vehiclesec26/presentation/low"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Löw et al., USENIX VehicleSec 2026. Relays Plug and Charge authentication so the attacker charges their own car while the victim is billed, exploiting missing station identity in the signature and weak TLS certificate handling, with a proof of concept."
sources:
  - url: "https://www.usenix.org/conference/vehiclesec26/presentation/low"
    retrieved: 2026-11-01
  - url: "https://arxiv.org/abs/2512.15966"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging
  - current-affairs-a-security-measurement-study-of-ccs-ev-charging-deployments
  - brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging
  - ocpp-charging-attacks
  - charging-trust-chain
---

Löw et al., USENIX VehicleSec 2026. Relays Plug and Charge authentication so the attacker charges their own car while the victim is billed, exploiting missing station identity in the signature and weak TLS certificate handling, with a proof of concept.

## What it is

Jakob Löw, Vishwa Vasu, Thomas Hutzelmann, and Hans-Joachim Hof, Technische Hochschule Ingolstadt. *4th USENIX Symposium on Vehicle Security and Privacy* (VehicleSec '26), Baltimore, MD, August 2026, pp. 181–190. The paper attacks the payment mechanism that ISO 15118 Plug and Charge (PnC) adds on top of an encrypted session. PnC authorisation is a challenge–response: the station sends random challenge bytes, and the vehicle signs them with the private key of its contract certificate, proving ownership of the contract to be billed. The design flaw is what the signature does *not* cover — the signed data is the challenge alone, with no station identity, no timestamp, no session context, so a signature elicited anywhere can be spent at any station in the world. The attack builds a **fake charging station** that needs no power electronics — only the communication half of a charger — plugs it into a parked victim vehicle, and relays exactly three application-layer messages (the contract certificate, the challenge, the signature) in real time to the attacker's own vehicle, which is plugged into a genuine station. The victim's car believes it authorised its own charging; the genuine station bills the victim's contract for the attacker's energy. Only the attacker's vehicle ever charges.

## What it showed

**Why TLS does not stop it.** ISO 15118 requires the station's EVSE ID to be encoded in its TLS certificate, but — as Szakály et al. had already analysed — the vehicle has no trusted way to learn which station it is physically plugged into, so any valid station certificate is accepted anywhere. An attacker who extracts one station's certificate and private key can therefore impersonate *any* station, from any vendor, in any country: the ecosystem's security is bounded by its least secure station (the paper cites the Alpitronic Hypercharger's powerline-reachable admin interface and default-credentials advisory, CVE-2024-4622, as the kind of access that makes extraction plausible — not demonstrated). Under ISO 15118-20 the bar rises — mutual TLS means the attacker additionally needs one compromised *vehicle* TLS certificate and key — but payment handling is identical in -20, so the relay itself is unchanged.

**The proof of concept.** Built on the open-source SwitchEV/EcoG ISO 15118 stack (also deployed in real stations), customised so the attacker vehicle transmits the victim's certificate in its own PaymentDetailsReq, the fake station issues the genuine station's challenge byte-for-byte, and the victim's signature is transplanted into the attacker session's AuthorizationReq. The attack was executed end-to-end in a fully virtual setup and on real powerline hardware — the authors' own station as the genuine station, their EV simulator as the victim, two PLC modems as attacker vehicle and fake station. Timing is comfortable: ISO 15118 allows 2 s for the relayed responses and cellular round trips run well under 100 ms; the attacker session simply stalls until the victim's certificate arrives. Both TLS sessions are independent and valid — the failure is not in TLS but in the context-free signature.

**Position against EVExchange.** Conti et al.'s EVExchange (ESORICS 2022) also bills a victim for an attacker's charge, but by a different mechanism: it opaquely forwards *all* network traffic between two adjacent stations on the same backend, so both vehicles must be at the same site, both actually charge, and their battery voltages must stay consistent — each vehicle reports its own voltage to the other's station, the values diverge as charging proceeds, and charging both destroys the profit. This paper's relay needs no shared site, backend, or voltage, relays three messages instead of a session, and charges only the attacker's car. EVExchange's proposed countermeasure, distance bounding, targets network-layer latency; the authors judge timing detection unreliable for this relay (heterogeneous controllers, noisy PLC channel).

**Who would run it.** The adversary analysis (Bao et al.'s models plus one new role) separates the *freeloader* (bills a stranger), the *contract-sharer* (the scalable abuse: one contract relayed to many users), and the *equipment supplier*, who packages the relay into ready-made devices (the keyless-entry relay market pattern), zeroing the expertise needed. Getting from proof of concept to production vehicles is still engineering (see Limits): the fake station is buildable from open evaluation kits, but the attacker side needs a modified vehicle stack or a man-in-the-middle device interposed via known powerline-layer attacks.

**Mitigations.** The direct fix is context-binding: include the station's EVSE ID in the signed data. A backwards-compatible encoding puts the station's country and operator identifier (5 bytes) inside the 16-byte challenge; updated vehicles extract the EVSE ID from the TLS certificate and reject mismatches, so an updated vehicle is protected even against legacy stations, while legacy vehicles keep working everywhere. Hardening the TLS layer (mandatory OCSP checking for leaf certificates; geo-coordinates in station certificates, checked against the vehicle's position — both from Szakály et al.) limits impersonation but does not by itself fix the relay. The paper's structural alternative is to abandon in-protocol payment: the vehicle sends the EVSE ID to its manufacturer's backend, which starts the session via OCPP RemoteStartTransaction — the mechanism charging apps already use — eliminating the cross-vendor PnC PKI entirely, at the cost of making the manufacturer a payment gatekeeper and requiring connectivity. Disclosure went to CharIN and several station manufacturers before publication; the manufacturers acknowledged it but saw no need for immediate mitigation, citing PnC's still-low deployment.

## Where it fits

The certificate-payment sequel to [Losing the Car Keys](losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging.md), and a different failure at a different layer — the two should not be blurred. Baker & Martinovic (2019) passively *listened* to the powerline physical layer and recovered whatever sessions sent; their theft path, AutoCharge, abused a charge-controller MAC address that the PHY leaks — an identifier with no cryptography behind it at all — and in 2019 there was no Plug and Charge deployment for them to attack. This paper assumes the cryptography is present and working — TLS established, contract certificate valid, challenge fresh — and shows the protocol semantics still fail, because the signature authenticates a contract to nobody in particular. Where the 2019 fix is "encrypt the link and deploy the PKI", this paper shows TLS plus PnC *as specified* still does not bind payment to place. [Current Affairs](current-affairs-a-security-measurement-study-of-ccs-ev-charging-deployments.md) supplies the deployment frame: PnC was live on only two measured networks — this attack's current-risk bound, and its authors' urgency argument for fixing the binding before adoption grows. The out-of-band mitigation is the one place this paper touches the [OCPP concept's](concepts/ocpp-charging-attacks.md) link, and only as a *user* of RemoteStartTransaction; the attack itself never leaves the vehicle↔charger link.

## Limits and safety notes

As the paper bounds them: the proof of concept's victim is an **EV simulator** and the genuine station is the authors' own — the production-vehicle chain (extracting a station certificate, building the attacker-side MitM device) is argued from prior work, not demonstrated end-to-end. The attack **requires a previously compromised charging-station certificate and private key** (under ISO 15118-20, a vehicle certificate and key as well); no extraction is performed in the paper. It also requires physical plug access to the victim's charge port — the paper's scenario has the attacker opening a parked car's port. Present-day exposure is limited by Plug and Charge's low deployment: most sessions still use external payment. The context-binding fix is specified and reasoned through but not implemented against production stacks, and the out-of-band payment alternative is proposed, explicitly not evaluated.

## Status and sources

Status: **published** — a finished 2026 conference publication; the proof of concept is open source (github.com/securityinmobility/plug-and-charge-relay-poc). Bibliographic record: *Proceedings of the 4th USENIX Symposium on Vehicle Security and Privacy*, pp. 181–190 (ISBN 978-1-939133-56-4). **DOI: none** — no DOI appears on the paper and USENIX does not assign DOIs to its proceedings papers. Full text read end-to-end from the USENIX proceedings PDF, 2026-11-01.

## Related

- [Losing the Car Keys: Wireless PHY-Layer Insecurity in EV Charging](losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging.md) — Baker & Martinovic 2019; the passive PHY-layer predecessor whose undeployed-PnC gap this paper fills
- [Current Affairs: A Security Measurement Study of CCS EV Charging Deployments](current-affairs-a-security-measurement-study-of-ccs-ev-charging-deployments.md) — Szakály et al. 2025; measured the TLS identity flaw and PnC deployment this attack builds on
- [Brokenwire: Wireless Disruption of CCS Electric Vehicle Charging](brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging.md) — the PLC-layer attack family the paper's real-world MitM variant would build on
- [OCPP and charging attacks](concepts/ocpp-charging-attacks.md) — the other charging link (charger↔backend); this attack touches it only via the proposed RemoteStart mitigation
