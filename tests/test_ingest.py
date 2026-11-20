#!/usr/bin/env python3
"""Stdlib unittest suite for the ingest triage classifier."""

from __future__ import annotations

import sys
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


if __name__ == "__main__":
    unittest.main()
