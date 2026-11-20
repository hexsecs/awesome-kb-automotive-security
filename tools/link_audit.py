#!/usr/bin/env python3
"""Crosslink-coverage audit for this KB.

`link_check.py` answers "do the links work?"; this tool answers "are the
pages actually wired together?" It reports:

- article pages with no inbound link from another article (orphans) —
  generated `index-*` sub-indexes are excluded, since they are reached from
  the L1 index by construction;
- entity pages that link to no concept page, and concept pages with very
  few inbound links;
- one-way `related:` pairs between two entity pages.

Both YAML `related:` frontmatter entries and relative Markdown body links
count as inbound links. External URLs and `kb://` links are ignored. The
tool reports only paths and counts, never article prose.

This is a reporting tool: it always exits 0. Use the numbers at campaign
milestones, alongside `concept_scan.py` (theme candidates) and
`link_check.py` (validity).

Usage: python3 tools/link_audit.py [--json] [--root PATH]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from link_check import (
    LINK_RE,
    is_ignored,
    iter_pages,
    parse_related,
    require_kb_root,
    resolve_link,
    split_frontmatter,
)

ROOT = Path(__file__).resolve().parent.parent


def declared_type(frontmatter: str) -> str | None:
    """Read `type:` the way the other tools do: top-level, LAST match wins.

    A regex with ``re.M`` and a first-match search disagreed with every other
    tool (they build a dict from top-level fields, so a duplicate key's last
    value wins). Malformed duplicate keys should not make this audit classify
    a page differently from the ingester that wrote it.
    """
    value = None
    for line in frontmatter.splitlines():
        if ": " not in line or line.startswith((" ", "\t", "-")):
            continue
        key, raw = line.split(": ", 1)
        if key.strip() != "type":
            continue
        candidate = raw.strip().strip("'\"").split("#", 1)[0].strip()
        if candidate in ("concept", "entity"):
            value = candidate
    return value


def audit(root: Path) -> dict:
    root = require_kb_root(root)
    pages = list(iter_pages(root))
    wiki = root / "wiki"
    stems = {p.stem for p in pages if p.is_relative_to(wiki)}
    page_set = {p.resolve() for p in pages}

    out: dict[Path, set[Path]] = {}
    inbound: dict[Path, set[Path]] = {}
    kind: dict[Path, str] = {}

    for page in pages:
        try:
            text = page.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        frontmatter, body = split_frontmatter(text)
        rel = page.relative_to(root).as_posix()
        is_wiki = page.is_relative_to(wiki)
        is_concept = is_wiki and page.parent.name == "concepts"
        is_index = page.stem.startswith("index-") or rel == "index.md"
        declared = declared_type(frontmatter)
        kind[page.resolve()] = (
            declared if declared else
            "index" if is_index else "concept" if is_concept
            else "entity" if is_wiki else "other"
        )

        targets: set[Path] = set()
        for slug in parse_related(frontmatter):
            # Resolve a bare slug to any wiki page with that stem.
            if slug in stems:
                matches = sorted(
                    (p for p in page_set
                     if p.stem == slug and p.is_relative_to(wiki)),
                    # A bare slug names the ENTITY at wiki/<slug>.md; a
                    # concept at wiki/concepts/<slug>.md is a different page.
                    # Without this tie-break the concept won (it sorts first)
                    # and the entity was reported as an orphan.
                    key=lambda p: (p.parent.name == "concepts", str(p)),
                )
                if matches:
                    targets.add(matches[0])
        for m in LINK_RE.finditer(body):
            raw = m.group(1)
            if is_ignored(raw):
                continue
            try:
                resolved = resolve_link(page, raw, root)
            except (OSError, ValueError, RuntimeError):
                continue  # e.g. a `%00` escape — a reporting tool must not abort
            if resolved is not None and resolved in page_set:
                targets.add(resolved)

        out[page.resolve()] = targets
        # Only articles (entity/concept) count as an inbound link; generated
        # index-* pages are reached from the L1 index by construction and
        # would make the orphan metric vacuous.
        if kind.get(page.resolve()) in ("entity", "concept"):
            for target in targets:
                inbound.setdefault(target, set()).add(page.resolve())

    def name(p: Path) -> str:
        return p.relative_to(root).as_posix()

    articles = [p for p in pages if kind.get(p.resolve()) == "entity"]
    concepts = [p for p in pages if kind.get(p.resolve()) == "concept"]

    orphans = sorted(
        name(p) for p in articles if not inbound.get(p.resolve())
    )
    no_concept = sorted(
        name(p) for p in articles
        if not any(kind.get(t) == "concept" for t in out.get(p.resolve(), ()))
    )
    concept_coverage = [
        {"page": name(p), "inbound": len(inbound.get(p.resolve(), ()))}
        for p in concepts
    ]
    concept_coverage.sort(key=lambda e: (e["inbound"], e["page"]))

    one_way = []
    entity_stems = {p.stem for p in articles}
    for p in articles:
        prelated = set(parse_related(split_frontmatter(
            p.read_text(encoding="utf-8"))[0]))
        for slug in prelated:
            if slug not in entity_stems or slug == p.stem:
                continue
            matches = [q for q in articles if q.stem == slug]
            if not matches:
                continue
            q = matches[0]
            back = set(parse_related(split_frontmatter(
                q.read_text(encoding="utf-8"))[0]))
            if p.stem not in back:
                one_way.append({"source": name(p), "target": name(q)})
    one_way.sort(key=lambda e: (e["source"], e["target"]))

    low = concept_coverage[:5]
    return {
        "root": str(root),
        "pages_scanned": len(pages),
        "entity_pages": len(articles),
        "concept_pages": len(concepts),
        "counts": {
            "orphans": len(orphans),
            "entities_without_concept_link": len(no_concept),
            "one_way_related_pairs": len(one_way),
        },
        "orphans": orphans,
        "entities_without_concept_link": no_concept,
        "concept_inbound": concept_coverage,
        "lowest_coverage_concepts": low,
        "one_way_related_pairs": one_way,
    }


def print_human(report: dict) -> None:
    c = report["counts"]
    print(f"Pages scanned: {report['pages_scanned']} "
          f"({report['entity_pages']} entity, {report['concept_pages']} concept)")
    print(f"Orphan entity pages (0 inbound): {c['orphans']}")
    for p in report["orphans"]:
        print(f"  {p}")
    print(f"Entity pages linking to no concept: {c['entities_without_concept_link']}")
    print(f"One-way entity related pairs: {c['one_way_related_pairs']}")
    print("Lowest-coverage concepts:")
    for e in report["lowest_coverage_concepts"]:
        print(f"  {e['inbound']:3} {e['page']}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable report")
    parser.add_argument("--root", type=Path, default=ROOT, help="KB root (default: repo root)")
    args = parser.parse_args(argv)
    try:
        report = audit(args.root)
    except ValueError as exc:
        print(f"link_audit: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
