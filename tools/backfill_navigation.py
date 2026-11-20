#!/usr/bin/env python3
"""Backfill navigation metadata on pages (idempotent, one-off maintenance tool).

Adds to every entity and concept page:

* ``facets: [..]`` — the matching slugs from ``tools/taxonomy.py``.
* ``cluster: <slug>`` on concept pages — the concept-map cluster they belong to.

Also rewrites inline ``related: [a, b]`` frontmatter into the block form used
by entity pages, so graph tooling has one shape to parse.

The ingester treats all three as unmanaged frontmatter and preserves them
verbatim across syncs. Run after editing the taxonomy; it never changes a
page's body, uid or dates.

Usage: python3 tools/backfill_navigation.py [--check]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from taxonomy import CONCEPT_CLUSTERS, assign_facets  # noqa: E402

CLUSTER_BY_CONCEPT = {
    slug: cluster.slug
    for cluster in CONCEPT_CLUSTERS for slug in cluster.concepts
}


def split_frontmatter(text: str) -> tuple[str, str, str] | None:
    """Return (opening, frontmatter body, rest) for a YAML-frontmatter page."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    return "---\n", text[4:end], text[end + 5:]


def page_fields(fm: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in fm.splitlines():
        if ": " in line and not line.startswith((" ", "-", "\t")):
            key, value = line.split(": ", 1)
            fields[key] = value
    return fields


def backfill(path: Path, check: bool) -> bool:
    """Return True when the page would change."""
    original = path.read_text(encoding="utf-8")
    parts = split_frontmatter(original)
    if parts is None:
        return False
    opening, fm, rest = parts
    fields = page_fields(fm)
    if "title" not in fields:
        return False

    summary = fields.get("summary", "").strip('"')
    category = fields.get("category", "").strip('"')
    lead = rest.split("\n## ", 1)[0][:1500]
    facets = assign_facets(f" {fields['title'].strip(chr(34))} {summary} {lead}", category)

    is_concept = fields.get("type", "") == "concept"
    lines = fm.splitlines()
    out: list[str] = []
    changed = False

    for line in lines:
        # One related-list shape everywhere: block style.
        inline = re.match(r"^related:\s*\[(.*)\]\s*$", line)
        if inline:
            values = [v.strip().strip("\"'") for v in inline.group(1).split(",") if v.strip()]
            out.append("related:")
            out.extend(f"  - {v}" for v in values)
            changed = True
            continue
        out.append(line)

    facet_line = "facets: [" + ", ".join(facets) + "]"
    if "facets" not in fields:
        out.append(facet_line)
        changed = True
    else:
        idx = next((i for i, line in enumerate(out) if line.startswith("facets:")), None)
        if idx is not None and out[idx] != facet_line:
            out[idx] = facet_line
            changed = True

    if is_concept:
        cluster = CLUSTER_BY_CONCEPT.get(path.stem)
        if cluster:
            cluster_line = f"cluster: {cluster}"
            existing = next(
                (i for i, line in enumerate(out) if line.startswith("cluster:")),
                None,
            )
            if existing is not None:
                if out[existing] != cluster_line:
                    out[existing] = cluster_line
                    changed = True
            else:
                # Place it beside `type:` for readability on hand-written pages.
                idx = next((i for i, line in enumerate(out)
                            if line.startswith("type:")), len(out))
                out.insert(idx + 1, cluster_line)
                changed = True

    if changed and not check:
        path.write_text(opening + "\n".join(out) + "\n---\n" + rest, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="report changes without writing")
    args = parser.parse_args()
    pages = sorted(p for p in (ROOT / "wiki").rglob("*.md")
                   if not p.name.startswith("index-"))
    changed = [p for p in pages if backfill(p, args.check)]
    verb = "would change" if args.check else "updated"
    print(f"backfill_navigation: {verb} {len(changed)} of {len(pages)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
