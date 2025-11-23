# Model Cards + Datasheets Integration Guide

**Version**: 1.0
**Date**: November 22, 2025
**Status**: Phase 1 Implementation

---

## Executive Summary

This guide provides a practical approach to integrating Model Cards with Datasheets for Datasets. While the `modelcards_harmonized.yaml` schema demonstrates the conceptual design, technical challenges require a phased implementation approach.

**Key Finding**: Direct schema merge via LinkML imports encounters naming conflicts that require careful resolution.

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

## Recommended Integration Patterns

### Pattern 1: External References (Recommended for Phase 1)

Instead of importing the entire datasheets schema, use external references:

**Model Card with Dataset References**:
```yaml
# modelcard_example.yaml
schema_version: "0.0.2"

model_details:
  name: "bert-sentiment-classifier"
  overview: "BERT-based sentiment analysis model"

model_parameters:
  model_architecture: "BERT-base with classification head"

  # REFERENCE to external datasheets documentation
  training_dataset_refs:
    - dataset_id: "imdb-reviews-v1"
      dataset_url: "https://example.org/datasheets/imdb-reviews-v1.yaml"
      dataset_type: "datasheets-for-datasets"

  evaluation_dataset_refs:
    - dataset_id: "sst2-v1"
      dataset_url: "https://example.org/datasheets/sst2-v1.yaml"
      dataset_type: "datasheets-for-datasets"
```

**Benefits**:
- No schema conflicts
- Datasets documented once, referenced many times
- Clean separation of concerns
- Works with current tooling

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

## Practical Implementation Steps

### Phase 1: Foundation (Current - Month 2)

**Status**: IN PROGRESS

**Completed**:
- ✅ Created `ALIGNMENT_ANALYSIS.md` (comprehensive analysis)
- ✅ Created `modelcards_harmonized.yaml` (conceptual design)
- ✅ Identified naming conflicts (Task, language)
- ✅ Tested import mechanisms

**Remaining**:
- [ ] Document all naming conflicts
- [ ] Create reference examples using Pattern 1 (external references)
- [ ] Update `CLAUDE.md` with integration guidance

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

- **ALIGNMENT_ANALYSIS.md**: Comprehensive 50,000+ word analysis of schema alignment
- **modelcards_harmonized.yaml**: Proposed harmonized schema (conceptual design)
- **Model Cards Paper**: Mitchell et al., 2019 - https://arxiv.org/abs/1810.03993
- **Datasheets for Datasets Paper**: Gebru et al., 2018
- **LinkML Documentation**: https://linkml.io/

---

**Document Status**: Living document, will be updated as implementation progresses.
