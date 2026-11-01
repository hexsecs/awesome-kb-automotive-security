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
