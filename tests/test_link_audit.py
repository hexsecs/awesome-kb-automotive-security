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

    def test_generated_index_inbound_does_not_hide_an_orphan(self):
        # A generated sub-index links to lonely.md, but no article does.
        write(self.root, "wiki/index-sub.md",
              "# Sub\n\n- [Lonely](lonely.md)\n")
        write(self.root, "wiki/lonely.md",
              "---\ntype: entity\nrelated: []\n---\n\nBody.\n")
        r = self.report()
        self.assertIn("wiki/lonely.md", r["orphans"])


class AuditRobustnessTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        make_kb(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_duplicate_stem_resolution_is_deterministic(self):
        write(self.root, "wiki/dup.md", "---\nrelated: []\n---\n\nEntity.\n")
        write(self.root, "wiki/concepts/dup.md",
              "---\nrelated: [alpha, beta]\n---\n\nConcept.\n")
        write(self.root, "wiki/a-ref.md", "---\nrelated: [dup]\n---\n\nBody.\n")
        results = [link_audit.audit(self.root) for _ in range(5)]
        counts = {
            next(e["inbound"] for e in r["concept_inbound"]
                 if e["page"] == "wiki/concepts/dup.md")
            for r in results
        }
        # The entity wiki/dup.md (not the concept) receives the bare-slug link.
        self.assertEqual(counts, {0})
        for r in results:
            self.assertNotIn("wiki/dup.md", r["orphans"])

    def test_declared_entity_type_beats_index_prefix(self):
        write(self.root, "wiki/index-utils.md",
              "---\ntype: entity\nrelated: []\n---\n\nBody.\n")
        r = link_audit.audit(self.root)
        self.assertIn("wiki/index-utils.md", r["orphans"])

    def test_quoted_declared_type_beats_index_prefix(self):
        for quote in ('"', "'"):
            with self.subTest(quote=quote):
                p = self.root / "wiki" / "index-utils.md"
                p.write_text(
                    f"---\ntype: {quote}entity{quote}\nrelated: []\n---\n\nBody.\n",
                    encoding="utf-8")
                r = link_audit.audit(self.root)
                self.assertIn("wiki/index-utils.md", r["orphans"])
                self.assertEqual(r["entity_pages"], 3)

    def test_bad_root_fails_instead_of_passing_empty(self):
        self.assertEqual(link_audit.main(["--root", str(self.root / "nope")]), 2)

    def test_nul_target_is_recorded_without_aborting_the_audit(self):
        write(self.root, "wiki/nul.md", "See [x](wiki/null%00.md).\n")
        write(self.root, "index.md",
              "# KB\n\n- [A](wiki/alpha.md)\n- [N](wiki/nul.md)\n")
        report = link_audit.audit(self.root)  # must not raise
        self.assertGreaterEqual(report["pages_scanned"], 4)

    def test_existing_dir_without_index_md_is_rejected(self):
        (self.root / "index.md").unlink()
        self.assertEqual(link_audit.main(["--root", str(self.root)]), 2)

    def test_duplicate_stem_resolution_is_deterministic_across_seeds(self):
        import json
        import os
        import subprocess

        write(self.root, "wiki/dup.md", "---\nrelated: []\n---\n\nEntity.\n")
        write(self.root, "wiki/concepts/dup.md",
              "---\nrelated: [alpha, beta]\n---\n\nConcept.\n")
        write(self.root, "wiki/a-ref.md", "---\nrelated: [dup]\n---\n\nBody.\n")
        script = (
            "import sys, json\n"
            "from pathlib import Path\n"
            f"sys.path.insert(0, {str(REPO / 'tools')!r})\n"
            "import link_audit\n"
            f"r = link_audit.audit(Path({str(self.root)!r}))\n"
            "concept = [e for e in r['concept_inbound'] "
            "if e['page'].endswith('/dup.md')]\n"
            "print(json.dumps({'concept_inbound': concept, "
            "'entity_orphan': 'wiki/dup.md' in r['orphans']}))\n"
        )
        outputs = []
        for seed in range(10):
            env = dict(os.environ, PYTHONHASHSEED=str(seed))
            out = subprocess.run(
                [sys.executable, "-c", script], env=env,
                capture_output=True, text=True, check=True,
            )
            outputs.append(out.stdout.strip())
        self.assertEqual(set(outputs), {outputs[0]},
                         f"cross-seed drift: {outputs}")
        # A bare slug names the ENTITY (wiki/dup.md), not the same-stemmed
        # concept that happens to sort first. The entity gets the inbound and
        # is no longer an orphan; the concept gets none.
        result = json.loads(outputs[0])
        self.assertEqual(result["concept_inbound"][0]["inbound"], 0)
        self.assertFalse(result["entity_orphan"])

    def test_declared_type_uses_last_top_level_value(self):
        write(self.root, "wiki/dup-type.md",
              "---\ntype: concept\ntype: entity\n---\n\nBody.\n")
        write(self.root, "index.md",
              "# KB\n\n- [A](wiki/alpha.md)\n- [D](wiki/dup-type.md)\n")
        report = link_audit.audit(self.root)
        self.assertIn("wiki/dup-type.md", report["entities_without_concept_link"])
        self.assertNotIn("wiki/dup-type.md",
                         [e["page"] for e in report["concept_inbound"]])

    def test_quoted_type_with_trailing_comment_uses_last_top_level_value(self):
        write(self.root, "wiki/quoted-comment.md",
              "---\ntype: entity\ntype: \"concept\" # last wins in YAML\n"
              "---\n\nBody.\n")
        write(self.root, "index.md",
              "# KB\n\n- [A](wiki/alpha.md)\n- [Q](wiki/quoted-comment.md)\n")
        report = link_audit.audit(self.root)
        self.assertIn("wiki/quoted-comment.md",
                      [e["page"] for e in report["concept_inbound"]])
        self.assertNotIn("wiki/quoted-comment.md",
                         report["entities_without_concept_link"])

    def test_tab_indented_type_does_not_override(self):
        write(self.root, "wiki/tab-type.md",
              "---\ntype: entity\n\ttype: concept\n---\n\nBody.\n")
        write(self.root, "index.md",
              "# KB\n\n- [A](wiki/alpha.md)\n- [T](wiki/tab-type.md)\n")
        report = link_audit.audit(self.root)
        self.assertIn("wiki/tab-type.md", report["entities_without_concept_link"])


if __name__ == "__main__":
    unittest.main()
