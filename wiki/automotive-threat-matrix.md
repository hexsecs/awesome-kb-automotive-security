---
title: "Automotive Threat Matrix"
summary: "Auto-ISAC's MITRE ATT&CK-style matrix of automotive adversary tactics and techniques, drawn from validated attacks and reproducible research, for threat…"
type: entity
category: "Security Analysis"
url: "https://atm.automotiveisac.com/"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Auto-ISAC's MITRE ATT&CK-style matrix of automotive adversary tactics and techniques, drawn from validated attacks and reproducible research, for threat modelling, TARA, and intelligence sharing."
related: [automotive-threat-modeling-template, autotara, avcdl, tara-methodology]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://atm.automotiveisac.com/"
    retrieved: 2026-11-01
  - url: "https://automotiveisac.com/atm-white-paper"
    retrieved: 2026-11-01
---

Auto-ISAC's MITRE ATT&CK-style matrix of automotive adversary tactics and techniques, drawn from validated attacks and reproducible research, for threat modelling, TARA, and intelligence sharing.

## What it is

The Automotive Threat Matrix (ATM) is the Automotive Information Sharing and Analysis Center's (Auto-ISAC) ATT&CK-style knowledge base of adversary tactics and techniques specific to motor vehicles. It enumerates tactics and their supporting techniques from real-world observations — in the site's own words, "validated automotive attacks and peer-reviewed and reproducible automotive exploit research" — and publishes them as a public web application. It was crafted by subject-matter experts from Auto-ISAC's member and partner network (the ATM User Group); per Auto-ISAC's own press releases the tool launched on 27 March 2024, Vultara, Inc. develops and maintains it (the live site's footer reads "powered by Vultara, Inc."), and Auto-ISAC's February 2025 white paper is its companion document.

## How it works

Tactics are columns and techniques sit under the tactics they serve, in the ATT&CK layout. The matrix as rendered at check time has **14 tactics** (IDs ATM-TA0000–ATM-TA0013): Reconnaissance, Manipulate Environment, Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, and Affect Vehicle Function. Two have no ATT&CK Enterprise analogue and are the automotive tailoring in miniature: *Manipulate Environment* (sensor/ML attacks, jamming, rogue infrastructure) and *Affect Vehicle Function* (the impact column — CAN bus denial of service, Modify Bus Message). Techniques carry ATM-T#### IDs and are vehicle-specific where the domain demands it — "Bypass UDS Security Access", "Abuse Standard Diagnostic Protocol", "Reprogram ECU", "Bridge Vehicle Networks" — alongside adapted ATT&CK staples (Phishing, Supply Chain Compromise, Network Sniffing); as in ATT&CK, the same technique can appear under several tactics. An Examples page maps published research onto the matrix step by step (e.g. "Free-fall: Hacking Tesla From Wireless To CAN Bus", annotated with how the researchers defeated UDS security access on the gateway ECU) — the worked form of the admission rule. Scope, per the white paper: "motor vehicles, including embedded systems as well as IT devices and external systems that directly interact with or 'touch' the vehicle". The white paper's documented uses centre on TARA modelling — ATM cells compose into the attack paths ISO/SAE 21434 requires, each step carrying a user-assigned default feasibility so a path's overall feasibility falls out of the composition — plus intelligence sharing, attack-trend analysis, vulnerability-management prioritisation, security testing, UN R155 compliance reporting, and incident response.

## Where it fits

The taxonomy layer of this section. ATM supplies the shared vocabulary of adversary behaviour that a TARA then uses: threat scenarios and attack paths in an ISO/SAE 21434 / UN R155 analysis can be named, compared across suppliers, and assigned feasibility in ATM terms. It complements rather than competes with the section's tools: the [NCC template](automotive-threat-modeling-template.md) models *your* system as a data-flow diagram and generates STRIDE threats against it, whereas ATM catalogues what *adversaries* do; [AutoTARA](autotara.md) automates a TARA over a system model and consumes external threat data rather than publishing a taxonomy; [AVCDL](avcdl.md) is the lifecycle process the analysis sits inside. Against MITRE ATT&CK itself, ATM's claim is scope: vehicle-only, including the vehicle-function impact column ATT&CK has no equivalent for.

## Limits and safety notes

It is a taxonomy and knowledge base, not an analysis tool: it does not model a user's system, score their risk, or generate their TARA — the white paper's feasibility mechanic depends on user-assigned defaults per step. Content currency is bounded by the curation process: novel techniques appear only after User Group validation. Three gaps are recorded, not filled: a canonical total technique count is **not stated** on Auto-ISAC's public pages (the "~80 techniques" figure circulating in third-party write-ups is not imported here); what the site's login gates, if anything, is unverified (the matrix and examples are publicly readable without one); and no licence or reuse terms for ATM content were found — Auto-ISAC's press language calls it an "open" knowledge base in the publicly-accessible sense, and this page does not upgrade that to a licensing claim.

## Status and sources

Checked 2026-11-01. **Active**: the matrix site is live and publicly readable on the check date (its footer reads "Copyright © 2026, AutoISAC ATM"); Auto-ISAC published the companion white paper in February 2025; the tool launched 2024-03-27 under a standing arrangement (announced 2022-11-01) for Vultara, Inc. to develop and maintain it — a maintained, living knowledge base, not a finished artefact. Documentation claims above come from the following primary sources.

- [Automotive Threat Matrix](https://atm.automotiveisac.com/)
- [Auto-ISAC ATM white paper page](https://automotiveisac.com/atm-white-paper)

## Related

- [Automotive Threat Modeling Template](automotive-threat-modeling-template.md)
- [AutoTARA](autotara.md)
- [AVCDL](avcdl.md)
