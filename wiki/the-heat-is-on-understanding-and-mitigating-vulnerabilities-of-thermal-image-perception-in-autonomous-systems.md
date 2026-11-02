---
title: "The Heat is On: Understanding and Mitigating Vulnerabilities of Thermal Image Perception in Autonomous Systems"
summary: "Bhupathiraju et al., NDSS 2026. Shows heat sources degrade thermal-camera pedestrian detection and sensor fusion, including in real driving, and proposes…"
type: entity
category: "Research Papers"
url: "https://www.ndss-symposium.org/ndss-paper/the-heat-is-on-understanding-and-mitigating-vulnerabilities-of-thermal-image-perception-in-autonomous-systems/"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Bhupathiraju et al., NDSS 2026. Shows heat sources degrade thermal-camera pedestrian detection and sensor fusion, including in real driving, and proposes real-time defences."
sources:
  - url: "https://www.ndss-symposium.org/ndss-paper/the-heat-is-on-understanding-and-mitigating-vulnerabilities-of-thermal-image-perception-in-autonomous-systems/"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.14722/ndss.2026.230330"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
  - illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications
  - adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving
  - invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving
  - sok-how-sensor-attacks-disrupt-autonomous-vehicles-an-end-to-end-analysis-challenges-and-missed-threats
  - sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion
---

Bhupathiraju et al., NDSS 2026. Shows heat sources degrade thermal-camera pedestrian detection and sensor fusion, including in real driving, and proposes real-time defences.

## What it is

Sri Hrushikesh Varma Bhupathiraju and Sara Rampazzi (University of Florida), Shaoyuan Xie and Qi Alfred Chen (UC Irvine), Michael Clifford (Toyota InfoTech Labs), and Takeshi Sugawara (University of Electro-Communications). *Network and Distributed System Security Symposium (NDSS 2026)*. The first security study of the thermal camera's own image-formation pipeline in driving use. Thermal (long-wave infrared, 8–14 µm, bolometer-array) cameras are being added to autonomous stacks because they see living beings in darkness, fog, and rain where RGB cameras fail — but a thermal pipeline must continuously *manufacture* its image: non-uniformity correction (NUC) calibration against thermal drift, histogram equalization to stretch a narrow dynamic range into contrast, and special-material lenses (germanium / zinc selenide; glass is opaque at these wavelengths) behind a circular aperture. Each stage, the paper shows, is an attack surface, exploitable *before* any input reaches a detection model, by heat radiation invisible to human eyes. The adversary is remote and black-box — no access to camera hardware, firmware, or models; processing knowledge comes from public manuals, and the weapon is a single ~USD 20 ceramic heat lamp (up to 240 °C) placed roadside, at an intersection, or on a lead vehicle. Three cameras are studied throughout: FLIR Boson, InfiRay T2S, and FPV XK-C130.

## What it showed

**1. Equalization linearity — genuine obstacles fade.** Plateau equalization (the automotive standard, per the paper, in FLIR and BAE cameras) clips the image histogram at a plateau limit and redistributes; but when the scene's peak histogram frequency sits *below* the limit — 19% of FLIR ADAS, 35% of ASL, and 61% of LTIR scenes at a limit of 2500 — no clipping happens and the mapping degenerates to linear, losing contrast. A hot source in frame stretches that mapping further. On the T2S, a pedestrian's relative pixel intensity drops by up to 91% as source temperature rises to 240 °C at 3 m, and is still reduced by 50% with the source 20 m away. Synthesized onto FLIR ADAS, pedestrian mAP@50 collapses below 0.1 for all three fine-tuned detectors (baselines 0.35 YOLOv5, 0.30 YOLOv8, 0.73 Faster R-CNN) at a 150 °C source — a ~50% mean drop as the paper summarizes it — and the flaw is not plateau-specific: CLAHE and BBHE give pedestrian misdetection of 66–81% and 72–87%. Fusion does not rescue it: at 240 °C fusion pedestrian mAP falls by 0.80 (fused Faster R-CNN) and 0.31 (DAMSDet).

**2. Calibration poisoning — obstacles that appear after the attacker leaves.** Shutter-less NUC recalibrates every few minutes, folding the current scene into a per-pixel offset (a weighted moving average; the T2S fits weight ≈0.2) subtracted from every subsequent frame until the next cycle. A structured heat source present during calibration — a human-shaped foil pattern over the lamp, held through a 60–120 s stop — is baked into that offset; when the source leaves the field of view, the over-correction remains, and a pedestrian-shaped artifact *grows* in the empty scene, reaching full strength tens of seconds to ~3 minutes later depending on the camera. Timing is forgiving (exposure 10 s off the calibration event: 18% intensity drop vs ~21% at exact alignment; the paper's worked example gives ≈83% spoofing probability at a typical intersection). On FLIR the artifacts are detected as pedestrians at up to 93.9% success overall and 100% on Faster R-CNN; against fusion the maximum is 69.7% (fused Faster R-CNN) and 56.4% (DAMSDet) — fusion halves the effect but does not remove it.

**3. Lens ghosts — structure-preserving flares.** Unlike RGB flare ghosts (polygonal, aperture-shaped), thermal lenses and circular apertures *preserve the heat source's structure*: an inverted copy appears opposite the optical centre — the paper gives the coordinates in closed form — so a pedestrian-shaped source produces a pedestrian-shaped ghost at an attacker-chosen position. Ghosts at 80 °C already reach ≥90% detection success across all three detectors; against fusion they reach 98.0% (DAMSDet) and 91.1% (fused Faster R-CNN).

**Real driving.** Outdoors, on a UGV at up to 10 km/h and a car at 40 km/h: equalization gives 100% pedestrian misdetection on T2S and Boson images across all models (the XK-C130, with proprietary equalization, is more resistant: 43–78% at 40 km/h); calibration artifacts reach ≥91.8% (T2S), ≥83.6% (XK-C130), and ≥55.1% (Boson) over a 500 m drive at 40 km/h; ghosts were validated statically and at a 2.5 km/h approach (76% on Faster R-CNN, lower on the YOLOs). **Defences** are the paper's second half — three threat-aware signal-processing algorithms, all pre-model: attack-aware equalization (exclude the histogram spikes a heat source creates) cuts the mAP drop from 50% to 4% and restores detection to 96–100% (benign-source images stay near-identical, SSIM 0.96); attack-aware calibration (a per-pixel counter halting offset updates after sustained one-directional increase) suppresses calibration artifacts at 100% outdoors without suppressing a genuine pedestrian; ghost mitigation (suppress the geometrically opposite pixels of implausibly hot regions — ghosts need ≈9500 raw intensity, a human reads 7000–7500) likewise reaches 100%.

## Where it fits

The thermal leg of the KB's physical-channel sensor line — and its extension *upstream*: prior thermal work attacked detection models with adversarial clothing, patches, and bulbs worn by the attacker; prior pipeline work attacked other modalities. This paper's claim is that for thermal cameras the exploitable layer is neither the model nor the transducer element but the conditioning chain the modality cannot operate without — equalization, calibration, lensing — and RGB-thermal fusion, the field's default answer to single-sensor attack, inherits the failure because the corrupted channel is the one fusion leans on in the dark. In the [Zhang sensor SoK's](sok-how-sensor-attacks-disrupt-autonomous-vehicles-an-end-to-end-analysis-challenges-and-missed-threats.md) terms, it is a worked instance of that SoK's least-tested cell: an attack evaluated *under* fusion (two fusion models, not just three detectors). Against [Petit et al. 2015](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md), it adds a third modality whose channel is invisible and whose calibration artifact is *time-shifted* — the only attack in this KB's sensor corpus whose effect begins after the stimulus ends.

## Limits and safety notes

- **The large-scale numbers are synthesized, and the paper says so.** Sections V–VI overlay characterized real heat-source traces onto FLIR ADAS images; the *outdoor* results are genuinely measured, but on the authors' UGV and car, with detection models run on captured images — no production stack and no closed-loop obstacle-avoidance behaviour was attacked or observed.
- **Close range, small source.** Characterization and outdoor work use a 10 cm lamp at 0.5–5 m. Larger emitters extending the range, and the one capability extrapolation (a 30 cm source ghosts at 4.5 m), are argued, not measured. Ghosts need the source held 1–2 m away and aligned (dynamic test: 2.5 km/h, for safety).
- **Generality is uneven across cameras.** The XK-C130's proprietary equalization resists the headline attack substantially; plateau's dominance is asserted from vendor adoption and a market-share figure, and CLAHE/BBHE results come from the same synthesis.
- **The defences are evaluated in the authors' own setups**, at 100% suppression on their scenarios; the paper itself notes that distinguishing malicious artifacts from natural ones (sun glare, exhausts — which can trigger these vulnerabilities with no attacker at all) is hard, and that lens hoods cost field of view.
- **Safety framing:** the lamp's diffusive emission falls to ~30 °C at 50 cm, per the paper; pedestrian scenarios were performed by the authors in controlled environments, and findings were responsibly disclosed to the tested devices' vendors (responses awaited at writing).

## Status and sources

Status: **published** — a finished 2026 conference publication. Bibliographic record: *Proceedings of the 2026 Network and Distributed System Security Symposium (NDSS 2026)*, San Diego, CA, paper s330 (no page ranges). DOI [10.14722/ndss.2026.230330](https://doi.org/10.14722/ndss.2026.230330) verified against Crossref (title, all six authors, venue, and event match; the DOI is also printed in the paper's footer and resolves to the proceedings PDF), 2026-11-01. Full text read end-to-end from the NDSS proceedings PDF, including appendices and the artifact appendix.

## Related

- [Remote Attacks on Automated Vehicles Sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) — Petit et al. 2015, the founding experiments this paper extends to a third modality
- [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md) — the closest conditioning-chain parallel, on LiDAR
- [Adversarial Sensor Attack on LiDAR-Based Perception](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md) — Cao et al. 2019, the LiDAR false-obstacle line
- [Invisible for Both Camera and LiDAR](invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving.md) — fusion attacked from the object side; this paper attacks it from the processing side
- [SoK: How Sensor Attacks Disrupt Autonomous Vehicles](sok-how-sensor-attacks-disrupt-autonomous-vehicles-an-end-to-end-analysis-challenges-and-missed-threats.md) — the systematization whose fusion gap this paper fills for thermal
