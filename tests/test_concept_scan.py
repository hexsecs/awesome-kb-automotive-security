#!/usr/bin/env python3
"""Regression tests for tools/concept_scan.py hardening. Stdlib only."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools" / "concept_scan.py"
spec = importlib.util.spec_from_file_location("concept_scan", TOOLS)
concept_scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(concept_scan)


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


if __name__ == "__main__":
    unittest.main()
