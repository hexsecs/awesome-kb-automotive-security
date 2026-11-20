#!/usr/bin/env python3
"""Stdlib unittest suite for tools/link_check.py using synthetic temp-dir fixtures."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import link_check  # noqa: E402


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_kb(root: Path) -> None:
    write(
        root,
        "index.md",
        "# KB\n\n- [Alpha](wiki/alpha.md)\n- [Sub](wiki/index-sub.md)\n",
    )
    write(
        root,
        "wiki/index-sub.md",
        "# Sub\n\n- [Beta](beta.md)\n",
    )
    write(
        root,
        "wiki/alpha.md",
        "---\nrelated:\n  - beta\n---\n\nSee [Beta](beta.md#section) and "
        "[ext](https://example.com/spec.md) and [kb](kb://other/page.md).\n",
    )
    write(
        root,
        "wiki/beta.md",
        "---\nrelated: [alpha]\n---\n\nBody links to [Alpha](alpha.md).\n",
    )


class LinkCheckTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        make_kb(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def report(self):
        return link_check.check(self.root)

    def test_valid_link_and_clean_kb(self):
        report = self.report()
        self.assertEqual(report["counts"]["broken_links"], 0)
        self.assertEqual(report["counts"]["unresolved_related"], 0)
        self.assertEqual(report["counts"]["unreachable"], 0)
        self.assertTrue(report["ok"])

    def test_dead_link_reported(self):
        write(self.root, "wiki/gamma.md", "See [Nope](does-not-exist.md).\n")
        write(self.root, "index.md",
              "# KB\n\n- [Alpha](wiki/alpha.md)\n- [Sub](wiki/index-sub.md)\n- [Gamma](wiki/gamma.md)\n")
        report = self.report()
        self.assertEqual(report["counts"]["broken_links"], 1)
        self.assertEqual(report["broken_links"][0]["source"], "wiki/gamma.md")
        self.assertEqual(report["broken_links"][0]["target"], "does-not-exist.md")

    def test_external_md_url_ignored(self):
        write(self.root, "wiki/delta.md",
              "See [ext](https://example.com/missing.md) and [http](http://example.com/x.md).\n")
        write(self.root, "index.md",
              "# KB\n\n- [Alpha](wiki/alpha.md)\n- [Sub](wiki/index-sub.md)\n- [Delta](wiki/delta.md)\n")
        report = self.report()
        self.assertEqual(report["counts"]["broken_links"], 0)

    def test_unresolved_related_slug_reported(self):
        write(self.root, "wiki/epsilon.md",
              "---\nrelated:\n  - no-such-slug-here\n---\n\nBody.\n")
        write(self.root, "index.md",
              "# KB\n\n- [Alpha](wiki/alpha.md)\n- [Sub](wiki/index-sub.md)\n- [Epsilon](wiki/epsilon.md)\n")
        report = self.report()
        slugs = [e["slug"] for e in report["unresolved_related"]]
        self.assertIn("no-such-slug-here", slugs)

    def test_inline_related_form_resolved(self):
        report = self.report()
        self.assertEqual(report["counts"]["unresolved_related"], 0)

    def test_unreachable_page_reported(self):
        write(self.root, "wiki/orphan.md", "No inbound links.\n")
        report = self.report()
        self.assertIn("wiki/orphan.md", report["unreachable"])

    def test_cli_exit_codes_and_json(self):
        write(self.root, "wiki/orphan.md", "No inbound links.\n")
        rc = link_check.main(["--root", str(self.root), "--json"])
        self.assertEqual(rc, 1)
        rc_ok = link_check.main(["--root", str(self.root)])
        self.assertEqual(rc_ok, 1)

    def test_cli_clean_exit_zero(self):
        rc = link_check.main(["--root", str(self.root)])
        self.assertEqual(rc, 0)


class ParserAndBoundaryTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        make_kb(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_unindented_related_block_is_parsed(self):
        self.assertEqual(
            link_check.parse_related("related:\n- alpha\n- beta\n"),
            ["alpha", "beta"],
        )

    def test_inline_related_with_trailing_comment_is_parsed(self):
        self.assertEqual(
            link_check.parse_related("related: [alpha, beta] # note\n"),
            ["alpha", "beta"],
        )

    def test_bom_frontmatter_is_parsed(self):
        fm, _ = link_check.split_frontmatter(
            "\ufeff---\nrelated: [alpha]\n---\n\nBody.\n"
        )
        self.assertEqual(link_check.parse_related(fm), ["alpha"])

    def test_markdown_link_forms_are_recognised(self):
        text = ("[x](<my file.md>) [y](foo(bar).md) "
                "[z](page.md 'title') [a [b]](page.md)")
        self.assertEqual(
            [m.group(1) for m in link_check.LINK_RE.finditer(text)],
            ["<my file.md>", "foo(bar).md", "page.md", "page.md"],
        )

    def test_angle_bracket_target_resolves_without_brackets(self):
        with tempfile.TemporaryDirectory() as d:
            r = Path(d)
            (r / "wiki").mkdir()
            target = link_check.resolve_link(
                r / "wiki/a.md", "<my file.md>", r
            )
            self.assertEqual(target, (r / "wiki/my file.md").resolve())

    def test_link_outside_root_is_reported_broken(self):
        write(self.root, "wiki/traveller.md", "See [x](../../../../etc/passwd).\n")
        write(self.root, "index.md",
              "# KB\n\n- [Alpha](wiki/alpha.md)\n- [T](wiki/traveller.md)\n")
        report = link_check.check(self.root)
        self.assertEqual(report["counts"]["broken_links"], 1)
        self.assertEqual(report["broken_links"][0]["source"], "wiki/traveller.md")

    def test_bad_root_fails_instead_of_passing_empty(self):
        with self.assertRaises(ValueError):
            link_check.check(self.root / "not-a-dir")
        self.assertEqual(
            link_check.main(["--root", str(self.root / "not-a-dir")]), 2
        )


if __name__ == "__main__":
    unittest.main()
