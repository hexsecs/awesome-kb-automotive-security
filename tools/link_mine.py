#!/usr/bin/env python3
"""Mine cross-links for this KB: fill `related:` on entity pages.

The ingester (tools/ingest.py) creates each page as an island: it never
writes `related:`, and links otherwise appear only when a human or agent
deepens a page by hand. This tool is the missing machine pass. It scores
every pair of entity pages from the signals a stub actually carries —
title, list summary, category, resource URL — and writes the strongest
relations as a reciprocal `related:` block.

Signals (all deterministic; same corpus in, same links out):
- shared significant tokens in title+summary, weighted by inverse
  document frequency (rare tokens are the informative ones);
- a page's title mentioned in another page's summary (strong);
- same list category (weak boost);
- same resource host/org, e.g. the same GitHub organisation (medium).

`related:` is an author-owned field (the ingester preserves unmanaged
frontmatter blocks verbatim), so mined links survive ingest syncs. A
page whose block changes gets its `updated:` stamp moved to the run
date — a mined link set is a substantive change to a stub.

Modes:
- default: recompute every non-archived entity page's set from scratch
  (safe where pages are machine-generated stubs);
- --fill-only: touch only pages whose `related:` is empty (the mode
  for KBs with hand-curated pages), plus --reciprocate to complete
  one-way links that already exist;
- --dry-run: print the census and samples, write nothing.

Usage: python3 tools/link_mine.py [--dry-run] [--fill-only]
       [--reciprocate] [--date YYYY-MM-DD] [--max-related 8]
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date as date_cls
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

from link_check import parse_related as _shared_parse_related

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "for", "to", "in", "on", "with",
    "via", "using", "use", "used", "based", "from", "by", "at", "as",
    "is", "are", "be", "it", "its", "this", "that", "your", "you", "can",
    "into", "over", "under", "per", "etc", "one", "two", "new", "open",
    "source", "free", "tools", "tool", "library", "framework", "project",
    "support", "supports", "supported", "system", "systems", "software",
    "hardware", "embedded", "security", "analysis", "research",
}


def tokens(text: str) -> list[str]:
    out = []
    for tok in re.split(r"[^a-z0-9]+", text.lower()):
        if len(tok) >= 3 and tok not in STOPWORDS and not tok.isdigit():
            out.append(tok)
    return out


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


def split_page(text: str) -> tuple[dict, list[str], str]:
    """(scalar fields, frontmatter lines, body) — scalars best-effort."""
    if text.startswith("\ufeff"):
        text = text[1:]
    if not text.startswith("---\n"):
        return {}, [], text
    end = text.find("\n---\n", 4)
    body_start = end + 5
    if end == -1 and text.endswith("\n---"):
        end, body_start = len(text) - 4, len(text)
    if end == -1:
        return {}, [], text
    fm_lines = text[4:end].splitlines()
    fields: dict = {}
    for line in fm_lines:
        # Match the ingester/backfill rule: a tab-indented line is nested
        # YAML, not a top-level field. Without ``\t`` a stray ``\ttype:
        # concept`` overrode the real ``type: entity`` here only.
        if ": " in line and not line.startswith((" ", "-", "\t")):
            key, raw = line.split(": ", 1)
            fields[key.strip()] = scalar(raw)
    return fields, fm_lines, text[body_start:]


def parse_related(fm_lines: list[str]) -> list[str]:
    """Parse `related:` slugs using link_check's parser so the two agree.

    Sharing the parser prevents the tools from disagreeing on comments,
    tab-indented list items, quoted scalars, or duplicated blocks.
    """
    return _shared_parse_related("\n".join(fm_lines))


def read_page(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"link_mine: skipping unreadable {path}: {exc}", file=sys.stderr)
        return None


def within_root(path: Path) -> bool:
    """True when ``path`` resolves to a location inside the KB root."""
    try:
        return path.resolve().is_relative_to(ROOT.resolve())
    except OSError:
        return False


def preflight(targets: list[Path]) -> None:
    """Reject every unsafe target before the first page is modified.

    Refusing a bad page mid-loop left an earlier alphabetical prefix of the
    KB mined and the rest untouched — a worse state than refusing up front.
    """
    for path in targets:
        if path.is_symlink() or not within_root(path):
            sys.exit(f"link_mine: refusing to write through symlink {path}")
        if path.is_dir():
            sys.exit(f"link_mine: refusing to write a directory at {path}")
        if path.exists() and path.stat().st_nlink > 1:
            sys.exit(f"link_mine: refusing to write hardlinked file {path}")
        if path.exists() and not os.access(path, os.W_OK):
            sys.exit(f"link_mine: cannot write {path}: permission denied")


def write_page(path: Path, fm_lines: list[str], body: str,
               related: list[str], run_date: str) -> None:
    """Replace/insert the related block; bump `updated:`; write the file."""
    if path.is_symlink() or not within_root(path):
        return
    if path.is_dir():
        sys.exit(f"link_mine: refusing to write a directory at {path}")
    if path.exists() and path.stat().st_nlink > 1:
        sys.exit(f"link_mine: refusing to write hardlinked file {path}")
    out: list[str] = []
    i = 0
    block = ["related:"] + [
        f"  - {json.dumps(slug, ensure_ascii=False)}" for slug in related
    ]
    # Pre-scan: if any related: block exists, the single replacement
    # block goes where the FIRST one was; never also after list_summary.
    had_related = any(l.startswith("related:") for l in fm_lines)
    placed = False
    while i < len(fm_lines):
        line = fm_lines[i]
        if line.startswith("related:"):
            if not placed:
                out.extend(block)
                placed = True
            i += 1
            # skip the old block's continuation lines (space- or tab-indented,
            # with or without trailing comments — whatever link_check reads)
            while i < len(fm_lines) and re.match(r"^\s*-\s+", fm_lines[i]):
                i += 1
            continue
        if line.startswith("updated:"):
            line = f"updated: {run_date}"
        out.append(line)
        if not placed and not had_related and line.startswith("list_summary:"):
            out.extend(block)
            placed = True
        i += 1
    if not placed:
        out.extend(block)
    try:
        path.write_text("---\n" + "\n".join(out) + "\n---\n" + body,
                        encoding="utf-8")
    except OSError as exc:
        sys.exit(f"link_mine: cannot write {path}: {exc}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--fill-only", action="store_true",
                    help="only pages with an empty related: get a set")
    ap.add_argument("--reciprocate", action="store_true",
                    help="also complete one-way links that already exist")
    ap.add_argument("--date", default=None,
                    help="updated: stamp for changed pages (default: today ET)")
    ap.add_argument("--max-related", type=int, default=6)
    ap.add_argument("--threshold", type=float, default=3.0)
    args = ap.parse_args()
    if args.date and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        ap.error("--date must be YYYY-MM-DD")
    run_date = args.date or str(
        date_cls.today() if False else
        __import__("datetime").datetime.now(ZoneInfo("America/Detroit")).date())

    pages: dict[str, dict] = {}
    for path in sorted(WIKI.rglob("*.md")):
        # Authored pages can legitimately be named `index-*` and can live in
        # subdirectories; only real, in-root, non-symlink files are entities.
        # A FIFO or a `*.md` directory would otherwise block on read_text().
        if (not path.is_file() or path.is_symlink()
                or not within_root(path)):
            continue
        text = read_page(path)
        if text is None:
            continue
        fields, fm_lines, body = split_page(text)
        if fields.get("type") != "entity" or "title" not in fields:
            continue
        if str(fields.get("status")) == "archived":
            continue
        # Key by path, not stem: rglob admits nested pages, and two files
        # may share a stem. The slug written into `related:` stays the stem
        # (that is what link_check resolves against).
        key = path.relative_to(WIKI).with_suffix("").as_posix()
        pages[key] = {
            "path": path, "slug": path.stem, "fields": fields,
            "fm_lines": fm_lines, "body": body,
            "related": parse_related(fm_lines),
        }
    if not pages:
        print("link_mine: no entity pages found")
        return 0

    # Document frequencies over title+summary tokens.
    page_tokens: dict[str, Counter] = {}
    df: Counter = Counter()
    for slug, p in pages.items():
        f = p["fields"]
        toks = Counter(tokens(str(f.get("title", ""))) * 3
                       + tokens(str(f.get("summary", ""))) * 2)
        page_tokens[slug] = toks
        for tok in toks:
            df[tok] += 1
    n = len(pages)
    idf = {t: math.log((n + 1) / (c + 0.5)) for t, c in df.items()}

    def org_of(p: dict) -> str:
        # Only code-host orgs are a real signal (the same GitHub org
        # publishing two tools). A shared document host (usenix.org,
        # arxiv.org, youtube.com) says nothing about relatedness.
        url = str(p["fields"].get("url", ""))
        host = urlparse(url).netloc.lower()
        parts = [x for x in urlparse(url).path.split("/") if x]
        if host == "github.com" and parts:
            return f"github.com/{parts[0].lower()}"
        return ""

    # A category is evidence only when it is selective: a section
    # holding most of the corpus (e.g. Research Papers) boosts
    # everything and therefore nothing.
    cat_counts = Counter(str(p["fields"].get("category", ""))
                         for p in pages.values())

    slugs = sorted(pages)
    stems = {key: p["slug"] for key, p in pages.items()}
    scores: dict[tuple[str, str], float] = {}
    for i, a in enumerate(slugs):
        ta = page_tokens[a]
        fa = pages[a]["fields"]
        title_a = str(fa.get("title", "")).lower()
        summ_a = str(fa.get("summary", "")).lower()
        for b in slugs[i + 1:]:
            # Two pages can share a stem. `related:` stores stems, so mining
            # that pair would collapse into a self-link that link_check cannot
            # even see as broken. Skip the ambiguous pair entirely.
            if pages[a]["slug"] == pages[b]["slug"]:
                continue
            tb = page_tokens[b]
            fb = pages[b]["fields"]
            shared = set(ta) & set(tb)
            s = sum(min(ta[t], tb[t]) * idf[t] for t in shared) / 3.0
            if fa.get("category") and fa.get("category") == fb.get("category") \
                    and cat_counts[str(fa.get("category"))] <= 0.20 * n:
                s += 1.0
            if org_of(pages[a]) and org_of(pages[a]) == org_of(pages[b]):
                s += 1.5
            title_b = str(fb.get("title", "")).lower()
            summ_b = str(fb.get("summary", "")).lower()
            distinctive_a = [t for t in tokens(title_a) if idf.get(t, 0) > 2.0]
            distinctive_b = [t for t in tokens(title_b) if idf.get(t, 0) > 2.0]
            # Whole-token match only: a title "Bus" is not mentioned by a
            # summary about "rebus puzzles". Substring hits invented links.
            summ_a_tokens, summ_b_tokens = set(tokens(summ_a)), set(tokens(summ_b))
            if distinctive_b and all(t in summ_a_tokens
                                     for t in distinctive_b[:2]):
                s += 3.0
            if distinctive_a and all(t in summ_b_tokens
                                     for t in distinctive_a[:2]):
                s += 3.0
            if s >= args.threshold:
                scores[(a, b)] = s
                scores[(b, a)] = s

    # Grow mutual pairs in global score order. Capping AFTER symmetrising
    # (the old way) cut one side of a pair and left one-way links, which
    # --reciprocate then needed a second pass to repair. Each pair is added
    # only when BOTH ends still have room, so every written link is mutual.
    neighbours: dict[str, list[str]] = defaultdict(list)
    for a, b in scores:
        neighbours[a].append(b)
    for a in neighbours:
        neighbours[a].sort(key=lambda b: (-scores[(a, b)], b))
    pairs = [(a, b) for a in slugs for b in neighbours[a] if a < b]
    pairs.sort(key=lambda ab: (-scores[ab], ab))
    final: dict[str, list[str]] = {a: [] for a in slugs}
    for a, b in pairs:
        if len(final[a]) < args.max_related and len(final[b]) < args.max_related:
            final[a].append(b)
            final[b].append(a)

    # Concept pages are never written by this tool, but their related
    # lists are sources for reciprocation: a concept that draws on an
    # entity should be linked back from that entity (house practice).
    concept_links: dict[str, list[str]] = {}
    # A concept is any `type: concept` page, wherever it lives — this is the
    # definition concept_scan and link_audit use. Scanning only concepts/
    # missed root-level concepts and broke reciprocation for their links.
    for path in sorted(WIKI.rglob("*.md")):
        if not path.is_file() or path.is_symlink() or not within_root(path):
            continue
        text = read_page(path)
        if text is None:
            continue
        fields, fm_lines, _ = split_page(text)
        if fields.get("type") == "concept" and "title" in fields:
            # Two concepts can share a stem. Last-write-wins here dropped the
            # canonical page's links; every page with that stem must feed
            # reciprocation (L1 and the concept map still prefer canonical).
            concept_links.setdefault(path.stem, []).extend(
                parse_related(fm_lines))

    changed = filled = recip_added = 0
    written: dict[str, list[str]] = {}
    samples: list[str] = []
    to_write: list[tuple[Path, list[str], str, list[str]]] = []
    for slug in slugs:
        p = pages[slug]
        old = p["related"]
        own = stems[slug]
        # Who already links here, that this page does not link back to?
        # `related:` entries are stems, while `slugs` are path keys.
        incoming = {o for o in slugs if own in pages[o]["related"]}
        incoming |= {c for c, rels in concept_links.items()
                     if own in rels}
        # With --reciprocate, preserve an author-owned set as the base;
        # otherwise default mode discarded it before adding the backlink and
        # the pair flipped direction on every run forever.
        fill_branch = bool(old) and (args.fill_only or args.reciprocate)
        if fill_branch:
            # Author-owned set: preserve it verbatim and in order;
            # only append missing reciprocal links.
            new = list(old)
        else:
            new = list(final[slug])
        if args.reciprocate:
            # `related:` holds stems, while `slugs` and `scores` use path
            # keys. Work at stem level so a link already on disk, or a
            # second path key sharing a stem, is not counted as a new add.
            seen = {stems.get(x, x) for x in old + new}
            adds = []
            for o in sorted(incoming,
                            key=lambda b: (-scores.get((slug, b), 0.0), b)):
                stem = stems.get(o, o)
                if stem not in seen:
                    adds.append(o)
                    seen.add(stem)
            new = new + adds
            recip_added += len(adds)
        if not fill_branch:
            new = sorted(set(new),
                         key=lambda b: (-scores.get((slug, b), 0.0), b))
        # Path keys are internal; the written slugs stay stems, which is
        # what link_check resolves. Two pages sharing a stem dedupe here.
        new_slugs = [s for s in dict.fromkeys(stems.get(x, x) for x in new)
                     if s != own]
        written[slug] = new_slugs
        if new_slugs != old:
            changed += 1
            if not old:
                filled += 1
            if len(samples) < 5:
                samples.append(f"  {slug}: {old} -> {new_slugs}")
            if not args.dry_run:
                to_write.append((p["path"], p["fm_lines"], p["body"],
                                 new_slugs))

    if to_write:
        preflight([item[0] for item in to_write])
        for path, fm, body, new_slugs in to_write:
            write_page(path, fm, body, new_slugs, run_date)

    total_rel = sum(len(written[s]) for s in slugs)
    zero = sum(1 for s in slugs if not written[s])
    print(f"link_mine: {n} entity pages | mined sets avg "
          f"{total_rel / n:.2f} related/page, {zero} pages with none | "
          f"{'would change' if args.dry_run else 'changed'} {changed} pages "
          f"({filled} previously unlinked, {recip_added} reciprocal adds)")
    for line in samples:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
