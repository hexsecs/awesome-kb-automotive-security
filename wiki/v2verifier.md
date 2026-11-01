---
title: "V2Verifier"
summary: "Open-source V2X security testbed with first open-source IEEE 1609.2 implementation for DSRC and C-V2X."
type: entity
category: "V2X Security"
url: "https://github.com/twardokus/v2verifier"
status: maintenance
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source V2X security testbed with first open-source IEEE 1609.2 implementation for DSRC and C-V2X."
related: [f2md, vanetza, artery, misbehavior-detection, v2x-credential-management]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/twardokus/v2verifier"
    retrieved: 2026-11-01
---

Open-source V2X security testbed with first open-source IEEE 1609.2 implementation for DSRC and C-V2X.

## What it is

An open-source, over-the-air V2X security testbed from RIT's Wireless Systems and Internet of Things (WISP) lab — the section's counterpoint to its simulators, because it works with real radios. Its core asset is the first open-source implementation of **IEEE 1609.2** (message signing/verification and V2V certificates), alongside WSMP (IEEE 1609.3) networking. Published work anchored on it includes an ICC 2021 targeted-discreditation attack paper and a CNERT 2021 evaluation of the SDR testbed design (DOIs recorded in the project's own wiki). Licence: MIT per the repo's LICENSE file (GitHub's licence detector reports NOASSERTION — the discrepancy is recorded here rather than resolved by assertion).

## How it works

The DSRC path is built on GNU Radio 3.10 with the WiME lab's gr-ieee802-11 out-of-tree module, driving USRP software-defined radios; the 1609.2 implementation signs and verifies BSM traffic and handles V2V certificates. A `--test` socket mode runs without SDRs — one transmitter emulates up to ten vehicles — which is the bench path when no RF hardware is available. Two flags from the project's own documentation define the current state and are kept prominent: the README warns that `master` is **mid-redesign and "will likely not work"**, and **C-V2X support is temporarily removed** in the 3.0 line pending fixes in its srsRAN dependency — so the list description's "for DSRC and C-V2X" is historical for the current code, not a present capability. The supported platform is Ubuntu 20.04; the docs actively discourage running it in a virtual machine.

## Where it fits

The over-the-air end of the section: where [F2MD](f2md.md) simulates the misbehavior-detection chain and [Artery](artery.md)/[Veins](veins.md) simulate traffic and stacks, V2Verifier transmits and receives real 802.11p frames with real 1609.2 security applied — the place to test whether a signed-message attack or defence survives contact with an actual PHY. Against [Vanetza](vanetza.md) it is the US-stack counterpart: 1609.2 implemented end-to-end here, versus Vanetza's ETSI TS 103 097 implementation with 1609.2 present only as shipped ASN.1 definitions.

## Limits and safety notes

The two README flags above *are* the limits: a mid-redesign master that likely does not work as-is, and no C-V2X in the current line — anyone building on it should start from the v3.0.1 release and the project's wiki, not from master, and should treat DSRC as the supported radio. Over-the-air transmission is real RF: the testbed transmits on DSRC channels, which carries the ordinary regulatory and lab-discipline obligations of SDR work and confines sensible use to a bench/shielded setting. Ubuntu 20.04 only, with VMs discouraged, narrows the bench further.

## Status and sources

Checked 2026-11-01. **Maintenance**: not archived; nine releases run from v0.9 (2020-04-29) to v3.0.1 (2023-08-15), master commits end 2024-11-04, and the repository still received a push in April 2025 on its redesign branches — sporadic life around a published testbed, short of active development. Documentation claims above come from the following primary sources; no transmission was made for this page.

- [Upstream repository](https://github.com/twardokus/v2verifier)

## Related

- [F2MD](f2md.md)
- [Vanetza](vanetza.md)
- [Artery](artery.md)
