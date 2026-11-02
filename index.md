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
- [Hardware Interfaces](wiki/index-hardware-interfaces.md) — 9 entries
- [Security Analysis](wiki/index-security-analysis.md) — 6 entries
- [Penetration Testing](wiki/index-penetration-testing.md) — 11 entries
- [Datasets](wiki/index-datasets.md) — 12 entries
- [Research Papers](wiki/index-research-papers.md) — 66 entries
- [Conference Presentations](wiki/index-conference-presentations.md) — 14 entries
- [Books](wiki/index-books.md) — 12 entries
- [Learning Resources](wiki/index-learning-resources.md) — 7 entries
- [Related Awesome Lists](wiki/index-related-awesome-lists.md) — 6 entries

## Concepts

- [Bootloader stages and bootstrap entry](wiki/concepts/bootloader-stages.md) — ECUs boot through layers owned by different parties; the corpus's breaks concentrate at the stage transitions and the weakest stage, not the application.
- [The calibration plane (XCP/A2L)](wiki/concepts/calibration-plane.md) — Beside diagnostics sits a second access plane into production ECUs: XCP's direct memory access and the A2L maps that name everything it can touch.
- [CAN availability and denial of service](wiki/concepts/can-availability.md) — Availability attacks remove or suppress the bus's genuine traffic, below the layer message authentication defends: flooding, bus-off, dominance, silencing.
- [CAN injection](wiki/concepts/can-injection.md) — Attacker taps exposed CAN wiring and impersonates a trusted ECU: classic CAN frames carry no sender authentication, so fake 'key valid' messages are believed.
- [CAN message authentication: the retrofit design space](wiki/concepts/can-message-authentication.md) — Two complete academic designs and the standardised answer, compared on freshness, key scope, frame cost, and evidence — plus the two limits they all share.
- [The EV–EVSE charging trust chain (ISO 15118 / DIN 70121)](wiki/concepts/charging-trust-chain.md) — The vehicle–charger link's trust is a chain — association, transport, contract authorisation — whose links fail independently and are measured failing.
- [Protocol-aware diagnostic fuzzing](wiki/concepts/diagnostic-fuzzing.md) — Fuzzing reaches the deep diagnostic states only when generation is grammar- and state-aware: sessions and SecurityAccess are the fuzzer's real problem.
- [Diagnostic-service abuse](wiki/concepts/diagnostic-service-abuse.md) — The diagnostic service set is the highest-privilege surface on the vehicle network: what it actuates, how its gates fail, and the one case where they held.
- [The vehicle's external attack surface: remote entry and the telematics pivot](wiki/concepts/external-attack-surface.md) — Compromise repeatedly begins at a boundary interface and pivots through the unit crossing it: connectivity units are most exposed and most privileged.
- [Firmware acquisition: the read-side channels](wiki/concepts/firmware-acquisition.md) — Before analysis comes acquisition: the channels the corpus documents for getting an ECU's image out — by bus, by bootstrap, by bench, by log, by package.
- [In-vehicle intrusion detection and ECU fingerprinting](wiki/concepts/in-vehicle-intrusion-detection.md) — The bus's defence literature, organised by observable signal: timing, clock skew, voltage, learned models — and split by detecting an anomaly vs attributing it.
- [IVI runtime privilege and service exposure](wiki/concepts/ivi-runtime-privilege.md) — The head unit's failures that are not on the update path: declared-but-unenforced permissions, unchecked service callers, and designed-in debug surfaces.
- [IVI update-path trust](wiki/concepts/ivi-update-trust.md) — How head-unit update trust anchors fail across six IVI platforms: absent checks, a public test key, a fleet-wide key, CRC-only integrity, patchable verifiers.
- [Key-fob relay attacks](wiki/concepts/key-fob-relay-attacks.md) — Two attackers relay a genuine key's radio exchange, so the car sees a valid key 'nearby' — encryption doesn't help, because nothing was forged, only forwarded.
- [Misbehavior detection in V2X](wiki/concepts/misbehavior-detection.md) — Why V2X needs a layer beyond signatures: detecting false content from validly credentialed stations, reporting it, and the authority that decides.
- [OCPP and charging attacks](wiki/concepts/ocpp-charging-attacks.md) — OCPP links chargers to cloud backends; weak transport security, shared identities and duplicate connections enable hijack, fraud and outage attacks.
- [Physical-channel sensor attacks](wiki/concepts/physical-channel-sensor-attacks.md) — Attacks that manufacture the measurement itself — in acoustics, optics, RF, and heat — where no digital interface is touched and the output is faithfully wrong.
- [Rolling-code failure classes](wiki/concepts/rolling-code-failure-classes.md) — Rolling codes move trust from the code's secrecy to the receiver's counter state; the failure classes attack that state: windows, resync, harvesting, blocking.
- [Secure firmware updates (Uptane)](wiki/concepts/secure-firmware-updates.md) — How Uptane secures vehicle software updates: two repositories, per-vehicle signed instructions, and compromise resilience when servers or keys fall.
- [Shared, default, and global secrets: the break-once pattern](wiki/concepts/shared-and-default-secrets.md) — The decisive failure is rarely cipher strength — it is one secret shared by a fleet or a type, or a default nobody changed. Break one, break all.
- [Simulation and test doubles for vehicle networks](wiki/concepts/simulation-and-test-doubles.md) — The corpus's simulation layer, rung by rung — virtual bus, replay, declarative doubles, physical miniatures — and what each rung cannot tell you.
- [SOME/IP and SOME/IP-SD](wiki/concepts/someip.md) — AUTOSAR's service-oriented middleware over IP: how services are offered, found and invoked — and why discovery is the trust root of every SOME/IP conversation.
- [TARA methodology: the ISO/SAE 21434 artefact chain](wiki/concepts/tara-methodology.md) — How an automotive TARA is actually assembled: the ISO/SAE 21434 artefact chain, the layers the KB's tools occupy, and where automation helps and lies.
- [UDS seed/key (SecurityAccess)](wiki/concepts/uds-seed-key.md) — UDS SecurityAccess (0x27) gates privileged diagnostics behind a seed/key exchange; weak seeds, reused secrets and simple algorithms defeat it.
- [V2X credential management](wiki/concepts/v2x-credential-management.md) — How vehicles get pseudonymous credentials: split-knowledge issuance in the ETSI CCMS and US SCMS, so linking a ticket to an identity takes a quorum.
