---
title: "panda"
summary: "Open-source CAN and CAN FD interface firmware from comma.ai running on an STM32H725, with Python bindings for full read/write access to vehicle buses."
type: entity
category: "Hardware Interfaces"
url: "https://github.com/commaai/panda"
status: active
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source CAN and CAN FD interface firmware from comma.ai running on an STM32H725, with Python bindings for full read/write access to vehicle buses."
related: [cantact, ramn]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/commaai/panda"
    retrieved: 2026-11-01
  - url: "https://github.com/commaai/panda/blob/master/README.md"
    retrieved: 2026-11-01
---

Open-source CAN and CAN FD interface firmware from comma.ai running on an STM32H725, with Python bindings for full read/write access to vehicle buses.

## What it is

comma.ai's CAN interface: firmware (MIT licence) for the panda board family — STM32H7-based hardware with **three CAN buses** (CAN FD capable) plus a GMLAN bus — together with the Python library that drives it. panda exists because comma's driving-assistance work needs a computer permanently interposed on a car's buses; it is the interface inside comma devices, published openly rather than kept as internal tooling.

## How it works

A host talks to the board over USB (Wi-Fi on equipped variants) through the Python API: enumerate buses, receive frames, transmit frames, set safety configuration. The defining feature is the on-device **safety layer**: per-car safety policies in the firmware check every transmitted frame against rules for that vehicle (which messages may be sent, with what values, under what conditions — steering torque limits and the like), and heartbeat/watchdog logic forces a safe state if the host misbehaves. Configuration flags (`unsafe_mode` bits in the safety code govern behaviours such as disengage-on-gas) tune the policy; the model is "the interface itself refuses impermissible traffic", not "the application promises to behave".

## Where it fits

panda is the outlier of this section in a productive direction: every other interface here will transmit whatever the host asks, while panda treats transmission as a safety-critical act to be policed in firmware — because in its native use a laptop bug becomes a steering input. For research, that cuts both ways (see Limits). As a multi-bus FD interface with a maintained Python API it is also simply one of the most capable open options — compare [CANtact](cantact.md)'s single classic channel. [RAMN](ramn.md) is its conceptual opposite number: a network you may attack freely because it is not a car.

## Limits and safety notes

The safety layer is a research constraint as well as a protection: arbitrary injection experiments fight the per-car policy, and bypassing it means modifying safety-critical firmware — the repository's own warnings about development on live vehicles apply with force. Safety policies exist per supported car; an unsupported vehicle has no policy, which is not the same as a permissive one being safe. This page relies only on the panda repository's own documentation; product claims about comma devices belong to comma's product pages, not here.

## Status and sources

Checked 2026-11-01. **Active**: the repository is not archived, commits land continuously (most recent 2026-10-30), and the firmware version header advanced to 0.0.10 in September 2026. This records observed project activity, not a promise of support. Documentation claims above come from the following primary sources; no hardware was run for this page.

- [Upstream repository](https://github.com/commaai/panda)
- [Upstream README](https://github.com/commaai/panda/blob/master/README.md)

## Related

- [CANtact](cantact.md)
- [RAMN](ramn.md)
