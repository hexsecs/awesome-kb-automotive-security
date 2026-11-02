---
title: "Viden: Attacker Identification on In-Vehicle Networks"
summary: "Cho and Shin, ACM CCS 2017. Fingerprints transmitting ECUs by their analogue voltage signature, moving CAN defence from detecting an attack to naming the…"
type: entity
category: "Research Papers"
url: "https://arxiv.org/abs/1708.08414"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Cho and Shin, ACM CCS 2017. Fingerprints transmitting ECUs by their analogue voltage signature, moving CAN defence from detecting an attack to naming the ECU responsible."
sources:
  - url: "https://arxiv.org/abs/1708.08414"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1145/3133956.3134001"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - fingerprinting-electronic-control-units-for-vehicle-intrusion-detection
  - evading-voltage-based-intrusion-detection-on-automotive-can
  - gids-gan-based-intrusion-detection-system-for-in-vehicle-network
  - in-vehicle-intrusion-detection
---

Cho and Shin, ACM CCS 2017. Fingerprints transmitting ECUs by their analogue voltage signature, moving CAN defence from detecting an attack to naming the ECU responsible.

## What it is

Kyong-Tak Cho and Kang G. Shin, University of Michigan. *ACM Conference on Computer and Communications Security (CCS) 2017*, pp. 1109–1123. DOI: [10.1145/3133956.3134001](https://doi.org/10.1145/3133956.3134001) (verified via Crossref). Viden is an **attacker-identification** system for CAN, designed to sit alongside a separate intrusion-detection system: when an IDS flags an attack, Viden names which ECU transmitted the attack frames. It fingerprints transmitters by the **analogue voltages of dominant (0) bits on CANH/CANL**, which vary per ECU because of manufacturing variation in supply voltage VCC, ground voltage, and transceiver transistor on-resistance (the paper's observations V1–V4; CANH and CANL transient deviations run in opposite directions, so summing the two cancels transients).

It works in four phases. (1) **ACK-threshold learning:** at Viden's low sampling rate it cannot tell which slot a sample came from, and ACK-slot voltages are driven by *all* receivers in parallel (much higher CANH / lower CANL than data bits), so it learns a per-message-ID threshold and discards ACK samples. (2) **Voltage instances:** each instance summarises a message's samples into six features (F1–F6) — most-frequent CANH/CANL values plus percentile tracking points on both lines. (3) **Attacker identification:** per-ECU **voltage profiles** are the slope Υ of accumulated cumulative voltage deviations over time, fitted online by Recursive Least Squares — profiles therefore track drift (temperature, battery state) instead of being batch-learned once; on detection, a profile built only from the attack messages is matched against stored profiles. (4) **Verification:** a multi-class Random Forest over voltage instances, invoked only when needed (profile collisions, targeted impersonation). Sampling is **50 kSamples/s** (10-bit ADC) — the paper contrasts this with prior voltage fingerprinting needing 2.5 GSamples/s, and with MSE fingerprinting valid only on 10 kbit/s CAN.

**Threat model.** The attacker controls a **remotely compromised, factory-installed ECU**; physically attached devices (e.g. an OBD-II dongle) are explicitly out of scope. Three adversary classes: naive; timing-aware; timing-voltage-aware (can shift its own voltages via battery drain/heating/cooling but **cannot precisely control instantaneous values** — a stated assumption). Adversary goals include hiding which ECU is attacking (arbitrary vs targeted impersonation).

## What it showed

- Evaluation parameters M=30, N=50, κ=15 non-ACK voltages per instance. Prototype: 4 Arduino UNO + MCP2515/MCP2551 nodes at 500 kbit/s, attack messages injected **aperiodically** (random 20–200 ms intervals); the three transmitters' profiles were cleanly distinct.
- Real vehicles (via OBD-II, 500 kbit/s): a **2013 Honda Accord** (6 ECUs, all with distinct profiles) and a **2015 Chevrolet Trax** (5 ECUs, distinct profiles). Ground truth came from timing-based identification (the CIDS approach), used *only* as ground truth. Stationary vs driving profiles were equivalent.
- Headline: **0.2% false identification rate** in simulation of 1,000 targeted-impersonation attempts (Honda dataset, Phase 3 + 200-tree Random Forest Phase 4); 0.3% on the combined 11-ECU two-vehicle dataset.
- Timing-aware adversaries were still identified, on the prototype and in the Accord. A timing-voltage-aware arbitrary impersonation after 8–10 days and 700 miles was handled by profile *adjustment* (both profiles had shifted by the same amount — a common battery/VCC shift — rather than relearning).

## Where it fits

Same authors' follow-on to their CIDS clock-skew IDS (USENIX Security 2016; KB page [Fingerprinting Electronic Control Units](fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md)). The difference, **as the paper itself states it**: CIDS fingerprints ECUs by clock skew in the arrival times of *periodic* messages, and can identify the attacker only if the attack messages are themselves injected periodically — aperiodic injection is still *detected* by CIDS but cannot be *pinpointed*. Viden's fingerprint is in each frame's analogue voltage, so identification works **regardless of injection timing or periodicity**. Viden is an identification layer, not a detector: its system model assumes an IDS (e.g. CIDS) is also installed and does the detecting. It is the physical-fingerprint counterpart to [GIDS](gids-gan-based-intrusion-detection-system-for-in-vehicle-network.md)'s learned ID-sequence model — and the baseline the later voltage-evasion work attacks.

## Limits and safety notes

The paper's own discussion:

- Needs at least one stored voltage profile: a compromised ECU that **transmits no message ID of its own** cannot be accurately identified (the paper suggests building profiles at manufacturing time).
- **Multiple ECUs sharing one message ID** breaks the single-profile-per-ID assumption unless the carmaker's scheduling is known in advance.
- Attacks entering CAN through a **gateway from another in-vehicle network** identify the gateway ECU, not the true source.
- Identification performance depends on the paired IDS's detection; profile collisions are possible (birthday paradox), mitigated by the Phase 4 classifier.
- Small evaluation fleets: 3 prototype transmitters, 6 and 5 vehicle ECUs (the paper notes 3–20 ECUs per CAN bus in modern vehicles).

## Status and sources

Status: **published** (finished 2017 publication). The full text read for this page is the arXiv extended version (arXiv:1708.08414, 35 pp.) of the 15-page proceedings paper; whether any number differs in the proceedings version is unverified. DOI and pp. 1109–1123 verified via Crossref.

## Related

- [Fingerprinting Electronic Control Units for Vehicle Intrusion Detection](fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md) — CIDS, the predecessor; Viden closes its aperiodic-injection identification gap
- [Evading Voltage-Based Intrusion Detection on Automotive CAN](evading-voltage-based-intrusion-detection-on-automotive-can.md)
- [GIDS](gids-gan-based-intrusion-detection-system-for-in-vehicle-network.md)
