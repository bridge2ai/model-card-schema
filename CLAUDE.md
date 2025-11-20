# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LinkML schema repository for Model Cards as described in the paper "Model Cards for Model Reporting" (https://arxiv.org/abs/1810.03993). Model Cards provide standardized documentation for trained machine learning models including benchmarks, applicable contexts, and demographic considerations.

The project uses the LinkML (Linked Data Modeling Language) framework to define schemas that can be automatically compiled into multiple target formats (JSON Schema, Python datamodels, SQL, GraphQL, OWL, etc.).

## Architecture

### Schema Source Files

**Primary Schema**: **`src/linkml/modelcards.yaml`** - Comprehensive LinkML schema incorporating:
- **Google Model Card Toolkit v0.0.2** - Complete implementation with all core classes
- **HuggingFace Model Cards** - Community metadata fields (framework, pipeline_tag, base_model, etc.)
- **Papers with Code** - Benchmark integration (model-index structure)

The schema includes 27 classes organized into functional groups:

**Core Metadata**: Version, License, owner, Reference, Citation
**Model Details**: ModelDetails (with overview, documentation, owners, version, licenses, references, citations)
**Datasets**: dataSet, SensitiveData, GraphicsCollection, graphic
**Model Parameters**: ModelParameters, KeyVal
**Performance**: performanceMetric, ConfidenceInterval, QuantitativeAnalysis
**Considerations**: User, UseCase, Limitation, Tradeoff, risk, Considerations
**Benchmarking**: Task, BenchmarkDataset, BenchmarkMetric, BenchmarkSource, BenchmarkResult, ModelIndex
**Root**: modelCard

**Legacy Schema**: `src/modelcards/schema/modelcards.yaml` exists but is a minimal stub version.

**IMPORTANT**: The `about.yaml` configuration references `src/model_card_schema/schema/model_card_schema.yaml` but this path does NOT exist. The actual schema paths use `modelcards` (not `model_card_schema`). This discrepancy means some make targets may not work correctly.

### Generated Artifacts

The `project/` directory contains auto-generated files and should NEVER be edited directly:
- `project/jsonschema/` - JSON Schema files
- `project/protobuf/` - Protocol Buffer definitions
- `project/sqlschema/` - SQL DDL
- `project/owl/` - OWL ontology
- `project/graphql/` - GraphQL schema
- `project/shex/`, `project/shacl/` - Shape expressions
- `project/excel/` - Excel representation

### Python Datamodel

Generated Python classes are in `src/modelcards/datamodel/modelcards.py` and should not be edited directly. They are regenerated from the LinkML schema via `make gen-project`.

## Common Commands

### Build and Generation

```bash
# Generate all project artifacts from schema
make gen-project

# Generate documentation
make gendoc

# Generate everything (project + docs)
make all

# Build and serve documentation locally
make testdoc
```

### Testing

```bash
# Run all tests (schema validation + Python tests + example validation)
make test

# Run only Python unit tests
make test-python

# Run schema validation
make test-schema

# Validate example data files
make test-examples
```

### Development

```bash
# Install dependencies with Poetry
make install

# Lint the schema
make lint

# Serve docs locally (on http://127.0.0.1:8000)
make serve
```

### Schema Updates

When modifying the LinkML schema in `src/linkml/modelcards.yaml`:

1. Edit the schema YAML file
2. Run `poetry run gen-project -d project src/linkml/modelcards.yaml` to generate artifacts
3. Run `cp project/modelcards.py src/modelcards/datamodel/` to update Python datamodel
4. Run `poetry run linkml-lint src/linkml/modelcards.yaml` to validate the schema
5. Run `make gendoc` to update documentation

**Note**: Direct usage of `make gen-project` may fail due to path discrepancies in `about.yaml`. Use the direct `poetry run gen-project` command instead.

### Google Sheets Integration

The project is configured to compile schemas from Google Sheets:

```bash
# Compile schema from Google Sheets (requires Sheet ID in about.yaml)
make compile-sheets
```

## Dependency Management

This project uses **Poetry** for Python dependency management:

- Dependencies are defined in `pyproject.toml`
- Lock file is `poetry.lock`
- All commands should be run via `poetry run` (the Makefile handles this with `RUN = poetry run`)

## Testing

The test suite in `tests/test_data.py` loads example YAML files from `src/data/examples/` and validates them against the Python datamodel using `linkml_runtime.loaders.yaml_loader`.

To add new test cases, place valid YAML examples in `src/data/examples/`.

## Documentation

Documentation is built with MkDocs Material theme:
- Configuration: `mkdocs.yml`
- Source markdown: `src/docs/`
- Generated docs: `docs/` (created by `make gendoc`)
- Published to: https://bbop.github.io/model-card-schema

## Schema Coverage

The enhanced schema provides comprehensive model card capabilities:

### Google Model Card Toolkit v0.0.2 (100% coverage)
- Complete ModelDetails with version, license, citations
- Full ModelParameters with architecture, data, I/O formats
- QuantitativeAnalysis with metrics and confidence intervals
- Considerations with users, use cases, limitations, tradeoffs, ethical risks
- Graphics support with base64 PNG encoding

### HuggingFace/Community Integration
- Framework metadata (framework, framework_version, library_name)
- Task classification (pipeline_tag)
- Language support
- Fine-tuning provenance (base_model)
- Discovery metadata (tags, datasets, metrics)

### Papers with Code Benchmark Integration
- Complete model-index structure
- Task, dataset, and metric specifications
- Source attribution
- Leaderboard compatibility

## Important Notes

- The project follows the LinkML project cookiecutter structure
- Never edit files in `project/` directory - they are auto-generated
- The schema name discrepancy (`model_card_schema` in config vs `modelcards` in actual files) may cause issues with some make targets
- Generated Python datamodels must be manually copied to `src/modelcards/datamodel/` after generation
- The schema passes linting with minor naming convention warnings (stylistic only, not functional)
- Runtime dependencies (linkml-runtime, jsonasobj2) required for Python datamodel usage
