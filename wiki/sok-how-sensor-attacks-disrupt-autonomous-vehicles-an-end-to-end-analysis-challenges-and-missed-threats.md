---
title: "SoK: How Sensor Attacks Disrupt Autonomous Vehicles: An End-to-end Analysis, Challenges, and Missed Threats"
summary: "Zhang et al., arXiv 2025. Traces how sensor-induced errors propagate through perception, localization, planning, and control to physical impact, and…"
type: entity
category: "Research Papers"
url: "https://arxiv.org/abs/2509.11120"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Zhang et al., arXiv 2025. Traces how sensor-induced errors propagate through perception, localization, planning, and control to physical impact, and identifies 12 previously overlooked attack vectors."
sources:
  - url: "https://arxiv.org/abs/2509.11120"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
  - illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications
  - adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving
  - invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving
  - does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack
  - a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving
  - on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance
---

Zhang et al., arXiv 2025. Traces how sensor-induced errors propagate through perception, localization, planning, and control to physical impact, and identifies 12 previously overlooked attack vectors.

## What it is

Qingzhao Zhang and Shaocheng Luo (equal contribution), Z. Morley Mao (University of Michigan), Miroslav Pajic and Michael K. Reiter (Duke University). A systematization of knowledge (SoK) over 121 papers published 2015–2025, drawn from security venues (IEEE S&P, CCS, USENIX Security, NDSS, EuroS&P, and others), systems and AI venues, and robotics venues. Its scope is wider than the road car: self-driving cars (SDCs), unmanned ground vehicles (UGVs), and unmanned aerial vehicles (UAVs), across cameras, LiDAR, mmWave radar, GNSS, IMUs, and fused systems. Its organising device is the System Error Propagation Graph (SEPG): a directed hypergraph whose nodes are physical attack vectors, errors of system components, or physical-world consequences, and whose edges are transitions (attack-to-error, error-to-error, error-to-impact) gated by explicit conditions. Every error node carries attributes — Precision, Continuity, Intensity, whether the target is moving (DynamicTarget), whether the error's value evolves (DynamicImpact), and the impact's distance to the target (DistanceImpactToTarget) — and nine construction rules (R1–R9) govern how attributes propagate: uncertainty caps Precision, sub-90% per-frame success caps Continuity, tracking can upgrade Continuity, prediction can shrink DistanceImpactToTarget, fusion is modelled as a transition an error must dominate to pass, and collision/braking impacts require a close error against a moving target. SEPGs are built manually — two experts independently, reconciled by discussion — and the graph, not the attack catalogue, is the paper's unit of analysis. Three research questions structure it: how sensor errors propagate to physical impact (RQ1), what feasibility barriers impede end-to-end attacks (RQ2), and which propagation paths remain overlooked (RQ3).

## What it showed

The systematization itself (RQ1) sorts the literature into 34 attack categories (A1–A34, Table IV): camera patch, laser, infrared, and strong-light attacks (A1–A12); LiDAR spoofing (A13–A18); radar spoofing (A19–A20); GNSS spoofing (A21–A22); acoustic/EMI attacks on IMUs and cameras (A23–A25); and physical-object or agent-behaviour attacks (A26–A34), including a cross-modal disappearing object (A30), trajectory-prediction attacks (A32–A33), and a planning attack (A34). Defences are systematized the same way, by which propagation step they constrain (D1–D7): hardware/raw-signal hardening, perception fusion, localization fusion, AI-model robustness, spatial/temporal/contextual consistency checks, control-software defences, and multi-agent collaboration. The eight feasibility findings (RQ2) are the paper's core. Fusion blocks single-sensor attacks but is barely analysed: only 4 of 59 object-detection or localization attacks were evaluated under sensor fusion (Finding 1). Precision degrades under environmental uncertainty and limited attacker knowledge — one cited GNSS attack optimizes using the victim's LiDAR image, an input a remote attacker would not have (Finding 2). Many attacks need high Continuity to survive filtering and tracking (Finding 3). The errors that matter must be close to the vehicle, but close range is exactly where spoofing is hardest, because dense point clouds and large image features resist forgery (Finding 4). Real stacks are not chained AI models: Baidu Apollo selects its predictor by scenario, smooths trajectories, and does not predict static objects at all, which defeats assumptions in published prediction attacks (Finding 5). Indirect errors — sign misdetection, latency, prediction errors — bite only in carefully arranged scenarios (Finding 6). Tracking and prediction can amplify small detection errors and so overcome some close-range limits, at the price of demanding precision and continuity (Finding 7). And localization is a shared dependency: ego-pose error distorts detection, prediction, and planning together (Finding 8). For RQ3 the graph's unused paths yield 12 overlooked vectors (N1–N12): tracking attack by misclassification, a multi-modal latency-discrepancy attack, prediction attack via localization error, LiDAR tracking and misclassification variants, joint detection–tracking–prediction attacks, joint camera+LiDAR and joint GNSS+IMU attacks against fusion itself, joint perception–planning attacks, and scenario-aware longer-term hybrid sequences (N9–N12 are clusters of coordinated attacks rather than single vectors). Proof-of-concept experiments cover N1–N3, run on recorded nuScenes data through BEVFusion, AB3DMOT, and Trajectron++: flipping a nearby car's class to "motorcycle" for 0.5 s destroys its track and its prediction; delaying the LiDAR stream by 1 s displaces fused detections and misses a vehicle 10 m ahead; injecting under 1 m of ego-pose error displaces every observed trajectory and can fabricate an approaching vehicle that triggers braking. A pilot user study (15 AV-security experts, IRB-approved) rated SEPG faithful and usable — at least 90% "correct or largely correct" on six dimensions, uncertainty modelling weakest at 53% — and an LLM evaluation (GPT-4/o3, Grok 3, Gemini 2.5 Pro) found LLM-drafted SEPGs structurally complete and 65–70% error-free: a usable first draft, not an authority.

## Where it fits

The widest end-to-end frame in this KB's sensor line, and the one that explains why its individual results do or do not compose. The KB's full sensor papers sit inside its categories: Petit et al. 2015 is the founding camera/LiDAR experimental leg; Illusion and Dazzle and the NDSS 2025 realism study (cited here as the next-generation LiDAR reference) bound what A13–A18-style spoofing can actually inject; Cao et al. 2019 is the canonical LiDAR false-positive path, and Cao et al. 2021 answers Finding 1 from the attack side by defeating fusion directly. Lou et al. 2024's trajectory-prediction attack belongs to the A32–A33 family, and this SoK's N3 inverts Lou's direction — reach prediction through localization error instead of through perceived objects. Wang et al. 2023's system-level null result is Finding 5 stated as an experiment: component success that the full pipeline absorbs. Against its companion SoK (Khan et al.), the division is breadth versus depth: Zhang spans three platforms and the full pipeline to physical impact but treats each attack qualitatively; Khan stays inside road-vehicle perception and counts. Both conclude that fusion is simultaneously the field's default defence and its least-tested assumption.

## Limits and safety notes

SEPG is a qualitative systematization device, not a measurement: attributes are coarse three-level judgements supplemented by natural language, graphs are hand-built, and the authors state it should complement, not replace, realistic experiments. The proof-of-concept validation is dataset-level — recorded nuScenes scenes through open-source models — and the paper itself says full feasibility assessment would require real-world evaluation; no vehicle was attacked. Scope exclusions are explicit and matter for KB use: end-to-end / foundation-model driving stacks are out (the modular pipeline is assumed), network attacks on connected vehicles are out, and stealthiness is discussed only occasionally, not systematized — a reader should not cite this SoK for any of the three. The literature window closes at 2025. The overlooked vectors N1–N12 are propagation-plausible paths derived from graph gaps, validated only for N1–N3 and only at dataset level; the page reports them as proposed, not demonstrated.

## Status and sources

Status: **published** — a finished work in the KB's sense, but as an arXiv preprint, with no peer-reviewed venue version found: arXiv:2509.11120, first posted 14 September 2025 (hence the stub's "arXiv 2025"), read here in v5 of 7 September 2026, 24 pages including appendices. **No DOI exists for this work as far as could be verified**: the arXiv record carries no DOI and no journal reference, and Crossref queries (title and bibliographic) returned no matching record — only unrelated works. This page therefore cites the arXiv identifier only, deliberately. One internal inconsistency is preserved rather than smoothed: the user-study section states coverage of "13 of the 38 attack categories in Table IV", while Table IV as printed enumerates 34 (A1–A34); this page follows the table. The systematized papers were not re-read beyond what the SoK itself reports.

## Related

- [SoK: The Next Frontier in AV Security](sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion.md)
- [Remote Attacks on Automated Vehicles Sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md)
- [Illusion and Dazzle](illusion-and-dazzle-adversarial-optical-channel-exploits-against-lidars-for-automotive-applications.md)
- [Adversarial Sensor Attack on LiDAR-Based Perception](adversarial-sensor-attack-on-lidar-based-perception-in-autonomous-driving.md)
- [Invisible for Both Camera and LiDAR](invisible-for-both-camera-and-lidar-security-of-multi-sensor-fusion-based-perception-in-autonomous-driving.md)
- [Does Physical Adversarial Example Really Matter to Autonomous Driving](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md)
- [A First Physical-World Trajectory Prediction Attack](a-first-physical-world-trajectory-prediction-attack-via-lidar-induced-deceptions-in-autonomous-driving.md)
- [On the Realism of LiDAR Spoofing Attacks](on-the-realism-of-lidar-spoofing-attacks-against-autonomous-driving-vehicle-at-high-speed-and-long-distance.md)
