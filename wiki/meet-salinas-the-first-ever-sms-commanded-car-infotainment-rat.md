---
uid: 01a1d439-cc58-7ac4-ac79-a2cfa5633587
title: "Meet Salinas: The First Ever SMS-Commanded Car Infotainment RAT"
summary: "Regalado, DEF CON 26 Car Hacking Village 2018. Shows how a production infotainment unit can be infected with malware that exfiltrates the driver's data…"
type: entity
category: "Conference Presentations"
url: "https://media.defcon.org/DEF%20CON%2026/DEF%20CON%2026%20villages/DEF%20CON%2026%20villages%20captions/DEF%20CON%2026%20-%20CAR%20HACKING%20VILLAGE%20-%20Dan%20Regalado%20-%20Meet%20Salinas%20the%20first%20ever%20SMS-commanded%20Car%20Infotainment%20RAT.eng.srt"
status: published
last_checked: 2026-11-17
created: 2026-11-13
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 6a8b17c
list_summary: "Regalado, DEF CON 26 Car Hacking Village 2018. Shows how a production infotainment unit can be infected with malware that exfiltrates the driver's data through SMS via the paired phone."
related:
  - car-hacking-village
  - security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study
  - external-attack-surface
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-13
  - url: "https://media.defcon.org/DEF%20CON%2026/DEF%20CON%2026%20villages/DEF%20CON%2026%20villages%20captions/DEF%20CON%2026%20-%20CAR%20HACKING%20VILLAGE%20-%20Dan%20Regalado%20-%20Meet%20Salinas%20the%20first%20ever%20SMS-commanded%20Car%20Infotainment%20RAT.eng.srt"
    retrieved: 2026-11-17
facets: [can, ivi, research]
---

Regalado, DEF CON 26 Car Hacking Village 2018. Shows how a production infotainment unit can be infected with malware that exfiltrates the driver's data through SMS via the paired phone.

## What it is

A DEF CON 26 Car Hacking Village talk (2018) by Dan Regalado, presented as a three-person effort. "Salinas" is an SMS-commanded remote access trojan (RAT) for a production car infotainment unit. The researchers' insight was to use the driver's **paired phone** as the command-and-control channel: rather than relying on a car's often-unstable built-in internet connection, the malware reads and writes SMS messages through the phone to move data back and forth. The talk ends with a live demo stealing SMS messages from a bench unit.

## How it works

The work started with **Cardloop**, an OBD2 dongle with a Particle microcontroller that can be programmed to monitor OBD2/CAN traffic. The team found that only the lights could be controlled over OBD2, so they pivoted to the driver: people routinely pair their phones with the car while driving, and a paired phone gives a stable two-way channel. That makes the privacy impact the point — the RAT's goal is to steal the driver's SMS data, not to drive the car.

They bought a matching infotainment unit on eBay (noting that the pigtail connectors are essential) and built a standalone bench. The unit runs **Linux ARM on a Freescale i.MX6**, 32-bit, with Bluetooth, JTAG, a Renesas CAN controller, GPS, a backup camera, and — importantly — **USB Ethernet**: the USB port that looks like a charging/MP3 port carries Ethernet. The wiring diagram was obtained from a leak on the internet, which let them connect the hardware.

The intrusion path has several stages:

- **Initial access via USB auto-run.** A file on an inserted USB triggers an INI-driven auto-run that checks for an `execute.ini` and runs a command through `system()`, giving a foothold.
- **Persistence.** The RAT is added to the XML configuration of an existing SMS service so it starts on every boot.
- **Debugging the services.** A watchdog resets a stopped service after about three seconds at a breakpoint; bypass options were killing the SMS service manager or setting a GPIO flag. To set GDB breakpoints in ARM Linux services, they patched the target instruction with an undefined-instruction trap (P-trace code), let the trap stop the debugger, then restored the original bytes and continued.
- **A manufacturer test client.** A leftover test app talks to a test-app server using XML commands; the team found an `AT+TMC` command prefix that let them drive the car through this channel and, among other things, reset the phone's Bluetooth pairing.
- **SMS internals.** A JavaScript front end in Opera talks over WebSockets to a multimedia unit interface; incoming SMS passes through a service handler and the MSG library into an SMS notification callback and is stored in an **unencrypted SQLite database**. The `attachment` and `message` tables are the interesting ones; watching the `attachment` table reveals when a new message arrives. Stealing the session between the paired phone and the infotainment then gives control of SMS messaging.

The reverse-engineering was substantial: understanding the component graph took the team weeks, and one member spent about three weeks statically compiling the needed libraries.

## Where it fits

This is a Car Hacking Village investigation of the infotainment/telematics privacy surface. [Car Hacking Village](car-hacking-village.md) is the parent session. [Security and privacy vulnerabilities of in-car wireless networks: a tire pressure monitoring system case study](security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study.md) is the other wireless-privacy case in the corpus. The later [Over the Air: Compromise of Modern Volkswagen Group Vehicles](over-the-air-compromise-of-modern-volkswagen-group-vehicles.md) and [DriveThru: car hacking, fast food, faster data breach](drivethru-car-hacking-fast-food-faster-data-breach.md) show the same infotainment boundary being crossed on other platforms; [Back to the connected car](back-connect-to-the-connected-car-search-for-vulnerabilities-in-the-vw-electric-car.md) is the related VW-side work.

## Limits and safety notes

The primary source is an **auto-generated caption transcript**, so product names and commands are transcribed imperfectly and the specifics above are the speakers' account, not independently reproduced here. No vendor or vehicle model is named, and the demo runs on a **standalone bench unit**, not a remote compromise of a moving car: planting the initial USB file requires physical access or an already-compromised path. The claim to be "first ever" is the presenters'. The RAT reads and writes the paired phone's SMS — a privacy attack with real-world harm, which is why the responsible framing is defensive. No malware, vehicle or infotainment unit was tested for this page.

## Status and sources

Checked 2026-11-17. **Published** — DEF CON 26 Car Hacking Village, 2018; official caption transcript hosted by DEF CON.

- [DEF CON 26 caption transcript](https://media.defcon.org/DEF%20CON%2026/DEF%20CON%2026%20villages/DEF%20CON%2026%20villages%20captions/DEF%20CON%2026%20-%20CAR%20HACKING%20VILLAGE%20-%20Dan%20Regalado%20-%20Meet%20Salinas%20the%20first%20ever%20SMS-commanded%20Car%20Infotainment%20RAT.eng.srt)

## Related

- [Car Hacking Village](car-hacking-village.md)
- [Security and privacy vulnerabilities of in-car wireless networks: a tire pressure monitoring system case study](security-and-privacy-vulnerabilities-of-in-car-wireless-networks-a-tire-pressure-monitoring-system-case-study.md)
- [The vehicle's external attack surface: remote entry and the telematics pivot](concepts/external-attack-surface.md)
