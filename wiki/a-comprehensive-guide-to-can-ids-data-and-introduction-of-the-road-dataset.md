---
title: "A Comprehensive Guide to CAN IDS Data and Introduction of the ROAD Dataset"
summary: "Verma et al., 2020. Systematises the CAN IDS dataset landscape, documents the flaws in earlier datasets, and introduces ROAD."
type: entity
category: "Research Papers"
url: "https://arxiv.org/abs/2012.14600"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Verma et al., 2020. Systematises the CAN IDS dataset landscape, documents the flaws in earlier datasets, and introduces ROAD."
sources:
  - url: "https://arxiv.org/abs/2012.14600"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1371/journal.pone.0296879"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - gids-gan-based-intrusion-detection-system-for-in-vehicle-network
  - on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems
  - evading-voltage-based-intrusion-detection-on-automotive-can
  - car-hacking-dataset
  - can-train-and-test
  - in-vehicle-intrusion-detection
---

Verma et al., 2020. Systematises the CAN IDS dataset landscape, documents the flaws in earlier datasets, and introduces ROAD.

## What it is

Miki E. Verma (Rewiring America), Robert A. Bridges, Michael D. Iannacone, Samuel C. Hollifield, Pablo Moriano, Steven C. Hespeler, and Frank L. Combs (Oak Ridge National Laboratory; Kay also PNNL). Two contributions in one paper: the first comprehensive guide to the publicly available CAN intrusion-detection datasets — HCRL's OTIDS, Survival Analysis, and Car Hacking datasets, Bosch's SynCAN, TU Eindhoven's Automotive CAN Bus Intrusion v2, and CrySyS Lab's Can Log Infector — each given a hands-on quality analysis; and ROAD (Real ORNL Automotive Dynamometer), a new dataset of real CAN data with physically verified attacks. arXiv:2012.14600 (December 2020); version of record PLOS ONE 19(1), 2024 (see Status and sources).

## What it showed

**Framework.** The guide adopts Cho & Shin's attack taxonomy: *fabrication* (frames added), *suspension* (an ID's frames removed), and *masquerade* (the legitimate sender silenced, spoofed frames sent in its place at a realistic rate). It adds a detection-oriented axis: an attack is *timing transparent* if it disturbs message timing or ID distributions, hence visible to frequency-based IDSs, and *timing opaque* if it does not — timing-opaque attacks (masquerade above all) can only be caught by payload-, signal-based, or physical side-channel methods. IDS methods themselves sort into five families: frequency/timing, payload, signal-based, physical side-channel, and other.

**The verdict on prior datasets.** Across the six pre-ROAD datasets, the only real attacks in real data are fabrication (simple injection) attacks; everything else is simulated attacks in real logs or fully synthetic data, and physical effects of attacks on the vehicle are generally not verified. Only one dataset (SynCAN) provides signal-translated data, with no corresponding raw binary version. The available fabrication attacks are usually blatant floods that disrupt bus timing, "too easily detectable to truly test the method"; the authors' summary is that the data "pigeon-holes" the field and has stymied comparability (of 65 surveyed anomaly-detection papers, 37 used simulated data, only 4 a baseline).

Per dataset, from the authors' own analyses:

- **OTIDS** (Kia Soul): injected messages are unlabelled, and the documented injection intervals are unclear and, on the authors' analysis, incorrect — attacks appear to run the whole capture, not from ~250 s as documented. The advertised "impersonation" attack is not a masquerade: the legitimate node was not suspended, so genuine and malicious remote-frame responses both appear — a fabrication attack. Verdict: not recommended unless an IDS uses remote frames.
- **Survival Analysis** (Hyundai Sonata, Kia Soul, Chevrolet Spark): the only dataset with real attacks on multiple vehicles, injections labelled — but every attack is blatant enough for "a very simple timing-based detector" and only 60–90 s of ambient data per vehicle is provided.
- **Car Hacking** (Hyundai YF Sonata — the dataset the GIDS paper introduced): the most widely used in the literature, but each attack capture ends in a long silent gap (≈22 s after the DoS capture, on the order of 3,000 s in the other three), an undocumented artifact the authors attribute to the bus entering stand-by because the vehicle was not driven during the attacks — while the ambient data was recorded driving, so test differs from training beyond the injections. (The guide gives trim points to salvage them.)
- **SynCAN** (Bosch): synthetic and signal-only. It holds the most nuanced masquerade attacks then available (signal values slowly drifting, replay) — but synthetic data is "somewhat 'cleaner' than in the real case," attack effects cannot be verified, no held-out ambient data is provided for false-positive testing, and with no raw version most detectors cannot consume it at all.
- **TU Eindhoven v2** (Opel Astra, Renault Clio, testbed): the only public diagnostic-protocol attack and the only simulated suspension attacks in real data — but the attacks were manufactured by editing logs ("added packets manually and adjusted timestamps accordingly"), destroying the arbitration-dependent timing fidelity; the DoS is 10 s of overwritten frames, and labels sit in an unstructured text file.
- **Can Log Infector** (CrySyS Lab): no attack data at all — open-source tooling to synthesise seven masquerade types in any ambient log. Modification is byte-level only (signals crossing byte boundaries cannot be targeted), the attack end point cannot be specified, and vehicle effects are unverifiable by construction.

**What ROAD contains.** One vehicle (mid-2010s; make and model withheld by ORNL, and the data obfuscated: IDs remapped one-to-one without preserving arbitration order, data fields scrambled consistently per ID, reserved/diagnostic-ID messages removed, timestamps shifted), captured via SocketCAN and a Kvaser Leaf Light V2 on the OBD-II port (timestamps 100 µs accurate). Twelve ambient captures (~3 h; 3 h 27 m of raw CAN in total), on roads and dynamometer, including deliberate anomalies (a door opened while driving) for false-positive testing. Thirty-three attack captures (~30 min), every one executed with the vehicle driven on the dynamometer and its physical effect verified, ordered by expected detection difficulty: a deliberately easy fuzzing attack (cycling IDs, maximum payload, every 5 ms); targeted-ID fabrication by *flam* delivery — exactly one injected frame immediately after each legitimate frame of the target ID, only the target signal's bits altered, the stealthiest fabrication possible — against four targets (Correlated Signal: four false wheel speeds on one ID, after which the accelerator has no effect; Max Speedometer and Max Engine Coolant Temperature: signal forced to 0xFF; Reverse Light On/Off: a 1-bit signal); and the Accelerator Attack, captures of the vehicle compromised through a newly discovered, responsibly disclosed vulnerability — it accelerates to a fixed speed in Drive and another in Reverse regardless of pedal or cruise control, braking normally — with *no injected messages at all*: only the vehicle's own ECUs transmit, making it timing opaque by construction. For each targeted-ID attack a simulated masquerade version is also provided (13 files), made by deleting the legitimate target-ID frames preceding each injection: every message in them was really on the bus in that order, but the guide is explicit that the masquerade aspect is simulated and no public capture of a real masquerade attack exists. Signal-translated time series (via the authors' CAN-D decoder, SynCAN-style CSV with per-frame labels) are provided for all ambient and 17 of 33 attack captures; raw logs carry interval-level labels in JSON metadata, not per-message. ROAD tests frequency/timing, payload, and signal-based detectors; dataset DOI 10.5281/zenodo.10462795 (the dataset's, not the paper's).

**ROAD's own stated drawbacks:** attacks only on a dynamometer; a single vehicle; 100 µs timestamp accuracy may be too coarse for some timing detectors; interval rather than per-message labels; obfuscation does not preserve ID priority order; nothing usable for physical-layer detection; masquerade attacks rely on a small amount of simulation. The conclusion names the gaps remaining open for everyone: real masquerade attack data, more real signal-translated data with attacks, and CAN data with physical-level characteristics (e.g. voltage).

## Where it fits

The dataset-side foundation of this cluster. The GIDS page describes the Car Hacking dataset from its makers' side; this guide is the independent audit of that dataset and its five peers, and its findings ground the model-side shortcut critique in the Lazeski paper. Its taxonomy is the vocabulary the IDS & fingerprinting concept page uses to say which detector class can even in principle see which attack.

## Limits and safety notes

- The Accelerator Attack is documented by its physical effects only: the vulnerability was responsibly disclosed to the OEM, and the paper withholds both the exploit and the CAN data recorded during it. Nothing about the mechanism is stated or should be inferred.
- The ROAD vehicle is anonymized by the authors' institution and the data deliberately obfuscated; it must not be named or guessed.
- Two conclusions are the authors' inferences, labelled as such in the paper: the stand-by explanation for the Car Hacking gaps is a hypothesis; the OTIDS discrepancies are reported as found documentation inconsistencies.
- ROAD's masquerade captures are simulated by construction (above); describing ROAD as containing real masquerade attacks contradicts the paper.

## Status and sources

Status: **published** — a finished publication and a released dataset. Bibliographic record: PLOS ONE 19(1): e0296879 (22 January 2024); DOI [10.1371/journal.pone.0296879](https://doi.org/10.1371/journal.pone.0296879), verified against Crossref (title and full author list match). Full text read end-to-end from arXiv:2012.14600v3 (7 February 2024), 2026-11-01; dataset at Zenodo, DOI 10.5281/zenodo.10462795 (as cited in the paper).

## Related

- [GIDS: GAN based Intrusion Detection System for In-Vehicle Network](gids-gan-based-intrusion-detection-system-for-in-vehicle-network.md) — introduces the Car Hacking dataset this guide audits
- [On the Real-World Applicability of Automotive CAN Intrusion Detection Systems](on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems.md) — the model-side sequel: what learners do with these datasets
- [Evading Voltage-Based Intrusion Detection on Automotive CAN](evading-voltage-based-intrusion-detection-on-automotive-can.md) — the physical side-channel line ROAD does not serve
- [Car Hacking Dataset](car-hacking-dataset.md)
- [can-train-and-test](can-train-and-test.md)
