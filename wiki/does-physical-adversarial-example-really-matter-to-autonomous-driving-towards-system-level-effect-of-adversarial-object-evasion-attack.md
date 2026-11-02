---
title: "Does Physical Adversarial Example Really Matter to Autonomous Driving? Towards System-Level Effect of Adversarial Object Evasion Attack"
summary: "Wang et al., ICCV 2023. Measures published physical adversarial attacks against a full driving pipeline rather than the perception model alone, and finds…"
type: entity
category: "Research Papers"
url: "https://arxiv.org/abs/2308.11894"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Wang et al., ICCV 2023. Measures published physical adversarial attacks against a full driving pipeline rather than the perception model alone, and finds that component-level success rarely translates into system-level effects such as traffic rule violations."
sources:
  - url: "https://arxiv.org/abs/2308.11894"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1109/ICCV51070.2023.00407"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving
  - adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving
  - a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving
  - dirty-road-can-attack-security-of-deep-learning-based-automated-lane-centering-under-physical-world-attack
  - sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion
  - robust-physical-world-attacks-on-deep-learning-visual-classification
---

Wang et al., ICCV 2023. Measures published physical adversarial attacks against a full driving pipeline rather than the perception model alone, and finds that component-level success rarely translates into system-level effects such as traffic rule violations.

## What it is

Ningfei Wang, Yunpeng Luo, Takami Sato, and Qi Alfred Chen (University of California, Irvine) with Kaidi Xu (Drexel University). *IEEE/CVF International Conference on Computer Vision (ICCV 2023)*, pp. 4389–4400. A measurement study, not a new attack on a model: it asks whether the physical adversarial object-evasion literature — attacks that report success as a per-frame misdetection rate against a lone object detector — actually achieves the effects that motivate it (collisions, traffic-rule violations) once the detector sits inside a complete driving system. To make the question measurable the paper defines a *system model* for AD adversarial attacks with three parts: the AD system model (the full pipeline enclosing the targeted component — object tracking, planning, control — under closed-loop control), the vehicle plant model (braking distances, accelerations, sensor placement, the distance at which the stop line leaves the camera's view), and the operation scenario model (road geometry, speed limit, traffic rules, and the system-level goal). Its target is the STOP sign-evasion attack, chosen as the most extensively studied and most directly safety-relevant of the evasion attacks.

## What it showed

**The measurement.** The representative prior attacks are the strongest published design per detector: RP² (Eykholt et al. 2018) against YOLO v2, SIB (Zhao et al., CCS 2019) against YOLO v3 and Faster R-CNN, and FTE (Jia et al., NDSS 2022) against YOLO v3 and YOLO v5. Because none of the attack authors could provide source code, the team reproduced RP² and FTE themselves (their RP² scores 61.0% against the original's ~63.5% under the original setup) and used SIB's author-shared sign images. Perception behaviour was measured in the physical world — printed full-size signs, drive-by video from 45 m down to 4 m along a real driving path, ≥400 frames per 5 m bin — and then injected into a closed-loop SVL simulator run: per-range detection rates stochastically drop the sign's detections at the perception output of a pipeline consisting of a Kalman-filter multi-object tracker, Baidu Apollo's lane-following planner, and OpenPilot's PID longitudinal and Stanley lateral controllers. Speeds 25, 30, and 35 mph; 10 runs per cell.

**The headline result is a zero.** At the component level the attacks work as advertised — overall attack success rates of 71.2% (RP²), 53.3% and 41.0% (FTE), 5.2% (SIB on Faster R-CNN — a reproduction the authors flag as possibly weakened). At the system level, **not one representative attack causes a single STOP sign violation at any speed in any cell where the benign sign is handled correctly**. The mechanism is visible in the physical measurements: the attacks are weakest exactly where it matters. Braking distance at 30 mph is ~15 m, and inside that envelope the sign is still detected and, crucially, *tracked* — e.g., SIB against YOLO v3 still detects the sign in 90.4% of frames at 15–20 m — so the tracker never loses the sign before the vehicle must brake. A detector that is fooled at 35 m and honest at 15 m has, systemically, not been fooled at all.

**Why: two design limitations.** (1) *Physical model-inconsistent size distribution.* Prior attacks use expectation-over-transformation with object pixel sizes sampled uniformly; but from the camera pinhole model, the time a uniformly moving vehicle spends at each apparent size follows a density proportional to 1/s² (derived in the paper, and confirmed in simulator histograms) — uniform sampling spends the attack's budget on sizes the vehicle rarely sees and under-trains the sizes that dominate an approach. (2) *No plant or system model.* Only one distance band is system-critical: nearer than the minimum braking distance d_min, detection no longer matters (the vehicle cannot stop in time anyway); farther than d_max, the sign is not yet reliably detected or tracked. Attacks optimized indiscriminately over all sizes waste strength outside that band and are too weak inside it.

**SysAdv: the fix, and what it buys.** The paper's constructive half integrates the system model into existing attacks. S1 samples object sizes from the derived 1/s²-consistent distribution instead of uniformly. S2 restricts optimization to the system-critical range, converting d_min (plant model) and d_max (detector range, conservative tracker-deletion behaviour) into pixel sizes via camera-based rendering over nuScenes. Applied on top of RP² and FTE, system-level violation rates rise from 0% to **100% in several cells** (RP²–YOLO v2 at 25 mph; FTE–YOLO v3 at 30 mph; FTE–YOLO v5 at 35 mph) — an average increase of around 70% on average (the paper's phrasing; the gain is uneven — see Limits), with overall component success up ~33% and success within the system-critical range up ~122%. The improvement is general: across varied tracker and braking parameters the SysAdv versions average ~98% violation against ~18% for the originals, and on a second object type — the adversarial T-shirt pedestrian-evasion attack — the average simulated pedestrian collision rate rises from ~47% to ~82%.

## Where it fits

This is the reality check the KB's perception-attack line has to be read against. The component-level results documented on pages like [Cao et al. 2019](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md) (perception fooled, decisions shown in a simulator replay) and [Cao et al. 2021](invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving.md) (100% collision in one stack's simulation) are measurements of a model or a pipeline segment; Wang et al. show that for the camera patch-attack literature the step from "the detector misses it" to "the car breaks the rule" is not automatic — tracking, braking geometry, and the distance profile of the misses decide it. But the paper is a measurement of *attack designs*, not a safety proof, and its second half cuts the other way: once an attack is designed against the system model rather than the detector alone, the same physical vectors do produce system-level violations at high rates. The accurate one-line summary is that the pre-2023 evasion literature evaluated the wrong quantity — not that physical adversarial objects don't matter. Its targets are also specific: camera patch attacks on STOP signs and pedestrians, in one representative open pipeline; LiDAR and fusion attacks are cited as fellow component-level work but are not among the measured systems.

## Limits and safety notes

- **The system level is simulated, with perception injected.** Real-world physical measurement stops at per-range detection rates; those rates are then used to randomly drop detections in SVL. Effects depending on *which* frames drop (correlated misses, tracker behaviour on real sequences) are modelled statistically, not observed on a real vehicle.
- **Reproduction caveat.** No original attack code was available; RP² and FTE are the authors' reproductions and SIB is evaluated from author-shared sign images against a possibly different pre-trained Faster R-CNN — the paper flags the anomalously low SIB/FR component numbers itself. Measured attacks may be weaker than the originals.
- **One pipeline, sedan-scale assumptions.** Tracker, planner, and controllers are representative open components (Apollo planner, OpenPilot controllers), not a commercial AD stack; the paper names evaluation on commercial systems such as Tesla as future work. White-box attack knowledge is assumed throughout.
- **Even SysAdv is uneven.** Near-distance component success stays low in several configurations — the FTE–YOLO v5 attack at 25 mph reaches only a 10% violation rate, and only after an added total-variation loss — so "system-level effects are achievable" is a demonstrated possibility with strong speed- and detector-dependence, not a uniform property.

## Status and sources

Status: **published** — a finished 2023 conference publication. Bibliographic record: *2023 IEEE/CVF International Conference on Computer Vision (ICCV)*, pp. 4389–4400. DOI [10.1109/ICCV51070.2023.00407](https://doi.org/10.1109/ICCV51070.2023.00407) verified against Crossref (title, venue, and page range match the paper), 2026-11-01. Full text read end-to-end from the arXiv author version (arXiv:2308.11894v1, 23 August 2023), 2026-11-01. A short demo version of the study later appeared at VehicleSec 2024; this page covers the ICCV paper.

## Related

- [Invisible for both Camera and LiDAR](invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving.md) — Cao et al. 2021; cited by this paper as component-level work, and the strongest form of the claim it qualifies
- [Adversarial Sensor Attack on LiDAR-based Perception in Autonomous Driving](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md) — Cao et al. 2019, the perception-layer result whose decision-level evidence is of the kind measured here
- [A First Physical-World Trajectory Prediction Attack via LiDAR-induced Deceptions](a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving.md) — Lou et al. 2024; designs against a downstream module's system behaviour rather than a component metric
- [Dirty Road Can Attack](dirty-road-can-attack-security-of-deep-learning-based-automated-lane-centering-under-physical-world-attack.md) — a further physical-world attack in the measured class
- [SoK: The Next Frontier in AV Security](sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion.md) — the systematization of this line (still a stub)
