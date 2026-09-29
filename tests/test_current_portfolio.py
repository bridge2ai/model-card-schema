"""Exercise archive/current selection through the actual portfolio Make target."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("evaluation_renderer", ROOT / "scripts/render_evaluation_html.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


def report(card: Path, digest: str, *, score=47, rubric="rubric10", timestamp="2026-09-28T00:00:00Z"):
    return {
        "model_card_file": str(card), "rubric": "mc_" + rubric,
        "evaluator": {"name": "hybrid-heuristic-evaluator"},
        "evaluation_timestamp": timestamp,
        "metadata": {"model_card_hash": digest},
        "overall_score": {"percentage": score * 2, "total_points": score, "max_points": 50},
    }


class CurrentSelectionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.card = Path(self.directory.name) / "card.yaml"
        self.card.write_bytes(b"model_details: {name: Current model}\n")
        self.digest = hashlib.sha256(self.card.read_bytes()).hexdigest()

    def test_old_or_unverified_evaluations_cannot_replace_current_report(self):
        fresh = report(self.card, self.digest)
        stale = report(self.card, "a" * 64, score=41, timestamp="2026-12-01T00:00:00Z")
        unverified = dict(report(self.card, "n/a"), evaluator={"name": "llm"})
        for inputs in ([fresh, stale, unverified], [unverified, stale, fresh]):
            selected = renderer.select_current_reports(inputs)
            self.assertEqual(len(selected), 1)
            self.assertEqual(selected[0]["overall_score"]["total_points"], 47)

    def test_newest_matching_result_wins_independent_of_input_order(self):
        older = report(self.card, self.digest, score=46)
        newer = report(self.card, "sha256:" + self.digest, score=48, timestamp="2026-09-29T00:00:00Z")
        for inputs in ([older, newer], [newer, older]):
            selected = renderer.select_current_reports(inputs)
            self.assertEqual(selected[0]["overall_score"]["total_points"], 48)

    def test_stale_only_hybrid_requires_fresh_evaluation(self):
        with self.assertRaisesRegex(ValueError, "No current hybrid evaluation"):
            renderer.select_current_reports([report(self.card, "a" * 64)])

    def test_same_timestamp_conflicting_scores_fail_instead_of_using_input_order(self):
        left = report(self.card, self.digest, score=46)
        right = report(self.card, self.digest, score=48)
        for inputs in ([left, right], [right, left]):
            with self.assertRaisesRegex(ValueError, "Conflicting current scores"):
                renderer.select_current_reports(inputs)
        self.assertEqual(len(renderer.select_current_reports([left, left])), 1)

    def test_distinct_inputs_cannot_collide_at_a_badge_filename(self):
        other = self.card.parent / "different" / self.card.name
        other.parent.mkdir()
        other.write_bytes(self.card.read_bytes())
        with self.assertRaisesRegex(ValueError, "badge name collision"):
            renderer.select_current_reports([report(self.card, self.digest), report(other, self.digest)])

    def test_unique_basename_alias_groups_with_full_path(self):
        full = report(self.card, self.digest)
        alias = dict(report(Path(self.card.name), self.digest), evaluator={"name": "llm"})
        selected = renderer.select_current_reports([full, alias])
        self.assertEqual(len(selected), 2)
        self.assertEqual(selected[0]["model_card_file"], selected[1]["model_card_file"])


class PortfolioMakeTests(unittest.TestCase):
    def test_default_target_preserves_archives_and_emits_current_scores(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            (fixture / "scripts").mkdir()
            for name in ("Makefile", "project.Makefile", "scripts/render_evaluation_html.py"):
                shutil.copy2(ROOT / name, fixture / name)
            source = Path("data/model_cards_assistant/densenet121_tv_in1k_model_card.yaml")
            card = fixture / source
            card.parent.mkdir(parents=True)
            card.write_text("model_details: {name: Current model}\n")
            digest = hashlib.sha256(card.read_bytes()).hexdigest()
            archived = {}
            for rubric in ("rubric10", "rubric20"):
                filename = f"{source.stem}_evaluation.json"
                old = fixture / "data/evaluation/hf_hub" / rubric / filename
                old.parent.mkdir(parents=True)
                old.write_text(json.dumps(report(source, "a" * 64, rubric=rubric, score=41)))
                archived[old] = old.read_bytes()
                current = fixture / "data/evaluation/remediation/2026-09-28/after" / rubric / filename
                current.parent.mkdir(parents=True)
                current.write_text(json.dumps(report(source, digest, rubric=rubric, score=47)))
                archived[current] = current.read_bytes()
            old_dashboard = fixture / "data/evaluation/all/portfolio.html"
            old_dashboard.parent.mkdir(parents=True)
            old_dashboard.write_text("Archived dashboard must stay unchanged.")
            archived[old_dashboard] = old_dashboard.read_bytes()
            env = dict(os.environ, PATH=str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", ""))
            command = ["make", "compare-portfolio", "RUN=", "SCHEMA_NAME=test", "SOURCE_SCHEMA_PATH=unused.yaml"]
            result = subprocess.run(command, cwd=fixture, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for rubric in ("rubric10", "rubric20"):
                badge = fixture / "data/evaluation/badges" / f"{source.stem}_{rubric}_hybrid.svg"
                root = ET.fromstring(badge.read_bytes())
                self.assertEqual(root.get("data-model-card-sha256"), digest)
                self.assertIn("47/50", root.find("{http://www.w3.org/2000/svg}title").text)
            self.assertTrue((fixture / "data/evaluation/current/portfolio/portfolio.html").is_file())
            for path, content in archived.items():
                self.assertEqual(path.read_bytes(), content)
            # A later audit uses the separate current tree, not the archived paths.
            staged = fixture / "data/evaluation/current/hf_hub/rubric10/fresh_evaluation.json"
            staged.parent.mkdir(parents=True)
            staged.write_text(json.dumps(report(source, digest, score=48, timestamp="2026-09-29T00:00:00Z")))
            result = subprocess.run(command, cwd=fixture, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            updated = fixture / "data/evaluation/badges" / f"{source.stem}_rubric10_hybrid.svg"
            self.assertIn("48/50", ET.parse(updated).getroot().find("{http://www.w3.org/2000/svg}title").text)
            for path, content in archived.items():
                self.assertEqual(path.read_bytes(), content)
            # A card edit must fail before replacing any previously generated badge.
            badge_bytes = {p: p.read_bytes() for p in (fixture / "data/evaluation/badges").glob("*.svg")}
            card.write_text("model_details: {name: Revised again}\n")
            result = subprocess.run(command, cwd=fixture, env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("No current hybrid evaluation", result.stderr)
            for path, content in badge_bytes.items():
                self.assertEqual(path.read_bytes(), content)


if __name__ == "__main__":
    unittest.main()
