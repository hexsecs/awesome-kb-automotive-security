---
uid: 01a19d3c-afe6-74f6-8b84-3860f4bba829
title: "tesla-opener"
summary: "Open-source tool to open Tesla charging port using HackRF and WebUSB with ASK/OOK RF transmission."
type: entity
category: "Penetration Testing"
url: "https://github.com/rgerganov/tesla-opener"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open-source tool to open Tesla charging port using HackRF and WebUSB with ASK/OOK RF transmission."
related: [key-fob-relay-attacks, flipper-zero]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/rgerganov/tesla-opener"
    retrieved: 2026-11-01
  - url: "https://github.com/rgerganov/tesla-opener/blob/master/docs/index.html"
    retrieved: 2026-11-01
  - url: "https://github.com/rgerganov/tesla-opener/blob/master/docs/js/hackrf.js"
    retrieved: 2026-11-01
---

Open-source tool to open Tesla charging port using HackRF and WebUSB with ASK/OOK RF transmission.

## What it is

A single static web page that makes a HackRF transmit the fixed radio signal a Tesla charge port listens for, opening the port door (and waking the port) without the car's key, app, or charge cable button. There is no protocol to speak of and no pairing: the charge-port receiver accepts a fixed, unauthenticated ASK/OOK bit pattern, and this page replays it from commodity SDR hardware driven directly from the browser over WebUSB. Per the README, the signal pattern is credited to @IfNotPike; this repository packaged it into the WebUSB page.

## How it works

The payload is one fixed bit pattern (published verbatim in the README), transmitted with ASK/OOK modulation at a symbol rate of 2500 bits/second. The shipped page holds the pattern as a JavaScript array, expands it to IQ samples at a 10 Msps sample rate, and sends it five times per button press. Frequencies are user-selectable in the page: **315.000 MHz** (default) or **433.920 MHz** — the two regional bands for this signal. TX VGA gain is a slider (1–47) with an optional RF amplifier toggle. The hardware path is a HackRF — the bundled `hackrf.js` is a JavaScript port of libhackrf speaking WebUSB vendor requests — connected to anything running Chrome; the README's demo uses a Pixel phone with a USB OTG cable, and the page is hosted for direct use. The repository also carries pre-generated IQ files for playback via rpitx (per the commit that added them), an alternate Raspberry Pi transmission path alongside the HackRF one.

## Where it fits

The minimal end of the RF & Key Fob spectrum: unlike the rolling-code and relay material in [key-fob relay attacks](concepts/key-fob-relay-attacks.md), nothing here is captured, relayed, or decrypted — the target system simply has no authentication to defeat, which is the finding. It pairs with general SDR/RF tooling in that section (Flipper Zero-class devices transmit the same class of fixed OOK signals) and is the charge-port counterpart to the EV-charging attack material: physical access to the port is the precondition other charging attacks assume.

## Limits and safety notes

Scope is exactly one party trick: it opens a charge port door. It does not unlock the car, start charging sessions, or interact with any other Tesla system, and the sources claim nothing more. Transmitting on 315 / 433.92 MHz is regulated radio use; the page offers an amplifier toggle and up to 47 dB TX gain with no guidance in the repository about legal power limits — that judgement is left entirely to the user. The README does not scope which Tesla models or model years respond. There is no licence file, so reuse terms are unstated.

## Status and sources

Checked 2026-11-01. **Unknown**: the repository is not archived; created 2022-03-27, it has seven commits with the latest on 2023-03-14, and no releases. Like Simos18_SBOOT in the Firmware section, it is a finished, single-purpose artefact whose repository shows no ongoing project state to observe, rather than a maintained tool gone quiet. Documentation claims above come from the following primary sources; no radio transmission was made for this page.

- [Upstream repository](https://github.com/rgerganov/tesla-opener)
- [Shipped page source](https://github.com/rgerganov/tesla-opener/blob/master/docs/index.html)
- [WebUSB libhackrf port](https://github.com/rgerganov/tesla-opener/blob/master/docs/js/hackrf.js)

## Related

- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md)
- [Flipper Zero](flipper-zero.md)
