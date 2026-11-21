#!/usr/bin/env python3
"""Regression tests for tools/concept_scan.py hardening. Stdlib only."""

import contextlib
import importlib.util
import io
import os
import shutil
import subprocess
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
            # The target is INSIDE the root so the containment check passes:
            # only the explicit is_symlink() guard can skip this page. An
            # out-of-root target was skipped by containment anyway, making
            # this test pass even with the symlink guard removed.
            real = root / "real.md"
            real.write_text(
                '---\ntype: entity\ntitle: "Real"\nsummary: "real"\n---\n\nBody.\n',
                encoding="utf-8",
            )
            (root / "alpha.md").symlink_to(real)
            out = run_scan(root)
            self.assertIn("1 entity pages", out)


class HardeningTests(unittest.TestCase):
    def test_generic_filter_has_no_whitespace(self):
        # Word tokens are produced by TOKEN_RE and can never contain spaces;
        # an entry with one is unreachable dead weight.
        bad = [word for word in concept_scan.GENERIC if not word.isalnum()
               and "-" not in word]
        self.assertEqual(bad, [], f"malformed GENERIC entries: {bad}")
        self.assertGreater(len(concept_scan.GENERIC), 10,
                           "an empty filter silently changes candidate output")

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
    def test_duplicate_stems_are_both_counted(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for rel in ("normal.md", "sub/normal.md", "other.md"):
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    '---\ntype: entity\ntitle: "Entity"\nsummary: "s"\n---\nbody\n',
                    encoding="utf-8")
            self.assertIn("3 entity pages", run_scan(root))

    def test_concept_type_page_outside_concepts_dir_is_excluded(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name in ("a", "b"):
                (root / f"{name}.md").write_text(
                    '---\ntype: entity\ntitle: "A deep theme"\n'
                    'summary: "deep theme in the vehicle"\n---\nbody\n',
                    encoding="utf-8")
            deep = root / "topics" / "deep-theme.md"
            deep.parent.mkdir()
            deep.write_text(
                '---\ntype: concept\ntitle: "Deep Theme"\n---\nbody\n',
                encoding="utf-8")
            out = run_scan(root)
            self.assertIn("1 existing concepts", out)
            self.assertNotIn("| deep theme ", out)

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

    def test_index_named_and_nested_entities_are_scanned(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for rel in ("normal.md", "index-of-tools.md", "topics/sub.md"):
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    '---\ntype: entity\ntitle: "Entity"\nsummary: "s"\n'
                    '---\n\nBody.\n', encoding="utf-8")
            self.assertIn("3 entity pages", run_scan(root))

    def test_fifo_named_md_does_not_block_the_scan(self):
        if not hasattr(os, "mkfifo"):
            self.skipTest("mkfifo unavailable")
        with tempfile.TemporaryDirectory() as d:
            kb = Path(d) / "kb"
            (kb / "tools").mkdir(parents=True)
            for f in TOOLS.parent.glob("*.py"):
                shutil.copy2(f, kb / "tools" / f.name)
            (kb / "wiki").mkdir()
            (kb / "index.md").write_text("# KB\n", encoding="utf-8")
            (kb / "wiki" / "a.md").write_text(
                '---\ntype: entity\ntitle: "A"\nsummary: "s"\n---\nbody\n',
                encoding="utf-8")
            os.mkfifo(kb / "wiki" / "fifo.md")
            result = subprocess.run(
                [sys.executable, "tools/concept_scan.py"], cwd=kb,
                capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0)
            self.assertNotIn("fifo.md", result.stderr)


class ExistingConceptTests(unittest.TestCase):
    """A concept must suppress its own theme regardless of spelling."""

    def scan(self, root, *args):
        saved = (concept_scan.ROOT, concept_scan.WIKI, sys.argv)
        concept_scan.ROOT, concept_scan.WIKI = root, root
        sys.argv = ["concept_scan", *args]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                concept_scan.main()
        finally:
            concept_scan.ROOT, concept_scan.WIKI, sys.argv = saved
        return buf.getvalue()

    def corpus(self, root, theme, count=3):
        for i in range(14):
            (root / f"f{i}.md").write_text(
                f'---\ntype: entity\ntitle: "Filler{i}"\n'
                f'summary: "unique filler{i}"\n---\nbody\n',
                encoding="utf-8")
        for i in range(count):
            (root / f"e{i}.md").write_text(
                f'---\ntype: entity\ntitle: "Scheme{i}"\n'
                f'summary: "uses {theme} in diagnostics"\n---\nbody\n',
                encoding="utf-8")

    def test_hyphenated_concept_suppresses_its_theme(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.corpus(root, "iso-tp")
            before = self.scan(root, "--min-pages", "3")
            self.assertIn("| iso-tp |", before)
            concepts = root / "concepts"
            concepts.mkdir()
            (concepts / "iso-tp.md").write_text(
                '---\ntype: concept\ntitle: "ISO TP"\n---\nbody\n',
                encoding="utf-8")
            after = self.scan(root, "--min-pages", "3")
            self.assertIn("1 existing concepts", after)
            self.assertNotIn("| iso-tp |", after)

    def test_entity_in_concepts_dir_is_not_counted_as_a_concept(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.corpus(root, "iso-tp")
            concepts = root / "concepts"
            concepts.mkdir()
            (concepts / "stray.md").write_text(
                '---\ntype: entity\ntitle: "Stray"\nsummary: "s"\n---\nbody\n',
                encoding="utf-8")
            out = self.scan(root, "--min-pages", "3")
            self.assertIn("0 existing concepts", out)
            # An entity's vocabulary must not be suppressed as if it were a
            # concept's own theme.
            self.assertIn("| iso-tp |", out)

    def test_case_variant_concept_suppresses_its_theme(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            # Uppercase in the corpus makes `tpm` a real single-word theme
            # (an acronym); a lowercase corpus would never propose it and
            # the assertion would pass even with the guard removed.
            self.corpus(root, "TPM")
            (root / "concepts").mkdir()
            (root / "concepts" / "TPM.md").write_text(
                '---\ntype: concept\ntitle: "TPM"\n---\nbody\n',
                encoding="utf-8")
            out = self.scan(root, "--min-pages", "3")
            self.assertIn("1 existing concepts", out)
            self.assertNotIn("| tpm |", out)


class SweepTwelveRegressionTests(unittest.TestCase):
    """Regressions for the twelfth sweep's acronym and pruning bugs."""

    def scan(self, root, *args):
        saved = (concept_scan.ROOT, concept_scan.WIKI, sys.argv)
        concept_scan.ROOT, concept_scan.WIKI = root, root
        sys.argv = ["concept_scan", *args]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                concept_scan.main()
        finally:
            concept_scan.ROOT, concept_scan.WIKI, sys.argv = saved
        return buf.getvalue()

    def page(self, root, name, summary):
        (root / f"{name}.md").write_text(
            f'---\ntype: entity\ntitle: "{name}"\n'
            f'summary: "{summary}"\n---\nbody\n', encoding="utf-8")

    def themes(self, out):
        return [ln.split("|")[1].strip() for ln in out.splitlines()
                if ln.startswith("| ") and "Candidate" not in ln
                and "---" not in ln]

    def test_uppercase_acronym_that_is_also_a_stopword_survives(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for i in range(60):
                self.page(root, f"f{i}", f"unique filler{i}")
            for i in range(8):
                self.page(root, f"p{i}", f"CAN bus intrusion dataset {i}")
            out = self.scan(root, "--min-pages", "3", "--top", "10")
            # Lowercasing before the stopword check erased CAN entirely;
            # the corpus itself flags CAN as an acronym, so it must survive.
            self.assertTrue(any(t.startswith("can") for t in self.themes(out)),
                            out)

    def test_subphrase_duplicate_is_collapsed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for i in range(20):
                self.page(root, f"f{i}", f"unique filler{i}")
            for i in range(6):
                self.page(root, f"h{i}", f"uses ISO-TP diagnostics {i}")
            for i in range(6):
                self.page(root, f"s{i}", f"uses ISO TP diagnostics {i}")
            out = self.scan(root, "--min-pages", "3", "--top", "25")
            themes = self.themes(out)
            # Each spelling is one family; the base/subphrase duplicates
            # ("iso diagnostics" inside "uses iso diagnostics") must not
            # all be reported alongside it.
            self.assertFalse({"iso", "iso diagnostics",
                              "uses iso diagnostics"} <= set(themes), out)
            self.assertFalse({"iso-tp", "iso-tp diagnostics",
                              "uses iso-tp diagnostics"} <= set(themes), out)
            self.assertLessEqual(len(themes), 4, out)


class SweepThirteenRegressionTests(SweepTwelveRegressionTests):
    """Regressions for the thirteenth sweep's theme pruning."""

    def test_generic_words_stay_filtered_even_when_uppercase(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for i in range(60):
                self.page(root, f"f{i}", f"unique filler{i}")
            for i in range(6):
                self.page(root, f"u{i}", f"USENIX workshop proceedings {i}")
            for i in range(6):
                self.page(root, f"e{i}", f"ECU firmware note {i}")
            out = self.scan(root, "--min-pages", "3", "--top", "10")
            themes = set(self.themes(out))
            # GENERIC is absolute; the sweep-12 acronym carve-out belongs
            # to STOPWORDS (CAN), not to this filter.
            self.assertNotIn("ecu", themes, out)
            self.assertNotIn("usenix", themes, out)

    def test_specific_theme_is_not_pruned_by_a_string_prefix(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for i in range(100):
                self.page(root, f"f{i}", f"unique filler{i}")
            for i in range(10):
                self.page(root, f"g{i}", f"TPM module research {i}")
            # The specific-theme pages must ALSO mention the broad theme,
            # so its page set is a strict superset and the prefix rule fires.
            for i in range(6):
                self.page(root, f"t{i}",
                          f"TPM module research and TPM2 attestation {i}")
            out = self.scan(root, "--min-pages", "3", "--top", "25")
            # `tpm2` starts with `tpm` as a string but is a distinct theme.
            self.assertIn("tpm2", self.themes(out), out)


if __name__ == "__main__":
    unittest.main()
