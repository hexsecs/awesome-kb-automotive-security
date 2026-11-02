---
title: "Security and Privacy Vulnerabilities of In-Car Wireless Networks: A Tire Pressure Monitoring System Case Study"
summary: "Rouf et al., USENIX Security 2010. Shows TPMS sensors are unauthenticated and trackable at roughly 40m, the first published wireless in-car network attack."
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity10/security-and-privacy-vulnerabilities-car-wireless-networks-tire-pressure"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Rouf et al., USENIX Security 2010. Shows TPMS sensors are unauthenticated and trackable at roughly 40m, the first published wireless in-car network attack."
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity10/security-and-privacy-vulnerabilities-car-wireless-networks-tire-pressure"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - comprehensive-experimental-analyses-of-automotive-attack-surfaces
  - experimental-security-analysis-of-a-modern-automobile
  - relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars
---

Rouf et al., USENIX Security 2010. Shows TPMS sensors are unauthenticated and trackable at roughly 40m, the first published wireless in-car network attack.

## What it is

A security and privacy analysis of tire pressure monitoring systems (TPMS) — the first published attack on a wireless in-car network — by Ishtiaq Rouf, Rob Miller, Hossen Mustafa, Travis Taylor, Sangho Oh, and Wenyuan Xu (University of South Carolina) with Marco Gruteser, Wade Trappe, and Ivan Seskar (WINLAB, Rutgers). 19th USENIX Security Symposium, Washington, DC, August 2010. TPMS had just become mandatory equipment in the US, with sensors required to report every 60–90 seconds — a wireless network, present in every new car, whose messages cross the vehicle's boundary. The team reverse-engineered two commercial sensor systems, anonymized in the paper as TPS-A (ASK modulation) and TPS-B (an ASK/FSK hybrid), described only as used in automobiles with high market shares in the US — anonymized, the paper says, to prevent misuse.

## What it showed

**Reverse engineering.** Using GNU Radio with a USRP and an ATEQ VT55 trigger tool — about $1,500 of openly available equipment in total — the team recovered the over-the-air format: differential Manchester encoding at roughly 5 kBd, and packets carrying a preamble, the sensor ID, pressure, temperature, status flags, and a CRC checksum (the CRC polynomials were brute-forced). Sensor IDs are 28-bit or 32-bit depending on type and are immutable for the sensor's lifetime. The reverse-engineering effort itself was small: a few days for a PhD-level engineer, several weeks for a master's student with no prior reverse-engineering or GNU Radio experience.

**Eavesdropping and tracking.** Sensor transmissions could be received at about 10.7 m without a low-noise amplifier — the car body attenuates the signal only slightly from broadside — and at 40 m with a basic LNA. Both sensor types transmit periodically even when the car is stationary, and one transmits even when the car is not running. A live decoder was tested on interstate I-26, decoding two cars driving in parallel at over 110 km/h. Because the ID is fixed and broadcast in the clear, a roadside listener can recognize a car across encounters; the paper's angle study recommends placing a sniffer 2.5 m from the lane markings for a ~99% probability of reading the sensor ID. Set against automatic number-plate recognition, TPMS tracking needs no line of sight and reads IDs more reliably (~99% vs ~90% for plates under ideal conditions). The paper is equally explicit about *blanket* passive tracking: covering a road so that a car at 60 km/h is guaranteed a capture would take 110 sniffers, which it calls cost-prohibitive — the practical attack is targeted or chokepoint tracking.

**Active tracking.** Sensors can be triggered on demand by a 125 kHz activation signal; the team demonstrated activating a targeted sensor and extracting its ID from a car moving at 35 km/h using the ATEQ VT55, a workshop tool whose own trigger range is deliberately only 0.5 m.

**Spoofing.** The system has no authentication at all: the ECU filters incoming packets by known sensor ID and otherwise accepts everything. The alert bit alone illuminates the low-pressure warning light even when the rest of the same message reports a normal 32 PSI — the ECU does not check the warning flag against the pressure value. Forged packets injected at 40 packets/sec raised no rate anomaly. Spoofing worked *between moving cars*: on I-26 the low-pressure warning was triggered at 55 km/h and the central warning light at 110 km/h. The ECU's filtering logic, mapped experimentally: a single spoofed packet does not light the warning, but it makes the ECU emit activation signals that cause the addressed sensor to transmit eight packets — a battery-drain vector against the sensor; four spoofed packets within one second, spaced at least 225 ms apart, do illuminate the low-pressure light.

**ECU crash.** After only two days of sporadic spoofing experiments, the team crashed the TPMS ECU completely — a "Check TPMS System" light and no pressure readings at all. The failure survived good packets, ignition restarts, hours of highway driving, and disconnecting the car battery; the dealership recovered the car only by replacing the TPMS ECU. The authors state they stopped further exploration of the ECU's logic due to the prohibitive cost of repairing it.

**Defences proposed:** consistency checks and input validation on the ECU (cross-checking values against warning flags, majority logic over sensor responses); encryption plus a sequence number for freshness and a MAC applied before the CRC, with keys provisioned at the factory, dealership, or certified garage; and one-way hash-chain sequencing to authenticate the activation signals themselves.

## Where it fits

This paper opened the wireless side of automotive security: [Koscher et al. 2010](experimental-security-analysis-of-a-modern-automobile.md) had shown what an attacker with bus access could do; Rouf et al. showed a vehicle's wireless interfaces could be read and forged from *outside* the car, with commodity radio equipment, before any physical access. [Checkoway et al. 2011](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md) cite it directly and build on its TPMS work — including reflashing the TPMS ECU as a trigger channel — and its accidental ECU crash is an early, concrete instance of an automotive ECU failing unsafe under malformed input rather than rejecting it.

## Limits and safety notes

Stated in the paper: the two sensor systems are anonymized and the results are demonstrated on those systems; the tracking mathematics assumes a uniform ID distribution, which the paper itself flags as unrealistic. The demonstrated ranges are with the team's low-cost antennas; the authors note amplifiers and high-gain antennas would extend them, so the numbers are a floor, not a ceiling. Blanket passive tracking is analysed and found cost-prohibitive at 2010 equipment assumptions. ECU-logic exploration was cut short by the cost of the ECU the spoofing destroyed — the filtering model above is what was mapped before that point. The durable content is the design lesson: no authentication, no consistency checking, fail-unsafe ECU behaviour.

## Status and sources

Status: **unknown** — a finished 2010 publication; no living artefact. Bibliographic note: no DOI is confirmed for this paper — the ACM Digital Library identifier string (10.5555/…) is an internal identifier, not a registered DOI, and is not printed as one. Full text openly available from USENIX and author mirrors; read in full 2026-11-01.

## Related

- [Comprehensive Experimental Analyses of Automotive Attack Surfaces](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md)
- [Experimental Security Analysis of a Modern Automobile](experimental-security-analysis-of-a-modern-automobile.md)
- [Relay Attacks on Passive Keyless Entry and Start Systems in Modern Cars](relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars.md)
