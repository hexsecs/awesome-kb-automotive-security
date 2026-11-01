# Automotive Security (Awesome KB)

Knowledge base for automotive security, ingested from the curated awesome list hexsecs/awesome-automotive-security.
Generated from page frontmatter by tools/ingest.py; do not edit by hand.

## Categories

- [CAN Bus Analysis](wiki/index-can-bus-analysis.md) — 28 entries
- [Diagnostic Tools](wiki/index-diagnostic-tools.md) — 19 entries
- [Firmware and ECU Reverse Engineering](wiki/index-firmware-and-ecu-reverse-engineering.md) — 7 entries
- [Automotive Ethernet](wiki/index-automotive-ethernet.md) — 6 entries
- [RF and Key Fob Analysis](wiki/index-rf-and-key-fob-analysis.md) — 6 entries
- [Infotainment and IVI](wiki/index-infotainment-and-ivi.md) — 6 entries
- [V2X Security](wiki/index-v2x-security.md) — 6 entries
- [EV Charging Security](wiki/index-ev-charging-security.md) — 11 entries
- [Hardware Interfaces](wiki/index-hardware-interfaces.md) — 8 entries
- [Security Analysis](wiki/index-security-analysis.md) — 6 entries
- [Penetration Testing](wiki/index-penetration-testing.md) — 11 entries
- [Datasets](wiki/index-datasets.md) — 12 entries
- [Research Papers](wiki/index-research-papers.md) — 65 entries
- [Conference Presentations](wiki/index-conference-presentations.md) — 14 entries
- [Books](wiki/index-books.md) — 12 entries
- [Learning Resources](wiki/index-learning-resources.md) — 7 entries
- [Related Awesome Lists](wiki/index-related-awesome-lists.md) — 6 entries

## Concepts

- [CAN injection](wiki/concepts/can-injection.md) — Attacker taps exposed CAN wiring and impersonates a trusted ECU: classic CAN frames carry no sender authentication, so fake 'key valid' messages are believed.
- [Key-fob relay attacks](wiki/concepts/key-fob-relay-attacks.md) — Two attackers relay a genuine key's radio exchange, so the car sees a valid key 'nearby' — encryption doesn't help, because nothing was forged, only forwarded.
- [OCPP and charging attacks](wiki/concepts/ocpp-charging-attacks.md) — OCPP links chargers to cloud backends; weak transport security, shared identities and duplicate connections enable hijack, fraud and outage attacks.
- [Secure firmware updates (Uptane)](wiki/concepts/secure-firmware-updates.md) — How Uptane secures vehicle software updates: two repositories, per-vehicle signed instructions, and compromise resilience when servers or keys fall.
- [SOME/IP and SOME/IP-SD](wiki/concepts/someip.md) — AUTOSAR's service-oriented middleware over IP: how services are offered, found and invoked — and why discovery is the trust root of every SOME/IP conversation.
- [UDS seed/key (SecurityAccess)](wiki/concepts/uds-seed-key.md) — UDS SecurityAccess (0x27) gates privileged diagnostics behind a seed/key exchange; weak seeds, reused secrets and simple algorithms defeat it.
