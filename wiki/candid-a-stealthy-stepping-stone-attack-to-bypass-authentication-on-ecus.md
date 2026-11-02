---
uid: 01a19d3c-af43-72ae-97c1-79df9d111a7e
title: "CANdid: A Stealthy Stepping-Stone Attack to Bypass Authentication on ECUs"
summary: "Kulandaivel, Jain, Guajardo, and Sekar, escar USA 2022. Shows a compromised ECU can authenticate against a safety-critical ECU's SecurityAccess without the…"
type: entity
category: "Conference Presentations"
url: "https://zenodo.org/records/18714273"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Kulandaivel, Jain, Guajardo, and Sekar, escar USA 2022. Shows a compromised ECU can authenticate against a safety-critical ECU's SecurityAccess without the failed attempts a CAN IDS would flag."
sources:
  - url: "https://zenodo.org/records/18714273"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - uds-seed-key
  - silently-disabling-ecus-and-enabling-blind-attacks-on-the-can-bus
---

Kulandaivel, Jain, Guajardo, and Sekar, escar USA 2022. Shows a compromised ECU can authenticate against a safety-critical ECU's SecurityAccess without the failed attempts a CAN IDS would flag.

An escar USA 2022 paper and talk by Sekar Kulandaivel, Shalabh Jain, Jorge Guajardo, and Vyas Sekar. CANdid asks whether an ECU an attacker already controls can be used as a stepping stone to reprogram a safety-critical ECU on the same CAN bus. The adversary snoops a legitimate technician firmware-update session and records a valid SecurityAccess challenge–response pair; it then forces the target ECU to re-issue the *same* challenge — modern ECUs commonly seed challenge randomness from processor uptime, and the attacker controls uptime via the unprivileged UDS ECUReset service, with a timing technique to raise the repeat probability further — and replays the recorded response. Authentication on a real powertrain ECU was bypassed in a handful of attempts, few enough that a CAN IDS watching for brute-force failures sees nothing, and the authors demonstrated uploading code to it; other powertrain and gateway ECUs also showed high challenge-repeat likelihood.

What you get: the full paper (PDF) deposited on Zenodo — substantially more than slides, including the timing analysis. Read it if you design or assess UDS SecurityAccess, seed/key schemes, or IDS detection assumptions. Caveat: it is a second-stage attack — it presupposes a compromised ECU on the bus and a captured legitimate update session — not an initial entry point.

## Status and sources

Status: **published** — escar USA 2022; paper PDF public. Verified against the proceedings deposit at [zenodo.org/records/18714273](https://zenodo.org/records/18714273) (the stub's resource), 2026-11-01.

## Related

- [UDS seed/key](concepts/uds-seed-key.md) — the concept page; CANdid is the replay-against-weak-seed-randomness instance
- [Silently Disabling ECUs and Enabling Blind Attacks on the CAN Bus](silently-disabling-ecus-and-enabling-blind-attacks-on-the-can-bus.md) — another attack that turns a trusted bus participant against the bus
