---
uid: 01a19d3c-af33-794c-9a33-87d589b0bb63
title: "Automotive Threat Modeling Template"
summary: "NCC Group stencil set for the Microsoft Threat Modeling Tool, supplying vehicle-specific element types, trust boundaries, and threat rules for ECU and…"
type: entity
category: "Security Analysis"
url: "https://github.com/nccgroup/The_Automotive_Threat_Modeling_Template"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "NCC Group stencil set for the Microsoft Threat Modeling Tool, supplying vehicle-specific element types, trust boundaries, and threat rules for ECU and in-vehicle network diagrams."
related: [automotive-threat-matrix, autotara, avcdl, tara-methodology]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://github.com/nccgroup/The_Automotive_Threat_Modeling_Template"
    retrieved: 2026-11-01
  - url: "https://github.com/nccgroup/The_Automotive_Threat_Modeling_Template/blob/master/README.md"
    retrieved: 2026-11-01
---

NCC Group stencil set for the Microsoft Threat Modeling Tool, supplying vehicle-specific element types, trust boundaries, and threat rules for ECU and in-vehicle network diagrams.

## What it is

A template file for the Microsoft Threat Modeling Tool 2016 that customises Microsoft's data-flow-diagram threat modelling for connected vehicles, published by NCC Group on GitHub in July 2016. The repository contains exactly two files: a README and the template itself, `automotive_TM_template-v1.2.tb7` (the .tb7 template format of the 2016 tool); the current version is v1.2 (September 2017). It exists because, per the README, "a threat modeling workshop for automotive-related technologies requires DFDs with custom elements, tailored threats and specific recommendations" — and the 2016 tool had just added support for entirely custom templates.

## How it works

The template is selected inside the Microsoft Threat Modeling Tool 2016 ("Template For New Models") before creating a model; the tool then generates threats against the drawn diagram using the template's elements and rules. What the template supplies, per the README: processes and data stores related to the components of connected cars; external interactors tailored to an automotive system; data flows corresponding to the messages exchanged over the air or inside the vehicle; trust boundaries that take into consideration the environment and vehicle-to-vehicle (V2V) networks; threat types and categories following the STRIDE classification, based on known and potential threats to connected cars' components; and tailored threat properties on each generated threat — *Priority* (based on the risk of the threat in its context), *Attack Methods* (methods to potentially exploit the threat, included "to help further with the creation of Attack Trees"), and *Recommendations* (suggested mitigations). The workflow is: draw the ECU / in-vehicle-network DFD with automotive stencils, let the tool enumerate STRIDE threats per element, then work the generated list using the attached priorities, attack methods and recommendations.

## Where it fits

The modelling layer of this section, and its oldest artefact. An analyst uses it at design time to model one system (an ECU, a gateway, an in-vehicle network) and generate a first threat list — the manual, diagram-first end of the space. The division of labour, precisely: the [Automotive Threat Matrix](automotive-threat-matrix.md) is the adversary-behaviour taxonomy a generated threat can be cross-referenced against; [AutoTARA](autotara.md) automates the ISO/SAE 21434 TARA over a graph model with attack simulation rather than STRIDE generation over a DFD; [AVCDL](avcdl.md) supplies the lifecycle process around the activity; Security AutoDesigner is the commercial automated-reporting counterpart. The template's "Attack Methods" property is its bridge toward attack-tree work.

## Limits and safety notes

Tool lock-in and age, stated by the sources themselves: the template was created with and for the Microsoft Threat Modeling Tool **2016**, and models are created in that product; compatibility with later versions of the tool is **not established** from primary sources. Threat content is the 2016–2017 view of connected-car threats; nothing in the repo updates it for post-2017 vehicle architectures. **No licence file** is present in the repository — reuse terms are unstated, flagged rather than assumed. The README's pointer to NCC Group's July 2016 blog post uses the retired nccgroup.trust domain and no longer resolves as written; the repo is the surviving primary source.

## Status and sources

Checked 2026-11-01. **Unknown**: not archived, but the repository's content has been unchanged since v1.2 in September 2017 (7 commits total, HEAD dated 2017-09-06, no releases or tags) — a finished, published template artefact with no observable ongoing project state. One wrinkle is recorded rather than smoothed: the API reports a 2020 push date, but no commit after 2017 exists on the sole branch, so no content change after v1.2 is observable. Documentation claims above come from the following primary sources.

- [Upstream repository](https://github.com/nccgroup/The_Automotive_Threat_Modeling_Template)
- [Upstream README](https://github.com/nccgroup/The_Automotive_Threat_Modeling_Template/blob/master/README.md)

## Related

- [Automotive Threat Matrix](automotive-threat-matrix.md)
- [AutoTARA](autotara.md)
- [AVCDL](avcdl.md)
