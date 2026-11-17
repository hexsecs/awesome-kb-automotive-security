---
uid: 01a1b02c-9902-73c3-817b-bf87ba4a9bed
title: "Research Only? Understanding the Scope of Automotive Cyberattacks in the Wild"
summary: "Savage, USENIX VehicleSec 2026 keynote. Asks why fifteen years of remote-takeover demonstrations have not been matched by attacks in the wild, and what…"
type: entity
category: "Conference Presentations"
url: "https://www.usenix.org/conference/vehiclesec26/presentation/keynote-savage"
status: published
last_checked: 2026-11-17
created: 2026-11-06
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: a25e33d
list_summary: "Savage, USENIX VehicleSec 2026 keynote. Asks why fifteen years of remote-takeover demonstrations have not been matched by attacks in the wild, and what would change that."
related:
  - ble-theft-auto-evaluating-the-security-of-aftermarket-ble-based-automotive-remote-control-systems
  - remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar
  - sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it
  - fast-and-vulnerable-a-story-of-telematic-failures
  - canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks
  - automotive-security-timeline
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-06
  - url: "https://www.usenix.org/conference/vehiclesec26/presentation/keynote-savage"
    retrieved: 2026-11-17
---

Savage, USENIX VehicleSec 2026 keynote. Asks why fifteen years of remote-takeover demonstrations have not been matched by attacks in the wild, and what would change that.

## What it is

The keynote at the 4th USENIX Symposium on Vehicle Security and Privacy (VehicleSec 26), Baltimore, August 2026, by **Stefan Savage** of UC San Diego, where he is Professor of Computer Science and Engineering and holds the Irwin and Joan Jacobs Chair. His research sits at the intersection of distributed systems, networking and computer security, with a focus on embedded security and the economics of cybercrime; he received the ACM Prize in Computing in 2015 and a MacArthur Fellowship in 2017. The talk is a field-level reflection on why the academic record of automotive insecurity has not translated into observed attacks.

## How it works

Savage starts from a documented contradiction. Over the previous **fifteen years**, a steady stream of research results identified significant cybersecurity issues across automotive systems, including multiple **remote takeover demonstrations on stock passenger vehicles** with adversarial control of drivetrain, brakes and steering. Yet, despite those results, there is **little evidence of similar attacks "in the wild"**.

The keynote's project is to explain that gap rather than to catalogue more bugs. It examines what makes cyberattacks attractive in some domains and not in others, and how that attacker doctrine manifests specifically in the automotive context. It then highlights the role that real-world adversarial "hacking" plays in the current automotive ecosystem, and discusses what kinds of scenarios might change today's status quo. In short, the argument is about **attacker economics and incentives**, not about whether the technical vulnerabilities are real — the remote takeovers are real, but the payoff structures that drive criminal hacking elsewhere have not, so far, made cars a comparable target.

## Where it fits

This keynote is the framing piece for the whole applied-automotive-security corpus. [BLE Theft Auto](ble-theft-auto-evaluating-the-security-of-aftermarket-ble-based-automotive-remote-control-systems.md) is a concrete example of a large population of vulnerable vehicles, and [Fast and vulnerable: a story of telematic failures](fast-and-vulnerable-a-story-of-telematic-failures.md) shows the OEM-side equivalent. [SoK: stealing cars since remote keyless entry](sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it.md) covers the theft-economics case where a criminal incentive does exist, while [remote attacks on automated vehicles' sensors](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md) and [CANflict](canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks.md) are examples of the research demonstrations the keynote is accounting for. [Automotive Security Timeline](automotive-security-timeline.md) supplies the chronological backdrop.

## Limits and safety notes

This page is based on the **official USENIX abstract and speaker biography**, not on a paper or full transcript: the specific economic arguments and the "scenarios that might change today's status quo" are developed in the talk itself and are not reproduced here. "Little evidence in the wild" is the speaker's characterisation of the public record, not proof that no such attacks have occurred; absence of published evidence is a weak claim. The keynote was delivered in 2026, and the economics it describes can change as vehicle connectivity, fleets and attack monetisation evolve. No technical claims about any specific vehicle are made on this page.

## Status and sources

Checked 2026-11-17. **Published** — VehicleSec 26 keynote, August 2026; official abstract and bio on the USENIX conference page.

- [USENIX VehicleSec 26 keynote page](https://www.usenix.org/conference/vehiclesec26/presentation/keynote-savage)

## Related

- [BLE Theft Auto: Evaluating the Security of Aftermarket BLE-based Automotive Remote Control Systems](ble-theft-auto-evaluating-the-security-of-aftermarket-ble-based-automotive-remote-control-systems.md)
- [Remote attacks on automated vehicles' sensors: experiments on camera and LiDAR](remote-attacks-on-automated-vehicles-sensors-experiments-on-camera-and-lidar.md)
- [SoK: stealing cars since remote keyless entry introduction and how to defend from it](sok-stealing-cars-since-remote-keyless-entry-introduction-and-how-to-defend-from-it.md)
- [Fast and vulnerable: a story of telematic failures](fast-and-vulnerable-a-story-of-telematic-failures.md)
- [CANflict: exploiting peripheral conflicts for data-link layer attacks on automotive networks](canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks.md)
- [Automotive Security Timeline](automotive-security-timeline.md)
