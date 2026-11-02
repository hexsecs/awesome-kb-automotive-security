---
title: "Invisible for both Camera and LiDAR: Security of Multi-Sensor Fusion based Perception in Autonomous Driving"
summary: "Cao et al., IEEE S&P 2021. Defeats the multi-sensor fusion designs that production stacks actually use, with a single adversarial object invisible to camera…"
type: entity
category: "Research Papers"
url: "https://arxiv.org/abs/2106.09249"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Cao et al., IEEE S&P 2021. Defeats the multi-sensor fusion designs that production stacks actually use, with a single adversarial object invisible to camera and LiDAR at once."
sources:
  - url: "https://arxiv.org/abs/2106.09249"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1109/SP40001.2021.00076"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
  - illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications
  - does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack
  - a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving
  - sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion
---

Cao et al., IEEE S&P 2021. Defeats the multi-sensor fusion designs that production stacks actually use, with a single adversarial object invisible to camera and LiDAR at once.

## What it is

Yulong Cao and Mingyan Liu (University of Michigan), Ningfei Wang and Qi Alfred Chen (UC Irvine), Chaowei Xiao (NVIDIA; Arizona State University), Dawei Yang (Michigan), Jin Fang (Baidu Research), Ruigang Yang (Inceptio), and Bo Li (University of Illinois at Urbana-Champaign). *42nd IEEE Symposium on Security and Privacy (S&P 2021)*, pp. 176–194. The first security study of multi-sensor fusion (MSF) based perception — the design production high-level AVs (the paper names Waymo, Pony.ai, and Baidu Apollo) predominantly use, fusing camera and LiDAR results on the assumption that not all sources can be attacked at the same time, so a fusion algorithm can always fall back on an unattacked source. The paper challenges that assumption directly, with the most direct attack goal available: make the victim AV fail to detect a front obstacle and crash into it. (An earlier, shorter version of the attack appeared at MLSys 2020.) Prior physical-world attacks each move only one modality — stickers and paint change an object's texture, which a camera reads and a LiDAR does not; laser spoofing injects LiDAR points and does nothing for a camera — so the authors' first move is choosing a vector that moves both: an object's *shape*, which determines both where its LiDAR points land and which pixels it covers.

## What it showed

**MSF-ADV.** Starting from a benign object's 3D mesh (a traffic cone is the running example), the method moves mesh vertices by projected gradient descent under an L∞ bound ε, with Laplacian-smoothness and printability losses and expectation-over-transformation over victim positions for robustness; texture is deliberately left untouched, for stealth and printability. Two constructions make the optimization possible. Differentiable renderers synthesize the object's camera image and LiDAR point cloud consistently, each from its own sensor mounting position. And because production LiDAR perception pre-processes point clouds into cell-level aggregated features (per-cell means of height, intensity, and similar, in 3D voxels or 2D bird's-eye cells) whose computation turns on a discontinuous point-inclusion test, the paper derives a differentiable approximation of point-inclusion and builds every commonly used aggregated feature differentiably from it — the piece prior attack pipelines lacked. For the rule-based (late) fusion that Apollo and Autoware.AI ship, the objective minimizes the object's detection confidence in the LiDAR and camera networks separately: if it is undetected in both outputs, no fusion rule can resurrect it, so the reported success rate is a lower bound for any specific fusion logic.

**Effectiveness.** Targets: LiDAR models from Baidu Apollo v5.5 (A5-L) and v2.5 (A2-L), a camera model from Apollo v5.5 (A5-C), and YOLO v3 as shipped in Autoware.AI (Y3) — 4 MSF combinations; 3 object types (traffic cone, bench, toy car), 100 real-world KITTI driving scenarios each, object placed 7 m ahead. Success — undetected by both models — is **at least 91% for every combination and object type**, and 100% for the traffic cone and bench; the toy car, an object type training data covers heavily, still falls at 91–97%. The perturbations are small: at ε = 2 cm the average vertex moves 3.4 cm, and success stays above 93% even at ε = 1 cm (1.5 cm average). Baselines at the same perturbation level collapse — Gaussian shape noise succeeds 8%, a genetic algorithm 9% — so the result belongs to the optimization, not the budget. Objects generated against one combination transfer to the others at ~75% average success, and with EoT the attack holds above 95% across victim approach distances of 5–35 m. A user study (105 participants) rated the adversarial cone as innocent as a benign one, and less suspicious than some genuinely broken benign cones.

**Physical realizability.** A 3D-printed adversarial cube (1:1 scale) placed on a real road in front of a vehicle carrying a Velodyne HDL-64E was detected in only **1 of 108 collected frames**; the benign cube was detected in 84.8% of its frames. In miniature-scale (1:6.67) experiments with a real camera and VLP-16 — the both-sensor physical test — the adversarial cone evaded both at 90% of sampled positions (94.7% of positions where the benign cone was detected), and transferred to another model combination at 85%.

**End-to-end impact.** The adversarial cone was imported into the LGSVL simulator driving Baidu Apollo v5.0 (whose perception models the paper identifies as the same as v5.5's): across 100 runs at 30 km/h the vehicle collided with the cone **100%** of the time, against 0% for the benign cone, and the logs show the cone evading both perception pipelines at every frame before fusion.

**Defences.** Evaluated DNN-level defences only dent it: of four input transformations, the best (median smoothing) reduces success to 66% without hurting benign detection; augmenting training data with adversarial inputs, to 69%; adversarial training with 2-step PGD, only to 95%. Adding further sources (more viewpoints, RADAR) is discussed as raising attack difficulty, not evaluated — with the caveat that RADAR perception is also DNN-based.

## Where it fits

The direct sequel to the same group's [Adversarial Sensor Attack on LiDAR-based Perception](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md) (Cao et al., CCS 2019) in this KB. There, sensor fusion appears in the limits as a defence "discussed, not evaluated"; this paper evaluates fusion as actually deployed and withdraws it as a generic answer to single-modality attacks — one shaped physical object perturbs both modalities simultaneously because shape is the property both sensors read. In the KB's sensor-attack line it sits one layer above [Petit et al. 2015](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) and [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md), which manufacture echoes and points at the transducer, and above Cao 2019, which fools one modality's perception pipeline: this one attacks the fusion layer's founding assumption. Two scope markers matter for reading it alongside [Wang et al. 2023](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md): every measured system here uses rule-based late fusion, and the 100% collision figure is a single-stack simulator result — the question of how component-level successes translate into system-level effects in general is exactly what Wang et al. take up.

## Limits and safety notes

- **White-box.** Full knowledge of the victim's MSF algorithm is assumed, as in most prior work; obtainability by purchasing/renting a vehicle and reverse-engineering it is argued (with a Tesla Autopilot precedent cited), not demonstrated against a commercial stack.
- **No end-to-end physical-world AV test** — the authors cite cost and safety, and note industry also leans on simulation. The full-scale vehicle experiment covers the LiDAR side only (the team lost access to the vehicle mid-project); both-sensor physical evidence is miniature-scale; the collision rate is LGSVL simulation.
- **DNN-based fusion is not evaluated.** Both open-source stacks use rule-based fusion; the authors state the method applies to DNN fusion, but no number in the paper measures it.
- **Defence results are against the non-adaptive attack.** The paper itself notes input-transformation defences are known to fall to adaptive attacks in the literature, so 66% is not a floor for a defended system either.
- The crash-severity scenarios (an object filled with granite or metal; nails or glass debris behind a cone) are the authors' threat framing, not experiments.

## Status and sources

Status: **published** — a finished 2021 conference publication; no living artefact beyond the authors' released code and data. Bibliographic record: *2021 IEEE Symposium on Security and Privacy (SP)*, pp. 176–194. DOI [10.1109/SP40001.2021.00076](https://doi.org/10.1109/SP40001.2021.00076) verified against Crossref (title, venue, and page range match the paper), 2026-11-01. Full text read end-to-end, appendices included, from the arXiv author version (arXiv:2106.09249v1, 17 June 2021), 2026-11-01.

## Related

- [Adversarial Sensor Attack on LiDAR-based Perception in Autonomous Driving](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md) — Cao et al. 2019; the single-modality predecessor whose unevaluated fusion defence this paper tests
- [Remote Attacks on Automated Vehicles Sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) — Petit et al. 2015, the raw-echo foundation
- [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md) — Shin et al. 2017, the point-cloud step
- [Does Physical Adversarial Example Really Matter to Autonomous Driving?](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md) — Wang et al. 2023, the system-level reality check on this attack class
- [A First Physical-World Trajectory Prediction Attack via LiDAR-induced Deceptions](a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving.md) — Lou et al. 2024, the pipeline-propagation step downstream of perception
- [SoK: The Next Frontier in AV Security](sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion.md) — the systematization of this line (still a stub)
