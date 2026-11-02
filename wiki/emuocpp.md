---
uid: 01a19d3c-af82-7864-a3a6-f2160f96727b
title: "EmuOCPP"
summary: "Mininet-based emulator for OCPP charging networks covering versions 1.6, 2.0, and 2.0.1 across all three security profiles, with attack demos for the MitM…"
type: entity
category: "EV Charging Security"
url: "https://github.com/vfg27/EmuOCPP"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Mininet-based emulator for OCPP charging networks covering versions 1.6, 2.0, and 2.0.1 across all three security profiles, with attack demos for the MitM and downgrade flaws in its companion research."
related: [checkocpp, everest, ocpp-charging-attacks, ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/vfg27/EmuOCPP"
    retrieved: 2026-11-01
  - url: "https://github.com/vfg27/EmuOCPP/commit/1265fe7028ff538626dc5358e50c413420682135"
    retrieved: 2026-11-01
  - url: "https://github.com/vfg27/EmuOCPP/blob/1265fe7028ff538626dc5358e50c413420682135/README.md"
    retrieved: 2026-11-01
---

Mininet-based emulator for OCPP charging networks covering versions 1.6, 2.0, and 2.0.1 across all three security profiles, with attack demos for the MitM and downgrade flaws in its companion research.

## What it is

A Python OCPP emulator with Mininet/IPMininet network-topology support for charger/central-system experiments. Its README documents OCPP 1.6, 2.0, and 2.0.1 and security profiles 1, 2, and 3; it also permits operation without a profile. It is an emulated communication environment, not an electrical charging simulator.

## How it works

Client and server configuration files select the protocol and security settings. The repository includes certificate-generation support, client/server programs, transaction API helpers, scenario scripts, and topology editing/launching tools. The README reports testing on Ubuntu 20.04/22.04 VMs with Python 3.8–3.10, and describes a required OCPP 2.0 BootNotification schema replacement. [CheckOCPP](checkocpp.md), maintained separately, inspects the generated traffic.

## Where it fits

Use it to build repeatable lab topologies and vary transport/security configuration before investigating behaviour in a real implementation such as [EVerest](everest.md). The identity and transport threats are explained in [OCPP and charging attacks](concepts/ocpp-charging-attacks.md); the [OCPPStorm paper](ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations.md) supplies a complementary fuzzing perspective.

## Limits and safety notes

The README explicitly says OCPP 1.6 transaction emulation is unsupported. Its setup still refers to the older ocpp-simulator repository/folder name and contains dissector instructions despite the latest commit removing CheckOCPP contents; verify paths against the checkout. Scenario scripts illustrate behaviour of this implementation and selected configuration, not a finding that every charger or CSMS is vulnerable. The checked README does not establish comprehensive protocol conformance or enumerate every MitM/downgrade scenario promised by the canon description. Keep generated credentials and deliberately weak profiles confined to an authorised, isolated lab.

## Status and sources

Checked 2026-11-01. **Active** at this check: the repository is not archived and its latest default-branch commit is dated 2026-03-22. This records observed project activity, not a promise of support or protocol completeness. See the [checked commit](https://github.com/vfg27/EmuOCPP/commit/1265fe7028ff538626dc5358e50c413420682135). Documentation claims above come from the following primary sources; no hardware execution was performed.

- [Upstream README](https://github.com/vfg27/EmuOCPP/blob/1265fe7028ff538626dc5358e50c413420682135/README.md)

## Related

- [CheckOCPP](checkocpp.md)
- [EVerest](everest.md)
- [OCPP and charging attacks](concepts/ocpp-charging-attacks.md)
- [OCPPStorm paper](ocppstorm-a-comprehensive-fuzzing-tool-for-ocpp-implementations.md)
