---
title: "Comprehensive Experimental Analyses of Automotive Attack Surfaces"
summary: "Checkoway et al., USENIX Security 2011. Follow-up establishing the remote attack surface, compromising a vehicle over Bluetooth, cellular, and the CD player."
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenix-security-11/comprehensive-experimental-analyses-automotive-attack-surfaces"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Checkoway et al., USENIX Security 2011. Follow-up establishing the remote attack surface, compromising a vehicle over Bluetooth, cellular, and the CD player."
sources:
  - url: "https://www.usenix.org/conference/usenix-security-11/comprehensive-experimental-analyses-automotive-attack-surfaces"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - experimental-security-analysis-of-a-modern-automobile
  - security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study
  - relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars
  - can-injection
  - a-survey-of-remote-automotive-attack-surfaces
---

Checkoway et al., USENIX Security 2011. Follow-up establishing the remote attack surface, compromising a vehicle over Bluetooth, cellular, and the CD player.

## What it is

A systematic experimental study of compromising a car *without prior physical access*, by Stephen Checkoway, Damon McCoy, Brian Kantor, Danny Anderson, Hovav Shacham, and Stefan Savage (UC San Diego) with Karl Koscher, Alexei Czeskis, Franziska Roesner, and Tadayoshi Kohno (UW). 20th USENIX Security Symposium, San Francisco, August 2011. It is the direct follow-up to [Koscher et al. 2010](experimental-security-analysis-of-a-modern-automobile.md), which had assumed the attacker already had physical (OBD-II) access; this paper asks whether that assumption can be discharged, vector by vector. The target was a single anonymized "moderately priced late model sedan" (make and model deliberately unnamed), with two equivalent vehicles used to confirm the results were not instance artefacts. The load-bearing claim: for *every* vulnerability demonstrated, the team obtained complete control over the vehicle's systems — and because ECUs are bridged, compromising any one amplifies to the whole vehicle.

## What it showed

**CD firmware update (indirect physical).** An ISO 9660 CD containing a particularly named file triggers a cryptic prompt and reflashes the media player — *by default if the user does not press the appropriate button*. The paper's footnote is explicit: not the manufacturer's standard update method, "likely a vestigial capability in the supplier's code base" — the manufacturer was unaware of it.

**CD / WMA exploit (indirect physical).** A media-player file-read function assumes input lengths, and an undocumented aspect of the WMA format leads through its parser to a buffer overflow. The modified WMA file plays perfectly on a PC, but in the car sends **arbitrary CAN packets** of the attacker's choosing.

**PassThru diagnostic device (dealership).** The manufacturer's J2534 PassThru device — a Linux appliance that dealership guidelines recommend connecting over WiFi — advertises itself via UDP multicast on every network it joins. Client-to-device communication is unauthenticated, and a proprietary unauthenticated configuration API contains input-validation bugs giving shell command injection; the box also ships telnetd and ftpd, and a poor root password. The team built a program that contacts advertised devices, shell-injects them, and installs a malicious binary injecting pre-programmed CAN messages into any car the device later services — then turned it into a **worm** that spreads to other PassThru devices.

**Bluetooth (short-range wireless).** The telematics unit's hands-free implementation combines a popular embedded Bluetooth stack with custom interface code containing over 20 `strcpy` calls, none clearly safe; the investigated instance was an easily exploitable unchecked `strcpy`. Exploitation requires a paired device, via two routes: a Trojan app on a paired phone (demonstrated on Android), or direct pairing — sniff the car's Bluetooth MAC, then brute-force the pairing PIN. The car answers pairing requests with *no user interaction* and does not need to be in pairing mode; at 8–9 PINs per minute the average is ~10 hours per car (trials ranged from 15 minutes to 13.5 hours). The blind-paired device does not appear on the driver's paired-device list and cannot be unpaired manually.

**Cellular / telematics (long-range wireless).** The telematics unit uses Airbiquity's aqLink software modem over the cellular *voice* channel. Two compounding failures: a *gateway buffer overflow* — aqLink supports 1024-byte packets, but the glue code to the unit's Command program assumes packets never exceed ~100 bytes — and *authentication*: the "random" 3-byte challenge's RNG is re-initialized at every unit start with the same constant seed, so challenges after the car has been off are static (identical on both test cars) and an observed valid response can be replayed; and the response-checking code has a logic flaw under which, for roughly 1 in 256 challenges, carefully formatted *incorrect* responses are accepted — the bypass succeeds after ~128 calls on average. Realizations include a laptop modem that calls repeatedly until authenticated and delivers the overflow, and a *fully blind* version with the exploit audio encoded in a file on an iPod played into an office telephone while dialling the car.

**Post-compromise control.** Once inside, the team demonstrated TPMS triggers (including the TPMS ECU reflashed via CAN to recognize wireless trigger packets, building on [Rouf et al.](security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study.md)), an FM RDS trigger via the reflashed media player, cellular IRC command-and-control verified with two compromised cars over 1,000 miles apart responding to a single command, GPS-location exfiltration, and cabin-audio recording through the hands-free microphone. The theft scenario was implemented end-to-end: unlock, start, disengage the shift-lock, and spoof the startup protocol to bypass the immobilizer, after which an accomplice drove the car.

**Diagnosis.** The synthesis the field still quotes: virtually all of the vulnerabilities emerged *at interface boundaries between code written by distinct organizations* — glue code misunderstanding a delivered component's assumptions. The structural cause is the automotive outsourcing model: parts are spec'd as completed components, manufacturers frequently lack access to ECU source code, and same-function ECUs had different code bases from different suppliers across model years.

## Where it fits

Together with Koscher et al. 2010, this is the foundational remote-compromise result for the modern car: it moved the field from "an attacker with the OBD-II port owns the car" to "the car's own radios and media paths are the port" — the framing later work, including the 2015 Miller/Valasek Jeep study, inherits. For this KB it is also a justified link into the [CAN injection](concepts/can-injection.md) concept: the WMA payload's entire effect is to send arbitrary CAN packets from a compromised media player — injection onto the bus from an infotainment ECU, distinct from the diagnostic-port injection path.

## Limits and safety notes

Stated in the paper: one representative sedan; portability to other models and manufacturers is explicitly *not* evaluated. GPS was excluded as not currently a practical access vector. The Bluetooth PIN attack takes ~10 hours on average and requires the car running; the cellular bypass is harder when the car is off. Results were disclosed to industry and government stakeholders, and the paper states many of the specific vulnerabilities "have or will soon be addressed" — the concrete bugs are historical; the structural findings (unauthenticated service protocols, pairing without user presence, constant-seeded challenge RNGs, size assumptions at boundaries) are the durable content. The vehicle is anonymized; its make and model must not be guessed or named here.

## Status and sources

Status: **unknown** — a finished 2011 publication; no living artefact. No DOI is confirmed (USENIX papers of this era typically carry none). Full text openly available from USENIX and the authors' group site; read in full 2026-11-01.

## Related

- [Experimental Security Analysis of a Modern Automobile](experimental-security-analysis-of-a-modern-automobile.md)
- [Security and Privacy Vulnerabilities of In-Car Wireless Networks: A Tire Pressure Monitoring System Case Study](security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study.md)
- [Relay Attacks on Passive Keyless Entry and Start Systems in Modern Cars](relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars.md)
- [CAN injection](concepts/can-injection.md)
