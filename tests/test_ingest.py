#!/usr/bin/env python3
"""Stdlib unittest suite for the ingest triage classifier."""

from __future__ import annotations

import os
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

    def test_scalar_drops_trailing_comment_and_keeps_embedded_quotes(self):
        fields, _ = ingest.split_page(
            '---\ntitle: "Foo" # a title\n'
            'created: "2026-01-01" # first seen\n'
            'nickname: \'He said "hello"\'\n---\n\nBody.\n'
        )
        self.assertEqual(fields["title"], "Foo")
        self.assertEqual(fields["created"], "2026-01-01")
        self.assertEqual(fields["nickname"], 'He said "hello"')

    def test_frontmatter_without_final_newline_is_parsed(self):
        fields, body = ingest.split_page('---\ntitle: "X"\nrelated: [ghost]\n---')
        self.assertEqual(fields["title"], "X")
        self.assertEqual(fields["related"], "[ghost]")
        self.assertEqual(body, "")
        blocks = ingest.frontmatter_blocks('---\ntitle: "X"\nrelated: [a]\n---')
        self.assertTrue(any(k == "related" for k, _ in blocks))


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

    def test_bom_page_preserves_unmanaged_frontmatter_blocks(self):
        page = self.wiki / "a.md"
        page.write_text(
            "\ufeff---\nuid: \"01aa0000-0000-7000-8000-000000000000\"\n"
            "title: \"A\"\nurl: \"https://example.com/a\"\n"
            "category: \"CAN Bus Analysis\"\nstatus: \"active\"\n"
            "created: \"2026-01-01\"\nlast_checked: \"2026-01-01\"\n"
            "related:\n  - beta\ndepth_note: \"deepen candidate — x\"\n"
            "---\n\nBody.\n",
            encoding="utf-8",
        )
        self.write_list(
            "## CAN Bus Analysis\n\n* [A](https://example.com/a) - a changed\n"
        )
        text = page.read_text(encoding="utf-8")
        self.assertIn("related:", text)
        self.assertIn("  - beta", text)
        self.assertIn("depth_note:", text)

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

    def test_hub_named_section_index_does_not_clobber_an_entity(self):
        self.write_list(
            "## Concept map\n\n* [Alpha](https://example.com/alpha) - a\n\n"
            "## Tools\n\n* [Index Concept Map 2](https://example.com/e) - e\n"
        )
        pages = [p for p in self.wiki.glob("*.md")
                 if "https://example.com/e" in p.read_text(encoding="utf-8")]
        self.assertEqual([p.name for p in pages], ["index-concept-map-2-2.md"])
        self.assertTrue((self.wiki / "index-concept-map-2.md").read_text(
            encoding="utf-8").startswith("# Concept map"))

    def test_entity_slug_cannot_take_the_glossary_stem(self):
        self.write_list(
            "## CAN Bus Analysis\n\n* [Index Glossary](https://example.com/g) - g\n"
        )
        self.assertTrue((self.wiki / "index-glossary-2.md").is_file())

    def test_facet_cleanup_keeps_an_authored_index_facet_page(self):
        self.write_list(
            "## Tools\n\n* [A](https://example.com/a) - a\n"
            "* [B](https://example.com/b) - b\n"
            "* [Index Facet Can](https://example.com/c) - c\n"
        )
        for name in ("a.md", "b.md"):
            p = self.wiki / name
            p.write_text(p.read_text(encoding="utf-8").replace(
                "depth: ", "facets: [can]\ndepth: "), encoding="utf-8")
        self.ingest()
        self.assertTrue((self.wiki / "index-facet-can-2.md").is_file())
        self.assertTrue((self.wiki / "index-facet-can.md").read_text(
            encoding="utf-8").startswith("# Facet:"))

    def test_relisted_entry_is_un_tombstoned(self):
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        self.write_list("# Empty\n")
        page = self.wiki / "a.md"
        self.assertIn('status: archived', page.read_text(encoding="utf-8"))
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        text = page.read_text(encoding="utf-8")
        self.assertNotIn("archived", text)
        self.assertNotIn("Delisted from the source list", text)

    def test_verified_archived_project_is_not_un_tombstoned(self):
        page = self.wiki / "a.md"
        page.write_text(
            '---\nuid: "01aa0000-0000-7000-8000-000000000000"\n'
            'title: "A"\nurl: "https://example.com/a"\n'
            'category: "CAN Bus Analysis"\nstatus: "archived"\n'
            'created: "2026-01-01"\nlast_checked: "2026-01-01"\n'
            '---\n\nThe upstream project is archived.\n',
            encoding="utf-8",
        )
        self.write_list(
            "## CAN Bus Analysis\n\n* [A](https://example.com/a) - a\n")
        text = page.read_text(encoding="utf-8")
        self.assertIn('status: "archived"', text)
        self.assertNotIn("Delisted from the source list", text)

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
        # No `status:` in frontmatter: a whole-file regex would rewrite the
        # first one it finds — which lives in the body — instead of leaving
        # prose alone. The page is still a real entry (it has a url).
        (self.wiki / "gone.md").write_text(
            '---\nuid: "01aa0000-0000-7000-8000-000000000001"\n'
            'title: "Gone"\nurl: "https://example.com/gone"\n'
            'summary: "Delisted from the source list"\n'
            'created: "2026-01-01"\nlast_checked: "2026-01-01"\n'
            '---\n\nBody paragraph.\n\nstatus: draft here.\n',
            encoding="utf-8",
        )
        self.write_list("## CAN Bus Analysis\n\n* [A](https://example.com/a) - a\n")
        text = (self.wiki / "gone.md").read_text(encoding="utf-8")
        _, body = text.split("\n---\n", 1)
        self.assertIn("> Delisted from the source list", body)
        self.assertIn("status: draft here.", body)
        self.assertEqual(body.count("status: draft"), 1,
                         "a body line must not be rewritten like frontmatter")
        self.assertNotIn("status: archived", body)


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

    def test_bom_source_readme_keeps_the_first_section(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "README.md"
            p.write_text(
                '\ufeff## First\n\n* [A](https://example.com/a) - a\n\n'
                '## Second\n\n* [B](https://example.com/b) - b\n',
                encoding="utf-8",
            )
            self.assertEqual(
                [e["title"] for e in ingest.parse_list(p)], ["A", "B"])


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
            # Target the temp root so containment passes: only the explicit
            # symlink guard can reject the write. A temp dir outside ROOT
            # raised via containment and made this test vacuous.
            saved = ingest.ROOT, ingest.WIKI
            self.addCleanup(lambda: (setattr(ingest, "ROOT", saved[0]),
                                     setattr(ingest, "WIKI", saved[1])))
            ingest.ROOT, ingest.WIKI = root, root
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


class SweepFourRegressionTests(unittest.TestCase):
    """Regressions for the fourth sweep's verified runtime bugs."""

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
        self.addCleanup(self._restore)

    def _restore(self):
        ingest.ROOT, ingest.WIKI = self._old_root, self._old_wiki
        self._tmp.cleanup()

    def commit_list(self, body):
        (self.source / "README.md").write_text(body, encoding="utf-8")
        for cmd in (
            ["git", "-C", str(self.source), "init", "-q"],
            ["git", "-C", str(self.source), "add", "README.md"],
            ["git", "-C", str(self.source), "-c", "user.email=clyde@example.com",
             "-c", "user.name=Clyde", "commit", "-q", "-m", "list"],
        ):
            subprocess.run(cmd, check=True, capture_output=True)

    def ingest(self):
        return ingest.main(["--source", str(self.source)])

    def test_case_insensitive_slug_preserves_authored_page(self):
        authored = self.wiki / "Alpha.md"
        authored.write_text(
            '---\ntitle: "Authored alpha"\n---\n\nAUTHORED BODY.\n',
            encoding="utf-8",
        )
        self.commit_list("## Tools\n\n* [Alpha](https://example.com/alpha) - a\n")
        self.ingest()
        text = authored.read_text(encoding="utf-8")
        self.assertIn("AUTHORED BODY.", text)
        self.assertNotIn("example.com/alpha", text)
        self.assertTrue((self.wiki / "alpha-2.md").is_file())

    def test_nested_page_links_are_relative_to_wiki(self):
        nested = self.wiki / "nested"
        nested.mkdir()
        (nested / "deep.md").write_text(
            '---\ntitle: "Deep"\nsummary: "s"\ntype: entity\n'
            'status: "unknown"\nfacets: [can]\n---\n\nBody.\n',
            encoding="utf-8",
        )
        (nested / "other.md").write_text(
            '---\ntitle: "Other"\nsummary: "s"\ntype: entity\n'
            'facets: [can]\n---\n\nBody.\n',
            encoding="utf-8",
        )
        self.commit_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        self.ingest()
        attention = (self.wiki / "index-needs-attention.md").read_text(
            encoding="utf-8")
        facet = (self.wiki / "index-facet-can.md").read_text(encoding="utf-8")
        self.assertIn("(nested/deep.md)", attention)
        self.assertIn("(nested/deep.md)", facet)
        self.assertNotIn("(deep.md)", attention)

    def test_directory_named_md_does_not_abort_ingest(self):
        (self.wiki / "notes.md").mkdir()
        self.commit_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        self.ingest()  # must not raise
        self.assertTrue((self.wiki / "a.md").is_file())

    def test_out_of_root_concept_symlink_is_not_listed(self):
        outside = self.base / "OUTSIDE"
        outside.mkdir()
        secret = outside / "secret.md"
        secret.write_text(
            '---\ntitle: "Secret"\nsummary: "LEAKCONCEPT"\n---\n\nBody.\n',
            encoding="utf-8",
        )
        (self.wiki / "concepts" / "leak.md").symlink_to(secret)
        self.commit_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        self.ingest()
        index = (self.kb / "index.md").read_text(encoding="utf-8")
        self.assertNotIn("LEAKCONCEPT", index)
        self.assertNotIn("secret.md", index)

    def test_hardlinked_page_write_is_refused(self):
        victim = self.base / "outside-victim.md"
        victim.write_text(
            '---\nuid: "01aa0000-0000-7000-8000-000000000000"\n'
            'title: "Old"\nurl: "https://example.com/old"\n'
            'status: "active"\ncreated: "2020-01-01"\n'
            'last_checked: "2020-01-01"\n---\n\nOld body.\n',
            encoding="utf-8",
        )
        (self.wiki / "old.md").hardlink_to(victim)
        self.commit_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        with self.assertRaises(SystemExit) as caught:
            self.ingest()
        self.assertIn("hardlinked", str(caught.exception))
        self.assertNotIn("archived", victim.read_text(encoding="utf-8"))

    def test_url_and_section_move_removes_stale_index_idempotently(self):
        self.commit_list("## Old Section\n\n* [A](https://example.com/old) - a\n")
        self.ingest()
        self.assertTrue((self.wiki / "index-old-section.md").exists())
        self.commit_list("## New Section\n\n* [A](https://example.com/new) - a\n")
        self.ingest()
        self.assertFalse((self.wiki / "index-old-section.md").exists())
        self.assertTrue((self.wiki / "index-new-section.md").exists())
        before = {p.name: p.read_bytes() for p in self.kb.rglob("*.md")}
        self.ingest()
        after = {p.name: p.read_bytes() for p in self.kb.rglob("*.md")}
        self.assertEqual(before, after, "no-op re-ingest must be byte-identical")

    def test_index_prefixed_entity_is_visible_to_generated_hubs(self):
        self.commit_list(
            "## Tools\n\n* [Index Concept Map](https://example.com/hub) - h\n"
        )
        self.ingest()
        page = self.wiki / "index-concept-map-2.md"
        self.assertTrue(page.is_file())
        attention = (self.wiki / "index-needs-attention.md").read_text(
            encoding="utf-8")
        self.assertIn("index-concept-map-2.md", attention)

    def test_provenance_fields_are_immutable_across_updates(self):
        page = self.wiki / "a.md"
        page.write_text(
            '---\nuid: "01aa0000-0000-7000-8000-000000000001"\n'
            'title: "A"\nurl: "https://example.com/old"\n'
            'category: "Tools"\nstatus: "active"\n'
            'created: "2020-01-01"\nlast_checked: "2020-01-02"\n'
            'updated: "2020-01-03"\n'
            'source_commit: "OLDCOMMIT"\nsource_list: "old-list"\n'
            'list_summary: "old summary"\n'
            'status_note: "verified manually"\n---\n\nBody.\n',
            encoding="utf-8",
        )
        self.commit_list("## Tools\n\n* [A](https://example.com/new) - new summary\n")
        self.ingest()
        fields, body = ingest.split_page(page.read_text(encoding="utf-8"))
        self.assertEqual(fields["uid"], "01aa0000-0000-7000-8000-000000000001")
        self.assertEqual(fields["created"], "2020-01-01")
        self.assertEqual(fields["last_checked"], "2020-01-02")
        # An unmanaged block (status_note) is preserved verbatim; the managed
        # provenance stamps are refreshed from the source commit.
        self.assertEqual(fields["status_note"], "verified manually")
        self.assertEqual(fields["list_summary"], "new summary")
        self.assertNotEqual(fields["source_commit"], "OLDCOMMIT")
        self.assertNotEqual(fields["updated"], "2020-01-03")

    def test_authored_depth_and_body_survive_an_update(self):
        page = self.wiki / "a.md"
        authored = (
            '---\nuid: "01aa0000-0000-7000-8000-000000000001"\n'
            'title: "A"\nurl: "https://example.com/old"\n'
            'category: "Tools"\nstatus: "active"\n'
            'created: "2020-01-01"\nlast_checked: "2020-01-02"\n'
            'depth: full\n---\n\n# Authored research\n\nA real paragraph.\n'
        )
        page.write_text(authored, encoding="utf-8")
        self.commit_list("## Tools\n\n* [A](https://example.com/new) - new summary\n")
        self.ingest()
        text = page.read_text(encoding="utf-8")
        self.assertIn('depth: "full"', text)
        self.assertIn("# Authored research", text)
        self.assertIn("A real paragraph.", text)
        self.assertNotIn("generated stub", text)

    def test_relisted_full_page_drops_delisted_note(self):
        page = self.wiki / "a.md"
        page.write_text(
            '---\nuid: "01aa0000-0000-7000-8000-000000000001"\n'
            'title: "A"\nurl: "https://example.com/a"\n'
            'category: "Tools"\nstatus: "archived"\n'
            'created: "2020-01-01"\nlast_checked: "2020-01-02"\n'
            'depth: full\n---\n\n# Real research.\n\n'
            '> Delisted from the source list as of deadbeef.\n',
            encoding="utf-8",
        )
        self.commit_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        self.ingest()
        text = page.read_text(encoding="utf-8")
        self.assertNotIn("Delisted from the source list", text)
        self.assertIn('depth: "full"', text)
        self.assertIn("# Real research.", text)


class SweepFiveRegressionTests(unittest.TestCase):
    """Regressions for the fifth sweep's verified runtime bugs."""

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
        for cmd in (
            ["git", "-C", str(self.source), "init", "-q"],
            ["git", "-C", str(self.source), "config", "user.email", "clyde@example.com"],
            ["git", "-C", str(self.source), "config", "user.name", "Clyde"],
        ):
            subprocess.run(cmd, check=True, capture_output=True)
        self.addCleanup(self._restore)

    def _restore(self):
        ingest.ROOT, ingest.WIKI = self._old_root, self._old_wiki
        self._tmp.cleanup()

    def write_list(self, body):
        (self.source / "README.md").write_text(body, encoding="utf-8")
        for cmd in (
            ["git", "-C", str(self.source), "add", "README.md"],
            ["git", "-C", str(self.source), "commit", "--allow-empty", "-qm", "list"],
        ):
            subprocess.run(cmd, check=True, capture_output=True)
        return ingest.main(["--source", str(self.source)])

    def test_new_section_preserves_earlier_index_named_entity(self):
        first = "## Misc\n\n* [Index Tools](https://example.com/x) - x\n"
        second = (first + "\n## Tools\n\n* [A](https://example.com/a) - a\n")
        self.write_list(first)
        page = self.wiki / "index-tools.md"
        self.assertTrue(page.read_text(encoding="utf-8").startswith("---"))
        self.write_list(second)
        text = page.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---"))
        self.assertIn("uid:", text)
        self.assertIn("example.com/x", text)
        self.assertTrue((self.wiki / "index-tools-2.md").is_file())
        self.assertIn("# Tools", (self.wiki / "index-tools-2.md").read_text())
        before = {p.name: p.read_bytes() for p in self.kb.rglob("*.md")}
        self.write_list(second)
        after = {p.name: p.read_bytes() for p in self.kb.rglob("*.md")}
        self.assertEqual(before, after, "no-op re-ingest must be byte-identical")

    def test_delisted_index_named_entity_is_tombstoned(self):
        self.write_list("## Misc\n\n* [Index Tools](https://example.com/x) - x\n")
        self.write_list("# Empty\n\nNo entries.\n")
        text = (self.wiki / "index-tools.md").read_text(encoding="utf-8")
        self.assertIn("status: archived", text)
        self.assertIn("Delisted from the source list", text)
        index = (self.wiki / "index-misc.md").read_text(encoding="utf-8")
        self.assertIn("(delisted)", index)

    def test_verified_archived_page_is_tombstoned_then_relisted(self):
        self.write_list("## Tools\n\n* [A](https://example.com/a) - old\n")
        page = self.wiki / "a.md"
        text = page.read_text(encoding="utf-8").replace(
            'status: "unknown"', 'status: "archived"')
        text = text.replace("---\n\n", 'status_note: "upstream dead"\n---\n\n', 1)
        page.write_text(text, encoding="utf-8")
        self.write_list("# Empty\n\nNo entries.\n")
        delisted = page.read_text(encoding="utf-8")
        self.assertIn('status: "archived"', delisted)
        self.assertIn("Delisted from the source list", delisted)
        self.write_list("## Tools\n\n* [A](https://example.com/a) - new desc.\n")
        relisted = page.read_text(encoding="utf-8")
        self.assertNotIn("Delisted from the source list", relisted)
        self.assertIn('status: "unknown"', relisted)
        self.assertIn("new desc.", relisted)

    def test_directory_at_generated_index_path_is_named_not_misdiagnosed(self):
        (self.wiki / "index-tools.md").mkdir()
        with self.assertRaises(SystemExit) as caught:
            self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        self.assertIn("directory", str(caught.exception))
        self.assertNotIn("hardlinked", str(caught.exception))

    def test_overlong_title_and_section_do_not_crash(self):
        self.write_list("## Tools\n\n* [" + "A" * 300 + "](https://x.example/a) - d\n")
        slugs = [p.stem for p in self.wiki.glob("a*.md")]
        self.assertEqual(len(slugs), 1)
        self.assertLessEqual(len(slugs[0]), ingest.MAX_SLUG)
        self.write_list("## " + "S" * 300 + "\n\n* [B](https://x.example/b) - d\n")
        self.assertTrue(any(p.name.startswith("index-sss") for p in self.wiki.glob("index-*.md")))

    def test_concept_map_links_nested_and_root_concepts(self):
        nested = self.wiki / "concepts" / "deep" / "deepconcept.md"
        nested.parent.mkdir(parents=True)
        nested.write_text(
            '---\ntitle: "Deep Concept"\nsummary: "a"\ntype: concept\n---\nbody\n',
            encoding="utf-8",
        )
        root_concept = self.wiki / "rootconcept.md"
        root_concept.write_text(
            '---\ntitle: "Root Concept"\nsummary: "b"\ntype: concept\n---\nbody\n',
            encoding="utf-8",
        )
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        concept_map = (self.wiki / "index-concept-map.md").read_text(encoding="utf-8")
        self.assertIn("(concepts/deep/deepconcept.md)", concept_map)
        self.assertIn("(rootconcept.md)", concept_map)

    def test_research_papers_create_sets_published(self):
        self.write_list(
            "## Research Papers\n\n* [Paper](https://example.com/paper) - p\n")
        text = (self.wiki / "paper.md").read_text(encoding="utf-8")
        self.assertIn('status: "published"', text)

    def test_block_form_facets_are_indexed(self):
        for name in ("a", "b"):
            (self.wiki / f"{name}.md").write_text(
                f'---\ntitle: "{name.upper()}"\nsummary: "s"\n'
                "type: entity\nfacets:\n  - can\n  - diagnostics\n---\nbody\n",
                encoding="utf-8",
            )
        self.write_list(
            "## Tools\n\n* [A](https://example.com/a) - a\n"
            "* [B](https://example.com/b) - b\n")
        self.assertTrue((self.wiki / "index-facet-can.md").is_file())
        self.assertTrue((self.wiki / "index-facet-diagnostics.md").is_file())
        self.assertIn("## Facets", (self.kb / "index.md").read_text(encoding="utf-8"))


class SweepSixRegressionTests(unittest.TestCase):
    """Regressions for the sixth sweep's verified state and index bugs."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self.source = self.base / "source"
        self.kb = self.base / "kb"
        self.wiki = self.kb / "wiki"
        (self.wiki / "concepts").mkdir(parents=True)
        self.source.mkdir()
        self._saved = ingest.ROOT, ingest.WIKI
        ingest.ROOT, ingest.WIKI = self.kb, self.wiki
        for cmd in (
            ["git", "-C", str(self.source), "init", "-q"],
            ["git", "-C", str(self.source), "config", "user.email", "clyde@example.com"],
            ["git", "-C", str(self.source), "config", "user.name", "Clyde"],
        ):
            subprocess.run(cmd, check=True, capture_output=True)
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        ingest.ROOT, ingest.WIKI = self._saved
        self._tmp.cleanup()

    def write_list(self, body):
        (self.source / "README.md").write_text(body, encoding="utf-8")
        for cmd in (
            ["git", "-C", str(self.source), "add", "README.md"],
            ["git", "-C", str(self.source), "commit", "--allow-empty", "-qm", "list"],
        ):
            subprocess.run(cmd, check=True, capture_output=True)
        return ingest.main(["--source", str(self.source)])

    def output(self, body):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.write_list(body)
        return buf.getvalue()

    @staticmethod
    def authored(title, url=None, status=None, stem=None):
        fields = (f'uid: "01aa0000-0000-7000-8000-000000000001"\n'
                  f'title: "{title}"\ntype: entity\nsummary: "s"\n'
                  'created: "2026-01-01"\nlast_checked: "2026-01-01"\n')
        if url:
            fields += f'url: "{url}"\n'
        if status:
            fields += f'status: "{status}"\n'
        return "---\n" + fields + "---\nbody\n"

    def test_uppercase_index_stem_is_reserved(self):
        # A human-authored page parked at an UPPERCASE index-* stem must still
        # reserve the generated index's lowercase slug. A case-sensitive
        # reservation lets the "Tools" index take index-tools.md, which on
        # APFS is the same inode as the authored index-Tools.md.
        page = self.wiki / "index-Tools.md"
        page.write_text(self.authored("Tools Hub", "https://example.com/hub"),
                        encoding="utf-8")
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        self.assertTrue(page.is_file())
        self.assertIn("Tools Hub", page.read_text(encoding="utf-8"))
        generated = self.wiki / "index-tools-2.md"
        self.assertTrue(generated.is_file())
        self.assertIn("# Tools", generated.read_text(encoding="utf-8"))

    def test_long_stem_url_move_preserves_identity(self):
        stem = "a" * 250
        page = self.wiki / f"{stem}.md"
        page.write_text(self.authored("Long", "https://example.com/old"),
                        encoding="utf-8")
        self.write_list(
            f"## Tools\n\n* [{stem}](https://example.com/new) - desc\n")
        self.assertEqual(len(list(self.wiki.glob("a*.md"))), 1)
        text = page.read_text(encoding="utf-8")
        self.assertIn("https://example.com/new", text)
        self.assertNotIn("archived", text)

    def test_block_facet_variants_and_last_key_wins(self):
        cases = {
            "comment between items":
                'facets:\n  - firmware\n  # note\n  - hardware\n',
            "unindented items": 'facets:\n- firmware\n- hardware\n',
            "block then inline": 'facets:\n  - hardware\nfacets: [firmware]\n',
        }
        expected = {
            "comment between items": "firmware hardware",
            "unindented items": "firmware hardware",
            "block then inline": "[firmware]",
        }
        for label, block in cases.items():
            with self.subTest(label):
                text = "---\ntitle: \"x\"\n" + block + "---\nbody\n"
                self.assertEqual(ingest.split_page(text)[0].get("facets"),
                                 expected[label])

    def test_tombstone_counter_is_idempotent_without_status(self):
        page = self.wiki / "gone.md"
        page.write_text(self.authored("Gone", "https://example.com/gone"),
                        encoding="utf-8")
        empty = "# Empty\n"
        first = self.output(empty)
        second = self.output(empty)
        self.assertIn("1 tombstoned", first)
        self.assertNotIn("tombstoned", second.replace("0 tombstoned", ""))
        self.assertIn("status: archived", page.read_text(encoding="utf-8"))

    def test_authored_page_at_generated_index_path_is_refused(self):
        (self.wiki / "index-glossary.md").write_text(
            self.authored("My Glossary"), encoding="utf-8")
        with self.assertRaises(SystemExit) as caught:
            self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        self.assertIn("authored page", str(caught.exception))
        self.assertIn("My Glossary",
                      (self.wiki / "index-glossary.md").read_text())

    def test_symlinked_entry_page_is_refused_then_recovers(self):
        page = self.wiki / "cabana.md"
        original = self.authored("Cabana", "https://example.com/cabana")
        page.write_text(original, encoding="utf-8")
        outside = self.base / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        page.unlink()
        page.symlink_to(outside)
        body = "## Tools\n\n* [Cabana](https://example.com/cabana) - c\n"
        with self.assertRaises(SystemExit) as caught:
            self.write_list(body)
        self.assertIn("symlinked page", str(caught.exception))
        page.unlink()
        page.write_text(original, encoding="utf-8")
        self.write_list(body)
        self.assertEqual(len(list(self.wiki.glob("cabana*.md"))), 1)


class SweepSevenRegressionTests(unittest.TestCase):
    """Regressions for the seventh sweep's index, identity and FIFO bugs."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self.source = self.base / "source"
        self.kb = self.base / "kb"
        self.wiki = self.kb / "wiki"
        (self.wiki / "concepts").mkdir(parents=True)
        self.source.mkdir()
        self._saved = ingest.ROOT, ingest.WIKI
        ingest.ROOT, ingest.WIKI = self.kb, self.wiki
        for cmd in (
            ["git", "-C", str(self.source), "init", "-q"],
            ["git", "-C", str(self.source), "config", "user.email", "clyde@example.com"],
            ["git", "-C", str(self.source), "config", "user.name", "Clyde"],
        ):
            subprocess.run(cmd, check=True, capture_output=True)
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        ingest.ROOT, ingest.WIKI = self._saved
        self._tmp.cleanup()

    def write_list(self, body):
        (self.source / "README.md").write_text(body, encoding="utf-8")
        for cmd in (
            ["git", "-C", str(self.source), "add", "README.md"],
            ["git", "-C", str(self.source), "commit", "--allow-empty", "-qm", "list"],
        ):
            subprocess.run(cmd, check=True, capture_output=True)
        return ingest.main(["--source", str(self.source)])

    def concept(self, rel, title, extra=""):
        path = self.wiki / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f'---\ntitle: "{title}"\nsummary: "concept summary"\n'
            f'type: concept\n{extra}---\nbody\n', encoding="utf-8")
        return path

    def test_nested_concept_is_listed_in_l1_index(self):
        self.concept("concepts/flat.md", "Flat Concept")
        self.concept("concepts/deep/nested.md", "Nested Concept")
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        l1 = (self.kb / "index.md").read_text(encoding="utf-8")
        concept_map = (self.wiki / "index-concept-map.md").read_text(
            encoding="utf-8")
        self.assertIn("Nested Concept", l1)
        self.assertIn("Nested Concept", concept_map)

    def test_url_less_authored_index_page_is_reserved(self):
        page = self.wiki / "index-tools.md"
        page.write_text(
            '---\ntitle: "My Tools Note"\ntype: entity\nsummary: "s"\n'
            'created: "2026-01-01"\n---\nAUTHORED BODY.\n', encoding="utf-8")
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a desc\n")
        self.assertIn("AUTHORED BODY.", page.read_text(encoding="utf-8"))
        self.assertTrue((self.wiki / "index-tools-2.md").exists())

    def test_fifo_at_generated_index_path_is_refused(self):
        path = self.wiki / "index-glossary.md"
        os.mkfifo(path)
        with self.assertRaises(SystemExit) as caught:
            self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        self.assertIn("non-regular", str(caught.exception))

    def test_fifo_at_l1_index_path_is_refused(self):
        os.mkfifo(self.kb / "index.md")
        with self.assertRaises(SystemExit) as caught:
            self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        self.assertIn("non-regular", str(caught.exception))

    def test_concept_url_is_a_cross_reference_not_list_identity(self):
        page = self.concept("concepts/probe.md", "Probe",
                            'url: "https://example.org/see-also"\n')
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        self.assertNotIn("status: archived", page.read_text(encoding="utf-8"))

    def test_duplicate_concept_stems_agree_across_hubs(self):
        self.concept("concepts/probe.md", "Probe Canonical")
        self.concept("topics/probe.md", "Probe Clone")
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        l1 = (self.kb / "index.md").read_text(encoding="utf-8")
        concept_map = (self.wiki / "index-concept-map.md").read_text(
            encoding="utf-8")
        self.assertIn("Probe Canonical", l1)
        self.assertNotIn("Probe Clone", l1)
        self.assertIn("Probe Canonical", concept_map)
        self.assertNotIn("Probe Clone", concept_map)


class SweepEightRegressionTests(SweepSevenRegressionTests):
    """Regressions for the eighth sweep's case, status and reservation bugs."""

    def test_url_move_reuses_an_uppercase_stem(self):
        page = self.wiki / "Alpha.md"
        page.write_text(
            '---\nuid: "01aa0000-0000-7000-8000-000000000001"\n'
            'title: "Alpha"\ntype: entity\nsummary: "s"\n'
            'url: "https://example.com/old"\nstatus: "active"\n'
            'created: "2026-01-01"\nlast_checked: "2026-01-01"\n'
            '---\nbody\n', encoding="utf-8")
        self.write_list("## Tools\n\n"
                        "* [Alpha](https://example.com/old) - old desc\n")
        self.write_list("## Tools\n\n"
                        "* [Alpha](https://example.com/new) - new desc\n")
        self.assertTrue(page.exists())
        self.assertIn("example.com/new", page.read_text(encoding="utf-8"))
        self.assertEqual(len(list(self.wiki.glob("[Aa]lpha*.md"))), 1)

    def test_verified_archived_paper_stays_archived_on_edit(self):
        page = self.wiki / "paper.md"
        page.write_text(
            '---\nuid: "01aa0000-0000-7000-8000-000000000001"\n'
            'title: "Paper"\ntype: entity\nsummary: "s"\n'
            'category: "Research Papers"\nurl: "https://example.com/paper"\n'
            'status: "archived"\nstatus_note: "verified dead"\n'
            'created: "2026-01-01"\nlast_checked: "2026-01-01"\n'
            '---\nbody\n', encoding="utf-8")
        self.write_list("## Research Papers\n\n"
                        "* [Paper](https://example.com/paper) - old desc\n")
        self.write_list("## Research Papers\n\n"
                        "* [Paper](https://example.com/paper) - NEW desc\n")
        text = page.read_text(encoding="utf-8")
        self.assertIn('status: "archived"', text)
        self.assertIn("status_note: \"verified dead\"", text)
        self.assertNotIn('status: "published"', text)

    def test_nested_index_page_does_not_reserve_the_root_slug(self):
        nested = self.wiki / "topics" / "index-tools.md"
        nested.parent.mkdir(parents=True)
        nested.write_text(
            '---\ntitle: "Nested hub"\ntype: entity\nsummary: "s"\n'
            '---\nNESTED AUTHORED.\n', encoding="utf-8")
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        self.assertTrue((self.wiki / "index-tools.md").exists())
        self.assertFalse((self.wiki / "index-tools-2.md").exists())

    def test_canonical_concept_beats_a_nested_clone(self):
        self.concept("concepts/probe.md", "Probe Canonical")
        self.concept("concepts/deep/probe.md", "Probe Deep")
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        concept_map = (self.wiki / "index-concept-map.md").read_text(
            encoding="utf-8")
        self.assertIn("Probe Canonical", concept_map)
        self.assertNotIn("Probe Deep", concept_map)


class SweepNineRegressionTests(SweepEightRegressionTests):
    """Regressions for the ninth sweep's archive and L1 dedupe bugs."""

    def test_verified_archive_survives_moving_into_research_papers(self):
        page = self.wiki / "paper.md"
        page.write_text(
            '---\nuid: "01aa0000-0000-7000-8000-000000000001"\n'
            'title: "Paper"\ntype: entity\nsummary: "s"\n'
            'category: "Tools"\nurl: "https://example.com/paper"\n'
            'status: "archived"\nstatus_note: "verified dead"\n'
            'created: "2026-01-01"\nlast_checked: "2026-01-01"\n'
            '---\nbody\n', encoding="utf-8")
        self.write_list('## Research Papers\n\n'
                        '* [Paper](https://example.com/paper) - p\n')
        text = page.read_text(encoding="utf-8")
        self.assertIn('status: "archived"', text)
        self.assertNotIn('status: "published"', text)

    def test_l1_classifies_concepts_by_type_not_directory(self):
        entity = self.wiki / "concepts" / "zephyr.md"
        entity.parent.mkdir(exist_ok=True)
        entity.write_text(
            '---\ntitle: "Zephyr"\nsummary: "s"\ntype: entity\n---\nbody\n',
            encoding="utf-8")
        concept = self.wiki / "root-concept.md"
        concept.write_text(
            '---\ntitle: "Root Concept"\nsummary: "s"\n'
            'type: concept\n---\nbody\n', encoding="utf-8")
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        l1 = (self.kb / "index.md").read_text(encoding="utf-8")
        concept_map = (self.wiki / "index-concept-map.md").read_text(
            encoding="utf-8")
        for hub in (l1, concept_map):
            self.assertIn("Root Concept", hub)
            self.assertNotIn("Zephyr", hub)

    def test_malformed_frontmatter_entry_is_refused_not_duplicated(self):
        page = self.wiki / "cabana.md"
        page.write_text('---\ntitle: "Cabana"\ntype: entity\n'
                        'summary: "s"\nbody with no closing fence\n',
                        encoding="utf-8")
        with self.assertRaises(SystemExit):
            self.write_list('## Tools\n\n'
                            '* [Cabana](https://example.com/cabana) - s\n')
        self.assertEqual(len(list(self.wiki.glob("cabana*.md"))), 1)

    def test_l1_and_concept_map_agree_on_duplicate_stems(self):
        self.concept("concepts/probe.md", "Probe Canonical")
        self.concept("concepts/deep/probe.md", "Probe Deep")
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        l1 = (self.kb / "index.md").read_text(encoding="utf-8")
        concept_map = (self.wiki / "index-concept-map.md").read_text(
            encoding="utf-8")
        for hub in (l1, concept_map):
            self.assertIn("Probe Canonical", hub)
            self.assertNotIn("Probe Deep", hub)


class SweepTenRegressionTests(SweepNineRegressionTests):
    """Regressions for the tenth sweep's hub and refusal edge cases."""

    def test_in_root_symlinked_leaf_is_invisible_to_safe_pages(self):
        # The symlink points INSIDE the wiki, so containment passes and only
        # safe_pages' is_symlink() guard can hide it. Its stem is not an
        # entry slug, so the row-50 symlink guard does not fire either.
        real = self.wiki / "real.md"
        real.write_text(
            '---\nuid: "01aa0000-0000-7000-8000-000000000001"\n'
            'title: "Real"\ntype: entity\nsummary: "s"\n'
            'url: "https://example.com/real"\ncreated: "2026-01-01"\n'
            'last_checked: "2026-01-01"\n---\nbody\n', encoding="utf-8")
        (self.wiki / "link.md").symlink_to(real)
        # Without the guard both files carry the URL and ingest aborts on a
        # duplicate-URL error.
        self.write_list("## Tools\n\n* [Real](https://example.com/real) - r\n")

    def test_summary_less_canonical_concept_still_wins_l1_stem(self):
        canonical = self.wiki / "concepts" / "probe.md"
        canonical.write_text(
            '---\ntitle: "Probe Canonical"\ntype: concept\n---\nbody\n',
            encoding="utf-8")
        self.concept("concepts/deep/probe.md", "Probe Deep")
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        l1 = (self.kb / "index.md").read_text(encoding="utf-8")
        concept_map = (self.wiki / "index-concept-map.md").read_text(
            encoding="utf-8")
        for hub in (l1, concept_map):
            self.assertIn("Probe Canonical", hub)
            self.assertNotIn("Probe Deep", hub)

    def _malformed_entry(self, stem, title, url):
        page = self.wiki / f"{stem}.md"
        page.write_text(
            '---\n'
            'uid: "01aa0000-0000-7000-8000-000000000001"\n'
            f'title: "{title}"\ntype: entity\nsummary: "s"\n'
            f'url: "{url}"\ncreated: "2026-01-01"\n'
            'last_checked: "2026-01-01"\n'
            '---\nbody\n', encoding="utf-8")
        listing = f"## Tools\n\n* [{title}]({url}) - s\n"
        self.write_list(listing)  # runs ingest once to stamp identity
        # Lose only the closing fence; identity is now unparseable and the
        # URL-keyed lookup cannot find the page any more.
        page.write_text(
            f'---\ntitle: "{title}"\ntype: entity\nsummary: "s"\n'
            'body with no closing fence\n', encoding="utf-8")
        return listing

    def test_malformed_suffixed_landing_page_is_refused_not_duplicated(self):
        listing = self._malformed_entry("cabana-2", "Cabana",
                                        "https://example.com/cabana")
        with self.assertRaises(SystemExit):
            self.write_list(listing)
        self.assertEqual(len(list(self.wiki.glob("cabana*.md"))), 1)

    def test_authored_index_stem_is_not_exempt_from_malformed_refusal(self):
        listing = self._malformed_entry("index-of-tools", "Index of Tools",
                                        "https://example.com/iot")
        with self.assertRaises(SystemExit):
            self.write_list(listing)
        self.assertEqual(len(list(self.wiki.glob("index-of-tools*.md"))), 1)

    def test_generated_index_is_still_exempt_from_malformed_refusal(self):
        # A generated index has no frontmatter at all; it must never trip
        # the refusal when an entry happens to slugify to the same stem.
        (self.wiki / "index-tools.md").write_text(
            "# generated\n", encoding="utf-8")
        self.write_list("## Tools\n\n"
                        "* [Tools](https://example.com/tools) - s\n")
        self.assertTrue((self.wiki / "index-tools.md").exists())


class SweepElevenRegressionTests(SweepTenRegressionTests):
    """Regressions for the eleventh sweep's refusal and symlink bugs."""

    def test_reserved_index_suffix_is_not_exempt_from_malformed_refusal(self):
        # index-glossary-2 is an authored entity: the base stem is reserved
        # only because the generated hub owns it. Stripping "-2" for the
        # exemption let a malformed copy be duplicated and stranded.
        listing = self._malformed_entry("index-glossary-2", "Index Glossary",
                                        "https://example.com/iot")
        with self.assertRaises(SystemExit):
            self.write_list(listing)
        self.assertEqual(
            len(list(self.wiki.glob("index-glossary*.md"))), 2)  # hub + page

    def test_uncapped_raw_slug_occupant_is_refused_not_duplicated(self):
        title = "X" * 250  # longer than slugify's 200-char cap
        url = "https://example.com/long"
        page = self.wiki / ("x" * 250 + ".md")
        page.write_text(
            f'---\ntitle: "{title}"\ntype: entity\nsummary: "s"\n'
            f'url: "{url}"\nbody with no closing fence\n', encoding="utf-8")
        with self.assertRaises(SystemExit):
            self.write_list(f"## Tools\n\n* [{title}]({url}) - s\n")
        self.assertEqual(len(list(self.wiki.glob("x*.md"))), 1)

    def test_stale_generated_index_does_not_block_an_entry(self):
        self.write_list("## Tools\n\n* [A](https://example.com/a) - a\n")
        self.assertTrue((self.wiki / "index-tools.md").exists())
        listing = ("## Gadgets\n\n"
                   "* [A](https://example.com/a) - a\n"
                   "* [Index Tools](https://example.com/iot) - s\n")
        # The section moved but A stayed listed, so no page is doomed: the
        # stale generated index survives until the post-update sweep. It has
        # no frontmatter and must not be read as a malformed authored page.
        self.write_list(listing)
        self.write_list(listing)  # idempotent
        authored = list(self.wiki.glob("index-tools*.md"))
        self.assertEqual(len(authored), 1)
        self.assertTrue(authored[0].read_text().startswith("---\n"))

    def test_nested_symlink_does_not_block_an_unrelated_entry(self):
        (self.wiki / "topics").mkdir()
        real = self.wiki / "topics" / "target.md"
        real.write_text("not an entry\n", encoding="utf-8")
        (self.wiki / "topics" / "foo.md").symlink_to(real)
        self.write_list("## Tools\n\n* [Foo](https://example.com/foo) - f\n")
        self.assertTrue((self.wiki / "foo.md").is_file())


if __name__ == "__main__":
    unittest.main()
