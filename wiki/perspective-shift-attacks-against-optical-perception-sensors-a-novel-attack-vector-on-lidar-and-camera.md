---
uid: 01a1a4a8-e0a8-71a6-a1f3-cd7e08aed2b5
title: "Perspective-Shift Attacks Against Optical Perception Sensors: A Novel Attack Vector on LiDAR and Camera"
summary: "Calipari et al., USENIX VehicleSec 2026. Introduces a new physical attack class that uses Direction Turning Film to shift LiDAR and camera fields of view…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/vehiclesec26/presentation/calipari"
status: published
last_checked: 2026-11-17
created: 2026-11-03
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 43fd1f2
list_summary: "Calipari et al., USENIX VehicleSec 2026. Introduces a new physical attack class that uses Direction Turning Film to shift LiDAR and camera fields of view, showing even a 20° shift significantly disrupts LiDAR odometry and camera lane detection in laboratory tests and on a real research vehicle, while barely affecting detection confidence."
related:
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
  - a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving
  - invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving
  - adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving
  - does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack
  - expanding-the-attack-scenarios-of-sae-j1939-a-comprehensive-analysis-of-established-and-novel-vulnerabilities-in-transport-protocol
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-03
  - url: "https://www.usenix.org/conference/vehiclesec26/presentation/calipari"
    retrieved: 2026-11-17
---

Calipari et al., USENIX VehicleSec 2026. Introduces a new physical attack class that uses Direction Turning Film to shift LiDAR and camera fields of view, showing even a 20° shift significantly disrupts LiDAR odometry and camera lane detection in laboratory tests and on a real research vehicle, while barely affecting detection confidence.

## What it is

A Best Paper at the 4th USENIX Symposium on Vehicle Security and Privacy (VehicleSec 26), Baltimore, August 2026, pp. 283–299, by Marco Calipari, Michael Kühr, Dominik Kulmer, Maximilian Luedecke, Mohammad Hamad and Sebastian Steinhorst of the Technical University of Munich. It introduces **Perspective Shift Attacks**, a class of physical attacks that target the sensors' field of view rather than the content the sensors see.

## How it works

The attack uses Direction Turning Film, an optical material that bends light by a predefined angle, to adversarially alter the field of view of a LiDAR or camera. The authors contrast this with prior work in two categories: injecting adversarial stimuli into the sensing range, and crafting adversarial objects to fool a machine-learning model. Their approach instead changes the *perceived sensing region* while leaving detection confidence largely intact — the sensing looks healthy even though it points somewhere else.

The paper presents a digital simulation framework and validates the attack in controlled laboratory experiments and in real-world deployments on an autonomous driving research vehicle. The reported result is that even a moderate **20° field-of-view shift** significantly affects LiDAR-based odometry and camera-based lane detection, potentially causing dangerous manoeuvres such as unintentionally invading the opposite lane. Object-detection confidence changes only slightly even though object positions are altered, which is what makes the attack stealthy. Proposed defences leverage physical-layer artifacts and semantic consistency checks.

## Where it fits

This is the sensor-perception counterpart to the other physical-attack papers in the corpus: [remote attacks on automated vehicles' sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md), [adversarial sensor attacks on LiDAR-based perception](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md), [a first physical world trajectory prediction attack via LiDAR-induced deceptions](a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving.md), and [invisible for both camera and LiDAR](invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving.md). [Does physical adversarial example really matter to autonomous driving?](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md) asks the system-level question that this paper answers from the field-of-view direction.

## Limits and safety notes

The description here comes from the official USENIX abstract, not the full paper: it gives the material, the 20° figure, the affected tasks and the defence categories, but not the film placement procedure, the exact experimental setup or the detection algorithms' internals. The results are from a research vehicle and simulations — the paper's claim is practicality, not a measurement of real-world crash rates. Applying optical film to a sensor on a public-road vehicle is unsafe and unlawful outside a controlled research programme. No sensor or vehicle was tested for this page.

## Status and sources

Checked 2026-11-17. **Published** — VehicleSec 26, August 2026, Best Paper, open access; paper, slides and video linked from the conference page.

- [USENIX VehicleSec 26 paper page](https://www.usenix.org/conference/vehiclesec26/presentation/calipari)

## Related

- [Remote attacks on automated vehicles' sensors: experiments on camera and LiDAR](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md)
- [A first physical world trajectory prediction attack via LiDAR-induced deceptions in autonomous driving](a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving.md)
- [Invisible for both camera and LiDAR: security of multi-sensor fusion based perception](invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving.md)
- [Adversarial sensor attack on LiDAR-based perception in autonomous driving](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md)
- [Does physical adversarial example really matter to autonomous driving?](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md)
- [Expanding the attack scenarios of SAE J1939](expanding-the-attack-scenarios-of-sae-j1939-a-comprehensive-analysis-of-established-and-novel-vulnerabilities-in-transport-protocol.md)
