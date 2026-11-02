---
title: "Physical-channel sensor attacks"
summary: "Attacks that manufacture the measurement itself — in acoustics, optics, RF, and heat — where no digital interface is touched and the output is faithfully wrong."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [walnut-waging-doubt-on-the-integrity-of-mems-accelerometers-with-acoustic-injection-attacks, illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications, remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar, on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance, drift-with-devil-security-of-multi-sensor-fusion-based-localization-in-high-level-autonomous-driving-under-gps-spoofing, all-your-gps-are-belong-to-us-towards-stealthy-manipulation-of-road-navigation-systems, the-heat-is-on-understanding-and-mitigating-vulnerabilities-of-thermal-image-perception-in-autonomous-systems]
sources:
  - url: "https://doi.org/10.1109/EuroSP.2017.42"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1007/978-3-319-66787-4_22"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.14722/ndss.2026.230330"
    retrieved: 2026-11-01
---

Every other attack class in this KB forges a *message*: a frame, a packet, a credential. This class forges a **measurement**. The attacker acts on the physical channel the sensor transduces — sound pressure, light, radio, heat — and the sensor faithfully converts the manufactured stimulus into a wrong reading. No digital interface is touched, nothing is malformed, and no cryptographic defence applies, because the compromise sits *below* the first bit, in the analogue conditioning chain that turns physics into numbers. Two papers from different modalities established the class in this corpus, and the papers campaign has since filled it in across nearly every automotive sensing modality.

## Mode 1: false-measurement injection

The attacker synthesises a stimulus the sensor reads as a genuine phenomenon. **[WALNUT](../walnut-waging-doubt-on-the-integrity-of-mems-accelerometers-with-acoustic-injection-attacks.md)** (EuroS&P 2017) is the canonical case: acoustic energy at a MEMS accelerometer's resonant frequency passes through the sensor's own conditioning flaws (amplifier saturation, low-pass aliasing) and emerges as a *forged acceleration output* — biased at best, attacker-controlled at worst — from a device that was never digitally addressed. **[Illusion and Dazzle](../illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md)** did the LiDAR version: a relayed/spoofed return, shaped through the receiver's own optics and predictable ping waveform, plants phantom obstacles. The modality census since: LiDAR spoofing measured at highway speed and 110 m ([On the Realism of LiDAR Spoofing](../on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance.md)); GNSS, where [Drift with Devil](../drift-with-devil-security-of-multi-sensor-fusion-based-localization-in-high-level-autonomous-driving-under-gps-spoofing.md) profiles a constant offset then escalates past the fusion filter's rejection threshold, and [All Your GPS](../all-your-gps-are-belong-to-us-towards-stealthy-manipulation-of-road-navigation-systems.md) matches route shape so the ghost location survives every plausibility check a navigation app applies; and thermal imaging, where [The Heat Is On](../the-heat-is-on-understanding-and-mitigating-vulnerabilities-of-thermal-image-perception-in-autonomous-systems.md) adds the class's first **stateful, delayed** injection — a heat source folded into the camera's per-pixel calibration offsets, growing *after the source leaves*.

## Mode 2: channel saturation and blinding

The second mode manufactures nothing; it drowns the genuine signal. [Petit et al. 2015](../remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) — the founding experimental leg, camera blinding and LiDAR relay/blinding against production sensor hardware — established the pattern, and Illusion and Dazzle's dazzle half is the same mode against the LiDAR receiver. The Heat Is On's equalization attack belongs here *by effect*: a scene-peak degeneracy collapses the thermal image's dynamic range until pedestrians fall below detection — suppression achieved through the image-formation stage rather than by raw saturation, which extends the conditioning chain this class exploits from transducer-plus-electronics to transducer-plus-electronics-plus-**image formation**.

## Where the defence can sit

The corpus's defences are physical or signal-level, never cryptographic — filtering, damping, sampling strategy, waveform randomisation (the LiDAR answers), attack-aware equalization and calibration (the thermal answers; the ghost mitigation exploits a raw-intensity gap between genuine and ghost sources). The GPS papers force a widening of that claim into an axis: a defence can sit in the **conditioning chain** (before the measurement), in the **estimator** (fusion logic that cross-checks measurements), or in the **human operator** (the navigation study's two detectors caught the spoof by noticing landmarks and street names — the cross-check the paper itself names as most promising). GNSS is the axis's hard endpoint: the civilian signal is unauthenticated *by design*, there is no conditioning fix, and Drift with Devil's deeper result is an estimator-level defence — chi-squared outlier rejection — **becoming** the attack mechanism in unconfident periods, when truthful LiDAR readings are the ones rejected. A defence layer is itself a trust decision, and this class's papers keep finding the layer that was trusted most.

## Boundaries

Excluded, and cross-linked: **TPMS and other digital wireless sensor protocols** forge messages over a radio protocol — the channel is digital, the defence is authentication, and they belong with the message classes on the [RKE](key-fob-relay-attacks.md) side. **PKES relay** forwards a genuine signal rather than manufacturing a measurement. Camera adversarial *patterns* (the RP²/Dirty Road family) are a neighbouring class — they exploit the learned model, not the conditioning chain — and await their own concept decision. What defines membership here is the locus: physics in, numbers out, and the flaw in between.

This page synthesizes the KB's own full entity pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source. Its filing scope cited the GPS and thermal modalities at stub depth; both reached full depth during the papers campaign, and the page is written to that depth.

## Related

- [WALNUT](../walnut-waging-doubt-on-the-integrity-of-mems-accelerometers-with-acoustic-injection-attacks.md) — acoustic injection through conditioning flaws, the canonical case
- [Illusion and Dazzle](../illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md) — both modes against one LiDAR
- [Remote Attacks on Automated Vehicles Sensors (Petit 2015)](../remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) — the founding experiments
- [The Heat Is On](../the-heat-is-on-understanding-and-mitigating-vulnerabilities-of-thermal-image-perception-in-autonomous-systems.md) — the image-formation stage, stateful injection, natural triggering
- [Drift with Devil](../drift-with-devil-security-of-multi-sensor-fusion-based-localization-in-high-level-autonomous-driving-under-gps-spoofing.md) — the estimator defence turned attack mechanism
