#!/usr/bin/env python3
"""
Validation utility for Model Cards + Datasheets integration.

This script validates that model cards properly reference datasheets and that
referenced datasheets exist and are valid.

Usage:
    python utils/validate_integration.py model_card.yaml
    python utils/validate_integration.py model_card.yaml --datasheets-dir ./datasheets

Features:
    - Checks for dataset_documentation section
    - Validates datasheet references
    - Checks if referenced datasheet files exist
    - Validates basic datasheet structure
    - Reports missing or incomplete documentation
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List, Tuple
from urllib.parse import urlparse


def load_yaml(file_path: str) -> Dict[str, Any]:
    """Load YAML file."""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None


class ValidationResult:
    """Stores validation results."""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def add_error(self, message: str):
        self.errors.append(message)

    def add_warning(self, message: str):
        self.warnings.append(message)

    def add_info(self, message: str):
        self.info.append(message)

    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def print_results(self):
        """Print validation results."""
        print("\n" + "=" * 70)
        print("VALIDATION RESULTS")
        print("=" * 70)

        if self.info:
            print("\nℹ️  Information:")
            for msg in self.info:
                print(f"   {msg}")

        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for msg in self.warnings:
                print(f"   {msg}")

        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for msg in self.errors:
                print(f"   {msg}")
        else:
            print("\n✅ No errors found!")

        print("\n" + "=" * 70)

        if self.is_valid():
            print("OVERALL: ✅ VALID")
        else:
            print("OVERALL: ❌ INVALID")

        print("=" * 70)


def validate_datasheet_reference(ref: Dict[str, Any], result: ValidationResult):
    """Validate a single datasheet reference."""
    required_fields = ['id', 'name', 'datasheet_url']
    recommended_fields = ['datasheet_format', 'description']

    # Check required fields
    for field in required_fields:
        if field not in ref:
            result.add_error(f"Missing required field '{field}' in datasheet reference")

    # Check recommended fields
    for field in recommended_fields:
        if field not in ref:
            result.add_warning(f"Missing recommended field '{field}' in datasheet reference")

    # Validate URL format
    if 'datasheet_url' in ref:
        url = ref['datasheet_url']
        try:
            parsed = urlparse(url)
            if not parsed.scheme:
                result.add_warning(f"Datasheet URL '{url}' may be invalid (no scheme)")
        except Exception:
            result.add_error(f"Invalid datasheet URL: {url}")


def check_datasheet_file(datasheet_id: str, datasheets_dir: Path, result: ValidationResult) -> Dict[str, Any]:
    """Check if datasheet file exists and load it."""
    datasheet_file = datasheets_dir / f"{datasheet_id}.yaml"

    if not datasheet_file.exists():
        result.add_warning(
            f"Datasheet file not found: {datasheet_file} "
            f"(This is OK if datasheet is hosted remotely)"
        )
        return None

    result.add_info(f"Found local datasheet file: {datasheet_file}")
    data = load_yaml(str(datasheet_file))

    if data is None:
        result.add_error(f"Failed to load datasheet file: {datasheet_file}")
        return None

    return data


def validate_datasheet_content(datasheet: Dict[str, Any], datasheet_id: str, result: ValidationResult):
    """Validate datasheet content structure."""
    required_sections = [
        'id', 'name', 'description',
        'motivation', 'composition', 'collection',
        'ethics', 'preprocessing', 'uses',
        'distribution', 'maintenance'
    ]

    missing_sections = []
    for section in required_sections:
        if section not in datasheet:
            missing_sections.append(section)

    if missing_sections:
        result.add_warning(
            f"Datasheet '{datasheet_id}' is missing sections: {', '.join(missing_sections)}"
        )

    # Check for TODO markers (indicating incomplete documentation)
    datasheet_str = str(datasheet)
    if 'TODO' in datasheet_str:
        todo_count = datasheet_str.count('TODO')
        result.add_warning(
            f"Datasheet '{datasheet_id}' contains {todo_count} TODO marker(s) - "
            f"documentation is incomplete"
        )


def validate_model_card(model_card_path: str, datasheets_dir: Path) -> ValidationResult:
    """
    Validate a model card and its datasheet references.

    Returns ValidationResult object.
    """
    result = ValidationResult()

    # Load model card
    result.add_info(f"Loading model card: {model_card_path}")
    model_card = load_yaml(model_card_path)

    if model_card is None:
        result.add_error("Failed to load model card")
        return result

    # Check for dataset_documentation section
    if 'dataset_documentation' not in model_card:
        result.add_warning(
            "No 'dataset_documentation' section found. "
            "Consider adding datasheet references for datasets."
        )

        # Check if there's old-style data section
        if 'model_parameters' in model_card and 'data' in model_card['model_parameters']:
            result.add_info(
                "Found old-style 'model_parameters.data' section. "
                "Consider migrating to datasheet references using utils/migrate_to_harmonized.py"
            )
    else:
        dataset_doc = model_card['dataset_documentation']

        # Validate training datasets
        if 'training_datasets' in dataset_doc:
            training_datasets = dataset_doc['training_datasets']
            if not isinstance(training_datasets, list):
                training_datasets = [training_datasets]

            result.add_info(f"Found {len(training_datasets)} training dataset reference(s)")

            for i, ref in enumerate(training_datasets):
                result.add_info(f"Validating training dataset {i + 1}...")
                validate_datasheet_reference(ref, result)

                # Check if local datasheet file exists
                if 'id' in ref:
                    datasheet = check_datasheet_file(ref['id'], datasheets_dir, result)
                    if datasheet:
                        validate_datasheet_content(datasheet, ref['id'], result)

        # Validate evaluation datasets
        if 'evaluation_datasets' in dataset_doc:
            eval_datasets = dataset_doc['evaluation_datasets']
            if not isinstance(eval_datasets, list):
                eval_datasets = [eval_datasets]

            result.add_info(f"Found {len(eval_datasets)} evaluation dataset reference(s)")

            for i, ref in enumerate(eval_datasets):
                result.add_info(f"Validating evaluation dataset {i + 1}...")
                validate_datasheet_reference(ref, result)

                if 'id' in ref:
                    datasheet = check_datasheet_file(ref['id'], datasheets_dir, result)
                    if datasheet:
                        validate_datasheet_content(datasheet, ref['id'], result)

    # Check for migrated language field
    if 'language' in model_card:
        result.add_warning(
            "Found 'language' field - should be 'model_language' in harmonized schema. "
            "Run migration tool to update."
        )

    if 'model_language' in model_card:
        result.add_info("✓ Using 'model_language' field (harmonized schema)")

    return result


def main():
    """Main validation function."""
    if len(sys.argv) < 2:
        print("Usage: python utils/validate_integration.py model_card.yaml [--datasheets-dir DIR]")
        print()
        print("Validates Model Cards + Datasheets integration.")
        print()
        print("Options:")
        print("  --datasheets-dir DIR    Directory containing datasheet files (default: ./datasheets)")
        print()
        print("This tool checks:")
        print("  ✓ Presence of dataset_documentation section")
        print("  ✓ Valid datasheet references")
        print("  ✓ Local datasheet files (if available)")
        print("  ✓ Datasheet content completeness")
        print("  ✓ Migration status (language → model_language)")
        sys.exit(1)

    model_card_file = sys.argv[1]

    # Parse datasheets directory
    datasheets_dir = Path('datasheets')
    if '--datasheets-dir' in sys.argv:
        idx = sys.argv.index('--datasheets-dir')
        if idx + 1 < len(sys.argv):
            datasheets_dir = Path(sys.argv[idx + 1])

    print("Model Cards + Datasheets Integration Validator")
    print("=" * 70)
    print(f"Model Card: {model_card_file}")
    print(f"Datasheets Directory: {datasheets_dir}")
    print("=" * 70)

    # Validate
    result = validate_model_card(model_card_file, datasheets_dir)

    # Print results
    result.print_results()

    # Exit with appropriate code
    sys.exit(0 if result.is_valid() else 1)


if __name__ == '__main__':
    main()
