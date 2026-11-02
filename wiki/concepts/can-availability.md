---
title: "CAN availability and denial of service"
summary: "Availability attacks remove or suppress the bus's genuine traffic, below the layer message authentication defends: flooding, bus-off, dominance, silencing."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [can-injection, sok-kicking-can-down-the-road-systematizing-can-security-knowledge, experimental-security-analysis-of-a-modern-automobile, adventures-in-automotive-networks-and-control-units, error-handling-of-in-vehicle-networks-makes-them-vulnerable, exposing-new-vulnerabilities-of-error-handling-mechanism-in-can, canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks, silently-disabling-ecus-and-enabling-blind-attacks-on-the-can-bus, diagnostic-service-abuse, canter, in-vehicle-intrusion-detection, can-message-authentication]
sources:
  - url: "https://www.usenix.org/legacy/events/sec10/tech/full_papers/Koscher.pdf"
    retrieved: 2026-11-01
  - url: "https://arxiv.org/abs/2510.02960"
    retrieved: 2026-11-01
---

Most CAN attacks in this KB forge: they add messages the bus never sent. Availability attacks do the opposite — they *remove* messages, or the ECUs that send them, or the receivers' ability to hear anything else. The [Kicking CAN SoK](../sok-kicking-can-down-the-road-systematizing-can-security-knowledge.md) grades availability the most exposed security element on the bus across its 150-paper corpus, ahead of integrity and confidentiality. This page organises the mechanisms the KB's full pages document, because they share one structural fact: they operate at or below the arbitration and error-handling layers, where the bus's best-known defences — message authentication — do not reach.

## Priority-arbitration flooding

CAN arbitration is a priority contest the lowest identifier always wins, with no fairness and no rate limit. Flooding the bus with ID 0x000 frames therefore starves every legitimate transmitter indefinitely. [Miller & Valasek 2013](../adventures-in-automotive-networks-and-control-units.md) demonstrated the complete version: a continuous ID-0000 flood is a total bus denial of service — the power-steering module shut down under it, and flooding before start prevented the car starting at all. Wolf 2004's analysis (on its KB page) already named the mechanism in the protocol's first security survey generation: arbitration priority is a designed-in availability asymmetry, not a bug — any node, including a compromised legitimate one, can hold the bus.

## Fault-confinement abuse: bus-off

CAN's error handling maintains per-node error counters; a node whose transmit error counter crosses the threshold is forced bus-off — disconnected by its own controller, for safety. The [bus-off attack](../error-handling-of-in-vehicle-networks-makes-them-vulnerable.md) (Cho & Shin, CCS 2016) turns that safety mechanism into a weapon: an attacker who can observe a victim ECU's transmissions and inject precisely timed errors drives the *victim's* counter up until the controller removes it — a healthy, uncompromised ECU silenced by its own fault confinement, presenting afterwards as a hardware fault rather than an attack. The 2022 successor ([Rogers & Rasmussen](../silently-disabling-ecus-and-enabling-blind-attacks-on-the-can-bus.md)) removes the attack's last timing constraint by interrupting error frames, and is carried on its page as analysis rather than demonstration. [CANOX](../exposing-new-vulnerabilities-of-error-handling-mechanism-in-can.md) (Serag et al., USENIX Security 2021) systematised the underlying surface — CAN's error handling itself — and [CANflict](../canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks.md) reaches the same layer through peripheral pin conflicts. The [CANvas](../canvas-fast-and-inexpensive-automotive-network-mapping.md) work showed the primitive from the defender's side of the bench: forced bus-off is also how a mapping tool isolates one ECU at a time.

## Physical-layer dominance

Below arbitration sits the wire itself. [Koscher 2010](../experimental-security-analysis-of-a-modern-automobile.md) documented physical-layer dominance: a node that drives the bus dominant continuously prevents all communication regardless of identifiers or error counters — the availability attack with no protocol surface at all. It needs sustained electrical access rather than a software foothold, which is why it appears less often in the remote-attack literature, but it bounds the class: no protocol redesign that keeps CAN's wired-AND medium answers it.

## Suppression of the genuine sender

The fourth mechanism removes one chosen voice rather than the whole bus. Diagnostic silencing — entering a session that mutes a genuine ECU, then optionally transmitting in its name — is covered on the [diagnostic-service abuse](diagnostic-service-abuse.md) page; its availability half belongs here: Koscher's silencing results (a muted ECM freezes the speedometer at 0; a muted BCM prevents restart) are denial of service against a single function, delivered by a legitimate service. The Ethernet generation has the same shape: SOME/IP service discovery's withdrawal is an ordinary Offer with TTL 0 and no proof of ownership, so a forged Stop Offer deletes subscriptions on both sides in one packet — the [SOME/IP](someip.md) page's one-packet kill, an availability attack by protocol courtesy rather than by force.

## Why authentication cannot answer these

The KB's authentication line — [vatiCAN](../vatican-vetted-authenticated-can-bus.md), LeiA, SecOC, and the [CAN message authentication](can-message-authentication.md) line — verifies that a received frame is genuine. Every mechanism above defeats the *channel*, not the message: a flooded bus delivers no frames to authenticate; a bus-off victim sends none; a dominated wire carries none; a silenced ECU's absence is not a forgery. Authentication and availability are orthogonal defences, and a deployment that buys only the first has not priced the second. The Kicking CAN SoK's transferability analysis sharpens this: CAN FD inherits the availability exposure wholesale, and even its hypothetical ideal bus leaves availability attacks standing, because they exploit access and arbitration rather than any fixable coding flaw.

## What answers exist in the corpus

Detection, not prevention, is the honest summary. [CANter](../canter.md) applies the bus-off paper's own detection rules (its F1/F2 line of work) as a countermeasure monitor; the Jeep's production conflict detection incidentally caught attack traffic in Miller & Valasek 2015's account. Rate and priority anomaly detection appears in the IDS concept's territory. Nothing in the KB's corpus *prevents* a flooding or dominance attack from a node already on the bus — the mitigations are segmentation (keeping untrusted nodes off safety buses), gateway filtering, and detection fast enough to matter. The theft-injector case — flooding as the entry to impersonation — is cross-linked from [CAN injection](can-injection.md), which owns forgery; this page owns removal and suppression.

This page synthesizes the KB's own full entity and concept pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source.

## Related

- [CAN injection](can-injection.md) — the forgery half of the bus attack surface; this page is the removal half
- [SoK: Kicking CAN Down the Road](../sok-kicking-can-down-the-road-systematizing-can-security-knowledge.md) — availability graded the bus's most exposed element
- [Experimental Security Analysis of a Modern Automobile](../experimental-security-analysis-of-a-modern-automobile.md) — physical-layer dominance and diagnostic silencing
- [The Bus-Off Attack Revisited](../error-handling-of-in-vehicle-networks-makes-them-vulnerable.md) — fault confinement turned against a healthy ECU
- [Silently Disabling ECUs](../silently-disabling-ecus-and-enabling-blind-attacks-on-the-can-bus.md) — the error-frame-interruption successor (analysis, not demonstration)
- [Diagnostic-service abuse](diagnostic-service-abuse.md) — silencing as a service-level primitive
- [CANter](../canter.md) — the corpus's detection answer
