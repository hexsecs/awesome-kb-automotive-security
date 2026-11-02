---
uid: 01a19d3c-af22-7479-a85f-776ad63e6ace
title: "A First Physical-World Trajectory Prediction Attack via LiDAR-induced Deceptions in Autonomous Driving"
summary: "Lou et al., USENIX Security 2024. Attacks trajectory prediction indirectly, by placing physical objects that deceive LiDAR perception, instead of…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity24/presentation/lou"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Lou et al., USENIX Security 2024. Attacks trajectory prediction indirectly, by placing physical objects that deceive LiDAR perception, instead of manipulating an attacker vehicle's own history as prior work required."
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity24/presentation/lou"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving
  - invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving
  - does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
  - illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications
---

Lou et al., USENIX Security 2024. Attacks trajectory prediction indirectly, by placing physical objects that deceive LiDAR perception, instead of manipulating an attacker vehicle's own history as prior work required.

## What it is

Yang Lou and Jianping Wang (City University of Hong Kong), Yi Zhu and Chunming Qiao (SUNY Buffalo), Qun Song (Delft University of Technology), Rui Tan (Nanyang Technological University), and Wei-Bin Lee (Hon Hai Research Institute; Feng Chia University). *33rd USENIX Security Symposium (USENIX Security '24)*, pp. 6291–6308. The first attack on the *trajectory prediction* module of an autonomous driving system launched from the physical world. Prediction — forecasting where nearby road users will be over the next seconds, from their tracked histories — sits between perception and planning, and planning trusts it. Prior prediction attacks worked digitally and directly — an attacker vehicle drives a crafted trajectory so the victim's predictor forecasts it wrongly — requiring precise execution of a precomputed path, tuned to an assumed victim speed. This paper instead attacks *indirectly*: the adversarial vehicle stays parked, and ordinary objects (cardboards) placed around it corrupt the victim's LiDAR perception of it — shifting its detected bounding box's coordinates and, above all, its heading — so the predictor, fed a subtly wrong current state, forecasts a moving trajectory for a stationary car that intersects the victim's own planned path. The victim then brakes, accelerates, or changes lane to avoid a collision that was never going to happen.

## What it showed

**Two findings make the attack tractable.** (F1) *Prediction models are disproportionately vulnerable at the current frame.* Perturbing each of the five historical input states in turn (PGD, on both Trajectron++ and AgentFormer) shows the current state has by far the largest effect on the predicted trajectory — recurrent models weight the newest state most, and others re-centre their coordinate frame on it. So the attacker need only corrupt perception at one moment: when the victim passes a fixed *attack point*. (F2) *The bounding-box perturbations that placed objects can induce are few and patterned.* Sampling 500 candidate object locations per scene and recording the resulting box deviations, the coordinate deviations fall mostly within ±1 m and the heading deviations cluster (notably near 0 and near ±π, i.e. heading flips). The achievable perturbation set can therefore be probed cheaply and described as a small set of clusters, instead of searching the physical world blindly.

**The inverse attack.** Stage one (prediction-side attack) searches, by PGD under expectation-over-transformation over victim velocities, for a current-state perturbation — constrained to lie inside the probed perturbation clusters — that minimizes the distance between the adversarial vehicle's predicted trajectory and the victim's planned trajectory, i.e., manufactures an intersection. Stage two (location matching) matches the wanted perturbations to placements that actually produce them (Hungarian algorithm), then refines by local probing. The design is "inverse": it starts from the prediction effect wanted and works back to the physical placement, rather than forward-sampling locations.

**Dataset results.** On 100 nuScenes scenes matching the scenario (ego approaching a roadside-parked car; PIXOR detection, CenterPoint tracking, Trajectron++ prediction, MPC planning), the attack at 2,000 queries reaches a **63% collision rate** — the share of scenes where the predicted trajectory intersects the victim's planned trajectory; at equal query budgets it consistently beats brute-force sampling, and its 400-query result exceeds brute force at 2,000 queries (a fivefold overhead reduction). Victim responses split into sudden brakes, sudden accelerations, and lane changes — hazardous in over 50% of trajectories at a 100-query budget. It degrades gracefully under object displacement up to the detector's 0.1 m grid scale and across object sizes of 0.2–0.4 m, and transfers black-box from Trajectron++ to an AgentFormer victim at up to 31% collision rate.

**Physical-world results.** On the team's custom testbed car (Robosense Helios-32 LiDAR, RTK-GNSS/INS; same model pipeline as the dataset experiments), two A3-size cardboards were placed at computed locations beside a parked car (the paper names it: a black Tesla Model 3, the team's own test vehicle — not a claim about any production system). Planned from data collected at 5 km/h, the attack succeeded (planning-response error > 1 m) in 5/5 trials at 5 km/h and 4/5 at 10 km/h with the parked car on the victim's left, and 4/5 and 5/5 respectively on the right; successful trials end in emergency braking by the victim. Random placement succeeded in 0/5 trials on either side; brute-force sampling in 3/5. The locations tolerate ±30° orientation shifts (5/5) and 0.1 m coordinate shifts (3/5), and survive 1 m lateral shifts of the victim's driving line at reduced rates (2–3/5).

**Defences.** The attack's signature — physically impossible heading volatility between frames — motivates the paper's proposed heading-centric detector, which checks observed heading changes against a kinematic bicycle model's maximum and replaces offending states: it flags 44.5% of attacked scenes and cuts the collision rate from 40% to 25%. Generic defences fare worse: a spatial-temporal consistency checker (PercepGuard) detects 4 of 400 attacked scenes, because nothing appears or disappears — boxes merely shift; adversarial fine-tuning of the predictor cuts collision rate only from 40% to 35% (and slightly degrades clean accuracy); MC-dropout does better, 40% to 18%, at significant inference cost.

## Where it fits

The downstream step in this KB's sensor/perception line. [Petit et al. 2015](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) and [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md) stop at the sensor; [Cao et al. 2019](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md) showed injected points can be shaped until a perception pipeline believes them; [Cao et al. 2021](invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving.md) attacked the fusion assumption. Lou et al. move the target one module further down the pipeline and change the attacker's problem accordingly: the perception errors they need are not disappearance or fabrication but small, *plausible* state errors — a heading flip in a tracked box — and the quantity optimized is a planning-relevant outcome, not a detector metric. It is also, in the terms of [Wang et al. 2023](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md), an attack designed from the start against system behaviour (trajectory intersection, planning response) rather than a component score — with physical-world trials on a real testbed, at 5–10 km/h in a single scenario.

## Limits and safety notes

- **One scenario.** A victim passing a roadside-parked vehicle, in dataset scenes and in testbed trials at 5–10 km/h. Moving adversarial vehicles, intersections, and dense traffic are named as future work; the attack's effect also decays once the victim passes the attack point — a braking victim resumes normal behaviour afterwards.
- **White-box design, partial transfer.** Location planning assumes full knowledge of the victim's detection, tracking, and prediction models; the black-box evidence is a single transfer pair (Trajectron++ → AgentFormer) at roughly half the white-box collision rate.
- **"Collision rate" is a prediction-space metric in the dataset experiments** — predicted trajectories intersecting planned ones, with hazardous planning responses as the harm — not physical collisions; the physical trials measure planning-response error on the team's own research stack, not a production AV.
- **Placement precision matters.** Effectiveness holds within roughly one detector grid cell (0.1 m) of the computed locations and degrades beyond it; the objects are conspicuous cardboards on tripods in the trials; stealth is asserted by substitutability (billboards, similar roadside objects), not tested.

## Status and sources

Status: **published** — a finished 2024 conference publication. Bibliographic record: *Proceedings of the 33rd USENIX Security Symposium*, pp. 6291–6308. **DOI: none** — USENIX does not assign DOIs to its proceedings papers and none appears on the paper. Full text read end-to-end, appendices included, from the USENIX open-access proceedings PDF, 2026-11-01.

## Related

- [Adversarial Sensor Attack on LiDAR-based Perception in Autonomous Driving](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md) — Cao et al. 2019; the perception-layer attack whose errors this paper learns to aim downstream
- [Invisible for both Camera and LiDAR](invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving.md) — Cao et al. 2021; object-based deception at the fusion layer
- [Does Physical Adversarial Example Really Matter to Autonomous Driving?](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md) — Wang et al. 2023; the system-level measurement frame this attack is designed inside
- [Remote Attacks on Automated Vehicles Sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) — Petit et al. 2015, the raw-echo foundation
- [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md) — Shin et al. 2017, the point-cloud step
