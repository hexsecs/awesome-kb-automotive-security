---
uid: 01a1ea9a-c0db-711a-9628-42e1d08668bb
title: "ISO-TP: the stateful transport under diagnostics"
summary: "ISO 15765-2 reassembles multi-frame diagnostic payloads on CAN; its flow-control state machine is an attacker-controllable resource."
type: concept
cluster: bus
created: 2026-11-17
updated: 2026-11-17
related:
  - the-vehicle-may-be-sick-denial-of-diagnostic-services-by-exploiting-the-can-transport-protocol
  - python-can-isotp
  - iso14229
  - gallia
  - doip-sim-ecu-dsl
  - cantact
  - j1939
  - can-availability
  - uds-seed-key
  - diagnostic-service-abuse
  - doip
  - owasp-automotive-emb-60
  - piccante
  - python-can
  - uds-firmware-extraction
  - can-utils
sources:
  - url: "https://doi.org/10.5281/zenodo.18715820"
    retrieved: 2026-11-17
  - url: "https://github.com/pylessard/python-can-isotp"
    retrieved: 2026-11-17
  - url: "https://github.com/driftregion/iso14229"
    retrieved: 2026-11-17
  - url: "https://www.iso.org/standard/66574.html"
    retrieved: 2026-11-17
facets: [can, diagnostics, iso-tp, attack, standards]
---

CAN frames carry at most eight bytes. UDS requests and responses routinely
need more. ISO-TP (ISO 15765-2) is the layer that segments them across
single, first, consecutive and flow-control frames and reassembles them at
the receiver. It is usually described as plumbing; the corpus shows it is
also an attack surface.

## What the corpus shows

Six full-depth entries carry the evidence:

- The escar USA 2026 talk
  [The Vehicle May Be Sick](../the-vehicle-may-be-sick-denial-of-diagnostic-services-by-exploiting-the-can-transport-protocol.md)
  defines **eight attack scenarios** against an in-progress transfer —
  preceding flow control, forced wait, forced overflow, corrupted data
  length, broken sequence numbers, session override, reserved values and
  timeout — and validates them with an aftermarket and an OEM-level tool on
  one production vehicle.
- [python-can-isotp](../python-can-isotp.md) is the user-space and
  SocketCAN-kernel implementation; its v2 docs expose flow control, STmin,
  blocking timing and thread behaviour.
- [iso14229](../iso14229.md) embeds ISO-TP in a static-allocation ECU-side
  UDS implementation, including 0x27 SecurityAccess examples.
- [Gallia](../gallia.md) makes `isotp://` a first-class target URI with
  CAN-FD options.
- [doip-sim-ecu-dsl](../doip-sim-ecu-dsl.md) implements segmentation, flow
  control and CAN-FD escape encodings to simulate ECUs in CI.
- [cantact](../cantact.md) is the hardware interface that puts a laptop on
  the bus to do any of this.

## The synthesis

No entity page states the general claim: **ISO-TP is a state machine
distributed across two ECUs, driven by unauthenticated frames, so the
transport itself can be denied or manipulated regardless of the security of
the UDS services above it.**

The eight scenarios are variations on one mechanism: the receiver's
reassembly state — its expected sequence number, its buffer, its timers and
its flow-control decision — can be steered by a frame that any node on the
bus may send. The attacker does not need to break SecurityAccess; they need
to make the transfer fail, stall, or deliver an altered result. The observed
impacts were missing ECU identifiers, manipulated DTC scan results, a false
evaporative "large leak", and inoperable variant coding — diagnosis being
lied to, not code execution.

The tooling corroborates the model. A library has to expose STmin and
threading because timing is semantics. An embedded server has to allocate
reassembly buffers statically because memory is finite. A pentest framework
has to name the transport in its target URI because transport choice changes
the attack. And a simulator has to implement flow control to test client
error paths — which is exactly the state an attacker pushes.

## Boundary with neighbouring concepts

[J1939](j1939.md) owns the heavy-vehicle sibling transport (TP.CM/TP.DT),
not ISO 15765-2. [CAN availability](can-availability.md) owns layer-2 DoS
such as priority jamming and bus-off. [UDS seed/key](uds-seed-key.md) owns
the 0x27 authentication that rides *over* this transport.
[Diagnostic service abuse](diagnostic-service-abuse.md) owns service-level
semantics. [DoIP](doip.md) owns the Ethernet diagnostic transport.

## Counter-cases and limits

The attack model already assumes CAN access — via a compromised infotainment
unit, a wireless flaw or a vulnerable dongle — so this is not a remote entry
path on its own. Results come from one vehicle and two tool sets, and the
escar detail slides are largely graphical, so the scenario names are faithful
paraphrases rather than a reproduced exploit recipe. The defensive
counter-case is architectural: a transport that reassembles correctly does
not thereby authorize actuation, and the KB's safety-related pages keep those
decisions separate. No bus, vehicle or tool was exercised for this page.
