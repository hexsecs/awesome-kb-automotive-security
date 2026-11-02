---
title: "Adventures in Automotive Networks and Control Units"
summary: "Miller and Valasek, 2013. The wired precursor to the Jeep work, documenting CAN injection against the Toyota Prius and Ford Escape and the methodology that…"
type: entity
category: "Research Papers"
url: "https://illmatics.com/car_hacking.pdf"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Miller and Valasek, 2013. The wired precursor to the Jeep work, documenting CAN injection against the Toyota Prius and Ford Escape and the methodology that followed."
sources:
  - url: "https://illmatics.com/car_hacking.pdf"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - remote-exploitation-of-an-unaltered-passenger-vehicle
  - can-injection
  - experimental-security-analysis-of-a-modern-automobile
  - comprehensive-experimental-analyses-of-automotive-attack-surfaces
---

Miller and Valasek, 2013. The wired precursor to the Jeep work, documenting CAN injection against the Toyota Prius and Ford Escape and the methodology that followed.

## What it is

A 101-page technical white paper by Charlie Miller and Chris Valasek, released in July 2013 as the companion document to their DEF CON 21 presentation (the paper itself states no venue and no institutional affiliations; the venue comes from the talk record). It is a white paper, not a peer-reviewed publication, and carries no DOI. Its stated aim is twofold: to answer the question the UW/UCSD studies of 2010–2011 ([Koscher](experimental-security-analysis-of-a-modern-automobile.md), [Checkoway](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md)) had left open — those studies showed an attacker could get code running on a car's ECUs but documented little of what such an attacker could then *do*, released no tools, and did not name the vehicles studied — and to lower the field's barrier to entry by releasing everything needed to reproduce the work: source code, hardware description, and message catalogues. The toolkit is EcomCat with its ecomcat_api library and PyEcom wrapper, built around an ECOM cable connected to the car's OBD-II port. The threat model is stated plainly and is the paper's central scoping decision: it assumes an attacker who can already send CAN messages — via physical access, or via code running on an ECU through some other interface. The paper does not itself demonstrate remote entry; it documents what becomes possible after it.

## What it showed

**The vehicles — named, on purpose.** A **2010 Ford Escape** with Active Park Assist and a **2010 Toyota Prius** with Intelligent Parking Assist, Lane Keep Assist, and the Pre-Collision System (PCS). The paper documents each car's bus topology and ECU inventory, with appendices giving diagnostic ECU maps and per-CAN-ID data layouts.

**Normal-packet attacks.** On the Escape: display control (arbitrary speedometer and odometer readings, false wheel data to navigation), and a complete bus denial of service by flooding with CAN ID 0000 — the highest arbitration priority, so nothing else transmits; the power steering module shuts down, and flooding before start prevents starting at all. Steering comes from the Parking Aid Module (PAM): recording a real auto-park manoeuvre and replaying its gradually-varying angle sequence steered the wheel to any position — with the paper's caveat that above roughly 5 mph the steering module ignores these packets. On the Prius: the PCS braking packet, sent continuously with its counter incremented as the real ECU would, slows or completely stops the car and defeats the accelerator even fully depressed, at any time. Steering at speed required forging the gear-state packet and flooding bogus speed packets, and yielded only "forceful, sporadic jerks" — vehicle instability, not control; the Lane Keep Assist packet works while driving but is capped at about 5 degrees from centre. Acceleration is the weakest result and the paper says so: the relevant packet is not visible at the OBD-II port (the authors spliced into the bus at the source ECU), and it produced acceleration for only a few seconds.

**Diagnostic attacks.** On the Escape, SecurityAccess failed two ways: the PAM always returns the same seed — the constant 11 22 33 — because its firmware randomizes the challenge and then overwrites it with the constant in both the stored copy and the send buffer, which the authors read as leftover debugging code; and for the other ECUs, the keys live in the dealer tool — reversing Ford's Integrated Diagnostic Software recovered the seed/key algorithm and an array of 407 keys to try. With authentication: a proprietary command engages the brakes and locks the car in position; another bleeds the brakes, during which the pedal cannot be depressed (works below ~5 mph; the paper records it "caused me to crash into the back of my garage once"); a shutdown command kills the Smart Junction Box — headlights, interior lights, radio, HVAC, and the brake lights; and a RoutineControl kills the engine at any speed with no diagnostic session at all. On the Prius, most diagnostic functions need no SecurityAccess at all, and the dealer "active tests" are directly usable — including the Pre-Collision System's seat-belt pre-tensioner motors, flagged precisely because there are no restrictions on when the tests can be issued. Where SecurityAccess is required, Toyota's key algorithm fell to reversing the Calibration Update Wizard: the key is the seed with its middle bytes XORed with a per-ECU secret, and the paper publishes the secrets it recovered.

**From packets to code execution.** The deepest result: on the Escape, the diagnostic download path is itself an execution path. Uploaded data beginning with a magic header is called as code via a RoutineControl, giving arbitrary code execution on the PAM that can read and write CAN — the foothold pattern the authors' later remote work builds on. The paper closes with a detection proposal grounded in its own data: normal driving produced zero diagnostic packets in 22 minutes, while attacks replay traffic at 10–20× natural rates — frequency anomaly detection would catch this class.

## Where it fits

The methodological bridge between the anonymized academic studies and the 2015 Jeep work: same authors, same move from "packets that influence" to "code that persists", and the first study to name its vehicles and publish its tooling — the reproducibility stance the field adopted after it. Its injection results are primary evidence for the KB's [CAN injection](concepts/can-injection.md) concept page, and the [2015 paper](remote-exploitation-of-an-unaltered-passenger-vehicle.md) is its direct continuation, discharging this paper's assumed entry condition over the cellular network.

## Limits and safety notes

Stated in the paper: entry is assumed, not solved — every result presupposes the ability to send CAN messages. Toyota acceleration is partial and unreliable in the authors' own assessment; steering at speed on the Prius is instability, not control; the authors had not obtained firmware from the Prius engine computer at publication. Two 2010 vehicles of two models carry all the concrete results; the paper argues the substrate (unauthenticated broadcast CAN, dealer-tool key custody) is industry-wide, but does not test that claim on other cars.

## Status and sources

Status: **unknown** — a finished 2013 white paper; the released tools were research artefacts, not a maintained project. No DOI. Full text openly available (illmatics.com); read in full 2026-11-01.

## Related

- [Remote Exploitation of an Unaltered Passenger Vehicle](remote-exploitation-of-an-unaltered-passenger-vehicle.md)
- [CAN injection](concepts/can-injection.md)
- [Experimental Security Analysis of a Modern Automobile](experimental-security-analysis-of-a-modern-automobile.md)
- [Comprehensive Experimental Analyses of Automotive Attack Surfaces](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md)
