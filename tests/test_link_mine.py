#!/usr/bin/env python3
"""Regression tests for tools/link_mine.py write_page(). Stdlib only."""

import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))  # link_mine imports parse_related from link_check
TOOLS = TOOLS_DIR / "link_mine.py"
spec = importlib.util.spec_from_file_location("link_mine", TOOLS)
link_mine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(link_mine)


def make_page(text: str) -> Path:
    d = Path(tempfile.mkdtemp())
    p = d / "alpha.md"
    p.write_text(text, encoding="utf-8")
    # The temp dir is this fixture's KB root: point the containment guard at it.
    link_mine.ROOT, link_mine.WIKI = d, d
    return p


def split(text: str):
    return link_mine.split_page(text)


PAGE_DUP = (
    "---\n"
    "title: \"Alpha\"\n"
    "type: entity\n"
    "list_summary: \"Alpha summary\"\n"
    "related:\n"
    "  - alpha-one\n"
    "  - alpha-two\n"
    "sources:\n"
    "  - https://example.invalid/alpha\n"
    "related:\n"
    "  - alpha-one\n"
    "  - alpha-two\n"
    "updated: 2020-01-01\n"
    "---\n"
    "Body line one.\n"
    "Body line two.\n"
)

PAGE_RELATED_AFTER_SOURCES = (
    "---\n"
    "title: \"Beta\"\n"
    "type: entity\n"
    "list_summary: \"Beta summary\"\n"
    "sources:\n"
    "  - https://example.invalid/beta\n"
    "related:\n"
    "  - beta-one\n"
    "updated: 2020-01-01\n"
    "---\n"
    "Beta body.\n"
)


class _RootRestoringTest(unittest.TestCase):
    def setUp(self):
        self._saved = (link_mine.ROOT, link_mine.WIKI)

    def tearDown(self):
        link_mine.ROOT, link_mine.WIKI = self._saved


class WritePageTests(_RootRestoringTest):
    def test_duplicate_related_blocks_collapse_to_first(self):
        path = make_page(PAGE_DUP)
        _, fm_lines, body = split(PAGE_DUP)
        # parse_related now collects every block (matching link_check); the
        # caller dedupes before writing, and write_page collapses to one block.
        slugs = sorted(set(link_mine.parse_related(fm_lines)))
        link_mine.write_page(path, fm_lines, body, slugs, "2026-11-17")
        out = path.read_text(encoding="utf-8")
        self.assertEqual(out.count("related:"), 1)
        self.assertIn('related:\n  - "alpha-one"\n  - "alpha-two"\n', out)
        self.assertNotIn("beta", out.split("---\n", 2)[1])

    def test_write_page_twice_is_byte_identical(self):
        path = make_page(PAGE_DUP)
        _, fm_lines, body = split(PAGE_DUP)
        rel = ["alpha-one", "alpha-two"]
        link_mine.write_page(path, fm_lines, body, rel, "2026-11-17")
        once = path.read_bytes()
        _, fm_lines2, body2 = split(once.decode("utf-8"))
        link_mine.write_page(path, fm_lines2, body2, rel, "2026-11-17")
        self.assertEqual(path.read_bytes(), once)

    def test_related_after_sources_not_duplicated(self):
        path = make_page(PAGE_RELATED_AFTER_SOURCES)
        _, fm_lines, body = split(PAGE_RELATED_AFTER_SOURCES)
        link_mine.write_page(path, fm_lines, body, ["beta-one"], "2026-11-17")
        out = path.read_text(encoding="utf-8")
        self.assertEqual(out.count("related:"), 1)

    def test_body_and_other_frontmatter_unchanged(self):
        path = make_page(PAGE_DUP)
        _, fm_lines, body = split(PAGE_DUP)
        link_mine.write_page(path, fm_lines, body,
                             ["alpha-one", "alpha-two"], "2026-11-17")
        out = path.read_text(encoding="utf-8")
        self.assertTrue(out.endswith("---\nBody line one.\nBody line two.\n"))
        self.assertIn('title: "Alpha"\n', out)
        self.assertIn('list_summary: "Alpha summary"\n', out)
        self.assertIn("sources:\n  - https://example.invalid/alpha\n", out)
        self.assertIn("updated: 2026-11-17\n", out)
        self.assertNotIn("updated: 2020-01-01\n", out)


class HardeningTests(_RootRestoringTest):
    def test_parse_related_strips_quoted_items(self):
        fm = ["related:", '  - "alpha-one"', "  - 'beta-two'"]
        self.assertEqual(link_mine.parse_related(fm),
                         ["alpha-one", "beta-two"])
        inline = ['related: ["alpha-one", "beta-two"]']
        self.assertEqual(link_mine.parse_related(inline),
                         ["alpha-one", "beta-two"])

    def test_parse_related_matches_link_check_on_comments_tabs_and_duplicates(self):
        import link_check
        cases = [
            ["related:", '  - "beta" # keep'],
            ["related:", "\t- beta"],
            ["related: [beta] # note"],
            ["related:", "  - alpha", "title: \"x\"", "related:", "  - beta"],
        ]
        for fm in cases:
            with self.subTest(fm=fm):
                self.assertEqual(link_mine.parse_related(fm),
                                 link_check.parse_related("\n".join(fm)))

    def test_write_page_removes_tab_indented_items_on_rewrite(self):
        text = '---\ntitle: "Alpha"\nrelated:\n\t- beta\n---\n\nBody.\n'
        path = make_page(text)
        _, fm_lines, body = split(text)
        link_mine.write_page(path, fm_lines, body, ["gamma"], "2026-11-17")
        out = path.read_text(encoding="utf-8")
        self.assertEqual(out.count("related:"), 1)
        self.assertNotIn("\t- beta", out)

    def test_single_quoted_scalars_are_normalised(self):
        fields, _, _ = link_mine.split_page(
            "---\ntype: 'entity'\ntitle: 'Alpha'\n---\n\nBody.\n"
        )
        self.assertEqual(fields["type"], "entity")
        self.assertEqual(fields["title"], "Alpha")

    def test_bom_frontmatter_is_parsed(self):
        fields, _, _ = link_mine.split_page(
            "\ufeff---\ntype: entity\ntitle: \"Alpha\"\n---\n\nBody.\n"
        )
        self.assertEqual(fields["type"], "entity")

    def test_scalar_drops_comments_and_keeps_embedded_quotes(self):
        fields, _, _ = link_mine.split_page(
            "---\ntype: 'entity' # a concept page\n"
            'title: \'He said "hello"\'\n---\n\nBody.\n'
        )
        self.assertEqual(fields["type"], "entity")
        self.assertEqual(fields["title"], 'He said "hello"')

    def test_frontmatter_without_final_newline_is_parsed(self):
        fields, _, body = link_mine.split_page(
            '---\ntitle: "X"\nrelated: [ghost]\n---')
        self.assertEqual(fields["title"], "X")
        self.assertEqual(body, "")

    def test_write_page_refuses_a_symlinked_parent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            outside_dir = root.parent / f"outside-{root.name}"
            outside_dir.mkdir()
            self.addCleanup(
                lambda: __import__("shutil").rmtree(outside_dir, ignore_errors=True))
            victim = outside_dir / "page.md"
            victim.write_text("do not touch", encoding="utf-8")
            linked = root / "linked"
            linked.symlink_to(outside_dir, target_is_directory=True)
            _, fm_lines, body = split(PAGE_DUP)
            saved = link_mine.ROOT
            link_mine.ROOT = root
            try:
                link_mine.write_page(linked / "page.md", fm_lines, body,
                                     ["x"], "2026-11-17")
            finally:
                link_mine.ROOT = saved
            self.assertEqual(victim.read_text(encoding="utf-8"), "do not touch")

    def test_write_page_refuses_a_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            outside = root / "outside.md"
            outside.write_text("do not touch", encoding="utf-8")
            link = root / "page.md"
            link.symlink_to(outside)
            # Target the temp dir so containment passes; an out-of-root
            # fixture returned early on containment and pinned nothing.
            link_mine.ROOT, link_mine.WIKI = root, root
            _, fm_lines, body = split(PAGE_DUP)
            link_mine.write_page(link, fm_lines, body, ["x"], "2026-11-17")
            self.assertEqual(outside.read_text(encoding="utf-8"),
                             "do not touch")

    def test_preflight_refuses_an_in_root_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            real = root / "real.md"
            real.write_text("do not touch", encoding="utf-8")
            link = root / "page.md"
            link.symlink_to(real)
            link_mine.ROOT, link_mine.WIKI = root, root
            with self.assertRaises(SystemExit) as caught:
                link_mine.preflight([link])
            self.assertIn("symlink", str(caught.exception))
            self.assertEqual(real.read_text(encoding="utf-8"),
                             "do not touch")

    def test_preflight_refuses_an_in_root_hardlink(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            victim = root / "victim.md"
            victim.write_text("do not touch", encoding="utf-8")
            page = root / "page.md"
            page.hardlink_to(victim)
            link_mine.ROOT, link_mine.WIKI = root, root
            with self.assertRaises(SystemExit) as caught:
                link_mine.preflight([page])
            self.assertIn("hardlinked", str(caught.exception))
            self.assertEqual(victim.read_text(encoding="utf-8"),
                             "do not touch")

    def test_write_page_refuses_an_in_root_hardlink(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            victim = root / "victim.md"
            victim.write_text("do not touch", encoding="utf-8")
            page = root / "page.md"
            page.hardlink_to(victim)
            link_mine.ROOT, link_mine.WIKI = root, root
            _, fm_lines, body = split(PAGE_DUP)
            with self.assertRaises(SystemExit) as caught:
                link_mine.write_page(page, fm_lines, body, ["x"], "2026-11-20")
            self.assertIn("hardlinked", str(caught.exception))
            self.assertEqual(victim.read_text(encoding="utf-8"),
                             "do not touch")

    def test_read_page_skips_invalid_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "bad.md"
            bad.write_bytes(b"\xff\xfe")
            self.assertIsNone(link_mine.read_page(bad))


class MainTests(unittest.TestCase):
    def setUp(self):
        import io
        import contextlib
        self._out = io.StringIO()
        self._cm = contextlib.redirect_stdout(self._out)
        self._cm.__enter__()
        self.addCleanup(self._cm.__exit__, None, None, None)
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.saved = (link_mine.ROOT, link_mine.WIKI, sys.argv)
        self.addCleanup(self._restore)
        link_mine.ROOT, link_mine.WIKI = self.root, self.root
        (self.root / "alpha.md").write_text(
            '---\ntype: entity\ntitle: "Alpha"\nrelated: [beta]\n---\n\nBody.\n',
            encoding="utf-8",
        )
        (self.root / "beta.md").write_text(
            '---\ntype: entity\ntitle: "Beta"\nrelated: []\n---\n\nBody.\n',
            encoding="utf-8",
        )

    def _restore(self):
        link_mine.ROOT, link_mine.WIKI, sys.argv = self.saved

    def test_dry_run_stats_reflect_preserved_author_related(self):
        sys.argv = ["link_mine", "--fill-only", "--dry-run", "--threshold", "100"]
        link_mine.main()
        out = self._out.getvalue()
        self.assertIn("avg 0.50 related/page", out)
        self.assertIn("1 pages with none", out)

    def test_bad_date_is_rejected(self):
        sys.argv = ["link_mine", "--date", "not-a-date"]
        with self.assertRaises(SystemExit) as caught:
            link_mine.main()
        self.assertEqual(caught.exception.code, 2)


class FieldPrefixTests(unittest.TestCase):
    def test_tab_indented_type_does_not_override(self):
        text = '---\ntitle: "X"\ntype: entity\n\ttype: concept\n---\n\nBody.\n'
        self.assertEqual(link_mine.split_page(text)[0]["type"], "entity")


class SweepFiveRegressionTests(unittest.TestCase):
    """Regressions for the fifth sweep's miner enumeration and write guards."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self.kb = self.base / "kb"
        (self.kb / "tools").mkdir(parents=True)
        for f in TOOLS_DIR.glob("*.py"):
            shutil.copy2(f, self.kb / "tools" / f.name)
        (self.kb / "wiki").mkdir()
        (self.kb / "index.md").write_text("# KB\n", encoding="utf-8")
        self.addCleanup(self._tmp.cleanup)

    def page(self, rel, text):
        path = self.kb / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run_tool(self, tool, *args, timeout=10):
        return subprocess.run(
            [sys.executable, "tools/" + tool, *args], cwd=self.kb,
            capture_output=True, text=True, timeout=timeout)

    @staticmethod
    def entity(title, summary):
        return (f'---\ntitle: "{title}"\ntype: entity\n'
                f'summary: "{summary}"\n---\nbody\n')

    def test_index_named_and_nested_entities_are_mined(self):
        self.page("wiki/normal.md", self.entity("Normal", "plain"))
        self.page("wiki/index-of-tools.md",
                  self.entity("Index of tools", "authored hub"))
        self.page("wiki/topics/sub.md", self.entity("Nested", "nested page"))
        out = self.run_tool("link_mine.py", "--dry-run").stdout
        self.assertIn("3 entity pages", out)

    def test_fifo_named_md_does_not_block_the_miner(self):
        if not hasattr(os, "mkfifo"):
            self.skipTest("mkfifo unavailable")
        self.page("wiki/a.md", self.entity("A", "plain"))
        os.mkfifo(self.kb / "wiki" / "fifo.md")
        result = self.run_tool("link_mine.py", "--dry-run", timeout=5)
        self.assertEqual(result.returncode, 0)

    def test_hardlinked_page_write_is_refused(self):
        original = self.entity("Old research", "CAN bus intrusion detection")
        victim = self.base / "outside-victim.md"
        victim.write_text(original, encoding="utf-8")
        (self.kb / "wiki" / "old.md").hardlink_to(victim)
        self.page("wiki/other.md",
                  self.entity("Other research", "CAN bus intrusion evaluation"))
        result = self.run_tool("link_mine.py", "--threshold", "0",
                               "--date", "2026-11-20")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("hardlinked", result.stderr)
        self.assertEqual(victim.read_text(encoding="utf-8"), original)

    def test_readonly_page_write_exits_cleanly(self):
        self.page("wiki/ro.md", self.entity("Ro", "CAN bus intrusion detection"))
        self.page("wiki/other.md", self.entity("Other", "CAN bus intrusion evaluation"))
        os.chmod(self.kb / "wiki" / "ro.md", 0o444)
        result = self.run_tool("link_mine.py", "--threshold", "0",
                               "--date", "2026-11-20")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot write", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


class SweepSixRegressionTests(unittest.TestCase):
    """Regressions for the sixth sweep's enumeration and atomicity bugs."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self.kb = self.base / "kb"
        (self.kb / "tools").mkdir(parents=True)
        for f in TOOLS_DIR.glob("*.py"):
            shutil.copy2(f, self.kb / "tools" / f.name)
        (self.kb / "wiki").mkdir()
        (self.kb / "index.md").write_text("# KB\n", encoding="utf-8")
        self.addCleanup(self._tmp.cleanup)

    def entity(self, rel, title):
        path = self.kb / "wiki" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f'---\ntitle: "{title}"\ntype: entity\n'
            'summary: "CAN bus intrusion detection"\n---\nbody\n',
            encoding="utf-8")
        return path

    def run_tool(self, *args):
        return subprocess.run(
            [sys.executable, "tools/link_mine.py", *args], cwd=self.kb,
            capture_output=True, text=True, timeout=15)

    def test_duplicate_stems_are_both_mined(self):
        root = self.entity("alpha.md", "Alpha")
        nested = self.entity("sub/alpha.md", "Nested Alpha")
        self.entity("beta.md", "Beta")
        result = self.run_tool("--threshold", "0", "--date", "2026-11-20")
        self.assertIn("3 entity pages", result.stdout)
        self.assertIn("related:", root.read_text(encoding="utf-8"))
        self.assertIn("related:", nested.read_text(encoding="utf-8"))

    def test_unsafe_target_refuses_before_any_page_is_written(self):
        first = self.entity("aaa.md", "Aaa")
        middle = self.entity("mmm.md", "Mmm")
        last = self.entity("zzz.md", "Zzz")
        victim = self.base / "outside-victim.md"
        victim.write_text(last.read_text(encoding="utf-8"), encoding="utf-8")
        last.unlink()
        last.hardlink_to(victim)
        result = self.run_tool("--threshold", "0", "--date", "2026-11-20")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("related:", first.read_text(encoding="utf-8"))
        self.assertNotIn("related:", middle.read_text(encoding="utf-8"))
        self.assertNotIn("related:", victim.read_text(encoding="utf-8"))

    def test_nested_concepts_are_used_for_reciprocation(self):
        alpha = self.entity("alpha.md", "Alpha")
        deep = self.kb / "wiki" / "concepts" / "sub" / "deep.md"
        deep.parent.mkdir(parents=True)
        deep.write_text(
            '---\ntitle: "Deep"\ntype: concept\nrelated: [alpha]\n---\nbody\n',
            encoding="utf-8")
        self.run_tool("--fill-only", "--reciprocate", "--threshold", "0",
                      "--date", "2026-11-20")
        self.assertIn('"deep"', alpha.read_text(encoding="utf-8"))


class SweepSevenRegressionTests(unittest.TestCase):
    """Regressions for the seventh sweep's scoring and reciprocity bugs."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self.kb = self.base / "kb"
        (self.kb / "tools").mkdir(parents=True)
        for f in TOOLS_DIR.glob("*.py"):
            shutil.copy2(f, self.kb / "tools" / f.name)
        (self.kb / "wiki" / "concepts").mkdir(parents=True)
        (self.kb / "index.md").write_text("# KB\n", encoding="utf-8")
        self.addCleanup(self._tmp.cleanup)

    def entity(self, rel, title, summary="s", related=None):
        path = self.kb / "wiki" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        rel_block = (f"related: [{', '.join(related)}]\n"
                     if related is not None else "")
        path.write_text(
            f'---\ntitle: "{title}"\ntype: entity\nsummary: "{summary}"\n'
            f'{rel_block}---\nbody\n', encoding="utf-8")
        return path

    def concept(self, rel, title, related=None):
        path = self.kb / "wiki" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        rel_block = (f"related: [{', '.join(related)}]\n"
                     if related is not None else "")
        path.write_text(
            f'---\ntitle: "{title}"\ntype: concept\n{rel_block}---\nbody\n',
            encoding="utf-8")
        return path

    def run_tool(self, *args):
        return subprocess.run(
            [sys.executable, "tools/link_mine.py", *args], cwd=self.kb,
            capture_output=True, text=True, timeout=15)

    def related_of(self, path):
        return link_mine.parse_related(link_mine.split_page(
            path.read_text(encoding="utf-8"))[1])

    def test_substring_title_mention_does_not_invent_a_link(self):
        alpha = self.entity("alpha.md", "Bus", "bus control research")
        self.entity("beta.md", "Rebus", "rebus puzzles")
        for i in range(15):
            self.entity(f"f{i}.md", f"Filler{i}", f"unique filler{i}")
        result = self.run_tool("--date", "2026-11-20")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("beta", self.related_of(alpha))

    def test_max_related_cap_keeps_every_pair_mutual(self):
        a = self.entity("a.md", "Aaa", "same shared theme")
        b = self.entity("b.md", "Bbb", "same shared theme")
        c = self.entity("c.md", "Ccc", "same shared theme")
        result = self.run_tool("--max-related", "1", "--threshold", "0",
                               "--date", "2026-11-20")
        self.assertEqual(result.returncode, 0, result.stderr)
        ra, rb, rc = (self.related_of(p) for p in (a, b, c))
        self.assertEqual(ra, ["b"])
        self.assertEqual(rb, ["a"])
        self.assertEqual(rc, [], "the capped-out page must not link one way")

    def test_reciprocate_counts_distinct_stems_only(self):
        a = self.entity("a.md", "Aaa", related=[])
        self.entity("sub1/x.md", "X one", related=["a"])
        self.entity("sub2/x.md", "X two", related=["a"])
        result = self.run_tool("--reciprocate", "--threshold", "100",
                               "--date", "2026-11-20")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 reciprocal adds", result.stdout)
        self.assertEqual(self.related_of(a), ["x"])

    def test_concept_outside_concepts_dir_is_reciprocated(self):
        cabana = self.entity("cabana.md", "Cabana", related=[])
        self.concept("probe.md", "Probe", related=["cabana"])
        result = self.run_tool("--fill-only", "--reciprocate",
                               "--threshold", "100", "--date", "2026-11-20")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("probe", self.related_of(cabana))


class SweepEightRegressionTests(SweepSevenRegressionTests):
    """Regressions for the eighth sweep's self-link and reciprocation bugs."""

    def test_duplicate_stems_never_produce_a_self_link(self):
        a = self.entity("alpha.md", "Alpha", "shared theme words")
        nested = self.entity("sub/alpha.md", "Nested Alpha",
                             "shared theme words")
        self.entity("beta.md", "Beta", "shared theme words")
        result = self.run_tool("--threshold", "0", "--date", "2026-11-20")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("alpha", self.related_of(a))
        self.assertNotIn("alpha", self.related_of(nested))
        self.assertIn("beta", self.related_of(a))

    def test_duplicate_stem_pair_does_not_crowd_out_real_links(self):
        a = self.entity("alpha.md", "Alpha", "shared theme words")
        self.entity("sub/alpha.md", "Nested Alpha", "shared theme words")
        b = self.entity("beta.md", "Beta", "different topic here")
        result = self.run_tool("--threshold", "0", "--max-related", "1",
                               "--date", "2026-11-20")
        self.assertEqual(result.returncode, 0, result.stderr)
        # The same-stem pair is skipped while scoring, so the one allowed
        # link goes to the real mutual pair instead of a filtered self-link.
        self.assertEqual(self.related_of(a), ["beta"])
        self.assertEqual(self.related_of(b), ["alpha"])

    def test_duplicate_concept_stems_all_contribute_backlinks(self):
        cabana = self.entity("cabana.md", "Cabana", "unique cabana")
        self.concept("concepts/shared-secrets.md", "Secrets",
                     related=["cabana"])
        self.concept("topics/shared-secrets.md", "Draft",
                     related=["busmaster"])
        result = self.run_tool("--fill-only", "--reciprocate",
                               "--threshold", "100", "--date", "2026-11-20")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("shared-secrets", self.related_of(cabana))

    def test_reciprocate_never_writes_a_self_link(self):
        entity = self.entity("alpha.md", "Alpha", "unique alpha theme")
        concept = self.kb / "wiki" / "concepts" / "alpha.md"
        concept.parent.mkdir(parents=True, exist_ok=True)
        concept.write_text(
            '---\ntitle: "Alpha concept"\ntype: concept\n'
            'related: [alpha]\n---\nbody\n', encoding="utf-8")
        result = self.run_tool("--fill-only", "--reciprocate",
                               "--threshold", "100", "--date", "2026-11-20")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("alpha", self.related_of(entity))

    def test_reciprocate_preserves_author_links_and_is_stable(self):
        source = self.entity("source.md", "Source", "zzz unique alpha",
                             related=["target"])
        target = self.entity("target.md", "Target", "qqq unique beta")
        first = self.run_tool("--reciprocate", "--date", "2026-11-20")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(self.related_of(source), ["target"])
        self.assertEqual(self.related_of(target), ["source"])
        before = (source.read_text(encoding="utf-8"),
                  target.read_text(encoding="utf-8"))
        second = self.run_tool("--reciprocate", "--date", "2026-11-20")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("changed 0 pages", second.stdout)
        self.assertEqual((source.read_text(encoding="utf-8"),
                          target.read_text(encoding="utf-8")), before)


class SweepNineRegressionTests(SweepEightRegressionTests):
    """Regressions for the ninth sweep's writer key-detection bug."""

    def test_space_before_colon_keys_are_rewritten_not_duplicated(self):
        a = self.kb / "wiki" / "a.md"
        a.write_text(
            '---\ntitle: "Alpha"\ntype: entity\nsummary: "unique alpha"\n'
            'related : [beta]\nupdated : 2020-01-01\n---\nBody.\n',
            encoding="utf-8")
        self.entity("c.md", "Charlie", "unique charlie", related=["a"])
        first = self.run_tool("--reciprocate", "--threshold", "100",
                              "--date", "2026-11-20")
        self.assertEqual(first.returncode, 0, first.stderr)
        _, fm_lines, _ = link_mine.split_page(a.read_text(encoding="utf-8"))
        self.assertEqual(len([l for l in fm_lines
                              if re.match(r"^related\s*:", l)]), 1)
        self.assertIn("updated: 2026-11-20", fm_lines)
        self.assertNotIn("updated :", fm_lines)
        # The single block replaces the old key in place, not appended after
        # it (the pre-scan that decides placement must see the spaced key too).
        self.assertLess(fm_lines.index("related:"),
                        fm_lines.index("updated: 2026-11-20"))
        self.assertEqual(link_mine.parse_related(fm_lines), ["beta", "c"])
        second = self.run_tool("--reciprocate", "--threshold", "100",
                               "--date", "2026-11-21")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("changed 0 pages", second.stdout)

    def test_spaced_related_key_is_replaced_before_list_summary(self):
        a = self.kb / "wiki" / "a.md"
        a.write_text(
            '---\ntitle: "Alpha"\ntype: entity\nsummary: "s"\n'
            'list_summary: "list text"\ntags: "between"\n'
            'related : [beta]\n---\nBody.\n',
            encoding="utf-8")
        self.entity("c.md", "Charlie", "unique charlie", related=["a"])
        result = self.run_tool("--reciprocate", "--threshold", "100",
                               "--date", "2026-11-20")
        self.assertEqual(result.returncode, 0, result.stderr)
        _, fm_lines, _ = link_mine.split_page(a.read_text(encoding="utf-8"))
        # The block replaces the spaced key in place (after `tags`), not
        # inserted right after list_summary as though no related key existed.
        self.assertGreater(fm_lines.index("related:"),
                           fm_lines.index('tags: "between"'))


class SweepTenRegressionTests(SweepNineRegressionTests):
    """Regressions for the tenth sweep's writer and fixpoint bugs."""

    def test_comments_in_related_block_are_consumed_when_replaced(self):
        saved = (link_mine.ROOT, link_mine.WIKI)
        self.addCleanup(lambda: setattr(link_mine, "ROOT", saved[0]))
        self.addCleanup(lambda: setattr(link_mine, "WIKI", saved[1]))
        text = ('---\ntitle: "Alpha"\ntype: entity\n'
                'related:\n  # hand-curated\n\n  - "ghost"\n'
                'updated: 2020-01-01\n---\nBody.\n')
        path = make_page(text)
        _, fm, body = split(text)
        link_mine.write_page(path, fm, body, ["beta"], "2026-11-20")
        out = path.read_text(encoding="utf-8")
        self.assertNotIn("hand-curated", out)
        self.assertNotIn("ghost", out)
        self.assertEqual(link_mine.parse_related(split(out)[1]), ["beta"])

    def test_block_scalar_list_summary_is_not_split_by_related_block(self):
        saved = (link_mine.ROOT, link_mine.WIKI)
        self.addCleanup(lambda: setattr(link_mine, "ROOT", saved[0]))
        self.addCleanup(lambda: setattr(link_mine, "WIKI", saved[1]))
        text = ('---\ntitle: "Alpha"\ntype: entity\n'
                'list_summary: |\n  line one\n  line two\n---\nBody.\n')
        path = make_page(text)
        _, fm, body = split(text)
        link_mine.write_page(path, fm, body, ["beta"], "2026-11-20")
        out = path.read_text(encoding="utf-8")
        lines = out.split("---\n")[1].splitlines()
        # Both scalar content lines must precede the new key, not be
        # orphaned into the related block as invalid YAML.
        self.assertLess(lines.index("  line two"), lines.index("related:"))
        self.assertEqual(lines.index("list_summary: |") + 3,
                         lines.index("related:"))
        _, fm2, body2 = split(out)
        link_mine.write_page(path, fm2, body2, ["beta"], "2026-11-21")
        self.assertEqual(out, path.read_text(encoding="utf-8"))

    def test_reciprocate_is_a_single_pass_fixpoint_with_authored_sets(self):
        a = self.entity("a.md", "Alpha Zephyr", "alpha zephyr widget",
                        related=["x"])
        b = self.entity("b.md", "Beta Zephyr", "beta zephyr widget",
                        related=[])
        first = self.run_tool("--reciprocate", "--threshold", "0",
                              "--date", "2026-11-20")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn("b", self.related_of(a))
        self.assertEqual(self.related_of(b), ["a"])
        second = self.run_tool("--reciprocate", "--threshold", "0",
                               "--date", "2026-11-21")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("changed 0 pages", second.stdout)

    def test_fill_only_stays_stable_after_self_link_is_stripped(self):
        a = self.entity("a.md", "Alpha Quartz", "alpha quartz widget",
                        related=["a"])
        b = self.entity("b.md", "Beta Quartz", "beta quartz widget",
                        related=[])
        first = self.run_tool("--fill-only", "--threshold", "0",
                              "--date", "2026-11-20")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(self.related_of(a), ["b"])
        self.assertEqual(self.related_of(b), ["a"])
        second = self.run_tool("--fill-only", "--threshold", "0",
                               "--date", "2026-11-21")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("changed 0 pages", second.stdout)


class SweepElevenRegressionTests(SweepTenRegressionTests):
    """Regressions for the eleventh sweep's writer and counter bugs."""

    def test_comment_before_next_key_is_preserved_on_replace(self):
        # A comment after the last item documents the NEXT key. Sweep 10's
        # block skip swallowed and deleted it, losing authored prose.
        text = ('---\ntitle: "Alpha"\ntype: entity\n'
                'related:\n  - "beta"\n'
                '# verified against the source on 2026-11-20\n'
                'sources:\n  - https://example.invalid/a\n---\nBody.\n')
        path = make_page(text)
        _, fm, body = split(text)
        link_mine.write_page(path, fm, body, ["gamma"], "2026-11-20")
        out = path.read_text(encoding="utf-8")
        self.assertIn("# verified against the source on 2026-11-20", out)
        self.assertEqual(link_mine.parse_related(split(out)[1]), ["gamma"])

    def test_block_scalar_related_is_replaced_wholly(self):
        # `related: |` is a scalar the shared parser reads as no links, but
        # the writer's key regex still matched it and left the scalar body
        # orphaned under the replacement list — invalid YAML.
        text = ('---\ntitle: "Alpha"\ntype: entity\n'
                'related: |\n  cangaroo\n  cannelloni\n---\nBody.\n')
        path = make_page(text)
        _, fm, body = split(text)
        link_mine.write_page(path, fm, body, ["beta"], "2026-11-20")
        out = path.read_text(encoding="utf-8")
        self.assertNotIn("cangaroo", out)
        self.assertNotIn("cannelloni", out)
        self.assertEqual(link_mine.parse_related(split(out)[1]), ["beta"])

    def test_reciprocate_does_not_count_a_self_filtered_add(self):
        self.entity("alpha.md", "Alpha")
        concepts = self.kb / "wiki" / "concepts"
        concepts.mkdir(exist_ok=True)
        (concepts / "alpha.md").write_text(
            '---\ntitle: "Alpha concept"\ntype: concept\n'
            'related: [alpha]\n---\nbody\n', encoding="utf-8")
        out = self.run_tool("--fill-only", "--reciprocate", "--threshold",
                            "100", "--date", "2026-11-20")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("changed 0 pages (0 previously unlinked, 0 reciprocal adds)",
                      out.stdout)


class SweepTwelveRegressionTests(SweepElevenRegressionTests):
    """Regressions for the twelfth sweep's writer and stat bugs."""

    def test_updated_trailing_comment_survives_rewrite(self):
        text = ('---\ntitle: "Alpha"\ntype: entity\n'
                'updated: 2020-01-01 # reviewed by Alice\n'
                'related: []\n---\nBody.\n')
        path = make_page(text)
        _, fm, body = split(text)
        link_mine.write_page(path, fm, body, ["beta"], "2026-11-20")
        out = path.read_text(encoding="utf-8")
        self.assertIn("updated: 2026-11-20 # reviewed by Alice", out)
        self.assertNotIn("2020-01-01", out)

    def test_self_link_only_pages_count_as_previously_unlinked(self):
        # A self-link is filtered at write time, so these pages have no
        # authored links; the stat must count them as filled nonetheless.
        self.entity("a.md", "Alpha", "alpha quartz", related=["a"])
        self.entity("b.md", "Beta", "beta quartz", related=["b"])
        self.entity("c.md", "Gamma", "gamma quartz", related=[])
        out = self.run_tool("--fill-only", "--threshold", "0",
                            "--date", "2026-11-20")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("3 previously unlinked", out.stdout)


class SweepThirteenRegressionTests(SweepTwelveRegressionTests):
    """Regressions for the thirteenth sweep's writer."""

    def test_multiline_flow_related_is_consumed_on_rewrite(self):
        text = ('---\ntitle: "Alpha"\ntype: entity\nsummary: "alpha quartz"\n'
                'related: [\n  alpha-one,\n  beta-two\n]\n'
                'updated: 2020-01-01\n---\nBody.\n')
        path = make_page(text)
        _, fm, body = split(text)
        link_mine.write_page(path, fm, body, ["gamma"], "2026-11-20")
        out = path.read_text(encoding="utf-8")
        self.assertIn('related:\n  - "gamma"', out)
        # The old flow items and its closing bracket must not be orphaned
        # under the new block key, which left the page as invalid YAML.
        self.assertNotIn("alpha-one", out)
        self.assertNotIn("beta-two", out)
        self.assertNotIn("\n]\n", out)


if __name__ == "__main__":
    unittest.main()
