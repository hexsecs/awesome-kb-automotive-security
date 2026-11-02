---
uid: 01a19d3c-af24-7525-b0a5-1169c283f246
title: "A Survey of Remote Automotive Attack Surfaces"
summary: "Miller and Valasek, Black Hat USA 2014. Compares the remote attack surfaces, network architectures, and cyber-physical features of a large set of production…"
type: entity
category: "Research Papers"
url: "https://illmatics.com/remote%20attack%20surfaces.pdf"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Miller and Valasek, Black Hat USA 2014. Compares the remote attack surfaces, network architectures, and cyber-physical features of a large set of production vehicles, framing a remote attack as initial access, CAN message injection, and physical effect."
related: [comprehensive-experimental-analyses-of-automotive-attack-surfaces, adventures-in-automotive-networks-and-control-units, remote-exploitation-of-an-unaltered-passenger-vehicle, experimental-security-analysis-of-a-modern-automobile]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://illmatics.com/remote%20attack%20surfaces.pdf"
    retrieved: 2026-11-01
---

Miller and Valasek, Black Hat USA 2014. Compares the remote attack surfaces, network architectures, and cyber-physical features of a large set of production vehicles, framing a remote attack as initial access, CAN message injection, and physical effect.

## What it is

A 94-page white paper by Charlie Miller and Chris Valasek (IOActive), presented at Black Hat USA 2014 and distributed free from the authors' site (illmatics.com). It is not peer-reviewed, and it is not an exploitation paper: the authors did not acquire most of the vehicles. Each car's features, standards, and network architecture were assembled from manufacturers' technical information sites — the author notes concede that merely finding topology information "could take many hours," and that some manufacturers are absent through parent-company overlap or unusable websites. Its contribution is a measurement frame applied fleet-wide: for each vehicle, the remote attack surface, the internal network layout, and the computer-controlled ("cyber physical") features, combined into a judgement of how hard a remote attack would be. No DOI exists (Crossref title/author query: no record; checked 2026-11-01).

## What it showed

**The three-stage anatomy.** A safety-critical remote attack needs three stages: (1) remotely compromise an ECU that faces the outside world, gaining the ability to inject messages; (2) get those messages to the safety-critical ECUs — usually on a different segment, so the gateway/bridge ECU must be tricked or compromised outright; (3) make the target ECU perform an unsafe action, which requires reverse engineering that manufacturer's message formats. The survey measures stage 1 by attack surface, stage 2 by architecture, and stage 3 by the presence of cyber-physical features — a feature designed to brake or steer on receipt of a network message is susceptibility built in. The caveat is stated up front: the most susceptible-looking vehicle may in fact be quite securely coded, and vice versa; surface is a proxy, not a vulnerability count.

**The surface catalogue**, each entry with a range and a verdict. PATS (the key transponder; ~10 cm): theft or denial of service only, "very small" surface. TPMS (~1 m): warning spoofing, and cited work showing the receiving ECU could be crashed and remotely bricked. Remote keyless entry (5–20 m): small surface. Bluetooth (~10 m, possibly more): "one of the biggest and most viable attack surfaces on the modern automobile," because the stack is large and complex — the paired/unpaired distinction is drawn, with the 2010 Escape's SYNC unit (user-entered 6-digit PIN, no covert pairing path found) as the worked example. Radio Data System (theoretically miles, realistically ~100 m): data is parsed and displayed, but likelihood judged much lower. Telematics / cellular / Wi-Fi: "the holy grail of automotive attacks," because range is wherever cellular coverage is — and a telematics unit had already been remotely exploited with no user interaction in the cited work. Internet / apps: browsers, apps, and hotspots import a desktop-class attack surface — an nmap scan of a 2014 Jeep Cherokee Wi-Fi hotspot shows open ports 2021 and 6667 when running unencrypted.

**Cyber-physical features** are catalogued the same way: park assist, adaptive cruise control, collision prevention, lane keep assist — each a computer physically acting on network messages, typically with built-in limits (park-assist steering only at very low speed; lane-keep movements small).

**Evolution.** The 2010 and 2014 Jeep Cherokee CAN-C diagrams, side by side: the ECU count "more than doubled" in four years, because manufacturers multiplex new features onto existing networks instead of adding wiring.

**The survey itself**: 21 vehicle profiles spanning 2006–2015 (Audi A8; Honda Accord; Infiniti Q50, G37, G35; Jeep Cherokee; Ram 3500; Chrysler 300; Dodge Viper; Cadillac Escalade; Ford Fusion ×2 years; BMW 3 Series, X3, and the paper's "i12"; Range Rover Evoque and Sport ×2; Toyota Prius ×3). Each profile lists standards, wireless communications, cyber-physical features, per-bus ECU inventories, and an entry-point → ECU → bus table with a diagram. The findings drawn from the set:

- TPMS and RKE ECUs are the remote-surface components most likely to share a segment with cyber-physical ECUs.
- **6 of 14 (42%) of the 2014 vehicles had no separation between at least one cyber-physical ECU and at least one remote-attack-surface ECU.**
- Topologies vary widely between makers but cluster by region — Japanese, German, and American architectures each resemble each other.
- Segmentation, where it exists, is rarely a security boundary: "we have rarely seen segmentation used for security boundaries, instead network segmentation is used for non-communicable network buses."
- Newer cars carry more cyber-physical features but also more segmentation — the two trends fight.
- Patchability counts too: recalls for the authors' own Escape and Prius required dealership visits, and over-the-air update essentially did not exist in July 2014.

**The ratings** ("C&C Car Ratings") score each vehicle −− to ++ on the three axes. Most hackable: **2014 Jeep Cherokee, 2015 Cadillac Escalade, 2014 Infiniti Q50**. Least hackable: **2014 Dodge Viper, 2014 Audi A8, 2014 Honda Accord**.

**Defending against remote attacks** — layered, one defence per stage, each assessed sceptically. Secure the remote endpoints (necessary, never sufficient — browser vendors still ship critical patches monthly). Restrict which ECUs may send CAN messages (sandboxing helps; escapes expected). Message cryptography draws the paper's notable dissent: against a *rogue added device* it works, but in the remote scenario the attacker executes code on a legitimate ECU and inherits its keys or its ability to send valid messages, so "this idea doesn't seem to present much of an obstacle in the remote attack scenario." Network architecture (isolate remote-facing from safety-critical ECUs) is recommended with costs attached: expensive, slow, and the necessary bridge becomes the single point of failure — the cited academics crossed networks by compromising the bridge. The defence backed for immediate effect is **attack detection**: automotive traffic is highly regular and computer-to-computer, and every known CAN injection attack takes one of two forms — diagnostic messages, or normal messages at an inflated rate (at minimum double, "in practice 20–100x higher than normal"), because the legitimate sender keeps transmitting. Their proof of concept: an OBD-II device that learns traffic patterns, detects anomalies, and responds by short-circuiting the CAN bus.

**Its relationship to Checkoway et al. 2011, as the survey itself presents it:** the UW/UCSD paper is reference [3] and the load-bearing citation throughout. The three-stage anatomy generalises that paper's results: Checkoway's Bluetooth and cellular-telematics compromises are the cited existence proofs for stage 1; their subnet-bridging demonstration ("the academic researchers… were able to move from one network to the other by compromising the bridge") is the worked example for stage 2; stage 3 is credited to the authors' own prior work ([9], their 2013 Prius/Escape study). Where Checkoway exploited one anonymized sedan end-to-end, this survey does the opposite: no new exploits — the preconditions for the Checkoway chain, measured across the fleet.

## Where it fits

The bridge in this KB between [Checkoway et al. 2011](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md) and the authors' own 2015 Jeep exploitation. Checkoway established that the remote chain exists on one car; this survey made "remote attack surface + network architecture + cyber-physical features" the standard triage for asking how widely it exists — and its most-hackable ranking, the 2014 Jeep Cherokee, grades the authors' next target a year early (see [Remote Exploitation of an Unaltered Passenger Vehicle](remote-exploitation-of-an-unaltered-passenger-vehicle.md)). The stage-3 half of the frame comes from [Adventures in Automotive Networks and Control Units](adventures-in-automotive-networks-and-control-units.md) (2013), the wired study cited as [9]. Its detection-first defence — bus traffic is regular enough to police, and injection betrays itself by rate — is the premise the KB's later CAN intrusion-detection pages build on.

## Limits and safety notes

Inspection, not testing: ratings rest on manufacturers' published documentation of uneven quality, normalised by hand, with some makers omitted; the −−/++ grades are the authors' judgement, not measurements — attack surface is a proxy for the *difficulty* of stage 1, and a well-coded large surface beats a sloppy small one. Its factual snapshot is July 2014: the absence of OTA updates, the Cherokee hotspot's open ports, and the feature lists are period facts, several overtaken within a year by the authors' own Jeep work and the recall that followed. Vehicles are named by the paper itself (unlike the anonymized experimental papers); per-model ECU inventories were not independently re-verified for this page.

## Status and sources

Status: **published** — a finished 2014 white paper; no living artefact, no DOI (Crossref checked, above). Sources: the paper (authors' PDF, illmatics.com), read in full 2026-11-01; the list.

## Related

- [Comprehensive Experimental Analyses of Automotive Attack Surfaces](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md)
- [Adventures in Automotive Networks and Control Units](adventures-in-automotive-networks-and-control-units.md)
- [Remote Exploitation of an Unaltered Passenger Vehicle](remote-exploitation-of-an-unaltered-passenger-vehicle.md)
- [Experimental Security Analysis of a Modern Automobile](experimental-security-analysis-of-a-modern-automobile.md)
