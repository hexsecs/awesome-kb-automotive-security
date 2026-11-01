# Awesome KB — Automotive Security

A living, LLM-friendly knowledge base for automotive security, built on top of
the curated awesome list
[hexsecs/awesome-automotive-security](https://github.com/hexsecs/awesome-automotive-security).

**Pilot project (started 2026-10-31).** This repo is the pilot for the
awesome-kb idea: awesome lists stay the human-curated canon, and knowledge
bases like this one ingest them and add the depth a one-line entry can't hold —
per-resource pages, cross-cutting concept pages, and a machine-readable index
an LLM can actually query.

## The canon rule

**The awesome list is the source of truth. This repo ingests it; it never
competes with it.**

- A resource enters this KB only by first appearing on the list.
- Entry pages here carry provenance: source list, source section, and the
  list commit they were ingested from (see `SPEC.md`).
- If the list removes a resource, its page here is tombstoned — marked
  delisted with the reason, never silently deleted.
- Research done here that finds a new resource is proposed *to the list*
  (its normal suggestion flow), not added here directly.

## Layout

- `entries/` — one page per resource on the list. Stub pages are generated
  by the ingester; a page becomes a *full* page when someone adds verified
  depth (what it does, hardware/protocols, gotchas, related work).
- `concepts/` — synthesis pages that cut across list sections (protocols,
  attack classes, workflows). Written by humans/bots, landed by PR.
- `index.json` — the full entry index, generated; load this instead of
  scraping markdown.
- `llms.txt` — a map of this KB for LLM crawlers/agents.
- `sources.yaml` — the lists this KB ingests (pilot: one).
- `tools/ingest.py` — the ingester. Deterministic and idempotent: same
  source commit in, same tree out.
- `SPEC.md` — the format spec this pilot is proving, intended to be reused
  by the other awesome-kb topic bases.

## Landing rules

- Machine ingest (stub generation, index, freshness metadata): direct
  commits — it is deterministic and verifiable by re-running the ingester.
- Synthesis (concept pages, depth added to entry pages): pull requests,
  maintainer merges. Anything with an opinion in it gets human review.

## Pilot review

Four weeks after bulk ingest (2026-11-28), this pilot is judged: it lives if
ingest drift stays at zero unprocessed changes over a week, concept pages are
gaining depth, and maintainer review load stays under ~15 minutes a week. If
the pages are still stubs nobody has deepened, the repo is archived — a worse
list wearing a wiki costume is not a knowledge base.
