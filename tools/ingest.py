#!/usr/bin/env python3
"""Ingest an awesome list into this knowledge base (SPEC.md §6).

Parses the source README with the same entry grammar the list's own
validator enforces — `* [name](url) - desc` under `##` sections — and:

- creates a stub page for every entry with no page,
- refreshes provenance frontmatter (section / summary / source commit) on
  existing pages without touching a `full` page's added depth,
- tombstones pages whose URL has left the list (`status: delisted`),
- regenerates `index.json` and `llms.txt`.

Deterministic and idempotent: same source commit in, byte-identical tree
out. No wall-clock timestamps are written anywhere.

Usage: python3 tools/ingest.py [--source ../awesome-automotive-security]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRY_RE = re.compile(r"^\* \[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\) - (?P<desc>.+)$")
HEADING_RE = re.compile(r"^## (?P<title>.+)$")
SKIP_SECTIONS = {"Contents"}
SOURCE_ID = "awesome-automotive-security"
KB_URL = "https://github.com/hexsecs/awesome-kb-automotive-security"


def normalise(url: str) -> str:
    """The list validator's identity rule (SPEC.md §3)."""
    u = url.rstrip("/").lower()
    return u[len("https://"):] if u.startswith("https://") else u


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


def parse_list(readme: Path) -> list[dict]:
    entries, section = [], None
    for line in readme.read_text(encoding="utf-8").splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            section = heading.group("title").strip()
            continue
        match = ENTRY_RE.match(line)
        if match and section and section not in SKIP_SECTIONS:
            entries.append({
                "title": match.group("name"),
                "url": match.group("url"),
                "section": section,
                "summary": match.group("desc"),
            })
    return entries


def frontmatter(fields: dict) -> str:
    lines = ["---"]
    for key in ("title", "url", "source", "source_section", "source_commit",
                "status", "summary"):
        lines.append(f"{key}: {q(str(fields[key]))}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def stub_body(e: dict) -> str:
    return (
        f"\n# {e['title']}\n\n{e['summary']}\n\n"
        f"- **Resource:** {e['url']}\n"
        f"- **List section:** {e['section']}\n"
        f"- **Source:** [{SOURCE_ID}](https://github.com/hexsecs/awesome-automotive-security)"
        f" — the list is canon; this page is a generated stub. Depth is added"
        f" by PR (see the KB README's landing rules).\n"
    )


def split_page(text: str) -> tuple[dict, str]:
    """Split an existing page into frontmatter fields and body."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fields = {}
    for line in text[4:end].splitlines():
        if ": " in line:
            key, raw = line.split(": ", 1)
            try:
                fields[key.strip()] = json.loads(raw)
            except json.JSONDecodeError:
                fields[key.strip()] = raw.strip('"')
    return fields, text[end + 5:]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(ROOT.parent / SOURCE_ID),
                        help="checkout of the source list repo")
    args = parser.parse_args()
    source = Path(args.source)
    readme = source / "README.md"
    if not readme.exists():
        sys.exit(f"source README not found: {readme}")
    source_commit = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()

    entries = parse_list(readme)
    entries_dir = ROOT / "entries"
    entries_dir.mkdir(exist_ok=True)

    # Index existing pages by normalised URL.
    existing: dict[str, Path] = {}
    for page in sorted(entries_dir.glob("*.md")):
        fields, _ = split_page(page.read_text(encoding="utf-8"))
        if "url" in fields:
            existing[normalise(fields["url"])] = page

    taken = {p.stem for p in entries_dir.glob("*.md")}
    seen: set[str] = set()
    index_entries = []
    created = updated = 0
    for e in entries:
        key = normalise(e["url"])
        seen.add(key)
        page = existing.get(key)
        fields = {
            "title": e["title"], "url": e["url"], "source": SOURCE_ID,
            "source_section": e["section"], "source_commit": source_commit,
            "summary": e["summary"],
        }
        if page is None:
            slug = slugify(e["title"], taken)
            page = entries_dir / f"{slug}.md"
            page.write_text(frontmatter({**fields, "status": "stub"})
                            + stub_body(e), encoding="utf-8")
            created += 1
            status = "stub"
        else:
            slug = page.stem
            old_fields, body = split_page(page.read_text(encoding="utf-8"))
            status = old_fields.get("status", "stub")
            if status == "delisted":
                status = "stub"  # re-listed: revive as a stub
            new_text = frontmatter({**fields, "status": status}) + (
                body if status == "full" else stub_body(e))
            if page.read_text(encoding="utf-8") != new_text:
                page.write_text(new_text, encoding="utf-8")
                updated += 1
        index_entries.append({
            "slug": slug, "title": e["title"], "url": e["url"],
            "section": e["section"], "status": status,
            "file": f"entries/{slug}.md",
        })

    tombstoned = 0
    for key, page in existing.items():
        if key not in seen:
            fields, body = split_page(page.read_text(encoding="utf-8"))
            if fields.get("status") != "delisted":
                fields["status"] = "delisted"
                fields["source_commit"] = source_commit
                page.write_text(frontmatter(fields) + body, encoding="utf-8")
                tombstoned += 1

    index = {"source": SOURCE_ID, "source_commit": source_commit,
             "count": len(index_entries), "entries": index_entries}
    (ROOT / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    sections: list[str] = []
    for e in index_entries:
        if e["section"] not in sections:
            sections.append(e["section"])
    llms = [f"# Awesome KB — Automotive Security",
            "",
            "> A knowledge base ingesting the curated awesome list"
            " hexsecs/awesome-automotive-security (the list is canon; this KB"
            " is the derived layer). One page per resource, concept pages for"
            " synthesis, and a JSON index for machines.",
            "",
            "## Machine layer",
            "",
            f"- [Index (JSON)]({KB_URL}/blob/main/index.json): every entry —"
            " slug, title, URL, source section, status, page path.",
            f"- [Spec]({KB_URL}/blob/main/SPEC.md): the format this KB follows.",
            "",
            "## Sections (from the source list)",
            ""]
    llms += [f"- {s}" for s in sections]
    llms += ["", "## Entry pages", "",
             "Entry pages live in `entries/<slug>.md`; resolve a slug through"
             " index.json. Pages with status `full` carry verified depth;"
             " `stub` pages carry the list's own description and provenance.",
             ""]
    (ROOT / "llms.txt").write_text("\n".join(llms), encoding="utf-8")

    print(f"ingest: {len(entries)} entries from {SOURCE_ID}@{source_commit} "
          f"— {created} created, {updated} updated, {tombstoned} tombstoned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
