---
title: "AutoTARA"
summary: "Web-based TARA (Threat Analysis and Risk Assessment) framework for ISO/SAE 21434 that models systems as attack graphs and applies MITRE's CTSA/CRRA…"
type: entity
category: "Security Analysis"
url: "https://github.com/HackProof/AutoTARA"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Web-based TARA (Threat Analysis and Risk Assessment) framework for ISO/SAE 21434 that models systems as attack graphs and applies MITRE's CTSA/CRRA prioritization methodology with a Meta Attack Language simulation backend."
related: [automotive-threat-matrix, automotive-threat-modeling-template, security-autodesigner]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/HackProof/AutoTARA"
    retrieved: 2026-11-01
---

Web-based TARA (Threat Analysis and Risk Assessment) framework for ISO/SAE 21434 that models systems as attack graphs and applies MITRE's CTSA/CRRA prioritization methodology with a Meta Attack Language simulation backend.

## What it is

An open-source (Apache-2.0), self-hosted web application that automates the ISO/SAE 21434 TARA process for automotive systems. It integrates three things the README names: MITRE's TARA methodology — CTSA (Cyber Threat Susceptibility Analysis) and CRRA (Cyber Risk Remediation Assessment) — for quantitative prioritisation of countermeasures; the Meta Attack Language (MAL, from KTH) as the attack-simulation backend that generates attack graphs; and LLMs. One naming precision this page keeps, because the underlying paper's title depends on it ("Bridging Two TARAs", VehicleSec '26, by Minhyuk Park, Yejun Kim and Seungjoo Kim): MITRE's *Threat Assessment and Remediation Analysis* is a different artefact from the ISO/SAE 21434 *Threat Analysis and Risk Assessment* — AutoTARA's premise is bridging the two. The v0.1.0-alpha release notes state that version "was presented as a prototype at USENIX VehicleSec '26" — the authors' own word for its maturity is *prototype*.

## How it works

Deployment is source-only and self-hosted: a Docker Compose file brings up four services — PostgreSQL 17, a FastAPI MAL simulation server, a Node.js/Express backend, and a Vue 3 frontend with a graph editor (AntV X6); no hosted instance is linked from the repo. The workflow: build and edit the system diagram in the visual editor; configure properties per component and connection; identify and manage threats against system elements; run attack simulation to generate attack paths; assess with the built-in CTSA and CRRA modules; review damage/threat scenarios and attack paths on a dashboard. The simulation backend executes MAL language definitions shipped in the repo — `coreLang` (compute/data resources, IAM, networking, vulnerabilities) and a `vehicleLang` extending it (encryption, Ethernet, public interfaces). Seeded knowledge data loaded into the database: MITRE ATT&CK Enterprise and ICS **v20.0** techniques, mitigations and detection strategies; UN R155 Annex 5 Parts A/B/C; mapping tables from MAL attack steps to ATT&CK mitigations and to R155 entries; and a per-attack-step **CTSA score** table — the quantitative input the CTSA/CRRA prioritisation runs on. The worked sample is a Tesla Model S (diagram + YAML model, scenario file, TTP assessment). The backend also loads LLM settings (the README names Gemini-related environment settings, i.e. the operator's own Google API key); exactly which workflow steps the LLM performs is not specified in the README and is not guessed here.

## Where it fits

The automation end of this section. Its closest sibling is [Security AutoDesigner](security-autodesigner.md) — likewise an automated ISO 21434 / UN R155 TARA platform — with the obvious split: AutoTARA is open-source, self-hosted and research-grade; AutoDesigner is a commercial product. Against the rest of the section: it *consumes* threat knowledge (ATT&CK v20.0 data, UN R155 Annex 5) rather than publishing a taxonomy (contrast the [Automotive Threat Matrix](automotive-threat-matrix.md)); its modelling surface is its own graph editor feeding a MAL simulation, not STRIDE generation over a Microsoft-tool DFD (contrast the [NCC template](automotive-threat-modeling-template.md)); and where [AVCDL](avcdl.md) defines the development lifecycle, AutoTARA is a tool used inside one step of it. For a team that wants the 21434 TARA artefacts (threat scenarios, attack paths, risk-treatment priorities) computed rather than hand-assembled, this is the section's open implementation.

## Limits and safety notes

Research prototype, by the authors' own description: one alpha release (v0.1.0-alpha), the default branch is a development branch literally named `v0.2.0`, and `main` has been untouched since June 2026 — pre-1.0 software under active restructuring. It is a small, young project (created June 2026; 6 stars, 0 forks at check time) with no community or production track record observable. The MAL-based results are only as good as the language coverage: the shipped languages are coreLang plus a vehicleLang sample set, so a given system's attack graphs are bounded by what those languages model — coverage beyond the samples is not established. LLM features depend on an external commercial API and the operator's key. Self-hosting only; there is no vendor-hosted instance to evaluate against.

## Status and sources

Checked 2026-11-01. **Active**: not archived; created June 2026 and still moving — commits on the v0.2.0 development branch as recently as 2026-10-24 and an alpha release on 2026-08-31. Active, but pre-1.0: the activity is a research prototype's, and this page says both halves of that. Documentation claims above come from the following primary sources; the stack was not run for this page.

- [Upstream repository](https://github.com/HackProof/AutoTARA)

## Related

- [Automotive Threat Matrix](automotive-threat-matrix.md)
- [Automotive Threat Modeling Template](automotive-threat-modeling-template.md)
- [Security AutoDesigner](security-autodesigner.md)
