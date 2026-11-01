---
title: "Kayak"
summary: "Java-based CAN bus analysis tool with bus monitoring and DBC/KCD file loading support."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/dschanoeh/Kayak"
status: archived
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Java-based CAN bus analysis tool with bus monitoring and DBC/KCD file loading support."
related: [cantools, canmatrix, savvycan, cangaroo]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/dschanoeh/Kayak"
    retrieved: 2026-10-31
---

Java-based CAN bus analysis tool with bus monitoring and DBC/KCD file loading support.

## What it is

A pure-Java desktop application for CAN monitoring and diagnosis, built
around SocketCAN. **The GitHub repository is now archived** — this page's
`status: archived` records that. The checked repository and documentation
do not name a primary maintainer or organisation; `dschanoeh` is the
repository owner/handle only.

## How it works

Kayak itself is platform-independent because it does not normally talk
directly to the CAN controller. A Linux machine attached to the bus runs
**socketcand**, which bridges SocketCAN to TCP/IP; Kayak connects over
the socket and uses an abstract bus/receiver/sender model. Native bus
descriptions use Kayak's **KCD** format. Existing DBC files must first be
converted to KCD with CANBabel — [canmatrix](canmatrix.md) and
[cantools](cantools.md) both read KCD today — after which Kayak can
interpret and display messages and signals. Implemented features include
project and log management, a raw-frame view, single and repetitive frame
sending, and log creation/replay.

## Where it fits

Cross-platform GUI monitoring and signal interpretation where KCD
descriptions are available, and Java projects that can reuse Kayak's CAN
abstraction model. For new work, [SavvyCAN](savvycan.md) and
[CANgaroo](cangaroo.md) are the maintained GUI successors; Kayak remains
relevant as the origin of the KCD format the ecosystem still converts.

## Limits and notes

Beyond the archived repository: its documentation site still describes
the downloadable build as a development version, says Kayak had not been
released, and warns it may be quite unstable (the currency of that site
could not be independently verified). The build instructions call for a
JDK and Maven 2 and warn that the first build downloads many NetBeans RCP
dependencies. No operational-safety warning was verified in the checked
pages.

## Related

- [cantools](cantools.md) — reads and writes its KCD format.
- [canmatrix](canmatrix.md) — converts DBC↔KCD and most other formats.
- [SavvyCAN](savvycan.md) — maintained GUI successor.
- [CANgaroo](cangaroo.md) — maintained analyser with KCD-adjacent workflows.
