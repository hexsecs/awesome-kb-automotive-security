---
title: "Fast and Compromised: Automotive Security on a Timer"
summary: "Ziv and Alfasi, escar USA 2025. Penetration test taking a production electric vehicle from an insecure Wi-Fi network to full compromise in eight working…"
type: entity
category: "Conference Presentations"
url: "https://zenodo.org/records/18716321"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Ziv and Alfasi, escar USA 2025. Penetration test taking a production electric vehicle from an insecure Wi-Fi network to full compromise in eight working days, via hardcoded credentials, insecure MQTT, and weak UDS Security Access."
sources:
  - url: "https://zenodo.org/records/18716321"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - fast-and-vulnerable-a-story-of-telematic-failures
  - uds-seed-key
---

Ziv and Alfasi, escar USA 2025. Penetration test taking a production electric vehicle from an insecure Wi-Fi network to full compromise in eight working days, via hardcoded credentials, insecure MQTT, and weak UDS Security Access.

An escar USA 2025 paper by Omer Ziv and Erez Alfasi: a time-boxed, real-world penetration test of a production-ready electric vehicle that went from minimal access — an insecure Wi-Fi network — to full compromise within eight working days. The chain ran through hardcoded credentials, insecure MQTT communication, and a weak UDS SecurityAccess implementation, and ended with remote control over safety-critical systems and effective vehicle theft. The authors frame the lessons as defensive basics: secure boot, proper credential management, and robust in-vehicle network protection.

What you get: the full paper (PDF) on Zenodo — a compact case study rather than a slide deck, and a useful realistic example of how unglamorous findings chain into total compromise in a modern EV. Caveats: the vehicle and vendor are anonymised, so you cannot check the claims against a specific product, and the eight-day figure reflects this team's starting access and the target's state — it is an existence proof, not a benchmark for other vehicles.

## Status and sources

Status: **published** — escar USA 2025; paper PDF public. Verified against the proceedings deposit at [zenodo.org/records/18716321](https://zenodo.org/records/18716321) (the stub's resource), 2026-11-01.

## Related

- [Fast and Vulnerable: A Story of Telematic Failures](fast-and-vulnerable-a-story-of-telematic-failures.md) — the earlier production-vehicle compromise case study (telematics unit rather than Wi-Fi/MQTT)
- [UDS seed/key](concepts/uds-seed-key.md) — weak SecurityAccess is one leg of this chain, as in so many others
