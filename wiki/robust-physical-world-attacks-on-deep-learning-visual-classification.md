---
uid: 01a19d3c-afce-76cf-91ab-f2f85c6d81da
title: "Robust Physical-World Attacks on Deep Learning Visual Classification"
summary: "Eykholt et al., CVPR 2018. The stop-sign sticker attack, the canonical physical adversarial example against road sign recognition."
type: entity
category: "Research Papers"
url: "https://arxiv.org/abs/1707.08945"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Eykholt et al., CVPR 2018. The stop-sign sticker attack, the canonical physical adversarial example against road sign recognition."
sources:
  - url: "https://arxiv.org/abs/1707.08945"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1109/CVPR.2018.00175"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack
  - dirty-road-can-attack-security-of-deep-learning-based-automated-lane-centering-under-physical-world-attack
  - too-good-to-be-safe-tricking-lane-detection-in-autonomous-driving-with-crafted-perturbations
  - invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving
  - sok-how-sensor-attacks-disrupt-autonomous-vehicles-an-end-to-end-analysis-challenges-and-missed-threats
  - sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion
---

Eykholt et al., CVPR 2018. The stop-sign sticker attack, the canonical physical adversarial example against road sign recognition.

## What it is

Kevin Eykholt and Ivan Evtimov (equal contribution) with Earlence Fernandes, Bo Li, Amir Rahmati, Chaowei Xiao, Atul Prakash, Tadayoshi Kohno, and Dawn Song — University of Michigan, University of Washington, UC Berkeley, and Samsung Research America / Stony Brook University. *IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2018)*, pp. 1625–1634. The paper that moved adversarial examples off the screen and onto a real object: it introduces **Robust Physical Perturbations (RP²)**, an algorithm for generating adversarial perturbations that survive the physical world — varying distance and angle, changing resolution, printing error — and demonstrates it on road sign classification, chosen because signs are visually simple (perturbations are hard to hide), live in an unconstrained environment, matter for transport safety, and fit a threat model in which the attacker cannot touch the vehicle but can modify objects the vehicle depends on. The attacker is white-box (justified by model-extraction attacks and by the need to assess a strong adversary when designing defences) and the attacks are *targeted*: the sign must be read as a chosen wrong class, not merely misread. The final perturbation is not a repainted sign but a set of black-and-white stickers shaped to resemble graffiti — vandalism humans expect and ignore, hiding the attack, in the paper's phrase, "in the human psyche."

## What it showed

**The algorithm.** A digital perturbation optimized on one image dies in the world for four reasons the paper names: environmental variability (above all distance and angle), spatial constraints (the attacker can modify the object, never its background), physical limits on imperceptibility (a perturbation too small for the camera to resolve is no attack), and fabrication error (printers cannot reproduce arbitrary colours). RP² answers each in the optimization. It minimizes a Lagrangian objective — perturbation norm plus a Non-Printability Score term penalizing unprintable colours — over the *expectation* of the classifier's loss across a distribution of images sampled from both real experimental photographs (varied distances, angles, lighting) and synthetic transformations (cropping, brightness, spatial transforms), a combination the paper stresses against concurrent work that used synthetic transformations alone. A mask confines the perturbation to the object's surface and gives it its graffiti shape; its placement is optimized in two passes — an L1-regularized run over the whole sign concentrates perturbation on the classifier's weak regions, and an L2 run then works inside a mask positioned there.

**The evaluation method is a contribution in its own right.** Finding no standardized methodology, the paper proposes two stages borrowed from the physical sciences: *lab tests* — stationary photographs across a grid of distances (5–40 ft) and angles (0–60°) — and *field tests* — drive-by video from a smartphone camera on a car approaching from ~250 ft at 0–20 mph, scored on every tenth frame, with a success counted only where the clean sign at the same distance/angle was classified correctly. Two standard-architecture classifiers are built for the purpose: LISA-CNN (91% on the LISA test set, 17 sign classes) and GTSRB-CNN (95.7% on the GTSRB test set, with US stop signs substituted for the German ones the team had no physical copies of).

**The results.** Against LISA-CNN, an object-constrained *poster* attack — the whole sign surface reprinted, perturbations confined to the sign where earlier printed-image attacks perturbed the background too — reads a Stop sign as Speed Limit 45 in 100% of stationary images (mean target confidence 80.51%) and 100% of drive-by frames. The *sticker* attacks on a real sign: camouflage abstract-art stickers reach 100% targeted success stationary and 84.8% of drive-by frames; the subtler LOVE–HATE graffiti stickers reach 66.67% stationary. A small perturbation confined to a Right Turn sign's arrow reaches 73.33% targeted — and the misses are still misclassifications, into other warning signs. Against GTSRB-CNN, the same camouflage-art design reads Stop as Speed Limit 80 in 80% of stationary conditions and 87.5% of drive-by frames. For generality, single stickers against Inception-v3 read a microwave as "phone" in 90% of conditions and a coffee mug as "cash machine" in 71.4% targeted (100% untargeted). The paper's conclusion is deliberately general: physical sources of noise are not a defence, and future defences cannot rely on them.

## Where it fits

This is the founding physical adversarial-example paper for the driving domain, and most of the KB's later perception-attack pages are downstream of it: the patch/sticker lineage runs through [Dirty Road](dirty-road-can-attack-security-of-deep-learning-based-automated-lane-centering-under-physical-world-attack.md) and [Too Good to Be Safe](too-good-to-be-safe-tricking-lane-detection-in-autonomous-driving-with-crafted-perturbations.md) to the fusion attacks, and the [Zhang sensor SoK](sok-how-sensor-attacks-disrupt-autonomous-vehicles-an-end-to-end-analysis-challenges-and-missed-threats.md) files sign attacks of this kind among its camera categories. Its second life in the KB is as a *measured object*. [Wang et al. 2023](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md) took RP² as one of its three representative attacks (reproducing it themselves, the original code being unavailable), measured a component-level success rate of 71.2% against YOLO v2 — the strongest of the three measured — and then found that inside a complete closed-loop driving pipeline it produced **zero system-level STOP-sign violations at any speed**: the attack is weakest at the close ranges where braking decisions are made, and the tracker holds the sign. That downstream verdict qualifies what this paper's numbers mean — a per-frame classifier result is not a vehicle behaviour — without diminishing what the paper itself demonstrated, which is exactly the component-level fact Wang et al. confirm: a few inconspicuous stickers reliably defeat a road-sign classifier across the distances and angles of a real approach. Wang et al.'s constructive half closes the loop in the other direction — redesigning attacks against the system model restores system-level effects — so the two pages are best read as a pair: the attack, and the measurement of what it does and does not buy.

## Limits and safety notes

- **Classifiers, not detectors, and not a driving system.** The paper attacks cropped-image classification with the crop done manually to match the clean images; detection in the wild is explicitly out of scope (a follow-on note extends RP² to YOLO). No vehicle was attacked — the field test is a camera on the authors' car scoring a classifier offline; as the authors put it on their webpage, they did not attack a real self-driving car.
- **Cropping matters.** Under a later pseudo-random crop (guaranteeing most of the sign is in frame), targeted success falls to averages of 70% (LISA-CNN) and 60% (GTSRB-CNN), though untargeted success stays at 90% and 100% — the sign is still not read as a stop sign.
- **White-box throughout.** Black-box physical attacks are named as an open question; transferability is argued from digital-domain precedent, not demonstrated here.
- **Ambient light was not controlled** (experiments span indoor to outdoor lighting, which the authors treat as a feature of the methodology), and the drive-by track was a straight approach; turning and curved-road geometries enter only through the stationary angle grid.
- The classifiers are the authors' own standard-architecture builds at 91% and 95.7% accuracy — representative of the era's crop-then-classify pipeline, not of any production traffic-sign-recognition stack.

## Status and sources

Status: **published** — a finished 2018 conference publication. Bibliographic record: *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2018)*, pp. 1625–1634. DOI [10.1109/CVPR.2018.00175](https://doi.org/10.1109/CVPR.2018.00175) verified against Crossref (title, all nine authors, venue, and page range match the paper), 2026-11-01. Full text read end-to-end from the arXiv author version (arXiv:1707.08945v5, 10 April 2018), which carries the CVPR 2018 appearance note. The arXiv version's own title is the earlier "…on Deep Learning Models"; the published title, used by this page and the list, is "…on Deep Learning Visual Classification."

## Related

- [Does Physical Adversarial Example Really Matter to Autonomous Driving?](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md) — Wang et al. 2023; measures this attack at component level (71.2%) and system level (zero violations), then shows how system-aware redesign restores the effect
- [Dirty Road Can Attack](dirty-road-can-attack-security-of-deep-learning-based-automated-lane-centering-under-physical-world-attack.md) — the physical-patch lineage applied to lane centering
- [Too Good to Be Safe](too-good-to-be-safe-tricking-lane-detection-in-autonomous-driving-with-crafted-perturbations.md) — crafted perturbations against lane detection on a production-grade stack
- [Invisible for Both Camera and LiDAR](invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving.md) — the adversarial-object line extended to multi-sensor fusion
- [SoK: How Sensor Attacks Disrupt Autonomous Vehicles](sok-how-sensor-attacks-disrupt-autonomous-vehicles-an-end-to-end-analysis-challenges-and-missed-threats.md) — the end-to-end systematization this attack sits inside
