---
uid: 01a19d3c-af20-7f78-b272-35b2293d3ba5
title: "A Comprehensible Guide to Controller Area Network"
summary: "Wilfried Voss, Copperhill 2005. The standard plain-language reference on CAN itself, covering frame formats, arbitration, error handling, and timing that…"
type: entity
category: "Books"
url: "https://copperhilltech.com/a-comprehensible-guide-to-controller-area-network/"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Wilfried Voss, Copperhill 2005. The standard plain-language reference on CAN itself, covering frame formats, arbitration, error handling, and timing that vehicle network attacks depend on."
sources:
  - url: "https://copperhilltech.com/a-comprehensible-guide-to-controller-area-network/"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - error-handling-of-in-vehicle-networks-makes-them-vulnerable
  - can-injection
---

Wilfried Voss, Copperhill 2005. The standard plain-language reference on CAN itself, covering frame formats, arbitration, error handling, and timing that vehicle network attacks depend on.

A single-author, plain-language introduction to the CAN protocol itself — not a security book. Based on ISO 11898-1/-2, its nine chapters work through message frame architecture (including remote and extended frames), message broadcasting, bus arbitration, bit timing and synchronization, error detection and fault confinement, and the physical layer, written explicitly to fill the gaps and ambiguities Voss found in the Bosch, CiA, and ISO specifications.

Read it when you need protocol ground truth underneath CAN security work — bus-off and error-handling attacks only make sense with the fault-confinement chapter in hand. Caveats: higher-layer protocols (CANopen, DeviceNet, SAE J1939) are only sketched, and the 2005 text predates CAN FD and CAN XL (the publisher's page now links follow-on articles on both). The underlying classic-CAN fundamentals have not changed. Print edition is 146 pages; a PDF edition is sold via Lulu.

## Status and sources

Status: **published** — Wilfried Voss, Copperhill Technologies Corporation, 2005. ISBN 978-09765116-0-1. Publisher's product page: https://copperhilltech.com/a-comprehensible-guide-to-controller-area-network/ (checked 2026-11-01).

## Related

- [Error Handling of In-Vehicle Networks Makes Them Vulnerable](error-handling-of-in-vehicle-networks-makes-them-vulnerable.md) — the attack research that builds on this book's fault-confinement material
- [CAN injection](concepts/can-injection.md) — the concept page for the attack class this protocol knowledge underpins
