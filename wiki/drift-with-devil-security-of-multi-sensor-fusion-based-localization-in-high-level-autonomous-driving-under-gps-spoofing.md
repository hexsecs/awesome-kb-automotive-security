---
title: "Drift with Devil: Security of Multi-Sensor Fusion based Localization in High-Level Autonomous Driving under GPS Spoofing"
summary: "Shen et al., USENIX Security 2020. Shows sensor fusion does not neutralise GPS spoofing, taking an autonomous vehicle off its lane with gradual position drift."
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity20/presentation/shen"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Shen et al., USENIX Security 2020. Shows sensor fusion does not neutralise GPS spoofing, taking an autonomous vehicle off its lane with gradual position drift."
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity20/presentation/shen"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - all-your-gps-are-belong-to-us-towards-stealthy-manipulation-of-road-navigation-systems
  - sok-how-sensor-attacks-disrupt-autonomous-vehicles-an-end-to-end-analysis-challenges-and-missed-threats
  - sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion
  - a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving
  - physical-channel-sensor-attacks
---

Shen et al., USENIX Security 2020. Shows sensor fusion does not neutralise GPS spoofing, taking an autonomous vehicle off its lane with gradual position drift.

## What it is

Junjie Shen, Jun Yeon Won, Zeyuan Chen, and Qi Alfred Chen, University of California, Irvine. *29th USENIX Security Symposium* (USENIX Security '20), pp. 931–948. The first security study of multi-sensor fusion (MSF) based localization in high-level autonomous driving under GPS spoofing. In a high-level AD stack, localization fixes the vehicle's global position on the map at centimetre level; perception detects obstacles but is not designed to identify road deviation, so a localization error by itself can put a vehicle off the road or into oncoming traffic while every other module works perfectly. The target is Baidu Apollo's MSF (BA-MSF), chosen for representativeness the authors argue on both axes: its design — a linear Kalman filter fusing GPS at 1 Hz, a LiDAR locator at 5 Hz, and IMU, with a chi-squared test as outlier detector — is the dominant pattern in the recent robotics literature (14 of 18 surveyed MSF papers are KF-based), and its implementation is production-grade, fleet-validated at 0.054 m accuracy and deployed in Apollo's robotaxi service. The attack scenario is a tailgating attack vehicle that spoofs the victim's GPS while tracking the victim's true position in real time; because the AD controller constantly steers back to lane centre, a deviation δ in the MSF output becomes a physical deviation of δ in the opposite direction. Two attack goals are defined from lane geometry: off-road (0.895 m lateral deviation on local roads, 1.945 m on highways) and wrong-way (2.405 m / 2.855 m).

## What it showed

**The reassuring baseline.** An exhaustive search for the maximum achievable deviation over 10-second attack windows finds MSF mostly works: the majority (71%) of even these upper-bound results in the real-world trace cause less than 50 cm of deviation, and 76% of windows cannot reach even the 0.895 m off-road threshold — the first spoofed point moves the output at most ~0.06 m before larger jumps fail the chi-squared test, and five LiDAR locator updates between GPS points keep correcting it. In a synthetic noise-free trace, no window exceeds 0.076 m. Sensor fusion, against an attacker who simply pushes, genuinely helps.

**The take-over effect.** In the real-world trace, however, 14% of windows reach over 2 m, and every one of them shows *exponential* deviation growth (fitted base ≥ 1.3). The mechanism inverts the defence: as spoofed updates accumulate in a window where the filter is already unsure of itself, the Kalman state migrates toward the spoofed positions until the *truthful* LiDAR locator measurements become the statistical outliers — the chi-squared test rejects them, and the spoofed GPS becomes the only update source, free to walk the output arbitrarily far. A cause analysis over four candidate factors finds two statistically significant drivers: the initial KF state uncertainty and the LiDAR locator's reported measurement uncertainty. Take-over opportunities are therefore **unconfident periods created by ordinary sensor noise and locator inaccuracy** — dynamic, non-deterministic, and absent from the noise-free trace. The vulnerability is not in the fusion equations but in the confidence dynamics around them, and it exists precisely because real sensors are noisy in the way MSF was designed to tolerate.

**FusionRipper.** Because the attacker cannot observe or schedule an unconfident period, the attack is two-stage and opportunistic. Stage 1 spoofs at a constant offset d and watches the victim's physical deviation; crossing 0.295 m (the lane-line touch distance, far above BA-MSF's normal 0.054 m error) signals a vulnerable period. Stage 2 then spoofs exponentially, d × f^i, riding the take-over growth. On six real-world traces (Apollo's ba-local plus five KAIST Complex Urban traces, selected and configured to be worst-case — the most confident traces, and an ideal ground-truth LiDAR locator where no HD map was available), some parameter pair achieves **at least 97% off-road and 91.3% wrong-way success in every trace** given a two-minute attack window (averages 98.6% and 95.9%), with mean success time under 35 seconds; success stays above 91.3% even when the required deviation is raised to 10 m. Neither stage alone exceeds 14% / 7% on ba-local, and naive random spoofing manages 3.7% / 0.2% — the staging, not the spoofing, is the contribution. The attack also succeeds (100%) against two other KF-based MSF implementations, though those are far less accurate systems (1.17–1.91 m natural error) that even random spoofing mostly defeats; BA-MSF is the meaningful target.

**Practicality checks.** Modelled spoofing inaccuracies barely dent it: at the realistic error level, success drops 0.2–0.8 points; at three times that error, the rates are still 84.3% / 74.2%. With Apollo's control loop in the loop, trace-based end-to-end success is 97.0% / 93.9%, and in LGSVL simulation with the full Apollo 5.0 stack the victim is driven into a road barrier and a stop sign. Because the best (d, f) pair is trace-sensitive, the authors add an **offline profiling** method: trial attacks against same-model AVs, stopped at a safe 0.45 m deviation, which finds parameters good for 84.2% / 80.7% success at a cost of ~42 short trips — under half a day.

## Where it fits

This is one of the very few papers inside the Zhang SoK's Finding 1 gap: of the 59 detection/localization attacks systematized there, only four were evaluated under sensor fusion — this one not only evaluates under fusion, it breaks the fusion, through the fusion's own consistency check. It is the concrete mechanism behind the SoK's Finding 8 (localization as shared dependency): here the dependency is total, because the stack assigns road-deviation detection to localization alone. In the SoK's categories it belongs to A21–A22 (GNSS spoofing), but its centre of gravity is downstream of the sensor — the transducer is fooled trivially, since civilian GPS is unauthenticated; the result is about estimator dynamics. It inverts the direction of Lou et al. 2024 and of the SoK's N3 vector: those reach prediction *through* a localization error; here the localization error is itself the terminal effect, converted into physical deviation by the lane-centring controller. Its direct predecessor is Zeng et al. 2018, which it cites for the single-source case — Zeng's victim had GPS and a human checker, no fusion at all. The defence space the paper engages is therefore mostly the fusion itself; beyond it, the authors discuss GPS spoofing detection and prevention (signal-power monitoring, angle-of-arrival, crowdsourced cross-validation, signal authentication) as limited or circumventable, improving MSF-state and LiDAR-locator confidence as the root-cause fix requiring sensing breakthroughs, and — as the practical short-term direction — camera-based lane detection as an independent fail-safe cross-check, which production stacks of the time did not use for that purpose; even perfect detection, they note, only converts the attack into denial of the localization function.

## Limits and safety notes

The evaluation is trace-based: spoofed inputs are applied to recorded real-world sensor traces replayed through the genuine BA-MSF binary, not transmitted at a live AV — the authors cite cost and the illegality of GPS spoofing, and note that GPS spoofing itself is already proven practical on cars and other systems. The end-to-end claims rest on the stated control assumption (output deviation equals opposite physical deviation), validated in trace-based Apollo runs and in LGSVL simulation, not on a physical vehicle being driven off a road. The attacker is strong: an AV-grade tailgater that tracks the victim's position to centimetres in real time — argued to be realistic for a rival-fleet attacker, but not physically demonstrated. Scope is KF-based MSF with chi-squared-style rejection; whether particle-filter designs or other outlier detectors resist is explicitly left open, and other OEM stacks (Waymo, GM) are untested — the generality claim is at design level. The KAIST numbers assume an ideal LiDAR locator, which makes the attack harder, so those results are conservative for the attacker; conversely, the headline success rates are for the best parameter pair per trace, and the offline-profiling rates (mid-80s / low-80s) are the more honest field estimate.

## Status and sources

Status: **published** — *Proceedings of the 29th USENIX Security Symposium*, August 2020, pp. 931–948. **DOI: none** — USENIX does not assign DOIs to its proceedings papers, and a Crossref bibliographic query (2026-11-01) returned no record for this paper; no aggregator identifier is substituted. Full text read end-to-end from the USENIX proceedings PDF, 2026-11-01. An extended version with the derivations is arXiv:2006.10318. Attack demos: sites.google.com/view/cav-sec/fusionripper.

## Related

- [All Your GPS Are Belong To Us](all-your-gps-are-belong-to-us-towards-stealthy-manipulation-of-road-navigation-systems.md) — Zeng et al. 2018; the single-source predecessor this paper cites
- [SoK: How Sensor Attacks Disrupt Autonomous Vehicles](sok-how-sensor-attacks-disrupt-autonomous-vehicles-an-end-to-end-analysis-challenges-and-missed-threats.md) — GNSS spoofing is its A21–A22; this paper is a Finding-1 exception and Finding 8's mechanism
- [SoK: The Next Frontier in AV Security](sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion.md)
- [A First Physical-World Trajectory Prediction Attack](a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving.md) — the inverse direction: prediction reached through localization error
