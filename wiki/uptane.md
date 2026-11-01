---
title: "Uptane"
summary: "Open standard for securing automotive over-the-air updates that extends TUF to limit the damage when a repository or signing key is compromised, governed…"
type: entity
category: "Security Analysis"
url: "https://uptane.org/"
status: maintenance
last_checked: 2026-11-01
updated: 2026-11-01
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Open standard for securing automotive over-the-air updates that extends TUF to limit the damage when a repository or signing key is compromised, governed under the Joint Development Foundation."
related: [secure-firmware-updates, uptane-securing-software-updates-for-automobiles]
sources:
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-10-31
  - url: "https://uptane.org/"
    retrieved: 2026-11-01
  - url: "https://uptane.org/docs/latest/all-versions"
    retrieved: 2026-11-01
  - url: "https://github.com/uptane/uptane-standard"
    retrieved: 2026-11-01
  - url: "https://uptane.org/learn-more/adoptions"
    retrieved: 2026-11-01
---

Open standard for securing automotive over-the-air updates that extends TUF to limit the damage when a repository or signing key is compromised, governed under the Joint Development Foundation.

## What it is

Uptane is an open standard — and the project that maintains it — for securing automotive software over-the-air update delivery, created as the automotive adaptation of The Update Framework (TUF). The artefact has three parts: the **Uptane Standard** (a versioned specification document), a **governance body** (a Linux Foundation Joint Development Foundation project with a standards committee), and a **constellation of implementations** in the `uptane` GitHub organisation (a C++ client, Scala backend services, a Yocto layer). It originated in academic work at NYU Tandon and partner institutions; standardisation began under IEEE-ISTO in 2018. This page is the artefact record; the design itself — roles, repositories, verification tiers, the compromise-resilience ladder — is covered by the [secure firmware updates](concepts/secure-firmware-updates.md) concept page and is not re-derived here. (The homepage's claim to resist "nation-state level actors" is the project's own framing of its threat model, attributed as such.)

## How it works

**Governance.** Uptane is "a Linux Foundation Joint Development Foundation Project, LLC, Uptane Series" (the homepage footer's wording). Standard releases are governed by the Uptane Standards Committee: per the standard repo's README, release dates are set by the committee and final releases are approved by majority vote of active members at bimonthly meetings (or by "approve" responses in a designated thread announced at least two weeks ahead). The Standard is licensed under the Community Specification License 1.0. Enhancement proposals live in the `uptane/pures` repo (PUREs — Proposed Uptane Revisions and Enhancements); deployment guidance is the separate *Uptane Deployment Best Practices* document, maintained as a living document. The Standard itself is a living document between releases: edits land in the repo in real time but are "not considered formally adopted" until the next versioned release.

**Version history** (from the project's own all-versions page): **IEEE-ISTO 6100.1.0.0** (2019-07-31 — the 6100 designation belongs to this 2019 edition only) → **v1.1.0** (the first release under the Linux Foundation's Joint Development Foundation) → **v1.2.0** → **v2.0.0** ("a few design changes, but primarily clarifications and wording improvements") → **v2.1.0** (2023-06-27, the current version; the standard repo's README independently confirms the date).

**Implementations.** **aktualizr**, the C++ client that Automotive Grade Linux ships: last tagged release is old (2020.2) but substantive commits run to October 2025 — releases are not its cadence signal. **meta-updater**, the Yocto layer wiring aktualizr + OSTree into images: genuinely maintained, with substantive commits in October 2026. The **Scala backend services** (director, ota-tuf, libats, treehub) still receive pushes, but their October 2026 pushes are scala-steward automated dependency updates — upkeep, not feature development, and stated as such. And a trap worth naming: the original Python reference implementation is **archived** and described by the project itself as "a reference implementation of a pre-1.0 version of the Uptane Standard and should not be used" — it is not the reference implementation, and there is no current single one.

## Where it fits

The section's odd one out, deliberately: every other Security Analysis entry is a TARA/lifecycle aid, while Uptane is a standard for one specific engineering activity — securing the update-delivery path that the lifecycle's release and operation phases depend on. In workflow terms it sits downstream of TARA: a TARA ([AutoTARA](autotara.md), [Security AutoDesigner](security-autodesigner.md)) identifies update-path threats; [AVCDL](avcdl.md)'s release-integrity and code-signing material governs the process around them; Uptane is the technical design a team adopts so the delivery mechanism itself survives server and key compromise. Its relationship to TUF is stated plainly because it is the most common point of confusion about the artefact: Uptane extends TUF's design, but the projects sit in **different foundations** — TUF is a CNCF graduated project (per TUF's own site); Uptane is a Linux Foundation JDF project.

## Limits and safety notes

Uptane secures *delivery*, not package content — one sentence here; the analysis is on the concept page. The adoption record is thin at the OEM level, stated at exactly the project's own strength: its Adoptions page opens "Uptane has been adopted by several major automakers, which will lead to its implementation in millions of vehicles" — unnamed automakers, future tense; **no automaker, vehicle model, or production deployment is named anywhere on the page**. The named, checkable record is: Automotive Grade Linux (via aktualizr), HERE OTA Connect, Airbiquity OTAmatic, Foundries.io (partial — its aktualizr build *removes* Uptane checks, preferring TUF's security without Uptane's complexity), and Torizon. The Standard has had no versioned release since June 2023; whether a successor is in preparation is not announced on the primary sources. The archived pre-1.0 reference implementation still surfaces in search results — anyone implementing from it would be implementing a superseded design.

## Status and sources

Checked 2026-11-01. **Maintenance**: the Standard is current and governed (v2.1.0; JDF committee process alive; licensing upkeep in the standard repo as of July 2026) and the implementation repos still receive upkeep — meta-updater substantively, the Scala services by automated dependency updates — but there has been no Standard release since June 2023 and no public project news since 2024: a stable, maintained standard, not an actively evolving one. Documentation claims above come from the following primary sources.

- [Project site](https://uptane.org/)
- [Standard — all versions](https://uptane.org/docs/latest/all-versions)
- [Standard repository](https://github.com/uptane/uptane-standard)
- [Adoptions page](https://uptane.org/learn-more/adoptions)

## Related

- [Secure firmware updates](concepts/secure-firmware-updates.md)
- [Uptane: Securing Software Updates for Automobiles](uptane-securing-software-updates-for-automobiles.md)
