---
title: "OCPP and charging attacks"
summary: "OCPP links chargers to cloud backends; weak transport security, shared identities and duplicate connections enable hijack, fraud and outage attacks."
type: concept
created: 2026-10-31
updated: 2026-10-31
related: [checkocpp, emuocpp, everest, ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations, losing-the-car-keys-wireless-phy-layer-insecurity-in-ev-charging, race-to-charge-concurrency-bugs-and-state-integrity-violations-in-ev-charging-infrastructure, charging-trust-chain]
sources:
  - url: "https://openchargealliance.org/ocpp-info-whitepapers/ocpp-1-6-security-whitepaper-4th-edition/"
    retrieved: 2026-10-31
  - url: "https://doi.org/10.3390/en15113931"
    retrieved: 2026-10-31
  - url: "https://www.ndss-symposium.org/ndss-paper/auto-draft-457/"
    retrieved: 2026-10-31
---

The Open Charge Point Protocol (OCPP) connects each charge point (EVSE)
to a cloud management backend (CSMS) that authorises sessions, bills
drivers, pushes configuration and firmware, and can steer charging
power. That link — and the identities on it — is the attack surface:
whoever controls it can hijack sessions, confuse billing, push firmware,
or switch large amounts of load.

## Attack model

- **Interposition:** on unencrypted OCPP 1.6J WebSocket deployments, a
  network-position attacker can observe or interpose on sessions.
  Lab and cyber-range work (Sandia/INL) demonstrated terminated sessions
  and, chained with charger-side implementation flaws, code execution.
- **Identity hijack:** charger identity long rested on an ID string plus
  a shared or basic credential. An attacker who knows a charger's
  identity can open a *second* connection under it where the CSMS
  mishandles duplicates — hijacking the session, blackholing the real
  charger, or enabling energy theft and billing confusion (SaiFlow,
  2023).
- **Update path:** a spoofed or compromised firmware channel delivers
  malicious firmware to unattended, internet-connected devices.
- **Scale:** simultaneous control of many chargers is the grid concern —
  coordinated load manipulation. This remains an assessed scenario, not
  an observed event.

## Why the design is vulnerable

OCPP 1.6 shipped **without a built-in security model**. Security arrived
later as an optional Open Charge Alliance whitepaper with three profiles:
1 = unencrypted plus basic authentication, 2 = TLS plus basic
authentication, 3 = TLS plus client certificates — so field posture
varies enormously, and no authoritative public census of profile usage
exists. The specification did not define how a CSMS must handle duplicate
simultaneous connections for one charge point. OCPP 2.0.1 builds the
security profiles, security event logging, and signed-firmware support
into the core specification, and the OCA's updated 1.6 certification
(from October 2025) makes Profile 2 and firmware management mandatory in
Core — an industry admission that the old baseline was too weak.

## Detection and mitigation

- **Profile 2 as the floor, Profile 3 as the target:** per-charger client
  certificates and unique credentials; migrate to OCPP 2.0.1. For
  stranded 1.6 fleets, compensating tunnels (SSH/IPsec/VPN, private APN),
  as demonstrated by the Sandia/INL work.
- **CSMS-side discipline:** reject or quarantine duplicate connections
  for one charge-point identity and alert on them; collect OCPP
  security-event notifications and session anomalies centrally.
- **Firmware integrity:** signed updates and secure boot.
- **EVSE hardening:** close unused maintenance ports and services,
  segment charger networks, and fuzz-test implementations — OCPPStorm
  (VehicleSec 2024, in this KB's Research Papers) found five confirmed
  CVEs in two open-source OCPP stacks.
- **Process:** Sandia's multi-lab best-practice guidance (Johnson et al.,
  *Energies* 2022) — owner authentication hardening, cabinet alarms,
  network IDS, code-signed firmware.

## Tools in this KB

- [CheckOCPP](../checkocpp.md) — Wireshark dissector that flags schema violations.
- [EmuOCPP](../emuocpp.md) — network emulator with MitM and downgrade attack demos.
- [EVerest](../everest.md) — the open-source reference charging stack.
- [OCPPStorm](../ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations.md) — the fuzzer behind the CVE findings above.
