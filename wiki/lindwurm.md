---
title: "Lindwurm"
summary: "Open-source CAN bus tracing and fuzzing tool designed for penetration testing with Burp Suite-inspired workflow."
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/lindwurm-can/lindwurm"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source CAN bus tracing and fuzzing tool designed for penetration testing with Burp Suite-inspired workflow."
related: [canalyzat0r, savvycan, can-utils]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/lindwurm-can/lindwurm"
    retrieved: 2026-10-31
  - url: "https://www.lindwurm-can.org/index.html"
    retrieved: 2026-10-31
---

Open-source CAN bus tracing and fuzzing tool designed for penetration testing with Burp Suite-inspired workflow.

## What it is

A C++/Qt CAN tracing and fuzzing application aimed specifically at
penetration testers, modelled on Burp Suite's workflow with
Wireshark-style display filters. Published under the `lindwurm-can`
organisation; the site and README are first-person (contact given as
"Sascha" at lindwurm-can.org).

## How it works

The Qt CAN interface manager can connect several interfaces at once. The
tracer shows frames chronologically or in a fixed view, with copy/paste
display filters (filter history and favourites; filters can be created
from selected frames). Traced frames can be sent straight to the composer
for replay; the composer edits frames as plain text and expands ID and
data byte ranges (for example `123-124 01 00-FF 33`) for fuzzing, with
multiple sending tabs per scenario. Two interfaces can be bridged to put
the tool man-in-the-middle between an ECU and the rest of the bus, using
direction to attribute frames to ECUs.

## Where it fits

Manual, interactive ECU penetration testing — observe, filter, replay,
mutate — especially bench setups and split-bus attribution. Where
[CANalyzat0r](canalyzat0r.md) organises the same work around projects,
Lindwurm organises it around the intercept-and-modify loop.

## Limits and notes

It is explicitly a first public **alpha**: "functions are buggy and
erroneous or not yet fully implemented. Keep in mind if you using it on a
*real* car!" — and its disclaimer says use at your own risk, especially
on a real car. Despite the cross-platform aim it was only tested with
Qt 5.15.2 on Linux; some Qt CAN plugins (TinyCAN, PeakCAN) don't
implement loopback/local echo, with SocketCAN as the workaround. DBC and
signal decoding, UDS tools, and transport-protocol support are listed as
*planned*, not present.

## Related

- [CANalyzat0r](canalyzat0r.md) — project-based GUI security analysis.
- [SavvyCAN](savvycan.md) — the mature capture/RE GUI.
- [can-utils](can-utils.md) — the command-line base layer.
