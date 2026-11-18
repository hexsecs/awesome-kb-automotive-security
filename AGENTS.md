# Maintainer schema — Automotive Security (Awesome KB)

This KB conforms to the **OpenShelf** standard (`openshelf: "1.4"`,
`profile: awesome`) — spec and schemas live in
[OpenNorms/openshelf](https://github.com/OpenNorms/openshelf); this file carries only
what is local to this KB. Read `kb.yaml` for the declared layout.
The maintenance **method** (deepening pipeline, evidence discipline,
concept mining, gates, traps) lives in the awesome-kb skill —
[hexsecs/awesome-kb-skill](https://github.com/hexsecs/awesome-kb-skill) —
not in this file; this file wins on local facts, the skill on method,
the spec on format.

## The canon rule

[hexsecs/awesome-automotive-security](https://github.com/hexsecs/awesome-automotive-security)
is canon. Ingest flows list → KB only: a resource exists in this KB because
it is on the list. Research here may *propose* list additions, but never adds
a page for an unlisted resource. The list's own contribution rules decide
what gets listed.

## Layout

- `wiki/<slug>.md` — entity pages, one per list entry (`type: entity`).
- `wiki/concepts/<slug>.md` — concept pages (`type: concept`), cross-linked
  synthesis over entities; listed in `index.md` directly.
- `wiki/index-<category>.md` — generated sub-index per list section
  (no frontmatter; do not edit by hand).
- `wiki/index-facet-<slug>.md` — generated cross-cutting topic index, from the
  page's `facets:` frontmatter. Facets come from the curated vocabulary in
  `tools/taxonomy.py`; they may be edited only there, then propagated with
  `python3 tools/backfill_navigation.py`. Do not edit the generated index.
- `wiki/index-concept-map.md`, `wiki/index-glossary.md`,
  `wiki/index-needs-attention.md` — generated navigation and maintenance hubs.
  Do not edit by hand.
- `index.md` — the L1 index, generated from page frontmatter; it reads as a
  classic awesome list. Do not edit by hand.
- `tools/ingest.py` — the ingester (see `x-ingest` in `kb.yaml`).
- `raw/` — L3 evidence staging: local captures go here only when a page needs
  a durable copy; the upstream list and page `sources:` URLs remain canonical.
- `log.md` — append-only activity log, one `## [YYYY-MM-DD] <op> | <title>`
  heading per operation.

## Page rules (awesome profile, local deltas)

- `summary` ≤ 160 chars (OpenShelf contract). The list's verbatim
  description lives in the body and in `list_summary`.
- `depth: stub | brief | full | deep` (OpenShelf SPEC §4.5): stubs are
  generated; a page becomes `full` when a human/LLM adds real depth — what
  it is, how it works, outbound links checked, and `related` links to
  sibling pages. `brief` is the shortest authored tier (pointer entries):
  a short orientation — who it is for, what you actually get, caveats —
  with the outbound link checked and status verified, but no
  how-it-works section; keeping `full` meaningful is the point.
  `deep` is the rare research-grade tier, loaded on demand only.
- `depth_note` (on `brief` pages) records the triage decision: either
  `brief by design — <reason>` (an intentional pointer — a book, talk,
  dataset or list with no accessible primary text) or `deepen candidate —
  <reason>` (a full source exists and the page is queued for deepening).
  It is an unmanaged frontmatter block, preserved by the ingester. The
  generated needs-attention hub splits brief pages by this key, so
  intentional pointers no longer read as unfinished work.
- `created` is the date the page first entered the KB (OpenShelf SPEC
  §4.2): the ingester stamps it from the source commit date at stub
  creation and preserves it verbatim thereafter; it never changes.
  Concept pages are hand-written, so their author sets `created` to the
  date the page is added. Existing pages were backfilled 2026-11-01 from
  each file's first commit in this repo (232 pages 2026-10-31, 7 pages
  2026-11-01). It is distinct from `updated` (last substantive change)
  and `last_checked` (last verification of the listed thing itself).
- `uid` is a page's durable identity (OpenShelf SPEC §4.1): minted once
  by tooling — never written by hand — when the page first enters the KB,
  and preserved verbatim across renames, moves and ingests. The ingester
  mints it for new stubs; existing pages and the KB itself were minted
  2026-11-02 with `openshelf uid` at the spec 1.4 adoption.
- `status` is the *resource's* status (active / maintenance / archived /
  published / unknown), verified when `last_checked` is stamped. Ingest
  sets `unknown` — except the Research Papers category, whose entries are
  finished works and get `published` (OpenShelf SPEC §9.2: `published` is
  for completed publications; `unknown` is for living resources whose
  state is unverified). A delisted entry's page is tombstoned to
  `archived`, never deleted.
- `status_note` records the evidence behind a verification stamp (e.g.
  "GitHub repo not archived; last push 2026-02-10"). It is written on a
  verification pass together with `status` and `last_checked`, and is an
  unmanaged block the ingester preserves verbatim.
- The ingester preserves unmanaged frontmatter blocks (`related`,
  `status_note`, `license`, a richer `sources`, …) and `full` bodies verbatim
  across syncs, and lists `wiki/concepts/` pages in the generated L1 index.

## Operations

- **ingest** — `python3 tools/ingest.py` after the list changes; creates
  stubs, refreshes provenance, tombstones delistings. Deterministic:
  dates come from the source commit. Commit machine syncs directly.
- **deepen** — pick stub(s), write depth, set `depth: full`, add `related`.
  Lands by PR. Agents maintain this KB (owner's delegation, 2026-10-31):
  the maintaining agent merges the PR when it meets the issue's
  definition of done with gates green; the owner merges personally only
  when he chooses to review a specific PR.
- **query** — read `index.md`, then pages, then sources. File useful
  answers back as pages so explorations compound.
- **navigate** — edit `tools/taxonomy.py` (facets, glossary, concept clusters and
  reading paths), run `python3 tools/backfill_navigation.py`, then
  `python3 tools/ingest.py`. Both tools are idempotent; the ingester owns all
  `index*.md` files.
- **lint** — `openshelf lint .` must report no errors before a PR merges.
