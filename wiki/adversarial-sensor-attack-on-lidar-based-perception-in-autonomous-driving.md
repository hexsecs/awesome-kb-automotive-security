---
uid: 01a19d3c-af27-7fb5-92e3-31ec35edf907
title: "Adversarial Sensor Attack on LiDAR-based Perception in Autonomous Driving"
summary: "Cao et al., ACM CCS 2019. Spoofs LiDAR returns to inject a fake obstacle into the perception pipeline of a production autonomous driving stack."
type: entity
category: "Research Papers"
url: "https://arxiv.org/abs/1907.06826"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Cao et al., ACM CCS 2019. Spoofs LiDAR returns to inject a fake obstacle into the perception pipeline of a production autonomous driving stack."
sources:
  - url: "https://arxiv.org/abs/1907.06826"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
  - illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications
  - walnut-waging-doubt-on-the-integrity-of-mems-accelerometers-with-acoustic-injection-attacks
  - on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance
  - invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving
  - does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack
  - a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving
---

Cao et al., ACM CCS 2019. Spoofs LiDAR returns to inject a fake obstacle into the perception pipeline of a production autonomous driving stack.

## What it is

Yulong Cao, Chaowei Xiao, Benjamin Cyr, Yimeng Zhou, Won Park, Sara Rampazzi, Kevin Fu, and Z. Morley Mao (University of Michigan) with Qi Alfred Chen (UC Irvine). *Proceedings of the 26th ACM Conference on Computer and Communications Security (CCS '19)*, London, November 2019, pp. 2267–2281. The paper is the first security study of LiDAR-based *perception* in autonomous vehicles — the authors' claim, and the operative word is perception. Petit et al. (2015) had shown fake echoes entering a LiDAR; Shin et al. (2017), fake points in its point cloud. Neither asked whether the software that turns points into driving decisions would believe them. This paper targets that stage in Baidu Apollo, the open-source AV stack: Apollo's LiDAR pipeline pre-processes the point cloud (coordinate transform, HDMap region-of-interest filtering, feature generation into an 8-feature 512×512 bird's-eye matrix over 60 m), runs a CNN detector, then post-processes — clustering on the network's *objectness* output, filtering on *positiveness*, box construction, tracking — before prediction and planning consume the perceived obstacles. The threat model is LiDAR spoofing — injecting points by firing lasers at the victim's sensor, roadside or from an attack vehicle — with white-box model access assumed. The attack goal: a fake obstacle close in front of the victim AV (~5 m; evaluated at 2–8 m), the placement likeliest to force an immediate, wrong decision.

## What it showed

**First, a clean negative result: blind spoofing does not survive perception.** The authors reproduced Shin et al.'s spoofing attack against a Velodyne VLP-16 with an improved rig — a laser driver (PCO-7114) firing at the LiDAR's own 2.304 µs pulse rate instead of the earlier setup's 100 µs, plus a focusing lens. The improvement is substantial: fake points at all 16 vertical angles across an 8° horizontal span at over 10 m — around 100 points in total, ~60 of them (the central 8–10 vertical lines) stably spoofed at high intensity. They then threw everything the sensor-level literature offered at Apollo's perception: Shin's original traces, their own stronger traces, the traces rotated through 100 sampled angles, and 100 random patterns of 160 spoofed points at 4–6 m. **None produced a perceived obstacle — not one, in any configuration.** The spoofed budget is too sparse and too narrow (8°, against the wide, dense return of a real vehicle) for the detection model and its post-processing to promote to an obstacle.

**Adv-LiDAR closes the gap by attacking the model, within the measured physical budget.** The method has three parts. (1) *Capability modelling:* delay steps move a point along range (nanosecond steps), between vertical lines (2.304 µs steps), and within the 8° azimuth window (55.296 µs steps); the whole pattern can be repositioned by moving the spoofer. They model this as global spatial transformations (rotation, translation, height scaling) of a captured real spoof trace, at 20, 40, and 60 reliably spoofed points — 60 being the measured figure. (2) *An objective from the post-processing, not just the network:* the adversarial loss directly maximizes Apollo's objectness and positiveness outputs under a Gaussian mask at the target position — fooling the *pipeline*, thresholds included. (3) *Sampling plus optimization:* direct optimization (Adam) stalls on a loss surface noisy at small scale and flat at large scale, so the authors initialize from a grid of global samples and optimize locally.

**Results.** On 300 frames sampled from Apollo's released 30-second Sunnyvale trace (HDL-64E), the method raises the average success rate for a front-near obstacle from 18.9% (vanilla optimization) to 43.3% across the three capability levels, and to **around 75% at the measured 60-point capability**. Every successful fake obstacle was classified by Apollo as a *vehicle*, though no class was targeted. The attacks are robust in the two ways that matter physically: applied to the 15 following frames (~1.5 s of driving), success at 60 points stays above 75% on average; and the same transformation applied to five freshly captured spoof traces succeeds over 82% of the time at every level (90% at 60) — tolerating both victim motion and its own imprecision. One mechanism deserves note: a 20-point spoof was perceived as a 283-point obstacle, because genuine ground-reflection points are clustered into it when the 3D cloud is flattened into the 2D feature matrix.

**Driving decisions.** As a case study, adversarial traces were replayed through Apollo 3.0's simulator (Sim-control). *Emergency brake:* a spoofed obstacle ahead of a moving AV triggers a stop decision — 43 km/h to 0 within one second. *AV freezing:* an AV waiting at a red light is still stationary after the light turns green, held indefinitely by the fake obstacle. In both, Apollo's distance-gated escape behaviours (overtaking; deviating around a static obstacle, which needs 15 m by default) are defeated by the obstacle's nearness.

## Where it fits

This is the third step of the KB's LiDAR line, and it changes what a "successful attack" means. [Petit et al.](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) (2015) manufacture echoes (and, via the LUX 3's tracker, unstable object labels) but test below any driving stack. [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md) (Shin et al., 2017) manufacture points on a VLP-16, including points closer than the spoofer, and state in their own text that their claims stop at the point cloud. Cao et al. take Shin et al.'s spoofing hardware as a given input capability and move the question up the stack: not "can points be injected?" but "can injected points be made to mean *obstacle* to the machine-learning pipeline that decides?" The answer is conditional in a way neither predecessor could have shown: raw spoofing, no; spoofing shaped by white-box optimization against the detector and its post-processing, yes, three times out of four at the measured capability. [WALNUT](walnut-waging-doubt-on-the-integrity-of-mems-accelerometers-with-acoustic-injection-attacks.md) is the analogue on another channel, one layer down.

## Limits and safety notes

The paper's own discussion (§10.1) is direct about these, and the page keeps them at that strength:

- **Nothing here was demonstrated on a moving vehicle on a road.** Capability was measured indoors against a stationary VLP-16; the perception evaluation *synthesizes* spoofed points into recorded HDL-64E traces; the decision study is a simulator replay — and Sim-control has no physics engine, so the AV "behaves exactly as what it plans". Dynamically aiming at a moving AV's LiDAR with the required precision is the authors' named open problem; real-world testing is future work.
- **White-box access is assumed.** The optimization needs the model and the post-processing logic. The authors argue it is obtainable by reverse engineering the software — an argument, not a demonstration; black-box transferability is not evaluated.
- **One stack, one sensor family.** All perception results are against Apollo's CNN pipeline of that period; the capability model derives from one VLP-16 rig. The paper's generality claim — other LiDAR perception systems are likely vulnerable because spoofed clouds were never in their training distribution — is the authors' reasoning, not a cross-system measurement.
- **The modelled capability is a subset,** as the authors note — it may understate a better-equipped attacker; conversely the 60-point figure is specific to their driver, optics, and synchronization.
- **Defences are discussed, not evaluated:** ground-reflection filtering and reduced 3D→2D information loss (system level); sensor fusion, reduced receiving angle, firing-pattern and waveform randomization (sensor level); adversarial retraining (model level). None is implemented or measured.

## Status and sources

Status: **published** — a finished 2019 conference publication; no living artefact. Bibliographic record: *Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security (CCS '19)*, pp. 2267–2281. DOI [10.1145/3319535.3339815](https://doi.org/10.1145/3319535.3339815) verified against Crossref (title, venue, page range, and all nine authors match). Full text read end-to-end, appendices included, from the arXiv v2 author version (arXiv:1907.06826, revised 20 August 2019), 2026-11-01. Not the overlapping team's companion *Adversarial Objects Against LiDAR-Based Autonomous Driving Systems* (arXiv:1907.05418), a different attack (hiding real objects); this paper is the spoofing one.

## Related

- [Remote Attacks on Automated Vehicles Sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) — Petit et al. 2015, the raw-echo foundation
- [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md) — Shin et al. 2017, the point-cloud step this paper builds on
- [WALNUT](walnut-waging-doubt-on-the-integrity-of-mems-accelerometers-with-acoustic-injection-attacks.md) — the acoustic analogue
- [On the Realism of LiDAR Spoofing Attacks](on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance.md) — the later realism check on this line (still a stub)
