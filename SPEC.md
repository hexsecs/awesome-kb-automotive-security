# SPEC — awesome-kb format (pilot v0.1, 2026-10-31)

Proven by `hexsecs/awesome-kb-automotive-security`, ingesting
`hexsecs/awesome-automotive-security`. If the pilot passes its review, this
spec is the format the other awesome-kb topic bases adopt.

## 1. Roles

- **Source list** (canon): a curated awesome list. Inclusion decisions, entry
  wording, and removals happen there, under that repo's own rules.
- **Knowledge base** (this repo): a derived layer. It expands canon entries
  into pages and synthesises across them. It holds no canon of its own.

## 2. Sources

`sources.yaml` names each ingested list:

```yaml
sources:
  - id: awesome-automotive-security
    repo: hexsecs/awesome-automotive-security
    file: README.md
```

Pilot scope: exactly one source. Multi-source ingest is a later version of
this spec, not a pilot feature.

## 3. Entry identity

An entry's identity is its **normalised URL** — the source list validator's
rule: lowercased, `https://` and trailing slash ignored. Its page slug derives
from the entry name (lowercase, non-alphanumerics to `-`, de-duplicated with a
numeric suffix). A rename that keeps the URL keeps the page; a URL change is a
new page plus a tombstone for the old one.

## 4. Entry pages

`entries/<slug>.md`, YAML frontmatter:

| Field | Meaning |
| --- | --- |
| `title` | Entry name, verbatim from the list |
| `url` | Canonical URL, verbatim from the list |
| `source` | Source list id (`sources.yaml`) |
| `source_section` | The `##` section the entry sits in on the list |
| `source_commit` | Short SHA of the list commit ingested |
| `status` | `stub` (generated only) or `full` (verified depth added) |
| `summary` | The list's one-line description, verbatim |

Body of a stub: the summary, the source section, and pointers. A `full` page
may add sections (what it does, requirements, protocols, related entries and
concepts, notes) — every factual claim in added depth must be verifiable from
the resource itself or a cited source; unsourced synthesis does not land.

## 5. Concept pages

`concepts/<slug>.md`, frontmatter: `title`, `status` (`draft`/`full`),
`related_entries` (slugs). Concept pages synthesise across sections — a
protocol, an attack class, a workflow. They link entries; they never
introduce a resource that is not on the list.

## 6. Ingest contract

`tools/ingest.py` parses the source README with the same entry grammar the
list's own validator enforces (`* [name](url) - desc` under `##` sections),
and:

- creates a stub for every entry with no page,
- updates `source_section` / `summary` / `source_commit` when the list's
  wording or placement changes (flagging `full` pages for re-check rather
  than overwriting their added depth),
- tombstones pages whose URL has left the list: `status: delisted` plus the
  removal reason when the list's `data/decisions.toml` records one,
- regenerates `index.json` and `llms.txt`.

Ingest is deterministic and idempotent: same source commit in, byte-identical
tree out (no wall-clock timestamps in generated files).

## 7. Machine layer

- `index.json`: `{source, source_commit, count, entries: [{slug, title, url,
  section, status, file}]}` — the one file an agent loads to know the KB.
- `llms.txt`: a short map of the KB (what it is, where the index and the
  concept pages live), following the llms.txt convention.

## 8. Freshness

Per-page freshness rides on ingest: a page whose `source_commit` is behind
the list's HEAD is stale by definition, and the next ingest run closes the
gap. Health facts about a resource itself (archived, dormant, moved) come
from the list's own health tooling and land as frontmatter in a later spec
version; pilot pages do not assert them.
