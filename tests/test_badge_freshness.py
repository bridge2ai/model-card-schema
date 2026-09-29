"""A model-card page must not present archived scores as a current evaluation."""
from __future__ import annotations

import base64
import hashlib
import importlib.util
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent.parent


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


badge_renderer = load_module("badge_renderer", "scripts/render_evaluation_html.py")
card_renderer = load_module("card_renderer", "src/html/human_readable_renderer.py")


class BadgeFreshnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.card = self.root / "example_model_card.yaml"
        # Hashes bind raw bytes, including line endings, not normalized YAML.
        self.card.write_bytes(b"model_details:\r\n  name: Example\r\n")
        self.card_hash = hashlib.sha256(self.card.read_bytes()).hexdigest()

    def write_badge(self, card_hash):
        report = {
            "model_card_file": str(self.card),
            "rubric": "mc_rubric10",
            "evaluator": {"name": "hybrid"},
            "overall_score": {"percentage": 80, "total_points": 40, "max_points": 50},
            "metadata": {"model_card_hash": card_hash},
        }
        written = badge_renderer.write_badges([report], self.root / "badges")
        return next(iter(written.values()))

    def render_with_badges(self, badges):
        with patch.object(card_renderer, "find_badge_files", return_value=badges):
            return card_renderer.render_card(self.card)

    def test_matching_hash_renders_portable_svg_bytes(self):
        for declared_hash in (self.card_hash, "sha256:" + self.card_hash.upper()):
            with self.subTest(declared_hash=declared_hash):
                badge = self.write_badge(declared_hash)
                self.assertEqual(ET.fromstring(badge.read_bytes()).get("data-model-card-sha256"), self.card_hash)
                page = self.render_with_badges([badge])
                data_urls = re.findall(r'src="data:image/svg\+xml;base64,([^"]+)"', page)
                self.assertEqual(len(data_urls), 1)
                self.assertEqual(base64.b64decode(data_urls[0]), badge.read_bytes())
                self.assertNotIn("Archived or unverified", page)

    def test_changed_yaml_omits_previously_matching_badge(self):
        badge = self.write_badge(self.card_hash)
        self.card.write_bytes(self.card.read_bytes() + b"# revised card\r\n")
        page = self.render_with_badges([badge])
        self.assertNotIn("data:image/svg+xml", page)
        self.assertIn("Archived or unverified evaluation badges are omitted", page)

    def test_missing_and_placeholder_hashes_are_not_stamped_or_displayed(self):
        for invalid_hash in (None, "", "n/a", "sha256:placeholder", "z" * 64):
            with self.subTest(invalid_hash=invalid_hash):
                badge = self.write_badge(invalid_hash)
                self.assertIsNone(ET.fromstring(badge.read_bytes()).get("data-model-card-sha256"))
                page = self.render_with_badges([badge])
                self.assertNotIn("data:image/svg+xml", page)
                self.assertIn("Archived or unverified", page)

    def test_mixed_fresh_and_archived_badges_display_only_fresh(self):
        fresh = self.write_badge(self.card_hash)
        archived = self.root / "example_model_card_rubric20_llm.svg"
        archived.write_text(badge_renderer.render_badge_svg("archived", "90%", "good"))
        page = self.render_with_badges([fresh, archived])
        self.assertEqual(page.count("data:image/svg+xml;base64,"), 1)
        self.assertNotIn('alt="example_model_card_rubric20_llm"', page)
        self.assertIn("Archived or unverified", page)

    def test_malformed_svg_is_omitted_without_breaking_page(self):
        badge = self.root / "broken.svg"
        badge.write_text("not an SVG")
        page = self.render_with_badges([badge])
        self.assertNotIn("data:image/svg+xml", page)
        self.assertIn("Archived or unverified", page)


if __name__ == "__main__":
    unittest.main()
