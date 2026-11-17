# Facet: V2X

Vehicle-to-everything, pseudonym credentials and misbehaviour reporting.

Generated from page frontmatter by tools/ingest.py; 16 pages. Do not edit by hand.

## V2X Security

- [Artery](artery.md) — OMNeT++ simulation framework pairing the Vanetza ITS-G5 stack with SUMO traffic, providing the environment that most misbehavior-detection and V2X attack…
- [F2MD](f2md.md) — Simulation framework recreating the whole misbehavior detection chain for ITS-G5 and C-V2X, with plausibility checks, machine learning detectors, and both…
- [V2Verifier](v2verifier.md) — Open-source V2X security testbed with first open-source IEEE 1609.2 implementation for DSRC and C-V2X.
- [VASP](vasp.md) — V2X Application Spoofing Platform from Qualcomm that runs a library of BSM spoofing and falsification attacks on top of Veins, the artifact of the…
- [VaN3Twin](van3twin.md) — ETSI-compliant multi-stack V2X framework for ns-3 covering ITS-G5, C-V2X, and LTE with SUMO and CARLA co-simulation; the continuation of ms-van3t.
- [Vanetza](vanetza.md) — Open-source ETSI C-ITS protocol stack covering GeoNetworking, BTP, DCC, and the security layer, widely used as the reference implementation for V2X…
- [Veins](veins.md) — Open-source vehicular network simulation framework coupling OMNeT++ and SUMO, used as the testbed for VANET and V2X security and attack studies.

## Datasets

- [VeReMi Extension](veremi-extension.md) — Simulated V2X misbehavior detection dataset generated with F2MD over the Luxembourg SUMO scenario, labelling position, speed, timing, replay, DoS, and Sybil…

## Research Papers

- [Pseudonym Schemes in Vehicular Networks: A Survey](pseudonym-schemes-in-vehicular-networks-a-survey.md) — Petit, Schaub, Feiri, and Kargl, IEEE Communications Surveys and Tutorials 2015. Defines the pseudonym lifecycle and categorises the schemes that reconcile…
- [Secure Vehicular Communication Systems: Design and Architecture](secure-vehicular-communication-systems-design-and-architecture.md) — Papadimitratos et al., IEEE Communications Magazine 2008. The SeVeCom architecture, which defined the certificate and pseudonym model underlying today's V2X…
- [Securing Vehicular Ad Hoc Networks](securing-vehicular-ad-hoc-networks.md) — Raya and Hubaux, Journal of Computer Security 2007. Threat analysis and security architecture for VANETs that set the direction for most later V2X security…

## Conference Presentations

- [Back-connect to the Connected Car. Search for Vulnerabilities in the VW Electric Car.](back-connect-to-the-connected-car-search-for-vulnerabilities-in-the-vw-electric-car.md) — Serdyuk, Kondikov, Razmakhnin, and Sakr, Black Hat Europe 2022. Maps the attack surface of the VW ID.3 across Wi-Fi, Bluetooth, V2X, cellular, CAN, and…

## Books

- [Automotive Cyber Security](automotive-cyber-security.md) — Shiho Kim and Rakesh Shrestha, Springer 2020. Academic introduction to connected and autonomous vehicle security, threats, and the standardisation landscape.
- [Hacking Connected Cars](hacking-connected-cars.md) — Alissa Knight, Wiley 2020. Tactics, techniques, and procedures for penetration testing, threat modelling, and risk assessment of telematics control units…

## Concepts

- [Misbehavior detection in V2X](concepts/misbehavior-detection.md) — Why V2X needs a layer beyond signatures: detecting false content from validly credentialed stations, reporting it, and the authority that decides.
- [V2X credential management](concepts/v2x-credential-management.md) — How vehicles get pseudonymous credentials: split-knowledge issuance in the ETSI CCMS and US SCMS, so linking a ticket to an identity takes a quorum.
