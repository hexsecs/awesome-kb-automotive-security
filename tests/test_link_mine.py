#!/usr/bin/env python3
"""Regression tests for tools/link_mine.py write_page(). Stdlib only."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools" / "link_mine.py"
spec = importlib.util.spec_from_file_location("link_mine", TOOLS)
link_mine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(link_mine)


def make_page(text: str) -> Path:
    d = Path(tempfile.mkdtemp())
    p = d / "alpha.md"
    p.write_text(text, encoding="utf-8")
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


class WritePageTests(unittest.TestCase):
    def test_duplicate_related_blocks_collapse_to_first(self):
        path = make_page(PAGE_DUP)
        _, fm_lines, body = split(PAGE_DUP)
        # Repair scenario: caller passes the first block's slugs
        # (what parse_related returns), keeping first content/order.
        first = link_mine.parse_related(fm_lines)
        link_mine.write_page(path, fm_lines, body, first, "2026-11-17")
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


class HardeningTests(unittest.TestCase):
    def test_parse_related_strips_quoted_items(self):
        fm = ["related:", '  - "alpha-one"', "  - 'beta-two'"]
        self.assertEqual(link_mine.parse_related(fm),
                         ["alpha-one", "beta-two"])
        inline = ['related: ["alpha-one", "beta-two"]']
        self.assertEqual(link_mine.parse_related(inline),
                         ["alpha-one", "beta-two"])

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


if __name__ == "__main__":
    unittest.main()
