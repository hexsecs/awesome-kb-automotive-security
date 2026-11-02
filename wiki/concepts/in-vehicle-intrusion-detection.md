---
uid: 01a19d3c-af64-71fa-9009-d1927143c3c0
title: "In-vehicle intrusion detection and ECU fingerprinting"
summary: "The bus's defence literature, organised by observable signal: timing, clock skew, voltage, learned models — and split by detecting an anomaly vs attributing it."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [fingerprinting-electronic-control-units-for-vehicle-intrusion-detection, viden-attacker-identification-on-in-vehicle-networks, gids-gan-based-intrusion-detection-system-for-in-vehicle-network, a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset, on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems, canter, can-injection]
sources:
  - url: "https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_cho.pdf"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1371/journal.pone.0296879"
    retrieved: 2026-11-01
---

CAN carries no sender authentication: an identifier claims an ECU, and nothing on the wire proves it. Where authentication retrofit is impractical, the field's answer is to watch — learn what genuine traffic looks like so precisely that forged traffic stands out. This KB's defence literature for the bus is otherwise scattered as mitigations inside attack pages; collected, it organises along two axes. The first is the **observable signal**: what physical or statistical property of the traffic the detector measures. The second is the **claim**: *detection* (something is wrong) versus *attribution* (this specific ECU did or did not send this frame). Fingerprinting is attribution technology; most detectors only detect. Confusing the two overstates what a deployment buys.

## Timing and frequency

The oldest family watches *when* frames arrive: each ID is periodic, so inter-arrival statistics expose injected, dropped, or suspended traffic. Miller & Valasek proposed the primitive in 2013 (normal driving emits almost no diagnostic traffic, so rate anomalies are loud), and [CANter](../canter.md) builds a countermeasure monitor on the bus-off line's detection rules. Timing is cheap and needs no training data beyond a baseline — and it is blind to an attacker who transmits on the genuine ECU's own schedule after silencing it, which is why the [availability](can-availability.md) page's suppression mode matters here.

## Clock skew: fingerprinting by oscillator

Each ECU's crystal oscillator runs at a slightly individual rate, so the *accumulated* timing offset of its periodic frames is a fingerprint. [CIDS](../fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md) (Cho & Shin, USENIX Security 2016) made this the canonical attribution result: per-message timed masquerade detection at 100% true positives and 0.055% false positives in its evaluation. [CANvas](../canvas-fast-and-inexpensive-automotive-network-mapping.md) uses the same offsets as an identification primitive for network mapping — the fingerprint works for whoever measures it, defender or mapper. The limits are in the corpus too: [Kicking CAN](../sok-kicking-can-down-the-road-systematizing-can-security-knowledge.md) records that published skew estimators are period-dependent and fail as mapping tools in exactly the conditions CANvas had to repair, and ECUs with near-identical skews defeat single-message attribution — the fingerprint is a distribution, not a per-frame verdict.

## Voltage: fingerprinting by analogue signature

A transmitter's analogue voltage profile — rise shape, levels, ringing — is set by its silicon and its position on the bus, and is far harder to imitate than timing. [VIDEN](../viden-attacker-identification-on-in-vehicle-networks.md) (CCS 2017) built attacker identification on accumulated voltage measurements. This family carries the corpus's sharpest evasion literature: [DUET](../evading-voltage-based-intrusion-detection-on-automotive-can.md) — the masquerade attack in which two compromised ECUs corrupt the bus voltage — showed profile-poisoning and mimicry against voltage-based detectors, defeating every published voltage IDS in its evaluation, subject to the qualifications its page keeps attached. Voltage fingerprinting is the strongest attribution signal in the KB and the one with a demonstrated adaptive adversary — both facts belong in any deployment claim.

## Learned traffic models

The fourth family learns the traffic itself: [GIDS](../gids-gan-based-intrusion-detection-system-for-in-vehicle-network.md) (PST 2018) trains a GAN discriminator on frame sequences. Its page carries the corpus's standing warning about this family's evaluation culture — the paper's conclusion claims an "average accuracy of 100%" that its own Table 2 contradicts; the KB reports the tables. The [ROAD guide](../a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset.md) (PLOS ONE 2024) is the field's own audit: a five-family taxonomy of CAN IDS and per-dataset verdicts on what the public benchmarks can and cannot establish. The [real-world applicability](../on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems.md) study presses the same point from deployment: dataset accuracy is not vehicle accuracy, and most published systems were never evaluated against the constraints of a production bus.

## The detect/attribute line, and the V2X contrast

Detection without attribution can raise an alarm but cannot say which ECU to distrust — and on a bus, the response options (ignore an ID? limp mode?) all need the attribution the detector may not have. The fingerprinting families exist to close exactly that gap, at the price of per-ECU models and an evasion surface. The contrast with [misbehavior detection](misbehavior-detection.md) is structural: that page's problem is *content* truth from validly credentialed stations, decided by an authority with revocation power; this page's problem is *signal* anomaly on a local bus, decided by nobody — a detector can flag, but the vehicle has no revocation act to take against its own brake controller. Detection here is therefore an input to logging, alerting, and degradation policy, not an enforcement loop.

This page synthesizes the KB's own full entity pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source.

## Related

- [Fingerprinting Electronic Control Units (CIDS)](../fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md) — clock-skew attribution, the canonical result
- [VIDEN](../viden-attacker-identification-on-in-vehicle-networks.md) — voltage-signature attacker identification
- [Evading Voltage-Based Intrusion Detection (DUET)](../evading-voltage-based-intrusion-detection-on-automotive-can.md) — the evasion literature for voltage fingerprinting
- [GIDS](../gids-gan-based-intrusion-detection-system-for-in-vehicle-network.md) — learned models, and the evaluation warning its own tables carry
- [A Comprehensive Guide to CAN IDS Data (ROAD guide)](../a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset.md) — the field's taxonomy and dataset audit
- [CAN injection](can-injection.md) — the attack class most of this literature watches for
- [Misbehavior detection](misbehavior-detection.md) — the V2X counterpart: content truth plus an authority loop
