---
title: "Simulation and test doubles for vehicle networks"
summary: "The corpus's simulation layer, rung by rung — virtual bus, replay, declarative doubles, physical miniatures — and what each rung cannot tell you."
type: concept
created: 2026-11-01
updated: 2026-11-01
related: [icsim, busmaster, candevstudio, udsim, uds-server, doip-sim-ecu-dsl, ramn, veins, van3twin]
sources:
  - url: "https://github.com/zombieCraig/ICSim"
    retrieved: 2026-11-01
  - url: "https://github.com/candle-usb/uds-server"
    retrieved: 2026-11-01
---

Almost nothing in this KB was first tried on a real car. The corpus's tools presume a stand-in: a virtual bus to develop against, a recorded ECU to replay, a simulated network to rehearse on — because the real target is dangerous to experiment on, stateful in ways a bench session corrupts, and non-repeatable (a car that has been fuzzed into a stuck brake does not reset for the next run; [Koscher 2010](../experimental-security-analysis-of-a-modern-automobile.md)'s team had to fuzz their way back out). The safety guidance across the KB's pages repeats one instruction — *use the simulator first* — and this page is that instruction's home: the simulation layer organised by what is being doubled, and by the fidelity limit each rung states or implies.

## Rung 1: the virtual bus and its nodes

The lightest double replaces the wire and the talkers. [ICSim](../icsim.md) simulates an instrument cluster and its controls on a virtual CAN bus — the teaching double the Car Hacker's Handbook tradition starts from. [BUSMASTER](../busmaster.md)'s rest-bus mode simulates the *rest* of the network around one real node under test, and [CANdevStudio](../candevstudio.md) assembles simulated nodes graphically. What is doubled: message traffic and node responses at the frame level. The limit is definitional: a virtual bus has no physics — no arbitration timing under load, no error frames from real transceivers, no voltage. Anything whose mechanism lives below the frame ([bus-off](../error-handling-of-in-vehicle-networks-makes-them-vulnerable.md), [voltage fingerprinting](../viden-attacker-identification-on-in-vehicle-networks.md)) cannot even be expressed here.

## Rung 2: recorded-behaviour replay

The next rung doubles a *specific* ECU by learning it. [UDSim](../udsim.md) learns a real module's diagnostic behaviour from traffic, then simulates it — well enough to rehearse attacks (its learn/simulate/attack loop includes silencing real modules against their doubles). [uds-server](../uds-server.md) serves UDS responses as a standing test endpoint. The limit is the recording: a replay double knows only the behaviour it observed. It cannot invent the response to an unseen request, a state it never entered, or an error path nobody triggered while recording — fuzzing a replay double explores the *recording*, not the ECU, and the difference matters exactly when the work turns adversarial.

## Rung 3: declarative ECU doubles

[doip-sim-ecu-dsl](../doip-sim-ecu-dsl.md) doubles an ECU from a *description* rather than a recording: a DSL declares the diagnostic personality — services, sessions, responses — for automated test rigs, aimed at DoIP-era ECUs. What is doubled is intent, not observation: the double behaves as specified, which makes it the right tool for testing a *client* (a tester, a flasher, a scanner) against the specification's cases including malformed ones, and the wrong tool for learning anything about a real ECU the description only approximates.

## Rung 4: physical miniature networks

[RAMN](../ramn.md) doubles the network in hardware: real ECUs on a real bench bus, a miniature vehicle electrical system for training and experiment. Physics returns — real arbitration, real error handling, real transceivers — at bench scale and bench cost. The limit is representativeness: a testbed's message set, gateway topology, and ECU population are *a* network, not the production vehicle the conclusions will be applied to (the same caution the [ROAD guide](../a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset.md) applies to datasets applies to benches verbatim). The V2X literature doubles at network scale instead — [Veins](../veins.md) and [VaN3Twin](../van3twin.md) simulate whole traffic-and-network systems, and [F2MD](../f2md.md)'s misbehavior framework is simulation-born — because a fleet cannot be a bench at all.

## Why the corpus routes through doubles

Three reasons recur. **Safety:** the attack literature's effects (brakes, steering, immobilisation) are rehearsed on doubles before any vehicle is touched, and several tool pages' safety notes amount to a pointer at this page's rungs. **Repeatability:** an experiment on a double can be reset and rerun bit-for-bit; the [real-world applicability](../on-the-real-world-applicability-of-automotive-can-intrusion-detection-systems.md) critique of IDS evaluation is partly a complaint that the field's doubles and datasets made results irreproducible in the other direction — accurate on the double, unmeasured on the car. **Access:** doubles are what most researchers *have*; production vehicles are expensive, current, and owned by someone else. The honest posture the corpus converges on is a ladder: develop on rung 1–3, validate on rung 4 or hardware, and claim vehicle-level truth only where a vehicle was actually involved — with the rung named in the claim.

This page synthesizes the KB's own full entity pages named above and in its frontmatter; every load-bearing claim is carried on those pages with its primary source. The evaluation that filed this concept flagged it as the mining pass's weakest ADD on falsifiability — an ecosystem fact rather than a mechanism — and the page is written to that standard: an orientation to the layer, not a claim about any one tool.

## Related

- [ICSim](../icsim.md) — the teaching double: a virtual cluster on a virtual bus
- [UDSim](../udsim.md) — learn a real ECU, then rehearse against its double
- [doip-sim ECU DSL](../doip-sim-ecu-dsl.md) — the declarative rung: doubles from descriptions
- [RAMN](../ramn.md) — the physical miniature: real ECUs, bench scale
- [Busmaster](../busmaster.md) and [CANdevStudio](../candevstudio.md) — rest-bus and graphical node simulation
