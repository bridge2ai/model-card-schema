# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LinkML schema repository for Model Cards as described in the paper "Model Cards for Model Reporting" (https://arxiv.org/abs/1810.03993). Model Cards provide standardized documentation for trained machine learning models including benchmarks, applicable contexts, and demographic considerations.

The project uses the LinkML (Linked Data Modeling Language) framework to define schemas that can be automatically compiled into multiple target formats (JSON Schema, Python datamodels, SQL, GraphQL, OWL, etc.).

**Current Status**: The schema has been comprehensively enhanced to 100% Google Model Card Toolkit v0.0.2 coverage plus HuggingFace and Papers with Code integration. A harmonization analysis with the Datasheets for Datasets schema has been completed, with a proposed harmonized schema available.

## Architecture

### Schema Source Files

**Primary Schema**: **`src/linkml/modelcards.yaml`** (967 lines, 27 classes)
- **Google Model Card Toolkit v0.0.2** - Complete 100% implementation
- **HuggingFace Model Cards** - Community metadata (framework, pipeline_tag, base_model, tags, datasets, metrics)
- **Papers with Code** - Benchmark integration (model-index structure)

The schema includes 27 classes organized into 8 functional groups:

1. **Core Metadata** (5): Version, License, owner, Reference, Citation
2. **Model Details** (1): ModelDetails (overview, documentation, owners, version, licenses, references, citations, path)
3. **Datasets** (4): dataSet, SensitiveData, GraphicsCollection, graphic
4. **Model Parameters** (2): ModelParameters, KeyVal
5. **Performance** (3): performanceMetric, ConfidenceInterval, QuantitativeAnalysis
6. **Considerations** (6): User, UseCase, Limitation, Tradeoff, risk, Considerations
7. **Benchmarking** (5): Task, BenchmarkDataset, BenchmarkMetric, BenchmarkSource, BenchmarkResult, ModelIndex
8. **Root** (1): modelCard

**Harmonized Schema**: **`src/linkml/modelcards_harmonized.yaml`** (1,200+ lines)
- Proposed schema integrating with Datasheets for Datasets
- Imports datasheets schema for comprehensive dataset documentation (60+ classes)
- Replaces simple `owner` with datasheets Creator/Person/Organization (ORCID, CRediT roles)
- Replaces simple `dataSet` with datasheets Dataset reference (most critical change)
- Adds provenance tracking (created_by, modified_by, timestamps, was_derived_from)
- Adds funding and maintainer references
- Enhanced ethics with datasheets PrivacyAndSecurity
- Includes comprehensive migration guide and inline documentation
- See `ALIGNMENT_ANALYSIS.md` for detailed rationale

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

## Harmonization with Datasheets for Datasets

### Documentation

**ALIGNMENT_ANALYSIS.md** (50,000+ words) - Comprehensive analysis documenting:
- Element-by-element comparison between model cards and datasheets schemas
- 9 category alignment analysis (metadata, creators, licensing, datasets, privacy, ethics, uses, versioning, file formats)
- Overall alignment: ~25% (excluding model-specific elements)
- Critical gap: Model cards has minimal dataset documentation (1 class, 7 fields) vs datasheets' comprehensive framework (60+ classes, 200+ fields)

### Seven Harmonization Actions

1. **Replace `owner` → datasheets `Creator`** - Use Person/Organization with ORCID, CRediT roles
2. **Replace `dataSet` → datasheets `Dataset`** - Most critical: leverage comprehensive dataset documentation
3. **Enhanced Licensing** - Add datasheets LicensingAndIntellectualProperty for IP/regulatory controls
4. **Enhanced Ethics** - Reference datasheets PrivacyAndSecurity for GDPR/CCPA compliance
5. **Provenance Tracking** - Add created_by, modified_by, timestamps, was_derived_from
6. **Funding Information** - Reference datasheets Grant for transparency
7. **Maintainer Information** - Distinguish creators from current maintainers

### Implementation Roadmap

- **Phase 1** (Months 1-2): Foundation - Import datasheets, add new slots
- **Phase 2** (Months 3-6): Core harmonization - Implement creator/dataset replacements
- **Phase 3** (Months 7-8): Advanced features - Ethics, provenance, funding integration
- **Phase 4** (Month 9): Ecosystem integration - Release v2.0

### Key Benefit

Single source of truth: Datasets documented once with datasheets (comprehensive 60+ class framework), referenced by many model cards. Eliminates duplication while maintaining model-specific focus.

## Related Repository

**Datasheets for Datasets Schema**: `/Users/marcin/Documents/VIMSS/ontology/bridge2ai/data-sheets-schema/`
- Schema location: `src/data_sheets_schema/schema/data_sheets_schema_all.yaml`
- 22,459 lines, 60+ classes for comprehensive dataset documentation
- Based on "Datasheets for Datasets" framework (Gebru et al., 2018)

## Datasheets Integration Implementation

### Documentation Suite

**Primary Guides**:
- **MIGRATION_GUIDE.md** - Step-by-step migration guide for users (start here)
- **INTEGRATION_GUIDE.md** - Technical integration patterns and roadmap
- **ALIGNMENT_ANALYSIS.md** - Comprehensive 50,000+ word schema analysis

### Utilities (`utils/`)

**Migration Tool** - `utils/migrate_to_harmonized.py`:
- Automates conversion of existing model cards
- Creates datasheet stubs for each dataset
- Handles `language` → `model_language` renaming
- Preserves backward compatibility
- Usage: `python utils/migrate_to_harmonized.py input.yaml output.yaml`

**Validation Tool** - `utils/validate_integration.py`:
- Validates model cards and datasheet references
- Checks datasheet completeness (TODO markers)
- Verifies migration status
- Usage: `python utils/validate_integration.py model_card.yaml`

See `utils/README.md` for complete tool documentation.

### Integration Examples (`src/data/examples/harmonized/`)

**sentiment-classifier-with-datasheet-refs.yaml**:
- Complete model card using Pattern 1 (external references)
- Shows how to reference datasheets without schema imports
- Demonstrates backward compatibility

**imdb-sentiment-datasheet-v1.yaml**:
- Complete dataset documentation using Datasheets format
- Shows all major sections (60+ fields)
- Referenced by the model card example

**README.md**:
- Usage guide and integration workflows
- Pattern comparisons
- Validation instructions

### Integration Approach (Implemented)

**Phase 1** (COMPLETED):
- ✅ External references pattern (no schema conflicts)
- ✅ Migration and validation utilities
- ✅ Complete examples and documentation
- ✅ Naming conflicts identified and documented

**Phase 2-4** (Future):
- Resolve remaining naming conflicts (language slot)
- Full schema import support
- Advanced tooling and validation

**Current Recommendation**: Use Pattern 1 (external references) for immediate adoption.

## Important Notes

- The project follows the LinkML project cookiecutter structure
- Never edit files in `project/` directory - they are auto-generated
- The schema name discrepancy (`model_card_schema` in config vs `modelcards` in actual files) may cause issues with some make targets
- Generated Python datamodels must be manually copied to `src/modelcards/datamodel/` after generation
- The schema passes linting with minor naming convention warnings (stylistic only, not functional)
- Runtime dependencies (linkml-runtime, jsonasobj2) required for Python datamodel usage
- Three versions available:
  - `modelcards.yaml` - Current production schema
  - `modelcards_harmonized.yaml` - Proposed harmonized schema (conceptual, has naming conflicts)
  - External reference pattern (recommended) - See examples in `src/data/examples/harmonized/`
