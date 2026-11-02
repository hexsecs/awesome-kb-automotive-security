---
uid: 01a19d3c-af86-73d7-ae20-b3c9bfe965a8
title: "Evading Voltage-Based Intrusion Detection on Automotive CAN"
summary: "Bhatia et al., NDSS 2021. The DUET masquerade attack, in which two compromised ECUs corrupt the bus voltage and defeat every published voltage-based IDS…"
type: entity
category: "Research Papers"
url: "https://www.ndss-symposium.org/ndss-paper/evading-voltage-based-intrusion-detection-on-automotive-can/"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Bhatia et al., NDSS 2021. The DUET masquerade attack, in which two compromised ECUs corrupt the bus voltage and defeat every published voltage-based IDS, including Viden."
sources:
  - url: "https://doi.org/10.14722/ndss.2021.23013"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - viden-attacker-identification-on-in-vehicle-networks
  - gids-gan-based-intrusion-detection-system-for-in-vehicle-network
  - fingerprinting-electronic-control-units-for-vehicle-intrusion-detection
  - error-handling-of-in-vehicle-networks-makes-them-vulnerable
  - a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset
  - in-vehicle-intrusion-detection
---

Bhatia et al., NDSS 2021. The DUET masquerade attack, in which two compromised ECUs corrupt the bus voltage and defeat every published voltage-based IDS, including Viden.

## What it is

Rohit Bhatia, Khaled Serag, Z. Berkay Celik, and Dongyan Xu (Purdue University), Vireshwar Kumar (IIT Delhi), and Mathias Payer (EPFL), at NDSS 2021. Voltage-based IDS (VIDS) — Viden, VoltageIDS, Scission, SIMPLE, and EASI — identify the sender of each CAN message from the analogue voltage fingerprint of its dominant bits, on the assumption that the fingerprint is fixed by the transmitter's hardware: a software-compromised ECU cannot controllably change its own fingerprint, let alone another ECU's. DUET is a masquerade attack that breaks the assumption at the measurement rather than the hardware: two compromised ECUs — an *attacker* and an *accomplice* — arrange that the recorded voltages are no longer any single ECU's. The paper also proposes a defence, RAID. DOI: 10.14722/ndss.2021.23013 (Status and sources).

## What it showed

**The voltage corruption tactic.** When two ECUs transmit simultaneously, the bus voltage is the superposition of both, and the resultant bit is the logical AND. The accomplice first drives the attacker into the *error-passive* state by deliberately colliding with its messages (a controller property reached via the error counter, not a software setting). The attacker then transmits simultaneously with the victim, using the victim's ID and bit-identical content up to a chosen bit inside the message's predictable prefix (PREP — the constant, counter, or otherwise predictable bits after arbitration; the control field alone guarantees ≥6 constant bits, and most messages on five profiled cars carried ≥1 byte), then sends recessive where the victim sends dominant. The victim sees the dominant resultant bit and completes its message unaware; the attacker hits the bit-error and stops, and because it is error-passive its error frame is all-recessive — no trace on the bus; its controller is set to one-shot mode so the aborted frame is never retransmitted. Synchronisation despite the spacing mismatch (error-passive needs an 11-bit intermission, error-active 3 bits) comes from the accomplice sending a "preceded ID" message just before the victim's periodic message, so both start after it with matched spacing. The VIDS therefore records, for the overlapped prefix, summed "victim + attacker" voltages as the victim's samples.

**Why the corruption is classifier-independent.** Samples from a single transmission follow a unimodal voltage distribution; samples from a simultaneous transmission are bimodal. Features computed from *any* simultaneous transmission (victim+attacker) are statistically closer to those of any other (accomplice+attacker) than to any single transmission's, so the corrupted profile and the attack-time profile land together whatever feature set or classifier the VIDS uses — the flaw is in the physical collection of voltage data on a shared bus.

**Stage 1 — fingerprint manipulation (training-set poisoning).** Fingerprints drift (one cited VIDS tolerates ~6 °C of temperature change, another ~10 °C; also supply voltage, workload, updates, aging), so every VIDS retrains — online, incrementally, or periodically (e.g. daily). During retraining, DUET corrupts one additional PREP bit, holding each level longer than the inter-retraining period, so each retraining absorbs a fingerprint one bit closer to fully corrupted; benign victim messages the attacker misses (timing accuracy 60–87%) are learned alongside, keeping the victim's genuine traffic alarm-free. Against online-learning Viden, Stage 1 completes in seconds; against daily-retraining Scission, in days — the paper frames it as a low-and-slow, APT-style attack. Existing "secure retraining" (authenticating the *messages* recorded) does not stop it — the corruption is in the payload's voltage samples — and since DUET can poison more than half the training samples, outlier-removal defences fail too.

**Stage 2 — impersonation.** The accomplice transmits the forged victim message while the attacker corrupts the accomplice's fingerprint in the same way; the VIDS classifies "accomplice + attacker" as the victim, whose learned fingerprint is "victim + attacker".

**Evaluation.** DUET was implemented in 1,400 lines of C++ and run on a 10-node Arduino/MCP2515 testbed (500 kbit/s, 50% busload) and on three buses in two real cars (both deliberately anonymized: a 2011 car, 4 ECUs / 50 messages / 35% busload; a 2013 car, buses of 6 ECUs / 88 messages / 61% and 3 ECUs / 27 messages / 34%), the attacker/accomplice pair attached via a customised OBD connector. Two of the five VIDS were implemented and measured directly. Against Viden (50 kS/s, six features per eight messages, random forest): per-message impersonation success exceeds 75% corrupting only the control bits (0.75 byte of PREP) and reaches 95% at 3 bytes; because Viden decides on an eight-message aggregate, effective impersonation success reaches 100% — the paper's headline is at least 90% impersonation success evading the two evaluated VIDS. Against Scission (20 MS/s, 48 features reduced to 18, logistic regression; SVM, Naive Bayes, and random-forest variants behaved alike): over 50% with control bits only, 76% at 3 bytes — and Scission's alarm counter (+4 per suspicious message, −1 per trustworthy one, alarm above 200) then needs roughly 1,000 spoofed messages to trip, about 10 s for a 10 ms-period brake message; the authors demonstrated forged Engine Control Unit RPM readings on the real car's dashboard with no alarm. The remaining three systems in the paper's comparison table (VoltageIDS, SIMPLE, EASI) are argued vulnerable rather than measured — Scission is presented as using a superset of their samples and features.

**The paper's own boundary on that claim.** DUET needs a retraining window. SIMPLE reduces retraining by updating fingerprints from supply-voltage/temperature models, and the paper states plainly — twice — that DUET cannot evade SIMPLE if it does not require retraining, while noting that modelling every drift factor is hard in practice. Payload encryption would cap PREP at the control field, reducing but not eliminating success.

**RAID (the proposed defence).** Randomized Identifier Defense changes only retraining: each ECU then sends its messages in extended frame format, with the 18-bit ID-B field carrying a fresh random nonce; receivers identify messages by the unchanged ID-A and discard ID-B, so priority and scheduling are preserved. The attacker can no longer predict the victim's arbitration bits — guessing the full field correctly has probability 2^-18 per message — and DUET's success against Scission fell to 0% on all platforms. Costs (retraining only): nonce generation ~50 µs, precomputable in idle time; busload up 7–13%; latency +50 µs.

## Where it fits

The direct counterpoint to the Viden page. Viden's threat model grants a timing- and voltage-aware attacker but assumes it "cannot precisely control instantaneous values" of the voltage signal; DUET shows two colluding ECUs do not need to control their own values — they control what the monitor measures, and they poison what it learns from. It is the physical-layer analogue of this cluster's dataset lesson (attack the training distribution, not the classifier). Its scope is deliberately narrow: DUET evades VIDS only; evading message-based IDS or CIDS simultaneously is a separate problem (CIDS evasion by clock-skew cloaking was already shown by others).

## Limits and safety notes

- The threat model is strong: arbitrary code execution on at least two ECUs, plus a one-time reverse-engineering effort to learn the target model's message timing and payload structure. A single compromised ECU cannot run DUET.
- Only Viden and Scission were experimentally evaluated; the claims covering VoltageIDS, SIMPLE, and EASI are analytical, and SIMPLE's no-retraining mode is a stated exception (above). The first-line summary's "every published voltage-based IDS" should be read with both qualifications attached.
- The experimental vehicles are anonymized by the authors and must not be named or guessed. (Three further cars' public traces were profiled for traffic characteristics only — not attack targets.)
- Success is bounded by synchronisation accuracy and PREP length: Stage-1 timing accuracy fell to 60% on the busiest bus, and per-message success against Scission tops out at 76% — practical evasion there rests on the alarm-aggregation argument, not on per-message perfection.

## Status and sources

Status: **published** — a finished NDSS 2021 publication. DOI [10.14722/ndss.2021.23013](https://doi.org/10.14722/ndss.2021.23013) verified against Crossref on 2026-11-01 (record title and all six authors match; publisher Internet Society). Full text read end-to-end from the authors' PDF, 2026-11-01. RAID and supplementary material: github.com/CAN-Bus-Duet/CAN-Bus-Duet.

## Related

- [Viden: Attacker Identification on In-Vehicle Networks](viden-attacker-identification-on-in-vehicle-networks.md) — the voltage-fingerprinting system DUET is built against
- [Fingerprinting Electronic Control Units for Vehicle Intrusion Detection](fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md) — the timing side-channel sibling; different assumption, separately shown evadable
- [Error Handling of In-Vehicle Networks Makes Them Vulnerable](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md) — the error-state behaviour DUET's corruption tactic builds on
- [A Comprehensive Guide to CAN IDS Data and Introduction of the ROAD Dataset](a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset.md)
- [GIDS: GAN based Intrusion Detection System for In-Vehicle Network](gids-gan-based-intrusion-detection-system-for-in-vehicle-network.md)
