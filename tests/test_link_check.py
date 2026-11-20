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

    def test_inline_related_ignores_brackets_in_the_comment(self):
        self.assertEqual(
            link_check.parse_related("related: [alpha, beta] # see [spec]\n"),
            ["alpha", "beta"],
        )
        self.assertEqual(
            link_check.parse_related("related: [] # keeps [brackets]\n"), [])

    def test_frontmatter_without_final_newline_is_parsed(self):
        fm, body = link_check.split_frontmatter('---\nrelated: [alpha]\n---')
        self.assertEqual(link_check.parse_related(fm), ["alpha"])
        self.assertEqual(body, "")

    def test_angle_bracket_external_and_anchor_targets_are_not_broken(self):
        write(self.root, "wiki/brackets.md",
              "[ext](<https://example.com/x>) [kb](<kb://other/p>) "
              "[anchor](<#section>).\n")
        write(self.root, "index.md",
              "# KB\n\n- [Alpha](wiki/alpha.md)\n- [B](wiki/brackets.md)\n")
        report = link_check.check(self.root)
        self.assertEqual(report["broken_links"], [])
        self.assertTrue(link_check.is_ignored("<https://example.com/x>"))
        self.assertTrue(link_check.is_ignored("<kb://other/p>"))
        self.assertTrue(link_check.is_ignored("<#section>"))

    def test_block_related_items_with_trailing_comments_are_parsed(self):
        self.assertEqual(
            link_check.parse_related(
                "related:\n  - ghost # why\n  - phantom # why\n"
            ),
            ["ghost", "phantom"],
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

    def test_existing_file_outside_root_is_reported_broken(self):
        # A non-existent target is broken for the wrong reason (is_file());
        # this one really exists, so only the containment guard catches it.
        outside = self.root.parent / f"outside-{self.root.name}.md"
        outside.write_text("# Outside\n", encoding="utf-8")
        self.addCleanup(outside.unlink)
        write(self.root, "wiki/traveller.md",
              f"See [x](../../{outside.name}).\n")
        write(self.root, "index.md",
              "# KB\n\n- [Alpha](wiki/alpha.md)\n- [Sub](wiki/index-sub.md)\n"
              "- [T](wiki/traveller.md)\n")
        report = link_check.check(self.root)
        self.assertEqual(report["counts"]["broken_links"], 1)
        self.assertEqual(report["broken_links"][0]["source"], "wiki/traveller.md")

    def test_bad_root_fails_instead_of_passing_empty(self):
        with self.assertRaises(ValueError):
            link_check.check(self.root / "not-a-dir")
        self.assertEqual(
            link_check.main(["--root", str(self.root / "not-a-dir")]), 2
        )

    def test_directory_without_index_md_is_rejected(self):
        # A dir with wiki/*.md but no L1 index.md is not a valid KB root.
        (self.root / "index.md").unlink()
        (self.root / "wiki").mkdir(exist_ok=True)
        (self.root / "wiki" / "orphan.md").write_text(
            "---\nrelated: []\n---\n\nBody.\n", encoding="utf-8"
        )
        with self.assertRaises(ValueError):
            link_check.check(self.root)
        self.assertEqual(link_check.main(["--root", str(self.root)]), 2)


class FilesystemGuardTests(unittest.TestCase):
    """Regressions for directory/symlink/NUL handling in the link checker."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        make_kb(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_symlinked_root_index_is_rejected_not_scanned_as_empty(self):
        real = self.root / "real-index.md"
        real.write_text((self.root / "index.md").read_text(encoding="utf-8"),
                        encoding="utf-8")
        (self.root / "index.md").unlink()
        (self.root / "index.md").symlink_to(real)
        with self.assertRaises(ValueError) as caught:
            link_check.check(self.root)
        self.assertIn("index.md", str(caught.exception))

    def test_directory_named_md_is_not_a_page(self):
        (self.root / "wiki" / "directory_page.md").mkdir()
        write(self.root, "wiki/alpha.md",
              "---\nrelated: [directory_page]\n---\n\nBody.\n")
        report = link_check.check(self.root)
        slugs = [e["slug"] for e in report["unresolved_related"]]
        self.assertIn("directory_page", slugs)
        self.assertNotIn("wiki/directory_page.md", report["unreachable"])

    def test_symlinked_leaf_is_not_audited(self):
        outside = self.root.parent / f"outside-{self.root.name}"
        outside.mkdir()
        self.addCleanup(
            lambda: __import__("shutil").rmtree(outside, ignore_errors=True))
        secret = outside / "outside.md"
        secret.write_text(
            "---\nrelated: [ghost]\n---\n\n[broken](missing.md)\n",
            encoding="utf-8",
        )
        (self.root / "wiki" / "outside.md").symlink_to(secret)
        report = link_check.check(self.root)
        self.assertFalse(any("outside.md" in e["source"]
                             for e in report["broken_links"]))
        self.assertNotIn("ghost", [e["slug"]
                                   for e in report["unresolved_related"]])

    def test_nul_escape_is_a_broken_link_not_a_crash(self):
        write(self.root, "wiki/nul.md", "See [x](wiki/null%00.md).\n")
        write(self.root, "index.md",
              "# KB\n\n- [Alpha](wiki/alpha.md)\n- [Sub](wiki/index-sub.md)\n"
              "- [Nul](wiki/nul.md)\n")
        report = link_check.check(self.root)  # must not raise
        self.assertEqual(report["counts"]["broken_links"], 1)
        self.assertEqual(report["broken_links"][0]["source"], "wiki/nul.md")


if __name__ == "__main__":
    unittest.main()
