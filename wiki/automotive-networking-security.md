---
title: "Automotive-Networking-Security"
summary: "Automotive networking security standards and solutions overview."
type: entity
category: "Learning Resources"
url: "https://automotive-network-security.com/standard_solutions.shtml"
status: unknown
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-01
depth: brief
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Automotive networking security standards and solutions overview."
sources:
  - url: "https://automotive-network-security.com/standard_solutions.shtml"
    retrieved: 2026-11-01
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
related:
  - what-is-automotive-macsec
  - someip
---

Automotive networking security standards and solutions overview.

A small reference website that catalogues the standardised security mechanisms for in-vehicle networks and links the governing documents directly: MACsec (IEEE 802.1AE), IPsec and IKEv2, TLS/DTLS, AUTOSAR SecOC, and the ASA Motion Link for SerDes, with a publications page on choosing between them. It is for engineers who need to find which standard governs a given layer of the vehicle network and get to the actual specification text fast.

Caveats: it is a link catalogue, not a tutorial — the explanations are a few lines per mechanism and several of the linked standards are paywalled or registration-gated at source. The site carries no dates, changelog, or named maintainer, so there is no way to tell from the site itself how current any given page is.

## Status and sources

Status: **unknown** — the site is live and complete at https://automotive-network-security.com/standard_solutions.shtml and its overview page, but publishes no update history, so its maintenance state cannot be verified. Checked 2026-11-01.

## Related

- [What is Automotive MACsec?](what-is-automotive-macsec.md) — video training on the first mechanism in this site's catalogue
- [SOME/IP](concepts/someip.md) — the middleware whose deployments these mechanisms protect
