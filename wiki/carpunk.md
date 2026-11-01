---
title: "Carpunk"
summary: "CAN injection toolkit and successor to CANghost, automating interface setup, sniffing, replay, and injection attacks."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/souravbaghz/Carpunk"
status: active
last_checked: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "CAN injection toolkit and successor to CANghost, automating interface setup, sniffing, replay, and injection attacks."
related: [can-utils, icsim, cantot, cantoolz]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/souravbaghz/Carpunk"
    retrieved: 2026-10-31
---

CAN injection toolkit and successor to CANghost, automating interface setup, sniffing, replay, and injection attacks.

## What it is

A small Bash-driven CAN-injection toolkit by souravbaghz, developed from
CANghost.

## How it works

`carpunk.sh <interface>` presents a menu that orchestrates Linux `ip` and
[can-utils](can-utils.md) commands. It can bring the interface up or
down, run coloured `cansniffer` output, record with `candump -L`, replay
a selected log with `canplayer`, continuously send an all-zero frame as a
denial-of-service action, and send a UDS ECU-reset payload to the
functional diagnostic ID or a user-supplied arbitration ID. The README
says it supports both simulated and real vehicles and was tested on
Ubuntu and Parrot OS.

## Where it fits

Lightweight, menu-led SocketCAN exercises — sniffing, capture/replay,
reset, and bus-flooding demonstrations — without adopting a larger
framework. It is a worked miniature of the [CAN injection](concepts/can-injection.md)
pattern: nothing in the workflow authenticates the sender, because CAN
itself doesn't. Practise against [ICSim](icsim.md) on `vcan0`.

## Limits and notes

The script only changes interface up/down state; the user must load the
CAN driver manually. Restarting it can overwrite `carpunk1.log`, so the
README tells users to back up logs. The script header says educational
use only and not to use it on unauthorised vehicles, and the README
disclaims author liability for damage or illegal use. Its reset and DoS
functions are inherently disruptive even in a lab.

## Related

- [can-utils](can-utils.md) — every action it takes is a can-utils command.
- [ICSim](icsim.md) — the safe target for its exercises.
- [canTot](cantot.md) — the framework-scale version of packaged attacks.
- [CANToolz](cantoolz.md) — modular analysis and replay.
