---
title: "CANvas: Fast and Inexpensive Automotive Network Mapping"
summary: "Kulandaivel, Goyal, Agrawal, and Sekar, USENIX Security 2019. Builds an nmap for the vehicle, recovering the sender and receiver map of a CAN network in…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/usenixsecurity19/presentation/kulandaivel"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Kulandaivel, Goyal, Agrawal, and Sekar, USENIX Security 2019. Builds an nmap for the vehicle, recovering the sender and receiver map of a CAN network in under an hour using clock offsets and forced ECU isolation."
sources:
  - url: "https://www.usenix.org/system/files/sec19-kulandaivel.pdf"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - fingerprinting-electronic-control-units-for-vehicle-intrusion-detection
  - error-handling-of-in-vehicle-networks-makes-them-vulnerable
  - viden-attacker-identification-on-in-vehicle-networks
  - canalyzat0r
  - can-utils
  - can-injection
---

Kulandaivel, Goyal, Agrawal, and Sekar, USENIX Security 2019. Builds an nmap for the vehicle, recovering the sender and receiver map of a CAN network in under an hour using clock offsets and forced ECU isolation.

## What it is

Sekar Kulandaivel, Tushar Goyal, Arnav Kumar Agrawal, and Vyas Sekar, Carnegie Mellon University. *28th USENIX Security Symposium* (USENIX Security '19), Santa Clara, CA, August 14–16, 2019, pp. 389–405. CANvas is a network mapper for in-vehicle CAN — the nmap analogue the authors argue automotive security lacks. A CAN frame names its contents, not its sender, and the bus is broadcast, so neither end of a communication channel is observable from traffic alone. CANvas recovers a mapper's three outputs — each ID's transmitting ECU, each ID's set of receiving ECUs, and the enumeration of active ECUs — in under an hour, for under $100 of hardware (an Arduino Due plus a TI VP232 transceiver), connected only at the OBD-II port and without disassembling the vehicle. Its scenarios are defensive: discovering a malicious or aftermarket ECU, attesting configuration over time, finding lenient receive filters. Code and data were released open-source.

## What it showed

**Source mapping — and why the obvious primitive fails.** The starting point is Cho & Shin's clock-skew fingerprinting (this KB's CIDS page): ECUs have distinct quartz clocks, so IDs from one ECU should share a skew. The paper's first result is negative — the skew the published estimators compute is *period-dependent*. Two IDs from one ECU at different periods (their worked example: 0x262, 0x4C8, 0x521 from a power-steering ECU) yield three different "skews" and are misread as three ECUs; batch-size corrections (Sagong et al.) do not repair it, because the quantity computed is effectively an offset, corrupted by period jitter (scheduling, queuing, arbitration). CANvas instead tracks the *relative offset between a pair of IDs*, sampled at the pair's hyper-period (the least common multiple of their periods): if both IDs share one transmitter clock, that offset stays constant (implementation threshold: standard deviation under 1 ms); if not, it drifts. Matching pairs are grouped transitively into ECUs. Pairs whose hyper-period runs to minutes are skipped and resolved through a third ID; IDs with period deviation over 8% are excluded from direct comparison; missed deadlines (inter-arrival 2p instead of p) are interpolated. Thirty minutes of logged traffic suffices. On both ground-truthed vehicles the source map had a **0% false-positive rate**; the Prius's 59 unique IDs resolved into 102 matching pairs and nine transmitter groups, and ≈95% of IDs were attributed overall.

**Destination mapping — bus-off as a tool, rebuilt below the controller.** "Destination" is defined at the CAN-controller level: an ECU that correctly receives a message sets the ACK bit, but with many ECUs active an ACK names nobody. CANvas therefore isolates one ECU at a time — forcing all the others into bus-off — then injects every observed ID and watches for ACKs, detected transmitter-side: an unacknowledged message is retransmitted continuously, so a repeating stream means "not received" — no logic analyser needed. Cho & Shin's bus-off attack works at message level — win arbitration against the victim with a corrupted twin frame — but its injection-count formula assumes period jitter of 0.025 ms; the authors measured ≥0.15 ms on real vehicles, where the attack needs 6–8 precisely timed injections per error while each successful victim transmission decrements the counter being raised. CANvas bypasses the CAN controller entirely: it taps the digital line between its own controller and transceiver, reads each frame's ID in real time, and drives dominant bits into the data field of the target ID's frames — a guaranteed bit error on every occurrence, +8 on the victim's transmit error counter each time, until it crosses into bus-off (>255). Attacking each ECU's shortest-period ID (every real ECU encountered had one under 100 ms) keeps it fast; a full map costs n(n−1) bus-offs. Two production behaviours had to be engineered around: ECUs that auto-recover from bus-off after seconds (re-isolate mid-run), and one recovering after the standard 128×11 recessive bits (hold the bus "busy" with false messages). The isolation was 100% reliable in their tests.

**Two findings on real cars.** (1) Mapping a 2009 Toyota Prius found **nine** transmitters where eight were expected. IDs 0x570–0x572 came from an ECU installed years earlier as part of an aftermarket plug-in battery conversion — the mapper's malicious-ECU scenario, in the authors' own test car, confirmed by physically disconnecting all eight known ECUs (traffic persisted) and by comparison against a same-generation Prius. (2) On the Prius and on a 2017 Ford Focus — ground truth for both obtained by disassembly, guided by paid Toyota/Ford service manuals — **no ECU on either car filtered received messages at the controller level**: every isolated ECU acknowledged every injected ID. The paper's framing: compromising any ECU that merely *receives* a safety-critical ECU's messages already gives the reception precondition for a bus-off shutdown of it — their example is the Focus's infotainment unit receiving transmission-ECU traffic. Source mapping also ran on three further vehicles (2008 Ford Escape, 2010 Toyota Prius, Ford Fiesta — see Limits), and forced isolation was demonstrated on three extracted Ford engine ECUs (2012 Focus, 2013/2014 Escape) sharing an ID set that suggests a common controller configuration.

## Where it fits

CANvas sits between this KB's two Cho & Shin pages and converts both into measurement infrastructure. From [CIDS](fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md) it takes the clock-fingerprint observation and shows why the published estimators fail as a *mapping* primitive: they detect change against a known baseline rather than clustering unknown senders. From the [bus-off paper](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md) it takes the error-handling mechanism and shows why the message-level attack is too fragile against real jitter to serve as a tool, rebuilding it below the CAN controller as a dependable isolation step. Against the CAN Bus Analysis tooling pages — [CANalyzat0r](canalyzat0r.md), [can-utils](can-utils.md) — which support the manual capture-and-infer workflow, CANvas automates the structural half of reverse engineering — who transmits and who receives — before anyone asks what payloads mean. It maps topology, not semantics. For the [CAN injection](concepts/can-injection.md) concept it supplies the empirical complement: CANvas's lenient-filter result states that on the cars tested *reception* — the precondition for injection's follow-on attacks — is effectively universal, so segmentation arguments cannot rest on assumed controller filters. [VIDEN](viden-attacker-identification-on-in-vehicle-networks.md) is the other physical-fingerprint answer to source identification (voltage, not clocks); CANvas needs only a timestamped log, at the price of the periodicity assumptions in Limits.

## Limits and safety notes

As the paper states them: **Periodic, well-behaved traffic only.** Source mapping needs periodic IDs; pairs are dropped when period deviation exceeds 8% of the period or hyper-periods grow to minutes, so roughly 5% of IDs go unattributed, and a purely event-driven ECU is invisible as a transmitter (a non-transmitting ECU can still be detected during destination mapping). **Countermeasure-free vehicles are assumed:** no ECU deliberately altering its timing, no IDS preventing suspension. An attacker transmitting *during* capture under a spoofed ID breaks source analysis (the paper leaves that case to IDSs). **Destination means correctly received, not accepted:** application-level acceptance filtering is finer-grained and vendor-specific (an overload-frame technique is sketched, not evaluated). **Destination mapping is intrusive by design:** it bus-offs ECUs, drives the car into error states (warning lights, possible limp-home behaviour), and needs up to one ignition cycle per ECU. The authors report all test cars returned to normal with no stored codes after power-cycling — occasionally plus a short drive or a scan-tool reset; that is their result for their procedure on their cars, not a guarantee for arbitrary vehicles. Full ground truth covers two vehicles. One internal inconsistency in the paper itself: the introduction lists a **2013** Ford Fiesta among the five vehicles, §7.4 a **'15** Fiesta; flagged here rather than resolved.

## Status and sources

Status: **unknown** — a finished 2019 publication; the mapper was a research artefact, released open-source (github.com/sekarkulandaivel/canvas, as cited in the paper); no maintenance claim is made for it here. **DOI: none** — USENIX does not assign DOIs to its proceedings papers; no aggregator identifier is substituted (verified by Crossref query, 2026-11-01). Full text open at USENIX; read in full 2026-11-01.

## Related

- [Fingerprinting Electronic Control Units for Vehicle Intrusion Detection](fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md) — CIDS; the clock-skew primitive CANvas replaces for mapping
- [Error Handling of In-Vehicle Networks Makes Them Vulnerable](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md) — the bus-off attack CANvas rebuilds as its isolation step
- [VIDEN: Attacker Identification on In-Vehicle Networks](viden-attacker-identification-on-in-vehicle-networks.md) — voltage-domain counterpart for transmitter identification
- [CANalyzat0r](canalyzat0r.md) and [can-utils](can-utils.md) — the manual workflow CANvas precedes
- [CAN injection](concepts/can-injection.md) — the concept whose reception precondition CANvas measures
