---
title: "EVerest"
summary: "Linux Foundation Energy full-stack open-source EV charging firmware implementing OCPP 1.6/2.0.1/2.1, ISO 15118-2/-3/-20, IEC 61851, and DIN SPEC 70121…"
type: entity
category: "EV Charging Security"
url: "https://github.com/EVerest/EVerest"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: 61ba124
list_summary: "Linux Foundation Energy full-stack open-source EV charging firmware implementing OCPP 1.6/2.0.1/2.1, ISO 15118-2/-3/-20, IEC 61851, and DIN SPEC 70121, useful as a reference target and test peer."
related: [checkocpp, emuocpp, ocpp-charging-attacks, dsv2gshark, wwcp-iso15118, pyplc]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/EVerest/EVerest"
    retrieved: 2026-11-01
  - url: "https://github.com/EVerest/EVerest/commit/2265c29a8dc0a841672012ccc0c31b00217174d8"
    retrieved: 2026-11-01
  - url: "https://github.com/EVerest/EVerest/blob/2265c29a8dc0a841672012ccc0c31b00217174d8/README.md"
    retrieved: 2026-11-01
  - url: "https://github.com/EVerest/EVerest/blob/2265c29a8dc0a841672012ccc0c31b00217174d8/modules/EVSE/EvseV2G/manifest.yaml"
    retrieved: 2026-11-01
  - url: "https://github.com/EVerest/EVerest/blob/2265c29a8dc0a841672012ccc0c31b00217174d8/modules/EVSE/Evse15118D20/manifest.yaml"
    retrieved: 2026-11-01
  - url: "https://github.com/EVerest/EVerest/blob/2265c29a8dc0a841672012ccc0c31b00217174d8/modules/EVSE/EvseSecurity/manifest.yaml"
    retrieved: 2026-11-01
---

Linux Foundation Energy full-stack open-source EV charging firmware implementing OCPP 1.6/2.0.1/2.1, ISO 15118-2/-3/-20, IEC 61851, and DIN SPEC 70121, useful as a reference target and test peer.

## What it is

A Linux Foundation Energy-backed modular EV charging software stack. The main README lists AC/DC charging, OCPP 1.6/2.0.1/2.1, ISO 15118-2/-3/-20, IEC 61851, DIN SPEC 70121, hardware drivers, energy management, and update support. It provides a substantial reference implementation and configurable peer for security and interoperability work.

## How it works

Interchangeable modules communicate through MQTT and connect protocol handling to hardware drivers and charging logic. The current Evse15118D20 manifest describes a C++ SECC implementation for DIN 70121 and ISO 15118-2/-20, with protocol selection, TLS negotiation, discovery, and Plug & Charge authorisation timeouts. EvseSecurity stores certificate/key material and exposes separate CSMS, manufacturer, mobility-operator, and V2G trust bundles. These configurations make the EV-facing and backend-facing certificate contexts inspectable.

## Where it fits

Use it as a configured charging-stack target when a small message emulator is insufficient. [EmuOCPP](emuocpp.md) and [CheckOCPP](checkocpp.md) address the backend link; [dsV2Gshark](dsv2gshark.md), [WWCP_ISO15118](wwcp-iso15118.md), and [pyPLC](pyplc.md) cover EV-facing observation or peers. [OCPP and charging attacks](concepts/ocpp-charging-attacks.md) explains why backend identities and firmware paths matter.

## Limits and safety notes

Protocol support in the project README is not a guarantee for every module, hardware combination, release, or deployment. EvseV2G is deprecated in 2026.10.0, with earliest removal 2027.04.0, and its manifest points to Evse15118D20 as successor. The successor's manifest warns that missing V2G leaf certificates can leave only unsecured sessions available unless TLS is enforced; it also describes configurations that allow non-conformant unsecured -20 sessions. Check the selected protocol/security settings explicitly. TLS key logging is marked for testing/simulation only. A software configuration and successful conversation do not validate the electrical safety of a hardware installation.

## Status and sources

Checked 2026-11-01. **Active** at this check: the repository is not archived and its latest default-branch commit is dated 2026-10-31. This records observed project activity, not a promise of support or protocol completeness. See the [checked commit](https://github.com/EVerest/EVerest/commit/2265c29a8dc0a841672012ccc0c31b00217174d8). Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream README](https://github.com/EVerest/EVerest/blob/2265c29a8dc0a841672012ccc0c31b00217174d8/README.md)
- [Deprecated EvseV2G manifest](https://github.com/EVerest/EVerest/blob/2265c29a8dc0a841672012ccc0c31b00217174d8/modules/EVSE/EvseV2G/manifest.yaml)
- [Evse15118D20 manifest](https://github.com/EVerest/EVerest/blob/2265c29a8dc0a841672012ccc0c31b00217174d8/modules/EVSE/Evse15118D20/manifest.yaml)
- [EvseSecurity manifest](https://github.com/EVerest/EVerest/blob/2265c29a8dc0a841672012ccc0c31b00217174d8/modules/EVSE/EvseSecurity/manifest.yaml)

## Related

- [CheckOCPP](checkocpp.md)
- [EmuOCPP](emuocpp.md)
- [OCPP and charging attacks](concepts/ocpp-charging-attacks.md)
- [dsV2Gshark](dsv2gshark.md)
- [WWCP_ISO15118](wwcp-iso15118.md)
- [pyPLC](pyplc.md)
