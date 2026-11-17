# Concept map

The concept layer organised by theme, with reading paths through it. Generated from tools/taxonomy.py and concept frontmatter; do not edit by hand.

## The bus and its protocols

What the in-vehicle networks say, and how their assumptions fail.

- [CAN injection](concepts/can-injection.md) — Attacker taps exposed CAN wiring and impersonates a trusted ECU: classic CAN frames carry no sender authentication, so fake 'key valid' messages are believed.
- [CAN availability and denial of service](concepts/can-availability.md) — Availability attacks remove or suppress the bus's genuine traffic, below the layer message authentication defends: flooding, bus-off, dominance, silencing.
- [DBC as the CAN semantic layer](concepts/dbc-semantic-layer.md) — A DBC file is the shared contract that turns CAN IDs and bytes into named signals — but it is a human claim about layout, not ground truth.
- [CAN message authentication: the retrofit design space](concepts/can-message-authentication.md) — Two complete academic designs and the standardised answer, compared on freshness, key scope, frame cost, and evidence — plus the two limits they all share.
- [In-vehicle intrusion detection and ECU fingerprinting](concepts/in-vehicle-intrusion-detection.md) — The bus's defence literature, organised by observable signal: timing, clock skew, voltage, learned models — and split by detecting an anomaly vs attributing it.
- [LIN as the trusted subordinate bus](concepts/lin-bus.md) — LIN sits behind gateways on door modules and sensors, so it is treated as trusted — yet its wiring is often the most reachable.
- [J1939 transport security](concepts/j1939.md) — Heavy-vehicle J1939 has its own request and transport semantics; TP.CM/TP.DT state is attackable in ways generic CAN IDS misses.
- [ISO-TP: the stateful transport under diagnostics](concepts/iso-tp.md) — ISO 15765-2 reassembles multi-frame diagnostic payloads on CAN; its flow-control state machine is an attacker-controllable resource.

## Access, diagnostics and updates

The privileged paths into an ECU, and where their gates break.

- [Diagnostic-service abuse](concepts/diagnostic-service-abuse.md) — The diagnostic service set is the highest-privilege surface on the vehicle network: what it actuates, how its gates fail, and the one case where they held.
- [UDS seed/key (SecurityAccess)](concepts/uds-seed-key.md) — UDS SecurityAccess (0x27) gates privileged diagnostics behind a seed/key exchange; weak seeds, reused secrets and simple algorithms defeat it.
- [Protocol-aware diagnostic fuzzing](concepts/diagnostic-fuzzing.md) — Fuzzing reaches the deep diagnostic states only when generation is grammar- and state-aware: sessions and SecurityAccess are the fuzzer's real problem.
- [DoIP moves diagnostics onto the network](concepts/doip.md) — DoIP replaces the physical OBD port with a routable endpoint; discovery and routing activation become the new trust boundary.
- [The calibration plane (XCP/A2L)](concepts/calibration-plane.md) — Beside diagnostics sits a second access plane into production ECUs: XCP's direct memory access and the A2L maps that name everything it can touch.
- [Firmware acquisition: the read-side channels](concepts/firmware-acquisition.md) — Before analysis comes acquisition: the channels the corpus documents for getting an ECU's image out — by bus, by bootstrap, by bench, by log, by package.
- [Bootloader stages and bootstrap entry](concepts/bootloader-stages.md) — ECUs boot through layers owned by different parties; the corpus's breaks concentrate at the stage transitions and the weakest stage, not the application.
- [Secure firmware updates (Uptane)](concepts/secure-firmware-updates.md) — How Uptane secures vehicle software updates: two repositories, per-vehicle signed instructions, and compromise resilience when servers or keys fall.
- [IVI update-path trust](concepts/ivi-update-trust.md) — How head-unit update trust anchors fail across six IVI platforms: absent checks, a public test key, a fleet-wide key, CRC-only integrity, patchable verifiers.
- [IVI runtime privilege and service exposure](concepts/ivi-runtime-privilege.md) — The head unit's failures that are not on the update path: declared-but-unenforced permissions, unchecked service callers, and designed-in debug surfaces.

## The external boundary

Where the vehicle meets the radio, the charger and the road.

- [The vehicle's external attack surface: remote entry and the telematics pivot](concepts/external-attack-surface.md) — Compromise repeatedly begins at a boundary interface and pivots through the unit crossing it: connectivity units are most exposed and most privileged.
- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md) — Two attackers relay a genuine key's radio exchange, so the car sees a valid key 'nearby' — encryption doesn't help, because nothing was forged, only forwarded.
- [Rolling-code failure classes](concepts/rolling-code-failure-classes.md) — Rolling codes move trust from the code's secrecy to the receiver's counter state; the failure classes attack that state: windows, resync, harvesting, blocking.
- [Shared, default, and global secrets: the break-once pattern](concepts/shared-and-default-secrets.md) — The decisive failure is rarely cipher strength — it is one secret shared by a fleet or a type, or a default nobody changed. Break one, break all.
- [The EV–EVSE charging trust chain (ISO 15118 / DIN 70121)](concepts/charging-trust-chain.md) — The vehicle–charger link's trust is a chain — association, transport, contract authorisation — whose links fail independently and are measured failing.
- [OCPP and charging attacks](concepts/ocpp-charging-attacks.md) — OCPP links chargers to cloud backends; weak transport security, shared identities and duplicate connections enable hijack, fraud and outage attacks.
- [V2X credential management](concepts/v2x-credential-management.md) — How vehicles get pseudonymous credentials: split-knowledge issuance in the ETSI CCMS and US SCMS, so linking a ticket to an identity takes a quorum.
- [Misbehavior detection in V2X](concepts/misbehavior-detection.md) — Why V2X needs a layer beyond signatures: detecting false content from validly credentialed stations, reporting it, and the authority that decides.
- [Physical-channel sensor attacks](concepts/physical-channel-sensor-attacks.md) — Attacks that manufacture the measurement itself — in acoustics, optics, RF, and heat — where no digital interface is touched and the output is faithfully wrong.
- [SOME/IP and SOME/IP-SD](concepts/someip.md) — AUTOSAR's service-oriented middleware over IP: how services are offered, found and invoked — and why discovery is the trust root of every SOME/IP conversation.
- [DoIP moves diagnostics onto the network](concepts/doip.md) — DoIP replaces the physical OBD port with a routable endpoint; discovery and routing activation become the new trust boundary.

## Method and evidence

How the work is modelled, simulated and reasoned about.

- [TARA methodology: the ISO/SAE 21434 artefact chain](concepts/tara-methodology.md) — How an automotive TARA is actually assembled: the ISO/SAE 21434 artefact chain, the layers the KB's tools occupy, and where automation helps and lies.
- [Simulation and test doubles for vehicle networks](concepts/simulation-and-test-doubles.md) — The corpus's simulation layer, rung by rung — virtual bus, replay, declarative doubles, physical miniatures — and what each rung cannot tell you.

## Reading paths

### Steal the car without the key

From physical access to a forged status claim, then the defences proposed against it.

1. [CAN injection](concepts/can-injection.md)
2. [Rolling-code failure classes](concepts/rolling-code-failure-classes.md)
3. [Key-fob relay attacks](concepts/key-fob-relay-attacks.md)
4. [CAN message authentication: the retrofit design space](concepts/can-message-authentication.md)
5. [In-vehicle intrusion detection and ECU fingerprinting](concepts/in-vehicle-intrusion-detection.md)

### Own the ECU

The privileged path: get access, get the image, understand the boot chain, break the update.

1. [Diagnostic-service abuse](concepts/diagnostic-service-abuse.md)
2. [UDS seed/key (SecurityAccess)](concepts/uds-seed-key.md)
3. [Firmware acquisition: the read-side channels](concepts/firmware-acquisition.md)
4. [Bootloader stages and bootstrap entry](concepts/bootloader-stages.md)
5. [Secure firmware updates (Uptane)](concepts/secure-firmware-updates.md)
6. [IVI update-path trust](concepts/ivi-update-trust.md)

### Plug in and pivot

Charging and V2X as trust chains rather than single protocols.

1. [The EV–EVSE charging trust chain (ISO 15118 / DIN 70121)](concepts/charging-trust-chain.md)
2. [OCPP and charging attacks](concepts/ocpp-charging-attacks.md)
3. [V2X credential management](concepts/v2x-credential-management.md)
4. [Misbehavior detection in V2X](concepts/misbehavior-detection.md)
5. [The vehicle's external attack surface: remote entry and the telematics pivot](concepts/external-attack-surface.md)

### Speak the protocol

The semantic layers that turn bytes and timing into meaning — and into attack surface.

1. [DBC as the CAN semantic layer](concepts/dbc-semantic-layer.md)
2. [ISO-TP: the stateful transport under diagnostics](concepts/iso-tp.md)
3. [J1939 transport security](concepts/j1939.md)
4. [LIN as the trusted subordinate bus](concepts/lin-bus.md)
5. [SOME/IP and SOME/IP-SD](concepts/someip.md)
6. [The calibration plane (XCP/A2L)](concepts/calibration-plane.md)
