---
uid: 01a1ea9a-c0db-711a-9628-42e012b2af53
title: "DoIP moves diagnostics onto the network"
summary: "DoIP replaces the physical OBD port with a routable endpoint; discovery and routing activation become the new trust boundary."
type: concept
cluster: boundary
created: 2026-11-17
updated: 2026-11-17
related:
  - python-doipclient
  - doip-sim-ecu-dsl
  - gallia
  - autofuze
  - canexplorer
  - ecubus-pro
  - nullsec-carfuzz
  - opensovd-classic-diagnostic-adapter
  - protocrawler
  - scapy
  - zephyr-reference-ecu
  - uds-seed-key
  - diagnostic-service-abuse
  - someip
  - iso-tp
  - external-attack-surface
sources:
  - url: "https://github.com/jacobschaer/python-doipclient"
    retrieved: 2026-11-17
  - url: "https://github.com/doip-sim-ecu/doip-sim-ecu"
    retrieved: 2026-11-17
  - url: "https://github.com/Fraunhofer-AISEC/gallia"
    retrieved: 2026-11-17
  - url: "https://www.iso.org/standard/78176.html"
    retrieved: 2026-11-17
facets: [can, diagnostics, doip, standards]
---

Diagnostics over IP (DoIP, ISO 13400) carries the same UDS services that
traditionally ran over CAN, but delivers them to a TCP endpoint on port
13400 instead of a connector on the bumper. The payload is familiar; the
trust boundary is not.

## What the corpus shows

Eleven full-depth entries touch DoIP:

- **Client transport.** [python-doipclient](../python-doipclient.md)
  implements the ISO 13400-2:2019 client view: Vehicle Identification
  Request, waiting for the power-up Vehicle Announcement, routing
  activation, entity status, alive check and diagnostic power mode, then
  diagnostic payloads over TCP. It exists to give
  [udsoncan](../udsoncan.md) an Ethernet transport.
- **Server and test side.** [doip-sim-ecu-dsl](../doip-sim-ecu-dsl.md)
  declares gateways and ECUs, emits announcements and answers TCP/UDP on
  port 13400; it can also make one ECU dual-homed on DoIP and CAN/UDS with
  shared state. [zephyr-reference-ecu](../zephyr-reference-ecu.md) is the
  embedded reference target; [opensovd-classic-diagnostic-adapter](../opensovd-classic-diagnostic-adapter.md)
  is the adapter path.
- **Attack and analysis tooling.** [Gallia](../gallia.md) selects transport
  with a URI — `doip://` includes gateway plus routing activation — and logs
  tests for reproducibility. [autofuze](../autofuze.md) spans UDS over both
  DoIP and CAN. [NullSec CarFuzz](../nullsec-carfuzz.md),
  [protocrawler](../protocrawler.md), [scapy](../scapy.md),
  [CAN Explorer](../canexplorer.md) and [ECUbus Pro](../ecubus-pro.md)
  round out the protocol and discovery side.

## The synthesis

No entity page states the structural claim: **DoIP converts a physical
access assumption into a network reachability assumption, and the new
handshake becomes a security control surface in its own right.**

With a wired diagnostic port, "can talk to the ECU" implied standing next to
the car. With DoIP it means reaching an IP endpoint, so the questions that
matter move *below* UDS:

- Who may believe a **Vehicle Announcement**? A false announcement or a
  spoofed identification response redirects a client before any diagnostic
  service is requested.
- What does **routing activation** authorize? It is a gate in front of the
  diagnostic connection, not part of UDS, and it is where gateway policy
  lives.
- Does the **alive check** and power-mode state distinguish an authorized
  session from a stale one? python-doipclient implements these as first-class
  API calls, which is itself evidence that they are protocol state a client
  must manage.

Gallia modelling `doip://` as gateway *plus* routing activation is the
clearest expression of the boundary: the transport is not a dumb pipe.
doip-sim-ecu-dsl's dual-homed ECU shows why the distinction matters — an
entity reachable over DoIP may also be on CAN, so a decision made at the
Ethernet gate has consequences on a second bus.

## Boundary with neighbouring concepts

[ISO-TP](iso-tp.md) owns the CAN transport counterpart, including its
flow-control state machine. [UDS seed/key](uds-seed-key.md) owns SecurityAccess
(0x27) *inside* UDS. [Diagnostic service abuse](diagnostic-service-abuse.md)
owns service-level semantics once a session exists.
[SOME/IP](someip.md) owns Ethernet service discovery and middleware, not
diagnostics. [External attack surface](external-attack-surface.md) owns how
an attacker reaches the network in the first place.

## Counter-cases and limits

DoIP is not automatically the weaker interface. A gateway can restrict
routing activation by address and interface, and a well-implemented alive
check bounds sessions; the corpus shows those controls as ordinary API
surface rather than exotic hardening. The specific "secure" option is a
caution, not a win: python-doipclient documents its TLS path (port 3496)
as **untested**. Gallia's README warns that inappropriate use can
irreversibly damage the device under test. This page synthesizes the KB's
verified pages and upstream documentation; no vehicle or ECU was exercised.
