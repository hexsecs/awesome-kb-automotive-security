---
uid: 01a19d3c-afb5-7e94-8beb-e703f655f31f
title: "On the Real-World Applicability of Automotive CAN Intrusion Detection Systems"
summary: "Lazeski et al., USENIX VehicleSec 2026. Work in progress showing that ML-based CAN intrusion detectors often learn dataset shortcuts because common datasets…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/vehiclesec26/presentation/lazeski"
status: published
last_checked: 2026-11-01
created: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: 61ba124
list_summary: "Lazeski et al., USENIX VehicleSec 2026. Work in progress showing that ML-based CAN intrusion detectors often learn dataset shortcuts because common datasets contain only simple attacks, so high scores do not imply robustness against a practical attacker."
sources:
  - url: "https://www.usenix.org/conference/vehiclesec26/presentation/lazeski"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - gids-gan-based-intrusion-detection-system-for-in-vehicle-network
  - a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset
  - car-hacking-dataset
  - can-train-and-test
  - in-vehicle-intrusion-detection
---

Lazeski et al., USENIX VehicleSec 2026. Work in progress showing that ML-based CAN intrusion detectors often learn dataset shortcuts because common datasets contain only simple attacks, so high scores do not imply robustness against a practical attacker.

## What it is

Kristijan Lazeski, Jannis Hamborg, Christoph Krauß, and Alexander Wiesmaier (Darmstadt University of Applied Sciences; ATHENE) and Michael Zohner (University of Applied Sciences Fulda), at the 4th USENIX Symposium on Vehicle Security and Privacy (VehicleSec '26, Baltimore, August 2026; proceedings pp. 135–145). The title begins "WIP:" — it is a work-in-progress paper, and says so about itself throughout. Not a new IDS and not a new dataset: an audit of what machine-learning CAN intrusion detectors actually learn. The method has three parts: (1) a structural analysis of five widely used datasets — the HCRL Car Hacking, OTIDS, and Survival datasets, can-train-and-test (CT&T), and the Car Hacking Attack & Defense Challenge 2020 dataset — covering trace organisation, recorded fields, attack construction, class distribution, and CAN-ID/payload overlap between benign and malicious traffic; (2) decision trees (DTs) trained per dataset and per attack type as interpretable stand-ins for ML detectors, over CAN ID, DLC, payload (as one integer and per byte), and an engineered *interval* feature (time since the ID last appeared), with absolute timestamps also available to the trees; (3) a re-assessment of the learned rules against a stated attacker model: an adversary with physical bus access (OBD-II or a compromised ECU) who can observe traffic and adapt CAN ID choice, payload values, and injection timing, without keys or proprietary specifications — plus a stronger physical-layer variant that can also suppress legitimate frames. Evaluation is binary and per-frame. No DOI (see Status and sources).

## What it showed

Headline: the trees reach F1 ≈ 1.000 on nearly every dataset and attack type — and the rules they learn are mostly dataset artefacts.

- **DoS.** In Car Hacking, Survival, OTIDS, and the Challenge dataset, DoS traffic is CAN ID 0x000 with an all-zero payload — a combination absent from benign traffic, so the learned rule is effectively a single split on the ID. CT&T deviates only slightly (IDs 0x000 and 0x002, three constant payloads, likewise absent benignly). An attacker who floods with a different high-priority ID, or varies the payload, keeps the denial-of-service effect and evades the rule entirely.
- **Spoofing.** Fixed ID–payload patterns outside the benign distribution: Car Hacking's gear spoofing uses ID 1087 with a single static payload, its RPM spoofing likewise one fixed payload; Survival's malfunction attack targets ID 0x153 with payloads outside the benign range; OTIDS's impersonation frames carry 8 data bytes where benign remote-frame requests carry none; CT&T's speed spoofing uses three fixed payloads encoding 0, 10, and 60 mph, none occurring benignly. Classification reduces to memorising constants; an attacker who observes the valid ranges and injects in-range values — still affecting the vehicle — bypasses every such rule. The Challenge dataset proves the point against itself: its submission and final files use spoofing patterns different from the training file's, and the trained model detects nothing there (F1 = 0.000).
- **Fuzzing.** Here benign and malicious traffic overlap in ID–payload space, so the trees cannot memorise constants — and instead exploit recording structure: they split first on the interval feature, then on payload bytes, and in places on absolute UNIX timestamps, i.e. they encode the recording's temporal attack boundaries (F1 93.7% on CT&T to 99.8% on Car Hacking and Survival). An attacker who adapts injection timing invalidates such splits; conversely, legitimate traffic outside the recording window risks misclassification.
- **Replay** (present only in the Challenge dataset). Replayed frames are genuine benign frames, so no general ID–payload rule exists to learn; the trees overfit — timestamp splits appear already at the second tree level — and scores are the study's worst (F1 54.7–76.4%) with by far its largest trees (up to 10,707 nodes).
- **Structural artefacts.** OTIDS attack files mix benign and malicious frames without frame-level labels, and earlier published work labelled entire attack files as malicious, so models learn file-level differences with timestamps as the primary feature. In Car Hacking, eleven benign CAN IDs appear only in the fuzzing file (ECU responses triggered by the injections), so the benign file does not cover all legitimately observable traffic — condition-triggered legitimate frames risk false positives at deployment, and an attacker can deliberately trigger such signals to raise false positives or mask activity. Class imbalance is severe in places (DoS is 2% of CT&T traces, 4% of Survival), inflating accuracy-style metrics.

The authors group these into three dataset limitations: attacks implemented as static, uniquely identifiable ID–payload combinations, reducing detection to recognising dataset-specific constants rather than malicious behaviour; incomplete benign coverage; and file-level separation, timestamp discontinuities, and labelling ambiguities that introduce structure unrelated to vehicle behaviour. Their conclusion: "the bottleneck is dataset realism, not model choice." Models trained on raw frames largely re-derive the static ID/payload ranges already specified in the manufacturer's DBC file — work better done by rule-based pre-filtering from vehicle specifications and domain knowledge, with ML applied to the residual traffic; they note manufacturers in practice deploy rule-based IDSs encoding exactly that knowledge. Their criteria for future datasets: realistic attacker capabilities and injection strategies, proper frame-level labelling, representative benign coverage across operating conditions, no file-level or timestamp-based separability, and multi-bus topologies.

## Where it fits

The model-side capstone of this cluster. The ROAD guide documents the same datasets' flaws from the data side; this paper shows what a learner does with them — the mechanism by which flawed data becomes a confident but empty detector. It also calibrates how to read headline numbers elsewhere in the KB: GIDS's supervised stage is exactly the per-frame setting audited here, evaluated on the Car Hacking dataset whose artefacts both papers catalogue, so its high scores inherit this paper's caveats. The attacker model is the bridge to the evasion work: as DUET asks whether voltage fingerprinting survives an attacker who adapts the physical channel, this paper asks whether learned payload/timing rules survive an attacker who adapts ID, payload, and timing. (ROAD appears in the paper's 14-dataset overview table but is not one of the five analysed in depth.)

## Limits and safety notes

The paper's own stated limitations bound every claim above:

- It is explicitly preliminary — a work in progress, as its title states.
- Decision trees are a proxy. The authors argue that artefacts dominating DT decisions will be exploited at least as much by opaque models trained on the same feature distributions (and cite tree-based models achieving deep-learning-comparable CAN IDS performance), but concede model-specific decision-boundary differences cannot be excluded.
- Training is binary and per-attack-type (chosen so dominant patterns cannot mask subtler ones), and the detection scope is per-frame and binary only: nothing here is shown about window/sequence-based detectors, multi-class settings, physical-layer (voltage/clock) fingerprinting, or specification-based IDS.
- Two of the five datasets qualify the headline in opposite directions: the Challenge's changing patterns already break pattern-memorising models inside its own test files, and CT&T was designed as a curated corpus — its attacks are still static-pattern.

## Status and sources

Status: **published** — a finished, published work-in-progress paper (VehicleSec '26 proceedings, pp. 135–145; ISBN 978-1-939133-56-4). DOI: none — USENIX does not assign DOIs to its proceedings papers, and a bibliographic title/author query against Crossref on 2026-11-01 returned no record for this paper. Full text read end-to-end from the USENIX open-access proceedings PDF, 2026-11-01. Artefact (data and models): TU Darmstadt tudatalib, handle/tudatalib/5167, as footnoted in the paper.

## Related

- [GIDS: GAN based Intrusion Detection System for In-Vehicle Network](gids-gan-based-intrusion-detection-system-for-in-vehicle-network.md) — the supervised per-frame setting this paper audits, on the same dataset
- [A Comprehensive Guide to CAN IDS Data and Introduction of the ROAD Dataset](a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset.md) — the data-side companion audit
- [Car Hacking Dataset](car-hacking-dataset.md)
- [can-train-and-test](can-train-and-test.md) — one of the five datasets analysed (Lampe & Meng's CT&T)
