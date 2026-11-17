---
uid: 01a1cf17-1a84-7bdd-a57b-9baecb6115b3
title: "HotWire: Real-World Impersonation and Discharge Attacks on Electric Vehicle Charging Systems"
summary: "Chen et al., USENIX WOOT 2026. Demonstrates identifier impersonation and forced battery discharge against production EVs and live charging networks, showing…"
type: entity
category: "Research Papers"
url: "https://www.usenix.org/conference/woot26/presentation/chen"
status: published
last_checked: 2026-11-17
created: 2026-11-12
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 058bc80
list_summary: "Chen et al., USENIX WOOT 2026. Demonstrates identifier impersonation and forced battery discharge against production EVs and live charging networks, showing DIN 70121 sessions trust protocol messages over physical verification."
related:
  - brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging
  - race-to-charge-concurrency-bugs-and-state-integrity-violations-in-ev-charging-infrastructure
  - relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars
  - pedal-to-the-bare-metal
  - charging-trust-chain
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-12
  - url: "https://www.usenix.org/conference/woot26/presentation/chen"
    retrieved: 2026-11-17
facets: [ev-charging, attack, research]
---

Chen et al., USENIX WOOT 2026. Demonstrates identifier impersonation and forced battery discharge against production EVs and live charging networks, showing DIN 70121 sessions trust protocol messages over physical verification.

## What it is

A paper at the 20th USENIX WOOT Conference on Offensive Technologies (WOOT 26), Baltimore, August 2026, pp. 1–16, by Kuan Yu Chen and Wen Wei Li and Shi Cho Cha (National Taiwan University of Science and Technology), Md Hasan Shahriar and Wenjing Lou (Virginia Tech). It presents HotWire, a systematic security analysis of the legacy **DIN 70121** EV charging protocol and, according to the abstract, the first demonstration of two practical, production-grade exploits against real charging ecosystems.

## How it works

DIN 70121 lacks cryptographic authentication and exposes critical control messages in plaintext. Prior work had noted conceptual weaknesses, but the authors argue that end-to-end feasibility and impact were not understood. Their two attacks are:

- **Unauthorised Autocharge activation by identifier impersonation.** An adversary replays a captured EV identifier (EVCCID) with a low-cost hardware toolkit to open a fraudulent Autocharge session on a commercial network. Experiments reportedly obtained repeated full charging sessions commonly valued at 35–45 without triggering existing fraud detection.
- **Unauthorised energy extraction through battery-state manipulation.** The authors exploit insecure battery-management-system state transitions by injecting protocol-compliant voltage claims, inducing controlled forced discharge and enabling persistent energy loss.

Both were validated across production vehicles and multiple public charging networks using a physical hardware-in-the-loop testbed. The paper's finding is a trust-model problem: the charging ecosystem trusts protocol state over physical verification. The authors released open-source auditing tools and report responsible-disclosure outcomes that already prompted firmware updates and additional authentication safeguards from several vendors.

## Where it fits

HotWire is the charging-protocol companion to [BrokenWire: wireless disruption of CCS electric vehicle charging](brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging.md), which attacks the physical/link side of the same session, and to [Race to Charge](race-to-charge-concurrency-bugs-and-state-integrity-violations-in-ev-charging-infrastructure.md), which studies concurrency and state-integrity violations in the same infrastructure. [Relay attacks on passive keyless entry and start systems](relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars.md) is the analogous identifier-replay problem on the vehicle-access side, and [Pedal to the Bare Metal](pedal-to-the-bare-metal.md) is the other 2026 hardware-adjacent EV case in the corpus. [OCPPuzz](ocppuzz.md) targets the management-system side rather than DIN 70121.

## Limits and safety notes

This page is based on the official USENIX abstract; it does not reproduce the packet sequences, the BMS state machine, or the toolkit construction details — read the open-access paper and slides for those. The abstract gives no currency for the "35–45" session value, so none is asserted here. The attacks affect billing and physical energy transfer on live infrastructure: this is not a passive testing topic, and the authors' disclosure path and released auditing tools are the appropriate starting point. No charging station, vehicle or protocol implementation was tested for this page.

## Status and sources

Checked 2026-11-17. **Published** — WOOT 26, August 2026; paper, slides and presentation video are linked from the conference page.

- [USENIX WOOT 26 paper page](https://www.usenix.org/conference/woot26/presentation/chen)

## Related

- [BrokenWire: wireless disruption of CCS electric vehicle charging](brokenwire-wireless-disruption-of-ccs-electric-vehicle-charging.md)
- [Race to Charge: concurrency bugs and state integrity violations in EV charging infrastructure](race-to-charge-concurrency-bugs-and-state-integrity-violations-in-ev-charging-infrastructure.md)
- [Relay attacks on passive keyless entry and start systems in modern cars](relay-attacks-on-passive-keyless-entry-and-start-systems-in-modern-cars.md)
- [Pedal to the Bare Metal](pedal-to-the-bare-metal.md)
- [The EV–EVSE charging trust chain (ISO 15118 / DIN 70121)](concepts/charging-trust-chain.md)
