#!/usr/bin/env python3
"""Regression tests for tools/link_mine.py write_page(). Stdlib only."""

import importlib.util
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


if __name__ == "__main__":
    unittest.main()
