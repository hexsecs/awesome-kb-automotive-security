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

    def test_concept_nested_below_concepts_dir_is_still_a_concept(self):
        write(self.root, "wiki/concepts/deep/nested.md",
              "---\nrelated: [alpha]\n---\n\nBody.\n")
        r = self.report()
        self.assertEqual(r["concept_pages"], 2)
        self.assertIn("wiki/concepts/deep/nested.md",
                      [e["page"] for e in r["concept_inbound"]])
        self.assertNotIn("wiki/concepts/deep/nested.md", r["orphans"])

    def test_nested_concept_does_not_steal_an_entity_bare_slug(self):
        # A bare slug resolves to the ENTITY at wiki/<slug>.md. The tie-break
        # must classify concepts by the whole subtree (as the page classifier
        # does), not by the immediate parent; otherwise a concept nested at
        # wiki/concepts/deep/<slug>.md sorts first and steals the link.
        write(self.root, "wiki/ref.md",
              "---\nrelated: [foo]\n---\n\nBody.\n")
        write(self.root, "wiki/foo.md",
              "---\ntype: entity\nrelated: []\n---\n\nEntity foo.\n")
        write(self.root, "wiki/concepts/deep/foo.md",
              "---\ntype: concept\nrelated: []\n---\n\nConcept foo.\n")
        r = self.report()
        self.assertNotIn("wiki/foo.md", r["orphans"])
        nested = next(e for e in r["concept_inbound"]
                      if e["page"] == "wiki/concepts/deep/foo.md")
        self.assertEqual(nested["inbound"], 0)

    def test_self_link_does_not_count_as_inbound(self):
        # Orphans are pages with no inbound link from ANOTHER article.
        write(self.root, "wiki/a.md", "# A\n\nSee [self](a.md).\n")
        self.assertIn("wiki/a.md", self.report()["orphans"])
        write(self.root, "wiki/a.md", "---\nrelated: [a]\n---\n\n# A\n")
        self.assertIn("wiki/a.md", self.report()["orphans"])

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

    def test_invalid_last_type_does_not_keep_a_stale_concept_classification(self):
        # At root (not in concepts/), the only thing that could classify this
        # page as a concept is a stale first `type: concept`. YAML's last key
        # wins, and the last value here is invalid, so declared_type() must
        # return None and the audit must fall back to `entity`.
        frontmatter = "type: concept\ntype: not-a-type\n"
        self.assertIsNone(link_audit.declared_type(frontmatter))
        write(self.root, "wiki/can-injection.md",
              "---\n" + frontmatter + "---\n\nBody.\n")
        report = link_audit.audit(self.root)
        # make_kb contributes exactly one real concept: concepts/theme.md.
        self.assertEqual(report["concept_pages"], 1)
        self.assertNotIn("wiki/can-injection.md",
                         [e["page"] for e in report["concept_inbound"]])

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


class SweepElevenRegressionTests(unittest.TestCase):
    """Regressions for the eleventh sweep's bare-slug tie-break bugs."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        make_kb(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_concept_outside_concepts_tree_does_not_steal_entity_slug(self):
        # Concept identity is `type: concept`, not a directory name. A
        # concept filed under wiki/deep/ must not win the bare slug over the
        # canonical entity at wiki/<slug>.md.
        write(self.root, "wiki/deep/dup.md",
              "---\ntype: concept\nrelated: []\n---\n\nConcept clone.\n")
        write(self.root, "wiki/dup.md",
              "---\ntype: entity\nrelated: []\n---\n\nEntity.\n")
        write(self.root, "wiki/a-ref.md",
              "---\nrelated: [dup]\n---\n\nBody.\n")
        r = link_audit.audit(self.root)
        self.assertNotIn("wiki/dup.md", r["orphans"])
        self.assertEqual(
            next(e["inbound"] for e in r["concept_inbound"]
                 if e["page"] == "wiki/deep/dup.md"), 0)

    def test_canonical_concept_wins_bare_slug_over_a_clone(self):
        # Ingest's L1 and concept map name the flat wiki/concepts/ page for
        # a duplicated stem; the auditor must credit that same page instead
        # of a clone filed elsewhere.
        write(self.root, "wiki/concepts/zzclone.md",
              "---\ntype: concept\nrelated: []\n---\n\nCanonical.\n")
        # Nest the clone so plain str ordering puts it BEFORE the flat
        # canonical page (.../concepts/archive/... < .../concepts/zzclone).
        # With the canonical-preference keys removed the clone would win,
        # making this test actually pin row 180's guard.
        write(self.root, "wiki/concepts/archive/zzclone.md",
              "---\ntype: concept\nsummary: \"clone\"\nrelated: []\n---\n\nClone.\n")
        write(self.root, "wiki/zzlinker.md",
              "---\ntype: entity\nrelated: [zzclone]\n---\n\nBody.\n")
        r = link_audit.audit(self.root)
        inbound = {e["page"]: e["inbound"] for e in r["concept_inbound"]}
        self.assertEqual(inbound["wiki/concepts/zzclone.md"], 1)
        self.assertEqual(inbound["wiki/concepts/archive/zzclone.md"], 0)


class SweepTwelveRegressionTests(LinkAuditTest):
    """Regressions for the twelfth sweep's unreadable-page handling."""

    def test_unreadable_concept_does_not_steal_an_entity_bare_slug(self):
        # A chmod-000 page has no recoverable content, so the path fallback
        # must still classify it: at wiki/concepts/foo.md it would otherwise
        # sort before the entity and steal its bare-slug link.
        write(self.root, "wiki/concepts/foo.md",
              "---\ntype: concept\nrelated: []\n---\n\nConcept foo.\n")
        write(self.root, "wiki/foo.md",
              "---\ntype: entity\nrelated: []\n---\n\nEntity foo.\n")
        write(self.root, "wiki/linker.md",
              "---\ntype: entity\nrelated: [foo]\n---\n\nBody.\n")
        unreadable = self.root / "wiki" / "concepts" / "foo.md"
        unreadable.chmod(0o000)
        try:
            r = self.report()
        finally:
            unreadable.chmod(0o644)  # before tearDown removes the temp tree
        self.assertNotIn("wiki/foo.md", r["orphans"])
        self.assertEqual(
            next(e["inbound"] for e in r["concept_inbound"]
                 if e["page"] == "wiki/concepts/foo.md"), 0)

    def test_unreadable_concept_still_appears_in_coverage(self):
        theme = self.root / "wiki" / "concepts" / "theme.md"
        theme.chmod(0o000)
        try:
            r = self.report()
        finally:
            theme.chmod(0o644)
        self.assertEqual(r["counts"]["entities_without_concept_link"], 0)
        self.assertEqual(
            next(e["inbound"] for e in r["concept_inbound"]
                 if e["page"] == "wiki/concepts/theme.md"), 2)

    def test_undecodable_concept_keeps_its_type_for_classification(self):
        # A bad byte needs the lenient decode; the path fallback cannot help
        # a concept filed outside concepts/.
        write(self.root, "wiki/foo.md",
              "---\ntype: entity\nrelated: []\n---\n\nEntity foo.\n")
        write(self.root, "wiki/linker.md",
              "---\ntype: entity\nrelated: [foo]\n---\n\nBody.\n")
        d = self.root / "wiki" / "a"
        d.mkdir(exist_ok=True)
        (d / "foo.md").write_bytes(
            b'---\ntype: concept\nrelated: []\n---\n\n\xff bad\n')
        r = self.report()
        self.assertNotIn("wiki/foo.md", r["orphans"])
        self.assertEqual(
            next(e["inbound"] for e in r["concept_inbound"]
                 if e["page"] == "wiki/a/foo.md"), 0)


if __name__ == "__main__":
    unittest.main()
