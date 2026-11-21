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
FRONTMATTER_RE = re.compile(r"\A\ufeff?---\n(.*?)\n---(?:\n|\Z)", re.DOTALL)
# YAML permits whitespace before the colon. A `related : [a]` key is the same
# field as `related: [a]`; treating it as absent made the whole graph toolchain
# (link_check, link_audit, link_mine, ingest) miss real links.
RELATED_INLINE_RE = re.compile(r"^related\s*:\s*\[([^\]]*)\]\s*(?:#.*)?$")
RELATED_FLOW_START_RE = re.compile(r"^related\s*:\s*\[([^\]]*)$")
RELATED_BLOCK_RE = re.compile(r"^related\s*:\s*(?:#.*)?$")
LIST_ITEM_RE = re.compile(r"^\s*-\s+(.*?)\s*$")


def iter_pages(root: Path):
    root = root.resolve()
    index = root / "index.md"
    if index.is_file() and not index.is_symlink():
        yield index
    wiki = root / "wiki"
    if wiki.is_dir() and not wiki.is_symlink():
        for page in sorted(wiki.rglob("*.md")):
            # ``rglob`` matches directories named ``*.md`` too, and a
            # symlinked leaf would read from outside the KB. Skip both.
            if not page.is_file() or page.is_symlink():
                continue
            try:
                if not page.resolve().is_relative_to(root):
                    continue
            except (OSError, RuntimeError):
                continue
            yield page


def split_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def split_flow_items(body: str) -> list[str]:
    """Split a YAML flow sequence on commas outside quotes.

    ``"alpha, beta"`` is one slug containing a comma, not two. Splitting the
    raw text fabricated a bogus slug and, in backfill, permanently rewrote a
    two-item list into three (rows 2/43 fixed comments, not quoting).
    """
    items: list[str] = []
    buf: list[str] = []
    quote: str | None = None
    escaped = False
    for ch in body:
        if quote:
            buf.append(ch)
            if quote == '"' and ch == "\\" and not escaped:
                escaped = True
                continue
            if ch == quote and not escaped:
                quote = None
            escaped = False
        elif ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch == ",":
            items.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    items.append("".join(buf))
    return items


def related_scalar(raw: str) -> str:
    """Read one YAML scalar from a related-list item.

    Both the inline and block shapes may quote a slug that contains spaces
    or a comma (row 190 made the inline comma form legal). Capturing only
    ``\\S+`` silently dropped such a whole block, and a bare ``strip("'\\\"")``
    left JSON escapes or doubled single quotes in the value that backfill
    then wrote back permanently changed.
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
        return str(json.loads(raw))
    except (json.JSONDecodeError, ValueError):
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
            inner = raw[1:-1]
            return inner.replace("''", "'") if raw[0] == "'" else inner
        return raw


def parse_related(frontmatter: str):
    """Collect slugs from every `related:` block (files may carry duplicates)."""
    slugs = []
    lines = frontmatter.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        inline = RELATED_INLINE_RE.match(line)
        if inline:
            for part in split_flow_items(inline.group(1)):
                slug = related_scalar(part)
                if slug:
                    slugs.append(slug)
            i += 1
            continue
        # YAML flow sequences may span lines. Rejoin them before the
        # one-line matcher so a hand-wrapped list is not silently empty.
        flow = RELATED_FLOW_START_RE.match(line)
        if flow:
            collected = [flow.group(1)]
            j = i + 1
            while j < len(lines) and "]" not in lines[j]:
                collected.append(lines[j])
                j += 1
            if j < len(lines):
                tail = lines[j].split("]", 1)[1]
                if re.match(r"^\s*(?:#.*)?$", tail):
                    collected.append(lines[j].split("]", 1)[0])
                    for part in split_flow_items(" ".join(collected)):
                        slug = related_scalar(part)
                        if slug:
                            slugs.append(slug)
                    i = j + 1
                    continue
        if RELATED_BLOCK_RE.match(line):
            i += 1
            while i < len(lines):
                cont = lines[i]
                # YAML allows blank lines and standalone comments between
                # a block key and its items. Stopping at the first one made
                # a hand-curated list look empty to every graph tool, so
                # fill-only then mined over the authored links.
                if not cont.strip() or cont.lstrip().startswith("#"):
                    i += 1
                    continue
                item = LIST_ITEM_RE.match(cont)
                if not item:
                    break
                slug = related_scalar(item.group(1))
                if slug:
                    slugs.append(slug)
                i += 1
            continue
        i += 1
    return slugs


def unwrap(target: str) -> str:
    """Markdown angle-bracket destinations: `<url>` wraps the real target."""
    t = target.strip()
    return t[1:-1].strip() if t.startswith("<") and t.endswith(">") else t


def is_ignored(target: str) -> bool:
    t = unwrap(target).lower()
    return (
        t.startswith("http://")
        or t.startswith("https://")
        or t.startswith("//")  # scheme-relative URL: always off-KB
        or t.startswith("kb://")
        or t.startswith("mailto:")
        or t.startswith("#")
    )


def resolve_link(source: Path, target: str, root: Path) -> Path | None:
    # Unwrap BEFORE splitting off the fragment: `<#section>` is an anchor, not
    # a file literally named `<`.
    t = unwrap(target).split("#", 1)[0].split("?", 1)[0].strip()
    if not t:
        return None
    t = unquote(t)
    if t.startswith("/"):
        return (root / t.lstrip("/")).resolve()
    return (source.parent / t).resolve()


def require_kb_root(root: Path) -> Path:
    """Fail loudly on a misconfigured root instead of passing an empty audit."""
    root = root.resolve()
    index = root / "index.md"
    # iter_pages() refuses a symlinked index.md, so admitting it here would
    # audit a KB with no start node and report every page as unreachable.
    if not root.is_dir() or not index.is_file() or index.is_symlink():
        raise ValueError(f"not a KB root (missing or symlinked index.md): {root}")
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
            # Keep unreadable pages in the graph with no outgoing links. A
            # valid inbound link still makes them reachable; dropping them
            # here reported them as orphans even though Broken links was 0.
            graph[page.resolve()] = set()
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
            # A `%00` escape becomes a NUL after unquoting and makes
            # ``Path.resolve``/``is_file`` raise. Record it as a broken link
            # rather than aborting the whole audit.
            try:
                resolved = resolve_link(page, raw, root)
                broken = resolved is not None and (
                    not resolved.is_relative_to(root) or not resolved.is_file()
                )
            except (OSError, ValueError, RuntimeError):
                resolved, broken = None, True
            if resolved is None and not broken:
                continue
            if broken:
                # `unwrap()` already decides resolution; the report must use
                # the same string or `<missing.md#sec>` is truncated into a
                # target that does not exist even as a literal path.
                broken_links.append(
                    {"source": rel_page,
                     "target": unwrap(raw).split("#", 1)[0]}
                )
                continue
            targets.add(resolved)
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
