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
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from link_check import related_scalar, split_flow_items  # noqa: E402
from taxonomy import CONCEPT_CLUSTERS, assign_facets  # noqa: E402

CLUSTER_BY_CONCEPT = {
    slug: cluster.slug
    for cluster in CONCEPT_CLUSTERS for slug in cluster.concepts
}


def split_frontmatter(text: str) -> tuple[str, str, str] | None:
    """Return (opening, frontmatter body, rest) for a YAML-frontmatter page."""
    if text.startswith("\ufeff"):
        text = text[1:]
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    body_start = end + 5
    if end == -1 and text.endswith("\n---"):
        end, body_start = len(text) - 4, len(text)
    if end == -1:
        return None
    return "---\n", text[4:end], text[body_start:]


def scalar(raw: str) -> str:
    """Parse one YAML scalar, dropping a trailing comment outside quotes."""
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


def page_fields(fm: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in fm.splitlines():
        if ": " in line and not line.startswith((" ", "-", "\t")):
            key, value = line.split(": ", 1)
            # YAML allows space before the colon; ingest and link_audit strip
            # it, so an unstripped key here silently hides the whole page.
            fields[key.strip()] = scalar(value)
    return fields


def managed_block_spans(lines: list[str], key: str
                        ) -> tuple[list[int], set[int]]:
    """Key lines and their block-list lines for a frontmatter key.

    Both `facets: [a, b]` and `facets:\\n  - a\\n  - b` are valid YAML. Writing
    the inline form over only the key line leaves the block items dangling,
    which is invalid YAML and makes ingest read a different (or no) value.
    Comments and blanks between items belong to the block; a trailing comment
    does not and is left alone.
    """
    # YAML allows a space before the colon (ingest and page_fields strip it),
    # so a `cluster : stale` key must be recognised and rewritten in place.
    keys = [i for i, line in enumerate(lines)
            if re.match(rf"^{re.escape(key)}\s*:", line)]
    continuations: set[int] = set()
    for i in keys:
        key_line = lines[i]
        # A block scalar (`facets: |`, `cluster: >-`) owns every more-indented
        # line, not just `- item` lines. Rewriting only the key left the old
        # prose behind: invalid YAML, or a silently concatenated value.
        # YAML permits the indentation and chomping indicators in either
        # order (`|2-` and `|-2` are both valid); `[+-]?\d*` only matched the
        # second, leaving the first's prose orphaned as invalid YAML.
        if re.match(
                rf"^{re.escape(key)}\s*:\s*[|>](?:[1-9][+-]?|[+-][1-9]?)?"
                r"\s*(?:#.*)?$", key_line):
            base_indent = len(key_line) - len(key_line.lstrip())
            for j in range(i + 1, len(lines)):
                line = lines[j]
                if not line.strip():
                    continuations.add(j)
                    continue
                if (len(line) - len(line.lstrip())) > base_indent:
                    continuations.add(j)
                else:
                    break
            continue
        pending: list[int] = []  # blank/comment lines awaiting a later item
        for j in range(i + 1, len(lines)):
            item = lines[j].lstrip()
            if re.match(r"^-\s+", item):
                continuations.update(pending)
                continuations.add(j)
                pending = []
            elif not item or item.startswith("#"):
                pending.append(j)
            else:
                break
    return keys, continuations


def within_root(path: Path) -> bool:
    """True when ``path`` resolves to a location inside the KB root."""
    try:
        return path.resolve().is_relative_to(ROOT.resolve())
    except OSError:
        return False


def preflight(targets: list[Path]) -> None:
    """Refuse every unsafe write target before the first page is modified."""
    for path in targets:
        if path.is_symlink() or not within_root(path):
            sys.exit(f"backfill_navigation: refusing to write through symlink {path}")
        if path.is_dir():
            sys.exit(f"backfill_navigation: refusing to write a directory at {path}")
        if path.exists() and path.stat().st_nlink > 1:
            sys.exit(f"backfill_navigation: refusing to write hardlinked file {path}")
        if path.exists() and not os.access(path, os.W_OK):
            sys.exit(f"backfill_navigation: cannot write {path}: permission denied")


def backfill(path: Path, check: bool) -> bool:
    """Return True when the page would change."""
    if path.is_symlink() or not within_root(path):
        return False
    try:
        original = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        sys.exit(f"backfill_navigation: cannot read {path}: {exc}")
    parts = split_frontmatter(original)
    if parts is None:
        return False
    opening, fm, rest = parts
    fields = page_fields(fm)
    if "title" not in fields:
        return False

    # ``page_fields`` already runs each scalar through ``scalar()``, which
    # unwraps quotes. Stripping them again corrupts a title/summary that
    # legitimately begins or ends with a quote character.
    summary = fields.get("summary", "")
    category = fields.get("category", "")
    lead = rest.split("\n## ", 1)[0][:1500]
    facets = assign_facets(f" {fields['title']} {summary} {lead}", category)

    is_concept = fields.get("type", "") == "concept"
    lines = fm.splitlines()
    out: list[str] = []
    changed = False

    for line in lines:
        # One related-list shape everywhere: block style.
        inline = re.match(r"^related\s*:\s*\[([^\]]*)\]\s*(?:#.*)?$", line)
        if inline:
            values = [related_scalar(v)
                      for v in split_flow_items(inline.group(1)) if v.strip()]
            out.append("related:")
            out.extend(f"  - {json.dumps(v, ensure_ascii=False)}" for v in values)
            changed = True
            continue
        out.append(line)

    facet_line = "facets: [" + ", ".join(facets) + "]"
    idxs, continuations = managed_block_spans(out, "facets")
    if not idxs:
        out.append(facet_line)
        changed = True
    else:
        # Duplicate YAML keys are legal but the LAST one wins: a stale second
        # `facets:` would silently shadow the value just backfilled. Remove
        # its whole block, not just the key line, or the items are orphaned.
        for i in sorted(continuations | set(idxs[1:]), reverse=True):
            del out[i]
            changed = True
        if out[idxs[0]] != facet_line:
            out[idxs[0]] = facet_line
            changed = True

    if is_concept:
        cluster = CLUSTER_BY_CONCEPT.get(path.stem)
        if cluster:
            cluster_line = f"cluster: {cluster}"
            existing, continuations = managed_block_spans(out, "cluster")
            if existing:
                # Same last-wins rule as facets: only the first cluster line
                # is rewritten, so a stale second one must be removed.
                for i in sorted(continuations | set(existing[1:]), reverse=True):
                    del out[i]
                    changed = True
                if out[existing[0]] != cluster_line:
                    out[existing[0]] = cluster_line
                    changed = True
            else:
                # Place it beside `type:` for readability on hand-written pages.
                idx = next((i for i, line in enumerate(out)
                            if line.startswith("type:")), len(out))
                out.insert(idx + 1, cluster_line)
                changed = True

    if changed and not check:
        if path.is_dir():
            sys.exit(f"backfill_navigation: refusing to write a directory at {path}")
        if path.exists() and path.stat().st_nlink > 1:
            sys.exit(f"backfill_navigation: refusing to write hardlinked file {path}")
        try:
            path.write_text(opening + "\n".join(out) + "\n---\n" + rest,
                            encoding="utf-8")
        except OSError as exc:
            sys.exit(f"backfill_navigation: cannot write {path}: {exc}")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="report changes without writing")
    args = parser.parse_args()
    # Generated indexes have no frontmatter and are skipped by ``backfill``;
    # filtering on the ``index-`` NAME used to hide authored entities whose
    # slug legitimately starts with that prefix. ``is_file`` also skips a
    # directory named ``*.md``, which ``rglob`` otherwise feeds to read_text.
    pages = sorted(p for p in (ROOT / "wiki").rglob("*.md")
                   if p.is_file() and not p.is_symlink() and within_root(p))
    # Determine the write set in --check mode first, then preflight all of
    # it. Writing inline left an alphabetical prefix of the KB backfilled
    # when a later page was unsafe — the defect link_mine fixed by refusing
    # up front (row 110), never ported here.
    changing = [p for p in pages if backfill(p, True)]
    if not args.check:
        preflight(changing)
        for p in changing:
            backfill(p, False)
    verb = "would change" if args.check else "updated"
    print(f"backfill_navigation: {verb} {len(changing)} of {len(pages)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
