---
uid: 01a19d3c-af39-7d10-af6e-1c06591af5f8
title: "Awesome Vehicle Security"
summary: "Long-running curated list of vehicle security resources, hardware, software, researchers, and manufacturer disclosure programs."
type: entity
category: "Related Awesome Lists"
url: "https://github.com/jaredthecoder/awesome-vehicle-security"
status: active
last_checked: 2026-11-01
created: 2026-10-31
updated: 2026-11-17
depth: full
source_list: awesome-automotive-security
source_commit: b7b92a7
list_summary: "Long-running curated list of vehicle security resources, hardware, software, researchers, and manufacturer disclosure programs."
related:
  - awesome-canbus
  - awesome-embedded-security
  - awesome-ev-charging
  - awesome-connected-things-sec
  - automotive-security-timeline
sources:
  - url: "https://github.com/jaredthecoder/awesome-vehicle-security"
    retrieved: 2026-11-01
  - url: "https://raw.githubusercontent.com/jaredthecoder/awesome-vehicle-security/master/README.md"
    retrieved: 2026-11-17
  - url: "https://github.com/hexsecs/awesome-automotive-security"
    retrieved: 2026-11-01
facets: [learning]
---

Long-running curated list of vehicle security resources, hardware, software, researchers, and manufacturer disclosure programs.

The field's long-running generalist list, maintained by Jared Smith (jaredthecoder) since 2016: a large Learn section (articles, presentations, books, research papers, courses, blogs, newsletters, conferences, podcasts, and who to follow), then projects, hardware, software organised by language, and companies/jobs including manufacturers' coordinated-disclosure programmes.

It is the broadest of the related lists and the most beginner-friendly — if you are new to vehicle security, its Learn section is the widest front door available. The overlap with this KB's parent list is large; the difference is emphasis: this list ranges over the whole hobbyist-and-industry landscape, where the parent list (and this KB) concentrate on security research.

## How it works

The resource is a single annotated README, not a site or a database. Its table of contents defines the taxonomy, and the entries are links with a one-line editorial gloss rather than metadata records. Reading it is a browse, not a query.

**The top-level structure** is: Related Lists; Learn; Projects; Hardware; Software; Companies and Jobs; Other Awesome Lists; Contributing. Two details matter for how to use it:

- **Learn is the front door.** It splits into Articles, Presentations, Books, Research Papers, Courses, Blogs, Websites, Newsletters, Conferences, Who to Follow, Podcasts and Episodes, and Miscellaneous. The historical backbone is the 2010–2015 research canon — Koscher et al., Checkoway et al., and the full Miller/Valasek sequence (2013 networks paper, the "Car Hacking for Poories" guide, the 2014 remote-surface survey, the 2015 Jeep hack, the 2016 CAN-injection work) — plus later talks through 2024 on V2GEvil and disclosure-war stories. The Newsletters section is an explicit call for contributions, so it is not a curated set.
- **Software is sliced by implementation language** (C, Java, C++, Python, Go, JavaScript) under a separate Applications heading. That is a practical organising choice for a tooling directory: you find can-utils and dbcc under C, CANdevStudio and CanCat under C++, and python-can, cantools, Scapy, Caring Caribou and canmatrix under Python. The boundary is soft — CanCat appears in both C++ and Python because its API is Python but its core is C++.

**Hardware** is a long, untiered catalogue rather than a buying guide: Arduino CAN shields, ELM327, Cantact, INTREPID tools, CANBadger, CANBus Triple, USBtin, OpenXC, Macchina M2, PandwaRF, a CAN MITM bridge, PiCCANTE and the AutoPi dongle. The list explicitly points to an external "car hacking tools trade" article for comparison, so it does not rank them itself.

**Companies and Jobs** ends with a **Coordinated Disclosure** subsection — GM on HackerOne, Stellantis and Tesla on Bugcrowd, the ASRG fallback disclosure process, and Zeekr/Geely. That is the part of the list with the most direct operational value for a researcher looking for a reporting path, and it is the reason the entry belongs in a security KB rather than a general car-hacking index.

**Maintenance** is lightweight and community-driven: contributions are directed to a `contributing.md` file, and the maintainer asks for help explicitly near the top. The repo also carries a "Related Lists" pointer to protocol-specialist lists (Awesome CAN Bus, Awesome LIN Bus) and a final "List of lists" section of general security indexes.

## Where it fits

In this KB it is the generalist sibling, not a source of depth: the [Awesome CANbus](awesome-canbus.md) and [Awesome Embedded Security](awesome-embedded-security.md) entries cover the two specialist layers it points to, and the parent list's own `awesome-automotive-security` catalogues the research-focused resources it overlaps. Its historical Learn section is a readable companion to the KB's [Automotive Security Timeline](automotive-security-timeline.md). Where the KB's entity pages go deep on individual tools and papers, this list is the map that shows how a newcomer found them.

## Limits and safety notes

It is a curated index, not an authoritative or complete catalogue: annotations are the maintainer's one-line judgements, several entries are a decade old, and many links point to vendor pages, blog posts or Amazon listings whose current state was not re-verified here. The licence is CC0-1.0 and commits continued into 2026 (last push 2026-05-30, 4,740 stars when checked), but a curated list ages by link rot rather than by version number. The disclosure programmes are named as listed; their current scope and terms must be read on the platform itself before use. The README was read from the repository's master branch on 2026-11-17; the live file can move between checks.

## Status and sources

Status: **active** — commits continue in 2026 (last push 2026-05-30); not archived; 4,740 stars; CC0-1.0. Source: https://github.com/jaredthecoder/awesome-vehicle-security — checked 2026-11-01.

## Related

- [Awesome CANbus](awesome-canbus.md) — the CAN-focused specialist list
- [Awesome Embedded Security](awesome-embedded-security.md) — the embedded layer underneath vehicle security
