---
title: "Dirty Road Can Attack: Security of Deep Learning based Automated Lane Centering under Physical-World Attack"
summary: "Sato et al., USENIX Security 2021. Physical dirty-road patches that steer a production lane-centering system out of its lane."
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity21/presentation/sato"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Sato et al., USENIX Security 2021. Physical dirty-road patches that steer a production lane-centering system out of its lane."
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity21/presentation/sato"
    retrieved: 2026-11-01
  - url: "https://arxiv.org/abs/2009.06701"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - too-good-to-be-safe-tricking-lane-detection-in-autonomous-driving-with-crafted-perturbations
  - adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
  - invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving
  - does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack
  - on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance
---

Sato et al., USENIX Security 2021. Physical dirty-road patches that steer a production lane-centering system out of its lane.

## What it is

Takami Sato and Junjie Shen (co-first authors) and Ningfei Wang (University of California, Irvine), Yunhan Jia (ByteDance), Xue Lin (Northeastern University), and Qi Alfred Chen (UC Irvine). *30th USENIX Security Symposium*, August 2021, pp. 3309–3326. The paper is the first systematic security study of deep-learning-based Automated Lane Centering (ALC) in its designed operational domain — roads that have lane lines. An ALC system runs camera frames through a DNN lane-detection (LD) model, fits lane curves, computes steering by lateral control (PID/MPC), and actuates under a strict rate limit. The evaluation target is comma.ai's **OpenPilot** (LD model v0.7.0), chosen as the only open-source production ALC and reported to perform close to Tesla Autopilot and GM Super Cruise. The attack goal is quantitative and safety-critical: force a lateral deviation out of the lane — 0.735 m on highways, 0.285 m on local roads — in under **2.5 seconds**, the average driver reaction time, so that even the fully attentive supervising driver an ALC assumes cannot take over in time.

## What it showed

**The vector: a dirty road patch (DRP).** The perturbation is printed on an adhesive road patch of the kind legitimately used to seal cracks, and patterned to look like ordinary dirt or white stains. Stealth is engineered as constraints: perturbations are grayscale only (Y-channel increases), dimmer than the original lane lines, the original lane lines are redrawn unchanged on the patch, and only a fraction of the patch area may be perturbed.

**Two domain-specific techniques make it work.** (1) *Motion-model-based input generation.* A single fooled frame cannot move the car — actuation is limited to 0.25° per 10 ms step, worth at most 0.3 mm of lateral deviation at 45 mph — so the attack must bend detection over a sequence of frames, and each steered frame changes the next frame's view. The authors synthesize those attack-influenced frames with a kinematic bicycle model plus perspective transformation, instead of re-driving the road or building a simulator scene per optimization iteration. (2) A *lane-bending objective function*: the lateral-control step is not differentiable, so the optimizer instead maximizes the derivative of the desired driving path — a differentiable surrogate equivalent, at the design level, to changing the steering decisions.

**Effectiveness.** On 80 scenarios built from comma2k19 driving traces (40 clips, attack left and right), DRP succeeds in **≥97.5%** of scenarios at every stealthiness level (100% at the two less-stealthy levels), with average success time **≤0.903 s** against the 2.5 s budget. The design choices are load-bearing: at a 12 m patch length, a single-frame EoT baseline scores 0% and a drawing-lane-line baseline 2.5%, against DRP's 66.25%. The attack holds ≥95% success under an average 1 m run-time position shift, reaches ≥90% against three OpenPilot LD model versions of different architecture (≈63% average transfer), and still achieves 93.8% in a multi-piece mode of eight patch pieces deployable in 5–10 seconds each by two people. A 100-participant user study found the patches stealthy from the driver's seat: fewer than 25% would take over even at the least stealthy setting, and at the two stealthier settings the patch read as innocent as a clean patch 2.5 s before success.

**Physical realizability and safety impact.** Because patching a public road for the test was not an option, realizability was validated at 1:12 miniature scale — printed road and patch, the real OpenPilot EON dashcam: designed steering angle 23.4° left vs 24.5° observed (4.7% difference), holding 20–24° across 12 lighting conditions (15–1210 lux) and 45 viewing angles. In LGSVL software-in-the-loop simulation the attack caused **100% collisions** (100/100 runs per scenario) with a highway barrier and an oncoming truck. On a real 2019 Toyota Camry running OpenPilot, with the attack trace injected at the LD model's output, the vehicle hit dummy obstacles in **10/10 trials**: lane-departure warning never fired (it shares the fooled LD module), forward-collision warning fired in only 5/10 trials and 0.46 s before impact on average, and automatic emergency braking never fired at all.

## Where it fits

This paper and [Too Good to Be Safe](too-good-to-be-safe-tricking-lane-detection-in-autonomous-driving-with-crafted-perturbations.md), in the same proceedings, are the KB's two lane-perception attacks, and they are mirror images: Jing et al. *create* a fake lane where none exists, black-box, on a closed production car; Sato et al. *bend* the detection of real lanes, white-box, on the open production stack. The only prior production-ALC attack the paper acknowledges, Tencent Keen Lab's white-sticker work, targeted road regions *without* lane lines and generated its perturbations unsystematically; this paper's baseline comparison shows that style of perturbation is nearly ineffective (2.5%) exactly where lane lines exist. In the sensor-attack line, this is the camera channel attacked at the learned-model layer rather than the optical layer: unlike Petit et al.'s blinding, the dirty patch is physically present and correctly sensed — the failure is in what the model makes of it. The five standard input-transformation defences evaluated (JPEG compression, bit-depth reduction, Gaussian noise, median blur, autoencoder reformation) all fail the trade-off test: configured to keep benign driving at 100%, they leave attack success at 99–100%; sensor/HD-map fusion defences are discussed but, as the paper notes, production Level-2 systems generally have neither.

## Limits and safety notes

- **One system, white-box.** All evaluation is on OpenPilot; whether Tesla Autopilot or GM Super Cruise fall the same way is untested, and the threat model assumes full knowledge of the target ALC (obtainable, the authors argue, because the system is purchasable and in this case open-source).
- **No physical patch ever steered a real car.** Realizability rests on the miniature-scale experiment; the real-vehicle collisions used attack traces injected at the LD output, not a deployed patch — a gap the paper attributes to safety limits and lack of access to private test facilities (OpenPilot's 28 mph minimum engagement speed among them).
- **Defences are evaluated only at the model-input level** (the five transformations above, all inadequate); the fusion and HD-map defences the paper prefers are argued, not measured.

## Status and sources

Status: **published** — a finished 2021 conference publication; no living artefact. **No DOI exists** for this paper: a Crossref bibliographic query (2026-11-01) returns records only for the authors' separate companion demo papers (IEEE SPW 2021; AutoSec 2021), and USENIX assigns no DOIs to its proceedings. Full text read end-to-end from the authors' UC Irvine copy of the proceedings version, 2026-11-01; an extended version exists as arXiv:2009.06701.

## Related

- [Too Good to Be Safe](too-good-to-be-safe-tricking-lane-detection-in-autonomous-driving-with-crafted-perturbations.md) — the mirror-image lane attack: fake lane creation, black-box, on a production Tesla
- [Adversarial Sensor Attack on LiDAR-based Perception in Autonomous Driving](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md) — the LiDAR-side perception-layer attack; both insist on system-level evaluation
- [Remote Attacks on Automated Vehicles Sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) — the camera channel attacked at the optical layer instead
- [Invisible for both Camera and LiDAR](invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving.md) — the same group's multi-sensor-fusion perception attack
- [Does Physical Adversarial Example Really Matter to Autonomous Driving?](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md) — Wang et al. 2023; the system-level measurement frame for this attack class
- [On the Realism of LiDAR Spoofing Attacks](on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance.md) — Sato and Chen's LiDAR-side counterpart
