---
title: "Too Good to Be Safe: Tricking Lane Detection in Autonomous Driving with Crafted Perturbations"
summary: "Jing et al., USENIX Security 2021. First lane-detection attack validated on a real production vehicle, exploiting the module's over-sensitivity with small…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity21/presentation/jing"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Jing et al., USENIX Security 2021. First lane-detection attack validated on a real production vehicle, exploiting the module's over-sensitivity with small road markings."
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity21/presentation/jing"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - dirty-road-can-attack-security-of-deep-learning-based-automated-lane-centering-under-physical-world-attack
  - adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
---

Jing et al., USENIX Security 2021. First lane-detection attack validated on a real production vehicle, exploiting the module's over-sensitivity with small road markings.

## What it is

Pengfei Jing, Qiyi Tang, Yuefeng Du, Lei Xue, Xiapu Luo, Ting Wang, Sen Nie, and Shi Wu — The Hong Kong Polytechnic University, Keen Security Lab (Tencent), and Pennsylvania State University. *30th USENIX Security Symposium*, August 2021, pp. 3237–3254. The paper is the first investigation of the lane detection module in a real vehicle. Its target is the Tesla Model S 75 named in the paper (Autopilot hardware 2.5, software 2018.6.1), and its central claim inverts the usual adversarial-ML story: the lane detection algorithm is not too weak but **too sensitive** — built to catch faint genuine lane lines, it promotes small adversarial road markings into a valid lane, and the car follows it. The threat model is black-box: the attacker owns a vehicle of the same model but has no knowledge of the module's internals, and the markings must be perceivable by the module yet unobtrusive to the driver.

## What it showed

**Getting eyes inside the car.** The technical precondition is reverse engineering: through static analysis (IDA Pro) and dynamic instrumentation of Autopilot's closed-source `vision` binary, the authors located the lane detection module's input and output inside GPU memory — the input camera image (the main front camera's 1280×960, 16-bit image) copied in by `cudaMemcpy`, and the output lane image (a 640×416 float matrix) produced by the kernel `t_cuda_lane_detection::compute`. That oracle — feed a modified camera image, read the resulting lane image — is what makes automated black-box search possible.

**The two-stage attack.** Stage 1 works in the digital domain: perturbations are described by eight physically meaningful parameters (length, width, longitudinal and lateral distances, spacing, grayscale increment ΔG, rotation angle, count) and projected into the camera image through a calibrated pinhole model, so anything found digitally can be built physically. A score balancing fake-lane visibility against perturbation visibility is optimized with heuristic search — of five algorithms tried (BAS, PSO, BSO, ABC, simulated annealing), particle swarm optimization was best, finding a better perturbation in 87 lane computations than a naive shrink-the-marking search found in 1,262. Stage 2 prints the winner as road markings. The best perturbations share a shape: **narrow but long** — 1–5 cm wide, 59–133 cm long, grayscale increments of only 7–28 (of 255), placed roughly 10–15 m ahead. One exemplar is a single sticker 1 cm wide and 92 cm long that produces a clear fake lane. The method worked across five environments (clean, dark, dirty, underground garage), with rotation angle degrading the score and perturbation count mattering little.

**Physical end-to-end result.** With white stickers deployed on a real road, the fake lane registers most strongly at 5–12 m and in both bright and dark conditions. In the decisive experiment — a crossroads, where the genuine straight-ahead lanes disappear — the Model S in auto-steer followed the fake lane into the **oncoming traffic lane**, deviating **5.1 m** (more than 2.5 vehicle widths) at over 40 km/h, with no human input. The deviation took 0.918 s, inside the 1.20–1.35 s driver reaction time the paper cites for unexpected events.

## Where it fits

Together with [Dirty Road](dirty-road-can-attack-security-of-deep-learning-based-automated-lane-centering-under-physical-world-attack.md) in the same proceedings, this paper brackets the lane-perception attack surface: Jing et al. inject a lane where the road offers none, on a closed production system, black-box; Sato et al. bend real lane detection on roads with lane lines, on the open-source production stack, white-box. The paper positions itself against the phantom attacks of Nassi et al., which needed darkness and were easy to notice; these markings work in daylight and are designed to be overlooked. Within this KB's sensor line it sits one layer above [Petit et al.](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md): Petit's camera attacks blind or confuse the sensor itself, whereas here the camera sees the markings perfectly — the failure is the detector's eagerness, the same move [Cao et al.](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md) made on the LiDAR side when they showed raw spoofed points fail but perception-shaped ones succeed. The title is the thesis: a lane detector tuned to miss nothing is, by that fact, willing to believe almost anything.

## Limits and safety notes

- **Not invisible — unobtrusive.** The paper's own limitation: the markings must be detectable by the module, so a driver who knows the attack and watches the road may spot them; the attack banks on the reduced attention of auto-steer driving and on the sub-second deviation time.
- **One vehicle, one firmware.** The GPU-memory oracle is specific to the examined Model S and its 2018.6.1 software; the reverse engineering, not the idea, would have to be redone per target.
- **End-to-end misguidance is demonstrated where lanes vanish.** Digital experiments generate fake lanes against images with real lanes present, but the physical drive-into-oncoming-traffic result is the crossroads scenario; sustained overruling of clearly detected genuine lanes on a normal road is not the demonstrated case.
- **Defences are proposals.** Abnormal-lane feature checks, adversarial training, multi-sensor fusion, and driver warning/forced handover are suggested, none evaluated. Responsible disclosure (§7): Tesla confirmed the attack changes the car's behaviour in auto-steer, emphasized that drivers must pay full attention, and stated no plan to fix it.

## Status and sources

Status: **published** — a finished 2021 conference publication; no living artefact. **No DOI exists** for this paper: a Crossref bibliographic query (2026-11-01) returns no record for the title, and USENIX assigns no DOIs to its proceedings. Full text read end-to-end, appendices included, from the USENIX proceedings PDF, 2026-11-01.

## Related

- [Dirty Road Can Attack](dirty-road-can-attack-security-of-deep-learning-based-automated-lane-centering-under-physical-world-attack.md) — the companion lane attack in the same proceedings: bending real lanes, white-box, on OpenPilot
- [Adversarial Sensor Attack on LiDAR-based Perception in Autonomous Driving](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md) — the perception-layer analogue on the LiDAR channel
- [Remote Attacks on Automated Vehicles Sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) — the camera attacked at the optical layer (blinding), one layer below this paper's detector-level attack
