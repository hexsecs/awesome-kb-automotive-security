# Maintainer schema — Automotive Security (Awesome KB)

This KB conforms to the **OpenShelf** standard (`openshelf: "0.1"`,
`profile: awesome`) — spec and schemas live in
[hexsecs/openkb](https://github.com/hexsecs/openkb); this file carries only
what is local to this KB. Read `kb.yaml` for the declared layout.

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
- `index.md` — the L1 index, generated from page frontmatter; it reads as a
  classic awesome list. Do not edit by hand.
- `tools/ingest.py` — the ingester (see `x-ingest` in `kb.yaml`).
- `log.md` — append-only activity log, one `## [YYYY-MM-DD] <op> | <title>`
  heading per operation.

## Page rules (awesome profile, local deltas)

- `summary` ≤ 160 chars (OpenShelf contract). The list's verbatim
  description lives in the body and in `list_summary`.
- `depth: stub | brief | full | deep` (OpenShelf SPEC §4.5): stubs are
  generated; a page becomes `full` when a human/LLM adds real depth — what
  it is, how it works, outbound links checked, and `related` links to
  sibling pages. `brief` is the shortest authored tier (pointer entries);
  `deep` is the rare research-grade tier, loaded on demand only.
- `created` is the date the page first entered the KB (OpenShelf SPEC
  §4.2): the ingester stamps it from the source commit date at stub
  creation and preserves it verbatim thereafter; it never changes.
  Concept pages are hand-written, so their author sets `created` to the
  date the page is added. Existing pages were backfilled 2026-11-01 from
  each file's first commit in this repo (232 pages 2026-10-31, 7 pages
  2026-11-01). It is distinct from `updated` (last substantive change)
  and `last_checked` (last verification of the listed thing itself).
- `status` is the *resource's* status (active / maintenance / archived /
  unknown), verified when `last_checked` is stamped. Ingest sets `unknown`;
  a delisted entry's page is tombstoned to `archived`, never deleted.
- The ingester preserves unmanaged frontmatter blocks (`related`,
  `license`, a richer `sources`, …) and `full` bodies verbatim across
  syncs, and lists `wiki/concepts/` pages in the generated L1 index.

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
- **lint** — `openshelf lint .` must report no errors before a PR merges.
