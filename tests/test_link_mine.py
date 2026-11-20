#!/usr/bin/env python3
"""Regression tests for tools/link_mine.py write_page(). Stdlib only."""

import importlib.util
import os
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
            _, fm_lines, body = split(PAGE_DUP)
            link_mine.write_page(link, fm_lines, body, ["x"], "2026-11-17")
            self.assertEqual(outside.read_text(encoding="utf-8"),
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


if __name__ == "__main__":
    unittest.main()
