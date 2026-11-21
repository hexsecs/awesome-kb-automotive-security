#!/usr/bin/env python3
"""Stdlib unittest suite for the navigation taxonomy and backfill tool."""

from __future__ import annotations

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

import yaml  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import backfill_navigation  # noqa: E402
import taxonomy  # noqa: E402


class FacetAssignmentTests(unittest.TestCase):
    def test_topic_facet(self) -> None:
        facets = taxonomy.assign_facets("SocketCAN candump CAN bus frames", "Tools")
        self.assertIn("can", facets)

    def test_kind_comes_from_category(self) -> None:
        facets = taxonomy.assign_facets("A survey of CAN security", "Research Papers")
        self.assertIn("research", facets)
        self.assertIn("can", facets)

    def test_no_lin_from_linux(self) -> None:
        facets = taxonomy.assign_facets("Linux userspace utilities", "Tools")
        self.assertNotIn("lin", facets)

    def test_tool_category_without_keyword(self) -> None:
        facets = taxonomy.assign_facets("CaringCaribou", "Penetration Testing")
        self.assertIn("tools", facets)

    def test_facets_declared_order(self) -> None:
        facets = taxonomy.assign_facets("UDS diagnostics over DoIP on CAN", "Tools")
        order = {facet.slug: i for i, facet in enumerate(taxonomy.FACETS)}
        self.assertEqual(list(facets), sorted(facets, key=order.get))


def use_temp_root(test, tmp: str) -> None:
    """Point backfill's containment guard at the temp KB for a test."""
    old = backfill_navigation.ROOT
    backfill_navigation.ROOT = Path(tmp)
    test.addCleanup(setattr, backfill_navigation, "ROOT", old)


class BackfillTests(unittest.TestCase):
    def test_inline_related_is_normalised_and_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = Path(tmp) / "example.md"
            page.write_text(
                '---\nuid: 01\ntitle: "Example"\nsummary: "CAN tool."\n'
                'type: entity\ncategory: "Tools"\nrelated: [alpha, beta]\n'
                '---\n\nBody text.\n', encoding="utf-8")
            self.assertTrue(backfill_navigation.backfill(page, check=False))
            first = page.read_text(encoding="utf-8")
            self.assertIn('related:\n  - "alpha"\n  - "beta"', first)
            self.assertIn("facets: [", first)
            self.assertFalse(backfill_navigation.backfill(page, check=False))
            self.assertEqual(page.read_text(encoding="utf-8"), first)
            self.assertTrue(first.endswith("---\n\nBody text.\n"))

    def test_blank_lines_in_frontmatter_are_preserved_on_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = Path(tmp) / "example.md"
            page.write_text(
                '---\ntitle: "Example"\nsummary: "A tool."\n'
                '---\n\nBody.\n', encoding="utf-8")
            backfill_navigation.backfill(page, check=False)
            self.assertIn("\n---\n\nBody.\n", page.read_text(encoding="utf-8"))

    def test_inline_related_with_comment_is_normalised(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = Path(tmp) / "example.md"
            page.write_text(
                '---\ntitle: "Example"\nsummary: "A tool."\n'
                'related: [alpha, beta] # keep\n'
                '---\n\nBody.\n', encoding="utf-8")
            self.assertTrue(backfill_navigation.backfill(page, check=False))
            out = page.read_text(encoding="utf-8")
            self.assertIn('related:\n  - "alpha"\n  - "beta"', out)
            self.assertNotIn("related: [alpha, beta]", out)

    def test_bom_page_is_backfilled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = Path(tmp) / "example.md"
            page.write_text(
                '\ufeff---\ntitle: "Example"\nsummary: "A tool."\n'
                'type: entity\ncategory: "Tools"\n---\n\nBody.\n',
                encoding="utf-8")
            self.assertTrue(backfill_navigation.backfill(page, check=False))
            self.assertIn("facets: [", page.read_text(encoding="utf-8"))

    def test_single_quoted_type_is_understood(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = Path(tmp) / "doip.md"
            page.write_text(
                "---\ntitle: 'DoIP'\nsummary: 'Diagnostics over IP.'\n"
                "type: 'concept'\ncategory: ''\ncluster: bus\nrelated: []\n"
                "---\n\nBody.\n", encoding="utf-8")
            self.assertTrue(backfill_navigation.backfill(page, check=False))
            self.assertIn("cluster: boundary", page.read_text(encoding="utf-8"))

    def test_scalar_drops_comments_and_keeps_embedded_quotes(self) -> None:
        fields = backfill_navigation.page_fields(
            'title: \'He said "hello"\' # note\ntype: "entity" # a page')
        self.assertEqual(fields["title"], 'He said "hello"')
        self.assertEqual(fields["type"], "entity")

    def test_frontmatter_without_final_newline_is_backfilled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = Path(tmp) / "x.md"
            page.write_text(
                '---\ntitle: "X"\nsummary: "CAN tool"\nrelated: []\n---',
                encoding="utf-8")
            self.assertTrue(backfill_navigation.backfill(page, check=False))
            self.assertIn("facets: [", page.read_text(encoding="utf-8"))

    def test_inline_related_ignores_brackets_in_comment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = Path(tmp) / "x.md"
            page.write_text(
                '---\ntitle: "X"\nsummary: "CAN tool"\n'
                'related: [] # keeps [brackets]\n---\n\nBody.\n',
                encoding="utf-8")
            self.assertTrue(backfill_navigation.backfill(page, check=False))
            out = page.read_text(encoding="utf-8")
            self.assertNotIn("[brackets]", out)
            self.assertIn("related:\n", out)

    def test_duplicate_facets_key_is_collapsed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = Path(tmp) / "x.md"
            page.write_text(
                '---\ntitle: "X"\nsummary: "CAN tool"\n'
                'facets: []\nfacets: [also-stale]\n---\n\nBody.\n',
                encoding="utf-8")
            self.assertTrue(backfill_navigation.backfill(page, check=False))
            out = page.read_text(encoding="utf-8")
            self.assertEqual(out.count("facets:"), 1)
            self.assertNotIn("also-stale", out)

    def test_symlinked_parent_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            root = Path(tmp)
            outside_dir = root.parent / f"outside-{root.name}"
            outside_dir.mkdir()
            self.addCleanup(
                lambda: __import__("shutil").rmtree(outside_dir, ignore_errors=True))
            victim = outside_dir / "page.md"
            victim.write_text('---\ntitle: "X"\nrelated: [a]\n---\n',
                              encoding="utf-8")
            linked = root / "linked"
            linked.symlink_to(outside_dir, target_is_directory=True)
            before = victim.read_text(encoding="utf-8")
            self.assertFalse(
                backfill_navigation.backfill(linked / "page.md", check=False))
            self.assertEqual(victim.read_text(encoding="utf-8"), before)

    def test_symlinked_page_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            root = Path(tmp)
            outside = root / "outside.md"
            outside.write_text('---\ntitle: "X"\nrelated: [a]\n---\n', encoding="utf-8")
            link = root / "page.md"
            link.symlink_to(outside)
            before = outside.read_text(encoding="utf-8")
            self.assertFalse(backfill_navigation.backfill(link, check=False))
            self.assertEqual(outside.read_text(encoding="utf-8"), before)

    def test_main_does_not_feed_symlinked_pages_to_backfill(self) -> None:
        # The direct backfill() guard is pinned above; main()'s own filter
        # had no witness. The symlink target is in-root, so containment
        # passes and only `not p.is_symlink()` can exclude the link.
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            wiki = Path(tmp) / "wiki"
            wiki.mkdir()
            real = wiki / "real.md"
            real.write_text('---\ntitle: "X"\nrelated: [a]\n---\n',
                            encoding="utf-8")
            link = wiki / "link.md"
            link.symlink_to(real)

            seen: list[Path] = []
            original = backfill_navigation.backfill
            saved_argv = sys.argv
            self.addCleanup(setattr, backfill_navigation, "backfill", original)
            self.addCleanup(lambda: setattr(sys, "argv", saved_argv))
            backfill_navigation.backfill = lambda path, check: (
                seen.append(path) or False)
            sys.argv = ["backfill_navigation", "--check"]
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(backfill_navigation.main(), 0)
            self.assertIn(real, seen)
            self.assertNotIn(link, seen)

    def test_unreadable_page_fails_loudly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = Path(tmp) / "bad.md"
            page.write_bytes(b"---\ntitle: \xff\xfe\n---\n")
            with self.assertRaises(SystemExit) as caught:
                backfill_navigation.backfill(page, check=False)
            self.assertIn("cannot read", str(caught.exception))


class TaxonomyTargetTests(unittest.TestCase):
    def test_glossary_targets_exist(self) -> None:
        for entry in taxonomy.GLOSSARY:
            with self.subTest(term=entry.term):
                self.assertTrue((REPO / "wiki" / f"{entry.target}.md").exists())

    def test_cluster_and_path_concepts_exist(self) -> None:
        known = {p.stem for p in (REPO / "wiki/concepts").glob("*.md")}
        for cluster in taxonomy.CONCEPT_CLUSTERS:
            for slug in cluster.concepts:
                with self.subTest(cluster=cluster.slug, concept=slug):
                    self.assertIn(slug, known)
        for path in taxonomy.READING_PATHS:
            for slug in path.steps:
                with self.subTest(path=path.title, concept=slug):
                    self.assertIn(slug, known)


class TaxonomyRegressionTests(unittest.TestCase):
    def test_modal_can_is_not_a_can_bus_facet(self):
        self.assertNotIn("can", taxonomy.assign_facets(
            "A tool that can scan a network", "Tools"))
        self.assertIn("can", taxonomy.assign_facets(
            "SocketCAN candump CAN bus frames", "Tools"))

    def test_each_concept_has_one_home(self):
        homes = [slug for cluster in taxonomy.CONCEPT_CLUSTERS
                 for slug in cluster.concepts]
        self.assertEqual(len(homes), len(set(homes)))

    def test_backfill_corrects_a_stale_cluster(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = Path(tmp) / "doip.md"
            page.write_text(
                '---\ntitle: "DoIP"\nsummary: "Diagnostics over IP."\n'
                'type: concept\ncategory: ""\ncluster: bus\nrelated: []\n'
                '---\n\nBody.\n',
                encoding="utf-8",
            )
            self.assertTrue(backfill_navigation.backfill(page, check=False))
            self.assertIn("cluster: boundary", page.read_text(encoding="utf-8"))
            self.assertFalse(backfill_navigation.backfill(page, check=False))


class BackfillSafetyTests(unittest.TestCase):
    """Regressions for the fourth sweep's navigation-tool bugs."""

    def _page(self, tmp, name, text):
        wiki = Path(tmp) / "wiki"
        wiki.mkdir(exist_ok=True)
        page = wiki / name
        page.write_text(text, encoding="utf-8")
        return page

    def test_check_reports_changes_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "x.md",
                '---\ntitle: "X"\nsummary: "CAN tool"\nrelated: []\n---\n\nBody.\n')
            original = page.read_text(encoding="utf-8")
            old_argv = sys.argv
            sys.argv = ["backfill_navigation", "--check"]
            self.addCleanup(setattr, sys, "argv", old_argv)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                backfill_navigation.main()
            self.assertIn("would change 1 of 1 pages", buf.getvalue())
            self.assertEqual(page.read_text(encoding="utf-8"), original)

    def test_directory_named_md_does_not_abort_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            self._page(tmp, "x.md",
                       '---\ntitle: "X"\nsummary: "CAN tool"\nrelated: []\n---\n\nBody.\n')
            (Path(tmp) / "wiki" / "notes.md").mkdir()
            old_argv = sys.argv
            sys.argv = ["backfill_navigation", "--check"]
            self.addCleanup(setattr, sys, "argv", old_argv)
            with contextlib.redirect_stdout(io.StringIO()):
                backfill_navigation.main()  # must not sys.exit

    def test_index_prefixed_entity_is_processed(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "index-of-tools.md",
                '---\ntitle: "Index of tools"\nsummary: "CAN tool"\n'
                'type: entity\nrelated: []\n---\n\nBody.\n')
            self.assertTrue(backfill_navigation.backfill(page, check=False))
            self.assertIn("facets: [", page.read_text(encoding="utf-8"))

    def test_trailing_quote_in_category_is_not_double_stripped(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "x.md",
                '---\ntitle: "X"\nsummary: "Thing"\ncategory: \'"Tools"\'\n'
                'related: []\n---\n\nBody.\n')
            backfill_navigation.backfill(page, check=False)
            facet_line = next(
                line for line in page.read_text(encoding="utf-8").splitlines()
                if line.startswith("facets:"))
            # \"Tools\" (with quotes) is not the canonical category "Tools",
            # so no category-derived `tools` facet may be injected.
            self.assertNotIn("tools", facet_line)

    def test_block_form_facets_are_replaced_not_left_dangling(self):
        blocks = {
            "plain": "facets:\n  - can-bus\n  - telemetry\n",
            "with comment": "facets:\n  - can-bus\n  # mid\n  - telemetry\n",
            "unindented": "facets:\n- can-bus\n- telemetry\n",
        }
        for label, block in blocks.items():
            with self.subTest(label):
                with tempfile.TemporaryDirectory() as tmp:
                    use_temp_root(self, tmp)
                    page = self._page(
                        tmp, "x.md",
                        '---\ntitle: "X"\nsummary: "CAN tool"\ntype: entity\n'
                        + block + '---\n\nBody.\n')
                    backfill_navigation.backfill(page, check=False)
                    text = page.read_text(encoding="utf-8")
                    self.assertRegex(text, r"(?m)^facets: \[[^\]]*\]$")
                    self.assertNotIn("can-bus", text)
                    self.assertNotIn("telemetry", text)
                    self.assertNotIn("# mid", text)

    def test_space_before_colon_related_is_canonicalised(self):
        import link_check
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "x.md",
                '---\ntitle: "X"\nsummary: "CAN tool"\ntype: entity\n'
                'related : [beta]\n---\n\nBody.\n')
            backfill_navigation.backfill(page, check=False)
            text = page.read_text(encoding="utf-8")
            self.assertIn("related:", text)
            self.assertNotIn("related :", text)
            fm, _ = link_check.split_frontmatter(text)
            self.assertEqual(link_check.parse_related(fm), ["beta"])

    def test_space_before_colon_cluster_is_rewritten_in_place(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "can-injection.md",
                '---\ntitle: "CAN Injection"\ntype: concept\n'
                'cluster : stale-here\nsummary: "s"\n---\n\nBody.\n')
            self.assertTrue(backfill_navigation.backfill(page, check=False))
            text = page.read_text(encoding="utf-8")
            self.assertEqual(text.count("cluster"), 1)
            self.assertIn("cluster: bus", text)
            self.assertNotIn("stale-here", text)
            self.assertFalse(backfill_navigation.backfill(page, check=False))

    def test_duplicate_cluster_keys_are_collapsed(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "can-injection.md",
                '---\ntitle: "CAN Injection"\ntype: concept\n'
                'cluster: stale-one\ncluster: stale-two\n---\n\nBody.\n')
            backfill_navigation.backfill(page, check=False)
            text = page.read_text(encoding="utf-8")
            self.assertEqual(text.count("cluster:"), 1)
            self.assertIn("cluster: bus", text)

    def test_space_before_colon_keys_are_recognised(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "x.md",
                '---\ntitle : Alpha\ntype: entity\nsummary: "CAN tool"\n---\n\nBody.\n')
            self.assertTrue(backfill_navigation.backfill(page, check=False))
            concept = self._page(
                tmp, "can-injection.md",
                '---\ntitle: "CAN Injection"\ntype : concept\nsummary: "s"\n---\n\nBody.\n')
            backfill_navigation.backfill(concept, check=False)
            self.assertIn("cluster: bus", concept.read_text(encoding="utf-8"))

    def test_main_with_check_processes_index_prefixed_entity(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            self._page(
                tmp, "index-of-tools.md",
                '---\ntitle: "Index of tools"\nsummary: "CAN tool"\n'
                'type: entity\nrelated: []\n---\n\nBody.\n')
            old_argv = sys.argv
            sys.argv = ["backfill_navigation", "--check"]
            self.addCleanup(setattr, sys, "argv", old_argv)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                backfill_navigation.main()
            self.assertIn("would change 1 of 1 pages", buf.getvalue())

    def test_hardlinked_page_write_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "x.md",
                '---\ntitle: "X"\nsummary: "CAN tool"\nrelated: []\n---\n\nBody.\n')
            victim = Path(tmp) / "outside-victim.md"
            victim.write_text(page.read_text(encoding="utf-8"), encoding="utf-8")
            page.unlink()
            page.hardlink_to(victim)
            with self.assertRaises(SystemExit) as caught:
                backfill_navigation.backfill(page, check=False)
            self.assertIn("hardlinked", str(caught.exception))
            self.assertNotIn("facets:", victim.read_text(encoding="utf-8"))

    def test_readonly_page_write_exits_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "x.md",
                '---\ntitle: "X"\nsummary: "CAN tool"\nrelated: []\n---\n\nBody.\n')
            os.chmod(page, 0o444)
            with self.assertRaises(SystemExit) as caught:
                backfill_navigation.backfill(page, check=False)
            self.assertIn("cannot write", str(caught.exception))

    def test_tab_indented_type_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "x.md",
                '---\ntitle: "X"\nsummary: "Thing"\n'
                'type: concept\n\ttype: entity\n---\n\nBody.\n')
            fields = backfill_navigation.page_fields(
                backfill_navigation.split_frontmatter(
                    page.read_text(encoding="utf-8"))[1])
            self.assertEqual(fields["type"], "concept")


class SweepElevenRegressionTests(BackfillSafetyTests):
    """Regressions for the eleventh sweep's all-or-nothing write guard."""

    def test_unsafe_later_page_leaves_earlier_pages_untouched(self):
        # Writing inline backfilled every page before an unwritable one,
        # leaving the KB half-updated. Preflight must refuse the whole set
        # before the first page changes. A hardlink is the reliable trigger:
        # it is a real file inside the root, so it enters the write set, but
        # preflight refuses to write through it.
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "aaa.md",
                '---\ntitle: "AAA"\nsummary: "CAN tool"\nrelated: []\n'
                '---\n\nBody.\n')
            zzz = self._page(
                tmp, "zzz.md",
                '---\ntitle: "ZZZ"\nsummary: "CAN tool"\nrelated: []\n'
                '---\n\nBody.\n')
            outside = Path(tmp) / "hardlink-target.md"
            os.link(zzz, outside)
            original = page.read_text(encoding="utf-8")
            old_argv = sys.argv
            sys.argv = ["backfill_navigation"]
            self.addCleanup(setattr, sys, "argv", old_argv)
            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit):
                    backfill_navigation.main()
            self.assertEqual(page.read_text(encoding="utf-8"), original)
            self.assertEqual(zzz.read_text(encoding="utf-8").count("facets:"), 0)


class SweepTwelveRegressionTests(BackfillSafetyTests):
    """Regressions for the twelfth sweep's frontmatter rewrite bugs."""

    def test_block_scalar_facets_is_replaced_wholly(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "aaa.md",
                '---\ntitle: "AAA"\ntype: entity\n'
                'facets: |\n  curated list\n  of facets\n---\n\nBody.\n')
            backfill_navigation.backfill(page, False)
            out = page.read_text(encoding="utf-8")
            self.assertNotIn("curated list", out)
            self.assertNotIn("of facets", out)
            fm = yaml.safe_load(out.split("---")[1])
            self.assertEqual(fm["facets"], [])

    def test_block_scalar_cluster_is_replaced_wholly(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "doip.md",
                '---\ntitle: "DoIP"\ntype: concept\n'
                'cluster: |\n  boundary\n  (old note)\n---\n\nBody.\n')
            backfill_navigation.backfill(page, False)
            out = page.read_text(encoding="utf-8")
            self.assertNotIn("old note", out)
            fm = yaml.safe_load(out.split("---")[1])
            self.assertEqual(fm["cluster"], "boundary")

    def test_quoted_comma_in_inline_related_stays_one_item(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "aaa.md",
                '---\ntitle: "AAA"\ntype: entity\n'
                'related: ["alpha, beta", gamma]\n---\n\nBody.\n')
            backfill_navigation.backfill(page, False)
            fm = yaml.safe_load(page.read_text(encoding="utf-8").split("---")[1])
            self.assertEqual(fm["related"], ["alpha, beta", "gamma"])


class SweepThirteenRegressionTests(BackfillSafetyTests):
    """Regressions for the thirteenth sweep's block-scalar/quote rewrites."""

    def test_block_scalar_indent_before_chomp_is_replaced_wholly(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "doip.md",
                '---\ntitle: "DoIP"\ntype: concept\n'
                'cluster: |2-\n  boundary\n  old note\n---\n\nBody.\n')
            backfill_navigation.backfill(page, False)
            out = page.read_text(encoding="utf-8")
            self.assertNotIn("old note", out)
            fm = yaml.safe_load(out.split("---")[1])
            self.assertEqual(fm["cluster"], "boundary")

    def test_inline_edge_quote_and_escape_survive_normalisation(self):
        with tempfile.TemporaryDirectory() as tmp:
            use_temp_root(self, tmp)
            page = self._page(
                tmp, "aaa.md",
                '---\ntitle: "AAA"\ntype: entity\n'
                'related: ["\'foo", "a\\"b"]\n---\n\nBody.\n')
            backfill_navigation.backfill(page, False)
            fm = yaml.safe_load(page.read_text(encoding="utf-8").split("---")[1])
            self.assertEqual(fm["related"], ["'foo", 'a"b'])


if __name__ == "__main__":
    unittest.main()
