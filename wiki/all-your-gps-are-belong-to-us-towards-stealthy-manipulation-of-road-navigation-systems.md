---
title: "All Your GPS Are Belong To Us: Towards Stealthy Manipulation of Road Navigation Systems"
summary: "Zeng et al., USENIX Security 2018. Spoofs GPS to reroute a driver to an attacker-chosen destination while keeping the displayed route plausible."
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity18/presentation/zeng"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Zeng et al., USENIX Security 2018. Spoofs GPS to reroute a driver to an attacker-chosen destination while keeping the displayed route plausible."
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity18/presentation/zeng"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - drift-with-devil-security-of-multi-sensor-fusion-based-localization-in-high-level-autonomous-driving-under-gps-spoofing
  - sok-how-sensor-attacks-disrupt-autonomous-vehicles-an-end-to-end-analysis-challenges-and-missed-threats
  - physical-channel-sensor-attacks
---

Zeng et al., USENIX Security 2018. Spoofs GPS to reroute a driver to an attacker-chosen destination while keeping the displayed route plausible.

## What it is

Kexiong (Curtis) Zeng (Virginia Tech), Shinan Liu (University of Electronic Science and Technology of China), Yuanchao Shu (Microsoft Research), and Dong Wang, Haoyu Li, Yanzhi Dou, Gang Wang, and Yaling Yang (Virginia Tech). *27th USENIX Security Symposium* (USENIX Security '18), pp. 1527–1542. The paper asks whether GPS spoofing can actually manipulate a *road navigation system* — a harder problem than spoofing a drone or a yacht, because roads constrain where a vehicle can plausibly be, and a human driver is watching for instructions that contradict the physical road. Prior spoofing work set random locations, which produces impossible instructions ("turn left" in the middle of a highway) and alerts the driver. The key idea is stealth through shape-matching: shift the victim's GPS position slightly to a **ghost location** whose navigation route to the destination has the same sequence of turn manoeuvres and near-equal segment lengths as the roads the victim is physically about to drive. Every instruction the navigation system then issues is physically executable, the displayed route looks like the road ahead, and following the fake turn-by-turn directions walks the victim along a different real route — to a wrong destination, a loop, or a wrong way. Three attack goals: deviating (any wrong route), targeted deviating (an attacker-chosen destination area), and endangering (a route containing wrong-way segments). The attacker needs no access to the device or the navigation service, only a rough knowledge of the victim's destination area or an unavoidable checkpoint on the way. The spoofing itself is the well-understood kind: civilian GPS signals are unauthenticated, and a receiver can be taken over either brute-force, by overpowering the genuine signal, or smoothly, by synchronizing with it and gradually pulling away — the smooth variant avoids any abnormal jump but needs costlier tracking hardware. The paper's contribution is to show the cheaper takeover suffices on roads, because what happens *after* the takeover is where previous attacks gave themselves away.

## What it showed

**The spoofer is cheap and works through the car.** A portable spoofer — HackRF One SDR, Raspberry Pi, antenna, power bank, ≈$223 total, remotely operated over SSH via cellular — was measured under a local radio-authority permit in Chengdu. Placed under a back seat or in the trunk, it took over a smartphone's GPS lock in ~35–48 s; between two cars, takeover worked at an effective range of 40–50 m (failure begins around 60 m), still worked with three additional cars parked between spoofer and phone, and once locked, the spoofed signal held for a 15-minute circling drive at ~15 m separation with no disconnections — so both the planted-spoofer and the tailgating geometries are practical, and the car body is no shield.

**The search finds routes almost everywhere.** The road network is built from OpenStreetMap; the basic attack enumerates ghost locations within a drift bound (400 m in the evaluation, within the range of ordinary urban GPS drift), computes each ghost route with the same navigation service the victim uses, and breadth-first-searches real routes from the victim's position whose turn-pattern categories match the ghost route's and whose segment lengths agree within a speed scale factor of 0.2; an iterative variant re-drifts mid-route to chain partial matches, and the targeted variant pre-grids the area and keeps only victim routes passing through the chosen grid. On 600 real taxi trips (300 Manhattan, 300 Boston): the basic attack finds at least one victim route for **all 600 trips** (335 per trip on average; the iterative attack finds 3,507), a loop route for 85% of Manhattan and 98% of Boston trips, and a **wrong-way victim route for 599 of 600 trips (99.8%)**, 90.4% of them containing a highway wrong-way segment. For targeted attacks, median hit rates at 500 m grids are ~70% / 47% / 20% for target areas within 500 / 1,000 / 2,000 m of the original route in Manhattan. The attack tolerates a badly estimated destination (a 1,000 m error still leaves ~half the route overlapping, enough to start) and runs in real time (0.2–0.3 ms per ghost candidate for the basic attack; 0.13–0.32 s iterative).

**Real cars, then real humans.** In real-world driving tests — the authors attacking their own car after midnight in a suburb, transmit power minimized and shielded — the system diverted the driver to pre-defined destinations 2.1 km and 2.5 km from the true one, with instructions firing in real time and the phone never dropping the spoofed lock, despite Google Maps' heading checks and filters. A deceptive user study (driving simulator with a real Budapest map and Google Maps navigation; N = 40 across the US and China; IRB-approved, debriefed afterwards) found **38 of 40 participants (95%) followed the navigation to all the wrong destinations** across four rounds varying rain and day/night. The two who caught it noticed the same classes of inconsistency: highway-vs-local-road mismatch, street names, and landmarks. The study also supplies the attack's enabling habits: navigation use is far heavier in unfamiliar areas (the attack's stated scope), users rely on voice prompts and visual route shape over street-name text, and 95% had previously experienced GPS malfunction — so the ~30 s signal loss during takeover read as ordinary GPS behaviour, not an attack.

## Where it fits

The founding full treatment of GPS spoofing against a *navigation* target, and the single-source predecessor the later fusion work positions against: Shen et al. 2020 cite it explicitly as targeting localization without fusion from other position sources, and Narain et al. extended the question to GPS/INS navigation. In the Zhang SoK's taxonomy it sits in A21–A22 (GNSS spoofing), but it also fills a gap the SoK names: Zhang states that stealthiness is discussed only occasionally and is *not* systematized — this paper is the KB's deepest account of stealth as the binding constraint, achieved not by hiding the spoofing but by making its *consequences* consistent with the map and the driver's expectations. Its defence discussion (§8) is a compact map of the whole GPS defence space, sorted by deployability: signal encryption/authentication is rated most effective and least deployable; receiver hardware defences (angle-of-arrival) need antenna arrays no phone has; receiver consistency checks catch brute-force takeover but not smooth takeover; modification-free checks — cross-verification against other GNSS constellations or network location, IMU dead reckoning — are themselves spoofable or drift-limited. The direction the authors single out as promising is computer-vision location verification (landmarks and street signs checked against the map) — notably, exactly the channel through which the study's two detecting participants caught the attack — with adversarial robustness of the vision models as its open problem.

## Limits and safety notes

As the authors state them: the attack is urban-shaped — dense road networks give the shape-matching search its options, and sparse suburban or rural roads reduce them; it targets drivers navigating unfamiliar areas who actually rely on the system, and does not claim to work on drivers who know the roads. The user study is simulator-based (a game engine, keyboard/mouse control, one route, no wrong-way or loop routes inflicted on participants), its N = 40 sample is half computer-science students — the authors argue the general population should be *more* susceptible — and in the study the phone's locations were supplied by a companion app fed from the simulator, not by RF spoofing; the RF chain is validated separately by the measurements and the authors' own-car driving tests. All RF experiments ran in China with local regulatory permission, after midnight, with power controls to avoid affecting bystanders; no third party's vehicle was ever spoofed. The destination-knowledge assumption (a rough area or a known checkpoint) is real, though the paper shows the attack degrades gracefully as the estimate worsens. Nothing in the paper involves an autonomous stack: the consistency checker being defeated is a human plus a routing engine, and transferring the result to fused AV localization is Drift with Devil's separate question.

## Status and sources

Status: **published** — *Proceedings of the 27th USENIX Security Symposium*, August 2018, pp. 1527–1542. **DOI: none** — USENIX does not assign DOIs to its proceedings papers, and a Crossref bibliographic query (2026-11-01) returned no record for this paper; no aggregator identifier is substituted. Full text read end-to-end from the USENIX proceedings PDF, 2026-11-01. IRB approval #17-936 covered the user study.

## Related

- [Drift with Devil](drift-with-devil-security-of-multi-sensor-fusion-based-localization-in-high-level-autonomous-driving-under-gps-spoofing.md) — Shen et al. 2020; the multi-sensor-fusion successor to this single-source attack
- [SoK: How Sensor Attacks Disrupt Autonomous Vehicles](sok-how-sensor-attacks-disrupt-autonomous-vehicles-an-end-to-end-analysis-challenges-and-missed-threats.md) — GNSS spoofing is its A21–A22; stealth, which this paper is built on, is the axis the SoK does not systematize
