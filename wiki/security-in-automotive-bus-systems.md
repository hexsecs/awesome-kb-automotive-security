---
title: "Security in Automotive Bus Systems"
summary: "Wolf, Weimerskirch, and Paar, Workshop on Embedded Security in Cars 2004. The first systematic treatment of CAN, LIN, MOST, and FlexRay as security…"
type: entity
category: "Research Papers"
url: "https://www.weimerskirch.org/files/WolfEtAl_SecureBus.pdf"
status: unknown
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Wolf, Weimerskirch, and Paar, Workshop on Embedded Security in Cars 2004. The first systematic treatment of CAN, LIN, MOST, and FlexRay as security problems, proposing the gateway and cryptographic measures later echoed in SecOC."
sources:
  - url: "https://www.weimerskirch.org/files/WolfEtAl_SecureBus.pdf"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - experimental-security-analysis-of-a-modern-automobile
  - comprehensive-experimental-analyses-of-automotive-attack-surfaces
  - can-injection
---

Wolf, Weimerskirch, and Paar, Workshop on Embedded Security in Cars 2004. The first systematic treatment of CAN, LIN, MOST, and FlexRay as security problems, proposing the gateway and cryptographic measures later echoed in SecOC.

## What it is

A study paper by Marko Wolf, André Weimerskirch, and Christof Paar, all at escrypt GmbH, Bochum, presented at the Workshop on Embedded Security in Cars (ESCAR) 2004. Not an experiment: it classifies the vehicle bus systems of its day, analyses their exposures, and proposes a secured communication architecture. No DOI exists (workshop paper); the canonical open source is the authors' PDF, read in full for this page.

## What it showed

**A five-group taxonomy of vehicle buses**, one representative each: sub-bus (LIN, 20 kbit/s), event-triggered (CAN, 1 Mbit/s), time-triggered (FlexRay, 10 Mbit/s), multimedia (MOST, up to 24 Mbit/s), and wireless (Bluetooth) — with a property table and per-bus exposure grading (LIN little, CAN **big**, FlexRay **acute**, MOST little, Bluetooth varied).

**An attacker model unusual for its date:** three groups — the car owner (generally low capability, full physical access), garage personnel (high capability, full physical access, assessed as the most dangerous group), and third parties (limited or no access). Motivations named include mileage manipulation, chip tuning, tachograph spoofing, privacy attacks, and targeted theft.

**The exposure analysis** is the paper's durable core. All bus communication is unencrypted plaintext; message formats sit in freely available documents; controllers cannot verify that a message comes from an authorized sender at all. The central structural claim: **interconnection is the major hazard** — via gateways, any controller on any bus can in principle reach any other, so a single compromised bus system endangers the whole vehicle communication network, and wireless interfaces plus multimedia buses carrying content from CDs, email, and attached computers make that reachability contactless. Unguarded diagnostic functions on gateways are called out explicitly.

**Feasible protocol-layer attacks per bus** (analysis, assuming physical or logical access): LIN — malicious sleep frames deactivate the subnet, bogus sync bytes break synchronization; CAN — priority-arbitration jamming by flooding top-priority messages, and forced disconnection of any controller by abusing the automatic fault-localization (error-flag) mechanism; FlexRay — bus-guardian abuse to deactivate controllers, attacks on the common time base, bogus sleep frames; MOST — timing-master frame attacks and channel-request jamming; Bluetooth — the then-known attack literature and the first Bluetooth worms.

**The countermeasure architecture (§4)** has three parts. *Controller authentication:* every controller holds a certificate (controller ID, public key, authorizations) signed by its OEM; the gateway verifies it against stored OEM public keys, enrols the controller on a valid-controller list, and returns a symmetric bus group key encrypted under the controller's public key. *Encrypted communication:* bus-internal broadcast traffic is encrypted under the shared, periodically updated group key (the gateway broadcasts per-controller-encrypted key updates); asymmetric cryptography is reserved for key distribution and authentication, with optional digital signatures for integrity and sender authentication. *Gateway firewalls:* forwarding rules based on the authorizations in controller certificates (or subnet-level rules for controllers that cannot sign); LIN and MOST controllers should generally be prevented from sending into CAN or FlexRay, and diagnostic functions should be completely disabled while driving. The worked example is a centralized "super gateway" holding every bus's group key and the valid-controller list in tamper-resistant protected memory — a TPM is suggested.

## Where it fits

The founding in-vehicle security paper in this section. Its CAN attack classes (priority jamming, fault-localization abuse) are the analytic ancestors of attacks later demonstrated experimentally — [Koscher et al. 2010](experimental-security-analysis-of-a-modern-automobile.md) is the empirical counterpart six years later, and the bus-off attack lineage descends from the error-handling observation. The authentication-plus-gateway-firewall design is the 2004 sketch of what AUTOSAR SecOC and gateway segmentation later standardized — the list summary's own framing, "later echoed in SecOC".

## Limits and safety notes

The attacks are feasibility analysis, not demonstrations: §3 states they are described assuming physical or logical access to the corresponding vehicle network, and nothing was run against a real vehicle. The §4 design is an example implementation in the architectural sense — a reference arrangement with no prototype build, no measurements, and no evaluation against the paper's own attack list. The specifics are dated (Bluetooth as the wireless frontier, MOST and FlexRay as the future); the durable content is the taxonomy, the interconnection argument, and the countermeasure shape.

## Status and sources

Status: **unknown** — a finished 2004 publication; no living artefact. Sources: the paper (open author copy, weimerskirch.org), read in full 2026-11-01; the list.

## Related

- [Experimental Security Analysis of a Modern Automobile](experimental-security-analysis-of-a-modern-automobile.md)
- [Comprehensive Experimental Analyses of Automotive Attack Surfaces](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md)
- [CAN injection](concepts/can-injection.md)
