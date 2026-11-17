# Facet: Simulation

Virtual buses, replay, SIL/HIL and physical miniatures.

Generated from page frontmatter by tools/ingest.py; 28 pages. Do not edit by hand.

## CAN Bus Analysis

- [BUSMASTER](busmaster.md) — Open-source CAN simulation, analysis, and test tool from Bosch Engineering and ETAS, with a node simulator, DBC-driven signal interpretation, and scriptable…
- [CAN Commander](can-commander.md) — Flipper Zero application and companion ESP32 CAN board for reverse engineering vehicle networks, with sniffing, DBC decoding, replay, and injection profiles…
- [CANdevStudio](candevstudio.md) — Flow-based graphical CAN simulation environment that wires senders, receivers, DBC decoders, and signal viewers together to stand in for missing ECUs on a…
- [Carpunk](carpunk.md) — CAN injection toolkit and successor to CANghost, automating interface setup, sniffing, replay, and injection attacks.
- [ICSim](icsim.md) — Instrument Cluster Simulator for safe CAN bus security testing with virtual dashboard controls.
- [pycangui](pycangui.md) — Graphical CAN bus tool with live trace and plots, transmit, CANopen, UDS, J1939, and XCP/CCP support on any python-can adapter, with Python scripting and…

## Diagnostic Tools

- [UDSim](udsim.md) — UDS (Unified Diagnostic Services) ECU simulator and fuzzer for discovering and testing UDS services.
- [doip-sim-ecu-dsl](doip-sim-ecu-dsl.md) — Kotlin DSL for scripting simulated DoIP ECUs, reachable over Ethernet, CAN with ISO-TP, or both at once, for exercising diagnostic clients against UDS error…
- [uds-server](uds-server.md) — UDS ECU simulator and fuzzer for use alongside ICSim, for practising diagnostic command discovery and fuzzing scan tools.
- [uds](uds.md) — Python package for ISO 14229 UDS in both client and server roles over CAN, Ethernet, LIN, FlexRay, and K-Line, usable for simulation, testing, and decoding…

## V2X Security

- [Artery](artery.md) — OMNeT++ simulation framework pairing the Vanetza ITS-G5 stack with SUMO traffic, providing the environment that most misbehavior-detection and V2X attack…
- [F2MD](f2md.md) — Simulation framework recreating the whole misbehavior detection chain for ITS-G5 and C-V2X, with plausibility checks, machine learning detectors, and both…
- [V2Verifier](v2verifier.md) — Open-source V2X security testbed with first open-source IEEE 1609.2 implementation for DSRC and C-V2X.
- [VaN3Twin](van3twin.md) — ETSI-compliant multi-stack V2X framework for ns-3 covering ITS-G5, C-V2X, and LTE with SUMO and CARLA co-simulation; the continuation of ms-van3t.
- [Veins](veins.md) — Open-source vehicular network simulation framework coupling OMNeT++ and SUMO, used as the testbed for VANET and V2X security and attack studies.

## EV Charging Security

- [V2Gdecoder](v2gdecoder.md) — Encodes and decodes EXI-compressed V2G messages on the fly, turning captured ISO 15118 exchanges into editable XML for replay and fuzzing.

## Hardware Interfaces

- [RAMN](ramn.md) — Resistant Automotive Miniature Network, a four-ECU CAN/CAN FD testbed on a single board with KiCad sources, CARLA closed-loop simulation, and use as the Car…

## Security Analysis

- [AutoTARA](autotara.md) — Web-based TARA (Threat Analysis and Risk Assessment) framework for ISO/SAE 21434 that models systems as attack graphs and applies MITRE's CTSA/CRRA…

## Datasets

- [AutoHack](autohack.md) — Multi-bus CAN dataset from a real vehicle covering C-CAN, P-CAN, and B-CAN, with physically verified fuzzing, spoofing, replay, DoS, and UDS-based attacks.
- [Cross-Vehicle Generalisation Benchmark](cross-vehicle-generalisation-benchmark.md) — Leave-one-vehicle-out benchmark unifying ROAD, CIDv2, and can-train-and-test into 217 captures across eight vehicles for evaluating whether CAN IDS models…
- [SynCAN](syncan.md) — ETAS synthetic CAN benchmark with continuous, plateau, playback, suspension, and flooding attacks in the signal space, for comparing IDS that work on…
- [TOW-IDS Automotive Ethernet Intrusion Dataset](tow-ids-automotive-ethernet-intrusion-dataset.md) — HCRL captures of AVTP, gPTP, and CAN-over-UDP traffic on an automotive Ethernet network, split into normal driving and five labelled attack scenarios.
- [VeReMi Extension](veremi-extension.md) — Simulated V2X misbehavior detection dataset generated with F2MD over the Luxembourg SUMO scenario, labelling position, speed, timing, replay, DoS, and Sybil…

## Research Papers

- [RollBack: A New Time-Agnostic Replay Attack Against the Automotive Remote Keyless Entry Systems](rollback-a-new-time-agnostic-replay-attack-against-the-automotive-remote-keyless-entry-systems.md) — Csikor et al., Black Hat USA 2022. Replaying already-invalid rolling codes in sequence triggers a resynchronisation rollback, unlocking a vehicle…

## Conference Presentations

- [How I Discovered and Hacked Learning Codes of the Key Fob of a Car Assembled in My Country](how-i-discovered-and-hacked-learning-codes-of-the-key-fob-of-a-car-assembled-in-my-country.md) — Erazo, DEF CON 32 Car Hacking Village 2024. Breaks the learning-code key fob of a locally assembled car with replay, a receiver backdoor, and a brute-force…

## Learning Resources

- [Automotive Cybersecurity Roadmap](automotive-cybersecurity-roadmap.md) — Structured learning path from CAN and UDS fundamentals through TARA, firmware reverse engineering, and hardware hacking into specialized career tracks.
- [OpenGarages](opengarages.md) — Open vehicle research collective behind the Car Hacker's Handbook, publishing the free edition of the book, ICSim, and workshop material for hands-on…

## Concepts

- [Simulation and test doubles for vehicle networks](concepts/simulation-and-test-doubles.md) — The corpus's simulation layer, rung by rung — virtual bus, replay, declarative doubles, physical miniatures — and what each rung cannot tell you.
