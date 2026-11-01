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
