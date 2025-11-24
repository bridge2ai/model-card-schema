# Model Cards + Datasheets Integration Guide

**Version**: 2.0
**Date**: November 23, 2025
**Status**: Phase 1 COMPLETED - D4D Harmonization Implemented

---

## Executive Summary

This guide documents the successful integration of Model Cards with Datasheets for Datasets (D4D) using the **external reference pattern**. This approach provides comprehensive dataset and creator documentation while avoiding schema import conflicts.

**Implementation Status**: The D4D harmonized schema (`model_card_schema_d4dharmonized.yaml`) is complete and ready for use, with comprehensive examples in `src/data/examples/d4d_integration/`.

**Key Achievement**: Upgraded from simple dataset documentation (7 fields) to comprehensive Datasheets coverage (60+ classes, 200+ fields) through external references.

---

## Naming Conflicts Identified

When importing the datasheets schema into model cards, the following naming conflicts occur:

| Element | Model Cards Usage | Datasheets Usage | Resolution Strategy |
|---------|-------------------|------------------|---------------------|
| **`Task`** | Benchmark task specification (e.g., "text-generation") | Dataset task/purpose | Rename to `BenchmarkTask` in model cards |
| **`language`** | Natural language(s) processed by model | Dataset language/locale | Rename to `model_language` in model cards |
| **Other potential conflicts** | TBD during implementation | TBD during implementation | Document as discovered |

### Conflict Details

#### 1. Task Class Conflict

**Model Cards `Task` class**:
```yaml
Task:
  description: ML task specification for benchmarking
  slots:
    - type  # e.g., "text-generation", "image-classification"
    - name  # Human-readable task name
```

**Datasheets `Task` class**:
```yaml
Task:
  description: Dataset purpose/task
  slots:
    - description  # What task the dataset supports
```

**Resolution**: Rename model cards `Task` → `BenchmarkTask`

#### 2. Language Slot Conflict

**Model Cards `language` slot**:
```yaml
language:
  description: Natural language(s) processed by the model
  multivalued: true
  range: string
  # Example: ["en", "fr", "es"]
```

**Datasheets `language` slot** (assumed based on standard dataset metadata):
```yaml
language:
  description: Dataset language/locale
```

**Resolution**: Rename model cards `language` → `model_language`

---

## D4D Harmonization: External Reference Pattern (IMPLEMENTED)

### Pattern Overview

The D4D harmonized schema (`model_card_schema_d4dharmonized.yaml`) implements the external reference pattern, providing three new reference structure classes:

1. **CreatorReference**: References to D4D Creator instances (replaces `owner` and `Contributor`)
2. **DatasetReference**: References to D4D Dataset instances (replaces `dataSet`)
3. **GrantReference**: References to D4D Grant instances (replaces `funding_source`)

**Model Card with D4D References** (Actual Implementation):
```yaml
# climate-forecasting-model-card.yaml
schema_version: d4d-1.0

# NEW: Provenance metadata
created_by: Jane Smith
modified_by: Jane Smith
created_on: 2025-01-15T10:00:00Z
modified_on: 2025-01-20T14:30:00Z

model_details:
  name: "Climate Forecasting Transformer v2.1"

  # NEW: References to D4D Creator instances
  creator_references:
    - url: file://./creators/jane-smith-creator.yaml
      description: Principal Investigator and Lead Developer
    - url: file://./creators/climate-ai-lab-creator.yaml
      description: Research organization

model_parameters:
  # NEW: References to D4D Dataset instances
  training_datasets:
    - url: file://./datasets/noaa-historical-climate-dataset.yaml
      description: Primary training data - 50 years of NOAA climate observations

  evaluation_datasets:
    - url: file://./datasets/noaa-test-dataset.yaml
      description: Held-out test set - 2020-2024 observations

mission_relevance:
  # NEW: References to D4D Grant instances
  funding_grants:
    - url: file://./grants/doe-scidac-grant.yaml
      description: Primary funding - DOE SciDAC Climate Modeling
```

**Benefits**:
- No schema conflicts or imports required
- Datasets/creators/grants documented once using full D4D schema, referenced many times
- Clean separation of concerns
- Works with current tooling
- Backward compatible migration path
- Comprehensive documentation (7 fields → 200+ fields for datasets)

### Pattern 2: Embedded Minimal Dataset Info (Backward Compatible)

Keep using the current simple `dataSet` class for basic info, with pointers to full datasheets:

```yaml
model_parameters:
  data:
    - name: "IMDb Reviews"
      link: "https://ai.stanford.edu/~amaas/data/sentiment/"
      description: "50,000 movie reviews"

      # NEW: Reference to full datasheet
      datasheet_url: "https://example.org/datasheets/imdb-reviews-v1.yaml"
      datasheet_doi: "10.xxxx/xxxxx"
```

### Pattern 3: Hybrid Approach (Future Phase 2+)

After resolving naming conflicts, selectively import specific datasheets classes:

```yaml
# Future modelcards_v2.yaml
imports:
  - linkml:types
  # Import only specific classes, not the whole schema
  - ../../../data-sheets-schema/src/data_sheets_schema/schema/D4D_Base_import

# Then explicitly map what we need
classes:
  ModelParameters:
    slots:
      - training_data:
          range: data_sheets_schema:Dataset  # Explicit prefix
```

---

## Implementation Status

### Phase 1: Foundation and D4D Harmonization - COMPLETED ✅

**Status**: COMPLETED (November 23, 2025)

**Completed Tasks**:
- ✅ Created `ALIGNMENT_ANALYSIS.md` (comprehensive schema comparison)
- ✅ Created `model_card_schema_d4dharmonized.yaml` (production-ready D4D harmonized schema)
- ✅ Identified and documented naming conflicts (Task, language, etc.)
- ✅ Implemented external reference pattern (no schema imports)
- ✅ Created comprehensive D4D integration examples:
  - `src/data/examples/d4d_integration/climate-forecasting-model-card.yaml`
  - `src/data/examples/d4d_integration/creators/` (2 Creator examples)
  - `src/data/examples/d4d_integration/datasets/` (1 Dataset example)
  - `src/data/examples/d4d_integration/grants/` (1 Grant example)
  - `src/data/examples/d4d_integration/README.md` (comprehensive usage guide)
- ✅ Added provenance metadata support (created_by, modified_by, created_on, modified_on)
- ✅ Replaced deprecated classes:
  - `owner` → `CreatorReference`
  - `Contributor` → `CreatorReference` (with D4D CRediT roles)
  - `dataSet` → `DatasetReference`
  - `SensitiveData` → Part of D4D Dataset
  - `funding_source` → `GrantReference`

**Schema Changes**:
- Removed: `owner`, `Contributor`, `ContributorRoleEnum`, `dataSet`, `SensitiveData` classes
- Added: `CreatorReference`, `DatasetReference`, `GrantReference` classes
- Added: Provenance metadata slots
- Updated: `ModelDetails`, `ModelParameters`, `MissionRelevance`, `modelCard` root

### Phase 2: Practical Integration (Months 3-6)

**Goals**:
- Resolve naming conflicts (rename classes/slots)
- Create conversion utilities
- Build example model cards using both schemas

**Tasks**:
1. **Rename conflicting elements** in model cards schema:
   - `Task` → `BenchmarkTask` ✅ (already done in harmonized schema)
   - `language` → `model_language`
   - Discover and resolve any additional conflicts

2. **Create conversion utilities**:
   - Script to convert old model cards to new format
   - Script to generate dataset references
   - Validation tools

3. **Build examples**:
   - Complete model card with datasheets references
   - Migration examples (before/after)
   - Integration patterns demonstration

### Phase 3: Advanced Features (Months 7-8)

**Goals**:
- Full datasheets integration
- Enhanced ethics/provenance tracking
- Production tooling

**Tasks**:
1. Test full schema import after conflict resolution
2. Generate artifacts from harmonized schema
3. Create comprehensive examples
4. Build validation suite

### Phase 4: Ecosystem (Month 9)

**Goals**:
- Community engagement
- Documentation
- Release v2.0

**Tasks**:
1. Final documentation
2. Migration guide
3. Community review
4. Release planning

---

## Example: Model Card with Datasheets References

### Minimal Example (Pattern 1)

```yaml
# examples/sentiment-classifier-with-datasheets.yaml
schema_version: "0.0.2"

model_details:
  name: "BERT Sentiment Classifier"
  overview: "Fine-tuned BERT model for binary sentiment classification"
  owners:
    - name: "ML Research Team"
      contact: "ml-team@example.org"

model_parameters:
  model_architecture: "BERT-base (110M parameters) + dense classification head"

  # CURRENT APPROACH: Simple references
  training_dataset_refs:
    - id: "imdb-sentiment-v1"
      url: "https://datasheets.example.org/imdb-sentiment-v1"
      name: "IMDb Movie Reviews"
      description: "50,000 polar movie reviews"
      format: "datasheets-for-datasets"

  # The actual dataset is documented separately using datasheets schema
  # See: https://datasheets.example.org/imdb-sentiment-v1.yaml

quantitative_analysis:
  performance_metrics:
    - type: "accuracy"
      value: 0.92
      confidence_interval:
        lower_bound: 0.91
        upper_bound: 0.93
```

### Corresponding Datasheet (Separate File)

```yaml
# datasheets/imdb-sentiment-v1.yaml (using datasheets schema)
id: "imdb-sentiment-v1"
name: "IMDb Movie Reviews Sentiment Dataset"
description: "50,000 highly polar movie reviews for binary sentiment classification"

download_url: "https://ai.stanford.edu/~amaas/data/sentiment/"
doi: "10.18653/v1/P11-1015"

purposes:
  - description: "Enable sentiment analysis research"

creators:
  - principal_investigator:
      name: "Andrew L. Maas"
      orcid: "0000-0002-xxxx-xxxx"
      affiliation:
        name: "Stanford University"

composition:
  instances:
    - instance_count: 50000
      description: "Movie reviews with binary sentiment labels"

  subsets:
    - name: "train"
      instance_count: 25000
    - name: "test"
      instance_count: 25000

# ... full datasheets documentation (60+ fields)
```

---

## Migration Strategy

### For Existing Model Cards

**Option A: Minimal Change**
1. Keep current model card format
2. Add `datasheet_url` field to existing `dataSet` entries
3. Create separate datasheet files for each dataset

**Option B: Full Migration** (Future Phase 2+)
1. Rename model card elements to avoid conflicts
2. Replace `dataSet` references with `Dataset` class from datasheets
3. Migrate creator info to datasheets `Person`/`Organization`

### Example Migration

**Before (Current)**:
```yaml
owners:
  - name: "Jane Doe"
    contact: "jane@example.com"

model_parameters:
  data:
    - name: "IMDb"
      link: "https://example.com/imdb"
      description: "Movie reviews"
```

**After (Phase 1 - External References)**:
```yaml
owners:
  - name: "Jane Doe"
    contact: "jane@example.com"

model_parameters:
  training_dataset_refs:
    - id: "imdb-v1"
      datasheet_url: "https://datasheets.example.org/imdb-v1.yaml"
      name: "IMDb Reviews"
```

**After (Phase 2+ - Full Harmonization)**:
```yaml
creators:
  - given_name: "Jane"
    family_name: "Doe"
    email: "jane@example.com"
    orcid: "0000-0002-1234-5678"

model_parameters:
  training_data:  # Direct Dataset reference
    - id: "imdb-v1"
      name: "IMDb Movie Reviews"
      # Full datasheets Dataset object
      purposes: [...]
      creators: [...]
      composition: [...]
      # etc.
```

---

## Technical Notes

### Import Challenges

**Issue**: LinkML import mechanism requires unique element names across all imported schemas.

**Current Conflicts**:
- `Task` class (both schemas)
- `language` slot (both schemas)
- Potentially others (to be discovered during full merge)

**Solutions**:
1. **Namespace prefixes**: Use `data_sheets_schema:Dataset` syntax (tested - has issues)
2. **Selective imports**: Import only specific submodules
3. **Element renaming**: Rename conflicting elements in one schema
4. **External references**: Don't import, just reference (Pattern 1)

**Recommendation**: Use Pattern 1 (external references) for Phase 1, resolve conflicts for Phase 2+.

### Tools Needed

1. **Validator**: Check model cards reference valid datasheets
2. **Converter**: Migrate old format to new format
3. **Generator**: Create stub datasheets from simple dataset info
4. **Linker**: Link model cards to datasheets in repositories

---

## Next Steps

### Immediate (Phase 1 - This Month)

1. ✅ Document naming conflicts (this guide)
2. Create example model card using Pattern 1
3. Create example datasheet for referenced dataset
4. Update `CLAUDE.md` with integration approach

### Short-term (Phase 2 - Months 3-6)

1. Resolve naming conflicts in schemas
2. Test full import after renaming
3. Create migration scripts
4. Build comprehensive examples

### Long-term (Phases 3-4 - Months 7-9)

1. Production tooling
2. Community engagement
3. Release v2.0 with full integration

---

## Conclusion

The integration of Model Cards with Datasheets for Datasets is **highly valuable but requires careful phased implementation**. The conceptual design in `modelcards_harmonized.yaml` demonstrates the vision, while this guide provides the practical roadmap.

**Key Takeaway**: Start with external references (Pattern 1), gradually adopt full integration as conflicts are resolved.

---

## References

### Documentation

- **D4D_HARMONIZATION.md**: Comprehensive guide to D4D harmonization (to be created)
- **ALIGNMENT_ANALYSIS.md**: Detailed schema comparison analysis
- **CLAUDE.md**: Repository guide with D4D harmonization section
- **src/data/examples/d4d_integration/README.md**: Complete usage guide for D4D integration

### Schemas

- **model_card_schema_d4dharmonized.yaml**: Production D4D harmonized schema (`src/model_card_schema/schema/`)
- **model_card_schema.yaml**: Base schema without D4D integration (`src/model_card_schema/schema/`)
- **Datasheets Schema**: https://github.com/bridge2ai/data-sheets-schema

### Examples

- **Climate Forecasting Model Card**: `src/data/examples/d4d_integration/climate-forecasting-model-card.yaml`
- **Creator Examples**: `src/data/examples/d4d_integration/creators/`
- **Dataset Example**: `src/data/examples/d4d_integration/datasets/noaa-historical-climate-dataset.yaml`
- **Grant Example**: `src/data/examples/d4d_integration/grants/doe-scidac-grant.yaml`

### Papers

- **Model Cards Paper**: Mitchell et al., 2019 - https://arxiv.org/abs/1810.03993
- **Datasheets for Datasets Paper**: Gebru et al., 2018 - https://arxiv.org/abs/1803.09010
- **LinkML Documentation**: https://linkml.io/

---

**Document Status**: Phase 1 COMPLETED. Updated November 23, 2025.
