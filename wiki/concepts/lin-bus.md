---
uid: 01a1ea9a-c0dc-7790-9d00-bf0f2bc92186
title: "LIN as the trusted subordinate bus"
summary: "LIN sits behind gateways on door modules and sensors, so it is treated as trusted — yet its wiring is often the most reachable."
type: concept
cluster: bus
created: 2026-11-17
updated: 2026-11-17
related:
  - linusbconverter
  - security-in-automotive-bus-systems
  - plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles
  - automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps
  - canexplorer
  - ecubus-pro
  - ics-cap
  - uds
  - can-injection
  - external-attack-surface
  - physical-channel-sensor-attacks
  - simulation-and-test-doubles
sources:
  - url: "https://github.com/IntergatedCircuits/USB-LIN-Converter"
    retrieved: 2026-11-17
  - url: "https://www.escrypt.com/en/publications/security-in-automotive-bus-systems.html"
    retrieved: 2026-11-17
  - url: "https://www.usenix.org/conference/usenixsecurity20/presentation/wen"
    retrieved: 2026-11-17
facets: [can, lin, sensors]
---

LIN is the single-wire, 9600/19200-baud subordinate bus behind door modules,
seats, climate control and steering-wheel controls. A master node runs a
schedule; slaves answer only when polled. Its position — one hop below the
CAN backbone — is why it is usually treated as uninteresting to security.
The corpus suggests that is a topology argument, not a security one.

## What the corpus shows

- [Security in automotive bus systems](../security-in-automotive-bus-systems.md)
  (Wolf, Weimerskirch & Paar, ESCAR 2004) puts LIN in its five-group bus
  taxonomy at 20 kbit/s and grades its exposure "little" — while still
  listing concrete attacks: a malicious sleep frame can deactivate the
  subnet, and a bogus sync byte breaks synchronization.
- [USB LIN Converter](../linusbconverter.md) is the bench entry: an isolated
  STM32F042 dongle that can act as master, slave or passive monitor, with a
  schedule table, switchable classic/enhanced checksums, and a read-only
  default for its AI-agent capture path.
- [Plug-N-Pwned](../plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles.md)
  measures the analogous failure one layer up: 77 of 77 wireless OBD-II
  dongles carry at least two vulnerability classes, and 84.16% have neither
  connection- nor application-layer authentication. The dongle is an
  unauthenticated bridge onto a bus that trusts every frame.
- [Automated reverse engineering of CAN bus commands](../automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps.md),
  [CAN Explorer](../canexplorer.md), [ECUbus Pro](../ecubus-pro.md),
  [ICS-CAP](../ics-cap.md) and py-uds ([uds](../uds.md), LIN planned) supply
  the capture, analysis and protocol context.

## The synthesis

No entity page states the connecting claim: **the reason LIN is considered
low-risk is that gateway policy assumes it cannot reach anything important —
but the assumption is enforced by topology, not by authentication, and LIN
wiring is physically among the easiest to reach in a vehicle.**

Wolf's "little" grading is about what a LIN node can do *on LIN*. The same
paper's central structural warning is that interconnection is the major
hazard: a gateway lets any controller on any bus reach any other, and it
explicitly recommends preventing LIN and MOST controllers from sending into
CAN. Remove that rule — or find a gateway that never had it — and the
subordinate bus is no longer subordinate. The 2004 design already knew this;
the corpus's OBD-dongle measurement shows the general pattern of an
unauthenticated bridge failing in the market.

So the useful question is not "is LIN valuable?" It is "what has the gateway
allowed a LIN node to cause on CAN?" Sleep-frame and sync disruption stay
local; anything that crosses the gateway inherits the CAN attack surface.

## Boundary with neighbouring concepts

[CAN injection](can-injection.md) owns forged frames on CAN and the access
paths that get them there — this page owns the LIN-side substrate and the
gateway trust assumption. [External attack surface](external-attack-surface.md)
owns physical reachability generally.
[Physical-channel sensor attacks](physical-channel-sensor-attacks.md) owns
spoofing at the sensor itself; LIN sits behind the sensor ECU, not at the
transducer. [Simulation and test doubles](simulation-and-test-doubles.md)
owns test benches; this page owns the bus they emulate.

## Counter-cases and limits

LIN is genuinely constrained: one wire, low rate, master/slave scheduling,
and in the 2004 paper the lowest exposure grade of the wired buses. The USB
LIN Converter's optical isolation, external LIN-side power and read-only
agent mode are concrete bench controls that contain the risk. The corpus
does not contain a demonstrated LIN-to-CAN pivot, and this page does not
claim one — the claim is about where the trust boundary sits and what would
have to fail for it to matter. No hardware, vehicle or bus was exercised.
