---
title: "Current Affairs: A Security Measurement Study of CCS EV Charging Deployments"
summary: "Szakaly et al., USENIX Security 2025. First measurement of publicly deployed CCS DC chargers, finding that only 12 percent of 325 units across four European…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity25/presentation/szakaly"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Szakaly et al., USENIX Security 2025. First measurement of publicly deployed CCS DC chargers, finding that only 12 percent of 325 units across four European countries negotiated TLS and that most ran decade-old HomePlug modem firmware."
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity25/presentation/szakaly"
    retrieved: 2026-11-01
  - url: "https://arxiv.org/abs/2404.06635"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging
  - brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging
  - charge-it-to-my-neighbor-a-relay-attack-on-iso-15118-plug-and-charge-payment
  - ocpp-charging-attacks
---

Szakaly et al., USENIX Security 2025. First measurement of publicly deployed CCS DC chargers, finding that only 12 percent of 325 units across four European countries negotiated TLS and that most ran decade-old HomePlug modem firmware.

## What it is

Marcell Szakály, Sebastian Köhler, and Ivan Martinovic, University of Oxford. *34th USENIX Security Symposium* (USENIX Security '25), pp. 7997–8016. The first measurement study of publicly deployed CCS DC fast chargers: instead of analysing the ISO 15118 standards on paper, the authors built a portable EV emulator — a Raspberry Pi 4, a Devolo dLAN Green PHY evaluation board, and a custom basic-signalling PCB, connected only to the charger's communication and ground pins, never the power pins — and ran real CCS sessions against production chargers across Europe. Because the emulator is software, it can re-run the session repeatedly against the same charger while varying its own configuration, interrogating one layer at a time: the entropy of the SLAC Network Membership Key (NMK), the HomePlug modem chip and firmware, TLS support and its implementation quality, and which V2G protocol versions (DIN SPEC 70121, ISO 15118-2, ISO 15118-20) are actually offered. The dataset covers 325 chargers (397 plugs, 149 installations, 26 manufacturers) in the UK, Switzerland, Hungary, and Croatia, manufactured between April 2013 and June 2023 and installed as late as May 2024, supplemented by a small vehicle-side check (8 real EVs against a charger emulator, plus an online survey of EV models).

## What it showed

**TLS is nearly absent.** Every charger supported a non-TLS session; only 12% offered TLS at all, and only 6% implemented standards-compliant TLS 1.2. None implemented mutual TLS, and only one vendor (ChargePoint) had TLS 1.3. Working TLS 1.2 came from four manufacturers supplying four networks (Ionity, Instavolt, ChargePoint, Porsche), of which only Ionity and Porsche advertised Plug and Charge. Support did not correlate with charger age — it tracked which manufacturers were actively deploying in a given year. Extrapolating over UK charger-network data, the authors estimate roughly 3.1% of chargers sit on network/manufacturer combinations expected to support TLS, against 74.5% on networks that do not.

**Where TLS exists, its deployment is fragile.** The correctly implemented certificates traced to the two big V2G PKI roots, Hubject (all European PnC networks) and Entrust, and were structurally right. But one manufacturer had shipped production chargers with a development TLS server still enabled: every unit presented the identical RSA-1024 certificate, expired in 2013, accepted TLS 1.1 with RSA key exchange and not-recommended ciphers — the manufacturer confirmed the devices were never meant to have TLS on. Another fleet shared one of only two leaf certificates across all its devices, one of them already expired at test time. One manufacturer's chargers transmitted NSS key-log material in cleartext UDP packets during the TLS handshake — a debugging feature that reached production (again confirmed by the vendor) and lets anyone on the powerline link decrypt the session, defeating Diffie-Hellman entirely. One more lacked the RFC 5746 renegotiation signalling that has been default in mainstream TLS libraries since 2010.

**Protocol versions lag a decade behind the standard.** All chargers support DIN SPEC 70121 (2012, no TLS, no PnC); 47% support ISO 15118-2, rising by build year to about 70% of chargers manufactured in 2023; **zero** support ISO 15118-20 or its mandatory mutual TLS — not even at dealerships selling -20-capable cars. On the vehicle side, all 8 tested EVs supported DIN and 7 supported 15118-2; the model survey found about half of newly announced cars offering -2 Plug and Charge and only 4 of 146 models announced for 2024 offering -20.

**The modem layer is frozen in 2013.** Every charger used a Qualcomm HomePlug Green PHY chip (QCA7000 78%, QCA7005 22%), and 62% ran firmware more than ten years old — the commonest build dates to August 2013. No charger ran firmware released after the 2022 Brokenwire disclosure, so that firmware-mitigable wireless denial of service stands unmitigated fleet-wide; Qualcomm publishes no advisories for these chips, so the true exposure of the old firmware cannot even be assessed publicly.

**SLAC keys are mostly sound, with sharp exceptions.** Most chargers generated a fresh random 128-bit NMK per session with the NID derived by PBKDF1 as specified. But two manufacturers fixed 4 of the 16 NMK bytes (96-bit entropy, with the shared fixed bytes making hash tables practical); one manufacturer's successive NMKs contained long, byte-shifted sections of previous keys, collapsing the search space for the next key; and one derived both NMK and NID from 4 random bytes padded with a fixed pattern — a 32-bit NMK trivially recoverable from the broadcast NID. The baseline weakness stands regardless: the NMK crosses in cleartext during SLAC, so it only ever excludes attackers who arrive after the session starts.

**A design flaw in charger PKI.** Charger certificates encode the EVSE ID, but a vehicle cannot know which charger it *ought* to be connected to, so any valid charger certificate is accepted at any location. One extracted certificate therefore enables man-in-the-middle attacks on every TLS session under that root, worldwide, until expiry or revocation — unlike web PKI, where a stolen certificate impersonates only its own name. The paper proposes two backwards-compatible repairs: bind certificates to place (GPS coordinates in the certificate's Subject Locality, verified by the CA at issuance and checked against the vehicle's own position), and require OCSP stapling for the *leaf* certificate — ISO 15118-2 currently mandates stapled responses only for Sub-CA certificates, vehicles need not check the leaf any other way, and no measured charger stapled a leaf response.

## Where it fits

This is the deployment census for the KB's CCS cluster. [Losing the Car Keys](losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging.md) (Baker & Martinovic, 2019) listened to 54 charging sessions and found no TLS at all and no deployed ISO 15118 PKI; this paper measures the charger side at fleet scale six years later and finds the ecosystem barely moved — the PKI now exists (Europe has converged on the Hubject root) but is barely used, and TLS is treated by operators as a Plug and Charge prerequisite rather than a security feature: the manufacturer implements it, the network operator decides whether it is switched on. Its §5.3 identity flaw is the same unverifiable-station-identity problem that [Charge It to My Neighbor](charge-it-to-my-neighbor-a-relay-attack-on-iso-15118-plug-and-charge-payment.md) weaponises — Szakály et al. is that paper's reference [20]. The paper also rebuts the earlier EVExchange relay (Conti et al.) on real-world grounds: passively forwarded sessions should trip basic-signalling and current cross-checks in a competent implementation, so TLS would defend there — a judgement about the network-layer relay that does not extend to Löw et al.'s application-layer one. Scope: everything here is the vehicle↔charger link; the charger↔backend link is the [OCPP concept's](concepts/ocpp-charging-attacks.md) separate surface.

## Limits and safety notes

As the paper states them: a **snapshot** — data collected through about September 2024, representative in the authors' judgement for Europe at that date, from four countries chosen by a geometric (density-based) sampling strategy rather than random selection. **Charger-side only**, apart from 8 vehicles and an unweighted online model survey that counts announced models, not sales. Experiments were non-malicious and standards-compliant in intent, terminated before power delivery; some chargers have incomplete experiment sets, so individual analyses rest on slightly different device totals. The ISO 15118-20 mutual-TLS probe used a self-signed vehicle certificate, so -20 support is inferred from the server's Certificate Request message rather than from a completed -20 session. The RFC 5746 gap was reported but deliberately not exploited. The implementations behind the anonymised findings (development certificates, key-log leak, weak NMKs) are **not named in the paper**, and this page follows that; manufacturers are named only where the paper names them.

## Status and sources

Status: **published** — a finished 2025 conference publication. Bibliographic record: *Proceedings of the 34th USENIX Security Symposium*, pp. 7997–8016. **DOI: none** — USENIX does not assign DOIs to its proceedings papers, and a Crossref bibliographic title query (2026-11-01) returned no record for this paper. Full text read end-to-end from the authors' arXiv version (arXiv:2404.06635v2), with pagination taken from the USENIX proceedings PDF, 2026-11-01. Artifacts (emulator code, hardware designs, dataset) are archived under DOI 10.5281/zenodo.14712107 — the artifact's DOI, not the paper's.

## Related

- [Losing the Car Keys: Wireless PHY-Layer Insecurity in EV Charging](losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging.md) — Baker & Martinovic 2019; the 54-session observation this census scales up
- [Brokenwire: Wireless Disruption of CCS Electric Vehicle Charging](brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging.md) — the firmware-mitigable DoS no measured charger is patched against
- [Charge It to My Neighbor: a Relay Attack on ISO 15118 Plug & Charge Payment](charge-it-to-my-neighbor-a-relay-attack-on-iso-15118-plug-and-charge-payment.md) — the attack built on this paper's TLS identity flaw
- [OCPP and charging attacks](concepts/ocpp-charging-attacks.md) — the other charging link (charger↔backend), linked to keep the boundary explicit
