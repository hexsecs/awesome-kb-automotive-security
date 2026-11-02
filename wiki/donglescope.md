---
title: "DongleScope"
summary: "Automated tool for detecting vulnerabilities in wireless OBD-II dongles based on USENIX Security 2020 research."
type: entity
category: "Penetration Testing"
url: "https://github.com/OSUSecLab/DongleScope"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Automated tool for detecting vulnerabilities in wireless OBD-II dongles based on USENIX Security 2020 research."
related: [plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles, pwnobd]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/OSUSecLab/DongleScope"
    retrieved: 2026-11-01
  - url: "https://github.com/OSUSecLab/DongleScope/blob/master/README.md"
    retrieved: 2026-11-01
  - url: "https://www.usenix.org/conference/usenixsecurity20/presentation/wen"
    retrieved: 2026-11-01
---

Automated tool for detecting vulnerabilities in wireless OBD-II dongles based on USENIX Security 2020 research.

## What it is

The automated testing tool from the USENIX Security 2020 paper "Plug-N-Pwned: Comprehensive Vulnerability Analysis of OBD-II Dongles as A New Over-the-Air Attack Surface in Automotive IoT" (OSU Security Lab). It tests wireless OBD-II dongles — Wi-Fi, Bluetooth Classic, and BLE models — for the vulnerability class the paper documents: a dongle that bridges an attacker's wireless connection to the vehicle's CAN bus without adequate authentication or message filtering. Four tests are implemented: read, write, filter, and fuzzing.

## How it works

The tool is a small Python program (`main.py`, `OBDPeripheral.py`, `settings.py`, driven by `config.json`) that talks to the dongle under test the way its phone app would — over Wi-Fi (TCP), Bluetooth Classic, or BLE, using PyBluez/pyble for the Bluetooth paths — and speaks ELM327-style AT commands and OBD PIDs through it (the README's worked example reads the VIN via PID `09 02`). The four tests: a **read test** (read the VIN through the dongle); a **write test** (ship CAN messages that change the odometer unit on a Toyota RAV4, proving write reach into the vehicle); a **filter test** (inject 10 arbitrary CAN messages to test whether the dongle filters what may pass); and a **fuzzing test** (fuzz through the dongle — see the safety note). The dongle under test must be plugged into a real vehicle's OBD-II port; the repository also carries a `ResponsibleDisclosure.md`.

## Where it fits

The aftermarket-dongle attack-surface entry: its subject is neither the vehicle nor the diagnostic protocol but the cheap wireless adapter as an unauthenticated bridge between them. The paper has its own page in this KB ([Plug-N-Pwned](plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles.md)); this page is the tool artefact of the same research. In this section it is the detection-side counterpart to [pwnobd](pwnobd.md), which attacks the same device class from the exploitation side.

## Limits and safety notes

The README's own warning is explicit: the fuzzing test "is very **dangerous** and will cause unpredicted consequences, we strongly recommend you do not try this on a vehicle in use". Testing requires a real automobile and the physical dongle. The write test's payload is specific to one vehicle (Toyota RAV4 odometer unit). The implementation stack — Python 2.7 on macOS, PyBluez/pyble — is obsolete, so running it today is itself a porting exercise; the durable value is the test design and the paper's findings.

## Status and sources

Checked 2026-11-01. **Unknown**: the repository is **not** archived — the archived flag is false, verified via the API, despite the repository's age — but its latest commit is 2020-07-27 and there are no releases. It is the finished code artefact of a 2020 paper; no ongoing project state is observable. Documentation claims above come from the following primary sources; no dongle was tested for this page.

- [Upstream repository](https://github.com/OSUSecLab/DongleScope)
- [Upstream README](https://github.com/OSUSecLab/DongleScope/blob/master/README.md)
- [Paper (USENIX Security 20)](https://www.usenix.org/conference/usenixsecurity20/presentation/wen)

## Related

- [Plug-N-Pwned (paper)](plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles.md)
- [pwnobd](pwnobd.md)
