# Awesome KB — Automotive Security

A living, LLM-friendly knowledge base for automotive security, built on top of
the curated awesome list
[hexsecs/awesome-automotive-security](https://github.com/hexsecs/awesome-automotive-security).

**This repo is the pilot** for turning awesome lists into knowledge bases:
the list stays the canonical, human-curated inventory; this KB is the depth
and machine layer on top of it. Pilot review date: **2026-11-28** (see
"Pilot terms" below).

**Browse the rendered site:** [hexsecs.github.io/awesome-kb-automotive-security](https://hexsecs.github.io/awesome-kb-automotive-security/)
— the searchable reading view of this KB, rebuilt from `main` on every push.
This KB is also imported into the composed network site at
[hexsecs.github.io/awesome-kb](https://hexsecs.github.io/awesome-kb/).

## Format: OpenShelf

This KB conforms to the [OpenShelf](https://github.com/hexsecs/openshelf)
standard (`openshelf: "1.4"`, `profile: awesome`): a `kb.yaml` manifest,
pages with `title` + one-line `summary` frontmatter, progressive context
(L0 description → L1 `index.md` → L2 pages → L3 sources), and an index that
still reads as a classic awesome list. It replaced the home-grown pilot spec
that this repo started with on 2026-10-31 — the format lives in OpenShelf,
and the local rules (canon, ingest, depth) live in
[AGENTS.md](AGENTS.md), per the standard's own layout.

## The canon rule

**The list is canon; ingest flows list → KB only.** A resource appears here
because it is on the list — never the other way around. Research done in
this KB may *propose* additions to the list, but list changes go through the
list's own contribution rules and maintainers. If the wiki ever earns
source-of-truth status, that inversion will be a deliberate, documented
decision — not drift.

## Layout

- `kb.yaml` — the OpenShelf manifest (id, description, layout, ingest config).
- `index.md` — L1 index, generated from page frontmatter; reads as the list.
- `wiki/` — the pages: one entity page per list entry, concept pages under
  `wiki/concepts/`, and a generated sub-index per list section.
- `tools/ingest.py` — the deterministic ingester (see below).
- `AGENTS.md` — the maintainer schema: local rules for humans and LLMs.
- `log.md` — append-only activity log.

## How it stays in sync

`tools/ingest.py` parses the list's README with the list validator's own
entry grammar, keyed on each entry's normalised URL. It creates stub pages
for new entries, refreshes provenance on existing pages without touching
added depth, and tombstones pages whose entry leaves the list — pages are
never silently deleted. Dates come from the source commit, so a sync is
byte-deterministic and safe to run in CI. Check conformance any time with
`openshelf lint .`

## Landing rules

- **Machine ingest syncs** land as direct commits (deterministic output).
- **Synthesis and depth** — filling in a stub, concept pages, cross-links —
  land by pull request, maintainer-merged.

## Pilot terms

- **Scope:** exactly one source list (this one). Other awesome-kb topic
  bases adopt OpenShelf directly; they don't copy this pilot's history.
- **Review date: 2026-11-28.** The pilot lives if, by then: ingest drift is
  zero unprocessed changes over a week, concept pages are gaining depth,
  and maintainer review load stays under ~15 min/week. If pages are still
  undeepened stubs at review, the repo is archived and the list carries on
  alone.

## License

CC0 1.0, matching the source list — see [LICENSE](LICENSE). (OpenShelf
recommends CC-BY-4.0; this KB keeps the source list's license so derived
pages carry the same terms as the list they mirror.)
