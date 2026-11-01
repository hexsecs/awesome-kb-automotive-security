---
title: "open-plc-utils"
summary: "Qualcomm Atheros powerline toolkit for HomePlug AV and Green PHY devices, the standard means of inspecting and manipulating the PLC layer that CCS charging…"
type: entity
category: "EV Charging Security"
url: "https://github.com/qca/open-plc-utils"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Qualcomm Atheros powerline toolkit for HomePlug AV and Green PHY devices, the standard means of inspecting and manipulating the PLC layer that CCS charging sessions run over."
related: [pyplc, acccs, openv2g]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/qca/open-plc-utils"
    retrieved: 2026-11-01
  - url: "https://github.com/qca/open-plc-utils/commit/5e0295719d70058221273ac0e780fcd82e28ea0f"
    retrieved: 2026-11-01
  - url: "https://github.com/qca/open-plc-utils/blob/5e0295719d70058221273ac0e780fcd82e28ea0f/README"
    retrieved: 2026-11-01
  - url: "https://github.com/qca/open-plc-utils/blob/5e0295719d70058221273ac0e780fcd82e28ea0f/docbook/plc.1.html"
    retrieved: 2026-11-01
  - url: "https://github.com/qca/open-plc-utils/blob/5e0295719d70058221273ac0e780fcd82e28ea0f/docbook/evse.1.html"
    retrieved: 2026-11-01
  - url: "https://github.com/qca/open-plc-utils/blob/5e0295719d70058221273ac0e780fcd82e28ea0f/docbook/pev.1.html"
    retrieved: 2026-11-01
  - url: "https://github.com/uhi22/pyPLC/blob/be5139bc6e66ba3b3bfa502666f494d3e157968b/readme.md"
    retrieved: 2026-11-01
---

Qualcomm Atheros powerline toolkit for HomePlug AV and Green PHY devices, the standard means of inspecting and manipulating the PLC layer that CCS charging sessions run over.

## What it is

Qualcomm Atheros's open Powerline Toolkit: small command-line programs and examples for interrogating, configuring, and managing supported powerline devices. The README documents builds for Linux and other host platforms; its plc manual is aimed at hardware engineers and software developers. The EV-relevant portion includes Green PHY SLAC tools and modem configuration support.

## How it works

The toolkit exchanges Ethernet management messages with QCA devices. The plc manual describes identifying firmware/hardware, resets, firmware/parameter-image operations, and HomePlug frame inspection. The evse and pev manuals specifically implement the two sides of SLAC association: signal attenuation measurements help a vehicle select its connected charging station. They take a host Ethernet interface and configuration profiles; this is link association, not an ISO 15118 charging application.

## Where it fits

Use it to understand or configure the PLC modem beneath a CCS research stack. [pyPLC](pyplc.md) explicitly references it for adaptor configuration, and [AcCCS](acccs.md) also depends on the Green PHY layer. [OpenV2G](openv2g.md) sits higher up, handling EXI/application messages rather than configuring the modem.

## Limits and safety notes

Device-management commands are chipset/firmware-specific. The ability to inspect HomePlug frames does not guarantee transparent capture of every EV/EVSE unicast packet: pyPLC documents firmware-dependent visibility. The toolkit does not supply a complete charging controller, TLS/Plug & Charge authorisation, or power electronics. The plc manual warns that amptest has no interlocks against loading an image for the wrong platform or in an illogical order; flashing/reset operations can change the device under test. Work on recoverable lab hardware and preserve its original configuration. Cross-platform compilation is not guaranteed by the upstream manual.

## Status and sources

Checked 2026-11-01. **Active** at this check: the repository is not archived and its latest default-branch commit is dated 2026-09-08. This records observed project activity, not a promise of support or protocol completeness. See the [checked commit](https://github.com/qca/open-plc-utils/commit/5e0295719d70058221273ac0e780fcd82e28ea0f). Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream README](https://github.com/qca/open-plc-utils/blob/5e0295719d70058221273ac0e780fcd82e28ea0f/README)
- [Toolkit manual](https://github.com/qca/open-plc-utils/blob/5e0295719d70058221273ac0e780fcd82e28ea0f/docbook/plc.1.html)
- [EVSE SLAC manual](https://github.com/qca/open-plc-utils/blob/5e0295719d70058221273ac0e780fcd82e28ea0f/docbook/evse.1.html)
- [PEV SLAC manual](https://github.com/qca/open-plc-utils/blob/5e0295719d70058221273ac0e780fcd82e28ea0f/docbook/pev.1.html)

- [pyPLC upstream README: integration and modem visibility](https://github.com/uhi22/pyPLC/blob/be5139bc6e66ba3b3bfa502666f494d3e157968b/readme.md)

## Related

- [pyPLC](pyplc.md)
- [AcCCS](acccs.md)
- [OpenV2G](openv2g.md)
