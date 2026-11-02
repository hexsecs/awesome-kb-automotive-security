---
title: "SoK: The Next Frontier in AV Security: Systematizing Perception Attacks and the Emerging Threat of Multi-Sensor Fusion"
summary: "Khan, Islam, and Hasan, arXiv 2026. Systematizes 48 studies of perception-layer attacks into a taxonomy of 20 attack vectors and shows how…"
type: entity
category: "Research Papers"
url: "https://arxiv.org/abs/2604.20621"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Khan, Islam, and Hasan, arXiv 2026. Systematizes 48 studies of perception-layer attacks into a taxonomy of 20 attack vectors and shows how multi-sensor fusion opens cross-modal attacks."
sources:
  - url: "https://arxiv.org/abs/2604.20621"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1109/EuroSP68448.2026.00028"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - sok-how-sensor-attacks-disrupt-autonomous-vehicles-an-end-to-end-analysis-challenges-and-missed-threats
  - invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving
  - adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
  - illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications
  - does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack
  - a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving
---

Khan, Islam, and Hasan, arXiv 2026. Systematizes 48 studies of perception-layer attacks into a taxonomy of 20 attack vectors and shows how multi-sensor fusion opens cross-modal attacks.

## What it is

Shahriar Rahman Khan (Kent State University), Tariqul Islam (University of Maryland, Baltimore County), and Raiful Hasan (Kent State University). *2026 IEEE 11th European Symposium on Security and Privacy (EuroS&P)*, pp. 281–300 — the published version of the arXiv preprint the stub links; read here from that preprint (see Status and sources). A systematization of knowledge (SoK) of attacks on autonomous-vehicle *perception*, scoped strictly to road vehicles: the authors argue road AVs' standardized camera+LiDAR+radar fusion architecture and safety constraints make the analysis sharper than a cross-robotics survey would, and they exclude drones and general robots on that basis. The method is a five-step structured literature review (Wolfs winkel et al.: define, search, select, analyze, present): 124 candidate papers reduced by abstract screening, a 2019–2025 window, and full-text review to a final corpus of 48 peer-reviewed studies. Each study is coded twice over: along seven dimensions (perception modality, attack stage, attack goal, attacker knowledge, attack surface, evaluation environment, and whether multi-sensor fusion is proposed as the defence), and into a unified taxonomy of 20 attack methods (AtkMtd1–AtkMtd20) built from three attack mediums (adversarial patches; 3D adversarial objects; signal spoofers), six attack classes (adversarial perturbation, physical adversarial object, physical object, data poisoning, denial of service, signal spoofing), and five attack goals (hiding, appearing/creating, targeted, non-targeted, move-in/move-out), mapped against the perception modules they strike — traffic sign recognition, monocular depth estimation, visual SLAM, lane detection, object detection/tracking/classification, point cloud generation, semantic segmentation, and trajectory prediction. The taxonomy is drawn as a causal flow diagram (sensor → module → class → objective) whose line thickness is the literature's attention, so its thin and missing paths are themselves a result.

## What it showed

The corpus is lopsided in ways the counts make precise. By stage, input-level manipulation dominates (41 of 48 studies), processing-level attacks are rare (7), and fusion-stage attacks rarer (6); by modality, camera and LiDAR work dwarfs radar, and only seven papers target multi-sensor fusion (MSF) systems at all — most of those by attacking a single modality *into* the fusion, with only a small subset coordinating across sensors synchronously. Attacker knowledge splits by modality: black-box attacks are largely confined to cameras, while LiDAR and radar attacks mostly assume white-box access, and physical-world vectors (including most MSF attacks) are the more accessible class. Evaluation is the field's weak leg: most studies validate on static datasets (KITTI above all) or in simulation, only 15 of 48 include any real-world testing, and fewer still test across weather and lighting. Defences lag the same way: roughly 75% of papers propose no defence or a narrow attack-specific one, only 16 of 48 propose anything fusion-aware, and the recurring mitigation for a single-sensor break is to recommend "add fusion" with no evidence the fusion in question withstands that attack class (Insight 7). Within the taxonomy, two methods concentrate the literature — AtkMtd18 (laser-based LiDAR spoofing, eight works) and AtkMtd2 (the most frequent camera technique) — so defences are shaped by a narrow slice of the space; signal spoofing is the most versatile class, fanning out to the widest range of modules, while physical adversarial objects cluster tightly on object detection. Three research gaps organize the agenda: synchronous multi-modal attacks are barely studied (Gap 1); attacks are evaluated for immediate effect only, with no longitudinal work on gradual degradation — the paper's example, malware slowly corrupting LiDAR calibration, is explicitly hypothetical (Gap 2); and digital-world evaluation cannot establish physical realizability (Gap 3). The gaps persist, the authors argue, for structural reasons: synchronizing a cross-modal attack is experimentally expensive, the community assumes fusion inherently provides security, simulators lack native physical-attack injection, and the required expertise is fragmented across signal processing, machine learning, and automotive engineering. The paper's own proof-of-concept targets Gap 1: a combined infrared-laser and LiDAR spoofing attack designed to manufacture a spatially consistent phantom pedestrian in an early-fusion system, simulated by inserting perspective-matched pedestrian image patches and statistically matched synthetic point clusters into KITTI scenes — the fused model detects the phantom at 0.74 confidence, above the real car's 0.43.

## Where it fits

The perception-bounded companion to Zhang et al.'s end-to-end SoK: where Zhang follows an error until it moves the vehicle, Khan stops at perception's output and instead measures the literature itself — who attacks what, with what knowledge, validated where. Its corpus is substantially this KB's sensor line at full depth: Petit et al. 2015 and Illusion and Dazzle are its signal-spoofing ancestry, Cao et al. 2019 its canonical LiDAR appearing attack, Cao et al. 2021 one of the few genuine MSF studies it can count, and Lou et al. 2024 and Wang et al. 2023 sit in its trajectory-prediction and system-effect corners. The SoK's central verdict — fusion is prescribed as a defence far more often than it is tested as a surface — is the systematized form of what Cao 2021 demonstrated constructively and what the NDSS 2025 realism study implies from the hardware side: redundancy helps only against attacks that fail to coordinate, and coordination is precisely the understudied case. For KB readers its flow diagram is the quickest map of which sensor-to-module paths the literature has actually walked, and its "negative space" (e.g., no documented path from GPS spoofing to semantic-segmentation failure) marks where absence of evidence is not evidence of safety.

## Limits and safety notes

The proof-of-concept is a simulation of sensor *outputs*, not of sensors: the paper devotes a full subsection to what the abstraction omits — atmospheric attenuation of an IR beam over 10–100 m, CMOS saturation and blooming, automotive IR-cut filters above ~700 nm (an invisible 830–980 nm attack needs exponentially higher power to register), and LiDAR pulse timing and receiver processing — and states plainly that it validates the fusion logic's vulnerability *if* the modelled artifacts can be produced, not end-to-end physical feasibility. The page reports the 0.74 figure with that condition attached, and it should never be quoted alongside physically demonstrated results (Cao 2021's printed object, the NDSS 2025 moving-vehicle rig) as if equivalent. The taxonomy's completeness is bounded by its own corpus by the authors' declaration: methods are mutually exclusive at mechanism level, not paper level (one paper can feed several methods), the 2019–2025 window excludes the founding pre-2019 experiments except as cited ancestry, and new methods — the authors name radar-specific perturbations and coordinated MSF attacks — are expected to extend it. Counts quoted from different sections use different cuts and are reported here as printed (fusion-*stage* attacks: 6 of 48; papers *targeting* MSF systems: 7) rather than reconciled. Scope is road-AV perception only: localization appears as a downstream module, planning and control only as consequences, and nothing here systematizes transducer-level physics — that is Zhang's and the primary papers' territory.

## Status and sources

Status: **published**: *2026 IEEE 11th European Symposium on Security and Privacy (EuroS&P)*, pp. 281–300. **DOI 10.1109/EuroSP68448.2026.00028 — verified firsthand against Crossref**: the fetched record's title, all three authors, venue, and page range (281–300) match the paper exactly. The text was read from the open arXiv version (arXiv:2604.20621v1, 22 April 2026), which the stub links; the proceedings PDF itself was not read, so any camera-ready differences from v1 are unexamined. The stub's "arXiv 2026" framing is the list's and stays in the list summary above; the venue of record is EuroS&P 2026.

## Related

- [SoK: How Sensor Attacks Disrupt Autonomous Vehicles](sok-how-sensor-attacks-disrupt-autonomous-vehicles-an-end-to-end-analysis-challenges-and-missed-threats.md)
- [Invisible for Both Camera and LiDAR](invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving.md)
- [Adversarial Sensor Attack on LiDAR-Based Perception](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md)
- [Remote Attacks on Automated Vehicles Sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md)
- [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md)
- [Does Physical Adversarial Example Really Matter to Autonomous Driving](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md)
- [A First Physical-World Trajectory Prediction Attack](a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving.md)
