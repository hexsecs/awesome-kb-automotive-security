---
title: "How API Flaws Led to Admin Access to Over 1k USA Dealers and Control Over Your Car"
summary: "Eaton Zveare, DEF CON 33 Car Hacking Village 2025. Slides showing how flaws in an automaker's central dealer platform yielded a national admin account…"
type: entity
category: "Conference Presentations"
url: "https://media.defcon.org/DEF%20CON%2033/DEF%20CON%2033%20villages%20and%20creators/DEF%20CON%2033%20-%20Car%20Hacking%20Village%20-%20Eaton%20Zveare%20-%20How%20API%20flaws%20led%20to%20admin%20access%20to%20over%201k%20USA%20dealers%20and%20control%20over%20your%20car.pdf"
status: published
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Eaton Zveare, DEF CON 33 Car Hacking Village 2025. Slides showing how flaws in an automaker's central dealer platform yielded a national admin account across over a thousand dealers."
sources:
  - url: "https://media.defcon.org/DEF%20CON%2033/DEF%20CON%2033%20villages%20and%20creators/DEF%20CON%2033%20-%20Car%20Hacking%20Village%20-%20Eaton%20Zveare%20-%20How%20API%20flaws%20led%20to%20admin%20access%20to%20over%201k%20USA%20dealers%20and%20control%20over%20your%20car.pdf"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - fast-and-vulnerable-a-story-of-telematic-failures
  - wir-wissen-wo-dein-auto-steht
---

Eaton Zveare, DEF CON 33 Car Hacking Village 2025. Slides showing how flaws in an automaker's central dealer platform yielded a national admin account across over a thousand dealers.

A DEF CON 33 Car Hacking Village talk (August 8, 2025) by Eaton Zveare — the public disclosure of a flaw chain in a major automaker's dealer platform, the invite-only system its dealers use to order cars and manage customers. Registration was invite-only in name only: the invite token was checked only by client-side JavaScript — the form itself was merely hidden with CSS — the server never validated it on submit, and a profile-update quirk then turned the resulting unapproved account into a live session. Inside, admin user-management scripts were enforced only in the browser; patching those checks let Zveare create a national admin account spanning over 1,000 dealers — customer lookup by name or VIN, dealer employee and finance data, inventory control, and the owner-pairing enrollment system, which he used, with a friend's consent, to transfer the friend's car to himself and with it the app-based remote start, unlock, and location tracking. A user-impersonation feature bypassed even login and two-factor authentication; cars from model year 2012 onward were reachable through the standard telematics module.

What you get: the complete 52-slide deck — the whole attack narrative, screenshots, and disclosure timeline included. Essential reading for anyone securing dealer, fleet, or owner-facing automotive backends: every failure is a conventional web/API failure, and the blast radius is a national dealer network. Caveats: the automaker is deliberately not named in the deck, and the flaws were fixed before publication (reported via the vendor's VDP in February 2025) — a post-mortem, not a live exposure.

## Status and sources

Status: **published** — DEF CON 33, Car Hacking Village, August 2025; slides public. Verified against the slide deck at [media.defcon.org](https://media.defcon.org/DEF%20CON%2033/DEF%20CON%2033%20villages%20and%20creators/DEF%20CON%2033%20-%20Car%20Hacking%20Village%20-%20Eaton%20Zveare%20-%20How%20API%20flaws%20led%20to%20admin%20access%20to%20over%201k%20USA%20dealers%20and%20control%20over%20your%20car.pdf) (the stub's resource), 2026-11-01.

## Related

- [Fast and Vulnerable: A Story of Telematic Failures](fast-and-vulnerable-a-story-of-telematic-failures.md) — backend/telematics weaknesses turned into vehicle access, a decade earlier
- [Wir wissen, wo dein Auto steht](wir-wissen-wo-dein-auto-steht.md) — backend-side owner-data exposure at fleet scale
