---
uid: 01a1e6dc-fe94-7430-9859-2179ced3db34
title: "Bypassing Debug Password Protection on the RH850 Family"
summary: "Quarkslab walkthrough of defeating the 16-byte IDCODE debug lock on Renesas RH850 ECU microcontrollers with crowbar voltage glitching, using a ChipWhisperer…"
type: entity
category: "Learning Resources"
url: "https://blog.quarkslab.com/bypassing-debug-password-protection-on-the-rh850-family-using-fault-injection.html"
status: published
last_checked: 2026-11-17
created: 2026-11-15
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: a570090
list_summary: "Quarkslab walkthrough of defeating the 16-byte IDCODE debug lock on Renesas RH850 ECU microcontrollers with crowbar voltage glitching, using a ChipWhisperer Husky or a low-cost Pico Glitcher."
related:
  - ghidra-v850
  - back-in-the-driver-s-seat-recovering-critical-data-from-tesla-autopilot-using-voltage-glitching
  - survey-on-security-threats-and-protection-mechanisms-in-embedded-automotive-networks
  - ford-ecu-bruteforcer
  - idrive7-8-ssh-root
  - firmware-acquisition
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-15
  - url: "https://blog.quarkslab.com/bypassing-debug-password-protection-on-the-rh850-family-using-fault-injection.html"
    retrieved: 2026-11-17
facets: [hardware, attack, learning]
---

Quarkslab walkthrough of defeating the 16-byte IDCODE debug lock on Renesas RH850 ECU microcontrollers with crowbar voltage glitching, using a ChipWhisperer Husky or a low-cost Pico Glitcher.

## What it is

A March 2026 Quarkslab blog post by Philippe Azalbert describing how the team reliably bypassed the 16-byte IDCODE password that locks debug access on several Renesas RH850 variants. RH850 is a family of 32-bit automotive microcontrollers and, in Quarkslab's words, the ones most often found in the ECUs they audit. Being able to bypass the lock matters in a black-box assessment because it lets you retrieve and reverse the firmware, and under UNECE R155 it is a direct check of whether an attacker can alter firmware. The post builds on earlier public work by Franck Jullien on the RX65 and by Willem Melching on an RH850/P1M-E in 2022.

## How it works

Renesas's proprietary debug protocol runs over 1- or 2-wire UART. A probe sends roughly ten `0x00` bytes; with FLMD0 held high the chip replies `0x00`, a `0x55` connect command gets `0xC1`, speeds are negotiated, and a SYNC command leads the chip to report debug access as granted, password-protected or prohibited. Crucially, the initialisation is still allowed even when access is disabled, which gives an attacker something to observe.

The attack is a **crowbar voltage glitch**: briefly shorting a supply rail to ground through a MOSFET. Rather than VCC, Quarkslab targeted the `ISOVCL` pin feeding the internal regulator that powers the CPU subsystem and code flash on the RH850/F1KM-S4 (G3KH, 240 MHz, ASIL-B), after removing its capacitor and soldering on an SMA connector. A glitch needs a trigger, an offset and a width; the trigger is what makes an attack repeatable. Their first attempt used the byte before the password checksum as a UART trigger, but roughly 80 µs of jitter made it unreliable — one successful bypass took days of brute force.

The reliable version came from simple power analysis. A second SMA connector on `ISOVCL` fed the ChipWhisperer Husky's 12-bit, 200 MS/s ADC, revealing a repeatable ~4 µs pattern when the password was checked. The Husky's SAD trigger was not selective enough, so they used its trigger sequencer: UART trigger first, then an ADC trigger at 80% of the pattern's highest spike. That reduced the search to about one minute — a successful response `81 00 01 3a c5 03` at delay 537, width 18, in 88 attempts, followed by an option-0x3A read identifying an R7F701648. The pattern held across their other RH850 ECUs; only the ADC threshold varied slightly, and each locked ECU fell within minutes after removing `ISOVCL` capacitors and measuring one sample trace. The post also describes automatically resetting IDCODE to `16 × 0xFF` on a successful glitch to get read/write firmware access, and a "poor man" reproduction with a €30–50 Pico Glitcher v3: custom PIO trigger logic, a ~5 µs window, and about 7,000 attempts versus ~100 with the Husky.

## Where it fits

This is the hardware-side analogue of [back-in-the-driver's-seat voltage glitching](back-in-the-driver-s-seat-recovering-critical-data-from-tesla-autopilot-using-voltage-glitching.md): both use fault injection to defeat a protection mechanism, and both land in an ECU's firmware. [GHIDRA V850](ghidra-v850.md) is the natural next step once a dump exists, and [Ford ECU bruteforcer](ford-ecu-bruteforcer.md) covers a different approach to the same access problem. The broader threat context is in [survey on security threats and protection mechanisms in embedded automotive networks](survey-on-security-threats-and-protection-mechanisms-in-embedded-automotive-networks.md), while [idrive7-8-ssh-root](idrive7-8-ssh-root.md) shows the same goal reached through a head unit's debug interface.

## Limits and safety notes

This is a physical, invasive technique: opening the ECU, identifying `ISOVCL`, removing capacitors and soldering an SMA connector permanently alter the board, and a wrong glitch can damage it. It needs the target part in scope — the post documents F1KM-S4 and a set of lab ECUs, not the whole RH850 family — and the ADC threshold must be measured per board. The parameter search can take from ~70 seconds to many hours depending on the trigger and hardware. All results, including the attempt counts, are the author's, not independently reproduced here; no fault injection was performed for this page. Treat it as authorised-audit material: extracting firmware from a vehicle you do not own or have permission to test is not a legitimate use.

## Status and sources

Checked 2026-11-17. **Published** — the post is dated 2026-03-05 and is a static technical article, not a maintained tool.

- [Quarkslab blog post](https://blog.quarkslab.com/bypassing-debug-password-protection-on-the-rh850-family-using-fault-injection.html)

## Related

- [GHIDRA V850](ghidra-v850.md)
- [Back in the driver's seat: recovering critical data from Tesla Autopilot using voltage glitching](back-in-the-driver-s-seat-recovering-critical-data-from-tesla-autopilot-using-voltage-glitching.md)
- [Survey on security threats and protection mechanisms in embedded automotive networks](survey-on-security-threats-and-protection-mechanisms-in-embedded-automotive-networks.md)
- [Ford ECU bruteforcer](ford-ecu-bruteforcer.md)
- [idrive7-8-ssh-root](idrive7-8-ssh-root.md)
- [Firmware acquisition: the read-side channels](concepts/firmware-acquisition.md)
