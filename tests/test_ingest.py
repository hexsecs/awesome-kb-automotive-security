#!/usr/bin/env python3
"""Stdlib unittest suite for the ingest triage classifier."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import ingest  # noqa: E402


class TriageKindTests(unittest.TestCase):
    def test_deepen_candidate(self) -> None:
        kind, note = ingest.triage_kind({"depth_note": "deepen candidate — full paper PDF linked"})
        self.assertEqual(kind, "deepen")
        self.assertIn("full paper PDF", note)

    def test_brief_by_design(self) -> None:
        kind, note = ingest.triage_kind({"depth_note": "brief by design — book, no open primary text"})
        self.assertEqual(kind, "by-design")
        self.assertIn("book", note)

    def test_missing_note_is_untriaged(self) -> None:
        self.assertEqual(ingest.triage_kind({}), ("untriaged", ""))
        self.assertEqual(ingest.triage_kind({"depth_note": ""}), ("untriaged", ""))

    def test_unrecognised_note_is_untriaged_but_preserved(self) -> None:
        kind, note = ingest.triage_kind({"depth_note": "something else"})
        self.assertEqual(kind, "untriaged")
        self.assertEqual(note, "something else")


class RelatedCountTests(unittest.TestCase):
    def test_unindented_related_block_is_counted(self):
        text = '---\ntitle: "X"\nrelated:\n- alpha\n- beta\n---\n\nBody.\n'
        self.assertEqual(ingest.related_count(text), 2)

    def test_related_with_inline_comment_is_counted(self):
        text = '---\ntitle: "X"\nrelated: [alpha, beta] # note\n---\n\nBody.\n'
        self.assertEqual(ingest.related_count(text), 2)


class IngestParsingTests(unittest.TestCase):
    def test_parenthesized_url_entry_is_parsed(self):
        with tempfile.TemporaryDirectory() as d:
            readme = Path(d) / "README.md"
            readme.write_text(
                "## Papers\n\n* [Foo](https://en.wikipedia.org/wiki/A_(B)_attack)"
                " - a paper\n",
                encoding="utf-8",
            )
            entries = ingest.parse_list(readme)
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["url"],
                             "https://en.wikipedia.org/wiki/A_(B)_attack")

    def test_long_unbroken_summary_is_not_collapsed(self):
        summary = ingest.short_summary("a " + "x" * 200)
        self.assertEqual(len(summary), 160)
        self.assertTrue(summary.startswith("a " + "x" * 10))

    def test_http_and_https_normalise_to_the_same_identity(self):
        self.assertEqual(ingest.normalise("HTTP://Example.com/x"),
                         "example.com/x")

    def test_single_quoted_note_survives_the_scalar_parser(self):
        fields, _ = ingest.split_page(
            '---\ntitle: "X"\ndepth_note: \'brief by design — book\'\n'
            '---\n\nBody.\n'
        )
        self.assertEqual(ingest.triage_kind(fields)[0], "by-design")

    def test_tab_indented_extra_key_is_preserved(self):
        text = ('---\ntitle: "X"\nurl: "https://example.com/x"\n'
                '\tobj: "keep me"\n---\n\nBody.\n')
        fields, _ = ingest.split_page(text)
        self.assertNotIn("obj", fields)
        self.assertTrue(any("\tobj:" in line
                            for block in ingest.extra_blocks(text)
                            for line in block))


class IngestMainTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self.source = self.base / "source"
        self.kb = self.base / "kb"
        self.wiki = self.kb / "wiki"
        (self.wiki / "concepts").mkdir(parents=True)
        self.source.mkdir()
        self._old_root, self._old_wiki = ingest.ROOT, ingest.WIKI
        ingest.ROOT, ingest.WIKI = self.kb, self.wiki
        self.write_list(
            "## CAN Bus Analysis\n\n* [A](https://example.com/a) - a\n\n"
            "## CAN-Bus Analysis\n\n* [B](https://example.com/b) - b\n"
        )

    def tearDown(self):
        ingest.ROOT, ingest.WIKI = self._old_root, self._old_wiki
        self._tmp.cleanup()

    def write_list(self, body: str) -> None:
        (self.source / "README.md").write_text(body, encoding="utf-8")
        subprocess.run(["git", "-C", str(self.source), "init", "-q"], check=True)
        subprocess.run(
            ["git", "-C", str(self.source), "add", "README.md"], check=True
        )
        subprocess.run(
            ["git", "-C", str(self.source), "-c", "user.email=clyde@example.com",
             "-c", "user.name=Clyde", "commit", "-q", "-m", "list"],
            check=True,
        )
        self.ingest()

    def ingest(self):
        return ingest.main(["--source", str(self.source)])

    def test_section_slug_collision_gets_distinct_indexes(self):
        index = (self.kb / "index.md").read_text(encoding="utf-8")
        self.assertIn("wiki/index-can-bus-analysis.md", index)
        self.assertIn("wiki/index-can-bus-analysis-2.md", index)
        self.assertTrue((self.wiki / "index-can-bus-analysis.md").is_file())
        self.assertTrue((self.wiki / "index-can-bus-analysis-2.md").is_file())

    def test_stale_category_index_is_removed(self):
        self.write_list(
            "## CAN Bus Tools\n\n* [A](https://example.com/a) - a\n\n"
            "* [B](https://example.com/b) - b\n"
        )
        self.assertFalse((self.wiki / "index-can-bus-analysis.md").exists())
        self.assertFalse((self.wiki / "index-can-bus-analysis-2.md").exists())
        self.assertTrue((self.wiki / "index-can-bus-tools.md").exists())

    def test_duplicate_url_fails_loudly(self):
        second = self.wiki / "b.md"
        head = ('---\nuid: 01aa0000-0000-7000-8000-000000000000\n'
                'title: "B"\nurl: "https://example.com/a"\n---\n\nBody.\n')
        for page in (second,):
            page.write_text(head, encoding="utf-8")
        with self.assertRaises(SystemExit) as caught:
            self.ingest()
        self.assertIn("duplicate URL", str(caught.exception))

    def test_unreadable_page_fails_loudly(self):
        (self.wiki / "broken.md").write_bytes(b"---\ntitle: \xff\xfe\n---\n")
        with self.assertRaises(SystemExit) as caught:
            self.ingest()
        self.assertIn("cannot read", str(caught.exception))

    def test_non_git_source_fails_loudly(self):
        plain = self.base / "plain"
        plain.mkdir()
        (plain / "README.md").write_text("## X\n\n* [A](https://example.com/a) - a\n",
                                         encoding="utf-8")
        with self.assertRaises(SystemExit) as caught:
            ingest.main(["--source", str(plain)])
        self.assertIn("not a usable git checkout", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
