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

    def commit_list(self, body: str) -> None:
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

    def write_list(self, body: str) -> None:
        self.commit_list(body)
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

    def test_duplicate_url_in_source_list_fails_loudly(self):
        self.commit_list(
            "## CAN Bus Analysis\n\n"
            "* [A](https://example.com/a) - a\n"
            "* [B](https://example.com/a) - b\n"
        )
        with self.assertRaises(SystemExit) as caught:
            self.ingest()
        self.assertIn("duplicate URL in source list", str(caught.exception))

    def test_bom_page_is_updated_not_recreated(self):
        page = self.wiki / "a.md"
        page.write_text(
            "\ufeff---\nuid: \"01aa0000-0000-7000-8000-000000000000\"\n"
            "title: \"A\"\nurl: \"https://example.com/a\"\n"
            "category: \"CAN Bus Analysis\"\nstatus: \"active\"\n"
            "created: \"2026-01-01\"\nlast_checked: \"2026-01-01\"\n"
            "---\n\nBody.\n",
            encoding="utf-8",
        )
        self.write_list(
            "## CAN Bus Analysis\n\n* [A](https://example.com/a) - a changed\n"
        )
        self.assertFalse((self.wiki / "a-2.md").exists())
        text = page.read_text(encoding="utf-8")
        self.assertNotIn("\ufeff", text)
        self.assertIn("01aa0000-0000-7000-8000-000000000000", text)
        self.assertIn('status: "active"', text)
        self.assertIn("a changed", text)

    def test_new_slug_cannot_collide_with_a_concept_stem(self):
        (self.wiki / "concepts" / "alpha.md").write_text(
            '---\ntitle: "Alpha concept"\ntype: concept\n---\n\nBody.\n',
            encoding="utf-8",
        )
        self.write_list("## CAN Bus Analysis\n\n* [Alpha](https://example.com/new-alpha) - a\n")
        self.assertTrue((self.wiki / "alpha-2.md").is_file())
        self.assertFalse((self.wiki / "alpha.md").exists())

    def test_research_papers_move_sets_published(self):
        self.write_list("## Research Papers\n\n* [A](https://example.com/a) - a\n")
        text = (self.wiki / "a.md").read_text(encoding="utf-8")
        self.assertIn('status: "published"', text)

    def test_entity_slug_cannot_take_a_hub_index_stem(self):
        self.write_list(
            "## CAN Bus Analysis\n\n"
            "* [Index Concept Map](https://example.com/hub) - a hub-named page\n"
        )
        self.assertTrue((self.wiki / "index-concept-map-2.md").is_file())
        hub = (self.wiki / "index-concept-map.md").read_text(encoding="utf-8")
        self.assertTrue(hub.startswith("# Concept map"))

    def test_category_slug_cannot_overwrite_a_hub_index(self):
        self.write_list("## Concept map\n\n* [Alpha](https://example.com/alpha) - a\n")
        hub = (self.wiki / "index-concept-map.md").read_text(encoding="utf-8")
        self.assertTrue(hub.startswith("# Concept map"))
        self.assertTrue((self.wiki / "index-concept-map-2.md").is_file())

    def test_refuses_to_invent_identity_fields(self):
        (self.wiki / "a.md").write_text(
            '---\ntitle: "A"\nurl: "https://example.com/a"\n---\n\nBody.\n',
            encoding="utf-8",
        )
        before = (self.wiki / "a.md").read_bytes()
        with self.assertRaises(SystemExit) as caught:
            self.ingest()
        self.assertIn("refusing to invent", str(caught.exception))
        self.assertEqual((self.wiki / "a.md").read_bytes(), before)

    def test_url_move_reuses_dashed_slug(self):
        # Only the -2 page exists, carrying the old URL: a new URL for the
        # same title must update it in place, not mint a fresh a.md.
        (self.wiki / "a.md").unlink()
        (self.wiki / "b.md").unlink()
        (self.wiki / "a-2.md").write_text(
            '---\nuid: "01aa0000-0000-7000-8000-000000000000"\n'
            'title: "A"\nurl: "https://example.com/old"\n'
            'category: "CAN Bus Analysis"\nstatus: "active"\n'
            'created: "2026-01-01"\nlast_checked: "2026-01-01"\n'
            '---\n\nBody.\n',
            encoding="utf-8",
        )
        self.write_list("## CAN Bus Analysis\n\n* [A](https://example.com/new) - a\n")
        self.assertFalse((self.wiki / "a.md").exists())
        self.assertIn("https://example.com/new",
                      (self.wiki / "a-2.md").read_text(encoding="utf-8"))

    def test_tombstone_rewrite_is_scoped_to_frontmatter(self):
        (self.wiki / "gone.md").write_text(
            '---\nuid: "01aa0000-0000-7000-8000-000000000001"\n'
            'title: "Gone"\nurl: "https://example.com/gone"\n'
            'status: "active"\nsummary: "Delisted from the source list"\n'
            'created: "2026-01-01"\nlast_checked: "2026-01-01"\n'
            '---\n\nBody says status: draft here.\n',
            encoding="utf-8",
        )
        self.write_list("## CAN Bus Analysis\n\n* [A](https://example.com/a) - a\n")
        text = (self.wiki / "gone.md").read_text(encoding="utf-8")
        head, body = text.split("\n---\n", 1)
        self.assertTrue(any(
            line.strip() in ("status: archived", 'status: "archived"')
            for line in head.splitlines()
        ))
        self.assertIn("> Delisted from the source list", body)
        self.assertIn("Body says status: draft here.", body)


class ListParsingTests(unittest.TestCase):
    def test_nested_parentheses_in_url(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "README.md"
            p.write_text(
                "## Papers\n\n"
                "* [Single](https://en.wikipedia.org/wiki/Foo_(bar)) - a\n"
                "* [Nested](https://en.wikipedia.org/wiki/Foo_(bar_(baz))) - b\n"
                "* [Comma](https://en.wikipedia.org/wiki/Foo_(bar,baz)) - c\n",
                encoding="utf-8",
            )
            urls = [e["url"] for e in ingest.parse_list(p)]
        self.assertEqual(urls, [
            "https://en.wikipedia.org/wiki/Foo_(bar)",
            "https://en.wikipedia.org/wiki/Foo_(bar_(baz))",
            "https://en.wikipedia.org/wiki/Foo_(bar,baz)",
        ])

    def test_bom_page_fields_are_parsed(self):
        text = ('\ufeff---\nurl: "https://example.com/a"\n'
                'uid: "01aa"\n---\n\nBody.\n')
        fields, _ = ingest.split_page(text)
        self.assertEqual(fields["url"], "https://example.com/a")
        self.assertEqual(fields["uid"], "01aa")


class NeedsAttentionTests(unittest.TestCase):
    def test_unrecognised_note_is_visible_in_the_queue(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            page = root / "brief.md"
            page.write_text('---\ntitle: "Brief"\n---\n\nBody.\n',
                            encoding="utf-8")
            old_root, old_wiki = ingest.ROOT, ingest.WIKI
            ingest.ROOT, ingest.WIKI = root, root
            try:
                ingest.write_needs_attention(
                    [(page, {"title": "Brief", "depth": "brief",
                             "depth_note": "needs review — PDF but no method"}, "")],
                    "2026-11-20",
                )
                text = (root / "index-needs-attention.md").read_text(
                    encoding="utf-8")
            finally:
                ingest.ROOT, ingest.WIKI = old_root, old_wiki
            self.assertIn("needs review — PDF but no method", text)


class FrontmatterSafetyTests(unittest.TestCase):
    def test_scalars_with_newlines_cannot_inject_yaml_keys(self):
        hostile = 'abc\nstatus: archived'
        text = ingest.frontmatter(
            {"title": "X", "summary": "s", "section": "Papers",
             "url": "https://example.com/x"},
            "active", "stub", "2026-11-20", "abc1234",
            uid=hostile, last_checked=hostile, created=hostile,
        )
        head = text.split("\n---\n", 1)[0]
        # Every managed scalar is a quoted, single-line YAML value.
        self.assertEqual(
            [line for line in head.splitlines() if line.startswith("status:")],
            ['status: "active"'],
        )
        self.assertEqual(
            [line for line in head.splitlines()
             if line.startswith(("uid:", "created:", "last_checked:"))],
            [f"{k}: {ingest.q(hostile)}"
             for k in ("uid", "last_checked", "created")],
        )

    def test_write_page_refuses_a_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            outside = root / "outside.md"
            outside.write_text("do not touch", encoding="utf-8")
            link = root / "page.md"
            link.symlink_to(outside)
            with self.assertRaises(SystemExit) as caught:
                ingest.write_page(link, "pwned")
            self.assertIn("refusing to write through symlink",
                          str(caught.exception))
            self.assertEqual(outside.read_text(encoding="utf-8"),
                             "do not touch")

    def test_symlinked_wiki_directory_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            src = root / "source"
            src.mkdir()
            (src / "README.md").write_text(
                "## Tools\n\n* [Foo](https://example.com/foo) - a desc\n",
                encoding="utf-8",
            )
            for cmd in (
                ["git", "init", "-q"],
                ["git", "config", "user.email", "a@b.c"],
                ["git", "config", "user.name", "t"],
                ["git", "add", "."],
                ["git", "commit", "-qm", "init"],
            ):
                subprocess.run(cmd, cwd=src, check=True, capture_output=True)
            kb = root / "kb"
            kb.mkdir()
            outside = root / "OUTSIDE"
            outside.mkdir()
            (kb / "wiki").symlink_to(outside, target_is_directory=True)
            old_root, old_wiki = ingest.ROOT, ingest.WIKI
            ingest.ROOT, ingest.WIKI = kb, kb / "wiki"
            try:
                with self.assertRaises(SystemExit) as caught:
                    ingest.main(["--source", str(src)])
                self.assertIn("refusing to write through symlink",
                              str(caught.exception))
            finally:
                ingest.ROOT, ingest.WIKI = old_root, old_wiki
            self.assertFalse((outside / "foo.md").exists())
            self.assertFalse(list(outside.glob("index-*.md")))


if __name__ == "__main__":
    unittest.main()
