"""Tests for the deterministic semantic rules in the rubric20 hybrid evaluator.

Covers Q18 (train/eval data leakage) and Q19 (bias declared without a matching
fairness tradeoff). Each test asserts both the helper's boolean return and the
end-to-end cap applied by `evaluate_one`.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import batch_evaluate_mc_rubric20_hybrid as evaluator  # noqa: E402


def _write_card(tmpdir: str, name: str, payload: dict) -> Path:
    path = Path(tmpdir) / name
    path.write_text(yaml.safe_dump(payload, sort_keys=False))
    return path


def _q_score(result: dict, qid: int) -> int:
    for cat in result["categories"]:
        for q in cat["questions"]:
            if q["id"] == qid:
                return q["score"]
    raise KeyError(f"Q{qid} not found in result")


class TrainEvalLeakageTests(unittest.TestCase):
    def test_disjoint_datasets_no_leakage(self):
        card = {
            "model_parameters": {
                "training_datasets": [{"name": "IMDb reviews"}],
                "evaluation_datasets": [{"name": "SST-2"}],
            },
        }
        flagged, reason = evaluator.detect_train_eval_leakage(card)
        self.assertFalse(flagged, reason)

    def test_exact_name_match_flags_leakage(self):
        card = {
            "model_parameters": {
                "training_datasets": [{"name": "ImageNet-1k"}],
                "evaluation_datasets": [{"name": "ImageNet-1k"}],
            },
        }
        flagged, reason = evaluator.detect_train_eval_leakage(card)
        self.assertTrue(flagged)
        self.assertIn("imagenet-1k", reason.lower())

    def test_substring_overlap_flags_leakage(self):
        """E.g. training='ImageNet-1k (ILSVRC2012)', eval='ImageNet-1k validation'."""
        card = {
            "model_parameters": {
                "data": [{"name": "ImageNet-1k (ILSVRC2012)"}],
            },
            "quantitative_analysis": {
                "performance_metrics": [
                    {"type": "top-1", "value": 74.4, "slice": "ImageNet-1k validation"},
                ],
            },
        }
        flagged, _ = evaluator.detect_train_eval_leakage(card)
        self.assertTrue(flagged)

    def test_version_tail_stripped_before_compare(self):
        """'E3SM v2 High-Resolution' should normalize to overlap with 'Test set (E3SM v2)'."""
        card = {
            "model_parameters": {
                "training_datasets": [{"name": "E3SM v2 High-Resolution"}],
                "evaluation_datasets": [{"name": "Test set (E3SM v2)"}],
            },
        }
        flagged, _ = evaluator.detect_train_eval_leakage(card)
        self.assertTrue(flagged)

    def test_no_eval_datasets_no_false_positive(self):
        card = {"model_parameters": {"training_datasets": [{"name": "IMDb"}]}}
        flagged, _ = evaluator.detect_train_eval_leakage(card)
        self.assertFalse(flagged)

    def test_model_index_dataset_overlap(self):
        card = {
            "model_parameters": {"training_datasets": [{"name": "GLUE"}]},
            "model_index": [
                {"results": [{"dataset": {"name": "GLUE"}, "metrics": []}]},
            ],
        }
        flagged, _ = evaluator.detect_train_eval_leakage(card)
        self.assertTrue(flagged)


class BiasTradeoffGapTests(unittest.TestCase):
    def test_no_bias_declared_no_gap(self):
        card = {
            "considerations": {"tradeoffs": [{"description": "size vs latency"}]},
        }
        flagged, _ = evaluator.detect_bias_tradeoff_gap(card)
        self.assertFalse(flagged)

    def test_bias_declared_no_tradeoffs_flags_as_gap(self):
        """Per the rubric20-semantic agent spec, an empty tradeoffs[] when
        bias_model/bias_output is declared IS a gap — the cap fires
        unconditionally. (Previous behavior deferred to the base presence
        rule; PR #27 review flagged that as too lenient.)"""
        card = {"bias_model": "Inherits ImageNet demographic skew"}
        flagged, reason = evaluator.detect_bias_tradeoff_gap(card)
        self.assertTrue(flagged, "Should flag empty tradeoffs as bias-vs-fairness gap")
        self.assertIn("empty", reason.lower())

    def test_bias_declared_tradeoffs_omit_fairness_flags_gap(self):
        card = {
            "bias_model": "Inherits ImageNet demographic skew.",
            "bias_output": "Uncalibrated class prior.",
            "considerations": {
                "tradeoffs": [
                    {"description": "Parameter count vs wall-clock latency"},
                    {"description": "DenseNet-121 vs ResNet-50 throughput"},
                ]
            },
        }
        flagged, reason = evaluator.detect_bias_tradeoff_gap(card)
        self.assertTrue(flagged, reason)

    def test_bias_declared_with_fairness_tradeoff_passes(self):
        card = {
            "bias_model": "Inherits ImageNet demographic skew.",
            "considerations": {
                "tradeoffs": [
                    {"description": "Higher accuracy on majority classes; fairness on rare classes degraded."},
                ]
            },
        }
        flagged, _ = evaluator.detect_bias_tradeoff_gap(card)
        self.assertFalse(flagged)

    def test_keyword_disparity_counts_as_fairness_mention(self):
        card = {
            "bias_output": "Output skews toward Western names.",
            "considerations": {
                "tradeoffs": [{"description": "Throughput optimized; demographic disparity tolerated."}],
            },
        }
        flagged, _ = evaluator.detect_bias_tradeoff_gap(card)
        self.assertFalse(flagged)


class EvaluateOneCappingTests(unittest.TestCase):
    """Integration: a card that would score 5 on Q18/Q19 gets capped to 3 and
    a semantic_deductions entry appears in overall_score."""

    def _full_card(self, **overrides) -> dict:
        """A card crafted to score 5 on Q18 (≥2 metrics, ≥2 slices, CI) and 5
        on Q19 (all three of limitations/tradeoffs/oos populated as lists)."""
        card = {
            "model_details": {
                "name": "Test Model",
                "overview": "x" * 600,
                "licenses": [{"identifier": "MIT"}],
                "version": {"name": "v1.0.0", "date": "2026-01-01"},
            },
            "model_parameters": {
                "model_architecture": "transformer",
                "input_format": "tokens",
                "output_format": "logits",
            },
            "quantitative_analysis": {
                "performance_metrics": [
                    {"type": "acc", "value": 0.9, "slice": "test-A", "confidence_interval": "0.88-0.92"},
                    {"type": "f1", "value": 0.85, "slice": "test-B"},
                ],
            },
            "considerations": {
                "limitations": [{"description": "limited to English"}],
                "tradeoffs": [{"description": "size vs latency"}],
                "out_of_scope_uses": [{"description": "not for medical use"}],
            },
        }
        card.update(overrides)
        return card

    def _evaluate(self, card: dict) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_card(tmp, "card.yaml", card)
            return evaluator.evaluate_one(path)

    def test_clean_card_no_caps(self):
        result = self._evaluate(self._full_card())
        self.assertEqual(result["overall_score"]["semantic_deductions"], [])
        self.assertGreaterEqual(_q_score(result, 18), 4)
        self.assertEqual(_q_score(result, 19), 5)

    def test_q18_capped_when_training_dataset_overlaps_eval_slice(self):
        card = self._full_card()
        card["model_parameters"]["training_datasets"] = [{"name": "ImageNet-1k"}]
        card["quantitative_analysis"]["performance_metrics"] = [
            {"type": "top-1", "value": 0.74, "slice": "ImageNet-1k validation",
             "confidence_interval": "0.73-0.75"},
            {"type": "top-5", "value": 0.92, "slice": "ImageNet-1k val-clean"},
        ]
        result = self._evaluate(card)
        self.assertEqual(_q_score(result, 18), 3, "Q18 must be capped to 3")
        deds = result["overall_score"]["semantic_deductions"]
        self.assertEqual(len(deds), 1)
        self.assertEqual(deds[0]["question"], "Q18")
        self.assertEqual(deds[0]["rule"], "train_eval_leakage")
        self.assertEqual(deds[0]["raw_score"], 5)
        self.assertEqual(deds[0]["capped_score"], 3)

    def test_q19_capped_when_bias_declared_but_tradeoffs_omit_fairness(self):
        card = self._full_card()
        card["bias_model"] = "Inherits ImageNet demographic skew."
        card["bias_output"] = "Uncalibrated class prior."
        # tradeoffs already populated in _full_card() with no fairness mention
        result = self._evaluate(card)
        self.assertEqual(_q_score(result, 19), 3, "Q19 must be capped to 3")
        deds = result["overall_score"]["semantic_deductions"]
        self.assertEqual(len(deds), 1)
        self.assertEqual(deds[0]["question"], "Q19")
        self.assertEqual(deds[0]["rule"], "bias_tradeoff_gap")
        self.assertEqual(deds[0]["raw_score"], 5)

    def test_both_rules_can_fire_simultaneously(self):
        card = self._full_card()
        card["model_parameters"]["training_datasets"] = [{"name": "ImageNet-1k"}]
        card["quantitative_analysis"]["performance_metrics"] = [
            {"type": "top-1", "value": 0.74, "slice": "ImageNet-1k validation",
             "confidence_interval": "0.73-0.75"},
            {"type": "top-5", "value": 0.92, "slice": "ImageNet-1k val-clean"},
        ]
        card["bias_model"] = "Demographic skew inherited from training data."
        result = self._evaluate(card)
        self.assertEqual(_q_score(result, 18), 3)
        self.assertEqual(_q_score(result, 19), 3)
        rules = {d["rule"] for d in result["overall_score"]["semantic_deductions"]}
        self.assertEqual(rules, {"train_eval_leakage", "bias_tradeoff_gap"})

    def test_cap_does_not_raise_a_low_score(self):
        """If the base scorer already returns ≤3, the cap is a no-op."""
        card = self._full_card()
        # Make Q19 score 3 via the base rule (drop tradeoffs/oos so only
        # limitations populated)
        card["considerations"] = {
            "limitations": [{"description": "limited"}],
        }
        card["bias_output"] = "skew"
        # Add at least one tradeoff so the gap detector even runs
        card["considerations"]["tradeoffs"] = [{"description": "size vs cost"}]
        result = self._evaluate(card)
        self.assertLessEqual(_q_score(result, 19), 3)


if __name__ == "__main__":
    unittest.main()
