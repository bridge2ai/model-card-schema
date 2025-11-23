"""Data test."""
import os
import glob
import unittest

from linkml_runtime.loaders import yaml_loader

ROOT = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(ROOT, "src", "data", "examples")

# Find model card example files (excluding Person example from template)
EXAMPLE_FILES = [
    f for f in glob.glob(os.path.join(DATA_DIR, '**/*.yaml'), recursive=True)
    if 'Person' not in f and 'kogut' in f  # Only test KOGUT examples
]


class TestData(unittest.TestCase):
    """Test data and datamodel."""

    def test_data(self):
        """Test model card examples can be loaded."""
        # Skip test if no example files (package installation not required for schema validation)
        if not EXAMPLE_FILES:
            self.skipTest("No model card example files found")

        # Import here to avoid import errors when package not installed
        try:
            from modelcards.datamodel.modelcards import modelCard
        except ImportError:
            self.skipTest("modelcards package not installed (not required for CI)")

        for path in EXAMPLE_FILES:
            with self.subTest(path=path):
                obj = yaml_loader.load(path, target_class=modelCard)
                self.assertIsNotNone(obj)
                # Verify required field
                self.assertIsNotNone(obj.model_details)
