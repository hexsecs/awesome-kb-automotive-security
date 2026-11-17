#!/usr/bin/env python3
"""Stdlib unittest suite for the navigation taxonomy and backfill tool."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

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


class BackfillTests(unittest.TestCase):
    def test_inline_related_is_normalised_and_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "example.md"
            page.write_text(
                '---\nuid: 01\ntitle: "Example"\nsummary: "CAN tool."\n'
                'type: entity\ncategory: "Tools"\nrelated: [alpha, beta]\n'
                '---\n\nBody text.\n', encoding="utf-8")
            self.assertTrue(backfill_navigation.backfill(page, check=False))
            first = page.read_text(encoding="utf-8")
            self.assertIn("related:\n  - alpha\n  - beta", first)
            self.assertIn("facets: [", first)
            self.assertFalse(backfill_navigation.backfill(page, check=False))
            self.assertEqual(page.read_text(encoding="utf-8"), first)
            self.assertTrue(first.endswith("---\n\nBody text.\n"))

    def test_blank_lines_in_frontmatter_are_preserved_on_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "example.md"
            page.write_text(
                '---\ntitle: "Example"\nsummary: "A tool."\n'
                '---\n\nBody.\n', encoding="utf-8")
            backfill_navigation.backfill(page, check=False)
            self.assertIn("\n---\n\nBody.\n", page.read_text(encoding="utf-8"))


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


if __name__ == "__main__":
    unittest.main()
