# Kill List

Kept by Clyde, the cowboy coding agent — whether the humans care or not.

**Town:** awesome-kb-automotive-security
**Status:** being cleaned

| # | Date found | Bug | Where | Status | How it died | PR | Clyde's note |
|---|------------|-----|-------|--------|-------------|-----|--------------|
| 1 | 2026-11-20 | Unindented YAML `related:` lists invisible | `tools/link_check.py:30`, `tools/ingest.py:related_count` | dead | shared YAML parser + tests | [#103](https://github.com/hexsecs/awesome-kb-automotive-security/pull/103) | YAML says list. Parser says no. |
| 2 | 2026-11-20 | Inline `related:` with trailing comment invisible | `tools/link_check.py:30` | dead | comment-tolerant regex + test | [#103](https://github.com/hexsecs/awesome-kb-automotive-security/pull/103) | Comments hide friends. |
| 3 | 2026-11-20 | UTF-8 BOM defeats frontmatter detection | `tools/link_check.py:29` | dead | BOM-tolerant frontmatter regex + test | [#103](https://github.com/hexsecs/awesome-kb-automotive-security/pull/103) | Three invisible bytes, one silent failure. |
| 4 | 2026-11-20 | Bad `--root` reports a clean KB | `tools/link_check.py:100`, `tools/link_audit.py:43` | dead | root validation, exit 2 + tests | [#103](https://github.com/hexsecs/awesome-kb-automotive-security/pull/103) | Zero pages, all clear. Sure. |
| 5 | 2026-11-20 | Link resolution escapes the KB root | `tools/link_check.py:90` | dead | containment check + test | [#103](https://github.com/hexsecs/awesome-kb-automotive-security/pull/103) | `..` needs no invitation. |
| 6 | 2026-11-20 | Audit stem resolution depends on set order | `tools/link_audit.py:73` | dead | sorted candidates + test | [#103](https://github.com/hexsecs/awesome-kb-automotive-security/pull/103) | Coin-flip metrics. |
| 7 | 2026-11-20 | Entity named `index-*` misread as generated index | `tools/link_audit.py:63` | dead | frontmatter `type:` wins + test | [#103](https://github.com/hexsecs/awesome-kb-automotive-security/pull/103) | Name tags lie. Frontmatter doesn't. |
| 8 | 2026-11-20 | List URLs with parentheses silently dropped | `tools/ingest.py:73` | at large | — | — | Wikipedia ate the entry. |
| 9 | 2026-11-20 | Single-quoted YAML scalars mis-parsed | `tools/ingest.py:221` | at large | — | — | Only double quotes got the memo. |
| 10 | 2026-11-20 | Tab-indented frontmatter lost on rewrite | `tools/ingest.py:216` vs `:153` | at large | — | — | Two parsers, one file, no truth. |
| 11 | 2026-11-20 | Long summaries collapse to a single character | `tools/ingest.py:114` | at large | — | — | Word boundary, meet word. |
| 12 | 2026-11-20 | `http://` and `https://` treated as different identities | `tools/ingest.py:93` | at large | — | — | Scheme change, identity crisis. |
| 13 | 2026-11-20 | New entity slug collides with a concept stem | `tools/ingest.py:450` | at large | — | — | Two pages, one name, no warning. |
| 14 | 2026-11-20 | Section-slug collision overwrites a category index | `tools/ingest.py:547` | at large | — | — | One heading eats another. |
| 15 | 2026-11-20 | Stale category indexes never removed | `tools/ingest.py:543` | at large | — | — | Facet indexes got cleanup. Categories didn't. |
| 16 | 2026-11-20 | Duplicate-URL pages collapse in ingester | `tools/ingest.py:442` | at large | — | — | One page goes invisible. |
| 17 | 2026-11-20 | URL-move fallback misses suffixed slugs | `tools/ingest.py:461` | at large | — | — | `-2` never gets called home. |
| 18 | 2026-11-20 | Tombstone rewrites the first `status:` anywhere | `tools/ingest.py:509` | at large | — | — | Whole-file regex, whole-file trouble. |
| 19 | 2026-11-20 | Missing dates fabricated from source commit | `tools/ingest.py:490` | at large | — | — | Verified by nobody. Dated by everybody. |
| 20 | 2026-11-20 | One unreadable page aborts ingest | `tools/ingest.py:245` | at large | — | — | One bad byte holds the town hostage. |
| 21 | 2026-11-20 | One unreadable page aborts link mining and backfill | `tools/link_mine.py:161`, `tools/backfill_navigation.py:58` | at large | — | — | Same bad byte, more victims. |
| 22 | 2026-11-20 | Non-git source gives a raw traceback | `tools/ingest.py:434` | at large | — | — | Error handling took the day off. |
| 23 | 2026-11-20 | `--fill-only` stats describe unmined sets | `tools/link_mine.py:296` | at large | — | — | Report counts what didn't happen. |
| 24 | 2026-11-20 | Dead entries in the generic-phrase filter | `tools/concept_scan.py:50` | at large | — | — | Spaces in a word token. Classic. |
| 25 | 2026-11-20 | Two pages carry facets stale after deepening | `wiki/concepts/bootloader-stages.md`, `wiki/concepts/shared-and-default-secrets.md` | at large | — | — | Facet indexes are trailing the prose. |
| 26 | 2026-11-20 | Backfill never corrects an existing `cluster:` | `tools/backfill_navigation.py:100` | at large | — | — | Insert-only is not update. |
| 27 | 2026-11-20 | DoIP lives in two concept clusters | `tools/taxonomy.py:244`, `:252` | at large | — | — | Two homes, one page, no consistency. |
| 28 | 2026-11-20 | CAN facet regex matches the English word "can" | `tools/taxonomy.py:35` | at large | — | — | Modal verb in a bus costume. |
| 29 | 2026-11-20 | Facet counts mix entity and concept pages | `tools/ingest.py:272`, `:534` | at large | — | — | Two numbers, both called "pages". |
| 30 | 2026-11-20 | Untriaged `depth_note` rationale dropped from queue | `tools/ingest.py:335` | at large | — | — | Note kept, note hidden. |
| 31 | 2026-11-20 | Symlinked pages let tools write outside the KB | `tools/ingest.py:444`, `tools/backfill_navigation.py:115`, `tools/link_mine.py:158` | at large | — | — | Follow the link, leave the repo. |
| 32 | 2026-11-20 | Unquoted frontmatter values allow YAML injection | `tools/ingest.py:174`, `:181` | at large | — | — | Newline in a UID, new key in a page. |
| 33 | 2026-11-20 | Maintenance tools emit unquoted YAML values | `tools/link_mine.py:128`, `tools/backfill_navigation.py:81` | at large | — | — | Filenames make bad list items. |
| 34 | 2026-11-20 | List text injected raw into generated Markdown | `tools/ingest.py:199`, `:282` | at large — human's call | — | — | Renderer policy is above Clyde's pay grade. |
| 35 | 2026-11-20 | Authored body discarded when `depth:` says `stub` | `tools/ingest.py:494` | at large — human's call | — | — | Truth lives in the body, not the label. |
| 36 | 2026-11-20 | Non-Latin titles collapse to `entry` slugs | `tools/ingest.py:99` | at large — human's call | — | — | Rename scheme is a town decision. |
| 37 | 2026-11-20 | Markdown link forms skipped or mis-parsed | `tools/link_check.py:28` | dead | broader link regex + tests | [#103](https://github.com/hexsecs/awesome-kb-automotive-security/pull/103) | Angle brackets, parentheses, single quotes. All ignored. |
