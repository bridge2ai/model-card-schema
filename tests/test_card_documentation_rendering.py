"""Evidence and uncertainty documentation must survive YAML-to-HTML export."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("card_renderer", ROOT / "src/html/human_readable_renderer.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


class DocumentationRenderingTests(unittest.TestCase):
    def test_source_and_uncertainty_documentation_survives_export(self):
        card = {
            "model_details": {
                "name": "Documented model",
                "version": {"last_updated": "2024-10-16T11:57:20Z"},
            },
            "model_parameters": {
                "training_procedure": {
                    "description": "Original training procedure is unverified.",
                    "methodology": "Fine-tuning methodology disclosure.",
                    "pre_training_info": "Base checkpoint lineage disclosure.",
                    "training_data_separate": False,
                    "reproducibility_info": {
                        "random_seed": 0,
                        "pipeline_url": "https://example.org/source/commit123",
                        "environment_config": "Unverified training environment.",
                        "hyperparameters": {"optimizer": "SGD"},
                    },
                },
            },
            # No metrics: an unknown-result caveat still needs to be visible.
            "quantitative_analysis": {
                "evaluation_procedure": {
                    "description": "Source-reported protocol only.",
                    "uncertainty_quantification": "Confidence intervals are not available.",
                    "evaluation_data_separate": False,
                },
            },
            "usage_documentation": {
                "installation_instructions": "Install declared dependencies.",
                "inference_configuration": "Pin the artifact revision before inference.",
                "code_examples": [{"code": 'print("example")\n', "code_language": "python"}],
            },
            "model_index": [{"name": "Source-reported benchmark", "results": [{
                "source": {"url": "https://example.org/benchmark/commit456"},
            }]}],
            "mission_relevance": {"description": "Institutional use requires confirmation."},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "documented.yaml"
            path.write_text(yaml.safe_dump(card))
            with patch.object(renderer, "find_badge_files", return_value=[]):
                page = renderer.render_card(path)
        for required in (
            "last_updated", "2024-10-16T11:57:20Z",
            "Fine-tuning methodology disclosure.", "Base checkpoint lineage disclosure.",
            "training_data_separate", "random_seed", "<code>0</code>", "<code>False</code>",
            "https://example.org/source/commit123", "Unverified training environment.", "SGD",
            "Evaluation procedure", "Source-reported protocol only.",
            "Confidence intervals are not available.", "evaluation_data_separate",
            "Usage Documentation", "Install declared dependencies.",
            "Pin the artifact revision before inference.", "print(&quot;example&quot;)",
            "Benchmark Index", "Source-reported benchmark", "https://example.org/benchmark/commit456",
            "Mission Relevance", "Institutional use requires confirmation.",
        ):
            with self.subTest(required=required):
                self.assertIn(required, page)

    def test_metrics_remain_visible_alongside_evaluation_procedure(self):
        output = renderer.render_quantitative_analysis({
            "performance_metrics": [{"type": "source accuracy", "value": 0, "unit": "%"}],
            "evaluation_procedure": {"uncertainty_quantification": "No error bounds supplied."},
        })
        self.assertIn("source accuracy", output)
        self.assertIn('<td class="num">0</td>', output)
        self.assertIn("No error bounds supplied.", output)
        self.assertEqual(output.count("<table"), output.count("</table>"))


if __name__ == "__main__":
    unittest.main()
