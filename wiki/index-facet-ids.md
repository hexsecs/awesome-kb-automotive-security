# Facet: Intrusion detection

IDS, ECU fingerprinting and anomaly attribution.

Generated from page frontmatter by tools/ingest.py; 23 pages (entities and concepts). Do not edit by hand.

## CAN Bus Analysis

- [CANter](canter.md) — Intrusion detection system for CAN and CAN-FD that detects drop-and-spoof attacks using frequency analysis of frame intervals.

## Datasets

- [AutoHack](autohack.md) — Multi-bus CAN dataset from a real vehicle covering C-CAN, P-CAN, and B-CAN, with physically verified fuzzing, spoofing, replay, DoS, and UDS-based attacks.
- [CAN-MIRGU](can-mirgu.md) — CAN bus attack dataset from a modern vehicle driven on real roads over six days, with physically verified masquerade, suspension, and real attacks.
- [Car Hacking Dataset](car-hacking-dataset.md) — HCRL captures from a Kia Soul with labelled DoS, fuzzing, and RPM and gear spoofing injections, the most widely cited baseline in CAN intrusion detection…
- [CarDS](cards.md) — ACSAC 2025 dataset of over nine hours of traffic from a 2020 electric vehicle with 10 CAN buses and 6 automotive Ethernet buses, covering benign driving and…
- [Cross-Vehicle Generalisation Benchmark](cross-vehicle-generalisation-benchmark.md) — Leave-one-vehicle-out benchmark unifying ROAD, CIDv2, and can-train-and-test into 217 captures across eight vehicles for evaluating whether CAN IDS models…
- [GEM-CAN](gem-can.md) — Labelled capture of about 143,000 CAN frames from an autonomous GEM e6 platform, with normal operation, DoS floods, and brake and steering-lock…
- [Survival Analysis Dataset](survival-analysis-dataset.md) — HCRL CAN captures from a Hyundai YF Sonata, Kia Soul, and Chevrolet Spark with labelled flooding, fuzzy, and malfunction attacks.
- [SynCAN](syncan.md) — ETAS synthetic CAN benchmark with continuous, plateau, playback, suspension, and flooding attacks in the signal space, for comparing IDS that work on…
- [TOW-IDS Automotive Ethernet Intrusion Dataset](tow-ids-automotive-ethernet-intrusion-dataset.md) — HCRL captures of AVTP, gPTP, and CAN-over-UDP traffic on an automotive Ethernet network, split into normal driving and five labelled attack scenarios.
- [can-train-and-test](can-train-and-test.md) — Labelled CAN captures from four vehicles across two manufacturers with nine attack types, split into known and unknown vehicle and attack test subsets for…

## Research Papers

- [A Comprehensive Guide to CAN IDS Data and Introduction of the ROAD Dataset](a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset.md) — Verma et al., 2020. Systematises the CAN IDS dataset landscape, documents the flaws in earlier datasets, and introduces ROAD.
- [Evading Voltage-Based Intrusion Detection on Automotive CAN](evading-voltage-based-intrusion-detection-on-automotive-can.md) — Bhatia et al., NDSS 2021. The DUET masquerade attack, in which two compromised ECUs corrupt the bus voltage and defeat every published voltage-based IDS…
- [Fingerprinting Electronic Control Units for Vehicle Intrusion Detection](fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md) — Cho and Shin, USENIX Security 2016. Clock-based IDS that fingerprints ECUs from clock skew in periodic messages, the most-replicated CAN IDS baseline.
- [GIDS: GAN based Intrusion Detection System for In-Vehicle Network](gids-gan-based-intrusion-detection-system-for-in-vehicle-network.md) — Seo, Song, and Kim, PST 2018. Trains a GAN on normal CAN traffic only, and is a common deep-learning IDS baseline alongside the authors' Car-Hacking dataset.
- [On the Real-World Applicability of Automotive CAN Intrusion Detection Systems](on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems.md) — Lazeski et al., USENIX VehicleSec 2026. Work in progress showing that ML-based CAN intrusion detectors often learn dataset shortcuts because common datasets…
- [Viden: Attacker Identification on In-Vehicle Networks](viden-attacker-identification-on-in-vehicle-networks.md) — Cho and Shin, ACM CCS 2017. Fingerprints transmitting ECUs by their analogue voltage signature, moving CAN defence from detecting an attack to naming the…

## Conference Presentations

- [CANdid: A Stealthy Stepping-Stone Attack to Bypass Authentication on ECUs](candid-a-stealthy-stepping-stone-attack-to-bypass-authentication-on-ecus.md) — Kulandaivel, Jain, Guajardo, and Sekar, escar USA 2022. Shows a compromised ECU can authenticate against a safety-critical ECU's SecurityAccess without the…

## Related Awesome Lists

- [Awesome CANb IDs](awesome-canb-ids.md) — CAN bus ID reference and documentation.
- [Awesome CANbus](awesome-canbus.md) — Comprehensive CAN bus security resources.

## Concepts

- [DBC as the CAN semantic layer](concepts/dbc-semantic-layer.md) — A DBC file is the shared contract that turns CAN IDs and bytes into named signals — but it is a human claim about layout, not ground truth.
- [In-vehicle intrusion detection and ECU fingerprinting](concepts/in-vehicle-intrusion-detection.md) — The bus's defence literature, organised by observable signal: timing, clock skew, voltage, learned models — and split by detecting an anomaly vs attributing it.
- [J1939 transport security](concepts/j1939.md) — Heavy-vehicle J1939 has its own request and transport semantics; TP.CM/TP.DT state is attackable in ways generic CAN IDS misses.
