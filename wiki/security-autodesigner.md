---
uid: 01a19d3c-afd4-748e-acb2-61988f58a975
title: "Security AutoDesigner"
summary: "Automated TARA platform for creating ISO 21434 and UNR 155 compliant threat analysis reports."
type: entity
category: "Security Analysis"
url: "https://plaxidityx.com/products/security-autodesigner/"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Automated TARA platform for creating ISO 21434 and UNR 155 compliant threat analysis reports."
related: [autotara, avcdl, automotive-threat-matrix, tara-methodology]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://plaxidityx.com/products/security-autodesigner/"
    retrieved: 2026-11-01
  - url: "https://plaxidityx.com/"
    retrieved: 2026-11-01
---

Automated TARA platform for creating ISO 21434 and UNR 155 compliant threat analysis reports.

## What it is

A commercial software product from PlaxidityX — the vendor's own homepage title reads "PlaxidityX (Formerly Argus)", i.e. the company is the renamed Argus Cyber Security — that automates the production of a Threat Analysis & Risk Assessment (TARA) for vehicles and ECUs. Per the vendor's product page, it combines a threat database built from "dozens of TARA projects" with OEMs and Tier-1s, the vendor research team's ongoing threat intake, and what the page calls "state-of-the-art AI technology" to generate a detailed TARA report whose stated purpose is compliance with ISO/SAE 21434 and UN R155. It is sold, not downloaded: the page's only call to action is "Contact Us", and no trial, pricing, or public documentation exists on the vendor site.

## How it works

What the vendor's own page establishes, and no more. **Input:** an ECU or vehicle design ("automated TARA creation based on ECU or vehicle design") — the page does not name import formats, model formats, or an authoring workflow. **Process:** asset identification, threat modeling, attack path analysis and risk scoring (the page's own FAQ definition of the TARA it automates), matched against an out-of-the-box database of "over 100 automotive threats prioritized from very low risks to critical risks" (vendor figure). **Output:** a detailed TARA report; the FAQ claims automation benefits including reduced manual effort (vendor figure: 60–80%) and auto-generated ISO 21434-compliant reports — vendor claims, kept attributed here. **Scope:** both vehicle-level and component (ECU)-level TARA. **Continuity:** "continuous TARA updates based on product architecture changes"; vulnerability data (CVE/NVD) can feed feasibility ratings via the vendor's separate supply-chain product. **Integration:** connection to "most common requirements management tools" (unnamed on the page), and integration with the vendor's own DevSecOps platform.

## Where it fits

One of the section's two TARA-automation tools, and the commercial pole: [AutoTARA](autotara.md) is the openly accessible, self-hosted research framework; AutoDesigner is the closed, vendor-supported product with a proprietary threat database and a services company behind it. Against [AVCDL](avcdl.md): AVCDL defines the whole lifecycle process in which TARA is one work product; AutoDesigner automates the production of that one work product. A TARA produced by either tool still lands inside a 21434 process of the AVCDL kind.

## Limits and safety notes

**Thin public documentation is the finding, and this page states it rather than paraphrasing marketing copy into facts.** From the vendor's own pages it was possible to establish: purpose, standards targeted (ISO/SAE 21434, UN R155), input at the level of "ECU or vehicle design", output (a TARA report), the threat-database size claim (100+), both TARA levels, and integration claims at a generic level. It was **not** possible to establish: the deployment model (SaaS vs on-premise), pricing or licensing terms, supported design-input formats, the AI techniques actually used, report-format specifics, or any version/release state — none of that is published anywhere on the vendor site. All quantitative claims (60–80% effort reduction, "over 100 threats", "dozens of projects") are the vendor's own and are presented here as vendor claims. One further precision: "compliant reports" is the vendor's phrasing — ISO/SAE 21434 conformity is a property of an organisation's process and evidence, not something a tool output confers by itself, and this page does not adopt the claim as its own.

## Status and sources

Checked 2026-11-01. **Active**: a commercial product with no public versioning; the vendor's site is maintained into 2026 (2026-dated content on the homepage, including a 2026 threat report and press releases) and the product is offered as a current part of the suite with an active sales route — an actively sold offering, with no public release state to cite. Documentation claims above come from the following primary sources.

- [Vendor product page](https://plaxidityx.com/products/security-autodesigner/)
- [Vendor homepage](https://plaxidityx.com/)

## Related

- [AutoTARA](autotara.md)
- [AVCDL](avcdl.md)
- [Automotive Threat Matrix](automotive-threat-matrix.md)
