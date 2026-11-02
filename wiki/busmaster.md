---
title: "BUSMASTER"
summary: "Open-source CAN simulation, analysis, and test tool from Bosch Engineering and ETAS, with a node simulator, DBC-driven signal interpretation, and scriptable…"
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/rbei-etas/busmaster"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source CAN simulation, analysis, and test tool from Bosch Engineering and ETAS, with a node simulator, DBC-driven signal interpretation, and scriptable test automation."
related: [candevstudio, savvycan, kayak, simulation-and-test-doubles]
license: GPL-3.0
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/rbei-etas/busmaster"
    retrieved: 2026-10-31
  - url: "https://www.can-cia.org/fileadmin/cia/documents/proceedings/2012_lorenz.pdf"
    retrieved: 2026-10-31
---

Open-source CAN simulation, analysis, and test tool from Bosch Engineering and ETAS, with a node simulator, DBC-driven signal interpretation, and scriptable test automation.

## What it is

A Windows PC application for designing, monitoring, analysing, and
simulating CAN bus systems — its framing in the authors' own iCC 2012 paper
is rest-bus simulation. It was conceptualised, designed, and implemented by
Robert Bosch Engineering and Business Solutions (RBEI) and is now a joint
RBEI + ETAS GmbH project. The repository is GPL-3.0 (the 2012 paper says
LGPL was chosen at launch; the repo's current licence is the operative
fact).

## How it works

BUSMASTER has a modular, plug-in GUI architecture — third parties can add
functions, and dynamically linked proprietary add-ons are permitted by
design. It runs fully in simulation mode with no hardware attached; for a
real bus it needs a vendor adapter plus that vendor's driver (the README
names PEAK PCAN-USB and ETAS ES 581/HSP). It imports network description
files in standard industry formats, and provides message/signal windows,
logging, replay, and a node-simulation facility for modelling ECU
behaviour.

## Where it fits

Bench rest-bus simulation and network design-and-test work where a free
alternative to commercial bus tools is wanted — especially inside
Bosch/ETAS hardware ecosystems. For flow-based simulation of missing ECUs,
compare [CANdevStudio](candevstudio.md); for interactive capture analysis,
[SavvyCAN](savvycan.md).

## Limits and notes

Windows host only. Real-bus use requires separately procured vendor
hardware and drivers. The primary documentation states no usage-safety
guidance.

## Related

- [CANdevStudio](candevstudio.md) — flow-based graphical simulation of missing ECUs.
- [SavvyCAN](savvycan.md) — cross-platform capture and reverse-engineering GUI.
- [Kayak](kayak.md) — Java-based bus monitoring with DBC/KCD loading.
