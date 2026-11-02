---
title: "GIDS: GAN based Intrusion Detection System for In-Vehicle Network"
summary: "Seo, Song, and Kim, PST 2018. Trains a GAN on normal CAN traffic only, and is a common deep-learning IDS baseline alongside the authors' Car-Hacking dataset."
type: entity
category: "Research Papers"
url: "https://arxiv.org/abs/1907.07377"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Seo, Song, and Kim, PST 2018. Trains a GAN on normal CAN traffic only, and is a common deep-learning IDS baseline alongside the authors' Car-Hacking dataset."
sources:
  - url: "https://arxiv.org/abs/1907.07377"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1109/PST.2018.8514157"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - fingerprinting-electronic-control-units-for-vehicle-intrusion-detection
  - viden-attacker-identification-on-in-vehicle-networks
  - evading-voltage-based-intrusion-detection-on-automotive-can
  - on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems
  - a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset
  - in-vehicle-intrusion-detection
---

Seo, Song, and Kim, PST 2018. Trains a GAN on normal CAN traffic only, and is a common deep-learning IDS baseline alongside the authors' Car-Hacking dataset.

## What it is

Eunbi Seo, Hyun Min Song, and Huy Kang Kim, Graduate School of Information Security, Korea University, Seoul. *16th Annual Conference on Privacy, Security and Trust (PST 2018)*, Belfast, 28–30 August 2018, IEEE, pp. 1–6. GIDS is an intrusion detection system for the in-vehicle CAN bus built on a Generative Adversarial Network (GAN). Its goal: detect attacks never seen in training by learning what normal CAN traffic looks like, from normal data only. To feed traffic to the network, GIDS discards everything except the CAN IDs: each hexadecimal digit of an ID is one-hot-encoded as a 16-bit vector, so a 3-digit ID becomes a 16×3 matrix, and a window of consecutive IDs — the tuned input size is **64** — becomes one "CAN image". (IITP/MSIT-funded.)

## What it showed

**Architecture — the generator exists only to train the second discriminator.** GIDS runs two discriminators in series at detection time. The **first discriminator** is a conventional supervised classifier (a three-layer deep neural network, ReLU hidden activations, sigmoid output) trained on normal CAN images *and* real attack images captured from a vehicle; it is the known-attack detector. The **second discriminator** is trained adversarially, in the GAN process: a generator (a five-layer deconvolutional network) produces fake CAN images from random noise, and the second discriminator learns to tell real normal images from the generator's fakes — in the authors' account the second discriminator "ultimately wins" that contest, so it can flag even near-real inputs that are not genuine traffic. The generator is a training device only; it plays no part in detection. A test image reaches the second discriminator only if the first clears it, and at either stage an output below the detection threshold (**0.1**) classifies the image as abnormal. An image counts as an attack image if it contains at least one attack packet (attack threshold 1).

**The dataset, as the paper describes making it.** The authors captured traffic from a **Hyundai YF Sonata**: a Y-cable into the OBD-II port (under the steering wheel), a Raspberry Pi 3 onto the CAN bus, and a laptop connected over WiFi. Each dataset is about **10 minutes** of traffic from the running vehicle, labelled into attack-free and attack portions. The attacks are the authors' own injections: **DoS** (ID 0x000 frames every **0.3 ms**), **FUZZY** (spoofed random ID and data values every **0.5 ms**), and **RPM/GEAR** (frames carrying RPM/GEAR-related IDs every **1 ms**). The authors released this dataset publicly (via the OCS Lab site, ocslab.hksecurity.net, as the CAN-intrusion dataset — the corpus later widely used as the Car-Hacking dataset). Sizes as tabled: normal training data 1,171,637 messages; DoS 3,665,771 messages / 17,128 attack images; FUZZY 3,838,860 / 20,317; RPM 4,621,702 / 32,501; GEAR 4,443,142 / 29,751; each attack dataset is independent, not multi-class.

**Results, at exactly the strength the paper reports them.** The first discriminator detects the attack it was trained on (detection rates: DoS 99.9%, FUZZY 98.7%, RPM 99.6%, GEAR 99.8%) and almost nothing else — cross-attack detection is 0.0–2.0%, with one exception the table itself shows (a FUZZY-trained discriminator catches 33.0% of RPM attacks). The **second discriminator**, in whose training *none* of the four attacks was used, is the paper's result: detection rate / precision / accuracy / AUC of **99.6% / 96.8% / 97.9% / 0.999** on DoS, **99.5% / 97.3% / 98.0% / 0.999** on FUZZY, **99.0% / 98.3% / 98.0% / 0.999** on RPM, and **96.5% / 98.1% / 96.2% / 0.996** on GEAR — summarised by the authors as an average of 98% accuracy across the four unknown attacks. No combined end-to-end figure for the cascaded system is tabled; the tables are per-discriminator. Detection speed on the authors' testbed (Xeon E5-1650 v4, 32 GB RAM, GTX 1080): **0.18 s to evaluate ≈1,954 CAN messages**, roughly one second of bus traffic — the basis of the paper's real-time claim. One-hot encoding is itself evaluated: with raw binary images the discriminator output spreads across 0–1 with no usable separation, while one-hot images give a threshold that separates normal from attack data.

## Where it fits

GIDS is the reference deep-learning CAN IDS in this section and the companion paper to a dataset much of the later literature trains on. It sits alongside the other unsupervised/semi-supervised in-vehicle detectors — Cho & Shin's clock-skew fingerprinting (CIDS) and voltage fingerprinting (VIDEN) — as the learned-representation entry: where CIDS and VIDEN fingerprint the *sender* from physical timing/voltage behaviour, GIDS models the *ID sequence* alone. That choice cuts both ways and defines the page's caveat: a frame with a plausible ID pattern is in-distribution for this model regardless of its payload, so the stealthier attack classes later CAN-IDS realism work worries about are largely outside its input. The cascaded design — supervised head for known attacks, GAN-trained head for unknown ones — is the paper's structural contribution, and its first-discriminator table quantifies how poorly a supervised CAN IDS generalises to untrained attack types.

## Limits and safety notes

From the paper and its own evaluation design:

- **The authors' stated open problem:** distinguishing anomalous traffic caused by "normal malfunctioning of electronic components" from anomalous traffic caused by intentional attacks remains challenging — the model flags abnormality, not intent.
- **Single vehicle, self-made attacks.** All training and test data come from one Hyundai YF Sonata and from the authors' own three injection patterns; the "unknown attack" claim is measured against attacks designed by the same team on the same car, not against independently sourced attacks or other vehicles. Hyperparameters (input size 64, threshold 0.1) were tuned on this data and are vehicle-environment-dependent per the paper.
- **IDs only.** By design the model consumes CAN ID sequences and never message payloads, so detection is at the level of ID-pattern abnormality per 64-message image, not per-frame content.
- **Headline discipline:** the tables govern. The conclusion's phrase "average accuracy of 100% for the first discriminator" overstates the paper's own Table 2 (99.9/98.7/99.6/99.8% on the trained attack, near-zero cross-attack); the figures quoted on this page are the tables'.

## Status and sources

Status: **published** (finished 2018 publication; no living artefact). Bibliographic verification: PST 2018 proceedings record — IEEE, pp. 1–6, Belfast, 28–30 August 2018 — and DOI [10.1109/PST.2018.8514157](https://doi.org/10.1109/PST.2018.8514157) verified against Crossref. Full text read: the authors' arXiv preprint (arXiv:1907.07377v1, posted 17 July 2019) — the openly readable version; the proceedings version is shorter (6 vs 9 pages) and whether its figures differ is unverified, so the figures here are the preprint's.

## Related

- [Fingerprinting Electronic Control Units for Vehicle Intrusion Detection](fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md)
- [VIDEN: Attacker Identification on In-Vehicle Networks](viden-attacker-identification-on-in-vehicle-networks.md)
- [Evading Voltage-Based Intrusion Detection on Automotive CAN](evading-voltage-based-intrusion-detection-on-automotive-can.md)
- [On the Real-World Applicability of Automotive CAN Intrusion Detection Systems](on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems.md)
