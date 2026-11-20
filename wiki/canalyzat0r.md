---
uid: 01a19d3c-af42-7a8f-b5af-4aacbbcb758e
title: "CANalyzat0r"
summary: "Security analysis toolkit for proprietary car protocols with graphical sniffing, fuzzing, packet comparison, background-noise filtering, and UDS fuzzing."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/schutzwerk/CANalyzat0r"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Security analysis toolkit for proprietary car protocols with graphical sniffing, fuzzing, packet comparison, background-noise filtering, and UDS fuzzing."
related:
  - icsim
  - savvycan
  - cantoolz
  - automated-cross-platform-reverse-engineering-of-can-bus-commands-from-mobile-apps
  - can-injection
  - canflict
  - canter
  - canvas-fast-and-inexpensive-automotive-network-mapping
  - caringcaribou
  - lindwurm
  - pycangui
  - diagnostic-fuzzing
license: GPL-3.0
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/schutzwerk/CANalyzat0r"
    retrieved: 2026-10-31
facets: [can, diagnostics, attack, tools]
---

Security analysis toolkit for proprietary car protocols with graphical sniffing, fuzzing, packet comparison, background-noise filtering, and UDS fuzzing.

## What it is

A GUI security-analysis toolkit for proprietary car protocols. It
originated as Philipp Schmied's bachelor's thesis at SCHUTZWERK in
collaboration with Aalen University and is hosted under the schutzwerk
organisation. GPLv3.

## How it works

A single tabbed Qt GUI over SocketCAN — it can load kernel modules and
manage physical and virtual SocketCAN devices itself, supports multiple
interfaces, and handles CAN FD. Work is organised into database-backed
projects (findings, dumps, and known packets per project; projects
import/export as human-readable JSON, and all actions are logged).
Analysis tabs run threaded sniffing, sending, and fuzzing. The distinctive
mechanisms are background-noise filtering to isolate action-specific
packets, binary packet filtering with randomisation, dump comparison, and
basic UDS fuzzing. All SocketCAN adapters should work in general; it is
tested with 8devices USB2CAN (CAN) and PEAK PCAN-USB Pro FD (CAN FD).

The [README](https://github.com/schutzwerk/CANalyzat0r), rechecked
2026-11-17, describes SQLite support and editable JSON project exchange.
These are complementary: the database keeps an engagement's working
state, while exported JSON lets another analyst inspect or transfer the
project without treating a screenshot as the only record. Known packets,
findings, and dumps remain associated with the project rather than being
an unlabelled stream of hexadecimal bytes.

For action isolation, first collect normal traffic, then capture traffic
while exercising one control. Background-noise filtering and dump
comparison help reduce the candidates; the GUI can filter unique packets
by ID alone or by the combination of ID and data. Those choices answer
different questions: ID-only uniqueness groups changing payloads under
one identifier, whereas ID-and-data uniqueness retains distinct payloads.
The README also documents ignoring packets during sniffing and pasting
SocketCAN files into compatible tables, so captured evidence can be reused
across tabs rather than manually retyped.

Sending, sniffing, and fuzzing run in separate threads, with multiple
analysis threads available in one window. Values can be changed while
fuzzing is running. That enables an interactive bench experiment, but
does not itself supply a test oracle: observing a changed packet or a
dashboard reaction still requires interpretation and a repeatable baseline.

## Where it fits

Structured protocol-reversing engagements on an unknown bus — especially
the "do an action, find which packets changed" workflow — with findings
managed per project. The README itself suggests [ICSim](icsim.md) as the
safe practice target.

## Limits and notes

The application must run as superuser (its troubleshooting section is
explicit, including the `sudo -E` environment-preservation workaround);
the Docker build is the currently recommended install route. No
usage-safety disclaimer was found in the README.

UDS fuzzing is explicitly described as **basic** support, not evidence of
complete diagnostic-service coverage, automatic security-access handling,
or ECU firmware extraction. SocketCAN compatibility is broader than the
two tested adapters, but the named tests are not a compatibility guarantee
for every adapter, driver, or CAN FD setup.

## Related

- [ICSim](icsim.md) — the safe practice target the README recommends.
- [SavvyCAN](savvycan.md) — capture analysis and RE without the project layer.
- [CANToolz](cantoolz.md) — modular black-box analysis framework.

The [CAN injection](concepts/can-injection.md) concept separates passive
candidate discovery from active replay. [Diagnostic fuzzing](concepts/diagnostic-fuzzing.md)
explains why a fuzzing interface still needs a controlled target and
observable failure criteria.
