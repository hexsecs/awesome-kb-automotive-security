---
uid: 01a1d968-352a-7d99-b3c5-acda2361c52c
title: "BLE Theft Auto: Evaluating the Security of Aftermarket BLE-based Automotive Remote Control Systems"
summary: "Yu et al., USENIX Security 2026. Shows three of six aftermarket Bluetooth vehicle remote-control systems have critical pairing and authentication flaws…"
type: entity
category: "Research Papers"
url: "https://cseweb.ucsd.edu/~schulman/docs/sec26-bletheftauto.pdf"
status: published
last_checked: 2026-11-17
created: 2026-11-14
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: 46f5cc7
list_summary: "Yu et al., USENIX Security 2026. Shows three of six aftermarket Bluetooth vehicle remote-control systems have critical pairing and authentication flaws, including a shared key across dealer-installed devices that lets a nearby attacker unlock doors and immobilize engines."
related:
  - fast-and-vulnerable-a-story-of-telematic-failures
  - comprehensive-experimental-analyses-of-automotive-attack-surfaces
  - research-only-understanding-the-scope-of-automotive-cyberattacks-in-the-wild
  - vehicle-immobilization-revisited
  - candid-a-stealthy-stepping-stone-attack-to-bypass-authentication-on-ecus
  - vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks
  - key-fob-relay-attacks
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-14
  - url: "https://www.usenix.org/conference/usenixsecurity26/yu-jerry"
    retrieved: 2026-11-17
  - url: "https://bleauto.sysnet.ucsd.edu/"
    retrieved: 2026-11-17
---

Yu et al., USENIX Security 2026. Shows three of six aftermarket Bluetooth vehicle remote-control systems have critical pairing and authentication flaws, including a shared key across dealer-installed devices that lets a nearby attacker unlock doors and immobilize engines.

## What it is

A USENIX Security 26 paper by Jerry Yu, Yibo Wei, Sumanth Rao, Mohak Vaswani and Jefferson Chien (UC San Diego), Christian Dameff (UC San Diego Health), Nishant Bhaskar and Aaron Schulman (UC San Diego), pp. 3459–3478. It was a runner-up for the Distinguished Paper Award. The subject is not the car maker's own key fob but the **aftermarket BLE remote-control systems** installed by dealers or individuals to add app-based control — systems that the authors note have received little security scrutiny.

## How it works

These systems let a smartphone app act like a key fob, unlocking doors and even starting the engine. They use Bluetooth Low Energy for offline remote control but do **not** use BLE's built-in security; instead each vendor implements its own application-layer protocol, creating a new attack surface. The authors found six systems in current use — KARR, CarLink, Rockledge, DS4, EvoStart and Linkr — and analysed their BLE application-layer security. At the time of the study DS4, EvoStart and Linkr had robust security, while KARR, CarLink and Rockledge had critical pairing or authentication flaws.

Targeting is practical because the devices broadcast BLE advertisements that can be found locally or through crowdsourced Bluetooth scanning databases — an attacker does not need to know the owner or the vehicle model in advance. Once connected, the systems are spliced into sensitive vehicle wiring: door locks, horn, lights, immobilizer, CAN bus and ignition. The paper's estimate of exposed systems is **1.4 million** aftermarket BLE control systems; the companion project page, apparently counting vehicles, says **more than two million** vehicles, including tens of thousands with vulnerable remote-start systems, across the US, Canada and beyond through used-car resale. Owners may not even know an active BLE system is installed, particularly when it was dealer-installed and never activated.

## Disclosure and impact

The researchers responsible-disclosed to the affected vendors and filed an NHTSA report about the KARR vulnerability. KARR was notified on 21 January 2025, took initial mitigation steps, and released a firmware update for all affected vehicles on 20 July 2026; the project page directs KARR owners to Acrisure's update instructions. CarLink and Rockledge issues were disclosed to CarLink on 31 July 2025, and Rockledge was contacted directly on 17 December 2025. According to the USENIX abstract, the disclosures led all vendors to patch improved application-layer BLE security. The project states that they deliberately do **not** publish the details needed to exploit the pairing, authentication or encryption flaws.

## Where it fits

This is the aftermarket-wireless case of a broader pattern: [fast and vulnerable: a story of telematic failures](fast-and-vulnerable-a-story-of-telematic-failures.md) and [comprehensive experimental analyses of automotive attack surfaces](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md) cover the OEM-side equivalent. [Research only? understanding the scope of automotive cyberattacks in the wild](research-only-understanding-the-scope-of-automotive-cyberattacks-in-the-wild.md) is the context for why a flaw in a dealer-installed device matters at population scale. On the defensive side, [vehicle immobilization revisited](vehicle-immobilization-revisited.md), [CANDID](candid-a-stealthy-stepping-stone-attack-to-bypass-authentication-on-ecus.md) and [Vulcan](vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks.md) address authentication and isolation for ECUs and vehicle functions.

## Limits and safety notes

The public sources give findings, system names, counts and disclosure timelines but deliberately withhold exploit details, so this page does not describe how to pair with or command a vulnerable device. The two different exposure figures are attributed above rather than reconciled: the paper's 1.4 million systems and the project site's more-than-two-million vehicles may reflect different units or updates. This is an active safety issue, not a historical curiosity: affected owners need a firmware update. No BLE device or vehicle was tested for this page.

## Status and sources

Checked 2026-11-17. **Published** — USENIX Security 26, August 2026, open access; a project site and disclosure timeline are maintained by the authors.

- [USENIX paper page](https://www.usenix.org/conference/usenixsecurity26/yu-jerry)
- [Project site and disclosure timeline](https://bleauto.sysnet.ucsd.edu/)

## Related

- [Fast and vulnerable: a story of telematic failures](fast-and-vulnerable-a-story-of-telematic-failures.md)
- [Comprehensive experimental analyses of automotive attack surfaces](comprehensive-experimental-analyses-of-automotive-attack-surfaces.md)
- [Research Only? Understanding the scope of automotive cyberattacks in the wild](research-only-understanding-the-scope-of-automotive-cyberattacks-in-the-wild.md)
- [Vehicle immobilization revisited](vehicle-immobilization-revisited.md)
- [CANDID: a stealthy stepping-stone attack to bypass authentication on ECUs](candid-a-stealthy-stepping-stone-attack-to-bypass-authentication-on-ecus.md)
- [Vulcan: efficient component authentication and software isolation for automotive control networks](vulcan-efficient-component-authentication-and-software-isolation-for-automotive-control-networks.md)
- [Key-fob relay attacks](concepts/key-fob-relay-attacks.md)
