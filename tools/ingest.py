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
# Lazy capture up to the `) - ` delimiter: handles URLs with any depth of
# nested parentheses (e.g. Wikipedia titles) without a recursive regex.
ENTRY_RE = re.compile(
    r"^\* \[(?P<name>[^\]]+)\]\((?P<url>.*?)\) - (?P<desc>.+)$"
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


# Leaves room for a ``-N`` collision suffix and ``.md`` under NAME_MAX (255).
MAX_SLUG = 200


def raw_slug(name: str) -> str:
    """Uncapped slug: older pages may still carry a NAME_MAX-avoiding stem."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "entry"


def slugify(name: str, taken: set[str], folder: Path | None = None) -> str:
    # ``taken`` must be case-folded: on a case-insensitive filesystem (APFS)
    # ``Alpha.md`` and ``alpha.md`` are the same inode, so a case-sensitive
    # reservation silently destroys an authored page. The filesystem check
    # catches collisions the caller did not put in ``taken`` at all.
    slug = raw_slug(name)
    if len(slug) > MAX_SLUG:
        slug = slug[:MAX_SLUG].rstrip("-") or "entry"
    base, n = slug, 2
    while (slug in taken
           or (folder is not None and (folder / f"{slug}.md").exists())):
        slug = f"{base}-{n}"
        n += 1
    taken.add(slug)
    return slug


def category_slugs(sections: list[str],
                   authored: set[str] | None = None) -> dict[str, str]:
    """Map each list section to its generated category-index slug.

    This is the single source of truth for category slugs: both the stem
    reservation for authored pages and the index writer call it, so an entity
    can never be created at a stem the generator will later overwrite.

    ``authored`` carries the unprefixed stems of pages that already occupy an
    ``index-*.md`` path from an earlier ingest. Reserving only this run's new
    pages let a section added later clobber a page created before it existed.
    """
    taken: set[str] = {"concept-map", "glossary", "needs-attention"}
    taken |= {f"facet-{f.slug}" for f in FACETS}
    taken |= set(authored or ())
    return {section: slugify(section, taken) for section in sections}


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


def strip_bom(text: str) -> str:
    """Drop a leading UTF-8 BOM so frontmatter is never hidden by three bytes."""
    return text[1:] if text.startswith("\ufeff") else text


def scalar(raw: str) -> str:
    """Parse one YAML scalar, dropping a trailing comment outside quotes.

    ``json.loads`` handles double-quoted values with escapes; a matching
    single/double outer pair is stripped by hand (YAML allows both). Crucially
    only ONE matching pair is removed, so a value that legitimately ends in a
    quote is not mangled, and a ``#`` after the value never becomes part of it.
    """
    raw = raw.strip()
    quote = None
    for i, ch in enumerate(raw):
        if quote:
            if ch == quote and (i == 0 or raw[i - 1] != "\\"):
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or raw[i - 1].isspace()):
            raw = raw[:i].rstrip()
            break
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
            return raw[1:-1]
        return raw


def frontmatter_bounds(text: str) -> tuple[int, int] | None:
    """Return (fm_end, body_start) for the frontmatter fences.

    The closing fence may sit at EOF with no trailing newline; such a page is
    still valid and must not become invisible to the maintenance tools.
    """
    end = text.find("\n---\n", 4)
    if end != -1:
        return end, end + 5
    if text.endswith("\n---"):
        return len(text) - 4, len(text)
    return None


def frontmatter_blocks(text: str) -> list[tuple[str, list[str]]]:
    """Split a page's frontmatter into (key, raw lines) top-level blocks."""
    text = strip_bom(text)
    if not text.startswith("---\n"):
        return []
    bounds = frontmatter_bounds(text)
    if bounds is None:
        return []
    end = bounds[0]
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
    text = strip_bom(text)
    if not text.startswith("---\n"):
        return {}, text
    bounds = frontmatter_bounds(text)
    if bounds is None:
        return {}, text
    end, body_start = bounds
    fields = {}
    lines = text[4:end].splitlines()
    for line in lines:
        if ": " in line and not line.startswith((" ", "\t")):
            key, raw = line.split(": ", 1)
            fields[key.strip()] = scalar(raw)
    # A bare `facets:` followed by a list is valid YAML (indented or not)
    # and is preserved verbatim by extra_blocks(), but the scalar loop above
    # cannot see it. Normalise it to the inline shape parse_slugs() reads.
    # YAML's last key wins, so a block must not override a later inline one.
    last_inline = max((i for i, line in enumerate(lines)
                       if re.match(r"^facets:\s*\S", line)), default=-1)
    for i, line in enumerate(lines):
        if line != "facets:" or i < last_inline:
            continue
        items = []
        for cont in lines[i + 1:]:
            if not cont.strip() or cont.lstrip().startswith("#"):
                continue  # comments and blank lines do not end a YAML list
            match = re.match(r"^\s*-\s+(.*)$", cont)
            if not match:
                break
            items.append(str(scalar(match.group(1))))
        if items:
            fields["facets"] = " ".join(items)
    return fields, text[body_start:]


def parse_slugs(value: object) -> set[str]:
    """Read a YAML inline list (or a flat scalar) of slugs from split_page."""
    return set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(value)))


def related_count(text: str) -> int:
    """Count `related` targets in either frontmatter list shape."""
    return len(parse_related(split_frontmatter(text)[0]))


def read_page(path: Path) -> str:
    """Read a page with a clear error instead of a half-written ingest.

    BOM is stripped here too (not only in the frontmatter splitters): the
    source README is read through this function, and a BOM there would hide
    the first section's heading and silently delist its entries.
    """
    try:
        return strip_bom(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as exc:
        sys.exit(f"ingest: cannot read {path}: {exc}")


def within_root(path: Path) -> bool:
    """True when ``path`` resolves to a location inside the KB root.

    A leaf-only ``is_symlink()`` check misses a symlinked parent (e.g. a
    ``wiki/`` that points outside the repo). Resolving the full path and
    checking containment covers every component at once.
    """
    try:
        return path.resolve().is_relative_to(ROOT.resolve())
    except OSError:
        return False


def checked(path: Path, action: str) -> None:
    """Refuse to touch a path that escapes the KB, is a symlink or a hardlink.

    A hardlink is neither a symlink nor resolvable outside the root, so the
    resolve-based containment check alone lets ``write_text`` truncate the
    other name of the inode — possibly outside the KB. Refuse extras links.
    """
    if path.is_symlink() or not within_root(path):
        sys.exit(f"ingest: refusing to {action} through symlink {path}")
    # Directories always have st_nlink >= 2 on POSIX, so without this branch
    # a directory at a generated-output path is misreported as a hardlink.
    if path.is_dir():
        sys.exit(f"ingest: refusing to {action} a directory at {path}")
    # A FIFO (or socket/device node) at a generated output path would block
    # on open-for-write forever. Every other tool skips non-regular files;
    # ingest must refuse rather than hang the pipeline.
    if path.exists() and not path.is_file():
        sys.exit(f"ingest: refusing to {action} a non-regular file at {path}")
    if path.exists() and path.stat().st_nlink > 1:
        sys.exit(f"ingest: refusing to {action} hardlinked file {path}")


def safe_pages(paths):
    """Yield real, in-root, non-symlink markdown files from an iterable.

    ``glob("*.md")`` matches directories too, and a symlinked leaf would be
    read from outside the root and merged into a generated index. Both must
    be skipped on the READ side, not just on writes.
    """
    for path in paths:
        if not path.is_file() or path.is_symlink() or not within_root(path):
            continue
        yield path


def link_target(page: Path) -> str:
    """Markdown link target for a page, relative to ``wiki/``.

    Generated indexes live at the wiki root; a page nested in a subdirectory
    (e.g. ``wiki/topics/foo.md``) needs ``topics/foo`` rather than its bare
    stem, or every generated link to it is dead.
    """
    return page.relative_to(WIKI).with_suffix("").as_posix()


def write_page(path: Path, text: str) -> None:
    """Write a page, refusing to follow a symlink out of the KB."""
    checked(path, "write")
    path.write_text(text, encoding="utf-8")


def all_pages() -> list[tuple[Path, dict, str]]:
    """Every authored page (entities and concepts), in stable path order.

    Generated indexes have no frontmatter, so the ``"title" in fields`` check
    excludes them without needing a filename-prefix filter — which used to
    hide legitimately named entities such as ``index-of-tools``.
    """
    pages = []
    for page in sorted(safe_pages(WIKI.rglob("*.md"))):
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
            by_group.setdefault(group, []).append(
                f"- [{fields['title']}]({link_target(page)}.md)"
                f" — {fields.get('summary', '')}")
        for group in sorted(by_group, key=lambda g: (order.get(g, 999), g)):
            lines += [f"## {group}", ""] + sorted(by_group[group]) + [""]
        write_index(WIKI / f"index-facet-{facet.slug}.md", "\n".join(lines))

    # Remove stale facet indexes when a facet drops below the threshold.
    # An authored page whose slug starts with ``index-facet-`` (e.g. the
    # collision-safe ``index-facet-can-2``) has frontmatter and is NOT a
    # generated index — deleting it would destroy that page silently.
    for path in safe_pages(WIKI.glob("index-facet-*.md")):
        if path.stem.removeprefix("index-facet-") not in counts:
            if read_page(path).startswith("---\n"):
                continue
            checked(path, "unlink")
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
        entry = f"- [{fields['title']}]({link_target(page)}.md)"
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
    write_index(WIKI / "index-needs-attention.md", "\n".join(lines))
    actionable = sum(len(v) for k, v in buckets.items()
                     if k != "Brief by design (no action)")
    return actionable


def write_glossary(pages: list[tuple[Path, dict, str]]) -> None:
    titles = {link_target(p): f for p, f, _ in pages}
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
    write_index(WIKI / "index-glossary.md", "\n".join(lines))


def write_index(path: Path, text: str) -> None:
    """Write a generated index, never over a page a human authored there."""
    # Check BEFORE read_page(): a FIFO here would block on read, not write.
    checked(path, "write generated index")
    if path.exists() and read_page(path).startswith("---\n"):
        sys.exit(f"ingest: refusing to overwrite authored page at {path}")
    write_page(path, text)


def write_concept_map(pages: list[tuple[Path, dict, str]]) -> None:
    # Keep the page alongside its fields: a concept need not be flat in
    # wiki/concepts/, and every other generated index uses link_target().
    # Two concepts may share a stem (e.g. a draft under wiki/topics/). The
    # L1 index lists only wiki/concepts/, so prefer that canonical page here
    # too; otherwise this hub points at the clone while L1 points at the
    # real concept, and link_check sees nothing wrong.
    concepts: dict[str, tuple[Path, dict]] = {}
    canonical = WIKI / "concepts"
    for p, f, _ in sorted(
            ((p, f, _) for p, f, _ in pages if f.get("type") == "concept"),
            key=lambda item: (not item[0].is_relative_to(canonical),
                              item[0].parent != canonical)):
        concepts.setdefault(p.stem, (p, f))
    lines = ["# Concept map", "",
             "The concept layer organised by theme, with reading paths through"
             " it. Generated from tools/taxonomy.py and concept frontmatter;"
             " do not edit by hand.", ""]

    placed: set[str] = set()
    for cluster in CONCEPT_CLUSTERS:
        lines += [f"## {cluster.label}", "", cluster.description, ""]
        for slug in dict.fromkeys(cluster.concepts):
            entry = concepts.get(slug)
            if entry is None:
                continue
            page, fields = entry
            placed.add(slug)
            lines.append(f"- [{fields['title']}]({link_target(page)}.md)"
                         f" — {fields.get('summary', '')}")
        lines.append("")

    orphans = [s for s in sorted(concepts) if s not in placed]
    if orphans:
        lines += ["## Unclustered concepts", "",
                  "Concepts added since the taxonomy was last updated:", ""]
        for slug in orphans:
            page, fields = concepts[slug]
            lines.append(f"- [{fields['title']}]({link_target(page)}.md)"
                         f" — {fields.get('summary', '')}")
        lines.append("")

    lines += ["## Reading paths", ""]
    for path in READING_PATHS:
        lines += [f"### {path.title}", "", path.description, ""]
        for i, slug in enumerate(path.steps, 1):
            entry = concepts.get(slug)
            if entry is not None:
                page, fields = entry
                lines.append(f"{i}. [{fields['title']}]({link_target(page)}.md)")
        lines.append("")
    write_index(WIKI / "index-concept-map.md", "\n".join(lines))


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
    seen_urls: set[str] = set()
    for e in entries:
        key = normalise(e["url"])
        if key in seen_urls:
            sys.exit(f"ingest: duplicate URL in source list: {key} "
                     f"({e['title']})")
        seen_urls.add(key)
    WIKI.mkdir(exist_ok=True)

    # A symlinked page is invisible to safe_pages(), but slugify() still sees
    # its filename and would pick a `-2` slug. The next ingest then finds two
    # pages with one URL and fails permanently. Refuse when the symlink is
    # exactly where an entry's page belongs; other symlinks are untouched.
    entry_slugs = set()
    for e in entries:
        entry_slugs.add(raw_slug(e["title"]))
        entry_slugs.add(slugify(e["title"], set()))
    for path in sorted(WIKI.rglob("*.md")):
        # slugify() only probes WIKI/<slug>.md, so a symlink nested below
        # the wiki root cannot influence slug choice. Refusing one aborted
        # an otherwise valid ingest for no protective reason.
        if (path.is_symlink() and path.parent == WIKI
                and path.stem.lower() in entry_slugs):
            sys.exit(f"ingest: symlinked page blocks an entry: {path}; "
                     "replace it with the real page")

    existing: dict[str, Path] = {}
    by_stem: dict[str, list[Path]] = {}  # case-folded: slugs are lowercase
    page_category: dict[Path, str] = {}
    for page in sorted(safe_pages(WIKI.rglob("*.md"))):
        fields, _ = split_page(read_page(page))
        # Concept pages are hand-written synthesis, not canon list entries.
        # A `url:` on one is a cross-reference, not identity: treating it as
        # identity tombstoned it on delist and made its URL collide with real
        # entries. Only entity pages carry list identity.
        if "url" in fields and str(fields.get("type")) != "concept":
            key = normalise(str(fields["url"]))
            if key in existing:
                sys.exit(f"ingest: duplicate URL {key}: {existing[key]} and {page}")
            existing[key] = page
            by_stem.setdefault(page.stem.lower(), []).append(page)
            if fields.get("category"):
                page_category[page] = str(fields["category"])

    entry_urls = {normalise(e["url"]) for e in entries}
    # Generated indexes own these stems; an authored page must never take one
    # (on a first ingest into an empty wiki they do not exist on disk yet).
    reserved = {"index-concept-map", "index-glossary", "index-needs-attention"}
    reserved |= {f"index-facet-{f.slug}" for f in FACETS}
    # The sections that will actually generate an index are the listed ones
    # plus those of tombstoned pages (which stay in their sub-index). Compute
    # the mapping ONCE and reuse it below — two independent slugify seeds were
    # the cause of entities being silently overwritten by their category index.
    # Sections of pages that merely moved are NOT included, so their now-stale
    # indexes are still cleaned up after the updates.
    doomed = [p for key, p in existing.items() if key not in entry_urls]
    section_order = list(dict.fromkeys(
        [e["section"] for e in entries]
        + [page_category[p] for p in doomed if p in page_category]
    ))
    # Lowercase like ``slugify`` does: on APFS ``index-Tools.md`` and
    # ``index-tools.md`` are one inode, so an uppercase authored stem must
    # still reserve the generated index's slug.
    # Reserve from ALL authored pages, not just URL-bearing entities: a
    # url-less hand-written `index-tools.md` must still route the generated
    # Tools index to `index-tools-2.md`. Generated indexes have no frontmatter
    # and are excluded, so they cannot poison the reservation on later runs.
    authored_index_slugs = {
        p.stem[len("index-"):].lower()
        for p in safe_pages(WIKI.rglob("*.md"))
        if p.stem.lower().startswith("index-")
        and p.parent == WIKI
        and read_page(p).startswith("---\n")
    }
    catslug = category_slugs(section_order, authored_index_slugs)
    reserved |= {f"index-{cs}" for cs in catslug.values()}
    taken = {p.stem.lower() for p in safe_pages(WIKI.rglob("*.md"))} | reserved
    matched: set[Path] = set()
    by_section: dict[str, list[dict]] = {}
    created = updated = 0
    for e in entries:
        key = normalise(e["url"])
        page = existing.get(key)
        if page is None:
            # URL moved? An entry under a new URL keeps its page when the
            # name's slug matches a page whose URL is no longer listed.
            # Match both today's capped slug and the uncapped one a page may
            # have been created with before the cap existed; otherwise a URL
            # move on a long title creates a duplicate and tombstones the
            # original instead of updating it.
            bases = {raw_slug(e["title"]), slugify(e["title"], set())}
            candidates = sorted(
                (p for stem, grouped in by_stem.items()
                 if any(stem == base or re.fullmatch(re.escape(base) + r"-\d+",
                                                     stem) for base in bases)
                 for p in grouped),
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
            # A file occupying the entry's natural slug — or a `-N` variant
            # from a URL move (row 17) — with no parseable frontmatter (e.g.
            # a lost closing fence) cannot carry list identity, so neither
            # the URL lookup nor the move fallback above can find it. Without
            # this check we mint a duplicate and strand the original as
            # permanently unreachable — silently, since link_check only
            # finds it after the damage. Generated indexes have no
            # frontmatter either: exempt exactly the stems this run reserves
            # for them (plus suffixed variants whose base is reserved), not
            # every `index-*` name — authored entities own those stems too.
            # Match both today's capped slug and the uncapped raw slug: a
            # page written before the cap (or moved to a new URL) can occupy
            # the long stem, and a malformed page there must be refused too.
            # The URL-move fallback above already checks both bases.
            bases = {raw_slug(e["title"]), slugify(e["title"], set())}
            occupants: set[Path] = set()
            for base in bases:
                occupants.add(WIKI / f"{base}.md")
                occupants.update(
                    p for p in WIKI.glob(f"{base}-[0-9]*.md")
                    if re.fullmatch(re.escape(base) + r"-\d+", p.stem)
                )
            for occupant in sorted(occupants):
                if (not occupant.is_file() or occupant.is_symlink()
                        or not within_root(occupant)):
                    continue
                stem = occupant.stem.lower()
                # Generated indexes (including a stale one from a section
                # that moved away) have no frontmatter and are never given a
                # `-N` suffix. An authored `index-*` page keeps its opening
                # fence even with a lost closing fence, so still refuse it.
                if stem in reserved or (
                        stem.startswith("index-")
                        and not read_page(occupant).startswith("---\n")):
                    continue
                occ_fields, _ = split_page(read_page(occupant))
                if "title" not in occ_fields:
                    sys.exit(
                        f"ingest: {occupant} has no parseable frontmatter; "
                        "refusing to create a duplicate entry page"
                    )
            slug = slugify(e["title"], taken, WIKI)
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
            # A re-listed entry is a change even when its list text is byte-
            # identical to the tombstoned version: it must come back to life.
            # The delisting NOTE is the signal, not `status: archived` alone —
            # a verification pass also archives pages whose upstream project
            # is dead while the entry is still on the canon list.
            was_tombstoned = "Delisted from the source list" in body
            changed = (
                str(fields.get("title", "")) != e["title"]
                or normalise(str(fields.get("url", ""))) != key
                or str(fields.get("category", "")) != e["section"]
                or str(fields.get("list_summary", "")) != e["summary"]
                or was_tombstoned)
            if changed:
                missing = [key for key in ("uid", "created", "last_checked")
                           if not str(fields.get(key, "")).strip()]
                if missing:
                    sys.exit(
                        f"ingest: {page} is missing {', '.join(missing)}; "
                        "refusing to invent it"
                    )
                depth = str(fields.get("depth", "stub"))
                if was_tombstoned:
                    # Back on the canon list: undo the tombstone rather than
                    # carrying its delisted note forward.
                    body = re.sub(
                        r"^> Delisted from the source list.*\n?", "", body,
                        flags=re.M)
                # A finished work in Research Papers is `published` even when
                # it moved there from another section (the create branch uses
                # the same rule). A re-listed resource returns to the default
                # unverified status; any other section keeps its status —
                # including a deliberately archived upstream project.
                # `status: archived` alone is not enough to stop a relist —
                # the delisting NOTE is that signal. But a page archived by a
                # verification pass (still on the canon list) carries real
                # evidence in status_note; moving it into Research Papers must
                # not overwrite that with `published`.
                verified_archived = (
                    str(fields.get("status")) == "archived"
                    and not was_tombstoned)
                entering_rp = (e["section"] == "Research Papers"
                               and str(fields.get("category", ""))
                               != e["section"]
                               and not verified_archived)
                status = ("published" if entering_rp
                          else "unknown" if was_tombstoned
                          else str(fields.get("status", "unknown")))
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
            {"slug": link_target(page), "title": e["title"],
             "summary": short_summary(e["summary"])})

    tombstoned = 0
    for page in sorted(set(existing.values()) - matched):
        # Generated indexes have no frontmatter and never enter ``existing``,
        # so this loop only sees authored pages — including ones legitimately
        # named ``index-*``. Skipping them by name lost their tombstone.
        text = read_page(page)
        fields, _ = split_page(text)
        bounds = frontmatter_bounds(text)
        head, tail = (text[:bounds[0]], text[bounds[0]:]) if bounds else ("", text)
        changed = False
        if fields.get("status") != "archived":
            new_head = re.sub(r"^status: .*$", "status: archived", head,
                              count=1, flags=re.M)
            if new_head == head and not re.search(r"^status:", head, re.M):
                # A hand-authored page may have no status key at all: write
                # one, or the next identical ingest "tombstones" it again.
                new_head = head.rstrip("\n") + "\nstatus: archived\n"
            if new_head != head:
                head = new_head
                changed = True
        # The note is the un-tombstone signal on re-list, independent of why
        # the page was archived. A project archived by a verification pass that
        # later leaves the list still needs to record the delisting.
        if "Delisted from the source list" not in tail:
            tail += (f"\n> Delisted from the source list as of {commit}."
                     f" Tombstoned, not deleted (see AGENTS.md).\n")
            changed = True
        if changed:
            write_page(page, head + tail)
            # Only count a real change: a page with no `status:` key is
            # already archived in effect, and counting it every run made
            # identical ingests claim another tombstone forever.
            tombstoned += 1
        # Tombstoned pages stay listed in their sub-index (marked), so
        # every page in wiki/ remains reachable from the index.
        category = str(fields.get("category", ""))
        if category:
            by_section.setdefault(category, []).append(
                {"slug": link_target(page),
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
    # ``catslug`` was computed once, before stem reservation, so the stem
    # written here is exactly the one every authored page was kept away from.
    by_section_order = list(by_section.keys())
    written_categories: set[str] = set()
    for section in by_section_order:
        cs = catslug[section]
        written_categories.add(f"index-{cs}.md")
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
        write_index(WIKI / f"index-{cs}.md", "\n".join(lines))

    # Drop category indexes not actually written this run. Trusting
    # ``catslug.values()`` instead left a stale index behind whenever a page
    # was matched by its title slug after a combined URL + section move — and
    # deleted it on the *next* identical ingest, breaking idempotency. Tracking
    # the files we really wrote makes the sweep correct by construction.
    # Generated sub-indexes have no frontmatter; an authored `index-*` page does.
    hub_indexes = {"index-concept-map.md", "index-glossary.md",
                   "index-needs-attention.md"}
    for path in safe_pages(WIKI.glob("index-*.md")):
        if (path.name in hub_indexes or path.name.startswith("index-facet-")
                or path.name in written_categories):
            continue
        if not read_page(path).startswith("---\n"):
            checked(path, "unlink")
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
    # Classification is by `type:` — the same rule the concept map, miner,
    # scanner and auditor use. A directory scan disagreed with all of them:
    # it listed entities filed under concepts/ and skipped root-level concepts.
    canonical = WIKI / "concepts"
    concepts: dict[str, tuple[str, str, str]] = {}
    for page, fields, _ in sorted(
            ((p, f, b) for p, f, b in pages
             if str(f.get("type", "")) == "concept"),
            key=lambda item: (not item[0].is_relative_to(canonical),
                              item[0].parent != canonical)):
        # Canonical-per-stem dedupe, identical to write_concept_map: a clone
        # nested deeper under concepts/ gets no second L1 row. The map also
        # dedupes summary-less concepts, so L1 must not drop them here and let
        # a nested clone win the stem by default.
        concepts.setdefault(page.stem,
                            (str(fields["title"]), link_target(page),
                             str(fields.get("summary", ""))))
    if concepts:
        lines += ["", "## Concepts", ""]
        for title, target, summary in concepts.values():
            lines.append(f"- [{title}](wiki/{target}.md) — {summary}")

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
