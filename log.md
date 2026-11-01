# Log

Append-only activity log for this KB (OpenShelf convention).

## [2026-10-31] init | KB created, bulk ingest of the source list

Created the KB and ingested hexsecs/awesome-automotive-security@b7b92a7:
228 entity stubs plus generated indexes, under a home-grown pilot spec.

## [2026-10-31] ingest | Retrofit to OpenShelf v0.1

Converged the pilot onto the OpenShelf standard (hexsecs/openkb): kb.yaml
manifest, wiki/ layout, OpenShelf page frontmatter (summary ≤160, verbatim
list text in body + list_summary), generated index.md + per-category
sub-indexes, AGENTS.md maintainer schema. Removed the parallel inventions
(sources.yaml, index.json, llms.txt, SPEC.md-as-format) — the format lives
in OpenShelf; local rules live in AGENTS.md. Verified with openshelf lint.

## [2026-10-31] deepen | CAN Bus Analysis depth slice + four concept pages

Deepened all 28 CAN Bus Analysis entity pages from stub to full (what it
is / how it works / where it fits / limits, `related` links, primary
sources checked 2026-10-31). Status calls from that check: CANalyse and
Kayak are `archived` (their repositories are archived); CANter stays
`unknown` (paper proof-of-concept, no released artefact). Added four
concept pages under `wiki/concepts/`: CAN injection, UDS seed/key
(SecurityAccess), key-fob relay attacks, and OCPP/charging attacks —
defensive, architecture-level synthesis cross-linked to the entity and
paper pages. Ingester updated to preserve unmanaged frontmatter and full
bodies across syncs and to list concept pages in the L1 index; verified
idempotent (0 created / 0 updated / 0 tombstoned) and `openshelf lint
--strict` clean. Landed by PR per the depth rule in AGENTS.md.

## [2026-10-31] deepen | Diagnostic Tools depth slice (issue #2)

Deepened all 19 Diagnostic Tools entity pages from stub to full (what
it is / how it works / where it fits / limits, `related` links, primary
sources checked 2026-10-31). Status calls from that check: most tools
are active; ford-ecu-bruteforcer, pq-flasher, uds-server, and udsim are
`maintenance` (dated or sparse recent activity); conescan and
uds-firmware-extraction stay `unknown` — conescan's README is empty and
its docs unreachable, so its page records source-tree evidence only and
says so, and uds-firmware-extraction has two commits from its creation
day. Gallia's research-only damage warning, Atlas's brick warning, and
pq-flasher's steering warnings are quoted on their pages. Landed by PR
per the depth rule in AGENTS.md.

## [2026-11-01] ingest | Sync to list 61ba124 + ingester identity fix

The list's 2026-10-31 merges (EVerest URL move, two VehicleSec 2026
papers) exposed two ingester flaws: identity was URL-only, so the EVerest
move tombstoned the page and created a duplicate, and every page was
rewritten whenever the source commit changed (last_checked re-stamped
without any verification). The ingester now matches by slug when a URL
moves, rewrites only pages whose own entry data changed, never moves
last_checked, and keeps tombstoned pages listed in their sub-index so
they stay reachable. This sync: 2 created (the VehicleSec papers),
1 updated (everest URL, in place), 0 tombstoned; re-run is 0/0/0.
## [2026-11-01] deepen | EV Charging Security depth slice (issue #3)

Deepened all 11 EV Charging Security pages from stub to full, with
what-it-is / how-it-works / where-it-fits / limits sections and primary
sources checked 2026-11-01. Documentation links are pinned to the checked
upstream commits. Added reciprocal sibling links, links back to the OCPP
charging-attacks concept, and reciprocal related metadata on the existing
OCPPStorm paper stub (its research depth remains for issue #12).

Status calls: 10 active (unarchived with observed 2026 default-branch
updates); OpenV2G maintenance (unarchived, latest checked commit is the
2025-11-12 import of 0.9.6, whose README records incremental fixes).
Maintenance is an editorial classification, not an upstream retirement
claim. No checked repository is archived. Each page records its evidence.

Limits retained explicitly: AcCCS's conflicting DIN-only versus newer
ISO/TLS/Plug & Charge instructions; dsV2Gshark's preliminary -20 support
and test-secret requirement; EmuOCPP's missing 1.6 transactions and stale
setup paths; OpenV2G's version-specific decoder fixes; WWCP's opt-in trust
roots, absent revocation checks and parent-checkout dependency; EVerest's
EvseV2G deprecation and configuration-dependent TLS/protocol behaviour.
No physical charging or security tools were executed.

Validation: full-tree ingest against the canon snapshot 61ba124 is
idempotent (0 created / 0 updated / 0 tombstoned); OpenShelf lint --strict
is clean; related links and pinned source endpoints were checked. The
shell proxy was unavailable, so repository and primary-source reads used
the GitHub connection; lint used the unmodified OpenShelf implementation
retrieved from hexsecs/openkb. One PR for this depth slice, per AGENTS.md.
