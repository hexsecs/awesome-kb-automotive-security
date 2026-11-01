# SPEC — superseded by OpenShelf

This repo began (2026-10-31) with a home-grown pilot spec. The same night it
was superseded: the format is the **OpenShelf** standard, maintained in
[hexsecs/openkb](https://github.com/hexsecs/openkb) (SPEC.md + JSON schemas +
the `openshelf` CLI/lint/MCP tooling), and this KB conforms to it
(`openshelf: "0.1"`, `profile: awesome` — see `kb.yaml`).

What was local to the pilot — the canon rule, the ingest contract, the
`depth` field, landing rules — moved to [AGENTS.md](AGENTS.md), the
maintainer schema OpenShelf's layout reserves for exactly that. Nothing in
this file is normative any more; it remains only as a pointer so old links
don't dead-end.
