#!/usr/bin/env python3
"""Ingest the source awesome list into this KB, in OpenShelf format.

The list is canon (see AGENTS.md). This ingester parses its README with the
same entry grammar the list's own validator enforces — `* [name](url) - desc`
under `##` sections — and maintains this KB's OpenShelf awesome profile:

- `wiki/<slug>.md` — one entity page per list entry (frontmatter per the
  OpenShelf page schema; `summary` is capped at 160 chars, the list's
  verbatim description is kept in the body and in `list_summary`),
- `wiki/index-<category>.md` — one sub-index per list section, no
  frontmatter, generated from page frontmatter,
- `index.md` — the L1 index linking the sub-indexes; reads as the list.

Existing pages with an authored depth (`brief`, `full`, or `deep`)
keep their body; only provenance frontmatter is refreshed. Stub pages
are regenerated from the entry. Unmanaged frontmatter blocks on an existing page
(`related`, `tags`, a richer `sources`, …) are preserved verbatim, so
hand-written depth survives a sync. Concept pages under `wiki/concepts/`
are listed in the L1 index.

Entry identity is the normalised URL, with a slug fallback: if an entry's
URL moves but its name still slugifies to an existing page's stem, the page
is updated in place (a move is not a delisting). Pages whose entry leaves
the list entirely are tombstoned (`status: archived`, body note appended
once), never deleted, and stay listed in their sub-index so every page
remains reachable from the index.

A page is rewritten only when its own entry data changes (title, URL,
section, or list description). `last_checked` is a human/agent verification
stamp and is never moved by an ingest; `updated` and `source_commit`
advance only on pages actually rewritten. `created` is stamped from the
source commit date when a stub is first created and preserved verbatim
thereafter — it records when the page first entered the KB and never
changes (OpenShelf SPEC section 4.2). `uid` follows the same lifecycle
(SPEC sections 4.1/2): minted once when a page is first created — the one
deliberately non-deterministic stamp, since a uid must be random — and
preserved verbatim thereafter, so re-ingests stay byte-identical.
Deterministic and idempotent otherwise: dates come from the source
commit, never the wall clock; same source commit in, byte-identical
tree out.

- `wiki/index-facet-<slug>.md` — cross-cutting topic indexes, from page
  frontmatter `facets:` assigned by `tools/taxonomy.py`,
- `wiki/index-glossary.md` — acronym/standard hub,
- `wiki/index-concept-map.md` — clusters and reading paths over concepts,
- `wiki/index-needs-attention.md` — maintenance queue (unverified, orphaned,
  brief, stale or tombstoned pages); brief pages are split into deepen
  candidates, untriaged and triaged brief-by-design by their `depth_note`.

Usage: python3 tools/ingest.py [--source ../awesome-automotive-security]
"""

from __future__ import annotations

import argparse
import json
import re
import secrets
import subprocess
import sys
import time
import uuid
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from link_check import parse_related, split_frontmatter  # noqa: E402
from taxonomy import (CONCEPT_CLUSTERS, FACET_BY_SLUG, FACETS,  # noqa: E402
                      GLOSSARY, READING_PATHS)

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
ENTRY_RE = re.compile(
    r"^\* \[(?P<name>[^\]]+)\]\((?P<url>[^)]+(?:\([^)]*\)[^)]*)*)\) - (?P<desc>.+)$"
)
HEADING_RE = re.compile(r"^## (?P<title>.+)$")
SKIP_SECTIONS = {"Contents"}
SOURCE_ID = "awesome-automotive-security"
SOURCE_URL = "https://github.com/hexsecs/awesome-automotive-security"
KB_TITLE = "Automotive Security (Awesome KB)"
KB_DESC = ("Knowledge base for automotive security, ingested from the curated "
           "awesome list hexsecs/awesome-automotive-security.")


def mint_uid() -> str:
    """A fresh UUIDv7, the form OpenShelf SPEC section 4.1 recommends."""
    if hasattr(uuid, "uuid7"):
        return str(uuid.uuid7())
    ms = int(time.time() * 1000) & ((1 << 48) - 1)
    value = (ms << 80) | (0x7 << 76) | (secrets.randbits(12) << 64) \
        | (0b10 << 62) | secrets.randbits(62)
    return str(uuid.UUID(int=value))


def normalise(url: str) -> str:
    """The list validator's identity rule: case, trailing slash, scheme ignored."""
    u = url.rstrip("/").lower()
    return re.sub(r"^https?://", "", u)


def slugify(name: str, taken: set[str]) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "entry"
    base, n = slug, 2
    while slug in taken:
        slug = f"{base}-{n}"
        n += 1
    taken.add(slug)
    return slug


def q(value: str) -> str:
    """A YAML-safe double-quoted scalar (JSON strings are valid YAML)."""
    return json.dumps(value, ensure_ascii=False)


def short_summary(desc: str) -> str:
    """OpenShelf summary: <=160 chars, cut at a word boundary."""
    desc = desc.strip()
    if len(desc) <= 160:
        return desc
    cut = desc[:157].rsplit(" ", 1)[0].rstrip(",;:")
    if len(cut) < 80:
        # A long unbroken token after an early space would otherwise leave
        # almost nothing. Prefer a hard cut over an empty summary.
        cut = desc[:159].rstrip()
    return cut + "…"


def parse_list(readme: Path) -> list[dict]:
    entries, section = [], None
    for line in read_page(readme).splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            section = heading.group("title").strip()
            continue
        match = ENTRY_RE.match(line)
        if match and section and section not in SKIP_SECTIONS:
            entries.append({"title": match.group("name"),
                            "url": match.group("url"),
                            "section": section,
                            "summary": match.group("desc")})
    return entries


MANAGED_KEYS = {"title", "uid", "summary", "type", "category", "url", "status",
                "last_checked", "created", "updated", "depth", "source_list",
                "source_commit", "list_summary"}


def frontmatter_blocks(text: str) -> list[tuple[str, list[str]]]:
    """Split a page's frontmatter into (key, raw lines) top-level blocks."""
    if not text.startswith("---\n"):
        return []
    end = text.find("\n---\n", 4)
    if end == -1:
        return []
    blocks: list[tuple[str, list[str]]] = []
    for line in text[4:end].splitlines():
        top_level = line and not line.startswith((" ", "-"))
        if top_level and (": " in line or
                          (line.strip().endswith(":")
                           and line.strip()[:-1].isidentifier())):
            blocks.append((line.strip().split(":", 1)[0].strip(), [line]))
        elif blocks:
            blocks[-1][1].append(line)
    return blocks


def extra_blocks(text: str) -> list[list[str]]:
    """Frontmatter blocks the ingester does not manage, kept verbatim."""
    return [lines for key, lines in frontmatter_blocks(text)
            if key not in MANAGED_KEYS]


def frontmatter(e: dict, status: str, depth: str, date: str, commit: str,
                extras: list[list[str]] | None = None,
                last_checked: str | None = None,
                created: str | None = None,
                updated: str | None = None,
                uid: str | None = None) -> str:
    lines = ["---",
             f"uid: {q(uid or mint_uid())}",
             f"title: {q(e['title'])}",
             f"summary: {q(short_summary(e['summary']))}",
             "type: entity",
             f"category: {q(e['section'])}",
             f"url: {q(e['url'])}",
             f"status: {q(status)}",
             f"last_checked: {q(last_checked or date)}",
             f"created: {q(created or date)}",
             f"updated: {q(updated or date)}",
             f"depth: {q(depth)}",
             f"source_list: {q(SOURCE_ID)}",
             f"source_commit: {q(commit)}",
             f"list_summary: {q(e['summary'])}"]
    extras = extras or []
    for block in extras:
        lines.extend(block)
    if not any(block and block[0].startswith("sources:") for block in extras):
        lines += ["sources:",
                  f"  - url: {q(SOURCE_URL)}",
                  f"    retrieved: {q(date)}"]
    lines.append("---")
    return "\n".join(lines) + "\n"


def stub_body(e: dict) -> str:
    return (f"\n{e['summary']}\n\n"
            f"- **Resource:** {e['url']}\n"
            f"- **List section:** {e['section']}\n"
            f"- **Source:** [{SOURCE_ID}]({SOURCE_URL}) — the list is canon;"
            f" this page is a generated stub (`depth: stub`). Depth is added"
            f" by PR (see AGENTS.md).\n")


def split_page(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fields = {}
    for line in text[4:end].splitlines():
        if ": " in line and not line.startswith((" ", "\t")):
            key, raw = line.split(": ", 1)
            raw = raw.strip()
            try:
                fields[key.strip()] = json.loads(raw)
            except json.JSONDecodeError:
                if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
                    fields[key.strip()] = raw[1:-1]
                else:
                    fields[key.strip()] = raw
    return fields, text[end + 5:]


def parse_slugs(value: object) -> set[str]:
    """Read a YAML inline list (or a flat scalar) of slugs from split_page."""
    return set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(value)))


def related_count(text: str) -> int:
    """Count `related` targets in either frontmatter list shape."""
    return len(parse_related(split_frontmatter(text)[0]))


def read_page(path: Path) -> str:
    """Read a page with a clear error instead of a half-written ingest."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        sys.exit(f"ingest: cannot read {path}: {exc}")


def write_page(path: Path, text: str) -> None:
    """Write a page, refusing to follow a symlink out of the KB."""
    if path.is_symlink():
        sys.exit(f"ingest: refusing to write through symlink {path}")
    path.write_text(text, encoding="utf-8")


def all_pages() -> list[tuple[Path, dict, str]]:
    """Every authored page (entities and concepts), in stable path order."""
    pages = []
    for page in sorted(WIKI.rglob("*.md")):
        if page.name.startswith("index-"):
            continue
        fields, body = split_page(read_page(page))
        if "title" in fields:
            pages.append((page, fields, body))
    return pages


def write_facet_indexes(pages: list[tuple[Path, dict, str]],
                        section_order: list[str]) -> dict[str, int]:
    """One index per facet with at least two pages; return facet -> count."""
    grouped: dict[str, list[tuple[Path, dict]]] = {f.slug: [] for f in FACETS}
    for page, fields, _ in pages:
        for slug in parse_slugs(fields.get("facets", "")):
            if slug in grouped:
                grouped[slug].append((page, fields))

    counts: dict[str, int] = {}
    order = {name: i for i, name in enumerate(section_order)}
    for facet in FACETS:
        items = grouped[facet.slug]
        if len(items) < 2:
            continue
        counts[facet.slug] = len(items)
        lines = [f"# Facet: {facet.label}", "", facet.description, "",
                 "Generated from page frontmatter by tools/ingest.py;"
                 f" {len(items)} pages (entities and concepts)."
                 " Do not edit by hand.", ""]
        by_group: dict[str, list[str]] = {}
        for page, fields in items:
            group = ("Concepts" if fields.get("type") == "concept"
                     else str(fields.get("category", "Other")))
            target = ("concepts/" if group == "Concepts" else "") + page.stem
            by_group.setdefault(group, []).append(
                f"- [{fields['title']}]({target}.md) — {fields.get('summary', '')}")
        for group in sorted(by_group, key=lambda g: (order.get(g, 999), g)):
            lines += [f"## {group}", ""] + sorted(by_group[group]) + [""]
        write_page(WIKI / f"index-facet-{facet.slug}.md", "\n".join(lines))

    # Remove stale facet indexes when a facet drops below the threshold.
    for path in WIKI.glob("index-facet-*.md"):
        if path.stem.removeprefix("index-facet-") not in counts:
            path.unlink()
    return counts


def triage_kind(fields: dict) -> tuple[str, str]:
    """Classify a brief page's `depth_note` for the maintenance queue.

    Returns (kind, note) where kind is 'deepen', 'by-design' or 'untriaged';
    the note is the recorded rationale (empty when absent). The rationale is
    an unmanaged frontmatter key, so it survives ingests verbatim.
    """
    note = str(fields.get("depth_note", "")).strip()
    if note.startswith("deepen candidate"):
        return "deepen", note
    if note.startswith("brief by design"):
        return "by-design", note
    return "untriaged", note


def write_needs_attention(pages: list[tuple[Path, dict, str]],
                          source_date: str) -> int:
    """A deterministic maintenance queue, relative to the source commit date."""
    buckets: dict[str, list[str]] = {
        "Unverified resources": [], "Graph orphans": [],
        "Deepen candidates": [], "Untriaged briefs": [],
        "Stale verification": [], "Tombstoned pages": [],
        "Brief by design (no action)": [],
    }
    cutoff = date.fromisoformat(source_date) - timedelta(days=180)
    for page, fields, _ in pages:
        target = ("concepts/" if fields.get("type") == "concept" else "") + page.stem
        entry = f"- [{fields['title']}]({target}.md)"
        if str(fields.get("status", "")) == "unknown":
            buckets["Unverified resources"].append(entry)
        if related_count(read_page(page)) == 0:
            buckets["Graph orphans"].append(entry)
        if str(fields.get("depth", "")) == "brief":
            kind, note = triage_kind(fields)
            labelled = f"{entry} — {note}" if note else entry
            if kind == "deepen":
                buckets["Deepen candidates"].append(labelled)
            elif kind == "by-design":
                buckets["Brief by design (no action)"].append(labelled)
            else:
                buckets["Untriaged briefs"].append(labelled)
        checked = str(fields.get("last_checked", ""))
        if checked:
            try:
                if date.fromisoformat(checked) < cutoff:
                    buckets["Stale verification"].append(
                        f"{entry} — last checked {checked}")
            except ValueError:
                pass
        if str(fields.get("status", "")) == "archived":
            buckets["Tombstoned pages"].append(entry)

    lines = ["# Needs attention", "",
             "Generated from page frontmatter by tools/ingest.py. A page may"
             " appear in more than one queue. 'Brief by design' entries are"
             " triaged pointers needing no action. Do not edit by hand.", ""]
    for name, entries in buckets.items():
        lines += [f"## {name} ({len(entries)})", ""]
        if entries:
            lines += sorted(entries)
        else:
            lines.append("_None._")
        lines.append("")
    write_page(WIKI / "index-needs-attention.md", "\n".join(lines))
    actionable = sum(len(v) for k, v in buckets.items()
                     if k != "Brief by design (no action)")
    return actionable


def write_glossary(pages: list[tuple[Path, dict, str]]) -> None:
    titles = {("concepts/" if f.get("type") == "concept" else "") + p.stem: f
              for p, f, _ in pages}
    lines = ["# Glossary", "",
             "Acronyms and standards used across this KB, with the page that"
             " explains each one. Generated from tools/taxonomy.py;"
             " do not edit by hand.", ""]
    for entry in GLOSSARY:
        target = entry.target + ".md"
        fields = titles.get(entry.target)
        if fields is None or not (WIKI / target).exists():
            continue
        lines.append(f"- **{entry.term}** — {entry.expansion}."
                     f" See [{fields['title']}]({target}) — {entry.note}")
    lines.append("")
    write_page(WIKI / "index-glossary.md", "\n".join(lines))


def write_concept_map(pages: list[tuple[Path, dict, str]]) -> None:
    concepts = {p.stem: f for p, f, _ in pages
                if f.get("type") == "concept"}
    lines = ["# Concept map", "",
             "The concept layer organised by theme, with reading paths through"
             " it. Generated from tools/taxonomy.py and concept frontmatter;"
             " do not edit by hand.", ""]

    placed: set[str] = set()
    for cluster in CONCEPT_CLUSTERS:
        lines += [f"## {cluster.label}", "", cluster.description, ""]
        for slug in dict.fromkeys(cluster.concepts):
            fields = concepts.get(slug)
            if fields is None:
                continue
            placed.add(slug)
            lines.append(f"- [{fields['title']}](concepts/{slug}.md)"
                         f" — {fields.get('summary', '')}")
        lines.append("")

    orphans = [s for s in sorted(concepts) if s not in placed]
    if orphans:
        lines += ["## Unclustered concepts", "",
                  "Concepts added since the taxonomy was last updated:", ""]
        for slug in orphans:
            fields = concepts[slug]
            lines.append(f"- [{fields['title']}](concepts/{slug}.md)"
                         f" — {fields.get('summary', '')}")
        lines.append("")

    lines += ["## Reading paths", ""]
    for path in READING_PATHS:
        lines += [f"### {path.title}", "", path.description, ""]
        for i, slug in enumerate(path.steps, 1):
            fields = concepts.get(slug)
            if fields is not None:
                lines.append(f"{i}. [{fields['title']}](concepts/{slug}.md)")
        lines.append("")
    write_page(WIKI / "index-concept-map.md", "\n".join(lines))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(ROOT.parent / SOURCE_ID),
                        help="checkout of the source list repo")
    args = parser.parse_args(argv)
    source = Path(args.source)
    readme = source / "README.md"
    if not readme.exists():
        sys.exit(f"source README not found: {readme}")
    try:
        commit = subprocess.run(
            ["git", "-C", str(source), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        date = subprocess.run(
            ["git", "-C", str(source), "log", "-1", "--format=%cs", commit],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, OSError) as exc:
        sys.exit(f"ingest: source is not a usable git checkout: {source} ({exc})")

    entries = parse_list(readme)
    WIKI.mkdir(exist_ok=True)

    existing: dict[str, Path] = {}
    by_stem: dict[str, Path] = {}
    for page in sorted(WIKI.rglob("*.md")):
        fields, _ = split_page(read_page(page))
        if "url" in fields:
            key = normalise(str(fields["url"]))
            if key in existing:
                sys.exit(f"ingest: duplicate URL {key}: {existing[key]} and {page}")
            existing[key] = page
            by_stem[page.stem] = page

    taken = {p.stem for p in WIKI.rglob("*.md")}
    entry_urls = {normalise(e["url"]) for e in entries}
    matched: set[Path] = set()
    by_section: dict[str, list[dict]] = {}
    created = updated = 0
    for e in entries:
        key = normalise(e["url"])
        page = existing.get(key)
        if page is None:
            # URL moved? An entry under a new URL keeps its page when the
            # name's slug matches a page whose URL is no longer listed.
            base = slugify(e["title"], set())
            candidates = sorted(
                (p for stem, p in by_stem.items()
                 if stem == base or re.fullmatch(re.escape(base) + r"-\d+", stem)),
                key=lambda p: p.as_posix(),
            )
            for candidate in candidates:
                if candidate in matched:
                    continue
                cfields, _ = split_page(read_page(candidate))
                if normalise(str(cfields.get("url", ""))) not in entry_urls:
                    page = candidate
                    break
        if page is None:
            slug = slugify(e["title"], taken)
            page = WIKI / f"{slug}.md"
            # Finished works (the Research Papers category) are complete
            # at listing time: their status is `published` (OpenShelf
            # SPEC §9.2), not the unverified default for living resources.
            new_status = ("published" if e["section"] == "Research Papers"
                          else "unknown")
            write_page(page, frontmatter(e, new_status, "stub", date, commit)
                       + stub_body(e))
            created += 1
        else:
            old_text = read_page(page)
            fields, body = split_page(old_text)
            changed = (
                str(fields.get("title", "")) != e["title"]
                or normalise(str(fields.get("url", ""))) != key
                or str(fields.get("category", "")) != e["section"]
                or str(fields.get("list_summary", "")) != e["summary"])
            if changed:
                missing = [key for key in ("uid", "created", "last_checked")
                           if not str(fields.get(key, "")).strip()]
                if missing:
                    sys.exit(
                        f"ingest: {page} is missing {', '.join(missing)}; "
                        "refusing to invent it"
                    )
                depth = str(fields.get("depth", "stub"))
                status = str(fields.get("status", "unknown"))
                new_text = frontmatter(
                    e, status, depth, date, commit, extra_blocks(old_text),
                    last_checked=str(fields["last_checked"]),
                    created=str(fields["created"]),
                    updated=date,
                    uid=str(fields["uid"])) + (
                    body if depth != "stub" else stub_body(e))
                write_page(page, new_text)
                updated += 1
        matched.add(page)
        by_section.setdefault(e["section"], []).append(
            {"slug": page.stem, "title": e["title"],
             "summary": short_summary(e["summary"])})

    tombstoned = 0
    for page in sorted(set(existing.values()) - matched):
        if page.stem.startswith("index-"):
            continue
        text = read_page(page)
        fields, _ = split_page(text)
        if fields.get("status") != "archived":
            end = text.find("\n---\n", 4)
            head, tail = (text[:end], text[end:]) if end != -1 else ("", text)
            head = re.sub(r"^status: .*$", "status: archived", head,
                          count=1, flags=re.M)
            if "Delisted from the source list" not in tail:
                tail += (f"\n> Delisted from the source list as of {commit}."
                         f" Tombstoned, not deleted (see AGENTS.md).\n")
            text = head + tail
            write_page(page, text)
            tombstoned += 1
        # Tombstoned pages stay listed in their sub-index (marked), so
        # every page in wiki/ remains reachable from the index.
        category = str(fields.get("category", ""))
        if category:
            by_section.setdefault(category, []).append(
                {"slug": page.stem,
                 "title": f"{fields.get('title', page.stem)} (delisted)",
                 "summary": short_summary(
                     str(fields.get("list_summary", "")))})

    pages = all_pages()
    facet_counts = write_facet_indexes(pages, list(by_section.keys()))
    attention_count = write_needs_attention(pages, date)
    write_glossary(pages)
    write_concept_map(pages)

    # Facet counts per list section, for the sub-index browse lines.
    facets_by_section: dict[str, dict[str, int]] = {}
    for page, fields, _ in pages:
        section = str(fields.get("category", ""))
        if not section:
            continue
        for slug in parse_slugs(fields.get("facets", "")):
            if slug in facet_counts:
                counts = facets_by_section.setdefault(section, {})
                counts[slug] = counts.get(slug, 0) + 1

    # Sub-indexes (no frontmatter — OpenShelf detects them as sub-indexes).
    by_section_order = list(by_section.keys())
    catslug = {}
    cat_taken: set[str] = set()
    for section in by_section_order:
        cs = slugify(section, cat_taken)
        catslug[section] = cs
        lines = [f"# {section}", ""]
        browse = ", ".join(
            f"[{FACET_BY_SLUG[s].label}](index-facet-{s}.md) ({n} here)"
            for s, n in sorted(facets_by_section.get(section, {}).items(),
                               key=lambda kv: (-kv[1], kv[0]))[:6])
        if browse:
            lines += [f"Browse by facet: {browse}.", ""]
        for item in by_section[section]:
            lines.append(f"- [{item['title']}]({item['slug']}.md) — {item['summary']}")
        lines.append("")
        write_page(WIKI / f"index-{cs}.md", "\n".join(lines))

    # Drop category indexes for sections no longer in the list. Generated
    # sub-indexes have no frontmatter; an authored `index-*` page does.
    generated_categories = {f"index-{cs}.md" for cs in catslug.values()}
    hub_indexes = {"index-concept-map.md", "index-glossary.md",
                   "index-needs-attention.md"}
    for path in WIKI.glob("index-*.md"):
        if (path.name in hub_indexes or path.name.startswith("index-facet-")
                or path.name in generated_categories):
            continue
        if not read_page(path).startswith("---\n"):
            path.unlink()

    # L1 index.
    lines = [f"# {KB_TITLE}", "", KB_DESC,
             "Generated from page frontmatter by tools/ingest.py;"
             " do not edit by hand.", "",
             "## Start here", "",
             "- [Concept map](wiki/index-concept-map.md) — the concept layer"
             " by theme, with reading paths through it.",
             "- [Glossary](wiki/index-glossary.md) — acronyms and standards,"
             " linked to the page that explains each one.",
             f"- [Needs attention](wiki/index-needs-attention.md) —"
             f" {attention_count} maintenance-queue entries.", "",
             "## Categories", ""]
    for section in by_section_order:
        n = len(by_section[section])
        lines.append(f"- [{section}](wiki/index-{catslug[section]}.md)"
                     f" — {n} entr{'y' if n == 1 else 'ies'}")

    # Concept pages (hand-written synthesis) are listed directly in the L1.
    concepts_dir = WIKI / "concepts"
    concepts = []
    if concepts_dir.is_dir():
        for page in sorted(concepts_dir.glob("*.md")):
            fields, _ = split_page(read_page(page))
            if "title" in fields and "summary" in fields:
                concepts.append((str(fields["title"]), page.stem,
                                 str(fields["summary"])))
    if concepts:
        lines += ["", "## Concepts", ""]
        for title, slug, summary in concepts:
            lines.append(f"- [{title}](wiki/concepts/{slug}.md) — {summary}")

    if facet_counts:
        lines += ["", "## Facets", "",
                  "Cross-cutting topics — browse a theme across every list"
                  " section.", ""]
        for slug in sorted(facet_counts, key=lambda s: (-facet_counts[s], s)):
            facet = FACET_BY_SLUG[slug]
            lines.append(f"- [{facet.label}](wiki/index-facet-{slug}.md) —"
                         f" {facet_counts[slug]} pages (entities and concepts)."
                         f" {facet.description}")
    lines.append("")
    write_page(ROOT / "index.md", "\n".join(lines))

    print(f"ingest: {len(entries)} entries from {SOURCE_ID}@{commit} "
          f"— {created} created, {updated} updated, {tombstoned} tombstoned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
