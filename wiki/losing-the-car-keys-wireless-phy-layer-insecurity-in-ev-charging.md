---
title: "Losing the Car Keys: Wireless PHY-Layer Insecurity in EV Charging"
summary: "Baker and Martinovic, USENIX Security 2019. Recovers ISO 15118 charging messages from the unintentional wireless emissions of CCS power-line communication…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity19/presentation/baker"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Baker and Martinovic, USENIX Security 2019. Recovers ISO 15118 charging messages from the unintentional wireless emissions of CCS power-line communication across 54 real charging sessions."
sources:
  - url: "https://www.usenix.org/system/files/sec19-baker.pdf"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - pyplc
  - openv2g
  - open-plc-utils
  - ocpp-charging-attacks
  - brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging
  - charge-it-to-my-neighbor-a-relay-attack-on-iso-15118-plug-and-charge-payment
---

Baker and Martinovic, USENIX Security 2019. Recovers ISO 15118 charging messages from the unintentional wireless emissions of CCS power-line communication across 54 real charging sessions.

## What it is

Richard Baker and Ivan Martinovic, University of Oxford. *28th USENIX Security Symposium* (USENIX Security '19), Santa Clara, CA, August 14–16, 2019, pp. 407–424. The Combined Charging System (CCS) — adopted, the paper notes, by seven of the ten largest car manufacturers — runs vehicle-to-charger communication as ISO 15118 over HomePlug GreenPHY power-line communication (PLC) on the cable's Control Pilot and Protective Earth lines. This paper asks what that cable *radiates*. Because the PLC circuit is wired single-ended rather than differential — a consequence of sharing lines with legacy IEC 61851 signalling — the cable and equipment act as an antenna, and the OFDM waveform survives the channel essentially intact. The authors build the first wireless eavesdropping receiver for HomePlug GreenPHY — pure software, open-sourced under MIT — and use it in 54 real charging sessions at public chargers. The central claim is that this is not an implementation bug: the leakage follows from the standard's design choices, and every site tested leaked.

## What it showed

**The channel.** Differential signalling is PLC's emissions defence: two lines driven with opposite signals, whose fields cancel. CCS's backwards-compatibility arrangement grounds one transmission line (Appendix A shows the unbalanced circuit), so no cancellation occurs and the circuit radiates. A square-wave signal radiates only its transitions (the emissions are its gradient); an OFDM waveform has no static level, so the emission is a phase-shifted *replica* of the signal, and the eavesdropper's demodulation task is the legitimate receiver's minus the wire. All observations were in the near field (even at 28 MHz the wavelength is 10.7 m), so channel gain varies sharply with position and cannot be predicted from distance. Empirically, all 14 test sites leaked: peak SNR from 8 dB to 35 dB, usable bandwidth from 4.5 MHz to about 25 MHz, across chargers from six manufacturers — the flaw is systemic to CCS, not one vendor's.

**Recovery rates.** The capture rig cost roughly $800 (bladeRF SDR, upconverter, short monopole; equivalent setups under $300 are noted). Message recovery was routinely high, measured by the share of received payloads validating CRC32: beside the cable, up to 99.8%; from inside the car, one site's best capture reached 100.0%; and from an **adjacent parking bay — over 4 m away, on the far side of the car from the cable — 91.8%**. With two cars charging simultaneously and the antenna between them, both sessions were readable (CRC-valid rates 24.3–94.8%, mean 59.7%): an attacker parked at a busy station harvests whoever plugs in. Two caveats bound these numbers from below: with no ground truth, messages never detected cannot be counted; and the receiver's single-pass Turbo decoder understates what a better-resourced receiver would recover.

**What the recovered traffic gave up.** The HomePlug layer encrypts MAC traffic with AES-128 under an ephemeral Network Encryption Key — but the Network Membership Key (NMK) is delivered at association time by SLAC, and while HomePlug GreenPHY has a secure SLAC mode, **ISO 15118 specifies SLAC in its plaintext form**. Every observed SLAC exchange was insecure; the authors intercepted the CM_SLAC_MATCH.CNF carrying the NMK in **31 sessions**, and in 9 also the follow-on key message yielding the ephemeral NEK, after which the encrypted MAC layer decrypts passively. One layer up, **no observed session established TLS at all**: TLS is mandatory for contract-based Plug & Charge but optional with external authorisation (RFID card, app, operator) — and every session in the campaign used external authorisation. The full ISO 15118 conversation — state of charge, projected departure time, tariff preferences, vehicle-to-grid power flows — was therefore readable, as were the vehicle's persistent identifiers: its EV ID and charge-controller MAC address, both lifetime-stable and globally unique, recovered in **41 of 54 sessions (76%)** — in the two-car tests, for both vehicles from one antenna position.

**Why it matters beyond privacy.** One deployed billing arrangement turns the leak into theft: AutoCharge — in production, the paper reports, on a 60-location network across three European countries — authorises billing from the vehicle's charge-controller MAC address alone, exactly what this attack collects wirelessly and undetectably from the next bay; the paper also notes how such an address can be written onto another charge controller (via open-plc-utils and a serial debug port). Tracking needs no billing system: identifiers plus time and place build movement profiles, up to wardriving-style association of vehicles with home addresses. The lessons they draw: wireless threat models must be designed in (prior analyses assumed an attacker holding a modified cable or adapter plug); the ISO 15118 security model rests on a PKI that, at the time of writing, **did not exist** — no widely deployed root, its governance model still contested — so the TLS it underpins is absent in practice; and a PHY-layer security mode was specified off. Their concrete countermeasure needs no PKI and no new hardware: insert an ephemeral ECDH exchange into SLAC so the NMK is *derived* rather than transmitted, blank the key field in the match confirmation, and fall back to today's behaviour on timeout — sufficient against passive eavesdropping, though without authentication it cannot stop an active man-in-the-middle. Emissions-level fixes (chokes, shielding, liquid-cooled cables) are costly retrofits that cannot silence the vehicle/charger circuitry itself. Findings were disclosed to the tested vehicle and charger manufacturers and to AutoCharge operators.

## Where it fits

Scope first, because this KB has two charging surfaces easily conflated: this paper concerns **only the vehicle↔charger link** — the cable in the parking bay. The [OCPP charging attacks](concepts/ocpp-charging-attacks.md) concept covers the **charger↔cloud-backend link**: different wire, different protocol, different attacker position; Baker & Martinovic never leave the parking bay, and OCPP attacks never enter it. What this paper interrogates is the physical layer beneath the KB's ISO 15118 tooling pages. [pyPLC](pyplc.md) poses as vehicle or charger and walks the same SLAC, DIN 70121, and ISO 15118 state machines this paper listens to; its documentation records that stock modem firmware sees only SLAC/broadcast traffic while patched firmware exposes the full session — this paper shows why that traffic matters, recovered with no modem at all. [OpenV2G](openv2g.md) supplies the EXI codec for the message layer the tool reconstructs after V2GTP deframing; [open-plc-utils](open-plc-utils.md) is the toolkit the paper cites for the MAC-spoofing step of the AutoCharge attack. The natural sequels in this KB are the Brokenwire paper — wireless *disruption* of the same CCS physical layer, active where this paper is passive (a stub) — and the Plug & Charge relay paper (also a stub), which attacks the certificate-payment path whose absence this paper documents.

## Limits and safety notes

As the paper states them: **Passive only.** Testing on public infrastructure restricted the authors to listening; the injection direction is analysed (an injector must exploit component nonlinearities to synthesise constant levels) but never demonstrated — active-attack feasibility is reasoning, not a result. **Public chargers only, in one country, with three vehicles:** 14 sites in southern England; the vehicles (a BMW i3, a Jaguar I-PACE, and a Volkswagen e-Golf — the authors' own test cars) charged on hardware from six manufacturers; private and home chargers were not measured. **No ground truth:** chargers and vehicles were untouched, so the count of messages missed entirely is unknown; CRC failure rates describe only detected frames. **The receiver is deliberately weakened:** one Turbo-decoding pass and an uncalibrated power scale (the ≈−70 dBm apparent-power figure is flagged as uncertain) — recovery rates are a floor for a real attacker's capability, not a ceiling. **Time-stamped claims:** "no ISO 15118 PKI deployed," the complete absence of TLS, and AutoCharge's deployment shape are 2019 observations of a moving ecosystem, recorded here as the paper's findings, not as the present state of CCS. The authors observed only their own vehicles' sessions.

## Status and sources

Status: **unknown** — a finished 2019 publication. The eavesdropping tool was open-sourced under MIT (gitlab.com/rbaker/hpgp-emis-rx, as cited in the paper); no maintenance claim is made for it here. **DOI: none** — USENIX does not assign DOIs to its proceedings papers; no aggregator identifier is substituted (verified by Crossref query, 2026-11-01). Full text open at USENIX; read in full 2026-11-01.

## Related

- [pyPLC](pyplc.md) — the CCS toolkit running the same SLAC/ISO 15118 state machines over a wired modem
- [OpenV2G](openv2g.md) — the EXI codec for the message layer this paper's receiver reconstructs
- [open-plc-utils](open-plc-utils.md) — modem tooling the paper cites for writing a harvested MAC onto a charge controller
- [OCPP and charging attacks](concepts/ocpp-charging-attacks.md) — the other charging link (charger↔backend), linked to keep the boundary explicit
- [Brokenwire: Wireless Disruption of CCS Electric Vehicle Charging](brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging.md) — active wireless attack on the same physical layer (stub)
- [Charge It to My Neighbor: a Relay Attack on ISO 15118 Plug & Charge Payment](charge-it-to-my-neighbor-a-relay-attack-on-iso-15118-plug-and-charge-payment.md) — the certificate-payment path found undeployed here (stub)
