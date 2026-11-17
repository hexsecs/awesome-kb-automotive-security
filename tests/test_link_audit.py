#!/usr/bin/env python3
"""Stdlib unittest suite for tools/link_audit.py using temp-dir fixtures."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import link_audit  # noqa: E402


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_kb(root: Path) -> None:
    write(root, "index.md", "# KB\n\n- [Alpha](wiki/alpha.md)\n")
    write(root, "wiki/index-sub.md", "# Sub\n\n- [Alpha](alpha.md)\n")
    write(root, "wiki/alpha.md",
          "---\nrelated: [beta, theme]\n---\n\n"
          "See [Beta](beta.md) and [Theme](concepts/theme.md).\n")
    write(root, "wiki/beta.md",
          "---\nrelated: [alpha, theme]\n---\n\n"
          "See [Alpha](alpha.md) and [Theme](concepts/theme.md).\n")
    write(root, "wiki/concepts/theme.md",
          "---\nrelated: [alpha, beta]\n---\n\n"
          "Synthesis over [Alpha](../alpha.md) and [Beta](../beta.md).\n")


class LinkAuditTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        make_kb(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def report(self):
        return link_audit.audit(self.root)

    def test_clean_kb_has_no_orphans_or_one_way_pairs(self):
        r = self.report()
        self.assertEqual(r["counts"]["orphans"], 0)
        self.assertEqual(r["counts"]["entities_without_concept_link"], 0)
        self.assertEqual(r["counts"]["one_way_related_pairs"], 0)
        self.assertEqual(r["concept_pages"], 1)

    def test_index_pages_are_not_orphans(self):
        r = self.report()
        self.assertNotIn("index.md", r["orphans"])
        self.assertNotIn("wiki/index-sub.md", r["orphans"])

    def test_article_with_no_inbound_is_orphan(self):
        write(self.root, "wiki/lonely.md",
              "---\nrelated: [alpha]\n---\n\nBody.\n")
        r = self.report()
        self.assertIn("wiki/lonely.md", r["orphans"])
        self.assertIn("wiki/lonely.md", r["entities_without_concept_link"])

    def test_one_way_related_pair_is_detected(self):
        # beta stops linking back to alpha.
        write(self.root, "wiki/beta.md",
              "---\nrelated: []\n---\n\nSee [Alpha](alpha.md).\n")
        r = self.report()
        pairs = [(e["source"], e["target"]) for e in r["one_way_related_pairs"]]
        self.assertIn(("wiki/alpha.md", "wiki/beta.md"), pairs)

    def test_concept_inbound_count_is_counted(self):
        r = self.report()
        theme = next(e for e in r["concept_inbound"]
                     if e["page"] == "wiki/concepts/theme.md")
        # alpha and beta both link to the concept.
        self.assertEqual(theme["inbound"], 2)


if __name__ == "__main__":
    unittest.main()
