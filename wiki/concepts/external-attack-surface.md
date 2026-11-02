---
title: "The vehicle's external attack surface: remote entry and the telematics pivot"
summary: "Compromise repeatedly begins at a boundary interface and pivots through the unit crossing it: connectivity units are most exposed and most privileged."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [comprehensive-experimental-analyses-of-automotive-attack-surfaces, remote-exploitation-of-an-unaltered-passenger-vehicle, experimental-security-analysis-of-a-modern-automobile, security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study, plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles, can-injection]
sources:
  - url: "https://www.usenix.org/legacy/events/sec11/tech/full_papers/Checkoway.pdf"
    retrieved: 2026-11-01
  - url: "https://illmatics.com/Remote%20Car%20Hacking.pdf"
    retrieved: 2026-11-01
---

Ask how the attacks in this KB *got in*, and a pattern repeats across fifteen years of papers: complete vehicle compromise begins at a boundary interface — a disc, a dealership tool, a radio, a modem — and pivots through the single unit that straddles the boundary between the outside world and the vehicle buses. The bus-side concepts ([CAN injection](can-injection.md) and its neighbours) begin their story once an attacker is *on* the bus; this page covers the step before: the external surface, organised by entry class, and the pivot pattern the full pages establish jointly — **the connectivity units are at once the most externally exposed components in the vehicle and the most internally privileged**, dual-homed by design, and historically the least hardened code in the car.

## Entry classes

**Indirect physical media.** Content the vehicle parses from objects: [Checkoway et al. 2011](../comprehensive-experimental-analyses-of-automotive-attack-surfaces.md) remains the systematic discharge of this class — a malicious audio file reaching the head unit through its media parser, a WMA crafted against the CD path — media as a code-delivery channel into a privileged parser (the [IVI runtime](ivi-runtime-privilege.md) family's intake).

**Service infrastructure.** The tools the vehicle's ecosystem trusts: Checkoway's dealership PassThru device — unauthenticated, wormable, and positioned to inject into *every car it later services* — is the class's purest instance: compromise the infrastructure once, inherit the fleet it touches. The [diagnostic-service abuse](diagnostic-service-abuse.md) page owns the services themselves; the entry point here is the trusted intermediary.

**Short-range wireless.** Bluetooth pairing obtained without user presence (Checkoway), TPMS reception and forgery at ~40 m ([Rouf 2010](../security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study.md) — the boundary crossed by *reception alone*, yielding tracking before any injection), BLE chargers and dongles. The class's shared property: proximity is the only gate, and proximity is cheap.

**Long-range cellular and telematics.** The pivot class proper. Koscher 2010's telematics module was dual-homed — cellular outside, both buses inside — a subnet bridge wearing a radio. [Miller & Valasek 2015](../remote-exploitation-of-an-unaltered-passenger-vehicle.md) is the completed arc: a carrier-reachable head unit, reflashed through its bridge chip, becomes the launch point for bus-side effects — the remote in "remote exploitation" is entirely this entry class plus the pivot. The attacker's distance collapses to zero at the moment the pivot unit falls, which is why these units' code quality carries fleet-level weight.

**Aftermarket, owner-installed devices.** The surface the owner adds themselves: [Plug-N-Pwned](../plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles.md)'s census of 77 wireless OBD-II dongles found every one exposing at least two of five vulnerability classes, bridging whatever network the dongle joins (Wi-Fi, Bluetooth, cellular) straight onto the diagnostic bus — with the DongleScope result that the *category*, not a vendor, is the problem. Insurance and fleet dongles arrive pre-trusted by the one person whose authorisation the vehicle cannot second-guess.

## Non-injection outcomes

The bus-side concepts measure success in actuation. The external surface's outcomes are broader, and the papers record them distinctly: **tracking** (TPMS IDs as persistent vehicle identifiers, readable by roadside receivers), **exfiltration** (the telematics and IVI units hold location history, contacts, credentials — Koscher's and Checkoway's units both yielded data stores), and **command-and-control residency** — a compromised connectivity unit is a persistent, powered, networked computer in the vehicle, usable as infrastructure (the PassThru worm's propagation logic is the fleet-scale version). A surface audit that prices only the injection outcome underprices every entry class above.

## The seam with the bus side

[CAN injection](can-injection.md) carries an Access paths section organising how attackers reach the bus; this page owns the boundary *before* the bus — the interfaces, the pivot units, the non-injection outcomes. Where a case needs both (the Jeep arc), the entry and pivot are here, the bus-side effects are there, and each page links the other's half rather than retelling it. The [IVI update channel](ivi-update-trust.md) is likewise a neighbouring special case: an entry class whose mechanism is trust in arriving code, owned by its own page.

This page synthesizes the KB's own full entity pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source.

## Related

- [Comprehensive Experimental Analyses of Automotive Attack Surfaces (Checkoway 2011)](../comprehensive-experimental-analyses-of-automotive-attack-surfaces.md) — the vector-by-vector discharge
- [Remote Exploitation of an Unaltered Passenger Vehicle](../remote-exploitation-of-an-unaltered-passenger-vehicle.md) — the completed telematics pivot
- [Experimental Security Analysis of a Modern Automobile](../experimental-security-analysis-of-a-modern-automobile.md) — the dual-homed telematics bridge
- [Plug-N-Pwned](../plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles.md) — the owner-installed entry class, measured as a category
- [CAN injection](can-injection.md) — the bus side of the seam
