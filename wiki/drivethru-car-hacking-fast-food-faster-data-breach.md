---
title: "DriveThru Car Hacking: Fast Food, Faster Data Breach"
summary: "Chen et al., Black Hat Asia 2025. Attack chain against more than 24 dashcam models, delivered through a drive-through ordering flow, with an accompanying tool."
type: entity
category: "Conference Presentations"
url: "https://citation.thinkst.com/talk/96125"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Chen et al., Black Hat Asia 2025. Attack chain against more than 24 dashcam models, delivered through a drive-through ordering flow, with an accompanying tool."
sources:
  - url: "https://citation.thinkst.com/talk/96125"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles
  - donglescope
---

Chen et al., Black Hat Asia 2025. Attack chain against more than 24 dashcam models, delivered through a drive-through ordering flow, with an accompanying tool.

A Black Hat Asia 2025 briefing by Alina Tan and George Chen, with Chee Peng Tan, Ri-Sheng Tan, Penelope Chua, and Benjamin Cao. The team audited more than two dozen dashcam models and built "DriveThru hacking": an automated attack that discovers a dashcam's Wi-Fi, connects, bypasses its authentication, and exfiltrates recorded video, audio, and GPS data — then summarises what it captured with an LLM pipeline — all inside the few minutes a car spends in a drive-through queue. The attack is vendor-agnostic rather than built on per-model exploits; the researchers built their tooling on 20 purchased dashcams and validated it against 40 study participants' dashcams, and the talk closes with countermeasures for owners and vendors.

What you get: the recorded briefing and a public slide deck; for one dashcam family, George Chen's write-up in his i-Drive repository documents the underlying findings as CVE-2025-1878 and following. This is the reference talk for anyone threat-modelling aftermarket in-car electronics — the device is not part of the car, but it records the car's occupants and routes. Caveats: the model sample reflects the Singapore market, the attack needs Wi-Fi proximity to the target car, and dashcam firmware and apps change fast, so treat model specifics as a 2025 snapshot.

## Status and sources

Status: **published** — Black Hat Asia 2025 briefing; recording and slides public. Abstract verified at [citation.thinkst.com/talk/96125](https://citation.thinkst.com/talk/96125) (the stub's resource); speakers and contributors from the published slide deck, 2026-11-01.

## Related

- [Plug-N-Pwned](plug-n-pwned-comprehensive-vulnerability-analysis-of-obd-ii-dongles.md) — the same genre of audit for OBD-II dongles, the other aftermarket device class
- [DongleScope](donglescope.md) — the tooling paper behind the dongle audit
