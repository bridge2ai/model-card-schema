# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LinkML schema repository for Model Cards as described in the paper "Model Cards for Model Reporting" (https://arxiv.org/abs/1810.03993). Model Cards provide standardized documentation for trained machine learning models including benchmarks, applicable contexts, and demographic considerations.

The project uses the LinkML (Linked Data Modeling Language) framework to define schemas that can be automatically compiled into multiple target formats (JSON Schema, Python datamodels, SQL, GraphQL, OWL, etc.).

**Current Status**: The schema has been comprehensively enhanced to 100% Google Model Card Toolkit v0.0.2 coverage plus HuggingFace and Papers with Code integration. **Phase 1 D4D harmonization is COMPLETED** with the external reference pattern implemented in `model_card_schema_d4dharmonized.yaml` and comprehensive examples provided.

## Architecture

### Schema Source Files

#### Production Schemas (LinkML Cookiecutter Standard Paths)

**Primary Schema**: **`src/model_card_schema/schema/model_card_schema.yaml`** (~1,515 lines, 34 classes)
- **Google Model Card Toolkit v0.0.2** - Complete 100% implementation
- **HuggingFace Model Cards** - Community metadata (framework, pipeline_tag, base_model, tags, datasets, metrics)
- **Papers with Code** - Benchmark integration (model-index structure)
- **DOE Extended Template** - Complete coverage for scientific models (compute infrastructure, reproducibility, mission relevance)

The schema includes 34 classes organized into 8 functional groups:

1. **Core Metadata** (7): Version, License, owner, Reference, Citation, Contributor, ContributorRoleEnum
2. **Model Details** (1): ModelDetails (with extended template: short_description, contributors, compute_infrastructure, mission_relevance)
3. **Datasets** (4): dataSet, SensitiveData, GraphicsCollection, graphic
4. **Model Parameters** (2): ModelParameters, KeyVal
5. **Performance** (3): performanceMetric, ConfidenceInterval, QuantitativeAnalysis
6. **Considerations** (7): User, UseCase, Limitation, Tradeoff, risk, Considerations, OutOfScopeUse
7. **Benchmarking** (6): Task, BenchmarkDataset, BenchmarkMetric, BenchmarkSource, BenchmarkResult, ModelIndex
8. **Extended Template** (8): Contributor, ComputeInfrastructure, Hyperparameters, ReproducibilityInfo, CodeExample, UsageDocumentation, MissionRelevance, TrainingProcedure, EvaluationProcedure

**D4D Harmonized Schema**: **`src/model_card_schema/schema/model_card_schema_d4dharmonized.yaml`** (~1,500 lines, 31 classes)
- **PRODUCTION-READY** implementation using external reference pattern
- **NO schema imports** - avoids naming conflicts
- Replaces simple classes with D4D references:
  - `owner` → `CreatorReference` (links to D4D Creator instances)
  - `Contributor` → `CreatorReference` (with D4D CRediT roles)
  - `dataSet` → `DatasetReference` (links to D4D Dataset instances with 60+ classes, 200+ fields)
  - `funding_source` → `GrantReference` (links to D4D Grant instances)
- Adds provenance tracking (created_by, modified_by, created_on, modified_on) at modelCard and ModelDetails levels
- **Preserves ALL extended template features** (compute infrastructure, reproducibility, DOE mission relevance)
- See `src/data/examples/d4d_integration/` for complete examples
- See `INTEGRATION_GUIDE.md` for implementation details

**Configuration**: The `about.yaml` file correctly points to `src/model_card_schema/schema/model_card_schema.yaml` (LinkML cookiecutter standard path).

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

### Implementation Status

- **Phase 1** (COMPLETED ✅): D4D harmonization using external reference pattern
  - Created `model_card_schema_d4dharmonized.yaml` production schema
  - Implemented CreatorReference, DatasetReference, GrantReference classes
  - Added provenance metadata (created_by, modified_by, timestamps)
  - Created comprehensive examples in `src/data/examples/d4d_integration/`
  - Updated INTEGRATION_GUIDE.md with implementation details
- **Phase 2-4** (Future): Full schema import approach (after resolving remaining naming conflicts)

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

### D4D Harmonization (COMPLETED ✅)

**Phase 1 COMPLETED** (November 23, 2025):
- ✅ Production D4D harmonized schema (`model_card_schema_d4dharmonized.yaml`)
- ✅ External reference pattern implemented (no schema imports/conflicts)
- ✅ Three new reference classes: CreatorReference, DatasetReference, GrantReference
- ✅ Provenance metadata support (created_by, modified_by, created_on, modified_on)
- ✅ Comprehensive examples (`src/data/examples/d4d_integration/`):
  - Climate forecasting model card
  - D4D Creator instances (Person, Organization)
  - D4D Dataset instance (comprehensive 60+ fields)
  - D4D Grant instance (DOE SciDAC example)
  - Complete README with usage guide
- ✅ Updated documentation (INTEGRATION_GUIDE.md)
- ✅ Preserved ALL extended template features

**Available Schemas**:
- **`model_card_schema.yaml`** - Base schema without D4D integration
- **`model_card_schema_d4dharmonized.yaml`** - D4D harmonized schema (recommended for new projects)

**Current Recommendation**: Use `model_card_schema_d4dharmonized.yaml` for new projects requiring comprehensive dataset/creator documentation. Use `model_card_schema.yaml` for simpler use cases.

## Important Notes

- The project follows the LinkML project cookiecutter structure
- Never edit files in `project/` directory - they are auto-generated
- Generated Python datamodels must be manually copied to `src/model_card_schema/datamodel/` after generation
- The schema passes linting with minor naming convention warnings (stylistic only, not functional)
- Runtime dependencies (linkml-runtime, jsonasobj2) required for Python datamodel usage
- **Two production schemas available**:
  - **`model_card_schema.yaml`** - Base schema (Google MCT + HuggingFace + Papers with Code + DOE Extended Template)
  - **`model_card_schema_d4dharmonized.yaml`** - D4D harmonized schema (external reference pattern, comprehensive dataset/creator docs)

## Model Card Extended Template

### Branch: `schema-extend`

The schema has been extended on the `schema-extend` branch to provide **100% coverage** for DOE scientific models through an extended template. This extended template emphasizes compute infrastructure, reproducibility, and mission relevance for scientific computing applications.

### Extensions Overview

**Schema Size**: ~1,500 lines (from 967 baseline)
**New Classes**: 10 extended template classes
**Enhanced Classes**: 6 existing classes
**New Slots**: ~40 new fields
**New Enums**: 1 (ContributorRoleEnum)

### New Classes (10)

1. **Contributor** - Role-based contributor attribution
   - Fields: name, role (ContributorRoleEnum), email, orcid, affiliation
   - Replaces/enhances simple `owner` class
   - Example: `{name: "Jane Doe", role: developed_by, orcid: "https://orcid.org/0000-0002-1234-5678"}`

2. **ComputeInfrastructure** - Hardware/software used for training
   - Fields: hardware, hardware_list, software, software_dependencies, training_speed
   - Captures DOE facility information (NERSC, ALCF, OLCF)
   - Example: `hardware_list: ["64 nodes × 4 NVIDIA A100 GPUs", "NERSC Perlmutter"]`

3. **Hyperparameters** - Complete training hyperparameters
   - Fields: optimizer, learning_rate, batch_size, training_epochs, training_steps, etc.
   - Supports LLM-specific fields (prompting_template, fine_tuning_method)
   - Example: `{optimizer: AdamW, learning_rate: 0.0001, batch_size: 512}`

4. **ReproducibilityInfo** - Reproducibility documentation
   - Fields: random_seed, environment_config, pipeline_url, hyperparameters
   - Example: `{random_seed: 42, hyperparameters: {...}}`

5. **CodeExample** - Code snippets with language
   - Fields: code, code_language, description
   - Example: `{code: "import torch...", code_language: python}`

6. **UsageDocumentation** - Installation and usage
   - Fields: installation_instructions, training_configuration, inference_configuration, code_examples
   - Supports conda/docker/SLURM workflows

7. **MissionRelevance** - DOE mission alignment
   - Fields: doe_project, doe_facility, funding_source, description
   - Example: `{doe_facility: "NERSC Perlmutter", doe_project: "Climate Model Development"}`

8. **OutOfScopeUse** - Prohibited uses
   - Fields: description
   - Example: `{description: "Not for real-time weather forecasting"}`

9. **TrainingProcedure** - Training methodology
   - Fields: description, methodology, reproducibility_info, pre_training_info, training_data_separate
   - Nested hyperparameters and reproducibility info

10. **EvaluationProcedure** - Evaluation methodology
    - Fields: description, benchmarks, baselines, sota_comparison, uncertainty_quantification, evaluation_data_separate
    - Example: Benchmark comparisons, SOTA references, uncertainty analysis

### Enhanced Classes (6)

1. **Version** - Added `last_updated`, `superseded_by`
2. **License** - Added `license_name`, `license_link` for custom licenses
3. **ModelDetails** - Added `short_description`, `contributors` (role-based)
4. **ModelParameters** - Added `compute_infrastructure`, `training_procedure`
5. **QuantitativeAnalysis** - Added `evaluation_procedure`
6. **Considerations** - Added `out_of_scope_uses`

### New Root-Level Fields (2)

Added to `modelCard` class:
- `mission_relevance` (MissionRelevance)
- `usage_documentation` (UsageDocumentation)

### Extended Template Coverage

| Template Section | Schema Mapping | Coverage |
|---------------|----------------|----------|
| Model Details → Description | `model_details.short_description` | ✅ 100% |
| Model Details → Developed By | `model_details.contributors` (role: developed_by) | ✅ 100% |
| Model Details → Shared By | `model_details.contributors` (role: contributed_by) | ✅ 100% |
| Model Details → Version | `model_details.version` (enhanced) | ✅ 100% |
| Model Details → License | `model_details.licenses` (enhanced) | ✅ 100% |
| Compute Infrastructure → Hardware | `compute_infrastructure.hardware_list` | ✅ 100% |
| Compute Infrastructure → Software | `compute_infrastructure.software_dependencies` | ✅ 100% |
| Training → Dataset | `model_parameters.data` | ✅ 100% |
| Training → Procedure | `model_parameters.training_procedure` | ✅ 100% |
| Training → Reproducibility | `training_procedure.reproducibility_info` | ✅ 100% |
| Training → Hyperparameters | `reproducibility_info.hyperparameters` | ✅ 100% |
| Evaluation → Metrics | `quantitative_analysis.performance_metrics` | ✅ 100% |
| Evaluation → Procedure | `quantitative_analysis.evaluation_procedure` | ✅ 100% |
| Uses → Intended Uses | `considerations.use_cases` | ✅ 100% |
| Uses → Out-of-Scope | `considerations.out_of_scope_uses` | ✅ 100% |
| Limitations | `considerations.limitations` | ✅ 100% |
| Ethical Considerations | `considerations.ethical_considerations` | ✅ 100% |
| DOE Mission Relevance | `mission_relevance` | ✅ 100% |
| Usage Documentation | `usage_documentation` | ✅ 100% |

**Overall Coverage**: ✅ **100%**

### Examples

**Extended Template Example**: `src/data/examples/extended/climate-model-extended.yaml`
- Complete ClimateNet-v2 model card
- Demonstrates all extended template features
- Realistic DOE scientific model (climate AI)
- Includes:
  - Role-based contributors with ORCID
  - NERSC Perlmutter compute infrastructure
  - Complete hyperparameters (optimizer, learning rate, batch size, etc.)
  - Reproducibility info (random seed, environment)
  - DOE mission relevance (BER funding, NERSC facility)
  - Complete usage documentation (conda/docker/SLURM)
  - Code examples in Python and Bash

**Example Documentation**: `src/data/examples/extended/README.md`
- Complete extended template feature documentation
- Before/after migration examples
- Coverage table
- Validation instructions

### Validation

Schema validates successfully with linkml-lint:
```bash
poetry run linkml-lint src/linkml/modelcards.yaml
```

Only non-blocking naming convention warnings (same as baseline).

### Use Cases

The extended template is ideal for:

1. **DOE Scientific Models**
   - Climate models (E3SM, CESM, MPAS)
   - Materials science, fusion, bioinformatics
   - Any model trained at DOE facilities

2. **HPC/Supercomputing Applications**
   - Models trained on NERSC Perlmutter, ALCF Polaris/Aurora, OLCF Frontier
   - Large-scale distributed training
   - Petabyte-scale datasets

3. **Reproducible Science**
   - Complete environment specifications
   - Random seeds and hyperparameters
   - Training pipeline URLs
   - Detailed methodology

4. **DOE Mission-Aligned Projects**
   - Office of Science grants (BER, ASCR, NP, HEP)
   - Facility-specific documentation
   - Funding transparency

### Backward Compatibility

All extended template features are **fully backward compatible**:
- Existing model cards remain valid
- Extended fields are optional
- Legacy `owner` class preserved (alongside new `contributors`)
- No breaking changes to existing schema

### Migration Path

To upgrade an existing model card with extended template features:

1. **Add contributors** (optional, recommended):
   ```yaml
   model_details:
     contributors:
       - name: "Jane Doe"
         role: developed_by
         orcid: "https://orcid.org/0000-0002-1234-5678"
   ```

2. **Add compute infrastructure** (optional):
   ```yaml
   model_parameters:
     compute_infrastructure:
       hardware_list: ["64 × NVIDIA A100 GPUs"]
       software_dependencies: "pytorch=2.1.0\nhorovod=0.28.1"
   ```

3. **Add reproducibility info** (optional):
   ```yaml
   model_parameters:
     training_procedure:
       reproducibility_info:
         random_seed: 42
         hyperparameters:
           optimizer: AdamW
           learning_rate: 0.0001
   ```

4. **Add DOE mission relevance** (optional):
   ```yaml
   mission_relevance:
     doe_facility: "NERSC Perlmutter"
     doe_project: "My DOE Project"
   ```

5. **Add usage documentation** (optional):
   ```yaml
   usage_documentation:
     installation_instructions: "pip install my-model"
     code_examples:
       - code: "import my_model"
         code_language: "python"
   ```

### Related Files

- **Schema**: `src/linkml/modelcards.yaml` (on `schema-extend` branch)
- **Template Source**: `data/input_docs/KOGUT/model-card.md` (original LBNL DOE KOGUT template - path preserved for historical reference)
- **Example**: `src/data/examples/extended/climate-model-extended.yaml`
- **Example Docs**: `src/data/examples/extended/README.md`
