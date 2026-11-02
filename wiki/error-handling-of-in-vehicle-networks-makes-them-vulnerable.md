---
title: "Error Handling of In-vehicle Networks Makes Them Vulnerable"
summary: "Cho and Shin, ACM CCS 2016. The bus-off attack, which abuses CAN error handling to force an uncompromised ECU off the bus without any vehicle-specific…"
type: entity
category: "Research Papers"
url: "https://dl.acm.org/doi/10.1145/2976749.2978302"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Cho and Shin, ACM CCS 2016. The bus-off attack, which abuses CAN error handling to force an uncompromised ECU off the bus without any vehicle-specific reverse engineering."
sources:
  - url: "https://rtcl.eecs.umich.edu/rtclweb/assets/publications/2016/ktcho_busoff_CCS_16.pdf"
    retrieved: 2026-11-01
  - url: "https://doi.org/10.1145/2976749.2978302"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
related:
  - fingerprinting-electronic-control-units-for-vehicle-intrusion-detection
  - vatican-vetted-authenticated-can-bus
  - can-injection
  - exposing-new-vulnerabilities-of-error-handling-mechanism-in-can
  - silently-disabling-ecus-and-enabling-blind-attacks-on-the-can-bus
  - canflict-exploiting-peripheral-conflicts-for-data-link-layer-attacks-on-automotive-networks
  - canvas-fast-and-inexpensive-automotive-network-mapping
---

Cho and Shin, ACM CCS 2016. The bus-off attack, which abuses CAN error handling to force an uncompromised ECU off the bus without any vehicle-specific reverse engineering.

## What it is

Kyong-Tak Cho and Kang G. Shin, University of Michigan. *Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security* (CCS '16), Vienna, Austria, October 24–28, 2016, pp. 1044–1055. DOI: [10.1145/2976749.2978302](https://doi.org/10.1145/2976749.2978302). The paper discovers and demonstrates the **bus-off attack**: a denial-of-service attack that turns CAN's fault-confinement mechanism — a safety feature — into the weapon, forcing a healthy, uncompromised ECU to disconnect *itself* from the bus. (The paper's own title capitalizes "In-Vehicle".) Companion piece to the same authors' CIDS paper (same batch).

## What it showed

**The mechanism abused.** Every CAN controller keeps a Transmit Error Counter (TEC). A transmitter that detects an error during its own transmission adds **+8 to its TEC**; each successful transmission subtracts only 1. A node is error-active while TEC ≤ 127, error-passive above 127 (its error flag becomes passive and cannot override bus traffic), and is forced into **bus-off — complete disconnection — when TEC > 255**. Fault confinement exists so a defective ECU removes itself; the attack makes a healthy ECU accumulate errors as if defective.

**The attack primitive.** The attacker (controlling one compromised ECU) transmits, at exactly the same time as a victim ECU's periodic message M, an *attack message* meeting three conditions: **C1** the same ID as M (both nodes win arbitration together and transmit bit-synchronized); **C2** the same transmission timing; **C3** identical bits up to some position, then a dominant (0) bit where M has a recessive (1) bit. The victim, monitoring the bus while transmitting, sees the opposite polarity — a *bit error* in its own frame — and takes +8 TEC. The attacker needs no knowledge of what M means, and the attack succeeds before any checksum or MAC on M is verified, so neither prevents it.

**Phase 1 — one injection cascades.** Both nodes start error-active. The forced bit error makes the victim raise an active error flag, which itself errors the attacker; both controllers then *automatically retransmit*, the collision recurs, and after 16 retransmissions both TECs reach 128 — both error-passive ("the controller does it all for the attacker"). One injected message thus coerces the victim into error-passive.

**The phase transition and Phase 2.** Now the asymmetry appears: the victim's passive error flag cannot disturb the attacker's frame, so on the next collision the attacker completes its transmission (TEC −1, returning to error-active at 127) while the victim takes +8 for the bit error and −1 for its eventual successful retransmission — a net **+7 per round**, staying error-passive. For each subsequent period of M, the attacker repeats the injection; the victim's TEC climbs by 7 each time until it exceeds 255 and the victim ECU is disconnected.

**Preconditions.** The attacker must already control an ECU on the bus able to inject arbitrary ID/DLC/data and to sniff traffic (how the ECU was compromised is explicitly out of scope); the target message must be **periodic**; and the attacker must synchronize with the victim's transmissions, achieved via CAN's common buffering behaviour — many ECUs transmit when a specific *preceded ID* arrives, so the attacker triggers on that message, genuine or fabricated. No reverse engineering of message semantics or checksum algorithms is required for any vehicle make or model — the paper's central contrast with prior vehicle attacks.

**Evaluation.** On a 3-node prototype at 500 kbit/s, run 1,000 times: the victim's TEC trajectory matched the two-phase model, and **all attempted attacks succeeded**, with error-passive reached in under 10 ms. On real vehicles (immobilized, controlled environment), the attack was mounted against a 2013 Honda Accord ECU sending message 0x295 every 40 ms and a 2016 Hyundai Sonata ECU sending 0x164 every 10 ms, via a fabricated preceded ID: Phase 1 succeeded in **13 of 15** attempts on the Honda and **14 of 15** on the Hyundai. A prototype node joined to each vehicle's live network was driven to bus-off under real bus load (error-passive within 2.4 ms).

**Why existing defences fail, and the proposed countermeasure.** The attack's symptoms (error frames, a node going silent) are indistinguishable from genuine hardware faults, so IDSs read it as a system error, not an attack; MACs do not help, because the victim is disconnected by the error-handling layer before authentication is evaluated, so *secured* future networks remain vulnerable. Per the paper's analysis, CAN-FD shares CAN's arbitration and error handling and is likewise vulnerable; TTCAN's static schedule hands the attacker the timings; FlexRay is *not* vulnerable the same way (its error-passive nodes may not transmit). The proposed countermeasure exploits two fingerprints: **F1** — Phase 1 produces at least 16 consecutive, bursty error frames (even two consecutive errors are ≤0.11% likely at a bit-error rate of 10⁻³); **F2** — in Phase 2, a message with the victim's ID is successfully transmitted by *someone* at the moment the victim's TEC rises, which cannot happen in a merely faulty network. On observing F2 after N = 16 bursty error frames, the victim resets its error counters; in prototype tests this kept the victim error-active.

## Where it fits

The canonical protocol-layer CAN denial-of-service result: it needs no message semantics, no checksum algorithm, and no vehicle-specific work, and it defeats the two defences the field was then deploying (checksums/MACs and content-based IDSs) by operating underneath both. It is the attack-side half of Cho & Shin's 2016 pair; the [CIDS paper](fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md) builds the fingerprinting IDS whose absence it exploits. It also completes the CAN attack taxonomy alongside [CAN injection](concepts/can-injection.md): injection puts words in a victim's mouth; bus-off removes the victim from the conversation entirely, enabling the classic follow-on — silence the genuine ECU, then transmit in its name. Wolf 2004 had identified CAN's fault-localization mechanism as an abuse target analytically; this is its experimental realization a decade later.

## Limits and safety notes

As the paper states them: **a compromised ECU is assumed** — the paper addresses what an adversary can do *with* a compromised ECU, not how to compromise one; the attack is a post-compromise primitive, not an entry point. **Periodic targets only:** synchronization depends on the target message being periodic (most in-vehicle messages are). **Real-vehicle demonstration scope:** on the two production vehicles, the directly observed result is Phase 1 against real ECUs (13/15 and 14/15) — full bus-off of a *production* ECU is inferred from the prototype-in-vehicle-network runs, because real ECUs' error counters cannot be read externally. **The countermeasure is a proposal, not a fix in silicon:** the F1/F2 rule was evaluated on the authors' prototype only; stronger variants require CAN controller hardware changes not in production parts. The attack had "not yet been seen in the wild" as of publication.

## Status and sources

Status: **unknown** — a finished 2016 publication; no living artefact (the attack and defence were research prototypes). Bibliographic record: CCS '16 proceedings and DOI as printed on the paper; the authors' open copy was read in full 2026-11-01.

## Related

- [Fingerprinting Electronic Control Units for Vehicle Intrusion Detection](fingerprinting-electronic-control-units-for-vehicle-intrusion-detection.md)
- [vatiCAN: Vetted, Authenticated CAN Bus](vatican-vetted-authenticated-can-bus.md)
- [CAN injection](concepts/can-injection.md)
