#!/usr/bin/env python3
"""Deterministic internal-link checker for this KB.

Scans `index.md` and every `wiki/**/*.md` page and reports:

- broken relative Markdown links in page bodies (target file does not exist),
- unresolved bare slugs in YAML `related:` frontmatter lists (inline or block form),
- wiki pages not reachable from `index.md` through links.

External URLs (http:// or https://) and `kb://` cross-KB links are ignored,
even when they end in `.md`. Only paths are reported, never article prose.

Usage: python3 tools/link_check.py [--json] [--root PATH]
Exit 0 when no problems are found, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent

LINK_RE = re.compile(
    r"\[(?:[^\[\]]|\[[^\[\]]*\])*\]\(\s*"
    r"(<[^>]+>|[^()\s]+(?:\([^()]*\)[^()\s]*)*|[^)\s]+)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)"
)
FRONTMATTER_RE = re.compile(r"\A\ufeff?---\n(.*?)\n---\n", re.DOTALL)
RELATED_INLINE_RE = re.compile(r"^related:\s*\[(.*)\]\s*(?:#.*)?$")
RELATED_BLOCK_RE = re.compile(r"^related:\s*$")
LIST_ITEM_RE = re.compile(r"^\s*-\s+(\S+)\s*(?:#.*)?$")


def iter_pages(root: Path):
    index = root / "index.md"
    if index.is_file():
        yield index
    wiki = root / "wiki"
    if wiki.is_dir():
        yield from sorted(wiki.rglob("*.md"))


def split_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def parse_related(frontmatter: str):
    """Collect slugs from every `related:` block (files may carry duplicates)."""
    slugs = []
    lines = frontmatter.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        inline = RELATED_INLINE_RE.match(line)
        if inline:
            for part in inline.group(1).split(","):
                slug = part.strip().strip("'\"")
                if slug:
                    slugs.append(slug)
            i += 1
            continue
        if RELATED_BLOCK_RE.match(line):
            i += 1
            while i < len(lines):
                item = LIST_ITEM_RE.match(lines[i])
                if not item:
                    break
                slugs.append(item.group(1).strip().strip("'\""))
                i += 1
            continue
        i += 1
    return slugs


def is_ignored(target: str) -> bool:
    t = target.strip().lower()
    return (
        t.startswith("http://")
        or t.startswith("https://")
        or t.startswith("kb://")
        or t.startswith("mailto:")
        or t.startswith("#")
    )


def resolve_link(source: Path, target: str, root: Path) -> Path | None:
    t = target.split("#", 1)[0].split("?", 1)[0].strip()
    if t.startswith("<") and t.endswith(">"):
        t = t[1:-1].strip()
    if not t:
        return None
    t = unquote(t)
    if t.startswith("/"):
        return (root / t.lstrip("/")).resolve()
    return (source.parent / t).resolve()


def require_kb_root(root: Path) -> Path:
    """Fail loudly on a misconfigured root instead of passing an empty audit."""
    root = root.resolve()
    if not root.is_dir() or not (root / "index.md").is_file():
        raise ValueError(f"not a KB root (missing directory or index.md): {root}")
    return root


def check(root: Path) -> dict:
    root = require_kb_root(root)
    pages = list(iter_pages(root))
    page_set = {p.resolve() for p in pages}
    stems = {p.stem for p in pages if p.is_relative_to(root / "wiki")}

    broken_links = []
    unresolved_related = []
    graph: dict[Path, set[Path]] = {}

    for page in pages:
        try:
            text = page.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        frontmatter, body = split_frontmatter(text)
        rel_page = page.relative_to(root).as_posix()

        for slug in parse_related(frontmatter):
            if slug not in stems:
                unresolved_related.append({"source": rel_page, "slug": slug})

        targets = set()
        for m in LINK_RE.finditer(body):
            raw = m.group(1)
            if is_ignored(raw):
                continue
            resolved = resolve_link(page, raw, root)
            if resolved is None:
                continue
            if not resolved.is_relative_to(root):
                broken_links.append(
                    {"source": rel_page, "target": raw.split("#", 1)[0]}
                )
                continue
            targets.add(resolved)
            if not resolved.is_file():
                broken_links.append(
                    {"source": rel_page, "target": raw.split("#", 1)[0]}
                )
        graph[page.resolve()] = targets

    # Reachability from index.md through links to in-repo .md files.
    start = (root / "index.md").resolve()
    reachable = set()
    stack = [start] if start in graph else []
    while stack:
        current = stack.pop()
        if current in reachable:
            continue
        reachable.add(current)
        for target in graph.get(current, ()):
            if target in graph and target not in reachable:
                stack.append(target)

    unreachable = sorted(
        p.relative_to(root).as_posix()
        for p in page_set
        if p != start and p not in reachable and p.is_relative_to(root / "wiki")
    )

    broken_links.sort(key=lambda e: (e["source"], e["target"]))
    unresolved_related.sort(key=lambda e: (e["source"], e["slug"]))

    return {
        "root": str(root),
        "pages_scanned": len(pages),
        "broken_links": broken_links,
        "unresolved_related": unresolved_related,
        "unreachable": unreachable,
        "counts": {
            "broken_links": len(broken_links),
            "unresolved_related": len(unresolved_related),
            "unreachable": len(unreachable),
        },
        "ok": not (broken_links or unresolved_related or unreachable),
    }


def print_human(report: dict) -> None:
    c = report["counts"]
    print(f"Pages scanned: {report['pages_scanned']}")
    print(f"Broken links: {c['broken_links']}")
    for e in report["broken_links"]:
        print(f"  {e['source']} -> {e['target']}")
    print(f"Unresolved related slugs: {c['unresolved_related']}")
    for e in report["unresolved_related"]:
        print(f"  {e['source']} -> {e['slug']}")
    print(f"Unreachable pages: {c['unreachable']}")
    for p in report["unreachable"]:
        print(f"  {p}")
    print("OK" if report["ok"] else "PROBLEMS FOUND")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable report")
    parser.add_argument("--root", type=Path, default=ROOT, help="KB root (default: repo root)")
    args = parser.parse_args(argv)

    try:
        report = check(args.root)
    except ValueError as exc:
        print(f"link_check: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=False))
    else:
        print_human(report)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
