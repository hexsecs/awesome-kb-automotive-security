---
title: "On the Realism of LiDAR Spoofing Attacks against Autonomous Driving Vehicle at High Speed and Long Distance"
summary: "Sato et al., NDSS 2025. Moving-vehicle spoofing rig and an adaptive high-frequency removal attack that succeed at 60 km/h and 110 m against production…"
type: entity
category: "Research Papers"
url: "https://www.ndss-symposium.org/ndss-paper/on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance/"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Sato et al., NDSS 2025. Moving-vehicle spoofing rig and an adaptive high-frequency removal attack that succeed at 60 km/h and 110 m against production driving stacks, closing the gap between bench demonstrations and moving-vehicle conditions."
sources:
  - url: "https://www.ndss-symposium.org/ndss-paper/on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance/"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.14722/ndss.2025.230628"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications
  - adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
  - dirty-road-can-attack-security-of-deep-learning-based-automated-lane-centering-under-physical-world-attack
  - physical-channel-sensor-attacks
---

Sato et al., NDSS 2025. Moving-vehicle spoofing rig and an adaptive high-frequency removal attack that succeed at 60 km/h and 110 m against production driving stacks, closing the gap between bench demonstrations and moving-vehicle conditions.

## What it is

Takami Sato, Ryo Suzuki, and Yuki Hayakawa (co-first authors), Kazuma Ikeda, Ozora Sako, Rokuto Nagata, and Ryo Yoshida (Keio University), Qi Alfred Chen (University of California, Irvine), and Kentaro Yoshioka (Keio). *Network and Distributed System Security Symposium (NDSS) 2025*, San Diego. The paper is the LiDAR-spoofing literature's realism audit, and it grades its predecessors harshly: its survey table scores every physically demonstrated prior attack and finds all of them stationary or low-speed, short-range, and none against a vehicle actually operated by an autonomous-driving stack — Petit et al. stationary at 1 m, Shin et al. stationary at 5 m, the moving-target attempts topping out at 5 km/h and 10 m. The authors' question is whether LiDAR spoofing can have end-to-end safety impact in practical conditions: a victim driving at highway-approach speeds, attacked from the roadside at long distance. Their answer is a system, the Moving Vehicle Spoofing (MVS) system, plus a new removal attack, A-HFR, designed for current-generation LiDARs. The threat model is the roadside "spoofer placed in environment" model the authors call the most practical and most challenging: straight flat road, target LiDAR height known, attack opening at ≥110 m.

## What it showed

**The MVS system removes the three bottlenecks the paper identifies in prior work.** (1) *Detection and tracking:* instead of a normal camera — the prior vision-based approach detects a target LiDAR at 5 m and fails entirely at 10 m, because the sensor is too small in frame — an infrared camera behind a 905 nm bandpass filter watches for the victim LiDAR's own laser emission, IRST-style. It is LiDAR-agnostic (no per-model training), achieves ≥90% detection at 5–20 m across three LiDAR models and works at 110 m; with YOLOv5 detection over 3-frame inputs plus Kalman tracking it holds ≈95–100%. (2) *Auto-aiming:* a high-precision servo (0.088° resolution; a 1° error is ≈1.7 m at 100 m) tracks the moving target. (3) *Spoofing:* two arrayed lasers behind 2-inch lenses give roughly 100× the beam area of prior rigs, and a parabolic-mirror antenna lets the receiver catch the victim's sparse pulses at long range. The system is built from off-the-shelf parts for about US$2.3k, plus general lab equipment.

**Verdicts on the earlier attacks' assumptions.** Synchronized injection attacks — the class of Shin et al. and Cao et al. — depend on a deterministic scan pattern and are directly foiled by the timing randomization now common in new-generation LiDARs. The high-frequency removal (HFR) attack (the same group's NDSS 2024 work) survives randomization, but **pulse fingerprinting** — pulse-pair interval authentication, deployed for anti-interference rather than security — cut it to 2.1% success in prior work and at most ~20% here, because pushing pulse frequency higher overheats the laser diode and collapses peak power, which must exceed the legitimate laser's.

**A-HFR restores the attack against fingerprinting LiDARs.** The trick is gray-box "weak synchronization": a photodiode senses when the target LiDAR is scanning the sector containing the object to be hidden, and the spoofer fires at high frequency only then, resting the diode the remaining ≈97% of the scan. That buys more than 25× the HFR pulse frequency on the same laser, and because randomly fired high-frequency pulses eventually land inside the fingerprint's tolerance window, authentication is bypassed stochastically. A-HFR removed 100% of points for the Hesai AT128 (at 15 MHz) and 96% for the Hesai XT32 (at 24 MHz) within a 20° × 16° window, sustainable for over 100 seconds; the Livox Mid-360's fingerprinting proved too lenient to need it, falling to plain HFR.

**Driving and end-to-end results.** On a private road, against a car driving at up to 60 km/h with the attack running from up to 110 m away: HFR hid a roadside pedestrian with ≥96% attack success down to the 20 m braking distance at 60 km/h; A-HFR was 100% successful out to 40 m, dropping to about 50% at 20 m when the optical receiver occasionally missed a scan; synchronized injection placed ≥1,000 points — a ghost wall — at about 20 m at 60 km/h. Finally, against a PIXKIT vehicle running the Autoware.ai stack (VLP-32c) — the first spoofing demonstration against a vehicle actually operated by an AD stack — the removal attack made the vehicle crash into an inflatable mock car it had stopped 7 m short of in the benign run, and the injection attack made it stop permanently in front of a wall that did not exist.

## Where it fits

This is the paper that closes the open limitation stated on every earlier page of this KB's LiDAR line. Petit et al. were "laboratory only," with outdoor attacks on moving vehicles as future work; Illusion and Dazzle treated aiming at a moving vehicle as an engineering problem, not a demonstration; Cao et al. named dynamic aiming at a moving AV's LiDAR their open problem and real-world testing as future work. The MVS system is precisely that missing engineering — detect, track, aim — and its survey table is the line's own scorecard of what had actually been shown. It also rearranges the line's conclusions: against current sensors, the surviving attack is not Cao et al.'s perception-optimized injection but crude high-frequency removal, which behaves like jamming; and the strongest deployed defence, pulse fingerprinting, is an anti-interference feature pressed into security service, effective but bypassable by an attacker willing to fire fast enough at the right moments. The authors' countermeasure discussion asks manufacturers to strengthen randomization and fingerprinting deliberately as security features, and AD developers to add availability checking (the HFR pattern is, they note, entropy-detectable) and fail-safe behaviour such as slowing down under sensing uncertainty.

## Limits and safety notes

- **The AD-stack end-to-end runs were slow.** Facility limits capped the Autoware vehicle at 5 km/h (removal) and 15 km/h (injection), at night; the 60 km/h results are against a human-driven car carrying a roof LiDAR, not a stack-driven vehicle — a gap the paper states itself.
- **Geometry is favourable by assumption:** roadside attacker, straight flat road, known and constant LiDAR height, horizontal-only aiming. Vertical tracking on uneven roads is discussed, not built.
- **A-HFR degrades at close range** (about 50% at 20 m against the AT128) when the receiver misses the victim's pulses; the proposed fix, speculative execution from prior scan timing, is future work.
- **Fingerprinting results are per-model:** the Mid-360's authentication is weak, the XT32 demands 24 MHz, and the AT128's tolerance was taken from documentation rather than measured — the verdicts do not transfer automatically to other new-generation LiDARs.
- Experiments ran on a private road under exclusive-use permission with a licensed driver and laser eye protection; the authors conducted responsible disclosure to popular Level-3/Level-4 AD companies before publication, noting production robotaxis may carry undisclosed countermeasures.

## Status and sources

Status: **published** — a finished 2025 conference publication; no living artefact. DOI [10.14722/ndss.2025.230628](https://doi.org/10.14722/ndss.2025.230628), verified against Crossref (title, all nine authors, NDSS 2025, San Diego all match). Full text read end-to-end, appendices included, from the authors' UC Irvine copy of the NDSS version, 2026-11-01. The paper extends the group's VehicleSec 2024 work-in-progress papers; a journal extension by the same team exists but is not the version read for this page.

## Related

- [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md) — Shin et al. 2017: the point-cloud spoofing whose moving-target gap this paper closes
- [Adversarial Sensor Attack on LiDAR-based Perception in Autonomous Driving](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md) — Cao et al. 2019: the perception-layer attack whose stated open problem (aiming at a moving AV) this paper solves
- [Remote Attacks on Automated Vehicles Sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) — Petit et al. 2015: the founding relay/spoofing work, stationary at 1 m in this paper's scorecard
- [Dirty Road Can Attack](dirty-road-can-attack-security-of-deep-learning-based-automated-lane-centering-under-physical-world-attack.md) — Sato and Chen's camera-side counterpart
