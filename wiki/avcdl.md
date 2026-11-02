---
title: "AVCDL"
summary: "Motional's open-sourced Versatile Cybersecurity Development Lifecycle with process definitions and templates mapped to ISO/SAE 21434, ISO 24089, and UN…"
type: entity
category: "Security Analysis"
url: "https://github.com/nutonomy/AVCDL"
status: maintenance
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Motional's open-sourced Versatile Cybersecurity Development Lifecycle with process definitions and templates mapped to ISO/SAE 21434, ISO 24089, and UN R155/R156, assessed by TUV SUD."
related: [autotara, security-autodesigner, automotive-threat-modeling-template]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/nutonomy/AVCDL"
    retrieved: 2026-11-01
  - url: "https://github.com/nutonomy/AVCDL/blob/main/README.md"
    retrieved: 2026-11-01
---

Motional's open-sourced Versatile Cybersecurity Development Lifecycle with process definitions and templates mapped to ISO/SAE 21434, ISO 24089, and UN R155/R156, assessed by TUV SUD.

## What it is

AVCDL — "A Versatile Cybersecurity Development Lifecycle" (the expansion is the repo description's own wording) — is an open, document-form secure development lifecycle for automotive systems, published by Motional. It is not software: it is a set of identified processes, the requirements of those processes, the products (documents) each process generates, and mappings from those products to the work products demanded by ISO/SAE 21434, ISO 24089, and UN R155/R156. The artefact is a primary document plus roughly 100 supporting documents — over 950 pages by the README's own count — distributed as a Git repository of PDFs with their sources, under CC BY-SA 4.0. Two provenance details belong on the page because they are visible in the primary sources: the repository still lives under the legacy `nutonomy` GitHub organisation, while the assessment documents inside it are titled for Motional.

## How it works

The lifecycle runs in phases, each with required products and (for the middle phases) a phase-gate document; the phase list is taken from the repo's own document-status page, which marks the core documents complete: **Foundation** (training catalogue, roles and responsibilities, approved tools/components list, global security goals and requirements, code protection plan, release integrity plan, cybersecurity monitoring plan) → **Requirements** → **Design** → **Implementation** → **Verification** → **Release** (each with a phase gate) → **Operation** → **Decommissioning**. Three trees organise the artefact: `distribution/` is the finished product (the primary document, secondary documents, templates, certification documents, working material); `source/` holds the editable sources the distribution PDFs are built from; `assessments/` holds the assessor summaries. Secondary documents are the per-phase work-product templates an adopter fills in — Attack Surface Analysis Report, Ranked-Risked Threat Report, Cybersecurity Interface Agreement, penetration/static/dynamic analysis reports, phase gates, decommissioning plan and report. Templates shipped include a Cybersecurity Interface Agreement template, capability-maturity worksheets, a supplier disclosure (AVCMDS) worksheet, and a worked UN R155 Annex 5 attack-methods template. Roughly 18 elaboration documents explain the judgement calls around the lifecycle — *Understanding TARA in an AVCDL Context*, code signing, SBOM lifecycle, manifest generation, incremental adoption, supplier process mapping, risk freshness, V&V — so TARA is one elaborated topic *inside* AVCDL, not the whole of it: the precise contrast with this section's TARA tools. Supply chain is a first-class track (supplier self-reported maturity assessment, AVCMDS, interface agreements). Per the README's Assessments section, AVCDL has been **assessed by TÜV SÜD as complying with ISO/SAE 21434** (assessment summary v2.12) **and with UN R155** (summary v3.2); it was "currently being assessed" for ISO 24089 and UN R156 as of the README's last state.

## Where it fits

The section's only full-lifecycle process framework. The division of labour: the [Automotive Threat Matrix](automotive-threat-matrix.md) catalogues techniques; the [NCC template](automotive-threat-modeling-template.md) supplies diagramming stencils; [AutoTARA](autotara.md) and [Security AutoDesigner](security-autodesigner.md) automate the TARA step specifically; AVCDL defines the surrounding lifecycle — phases, gates, roles, supplier agreements, monitoring, decommissioning — inside which a TARA, however produced, is one work product among many. Its natural user is an OEM/supplier security organisation adopting or evidencing a 21434/R155-conformant process, and its supplier track targets the assessed-party side of that relationship.

## Limits and safety notes

It is a document set, not a tool: adopting it means staffing the phases and producing the products; nothing in the repo executes. The assessment scope is the README's own and is not extended here: TÜV SÜD compliance assessments exist for ISO/SAE 21434 and UN R155; the ISO 24089 / UN R156 assessments were still in progress at the last repo state (May 2024) — whether they completed is **not established** from primary sources. Scale is itself a limit the README concedes: 950+ pages, with the advice to clone rather than cherry-pick because secondary documents cross-link by relative path. Companion video training was described as "currently under development" at the last repo state; completion unverified. The framework was written for autonomous-vehicle development (Motional's context); its generality to conventional programmes is the adopter's judgement, not a repo claim.

## Status and sources

Checked 2026-11-01. **Maintenance**: not archived; the document set was released intensively through 4.18.6 on 2024-05-07 and its own status page declares the core documents complete, but there has been no commit or release in the ~18 months before this check — a finished core with an open assessment thread (24089/R156), quiet rather than abandoned. Documentation claims above come from the following primary sources.

- [Upstream repository](https://github.com/nutonomy/AVCDL)
- [Upstream README](https://github.com/nutonomy/AVCDL/blob/main/README.md)

## Related

- [AutoTARA](autotara.md)
- [Security AutoDesigner](security-autodesigner.md)
- [Automotive Threat Modeling Template](automotive-threat-modeling-template.md)
