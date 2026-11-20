#!/usr/bin/env python3
"""Regression tests for tools/concept_scan.py hardening. Stdlib only."""

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools" / "concept_scan.py"
spec = importlib.util.spec_from_file_location("concept_scan", TOOLS)
concept_scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(concept_scan)


def run_scan(root: Path) -> str:
    """Run main() against a temp KB, returning its stdout."""
    saved = (concept_scan.ROOT, concept_scan.WIKI, sys.argv)
    concept_scan.ROOT, concept_scan.WIKI = root, root
    sys.argv = ["concept_scan", "--min-pages", "1", "--top", "1"]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            concept_scan.main()
    finally:
        concept_scan.ROOT, concept_scan.WIKI, sys.argv = saved
    return buf.getvalue()


class ScanningTests(unittest.TestCase):
    def test_bom_page_is_scanned(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "alpha.md").write_text(
                '\ufeff---\ntype: entity\ntitle: "Alpha"\n'
                'summary: "CAN bus tool."\n---\n\nBody.\n',
                encoding="utf-8",
            )
            self.assertIn("1 entity pages", run_scan(root))

    def test_single_quoted_type_is_scanned(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "alpha.md").write_text(
                "---\ntype: 'entity'\ntitle: 'Alpha'\n"
                "summary: 'CAN bus tool.'\n---\n\nBody.\n",
                encoding="utf-8",
            )
            self.assertIn("1 entity pages", run_scan(root))

    def test_frontmatter_without_final_newline_is_scanned(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "alpha.md").write_text(
                '---\ntype: entity\ntitle: "Alpha"\nsummary: "CAN tool."\n---',
                encoding="utf-8",
            )
            self.assertIn("1 entity pages", run_scan(root))

    def test_symlinked_wiki_directory_is_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            outside_dir = root.parent / f"outside-{root.name}"
            outside_dir.mkdir()
            self.addCleanup(
                lambda: __import__("shutil").rmtree(outside_dir, ignore_errors=True))
            (outside_dir / "alpha.md").write_text(
                '---\ntype: entity\ntitle: "Alpha"\n---\n\nBody.\n',
                encoding="utf-8",
            )
            wiki = root / "wiki"
            wiki.symlink_to(outside_dir, target_is_directory=True)
            saved = (concept_scan.ROOT, concept_scan.WIKI)
            concept_scan.ROOT, concept_scan.WIKI = root, wiki
            try:
                sys.argv = ["concept_scan", "--min-pages", "1", "--top", "1"]
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    concept_scan.main()
            finally:
                concept_scan.ROOT, concept_scan.WIKI = saved
            self.assertIn("0 entity pages", buf.getvalue())

    def test_symlinked_page_is_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            outside = root.parent / "outside-concept.md"
            outside.write_text(
                '---\ntype: entity\ntitle: "Outside"\n---\n\nBody.\n',
                encoding="utf-8",
            )
            self.addCleanup(outside.unlink, missing_ok=True)
            (root / "alpha.md").symlink_to(outside)
            self.assertIn("0 entity pages", run_scan(root))


class HardeningTests(unittest.TestCase):
    def test_generic_filter_has_no_whitespace(self):
        # Word tokens are produced by TOKEN_RE and can never contain spaces;
        # an entry with one is unreachable dead weight.
        bad = [word for word in concept_scan.GENERIC if not word.isalnum()
               and "-" not in word]
        self.assertEqual(bad, [], f"malformed GENERIC entries: {bad}")

    def test_read_page_skips_invalid_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "bad.md"
            bad.write_bytes(b"\xff\xfe")
            self.assertIsNone(concept_scan.read_page(bad))

    def test_fields_of_handles_bom_and_single_quotes(self):
        text = ("\ufeff---\ntype: 'entity'\ntitle: 'Alpha'\n"
                "summary: 'CAN tool.'\n---\n\nBody.\n")
        fields = concept_scan.fields_of(text)
        self.assertEqual(fields["type"], "entity")
        self.assertEqual(fields["title"], "Alpha")

    def test_fields_of_drops_comments_and_keeps_embedded_quotes(self):
        text = ('---\ntype: "entity" # a page\n'
                'title: \'He said "hello"\'\n---\n\nBody.\n')
        fields = concept_scan.fields_of(text)
        self.assertEqual(fields["type"], "entity")
        self.assertEqual(fields["title"], 'He said "hello"')


class FilesystemGuardTests(unittest.TestCase):
    def test_tab_indented_type_does_not_override(self):
        text = '---\ntype: entity\n\ttype: concept\n---\n\nBody.\n'
        self.assertEqual(concept_scan.fields_of(text)["type"], "entity")

    def test_symlinked_concepts_dir_is_not_scanned(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for i in range(10):
                summary = ("quintessential zephyr" if i < 2
                           else f"unique filler{i}")
                (root / f"p{i}.md").write_text(
                    f'---\ntype: entity\ntitle: "P"\n'
                    f'summary: "{summary}"\n---\n\nBody.\n',
                    encoding="utf-8",
                )
            outside = root.parent / f"outside-{root.name}"
            outside.mkdir()
            self.addCleanup(
                lambda: __import__("shutil").rmtree(outside, ignore_errors=True))
            (outside / "quintessential-zephyr.md").write_text(
                '---\ntitle: "Outside"\n---\n', encoding="utf-8")
            (root / "concepts").symlink_to(outside, target_is_directory=True)
            out = run_scan(root)
            # The outside file's stem must not be treated as an existing
            # concept and suppress the real corpus candidate.
            self.assertIn("quintessential zephyr", out)


if __name__ == "__main__":
    unittest.main()
