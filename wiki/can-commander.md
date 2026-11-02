---
uid: 01a19d3c-af3f-785c-8f5a-0c7bd57532c1
title: "CAN Commander"
summary: "Flipper Zero application and companion ESP32 CAN board for reverse engineering vehicle networks, with sniffing, DBC decoding, replay, and injection profiles…"
type: entity
category: "CAN Bus Analysis"
url: "https://github.com/MatthewKuKanich/CAN_Commander"
status: active
last_checked: 2026-10-31
created: 2026-10-31
updated: 2026-10-31
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Flipper Zero application and companion ESP32 CAN board for reverse engineering vehicle networks, with sniffing, DBC decoding, replay, and injection profiles usable without a laptop."
related: [savvycan, caringcaribou, icsim]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/MatthewKuKanich/CAN_Commander"
    retrieved: 2026-10-31
---

Flipper Zero application and companion ESP32 CAN board for reverse engineering vehicle networks, with sniffing, DBC decoding, replay, and injection profiles usable without a laptop.

## What it is

A two-part field tool for CAN reverse engineering: a Flipper Zero app plus
a companion ESP32-based CAN board with dual CAN ports (`can0` right /
primary, `can1` left). Maintained by Matthew KuKanich.

## How it works

The Flipper app is a UART-driven controller: it sends tool and config
actions over UART, the ESP32 firmware executes the CAN operations and
streams events back, and the Flipper renders dashboards and owns profiles
and storage. DBC and injection profiles (`.dbcprof` / `.injprof`) are
authored in a web tool at cancommander.com and loaded from SD. The board
can also expose its full CLI over its own Wi-Fi access point as a raw TCP
socket, concurrently with the Flipper session.

Two workflows define it: **Auto Reverse Engineer**, a two-phase flow where
a calibration pass builds a noise blacklist and monitoring then surfaces
changed IDs, feeding Bit Tracker or Replay; and **Smart Injection**, which
tracks live frames for selected IDs and swaps only the targeted bits or
fields in-frame.

## Where it fits

Laptop-free, in-vehicle reverse engineering: finding which IDs and bits
change with an action, replaying a captured sequence with original timing,
and quick OBD-II diagnostics (live PIDs, VIN, DTC read/clear). Practice
against [ICSim](icsim.md) before touching a real bus.

## Limits and notes

App v2.3.1 requires ESP32 firmware ≥ v2.2 (checked by handshake at boot).
Smart Injection is capped at 5 slots per profile, the DBC cache at 16
signals, and the replay buffer at 384 frames per recording. Streaming the
Flipper screen during DBC decode can exhaust RAM, and very heavy traffic
still needs filtering. The Wi-Fi CLI ships with a default AP password that
the README explicitly tells users to change.

## Related

- [SavvyCAN](savvycan.md) — the laptop-side capture/RE counterpart.
- [CaringCaribou](caringcaribou.md) — scripted ECU discovery and exploration.
- [ICSim](icsim.md) — safe virtual instrument cluster for practice.
