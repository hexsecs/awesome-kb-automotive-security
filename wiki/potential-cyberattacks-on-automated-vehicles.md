---
uid: 01a19d3c-afbc-7601-8961-06f96519fbf6
title: "Potential Cyberattacks on Automated Vehicles"
summary: "Petit and Shladover, IEEE T-ITS 2015. The standard reference taxonomy of attack vectors against autonomous and cooperative automated vehicles."
type: entity
category: "Research Papers"
url: "https://its.berkeley.edu/publications/potential-cyberattacks-automated-vehicles"
status: published
last_checked: 2026-11-17
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Petit and Shladover, IEEE T-ITS 2015. The standard reference taxonomy of attack vectors against autonomous and cooperative automated vehicles."
related:
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
  - sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion
  - over-the-air-compromise-of-modern-volkswagen-group-vehicles
  - pseudonym-schemes-in-vehicular-networks-a-survey
  - does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://its.berkeley.edu/publications/potential-cyberattacks-automated-vehicles"
    retrieved: 2026-11-17
facets: [attack, research]
---

Petit and Shladover, IEEE T-ITS 2015. The standard reference taxonomy of attack vectors against autonomous and cooperative automated vehicles.

## What it is

Jonathan Petit and Steven E. Shladover, *Potential Cyberattacks on Automated Vehicles*, IEEE Transactions on Intelligent Transportation Systems 16(2), April 2015, pp. 546–556, DOI 10.1109/TITS.2014.2342271. The paper is one of the earliest systematic treatments of security for automated driving, and an official abstract is hosted by UC Berkeley's Institute of Transportation Studies, where Shladover is affiliated.

## How it works

The authors frame the problem from the history of intelligent transportation systems. Vehicle automation has been a fundamental ITS application since ITS research began in the mid-1980s, but for most of that period it was treated as a futuristic concept. Announcements by car manufacturers of deployment by 2020 made it a near-term reality. In parallel, the industry focused on **connected vehicles** (US) or **cooperative ITS** (Europe): exchanging data between vehicles (V2V) and between vehicles and infrastructure (V2I/I2V) to supply the information ITS applications need.

Petit and Shladover observe that the threads of automation and cooperative ITS had not yet been thoroughly woven together, but that this would be a necessary step because cooperative data exchange would provide vital inputs to automation performance and safety. Their contribution is to start thinking about the cybersecurity implications of *cooperative* automated vehicle systems: they investigate attacks specific to automated vehicles, with their special needs and vulnerabilities, and analyse threats against both autonomous automated vehicles and cooperative automated vehicles. Two conclusions stand out in the abstract: the analysis shows a need for considerably more redundancy than many had expected, and the authors explicitly aim to raise awareness and generate discussion at an early stage of system development rather than after deployment.

## Where it fits

This is the foundational taxonomy that later sensor-attack work builds on. [Remote attacks on automated vehicles' sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) and the [SoK on perception attacks and multi-sensor fusion](sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion.md) are the modern empirical and systematised follow-ons. [Over the Air: compromise of modern Volkswagen Group vehicles](over-the-air-compromise-of-modern-volkswagen-group-vehicles.md) is the concrete remote-compromise case, and [pseudonym schemes in vehicular networks](pseudonym-schemes-in-vehicular-networks-a-survey.md) covers the identity machinery of the cooperative side. [Does physical adversarial example really matter to autonomous driving?](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md) asks the system-level impact question a decade later.

## Limits and safety notes

The full text is paywalled behind IEEE Xplore and no legitimate open copy was found when this page was checked; the earlier Research Papers campaign therefore deliberately left this entry at stub depth. This page is at full depth because the current campaign requires it, and it is based strictly on the **primary official abstract and citation** from Berkeley ITS, not on secondary summaries. That means it records the paper's framing and headline conclusions but cannot reproduce its specific attack taxonomy, threat model details or case studies. Those require access to the full text. No claim here goes beyond the abstract.

## Status and sources

Checked 2026-11-17. **Published** — IEEE T-ITS, April 2015; full text behind IEEE Xplore, official abstract open.

- [UC Berkeley ITS publication record and abstract](https://its.berkeley.edu/publications/potential-cyberattacks-automated-vehicles)
- [DOI record](https://doi.org/10.1109/TITS.2014.2342271)

## Related

- [Remote attacks on automated vehicles' sensors: experiments on camera and LiDAR](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md)
- [SoK: the next frontier in AV security — systematizing perception attacks and the emerging threat of multi-sensor fusion](sok-the-next-frontier-in-av-security-systematizing-perception-attacks-and-the-emerging-threat-of-multi-sensor-fusion.md)
- [Over the Air: Compromise of Modern Volkswagen Group Vehicles](over-the-air-compromise-of-modern-volkswagen-group-vehicles.md)
- [Pseudonym schemes in vehicular networks: a survey](pseudonym-schemes-in-vehicular-networks-a-survey.md)
- [Does physical adversarial example really matter to autonomous driving?](does-physical-adversarial-example-really-matter-to-autonomous-driving-towards-system-level-effect-of-adversarial-object-evasion-attack.md)
