---
uid: 01a1e6dc-fe95-75da-8bf6-db51287a60fd
title: "Fleet Cyber Challenge"
summary: "NMFTA's free self-paced capture-the-flag lab for commercial vehicle security, with scenarios on CAN traffic analysis, ELD compromise, GPS spoofing, firmware…"
type: entity
category: "Learning Resources"
url: "https://nmfta.org/standards/cybersecurity/fleet-cyber-challenge/"
status: active
last_checked: 2026-11-17
created: 2026-11-15
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: a570090
list_summary: "NMFTA's free self-paced capture-the-flag lab for commercial vehicle security, with scenarios on CAN traffic analysis, ELD compromise, GPS spoofing, firmware artifacts, and telematics API credentials, needing no account to start."
related:
  - cybersecurity-for-commercial-vehicles
  - drift-with-devil-security-of-multi-sensor-fusion-based-localization-in-high-level-autonomous-driving-under-gps-spoofing
  - expanding-the-attack-scenarios-of-sae-j1939-a-comprehensive-analysis-of-established-and-novel-vulnerabilities-in-transport-protocol
  - automotive-cyber-security
  - pretty-j1939
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-15
  - url: "https://nmfta.org/standards/cybersecurity/fleet-cyber-challenge/"
    retrieved: 2026-11-17
---

NMFTA's free self-paced capture-the-flag lab for commercial vehicle security, with scenarios on CAN traffic analysis, ELD compromise, GPS spoofing, firmware artifacts, and telematics API credentials, needing no account to start.

## What it is

The Fleet Cyber Challenge is a free, always-open capture-the-flag lab from the National Motor Freight Traffic Association (NMFTA), launched in November 2026. Unlike research-oriented automotive CTFs built around passenger cars and single events, it is aimed at the people who maintain commercial fleets: fleet IT and fleet technicians first, with no cybersecurity background assumed. The site is explicit that it is not a competition — no time limit, no leaderboard, no prizes, no pay-to-play — and no email is needed to start the first challenge.

## How it works

Scenarios are progressively harder and modelled on situations a fleet team could actually meet, without VM setup. The listed challenges cover fleet log analysis, GPS spoofing investigation, ELD compromise investigation, CAN traffic analysis, firmware artifact analysis and API credential discovery, all built around J1939, ECUs, telematics and diagnostic ports. Every scenario runs on simulated environments with fictional data, so nothing touches a live vehicle or production system. Completing challenges earns numbered, downloadable "Mile Markers" rather than leaderboard points, and an optional survey appears around the midpoint of progress.

The content is grounded in NMFTA's own work: the Heavy Vehicle Cybersecurity Assessment and Testing Tool and published vulnerability findings including a CVE on trailer brake-controller compromise. That grounding is the reason the lab speaks J1939 and fleet operations rather than generic IT security.

## Where it fits

This is the entry-level, commercial-vehicle counterpart to the rest of the heavy-vehicle material in the KB. [Cybersecurity for commercial vehicles](cybersecurity-for-commercial-vehicles.md) is the book-length background, and the [J1939 attack-scenarios talk](expanding-the-attack-scenarios-of-sae-j1939-a-comprehensive-analysis-of-established-and-novel-vulnerabilities-in-transport-protocol.md) is where a graduate of the lab can go deeper. [Pretty J1939](pretty-j1939.md) is the tooling for working with J1939 traces, [Drift with Devil](drift-with-devil-security-of-multi-sensor-fusion-based-localization-in-high-level-autonomous-driving-under-gps-spoofing.md) covers the GPS-spoofing research behind one scenario, and [Automotive cyber security](automotive-cyber-security.md) is the general reference.

## Limits and safety notes

The site deliberately positions this as entry-level — its FAQ says it is probably not challenging enough for an experienced researcher — so treat it as a first foothold, not an advanced range. It is a browser-based lab with fictional data, so findings and artefacts do not transfer directly to a real truck. No challenge was attempted for this page; the description comes from NMFTA's own page. The absence of a leaderboard is a design choice, not a lack of scoring: progress is tracked through the Mile Markers.

## Status and sources

Checked 2026-11-17. **Active** at this check: the lab is open and free, with the launch announced by NMFTA on 2026-11-03 and related posts through 2026-11-13. As a web service, "active" records availability at the check date, not a service-level guarantee.

- [Fleet Cyber Challenge](https://nmfta.org/standards/cybersecurity/fleet-cyber-challenge/)

## Related

- [Cybersecurity for commercial vehicles](cybersecurity-for-commercial-vehicles.md)
- [Drift with Devil: security of multi-sensor fusion based localization under GPS spoofing](drift-with-devil-security-of-multi-sensor-fusion-based-localization-in-high-level-autonomous-driving-under-gps-spoofing.md)
- [Expanding the attack scenarios of SAE J1939](expanding-the-attack-scenarios-of-sae-j1939-a-comprehensive-analysis-of-established-and-novel-vulnerabilities-in-transport-protocol.md)
- [Automotive cyber security](automotive-cyber-security.md)
- [Pretty J1939](pretty-j1939.md)
